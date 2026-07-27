# Query Register — Format Specification and Phase-1 Worked Examples

**Status:** proposal for approval. Read-only pass; no logical model, no schema, no records.
**Written against:** `docs/methodology/conceptual_ontology.md` (frozen 2026-07-23) and `docs/research_questions.md` (frozen 2026-07-23).
**Corpus state:** `origin/main` at `44988e2`, 1,453 records, verified 2026-07-23.
**Scope of this phase:** the format, argued; three worked entries; the discrepancy procedure.
**Suggested repository path:** `docs/methodology/query_register.md`

---

## 1. What the register is for

Three jobs, and the format has to serve all three or it is not worth writing.

1. **Acceptance test for the logical model.** The model passes when every register entry runs against the store with no intervening remodelling step. Written before the model so that the model is designed against executable requirements rather than prose.
2. **Boundary condition on reopening the frozen ontology.** Governance §5.8 admits a content amendment to a frozen document only on a *demonstrated defect*. The register is where a defect is demonstrated: a query the frozen specification promised and cannot express is a defect; a query that is merely awkward, or blocked by work not yet done, is not.
3. **A prospective record of what was predicted.** Recording the dependency state before execution, on the Item-G model, so that a surprise at execution time is legible as a surprise rather than being absorbed into a revised expectation.

The third job constrains the format more than the other two, and §6 is about it.

---

## 2. Notation: the decision, and the argument for it

### 2.1 The requirement

The queries must be expressed in **ontology terms** — entity types, relationship types, phases, assertions, designated pointers — and must not presuppose a logical model. A register written against a guessed schema tests whether the logical model matches the guess.

### 2.2 What was considered

| Option | Verdict |
|---|---|
| **SPARQL / basic graph patterns** | Rejected. A BGP presupposes a triple-shaped model. Worse, most register queries need operations BGPs cannot express — spatial predicates (viewshed, least-cost path), aggregation ("coverage varies between regions"), set difference ("sites never examined"). Reaching for SPARQL 1.1 with `FILTER`, `GROUP BY` and geospatial extensions imports a query-language commitment through the back door, and the geospatial extensions are exactly where implementations diverge. |
| **Cypher / property-graph patterns** | Rejected for the same reason, more sharply: property graphs commit to a node/edge/property split that the ontology does not make. A designated spatial assertion is neither obviously a node nor obviously a property, and the notation would force the choice before the logical model has made it. |
| **Relational algebra** | Rejected. Presupposes tables, which is precisely the schema-level commitment the brief forbids. |
| **Unstructured prose** | Rejected. Not checkable. Two readers can disagree about which ontology elements a prose query traverses, and the disagreement surfaces only at execution — the worst moment. |
| **Structured English over a closed inventory** | **Adopted.** Argued below. |

### 2.3 Why structured English over a closed inventory

**The register is not executed as written; it is *translated*.** Whatever the logical model turns out to be, someone will write the actual query in that model's language. The register's job is to make the translation unambiguous and to make the translation's fidelity checkable. A formal notation would give apparent precision while smuggling in model commitments — and precision about the wrong thing, since what determines whether the model passes is not the phrasing but *which ontology elements must be traversable*.

**The inventory is the load-bearing part, not the English.** This is the central design decision of the format. The English states the intent; the required-inventory states the test. Every element in the inventory is drawn from a closed list — the type register at conceptual ontology §1, the relationship vocabulary, the certainty dimensions at §8.1, the assertion roles at §5.6 — and is therefore **mechanically checkable against the frozen specification**. An entry naming an element that does not exist in the ontology or in a filed §5.5 proposal is malformed and fails review before it is ever executed.

That checkability is what a formal notation was supposed to buy, and the inventory buys it without the model commitment.

**Readability matters here more than usual.** The register operates the reopening gate. A Board of historians must be able to read an entry and judge whether a failure constitutes a demonstrated defect. A SPARQL query with geospatial extensions cannot be read that way; a structured-English statement with an explicit element inventory can.

**One further argument, from the dual-implementation commitment.** Success criterion 4 requires the ontology to be implementable in both PostgreSQL/PostGIS and YAML with lossless correspondence. A register written in any one query language would be an acceptance test for one implementation and a translation exercise for the other. Written at the ontology level it is the same test for both, which is what an acceptance test for the *model* rather than for a *store* has to be.

### 2.4 The optional traversal sketch

Structured English is weak at two things: **direction** and **cardinality**. "Sites and the passes they control" does not say whether the relationship is traversed from site to pass or the reverse, or whether one site may control several passes.

So each entry may carry a **traversal sketch** — a minimal arrow notation, explicitly non-executable, whose only purpose is to disambiguate direction and multiplicity:

