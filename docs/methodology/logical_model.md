# Logical Data Model — Byzantine-Islamic Frontier Database

**Status:** draft specification, **held for review**. Delivery is not commit.
**Realises:** the frozen `conceptual_ontology.md` (v0.2) and **only** that. No v2_preview construct is adopted (§0.3).
**Expressibility target:** the nineteen-item edge-case enumeration of Step 1 (Deliverable B).
**Purpose:** complete enough on entities, attributes, keys, cardinalities and constraints that Step 3 can build a checkable schema from it **without further design decisions**.
**Read against:** commit `4365b88`. No migration, no fixture, no records touched. This is a specification, not executed.
**Revision note (this draft):** closes four held items — heredoc-leak removal with a full-boundary scan (§0.4), Assertion subject-set derivation (§2.3a), invariant completeness incl. I5a/I1/I12 (§6), and the ID-prefix decision (§0.5). Assembled by single write, not concatenation.

**Notation.** Entities carry an identity key (**PK**) and, where identity is dependent, the parent whose deletion cascades. Attributes list type and null-discipline. Relationships are first-class records (principle 9), specified with endpoint types, direction, cardinality `(source-side : target-side)`. `1`, `0..1`, `1..n`, `0..n`, `m:n` have their usual meanings. Controlled vocabularies are named; term lists are the §5.5 vocabulary files, not restated.

---

## 0. Framing

### 0.1 Three layers, one storage model

The model preserves the ontology's three layers (§3) as a property of *reference direction*, not of separate stores. Every record type is tagged **D** (domain), **E** (epistemic), **S** (structural), or **A** (analytical). Layering invariants L1 and L2 (§3.1) are realised as constraints on which foreign keys may exist, stated in §8.

### 0.2 What "the model realises the ontology" means here

Each entity maps to one ontology type. Where the ontology carries a datum as a *designated pointer into the epistemic layer* rather than as a column (geometry, dating — §5.6), the model does the same: the domain record holds a nullable FK to a designated Assertion, and the competing values live as Assertion rows. A model that flattened these into columns would pass items instantiating a single geometry and fail items 7 and 9. Stated now because it is the decision most easily lost in translation to a relational schema.

### 0.3 Excluded: v2_preview constructs

`FuzzyRegion` and `WitnessRecord` appear in `v2_preview/` and are **not part of the frozen ontology**. Excluded.

- **FuzzyRegion** — its capability (spatial extent varying by time-slice) is **already delivered** by the frozen design: a phased subject with a designated spatial assertion per Phase (§5.6, items 7/9). **Mapped onto frozen constructs; not adopted.**
- **WitnessRecord** — manuscript-witness modelling has **no frozen counterpart**. Source identity is "the work, distinct from edition and witness" (§5.2, hard rule 3). A genuine extension beyond the frozen ontology, not a mapping. **Flagged, not adopted.** If wanted later, a §5.8 amendment, not a logical-model decision.

### 0.4 Assembly integrity

The prior draft leaked shell scaffolding (an `ENDFILE` delimiter and an `echo`/`wc` line) at the join between §2.6 and §3, because it was assembled by concatenating heredocs and that boundary was the seam. **This draft is written in a single pass, so no inter-section seam exists.** A full-boundary scan was nonetheless run over the reassembled file for the same leak class — heredoc delimiters, shell commands, and tool scaffolding at every section boundary — and is confirmed clean in the delivery response.

### 0.5 Identifier decision

Recorded here because it governs keys throughout and was the one key-decision the prior draft left proposed rather than settled.

- **`ASR-` supersedes `OBS-` for Assertion — ADOPTED.** It rides the M1 rename already being paid for; no additional cost.
- **`ENT-CMP-` for Component — ADOPTED.** Component is a genuinely new type with no prior identifiers, so a fresh opaque prefix is free and encodes nothing mutable.
- **`ENT-SIT-` / `ENT-LFT-` / `ENT-RTE-` / `ENT-TER-` for the spatial four — RETIRED, not adopted.** Identifiers for the spatial four stay **opaque and stable**: the current `ENT-PLC-` prefix (or a single opaque spatial prefix) is retained, and the four-way type is carried in a **column** (`spatial_type`), not in the identifier.

  **Reason, recorded as required.** M4's own adjudications establish that re-typing across the four spatial subtypes is **recurrent**: `region` records split between physiography (→ LandscapeFeature) and jurisdiction (→ TerritorialUnit), and the type may differ per attestation (Cappadocia, Armenia). A subtype-encoded identifier would force an ID re-issue on every re-typing, and re-issuing an identifier breaks every cross-reference to it. **Identity must not encode a mutable property.** `spatial_type` is exactly such a property; it belongs in a column, and the identifier stays opaque so that a re-typing is a column update, not an identity change.

  Consequence for the tables below: the four spatial entities share the `ENT-PLC-` identifier space and are distinguished by a `spatial_type` discriminator. The per-type attribute sets still differ; the *identifier* does not encode which. Component and the `ASR-` rename are unaffected by this, and both follow the same principle — Component's prefix is fresh precisely because it encodes a type that its records will never leave (a Component cannot become a non-Component), whereas a spatial record's subtype is mutable.

---

