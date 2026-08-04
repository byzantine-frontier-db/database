# Step 4 — Register Expressibility Run

**Status:** held for review. Delivery is not commit.
**Read against:** commit `d23d091` — confirmed as my clone's tip before running; carries the committed fixture suite `tests/logical_model_fixture/`.
**Corpus stability:** `git log 44988e2..HEAD -- records/` is **empty** — the corpus is unchanged since the calibration base. This is the precondition that makes the calibration record a valid fixed point for D1a.
**Read-only:** register entries against the committed synthetic fixture, and for category 1 also against the live corpus. No corpus record touched, no migration.

---

## Deliverable 0 — Vocabulary clock (stated before any entry ran)

**Finding: every step-0 register term is PROVISIONAL — filed under §5.5, not yet ratified.** The ratified vocabulary file `vocabularies/byzfrontier_vocabularies_v1_1.ttl` contains **none** of them; the proposals live in `docs/governance/vocabulary_proposals_2026-07-23.md` as *"filed for immediate decision"* (Board-proposed) and *"held"* (below threshold). "Filed" is not "ratified": Board-plus-three-cases has not cleared for any of them in a committed vocabulary file.

| Term | Register role | Filing status (proposals doc) | **Clock status** |
|---|---|---|---|
| `co_located_aspect` | dual-aspect link (17, QR-501) | **not filed** — surfaced by the logical model, needs a §5.5 filing | **PROVISIONAL (unfiled)** |
| `controls` | control geography (QR-102/204/501) | filed for immediate decision (3 cases) | **PROVISIONAL** |
| `overlooks` | viewshed base (QR-102/501) | filed for immediate decision (3 cases) | **PROVISIONAL** |
| `crosses_at` | crossings (QR-101/204) | filed for immediate decision (4 cases) | **PROVISIONAL** |
| `corroborates` | interpretation links (QR-403) | filed for immediate decision (4 cases) | **PROVISIONAL** |
| `parallel_case` | interpretation links (QR-403) | filed for immediate decision (3 cases) | **PROVISIONAL** |
| `examined` | investigation coverage (QR-503) | filed for immediate decision (19+ cases) | **PROVISIONAL** |
| `member_of_argued_group` | argued systems (QR-205) | filed (Update 2, 3 cases) | **PROVISIONAL** |
| `member_of_route_family` | route families (QR-103/104) | **held** — 0 cases (routes not yet extracted) | **PROVISIONAL (held)** |
| `traverses` | route/feature (QR-101/104) | **held** — 1 case | **PROVISIONAL (held)** |
| `succeeds` | site/component succession (19a, QR-502-adjacent) | **held** — <3 cases | **PROVISIONAL (held)** |
| `restores` | jurisdiction interruption (16, QR-302) | **held** — 0 cases (no TerritorialUnits yet) | **PROVISIONAL (held)** |
| `subordinate_to` | hierarchy (QR-203) | existing enum, **0 uses** — usable but untested | **RATIFIED (unused)** |
| `dependent_settlement_of` | hierarchy (QR-203) | **held** — 0 usable cases | **PROVISIONAL (held)** |
| `produced_phase` / `terminated_phase` / `damaged` | conflict→phase (QR-301/304/502) | filed **conditionally on Phase** | **PROVISIONAL (conditional)** |
| `interaction_mechanism` (attribute) + 9 terms | mechanisms (QR-305) | Amendment 1 **adopted**; 9 of 11 terms at threshold; `pilgrimage`/`communication` held | **RATIFIED (attribute); 9/11 terms** |
| `intervisible_with` | viewshed output (QR-501) | **held — 0 cases by design** (computed, not attested) | **PROVISIONAL (by design)** |

**Existing enum terms — ratified, NOT provisional** (already in corpus use, so any entry leaning only on these is not vocabulary-provisional): `contains` (27 uses), `near` (21), `belongs_to` (5), `adjoins` (2), `different_from` (8), `lies_on_route` (3), `located_at` (26), `rebuilt` (9), `captured` (5), `founded` (6). QR-204, QR-303's `contains`/`depends_on`-adjacent structure, and QR-302's `belongs_to` draw on these and are **not** marked vocabulary-provisional on their account.