```
Site --[controls]--> LandscapeFeature{feature_type: pass}     (n:m)
Site --[has_phase]--> Phase --[designated_temporal]--> TemporalAssertion   (1:n, 1:1)
```

Conventions: `-->` is the stored direction; `<--` marks a traversal that runs against the stored direction and therefore requires inverse traversal (permitted under L1, which constrains stored references and not query direction, but worth flagging because a logical model may implement an edge one-way); `{...}` is an attribute constraint; `(1:1)`, `(1:n)`, `(n:m)` give multiplicity.

The sketch is **optional and subordinate**. Where it and the English disagree, the English governs and the entry is malformed. It exists to prevent a class of ambiguity, not to become the notation by the back door.

### 2.5 Two disciplines the notation must enforce

**Designated-pointer resolution must be explicit.** Every entry that touches geometry or dating states whether it reads the **designated** assertion or the **full set** of competing assertions. This is the co-equality mechanism (§5.6) and it is exactly where a logical model can quietly fail — by implementing a single geometry column and satisfying every query that reads the designated pointer while silently failing every query about the dispute. An entry that does not state which it reads is malformed.

**Certainty dimensions read must be named individually.** Not "confidence" — which of the five, or which of the two evidential quantities (§8.2). An entry naming "confidence" unqualified is malformed. This is the register's defence against the single-confidence-score failure the contract rejects.

---

## 3. Entry format specification

### 3.1 Identifier and heading

```
QR-<rq><nn>   <short title>
Question:     <verbatim subordinate question from the frozen contract, with its RQ>
Entry status: Draft | Approved | Blocked | Passed | Partial | Failed | Discrepancy
Prediction recorded: <date>          [immutable once Approved — see §6]
```

Identifiers are `QR-` plus the RQ number plus a two-digit sequence: `QR-102` is the second entry serving RQ1. **The register is indexed by subordinate question but not limited to one entry per question**: a question may need several queries, and some queries serve the instrument as a whole. The baseline is the 22 subordinate questions (RQ1: 4, RQ2: 5, RQ3: 5, RQ4: 4, RQ5: 4); derived entries are permitted and are marked as such.

**Entry status is distinct from result.** *Blocked* is not *Failed*: a blocked entry has not been run because a recorded dependency has not cleared. Conflating the two is how a scheduling fact becomes a capability claim.

### 3.2 Field 1 — Expected analytical result

Two parts, both required.

- **Purpose.** What the query is for, in one or two sentences: what a historian would do with the answer.
- **Answer shape.** What would constitute an answer. Cardinality (one row per what?), the fields returned, ordering where it matters, and — critically — **what a null or empty result means**. An empty result may mean "no such case exists", "no evidence has been recorded", or "the question does not apply"; an entry that does not distinguish these cannot be interpreted when it returns nothing.

### 3.3 Field 2 — Required inventory

The closed, explicit list of every ontology element the query traverses. Sub-fields; each is `none` where it does not apply, never omitted.

- **2a Entity types** — with any attribute constraints.
- **2b Relationship types** — each with stored direction, and flagged where inverse traversal is required.
- **2c Assertion roles and designated pointers** — spatial or temporal; and for each, **designated or full set** (§2.5).
- **2d Certainty dimensions read** — named individually from the five, plus evidential or argumentative confidence where read (§2.5).
- **2e Non-graph operations** — spatial predicates, aggregation, set difference, path computation, ordering. Named because these are what a graph-pattern notation would have hidden and what a logical model most often cannot do natively.
- **2f Analytical-layer elements** — AnalyticalRegion and its membership specification, where used. Flagged separately because L2 forbids the domain referencing them, and a query that appears to need a domain record to know its region is malformed.
- **2g Traversal sketch** — optional (§2.4).

### 3.4 Field 3 — Predicted dependency state

**Recorded prospectively, before any attempt to execute.** The four categories:

1. **none** — executable against the corpus as it stands
2. **vocabulary dependency** — needs a term still in §5.5 governance
3. **migration dependency** — needs a corpus transformation not yet done
4. **evidence-coverage dependency** — needs extraction or evidence that does not exist

**The dependency state is a set, not a single value.** An entry may carry several categories at once, and most non-trivial entries will. Recording only the most obvious one is a way for a category-1 component to hide behind a category-3 headline: if an entry is marked "migration-dependent" and fails after the migration, the vocabulary dependency nobody wrote down absorbs the surprise. Every blocking item is listed individually with its own category.

Each blocking item records:

| | |
|---|---|
| **Item** | the specific thing that is missing |
| **Category** | 1–4 |
| **Clears at** | the named governance decision, migration step or extraction pass that clears it |

**Predictions must be specific.** "Category 3, needs migration" is malformed. "Category 3: Site type does not exist; clears at migration step 3 (place pass)" is well formed. A vague prediction can absorb any failure, which defeats the purpose of recording it in advance — §6 depends entirely on this.

