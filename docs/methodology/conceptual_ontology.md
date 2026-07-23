# Conceptual Ontology — Byzantine-Islamic Frontier Database

**Version 0.2 — stable specification.** Written to be frozen as the input to logical modelling.
**Design input:** `docs/research_questions.md`, treated as a frozen contract.
**Supersedes:** v0.1 (2026-07-23), which was a scoping pass. This document is self-contained; v0.1 need not be read alongside it.
**Corpus state:** `origin/main`, 1,453 records, verified against a fresh clone on 2026-07-23.
**Status of this pass:** read-only. No patches, no schema files, no record changes.
**Status: Frozen 2026-07-23** under governance §5.8, following completion of the Rule 14 and Rule 15 ratification and the governance audit. No substantive changes from Version 0.2. *This line records a lifecycle status transition, not a content revision.*

---

## 0. Status, ratification register, and what changed from v0.1

### 0.1 What this document is

v0.1 tested a design against the corpus and returned a set of policy questions. Those questions have been adjudicated. This document states the resulting specification in stable form: every decision is settled or explicitly deferred with a stated resolving condition, every rule proposed for ratification is given in full text rather than by reference, and the two acknowledged limitations are retained and honestly stated.

Nothing here is an open proposal except where marked **DEFERRED**, and each deferral carries the condition that would resolve it (§19).

### 0.2 Ratification register

Three rules are entered into the record, with their provenance distinguished. The distinction is not pedantry: quietly widening a rule's scope without an audit trail is the failure mode the Ṭaranda correction exists to prevent, and a rule set that cannot say which of its members were recovered and which were newly made cannot be audited at all.

| Rule | Status | Provenance | Text |
|---|---|---|---|
| **9** | **RECOVERED** | Pre-existing rule, undocumented in the repository, recovered from Curtis's records 2026-07-23. Reconstruction from usage in v0.1 confirmed correct. | An InterpretationRecord's `supporting_evidence` cites Attestations, never raw Sources. |
| **10** | **RECOVERED** | Pre-existing rule, undocumented in the repository, recovered from Curtis's records 2026-07-23. | Related and competing interpretations are explicitly cross-referenced. |
| **11** | **RATIFIED — NOT RECOVERED** | The archived wording was phase-specific to the Eger extraction ("Section-4 personal observations use `primary_observation` + `observation_date` at `schema_version` 2.0.0"). The general form below is a **new rule ratified 2026-07-23**, superseding the phase-specific form. | An author's own direct observations are represented as `primary_observation` carrying an `observation_date`. |
| **14** | Proposed for ratification | New, this pass. Full text at §15.1. | Site displacement threshold. |
| **15** | Proposed for ratification | New, this pass. Full text at §15.2. | Dual aspect — feature and site. |

All five belong in `docs/editorial_workflow.md` alongside rules 1–13, not in this document. They are extraction and editorial discipline, not data model. §15 gives 14 and 15 in full so they can be approved or redlined as text; 9, 10 and 11 are given above in the form Curtis supplied.

**Compliance scans, run because the recovered rules can now be enforced.** These are the first measurements of a rule set that until 2026-07-23 could not be checked, and the pattern is the same one Item G found for rule 8: a silent convention with a systematic, invisible breach.

- **Rule 9.** Of 174 interpretations, **zero** cite non-attestation evidence — the ATT-only half is fully compliant. But **57 (33%) carry an empty `supporting_evidence`**, breaching the requirement that an interpretation rest on attested support. This is the exact shape of the rule-8 finding: a convention observed in what it forbids and neglected in what it requires, invisible because nothing enforced it.
- **Rule 10.** **Zero** relationships have an interpretation as an endpoint. **29 interpretations name another interpretation in prose.** So rule-10 compliance today is 100% textual and 0% structural — the cross-referencing is being done, but as text rather than as data.
- **Rule 11 (general form).** 19 attestations carry `provenance: primary_observation`; **all 19 carry an `observation_date`**, and no attestation carries an `observation_date` without that provenance. Compliance is total and the back-fill is empty. All 19 cite one source, `SRC-0065` — which is precisely why the archived wording was Eger-specific, and precisely why ratifying the general form is a forward-looking act with no retrospective effect.

### 0.3 What changed from v0.1

| v0.1 | v0.2 |
|---|---|
| Rename Observation → Assertion proposed | **Settled: approved.** §5.1, §5.4 |
| Assertion layer argued from under-population | **Argument replaced** with the prospective case; §5.4 |
| Person retention flagged as a reading of design note (b) | **Settled: confirmed as consistent application of the admission test**; §4.10 |
| AnalyticalRegion temporal window recommended | **Settled**, with null-window semantics and the intersection rule specified; §7 |
| `PlaceType` finding buried in §2 | **Promoted to §1**; the net-simplifying result stated plainly |
| Dossier unbundling proposed as a design requirement | **Reframed as a correction** — rule 10 already required it; §5.5 |
| Competing phase schemes "matters most for excavated sites, a minority" | **Timeline revised**: expected to bind during Phase 3; §10.13 |
| `overall_confidence` left open | **Resolved: retire, in the schema-migration pass**; §8.3 |
| Rules 14, 15 by cross-reference | **Full text given**; §15 |
| Designation versioning unaddressed | **New: Policy B-2**; §13 |
| Examination-as-Event unaddressed; §10.14 a flat gap | **New: L1 check cleared, limitation narrowed**; §14, §10.14 |
| Six independent migration estimates | **New: consolidated assessment with interaction analysis and sequencing**; §17 |

---

## 1. The proposal at a glance

### 1.1 The ontology is net-simplifying

This is the result worth stating first, because it is the opposite of what a design pass of this kind usually produces.

The proposal adds **three record types** — Component, Phase, AnalyticalRegion — and splits one existing type four ways on four distinct identity criteria. Against that, it **removes more classificatory apparatus than it introduces**:

- The current `PlaceType` enum carries **27 terms conflating five incompatible bases of classification**: kind, administrative rank, modern condition, historical event-association, and jurisdiction. Rationalising it does not redistribute 27 terms among the new types.
- **Five terms are retired outright as category errors**, not recategorised: `city`, `village` and `capital_city` classify by rank, which is time-varying and belongs on a phase; `ruined_site` classifies by modern condition, which is a property of the latest phase; `battle_site` classifies a place by an event that happened there, which is a relationship.
- **One term is retired as irreducibly ambiguous**: `region`, which the corpus uses for physiography (12 records), jurisdiction (3 records) and, arguably, researcher selection.
- **Four terms collapse into one**: `fortification`, `fortress`, `castle` and `kastron` are one kind under four labels.
- **One field required on 325 records is retired**: `overall_confidence`, which either restates one certainty dimension or aggregates quantities principle 6 says are independent (§8.3).
- **Fourteen candidate types were considered and rejected** (§18.2), including several the author wanted to add.

The residue is four spatial types, each with **one** identity criterion and a small vocabulary with **one** basis of classification. A cataloguer asking "what type is this?" currently has to decide between answers drawn from five different questions; afterwards there is one question.

**This is the strongest single argument for the design.** An ontology that answers more research questions while carrying less classificatory apparatus is not trading complexity for capability; the capability was being blocked by the apparatus.

### 1.2 Domain layer — what existed

| Type | What it represents | Identity criterion | Temporal scope | RQ |
|---|---|---|---|---|
| **SpatialThing** *(abstract)* | supertype; holds no records | — | — | principle 7 |
| **Site** | a bounded locus of human occupation or use | physical continuity of the occupied locus | persistent; existence interval derived from phases | RQ1, RQ2, RQ3 |
| **LandscapeFeature** | an extended element of terrain conditioning movement, settlement or production | continuity of physical form and the affordance it provides | persistent; usually unbounded | RQ1, RQ3 |
| **Route** | a corridor of movement between termini | continuity of corridor under the same constraints — *not* track geometry | persistent; phased | RQ1 |
| **TerritorialUnit** | a jurisdiction: thughūr, ʿawāṣim, jund, kura, theme | unbroken chain of administrative succession | persistent, bounded | RQ2, RQ3 |
| **Component** | a constituent part of a Site | continuity of physical fabric within its parent Site | dependent; persistent within parent | RQ2 |
| **Phase** | a dated state of a persistent thing | (subject, designated interval, defining state) | inherently interval-shaped | RQ2, RQ3 |
| **Event** | a bounded historical happening, including acts of examination | same kind + overlapping time + same place(s) + same principal participants | inherently interval-shaped | RQ3, RQ4 |
| **Polity** | a corporate political actor | continuity of political succession as recognised by the sources | persistent, bounded | RQ3 |
| **Person** | a named historical individual | prosopographic identity | persistent, bounded | RQ3, RQ4 |

### 1.3 Epistemic layer — what is known and argued

| Type | What it represents | Identity criterion | RQ |
|---|---|---|---|
| **Source** | a work that generates evidence | the work, distinct from edition and witness | RQ4 |
| **Attestation** | one source's statement of a datum, with provenance | (source, location-in-source, datum) | RQ4 |
| **Assertion** | the deduplicated proposition several attestations may share | (proposition, subject set) | RQ4 |
| **Interpretation** | one scholar's argued reading of one or more attestations | (scholar, publication, argument) | RQ4 |

Geometry and dating are **not types**. They are typed roles of Assertion (§5.6), each subject holding a designated pointer to one. This is the decision that does the most structural work in the specification, and §13 gives its versioning consequences.

### 1.4 Structural and analytical layers

| Type | What it represents | Identity criterion | RQ |
|---|---|---|---|
| **Relationship** | a connection between two records, with its own metadata | (type, source, target, temporal scope) | RQ1, RQ2, RQ5 |
| **AnalyticalRegion** | a researcher-defined selection over the domain | (author, name, version, membership specification) | RQ5 |

---

## 2. The type-admission test

Principle 1 requires each type to earn a research question; principle 8 requires difference in kind to be carried by attributes rather than new types. Together these say when a type is *unjustified*, not when a candidate that does serve a question should nevertheless be an attribute. The corpus needs the sharper form, because most proliferation pressure in a gazetteer comes from types that *can* cite a question.

> **THE ADMISSION TEST. A candidate becomes a type only if it has a different identity criterion or a different lifecycle from every existing type, *and* it enables a query named in the contract. If it shares an identity criterion with an existing type and differs only in label, function, condition, rank or dimension, it is a vocabulary term or a phase-borne attribute.**

### 2.1 The `PlaceType` finding

Applied to the existing schema, the test does more work than it does applied to any candidate. Scanning all 190 place records, the 27-term `PlaceType` enum classifies on five incompatible bases at once:

| Basis | Terms | Verdict |
|---|---|---|
| **Kind** — what the thing is | `settlement`, `fortification`, `monastery`, `river`, `pass`, `mountain`, `harbour`, `bridge`, `natural_feature` | Legitimate, but belongs to four different types once identity criteria are separated |
| **Administrative rank** — a time-varying status | `city`, `village`, `capital_city` | **Retire.** Constantinople is not a different *kind* from a village; rank is a phase-borne attribute, and the schema already has `administrative_status_history` for it (used once) |
| **Modern condition** | `ruined_site` (4 records) | **Retire.** Ruination is a state of the latest phase |
| **Event association** | `battle_site` (1 record: `ENT-PLC-0002`, Anzen/Dazimon) | **Retire.** Types a place by something that happened there. Becomes a Site or LandscapeFeature with an Event related `located_at` |
| **Jurisdiction, conflated with physiography** | `region` (15), `administrative_unit` (7), `theme`, `frontier_zone` (4), `kura`, `jund` | **Split.** `region` covers the Cilician Plain and Ṭūr ʿAbdīn (physiographic → LandscapeFeature) *and* Cappadocia, Jazīra and Armenia (jurisdictional → TerritorialUnit). Two identity criteria under one term |

Two further observations from the same scan:

- **`fortification` (17), `fortress` (13), `castle` (4) and `kastron`** are one kind under four labels — exactly the proliferation principle 8 forbids, already present in the schema.
- **All five Polity records** (`ENT-POL-0001`–`0005`, including the Byzantine Empire) are stored as `record_type: place` with `place_type: administrative_unit`. The identifier prefix has been carrying the real semantics while the schema has not.

The corollary is the point of §1.1: `city`, `village`, `capital_city`, `ruined_site` and `battle_site` should not become five types — they should stop being types. **Anti-proliferation is not only a rule for adding types; applied to the current schema it removes five and consolidates four more.**

---

## 3. Three layers, and the reference rules

**Domain layer.** What existed in the world: sites, features, routes, jurisdictions, components, phases, events, polities, persons. These records are stable and are not made uncertain by disagreement about them.

**Epistemic layer.** What is known and argued: sources, attestations, assertions, interpretations. All uncertainty about the world lives here, or in the designated-assertion pointers the domain layer holds into it.

**Analytical layer.** What a researcher has selected for a study. Nothing here is a historical thing.

### 3.1 The reference rules, restated precisely

v0.1 stated these loosely enough that they appeared to forbid a traversal they in fact permit (§14). The restatement is the substantive correction:

> **L1 — Referential dependency, not query direction.** A domain record's fields may name epistemic records in exactly two forms: **designated-assertion pointers** and **evidential back-links** (`linked_attestations`, `linked_interpretations`, and their successors). Epistemic records may name domain records freely.
>
> **L1 constrains what a record may store, not which direction a query may traverse.** Inverse traversal of any permitted reference is unrestricted, because an inverse is an index, not a dependency.
>
> **L2 — The analytical layer may reference the domain and epistemic layers; neither may ever reference the analytical layer.**

