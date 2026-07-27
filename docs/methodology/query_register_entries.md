# Query Register — Phase 2: Nineteen Entries

**Status:** proposal. Read-only pass; no logical model, no schema, no records.
**Format:** as approved 2026-07-23, with the §3.3.1 amendment below.
**Written against:** `docs/methodology/conceptual_ontology.md` and `docs/research_questions.md`, both frozen 2026-07-23.
**Corpus state:** `origin/main` at `44988e2`, 1,453 records, measured 2026-07-23.
**Prediction date for every entry below:** 2026-07-23.

---

## 0. Amendment to §3.3 — the review rule

### 3.3.1 Drafting error versus capability finding

An entry naming an element that does not exist in the frozen specification or in a filed §5.5 proposal is **not automatically malformed**. Two things could be true:

- **Drafting error.** The element exists under another name, at another level, or the requirement is met by a combination of existing elements the author failed to assemble. The entry is malformed; it is redrafted against the element that does exist.
- **Capability finding.** No ontology element, and no combination of them, expresses what the subordinate question requires. The entry is **not** malformed. It is a **classification (iv) finding**, recorded as such on the entry at authoring time.

**Burden, identical in structure to §7.2 Rule 3: the cheap answer must be positively established; the expensive one is the residual.** A finding of drafting error requires **naming the element or combination that does express the requirement**. Absent that naming, the entry stands as a capability finding and is carried forward as one.

*Rationale.* Authoring time is the cheapest moment at which an ontology defect can be found — before a logical model has been built against the specification and before any migration has been executed on its assumptions. An unqualified "malformed, redraft" rule would absorb exactly those findings into a redraft, converting the cheapest discovery into the most expensive one, and would leave the register able to detect ontology defects only after the model exists. That is the situation writing the register first was intended to avoid.

A capability finding recorded at authoring time is carried to the Board under governance §5.8. Where the Board declines to amend, it becomes an **accepted limitation with its reasoning**, per §5.8's third sentence. It does not silently become a redraft.

**Findings under this rule in phase 2: one.** QR-305 (interaction mechanisms) was recorded as a capability finding at §4.3 rather than redrafted. **It has since been resolved**: the Board accepted it as a demonstrated defect and adopted conceptual ontology **Amendment 1** (2026-07-23), adding an `interaction_mechanism` attribute to Event and Assertion. The entry below retains the finding as its historical record and states the resolved position.

---

## 1. Corpus measurements underlying these predictions

Every dependency prediction below rests on these, measured 2026-07-23. **One correction to a figure used in earlier passes**: an initial scan reported all 54 events as having no category and no date, because it read schema field names rather than record field names. The records use `event_type: {primary, sub}` and `start_date`/`end_date`. The corrected figures are below, and the error is recorded because it is exactly the class of thing §7.3's accuracy tally exists to catch.

| Measurement | Value |
|---|---|
| Events | 54 — military 18, construction_infrastructure 15, administrative 6, demographic 5, political 4, diplomatic 3, **environmental 2**, religious 1 |
| Events with `start_date` / `end_date` | 52 / 8 |
| Events linked to places | 53 of 54 |
| Events with parent or child | 7 |
| Places | 190 — with coordinates 57 (30%), alternative names 152, `chronology` 1, `political_affiliation_history` 5, `administrative_status_history` 1 |
| `identification_status` | identified 131, probably 32, approximately 10, disputed 7, unidentified 7, hypothetically 3 — populated on all 190 |
| Attestations | 477 — provenance: primary_paraphrase 225, modern_synthesis 95, archaeological_evidence 57, primary_quotation 33, gis_derived 22, primary_observation 19, primary_summary 11, modern_identification 9, numismatic 2, epigraphic 2, cross_source_synthesis 1, modern_interpretation 1 |
| Assertions (`ObservationRecord`) | 254 — 32 with >1 supporting attestation |
| Interpretations | 174 — 58 entities carry 2 or more |
| Relationships | 144 — **all 144 carry confidence; only 2 carry a temporal scope** |
| Sources | 79 |

Two of these drive many predictions below. **Only 2 of 144 relationships carry a temporal scope**, so any query needing relationships to hold during a phase is evidence-limited even after the vocabulary and migration clear. And **`alternative_datings` is used by zero places and zero events**, so competing-chronology queries have no data yet even though the structure exists.

---

## 2. The calibration set — category-1 entries

Flagged as a separate list, for execution by hand against the present corpus before any logical model exists.

| Entry | Title | Serves |
|---|---|---|
| **QR-402** | Provenance chain preservation | RQ4-2 |
| **QR-441** | Certainty-dimension separability audit *(derived)* | RQ4-4 |
| **QR-544** | Gazetteer generation from present data *(derived)* | RQ5-4 |

**Only one of the nineteen primary entries is category 1.** My phase-1 prediction was two or three. One is below that, and the shortfall is itself a calibration datum: it says the corpus's presently-executable surface is narrower than the frozen document's claim that "the existing corpus already embodies" the attestation-provenance model would suggest. The claim is not false — QR-402 runs — but it is thinner than it reads.

Because one entry is too small a calibration set to be diagnostic, I have added **two derived category-1 entries** (§6.4, §7.4). Both are honest register entries serving named subordinate questions; neither is a made-up exercise. They exist because you intend to execute the set now, and a set of one cannot tell you whether the register's authors understand the corpus.

---

## 3. RQ1 — Landscape and Mobility

### QR-101 · Environmental conditioning of available routes

**Question** (RQ1-1): *"How did topography, hydrology and environmental constraint condition the routes available for movement across the frontier?"*
**Status** Draft

**1 Result.** *Purpose:* to establish which landscape features constrained or afforded movement, and where routes were compelled to run. The evidential base for every least-cost model, and the query that says whether a modelled corridor is corroborated by terrain the sources themselves treat as decisive. *Answer shape:* one row per landscape feature: identifier, name, feature type, origin, designated geometry, the routes recorded as traversing or crossing it, and the attestations characterising it as a constraint or affordance. *Null means:* no feature has been recorded for that stretch of terrain — not that terrain there was unconstraining.

**2 Inventory.**

| | |
|---|---|
| Entities | `LandscapeFeature` (all feature types); `Route` |
| Relationships | `traverses` (Route → LandscapeFeature); `crosses_at` (Route\|Site → LandscapeFeature) |
| Assertions / pointers | Designated spatial assertion of `LandscapeFeature` and of `Route` — **designated only** |
| Certainty read | Spatial certainty; identification certainty on features |
| Non-graph ops | Spatial containment and adjacency; no path computation |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `traverses` term | 2 | **Held** — 1 case. Clears when 2 further cases arise |
| `crosses_at` term | 2 | §5.5 Board decision; filed with 4 cases |
| `LandscapeFeature`, `Route` types | 3 | Migration step 3 (place pass); Route requires rebuilding, not migration |
| Designated spatial assertions | 3 | Migration step 3 (M5) |
| Route entities beyond the single existing record | 4 | Phase 3 extraction |

**4 Limitations.** *Model:* none identified. *Record:* one Route record exists, held as a point with a 200 km radius; 42 landscape features are projected from the place triage but none exists yet as a typed record. *Scholarship:* "constraint" and "affordance" are analytic categories the sources do not use; the query returns features and their attested characterisations, not a graded constraint surface.