### 3.5 Field 4 — Known limitations

Where the query will answer partially, and why, under a three-way distinction that is **not** cosmetic:

- **Model limitation** — the ontology cannot express what is being asked. *This is the only kind that can constitute a demonstrated defect under governance §5.8.*
- **Record limitation** — the ontology can express it; the corpus does not currently contain the data.
- **Scholarship limitation** — the ontology can express it and the corpus holds what is known; the field does not know the answer.

Each is stated, or explicitly `none identified`. Silence is not permitted, because an unstated limitation reappears at execution as a surprise.

**The distinction between fields 3 and 4 is the distinction between time and capability.** A dependency clears on a schedule. A limitation does not. Conflating them makes a query blocked on scheduled work read as a capability failure of the ontology — which would be both false and, given the reopening gate, expensive. §5's third worked example exists to test this.

### 3.6 Field 5 — Acceptance criteria

What result satisfies the question, such that the logical model passes. Three bands:

- **Pass** — the condition under which the model has expressed the query.
- **Partial** — the condition under which the model expressed the query but the answer is limited by a field-4 limitation. A partial is a pass for the model and a limitation on the corpus, and the entry must say which limitation it is attributed to.
- **Fail** — the condition under which the model has not expressed the query. Fail requires a §6 discrepancy record.

Acceptance criteria are about **expressibility, not about the historical answer**. "Returns at least twelve fort/pass pairs" is a bad criterion — it tests the corpus. "Returns one row per fort/pass pair with phase interval and relationship certainty, without a transformation step" is a good one.

---

## 4. Worked example — QR-102

```
QR-102        Installations controlling passes and crossings, by phase
Question:     "How were passes, river crossings and other critical landscape features
              controlled, monitored and exploited, and by what installations
              (fortifications, watch-posts, kleisourai)?"  — RQ1, subordinate 2
Entry status: Draft
Prediction recorded: 2026-07-23
```

**1. Expected analytical result**

*Purpose.* To recover the control geography of the frontier: which installations stood in a controlling or observing relation to which passes, crossings and corridors, and when. It is the evidential base for the viewshed and corridor analyses RQ1 names, and the first query that would be run to produce a phased control map.

*Answer shape.* One row per (installation, landscape feature, phase) triple: installation identifier and name; feature identifier, name and feature type; relation type; the phase interval during which the relation held; relationship certainty; spatial certainty of each endpoint's designated geometry. Ordered by feature, then by phase start. **An empty result for a given feature means no controlling installation has been recorded for it** — which is distinct from no such installation having existed, and the two must not be conflated in any map generated from this query.

**2. Required inventory**

- **2a Entity types.** `Site`; `LandscapeFeature` constrained to `feature_type ∈ {pass, ford, crossing, defile}`; `Phase`.
- **2b Relationship types.** `controls` (Site → LandscapeFeature); `overlooks` (Site → LandscapeFeature). Both traversed in stored direction. Inverse traversal required for the per-feature grouping ("which installations control *this* pass").
- **2c Assertion roles and designated pointers.** Designated spatial assertion of `Site` — **designated only**. Designated spatial assertion of `LandscapeFeature` — **designated only**. Designated temporal assertion of `Phase` — **designated only**. *Rationale:* this query produces a map and needs one geometry per object; the competing-geometry question is a different query and is registered separately.
- **2d Certainty dimensions read.** Relationship certainty (on the `controls`/`overlooks` relationship); spatial certainty (on each designated spatial assertion). Chronological certainty on the phase's designated temporal assertion. **Not** identification certainty; **not** functional certainty.
- **2e Non-graph operations.** Interval overlap (relationship temporal scope against phase interval). Grouping and ordering. No spatial predicate — this query reads *attested* control relations; the computed-viewshed variant is a separate entry under RQ5.
- **2f Analytical-layer elements.** None.
- **2g Traversal sketch.**

```
Site --[controls|overlooks]--> LandscapeFeature{feature_type: pass|ford|crossing|defile}   (n:m)
Site --[has_phase]--> Phase                                                                 (1:n)
relationship --[temporal_scope]--> interval    ∩    Phase --[designated_temporal]--> interval
Site --[designated_spatial]--> SpatialAssertion                                             (1:1)
LandscapeFeature --[designated_spatial]--> SpatialAssertion                                 (1:1)
```

**3. Predicted dependency state — categories 2 and 3**

