# Vocabulary Extension Proposals — governance §5.5

**Filed:** 2026-07-23
**Contributor:** Claude (review/validation layer), at Curtis's instruction
**Vocabularies affected:** `RelationshipType`; `EventCategory` and `EventSubCategory`
**Decision required:** Editorial Board majority per governance §5.5
**Suggested repository path:** `docs/schema/vocabulary_proposals_2026-07-23.md`

Filed now rather than at migration step 7 so that the approval process runs in parallel with the migration work. Nothing here requires the migration to have started.

---

## 0. Summary, and four corrections to the ontology's own assumptions

Conceptual ontology v0.2 §6.2 and §14.5 named **roughly twenty-four candidate terms**. Establishing three concrete cases for each against the live corpus — rather than assuming them — supports **eleven for immediate filing, three conditionally, and leaves ten held**. Four terms are **withdrawn before filing**.

That ratio is the point of the exercise. Terms proposed from intuition about what a frontier ontology needs did not survive contact with what the corpus actually attests.

**Four corrections the scan forced, in both directions:**

| Term | v0.2 said | Corpus says | Correction |
|---|---|---|---|
| `excavation` | defer to Phase 3 — no cases yet | **9 cases** (Tarsus, Sumaysāṭ, Dibsi Faraj, Tilbeşar, Ruṣāfat Hishām, Ḥiṣn al-Tīnāt, Domuztepe, Bolkardağ, ʿAyn Zarba) | **File now** |
| `remote_sensing_survey` | defer to Phase 3 | **3 cases** (ATT-0134, ATT-0115 CORONA; ATT-0229 remote sensing) | **File now** |
| `material_reexamination` | file now — three cases available | **2 cases only.** The apparent third was double-counting: ATT-0440 is a site visit that included basket examination, and 29 further "autopsy" hits are §4 site visits already covered by `site_visit` | **Hold** |
| `guards`, `commands_approach_to` | separate terms alongside `controls` | The sources do not distinguish them. Splitting one relation three ways, each scraping to three cases on distinctions the evidence does not make, is the proliferation §2 removes | **Withdraw; consolidate into `controls`** |

v0.2 §14.5 was wrong on three of its six event terms, in both directions. It is recorded here rather than quietly corrected.

---

## 1. Method

Every case below cites live record identifiers from `origin/main` at commit `82c2679`, verified 2026-07-23. No case is hypothetical and none was constructed for the filing.

**A case counts only when both endpoints exist as records.** This is stricter than governance §5.5 requires — it asks for "concrete cases the new term would describe" — but it is the right test for a relationship vocabulary, because a term whose targets do not exist cannot be used on approval. Where a relation is well attested in prose but one endpoint has no record (a fort guarding an unnamed pass; a monastery owning unnamed dependents), the case is reported and **not counted**. Several terms fail on exactly this ground, and the failure is informative: it says the vocabulary gap is downstream of an entity gap.

**External alignments are not asserted.** Governance §5.5(4) requires a SKOS definition and external alignment at the vocabulary-file update. SKOS definitions are supplied below. **AAT, Pleiades-type and CIDOC CRM property identifiers are deliberately left blank**, because they cannot be verified from this environment and hard rule 2 prohibits inserting identifiers that have not been confirmed to resolve. They are to be supplied at the vocabulary-file update, by a contributor who can verify them.

---

## 2. Terms filed for immediate decision

### 2.1 `RelationshipType` — visibility and landscape control

#### `overlooks`

**SKOS definition.** A spatial entity stands in a commanding visual relation to another, such that the second is visible from the first. Directional and asymmetric. Distinct from proximity: a site may overlook a feature it is not near, and be near one it cannot see.

**Rationale.** RQ1 asks how passes, crossings and routes were monitored, and names viewshed analysis as the operation that answers it. Viewshed requires a directional visibility relation. The corpus currently records these as `near`, which is symmetric, non-directional, and analytically inert.

**Concrete cases (3):**

| # | Relation | Records | Evidence | Currently |
|---|---|---|---|---|
| 1 | Jawzāt overlooks Tarsus | ENT-PLC-0187 → ENT-PLC-0004 | "in a mountain pass overlooking the city some eight farsakhs (c. 65 km) away" | unrecorded |
| 2 | Dibsi Faraj overlooks the Euphrates | ENT-PLC-0036 → ENT-PLC-0044 | "on a plateau overlooking the river" | **REL-0022, `near`** |
| 3 | Monastery of St Simeon the Younger overlooks the Orontes | ENT-PLC-0165 → ENT-PLC-0156 | "on the Wondrous Mountain overlooking the Orontes Delta" | **REL-0125, `near`** |