## 1. Domain-layer entities

### 1.1 SpatialThing *(abstract — D)*

Not a stored table of its own; an abstract supertype whose four concretions share the spatial primitives (§4.1). Realised as a **shared structural contract**: each concrete spatial entity carries the same four capabilities — attested names, spatial assertions with a designated pointer, phases, and eligibility as a spatial-relationship endpoint — and a `spatial_type` discriminator (§0.5). Whether Step 3 implements this as a supertable with subtype tables or as one table with a discriminator and nullable per-type columns is a *physical* decision left open; the logical requirement is that the four share these primitives, share one opaque identifier space, and that a spatial relationship may take any of them as an endpoint.

`spatial_type` enum: `site` / `landscape_feature` / `route` / `territorial_unit`. **Mutable** — a re-typing is a column update, never an ID re-issue (§0.5).

### 1.2 Site *(D, SpatialThing — `spatial_type = site`)*

**Represents.** A bounded locus of human occupation or use (§4.2).

**Identity — physical continuity of the occupied locus.** PK in the shared `ENT-PLC-` space. Identity is **not** nominal, **not** functional, and **gap-tolerant**: an occupation gap does not break it (item-15 constraint, §4).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `id` | ID (`ENT-PLC-`) | PK | opaque; shared spatial space |
| `spatial_type` | enum | not null | = `site` |
| `standardised_name` | text | not null | |
| `designated_spatial_assertion` | FK to SpatialAssertion | **nullable** | item 8: a Site may have zero geometry |
| `identification_status` | enum | not null | identified / probably / approximately / disputed / unidentified / hypothetically |
| `identification_confidence` | int 1-5 | not null | identification dimension only |
| `existence_interval` | derived | — | union of phase intervals (I7); **computed, never stored** |

Names, geometry, dating, function, rank: **not columns.** `overall_confidence`: **absent** (retired). Phases: `0..n`, may not overlap within a scheme (I6, Demand-D).

### 1.3 LandscapeFeature *(D, SpatialThing — `spatial_type = landscape_feature`)*

**Represents.** An extended terrain element conditioning movement, settlement or production, not itself a locus of occupation (§4.3). **Identity — continuity of physical form and affordance.**

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `id` | ID (`ENT-PLC-`) | PK | opaque; shared spatial space |
| `spatial_type` | enum | not null | = `landscape_feature` |
| `standardised_name` | text | not null | |
| `feature_type` | enum | not null | pass / ford / crossing / defile / river / valley / range / plain / basin / marsh / spring / canal / ... |
| `origin` | enum | not null | natural / modified / anthropogenic |
| `designated_spatial_assertion` | FK to SpatialAssertion | nullable | |
| `identification_status` | enum | not null | |
| `identification_confidence` | int 1-5 | not null | |

Phases: `0..n`, usually zero (§4.3).

### 1.4 Route *(D, SpatialThing — `spatial_type = route`)*

**Represents.** A corridor of movement between termini (§4.4). **Identity — continuity of corridor under the same constraints, explicitly not geometry.**

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `id` | ID (`ENT-PLC-`) | PK | opaque; shared spatial space |
| `spatial_type` | enum | not null | = `route` |
| `standardised_name` | text | not null | |
| `route_class` | enum | not null | documented / modelled / inferred / **family** |
| `designated_spatial_assertion` | FK to SpatialAssertion | nullable | a family may hold none |
| `identification_confidence` | int 1-5 | not null | |

Family membership is a relationship, not a column — §3, `member_of_route_family`, **Demand-18 (M:N)**. Phases: `0..n`.

### 1.5 TerritorialUnit *(D, SpatialThing — `spatial_type = territorial_unit`)*

**Represents.** A jurisdiction (§4.5). **Identity — unbroken chain of administrative succession.** **Gap-breaking**: dissolution then recreation is **two** units, unless sources treat the later body as a restoration (item-16 constraint, §4).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `id` | ID (`ENT-PLC-`) | PK | opaque; shared spatial space |
| `spatial_type` | enum | not null | = `territorial_unit` |
| `standardised_name` | text | not null | |
| `unit_type` | enum | not null | thughur / awasim / jund / kura / theme / kleisoura-command / ... |
| `constituted_date` | TemporalValue | nullable | |
| `dissolved_date` | TemporalValue | nullable | bounded lifecycle |
| `designated_spatial_assertion` | FK to SpatialAssertion | nullable | boundaries are the weakest geometry; often none |

`held_by` is a phased relationship, not a column. Extent is **never** a Polity column (§1.8). Phases: `0..n`.

### 1.6 Component *(D — dependent)*

**Represents.** A constituent part of a Site (§4.6). **Identity — continuity of physical fabric within its parent Site. Fabric, not footprint.** PK `component_id` (`ENT-CMP-`, adopted §0.5). **Dependent:** deletion of the Site cascades; under a Site split, components follow the fabric (I13). Item-19a constraint.

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `component_id` | ID (`ENT-CMP-`) | PK | |
| `parent_site` | FK to Site | **not null** | dependency; cascade delete |
| `component_type` | enum | not null | wall / tower / gate / church / mosque / cistern / bath / kiln / workshop / field-system / cemetery / quarry / ... |
| `designated_spatial_assertion` | FK to SpatialAssertion | nullable | |