| Item | Cat | Clears at |
|---|---|---|
| `controls` relationship term | **2** | §5.5 Board decision; filed 2026-07-23 with 3 verified cases |
| `overlooks` relationship term | **2** | §5.5 Board decision; filed 2026-07-23 with 3 verified cases |
| `Site` type does not exist | **3** | Migration step 3 (place pass) |
| `LandscapeFeature` type does not exist | **3** | Migration step 3 (place pass) |
| `Phase` type does not exist | **3** | Migration step 9 (net-new construction) |
| Designated spatial assertions do not exist | **3** | Migration step 3 (geometry restructuring, M5) |

*A note on this prediction, offered because it bears on the format.* The brief anticipated this entry as "expected migration-dependent and nothing else". Applying the format honestly returns **2 and 3**, because `controls` and `overlooks` are filed under §5.5 but not yet approved, and a filed term is not an available term. The divergence is small, but it is exactly the class of item that would otherwise have surfaced only at execution — and by then the migration would be the obvious culprit and the vocabulary dependency would have been absorbed into it without anyone noticing. **Recording the dependency set rather than a single category is what caught it**, which is the argument for §3.4 in miniature.

**4. Known limitations**

- **Model limitation.** None identified. The ontology expresses attested control relations directly; the types, the relationship, the phase scoping and the certainty dimensions are all specified in the frozen document.
- **Record limitation.** Substantial and quantified. Of the control relations attested in prose in the present corpus, **at least six cannot be recorded as entity pairs because the controlled feature has no record** — Darbassak → Çalan Pass, Ṭaranda → Mazikiran Pass, Būqā → the Anṭākiya–Marʿash route, ʿAyn Zarba → the Jayhān–Taurus route, Hadath → an unnamed Taurus pass, al-Massīsa → route. The vocabulary gap sits downstream of an entity gap, and this query will under-report until Phase 3 mints the missing passes and routes. Separately, **70% of place records carry no geometry**, so any map generated from this query reports on a minority of its rows and must state its coverage.
- **Scholarship limitation.** The sources do not distinguish guarding from controlling from commanding an approach; a single `controls` term was filed for that reason. A query asking for the *mode* of control would exceed what the evidence supports, and this entry deliberately does not ask it.

**5. Acceptance criteria**

- **Pass.** The store returns one row per (installation, feature, phase) triple with all fields at §1, resolving each designated pointer, computing the interval overlap, and grouping in both directions (installations per feature, features per installation) — with no export-and-remodel step.
- **Partial.** As above, but returning only rows where both endpoints carry a designated geometry. Attributable to the record limitation, not to the model.
- **Fail.** Any of: the relationship cannot be phase-scoped; relationship certainty cannot be read independently of the endpoints' certainties; the designated geometry cannot be resolved without an application-side join written for this query. Requires a §6 discrepancy record.

---

## 5. Worked example — QR-401

```
QR-401        Corroboration and single-witness assertions, with transmission route
Question:     "How do archaeological, historical and spatial sources complement,
              contradict or refine one another in reconstructing the frontier?"
              — RQ4, subordinate 1
Entry status: Draft
Prediction recorded: 2026-07-23
```

**1. Expected analytical result**

*Purpose.* To separate what the corpus knows on one witness from what it knows on several, and to expose the transmission route of each. It is the query behind any statement of the form "the sources agree that…", and it is the one that tells a reader when that phrase is doing work and when it is resting on a single passage.

*Answer shape.* One row per assertion: assertion identifier and proposition; count of supporting attestations; the distinct sources, each with its provenance category and evidential confidence; and a flag for whether the supporting attestations reach their sources by distinct transmission routes or share one. Ordered by attestation count descending. **An empty supporting set means the assertion is unsupported and is an invariant violation (I4), not a finding** — the query must surface these as errors rather than as zero-corroboration rows.

**2. Required inventory**

- **2a Entity types.** None. This query runs entirely in the epistemic layer, which is itself worth recording: it is the test that the epistemic layer stands up without the domain layer, as §5.7's neutrality argument requires.
- **2b Relationship types.** None. The evidential links (`supporting_attestations`, `source`) are structural, not `RelationshipType` vocabulary.
- **2c Assertion roles and designated pointers.** `Assertion` in the general propositional role; no spatial or temporal assertion roles read; no designated pointers resolved.
- **2d Certainty dimensions read.** **Evidential confidence** on each Attestation (§8.2). **None of the five substantive dimensions.** This entry is the register's test that the sixth quantity is retrievable without being conflated with the five.
- **2e Non-graph operations.** Count and distinct-count over supporting attestations; grouping by source; comparison of citation transmission routes.
- **2f Analytical-layer elements.** None.
- **2g Traversal sketch.**

```
Assertion <--[supports]-- Attestation --[source]--> Source        (1:n, n:1)
Attestation --[provenance_category]--> vocabulary term
Attestation --[evidential_confidence]--> 1..5
```

`<--` marks the inverse traversal from assertion to its attestations, which is stored on the attestation side.

