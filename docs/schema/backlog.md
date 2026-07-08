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

## Deferred source-minting queue (Phase 2)

**Standing policy (from Session 2):** during extraction, one-clause primary-source mentions
are **deferred, not minted mid-session** (keeps sessions focused; matches Session 1's
zero-mint precedent). Deferred sources are queued here and minted in a **dedicated
source-minting pass** at a checkpoint (suggested: before Session 4, or whenever the queue
reaches ~5), which also back-fills the attestations that reference them. Both named
geographers below recur across the thughūr/ʿawāṣim material, so minting them once serves all
later sessions.

- **al-Iṣṭakhrī** — deferred at ATT-0354 (Al-Ḥadath "fertile lands"). Major 10th-c. geographer;
  will recur.
- **Ibn Rusta** — deferred at INT-0165 / Dulūk ("thughūr site in 903"). Major geographer; will recur.

## Tooling fix applied (Session 2 follow-up)

`normalize_gazetteer.py` header detection previously mis-keyed Al-Ḥadath's coordinate under the
concordance token "Göynük)" (embedded era/Modern markers weren't excluded). Fixed; sidecars
`eger_2008_coordinates.json` and `eger_2008_page_map.json` regenerated — Al-Ḥadath's point
(37.70N 37.44E) and page span (pp. 458–462) now key correctly. Cleaned text unchanged.
Commit the updated tool + regenerated sidecars together.

## Tooling fix #2 (Session 3 follow-up) — entry-boundary phantoms

`normalize_gazetteer.py` was minting phantom entries off two line types inside a real entry:
(1) `(see Chapter N)` cross-reference lines, and (2) wrapped concordance continuations whose
"Modern" keyword sat on the previous line (e.g. `Gözeneler68`). These phantoms stole neighbouring
coordinates (Session 3 rows #8, #11/#12). Fixed: `(see…` lines and any line immediately preceded
by a concordance line are excluded from header detection. Sidecars regenerated — Iskandarūna,
Al-Muthaqqab, and Al-Kanīsa as-Sawdā' now key correctly; the UNRECOVERABLE 43750/95800 point is
re-attributed to ENT-PLC-0121 (Al-Kanīsa/Epiphaneia), not al-Maṣṣīṣa. Cleaned text unchanged.
Commit the updated tool + regenerated sidecars together.

## Source-minting queue — AT CHECKPOINT (do before Session 4)

Queue is now ~6 and past the ~5 trigger. A dedicated source-minting pass is warranted before
Session 4:
- al-Iṣṭakhrī (recurs), Ibn Rusta (recurs) — from Session 2
- al-Balkhī (Hārūnīyya joint small-fort description)
- al-Dimashqī (Kamkh, thughūr al-jazīra list)
- Abū ʿAmr al-Bāhilī (Ḥiṣn Manṣūr naming tradition)
- unnamed source behind the Jawzāt garrison roster (Abū ʿAmr al-Ṭarsūsī named as qāḍī, not author)
Pass mints SRC-0066+ for each resolvable source and back-fills the deferred attestations to point
at them (updating the placeholder notes in ATT-0354, INT-0165, and the Session 3 deferrals).

## Source-minting pass — DONE (2026-07-08)

Cleared four of the six queued sources by minting SourceRecords and back-filling the deferred
mentions (patch: phase2_source_minting_pass.patch):
- **SRC-0066 al-Iṣṭakhrī** — attestations ATT-0405 (Hārūnīyya small-fort), ATT-0407 (Al-Kanīsa Friday-mosque)
- **SRC-0067 Ibn Rusta** — ATT-0408 (Dulūk thughūr, 903)
- **SRC-0068 al-Dimashqī** — ATT-0409 (Kamkh thughūr al-jazīra)
- **SRC-0069 al-Balkhī** — ATT-0406 (Hārūnīyya) — **FLAGGED for bibliographic review**: original lost,
  preserved only via al-Iṣṭakhrī/Ibn Ḥawqal; Curtis to confirm mint-as-distinct vs fold into SRC-0066/0009.
Deferral notes on ATT-0369, ATT-0375, ATT-0401 updated to RESOLVED; the four referenced entities
(ENT-PLC-0062/0078/0121/0122) MINOR-bumped with reciprocal linked_attestations.

## Category: "named tradent, unknown author" (stays deferred)

Mentions credited to a *named authority* for whom Eger cites *no citable work* — not minted, held here:
- **Abū ʿAmr al-Bāhilī** — Ḥiṣn Manṣūr naming tradition (ATT-0378). A naming tradition credited to him;
  no work cited, single mention. Stays deferred.
- **Jawzāt garrison-roster source** — only a qāḍī name (Abū ʿAmr al-Ṭarsūsī) survives, not an author.
These resolve only if a printed-source check turns up an actual work/edition; otherwise permanent notes.