**No footprint-based identity key.** Two components on one footprint are distinct if fabric is distinct (item 19a). Succession is the `succeeds` relationship, Component-to-Component (§3, Demand-B). Phases: `0..n`, may overlap (I6), unlike Site phases.

### 1.7 Event *(D)*

**Represents.** A bounded historical happening, including acts of examination (§4.8, §14). **Identity — same kind + overlapping time + same place(s) + same principal participants.** PK `event_id` (`ENT-EVT-`, retained — opaque already).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `event_id` | ID (`ENT-EVT-`) | PK | |
| `event_type_primary` | enum | not null | military / construction_infrastructure / administrative / demographic / political / diplomatic / environmental / religious / **investigation** |
| `event_type_sub` | enum | nullable | incl. site_visit / survey / excavation / material_reexamination under investigation |
| `start_date` | TemporalValue | nullable | |
| `end_date` | TemporalValue | nullable | |
| `detection_scope` | structured | nullable | **item 14**: on investigation events |
| `interaction_mechanism` | enum **multi** | nullable | Amendment 1; repeatable; orthogonal to `event_type` |
| `identification_confidence` | int 1-5 | not null | carries "did it happen" |

Parent/child nesting via `parent_event_of` (§3), `0..n`.

### 1.8 Polity *(D)*

**Represents.** A corporate political actor (§4.9). PK `polity_id` (`ENT-POL-`, formalised out of `records/places/` at M7 — opaque already).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `polity_id` | ID (`ENT-POL-`) | PK | |
| `standardised_name` | text | not null | |
| `identification_confidence` | int 1-5 | not null | |
| **extent** | — | — | **not stored**; derived from held TerritorialUnits |

### 1.9 Person *(D)*

**Represents.** A named historical individual (§4.10). PK `person_id` (`ENT-PERS-`, retained — opaque already).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `person_id` | ID (`ENT-PERS-`) | PK | |
| `standardised_name` | text | not null | |
| `floruit` | TemporalValue | nullable | |
| `identification_confidence` | int 1-5 | not null | |

### 1.10 AttestedName *(D — dependent, shared by all SpatialThings)*

**Represents.** One attested name of a spatial entity, with its own provenance (item 4).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `name_id` | ID | PK | |
| `subject` | FK to SpatialThing | not null | polymorphic over the shared spatial space (§8, L-poly) |
| `form` | text | not null | |
| `language` | enum | nullable | |
| `script` | enum | nullable | |
| `name_type` | enum | nullable | |
| `temporal_validity` | TemporalValue | **nullable** | item 4: optional; **not back-filled** |
| `supporting_attestation` | FK to Attestation | not null | every name is evidenced |

---

## 2. Epistemic-layer entities

### 2.1 Source *(E)*

**Represents.** A work that generates evidence (§5.2). PK `source_id` (`SRC-`). Identity = the work, distinct from edition and witness (hard rule 3). No certainty dimension; carries reliability/bias. `author_unnamed: bool` supports source category (A).

### 2.2 Attestation *(E)*

**Represents.** One source's statement of one datum, with provenance (§5.3). PK `attestation_id` (`ATT-`). **Identity — (source, location-in-source, datum).**

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `attestation_id` | ID (`ATT-`) | PK | |
| `source` | FK to Source | **not null, exactly one** | rule 3 |
| `citation` | text | not null | |
| `paraphrase` | text | nullable* | |
| `direct_quotation` | text | nullable* | *rule 8 / I2: **at least one of the two** non-empty |
| `provenance_category` | enum | not null | 15-term vocab |
| `observation_date` | TemporalValue | conditional | **rule 11 / I5b**: present iff `provenance_category = primary_observation` |
| `evidential_confidence` | int 1-5 | not null | sixth quantity (§8.2); distinct from the five |
| `interaction_mechanism` | enum **multi** | nullable | Amendment 1 |

**Subject links** are QualifiedSubjectLink rows (§2.5), not a plain list.

### 2.3 Assertion *(E)*

**Represents.** The deduplicated proposition that one or more attestations support (§5.4). PK `assertion_id` (**`ASR-`, adopted §0.5**, superseding `OBS-` — the record currently named `ObservationRecord`; rename is M1, a rename not a capability change).

**Identity — (proposition, subject set).** The subject set is **derived**, per §2.3a.

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `assertion_id` | ID (`ASR-`) | PK | |
| `proposition` | text | not null | |
| `assertion_kind` | enum | not null | general / **spatial** / **temporal** / functional / identification |
| `assertion_polarity` | enum | not null, default `asserted` | **item 14**: asserted / denied |
| `supporting_attestations` | (relationship set) | **1..n** | **I3 / I4**: at least one (§2.6, §6) |

### 2.3a Assertion subject set — derivation and folding rule *(closes held item 2)*

The prior draft gave Assertion identity as `(proposition, subject set)` but provided no path from an Assertion to its subject set: the Assertion table had no subject column, and QualifiedSubjectLink carried only an Attestation FK. **Resolved by option (a): the subject set is derived, with an explicit folding rule.** No Assertion-side subject link is added; the derivation is stated so it is not a Step-3 decision.