L1's second paragraph is new in v0.2 and it matters: without it, the rule reads as a constraint on querying, which would forbid ordinary and necessary operations (§14.2). What L1 actually prevents is a domain record acquiring epistemic *dependencies* — a Site whose definition presupposes a particular reading of a particular source — which is principle 4 enforced structurally.

L2 is the formal content of the domain/analytical distinction. It makes "sectors are researcher-defined groupings, not divisions of the domain" a property a validator can check. The error it prevents is the plausible one, where a study area quietly acquires attestations and starts behaving like a historical region.

**The worked distinction.** The **ʿAwāṣim is a TerritorialUnit**, not an AnalyticalRegion: a domain object created by an identifiable administrative act that RQ3 names, attested in the sources, held by a polity, with a dissolution. **"The northeast Anatolian corridor" is an AnalyticalRegion**: a selection made for a dissertation, with no historical existence and no attestations. The corpus's four `frontier_zone` records are all of the first kind.

---

## 4. The domain layer

### 4.1 SpatialThing — the abstract supertype

Not a record type. An abstract supertype over Site, LandscapeFeature, Route and TerritorialUnit, carrying the spatial primitives principle 7 requires all spatial things to share: attested names, geometry assertions, phases, spatial certainty, and eligibility as an endpoint of spatial relationships.

**Why a supertype rather than one type with a category attribute.** The four concrete types fail the shared-identity half of the admission test: a Site's identity rests on continuity of an occupied locus; a LandscapeFeature's on continuity of form and affordance; a Route's identity explicitly *survives* geometric change, since the contract asks for corridors that persist as tracks shift; a TerritorialUnit's rests on an unbroken chain of authority and survives wholesale boundary replacement. Four answers to "when are these the same thing?" is four types. What they share is spatial *structure*, which the supertype carries — which is what principle 7 asks for when it says spatial things share primitives and differ in category.

**Waterbodies are not a fifth type.** Principle 7's list names them and the corpus has 16 rivers, but a river's identity criterion is continuity of the drainage line — the LandscapeFeature criterion. `river`, `lake`, `spring`, `marsh` and `canal` are vocabulary terms. Principle 7's list is a list of examples, not a mandated register.

---

### 4.2 Site

**What it is.** A bounded locus of human occupation or use: settlement, fortress, monastery, tell, quarry complex, free-standing cemetery. 132 of the 190 current place records (§17.4).

**Identity criterion — physical continuity of the occupied locus.** Two records denote the same Site if and only if there is an unbroken chain of physical and topographic continuity of the occupied place, irrespective of function, name, ruling polity, or gaps in occupation.

Three consequences, each disposing of an edge case:

1. **Identity is not nominal.** Sozopetra, Zibaṭra and Doğanşehir are one Site with three attested names. A toponym applied to two locations produces two Sites, each carrying the name.
2. **Identity is not functional.** A monastery that becomes a fortress is one Site with two phases. Function lives on Phase, never on the Site.
3. **Identity survives abandonment.** A gap in occupation is a gap between phases. A site abandoned in 730 and reoccupied in 780 is one Site.

**Displacement.** Governed by **Rule 14**, full text at §15.1. The threshold is scale-relative by construction and specifies no fixed distance.

**Temporal scope.** Persistent. A Site has no dates of its own; its existence interval is *derived* from the union of its phase intervals (invariant I7). Where a source asserts a foundation date directly, that is a dated assertion attached to the Site and must be consistent with the phases or flagged.

**Certainty dimensions.** Identification applies to the Site directly. Spatial applies to its geometry assertions. **Chronological and functional apply to its phases, not to the Site** — principle 4 made structural, so that "we are unsure this is a monastery" cannot be recorded as uncertainty about the site's existence.

**Research questions.** RQ2 throughout; RQ1 (installations controlling passes and crossings); RQ3 (the objects events act upon).

---

### 4.3 LandscapeFeature

**What it is.** An extended element of terrain conditioning movement, settlement or production, and not itself a locus of occupation: passes, valleys, ranges, plains and basins, marshes, fords, springs, and terrain-scale anthropogenic works such as canals.

**Identity criterion — continuity of physical form and of the affordance it provides.** The Cilician Gates are the same pass while the topography and the passage it affords persist. A river is the same river while the drainage line is continuous.

**The boundary with Site is occupation, not origin.** The corpus breaks an origin-based boundary immediately: `ENT-PLC-0045` (Nahr Maslama, the Balis canal) and `ENT-PLC-0097` (Nahr al-Abbāra) are anthropogenic, terrain-scale, and not loci of occupation. They are LandscapeFeatures. The type therefore carries an `origin: natural | modified | anthropogenic` attribute, which is analytically valuable in its own right: a query for anthropogenic landscape features *is* a query for landscape transformation (RQ3).

**Dual aspect.** Where a thing is both feature and locus — a bridge, a fortified pass — governed by **Rule 15**, full text at §15.2.

**Temporal scope.** Persistent and normally unbounded; a pass has no foundation date. Features may carry phases where the evidence records a change of state (a canal cut, silted, recut), but most will have none. This asymmetry with Site is correct: geomorphology and settlement have different temporalities, and it is why Phase is optional rather than mandatory on SpatialThing.

**Certainty dimensions.** Identification and spatial. Functional weakly, and mainly for anthropogenic features. Chronological only where phased.

**Research questions.** RQ1 directly — "How were passes, river crossings and other critical landscape features controlled, monitored and exploited?" is unanswerable without this type. RQ3 for environmental conditioning.

---

### 4.4 Route

**What it is.** A corridor of movement between termini. One type with a class attribute distinguishing **documented**, **modelled**, **inferred** and **family** — mandated verbatim by principle 8.

**Identity criterion — continuity of the corridor between the same termini under the same controlling constraints, explicitly not geometry.** This is the type whose identity criterion departs most sharply from the intuitive one, and the contract requires the departure: RQ1 asks whether "route families that persisted even as specific tracks shifted" can be identified. If identity were geometric, a shifted track would be a new route and the question could not be asked.

Track-level routes relate to their family by a `member_of_route_family` relationship rather than by containment, keeping the family a peer and letting one track belong to two families where corridors braid.

**Why one type and not three.** A documented route and a modelled route differ in how we came to know them, not in what they are — and that difference is provenance, which is the epistemic layer's business. Keeping the comparison inside one type is what makes RQ1's fourth sub-question — how attested routes relate to least-cost predictions — a single query over one type rather than a join across two.

**Temporal scope.** Persistent, phased.

**Certainty dimensions.** All four of identification, chronological, spatial and functional. Routes are where the dimensions least collapse into one another: a route can be securely identified and dated while its geometry is speculative, which is the ordinary condition of a documented itinerary.

**Current state.** One Route record (`ENT-PLC-0011`), modelled as a point with a 200 km uncertainty radius. It is the clearest demonstration that the present spatial model cannot serve RQ1, and it requires rebuilding rather than migration.

---

### 4.5 TerritorialUnit

**What it is.** A jurisdiction: the ʿawāṣim, the thughūr and their Syrian and Jaziran divisions, a jund, a kura, a theme, a kleisoura considered as a command.

**Identity criterion — an unbroken chain of administrative succession.** The same unit while authority passes in a continuous line under a recognised name or office, *irrespective of boundary change*. Genuinely different from any spatial criterion: a jund whose boundaries are wholly redrawn is the same jund.

**Why not a LandscapeFeature or Site.** It is constituted by an act, not by physical persistence. RQ3 asks how "administrative and political reorganisation reshape the frontier's structure", and the ʿawāṣim's creation is the contract's own worked example. A type whose instances are brought into being by datable events, held by polities, and dissolved by decree behaves differently from terrain.

**Temporal scope.** Persistent but bounded: constituted at a date, dissolved at a date, phased in between as boundaries and holders change.

**The interruption rule.** Dissolution and later recreation under the same name produces **two units linked by a `restores` relationship**, unless the sources themselves treat the later body as a restoration, in which case one unit with a gap. This inverts the Site rule, and the inversion is principled: physical continuity persists through a gap because the stones remain, whereas an abolished jurisdiction has no continuant. Flagged as a judgement call not to be made silently at extraction time.

**Certainty dimensions.** Identification, chronological, spatial (boundaries are the least certain geometry in the corpus and will often be absent entirely), and functional in the weak sense of administrative character.

---

### 4.6 Component

**What it is.** A constituent part of a Site: curtain wall, tower, gate, church, mosque, cistern, bath, kiln, workshop, field system, cemetery, quarry. One type with a controlled vocabulary, mandated by principle 8.

**Identity criterion — continuity of physical fabric within its parent Site.** Fabric, not location and not function. This settles the church→mosque case (§12.2): converted fabric is one component with two phases; demolished-and-rebuilt fabric on the same footprint is two components in succession.

**Dependent identity.** A Component cannot exist without its parent Site; under a split, components follow the fabric. This dependency is what makes Component a type rather than a Site with a `part_of` relationship: Site identity is independent, Component identity is not, and the difference determines behaviour under the merge and split operations governance §5.3 requires to be defined.

**Independent chronology.** Component phases are independent of Site phases and of each other (invariant I6). RQ2 asks for "components... with independent chronologies", and the invariant makes the independence explicit rather than incidental.

**Certainty dimensions.** All five in principle; functional is the one that matters and the one the type exists to carry. The contract's paradigm case — a structure whose existence is certain and whose reading as monastery, palace or caravanserai is disputed — is a Component with competing interpretations attached and the entity untouched.

**Current state.** No component records exist. Entirely new construction, not migration.

---

### 4.7 Phase

**What it is.** A dated state of a persistent thing. Phase is the mechanism by which principle 2 is satisfied — persistent identity with change carried elsewhere.

**One Phase type, not four.** A site phase, component phase, route phase and territorial-unit phase have the same structure and the same identity criterion, differing only in the type of their subject. Principle 3 states the general form when it says "*no entity* possesses a single geometry or a single date by default".

**Identity criterion — (subject, designated interval, defining state).** Dependent, like Component's.

**What a Phase carries, and what it does not.** It carries function, occupation regime (`permanent | seasonal | intermittent | unknown`), rank or status, and its evidential links. **It does not carry a date or a geometry directly.** It carries a *designated* temporal assertion and a *designated* spatial assertion, selected from the competing assertions attached to it (§5.6).

**The honest tension.** A phase is partly an interpretive construct: the site really did have a period of fortress use, but where that period begins and ends is a scholarly judgement. Resolution in two parts:

- *Competing dates for an agreed division* are native: competing temporal assertions on one Phase, one designated, the rest retained.
- *Competing divisions* — two scholars carving the same evidence into different numbers of phases — are **not** handled. §10.13 states this as a limitation and revises its expected timing.

**Temporal scope.** Inherently interval-shaped. Phases of one subject are ordered, may be non-contiguous (which is how seasonal and intermittent occupation is represented without special-casing), and, for a Site, may not overlap.

**Certainty dimensions.** Chronological, spatial and functional. **Not identification** — a phase is not identified with anything historical, so the dimension does not apply. A good illustration of principle 6's requirement that the ontology say which dimensions apply where.

**Current state.** No phase records. The fields Phase replaces are near-unused: one place of 190 uses `chronology`, one uses `administrative_status_history`, five use `political_affiliation_history`. The temporal dimension of the spatial corpus is at present essentially unmodelled, and Phase is where the largest share of new analytical capability lives.

---

### 4.8 Event

**What it is.** A bounded historical happening: siege, battle, raid, earthquake, foundation, administrative reform, reoccupation, abandonment — **and acts of examination: excavation, survey, site visit, material re-examination** (§14). One type with the existing two-level category/sub-category vocabulary, mandated by principle 8 and already implemented.

**Identity criterion — same kind, overlapping time, same place(s), same principal participants.** The specification's worked example (§4.5, the Caesarea raid) already states this and carries forward unchanged.

**First-class, and why.** An Event is a thing that happened; an Assertion is a claim about the world. Making the 838 campaign a kind of claim would mean the campaign exists only as the sum of statements about it — the ontology/epistemology collapse principle 4 forbids — and the collapse would propagate: if events are claims, then sites attested only textually are claims too, and the domain layer dissolves into its evidence. §12.4 develops the argument and treats the residual case of topical or fictitious events.

**Events act on phases.** RQ3 requires links "from events to the phases they produce". This is a relationship family — `produced_phase`, `terminated_phase`, `damaged` — absent from the current enum and the most analytically valuable addition to it (§6.2), because it converts a list of destructions into a queryable model of transformation.

**Examinations are Events.** Argued in full at §14. The short form: an examination has the Event identity criterion exactly — same kind, time, place, participants — so under the admission test it is an Event with vocabulary terms, not a new type and not a subtype.

**Temporal scope.** Inherently interval-shaped, nestable via the existing parent/child structure.

**Certainty dimensions.** Identification (did this happen, and is the event in this source the same one?), chronological, spatial. Functional does not apply. Note the terminological stretch: for events, identification certainty carries the load a sixth "existence" dimension would carry. No sixth dimension is proposed — the dimension does the same work in both cases, measuring how securely a record corresponds to a real historical particular.

---

### 4.9 Polity

**What it is.** A corporate political actor: the Byzantine Empire, the Abbasid and Umayyad Caliphates, the Hamdanid emirate. Five records.

**Identity criterion — continuity of political succession as recognised by the sources.**

**The honest justification, because this is the weakest domain type.** The case for reducing Polity to a controlled vocabulary term is real — "which sites were held by whom in 850" is answerable with a term in a time-bounded attribute. Three things decide it the other way:

1. Polities carry evidence. `ENT-POL-0001` has 24 attestations and 8 interpretations; a vocabulary term cannot.
2. They carry multilingual attested names with their own provenance — Ῥωμανία, Rūm — which is the structure principle 2 gives to entities.
3. TerritorialUnits are *held by* polities, and RQ3's question about the distribution of authority is a query over that relationship. A relationship endpoint must be a record.

Polity earns its place on RQ3 alone and should be watched: if a future pass finds polity records accumulating only structural links and no evidence, the type should be reconsidered.

**Certainty dimensions.** Identification and chronological. **Not spatial** — a polity's extent is the union of the territorial units it holds, derived and never stored, or the two will contradict.

---

### 4.10 Person — retained; Community deferred

**Settled.** Design note (b) defers the human-scale dimension against a recurrent-evidence threshold. Applied consistently, that threshold splits its own list, and the split is the admission test working correctly rather than an exception to it:

- **Named individuals clear the threshold decisively.** Source authorship alone makes them structural — every Source has an author and there are 79 sources — and event participation adds more. 81 existing records carrying attestations is not a threshold case. RQ3's questions about who reorganised what and RQ4's transmission chains both require them.
- **Communities, households and mortuary populations do not clear it.** No such records exist, no recurrent evidence demands them, and no contract question requires them. RQ2's settlement-hierarchy questions are about places, not populations.

So Person is retained as a **minimal actor type justified by authorship and event participation**, and Community, Household and Population stay outside the ontology until recurrent evidence justifies them. §5.7 confirms that admitting them later requires no change to the evidence machinery.

**Identity criterion.** Prosopographic identity, resolved by name, office, floruit and relations, per the specification's existing identity-resolution procedure.

**Certainty dimensions.** Identification and chronological.

---

### 4.11 Types considered and rejected

Recorded so the reasoning survives and a later pass need not re-litigate.

| Candidate | Why rejected |
|---|---|
| **Waterbody** | Shares LandscapeFeature's identity criterion. Vocabulary term. |
| **Fortification / Fortress / Castle / Kastron** | Share Site's identity criterion. One kind under four labels — the proliferation principle 8 forbids, already in the schema. |
| **Settlement / City / Village / CapitalCity** | Administrative rank, not kind. Phase-borne attribute, so that a village becoming a city is representable. |
| **RuinedSite** | Modern condition. A property of the latest phase. |
| **BattleSite** | Types a place by an event that occurred there. Replaced by an Event with a `located_at` relationship. |
| **Region** | Irreducibly ambiguous between physiography (→ LandscapeFeature), jurisdiction (→ TerritorialUnit) and researcher selection (→ AnalyticalRegion). Retiring the term forces the useful question at extraction time. |
| **Geometry** | A statement about where a thing is, therefore epistemic. A typed role of Assertion (§5.6). |
| **DatingAssertion** | Same. A typed role of Assertion. |
| **AnalyticalWindow** | **Shares AnalyticalRegion's identity criterion** — a researcher-defined selection — and differs only by which dimension it selects on. Under the admission test, difference by one dimension is an attribute, not a type. Becomes AnalyticalRegion's optional temporal extent (§7.3). A further worked application of the test, and a useful one because the temptation to pair a spatial type with a temporal twin is strong. |
| **ExaminationEvent** | Shares Event's identity criterion exactly. Vocabulary terms under a new `investigation` category (§14). A subtype here would violate principle 8 and reintroduce the proliferation §2 removes. |
| **Community / Household / Population** | Deferred per §4.10; no recurrent evidence, no contract question. |
| **Institution** | The specification's §2.1 list mentions institutions. No record exists, no research question requires them, and monasteries as *places* are Sites. Deferred. |
| **Correction / Retraction** | Handled by an Interpretation plus a supersession relationship plus workflow state (§10.12). A type would add nothing. |
| **Dossier** | A bundle of competing interpretations is better expressed as relationships between Interpretations, which makes each independently retrievable — and which rule 10 already requires (§5.5). |
| **EvidenceClaim** | Explicitly rejected by principle 5. |

---

## 5. The epistemic layer

### 5.1 Terminology — settled

The contract and the corpus used the same two words in opposite senses. The contract's *observation* ("what a source records, carried with its provenance") is the corpus's *attestation*; the contract's *assertion* ("what a source or scholar states") is close to the corpus's *observation*. Read literally against each other they produce an inverted model.

**The corpus's structure was coherent; the propositional layer was misnamed, not misconceived.** The split is not the raw-versus-claim layer principle 5 rejects — it is evidence-instance versus deduplicated proposition, a many-to-many join. Source, Attestation and the propositional record together constitute **one** evidential level; Interpretation is the second. The two-level commitment holds.

**Settled resolution:**

| Contract term | Ontology type | Corpus record | Change |
|---|---|---|---|
| Source | **Source** | `SourceRecord` | none |
| Observation ("what a source records, with provenance") | **Attestation** | `AttestationRecord` | none; the contract's sense is glossed in the definition |
| Assertion ("what a source or scholar states") | **Assertion** | `ObservationRecord` | **RENAMED** |
| Interpretation | **Interpretation** | `InterpretationRecord` | none |

`ObservationRecord` → `Assertion`, implementing principle 11. Touches 254 observation records, the `OBS-` prefix, hard rule 3's wording, the `observations_supported` field name, and every record carrying an `OBS-` reference. Full scope at §17.2. **Attestation is unchanged** — it is the more precise term for a sourced textual instance, it is embedded in hard rules 3 and 4 and in the provenance discipline, and it runs through 477 records.

### 5.2 Source

**What it is.** A work that generates evidence: a chronicle, a geography, a survey publication, a TIB volume, a numismatic catalogue, a modern monograph. 79 records.

**Identity criterion — the work, held distinct from its editions, translations and manuscript witnesses.** Hard rule 3 states this and it carries forward unchanged. The corpus's discipline here is mature: `SRC-0065` (Eger 2008), `SRC-0079` (Eger 2012) and `SRC-0007` (Eger 2015) are three sources by one author, correctly separated, with the relations between them recorded rather than collapsed.

**Certainty dimensions.** None of the five. A source's epistemic properties are reliability and bias, which are assessments recorded on the record, not certainty about the world.

**Carries forward.** The two standing categories for hard-to-source citations — (A) authorless-but-citable, `author_unnamed: true`; (B) named tradent with no citable work, not minted — unchanged. Nothing in the new ontology disturbs them.

### 5.3 Attestation

**What it is.** One source's statement of one datum about one or more subjects, with full provenance: citation, location within source, quotation or paraphrase, provenance category, evidential confidence.

**Identity criterion — (source, location within source, datum).** The corpus has litigated this well under pressure. The `ATT-0470` split at Sumaysāṭ — a joint Ibn Ḥawqal/al-Iṣṭakhrī datum separated into two attestations because two sources cannot share one — is the criterion applied correctly, as is the Item-F outcome retaining five complementary pairs rather than merging them.

**Carries forward, in full.** Hard rule 1 (no fabricated citations; `[citation needed]` plus review flag). Hard rule 3 (evidential levels distinct). Hard rule 4 and the secondary-source-mediated extraction pattern. Hard rule 5 (`editorial_review_required` until verified against the printed page). Rule 8 (the evidential claim lives in `paraphrase` or `direct_quotation`, never only in `notes`) — validator-enforced, with **zero violations across all 477 records**. Rule 11 in its ratified general form — 19 `primary_observation` attestations, **all 19 carrying `observation_date`**, no violations either way. Rule 12 (thin one-clause primaries citing an existing source are attested inline). Rule 13 (al-Yaʿqūbī work attribution). The bare-mention rule — which becomes *more* load-bearing under the new ontology, because a controlled vocabulary of components and functions creates fresh temptation to mint attestations for name-occurrences.

**Extension: reference mode.** The subject link is currently a plain list, read conjunctively. The corpus needs a disjunctive case: a source names "the fortress of Ḥiṣn *X*" and it is not known which of two candidate sites is meant. Attaching to both falsely asserts both; attaching to neither loses the evidence. The subject link becomes a **qualified link** carrying `reference_mode: definite | candidate | collective` and its own identification confidence. A small extension to a link, not a new type; it makes the "one name, several places" edge case fully representable (§10.5).

**Extension: examination provenance.** Where an attestation records the findings of an examination, it carries an evidential back-link to the examination Event (§14). Optional, additive.

**Certainty dimensions.** None of the five substantive dimensions. An attestation carries **evidential confidence** — how securely this source supports this datum — a different quantity that must stay nominally distinct from the five (§8.2).

### 5.4 Assertion

**What it is.** The deduplicated proposition that one or more attestations support: *al-Muʿtaṣim led a major campaign against Byzantium in 838*; *Mutallip Höyük yielded Early Islamic wares*; *this site lies at 38.09 N, 37.88 E*.

**Identity criterion — (proposition, subject set).** One proposition asserted by five sources is one Assertion with five supporting attestations. This is the deduplication key and the justification for the layer: it makes "which claims are multiply attested, and which rest on a single witness?" a query rather than a reading exercise.

**Settled: every attestation supports at least one Assertion** (invariant I3). 208 of 477 attestations currently support none and require back-fill.

**The justification is prospective, and the current measurements must not be read as an argument about the layer's value.** The corpus today is dominated by a single secondary transmission route: the great majority of attestations have the shape *Eger reports that al-Balādhurī says X* — one primary, one datum, no convergence. That extraction pattern **structurally suppresses multiple attestation**. Of 254 assertions, 32 have more than one supporting attestation; that figure measures the composition of a Phase-2 gazetteer extraction, not the intrinsic value of a deduplication layer.

As Phase 3 extracts primary Arabic, Byzantine and archaeological sources directly, genuine convergence on propositions **already in the corpus** should rise sharply — several independent geographers on one settlement's status, several chronicles on one campaign, survey and excavation on one ceramic horizon. The layer is the structure that will hold that convergence when it arrives. Building it now, while the back-fill is 208 records, is materially cheaper than building it after Phase 3, and a corpus that acquires convergent evidence with nowhere to record convergence will simply record it as parallel unconnected attestations — which is the failure the layer exists to prevent.

**Assertion kinds.** An Assertion inherits its certainty dimension from its kind: locational → spatial; dating → chronological; functional → functional; identification → identification. This is how principle 6's "specify which dimensions apply to which types" is satisfied without forcing five dimensions onto one record. Geometry and dating assertions are the two kinds that also carry structured payloads (§5.6).

**Extension: polarity.** `assertion_polarity: asserted | denied`. Eger's 2012 re-examination found *no* Early Islamic pottery; RQ2 asks about contraction, which is a question about absence. §10.14 states what this does and does not solve.

### 5.5 Interpretation

**What it is.** One scholar's argued reading of one or more attestations, attributed and dated.

**Identity criterion — (scholar, publication, argument).** One scholar advancing one argument in one publication is one Interpretation. The same scholar reversing position in a later publication produces a *second* Interpretation, related to the first by `revises` — the Eger 2005→2012 ceramic reversal is two positions and a revision, not one record describing a change of mind.

**Rules 9 and 10 carry forward, and the corpus does not yet satisfy either fully.** With both now documented, compliance is measurable for the first time:

- **Rule 9** — supporting evidence cites Attestations, never raw Sources. **Fully compliant on the ATT-only constraint: zero of 174 interpretations cite non-attestation evidence.** But **57 (33%) carry an empty `supporting_evidence`**, breaching the requirement that an interpretation rest on attested support. This is the same shape as the Item-G rule-8 finding — a convention observed in what it forbids and neglected in what it requires, invisible because nothing enforced it. Back-fill and a validator check are indicated, and the Item-G sequence discipline applies: **add the check first, confirm it reports exactly 57, then back-fill.**
- **Rule 10** — related and competing interpretations are explicitly cross-referenced. **Zero relationships have an interpretation endpoint; 29 interpretations name another interpretation in prose.** Compliance is 100% textual and 0% structural.

**Dossier unbundling is a correction, not a proposal.** v0.1 presented it as a design requirement arising from success criterion 6. With rule 10 recovered, the position is different and simpler: `INT-0174` holds four distinct scholarly positions (Özgen & Gates 1991, Killebrew 2004, Eger 2005, Eger 2012) inside one record's `argument` prose, and **an existing editorial rule already required them to be explicitly cross-referenced**. A bundled dossier is not a new requirement the ontology imposes; it is an existing record that does not yet satisfy existing discipline. The correction:

> **Each position is its own Interpretation. Disagreement is expressed by first-class Relationships between Interpretations — `contradicts`, `revises`, `supersedes`, `corroborates`. A dossier is a queryable subgraph, not a paragraph.**

Scope of the correction, measured: **4 interpretations carry two or more numbered positions in a single argument** (`INT-0037`, `INT-0114`, `INT-0124`, `INT-0174`); **29 carry a prose cross-reference to be promoted to a relationship**; the two sets overlap in none. This uses principle 9 to satisfy rule 10, adds no type, and gives each position its own scholar, date and confidence, which the bundled form flattens.

**Certainty dimensions.** None of the five. An Interpretation carries **argumentative confidence**, which like evidential confidence stays nominally distinct from the five.

### 5.6 Geometry and dating as designated assertions

This section carries principle 3, and §13 gives its versioning consequences.

**The problem.** Principle 3 requires geometry and date to vary independently, each with its own provenance and uncertainty, neither privileged. The edge-case catalogue requires several competing geometries per site, each with source, method and confidence. Success criterion 5 requires geometries queryable as geometries straight from the store. A design that satisfies the first two by scattering geometries across records defeats the third.

