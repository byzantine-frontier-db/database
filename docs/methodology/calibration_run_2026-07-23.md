# Query Register — Calibration Run

**Executed:** 2026-07-23, read-only, against `origin/main` at `baebd01`.
**Entries:** QR-401, QR-402 (primary); QR-441, QR-544 (derived, corroborative).
**Predictions tested against:** the committed text of `docs/methodology/query_register_format.md` §5 and `docs/methodology/query_register_entries.md`, read from the repository rather than recalled. No prediction amended, per register §7.2 Rule 1.
**Rule 16 applied throughout:** every count verified candidate by candidate before being reported or acted on.

---

## 1. Result

> **Zero divergences. Every figure the four entries commit to was measured exactly. Four passes of four.**
>
> **No discrepancy record opened.** No entry failed, so §7.2's procedure is not engaged.

The three figures named as the specific test — the 208-of-477, the 32-of-254, and the twelve-category provenance distribution — matched to the record and to the category. The provenance distribution matched on **all twelve values simultaneously**, which is the figure hardest to have arrived at by estimation.

**Corpus stability confirmed first.** `git log 44988e2..HEAD -- records/` returns empty: no record changed between the recording of the predictions and this execution. A divergence could therefore not have been explained under §7.2 classification (ii), and that route was closed before measurement rather than after.

---

## 2. QR-402 — Provenance chain preservation · **PASS** *(primary)*

| Figure committed | Predicted | Actual | |
|---|---|---|---|
| Attestations | 477 | **477** | ✓ |
| Sources present | 79 | **79** | ✓ |
| Attestations with a malformed or non-single `source` | 0 | **0** | ✓ |
| Dangling source references | 0 | **0** | ✓ |
| Rule-8 violations (empty claim) | 0 | **0** | ✓ |
| Missing provenance / confidence / citation | 0 / 0 / 0 | **0 / 0 / 0** | ✓ |
| Provenance categories in use | 12 | **12** | ✓ |
| Attestations supporting no assertion | 208 (43.6%) | **208 (43.6%)** | ✓ |

**Provenance distribution — all twelve values:**

| Category | Pred. | Act. | | Category | Pred. | Act. | |
|---|---|---|---|---|---|---|---|
| primary_paraphrase | 225 | **225** | ✓ | primary_summary | 11 | **11** | ✓ |
| modern_synthesis | 95 | **95** | ✓ | modern_identification | 9 | **9** | ✓ |
| archaeological_evidence | 57 | **57** | ✓ | epigraphic_evidence | 2 | **2** | ✓ |
| primary_quotation | 33 | **33** | ✓ | numismatic_evidence | 2 | **2** | ✓ |
| gis_derived_observation | 22 | **22** | ✓ | cross_source_synthesis | 1 | **1** | ✓ |
| primary_observation | 19 | **19** | ✓ | modern_interpretation | 1 | **1** | ✓ |

Sums to 477. **Exact match on every category.**

**Acceptance: PASS.** Every attestation resolves to source, provenance category, evidential confidence and citation in a single pass with no transformation step. Evidential confidence is a field on the attestation and is not reachable through, or coerced into, any of the five substantive dimensions — `overall_confidence` exists on places, persons and events, and on no attestation.

---

## 3. QR-401 — Corroboration and single-witness assertions · **PASS** *(primary)*

| Figure committed | Predicted | Actual | |
|---|---|---|---|
| Assertions | 254 | **254** | ✓ |
| Attestations | 477 | **477** | ✓ |
| Sources | 79 | **79** | ✓ |
| Attestations supporting no assertion | 208 of 477 (43.6%) | **208 of 477 (43.6%)** | ✓ |
| Assertions with >1 supporting attestation | 32 of 254 (12.6%) | **32 of 254 (12.6%)** | ✓ |
| Assertions with zero support (I4) | implied 0 | **0** | ✓ |

Single-witness/multiply-attested separation: **222 single, 32 multiple**, computed directly.