**5 Acceptance.** *Pass:* one row per feature with its designated geometry and its route relations, resolved without a transformation step. *Partial:* features returned without route relations, attributable to the record limitation. *Fail:* feature geometry cannot be held as a polygon or linestring, so that a valley or range must be reduced to a point.

---

### QR-103 · Route families and persistent corridors

**Question** (RQ1-3): *"Can recurring corridors of movement — route families that persisted even as specific tracks shifted — be identified from the combined archaeological, historical and spatial evidence?"*
**Status** Draft

**1 Result.** *Purpose:* to test the ontology's central claim about Route identity — that a corridor persists while its tracks shift — by retrieving families with their member tracks and each track's period of use. *Answer shape:* one row per route family: identifier, name, termini, member tracks, and for each track its class (documented, modelled, inferred), designated geometry and phase intervals. *Null means:* no family has been recorded — which, given one Route record exists, will be the answer until Phase 3.

**2 Inventory.**

| | |
|---|---|
| Entities | `Route` with `class ∈ {family, documented, modelled, inferred}`; `Phase` |
| Relationships | `member_of_route_family` (Route → Route), traversed both directions |
| Assertions / pointers | Designated spatial assertion of each track — **designated only**; designated temporal assertion of each phase |
| Certainty read | Spatial; chronological; identification |
| Non-graph ops | Grouping; interval ordering |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `member_of_route_family` term | 2 | **Held** — 0 cases. Clears when Phase 3 mints routes and 3 family relations arise |
| `Route`, `Phase` types | 3 | Migration step 3; step 9 |
| Route entities | 4 | Phase 3 extraction — this is the binding constraint, not the vocabulary |

**4 Limitations.** *Model:* none identified. The identity criterion at conceptual ontology §4.4 — continuity of corridor, explicitly not geometry — is what makes the question askable, and it is specified. *Record:* one Route record. *Scholarship:* whether two tracks belong to one family is a scholarly judgement, and the query reports asserted membership rather than establishing it.

**5 Acceptance.** *Pass:* families returned with member tracks and per-track phases, and a family retrievable without any of its tracks' geometries. *Partial:* families without phase intervals. *Fail:* route identity cannot be maintained across a change of designated geometry — which would falsify the §4.4 identity criterion and is a candidate classification (iv).

---

### QR-104 · Attested routes against least-cost prediction

**Question** (RQ1-4): *"How did the routes attested in the geographical and historical sources relate to the routes that least-cost analysis of the terrain would predict?"*
**Status** Draft

**1 Result.** *Purpose:* the comparison RQ1 exists to make. *Answer shape:* one row per attested route: its designated geometry, the modelled least-cost path between the same termini, a divergence measure, and the landscape features each passes that the other does not. *Null means:* one of the two is absent — and the row must say which, since "no divergence" and "no model" are different findings.

**2 Inventory.**

| | |
|---|---|
| Entities | `Route` with `class: documented` and `class: modelled`; `LandscapeFeature` |
| Relationships | `traverses`; `member_of_route_family` where a documented and a modelled route are held as members of one family |
| Assertions / pointers | Designated spatial assertion of each route — **designated only**; provenance of the modelled route's spatial assertion must be `gis_derived_observation` |
| Certainty read | Spatial certainty on both |
| Non-graph ops | **Least-cost path computation**; geometric divergence measure; spatial intersection |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `traverses`, `member_of_route_family` | 2 | As QR-101, QR-103 |
| `Route` type; full geometry types | 3 | Migration step 3 |
| Attested route entities | 4 | Phase 3 |
| Terrain cost surface (DEM, hydrology, land cover) | 4 | External data acquisition — **not a corpus dependency**, and the only entry whose category-4 item lies outside the project's own extraction |

**4 Limitations.** *Model:* none identified. The one-Route-type decision at §4.4, holding documented and modelled routes in one type distinguished by a class attribute, is what makes this a single query rather than a join across two types. *Record:* one route. *Scholarship:* least-cost modelling encodes assumptions about what was being minimised — time, effort, exposure — which the sources do not state; the divergence measure is only as meaningful as the cost surface's assumptions, which must be recorded with the modelled route's assertion.

**5 Acceptance.** *Pass:* documented and modelled routes returned as instances of one type, comparable without a transformation step, each carrying its own provenance. *Partial:* comparison possible for termini pairs where both exist. *Fail:* the modelled route cannot carry `gis_derived_observation` provenance and a confidence distinct from the documented route's.

---

## 4. RQ2 — Settlement Systems

### QR-201 · Morphology and extent through time

**Question** (RQ2-1): *"How did the morphology and extent of frontier settlements change between the eighth and tenth centuries?"*
**Status** Draft

**1 Result.** *Purpose:* the phased-extent query; the data behind any statement that a settlement expanded or contracted. *Answer shape:* one row per (site, phase): phase interval, designated geometry, computed area, occupation regime, and the change in area from the preceding phase. Ordered by site, then phase start. *Null means:* the phase has no designated geometry — **distinct from zero extent**, and the two must be labelled differently or every contraction analysis built on this query will be wrong.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `Phase` |
| Relationships | None — phase membership is structural |
| Assertions / pointers | Designated spatial assertion of each `Phase` — **designated only**; designated temporal assertion of each `Phase` |
| Certainty read | Spatial; chronological. **Not** identification, **not** functional |
| Non-graph ops | Area computation; phase ordering; difference between consecutive phases |
| Analytical layer | None |

**3 Dependencies — categories 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `Site`, `Phase` types | 3 | Migration step 3; step 9 |
| Phase-attached designated spatial assertions | 3 | Migration step 9 |
| Polygon geometry (extent, not point) | 3 | Migration step 3 (M5) |
| Phased extent evidence | 4 | Phase 3 — 57 places carry a point; **none carries an extent polygon**, and no place carries more than one geometry |

**4 Limitations.** *Model:* none identified. *Record:* severe and quantified. One place record of 190 uses `chronology`; zero use `alternative_datings`; zero carry polygonal extent. This query has essentially no data today and will have little until excavated and surveyed sites are extracted. *Scholarship:* extent is rarely recoverable for textually-attested sites at all, so the query will always answer for the excavated minority.

**5 Acceptance.** *Pass:* one row per (site, phase) with area and inter-phase difference, resolving the phase's own designated geometry rather than the site's. *Partial:* phases returned without geometry. *Fail:* a phase cannot hold a geometry distinct from its site's — which would collapse principle 3's co-equality and is a candidate classification (iv).

---

### QR-202 · Functional change and its evidence

**Question** (RQ2-2): *"How did the function of sites change — between military, ecclesiastical, agricultural and administrative roles — and how are those functional shifts evidenced?"*
**Status** Draft

**1 Result.** *Purpose:* the monastery-to-fortress query; establishes that functional change is representable without disturbing site identity. *Answer shape:* one row per (site, phase): function, functional certainty, phase interval, and the attestations and interpretations supporting the functional attribution. Sites with two or more distinct functions across phases flagged. *Null means:* function unrecorded for that phase, not that the phase was functionless.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `Phase` with `function` from the controlled vocabulary; `Component` where the functional evidence is componential |
| Relationships | None required |
| Assertions / pointers | Designated temporal assertion of each `Phase`; functional assertions with their supporting attestations |
| Certainty read | **Functional certainty** — the dimension this entry exists to exercise; chronological |
| Non-graph ops | Sequence comparison across phases of one site |
| Analytical layer | None |

