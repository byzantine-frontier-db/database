# Ontology Alignment

## Byzantine-Islamic Frontier Database — Mapping to External Standards

**Version:** 1.0.0
**Schema referenced:** `byzfrontier_schema_v1.json`
**Specification referenced:** `byzantine_islamic_frontier_database_specification_v2.md`

---

## 1. Purpose

The database does not exist in isolation. It sits within a substantial ecosystem of digital-humanities and historical-GIS infrastructure: CIDOC-CRM (the ISO standard for cultural-heritage data), the Linked Places format used by World-Historical Gazetteer and Pelagios, Pleiades for ancient-world place identifiers, VIAF for personal-name authorities, and so on. This document specifies how records in the Byzantine-Islamic Frontier Database map onto these external standards, so that records can be exported as Linked Open Data without re-modelling.

The principle is **internal richness, external compatibility**: the internal schema is shaped by the research needs of the project, but every record type has a documented serialisation pathway into CIDOC-CRM and, where relevant, into Linked Places, PeriodO, and SKOS.

This document does not require the internal database to *be* CIDOC-CRM. It requires that the internal database *map* to CIDOC-CRM losslessly enough to support export and federation.

---

## 2. CIDOC-CRM Core Alignment

CIDOC-CRM is the reference ontology. Internal record types map to CRM classes as follows.

### 2.1 Class Mapping

| Internal Record Type | CIDOC-CRM Class | Notes |
|---|---|---|
| `PlaceEntity` (place_type ∈ settlement, city, fortification, monastery, etc.) | `E53_Place` | Physical extent. A settlement also typically has an associated `E27_Site` for the archaeological dimension. |
| `PlaceEntity` (place_type = region / administrative_unit / theme / kura / jund / frontier_zone) | `E53_Place` + `E55_Type` qualifier | Regions are still places under CRM; the categorical distinction is via type. |
| `PersonEntity` | `E21_Person` | |
| Group entity (where modelled) | `E74_Group` | |
| `EventEntity` (top-level military, political, religious, etc.) | `E5_Event` | Or, more specifically, `E7_Activity` where intentional human action is the focus (battles, sieges, embassies). Environmental events stay at `E5_Event`. |
| `EventEntity` (sub: construction) | `E12_Production` | For founding, construction, rebuilding. |
| `EventEntity` (sub: destruction, sack) | `E6_Destruction` | |
| `SourceRecord` | `E73_Information_Object` | Or more specifically `E33_Linguistic_Object` for textual sources. Manuscript witnesses are `E84_Information_Carrier`. |
| `AttestationRecord` | `E13_Attribute_Assignment` (with `P140 assigned attribute to` and `P141 assigned`) | Attestations are reified attribute assignments: a source assigns information about an entity. |
| `ObservationRecord` | `E89_Propositional_Object` | The propositional content separable from any particular textual instance. |
| `InterpretationRecord` | `I1_Argumentation` (CRMinf extension) | Modern scholarly arguments. |
| `RelationshipRecord` | Reified `E13_Attribute_Assignment` with relationship type as property | Or directly via the appropriate CRM property where one exists. |
| Controlled-vocabulary terms (event types, place types, etc.) | `E55_Type` | All controlled-vocabulary terms are CRM Types. |
| Alternative names | `E41_Appellation` | Linked via `P1 is identified by`. |
| Coordinates | `E94_Space_Primitive` | Geometric representation of a place. |

### 2.2 Property Mapping

| Internal field / relationship | CIDOC-CRM Property |
|---|---|
| Event `participants` | `P14 carried out by` (person → event) |
| Event `associated_places` | `P7 took place at` |
| Event `start_date` / `end_date` | `P4 has time-span` → `E52_Time-Span` |
| Event `parent_event` | `P9 consists of` (inverse: `P9i forms part of`) |
| Person `kinship` | CRM-Soc extension or directly via specific properties (`P107.1 kind of member`, etc.); v1 uses internal vocabulary. |
| Person `offices_held` | `P14B in the role of` with `E55_Type` for the office |
| Source attests Entity | `P67 refers to` |
| Source documents Event | `P70 documents` |
| Place `alternative_names` | `P1 is identified by` → `E41_Appellation` |
| Place `coordinates` | `P168 place is defined by` → `E94_Space_Primitive` |
| Attestation source | `P14 carried out by` (source → attribute assignment; via authorial agency) and `P140 assigned attribute to` (the entity) |
| Attestation `direct_quotation` / `paraphrase` | The attestation's `E13` carries a note (`P3 has note`) containing the textual evidence. The full passage may be modelled as an `E33` part of the parent `E33`. |
| Relationship `temporal_scope` | `P4 has time-span` on the relationship's reified `E13` |
| Confidence | CRMinf `J5 holds to be` with `I2 Belief` carrying degree |

