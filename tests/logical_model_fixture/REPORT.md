# Step 3b — Conformance and Discrimination Report

**Status:** held for review. Delivery is not commit.
**Build spec:** the ratified Step-3a schema-realisation plan, fixture manifest, and conformance plan — realised, not re-derived.
**Read against:** commit `63e88eb` (carries `logical_model.md`). Read-only against the corpus; the fixture is synthetic in the reserved `FX-` space, workspace-only, no corpus record touched, no migration.
**How to reproduce:** in this directory, `python3 run_gates.py` (conformance + discrimination) and `python3 perturb_test.py` (proves each counterfactual derives, not asserts). Exit 0 iff every gate / every case passes.

---

## Gate-3 correction (this revision)

The prior Gate 3 had a confined defect: counterfactuals **16, 17, and 5b** reported the wrong-model observable as a **hardcoded literal** rather than deriving it from the fixture under the wrong constraint. 15/18/19a already derived. The standard: changing the fixture must change the result. This revision fixes the three:

- **16** — `obs_ter16_rowcount` now collapses the *actual* `FX-TER-16a/16b` rows under the tolerate-merge by folding along the *actual* `restores` edges present, and counts the surviving rows and surviving edges. Both numbers are computed from fixture data.
- **17** — `obs_dual17` under `allow_contains_dual` now derives one `contains` edge *per real `co_located_aspect` edge present* between `FX-LFT-17`/`FX-SIT-17` and counts it. The `1` is an observed, derived edge, not a literal.
- **5b** — the divergence key is now the **derived subject-set shape** (`identifying_subjects`, 0 vs 4), which `assertion_subject_set` computes from the fixture under `candidate_in_dedup`; `assertions_from_two_atts` is likewise derived by counting distinct dedup keys over the actual subject links, not returned as a literal.
- **18** — additionally hardened: the single-parent wrong-model now keeps the first membership *by id* from the actual edges, so the survivor count tracks which edges exist (removing them moves it to 0), rather than `min(1, n)` which was insensitive at n≥1.

No model change, no schema change, no fixture-structure change beyond what deriving the three observables requires (none was needed — the derivations read existing fixture records). Scope change limited to adding `perturb_test.py`.

---

## Result

```
FIXTURE LOADED: 307 records
GATE 1 — structural conformance ............ PASS
GATE 2 — validator invariants .............. PASS (7/7 hard invariants clean)
GATE 2 — boundary cases (13, 14) ........... PASS (boundary reported, not solved)
GATE 3 — six executed counterfactuals ...... PASS (6/6 diverge, all derived)
PERTURBATION SELF-TEST (perturb_test.py) ... GREEN (6/6 observables move under mutation)
RESULT: ALL GATES PASS
```

The schema (`schema.py`), fixture (`fixture.py`), harness (`run_gates.py`), and perturbation self-test (`perturb_test.py`) are the executable artifacts. This report records what they produced.

## Perturbation self-test — proof of derivation

`perturb_test.py` proves each of the six counterfactuals **discriminates by derivation, not by literal**. For each case it mutates a fixture record the case depends on, re-runs the wrong-model observe function, and asserts the observable **changed**. A derived observable moves under perturbation; a literal cannot — so the test fails on any literal. All six move:

| Case | Discrimination depends on (record perturbed) | Wrong-model observable: before → after |
|---|---|---|
| 15 | `FX-PHA-15c` (the post-gap phase) | `site_rows_for_gap_entity` 2 → 1 |
| 16 | `FX-REL-16` (the restores edge) | `territorial_unit_rows` 1 → 2 |
| 17 | the `co_located_aspect` edge (LFT-17/SIT-17) | `forbidden_contains_edges` 1 → 0 |
| 18 | `FX-RTE-18t`'s membership edges | `track_family_memberships` 1 → 0 |
| 19a | `FX-CMP-19b`'s footprint (shared vs distinct) | `component_rows_on_footprint` 1 → 2 |
| 5b | `FX-ATT-5b2`'s candidate subject links | `identifying_subjects` 4 → 2 |

Each dependency is the exact record whose presence the wrong constraint's failure hinges on; the test names it so the discrimination dependency is explicit rather than implicit. **`perturb_test.py` is part of the suite and part of the run instructions above.**

---

## Gate 1 — structural conformance

Every one of the 307 fixture records conforms to the schema: table membership, column types, enum domains (`spatial_type`, `reference_mode`, `assertion_kind`, `polarity`, `provenance`), the `GeometryType` CHECK (four types only), and every structural / by-absence constraint (I2, I5b, I6 exclusion, I10 attachment, I11 single-valued FK, I12 by-absence). **Zero violations.**