**3 Dependencies — categories 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `Site`, `Phase`, `Component` types | 3 | Migration steps 3 and 9 |
| Functional certainty has no field in the present schema | 3 | Migration step 9 — it is specified in the ontology at §8.1 but exists nowhere in the corpus |
| Function vocabulary | 3 | Schema v3 |
| Phased functional evidence | 4 | Phase 3 |

**4 Limitations.** *Model:* none identified — and this is the entry that tests §4.2's consequence 2 most directly, that identity is not functional. *Record:* the current schema has no functional certainty field at all, so no baseline exists. *Scholarship:* function is inferred from morphology and finds, and the inference is contested for exactly the structures the contract names in its "contested function" edge case; the query returns competing attributions rather than resolving them.

**5 Acceptance.** *Pass:* a site returns two phases of differing function with independent functional certainties, its identity unchanged and its identification certainty untouched. *Partial:* functions returned without certainties. *Fail:* recording a functional change alters the site's identity or requires a second site record.

---

### QR-203 · Settlement hierarchy

**Question** (RQ2-3): *"Can settlement hierarchies be reconstructed, distinguishing major fortified centres from subordinate installations and open settlements?"*
**Status** Draft

**1 Result.** *Purpose:* to reconstruct rank and dependency, and — because rank is phase-borne — to show rank changing through time. *Answer shape:* one row per (site, phase): rank or status, its evidence, superordinate sites, dependent settlements, and area where available. Grouped into hierarchy trees per region. *Null means:* rank unrecorded.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `Phase` with `rank`/`administrative_status` |
| Relationships | `subordinate_to` (existing enum term, **0 uses**); `dependent_settlement_of` |
| Assertions / pointers | Designated temporal assertion of each phase |
| Certainty read | Relationship certainty; chronological |
| Non-graph ops | Transitive closure over the hierarchy; grouping |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `dependent_settlement_of` term | 2 | **Held** — 0 usable cases: three prose cases exist but every dependent is unnamed and has no record |
| `Site`, `Phase` types; rank as phase-borne attribute | 3 | Migration steps 3 and 9 |
| Dependent settlements as entities | 4 | Phase 3 — the vocabulary gap is downstream of an entity gap |

**4 Limitations.** *Model:* none identified. Retiring `city`, `village` and `capital_city` as types and re-expressing them as phase-borne rank (§2.1) is what makes "a village became a city" representable, and this entry is its test. *Record:* `administrative_status_history` is used by 1 place of 190; `subordinate_to` by 0 relationships of 144. *Scholarship:* the Arabic and Byzantine administrative vocabularies do not map onto a single rank scale, and a reconstructed hierarchy is an argument, not a reading.

**5 Acceptance.** *Pass:* hierarchy trees returned per phase interval, with a site's rank differing between phases. *Partial:* a single undated hierarchy. *Fail:* rank can only be held on the site, so that a rank change requires a new site record.

---

### QR-204 · Spatial and functional relations between site classes

**Question** (RQ2-4): *"How did fortifications, settlements, monasteries, agricultural landscapes and communications infrastructure relate to one another spatially and functionally?"*
**Status** Draft

**1 Result.** *Purpose:* the query behind any claim about how the frontier's built and worked landscape hung together. *Answer shape:* one row per related pair: the two entities with their types and phase functions, the relation, its temporal scope, its certainty, and the distance between designated geometries where both exist. *Null means:* no relation recorded — and given that 21 of 144 relationships are `near`, an absent relation frequently means unexamined rather than unrelated.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `LandscapeFeature` (agricultural landscapes, canals, field systems); `Route`; `Component` |
| Relationships | `contains` (narrowed to spatial containment); `adjoins`; `near`; `crosses_at`; `controls`; `member_of_argued_group` |
| Assertions / pointers | Designated spatial assertions of both endpoints — **designated only** |
| Certainty read | Relationship certainty; spatial; functional (via phases) |
| Non-graph ops | Distance computation; grouping by type pair |
| Analytical layer | None |

**3 Dependencies — categories 2, 3.**

| Item | Cat | Clears at |
|---|---|---|
| `crosses_at`, `controls`, `member_of_argued_group` | 2 | §5.5 Board decision; all filed with ≥3 cases |
| `Site`, `LandscapeFeature`, `Route`, `Component` types | 3 | Migration step 3; Component at step 9 |
| `contains` narrowing | 3 | Migration step 7 — 27 records currently do three jobs under one term |
| Designated spatial assertions | 3 | Migration step 3 |

**4 Limitations.** *Model:* none identified. *Record:* only 2 of 144 relationships carry a temporal scope, so the "functionally related during which period" half of the question is unanswerable from present data even after migration. *Scholarship:* spatial proximity is not functional relation, and the query cannot supply the inference; `near` in particular carries no directional or functional content.

**5 Acceptance.** *Pass:* pairs returned across all four entity types with relation, temporal scope, certainty and distance, without type-specific special-casing. *Partial:* relations returned without temporal scope. *Fail:* a relationship cannot hold endpoints of two different spatial types — which would defeat the common spatial supertype at §4.1.

---

### QR-205 · Regional defensive systems

**Question** (RQ2-5): *"Can regional defensive systems — coordinated networks of fortification rather than isolated sites — be identified?"*
**Status** Draft

**1 Result.** *Purpose:* to retrieve argued site-groupings as structures rather than as prose, and to distinguish a system argued by a scholar from one attested by a source. *Answer shape:* one row per argued group: the interpretation, its scholar, publication, argumentative confidence, the member sites, and the attestations underlying each member. *Null means:* no group has been argued for those sites — which is a fact about the scholarship, not about the frontier.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `Interpretation` |
| Relationships | `member_of_argued_group` (Site → Interpretation), traversed both directions |
| Assertions / pointers | Designated spatial assertion of each member — **designated only** — for the map output |
| Certainty read | **Argumentative confidence** on the interpretation; spatial on members |
| Non-graph ops | Grouping; convex hull or centroid spread for the map |
| Analytical layer | None. **L2 check:** an argued group is an epistemic object, not an analytical region — it claims something about the past |

**3 Dependencies — categories 2, 3.**

| Item | Cat | Clears at |
|---|---|---|
| `member_of_argued_group` term | 2 | §5.5 Board decision; filed 2026-07-23 with 3 verified cases (INT-0060, INT-0062, INT-0043) |
| `Site` type | 3 | Migration step 3 |
| Designated spatial assertions | 3 | Migration step 3 |

**4 Limitations.** *Model:* none identified — and this entry is where the §6 modelling question of the vocabulary filing was resolved. Testing INT-0060 against its three attestations showed that none attests a system: the systemic reading is Eger's inference from siting and common patronage. The group is therefore epistemic, the relation runs Site → Interpretation, and no entity type is required. *Record:* membership is already recorded, as untyped `associated_entities`; the typed relation makes it queryable, which is the whole gain. *Scholarship:* whether a coordinated system existed is precisely what is contested; the query returns who argued what, and deliberately does not adjudicate.

**5 Acceptance.** *Pass:* argued groups returned with members, scholar, publication and argumentative confidence, distinguishable from attested groupings. *Partial:* groups returned without member geometries. *Fail:* the relationship cannot hold an `INT-` endpoint — though note the existing `Identifier` pattern already admits one, so this failure would indicate a logical model narrower than the present schema.

---

## 5. RQ3 — Landscape Transformation

### QR-301 · Military conflict driving site development