**Supporting argument — the existing vocabulary is being overloaded.** `near` is the third most-used relationship type (21 records). At least six of those 21 are settlement-above-river relations of the Dibsi Faraj kind, where the source language is directional and the recorded relation is not. `near` is absorbing a relation it cannot express, and the loss is analytical: no viewshed query can be built on a symmetric predicate.

---

#### `controls`

**SKOS definition.** A site stands in a relation of military or administrative control over a landscape feature, route, crossing or approach — guarding, commanding, monitoring or taxing movement through it. Directional and asymmetric. **Consolidates the `guards` and `commands_approach_to` candidates**, which are withdrawn (§3.1).

**Rationale.** RQ1's second subordinate question asks how passes and river crossings "were controlled, monitored and exploited, and by what installations". This is the relation that question is about, and the corpus has no term for it.

**Concrete cases (3 with both endpoints as records):**

| # | Relation | Records | Evidence | Currently |
|---|---|---|---|---|
| 1 | Baghras controls the Belen Pass | ENT-PLC-0027 → ENT-PLC-0033 | Stated reciprocally in both records: "guarding the Belen Pass (Syrian Gates)"; "guarded by Baghras" | **REL-0018, `defended`** |
| 2 | al-Hārūnīyya controls the Bahçe Pass | ENT-PLC-0122 → ENT-PLC-0139 | Stated reciprocally: "guards the Bahçe Pass approach"; "guarded on its approach by al-Hārūnīyya" | unrecorded |
| 3 | Ḥiṣn Qalawdiya controls the eastern approach to Malaṭiya | ENT-PLC-0186 → ENT-PLC-0016 | "guarding the eastern approach to Malaṭiya" | unrecorded |

**Six further cases, reported but not counted**, because the controlled entity has no record: Darbassak → Çalan Pass (no record); Ṭaranda → Mazikiran Pass (no record); Būqā → the Anṭākiya–Marʿash route (no record); ʿAyn Zarba → the Jayhān–Taurus route (no record); Hadath → an unnamed Taurus pass; al-Massīsa → route (no record). **These six are evidence that the vocabulary gap sits downstream of a route and pass entity gap**, and that `controls` will be heavily used once Phase 3 mints the missing features. They are not offered as qualifying cases.

**Supporting argument — `defended` is being overloaded.** REL-0018 records Baghras → Belen Pass as `defended`. In the enum, `defended` sits in the punctual military-action cluster (`besieged`, `occupied`, `captured`, `destroyed`) and denotes an act in an event. Here it is carrying a standing landscape relation that held for centuries. The overload conflates an act with a condition, and it is the reason a `controls` term is needed rather than a broader reading of `defended`.

---

### 2.2 `RelationshipType` — route and crossing structure

#### `crosses_at`

**SKOS definition.** A route or way crosses a watercourse or barrier at a named point. Links the crossing locus to the feature crossed.

**Rationale.** RQ1 asks how river crossings were controlled and exploited. Crossings are among the most densely attested features in the corpus and have no term of their own.

**Concrete cases (3+):**

| # | Relation | Records | Currently |
|---|---|---|---|
| 1 | Pınar Tarlası crossing of the Euphrates | ENT-PLC-0059 → ENT-PLC-0044 | **REL-0034, `lies_on_route`** |
| 2 | Jarablus Tahtani way station crossing of the Euphrates | ENT-PLC-0060 → ENT-PLC-0044 | **REL-0035, `lies_on_route`** |
| 3 | Jisr Manbij crossing of the Euphrates | ENT-PLC-0064 → ENT-PLC-0044 | unrecorded |
| 4 | Zeugma crossing of the Euphrates | ENT-PLC-0042 → ENT-PLC-0044 | unrecorded |

**One reframing the Board should rule on explicitly.** v0.2 §6.2 conceived `crosses_at` as a **route→feature** relation. In that form it has **zero** qualifying cases, because the corpus holds one route record. The cases above are **site→feature**: a crossing locus and the river it crosses. The relation is real and well attested; the domain is not the one proposed. The Board is asked either to approve the site→feature reading, or to hold the term until routes exist. **Recommendation: approve the site→feature reading**, since it is what the evidence supports and the route→feature use is a straightforward later extension of the same term.