**The specification.** Geometry and dating are typed roles of Assertion, and every SpatialThing and Phase holds a **designated** pointer to one.

- Any number of **spatial assertions** may attach to a SpatialThing or a Phase, each with geometry payload, method, uncertainty radius, spatial confidence, and supporting attestations.
- Any number of **temporal assertions** may attach to a Phase, an Event or a bounded entity, each with dating, precision, dating system, chronological confidence, and supporting attestations.
- Each subject carries a **designated spatial assertion** and a **designated temporal assertion**: the value the project has adopted for analysis. **Designation is an editorial act with a recorded rationale, not a silent default.**
- **The designated pointer is a field on the domain record, not a flag on the assertion.** This is single-valued by construction, is explicitly within L1's permitted references, and keeps the audit trail where a consumer reads the value. §13 depends on this choice.

**Why this is right, in four steps.**

1. *It follows from principle 4.* A geometry is knowledge about where a thing is, not the thing. Competing geometries are competing knowledge, and putting them in the epistemic layer is the principle applied consistently — which is why the multiple-geometries edge case needs no special handling.
2. *It makes space and time structurally symmetrical.* Both are assertion sets with a designated member. Principle 3's co-equality becomes the shape of the model rather than an aspiration: a Phase with a firm date and three candidate footprints and a Phase with a firm footprint and three candidate dates are the same structure.
3. *It preserves direct analysis.* The designated assertion gives every analysis one geometry and one date per subject. Competing values remain queryable when the question is about the dispute.
4. *It is what the corpus already does.* The Zibaṭra adoption is this pattern executed by hand: two candidate points, an Interpretation weighing them (`INT-0172`), a corroborating attestation (`ATT-0512`), an adoption decision with rationale, a MAJOR bump. Likewise Bālis (`INT-0169`) and Malaṭya (`INT-0170`). §13.4 shows that Policy B-2 reproduces all three exactly.

**How geometry attaches.** To **both** entity and phase, semantically rather than by convenience:

- To a **Phase** when asserted for a dated state — an excavation plan of the Umayyad fort, a surveyed circuit of the tenth-century wall.
- To the **entity** when asserted period-independently — a gazetteer point locating the site as such. Most of the corpus's 57 existing coordinates are of this kind.
- **Invariant I10:** a phase-attached geometry inherits that phase's temporal scope; an entity-attached geometry is temporally unscoped and may never be silently treated as period-specific. This blocks the commonest temporal-GIS error, drawing a phase map from undated points.

**What this replaces.** The `Coordinates` block; `alternative_coordinates` (defined, used by **zero** records); `chronology` (used by one); and the point-only latitude/longitude pair. Geometry becomes a full geometry type — point, linestring, polygon, multipolygon — required independently by Route and by the two-nuclei case. `EPSG:4326`, `coordinate_method`, `coordinate_precision`, `uncertainty_radius_m` and `coordinate_confidence` carry forward onto the spatial assertion unchanged.

### 5.7 Evidence-machinery neutrality — confirmed

Design note (b) requires that Assertion and Interpretation be neutral about *what* they evidence, so that deferring community and population types stays a live option rather than a decision that quietly becomes irreversible.

**Confirmed. The property that makes it true:** the epistemic layer references its subjects through an **abstract Entity supertype, not a closed union of concrete types**. An Attestation's subjects, an Assertion's subjects, an Interpretation's subjects and a Relationship's endpoints are all "any domain record", constrained by invariant rather than by enumeration. Nothing in the epistemic layer's structure names Site, Component or Person.

Three checks:

1. **Negative.** No epistemic type's definition in §5.2–5.6 mentions a concrete domain type. Attestation carries a source, citation, claim, provenance category and subject set; none of that is spatial, and none would change if the subject were a mortuary population.
2. **Forward.** Add a hypothetical `MortuaryPopulation` on paper. What must change in the epistemic layer? Nothing. An attestation cites the excavation report; an assertion states the demographic proposition; two interpretations disagree; a relationship associates the population with a Site's cemetery Component. The only additions are a domain type and vocabulary terms.
3. **Empirical.** The corpus already does this without noticing. `entities_referenced` is a list of bare identifiers with no type discrimination, currently carrying `ENT-PLC-`, `ENT-PERS-`, `ENT-EVT-` and `ENT-POL-` references through one field.

**One binding implementation constraint.** Neutrality holds only if the logical model resists giving Attestation a typed foreign key per subject type — separate `site_id`, `component_id`, `person_id` columns, which is the natural relational instinct. That would silently convert the union into a closed enumeration and make design note (b)'s deferral irreversible. **The subject link must remain polymorphic over the Entity supertype.** This is a standing check for logical-model review, recorded here because the pressure arises there and not now.

---

## 6. Relationships as first-class records

**What they are.** A typed, dated, evidenced connection between two records, carrying its own metadata. 144 records exist, implementing principle 9.

**Identity criterion — (type, source, target, temporal scope).** Two records with the same type and endpoints but different temporal scopes are **different relationships**. "Malaṭya subordinate to the Abbasid Caliphate, 758–934" and "Malaṭya subordinate to the Byzantine Empire, 934–" are two facts, and a model treating them as one relationship with a changing target loses the first.

**Endpoints may be entities, phases or interpretations.** Interpretation endpoints are required by rule 10 and are currently unused (zero of 144). **Invariant I8:** a relationship with a Phase endpoint inherits that phase's temporal scope and may not assert a wider one.

**Certainty dimensions.** Relationship certainty — the fifth dimension, which applies here and only here — plus chronological certainty on the temporal scope.

**Carries forward.** The record structure, the 21 types in active use, the `linked_attestations` discipline, and the allowance that structural relationships (`contains`, `parent_event_of`) may carry no direct evidence because their support is inherited.

### 6.2 Five missing relationship families

The `RelationshipType` enum has 44 terms, 21 in use. Five families the contract requires are **absent entirely**:

| Family | Required by | Terms |
|---|---|---|
| **Visibility and control of landscape** | RQ1: "which forts overlook which passes... which sites are intervisible" | `overlooks`, `intervisible_with`, `controls`, `guards`, `commands_approach_to` |
| **Event → phase production** | RQ3: "links from events to the phases they produce" | `produced_phase`, `terminated_phase`, `damaged` |
| **Route structure** | RQ1: route families and corridors | `member_of_route_family`, `traverses`, `crosses_at` |
| **Settlement hierarchy and defensive systems** | RQ2: "settlement hierarchies... regional defensive systems" | `subordinate_installation_of`, `member_of_defensive_system`, `dependent_settlement_of` |
| **Interpretation-to-interpretation** | **Rule 10**, and §5.5 | `revises`, `corroborates` (`contradicts` and `supersedes_attestation` exist) |
| **Examination** | §14 | `examined`, `examined_without_result` (or a scope-qualified `examined`) |
| **Succession and restoration** | §4.2, §4.5, §12.2 | `succeeds`, `restores` |

The absence is diagnostic rather than accidental: the enum was built for a text-centred Phase-1 corpus of events and persons, and the contract's landscape questions were never expressed in it. That the corpus records `near` 21 times and `overlooks` zero times is an observation about the vocabulary, not about the frontier. Extension is governance §5.5 business — Board majority, three concrete cases per term.

**`contains` needs narrowing.** The most-used type (27 records) is doing three jobs: spatial containment, administrative subordination, and part-whole. Under this ontology, part-whole between Site and Component is structural; administrative subordination is `belongs_to` or a TerritorialUnit link; `contains` narrows to spatial containment. A read-only scoping pass before migration (§17.6).

---

## 7. The analytical layer — AnalyticalRegion

**What it is.** A named, versioned, attributable selection over the domain: "the northeast Anatolian corridor", "Cilicia", "the whole frontier", "the sites in Eger's Appendix 2", "the study area of chapter 4".

**Identity criterion — (author, name, version, membership specification).** An analytical region is identified by who defined it and how, not by what it contains. Two researchers drawing the same boundary have defined two regions; the same researcher revising a boundary has produced a second version. Deliberately unlike every domain type, because an analytical region is a *research act* and its identity is the identity of that act.

### 7.1 Membership

- **Extensional** — an explicit list of member records. Reproducible exactly, which is what a published figure needs.
- **Intensional** — a boundary geometry plus a predicate ("all Sites whose designated geometry falls within this polygon"). Scale-flexible, re-evaluating as the corpus grows, which is what an ongoing analysis needs.
- **Hybrid** — an intensional rule with explicit inclusions and exclusions. What real study areas look like.

### 7.2 Prohibitions

No domain record may reference an AnalyticalRegion (L2). Analytical regions have no attestations, no interpretations, no phases and no place in the CRM crosswalk. They may be exported alongside data as the provenance of a figure or table, but they are not part of the historical model.

**Certainty dimensions: none.** A researcher's selection is not uncertain; it is stipulated. This is a useful check on the layering — any analytical-layer candidate that seems to need a certainty dimension is probably a domain object in disguise.

### 7.3 Temporal extent — settled semantics

AnalyticalRegion carries an **optional temporal extent**. The semantics are specified rather than left to implementation, because the failure modes are silent ones.

> **A null temporal extent means TEMPORALLY UNBOUNDED.** It records that no analytical temporal scope forms part of the region's definition; any temporal constraint is supplied by the query.
>
> **A null extent must never be interpreted as "the full corpus extent."** That reading is specifically rejected because it creates hidden coupling: if the corpus later extends past 1100, every null-extent region would silently change meaning with no record having changed.

**Interaction between region-defined and query-defined windows:**

1. An **unbounded** region accepts whatever temporal filter the query supplies.
2. A **bounded** region contributes its own constraint, and the effective result is the **intersection** of region extent and query window.
3. **A query may narrow a bounded region's extent but may never widen it.** A populated extent is part of the region's definition, and silently widening it destroys the citable, reproducible property the field exists to provide. A query requesting a range outside a bounded region's extent returns the intersection — which may be empty — and does not fall back to the region's members outside its extent.

Rule 3 is the load-bearing one: it is what makes an AnalyticalRegion a *citable object* rather than a convenience. A figure captioned "sites in region R" means the same thing when regenerated.

**Why one type and not two.** A separate `AnalyticalWindow` type was considered and rejected under the admission test: it shares the identity criterion — a researcher-defined selection — and differs only by which dimension it selects on. Difference by one dimension is an attribute, not a type (§4.11). The unified form also prevents a study's spatial and temporal scopes drifting out of sync, which two records permit and one does not.

**Research questions.** RQ5 — publication-quality outputs generated directly from the data, and reproducible analytical scoping. Also the contract's §8 comparative dimension: a comparison with al-Andalus or the Roman limes is a comparison between analytical regions, which is why the domain must not be pre-partitioned.

---

## 8. Certainty

### 8.1 Which dimensions apply where

| Type | Identification | Chronological | Spatial | Functional | Relationship |
|---|---|---|---|---|---|
| Site | ✅ on the entity | via phases | via geometry assertions | via phases | — |
| LandscapeFeature | ✅ | via phases (rare) | via geometry assertions | weak; anthropogenic only | — |
| Route | ✅ | via phases | via geometry assertions | ✅ on phases | — |
| TerritorialUnit | ✅ | via phases | via geometry assertions (weak) | ✅ on phases | — |
| Component | ✅ (weak) | via phases | via geometry assertions | ✅ on phases — the central case | — |
| Phase | — | ✅ via designated temporal assertion | ✅ via designated spatial assertion | ✅ | — |
| Event | ✅ (bearing "did it happen") | ✅ | ✅ | — | — |
| Polity | ✅ | ✅ | — (derived) | — | — |
| Person | ✅ | ✅ | — | — | — |
| Relationship | — | ✅ on temporal scope | — | — | ✅ — the only bearer |
| Source | — | — | — | — | — |
| Attestation | — | — | — | — | — |
| Assertion | by kind | by kind | by kind | by kind | — |
| Interpretation | — | — | — | — | — |
| AnalyticalRegion | — | — | — | — | — |

**Dimensions live at the level where the question is asked.** The chronological column is the important one: it almost never sits on an entity, because "when was this?" is a question about a state, not about a persistent identity. That is principles 2 and 3 acting together, and it is what makes a redating a change to a phase's designated temporal assertion rather than a change to the site.

### 8.2 A sixth quantity, kept distinct

Attestations carry **evidential confidence**; Interpretations carry **argumentative confidence**. These are about the strength of a piece of evidence or an argument, not about a property of the world. The five dimensions describe the world; these two describe our grip on it. Conflating them is how a single confidence score gets rebuilt by accident, and the logical model must keep them nominally distinct.

### 8.3 `overall_confidence` — RESOLVED: retire

**Recommendation: retire outright, executed within the schema-migration pass.**

*The substantive argument.* `overall_confidence` is either a redundant restatement of one dimension or an aggregate of quantities principle 6 says are independent and must be recorded separately. There is no derivation rule that is both honest and useful: any rule for combining independent dimensions is itself a claim that they are not independent. And a field that exists will be filtered on, which silently reintroduces the single confidence score the contract rejects.

*The cost argument, which resolves the inclination to defer.* The field is present on exactly **325 records: 190 places + 81 persons + 54 events** — verified, and exactly the union of the three types that carry it. **Every one of those 325 records is already being opened** by the migrations in §17: places by the place pass, persons and events by the person/event pass. The marginal cost of retiring the field within those passes is close to zero.

**Deferring is therefore the expensive option.** If it is not retired during the schema migration, it becomes a standalone 325-record MAJOR migration afterwards, at full cost for no benefit gained by waiting.