**3. Predicted dependency state — category 1, none**

Executable against the corpus as it stands. 254 assertions (currently `ObservationRecord`), 477 attestations, 79 sources, all present; `provenance` and evidential `confidence` populated throughout; rule 8 gives every attestation a non-empty claim, at 0 violations across 477.

*One item deliberately not recorded as a dependency.* The `ObservationRecord` → `Assertion` rename is a migration (M1, step 2). It is **not** a dependency of this entry, because the register is expressed in ontology terms and the corpus's `ObservationRecord` *is* the ontology's Assertion. The rename changes a name, not a capability. This is the clearest illustration of why the expression level was chosen as it was: a register written in schema terms would have recorded a spurious migration dependency here and blocked a query that runs today.

**4. Known limitations**

- **Model limitation.** None identified.
- **Record limitation.** Two, both measured. **208 of 477 attestations (43.6%) support no assertion** and are invisible to this query until the I3 back-fill at migration step 5 — so the corroboration counts it returns are lower bounds, not counts. And **only 32 of 254 assertions (12.6%) have more than one supporting attestation**, which is a fact about Phase-2 extraction composition rather than about the sources: the corpus is dominated by the single route *Eger reports that al-Balādhurī says X*. Both figures should rise sharply as Phase 3 extracts primaries directly, which is the prospective argument at conceptual ontology §5.4.
- **Scholarship limitation.** **"Independent" is a scholarly judgement the query cannot make.** Al-Iṣṭakhrī and Ibn Ḥawqal are not independent witnesses; nor are two chronicles drawing on a common lost source. The query can report distinct sources and distinct transmission routes; it cannot report evidential independence, and any use of its output must not silently promote the first into the second. A further step precedes independence and was confirmed by the calibration run of 2026-07-23: **multiple attestations are not necessarily distinct sources.** Of the 32 assertions with more than one supporting attestation, 3 draw those attestations from a single source (OBS-0057, OBS-0103, OBS-0253), so genuine multi-source corroboration is **29 of 254 (11.4%)**, not 32. A consumer must reduce a supporting-attestation count to its distinct sources before reading it as corroboration, and to independent witnesses before reading it as agreement — two reductions, not one. The thinner baseline **strengthens** conceptual ontology §5.4's prospective argument rather than weakening it: the lower the present multi-source figure, the more headroom direct primary extraction in Phase 3 has to close, and the argument was always that the 12.6% reflects Phase-2 transmission composition rather than the sources themselves.

  *Field-4 amendment, 2026-07-23, authorised following the calibration run. Field 3 (the prediction) is unchanged, per §7.2 Rule 1.*

**5. Acceptance criteria**

- **Pass.** The store returns, for every assertion, its supporting attestations with each attestation's source, provenance category and evidential confidence; distinguishes single-witness from multiply-attested; and reports the transmission route from each attestation's citation — with no transformation step, and without evidential confidence being aggregated with or coerced into any of the five substantive dimensions.
- **Partial.** As above but unable to compare transmission routes, since that reads citation prose. Attributable to a record limitation (citations are free text), not to the model.
- **Fail.** Any of: evidential confidence is not retrievable separately from the five dimensions; the attestation-to-assertion link cannot be traversed in the inverse direction without a purpose-built join; assertions with zero support are returned as ordinary rows rather than raised as I4 violations.

---

## 6. Worked example — QR-503

```
QR-503        Evidence and investigation coverage by analytical region      [derived entry]
Question:     "How does holding provenance and competing interpretations as first-class
              data change what can be asked of the evidence, compared with a database
              that stores only resolved conclusions?"  — RQ5, subordinate 3
              Register query: How does evidence and investigation coverage vary between
              analytical regions?
Entry status: Draft
Prediction recorded: 2026-07-23
```

**1. Expected analytical result**

*Purpose.* To make the corpus's own evidential geography visible: which parts of the frontier are densely investigated and which are known only from texts, and how far an apparent regional contrast is a fact about the frontier rather than about where archaeologists have worked. It is the query that must be run *before* any comparative claim between regions, and it is the answer to "compared with a database that stores only resolved conclusions" — a database of conclusions cannot ask it at all.

*Answer shape.* One row per analytical region: member count; number and proportion of members carrying at least one investigation event, broken down by investigation type; number carrying at least one attestation, by provenance category; mean attestations per member; number carrying a designated geometry. **A low investigation count means the region is under-investigated, not under-occupied**, and the answer shape must carry that distinction in its labels, since the whole point of the query is that the two are routinely confused.

**2. Required inventory**