**One fixture bug was found and fixed during the run — reported as a fixture bug, not a model finding, per the brief.** The first execution flagged **I3** (every attestation supports ≥1 assertion) against ten attestations: the name-attestations (`FX-NAM-04*-at`), the interpretation-evidence attestations (`FX-ATT-10a/10b/11a/11b/205/403`), and the deprecated `FX-ATT-12`. These were attestations the manifest introduced to evidence *names* and *interpretations* but which supported no *assertion*, violating I3. The fix is fixture-side (`_support_all_attestations`): each such attestation now also supports a minimal assertion — a name is a proposition about its entity, and a deprecated attestation still made a claim (its wrapping assertion is correspondingly marked deprecated). **No schema or model change** — the model's I3 is correct as written; the fixture had simply under-built. This is exactly the "manifest line unbuildable as written → manifest correction" path, and it is logged in §5 below.

---

## Gate 2 — validator invariants

All seven hard validator invariants hold, each exercised by ≥1 conforming instance:

| Invariant | Result | Exercised by |
|---|---|---|
| I1 domain-entity-evidenced | clean | every domain entity carries a definite QSL |
| I3 attestation-supports-assertion | clean | every attestation in ≥1 `supporting_attestations` (post-fix) |
| I4 assertion-has-attestation | clean | every assertion has ≥1 supporting attestation |
| I5 interpretation-evidence (ATT-only) | clean | `FX-INT-*` cite attestations via the junction |
| I8 relationship-scope-within-phase | clean | phase-endpoint relationships within scope |
| I9 designation-valid + rationale | clean | `FX-SIT-09` designated `FX-SPA-09b` with rationale |
| RI relationship-endpoints | clean | every polymorphic endpoint resolves (flagged reading 1: validator + partial FK) |

Flag-class checks (I5a interpretation cross-reference, I7 existence-interval) report clean: `FX-INT-11a`↔`11b` carry an explicit `contradicts` relationship (not just prose), so I5a does not fire; the gap-tolerant `FX-SIT-15` existence interval is the span 730–850 and no phase falls outside it, so I7 does not fire.

### Boundary cases — reported, not solved

- **13 competing phase divisions.** Two phasing schemes (`A`: 2 phases; `B`: 3 phases) coexist on `FX-SIT-13`, each internally ordered and non-overlapping (I6 keyed on `(subject, scheme)`). **Reconciliation records: 0.** The harness asserts `13_boundary_correct = (two schemes AND zero reconciliation)` — the model represents both divisions and declines to reconcile them, which is the honest limit (model §10.13). A fixture that added a reconciliation record would assert a capability the model disclaims; the check confirms none exists.
- **14 negative evidence.** Three-way distinction present: `FX-ASR-14a` (asserted present), `FX-ASR-14b` (denied, with `FX-EVT-14.detection_scope`), `FX-SIT-14u` (never examined by excavation). **Residual assertion absent:** the harness confirms no assertion whose proposition starts "period-Z" exists — the examined-and-found-but-never-entered case is the deliberately empty slot (`FX-RESIDUAL-14`), demonstrably outside what the store represents (model §10.14). `14_boundary_correct = asserted ∧ denied ∧ residual-absent`.

---

## Gate 3 — six executed counterfactuals

**Each divergence below is observed by running a wrong-constraint variant of the schema against the same fixture pairing — not argued.** For each case: the correct model's observed result, the wrong model's observed result on the identical fixture, and the divergence, which matches the predicted observable from Step-3a Deliverable 3.

| Case | Wrong constraint (built and run) | Correct observed | Wrong observed | Predicted observable (3a-D3) | Diverges |
|---|---|---|---|---|---|
| **15** Site gap | `unified_gap_rule = "split"` | `site_rows_for_gap_entity = 1` | `= 2` | Site row count 1 vs 2 | **YES** |
| **16** TU interruption | `unified_gap_rule = "tolerate"` | `territorial_unit_rows = 2, restores_edges = 1` | `= 1, 1` | TU count 2 vs 1 (derived by collapsing real rows along real edges) | **YES** |
| **17** dual aspect | `allow_contains_dual = True` | `forbidden_contains_edges = 0` | `= 1` | forbidden `contains` edge derived per real co_located edge | **YES** |
| **18** route braiding | `single_parent_family = True` | `track_family_memberships = 2` | `= 1` | membership rows 2 vs 1 (first-by-id survives) | **YES** |
| **19a** component | `footprint_identity = True` | `component_rows_on_footprint = 2, dangling = 0` | `= 1, 1` | rows 2 vs 1; `succeeds` dangles | **YES** |
| **5b** pooling | `candidate_in_dedup = True` | `identifying_subjects = 0` (pooled 4 non-id) | `= 4` (4 identifying) | subject-set shape 0 vs 4 (derived from the view) | **YES** |