**Supporting argument — `lies_on_route` is being overloaded.** Two of its three uses are crossings, not route membership; a way station on a river bank is not "on a route" in the sense the term was minted for.

---

### 2.3 `RelationshipType` — interpretation to interpretation

Both terms below are required by **rule 10** (recovered 2026-07-23), which requires related and competing interpretations to be explicitly cross-referenced. Rule-10 compliance is currently **100% textual and 0% structural**: 29 interpretations cross-reference in prose; zero relationships have an interpretation endpoint. These terms are what convert an existing obligation from prose into data.

#### `corroborates`

**SKOS definition.** One interpretation supports, underpins or supplies evidential or theoretical backing for another, without being the same argument. Directional. Distinct from `contradicts`, which already exists in the enum.

**Concrete cases (4):**

| # | Relation | Records | Prose in the record |
|---|---|---|---|
| 1 | Smith's theoretical position corroborates Eger's continuity argument | INT-0161 → INT-0153 | "Eger deploys Smith's general theoretical claim to support the anti-core-periphery / archaeological-continuity argument of INT-0153" |
| 2 | Zadeh corroborates Eger's frontier-imagination strand | INT-0162 → INT-0156 | "Supports the 'fantastical geographies' strand of INT-0156" |
| 3 | Durak corroborates the porous-frontier argument | INT-0163 → INT-0159 | "Underpins the 'objects travelled' component of INT-0159" |
| 4 | Straughn complements Eger's ḥimā argument | INT-0133 → INT-0127 | "Complements Eger's own ḥimā argument (INT-0127)" |

---

#### `parallel_case`

**SKOS definition.** Two interpretations address structurally identical situations at different entities, such that the reasoning in one bears on the other without either supporting or contradicting it. Symmetric.

**This term is not in ontology v0.2 §6.2. It was surfaced by the scan**, and is filed because the corpus already uses it in prose three times and has no way to record it. It is reported as an addition rather than folded silently into the filing.

**Concrete cases (3):**

| # | Relation | Records | Prose in the record |
|---|---|---|---|
| 1 | Bālis ↔ Malaṭya coordinate divergence | INT-0169 ↔ INT-0170 | "Parallel case: Malaṭya, INT-0170" / "Parallel case: Bālis, INT-0169" |
| 2 | Zibaṭra ↔ Bālis | INT-0172 → INT-0169 | "Parallel cases: Bālis INT-0169, Malaṭya INT-0170" |
| 3 | Zibaṭra ↔ Malaṭya | INT-0172 → INT-0170 | *ibid.* |

All three are coordinate-divergence interpretations of the same methodological shape. This is the relation that makes the designated-assertion pattern (ontology §5.6) queryable as a class rather than as three unconnected records.

---

### 2.4 `RelationshipType` — examination

#### `examined`

**SKOS definition.** An investigation event took a spatial entity or its material as its subject. Carries the examination's coverage through the event's `detection_scope`.

**Rationale.** This is the relation on which the narrowing of the negative-evidence limitation depends (ontology §10.14, §14.3). Without it, "sites never examined" cannot be distinguished from "sites examined and found empty".

**Concrete cases: 19 dated site visits alone**, each already carrying `provenance: primary_observation` and an `observation_date`. A sample:

| Attestation | Date | Site |
|---|---|---|
| ATT-0357 | 2004-09-25 | Dulūk (ENT-PLC-0062) |
| ATT-0440 | 2005-07-20 | al-Muthaqqab / Mutallip Höyük (ENT-PLC-0124) |
| ATT-0507 | 2005-08-19 | Zibaṭra (ENT-PLC-0007) |
| ATT-0497 | 2005-07 | Tarsus (ENT-PLC-0004) |
| ATT-0466 | 2004-07-20 | Sīs (ENT-PLC-0127) |

Plus nine excavation attestations and more than ten survey attestations (§2.5). **Well above threshold.**

**Dependency.** The Event-side endpoint requires the `investigation` event vocabulary (§2.5) to be approved in the same decision. The relationship term is unusable without it; the two should be voted together.

---

### 2.5 `EventCategory` and `EventSubCategory` — investigation

#### `investigation` *(new EventCategory)*