**Acceptance: PASS.** All four clauses satisfied — supporting attestations returned with source, provenance and evidential confidence; single-witness distinguished from multiply-attested; transmission route derived from the citation (§6); no transformation step; evidential confidence unaggregated.

---

## 4. QR-441 — Certainty-dimension separability audit · **PASS** *(derived)*

| Figure committed | Predicted | Actual | |
|---|---|---|---|
| `identification_status` on places | 190/190 | **190/190** | ✓ |
| `identification_confidence` on places | present | **190/190** | ✓ |
| `coordinate_confidence` on coordinate-bearing places | 57/57 | **57/57** | ✓ *(see §7)* |
| `confidence` on relationships | 144/144 | **144/144** | ✓ |
| `confidence` on attestations | all | **477/477** | ✓ |
| `confidence` on interpretations | all | **174/174** | ✓ |
| `start_date.confidence` on events | 52 of 54 | **52 of 54** | ✓ |
| `overall_confidence` | exactly 325 | **325** (places 190, persons 81, events 54) | ✓ |
| Functional certainty bearer | **none** | **none** — no field matching `/function/` exists on any record of any type | ✓ |

**Acceptance: PASS.** The audit returns a complete per-type map of bearers and counts, identifies `overall_confidence` on exactly 325 records, and confirms functional certainty as unborne.

---

## 5. QR-544 — Gazetteer generation · **PASS** *(derived)*

| Figure committed | Predicted | Actual | |
|---|---|---|---|
| Places | 190 | **190** | ✓ |
| With `standardised_name` | 190 | **190** | ✓ |
| With `identification_status` | 190 | **190** | ✓ |
| With `alternative_names` | 152 | **152** | ✓ |
| With coordinates | 57 | **57** | ✓ |
| Proportion carrying no coordinate | 70% | **70.0%** (133 of 190) | ✓ |
| `identification_status: disputed` | 7 | **7** | ✓ |
| `linked_attestations` populated | all | **190/190**, none missing | ✓ |

**The artefact was generated, not merely costed.** A complete 190-entry gazetteer was produced in one pass, alphabetically ordered, each entry carrying names with language and name type, location with method, uncertainty radius and spatial confidence, identification status with identification confidence, and inline evidence resolving 426 attestation references to source, provenance and evidential confidence. Header coverage statement: *57/190 located (30%); 133 unlocated (70%); 7 disputed identifications.* Zero entries lacked an evidence block.

**Acceptance: PASS.** Three separately-named uncertainty quantities printed per entry (identification, spatial, evidential); corpus-level coverage statement present; no manual assembly.

*One incidental observation.* The generated gazetteer includes the five polity records — the Abbasid Caliphate appears as a gazetteer entry, unlocated. This is the §2.1 modelling error surfacing in output rather than in analysis, and it is the clearest practical illustration yet of why the place/polity split is worth doing.

---

## 6. Functional test — the mediation flag

QR-402's Pass clause requires the mediation flag to be derived from the citation. It can be, and is.

| | Count |
|---|---|
| Raw scan total | 234 of 477 |
| False positives on reading | **22** |
| **Verified mediation citations** | **212 of 477 (44.4%)** |

Markers used across the 212: `reached via` 194, ` via ` 10, `cited in` 2, `quoted in` 1, `reported in` 1.

**All 22 false positives are one class:** citations of the form *"coordinate 37N N4270288 E368271, converted to WGS84 **via** pyproj"* — a coordinate transformation, not a transmission route. Reported as verified rather than as the scan total, per rule 16.

**Substantive finding:** nearly half of all attestations were reached through an intermediary, and 194 of the 212 use the single marker *reached via*. That is direct corroboration of conceptual ontology §5.4's prospective argument — the corpus is dominated by one secondary transmission route, which is why multiple attestation is presently suppressed.

---

## 7. The one apparent divergence, and its classification

**`coordinate_confidence`: predicted 57/57, first measured 0/57.**