**Consequence for D1, stated before running:** any entry whose run leans on a provisional term has its result **marked provisional** (`PASS*`). A `PASS*` means *the model expresses the structure; the vocabulary is not yet ratified* — a known-provisional outcome, categorically distinct from a model-defect FAIL. This marking is applied at run time, not reconstructed after.

---

## Deliverable 1 — Expressibility run (all 22 entries)

Run against the committed fixture schema (`tests/logical_model_fixture/schema.py` + `fixture.py`). The test is **structural expressibility**: can the model, as realised in the fixture schema, express the entry's field-2 inventory and return the answer-shape field-1 describes. Category 1 additionally run against the live corpus (D1a).

`PASS` = expresses cleanly, no provisional dependency. `PASS*` = expresses cleanly **but** depends on ≥1 provisional term (vocabulary-provisional, not a failure). No entry returned FAIL or a model-attributable partial.

| Entry | Cat | Result | Provisional dependency (if any) |
|---|---|---|---|
| QR-101 | 2 | **PASS\*** | `traverses`, `crosses_at` |
| QR-102 | 2 | **PASS\*** | `controls`, `overlooks` |
| QR-103 | 2 | **PASS\*** | `member_of_route_family` (held) |
| QR-104 | 4 | **PASS\*** | `traverses`, `member_of_route_family`; + evidence-coverage note (terrain cost surface is external data) |
| QR-201 | 3 | **PASS** | — |
| QR-202 | 3 | **PASS** | — |
| QR-203 | 2 | **PASS\*** | `dependent_settlement_of` (held); `subordinate_to` ratified-but-unused |
| QR-204 | 2 | **PASS\*** | `controls`, `crosses_at`, `member_of_argued_group` (existing `adjoins`/`near` are not provisional) |
| QR-205 | 2 | **PASS\*** | `member_of_argued_group` |
| QR-301 | 2 | **PASS\*** | `produced_phase`, `terminated_phase`, `damaged` (conditional on Phase) |
| QR-302 | 3 | **PASS\*** | `restores` (held); `belongs_to`/`held_by` — `belongs_to` existing, `held_by` new |
| QR-303 | 2 | **PASS\*** | `depends_on` (new); `contains` existing (not provisional) |
| QR-304 | 2 | **PASS\*** | `damaged`, `terminated_phase` |
| QR-305 | 2 | **PASS** | mechanism attribute ratified; uses `diplomacy` (a ratified mechanism) |
| QR-401 | 1 | **PASS** | — (corpus-reconciled, D1a) |
| QR-402 | 1 | **PASS** | — (corpus-reconciled, D1a) |
| QR-403 | 2 | **PASS\*** | `corroborates`, `parallel_case` |
| QR-404 | 3 | **PASS** | — (full-set competing geometries + functional certainty exercised) |
| QR-441 | 1 | **PASS** | — (corpus-reconciled, D1a) |
| QR-501 | 2 | **PASS\*** | `controls`, `overlooks`; `intervisible_with` inputs-only by design |
| QR-502 | 3 | **PASS\*** | `produced_phase`, `terminated_phase` (competing-scheme view exercised) |
| QR-503 | 2 | **PASS\*** | `examined` |
| QR-504 | 3 | **PASS** | — (region temporal extent + names temporal validity exercised) |
| QR-544 | 1 | **PASS** | — (corpus-reconciled, D1a) |

**Tally: 22 of 22 express structurally. 9 clean PASS, 13 PASS\* (vocabulary-provisional). Zero FAIL, zero model-attributable partial.** The model, as realised, expresses every register entry's field-2 inventory and answer-shape. Thirteen entries await vocabulary ratification — a §5.5 clock matter, not a design matter.

---

## Deliverable 1a — Category-1 corpus reconciliation against calibration

The four category-1 entries were calibration-run at zero divergences (2026-07-23); their field-3 predictions are immutable under §7.2 Rule 1(a); the corpus is unchanged (confirmed above). **Every figure reproduces the committed calibration exactly. No divergence.**