**SKOS definition.** An act of archaeological, topographic or documentary investigation of a place or its material: excavation, survey, site visit, instrumental prospection. Distinguished from the ten existing categories, none of which accommodates the investigation of the frontier as opposed to events within it.

**Rationale.** Modelling investigation as an event makes the corpus's own evidential formation analysable, which RQ4 requires, and supplies the endpoint the `examined` relation needs. Ontology §14 gives the argument and the L1 check.

**Note on scope.** Investigation events fall outside the corpus's 640–1100 range. This is not a violation — principle 14 holds that temporal boundaries are properties of analyses, not of the data model, and the corpus already carries 2005 dates in `observation_date` — but no query or export may assume all events fall within the corpus range.

---

#### `site_visit` *(sub-category)*

**SKOS definition.** A dated first-hand visit to a site by a named observer, producing direct observations of its visible state.

**Concrete cases: 19**, listed at §2.4. Every one is dated, attributed and already recorded as `primary_observation` under rule 11.

---

#### `survey` *(sub-category)*

**SKOS definition.** A systematic, usually multi-site programme of surface investigation, published under a project name.

**Concrete cases (10+ named survey programmes attested):** the Amuq Valley Survey and Kahramanmaraş Survey (ATT-0247); the Bolkardağ survey, 1983–85 (ATT-0062); the Tabqa Dam Euphrates Survey (ATT-0095); the 1939 Jabbūl Survey and the new Jabbūl Survey (ATT-0115, ATT-0143); the Rifaʿat Survey (ATT-0134); the 2004 Mopsus Survey (ATT-0510); the 1991 Özgen & Gates survey (ATT-0509); Sinclair and Carter's survey (ATT-0424); the Salmeri & d'Agata Cilicia Survey Project (ATT-0431).

---

#### `excavation` *(sub-category)* — **corrected from v0.2, which deferred this term**

**SKOS definition.** A programme of stratigraphic excavation at a site, published or reported.

**Concrete cases (9):**

| Attestation | Site | Programme |
|---|---|---|
| ATT-0496 | Tarsus (ENT-PLC-0004) | three excavation programmes bearing on the Early Islamic city |
| ATT-0096 | Dibsi Faraj (ENT-PLC-0036) | Harper & Wilkinson, *Excavations at Dibsi Faraj*, DOP 29 (1975) |
| ATT-0477 | Sumaysāṭ (ENT-PLC-0073) | ʿAbbāsid lustrewares from the excavations |
| ATT-0145 | Tilbeşar (ENT-PLC-0055) | French excavations from 1994 |
| ATT-0139 | Ruṣāfat Hishām (ENT-PLC-0067) | recent excavations |
| ATT-0372 | Ḥiṣn al-Tīnāt / Tüpraş Field (ENT-PLC-0123) | securely identified, excavated site |
| ATT-0207 | Domuztepe (ENT-PLC-0138) | one of the few excavated rural sites in the plain |
| ATT-0062 | Bolkardağ (ENT-PLC-0017) | underlying excavation reports |
| ATT-0345 | ʿAyn Zarba (ENT-PLC-0120) | published-archaeology pattern, named excavator |

v0.2 §14.5 stated that excavation cases would have to be "drawn from Phase 3". That was an assumption about a gazetteer-derived corpus, and it was wrong: Eger's §3 published-archaeology sections carry excavation reports throughout.

---

#### `remote_sensing_survey` *(sub-category)* — **corrected from v0.2, which deferred this term**

**SKOS definition.** Investigation of a site or landscape by satellite, aerial or other remotely sensed imagery, without ground contact.

**Concrete cases (3):**

| Attestation | Method | Subject |
|---|---|---|
| ATT-0134 | CORONA imagery | Rifaʿat Survey area |
| ATT-0115 | CORONA image showing a possible canal and Early Islamic anomalies | Jabbūl Survey shrine and cemetery |
| ATT-0229 | canal and qanat system traced via remote sensing | Nahr al-Nīl, Raqqa |

**A false-positive worth recording.** A naive keyword scan returned six hits, two of which were **"Lidar Höyük"** — a Turkish place name on the Euphrates, not lidar the technique. Counting them would have inflated this term to six cases and pushed `geophysical_survey` over threshold on the same error. The hits were read rather than counted, which is the whole point of the exercise and the reason this filing rests on read evidence rather than grep output.

---

## 3. Terms withdrawn before filing

