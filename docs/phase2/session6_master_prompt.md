# Phase 2 Master Extraction Prompt — Eger 2008 Gazetteer (SRC-0065) — SESSION 6

You are doing **read-only analysis and patch drafting** for the Byzantine-Islamic Frontier
Database. Curtis applies all patches and commits from Windows. Never push; hand back one patch.

## Baseline — confirm before touching anything
- Live corpus is **1366 records** after Session 5 + the rules-12/13 back-fill (older figures are
  stale). Validate with **both schemas**:
  `python tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json --schema schema/byzfrontier_schema_v2.json records/`
  then `python tools/byzfrontier_xref.py records/`. Both must end at **0 errors / 0 warnings**.
- Work from the committed `docs/eger_2008_gazetteer_cleaned.txt`, coordinate sidecar
  `docs/eger_2008_coordinates.json`, and page map `docs/eger_2008_page_map.json`. Use the sidecars.
- Extraction source of record: **SRC-0065** (Eger 2008 gazetteer).

## Hard rules 1–7 (non-negotiable)
1. No fabricated citations. 2. No fabricated external ids. 3. Distinct evidential levels. 4. Provenance
honesty. 5. `editorial_review_required: true` on everything unverified against print. 6. Validate
(both schemas + xref) to 0/0. 7. Honest framing incl. review-flag proportion.

## Rules 8–13 (Phase-2 conventions, all active)
- **8** — evidential claim in `paraphrase`/`direct_quotation`, never only `notes` (empty attestation is invalid).
- **9** — interpretation `supporting_evidence` cites attestations, not raw sources.
- **10** — cross-reference related/competing interpretations.
- **11** — three attestation patterns from SRC-0065 (below).
- **12 — attest existing sources inline.** A thin one-clause primary that cites a SourceRecord
  **already in the corpus** is attested at extraction time (a two-minute attestation), NOT deferred.
  Deferral (defer-then-batch) applies only to *minting new* SourceRecords. The inline attestation still
  carries `editorial_review_required: true` and an edition/page `[citation needed]` (rule 5).
- **13 — al-Yaʿqūbī work attribution.** Topographic/administrative content → **Kitāb al-Buldān
  (SRC-0008)**; narrative-historical content → **Taʾrīkh (SRC-0003)**. This is a *provisional
  convention*, not a determination, so each such attestation's note must say "routed per rule 13,
  pending printed confirmation" (keeps rule 4 honest — it doesn't claim Eger specified the work).

## Settled policies
- **schema_version (Policy B):** new + MINOR/MAJOR-bumped records declare `2.0.0`; PATCH keeps its version.
- **identification_status downgrades are MAJOR** — flag, don't apply silently.
- **coordinate_method: gazetteer_entry** (enum); UTM/zone text in **coordinate_source**; `uncertainty_radius_m: 500`.
- **Real page citations** from the page map, never `s.v.`-only.
- **Defer-then-batch** only for *new* SourceRecords (contrast rule 12). Now-available direct-route
  sources: SRC-0066 al-Iṣṭakhrī, SRC-0067 Ibn Rusta, SRC-0068 al-Dimashqī, SRC-0069 al-Balkhī (flagged).

## Section 4 — VERIFY PER ENTRY (not by the exclusion list)
The front-matter non-visited list is unreliable **both ways**. Mint `primary_observation` +
`observation_date` **only** where the entry text contains an actual `Personal Observations, <date>`
header with first-person autopsy; otherwise Sections 1–3 only, route "Remains" as
`archaeological_evidence` (credit the team), add a `"not visited by Eger"` note. Ignore false
positives ("I" in regnal numerals).

## The three attestation patterns from SRC-0065
- **§1 Location/coordinate** → sidecar lat/lon; add `coordinates` only if absent (compare, don't
  overwrite; flag divergence beyond radius as a candidate InterpretationRecord). Locational id →
  attestation `gis_derived_observation`, source SRC-0065.