| Entry | Figure | Calibration | Step-4 re-measure | Reconciliation |
|---|---|---|---|---|
| **QR-402** | attestations | 477 | 477 | **MATCH** |
| | provenance categories | 12 | 12 | **MATCH** |
| | primary_paraphrase | 225 | 225 | **MATCH** |
| | archaeological_evidence | 57 | 57 | **MATCH** |
| **QR-401** | assertions | 254 | 254 | **MATCH** |
| | attestations supporting no assertion | 208 of 477 | 208 of 477 | **MATCH** |
| | assertions >1 supporting att | 32 of 254 | 32 of 254 | **MATCH** |
| **QR-441** | identification_status on places | 190/190 | 190/190 | **MATCH** |
| | coordinate_confidence | 57/57 | 57/57 | **MATCH** |
| | confidence on relationships | 144/144 | 144/144 | **MATCH** |
| | overall_confidence | 325 | 325 | **MATCH** |
| | start_date.confidence | 52/54 | 52/54 | **MATCH** |
| | functional certainty bearer | NONE | NONE | **MATCH** |
| **QR-544** | places | 190 | 190 | **MATCH** |
| | alternative_names | 152 | 152 | **MATCH** |
| | coordinates | 57 | 57 | **MATCH** |
| | disputed | 7 | 7 | **MATCH** |
| | linked_attestations | 190/190 | 190/190 | **MATCH** |
| | no coordinate | 133 (70.0%) | 133 (70.0%) | **MATCH** |

**Reconciliation verdict: exact match on all nineteen tracked figures.** Neither of the two checkable divergence causes is present — the corpus has not moved (git log clean) and the Step-4 measurement reproduces the calibration measurement. The calibration record stands as a verified fixed point, and the Step-4 run is confirmed against it. The `coordinate_confidence` field-name subtlety the calibration caught (`coordinates.coordinate_confidence`, not `coordinates.confidence`) was applied here, so the 57/57 reproduces rather than re-tripping the original measurement error.

---

## Deliverable 2 — Classification of every non-pass to the §5.9 completion gate

**There is no FAIL and no model-attributable partial to classify.** Every entry expresses. What requires classification is the **thirteen PASS\*** — each is a pass whose *acceptance-test* result is clean but whose *vocabulary* is unratified. Under the register's four-way scheme these are **VOCABULARY** dependencies, and the Rule 3 burden requires each to be positively established: name the term, and confirm the entry passes with the term ratified. That confirmation is direct here — the expressibility run *already passed the structure* with the provisional term instantiated in the fixture, so ratification changes the term's status, not the entry's result.

| Entry | Classification | Term(s) named | Passes on ratification? (Rule 3 burden) |
|---|---|---|---|
| QR-101 | **VOCABULARY** | `traverses`, `crosses_at` | Yes — structure passed with the terms present; `crosses_at` is filed (4 cases), `traverses` held (routes pending) |
| QR-102 | **VOCABULARY** | `controls`, `overlooks` | Yes — both filed (3 cases each); structure passed |
| QR-103 | **VOCABULARY** | `member_of_route_family` | Yes on ratification, **but** the term is *held* pending route extraction — see cross-note |
| QR-104 | **VOCABULARY + EVIDENCE-COVERAGE** | `traverses`, `member_of_route_family` (vocab); terrain cost surface (evidence) | Vocab: yes on ratification. Evidence: the cost surface is **external data, not model capability** — the model expresses the modelled route and its `gis_derived_observation` provenance; the DEM is corpus-external input |
| QR-203 | **VOCABULARY** | `dependent_settlement_of` (held); `subordinate_to` (ratified, unused) | `subordinate_to` needs no ratification; `dependent_settlement_of` is held pending named dependent entities |
| QR-204 | **VOCABULARY** | `controls`, `crosses_at`, `member_of_argued_group` | Yes — all filed; the `adjoins`/`near` portion is already-ratified enum |
| QR-205 | **VOCABULARY** | `member_of_argued_group` | Yes — filed (3 cases); structure passed |
| QR-301 | **VOCABULARY** | `produced_phase`, `terminated_phase`, `damaged` | Yes on ratification — filed **conditional on Phase**; Phase is net-new construction (migration step 9), so see cross-note |
| QR-302 | **VOCABULARY** | `restores` (held), `held_by` (new) | `restores` held pending TerritorialUnit instances; structure passed |
| QR-303 | **VOCABULARY** | `depends_on` (new) | Yes — `contains` portion already enum |
| QR-304 | **VOCABULARY** | `damaged`, `terminated_phase` | Yes on ratification (conditional on Phase) |
| QR-403 | **VOCABULARY** | `corroborates`, `parallel_case` | Yes — both filed; structure passed |
| QR-501 | **VOCABULARY** | `controls`, `overlooks` | Yes; `intervisible_with` is inputs-only by design, not a blocking dependency |
| QR-502 | **VOCABULARY** | `produced_phase`, `terminated_phase` | Yes on ratification (conditional on Phase) |
| QR-503 | **VOCABULARY** | `examined` | Yes — filed (19+ cases); structure passed |