**Question** (RQ3-1): *"How did military conflict — siege, capture, destruction, refoundation — drive the development, contraction and abandonment of frontier sites?"*
**Status** Draft

**1 Result.** *Purpose:* the query that converts a list of destructions into a model of transformation, by linking events to the phases they produced and terminated. *Answer shape:* one row per (event, site, phase): event identifier, type, date, the phase it terminated and the phase it produced, and the attestations for each link. Ordered by site, then event date. *Null means:* no phase link has been recorded — **not** that the event had no effect, which is the commonest misreading this query invites.

**2 Inventory.**

| | |
|---|---|
| Entities | `Event` with `event_type.primary: military`; `Site`; `Phase` |
| Relationships | `produced_phase`, `terminated_phase`, `damaged` (Event → Phase \| Site) |
| Assertions / pointers | Designated temporal assertion of each `Phase`; the event's own `start_date`/`end_date` |
| Certainty read | Chronological on both event and phase; identification certainty on the event ("did it happen") |
| Non-graph ops | Interval adjacency between terminated and produced phases; sequence per site |
| Analytical layer | None |

**3 Dependencies — categories 2, 3.**

| Item | Cat | Clears at |
|---|---|---|
| `produced_phase`, `terminated_phase`, `damaged` | 2 | §5.5 — **filed conditionally**, effective on Phase implementation |
| `Site`, `Phase` types | 3 | Migration step 3; step 9 |

**4 Limitations.** *Model:* none identified. *Record:* the event side is comparatively strong — 18 military events, 52 of 54 with a start date, 53 linked to places — so this entry is blocked by the phase side alone. *Scholarship:* attributing a phase transition to a named event is an inference, frequently from a destruction layer dated to a century rather than a year; the query records the asserted link with its confidence and does not establish causation.

**5 Acceptance.** *Pass:* one row per event/phase link with both phases and their intervals, and the interval adjacency computable. *Partial:* events returned linked to sites but not to phases. *Fail:* an event cannot stand in a relation to a phase, only to a site — which would lose the transformation model RQ3 requires and is a candidate classification (iv).

---

### QR-302 · Administrative reorganisation and the distribution of authority

**Question** (RQ3-2): *"How did administrative and political reorganisation reshape the frontier's structure and the distribution of authority across it?"*
**Status** Draft

**1 Result.** *Purpose:* to trace jurisdictions through their constitution, boundary change and dissolution, and to answer "who held what, when". *Answer shape:* one row per (territorial unit, phase): unit, holding polity, phase interval, designated boundary geometry where any, member sites, and the events that constituted or dissolved it. *Null means:* boundary unrecorded — which for jurisdictions is the normal state, not an omission.

**2 Inventory.**

| | |
|---|---|
| Entities | `TerritorialUnit`; `Polity`; `Site`; `Phase`; `Event` with `event_type.primary: administrative` |
| Relationships | `belongs_to` (Site → TerritorialUnit); `held_by` or `subordinate_to` (TerritorialUnit → Polity); `produced_phase`; `restores` |
| Assertions / pointers | Designated spatial assertion of the unit — **designated only**; designated temporal assertion of each phase |
| Certainty read | Spatial (weak, boundaries); chronological; relationship |
| Non-graph ops | Membership aggregation; interval sequencing |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `restores` term | 2 | **Held** — 0 cases; no TerritorialUnit records exist |
| `TerritorialUnit`, `Polity` as distinct types; `Phase` | 3 | Migration step 3 (10 records triaged); Polity extraction (M7); Phase at step 9 |
| Jurisdiction boundaries | 4 | Phase 3 — no place record carries a boundary polygon |

**4 Limitations.** *Model:* none identified. The interruption rule at §4.5 — dissolution and recreation give two units unless the sources treat it as restoration — is the specified answer to the hardest case here. *Record:* `political_affiliation_history` is used by 5 places of 190 and `administrative_status_history` by 1; 3 events are `creation_of_administrative_unit`, which is the ʿawāṣim material the contract names. *Scholarship:* the thughūr and ʿawāṣim boundaries are contested and were probably never sharp; a unit with no boundary geometry is the honest representation and the query must not present it as missing data.

**5 Acceptance.** *Pass:* units returned with holder, phase interval and member sites, and a boundary change representable as a phase rather than as a new unit. *Partial:* units without boundaries. *Fail:* a polity's extent must be stored rather than derived from its held units — which would allow the two to contradict.

---

### QR-303 · Economic processes sustaining or undermining settlement

**Question** (RQ3-3): *"How did economic processes — agricultural exploitation, resource extraction, the fiscal burden of defence — sustain or undermine frontier settlement?"*
**Status** Draft