*If display needs it.* A derived indicator may be computed at the presentation layer from the applicable dimensions, provided it is (a) computed, never stored; (b) documented as a display heuristic; (c) never available as a query filter. It is out of the ontology.

---

## 9. Invariants

Stated so they can be validated. Several correspond to checks the corpus already runs; the compliance state of the rest is given at §17.

**Layering**

- **L1** — A domain record's fields may name epistemic records only as designated-assertion pointers or evidential back-links. Epistemic records may name domain records freely. L1 constrains stored references, not query traversal direction.
- **L2** — The analytical layer may reference the domain and epistemic layers; neither may reference the analytical layer.

**Evidence**

- **I1** — Every domain entity has at least one supporting attestation. *(Specification §3.1.)*
- **I2** — Every attestation names exactly one Source and carries a non-empty `paraphrase` or `direct_quotation`. *(Rule 8; enforced; zero violations.)*
- **I3** — Every attestation supports at least one Assertion. *(§5.4; 208 records currently violate.)*
- **I4** — Every Assertion has at least one subject and at least one supporting attestation.
- **I5** — Every Interpretation has at least one supporting attestation, and cites Attestations only. *(Rule 9; the ATT-only half is fully compliant, the non-empty half breached by 57 records.)*
- **I5a** — Related and competing interpretations are linked by explicit Relationships. *(Rule 10; 29 records carry the link as prose, 0 as data.)*
- **I5b** — An attestation with `provenance: primary_observation` carries an `observation_date`, and no other attestation carries one. *(Rule 11, general form; fully compliant.)*

**Time and structure**

- **I6** — A Phase belongs to exactly one subject. Site phases may not overlap; component phases may overlap each other and need not align with site phases. Phases may be non-contiguous.
- **I7** — An entity's asserted existence interval must be consistent with the union of its phase intervals, or be flagged.
- **I8** — A relationship with a Phase endpoint inherits that phase's temporal scope and may not assert a wider one.
- **I8a** — Where an examination Event and a rule-11 attestation both record the same fieldwork, the attestation's `observation_date` falls within the Event's interval. *(§14.4.)*

**Space and designation**

- **I9** — A designated spatial or temporal assertion must be one of the subject's own asserted values, and the designation carries a recorded rationale.
- **I10** — An entity-attached geometry is temporally unscoped and may not be treated as period-specific.
- **I11** — A subject has at most one designated spatial and at most one designated temporal assertion. *(Guaranteed by construction: the pointer is a single-valued field on the domain record.)*

**Identity**

- **I12** — Multiple names never generate multiple entities; a shared name never merges entities. *(Master-record rule, specification §4.1.)*
- **I13** — Interpretive disagreement about function never propagates to an entity's existence or identity. *(Principle 4; checkable as "no functional certainty field on a persistent entity".)*
- **I14** — Component identity is dependent on its parent Site; Phase identity on its subject. Neither survives the deletion of its parent, and both follow the fabric under a split.

**Editorial**

- **I15** — A source named without a datum produces a note, not an attestation. *(Bare-mention rule.)*
- **I16** — Contradictory assertions are retained. Any editorial resolution is recorded as an Interpretation or a designation act with rationale, never as an overwrite. *(Governance §14.)*
- **I17** — A datum reached through an intermediary is filed against the source that stated it, with the transmission route in the citation. *(Hard rule 4.)*

---

## 10. The edge-case test suite

Verdicts: **clean** (typical-case design, no addition), **extension** (a small named addition), **limitation** (honestly not handled).

### 10.1 A fort controlling a mountain pass — clean
A LandscapeFeature (the pass, existing independently, `origin: natural`) and a Site (the fort), linked by `controls` or `commands_approach_to` carrying relationship certainty, temporal scope and supporting attestations. Where the fort controls the pass only in some phases, the relationship attaches to those phases. *Requires the visibility-and-control relationship family (§6.2).*

### 10.2 A settlement that moves a short distance — clean, with a ratified threshold
One Site, two Phases, different designated spatial assertions. Governed by **Rule 14** (§15.1), which is scale-relative by construction and provides a recorded outcome for undecidable cases.

### 10.3 A monastery that becomes a fortress — clean
One Site, successive Phases of differing function. Function lives on the Phase, so physical identity is structurally incapable of being disturbed by the functional change. Functional certainty attaches per phase, so "certainly a fortress, probably a monastery before that" is representable without either claim contaminating the other.

### 10.4 Multiple names for one place — extension (small)
One Site carrying a set of attested names, each with language, script, name type and its own supporting attestation. 152 of 190 places already carry alternative names. *Extension:* names gain optional temporal validity, since the catalogue specifies names attested "in different sources **or periods**". The schema's existing `TimeBoundedAttribute` is the right shape. **Recommendation: add the field, do not back-fill** — dating a name's currency is a scholarly claim, and 152 speculative datings would be worse than none (§17.5).

### 10.5 One name referring to different places — extension (small)
Two Sites, each carrying the shared name, linked by `different_from` or `alternative_identification_of` — both in the enum, and `different_from` is already used 8 times, so the corpus has met this case. *Extension:* the harder half, where an attestation uses the shared name and the referent is unknown. The **qualified reference link** (§5.3) resolves it: the attestation links to both as *candidates*, and two competing Interpretations argue for each. The ambiguity is represented rather than resolved by fiat, which is what the catalogue asks.

### 10.6 Seasonal or intermittent occupation — clean
Phases need not be contiguous (I6), handling gaps with no special machinery. A Phase attribute `occupation_regime: permanent | seasonal | intermittent | unknown` handles within-phase intermittency. A vocabulary term, not a type — "seasonal site" would be a tempting and wrong new type.

### 10.7 Two contemporaneous occupation nuclei — clean
One Phase whose designated spatial assertion is a multipolygon. *Requires* full geometry types, which Route requires independently.

### 10.8 Uncertain site location — clean, and reclassified as typical
A Site with no spatial assertion, or several candidates and no designation, retaining identification status and confidence.

**The catalogue treats this as an edge case; in the corpus it is the majority case. 57 of 190 places carry coordinates — 70% have none.** A design tuned for the typical case must treat unlocated entities as ordinary, and no analysis or output may assume a geometry exists. Direct consequence for RQ5: **any spatial analysis reports its coverage as a matter of course**, because a least-cost network built from 30% of the sites is a different object from one built from all of them. Principle 12 says edge cases are a test not a driver — but this one is not an edge case, and the specification says so.

### 10.9 Multiple possible geometries — clean, natively
The paradigm case for geometry-as-assertion. A survey polygon, a digitised TIB outline, a remote-sensing interpretation and an excavation plan are four spatial assertions on one subject, each with its own method, provenance and confidence; one designated, the rest retained. Zibaṭra, Bālis and Malaṭya are three worked examples already in the corpus.

### 10.10 Contested function, uncontested existence — clean
Structurally guaranteed rather than merely permitted: functional certainty has no field on a persistent entity (I13), so the disagreement has nowhere to attach except phases and interpretations.

### 10.11 Conflicting chronologies for the same material — clean, with the §5.5 correction
Four competing dated assertions on the same Phase or Component, none designated while the dispute is unresolved, the disagreement expressed as Interpretations related by `contradicts` and `revises`. Eger's 2005→2012 self-reversal is two Interpretations with a `revises` link, representing the reversal as a fact about the historiography rather than as a note. The dossier unbundling that makes this work is a **rule-10 correction**, not a new requirement (§5.5).

### 10.12 An attestation that misreads an earlier scholarly statement — clean
Three existing mechanisms, no new type: the erroneous attestation **retained** at `workflow_state: deprecated`, never deleted; a correction **Interpretation** recording what was misread, the source passage, and why the reading fails; a `supersedes_attestation` **Relationship** linking correction to error. **General pattern: a retraction is an editorial act represented by an interpretation plus a supersession, not an entity type.**

This case tests *behaviour* as much as structure. The ontology guarantees the correction is representable; rule 5 and the `editorial_review_required` discipline guarantee it is performed.

### 10.13 LIMITATION — competing phase divisions

The model handles competing *dates* for an agreed division natively (§10.11). It does **not** handle competing *divisions* — one scholar reading three phases where another reads five, or two schemes placing a boundary at different points in the same stratigraphy.

- **(i)** Editorially adjudicate one canonical phasing; hold competing periodisations as Interpretations referencing the phases they dispute. Cheap; the rival scheme exists as prose, not as structure.
- **(ii)** Give Phase a `phasing_scheme` discriminator so multiple schemes coexist over one subject, each internally ordered and non-overlapping. Complete; roughly doubles phase records for disputed sites and complicates every query assuming one phasing.

**Recommendation (i) now, (ii) as the principled extension. Timing revised from v0.1.** v0.1 said this "matters most for excavated sites, which are the minority of the corpus" — true of the gazetteer corpus as it stands, and misleading about what is coming. **The dissertation corpus is the northeast Anatolian corridor — Komana, Satala, Sebastopolis — which is proportionally far more excavation-heavy, with published stratigraphic sequences and rival periodisations.** The limitation should be expected to bind **during Phase 3**, not eventually.

**Consequence for the logical model, and this is the actionable part.** Because (ii) is expected rather than hypothetical, the logical model must be built so that adding a `phasing_scheme` discriminator later is a MINOR addition rather than a restructuring:

> **Do not build a uniqueness constraint that assumes one phasing per subject.** Phase ordering and non-overlap (I6) must be enforced *within a scheme*, with the scheme defaulting to a single implicit value, rather than across all phases of a subject unconditionally.

This costs nothing now and is the difference between a MINOR field addition and a MAJOR restructuring when Phase 3 arrives.

### 10.14 LIMITATION, SUBSTANTIALLY NARROWED — negative evidence and absence

*Revised from v0.1 following the L1 check at §14, which clears examination-as-Event.*

**What v0.1 said.** A query for "sites with no Early Islamic occupation" could not distinguish evidence of absence from absence of evidence, and the gap was stated flatly.

**What changes.** With examinations modelled as Events (§14) and assertion polarity available (§5.4), the two-way confusion becomes a **three-way distinction, each branch queryable**:

| Branch | Query | Epistemic status |
|---|---|---|
| **Evidence of absence** | Sites carrying a *denied* assertion of Early Islamic occupation, supported by an attestation from an examination Event whose detection scope covers Early Islamic ceramics | A competent examination looked and found nothing |
| **Absence of evidence** | Sites with no examination Event of adequate detection scope | Nobody has looked |
| **Unresolved** | Sites with an adequate examination but no assertion either way | Looked at, nothing recorded |

Eger's 2012 Bilkent re-examination is a clean instance of the first branch: an examination Event, a denied assertion, an attestation, adequate scope.

**The condition.** This requires a `detection_scope` attribute on examination Events — what material classes, periods and methods the examination was competent to detect. Without it, a Bronze Age survey that would never have reported Early Islamic sherds counts as an examination, and the first branch silently absorbs cases belonging in the second. `detection_scope` is an attribute on an existing type, not a new type.

**The residual, which is real and irreducible.** A site examined with adequate scope, where Early Islamic material *was* found but the assertion was never entered, appears in the "unresolved" branch and, if the branch is collapsed, in the absence branch. **No ontology can fix this: it is a completeness property of the corpus, not of the model.** The mitigation is the same as for spatial coverage (§10.8) — any RQ2 argument about contraction reports its evidential coverage rather than assuming it.

**Revised verdict: narrowed from a flat gap to a three-way queryable distinction with one irreducible residual and one required attribute.**

### 10.15 Summary

| # | Case | Verdict |
|---|---|---|
| 1 | Fort controlling a pass | clean *(needs relationship vocabulary)* |
| 2 | Settlement moving a short distance | clean *(Rule 14)* |
| 3 | Monastery → fortress | clean |
| 4 | Multiple names for one place | extension — time-bounded names |
| 5 | One name, several places | extension — qualified reference links |
| 6 | Seasonal / intermittent occupation | clean |
| 7 | Two contemporaneous nuclei | clean *(needs full geometry types)* |
| 8 | Uncertain site location | clean — **reclassified as typical** |
| 9 | Multiple possible geometries | clean, natively |
| 10 | Contested function, uncontested existence | clean |
| 11 | Conflicting chronologies | clean *(via the rule-10 correction)* |
| 12 | Attestation misreading a scholar | clean |
| 13 | *Competing phase divisions* | **LIMITATION** — (i) now, (ii) expected in Phase 3 |
| 14 | *Negative evidence and absence* | **LIMITATION, NARROWED** — three-way distinction; residual is corpus completeness |

Ten clean, two small extensions, two limitations — one of them substantially narrowed since v0.1, both stated rather than smoothed.

---

## 11. The seven success criteria

### 11.1 Query coverage — satisfiable
Every RQ is expressible over the proposed structures, conditional on the relationship vocabulary extension (§6.2). RQ1 runs over Sites, LandscapeFeatures, Routes, spatial assertions and control/visibility relationships; RQ2 over Sites, Components, Phases and hierarchy relationships; RQ3 over Events, `produced_phase` links, TerritorialUnits and Polities; RQ4 over the epistemic layer and the five dimensions; RQ5 over all of these plus AnalyticalRegion.

**Check.** A **query register**: one named, executable query or defined workflow per *subordinate* question — twenty-two across the five RQs — each with its expected result shape. The criterion is met when every entry runs against the store with no intervening remodelling. **Written before the logical model, as its acceptance test** (§19.3).

### 11.2 Edge-case coverage without special-casing — partial, with the remainder named
All twelve catalogued cases are representable: ten with no addition, two with principled extensions that are neither project-specific types nor one-off exceptions. Two further limitations found by testing (§10.13, §10.14) are not fully satisfied and are stated as such.
**Check.** Each of the fourteen cases realised as a worked record set using only general types, confirming none required a type or field existing solely for it.