**Classification: measurement error, not prediction error. The register was correct.**

On verification the field is `coordinates.coordinate_confidence`, populated on 57 of 57. My first scan queried `coordinates.confidence`, which does not exist. The prediction was right; the measurement was wrong.

This matters more than the figure does. It is **rule 16's fourth instance class recurring — reading the wrong field name — and it recurred inside the run designed to test predictions.** Had I classified at first measurement, I would have opened a false discrepancy against QR-441, recorded a prediction error that did not occur, and possibly proposed remediation for a field that is completely populated. Rule 16 caught it because classifying a discrepancy is a governance action, and a governance action may not rest on an unverified count.

No discrepancy record is opened, because there was no discrepancy.

---

## 8. Two findings not predicted

Neither contradicts a committed figure. Both refine what a committed figure means.

**(a) Of the 32 multiply-attested assertions, 3 rest on a single source.** OBS-0253 (2 attestations), OBS-0057 (2), OBS-0103 (3) each draw multiple attestations from one source. The committed figure — *"32 of 254 assertions have more than one supporting attestation"* — is exactly correct as worded. But **genuine multi-source corroboration is 29 of 254 (11.4%), not 32 (12.6%)**, and the corroboration picture is thinner than the sentence reads.

QR-401's scholarship limitation anticipated the shape of this — *"'independent' is a scholarly judgement the query cannot make"* — but anticipated it one step too late. It warned that distinct sources are not independent witnesses; it did not warn that **multiple attestations are not even distinct sources**. That is a gap between the figure and its meaning, and it should be closed in field 4 when the entry is next amended.

**(b) The mediation flag errs in both directions, not one.** QR-402's scholarship limitation predicted *"a string test [that] will miss unconventional phrasings; the count is a lower bound."* It does miss phrasings — but it also over-matches, by 22. The prediction about the *direction* of error was wrong even though the prediction about its *character* was right.

**Both are field-4 corrections, and field 4 is amendable.** §7.2 Rule 1 makes **field 3** immutable once an entry is approved; the limitations field carries no such restriction, and correcting it is how the register learns. Neither correction touches a prediction and neither is proposed here — this run reports, and amendment is a separate act.

---

## 9. Register accuracy tally — §7.3

| Metric | Value |
|---|---|
| Predictions upheld / entries executed | **4 / 4** |
| Discrepancies opened | **0** |
| Discrepancies by classification (i)–(iv) | none |
| **Category-1 entries that failed** | **0 of 4** |

The last row is the diagnostic one, and it is clean.

---

## 10. What this establishes, and what it does not

**Establishes.** The register's category-1 predictions were **measured, not estimated**. That was the specific question, and the twelve-category provenance distribution settles it: twelve simultaneous exact matches, including four categories with counts of one or two, is not a pattern estimation produces. The two primary entries — neither selected for executability — carry every figure exactly.

**Does not establish.** Nothing about categories 2, 3 or 4, and nothing about the logical model, which does not exist. All four entries sit in the epistemic layer or read the present place records directly; the corpus understanding tested is of the part already implemented, which is the part the register itself identifies as the corpus's strength. A calibration set drawn entirely from the working half of a system is a weak test of understanding of the whole, and the register said as much when it recorded that only one of nineteen primary entries was corpus-executable.

**One limitation of the exercise itself, worth recording.** I authored both the predictions and the measurements. This run detects estimation passed off as measurement — which is what it was for, and it found none — but it cannot detect motivated reasoning shared between the two acts, because the same understanding produced both. The §7 procedure's burden rules are designed for the case where a model author diagnoses a failure under pressure; they do not cover an author checking their own arithmetic. An independent execution of the same four entries would be a stronger datum than this one, and if the calibration set is ever re-run, it should be re-run by someone else.

---

*Read-only. No patches, no records, no schema. Suggested repository path: `docs/methodology/calibration_run_2026-07-23.md`.*