- **2a Entity types.** `Site`; `LandscapeFeature`; `Event` constrained to `category: investigation`.
- **2b Relationship types.** `examined` (Event → Site | LandscapeFeature), traversed in both directions — forward to count what a region's members were examined by, inverse to establish which members were never examined at all.
- **2c Assertion roles and designated pointers.** Designated spatial assertion of each member — **designated only** — used solely for intensional region membership. Assertion in the general propositional role, for the attestation counts.
- **2d Certainty dimensions read.** None of the five. **Evidential confidence** on attestations, for the mean-confidence column. `detection_scope` on the investigation event is read as an attribute, not as a certainty.
- **2e Non-graph operations.** Aggregation and proportion by region; **set difference** (members minus examined members) — the operation on which the entire absence/evidence distinction rests; grouping by investigation type and provenance category.
- **2f Analytical-layer elements.** `AnalyticalRegion`, with membership specification in all three modes (extensional, intensional, hybrid). **L2 check:** the query reads from region to members. No domain record refers to a region; membership is resolved analytical-side. An implementation that satisfies this query by storing a region identifier on a Site violates L2 and fails the entry regardless of the result it returns.
- **2g Traversal sketch.**

```
AnalyticalRegion --[members]--> {Site | LandscapeFeature}                    (1:n)
  extensional: explicit list
  intensional: member --[designated_spatial]--> geometry ⊆ region boundary
Event{category: investigation} --[examined]--> {Site | LandscapeFeature}     (n:m)
Event --[detection_scope]--> vocabulary terms
member <--[subject]-- Attestation --[source]--> Source                       (1:n, n:1)
NEVER-EXAMINED := members ∖ (members reachable by inverse [examined])
```

**3. Predicted dependency state — categories 2, 3 and 4**

| Item | Cat | Clears at |
|---|---|---|
| `investigation` EventCategory | **2** | §5.5 Board decision; filed 2026-07-23 |
| `site_visit`, `survey`, `excavation`, `remote_sensing_survey` sub-categories | **2** | §5.5 Board decision; filed 2026-07-23 |
| `examined` relationship term | **2** | §5.5 Board decision; filed 2026-07-23 |
| `material_reexamination` sub-category | **2** | **Held** — 2 verified cases, below the three-case threshold. Clears when a third case arises |
| `geophysical_survey` sub-category | **2** | **Held** — 1 verified case. Clears when two further cases arise |
| `AnalyticalRegion` type does not exist | **3** | Migration step 9 (net-new construction) |
| `Site` / `LandscapeFeature` types do not exist | **3** | Migration step 3 (place pass) |
| Designated spatial assertions do not exist | **3** | Migration step 3 (M5 geometry restructuring) |
| Investigation Event *instances* do not exist | **3** | Migration step 9; ≥19 site visits, ≥9 excavations and ≥10 surveys are already identifiable in the corpus and would be minted from existing attestations |
| `detection_scope` values not extracted for existing examinations | **4** | Extraction pass; the attribute must be populated per examination, and it cannot be inferred |
| Investigation coverage outside Eger's gazetteer | **4** | Phase 3. Investigation events are currently recoverable almost entirely from one secondary work |

**Two of these are held rather than pending**, and the distinction matters for scheduling: a pending term clears at a Board meeting; a held term clears only when evidence accumulates, and may not clear at all. Recording both as "category 2" without the distinction would misrepresent the timeline.

**4. Known limitations**

- **Model limitation.** **None identified — and this is the point of the entry.** Every element the query needs is specified in the frozen ontology: AnalyticalRegion with three membership modes (§7.1), investigation as an Event category (§14), `examined` as a relationship, `detection_scope` as an attribute, and the L2 one-way rule which the query respects. The ontology can express this query today, on paper, in full. **What blocks it is entirely work not yet done, not capability not present.**
- **Record limitation.** Investigation events must be created before they can be counted, and the corpus's investigation coverage is itself skewed: nearly all recoverable investigations come through a single secondary work, so a coverage map built now would measure Eger's fieldwork and reading rather than the discipline's.
- **Scholarship limitation.** The **irreducible residual at conceptual ontology §10.14**: a site examined with adequate scope where material *was* found but no assertion was ever entered is indistinguishable, in this query's output, from a site examined and empty. No ontology can close this; it is a completeness property of the corpus. Any use of this query's output states its own coverage rather than assuming it — the same discipline §10.8 requires of spatial analysis.

**5. Acceptance criteria**

- **Pass.** The store returns one row per region with all columns at §1, resolving membership in all three modes, computing the set difference for never-examined members, and grouping by investigation type and provenance — with no transformation step, and **without any domain record holding a reference to a region**.
- **Partial.** As above but reporting only attestation coverage and not investigation coverage, since investigation events have not been created. **Attributable to a category-3 dependency, not to a limitation** — and therefore *not* a partial pass of the model but a blocked entry, which is the distinction §3.5 draws. Recorded as **Blocked**, not as **Partial**.
- **Fail.** Any of: region membership cannot be resolved intensionally against designated geometries; the set difference requires materialising a domain-side region reference (L2 violation); `detection_scope` cannot be read as a filter, so that examinations of any scope count toward coverage of every material class.

