"""
byzfrontier_validate.py
A minimal JSON Schema Draft 2020-12 validator implementing the keyword subset
used by byzfrontier_schema_v1.json. Self-contained — no external dependencies
beyond PyYAML (which is in Debian Python by default).

Supported keywords: type, enum, const, pattern, required, properties,
additionalProperties, items, minItems, maxItems, minLength, minimum, maximum,
$ref (local only), $defs, oneOf, allOf, anyOf, format (date / date-time / uri).

Not supported (will silently pass): if/then/else, dependentRequired,
dependentSchemas, contains, $dynamicRef, full format vocabulary.

Usage:
    from byzfrontier_validate import Validator
    v = Validator.from_file("byzfrontier_schema_v1.json")
    errors = v.validate(record_dict)
    if errors:
        for e in errors: print(e)
"""

from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ValidationError:
    path: list
    message: str

    def __str__(self) -> str:
        loc = "/".join(str(p) for p in self.path) or "<root>"
        return f"  at {loc}: {self.message}"


class Validator:
    def __init__(self, schema: dict):
        self.schema = schema
        self.defs = schema.get("$defs", {})

    @classmethod
    def from_file(cls, path: str | Path) -> "Validator":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def validate(self, instance: Any) -> list[ValidationError]:
        errors: list[ValidationError] = []
        self._validate(instance, self.schema, [], errors)
        return errors

    def _resolve_ref(self, ref: str) -> dict:
        # Only #/$defs/Name supported
        if not ref.startswith("#/$defs/"):
            raise ValueError(f"Unsupported ref form: {ref}")
        name = ref[len("#/$defs/"):]
        if name not in self.defs:
            raise ValueError(f"Unknown $defs entry: {name}")
        return self.defs[name]

    def _validate(self, instance: Any, schema: dict, path: list, errors: list[ValidationError]) -> None:
        if "$ref" in schema:
            self._validate(instance, self._resolve_ref(schema["$ref"]), path, errors)
            return

        if "oneOf" in schema:
            matches = []
            sub_errors_per_branch = []
            for i, sub in enumerate(schema["oneOf"]):
                sub_errs: list[ValidationError] = []
                self._validate(instance, sub, path, sub_errs)
                if not sub_errs:
                    matches.append(i)
                sub_errors_per_branch.append((i, sub_errs))
            if len(matches) == 0:
                # Choose the branch with the fewest errors as the "intended" branch
                best = min(sub_errors_per_branch, key=lambda x: len(x[1]))
                errors.append(ValidationError(path, f"does not match any oneOf branch; best fit was branch {best[0]} with {len(best[1])} errors"))
                errors.extend(best[1])
                return
            elif len(matches) > 1:
                errors.append(ValidationError(path, f"matches multiple oneOf branches: {matches}"))
                return

        if "allOf" in schema:
            for sub in schema["allOf"]:
                self._validate(instance, sub, path, errors)

        if "anyOf" in schema:
            any_match = False
            collected: list[ValidationError] = []
            for sub in schema["anyOf"]:
                sub_errs: list[ValidationError] = []
                self._validate(instance, sub, path, sub_errs)
                if not sub_errs:
                    any_match = True
                    break
                collected.extend(sub_errs)
            if not any_match:
                errors.append(ValidationError(path, "does not match any anyOf branch"))
                errors.extend(collected)
                return

        # Type
        if "type" in schema:
            self._check_type(instance, schema["type"], path, errors)

        # Const
        if "const" in schema:
            if instance != schema["const"]:
                errors.append(ValidationError(path, f"expected const {schema['const']!r}, got {instance!r}"))

        # Enum
        if "enum" in schema:
            if instance not in schema["enum"]:
                preview = schema["enum"][:5]
                more = "" if len(schema["enum"]) <= 5 else f" (and {len(schema['enum'])-5} more)"
                errors.append(ValidationError(path, f"value {instance!r} not in enum: {preview}{more}"))

        # String validations
        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                errors.append(ValidationError(path, f"string shorter than minLength {schema['minLength']}"))
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                errors.append(ValidationError(path, f"string longer than maxLength {schema['maxLength']}"))
            if "pattern" in schema:
                if not re.search(schema["pattern"], instance):
                    errors.append(ValidationError(path, f"string {instance!r} does not match pattern {schema['pattern']!r}"))
            if "format" in schema:
                if not self._check_format(instance, schema["format"]):
                    errors.append(ValidationError(path, f"string {instance!r} not valid {schema['format']}"))

        # Number validations
        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                errors.append(ValidationError(path, f"value {instance} below minimum {schema['minimum']}"))
            if "maximum" in schema and instance > schema["maximum"]:
                errors.append(ValidationError(path, f"value {instance} above maximum {schema['maximum']}"))

        # Array validations
        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                errors.append(ValidationError(path, f"array has {len(instance)} items, minItems is {schema['minItems']}"))
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                errors.append(ValidationError(path, f"array has {len(instance)} items, maxItems is {schema['maxItems']}"))
            if "items" in schema:
                for i, item in enumerate(instance):
                    self._validate(item, schema["items"], path + [i], errors)

        # Object validations
        if isinstance(instance, dict):
            if "required" in schema:
                for req in schema["required"]:
                    if req not in instance:
                        errors.append(ValidationError(path, f"missing required property {req!r}"))
            if "properties" in schema:
                for prop_name, prop_schema in schema["properties"].items():
                    if prop_name in instance:
                        self._validate(instance[prop_name], prop_schema, path + [prop_name], errors)
            if schema.get("additionalProperties") is False and "properties" in schema:
                allowed = set(schema["properties"].keys())
                for k in instance.keys():
                    if k not in allowed:
                        errors.append(ValidationError(path, f"additional property {k!r} not allowed"))

    def _check_type(self, instance: Any, type_value: str | list, path: list, errors: list[ValidationError]) -> None:
        if isinstance(type_value, list):
            ok = any(self._is_type(instance, t) for t in type_value)
            if not ok:
                errors.append(ValidationError(path, f"value {instance!r} is not of type {type_value}"))
        else:
            if not self._is_type(instance, type_value):
                errors.append(ValidationError(path, f"value {instance!r} is not of type {type_value!r}"))

    def _is_type(self, instance: Any, type_name: str) -> bool:
        if type_name == "null":
            return instance is None
        if type_name == "boolean":
            return isinstance(instance, bool)
        if type_name == "integer":
            return isinstance(instance, int) and not isinstance(instance, bool)
        if type_name == "number":
            return isinstance(instance, (int, float)) and not isinstance(instance, bool)
        if type_name == "string":
            return isinstance(instance, str)
        if type_name == "array":
            return isinstance(instance, list)
        if type_name == "object":
            return isinstance(instance, dict)
        return False

    def _check_format(self, value: str, fmt: str) -> bool:
        if fmt == "date":
            return bool(re.fullmatch(r"-?\d{4}-\d{2}-\d{2}", value))
        if fmt == "date-time":
            return bool(re.fullmatch(r"-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?", value))
        if fmt == "uri":
            return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:", value))
        return True  # unknown formats pass