### 2.3 The Attestation as Reified E13

The single most important alignment decision is the modelling of Attestations. The internal model treats them as a many-to-many link carrying provenance and confidence metadata. The CRM-correct serialisation is as a reified `E13_Attribute_Assignment`:

```
:ATT-0001 a crm:E13_Attribute_Assignment ;
    crm:P14_carried_out_by   :SRC-0001 ;     # the source
    crm:P140_assigned_attribute_to  :ENT-PLC-0001 ;   # the entity
    crm:P141_assigned        :OBS-0002 ;     # the observation as propositional object
    crm:P4_has_time-span     [ a crm:E52_Time-Span ; ... ] ;
    crm:P3_has_note          "..." ;         # paraphrase or quotation
    crminf:J2_concluded_that :OBS-0002 ;
    bzfdb:provenance         bzfdb:primary_paraphrase ;
    bzfdb:confidence         4 .
```

Where the internal model has a single Attestation row, the CRM export produces one `E13` node and zero or more related `E33_Linguistic_Object` and `E52_Time-Span` nodes.

### 2.4 Worked Example: Amorium as CRM

The full export of `ENT-PLC-0001` (Amorium) in Turtle, simplified:

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix bzfdb: <https://byzantine-frontier-db.org/vocab/> .
@prefix pleiades: <https://pleiades.stoa.org/places/> .

:ENT-PLC-0001 a crm:E53_Place ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "Amorium" ;
        bzfdb:isStandardisedForm true
    ] ,
    [ a crm:E41_Appellation ;
      crm:P190_has_symbolic_content "Amorion"@grc ] ,
    [ a crm:E41_Appellation ;
      crm:P190_has_symbolic_content "ʿAmmūriya"@ar ] ;
    crm:P2_has_type bzfdb:settlement ;
    crm:P168_place_is_defined_by [
        a crm:E94_Space_Primitive ;
        crm:P168_place_is_defined_by "POINT(31.2867 39.0211)"^^geo:wktLiteral
    ] ;
    owl:sameAs pleiades:609443 .