**Six run counterfactuals, six observed divergences, each matching its predicted observable.** The fixture discriminates against a *real* wrong model, not a described one. The 15/16 pair is the decisive demonstration: the two wrong rules are the *same* uniform rule applied under two settings — `split` breaks 15 (the Site), `tolerate` breaks 16 (the TerritorialUnit) — and because both entities are in the one fixture, no single uniform gap rule passes both, which is precisely why the model forbids a unified rule and why the two cases share a fixture.

### How each counterfactual is constructed (so the run is auditable, not magic)

- **15/16** — the wrong schema applies one gap rule to *all* spatial subjects. `split` re-runs the phase-run detector on `FX-SIT-15` and emits one Site per contiguous run (→ 2); `tolerate` merges dissolution-recreation into one TerritorialUnit and drops the `restores` edge (→ 1). The correct schema leaves Site identity gap-tolerant and TU identity gap-breaking.
- **17** — `allow_contains_dual` lets a containment default emit a `contains` edge between `FX-LFT-17` and `FX-SIT-17`; the correct schema carries only `co_located_aspect` and the harness counts forbidden `contains` edges (0 vs 1).
- **18** — `single_parent_family` truncates `FX-RTE-18t`'s memberships to the first; the correct m:n keeps both.
- **19a** — `footprint_identity` groups components on `(parent_site, footprint)` and merges the two same-footprint walls, leaving the `succeeds` edge dangling; the correct fabric identity keeps two.
- **5b** — `candidate_in_dedup` folds candidate subjects into the dedup key, so disjoint candidate sets key to two assertions; the correct rule excludes candidates (flagged reading 2: absence-of-identifying-rows), pooling to one assertion with four non-identifying subjects.

---

## The two flagged readings — wired as specified, still flagged

Both were carried into the build exactly as Step-3a specified, and **neither is settled here.**

1. **Relationship RI — validator + optional partial FK** (`RI_MODE = "validator+partial"`). The RI check runs as a validator over polymorphic endpoints; same-type pairs are admitted (no distinctness constraint), which the 19a `succeeds` (Component→Component) and the harness's `distinctness_on_rels` switch confirm: turning the wrong distinctness constraint *on* would reject the same-type pair. Left flagged.
2. **Pure-candidate subject set — absence of identifying rows** (`pure_candidate_repr = "absence"`). `FX-ASR-5b` yields zero identifying subjects and four non-identifying — the absence semantics. Left flagged.

**If Step 4's expressibility run exposes the pure-candidate representation as ambiguous, it routes through the register's four-way dependency classification (ontology-defect / vocabulary / migration / evidence-coverage), not through governance §5.8** — `logical_model.md` is a working document, not frozen, and only an ontology-defect finding touches design. Recorded here so the routing is fixed before Step 4, not decided under pressure.

---

## Manifest lines flagged during the build

Per the brief: unbuildable-as-written lines are **manifest corrections**, not licence to change the model or schema. One arose:

- **I3 coverage of name- and interpretation-attestations.** The manifest (Part A items 4, 10, 11, 12; Part D QR-205, QR-403) introduced attestations evidencing names and interpretations without also supporting an assertion, which I3 forbids. **Correction:** the fixture wraps every such attestation in a minimal supporting assertion (a name is a proposition; a deprecated attestation still claimed something). No model or schema change. This should be reflected in the manifest as a one-line note that name/interpretation attestations, like all attestations, must support an assertion under I3 — the manifest's Part D "every FX-ATT carries source+provenance by construction" is true but insufficient; I3 also requires assertion support.

No other manifest line was unbuildable. Every Part-A/B/C record and every Part-D `+add` instantiated as written, and every register field-2 line has its record.

---

## Provisional vocabulary

Cases using not-yet-ratified terms ran with their provisional terms and are structurally identical to their post-ratification form — a later ratification changes a term's status, not the fixture's structure. Provisional terms exercised: `co_located_aspect` (17), `traverses`/`crosses_at` (QR-101/104/204), `member_of_argued_group` (QR-205), `subordinate_to` (QR-203), `produced_phase`/`terminated_phase`/`damaged` (QR-301/304), `examined` (QR-503/14), `corroborates`/`parallel_case` (QR-403), `interaction_mechanism` (QR-305, ratified subset). `intervisible_with` is inputs-only by the manifest (QR-501) and is not instantiated as data.

---

*Held for review. Synthetic fixture, workspace-only; no corpus record touched; no migration. Frozen ontology via the committed logical model only; no v2_preview.*