**Note on how this entry reads.** Every dependency above resolves to a dated route. Nothing in it is an ontology failure, and the format is arranged so that a reader reaches that conclusion from the structure rather than from a defensive paragraph: field 4 says *none identified* under model limitation, and field 3 lists eleven items each with a clearing event. **A blocked query and a defective ontology look different on the page**, which is what the brief asked the format to demonstrate.

---

## 7. Discrepancy handling — when a query fails for an unrecorded reason

### 7.1 The problem this procedure exists to solve

An entry fails for a reason not in its recorded dependency list. Four things could be true, and they are not equally cheap:

| | What happened | Cost |
|---|---|---|
| **(i)** | **Prediction error** — the dependency existed and was missed | Cheap. Amend the register. |
| **(ii)** | **New dependency** — something arose after the prediction was recorded | Cheap. Date it. |
| **(iii)** | **Logical-model defect** — the ontology expresses it; the model does not | Expensive. The model changes. |
| **(iv)** | **Ontology defect** — the frozen specification cannot express what it promised | Most expensive. Candidate demonstrated defect under §5.8; the only route to reopening a frozen document. |

**The diagnosis is made under pressure, by whoever is trying to ship the logical model, and (i) is the cheapest answer available.** Left to adjudication at failure time, an unpredicted failure will be classified as a forgotten dependency far more often than it should be, because that classification costs nothing and closes the ticket. This is the same asymmetry that let rules 8 and 9(b) accumulate breaches: not dishonesty, but the path of least resistance running in a consistent direction.

### 7.2 The procedure

**A discrepancy is a record, not a judgement.** When an entry fails for a cause not in its dependency list, a discrepancy record is opened — `QR-503-D1`, and so on — carrying:

- the entry's **recorded prediction, quoted, unaltered**;
- the **actual failure**, stated as the specific element or operation that could not be expressed;
- the **unlisted cause**;
- the **proposed classification** among (i)–(iv), with its evidence.

Three rules give the record its force.

**Rule 1 — the prediction is immutable.** Once an entry is Approved, field 3 may not be edited. Corrections are appended as dated amendments below the original, which remains visible. An entry whose prediction has been silently rewritten is worthless as a prospective record, and the only way to guarantee it has not been is to make editing structurally impossible rather than merely discouraged.

**Rule 2 — a discrepancy is not closed by amending the prediction.** It is closed by classifying the cause. Amending the register is what happens *after* a classification of (i), not instead of one.

**Rule 3 — the burden falls on the cheap answers.** This is the load-bearing rule. **Classifications (i) and (ii) must be positively established; (iii) and (iv) are the residual.**

- **(i) requires** showing that the unlisted item was a dependency *at the time of prediction* — that it was missing then, and that its absence alone accounts for the failure. Not that it is missing now, which is compatible with (iii) and (iv).
- **(ii) requires** a dated change to the corpus, governance state or vocabulary between prediction and execution.
- Where neither is established, the discrepancy **escalates by default to (iii)**, and to (iv) if the model's author can show that no implementation of the frozen ontology could express the entry.

This inverts the pressure. Under the default rule, "we must have missed a dependency" is not available as a shrug; it is a claim requiring evidence about a past state, which is precisely what the immutable prediction preserves. The expensive answers become the ones you get by *failing to do work*, rather than the ones you get by doing it.

### 7.3 The register's own accuracy is tracked

A running tally, updated whenever a discrepancy is classified:

| Metric | Why it is kept |
|---|---|
| Predictions upheld / total entries executed | The register's hit rate |
| Discrepancies by classification (i)–(iv) | The shape of the register's failure |
| **Category-1 entries that failed** | The single most diagnostic number |

The last row is the one to watch. A category-1 entry is a prediction that a query runs *today*, against a corpus whose state is known. If several of those fail, the register is not measuring the logical model — it is measuring its own authors' understanding of the corpus, and the acceptance test is compromised at its foundation. **Fewer than three category-1 entries are expected across all twenty-two**, so the denominator is small and any failure in it is worth a stop-and-look rather than a ticket.

### 7.4 What a discrepancy is not

A discrepancy is not a fault in the entry's author, and the procedure should not be operated as though it were — a register whose authors are penalised for discrepancies will acquire vague predictions, which defeats §3.4 and with it the whole prospective method. The useful posture is that a discrepancy is **information about the boundary between what the ontology promised and what it can do**, which is the thing the register was written to find out. Classification (iv), in particular, is a success of the method: it is the register doing the one job that justifies writing it before the logical model rather than after.

