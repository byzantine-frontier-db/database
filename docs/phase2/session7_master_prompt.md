# Phase 2 Master Extraction Prompt — Eger 2008 Gazetteer (SRC-0065) — SESSION 7 (FINAL)

You are doing **read-only analysis and patch drafting** for the Byzantine-Islamic Frontier
Database. Curtis applies all patches and commits from Windows. Never push; hand back one patch.
**This is the final Session of the Eger 2008 gazetteer extraction (pp. 536–554).**

## Baseline — confirm before touching anything
- Live corpus is **1414 records** after the ATT-0470 split, the second source-minting pass, and the
  Bālis/Malaṭya coordinate interpretations (older figures are stale). Validate with **both schemas**:
  `python tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json --schema schema/byzfrontier_schema_v2.json records/`
  then `python tools/byzfrontier_xref.py records/`. Both must end at **0 errors / 0 warnings**.
- Work from the committed `docs/eger_2008_gazetteer_cleaned.txt`, coordinate sidecar
  `docs/eger_2008_coordinates.json`, page map `docs/eger_2008_page_map.json`. Cross-check any point
  whose sidecar `status` is `repaired`/`unrecoverable`.
- Extraction source of record: **SRC-0065**.

## Hard rules 1–7 · Rules 8–13 (all active)
1–7: no fabricated citations/ids; distinct evidential levels; provenance honesty; editorial_review_required
on unverified; validate both schemas + xref to 0/0; honest framing.
8: claim in `paraphrase`/`direct_quotation`, never only `notes`. 9: interpretation `supporting_evidence`
cites attestations. 10: cross-reference related/competing interpretations. 11: three attestation patterns
from SRC-0065. **12: attest existing sources inline** (thin one-clause primary citing a corpus source →
attest now, don't defer; deferral is only for *minting new* sources). **13: al-Yaʿqūbī** →
topographic/administrative to Kitāb al-Buldān (SRC-0008), narrative-historical to Taʾrīkh (SRC-0003),
each noted "per rule 13, pending printed confirmation".

## Settled policies
- **schema_version (Policy B):** new + MINOR/MAJOR-bumped → `2.0.0`; PATCH keeps version.
- **identification_status downgrades are MAJOR** — flag, don't apply silently.
- **coordinate_method: gazetteer_entry** (enum); UTM/zone text in **coordinate_source**; radius 500.
- **Real page citations** from the page map; never `s.v.`-only.
- **Minting new entities** (this session has one): next free `ENT-PLC-NNNN`, `schema_version: 2.0.0`,
  full required fields, a bootstrap attestation so `linked_attestations` is non-empty.

## Section 4 — VERIFY PER ENTRY, typo-tolerant (Session 6 lesson; NO inventory to trust)
The §4 inventory was retracted — it was wrong on 3 of 4 Session-6 sites (boundary spill + a
"Ob**v**servations" typo + header-detection gaps). **There is no §4 guess column below on purpose.**
For each entry: read the text between its header and its closing coordinate; mint `primary_observation`
+ `observation_date` **only** if it contains a first-person autopsy header, matched **typo-tolerantly**
(`Personal Ob[a-z]*ervations`). Otherwise Sections 1–3 only, route "Remains"/"Research" as
`archaeological_evidence` (credit the team), add a `"not visited by Eger"` note. Ignore regnal-numeral "I".
The front-matter non-visited list is unreliable both ways — do not use it.

## The three attestation patterns from SRC-0065
- **§1** coordinate → sidecar lat/lon; add `coordinates` only if absent (compare, don't overwrite; flag
  divergence beyond radius as a candidate coordinate InterpretationRecord, cf. INT-0169/0170). Locational
  id → attestation `gis_derived_observation`, source SRC-0065.
- **§2** primary → its own SourceRecord, `primary_paraphrase`, "…reached via Eger 2008, s.v. <entry>,
  pp. <span> (SRC-0065)"; existing source → rule 12 (inline); Eger's own argument → InterpretationRecord.
- **§3/Remains** → `archaeological_evidence` (credit team); Eger's own autopsy (only if a §4 header
  exists) → `primary_observation` + observation_date.

## Now-available sources (route directly, don't defer)
SRC-0066 al-Iṣṭakhrī · SRC-0067 Ibn Rusta · SRC-0068 al-Dimashqī · SRC-0069 al-Balkhī (flagged) ·
SRC-0070 Ibn al-ʿIbrī · SRC-0071 Acta Conciliorum Oecumenicorum · SRC-0072 Ibn al-Shiḥna ·
SRC-0073 al-Wāqidī · SRC-0074 Antonine Itinerary · SRC-0075 Cicero · SRC-0076 Theophylact Simocatta.
For Cilician sites (Ṭarsūs) watch for Cicero / the Antonine Itinerary — now mintable-free (route direct).

---

## SESSION 7 — Tall Jubayr + Ṭaranda + Ṭarsūs + Tīzīn + Zibaṭra  (pp. 536–554)

Verified IDs (the norm-matcher mis-fires badly here — Ṭarsūs collides with a Cydnus/Baradān river
record; confirm each against the freshly regenerated `current_entities.txt`):

| Site | Entity | Coordinate (sidecar) | Pages | Coord action |
|------|--------|----------------------|-------|--------------|
| Tall Jubayr | **MINT** (new ENT-PLC) | none | 536 | no coordinate; short entry |
| Ṭaranda (Darende) | **ENT-PLC-0080** 'Taranda' | 38.57129, 37.48786 | 536–537 | **add** (no prior coords) |
| Ṭarsūs | **ENT-PLC-0004** 'Tarsus' | 36.90778, 34.88986 (**repaired**, conf 2) | 538–550 | **has coords → compare**, don't overwrite; flag divergence; the sidecar point is the Gözlü Küle repair |
| Tīzīn | **ENT-PLC-0071** 'Tīzīn' | none in sidecar | 551 | verify entry's Coordinates line; add if present |
| Zibaṭra (Sozopetra) | **ENT-PLC-0007** 'Zibatra / Sozopetra' | 38.09227, 37.88248 | 551 | **has coords → compare** |

Notes:
- **Ṭarsūs = ENT-PLC-0004** (the city), NOT the Cydnus/Baradān river record (ENT-PLC-0134). It is the
  major/long entry (pp. 538–550) with a full §2 source chain; expect Cicero / Antonine Itinerary / the
  Arabic geographers — route directly. Its sidecar point is `repaired` (Gözlü Küle mound); since the
  entity already has a coordinate, compare and flag divergence rather than overwrite.
- **Tall Jubayr is a mint** — no existing entity, no gazetteer coordinate. Born with full required fields
  + a bootstrap attestation; `identification_status` per what the entry supports.
- **Tīzīn and Zibaṭra both page-map to p551** (header-detection overlap) — read header-to-header, don't
  trust the page numbers to separate them. Tīzīn is on the non-visited list but **verify §4 in text
  anyway** (the list is unreliable). Zibaṭra closes the appendix.
- Confirm next free ATT/OBS/INT/ENT-PLC ids from the snapshot before minting.

## Deliverables
One patch. A session-tracker row (mark the gazetteer extraction COMPLETE). A deferred-items list (any
`[citation needed]`, genuinely-new sources to mint, coordinate divergences as candidate
InterpretationRecords, any identification_status downgrade flagged MAJOR). Validate both schemas + xref
to **0/0**, preserve back-reference symmetry, report the review-flag proportion (should be 100%).