```

---

## 3. CRMinf Alignment (Argumentation and Belief)

The CRMinf extension covers what CRM-base does not: reasoning, beliefs, and arguments. Internal Interpretation records and confidence assertions map here.

| Internal | CRMinf |
|---|---|
| `InterpretationRecord` | `I1_Argumentation` |
| Interpretation `argument` text | `I2_Belief` content |
| Interpretation `supporting_evidence` | `J2_concluded_that` linking from `I7_Belief_Adoption` events |
| `confidence` level | `J5_holds_to_be` with belief value mapped from 1–5 scale |

Confidence levels map to CRMinf `I2_Belief.J5_holds_to_be` values as follows (the project commits to publishing a SKOS scheme for this mapping):

- 5 Certain → `crminf:true`
- 4 Highly Probable → custom skos:Concept `bzfdb:highly-probable`
- 3 Probable → custom skos:Concept `bzfdb:probable`
- 2 Possible → custom skos:Concept `bzfdb:possible`
- 1 Speculative → custom skos:Concept `bzfdb:speculative`

The five-level scale is project-internal; CRMinf permits arbitrary belief values, so no information is lost.

---

## 4. Linked Places Format (LPF) Alignment

Linked Places Format is the GeoJSON-based format used by World-Historical Gazetteer and Pelagios. Every `PlaceEntity` in the database has a defined LPF export.

### 4.1 Field Mapping

| Internal field | LPF field |
|---|---|
| `id` (with canonical URI prefix) | `@id` |
| `standardised_name` | `properties.title` |
| `alternative_names` | `names[]` with `toponym`, `lang` |
| `coordinates` | `geometry` (GeoJSON Point or Polygon) |
| `place_type` | `types[]` (linked to AAT or Pleiades types where possible) |
| `chronology` | `when` |
| `political_affiliation_history` | `when` with multiple periods + `relations` |
| External `pleiades` identifier | `links[]` with `type: "closeMatch"` |
| `analytical_summary` | `descriptions[]` |
| `linked_attestations` | `attestations[]` with `citation_type` and `source` |

### 4.2 Worked Example

Amorium's LPF export:

```json
{
  "@context": "https://linkedpasts.org/assets/linkedplaces-context.jsonld",
  "type": "FeatureCollection",
  "features": [{
    "@id": "https://byzantine-frontier-db.org/place/ENT-PLC-0001",
    "type": "Feature",
    "properties": { "title": "Amorium", "ccodes": ["TR"] },
    "names": [
      { "toponym": "Amorium", "lang": "en" },
      { "toponym": "Amorion", "lang": "grc" },
      { "toponym": "ʿAmmūriya", "lang": "ar" }
    ],
    "types": [
      { "identifier": "https://byzantine-frontier-db.org/vocab/settlement",
        "label": "Settlement" }
    ],
    "geometry": {
      "type": "Point",
      "coordinates": [31.2867, 39.0211],
      "certainty": "certain"
    },
    "when": {
      "timespans": [{ "start": { "in": "0600" }, "end": { "in": "1116" } }]
    },
    "links": [
      { "type": "closeMatch", "identifier": "https://pleiades.stoa.org/places/609443" }
    ],
    "descriptions": [
      { "value": "Principal Byzantine military and administrative centre of central Anatolia ...",
        "lang": "en" }
    ]
  }]
}
```

LPF compatibility ensures that the place layer of the database can be ingested by World-Historical Gazetteer without transformation beyond format conversion.

---

## 5. Other Standards

### 5.1 Pleiades

For places attested in classical or early Byzantine sources, the Pleiades identifier is recorded as an `external_identifiers` entry with `authority: pleiades`. Two-way linking: the internal entity carries `owl:sameAs` to the Pleiades URI; where Pleiades publishes the relevant record, alignment is `closeMatch` rather than `sameAs` to allow for chronological scope differences.

### 5.2 VIAF, Wikidata

For persons of broad scholarly recognition, VIAF and Wikidata identifiers are recorded. PBW (Prosopography of the Byzantine World) identifiers are used for Byzantine persons; PMBZ (Prosopographie der mittelbyzantinischen Zeit) identifiers where applicable.

### 5.3 PeriodO

Named historical periods referenced in the database (e.g. "the reign of Theophilos," "the early Abbasid period," "the Macedonian dynasty") are aligned with PeriodO period definitions where available. Custom periods follow PeriodO modelling and are publishable as a PeriodO contribution.

### 5.4 SKOS

All controlled vocabularies are published as SKOS concept schemes:

- `bzfdb:event-types` (top-level + sub)
- `bzfdb:place-types`
- `bzfdb:person-types`
- `bzfdb:relationship-types`
- `bzfdb:provenance-categories`
- `bzfdb:confidence-levels`
- `bzfdb:temporal-precision`
- `bzfdb:identification-status`
- `bzfdb:dating-systems`

SKOS publication enables `closeMatch`/`exactMatch` linking to AAT (Getty Art and Architecture Thesaurus), the Heritage Data terminology, and other thesauri. Where AAT has an exact equivalent (e.g. "siege" → `aat:300055316`), it is recorded.

### 5.5 TEI

Source texts, where transcribed in full, are encoded in TEI P5. The internal SourceRecord points to the TEI document; specific passages cited in attestations point to the `xml:id` of the relevant `<seg>` or `<div>` within that document. This is deferred to v2.0 of the schema; v1.0 records textual evidence as freeform `direct_quotation` / `paraphrase` strings on the Attestation.

### 5.6 GeoSPARQL

Spatial queries are supported via GeoSPARQL. Coordinates are exposed as `geo:asWKT` literals; the WGS84 CRS is mandated. Fuzzy regions (themes, ajnād, kūras) when modelled as polygons in v2.0 will use `geo:hasGeometry` with explicit confidence annotation.

---

## 6. Persistent Identifier Policy

### 6.1 URI Structure

All entities, sources, attestations, observations, interpretations, and relationships have canonical URIs of the form:

```
https://byzantine-frontier-db.org/{type}/{id}
```

For example:

- `https://byzantine-frontier-db.org/place/ENT-PLC-0001` — Amorium
- `https://byzantine-frontier-db.org/source/SRC-0001` — al-Ṭabarī
- `https://byzantine-frontier-db.org/attestation/ATT-0001`

### 6.2 Cool URIs

Per W3C "Cool URIs don't change," these URIs are persistent. Records that are merged retain redirect entries from their original URIs to the merged successor's URI. Records that are split likewise retain redirect entries that point to a disambiguation page listing the successor URIs. URIs are never reassigned to different entities.

### 6.3 Minting Authority

The Editorial Board (see Governance Charter §2) is the sole minting authority for canonical URIs. Identifiers are assigned sequentially within type. Contributor-proposed entities receive provisional identifiers (prefixed `PROV-`) until adopted into the published database.

### 6.4 External Alignment Priorities

When creating a new place entity, the contributor must check the following authorities in order:

1. Pleiades (for ancient and Byzantine-period places)
2. World-Historical Gazetteer
3. GeoNames
4. TGN (Getty Thesaurus of Geographic Names)
5. Wikidata

When creating a new person entity:

1. PBW (Prosopography of the Byzantine World)
2. PMBZ (Prosopographie der mittelbyzantinischen Zeit)
3. VIAF
4. Wikidata

Recording the external identifier is mandatory whenever a match exists.

---

## 7. RDF Serialisation: Full Example

Combining sections 2–6, here is a partial RDF/Turtle serialisation of the Amorium siege records:

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.cidoc-crm.org/crminf/> .
@prefix bzfdb: <https://byzantine-frontier-db.org/vocab/> .
@prefix pbw: <https://pbw2016.kdl.kcl.ac.uk/person/> .
@prefix pleiades: <https://pleiades.stoa.org/places/> .
@prefix : <https://byzantine-frontier-db.org/> .

:place/ENT-PLC-0001 a crm:E53_Place ;
    crm:P1_is_identified_by [ a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "Amorium" ] ;
    crm:P2_has_type bzfdb:settlement ;
    owl:sameAs pleiades:609443 .

:event/ENT-EVT-0003 a crm:E7_Activity ;
    crm:P2_has_type bzfdb:siege ;
    crm:P7_took_place_at :place/ENT-PLC-0001 ;
    crm:P9i_forms_part_of :event/ENT-EVT-0001 ;
    crm:P4_has_time-span [ a crm:E52_Time-Span ;
        crm:P82a_begin_of_the_begin "0838-08-01"^^xsd:date ;
        crm:P82b_end_of_the_end   "0838-08-15"^^xsd:date ;
        bzfdb:precision bzfdb:month ;
        bzfdb:confidence 3 ] .

:attestation/ATT-0001 a crm:E13_Attribute_Assignment ;
    crm:P14_carried_out_by :source/SRC-0001 ;
    crm:P140_assigned_attribute_to :place/ENT-PLC-0001 ;
    crm:P141_assigned :observation/OBS-0002 ;
    bzfdb:provenance bzfdb:primary_paraphrase ;
    bzfdb:confidence 5 ;
    crm:P3_has_note "Under AH 223 al-Ṭabarī gives an extended account ..." .

:observation/OBS-0002 a crm:E89_Propositional_Object ;
    rdfs:label "Amorium fell to Abbasid forces in August 838" .

:interpretation/INT-0001 a crminf:I1_Argumentation ;
    crminf:J2_concluded_that :observation/OBS-0002 ;
    crm:P3_has_note "The 838 campaign was strategically and symbolically devastating ..." ;
    bzfdb:scholar "Treadgold, W." ;
    bzfdb:confidence 4 .
```

This example demonstrates that the internal model serialises cleanly to standard CIDOC-CRM with CRMinf extensions, with custom `bzfdb:` predicates only where CRM has no native equivalent (provenance category, numeric confidence, precision categorical).

---

## 8. Outstanding Alignment Decisions

The following alignment questions remain open and are flagged for resolution before v2.0:

1. **Fuzzy regions.** Modelling themes, ajnād, and other zones with shifting boundaries requires either GeoSPARQL fuzzy geometries (not widely supported), explicit polygon-per-time-slice via the temporal-versioning pattern, or extension via CRMgeo. Decision deferred.

2. **Manuscript witnesses.** Full alignment with TEI msDesc and the FRBR-derived LRMoo (replacement for FRBRoo) is required for serious source-critical work. v1 collapses witnesses into the SourceRecord; v2 will introduce a separate `WitnessRecord` aligned to `lrm:F5_Item` and `lrm:F3_Manifestation`.

3. **Dating-system reconciliation.** AH-to-Julian conversion has known ambiguities. The project commits to the standard astronomical Julian-Day-Number conversion via `dating-systems.json` lookup tables, but the published rule must be documented and tested.

4. **Confidence aggregation.** No standard exists for combining attestation-level confidence into entity-level confidence. The project will publish a documented heuristic (likely Dempster-Shafer or a simple weighted-mean variant) and tag entity-level confidence values as algorithmically derived versus editorially imposed.

5. **The events-as-entities question.** CRM resolves this cleanly (events are `E5_Event`, distinct from `E18_Physical_Thing`); the internal schema treats events as one entity type alongside places and persons, which is a pragmatic simplification rather than a CRM violation. Documented and accepted.

---

## 9. Compliance Statement

For a record to claim CIDOC-CRM compliance under v1.0.0 of this database, it must (a) validate against `byzfrontier_schema_v1.json`, (b) export to a CRM-conformant RDF serialisation using the mappings in §2 and §3, and (c) carry SKOS-resolvable values in all controlled-vocabulary fields.

Records that meet (a) but not (b) and (c) are "internally valid"; records that meet all three are "CRM-compliant." The project goal is full CRM compliance for all published records by the v1.1 milestone.