### 11.3 CIDOC CRM mapping — satisfiable
| Type | CRM |
|---|---|
| Site | `E27_Site` + `E53_Place` for extent |
| LandscapeFeature | `E26_Physical_Feature` (+ `E53_Place`), typed via `E55_Type` |
| Route | `E53_Place` + `E55_Type`; family membership via `P89` or a typed `E13` |
| TerritorialUnit | `E53_Place` + `E55_Type`; constitution/dissolution as `E7_Activity` / `E64_End_of_Existence` |
| Component | `E22` / `E24`, `P46 is composed of` from the Site |
| Phase | `E4_Period` (or `E3_Condition_State` where it records condition) |
| Spatial assertion | `E13_Attribute_Assignment` assigning an `E94_Space_Primitive` |
| Temporal assertion | `E13` assigning an `E52_Time-Span` |
| Examination Event | `E7_Activity`, or `E87_Curation_Activity` for material re-examination |
| Polity | `E74_Group` |
| Assertion *(renamed)* | `E89_Propositional_Object` — unchanged from the current mapping |
| Interpretation | `I1_Argumentation` (CRMinf) — unchanged |
| **AnalyticalRegion** | **no CRM class; not exported** |

The last row is a check, not a shortfall: CRM models the historical world and an analytical region is not part of it. That the crosswalk stops exactly at the layer boundary independently confirms the boundary is real, and makes the CRM export a clean projection rather than a filtered one.

Note also that geometry-as-assertion *improves* the CRM fit: reified `E13` assignments carrying `E94` primitives is CRM's own idiom for sourced spatial claims, reached from this project's requirements rather than by bending toward CRM. Principle 10 working as intended.

**Check.** One row per type and per relationship type in `ontology_alignment.md`, plus a round-trip export read by someone who did not write the mapping.

### 11.4 Dual implementation with lossless correspondence — satisfiable, three named risks
1. **Geometry** — PostGIS ↔ YAML needs a canonical serialisation (WKT or GeoJSON), fixed CRS, fixed coordinate precision. Round-tripping a polygon through floating point without a canonicalisation rule loses bytes.
2. **Ordered arrays** — phase sequence, route waypoints and attestation lists are order-bearing in YAML and unordered in SQL without an explicit ordinal.
3. **Null versus absent** — YAML distinguishes them, SQL does not. The corpus already depends on this: `paraphrase` nullable-versus-absent is exactly what made the rule-8 violations invisible before Item G. A convention must be fixed and enforced.

**Check.** A round-trip harness: YAML → Postgres → YAML, canonicalised, byte-compared. A natural extension of the existing validator tooling, built alongside the logical model rather than after it.

### 11.5 Direct analysis — satisfiable; one change is decisive
*Geometries as geometries* requires the move from point-only latitude/longitude to real geometry types (§5.6) — the single change that most determines whether RQ5 is answerable. *Dates as dates* is largely already satisfied: `TemporalValue` with `normalised_start`/`normalised_end` on alternative datings handles AH and Byzantine AM conversion and carries forward unchanged. *Relationships as a graph* is already satisfied.

**Check.** Run three analyses directly against the store: a least-cost path between attested termini; a viewshed from a fort over a pass; a betweenness-centrality computation over the site-and-route network. If any needs a transformation script, the criterion fails and the script names the missing structure.

### 11.6 Evidence-interpretation separation with full provenance — satisfiable
*Provenance resolution* is native and enforced: Assertion → attestations → source, transmission chain in the citation per hard rule 4, rule 8 guaranteeing a non-empty claim at every step, with zero violations. *Independent retrieval of competing interpretations* is currently blocked where a dossier bundles positions in prose; the §5.5 rule-10 correction satisfies it.

**Check.** Two queries. For every assertion, resolve the full chain to a source. For a known dispute, retrieve each position as a separate record with its own scholar, date and confidence — failing if any position is reachable only by reading prose.

### 11.7 Extension without redesign — satisfied
New sources: routine. New relationship types: governance §5.5, no structural change. New entity types: §5.7's polymorphic subject link means adding `Community` or `MortuaryPopulation` requires **no** change to Source, Attestation, Assertion, Interpretation or Relationship. New analytical requirements: the analytical layer is additive and nothing depends on it (L2).
**Check.** The §5.7 forward exercise run against the logical model, with the one falsifying condition — typed per-subject foreign keys on Attestation — as a standing review check.

### 11.8 Summary
| Criterion | Verdict | Remaining work |
|---|---|---|
| Query coverage | satisfiable | relationship vocabulary; query register |
| Edge-case coverage | partial | two limitations, both named |
| CIDOC mapping | satisfiable | extend alignment doc; round-trip export |
| Dual implementation | satisfiable | geometry canonicalisation, ordinals, null convention |
| Direct analysis | satisfiable | full geometry types |
| Evidence separation | satisfiable | rule-10 correction; assertion back-fill |
| Extension without redesign | satisfied | keep the subject link polymorphic |

---

## 12. Settled design calls

The five hard calls of v0.1, plus three that emerged, all now settled.

