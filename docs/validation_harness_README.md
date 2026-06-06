# Record Validation Harness

## Byzantine-Islamic Frontier Database

The validation harness checks that records conform to `byzfrontier_schema_v1.json` before they enter the database. It runs locally (for contributors) and in CI (for pull requests).

## Files

- `byzfrontier_validate.py` — the validator. A self-contained JSON Schema Draft 2020-12 validator implementing the keyword subset used by the project schema. No external dependencies beyond PyYAML.
- `byzfrontier_schema_v1.json` — the schema being validated against.
- `validate_records.yml` — GitHub Actions workflow that runs validation on pull requests. Place at `.github/workflows/validate_records.yml` in the repository.

## Local use

Contributors should run the validator on any record they intend to submit:

```bash
python byzfrontier_validate.py \
    --schema byzfrontier_schema_v1.json \
    records/my_new_records.yaml
```

The validator accepts YAML or JSON files and directories of either. When given a directory it recursively validates every `.yaml`, `.yml`, and `.json` file. Exit code is 0 if all records pass, 1 if any fail.

Verbose mode reports each successful file:

```bash
python byzfrontier_validate.py \
    --schema byzfrontier_schema_v1.json \
    --verbose \
    records/
```

## Output format

For each failing record, the validator prints the record's path and identifier followed by an indented list of errors with their JSON paths:

```
FAIL records/places/amorium.yaml::ENT-PLC-0001
  at <root>: missing required property 'analytical_summary'
  at coordinates: missing required property 'crs'
  at alternative_names/2/name_type: value 'greek_form' not in enum: [...]
```

A summary block at the end reports totals:

```
--- Summary ---
Records validated: 247
Files with errors: 3 / 89
Total errors:      11
```

## CI integration

The `validate_records.yml` workflow runs on every pull request that touches records, the schema, or the validator. It installs PyYAML, runs the validator on the `records/` directory in verbose mode, and fails the build if any record fails. The PR cannot be merged until all records pass.

The validator deliberately has no other dependencies. PyYAML is in Debian Python by default and trivial to install; no NPM or other ecosystem is required. The CI workflow therefore runs reliably regardless of network conditions.

## Extending the validator

The validator implements the following JSON Schema keywords: `type`, `enum`, `const`, `pattern`, `required`, `properties`, `additionalProperties`, `items`, `minItems`, `maxItems`, `minLength`, `minimum`, `maximum`, `$ref` (local refs only), `$defs`, `oneOf`, `allOf`, `anyOf`, and the `format` values `date`, `date-time`, and `uri`.

Keywords not supported (silently passed): `if`/`then`/`else`, `dependentRequired`, `dependentSchemas`, `contains`, `$dynamicRef`, the full `format` vocabulary.

If a future schema change uses a keyword outside this set, the validator must be extended first. The validator's source is annotated to make extension straightforward.

## Calibration: ensuring the validator matches the schema's intent

The harness was tested during v1.0.0 development against the 37 records of Appendix C of the specification. Validation caught:

- 6 entity records missing the spec-mandated `analytical_summary` field
- 1 `name_type` value outside the enum
- 2 free-text `dependencies` entries that should be either omitted or modelled as Source records
- 1 free-text `target_entity` on a relationship that should be a proper identifier
- 1 schema bug (date pattern too restrictive for three-digit Byzantine years)
- 1 schema bug (`linked_attestations` over-strict on structural relationships)
- 1 missing `$defs` entry (`PersistentIdentifier` referenced but never defined)

Each was a real defect that prose review had missed. The validator is the correctness criterion for the schema, not the other way around: when the validator and the prose disagree, the validator wins.

## Performance

The validator is pure Python and uses only the standard library plus PyYAML. It processes the 37 Appendix C records in well under a second. A real database of tens of thousands of records is expected to validate in seconds rather than minutes. For larger scales, the validator's `_validate` method is straightforward to parallelise across files; this is not required at v1.0 volumes.

## Limitations and future work

1. No JSON Schema `$ref` resolution beyond `#/$defs/`. External schema imports are not supported.
2. No semantic validation beyond schema conformance — the validator does not check, for example, that an `attestation` references a `source` that actually exists. Cross-reference checking is a separate validator layer planned for v1.1.
3. No incremental validation — every record is validated independently. Cross-record consistency checks (orphan detection, dangling references, circular dependencies) require a second pass that operates over the whole record set.
4. No automatic formatting. YAML files must be valid YAML before validation; broken syntax produces a parse error rather than a schema error.
