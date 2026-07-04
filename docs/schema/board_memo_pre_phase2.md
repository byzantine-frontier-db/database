## Editorial Board Memo — Pre-Phase-2 Schema Batch

**To:** Editorial Board
**From:** Maintainer (Curtis)
**Re:** Three bundled schema changes ahead of the Eger 2008 gazetteer extraction (Phase 2)
**Decision required:** §5.6 schema change — Board majority (the batch is MAJOR overall)
**Accompanying detail:** full JSON diffs, rationale, and migration notes in
`schema_batch_pre_phase2.md`

---

### Summary

Phase 2 extracts A. Asa Eger's 2008 dissertation site-gazetteer (SRC-0065), whose Section-4
entries are dated first-person archaeological field observations. Capturing them faithfully
needs two additive schema elements; a third, already-migrated change is folded in so the
Board reviews one delta. The batch is proposed as a single commit, behind CI, separate from
all data commits.

| # | Change | §5.6 class | Migration | Decision |
|---|--------|-----------|-----------|----------|
| 1 | Add `primary_observation` to `ProvenanceCategory` | MINOR (broadened enum) | Additive; no record uses it yet | §5.5 + §5.6 Board majority |
| 2 | Add optional `observation_date` to `AttestationRecord` | MINOR (new optional field) | Additive; `required` unchanged | §5.6 Board majority |
| 3 | Make `editorial_review_required` required on `RecordMetadata` | MAJOR (required-set change) | **Already complete** — 1228/1228 records carry it | §5.6 Board majority + migration plan |

Because the batch contains a MAJOR change (3), the batch as a whole is treated as MAJOR:
Board majority plus the migration plan, a transition window in which both schema versions
validate, and a change-log entry.

### Rationale in brief

- **Change 1** — Eger's dated site autopsy ("Personal Observations, 7/20/05 … walking the
  east bank revealed no traces of a ruined castle") is primary observation by the author,
  evidentially distinct from `archaeological_evidence` (transmitted excavation/survey) and
  `modern_synthesis` (reading of prior scholarship). No existing enum value fits. The name
  follows the existing `primary_*` family and stays distinct from `gis_derived_observation`.
  §5.5's three-cases threshold is met many times over (~19 visited sites).
- **Change 2** — those observations are dated per visit, but no temporal field exists on
  ObservationRecord or AttestationRecord. Without it the date lives only in prose, which
  breaks the separation-of-levels principle (cf. editorial-workflow rule 8: structured data
  belongs in structured fields). It sits on the attestation (Eger's dated observing act),
  optional, so only field observations populate it.
- **Change 3** — carried from the post-Eger audit. The field gates draft→published but was
  never schema-enforced (163 records were silently missing it until back-fill). The
  2026-06-30 back-fill set it on every record, so making it required now invalidates nothing.

### Decisions requested

- **D1** — Approve `primary_observation` and its name (vs `field_observation` / `autopsy`)?
- **D2** — Approve `observation_date` on AttestationRecord; type as the self-contained
  `{date, precision}` object, or align it with `EventRecord.start_date`'s temporal type for
  consistency?
- **D3** — For Change 3: ship the property *definition* (a PATCH) before promoting to
  `required` (the MAJOR step), or do both together? Also raise: optional
  `additionalProperties: false` hardening on RecordMetadata (separate, needs a stray-key
  scan first), and the `schema_version` const cascade a MAJOR bump implies.

### Process

On approval: apply as one schema-only commit; run the validation harness against the full
1228-record corpus (must stay at 0 errors); record all three in the change log; bump the
schema version MAJOR. No data commit rides along.