- **§2 History** → primary content to its **own** primary SourceRecord, `primary_paraphrase`, citation
  "…reached via Eger 2008, Appendix 2, s.v. <entry>, pp. <span> (SRC-0065)". Existing sources → rule 12
  (attest inline). Eger's own argument → InterpretationRecord.
- **§3/Remains** → published archaeology `archaeological_evidence` (credit team); Eger's own autopsy
  (only if a §4 header exists) → `primary_observation` + observation_date.

---

## SESSION 6 — Sanjah/Bahasnā + Shimshāṭ + Sīs + Sumaysāṭ  (pp. 519–535)

All four are **existing entities → enrichment, no mints expected.** Confirm against the (freshly
regenerated) `current_entities.txt` — the norm-matcher is easily fooled here (Sīs collides with
al-Ma**ssī**sa; Sumaysāṭ/Samosata collides with Shimshāṭ/Ar**samosata**), so use these verified IDs:

| Site | Entity | Coordinate (sidecar) | Pages | §4? (verify in text) |
|------|--------|----------------------|-------|----------------------|
| Sanjah/Bahasnā (Bethesna/Octacuscum) | **ENT-PLC-0070** 'Sanjah-Bahasnā' | none | 519–520 | no §4 in inventory → §1–3 only |
| Shimshāṭ (Arsamosata) | **ENT-PLC-0075** 'Shimshāṭ' | none | 521–522 | **YES — has §4 (p521) despite being on the non-visited list.** Verify and mint the autopsy |
| Sīs (Sīsīya / Kozan / Flaviopolis) | **ENT-PLC-0127** 'Sīs' | 37.45002, 35.81247 | 523–524 | **likely yes** — the p525 §4 header sits at the Sīs/Sumaysāṭ boundary; resolve to Sīs vs Sumaysāṭ by reading the prose |
| Sumaysāṭ (Samosata/Samsat) | **ENT-PLC-0073** 'Sumaysāṭ' | **none** (see note) | 525–535 | **likely no** — appears to lack §4 (like Malaṭiya/Marʿash); confirm |

Notes:
- **Sīs vs Sumaysāṭ identity:** do not conflate. Sīs = ENT-PLC-0127 (Cilician, Kozan). Sumaysāṭ =
  ENT-PLC-0073 (Euphrates, Samsat). They are unrelated despite the Samosata/Arsamosata transliteration overlap.
- **Sumaysāṭ coordinate:** the sidecar attributes none. A `36N N4148511 E748786` line near the entry
  boundary converts to 37.45N 35.81E — that is **Sīs's** point (Cilicia), not Samsat's (~37.53N 38.49E,
  zone 37). Do **not** attach it to Sumaysāṭ. If the Sumaysāṭ entry has its own Coordinates line, verify
  it lands near Samsat before using; otherwise add no coordinate and note it.
- **p525 §4 attribution:** the single Personal-Observations header in the 523–535 range (p525) most
  likely closes the **Sīs** entry (autopsy comes at an entry's end; Sīs ends ~524). Read the prose to
  confirm whose visit it is, exactly as the Al-Muthaqqab/Qūrus p513 case was resolved. Do not duplicate it.
- Sumaysāṭ is the **long entry** (pp. 525–535) — expect a full §2 source chain (Balādhurī, the
  geographers, possibly al-Iṣṭakhrī/al-Balkhī via SRC-0066/0069 — route directly per the settled sources).
- Rule 12 is live: any thin mention of a source already in the corpus gets an inline attestation this
  session, not a deferral.

## Deliverables
One patch. A session-tracker row. A deferred-items list (any `[citation needed]`, **new** sources to
mint (rule 12 means only genuinely-absent sources defer), coordinate divergences as candidate
InterpretationRecords, the p525 §4 attribution, any identification_status downgrade flagged MAJOR).
Validate both schemas + xref to **0/0**, preserve back-reference symmetry, report the review-flag
proportion (should be 100%).