**Derivation.** An Assertion's subject set is the fold, over its supporting Attestations, of those attestations' QualifiedSubjectLinks: the subject set of an Assertion is the union of `QualifiedSubjectLink.subject` for every QualifiedSubjectLink whose `attestation` is one of the Assertion's supporting attestations, filtered by the reference-mode rule below.

The §2.5 phrase "from an Attestation (or Assertion)" is corrected: **subject links attach to Attestations only.** An Assertion reaches subjects **through** its attestations, never directly. §2.5 is amended accordingly.

**Folding rule for `reference_mode` — the part that was undefined:**

1. **`definite` links enter the dedup key.** A definite-linked subject is part of the proposition's subject set and part of Assertion identity. Two attestations whose definite subject sets and proposition coincide support **one** Assertion.

2. **`collective` links enter the dedup key, as a set member.** A source speaking of several subjects together asserts something of the collective; the collective membership is part of what is asserted, so it is part of identity.

3. **`candidate` links do NOT enter the dedup key.** A candidate link records unresolved ambiguity about *which* subject is meant (item 5, "one name, several places"). Ambiguity about the referent is not part of the proposition asserted — the source asserted one thing about one place, and the corpus does not yet know which. Folding candidate subjects into identity would let an *editorial* uncertainty determine *propositional* identity, which inverts §4 of the ontology: the object is not its interpretation.

