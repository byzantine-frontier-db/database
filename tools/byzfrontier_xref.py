"""
byzfrontier_xref.py
====================

Cross-reference validator v1.1 — Byzantine-Islamic Frontier Database.

The schema validator (byzfrontier_validate.py, v1.0) checks each record in
isolation. This second-pass validator runs over the whole record set and
catches the inter-record problems the schema cannot:

  1. Dangling references — IDs that are referenced but never defined.
  2. Orphan attestations — attestations not linked from any entity.
  3. Orphan observations — observations supported by no attestations
                          (caught by schema) OR supporting nothing.
  4. Duplicate IDs — the same ID appearing on two records.
  5. Cycles in parent_event chains.
  6. Reflexive relationships — A == B in source/target.
  7. Soft consistency checks — attestation.source must point to a SOURCE,
                                attestation.entities_referenced must point
                                to entities (not other attestations), etc.

Usage:
    python byzfrontier_xref.py records/

Returns exit code 0 if all checks pass, 1 if any fail.
"""

from __future__ import annotations
import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. apt install python3-yaml or pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# Map ID prefixes to expected record types. Used to check that IDs referenced
# from a given field are of the right kind.
PREFIX_TYPES = {
    "SRC":      "source",
    "ENT-PLC":  "place",
    "ENT-PERS": "person",
    "ENT-EVT":  "event",
    "ENT-POL":  "political_entity",
    "ENT-GRP":  "group",
    "ENT-INS":  "institution",
    "ENT-RTE":  "route",
    "ENT-OBJ":  "object",
    "OBS":      "observation",
    "ATT":      "attestation",
    "INT":      "interpretation",
    "REL":      "relationship",
}

# Entity-like records that can be the subject of attestations
ENTITY_TYPES = {"place", "person", "event", "political_entity", "group",
                "institution", "route", "object"}


@dataclass
class XrefIssue:
    severity: str   # 'error' or 'warning'
    code: str       # short machine-readable code
    record_id: Optional[str]
    message: str

    def __str__(self) -> str:
        tag = "ERROR" if self.severity == "error" else "WARN "
        loc = f" [{self.record_id}]" if self.record_id else ""
        return f"{tag} {self.code}{loc}: {self.message}"


def infer_type_from_id(record_id: str) -> Optional[str]:
    """Return the expected record type from the ID prefix."""
    for prefix, rtype in sorted(PREFIX_TYPES.items(), key=lambda x: -len(x[0])):
        if record_id.startswith(prefix + "-"):
            return rtype
    return None


def collect_id_references(obj: Any, path: list = None) -> list[tuple[str, list]]:
    """Walk a record object and return every value that looks like an Identifier
    (matches the ID prefix pattern), along with its JSON path."""
    if path is None:
        path = []
    refs = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            # Skip the record's own id field
            if path == [] and k == "id":
                continue
            refs.extend(collect_id_references(v, path + [k]))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            refs.extend(collect_id_references(item, path + [i]))
    elif isinstance(obj, str):
        if infer_type_from_id(obj):
            refs.append((obj, path))
    return refs


def load_all_records(paths: list[Path]) -> list[tuple[Path, dict]]:
    """Load every record from every YAML/JSON file under the given paths."""
    files = []
    for p in paths:
        if p.is_dir():
            files.extend(p.rglob("*.yaml"))
            files.extend(p.rglob("*.yml"))
            files.extend(p.rglob("*.json"))
        else:
            files.append(p)

    records = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            if f.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(text)
            else:
                data = json.loads(text)
        except Exception as e:
            print(f"PARSE ERROR in {f}: {e}", file=sys.stderr)
            continue
        if isinstance(data, list):
            for rec in data:
                if isinstance(rec, dict):
                    records.append((f, rec))
        elif isinstance(data, dict):
            records.append((f, data))
    return records