| Term | Reason |
|---|---|
| **`guards`** | Consolidated into `controls`. The sources use "guarding", "controlling" and "commanding" interchangeably for the same standing relation; three terms would each scrape to three cases on distinctions the evidence does not make. |
| **`commands_approach_to`** | Consolidated into `controls`. Its only qualifying case (Ḥiṣn Qalawdiya → Malaṭiya) is counted under `controls`. |
| **`examined_without_result`** | Redundant. A negative finding is expressed by an `examined` relation plus an Assertion with `polarity: denied` plus the event's `detection_scope` — machinery already proposed. A dedicated relationship term would encode in the vocabulary what belongs in the evidence layer, and would make negative findings unqueryable alongside positive ones. |
| **`subordinate_installation_of`** | **`subordinate_to` already exists in the enum and has zero uses.** Proposing a near-synonym for an unused existing term is proliferation. If the existing term proves too coarse once used, a refinement can be proposed then, with cases. |

**A general finding behind the last row: 18 of the 44 existing `RelationshipType` terms have never been used**, including `subordinate_to`, `contradicts`, `alternative_identification_of`, `supersedes_attestation`, `depends_on` and `same_as`. Several needs identified in ontology §6.2 are covered by terms that already exist and are simply not being reached for. **The Board may wish to treat "is there an unused existing term for this?" as a standing first question on any future extension proposal.**

---

## 4. Terms held — insufficient concrete cases

Per Curtis's instruction, these are reported as insufficient rather than furnished with invented cases. Each states what would resolve it.

| Term | Cases found | Why held | Resolves when |
|---|---|---|---|
| `intervisible_with` | **0** | Zero hits corpus-wide for intervisibility, beacon, signal or line-of-sight language. | **Not a Phase-3 extraction matter.** Intervisibility is *computed* by viewshed analysis, not attested in texts. Its cases will be generated by the RQ1 analysis the ontology enables, and the term should be proposed then, from results. |
| `member_of_route_family` | **0** | One route record exists in the corpus. | Phase 3 mints route entities. |
| `traverses` | **1** | ENT-PLC-0011 traverses the Cilician Gates (ENT-PLC-0005). Same cause. | Phase 3 mints route entities. |
| `dependent_settlement_of` | **0 usable** | Three prose cases exist — al-Jurjuma "with dependent settlements", al-Jūma "villages assigned to its district", Qartmīn owning subordinate monasteries — but **in every case the dependents are unnamed and have no records**. The gap is an entity gap, not a vocabulary gap. | Dependents are minted as entities. |
| `revises` | **1** | Eger's 2005→2012 ceramic reversal, and it is not yet two records — it sits inside INT-0174's prose. Other "revision" hits are one scholar revising *another's* position, which is `contradicts`. | The interpretation pass (migration step 6) unbundles INT-0174 and its relatives, **creating the cases**. Propose immediately after. |
| `builds_on` | **2** | INT-0092 → INT-0094 (adapting a comparative al-Andalus model); INT-0166 → INT-0063. Not in §6.2; surfaced by the scan. | A third case accumulates. |
| `succeeds` | **<3** | Ḥiṣn ʿAwlās "replaced the destroyed Qalamya" — **Qalamya has no record**. Baghras's upland castle and lowland settlement are currently one record. Dābiq's "Middle Islamic successor" is unnamed. Note that `rebuilt` already exists and is used 9 times for same-site continuity; `succeeds` is for genuinely distinct successive sites, which the corpus does not yet separate. | The place pass (migration step 3) splits conflated sites. |
| `restores` | **0** | No TerritorialUnit records exist in the current model; the interruption case (ontology §4.5) has no instances yet. | TerritorialUnits exist and a dissolution-and-recreation case arises. |
| `material_reexamination` | **2** | Eger's 2005 examination of the Mopsus baskets (ATT-0440) and his 2012 Bilkent re-examination (ATT-0511). **v0.2 claimed three; the third was double-counting a site visit.** | A third case arises. Note that the two extant cases are the crux of the Al-Muthaqqab dossier, so this term will matter — but two is two. |
| `geophysical_survey` | **1** | ATT-0251, geophysically detected structures linking enclosure to coast. | Phase 3, or a further case. |

---

## 5. Terms filed conditionally — cases identified, endpoint type unimplemented

These three are held back for a **different reason** from §4, and the distinction matters for the Board's decision: the evidence is sufficient, but one endpoint type does not yet exist.