**1 Result.** *Purpose:* to assemble the economic base of frontier settlement — irrigation, mining, agricultural landscapes, fiscal arrangements — against settlement phases, so that expansion and contraction can be set beside their economic conditions. *Answer shape:* one row per (site or landscape feature, phase, economic process): the process, its evidence, the associated infrastructure, and the phase interval. *Null means:* no economic evidence recorded — very frequently the case, and not a finding about economic activity.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `LandscapeFeature` with `origin: anthropogenic` (canals, field systems); `Component` (mills, kilns, cisterns); `Phase`; `Event` with `event_type.primary: economic` |
| Relationships | `contains`; `depends_on`; `crosses_at` |
| Assertions / pointers | Designated temporal assertion of each phase; economic assertions with supporting attestations |
| Certainty read | Chronological; functional (on the infrastructure's phase) |
| Non-graph ops | Aggregation by process type; co-occurrence of process and phase |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| Economic-process vocabulary (extraction, irrigation, fiscal, pastoral) | **2** | **Not yet filed.** No controlled vocabulary exists for economic process; `EventCategory: economic` exists but has **0 events** |
| `Site`, `LandscapeFeature`, `Component`, `Phase` types | 3 | Migration steps 3 and 9 |
| Fiscal evidence | 4 | Phase 3 — 9 attestations mention taxation; the fiscal burden of defence is barely attested in the present corpus |

**4 Limitations.** *Model:* none identified. *Record:* the hydraulic evidence is the strongest of the three processes — 47 attestations and 18 places — while mining is thin (15 attestations, 4 places) and fiscal thinner (9 attestations). **Zero events carry `economic` as a primary type**, so economic processes are presently recorded only as attestation content, not as modelled processes. *Scholarship:* the causal claim in the question — that economic conditions sustained or undermined settlement — is not recoverable from co-occurrence, and the query supplies the evidence for the argument rather than the argument.

**5 Acceptance.** *Pass:* economic processes returned per phase with their infrastructure and evidence, aggregable by process type. *Partial:* processes returned without phase association. *Fail:* anthropogenic landscape-scale infrastructure (a canal) cannot be held as a spatial entity of equal standing with a site — which would defeat the occupation-not-origin boundary at §4.3.

---

### QR-304 · Environmental conditioning of settlement and movement

**Question** (RQ3-4): *"How did environmental conditions and events condition the possibilities of settlement and movement?"*
**Status** Draft

**1 Result.** *Purpose:* to set environmental constraint and environmental event against settlement and route evidence. *Answer shape:* two result sets — environmental events with the sites and phases they affected; and landscape features characterised as environmental constraints with the settlements and routes falling within or against them. *Null means:* unrecorded, and for environmental events this is near-total.

**2 Inventory.**

| | |
|---|---|
| Entities | `Event` with `event_type.primary: environmental`; `LandscapeFeature`; `Site`; `Phase` |
| Relationships | `damaged`, `terminated_phase` (Event → Site \| Phase); `contains`, `adjoins` |
| Assertions / pointers | Designated spatial assertions — **designated only**; designated temporal assertions |
| Certainty read | Chronological (environmental events are frequently loosely dated); spatial |
| Non-graph ops | Spatial containment; interval overlap |
| Analytical layer | None |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `damaged`, `terminated_phase` | 2 | §5.5 — filed conditionally on Phase |
| `Site`, `LandscapeFeature`, `Phase` | 3 | Migration steps 3 and 9 |
| Environmental evidence | **4** | **The binding constraint. 2 environmental events exist in the whole corpus, of which 1 is an earthquake; 3 attestations mention seismic activity.** This entry is evidence-starved rather than structurally blocked |

**4 Limitations.** *Model:* none identified. *Record:* the most severe of any entry here. Two environmental events for a four-century frontier is not a sample. *Scholarship:* environmental determinism is a live methodological danger, and the query deliberately returns co-occurrence rather than conditioning; the inference belongs to the historian and should be made explicit as an Interpretation.

**5 Acceptance.** *Pass:* environmental events returned with affected sites and phases, and features returned with the settlements standing in spatial relation to them. *Partial:* events returned without phase effects. *Fail:* an environmental event cannot use the same event-to-phase machinery as a military one — which would mean the single Event type is not carrying its vocabulary honestly.

---

### QR-305 · Mechanisms of interaction — **candidate capability finding, §3.3.1**

**Question** (RQ3-5): *"Through what mechanisms did the frontier facilitate interaction as well as conflict?"* The contract operationalises this by naming eleven mechanisms: *trade and exchange; pilgrimage; diplomacy; prisoner exchange; raiding; taxation; pastoral movement; agricultural exploitation; military logistics; communication; and migration.*
**Status** Draft — **classification (iv) finding raised, and resolved by ontology Amendment 1 (2026-07-23)**

**1 Result.** *Purpose:* to retrieve, per mechanism, the evidence that the frontier operated in that mode, so that the "barrier" model can be tested against what the sources actually record. *Answer shape:* one row per (mechanism, evidence item): the mechanism, the entity or event it attaches to, the attestation, its provenance and date. Aggregable to a mechanism-by-period table. *Null means:* the mechanism is unattested in the corpus.

**2 Inventory.**

| | |
|---|---|
| Entities | `Event`; `Site`; `Route`; `Person`; `Polity` |
| Relationships | various, per mechanism |
| Assertions / pointers | Assertions in the general propositional role |
| Certainty read | Evidential confidence; chronological |
| Non-graph ops | Aggregation by mechanism and by period |
| Analytical layer | None |

**3 Dependencies — category 2, with a §3.3.1 finding.**

| Item | Cat | Clears at |
|---|---|---|
| `interaction_mechanism` attribute on Event and Assertion | — | **Cleared.** Adopted 2026-07-23 as ontology Amendment 1, on the finding below |
| Nine mechanism terms: `trade_exchange`, `diplomacy`, `prisoner_exchange`, `raiding`, `taxation`, `pastoral_movement`, `agricultural_exploitation`, `military_logistics`, `migration` | 2 | §5.5 Board decision; filed 2026-07-23 with verified cases |
| `pilgrimage` (2 verified cases), `communication` (1) | 2 | **Held** pending sufficient evidence |
| Entity types for the mechanisms' subjects | 3 | Migration step 3 |

**§3.3.1 finding.** The contract names eleven mechanisms and states that naming them "specifies what the database must be able to capture". **No element of the frozen ontology carries a mechanism.** The candidates and why each fails:

- `EventCategory` — carries the *kind* of a happening, not the mode of interaction it instantiates. A prisoner exchange is a `diplomatic` event; so is a treaty. The category cannot distinguish them, and widening it to eleven terms would conflate two classification bases, which is exactly the `PlaceType` error §2.1 removes.
- A `Relationship` type — mechanisms are not relations between two records. Pastoral movement is not a relation; it is a mode of activity.
- An `Assertion` — an assertion carries a proposition, and any given assertion may evidence a mechanism, but the mechanism is a property of what the assertion is *about*, not of the assertion.
- An `AnalyticalRegion` — analytical layer, and L2 forbids the domain referencing it.

**Per §3.3.1, the burden is on establishing drafting error, which requires naming the element that does express the requirement. I cannot name one.** The entry is therefore recorded as a capability finding and is not redrafted.

*What the finding was, precisely.* The ontology could record every mechanism's *evidence* — the corpus holds it, in **verified** counts: 8 attestations on taxation, 8 on raiding, 8 on agricultural exploitation, 6 on trade and exchange, 6 on diplomacy, 6 on migration, 4 on pastoral movement, 4 on military logistics, 3 on prisoner exchange, 2 on pilgrimage, 1 on communication. What it could not do was make the mechanism a **retrievable dimension**, so that "which mechanisms operated at this site in this period" is a query rather than a reading exercise. The eleven mechanisms were introduced by the contract specifically to make interaction operationalisable, and the ontology as frozen did not operationalise them.

*Correction to this entry, per rule 16.* As first drafted this paragraph cited 14 attestations on prisoner exchange and 5 on pilgrimage. Those were **scan totals, not verified counts**: *fidāʾ* had matched **Abū al-Fidāʾ**, the fourteenth-century geographer cited throughout the corpus, and one pilgrimage hit was an Ottoman-era site outside the corpus period while another concerned the same entity as a hit already counted. The verified figures are **3 and 2**. The finding is unaffected — it was never a count argument, and rests on the absence of a bearer rather than on the quantity of evidence — but the entry may not enter the repository carrying figures known to be wrong. This correction is one of the five instances justifying **rule 16**.

*Outcome.* The assessment offered here was that this was a **modest** defect with a **cheap** remedy — an `interaction_mechanism` controlled vocabulary applied as an attribute to Event and to Assertion, adding no type and following principle 8 exactly. **The Board accepted it**, and adopted conceptual ontology **Amendment 1** on 2026-07-23 under §5.8, naming this entry as the demonstrated defect in the commit's first line. The accepted framing was **incompleteness with respect to the contract rather than defect**: the ontology was internally consistent and every commitment held, but one analytical dimension the contract requires was not representable.

**4 Limitations.** *Model:* **resolved.** The ontology now provides an explicit `interaction_mechanism` attribute on Event and Assertion. Nine mechanisms currently satisfy the §5.5 admission threshold; `pilgrimage` and `communication` are held pending sufficient evidence. **This is the expected condition of a vocabulary that grows on evidence, per Amendment 1's own text, and not a shortfall in the amendment** — the attribute was adopted with an incomplete vocabulary by design, and the two held terms are held rather than stretched. The northeast Anatolian corridor extraction is a plausible source of the missing cases: pilgrimage traffic and the *barīd* are both better attested in that material than in the Cilician and Jaziran gazetteer the present corpus derives from. *Record:* mechanism evidence exists but is unlabelled until the attribute is populated, so counts before population remain reading-derived. *Scholarship:* the eleven mechanisms are the contract's own analytic scheme, not the sources'; assigning a passage to a mechanism is an editorial act and should be attested as one.

**5 Acceptance.** *Pass:* one row per (mechanism, evidence item), aggregable to a mechanism-by-period table, with the mechanism as a retrievable value rather than a keyword match. *Partial:* evidence returned per mechanism by manual assignment. *Fail:* mechanism is recoverable only by reading — **which is the present state, and is the finding.**

---

## 6. RQ4 — Evidence Integration

### QR-402 · Provenance chain preservation — **CALIBRATION ENTRY**

**Question** (RQ4-2): *"How can the provenance of every statement — which source, reached through which chain of transmission, at what evidential level — be preserved rather than flattened?"*
**Status** Draft · **Category 1 — executable against the present corpus**

**1 Result.** *Purpose:* to demonstrate that every statement in the corpus resolves to a source, a transmission route and an evidential level, and to expose any statement that does not. This is the corpus's central methodological claim, stated as a test. *Answer shape:* one row per attestation: attestation identifier, the assertion it supports, source identifier and short title, provenance category, evidential confidence, citation string, and a flag for whether the citation records a mediating source. Plus a summary by provenance category. *Null means:* a broken chain, and every null is an error rather than a finding.

**2 Inventory.**

| | |
|---|---|
| Entities | None — epistemic layer only |
| Relationships | None — evidential links are structural |
| Assertions / pointers | `Assertion` in the propositional role; no designated pointers resolved |
| Certainty read | **Evidential confidence** only. None of the five substantive dimensions |
| Non-graph ops | Grouping and counting by provenance category; string inspection of citations for mediation markers |
| Analytical layer | None |

**3 Dependencies — category 1, none.** All 477 attestations carry a single `source` (0 violations at scan), a provenance category from the 12 in use, an evidential confidence, and a citation. All 79 sources are present. Rule 8 gives every attestation a non-empty claim, at 0 violations.

*Not recorded as dependencies, deliberately:* the `ObservationRecord` → `Assertion` rename (a name, not a capability); the reference-mode extension (this entry does not read subject links).

**4 Limitations.** *Model:* none identified. *Record:* 208 of 477 attestations support no assertion, so the assertion column is null for 43.6% of rows — **an I3 violation surfaced as a finding, which is the correct behaviour and not a limitation of the query.** *Scholarship:* the citation's transmission marker is free text, so mediation detection is a string test and will miss unconventional phrasings; the count is a lower bound.

*Correction (field-4 amendment, 2026-07-23, authorised following the calibration run).* The flag errs in **both** directions, not one. The **character** of the limitation was predicted correctly — a free-text string test is unreliable — but its **direction** was not. The calibration run found a raw scan of 234 against a verified **212 of 477 (44.4%)**, the 22 false positives forming a single class: coordinate-transformation citations of the form "converted to WGS84 *via* pyproj", where *via* marks a transformation and not a transmission route. The predicted miss of unconventional phrasings also holds, so the verified 212 is **itself a floor**: true mediation is at least 212 of 477. Per rule 16, the mediation figure is reported as the verified count, never the scan total. Field 3 (the prediction) is unchanged, per §7.2 Rule 1.

**5 Acceptance.** *Pass:* every attestation resolves to source, provenance category, evidential confidence and citation, with the mediation flag derived from the citation, and the summary by provenance category matching the measured distribution (primary_paraphrase 225, modern_synthesis 95, archaeological_evidence 57, primary_quotation 33, gis_derived 22, primary_observation 19, primary_summary 11, modern_identification 9, numismatic 2, epigraphic 2, cross_source_synthesis 1, modern_interpretation 1). *Partial:* mediation flag unavailable. *Fail:* any attestation cannot be resolved to exactly one source; or evidential confidence cannot be read without an aggregate.

---

### QR-403 · Competing interpretations retrievable independently

**Question** (RQ4-3): *"How can competing scholarly interpretations of the same evidence be represented transparently, without the database privileging one reading?"*
**Status** Draft

**1 Result.** *Purpose:* success criterion 6's second clause, as a query. To retrieve every position in a dispute as a separate record with its own scholar, date and confidence, and to retrieve the disagreement itself as a structure. *Answer shape:* one row per interpretation in a dispute: scholar, publication, date, argumentative confidence, argument summary, supporting attestations, and the interpretations it contradicts, revises, corroborates or parallels. Grouped into dispute clusters. *Null means:* no relation recorded — currently the state for all 174 interpretations.

**2 Inventory.**

| | |
|---|---|
| Entities | The subject entities of the dispute, of any type |
| Relationships | `contradicts` (existing, 0 uses); `corroborates`; `parallel_case`; `revises`; `supersedes_attestation` (existing, 0 uses) — all with `INT-` endpoints |
| Assertions / pointers | `Assertion`, `Attestation` for the shared evidence base |
| Certainty read | **Argumentative confidence**; evidential confidence on the shared attestations |
| Non-graph ops | Connected-component grouping over the interpretation graph |
| Analytical layer | None |

**3 Dependencies — categories 2, 3.**

| Item | Cat | Clears at |
|---|---|---|
| `corroborates`, `parallel_case` | 2 | §5.5 Board decision; filed with 4 and 3 cases |
| `revises` | 2 | **Held** — 1 case, and that case does not yet exist as two records |
| Interpretation-to-interpretation relationship instances | 3 | Migration step 6 — rule-10 promotion of 29 prose cross-references |
| Dossier unbundling | 3 | Migration step 6 — 4 interpretations hold multiple numbered positions in one argument |

**4 Limitations.** *Model:* none identified — and note the schema already admits `INT-` relationship endpoints, so this is a data and vocabulary gap, not a structural one. *Record:* 58 entities carry two or more interpretations, so the raw material for dispute clusters exists; what does not exist is a single structural link between any two of them (0 of 144 relationships). *Scholarship:* whether two positions genuinely conflict, as against addressing different questions, is a judgement — INT-0167's explicit "distinct from INT-0060, which concerns siting rather than scale" is an example of a scholar making it, and the query records such judgements rather than inferring them.

**5 Acceptance.** *Pass:* each position returned as a separate row with its own scholar and confidence, and the dispute retrievable as a connected component, with no position reachable only by reading prose. *Partial:* positions returned separately but disputes only by prose inspection. *Fail:* a relationship cannot hold two `INT-` endpoints; or a bundled dossier cannot be represented as separate positions without losing the association between them.

---

### QR-404 · Multidimensional uncertainty

**Question** (RQ4-4): *"How can uncertainty be represented as the multidimensional quantity it is, rather than as a single confidence score?"*
**Status** Draft

**1 Result.** *Purpose:* to retrieve, for a subject, each certainty dimension independently, and to confirm that no stored aggregate exists to be filtered on. *Answer shape:* one row per subject: identification, chronological, spatial, functional and relationship certainty, each with the record element that bears it, plus the evidential and argumentative confidences of its supporting evidence — seven quantities, none derived from another. *Null means:* the dimension does not apply to that subject type, per the §8.1 register — and the query must distinguish "does not apply" from "not recorded".

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`, `LandscapeFeature`, `Route`, `TerritorialUnit`, `Component`, `Phase`, `Event`, `Polity`, `Person` |
| Relationships | Any, for relationship certainty |
| Assertions / pointers | Spatial and temporal assertions — **full set, not designated only**, since spatial certainty attaches per assertion |
| Certainty read | **All five, plus both evidential quantities, each named individually** |
| Non-graph ops | Per-type dimension applicability lookup against §8.1 |
| Analytical layer | None |

**3 Dependencies — category 3.**

| Item | Cat | Clears at |
|---|---|---|
| Functional certainty has no field anywhere in the schema | 3 | Migration step 9 (Phase and Component) |
| Chronological certainty on entities other than events | 3 | Migration step 9 (Phase) |
| `overall_confidence` retirement | 3 | Migration step 3/4 — present on 325 records and filterable today |
| Spatial certainty per competing assertion | 3 | Migration step 3 (M5) |

**4 Limitations.** *Model:* none identified. *Record:* four of the five are separately retrievable today in some form — identification (via `identification_status` and `identification_confidence`), spatial (`coordinate_confidence`), chronological (on event `start_date.confidence`), relationship (all 144 relationships carry confidence) — while **functional certainty has no home at all**, and `overall_confidence` sits over the top of them on 325 records. *Scholarship:* the five dimensions are the project's analytic scheme; a scholar assigning them is making five judgements where the literature usually makes none explicitly.

**5 Acceptance.** *Pass:* seven quantities returned independently for a subject, with per-type applicability distinguishing "not applicable" from "not recorded", and no aggregate present to filter on. *Partial:* the four presently-separable dimensions returned. *Fail:* any dimension can only be obtained by decomposing an aggregate — which would mean the aggregate is authoritative and principle 6 is defeated.

---

### QR-441 · Certainty-dimension separability audit — **CALIBRATION ENTRY, derived**

**Question** — derived from RQ4-4, serving as its pre-migration baseline.
**Status** Draft · **Category 1 — executable against the present corpus**

**1 Result.** *Purpose:* to establish, before migration, exactly which certainty quantities are separately retrievable in the corpus as it stands, which are absent, and where aggregates are stored. It is both a baseline against which QR-404 can later be judged and, on its own, a partial answer to RQ4-4 in the instrument-facing sense. *Answer shape:* one row per record type: which of the five dimensions has a bearer, the field bearing it, how many records populate it, and whether an aggregate is present. *Null means:* the dimension has no bearer for that type — a finding, not missing data.

**2 Inventory.**

| | |
|---|---|
| Entities | All present record types |
| Relationships | All, for relationship certainty |
| Assertions / pointers | Coordinates block as the present bearer of spatial certainty |
| Certainty read | All five plus both evidential quantities, **named individually and counted, not aggregated** |
| Non-graph ops | Counting and grouping by record type and field |
| Analytical layer | None |

**3 Dependencies — category 1, none.** Every field this query reads exists and is populated: `identification_status` on all 190 places, `identification_confidence`, `coordinate_confidence` on the 57 coordinate-bearing places, `confidence` on all 144 relationships, `confidence` on all attestations and interpretations, `start_date.confidence` on 52 of 54 events, `overall_confidence` on 325 records.

**4 Limitations.** *Model:* none identified. *Record:* the audit will report **functional certainty as having no bearer anywhere**, which is a true finding about the present schema and not a query failure. *Scholarship:* none.

**5 Acceptance.** *Pass:* the audit returns a complete per-type map of dimension bearers and counts, identifying `overall_confidence` on exactly 325 records and functional certainty as unborne. *Partial:* counts without the per-type applicability map. *Fail:* any dimension's count cannot be obtained without reading an aggregate.

---

## 7. RQ5 — Analytical Infrastructure

### QR-501 · Spatial and network analyses

**Question** (RQ5-1): *"What spatial and network analyses — least-cost path modelling, viewshed and intervisibility analysis, catchment and territory reconstruction, network analysis of relationships between sites and landscape features — become possible when the evidence is integrated spatially?"*
**Status** Draft

**1 Result.** *Purpose:* the demonstration entry for RQ5's central claim. Four analyses run directly against the store, each returning a result and a coverage statement. *Answer shape:* four result sets — a least-cost path between attested termini; a viewshed from a fort over a pass with the intervisible set; a catchment polygon per major centre; and a centrality ranking over the site-and-feature network. Each accompanied by the proportion of relevant entities carrying a designated geometry. *Null means:* insufficient geometric coverage to run — and the coverage statement makes that legible rather than silent.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `LandscapeFeature`; `Route` |
| Relationships | `controls`, `overlooks`, `intervisible_with`, `crosses_at`, `traverses`, `member_of_route_family`, plus the existing spatial terms |
| Assertions / pointers | Designated spatial assertion of every participant — **designated only**; the computed outputs written back as new spatial assertions with `gis_derived_observation` provenance |
| Certainty read | Spatial on every input; relationship certainty on the network edges |
| Non-graph ops | **Least-cost path; viewshed; catchment (Thiessen or cost-allocation); betweenness centrality.** The heaviest non-graph load of any entry |
| Analytical layer | None — though results are typically reported per `AnalyticalRegion` |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `controls`, `overlooks`, `crosses_at` | 2 | §5.5 Board decision |
| `intervisible_with` | 2 | **Held — 0 cases, and by design.** Intervisibility is computed, not attested; its cases will be *generated by this very entry*. The term should be proposed from this query's results |
| `traverses`, `member_of_route_family` | 2 | Held |
| Spatial types; full geometry types; designated assertions | 3 | Migration step 3 |
| Geometric coverage | **4** | Phase 3. **70% of places carry no coordinate**, so every analysis here runs on a minority and must report it |
| Terrain cost surface | 4 | External acquisition |

**4 Limitations.** *Model:* none identified. *Record:* the coverage limitation is the binding one and does not clear with migration — it clears with extraction. *Scholarship:* a network built from attested relationships measures what has been recorded about the frontier, not the frontier; centrality over 144 relationships of which 21 are `near` is a statement about the corpus.

**5 Acceptance.** *Pass:* all four analyses execute against the store with no export-and-remodel step, and each writes its output back as a spatial assertion with `gis_derived_observation` provenance and its own confidence. *Partial:* analyses run on the geometry-bearing subset with coverage reported. *Fail:* any analysis requires a transformation script — in which case the script names the missing structure, per success criterion 5.

---

### QR-502 · Temporal analyses

**Question** (RQ5-2): *"What temporal analyses — the tracing of settlement expansion and contraction, the correlation of destructions and refoundations with attested events, the reconstruction of a site's or a region's phased development — become possible when the evidence is modelled with explicit chronology?"*
**Status** Draft

**1 Result.** *Purpose:* the temporal counterpart to QR-501. *Answer shape:* three result sets — a site count and aggregate extent per time slice across the study period; destructions and refoundations aligned to their attested events; and a phase-by-phase development sequence for a named site or region. *Null means:* the slice has no phased evidence, which for most of the corpus is currently the case.

**2 Inventory.**

| | |
|---|---|
| Entities | `Site`; `Phase`; `Event`; `Component` |
| Relationships | `produced_phase`, `terminated_phase` |
| Assertions / pointers | Designated temporal assertion of each phase — **designated only for the time-slice counts, full set for the competing-chronology view**, and the entry requires both |
| Certainty read | Chronological on every phase and event; spatial where extent is aggregated |
| Non-graph ops | Time-slicing; interval overlap; aggregation per slice; sequence reconstruction |
| Analytical layer | Optional temporal extent of an `AnalyticalRegion`, where a region bounds the analysis |

**3 Dependencies — categories 2, 3, 4.**

| Item | Cat | Clears at |
|---|---|---|
| `produced_phase`, `terminated_phase` | 2 | §5.5 — filed conditionally |
| `Phase`, `Site`, `Component` types | 3 | Migration steps 3 and 9 |
| Competing datings as assertions | 3 | Migration step 9 |
| Phased chronological evidence | **4** | Phase 3. **`alternative_datings` is used by zero places and zero events**, and `chronology` by one place of 190 |

**4 Limitations.** *Model:* none identified — this is the entry that exercises principle 3's co-equality from the temporal side, as QR-201 does from the spatial. *Record:* the temporal dimension of the spatial corpus is at present essentially unmodelled; 52 of 54 events carry a start date, but only 8 carry an end date, so event durations are largely absent. *Scholarship:* **the competing-phase-division limitation at §10.13 bites here first and hardest**, and is expected to bind during Phase 3 on the excavation-heavy northeast Anatolian corridor. A time-slice count assumes one phasing per site; where two are argued, this entry silently adopts the adjudicated one.

**5 Acceptance.** *Pass:* time-slice counts and extents computed from designated temporal assertions, with the competing-dating view retrievable from the full assertion set for the same phases. *Partial:* slices computed where phases exist. *Fail:* a phase can carry only one dating, so competing chronologies cannot coexist — which would defeat the §10.11 handling of the Al-Muthaqqab case and is a candidate classification (iv).

---

### QR-504 · Publication-quality outputs

**Question** (RQ5-4): *"What publication-quality outputs — phased maps, gazetteers, network diagrams, analytical tables — can the integrated system generate directly from its data?"*
**Status** Draft

**1 Result.** *Purpose:* to establish which of the four named outputs the system generates without an intermediate authoring step. *Answer shape:* four artefacts, each with a provenance block naming the query, the analytical region and temporal window used, and the coverage achieved. *Null means:* the output cannot be generated, and the entry says which of the four.

**2 Inventory.**

| | |
|---|---|
| Entities | All spatial types; `Phase`; `Event` |
| Relationships | The full spatial and hierarchical set, for the network diagram |
| Assertions / pointers | Designated spatial and temporal assertions — **designated only**; attested names with their temporal validity for the gazetteer |
| Certainty read | All five, since a publication-quality gazetteer reports uncertainty per dimension |
| Non-graph ops | Cartographic rendering; table aggregation; graph layout |
| Analytical layer | `AnalyticalRegion` with membership and optional temporal extent, cited in each artefact's provenance block |

**3 Dependencies — categories 2, 3, 4.** Mixed by artefact, and the entry records them separately because they clear at different times:

| Artefact | Cat | Clears at |
|---|---|---|
| **Gazetteer** | **1 for the present-corpus form** — see QR-544 | now |
| Phased map | 3 | Migration steps 3 and 9 |
| Network diagram | 2, 3 | §5.5 vocabulary; migration step 3 |
| Analytical table | 3 | Depends on the table; most need Phase |

**4 Limitations.** *Model:* none identified. *Record:* a phased map needs both phases and polygons and has neither. *Scholarship:* publication quality includes the caveats, and an output that does not carry its coverage statement is not publication quality regardless of its rendering.

**5 Acceptance.** *Pass:* all four artefacts generated directly, each carrying a provenance block naming its query, region and window. *Partial:* the gazetteer alone, per QR-544. *Fail:* any artefact requires manual assembly of data the store holds.

---

### QR-544 · Gazetteer generation from present data — **CALIBRATION ENTRY, derived**

**Question** — derived from RQ5-4, isolating the one named output the present corpus can generate.
**Status** Draft · **Category 1 — executable against the present corpus**

**1 Result.** *Purpose:* to generate a publication-form gazetteer from the corpus as it stands, and thereby to establish what "directly from its data" currently means. *Answer shape:* one entry per place: standardised name; alternative names with language, script and name type; coordinates with method, precision and uncertainty radius where present; identification status and identification confidence; supporting attestations with source and provenance; and a coverage statement. Ordered alphabetically by standardised name. *Null means:* the datum is unrecorded, and the gazetteer prints it as unrecorded rather than omitting the field.

**2 Inventory.**

| | |
|---|---|
| Entities | The present `PlaceEntity` population, as the ontology's spatial types will be derived from it |
| Relationships | None required |
| Assertions / pointers | The present coordinates block, standing in for the designated spatial assertion |
| Certainty read | **Identification certainty** (`identification_status`, `identification_confidence`); **spatial certainty** (`coordinate_confidence`); **evidential confidence** on each attestation. Named individually |
| Non-graph ops | Sorting; per-entry aggregation of attestations; coverage computation |
| Analytical layer | None — the whole corpus is the scope, stated as such rather than as a null region |

**3 Dependencies — category 1, none.** 190 places, all carrying `standardised_name` and `identification_status`; 152 with alternative names; 57 with coordinates; `linked_attestations` populated throughout.

**4 Limitations.** *Model:* none identified. *Record:* the coverage statement is the honest content here — **70% of entries will carry no coordinate**, and the gazetteer must print that as a headline figure rather than as 133 blank fields. Alternative names carry no temporal validity, so a name cannot be dated. *Scholarship:* identification status reflects current scholarly opinion and 7 places are recorded as disputed; the gazetteer reports the dispute rather than choosing.

**5 Acceptance.** *Pass:* a complete gazetteer generated in one pass with no manual assembly, printing per-entry uncertainty across three separately-named quantities and a corpus-level coverage statement. *Partial:* a gazetteer without per-entry provenance. *Fail:* attestation provenance cannot be carried into the output without a second pass — which would mean the gazetteer is assembled rather than generated.

---

## 8. Summary

### 8.1 Dependency distribution across all twenty-two entries

| Category present | Entries |
|---|---|
| **1 — none** | 3: QR-401, QR-402, QR-441, QR-544 *(four, of which QR-401 was phase 1)* |
| **2 — vocabulary** | 13 |
| **3 — migration** | 18 |
| **4 — evidence coverage** | 10 |

Only **four entries in the whole register are executable today**, and three of the four sit in the epistemic layer. Every entry touching the spatial or temporal dimensions is migration-dependent without exception. That is the expected shape given that Phase and the spatial type split are net-new construction, but it is worth stating plainly: **the register's verdict on the present corpus is that the evidence machinery works and the landscape machinery does not yet exist.**

### 8.2 Candidate classification (iv) findings

| Entry | Finding | Provisional severity |
|---|---|---|
| **QR-305** | No ontology element carried an interaction mechanism; the contract's eleven named mechanisms were not operationalised | **Resolved.** Accepted as a demonstrated defect; ontology Amendment 1 adopted 2026-07-23, adding an `interaction_mechanism` attribute to Event and Assertion. No new type |

One finding across twenty-two entries. Three further entries record a *potential* classification (iv) in their **Fail** criteria rather than as findings — QR-103 (route identity across geometry change), QR-201 (phase-level geometry), QR-502 (competing datings per phase) — because in each case the ontology specifies the capability and only execution can show whether a logical model delivers it. Those are tests, not findings.

### 8.3 Calibration set, for execution now

**QR-402**, **QR-441**, **QR-544** — plus **QR-401** from phase 1, giving four. Executing these by hand before any logical model exists tests whether the register's authors understand the corpus. Predicted outcomes are stated in each entry's acceptance criteria and, where a count is predicted, the expected figure is given so that a discrepancy is unambiguous.

The phase-1 prediction was that two or three of the nineteen would be category 1. **One is.** The prediction was optimistic, and the shortfall is recorded here as the register's first accuracy datum under §7.3.

---

*End of phase 2. Read-only: no logical model, no schema, no records.*