**Two cross-notes where a VOCABULARY classification would be too cheap if left unqualified — Rule 3 discipline applied:**

1. **QR-103, QR-104 `member_of_route_family` / `traverses` are held for a reason that is EVIDENCE-COVERAGE, not merely vocabulary.** The terms are held because the corpus has **one** route record — route families cannot be attested until routes are extracted (Phase 3). So the honest classification is **VOCABULARY *gated behind* EVIDENCE-COVERAGE**: ratifying the term needs the three cases, and the cases need the extraction. Naming it "vocabulary" alone would understate the dependency. The **model** expresses the m:n structure (proven in the fixture, case 18); the gap is corpus content plus the clock.

2. **QR-301, QR-304, QR-502 `produced_phase` / `terminated_phase` / `damaged` are conditional on Phase, which is MIGRATION (step 9, net-new construction).** So these carry **VOCABULARY conditional on MIGRATION**: the terms were filed conditionally on Phase existing, and Phase arrives at migration step 9. Per the Rule 3 migration burden, the migration is named (step 9, Phase/Component construction) and sufficiency is confirmed — the fixture *has* Phase and the structure passed against it, so once step 9 builds Phase in the corpus the entries express. "Needs migration" is established as sufficient, not asserted.

**No entry is classified ONTOLOGY DEFECT.** The residual was not reached, because for every non-clean entry a cheaper cause (vocabulary, and behind it migration or evidence-coverage) was **positively established** — the structure passed in the fixture with the term/type present, which is the positive evidence Rule 3 demands. No entry required reopening `logical_model.md` or the frozen ontology. The pressure Rule 3 warns of — relabelling a design defect as a cheap dependency — did not arise, because there was no failing structure to relabel: everything expressed.

---

## Closing flag — fixture gap vs expressibility failure (held distinct)

The brief requires confirming that where the fixture exercises an entry's field-2, it is because the model *can* produce the structure — not that a fixture gap is masking an expressibility failure one level down.

**No fixture gap arose in this run.** Every field-2 inventory line had a fixture record (confirmed in Step-3a Part D and instantiated in Step-3b). No entry hit a "fixture cannot exercise this" condition, so the two categories the brief asks to keep distinct did not need separating in practice — but they are defined here for the record:

- **Fixture gap (Step-3 manifest correction):** field-2 needs a structure the model *can* express but the fixture lacks a record for. Remedy: add a fixture record. Not a model finding.
- **Expressibility failure one level down:** the fixture lacks the record *because the model cannot produce the structure the record would need*. Remedy: this is a model/ontology finding, routed through the four-way classification. Not a manifest correction.

The single item that came closest was Step-3b's I3 fixture bug (name/interpretation attestations supporting no assertion) — resolved there as a manifest correction, confirmed genuinely a missing-record issue (the model expresses assertion support fine), not an expressibility failure. It is already committed-fixed in the suite this run used; no residue reaches Step 4.

**One item flagged for the record, not a failure:** `co_located_aspect` (dual-aspect link, item 17 / QR-501) is **not yet filed** in the proposals doc — it was surfaced by the logical model after the vocabulary filing. It needs a §5.5 filing of its own. The fixture instantiates it provisionally and QR-501 passed structurally; the action is a filing, not a model change.

---

*Held for review. Read-only; committed fixture and, for category 1, the live corpus; no corpus record touched; no migration. Frozen ontology and committed model only.*