| Term | SKOS definition | Cases identified |
|---|---|---|
| `produced_phase` | An event brought into being a new dated state of a spatial entity. | Sack of Amorium (ENT-EVT-0006) → Amorium's post-838 state (ENT-PLC-0001); Sacking of Qenneshre 811 (ENT-EVT-0019) → Qenneshre (ENT-PLC-0054); the ʿAyn Zarba refortification under Hārūn al-Rashīd (796/804) → ʿAyn Zarba (ENT-PLC-0120) |
| `terminated_phase` | An event brought a dated state to an end. | The same three, read from the other side |
| `damaged` | An event caused physical harm to a spatial entity or component without terminating its occupation. | The three sack events (ENT-EVT-0001, 0005, 0006, 0019) |

**The Phase type does not exist.** These terms are unusable until migration step 9. The Board is asked to **approve them conditionally**, effective on Phase implementation, so that the approval clock runs now — which is the purpose of filing early. If the Board prefers to defer, the cost is a delay at step 9 rather than a modelling problem.

---

## 6. One modelling question this filing surfaced, requiring a decision before `member_of_defensive_system` can be proposed

Ontology §6.2 listed `member_of_defensive_system` among the required terms. The corpus supplies a strong case — **INT-0060** argues that Kanīsa al-Sawdāʾ (ENT-PLC-0121), ʿAyn Zarba (ENT-PLC-0120) and al-Hārūnīyya (ENT-PLC-0122) "form an equidistant triangle of strategically sited eastern-plain towns developed together". A second, the "Cilician city triad" with Adhana (ENT-PLC-0119) as central node, is recorded in the same terms.

**But the term as worded presupposes an entity that does not exist and that the ontology deliberately did not create.** "Member of a defensive system" requires the system to be a record. Ontology §4.11 rejected no such type — it was never considered, which is itself the finding. Three constructions are available:

1. **The system is an entity** — a new domain type, which must pass the admission test and has not been put to it.
2. **The system is an Interpretation** — which is what the corpus already does: INT-0060 *is* the argument that these three form a system. Membership would then be a relation from site to interpretation, and the system has exactly the epistemic status it should, since "these forts formed a coordinated system" is a scholarly reading, not an observed fact.
3. **The system is an AnalyticalRegion** — a researcher-defined grouping, which is wrong here: the argument is that the Abbasids built them as a system, which is a claim about the past, not a selection by a modern researcher.

**Recommendation: construction (2)**, and the term should be `member_of_system_argued_by` or the relation simply expressed site→Interpretation. But this is a modelling decision, not a vocabulary decision, and it belongs in the ontology rather than in a §5.5 proposal. **`member_of_defensive_system` is therefore withheld pending that decision**, with the two cases recorded here so they are not lost.

This is the second time a scoping pass has surfaced a more consequential question than the task it was scoping — the first being Item F surfacing Item G.

---

## 7. Summary

| Status | Count | Terms |
|---|---|---|
| **Filed for immediate decision** | **11** | `overlooks`, `controls`, `crosses_at`, `corroborates`, `parallel_case`, `examined`; `investigation` (category), `site_visit`, `survey`, `excavation`, `remote_sensing_survey` |
| **Filed conditionally** (on Phase) | **3** | `produced_phase`, `terminated_phase`, `damaged` |
| **Withdrawn before filing** | **4** | `guards`, `commands_approach_to`, `examined_without_result`, `subordinate_installation_of` |
| **Held — insufficient cases** | **10** | `intervisible_with`, `member_of_route_family`, `traverses`, `dependent_settlement_of`, `revises`, `builds_on`, `succeeds`, `restores`, `material_reexamination`, `geophysical_survey` |
| **Withheld pending a modelling decision** | **1** | `member_of_defensive_system` |

Of the eleven filed, **two are not in ontology §6.2**: `parallel_case`, surfaced by the scan, and `excavation`, which v0.2 wrongly deferred.

---

## 8. What the Board is asked to decide

1. **Approve the eleven terms at §2**, each with three or more verified concrete cases. `examined` and the `investigation` vocabulary should be voted together, since the first is unusable without the second.
2. **Rule on the `crosses_at` reframing** (§2.2): approve the site→feature reading the evidence supports, or hold the term until route entities exist.
3. **Approve or defer the three conditional terms at §5**, noting that conditional approval costs nothing and deferral delays migration step 9.
4. **Note the four withdrawals at §3**, and consider adopting "is there an unused existing term for this?" as a standing first question on extension proposals — 18 of 44 existing terms have never been used.
5. **Take the modelling question at §6** back into the ontology rather than deciding it here.