---

## 8. What phase 2 would commission

On approval of this format: the remaining **nineteen** entries, one per subordinate question — RQ1 ×3 further, RQ2 ×5, RQ3 ×5, RQ4 ×3 further, RQ5 ×3 further — plus any derived entries the questions require.

Two things worth settling with the format rather than during it:

- **How many entries are expected to be category 1.** My estimate is two or three, all in RQ4, since the epistemic layer is the only part of the ontology already implemented. If phase 2 returns many more, the predictions are probably optimistic; if it returns none, RQ4's methodological claim that the corpus already embodies the attestation-provenance model is weaker than the frozen document asserts.
- **Whether entries are approved individually or as a set.** I would recommend as a set, per RQ, since the dependency predictions are correlated — most of RQ1 and RQ2 will block on the same migration step 3, and reviewing them together makes an omitted dependency in one visible against its neighbours.

---

*End of phase-1 format specification. Read-only: no logical model, no schema, no records.*

---

# Addendum — §3.4.1 Execution route (2026-07-23)

## The question answered directly

*Does the dependency classification distinguish "blocked for analysis" from "blocked for acceptance testing"?*

**No. It does not, and it was not built to.** The four categories at §3.4 classify an entry by what stands between it and a **historical answer**. That is the right axis for planning extraction and migration, and the wrong axis for scheduling acceptance testing — which asks only whether the logical model can *express* the query, a question a synthetic fixture can answer without the corpus holding a single real instance.

Reporting "four of twenty-two entries are executable" was therefore accurate about analysis and misleading about acceptance testing. The two are independent, and the format needs a second axis rather than a reinterpretation of the first.

## §3.4.1 Execution route

Each entry carries an **execution route**, orthogonal to its dependency set:

| Route | Meaning | Which entries |
|---|---|---|
| **Corpus-executable** | Runs against the live corpus now. Yields a historical answer *and* an acceptance-test result. | Category-1 entries |
| **Fixture-executable** | Acceptance-testable now against a synthetic fixture; analysis-blocked until dependencies clear. | Every entry whose ontology elements exist — categories 2, 3 and 4, with category-2 terms admitted **provisionally** |
| **Not testable** | Neither corpus nor fixture can supply the case, because no ontology element expresses it. | Classification (iv) findings, until amended |

Three rules follow.

**The fixture is the intended execution path for categories 3 and 4.** A category-3 entry is blocked because a type does not yet exist *in the corpus*; the fixture instantiates it. A category-4 entry is blocked because evidence has not been extracted; the fixture supplies synthetic evidence of the right shape. Neither blocks the acceptance test, and treating them as though they did would defer validation of the logical model until after the migration it is supposed to de-risk. Governance §5.9 makes this the required sequence.

**Category-2 entries execute with provisional vocabulary.** A term filed under §5.5 and awaiting decision enters the fixture marked provisional. The acceptance criterion is structural expressibility, and whether the Board settles on `controls` or some other name does not bear on whether the model can hold a relationship of that shape. Provisional terms carry no force outside the fixture.

**"Not testable" is the diagnostic route.** An entry that neither the corpus nor a fixture can execute is not a scheduling problem; it is a statement that the ontology lacks an element. It is the same finding §3.3.1 records at authoring time, seen from the execution side, and the two should agree — an entry recorded as a §3.3.1 capability finding must route to *Not testable*, and one that routes to *Not testable* without a §3.3.1 finding indicates the authoring review missed something.

## Restated register position

| Route | Count | Entries |
|---|---|---|
| Corpus-executable | **4** | QR-401, QR-402, QR-441, QR-544 |
| Fixture-executable | **18** | all others, following ontology Amendment 1 |
| Not testable | **0** | was 1 — QR-305, until Amendment 1 supplied `interaction_mechanism` |

**Twenty-two of twenty-two entries are now acceptance-testable, of which four are also corpus-executable.** That is a materially different and better position than §8.1 of phase 2 reported, and the difference is entirely the second axis rather than any change to the entries.

QR-305 is the worked demonstration of why the third route exists. Before Amendment 1 it was not fixture-executable: no fixture could be built, because there was no element to instantiate. That is exactly the distinction between an entry blocked by work not yet done and an entry blocked by capability not present — the distinction §10.14's revision turned on, now made structural in the register itself.

## Phase-2 entries: route assignments

Corpus-executable: QR-401, QR-402, QR-441, QR-544.
Fixture-executable: QR-101, QR-102, QR-103, QR-104, QR-201, QR-202, QR-203, QR-204, QR-205, QR-301, QR-302, QR-303, QR-304, QR-305, QR-403, QR-404, QR-501, QR-502, QR-503, QR-504.

No entry routes to *Not testable*.
