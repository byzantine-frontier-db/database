# Phase 2 Master Extraction Prompt — Eger 2008 Gazetteer (SRC-0065) — SESSION 5

You are doing **read-only analysis and patch drafting** for the Byzantine-Islamic Frontier
Database. Curtis applies all patches and commits from Windows. Never push; hand back one patch.

## Baseline — confirm before touching anything
- Live corpus is **1336 records** after Session 4 (older figures are stale; work from live state).
  Validate with **both schemas**:
  `python tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json --schema schema/byzfrontier_schema_v2.json records/`
  then `python tools/byzfrontier_xref.py records/`. Both must end at **0 errors / 0 warnings**.
- Work from the committed `docs/eger_2008_gazetteer_cleaned.txt`, coordinate sidecar
  `docs/eger_2008_coordinates.json`, and page map `docs/eger_2008_page_map.json`. Use the sidecars
  for coordinates/pages; cross-check any point whose sidecar `status` is `repaired`/`unrecoverable`.
- Extraction source of record: **SRC-0065** (Eger 2008 gazetteer).

## Hard rules 1–7 (non-negotiable)
1. No fabricated citations. 2. No fabricated external ids. 3. Distinct evidential levels
(Observation ≠ Attestation ≠ Source). 4. Provenance honesty (primary-via-secondary records both +
the route). 5. `editorial_review_required: true` on everything unverified against print. 6. Validate
(both schemas + xref) to 0/0 before handoff. 7. Honest framing incl. review-flag proportion.

## Rules 8–11 (carried forward)
- **8** — evidential claim in `paraphrase`/`direct_quotation`, never only `notes`; an attestation with
  no paraphrase and no supported observation is invalid (EMPTY_ATTESTATION).
- **9** — an InterpretationRecord's `supporting_evidence` cites attestations, not raw sources.
- **10** — cross-reference related/competing interpretations (distinct dated positions kept separate).
- **11** — three attestation patterns from SRC-0065 (below).

## Settled policies
- **schema_version (Policy B):** new records and any MINOR/MAJOR-bumped record declare `2.0.0`;
  PATCH-only touches keep their version.
- **identification_status downgrades are MAJOR** — flag, don't apply silently.
- **coordinate_method: gazetteer_entry** (closed enum); UTM/zone/conversion text in
  **coordinate_source**; `uncertainty_radius_m: 500` (map-derived).
- **Real page citations** from the page map (`s.v. <entry>, pp. <span>`), never `s.v.`-only.
- **Defer-then-batch** for one-clause primaries with no SourceRecord — but route the now-available
  **SRC-0066 al-Iṣṭakhrī / SRC-0067 Ibn Rusta / SRC-0068 al-Dimashqī / SRC-0069 al-Balkhī** directly
  if cited (al-Balkhī carries a bibliographic flag — survives only via al-Iṣṭakhrī/Ibn Ḥawqal).

## Section 4 — VERIFY PER ENTRY (revised after Session 4)
**Do NOT assume a Section 4 exists just because a site is absent from the non-visited list.** The
front-matter "visited summers 2002–2006" is a general statement, not a per-entry guarantee: Malaṭiya
and Marʿash have no §4 despite not being on the exclusion list, and Shimshāṭ *is* on the list yet has
one. **The only reliable signal is an actual "Personal Observations" header in the entry text.** For
each site: scan the entry; if it contains a `Personal Observations, <date>` section → mint
`primary_observation` + `observation_date` for the dated autopsy. If not → Sections 1–3 only, route
"Remains" as `archaeological_evidence` (crediting the excavator/team), and mint no primary_observation.
Watch for false positives: "I" in regnal numerals (Yazīd I) is not first-person autopsy.

## The three attestation patterns from SRC-0065
- **Section 1 — Location/coordinate.** Sidecar lat/lon → `coordinates` block only if the entity lacks
  one (compare, don't overwrite; flag divergence beyond the radius as a candidate InterpretationRecord,
  cf. Bālis/Malaṭya). Locational id → attestation, `provenance: gis_derived_observation`, source SRC-0065.
- **Section 2 — History.** Primary content footnoted to a primary → attest against **that** primary
  SourceRecord, `primary_paraphrase`, citation "…reached via Eger 2008, Appendix 2, s.v. <entry>,
  pp. <span> (SRC-0065)". Eger's own argument/identification → InterpretationRecord attributed to Eger.
- **Section 3/Remains — Archaeology.** Published excavation/survey → `archaeological_evidence`, note the
  team. Eger's own field autopsy (only if a §4 section exists) → `primary_observation` + observation_date.

---

## SESSION 5 — Al-Maṣṣīṣa + Al-Muthaqqab + Qūrus + Raʿbān  (pp. 501–518)

**Batching note:** this is the page-order-correct next block after Session 4 (which ended at Marʿash,
p500). It is **not** the Bethesna/Shimshāt/Sīs/Sumaysāt set — that block (pp. 519–535) is the session
*after* this one. Starting at Bethesna would orphan Al-Maṣṣīṣa (a 9-page entry with a §4 section), so
this session takes pp. 501–518.

All four are **existing entities → enrichment, no mints expected.** Confirm each against the uploaded
`current_entities.txt`:

| Site | Entity | Coordinate (sidecar) | Pages | §4? (verify in text) |
|------|--------|----------------------|-------|----------------------|
| Al-Maṣṣīṣa (Mopsuestia/Misis) | **ENT-PLC-0118** 'al-Massīsa' | 36.95784, 35.62372 | 501–509 | **yes** — Personal Observations, 8/3/04 |
| Al-Muthaqqab (Mutallip Höyük) | **ENT-PLC-0124** 'al-Muthaqqab' | 36.91997, 35.98208 | 510–512 | **verify** — a §4 header sits at p513 (may be this entry or Qūrus) |
| Qūrus (Cyrrhus) | **ENT-PLC-0063** 'Qūrus' | 36.74505, 36.95959 | 513–516 | **verify** — resolve the p513 §4 to Al-Muthaqqab vs Qūrus by reading the text |
| Raʿbān | **ENT-PLC-0061** 'Raʿbān' | 37.42534, 37.69022 | 517–518 | **yes** — Personal Observations, 7/24/05 |

Notes:
- Check each entity for an existing `coordinates` block: compare-don't-overwrite where present; add
  where absent. All four sidecar points are clean (`status: ok`).
- The p513 Personal-Observations header is ambiguous between Al-Muthaqqab (510–512) and Qūrus (513–516)
  — read the surrounding prose to attach the dated autopsy to the correct entity; do not duplicate it.
- Qūrus/Cyrrhus and Al-Maṣṣīṣa are the substantial entries; Al-Muthaqqab and Raʿbān are short.
- Al-Maṣṣīṣa: watch for possible overlap with existing ENT-PLC-0118 attestations (a corpus-wide dedup
  pass is queued separately — flag overlaps, don't guess which to drop).

## Deliverables
One patch. A session-tracker row. A deferred-items list (any `[citation needed]`, newly-deferred
sources, coordinate divergences flagged as candidate InterpretationRecords, the p513 §4 attribution,
any identification_status downgrade flagged MAJOR not applied). Validate both schemas + xref to
**0/0**, preserve back-reference symmetry, report the review-flag proportion (should be 100%).