On approval, governance §5.5(4)–(5) require the vocabulary file to be updated with each term, its SKOS definition and its external alignment, and the vocabulary's MINOR version incremented. **External alignments are not supplied in this filing** and must be added by a contributor able to verify that each identifier resolves, per hard rule 2.

---

# Addendum — dated updates to this filing

*Recorded here rather than by amending conceptual ontology v0.2, so that the governance document stays stable while the audit trail remains complete. Each entry is dated and states what changed and on what evidence.*

---

## Update 1 — 2026-07-23. Status of the ontology §19.3 vocabulary deferrals

Conceptual ontology v0.2 §19.3 deferred **three** event sub-category terms — `excavation`, `remote_sensing_survey` and `geophysical_survey` — with the resolving condition *"Phase 3 supplies three concrete cases each, per governance §5.5."*

Two of the three were satisfied by evidence **already in the corpus** and did not require Phase 3:

| §19.3 deferral | Status | Evidence |
|---|---|---|
| `excavation` | **SATISFIED — deferral discharged.** Filed at §2.5. | 9 cases: ATT-0496 (Tarsus), ATT-0096 (Dibsi Faraj), ATT-0477 (Sumaysāṭ), ATT-0145 (Tilbeşar), ATT-0139 (Ruṣāfat Hishām), ATT-0372 (Ḥiṣn al-Tīnāt), ATT-0207 (Domuztepe), ATT-0062 (Bolkardağ), ATT-0345 (ʿAyn Zarba) |
| `remote_sensing_survey` | **SATISFIED — deferral discharged.** Filed at §2.5. | 3 cases: ATT-0134, ATT-0115 (CORONA), ATT-0229 (remote sensing) |
| `geophysical_survey` | **STILL DEFERRED.** | 1 case (ATT-0251). Resolving condition unchanged. |

**Cause of the error.** v0.2 assumed a gazetteer-derived corpus would not carry excavation or instrumental-survey reporting. It does: Eger's §3 published-archaeology sections relay both throughout. The deferral was made on an assumption about the corpus rather than a measurement of it.

**One correction to the framing of this update.** `material_reexamination` was **not** a §19.3 deferral. v0.2 §14.5 *proposed it for immediate filing*, and the scan moved it in the opposite direction: only 2 verified cases (ATT-0440, ATT-0511), the apparent third being a double-count of a site visit. It is **held at §4 of this filing**, not discharged. Recording it alongside the two discharged deferrals would misstate which way each term moved, so the two movements are kept distinct:

- **Discharged (deferred → filed):** `excavation`, `remote_sensing_survey`
- **Demoted (filed → held):** `material_reexamination`
- **Unchanged (still deferred):** `geophysical_survey`

---

## Update 2 — 2026-07-23. `member_of_defensive_system` resolved as a vocabulary decision

§6 of this filing withheld `member_of_defensive_system` pending what it characterised as an ontology-level question about whether defensive systems are entities. **That characterisation was wrong, and the alternative hypothesis is correct.** The question was tested against INT-0060 and resolves as a vocabulary decision. No new entity type; no reopening of the ontology.

### The test

**Question: is the "defensive system" an independently attested domain entity, or a scholarly interpretation relating a group of sites?**

INT-0060 rests on three attestations. Reading them:

| Attestation | Provenance | What it attests |
|---|---|---|
| ATT-0200 | `archaeological_evidence` | ʿAyn Zarba's ceramic sequence and occupation phases; fortification by Hārūn al-Rashīd (796 or 804) |
| ATT-0201 | `archaeological_evidence` | Kanīsa al-Sawdāʾ's occupation sequence, salvage excavation, Early Islamic phase; fortification by Hārūn al-Rashīd (799 or 806) |
| ATT-0202 | `modern_synthesis` | Hārūnīyya as an Abbasid foundation attributed to Hārūn al-Rashīd; its two candidate locations |

**Each attests an individual site. None attests a system.** No attestation contains "triangle", "system", "together", or any claim of joint development. What the sources supply is three separate fortification or foundation acts sharing one patron. The systemic reading — *equidistant*, *developed together*, *to settle the eastern plain and improve trade and security* — is Eger's inference from siting plus common patronage.

