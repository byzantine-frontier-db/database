# Phase 2 Master Extraction Prompt — Eger 2008 Gazetteer (SRC-0065)

**Reusable master prompt for the seven Phase 2 sessions.** Session 1 specifics are filled
in at the end; later sessions swap the site list, page range, and pre-resolved entity map.
Adapted from the Eger 2015 master prompt (18 clean sessions) for the palimpsest-dense,
four-section gazetteer pattern.

---

## Role and context

You are doing **read-only analysis and patch drafting** for the Byzantine-Islamic Frontier
Database. Curtis applies all patches and commits from Windows. Never push; hand back patches.

- Corpus state: **1228 records**, both validators clean (0 errors / 0 warnings).
- Phase 2 source: **A. Asa Eger, 2008 dissertation, Appendix 2 gazetteer = SRC-0065.**
- Work from the **normalized** text, never the raw file:
  - `docs/eger_2008_gazetteer_cleaned.txt` — cleaned narrative (mojibake fixed, page
    numbers and footnotes de-interleaved).
  - `docs/eger_2008_coordinates.json` — pre-extracted UTM→WGS84 coordinates, per entry.
- Scope: ~29 site entries + several "see Chapter" stubs, 7 sessions of ~15–20 pp.

## The seven hard rules (editorial_workflow.md — non-negotiable)

1. No fabricated citations (`[citation needed: …]` + `editorial_review_required: true` when unsure).
2. No fabricated external identifiers (Pleiades/VIAF/Wikidata only when verified).
3. Distinct evidential levels — Observation ≠ Attestation ≠ Source.
4. Provenance honesty — primary reached via a secondary records the primary + the route.
5. `editorial_review_required: true` on anything not verified against the printed page.
6. Validate (`byzfrontier_validate.py` + `byzfrontier_xref.py`) to 0 errors before handoff.
7. Honest framing — say what was actually done, including the review-flag proportion.

Every record this session is `workflow_state: draft`, `editorial_review_required: true`,
`created_by: Curtis`.

---

## Palimpsest workflow — enrich vs mint

Phase 2 is attestation-dense and entity-light: most sites already exist. For each gazetteer
site:

**The test.** Unicode-normalize (NFKD, strip combining marks and ʿ/ʾ/'/'') the gazetteer
site name **and** every concordance alternate (Seleucid/Classical/Modern names). Compare
against `standardised_name` + `alternative_names` of existing place records.
- **Match → ENRICH** the existing entity: add new attestations/observations/interpretations,
  update `linked_attestations` / `linked_interpretations`, MINOR-bump the entity's version
  (§4.3). Do **not** mint a duplicate (Master Record rule, specification §4.1).
- **No match → MINT** a new EntityRecord with full provenance, then attach attestations.

Enrichment never overwrites existing asserted content; it adds and back-references.

---

## The four-section template → three attestation patterns

Each gazetteer entry has up to four sections. They map to **three distinct attestation
patterns from the single source SRC-0065** — this is the core Phase 2 move, so walk it
deliberately for every site:

### Section 1 — Location (coordinate + setting)
- **Coordinate** → take the converted lat/lon from `eger_2008_coordinates.json`. If the
  entity has **no** `coordinates` block, add one:
  `crs: EPSG:4326`, `coordinate_method: "UTM zone <z> from Eger 2008 gazetteer (SRC-0065), converted via pyproj"`,
  `uncertainty_radius_m: 500` (map-derived — never the spurious metre precision),
  `coordinate_confidence: 5` (or **2** for a repaired point, + `editorial_review_required`).
  If the entity **already has** coordinates, do **not** overwrite — record Eger's point as a
  cross-check in notes and, if it diverges beyond the uncertainty radius, flag for editorial
  review (a candidate future InterpretationRecord on the identification).
- **The locational identification** (Eger equating the ancient site with a modern place) →
  an attestation, `provenance: gis_derived_observation`, `source: SRC-0065`.
- Descriptive setting/routes prose → observations as warranted (`primary_observation` if
  Eger's own field note; `modern_synthesis` if he's citing others).

### Section 2 — History (primary + secondary)
- Content Eger draws from a **primary** text (footnoted to al-Balādhurī, al-Ṭabarī, …) →
  attestation against **that primary SourceRecord** (create it if absent),
  `provenance: primary_paraphrase` (or `primary_quotation` if short and verbatim), and the
  `citation` records the full chain ending "…reached via Eger 2008, Appendix 2, p. NNN
  (SRC-0065)". This is the secondary-mediated pattern with SRC-0065 as the route — **never**
  attest primary content against SRC-0065 itself.
- Eger's **own** historical argument or identification (e.g. his Ḥadath / Hārūnīyya
  identifications) → **InterpretationRecord** attributed to Eger, against SRC-0065.