**Consequence for the candidate case, stated explicitly (the second half of the held question).** A candidate ambiguity yields **one Assertion over the definite/collective subject set**, carrying the candidate-linked subjects as *non-identifying* associated subjects. It does **not** yield multiple Assertions, one per candidate. The competing readings of which candidate is correct are **Interpretations** (item 5's resolution), not distinct Assertions. This keeps a single proposition single while its referent is disputed, and routes the dispute to the layer built for disputes.

**Worked instance (Hisn X, candidate between two sites).** One Attestation, `definite` links to none, `candidate` links to Site-P and Site-Q. One Assertion (the proposition "a fortress named Hisn X exists / did Y"), subject set from the definite/collective fold (here empty of identifying members), Site-P and Site-Q carried as non-identifying candidate subjects. Two Interpretations argue P vs Q. **Not** two Assertions.

**Two-attestation consequence, stated explicitly.** Two *pure-candidate* attestations — each with no definite or collective link — whose propositions coincide and whose candidate sets are **disjoint** fold into **one** Assertion, pooling their candidate subjects. This is intended: a named referent with a disputed location is **one proposition**, and the dispute over which candidate is meant is routed to Interpretations, not multiplied into distinct Assertions. Attestation-1 (candidates P, Q) and Attestation-2 (candidates R, S), same proposition, produce one Assertion carrying {P, Q, R, S} as non-identifying candidate subjects — not two Assertions split on candidate set.

**Why this corner needs stating — the load-bearing half.** The pure-candidate case is the **only** dedup case with no subject-set anchor. Everywhere else the subject set constrains identity: two attestations dedup to one Assertion only if their identifying subjects coincide, so the subject set is a check against accidental over- or under-pooling. In the pure-candidate case the identifying subject set is empty by rule 3 above, so **proposition wording alone carries identity** — and nothing in the schema enforces proposition-wording consistency, because `proposition` is free text. The pooling default is correct and defensible, but it rests here on an **external editorial discipline** (that two attestations of the same claim are worded consistently) rather than on a constraint the model imposes. A Step-3 author must see that identity rests on proposition text alone in this one case, rather than derive it on encountering a mispooled pair; that is the point of recording it, and it is treated as the sixth adversarial case at §4 and §10.

**Derived, not stored.** The subject set is computed from the attestation links, never stored on the Assertion, so it cannot drift from the links it derives from. Step 3 realises it as a view or a derivation, not a column.

### 2.4 SpatialAssertion / TemporalAssertion payloads *(E — Assertion specialisations)*

Per §5.6, geometry and dating are **typed roles of Assertion**, not types.

**SpatialAssertion** (an Assertion, `kind = spatial`):

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `geometry` | geometry(point / linestring / polygon / multipolygon) | not null | **full geometry types** (items 7, 9); EPSG:4326 |
| `coordinate_method` | enum | not null | |
| `coordinate_precision` | enum | nullable | |
| `uncertainty_radius_m` | numeric | nullable | |
| `spatial_confidence` | int 1-5 | not null | spatial dimension |
| `attaches_to` | FK to (SpatialThing OR Phase) | not null | entity-level or phase-level; I10 |

**TemporalAssertion** (an Assertion, `kind = temporal`):

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `dating` | TemporalValue | not null | normalised_start / normalised_end; AH and Byzantine AM |
| `temporal_precision` | enum | not null | |
| `dating_system` | enum | not null | |
| `chronological_confidence` | int 1-5 | not null | |
| `attaches_to` | FK to (Phase OR Event OR bounded entity) | not null | |

**Designation.** Each subject holds **at most one** `designated_spatial_assertion` and **at most one** `designated_temporal_assertion` (I11), each a nullable FK **on the domain record** (§5.6). Non-designated competing assertions remain as rows, queryable (items 7, 9). Designation carries a recorded rationale (I9); the designated value must be one of the subject's own asserted values.

### 2.5 QualifiedSubjectLink *(E — dependent on Attestation)*

**Represents.** The link **from an Attestation** to a domain subject, qualified by reference mode (item 5, §5.3). **Attestation-side only** — corrected from the prior draft's "(or Assertion)"; Assertions reach subjects through their attestations (§2.3a).

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `link_id` | ID | PK | |
| `attestation` | FK to Attestation | not null | the only subject-bearing FK |
| `subject` | FK to **any domain entity** | not null | polymorphic (§8, L-poly) |
| `reference_mode` | enum | not null | **definite / candidate / collective** |
| `identification_confidence` | int 1-5 | not null | **its own** |

A `candidate` link represents "one name, several places" without asserting either (item 5); its folding into Assertion identity is defined at §2.3a (it does not fold in).

### 2.6 Interpretation *(E)*

**Represents.** One scholar's argued reading (§5.5). PK `interpretation_id` (`INT-`). **Identity — (scholar, publication, argument).**

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `interpretation_id` | ID (`INT-`) | PK | |
| `scholar` | text | not null | |
| `publication` | FK to Source | not null | |
| `argument` | text | not null | |
| `supporting_evidence` | (relationship set) | **1..n**, **ATT-only** | **rule 9 / I5**: at least one, cites Attestations never Sources |
| `argumentative_confidence` | int 1-5 | not null | seventh quantity (§8.2) |

---

## 3. Relationships (first-class — S)

All relationships are records (principle 9). Common structure:

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `relationship_id` | ID (`REL-`) | PK | |
| `rel_type` | enum | not null | vocab §6.2 / §5.5 |
| `source_entity` | FK to any record | not null | **polymorphic; same-type pairs admitted — Demand-B** |
| `target_entity` | FK to any record | not null | |
| `temporal_scope` | TemporalValue | nullable | I8 |
| `relationship_confidence` | int 1-5 | not null | fifth dimension, borne only here |
| `linked_attestations` | (set) | 0..n | structural relationships may inherit support |

**Endpoint typing (Demand-B).** `source_entity` and `target_entity` reference the shared identifier space; the model **does not assume distinct endpoint types**. Same-type pairs are valid. The one same-type pair the enumeration forces is **Component to Component (`succeeds`)**, item 19a — called out so Step 3 cannot omit it in a cross-type-dominated vocabulary.

| `rel_type` | Endpoints | Cardinality | Serves |
|---|---|---|---|
| `controls`, `overlooks` | Site to LandscapeFeature | m:n | item 1 |
| `member_of_route_family` | Route(track) to Route(family) | **m:n** | **item 18 — no single-parent constraint** |
| `succeeds` (component) | **Component to Component** | 1:1 per succession, chainable | **item 19a — same-type** |
| `succeeds` (site) / `restores` | Site to Site / TerritorialUnit to TerritorialUnit | 1:1 | items 2, 16 |
| `different_from`, `alternative_identification_of` | Site to Site | m:n | item 5 |
| `produced_phase`, `terminated_phase`, `damaged` | Event to (Phase OR Site) | m:n | RQ3 (via Phase) |
| `contradicts`, `revises`, `corroborates`, `supersedes_attestation` | Interpretation to (Interpretation OR Attestation) | m:n | item 11 |
| `co_located_aspect` (dual-aspect link, Demand-17) | LandscapeFeature to Site | 1:1 | **item 17 — explicit link, neither contains** |

**No `contains` between a dual-aspect LandscapeFeature and Site.** `contains` narrows to spatial containment at M8 and is **excluded** as the dual-aspect link (Demand-17).

---

## 4. The high-risk four — constraint decisions and adversarial fixtures

**Governing principle (stated in the model, as required).** For these four, **the fixture is adversarial**: a model with the wrong constraint stores a single instance without complaint and fails only on a *second, conflicting* instance or on a *multiplicity*. Instantiation does not test them. Each fixture case below must carry the specific second instance or multiplicity a plausible-but-wrong constraint cannot satisfy. A fixture carrying one of each type but none of these pairings is a smoke test (governance §5.9) and does not validate items 15–19a, nor the sixth case (Demand-5b) added below.

### Demand-15/16 — divergent gap rules, no unified rule

**Decision.** Site identity is **physical continuity, gap-tolerant**: an occupation gap is a gap between phases, does not break identity, no `restores` link, one Site. TerritorialUnit identity is **administrative succession, gap-breaking**: dissolution then recreation is **two units linked by `restores`**, unless sources treat the later body as a restoration (then one unit, gap). **No unified gap rule across the two**, and the model must not introduce one (no shared "gap to new record" trigger, no shared "gaps always tolerated" rule).

**Adversarial fixture case.** One Site with an occupation gap (one `id`, non-contiguous phases) **and, in the same fixture,** one TerritorialUnit dissolved and recreated (**two** ids linked by `restores`). Gap-tolerant-everywhere wrongly merges the TerritorialUnit; gap-breaking-everywhere wrongly splits the Site.

### Demand-17 — dual aspect, two entities, neither contains

**Decision.** A dual-aspect referent (bridge, fortified pass, kleisoura, tell-as-landmark) is **two entities** — a LandscapeFeature and a Site — **linked by an explicit relationship (`co_located_aspect`), with neither containing the other and no collapse into one entity**. Not `contains`. Both created only where evidence distinguishes them (Rule 15). The model must not (a) default to `contains`, (b) force single-type membership, or (c) merge the two.

**Adversarial fixture case.** A fortified pass **or** a bridge as **two linked entities** — LandscapeFeature (pass/crossing) plus Site (fort/bridgehead) — with the explicit non-containment link. A containment default stores the fort inside the pass and breaks; a single-type model has no way to hold one referent as two aspects and breaks.

### Demand-18 — M:N route-family membership

**Decision.** `member_of_route_family` is **many-to-many**. **No single-parent or uniqueness constraint** on membership: one track may belong to two families where corridors braid. The family is a peer (Route, `route_class = family`), not a container.

**Adversarial fixture case.** One track with **two** memberships to two families. A single-parent model (track has one `family_id`) or a uniqueness constraint on `(track)` breaks on the second membership.

### Demand-19a — fabric identity, Component-to-Component `succeeds`

**Decision.** Component identity is **fabric, not footprint**. A **Component to Component `succeeds`** relationship is admitted (same-type, Demand-B). Demolished-and-rebuilt fabric on one footprint is **two Components in succession**; converted fabric is one Component with two phases. No footprint-based identity key.

**Adversarial fixture case.** A demolished-and-rebuilt pair on the **same footprint**, two `component_id`s linked by `succeeds`. A footprint-keyed identity (unique on `(parent_site, footprint)`) merges them and breaks; `succeeds` then has nowhere to attach.

### Demand-5b — pure-candidate assertion pooling (sixth adversarial case)

**Decision.** Two pure-candidate attestations with coinciding proposition and disjoint candidate sets fold into **one** Assertion, pooling their candidate subjects (§2.3a). The dispute over referent is routed to Interpretations, not multiplied into distinct Assertions.

**How this differs from the other five, and why it is still adversarial.** The other five are **constraint-absence** demands: the model gets them right by *not* imposing a constraint (a gap rule, a containment default, a single-parent key, a footprint key), and fails by **adding** one. This case is the inverse. The model gets it right **by default** — the folding rule already pools correctly. Its risk is not an over-constraint the model might add; it is that **the correct default is load-bearing on an external discipline** — proposition-wording consistency — rather than on any constraint the model imposes (§2.3a, "why this corner needs stating"). It is nonetheless adversarial by the §4 principle: a single pure-candidate assertion instantiates fine, and only a *second* with the same proposition reveals whether the pooling actually happens. Instantiation cannot test it; the second instance can.

**Adversarial fixture case.** Two pure-candidate attestations — each with no definite or collective link — with the **same proposition** and **disjoint candidate sets** (Attestation-1: candidates P, Q; Attestation-2: candidates R, S). They must fold to **one** Assertion carrying pooled candidates {P, Q, R, S}, **not two** Assertions split on candidate set. A model that keys Assertion identity on candidate subjects (wrongly folding them into the dedup key) produces two and breaks; a model that keys on proposition alone, as specified, produces one.

**Why these four — now five demands, six cases — and not the other thirteen.** The other thirteen are validated by instantiation. These are validated by *the second instance*: five (Demand-15/16, 17, 18, 19a) because each is a constraint the model could wrongly *add* and still pass every single-instance test, and one (Demand-5b) because its correct default is silent under a single instance and only a second instance shows whether the pooling occurred. The first five fail by over-constraint; the sixth would fail by a wrong dedup key or by unenforced proposition variance — different mechanisms, same test shape, hence a named adversarial pairing each rather than coverage-by-family.

---

## 5. Core structural demands (Demand-C)

**Assertion layer with designated pointers (items 7, 9; §5.6).** Every subject carrying geometry or dating holds a nullable `designated_spatial_assertion` / `designated_temporal_assertion` FK; competing values are SpatialAssertion / TemporalAssertion rows; non-designated rows are retained and queryable (§2.4). **A single geometry column on the domain record fails items 7 and 9 and is prohibited.**

**reference_mode qualified link (item 5; §5.3).** The attestation-subject link is a QualifiedSubjectLink row carrying `reference_mode` and its own `identification_confidence` (§2.5). Its fold into Assertion identity is defined at §2.3a. A plain FK list fails item 5.

**I3 — every attestation supports at least one Assertion.** Every Attestation appears in at least one `supporting_attestations` set (§6). 208 attestations currently violate; that is the M2 back-fill, not a model defect.

**Assertion polarity (item 14).** `assertion_polarity` on Assertion (§2.3) plus `detection_scope` on investigation Events (§1.7) give the three-way negative-evidence distinction; the irreducible residual (§10.14) is not a model matter.

---

## 6. Invariants as constraints

Step 3 builds constraints from this table; an invariant absent here is a check that never gets built, so the table is now complete against both the ontology's invariant set (§9) and the step-1 validator list (§17.6: I2, I3, I5, **I5a**, I5b, I11).

| Invariant | Constraint | Class |
|---|---|---|
| **I1** | Every domain entity is referenced by at least one supporting Attestation (via QualifiedSubjectLink or evidential back-link). | **structural — built** |
| **I2** | Attestation: `paraphrase` or `direct_quotation` non-empty (at least one of two). | structural |
| **I3** | Every Attestation is referenced by at least one `Assertion.supporting_attestations`. | structural |
| **I4** | Every Assertion has at least one supporting Attestation; its subject set is the §2.3a fold (may be empty of *identifying* members in a pure-candidate case, but the Assertion still has at least one attestation). | structural |
| **I5** | Every `Interpretation.supporting_evidence` is non-empty and contains only `ATT-` references (rule 9). | structural |
| **I5a** | **Related and competing interpretations are linked by explicit Relationships** (rule 10). Checkable fragment: an Interpretation naming another `INT-` in prose with no corresponding Relationship is flagged. *(Added this revision — named in §17.6's step-1 validator list and omitted from the prior draft's table.)* | **(c) fragment — flagged, not hard-rejected** |
| **I5b** | `Attestation.observation_date` present **iff** `provenance_category = primary_observation` (rule 11). | structural |
| **I6** | Phase belongs to exactly one subject. **Site** phases may not overlap; **Component** phases may. Ordering/non-overlap enforced **within a phasing scheme** (Demand-D), keyed `(subject, phasing_scheme)`. | structural |
| **I7** | A subject's derived existence interval must be consistent with the union of its phase intervals, or be flagged. Existence interval derived, never stored. | (c) — flagged |
| **I8** | A relationship with a Phase endpoint may not assert a temporal scope wider than that phase's. | structural |
| **I9** | A designated assertion must be one of the subject's own asserted values; designation carries a rationale. | structural + (c) for rationale quality |
| **I10** | A phase-attached geometry inherits the phase's temporal scope; an entity-attached geometry is temporally unscoped and may not be treated as period-specific. | structural |
| **I11** | At most one designated spatial and one designated temporal assertion per subject (single-valued FK). | structural |
| **I12** | Interpretive disagreement about function never propagates to an entity's existence or identity. **Realised structurally by absence, not by a check:** there is no functional-certainty column on any persistent entity (it lives only on Phase, §7), so a functional dispute has nowhere to attach except phases and interpretations. **Built by schema shape, not by a constraint.** | **structural — by absence** |
| **I13** | Component identity depends on parent Site; Phase identity depends on subject. Neither survives parent deletion (cascade); both follow fabric under a split. | structural |

**I1 and I12 — resolved as asked.** Both are **structural, not omitted.** I1 is a built referential constraint (every domain entity evidenced). I12 is realised **by absence**: it is enforced not by a check that fires but by the schema shape — functional certainty has no column on any persistent entity (§1.2–1.9 carry none; only Phase does, §7), so the disagreement is structurally incapable of attaching to entity identity. A check cannot be "missing" for I12 because the guarantee is the absent column itself. Stated here so neither is left unexplained.

---

## 7. Demand-D — phasing without a one-phasing uniqueness constraint

**Verbatim in effect (item 13, §10.13).** The model **does not build a uniqueness constraint assuming one phasing per subject.** Phase ordering and non-overlap (I6) are enforced **within a scheme**, the scheme **defaulting to a single implicit value**.

**Realisation.** Phase carries a `phasing_scheme` discriminator defaulting to `default`, so today's single-phasing corpus needs no scheme value. I6 non-overlap is keyed on `(subject, phasing_scheme)`, **not** `(subject)`.

| Phase attribute | Type | Null | Notes |
|---|---|---|---|
| `phase_id` | ID | PK | dependent on subject |
| `subject` | FK to (Site OR Component OR Route OR TerritorialUnit) | not null | polymorphic; cascade delete (I13) |
| `phasing_scheme` | text | not null, default `default` | **item-13 discriminator** |
| `designated_spatial_assertion` | FK to SpatialAssertion | nullable | |
| `designated_temporal_assertion` | FK to TemporalAssertion | nullable | |
| `function` | enum | nullable | item 3 / 10 |
| `functional_confidence` | int 1-5 | nullable | **functional dimension's only bearer** (see I12) |
| `occupation_regime` | enum | nullable | permanent / seasonal / intermittent / unknown (item 6) |
| `rank` | enum | nullable | administrative status (RQ2) |

**Consequence.** A competing phasing later is rows with a new `phasing_scheme` value — a **MINOR** addition, no restructure. A constraint keyed on `(subject)` would have made option (ii) a MAJOR restructure; prohibited here for that reason.

---

## 8. Layering constraints (L1, L2) and polymorphism

**L1** — FK whitelist: a domain record may hold `designated_spatial_assertion`, `designated_temporal_assertion`, and evidential back-link sets into the epistemic layer, and **no other** epistemic FK. L1 constrains stored references, not query direction; inverse traversal is unrestricted.

**L2** — no domain or epistemic record may hold an FK to an AnalyticalRegion. Membership is resolved analytical-side (§9). A domain record carrying a region reference fails validation regardless of result.

**L-poly** — the polymorphic subject link is a **required property, not an option** (§5.7). QualifiedSubjectLink.`subject`, Relationship endpoints, and AttestedName.`subject` are polymorphic over the domain entity space. The model **prohibits typed per-subject FK columns** (`site_id`, `component_id`, `person_id` on Attestation). That prohibition keeps the deferred human-scale types a live option: adding Community/Population requires no epistemic-layer change. This is the single implementation constraint §5.7 names — a constraint on Step 3, not a preference. It also carries the §0.5 identifier decision: because subjects are referenced through one opaque spatial identifier space plus a `spatial_type` column, a re-typing never changes a subject FK.

---

## 9. Analytical layer

### 9.1 AnalyticalRegion *(A)*

**Represents.** A researcher-defined selection (§7). PK `region_id`.

| Attribute | Type | Null | Notes |
|---|---|---|---|
| `region_id` | ID | PK | |
| `author` | text | not null | identity = (author, name, version, membership) |
| `name` | text | not null | |
| `version` | text | not null | |
| `membership_mode` | enum | not null | extensional / intensional / hybrid |
| `member_list` | (set) | conditional | extensional/hybrid |
| `boundary_geometry` + `predicate` | geometry + expr | conditional | intensional/hybrid |
| `temporal_extent` | TemporalValue | **nullable** | null = **temporally unbounded**, never "full corpus extent" (§7.3) |

**Certainty dimensions: none.** No CRM mapping (§11.3). Bounded-extent intersection and no-silent-widening per §7.3.

---

## 10. Coverage check — nineteen items against the model

| # | Item | Realised by | Class |
|---|---|---|---|
| 1 | Fort controls pass | `controls`/`overlooks` | instantiation |
| 2 | Settlement moves | Site + phases + `succeeds`(site) | instantiation |
| 3 | Monastery to fortress | Phase.function, one Site | instantiation |
| 4 | Multiple names | AttestedName rows, optional `temporal_validity` | instantiation |
| 5 | One name, several places | QualifiedSubjectLink.`reference_mode=candidate`; §2.3a fold | instantiation |
| 5b | Pure-candidate assertion pooling | §2.3a fold; identity on proposition alone (Demand-5b) | **constraint (adversarial — default load-bearing on external discipline)** |
| 6 | Seasonal occupation | Phase.`occupation_regime`, non-contiguous phases | instantiation |
| 7 | Two nuclei | SpatialAssertion.geometry = multipolygon | instantiation |
| 8 | Uncertain location | nullable `designated_spatial_assertion` | instantiation |
| 9 | Multiple geometries | SpatialAssertion rows + designated pointer | instantiation |
| 10 | Contested function | Phase.`functional_confidence` + Interpretations; no functional field on entity (I12) | instantiation |
| 11 | Conflicting chronologies | competing TemporalAssertions, none designated; `contradicts`/`revises` | instantiation |
| 12 | Misreading | deprecated Attestation + correction Interpretation + `supersedes_attestation` | instantiation |
| 13 | Competing phase divisions | `phasing_scheme`; I6 keyed within scheme (Demand-D) | **constraint (absence)** |
| 14 | Negative evidence | `assertion_polarity` + Event.`detection_scope` | instantiation (residual not model) |
| 15 | Site abandonment gap | gap-tolerant Site identity, non-contiguous phases | **constraint (adversarial vs 16)** |
| 16 | Jurisdiction interruption | gap-breaking TerritorialUnit identity, `restores` | **constraint (adversarial vs 15)** |
| 17 | Dual aspect | two entities, `co_located_aspect`, **not** `contains` | **constraint (adversarial)** |
| 18 | Route braiding | `member_of_route_family` m:n, no single-parent | **constraint (adversarial)** |
| 19a | Component demolish/rebuild | fabric identity, Component-to-Component `succeeds` | **constraint (adversarial)** |

Thirteen validated by instantiation; item 13 by constraint-absence; 5b, 15, 16, 17, 18 and 19a by adversarial pairing — six adversarial cases in all; twenty rows in all (13 + 1 + 6). §4 states the adversarial case for each of the latter, and Demand-5b's §4 note records how its risk class (a default load-bearing on external discipline) differs from the other five (constraint-absence).

---

## 11. Open items for Step 3, and one flag

**No design decisions are deferred** — the specification is complete on keys, cardinalities and constraints. The prior draft's one deferral (Assertion subject-set derivation) is closed at §2.3a. What remains for Step 3 is *physical* realisation:

- SpatialThing: supertable+subtypes vs one table with `spatial_type` discriminator (§1.1) — physical; logical requirement (shared primitives, shared opaque identifier space, any-endpoint eligibility) stated.
- Polymorphic FKs (L-poly): typed-junction table vs type-tag+id pair — Step 3's; the prohibition on typed per-subject columns is fixed.
- Geometry storage: PostGIS types, canonicalisation for the YAML round-trip (SC4) — physical.

**One flag, not a decision.** `WitnessRecord` (§0.3) is the one place the enumeration and the frozen ontology do **not** cover a plausible future need — manuscript-witness provenance below the level of the work. Excluded here correctly. Flagged so Step 3 does not invent it: if wanted, a §5.8 amendment, not a schema decision.

---

*End of logical model draft. Held for review; delivery is not commit. Frozen ontology only; no migration, no fixture, no records touched. Assembled by single write; full-boundary leak scan clean (§0.4).*