The record says as much in its own metadata: `scholar: Eger, A. A.`; `publication_source_id: SRC-0007`; `confidence: 3`. It is filed as an interpretation because it is one.

**Conclusion: the "defensive system" is a scholarly interpretation relating a group of sites. It is not an independently attested domain entity.**

### The modelling already exists — in two senses

1. **The membership is already recorded.** INT-0060 carries `associated_entities: [ENT-PLC-0121, ENT-PLC-0120, ENT-PLC-0122]`. The relation is in the corpus today, as an untyped field rather than a typed relationship.
2. **The schema already permits the endpoint.** `RelationshipRecord.source_entity` and `.target_entity` both `$ref` the shared `Identifier` definition, whose pattern is `^(ENT-(PLC|PERS|EVT|POL|GRP|INS|RTE|OBJ)|SRC|OBS|ATT|INT|REL)-[0-9]{4,8}$`. **`INT-` is already an admissible relationship endpoint.** A Site → Interpretation relationship is schema-valid today, with no schema change. Rule 10's interpretation-endpoint requirement is not merely provided for in principle; it is available in the schema and has simply never been used (0 of 144 relationships have an `INT-` endpoint).

### What the term adds, and why it must be renamed

`associated_entities` is untyped and therefore cannot distinguish *"these three form the group this interpretation argues for"* from *"this interpretation is about these three sites severally."* **79 interpretations associate two or more places; only about 16 make a grouping claim.** A typed link separates the two and makes argued groupings queryable. That is the analytical gain, and it is real.

But `member_of_defensive_system` names one *kind* of grouping, and the corpus's grouping arguments are not all defensive — they include road systems, hydraulic villages and irrigation-scale models. Minting `member_of_defensive_system`, then `member_of_road_system`, then `member_of_irrigation_system` is the proliferation §2 of the ontology removes. **One term; the character of the grouping stays in the interpretation's argument, where it already lives.**

### Filed: `member_of_argued_group`

**SKOS definition.** A spatial entity is a member of a group that a named interpretation argues to be a coherent unit — a defensive system, a road network, an irrigation scheme, a settlement pattern. Directed Site → Interpretation. The nature and purpose of the grouping are carried by the interpretation's argument; this relation records membership only, and does not assert that the grouping is attested rather than inferred.

**Concrete cases (3):**

| # | Interpretation | Grouping argued | Members |
|---|---|---|---|
| 1 | **INT-0060** (Eger 2015 ch. 5, conf. 3) | "equidistant triangle of strategically sited eastern-plain towns developed together" | ENT-PLC-0121 Kanīsa al-Sawdāʾ, ENT-PLC-0120 ʿAyn Zarba, ENT-PLC-0122 al-Hārūnīyya |
| 2 | **INT-0062** (Eger 2015 ch. 5, conf. 3) | "The four Amanus forts built by Hishām… formed a **deliberate small system** guarding major and minor passes" | ENT-PLC-0135 Ḥiṣn Qatraghash, ENT-PLC-0136 Ḥiṣn Mura, ENT-PLC-0027 Baghras, ENT-PLC-0029 Būqā |
| 3 | **INT-0043** (Eger 2015 ch. 3, conf. 2) | "A **system of way stations** roughly a day's travel apart structured the Raqqa–Sarūj–Sumaysāṭ road" | ENT-PLC-0086 Karababa Basin, ENT-PLC-0074 Ḥiṣn Manṣūr, ENT-PLC-0073 Sumaysāṭ, ENT-PLC-0091 Raqqa, ENT-PLC-0082 Sarūj |

All three are Eger's arguments at confidence 2–3, each inferring a system from siting plus a common patron or a common road. **INT-0062 is the paradigm case**, since Eger's own words are "formed a deliberate small system" — the systemic claim is explicitly his, which is exactly the point.

**Board decision requested:** approve `member_of_argued_group` (Site → Interpretation) and **withdraw `member_of_defensive_system`**. This raises the filing from eleven terms to **twelve filed for immediate decision**, and closes §6 without an ontology change.

**Note for the ontology, not requiring an amendment.** Ontology §4.11's rejected-types table has no row for a "defensive system" or "site group" type, because the candidate was never put to the admission test. It fails it: a group argued by a scholar has no identity criterion independent of the argument that proposes it, which is the definition of an epistemic object rather than a domain one. This can be added to §4.11 at the next revision; it changes no decision.