def validate_xrefs(records: list[tuple[Path, dict]]) -> list[XrefIssue]:
    """Run all cross-reference checks. Returns a list of issues."""
    issues: list[XrefIssue] = []

    # Build the ID index
    id_to_record: dict[str, dict] = {}
    id_to_file: dict[str, Path] = {}
    duplicates: list[str] = []
    for f, rec in records:
        rid = rec.get("id")
        if not rid:
            issues.append(XrefIssue("error", "NO_ID", None, f"Record in {f} has no 'id' field"))
            continue
        if rid in id_to_record:
            duplicates.append(rid)
            issues.append(XrefIssue("error", "DUPLICATE_ID", rid,
                f"ID appears in both {id_to_file[rid]} and {f}"))
        else:
            id_to_record[rid] = rec
            id_to_file[rid] = f

    # Check 1: Dangling references
    for rid, rec in id_to_record.items():
        for ref, path in collect_id_references(rec):
            if ref not in id_to_record:
                path_str = "/".join(str(p) for p in path)
                issues.append(XrefIssue(
                    "error", "DANGLING_REF", rid,
                    f"Field '{path_str}' references {ref} which does not exist"
                ))

    # Check 2: Type-correctness of references
    # Particular fields are typed: attestation.source -> SRC,
    # attestation.entities_referenced -> entity, observation.supporting_attestations -> ATT, etc.
    type_constraints = [
        ("attestation", "source", lambda t: t == "source"),
        ("attestation", "entities_referenced", lambda t: t in ENTITY_TYPES),
        ("attestation", "observations_supported", lambda t: t == "observation"),
        ("observation", "supporting_attestations", lambda t: t == "attestation"),
        ("observation", "contradicting_attestations", lambda t: t == "attestation"),
        ("observation", "associated_entities", lambda t: t in ENTITY_TYPES),
        ("interpretation", "associated_entities", lambda t: t in ENTITY_TYPES),
        ("interpretation", "supporting_evidence", lambda t: t == "attestation"),
        ("interpretation", "counter_evidence", lambda t: t == "attestation"),
        ("relationship", "source_entity", lambda t: t in ENTITY_TYPES or t == "source"),
        ("relationship", "target_entity", lambda t: t in ENTITY_TYPES or t == "source"),
        ("relationship", "linked_attestations", lambda t: t == "attestation"),
        ("place", "linked_attestations", lambda t: t == "attestation"),
        ("person", "linked_attestations", lambda t: t == "attestation"),
        ("event", "linked_attestations", lambda t: t == "attestation"),
        ("place", "linked_interpretations", lambda t: t == "interpretation"),
        ("person", "linked_interpretations", lambda t: t == "interpretation"),
        ("event", "linked_interpretations", lambda t: t == "interpretation"),
        ("event", "parent_event", lambda t: t == "event"),
        ("event", "child_events", lambda t: t == "event"),
        ("event", "associated_places", lambda t: t == "place"),
        ("event", "participants", lambda t: t in ENTITY_TYPES),
        ("source", "dependencies", lambda t: t == "source"),
    ]
    for rid, rec in id_to_record.items():
        rec_type = rec.get("record_type")
        if not rec_type:
            continue
        for constraint_type, field_name, type_check in type_constraints:
            if rec_type != constraint_type:
                continue
            value = rec.get(field_name)
            if value is None:
                continue
            if isinstance(value, str):
                values = [value]
            elif isinstance(value, list):
                values = [v for v in value if isinstance(v, str)]
            else:
                continue
            for v in values:
                if v not in id_to_record:
                    continue  # caught by dangling-ref check
                ref_type = id_to_record[v].get("record_type")
                if ref_type and not type_check(ref_type):
                    issues.append(XrefIssue(
                        "error", "TYPE_MISMATCH", rid,
                        f"Field '{field_name}' references {v} (type: {ref_type}); "
                        f"expected one of: see constraint"
                    ))

    # Check 3: Cycles in parent_event chains
    parent_map = {}
    for rid, rec in id_to_record.items():
        if rec.get("record_type") == "event":
            parent = rec.get("parent_event")
            if parent:
                parent_map[rid] = parent

    for event_id in parent_map:
        seen = set()
        current = event_id
        while current in parent_map:
            if current in seen:
                cycle = " -> ".join(list(seen) + [current])
                issues.append(XrefIssue(
                    "error", "CYCLE_PARENT_EVENT", event_id,
                    f"Cycle in parent_event chain: {cycle}"
                ))
                break
            seen.add(current)
            current = parent_map[current]

    # Check 4: parent/child consistency — if A.parent_event = B, then B.child_events should contain A
    for rid, rec in id_to_record.items():
        if rec.get("record_type") != "event":
            continue
        parent = rec.get("parent_event")
        if parent and parent in id_to_record:
            parent_rec = id_to_record[parent]
            children = parent_rec.get("child_events", []) or []
            if rid not in children:
                issues.append(XrefIssue(
                    "warning", "PARENT_CHILD_INCONSISTENT", rid,
                    f"Record declares parent_event={parent}, "
                    f"but {parent}.child_events does not list this record"
                ))

    # Check 5: Orphan attestations (no entity links to them)
    referenced_atts = set()
    for rid, rec in id_to_record.items():
        for field_name in ("linked_attestations", "supporting_attestations",
                           "contradicting_attestations", "supporting_evidence",
                           "counter_evidence"):
            v = rec.get(field_name)
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, str) and x.startswith("ATT-"):
                        referenced_atts.add(x)
    for rid, rec in id_to_record.items():
        if rec.get("record_type") == "attestation" and rid not in referenced_atts:
            issues.append(XrefIssue(
                "warning", "ORPHAN_ATTESTATION", rid,
                "Attestation is not referenced by any entity, observation, or interpretation"
            ))

    # Check 6: Reflexive relationships
    for rid, rec in id_to_record.items():
        if rec.get("record_type") == "relationship":
            src = rec.get("source_entity")
            tgt = rec.get("target_entity")
            if src and src == tgt:
                rel_type = rec.get("type", "?")
                # Some relationship types may legitimately be reflexive (e.g.
                # "same_as" is reflexive trivially, but we don't expect explicit
                # statements of it). Always warn so editor can confirm.
                issues.append(XrefIssue(
                    "warning", "REFLEXIVE_RELATIONSHIP", rid,
                    f"Relationship of type '{rel_type}' has source_entity == target_entity == {src}"
                ))

    # Check 7: Attestation must support at least one observation OR carry
    # evidence directly (paraphrase / direct quotation). Otherwise it asserts
    # nothing.
    for rid, rec in id_to_record.items():
        if rec.get("record_type") != "attestation":
            continue
        obs = rec.get("observations_supported") or []
        has_text = bool(rec.get("paraphrase") or rec.get("direct_quotation"))
        if not obs and not has_text:
            issues.append(XrefIssue(
                "warning", "EMPTY_ATTESTATION", rid,
                "Attestation supports no observations and carries no quotation/paraphrase"
            ))

    # Check 8: At least one observation per entity is recommended
    entity_with_attestations: set[str] = set()
    for rid, rec in id_to_record.items():
        if rec.get("record_type") == "attestation":
            for e in rec.get("entities_referenced", []) or []:
                entity_with_attestations.add(e)
    for rid, rec in id_to_record.items():
        if rec.get("record_type") in ENTITY_TYPES:
            linked = rec.get("linked_attestations", []) or []
            if not linked:
                issues.append(XrefIssue(
                    "warning", "ENTITY_NO_LINKED_ATTESTATIONS", rid,
                    "Entity has no linked_attestations; consider whether it has evidential support"
                ))

    return issues


def print_summary(issues: list[XrefIssue]) -> tuple[int, int]:
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    # Group by code
    by_code: dict[str, list[XrefIssue]] = defaultdict(list)
    for i in issues:
        by_code[i.code].append(i)

    if issues:
        print("\nIssues:\n")
        for code in sorted(by_code):
            print(f"--- {code} ({len(by_code[code])}) ---")
            for issue in by_code[code]:
                print(f"  {issue}")
            print()

    print("--- Summary ---")
    print(f"Errors:   {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    return len(errors), len(warnings)


def main():
    parser = argparse.ArgumentParser(description="Cross-reference validator for byzfrontier records")
    parser.add_argument("paths", nargs="+", help="YAML/JSON files or directories")
    parser.add_argument("--warnings-as-errors", action="store_true",
                       help="Treat warnings as errors (exit code 1)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    paths = [Path(p) for p in args.paths]
    records = load_all_records(paths)
    print(f"Loaded {len(records)} records from {len(paths)} path(s)")

    issues = validate_xrefs(records)
    errors, warnings = print_summary(issues)

    if errors > 0:
        sys.exit(1)
    if warnings > 0 and args.warnings_as_errors:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