### 12.1 Site identity through time — physical continuity of the occupied locus
Rejected alternatives: *nominal continuity* (splits Sozopetra from Zibaṭra and merges the two places sharing a toponym — two of the catalogue's own cases); *functional continuity* (fails the monastery→fortress case directly); *stratigraphic continuity* (precise where excavated, inapplicable to ~90% of the corpus); *administrative continuity* (makes identity hostage to conquest, so Malaṭya becomes a different site in 934). The catalogue names physical continuity, so this is confirmation rather than choice; what it needed was the operational threshold, supplied as Rule 14 (§15.1).

### 12.2 Component identity through function change — fabric continuity
**Converted fabric is ONE component with successive phases of differing function. Demolished-and-rebuilt fabric is TWO components in succession, even on the same footprint**, linked by `succeeds`.

Rejected: *two components for any function change* — makes function constitutive of physical identity, principle 4 inverted at the component level; if a converted church is two components, a fortress that becomes a monastery is arguably two sites and persistent identity unravels from the bottom up. *One component with a function history but no phases* — loses the independent chronology RQ2 requires.

**Why fabric rather than footprint.** Footprint continuity would make the demolished-and-rebuilt case one component, which is wrong — nothing physical persists. Fabric tracks what actually continues, matches how excavation reports reason, and degrades gracefully: where the evidence cannot say whether fabric was reused, the case is one component with the alternative held as an Interpretation, exactly as Rule 14 provides for sites.

### 12.3 Site versus LandscapeFeature — occupation, not origin
The boundary is occupation. Where a thing is genuinely both, create both, governed by **Rule 15** (§15.2). Residuals from the corpus: **bridges** (crossing = feature or route component; garrisoned bridgehead = Site); **canals** (`ENT-PLC-0045`, `ENT-PLC-0097`: anthropogenic, terrain-scale, not loci of occupation → LandscapeFeature, `origin: anthropogenic` — the case that killed the origin-based boundary); **kleisourai** (genuinely three: pass, fort, command); **tells** (Sites, since they are loci of occupation); **`ENT-PLC-0002` Anzen/Dazimon** (neither — a Site or feature, with the battle as an Event related `located_at`).

*Cost, stated plainly.* This produces more records than a single-place-type model for the same evidence. The compensations: each record has one identity criterion instead of several; the fortified-pass query RQ1 asks for becomes expressible; and Rule 15 ties the multiplication to evidence rather than to completeness.

### 12.4 Events first-class — confirmed
An Event is a thing that happened; an Assertion is a claim about the world. Three structural confirmations: events have *participants*, *sub-events* and *causal links to phases*, which assertions do not; events have a multi-source identity criterion, so two differing accounts are one Event with a disagreement *about* something rather than two events with the disagreement dissolved into the ontology; and RQ3 requires events to act on the landscape, which only a domain object can do to another domain object.

**Residual: topical or fictitious events.** A siege attested once in a source given to literary topoi may not have happened. It is an Event with low identification certainty, structurally identical to a site attested but unlocated — consistent, and correct: the corpus records that the sources report a siege and that confidence it occurred is low, which is more informative than either asserting it or suppressing it. Admitting events only when occurrence is secure would silently editorialise the source tradition.

### 12.5 How geometry attaches — both, via designated assertions
Settled at §5.6. Rejected: *entity only* (cannot express phased extent; defeats RQ2 and temporal GIS); *phase only* (forces a spurious phase for every gazetteer point, and breaks the 57 existing period-independent coordinates); *both as plain attributes* (cannot carry competing geometries with independent provenance, required twice by the catalogue). The decisive consideration is symmetry: because dating is handled identically, principle 3's co-equality becomes structural rather than stated.

### 12.6 The propositional layer — retained and made mandatory
Settled at §5.4, on the prospective argument. Invariant I3.

### 12.7 Terminology — `ObservationRecord` renamed `Assertion`
Settled at §5.1.

### 12.8 `overall_confidence` — retired
Settled at §8.3, within the schema-migration pass.

---

## 13. Designation versioning — Policy B-2

Once geometry and chronology are designated Assertions rather than entity attributes, what constitutes a versioning event? This extends Policy B and is specified here so it does not emerge during implementation.

### 13.1 The governing principle

> **A change is MAJOR when a value the record previously published is invalidated for a downstream consumer; MINOR when the record gains something without invalidating anything; PATCH when nothing the record asserts changes.**

This is Policy B's existing logic made explicit, and every rule below is derived from it rather than stipulated separately.

### 13.2 The rules

| Event | Record affected | Bump |
|---|---|---|
| A new assertion is minted (a new survey publishes a geometry) | the new **Assertion** (born 1.0.0); the subject gains an evidential back-link | **MINOR on the subject** |
| **First** designation, where the subject had none | subject's designated pointer set | **MINOR** — nothing previously published is invalidated |
| **Designation changed** to a different assertion | subject | **MAJOR** — the previously published value is invalidated |
| **Designation withdrawn** (pointer → null) | subject | **MAJOR** |
| Designated assertion's confidence or uncertainty radius refined, value unchanged | the **Assertion** | **MINOR on the Assertion; no bump on the subject** |
| Designated assertion's value corrected (e.g. a projection-conversion error) | the **Assertion** | **MAJOR on the Assertion; no bump on the subject** — the pointer is unchanged |
| Superseded assertion annotated with a supersession note | that Assertion | **PATCH** |
| Interpretation gains an adoption-outcome note | that Interpretation | **PATCH** |
| A Phase's designation changes | that **Phase** | **MAJOR on the Phase** |

### 13.3 Two rules that prevent the obvious errors

> **No cascade.** A Phase's bump never propagates to its Site; a Site's never to its TerritorialUnit. Derived values — an entity's existence interval, a polity's extent, a site's location as read through its latest phase — are computed at query time and never stored, so there is nothing to bump. Without this rule, every phase edit would ripple upward through the corpus and version numbers would stop carrying information.

> **`schema_version` is orthogonal to designation.** `schema_version` records which schema the record validates against and changes only when the record is emitted under a different schema. A designation change is a `record_version` event, not a `schema_version` event. This clarifies the Phase-2 pattern in which coordinate adoptions coincided with the v1→v2 migration: the two moved together because the records were re-emitted under v2 at the same time, not because adoption causes schema migration.

### 13.4 Retrospective check against the three coordinate adoptions

Policy B-2 reproduces all three exactly, which is the test that matters:

| Zibaṭra, as executed | Under B-2 |
|---|---|
| `ATT-0512` minted (Eger 2012 corroboration) | new record, 1.0.0 ✓ |
| Coordinate replaced on `ENT-PLC-0007`, TIB 2 → Doğanşehir | designation changed → **MAJOR**, 1.4.0 → 2.0.0 ✓ |
| `INT-0172` gains an adoption-outcome note | **PATCH**, 1.0.0 → 1.0.1 ✓ |

Bālis (`INT-0169`) and Malaṭya (`INT-0170`) follow the same shape.

### 13.5 The architectural consequence — entity churn falls

Under the current model, refining a coordinate's confidence bumps the *entity*: the Manbij corroboration raised confidence 3→4 and reduced the radius 3000→1500 m, and `ENT-PLC-0043` versioned for it. Under B-2 the same refinement bumps the **assertion** and leaves the entity untouched, because the entity's designated pointer did not move.

This is the right signal. **An entity versions when the project's adopted position changes; an assertion versions when the evidence about it is refined.** A consumer watching entity versions is then watching decisions rather than evidential housekeeping — which is exactly what an entity version number should mean, and what it currently does not.

---

## 14. Examination-as-Event, and the L1 check

Curtis's proposal: model excavations and surveys as **terms in the Event type vocabulary**, not as subtypes, so that "which sites were examined, by whom, when, with what coverage" becomes a relationship query, and the negative-evidence gap may narrow. The proposal is accepted. This section gives the L1 check it was conditional on.

### 14.1 Does examination-as-Event survive the admission test? — Yes

An examination — an excavation season, a survey campaign, a dated autopsy visit, a re-examination of stored material — is a bounded happening with participants, a date and a place. Its identity criterion is *same kind, overlapping time, same place, same principal participants*: **the Event identity criterion exactly.** Under the admission test that makes it an Event with vocabulary terms, not a new type. A subtype would violate principle 8 and reintroduce precisely the proliferation §2 removes.

### 14.2 Does it survive L1? — Yes, twice over

The traversal in question is **Site → examination Event → the attestations that Event generated.** Decomposed:

**Hop 1: Site → examination Event.** This is **domain → domain.** Event is a domain type (§4.8, confirmed at §12.4), and an examination Event is a domain record like any other. The hop runs through a Relationship, which is a structural record, not an epistemic one. **L1 is not engaged by this hop at all.**

The apparent difficulty came from treating the examination Event as epistemic because its *subject matter* is evidential. It is not. The 2005 autopsy of Mutallip Höyük is a thing that happened, in the same sense that the 838 sack of Amorium is a thing that happened; what distinguishes them is their date and category, not their ontological layer. Modelling acts of investigation as events in the world is the correct treatment, and it is the same move that makes the historiography itself analysable — which is what RQ4 is for.

**Hop 2: examination Event → the attestations it generated.** This is domain → epistemic, and it is **explicitly within L1's permitted set**: it is an evidential back-link, the second of L1's two allowed forms. Every entity in the corpus already holds these — `ENT-PLC-0124` carries 16 of them in `linked_attestations`. Nothing new is being asked of L1.

**And the restatement at §3.1 removes the residual worry.** L1 constrains *stored references*, not *query direction*. Even if the link were stored only on the attestation side, traversing it in the inverse direction would be unrestricted, because an inverse is an index, not a dependency. Curtis's concern — that traversing the other way would turn "sites never examined" into a negation over the attestation set rather than a property of the Site — does not arise, because the Site→Event edge exists as a domain relationship independent of any attestation.

**Verdict: the traversal is permitted on both hops, and the second is permitted twice over.** Curtis's question exposed a genuine ambiguity in v0.1's wording of L1, which §3.1 now fixes. That correction is the more valuable output of the question.

### 14.3 Does the negative-evidence limitation narrow? — Yes, substantially

Set out at §10.14. In short: the two-way confusion becomes a three-way queryable distinction — **evidence of absence** (denied assertion + adequate-scope examination), **absence of evidence** (no adequate-scope examination), **unresolved** (adequate examination, no assertion either way).

**Required attribute: `detection_scope` on examination Events** — what material classes, periods and methods the examination was competent to detect. Without it, a Bronze Age survey counts as an examination and the first branch silently absorbs cases belonging in the second. An attribute on an existing type, not a new type.

**Irreducible residual:** a site examined with adequate scope where material *was* found but no assertion was entered. This is a completeness property of the corpus, not of the model, and no ontology can fix it. Mitigation is the same as for spatial coverage: report evidential coverage rather than assume it.

### 14.4 Interaction with rule 11

Rule 11 and examination-as-Event are complementary, not redundant:

- The **examination Event** is the domain record of the fieldwork episode: who, where, when, what scope.
- The **rule-11 attestation** is the epistemic record of the author's own written report of it, with `provenance: primary_observation` and an `observation_date`.

Worked example, `ATT-0440`: an examination Event dated 2005-07-20 at `ENT-PLC-0124`, participants Eger and de Giorgi, category `investigation`, sub-category `site_visit`, detection scope covering surface ceramics; and `ATT-0440` unchanged, keeping its `primary_observation` provenance and `observation_date`, gaining an evidential back-link to the Event.

The date then appears in two places, which needs a consistency check rather than a design change:

> **I8a — Where an examination Event and a rule-11 attestation record the same fieldwork, the attestation's `observation_date` falls within the Event's interval.**

### 14.5 Vocabulary additions

A new `EventCategory` and six sub-categories. Governance §5.5 requires three concrete cases per term; the corpus supplies them comfortably.

| Term | Concrete cases available |
|---|---|
| `investigation` *(category)* | all of the below |
| `site_visit` | **19 cases** — every `primary_observation` attestation in the corpus, all from `SRC-0065`, each with a dated visit (e.g. `ATT-0440`, 20 July 2005) |
| `survey` | the 1991 Özgen & Gates survey; the 2004 Mopsus Survey; Sinclair's survey at Zibaṭra |
| `material_reexamination` | Eger's 2005 autopsy of the Mopsus baskets; Eger's 2012 Bilkent re-examination |
| `excavation` | to be drawn from Phase 3 (Komana, Satala, Sebastopolis) |
| `remote_sensing_survey`, `geophysical_survey` | to be drawn from Phase 3; propose when cases exist rather than pre-emptively |

**Recommendation: propose `investigation`, `site_visit`, `survey` and `material_reexamination` now**, where the three-case requirement is already met, and hold `excavation`, `remote_sensing_survey` and `geophysical_survey` until Phase 3 supplies cases. This follows the corpus's own standing discipline against pre-emptive minting — the `SRC-0076` Theophylact pre-emptive mint remains a flagged orphan and is not a precedent to repeat.

Also required: the **examination relationship family** (§6.2) — `examined`, scope-qualified.

### 14.6 Costs, stated

1. **General Event queries must filter by category**, or they will return modern fieldwork alongside ninth-century sieges. This is what principle 8's controlled-vocabulary-through-attributes is for, and it is the ordinary cost of a single Event type.
2. **Examination Events fall outside the corpus's 640–1100 range.** This is not a violation — principle 14 says temporal boundaries are properties of analyses, not of the data model, and the corpus already carries 2005 dates in `observation_date`. But no query or export may assume all Events fall within the corpus range.
3. **An excavation physically transforms a site.** Modelling it as an Event is honest about that, and permits `damaged` and `terminated_phase` relationships from modern fieldwork where the evidence supports them — which is a small analytical gain rather than a cost.

**Verdict: accepted. §10.14 is revised accordingly, and the L1 wording is corrected at §3.1.**

---

## 15. Rules proposed for ratification — full text

Both are extraction and editorial discipline rather than data model. **Once ratified they belong in `docs/editorial_workflow.md` alongside rules 1–13, not in this ontology document.** They are given here in full so that a sentence can be approved or redlined rather than chased through cross-references.

### 15.1 Rule 14 — Site displacement

> **Rule 14 — Site displacement.** A displaced occupation is the **same Site** when its footprint overlaps or abuts the earlier one, or when the documentary or stratigraphic evidence treats the move as continuous. It is a **new Site** when the footprints are disjoint and the separation between their nearest edges exceeds the greatest dimension of the larger footprint. Where footprints are unknown — the majority case — the test rests on documentary and stratigraphic evidence of continuity alone. Where no test settles the case, it is recorded as a single Site, the alternative construal is recorded as an Interpretation, and the record is flagged for editorial review.

**On the fixed-distance question, plainly: the wording proposes no fixed distance, and is scale-relative by construction.** The threshold is "the greatest dimension of the larger footprint", which is a property of the sites being compared. Curtis's own example demonstrates it working:

- A **hilltop fort** of roughly 80 m across, displaced 400 m to a disjoint position: 400 m exceeds 80 m → **new Site.**
- A **lower town** of roughly 600 m across, displaced 400 m: the footprints almost certainly overlap, and even if disjoint, 400 m does not exceed 600 m → **same Site.**

Same distance, opposite judgements, because the threshold scales. **No fixed distance should be introduced, and the rule says so.**

**Two clauses worth attention when redlining.** First, *"nearest edges"* rather than centroid separation: centroid distance is badly misleading for elongated or irregular sites, and specifying edges avoids that. Second, the *"footprints unknown"* clause is not a marginal provision — **70% of the corpus's places carry no geometry at all** (§10.8), so for most records the documentary-and-stratigraphic test is the *only* test, and the rule must be usable without geometry.

### 15.2 Rule 15 — Dual aspect

> **Rule 15 — Dual aspect.** Where a thing is both a feature of the terrain and a locus of occupation — a bridge, a fortified pass, a tell that also serves as a landmark — create both a LandscapeFeature and a Site **only when the evidence distinguishes them**: that is, when there are attestations about the terrain feature and separately about the installation. Otherwise create only the aspect the evidence speaks to, and add the second when it earns records of its own. The two are linked by an explicit relationship; neither contains the other.

**Rationale.** Principle 7 requires that a fortified pass be two entities rather than one ambiguous object, which is right and which the catalogue mandates. Left unqualified, it also licenses creating two records for every bridge in the corpus on grounds of completeness. Rule 15 ties the multiplication to evidence, applying at the *instance* level the same recurrent-evidence logic that design note (b) applies at the *type* level. It is the main defence against a gazetteer bloating under a correct principle.

---

## 16. What carries forward, and what changes

### 16.1 Carries forward unchanged

**Hard rules 1–7** in full: no fabricated citations; no fabricated external identifiers; distinct evidential levels; provenance honesty and the secondary-source-mediated extraction pattern; the `editorial_review_required` discipline; validate before commit; honest framing in summaries.

**Rules 8–13** in full, including the three now documented (9, 10, 11) and the bare-mention rule — which becomes more load-bearing under a controlled vocabulary of components and functions.

**The two source categories** (authorless-but-citable; named tradent, unminted). **All fifteen provenance categories.** **The 1–5 confidence scale** with the specification's §6 definitions, applied per dimension. **The temporal framework** — `TemporalPrecision`, `DatingValue`, `DatingSystem`, `alternative_datings` with normalisation, AH and Byzantine AM handling — moved onto temporal assertions untouched. **`IdentificationStatus`, `CoordinateMethod`, `CoordinatePrecision`, `uncertainty_radius_m`, the EPSG:4326 mandate** — onto spatial assertions. **The three-layer record structure** (structured data / analytical summary / source evidence) as the per-record authoring discipline. **The master-record rule and identity-resolution procedure.** **Merge and split as logged, reversible, documented operations.** **The prohibition on silent reconciliation**, strengthened by the rule-10 correction. **Policy B**, extended by **Policy B-2** (§13). **The coordinate-adoption pattern**, which is the designated-assertion mechanism executed by hand. **Governance** §5.5, §5.6 and Appendix A. **Workflow states**, with `deprecated` becoming load-bearing under §10.12.

### 16.2 What changes

| Change | Scale | Why |
|---|---|---|
| `PlaceEntity` splits into Site / LandscapeFeature / Route / TerritorialUnit; Polity moves out of `records/places/` | 190 records | Four identity criteria in one type (§4.1) |
| `PlaceType` enum retired; five terms retired outright, four consolidated | 27 terms | Five bases of classification in one enum (§2.1) |
| `Coordinates` → spatial assertions with a designated pointer | 57 records | §5.6; zero records use `alternative_coordinates`, so nothing is lost |
| Point-only geometry → full geometry types | schema-level | Required by Route and by the two-nuclei case |
| `chronology`, `political_affiliation_history`, `administrative_status_history` → phases and phase-borne attributes | 7 records use these | §4.7 |
| **Phase** introduced | net-new | RQ2, RQ3 — the largest new capability |
| **Component** introduced | net-new | RQ2 |
| `ObservationRecord` renamed **Assertion** | 537 record-touches | Principle 11 (§5.1) |
| Assertion mandatory per attestation | 208 back-fills | §5.4 |
| `overall_confidence` retired | 325 records | Principle 6 (§8.3) |
| Rule-9 back-fill (empty `supporting_evidence`) | 57 records | Rule 9 now enforceable |
| Rule-10 promotion (prose cross-refs → relationships) | 29 records | Rule 10 now enforceable |
| Dossier unbundling | 4 records | Rule-10 correction (§5.5) |
| Attested names gain optional temporal validity | field only; no back-fill | Edge case 4 |
| Attestation subject links gain a reference mode | schema-level | Edge case 5 |
| Assertion gains polarity | schema-level | §10.14 |
| Examination Events; `detection_scope` | net-new + 4 vocabulary terms | §14 |
| `RelationshipType` extended across seven families | ~20 terms | §6.2 |
| `contains` narrowed to spatial containment | 27 records | §6.2 |

---

## 17. Consolidated migration assessment

### 17.1 Headline

> **1,423 nominal record-migrations collapse to 1,157 distinct records. 264 of the 266 duplications fall on the 190 place records.**
>
> **The migrations are not six projects. They are one schema migration with six content components, and the place migrations must be executed as a single pass.**

A further **296 records** (79 sources, 117 untouched relationships, 100 untouched interpretations) need only a `schema_version` migration — a mechanical residual sweep. Total corpus touched: **1,453**, i.e. all of it, but 296 of those touches are trivial.

### 17.2 Migration inventory

| ID | Migration | Touch set | Nominal records |
|---|---|---|---|
| M1 | `ObservationRecord` → `Assertion` rename | 254 observations + 270 attestations + 12 places + 1 interpretation | **537** |
| M2 | Assertion back-fill (I3) | 208 attestations | **208** |
| M3 | `overall_confidence` retirement | 190 places + 81 persons + 54 events | **325** |
| M4 | `PlaceType` rationalisation | 190 places | **190** |
| M5 | Geometry restructuring | 57 places | **57** |
| M6 | Interpretation work: rule-9 back-fill (57) ∪ rule-10 promotion (29) ∪ dossier unbundling (4) | 74 interpretations | **74** |
| M7 | Polity extraction from `records/places/` | 5 places | **5** |
| M8 | `contains` narrowing | 27 relationships | **27** |
| | **Nominal total** | | **1,423** |
| | **Distinct records** | | **1,157** |
| | **Duplication** | | **266** |

Counts verified against the clone. Note that all 12 places carrying an `OBS-` reference, all 57 coordinate-bearing places, all 5 polities and all 152 name-bearing places are **subsets of the same 190 place records** — which is where the duplication concentrates and why sequencing matters.

### 17.3 New records created

| Source | Estimate |
|---|---|
| Assertions from M2 back-fill | ≤ 208 (fewer where a datum merges into an existing proposition) |
| Spatial assertions from M5 | 57 |
| Relationships from rule-10 promotion | ≥ 29 |
| Interpretations from dossier unbundling | ~ +8 net (4 records → ~12) |
| **Migration subtotal** | **~300** |
| Phases, Components, examination Events | net-new construction, unbounded — not a migration |

### 17.4 Mechanical versus judgement-requiring

| Migration | Class | Characterisation |
|---|---|---|
| **M1** rename, 537 | **Mechanical** | Identifier and field-name substitution. No content decisions. |
| **M3** `overall_confidence`, 325 | **Mechanical** | Field deletion. |
| **M5** geometry, 57 | **Mechanical — unexpectedly** | **Zero places use `alternative_coordinates`**, so every one of the 57 has exactly one coordinate and designation is trivially that one. The three genuinely competing cases (Zibaṭra, Bālis, Malaṭya) were already adjudicated in post-Phase-2 Items B, C and D. This migration was expected to be the hardest and is in fact among the easiest. |
| **M7** Polity extraction, 5 | **Mechanical** | Relocation; the `ENT-POL-` prefix already carries the semantics. |
| **M4** `PlaceType`, 190 | **Mixed** | ~156 mechanical-with-review (settlement, city, village, fortification, fortress, castle, monastery, river, mountain, pass → one clear target each). **~31 require adjudication**: the 15 `region` records splitting between physiography and jurisdiction, 4 `frontier_zone`, 7 `administrative_unit`, 2 `other` (canals), 2 `bridge` (Rule 15), 1 `battle_site`. **3 require argument**: `ENT-PLC-0017` Bolkardağ mining district (feature, resource zone, or analytical region?); `ENT-PLC-0013` Cappadocia and `ENT-PLC-0168` Armenia (cultural-geographical names that were also jurisdictions — and the answer may differ per attestation, which is itself informative). |
| **M2** back-fill, 208 | **Split unknown — requires scoping** | Most will be mechanical one-to-one wrappers; an unknown subset restate propositions already in the corpus and require a merge decision. **I decline to estimate the split without reading the 208.** Per the Item-G precedent, a read-only sweep determines it before any patch. |
| **M6** interpretations, 74 | **Judgement** | The 57 rule-9 back-fills require reading each argument to identify which attestations support it. The 29 rule-10 promotions are near-mechanical in extraction (the prose already names the target) but the relationship *type* is a judgement. The 4 unbundlings are the heaviest per record: scholar, date and confidence must be extracted per position from prose. |
| **M8** `contains`, 27 | **Judgement, small** | Each record is doing one of three jobs; determining which requires reading. |

**Summary:** 924 of 1,157 distinct records (80%) are mechanical; ~233 require judgement, concentrated in 31 place adjudications, 74 interpretations, 27 relationships, and an unknown share of the 208 attestations.

### 17.5 One recommended non-migration

**Do not back-fill name temporal validity.** Add the field; populate going forward. Dating a name's currency is a scholarly claim, and 152 speculative datings would be worse than none. This removes 152 records from the migration at no analytical cost.

### 17.6 Recommended sequencing

| Step | Work | Records | Class | Why here |
|---|---|---|---|---|
| **0** | Ratify and document rules 9, 10, 11, 14, 15 in `editorial_workflow.md` | 0 | — | **Prerequisite.** Rules 14–15 govern the M4 adjudications; rules 9–10 govern M6. Adjudicating before the rules exist means re-adjudicating. |
| **1** | Schema v3 + validators for I2, I3, I5, I5a, I5b, I11 | 0 | — | **Item-G discipline: checks first.** Confirm the validators report exactly the pre-identified counts — 208 (I3), 57 (I5), 29 (I5a), 0 (I2, I5b) — on the unmigrated corpus. A failing-CI moment that matches the scan is positive confirmation the rules catch what was predicted and nothing else. |
| **2** | **M1 rename**, alone | 537 | Mechanical | First and alone. Every later patch would otherwise be written against a moving identifier, and the rename is corpus-wide. |
| **3** | **Place pass**: M4 + M5 + M7 + M3(places) + name field + schema migration | 190 | Mixed | **The critical consolidation.** These five migrations touch the same 190 records; done separately that is 454 record-opens instead of 190. Preceded by a read-only scoping pass on the 31 adjudications and 3 arguments. |
| **4** | **Person/Event pass**: M3 + schema migration | 135 | Mechanical | Trivial once the schema exists. |
| **5** | **Attestation pass**: M2 + reference mode + polarity + schema migration | 477 | Mixed | After step 2, so assertions are not created under a name about to change. Preceded by a read-only scoping pass to determine the mechanical/merge split of the 208. |
| **6** | **Interpretation pass**: rule-9 back-fill + rule-10 promotion + unbundling + schema migration | 74 | Judgement | After step 2 (`INT-0174` carries an `OBS-` reference) and after step 5 (rule-9 back-fill cites attestations, which step 5 has finished touching). |
| **7** | **Relationship pass**: `contains` narrowing + vocabulary extension + new relationships from step 6 | 27 + ~29 new | Judgement | After step 6, which generates the rule-10 relationships. |
| **8** | **Residual schema sweep**: 79 sources + 117 relationships + 100 interpretations | 296 | Mechanical | Everything not otherwise touched. |
| **9** | **Net-new construction**: Phase, Component, examination Events | — | — | Not a migration. Requires the migrated spatial types to attach to. |

**Two practical notes on the critical path.**

*Vocabulary extension has governance lead time.* The seven relationship families and four examination terms each require Board majority and three concrete cases (governance §5.5). Execution sits at step 7, but the **proposals should be filed at step 0**, or step 7 stalls waiting on a decision process that could have run in parallel throughout.

*Scoping precedes steps 3, 5, 6 and 7.* Each is a read-only sweep in the Item-F/G pattern. This is standing practice, and its value is not hypothetical: the Item-F sweep surfaced Item G, and the scans run for this document surfaced the 57-record rule-9 breach, which nobody was looking for.

---

## 18. Proliferation audit

### 18.1 Each type against the admission test

| Type | Distinct identity criterion? | Question it earns | Verdict |
|---|---|---|---|
| SpatialThing | abstract; holds no records | principle 7 | structural |
| Site | physical continuity of occupied locus | RQ2, RQ1, RQ3 | **earns** |
| LandscapeFeature | continuity of form and affordance | RQ1 — passes, crossings, corridors | **earns** |
| Route | continuity of corridor, *not* geometry | RQ1 — route families | **earns**; mandated by principle 8 |
| TerritorialUnit | unbroken administrative succession | RQ3 — the ʿawāṣim's creation | **earns** |
| Component | dependent fabric continuity within a Site | RQ2 — independent component chronologies | **earns** |
| Phase | dependent (subject, interval, state) | RQ2, RQ3 | **earns**; the mechanism of principle 2 |
| Event | kind + time + place + participants | RQ3, RQ4 (examinations) | **earns**; mandated by the capability table |
| Polity | continuity of political succession | RQ3 — distribution of authority | **earns, weakest** — watch it (§4.9) |
| Person | prosopographic identity | RQ3, RQ4 (authorship) | **earns** under design note (b)'s own threshold |
| Source | the work, not edition or witness | RQ4 | **earns**; existing |
| Attestation | (source, location, datum) | RQ4 | **earns**; existing |
| Assertion | (proposition, subject set) | RQ4 — multiple attestation | **earns**; prospective case at §5.4 |
| Interpretation | (scholar, publication, argument) | RQ4 | **earns**; existing |
| Relationship | (type, endpoints, temporal scope) | RQ1, RQ2, RQ5 | **earns**; mandated by principle 9 |
| AnalyticalRegion | (author, name, version, membership) | RQ5, contract §8 | **earns**; design note (a) |

### 18.2 Net effect

The corpus has 8 declared record types plus an undeclared Polity carried by identifier prefix — 9 in practice. The specification has 16, of which:

- **4 carry forward unchanged** — Source, Attestation, Interpretation, Relationship
- **1 is renamed** — Observation → Assertion
- **1 is formalised** — Polity, currently a `place_type` with its own prefix
- **1 is retained minimally** — Person
- **1 carries forward** — Event, extended by vocabulary to cover examinations
- **1 splits four ways** on four distinct identity criteria — Place → Site, LandscapeFeature, Route, TerritorialUnit
- **1 is abstract and holds no records** — SpatialThing
- **3 are genuinely new** — Component, Phase, AnalyticalRegion

**Genuinely new machinery: three record types.** Everything else is carried forward, renamed, formalised, or split on criteria the corpus was already conflating.

### 18.3 What the test removed

Applied to the existing schema, the same test **retires five `PlaceType` terms as category errors** (`city`, `village`, `capital_city`, `ruined_site`, `battle_site`), **consolidates four into one** (`fortification`, `fortress`, `castle`, `kastron`), **retires one as irreducibly ambiguous** (`region`), **retires one field required on 325 records** (`overall_confidence`), and **rejects fourteen candidate types** (§4.11) — including `AnalyticalWindow` and `ExaminationEvent`, both of which arrived in this round as reasonable-looking proposals and both of which failed on the same ground: shared identity criterion, difference by one dimension.

The register is not the result of adding what seemed useful. Several of the things most wanted are in §4.11.

---

## 19. Decisions register and forward sequencing

### 19.1 Every v0.1 open question, resolved

| # | Question | Resolution |
|---|---|---|
| 1 | Observation → Assertion rename | **RESOLVED — approved.** §5.1 |
| 2 | Person retained or deferred? | **RESOLVED — Person retained, Community/Household/Population deferred.** §4.10 |
| 3 | Assertion mandatory or optional? | **RESOLVED — mandatory (I3)**, on the prospective argument. §5.4 |
| 4 | `overall_confidence` retired or redefined? | **RESOLVED — retired**, within the schema-migration pass; deferral is the expensive option. §8.3 |
| 5 | AnalyticalRegion spatial only, or with a temporal extent? | **RESOLVED — optional temporal extent; null means unbounded; intersection rule; no silent widening.** §7.3 |
| 6 | Rule 14 wording | **RESOLVED — full text at §15.1**, scale-relative, no fixed distance |
| 7 | Dual-aspect rule wording | **RESOLVED — full text at §15.2 as Rule 15** |
| 8 | Rules 9, 10, 11 | **RESOLVED — 9 and 10 recovered, 11 ratified as new** (2026-07-23). §0.2 |

### 19.2 Questions raised in the v0.2 brief, resolved

| Question | Resolution |
|---|---|
| Designation versioning | **RESOLVED — Policy B-2**, §13. Reproduces all three coordinate adoptions exactly; adds a no-cascade rule and separates `schema_version` from designation. |
| Examination-as-Event and the L1 check | **RESOLVED — clears L1 twice over**, §14. §10.14 revised from a flat gap to a narrowed three-way distinction; L1's wording corrected at §3.1. |
| Consolidated migration assessment | **DELIVERED**, §17. |

### 19.3 Explicit deferrals, with resolving conditions

Only three, and each carries the condition that would resolve it.

| Deferral | Resolving condition |
|---|---|
| **`phasing_scheme` discriminator (§10.13, option ii)** | Resolves when the corpus holds a site with two published, incompatible phase divisions. **Expected during Phase 3** (Komana, Satala, Sebastopolis). Until then, option (i). *Actionable now:* the logical model must not build a uniqueness constraint assuming one phasing per subject. |
| **Community / Household / Population types (§4.10)** | Resolves when recurrent evidence about non-individual human groups accumulates and a research question requires querying it. §5.7 guarantees admission costs no epistemic-layer change. |
| **`excavation`, `remote_sensing_survey`, `geophysical_survey` vocabulary terms (§14.5)** | Resolves when Phase 3 supplies three concrete cases each, per governance §5.5. Proposing them earlier would repeat the flagged `SRC-0076` pre-emptive-mint pattern. |

### 19.4 Retained limitations

Two, both stated rather than smoothed:

- **Competing phase divisions (§10.13)** — handled by editorial adjudication plus an Interpretation, not by the model. The rival periodisation exists as prose. Expected to bind in Phase 3.
- **Negative evidence (§10.14)** — narrowed to a three-way queryable distinction, conditional on `detection_scope`. The irreducible residual is corpus completeness, not model capability, and no ontology can fix it.

Both will be met in the writing as well as in the database: an RQ2 argument about contraction reports its evidential coverage, as an RQ1 spatial analysis reports its geometric coverage (§10.8).

### 19.5 Forward sequencing — confirmed

Once this document is frozen, the next deliverables in order:

1. **Ratification and documentation** — rules 9, 10, 11, 14, 15 into `docs/editorial_workflow.md`. Zero records. **Prerequisite to everything else**, because rules 14–15 govern the place adjudications and rules 9–10 govern the interpretation pass. Vocabulary-extension proposals (§6.2, §14.5) filed here so governance lead time runs in parallel.

2. **The query register** — one executable query or defined workflow per subordinate research question, **twenty-two in all**, each with its expected result shape. **Written before the logical model, as its acceptance test**, so the logical model is designed against executable requirements rather than against prose. This is the deliverable that converts "query coverage" from an assertion into a test.

3. **The `RelationshipType` vocabulary extension** — seven families, roughly twenty terms (§6.2), plus the four examination terms (§14.5). Governance §5.5: Board majority, three concrete cases per term. Filed at step 1, executed here.

4. **The logical model**, tested against the query register.

5. **The migration**, per the sequencing at §17.6, beginning with schema and validators and only then touching records.

Deliverables 2 and 3 are independent of each other and can run in parallel; both must precede 4, and 4 must precede 5.

---

*End of conceptual ontology specification v0.2. This document is offered as stable and freezable. It supersedes v0.1 and is self-contained.*