def cli_main():
    import argparse
    import sys
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. apt install python3-yaml", file=sys.stderr)
        sys.exit(2)

    parser = argparse.ArgumentParser(description="Validate Byzfrontier records against the schema.")
    parser.add_argument("--schema", required=True, action="append",
                        help="Path to a schema file. Repeatable: during the migration "
                             "transition window pass --schema for each of v1 and v2. Each "
                             "record is validated against the schema whose "
                             "RecordMetadata.schema_version const matches the record's "
                             "declared metadata.schema_version.")
    parser.add_argument("paths", nargs="+", help="YAML or JSON files / directories to validate")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    # {declared schema_version -> Validator} dispatch map (transition window). With a single
    # --schema this behaves exactly as before: that schema validates every record.
    schemas: dict = {}
    for spath in args.schema:
        sdoc = json.loads(Path(spath).read_text(encoding="utf-8"))
        ver = (sdoc.get("$defs", {}).get("RecordMetadata", {})
               .get("properties", {}).get("schema_version", {}).get("const"))
        schemas[ver] = Validator(sdoc)
    single = next(iter(schemas.values())) if len(schemas) == 1 else None

    def pick_validator(rec):
        if single is not None:
            return single
        ver = (rec.get("metadata") or {}).get("schema_version") if isinstance(rec, dict) else None
        return schemas.get(ver)

    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(path.rglob("*.yaml"))
            files.extend(path.rglob("*.yml"))
            files.extend(path.rglob("*.json"))
        else:
            files.append(path)

    total_records = 0
    total_errors = 0
    files_with_errors = 0

    for f in files:
        text = f.read_text(encoding="utf-8")
        try:
            if f.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(text)
            else:
                data = json.loads(text)
        except Exception as e:
            print(f"PARSE ERROR in {f}: {e}")
            total_errors += 1
            files_with_errors += 1
            continue

        records = data if isinstance(data, list) else [data]
        file_errors = 0
        for i, rec in enumerate(records):
            total_records += 1
            v = pick_validator(rec)
            if v is None:
                declared = (rec.get("metadata") or {}).get("schema_version") if isinstance(rec, dict) else None
                errs = [ValidationError(["metadata", "schema_version"],
                        f"no schema loaded for declared schema_version {declared!r} "
                        f"(loaded: {sorted(k for k in schemas)})")]
            else:
                errs = v.validate(rec)
            errs = errs + rule8_claim_present(rec)
            if errs:
                file_errors += len(errs)
                rec_id = rec.get("id", f"<record {i}>") if isinstance(rec, dict) else f"<record {i}>"
                print(f"\nFAIL {f}::{rec_id}")
                for e in errs:
                    print(e)
        if file_errors > 0:
            files_with_errors += 1
            total_errors += file_errors
        elif args.verbose:
            print(f"OK   {f} ({len(records)} record{'s' if len(records)!=1 else ''})")

    print(f"\n--- Summary ---")
    print(f"Records validated: {total_records}")
    print(f"Files with errors: {files_with_errors} / {len(files)}")
    print(f"Total errors:      {total_errors}")
    sys.exit(0 if total_errors == 0 else 1)



# --- Rule 8: the evidential claim must live in paraphrase/direct_quotation, not only in notes ---
# Universal form: every attestation must carry a non-empty paraphrase OR direct_quotation.
def rule8_claim_present(rec):
    errors = []
    if not isinstance(rec, dict) or rec.get("record_type") != "attestation":
        return errors
    para = (rec.get("paraphrase") or "").strip()
    dq = (rec.get("direct_quotation") or "").strip()
    if not para and not dq:
        errors.append(ValidationError(
            ["paraphrase"],
            f"rule 8: attestation {rec.get('id', '?')} (provenance "
            f"{rec.get('provenance')!r}) has empty 'paraphrase' and 'direct_quotation'; "
            f"the evidential claim must not live only in 'notes'"))
    return errors


if __name__ == "__main__":
    cli_main()