- Modern scholarship Eger cites (Honigmann, Hild–Hellenkemper) → attest against that modern
  SourceRecord if it warrants one, else `modern_synthesis` against SRC-0065.

### Section 3 — Archaeology
- **Published** excavation/survey Eger reports → `provenance: archaeological_evidence`, note
  the excavator/project.
- Eger's **own** field archaeology (autopsy of standing remains) → `provenance:
  primary_observation`, `source: SRC-0065`, with `observation_date`.

### Section 4 — Personal Observations (visited sites only)
- Each dated observation → ObservationRecord (the proposition) + AttestationRecord
  (`provenance: primary_observation`, `source: SRC-0065`, `observation_date` = the visit date
  from the section header, e.g. `{date: "2005-07-20", precision: day}`). First-person autopsy;
  high-value, distinct evidential type.
- **Skip Section 4 entirely** on the nine non-visited sites (Shimshāt, Ḥiṣn Ziyād, Kamkh,
  Ḥiṣn Qalawdiya, Tīzīn, Dābiq, Qūrus, Jūma, Manbij) — do **not** mint empty
  `primary_observation` records; instead add a `"not visited by Eger"` note to the entity
  (methodologically meaningful, not a gap).

### Schema-dependency gate
`primary_observation` (provenance) and `observation_date` (attestation field) require the
pre-Phase-2 schema batch (changes 1 & 2) to be **Board-approved and merged** first. Until
then they will fail validation:
- `gis_derived_observation`, `primary_paraphrase`, `archaeological_evidence`,
  `modern_synthesis` are **already** in the enum — Sections 1 and 2 proceed regardless.
- If extracting before approval, **stage** Section-4 and Section-3-autopsy records separately
  and apply them once the schema lands; do not emit the two new values into validated records.

---

## Per-session deliverables

1. **Patches** (not commits): new ATT/OBS/INT records; enriched-entity diffs (coordinates +
   `linked_*` + MINOR bump); any new primary/modern SourceRecords; SRC-0065 if not yet committed.
2. **Session-tracker row**: `# | sites | pages | status | records | commit | verified`.
3. **Deferred-items list**: repaired-coordinate flags, Eger-identification interpretations,
   coordinate discrepancies, `[citation needed]` items, any enrich-vs-mint judgement calls.
4. **Validation**: both validators to 0 errors, back-reference symmetry preserved, before handoff.
5. **Honest framing**: record counts and the review-flag proportion; note the palimpsest
   shape (attestation-dense, entity-light, version-bump-heavy).

Confirm the next available ATT / OBS / INT / SRC IDs from the live corpus before minting.

---

## SESSION 1 — Adhana + ʿAyn Zarba + Bālis  (~pp. 437–453, ~17 pp)

All three are **existing entities → pure enrichment, no new place minting expected:**

| Site | Entity | Current version | Coordinate action |
|------|--------|----------------|-------------------|
| Adhana (Adana) | **ENT-PLC-0119** | 1.2.0 | **Add** — 36.98626, 35.33729 (36N, clean, conf 5) |
| ʿAyn Zarba (Anazarbus) | **ENT-PLC-0120** | 1.5.0 | **Add** — 37.25572, 35.89868 (**repaired** northing, conf 2, flag review) |
| Bālis | **ENT-PLC-0037** | 1.4.0 | **Compare** — Eger 35.98836, 38.10952; entity already has coordinates, do not overwrite, flag any divergence |

- **Section 4 present** for Adhana ("Personal Observations, 7/20/05") and ʿAyn Zarba ("In my
  first visit in 2004…"). Confirm Bālis in the cleaned text. Section-4 records are
  schema-gated (see gate above).
- **SRC-0065** must be committed (Commit 1) before this session's citations resolve; if
  extracting before the schema batch merges, stage the Section-4 records.
- Expected shape: 3 entities MINOR-bumped, 2 coordinate additions + 1 comparison, a cluster
  of new ATT/OBS/INT, no new place entities. Confirm each with the validators before handoff.
