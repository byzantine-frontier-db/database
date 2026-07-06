# Schema Backlog

Tracked schema follow-up items. Not part of any current commit.

## D3.i — `additionalProperties: false` on RecordMetadata (OPEN)

Board follow-up from the pre-Phase-2 schema batch. Setting `additionalProperties: false`
on `RecordMetadata` would prevent future undeclared metadata keys from slipping through
validation (the mechanism by which `editorial_review_required` went unenforced until the
2026-06-30 back-fill).

- **Type:** MAJOR schema change (can newly reject records) — Editorial Board approval + §5.6.
- **Diagnostic prerequisite (done):** a corpus-wide stray-key scan (2026-07-04) found
  **zero** non-schema keys in any record's `metadata`. The hardening would therefore break
  no existing record; it only guards against future stray keys.
- **Status:** ready to schedule as its own MAJOR change once the current v2 transition
  window closes. Re-run the stray-key scan immediately before applying, in case Phase 2
  extraction introduced any.

## D3.ii — schema_version cascade (POLICY APPROVED; migration in progress)

Lazy migration of `metadata.schema_version`, approved by the Board and documented in
governance §5.6. Records update to the current schema version only on their next MINOR/MAJOR
bump; no dedicated rewrite pass.

- **Mechanism:** the transition-window validator (`byzfrontier_validate.py`, repeatable
  `--schema`) dispatches each record to the schema matching its declared `schema_version`.
- **Status:** in progress and self-completing. Migration is complete when every record has
  reached the current schema version; at that point the superseded schema and its
  `--schema` entry can be retired and any deferred required-field promotion (see split-ship,
  §5.6) can land as its MAJOR step.
- **Tracking metric:** count of records still at each `schema_version` (a one-line scan).

## Phase 2 editorial follow-ups (scheduled)

### Bālis identification — InterpretationRecord (before Session 7 closes)

Session 1 surfaced a coordinate divergence on ENT-PLC-0037 (Bālis / Meskene / Barbalissos):
the stored editorial point (35.83, 38.27) and Eger 2008's gazetteer point (35.98836,
38.10952) differ by **~22.8 km — ~4.6× the stored 5000 m uncertainty radius**. The stored
coordinate is explicitly flagged "verify against a gazetteer", and Eger 2008 is that
gazetteer. Left unresolved this session (compare, do not overwrite). Action: mint an
InterpretationRecord on the Bālis identification weighing the two points, and decide whether
to adopt Eger's coordinate — which would carry the corresponding MINOR/MAJOR bump on the
entity. **Target: before Session 7 closes.**

### ATT-0339 — printed Ibn Shaddād verification

ATT-0339 (Adhana fortification under al-Amīn; refortified 808–810) is provisionally attributed
to al-Yaʿqūbī's **Kitāb al-Buldān (SRC-0008)** on scholarly-probability grounds (frontier-town
foundation/settlement content characteristic of the Buldān and of Ibn Shaddād's use of it),
flipped this session from the earlier Taʾrīkh (SRC-0003) guess. Carries `[citation needed]`.
Action: check the printed Ibn Shaddād, al-Aʿlāq al-khaṭīra, which names its al-Yaʿqūbī source;
confirm or disconfirm the SRC-0008 attribution and clear the flag.
