# Byzantine–Islamic Frontier Historical-Geographical Database Project

## A Formal Specification for a Provenance-Aware Historical Knowledge Graph

---

## 1. Purpose and Scope

The purpose of this project is to construct a comprehensive, provenance-aware historical-geographical database of places, events, actors, institutions, routes, political entities, and interactions associated with the Byzantine–Islamic frontier and its wider connected regions between the seventh and eleventh centuries.

The database will be constructed through the systematic extraction, standardisation, integration, reconciliation, and synthesis of information derived from primary and secondary source material. The resulting dataset is intended to support both traditional historical scholarship and advanced spatial, temporal, relational, and computational analysis within GIS and related research environments.

Primary source material may include chronicles, annals, histories, hagiographies, administrative texts, legal texts, military treatises, geographical works, travel accounts, inscriptions, documentary archives, letters, and other contemporary evidence. Secondary source material may include archaeological reports, regional studies, gazetteers, prosopographies, historical analyses, thematic monographs, and specialist scholarship.

The objective is not merely to catalogue places or record events. Rather, it is to transform dispersed and heterogeneous historical evidence into a structured, transparent, auditable, and analytically robust knowledge system capable of preserving both the content of historical claims and the evidential basis upon which those claims rest.

The database is designed to function simultaneously as:

* A historical gazetteer.
* An event database.
* A source repository and source-network resource.
* A prosopographical resource.
* A frontier interaction database.
* A GIS-compatible research dataset.
* A historical knowledge graph.
* A provenance and evidence management system.
* A transparent evidential framework linking analytical conclusions to source material.

The project seeks to bridge the traditional divide between qualitative historical scholarship and quantitative spatial analysis while preserving the uncertainty, complexity, and interpretative plurality inherent within the historical record.

---

## 2. Conceptual Data Model

The conceptual model is organised around five first-class object types: Entities, Sources, Observations, Attestations, and Relationships. The relationships between these object types are deliberately strict, because the analytical integrity of the database depends upon never collapsing one type into another.

The fundamental chain of the model is as follows:

> A **Source** generates an **Attestation** that records an **Observation** about an **Entity**, optionally describing a **Relationship** between Entities.

Each component of this chain is defined separately and must remain independently identifiable throughout the lifetime of the database.

### 2.1 Historical Entities

Historical entities constitute the primary analytical objects of study. They represent things that existed, acted, occurred, or were conceptualised within the historical world.

Entities may include:

* Places.
* Settlements.
* Fortifications.
* Regions.
* Routes.
* Political entities.
* Administrative units.
* Persons.
* Groups.
* Institutions.
* Events.
* Military campaigns.
* Diplomatic missions.
* Trade networks.
* Religious communities.
* Environmental features.

Entities are persistent analytical objects that exist independently of any individual source. An entity may be supported by many attestations drawn from many sources, but the entity itself is a single analytical object that the database treats as a master record.

### 2.2 Sources

A Source is a textual, material, archaeological, epigraphic, numismatic, or modern scholarly work that generates attestations. Sources are first-class objects of the model and are treated as analytical objects in their own right, not merely as citation strings attached to other records.

Examples of sources include:

* al-Ṭabarī, *Taʾrīkh al-rusul wa-l-mulūk*.
* Theophanes Continuatus.
* al-Yaʿqūbī, *Taʾrīkh*.
* The Acts of the Forty-Two Martyrs of Amorium.
* The Tabula Imperii Byzantini volume on Cappadocia.
* A named archaeological survey publication.
* A specific numismatic catalogue.
* A specific modern monograph.

Treating Sources as first-class objects supports source-network analysis, historiographical analysis, the study of textual dependencies and shared traditions, and the systematic evaluation of evidential weight across the database. It also ensures that the same source is recognised consistently every time it is cited, which is essential once the database scales to thousands of attestations.

Each source record carries its own metadata, including author, date of composition, language, genre, transmission history, edition or translation used, and scholarly assessment of reliability and biases.

### 2.3 Observations

An Observation is a discrete historical claim extracted from evidence. It is the propositional content of what is being asserted about the historical world.

Examples of observations include:

* Amorium fell in 838.
* The city of Amorium was destroyed.
* The emperor Theophilos fled the battlefield.
* The fortress at Loulon was held by an Arab garrison.
* A treaty was concluded between Byzantines and Abbasids.

An observation is a claim. It is propositional. It is the *what* of the historical statement.

Crucially, an observation is not the same as the source that records it. Multiple sources may record the same observation; a single source may record many observations; and observations may be derived by inference or synthesis rather than by direct statement.

### 2.4 Attestations

An Attestation is the evidential record of a claim. It is the documented instance in which a specific source provides information supporting a specific observation about a specific entity.

An attestation is the *that* and the *where* of the evidence:

* That al-Ṭabarī states it.
* That Theophanes Continuatus states it.
* That a specific inscription records it.
* That a specific modern survey concludes it.

An attestation always links three things: a Source, an Observation, and the Entity (or Entities) the observation concerns.

The relationship between observations and attestations is many-to-many. A single observation may be supported by many attestations. A single attestation may record several observations. The database preserves this structure rather than flattening it.

The distinction may be summarised:

> An **Observation** is the claim. An **Attestation** is the evidence for that claim. A **Source** is the work that generates the attestation.

This three-level distinction is the foundation of the model and must be preserved at every stage of extraction, ingestion, querying, and analysis.

### 2.5 Relationships

Relationships describe connections between entities, between observations, between attestations, between sources, and between any of these and interpretations.

Relationship types include but are not limited to:

* Person participated in Event.
* Event occurred at Place.
* Place belonged to Political Entity.
* Route connected Places.
* Institution administered Region.
* Settlement controlled Passage.
* Source depends upon Source.
* Source contradicts Source.
* Observation contradicts Observation.
* Attestation supports Interpretation.

Relationships are themselves recorded as structured objects and may carry their own attestations, confidence values, and chronological information.

---

## 3. Core Design Principles

### 3.1 Evidential Transparency

Every record must remain fully traceable to the evidence from which it was derived. No information should exist within the database without a documented evidential basis. Researchers must be able to move directly from any analytical record to the precise source material supporting it. Transparency takes precedence over simplicity.

### 3.2 Auditability

Every record must be auditable back to its evidential foundation. The database must preserve not only conclusions but the evidential pathway through which those conclusions were reached. Researchers should be able to reconstruct why a record exists, which sources support it, which sources contradict it, how interpretations were formed, and what degree of certainty accompanies each conclusion. The evidential layer is considered equally important as the analytical layer.

### 3.3 Entity–Observation–Attestation Separation

The database must maintain a strict distinction between entities, observations, and attestations. Entities are analytical objects. Observations are claims. Attestations are evidence. Multiple attestations may support the same observation; multiple observations may concern the same entity; multiple entities may be implicated in a single attestation. The database must preserve these structures rather than collapse them.

### 3.4 Preservation of Historical Complexity

The database must preserve uncertainty, contradiction, ambiguity, and competing interpretations. It must explicitly allow multiple dates, multiple chronologies, alternative place identifications, competing interpretations, contradictory narratives, uncertain locations, and disputed historical significance. Uncertainty is recorded rather than artificially resolved.

### 3.5 Cumulative Evidence

Historical entities accumulate evidence over time. When new evidence is encountered, the database expands existing records rather than generating duplicates. The unit being accumulated is the body of attestations supporting an entity, not the entity itself. The database therefore functions as a cumulative repository of evidence rather than a collection of isolated observations.

### 3.6 Controlled Vocabularies and Machine-Operable Ontology

To ensure consistency across thousands of records and across multiple contributors, including AI-assisted extraction, the database employs controlled vocabularies for entity types, event types, provenance categories, relationship types, identification statuses, and confidence values. Free-text fields are reserved for narrative content; analytical fields draw from defined vocabularies specified in this document.

---

## 4. Master Record and Identity Resolution Framework

Identity resolution is the operational backbone of the database. Without a formal rule, contributors (human or AI) will over-produce entities, fragmenting the evidential record and undermining the cumulative-evidence principle.

### 4.1 The Master Record Rule

> Historical entities are treated as master records to which observations, attestations, interpretations, and relationships are attached. Before creating a new entity, available evidence must be evaluated to determine whether the information refers to an existing entity. A new entity may be created only when available evidence indicates that no existing entity can reasonably accommodate the observation. Alternative names, spellings, languages, transliterations, and disputed identifications should normally be recorded within the same entity record rather than generating duplicate entities.

### 4.2 Identification Procedure

When evaluating whether a new observation refers to an existing entity, the following procedure applies:

1. Search existing entities by standardised name, alternative names, original-language forms, and known transliterations.
2. Search by geographic proximity, where applicable.
3. Search by chronological window and historical role.
4. Search by associated persons, events, and political affiliation.
5. If a plausible candidate is found, attach the new observation as an additional attestation.
6. If no candidate is found, or if the candidate cannot reasonably accommodate the new evidence, create a new entity and record the reasoning in the entity's notes.

### 4.3 Disputed Identification

Where scholars dispute whether two names or descriptions refer to the same entity, the disputed identification is recorded *within* a single entity record using the identification framework defined in section 8. Generating parallel duplicate entities to express disagreement is prohibited; disagreement is captured through identification status, identification confidence, and linked interpretation records.

### 4.4 Merging and Splitting

The database supports two operations to maintain identity integrity:

* **Merge.** When two entities are determined to refer to the same historical object, they are merged into a single master record with full preservation of the attestations, observations, and interpretations originally attached to each.
* **Split.** When a single entity is determined to conflate two distinct historical objects, it is split into two entities, with each attestation reassigned to the appropriate successor.

Both operations are logged, reversible, and accompanied by a documented rationale.

### 4.5 Worked Examples

* *Amorion / Amorium / ʿAmmūriya*: These are recorded as alternative-name forms of a single entity, not as three entities.
* *Raid on Caesarea / Arab campaign against Caesarea / Sack of Caesarea*: If the descriptions concern the same chronological window and participants, they are treated as alternative attestations of a single event. If they refer to distinct campaigns, they are recorded as distinct events with cross-references.

---

## 5. Provenance Framework

Not all information possesses the same epistemological status. Each attestation is assigned one provenance category from the following controlled vocabulary:

* **Primary quotation.** A direct verbatim quotation from a primary source.
* **Primary paraphrase.** A close paraphrase of a primary source statement.
* **Primary summary.** A higher-level summary of primary source content.
* **Archaeological evidence.** Material evidence drawn from excavation or survey.
* **Epigraphic evidence.** Inscriptional evidence.
* **Numismatic evidence.** Coin-based evidence.
* **Papyrological evidence.** Documentary evidence on papyrus or related media.
* **Sigillographic evidence.** Lead seal evidence.
* **Modern synthesis.** A modern scholarly synthesis of multiple sources.
* **Modern identification.** A modern scholarly identification of a place, person, or object.
* **Modern interpretation.** A modern interpretative argument.
* **GIS-derived observation.** An observation generated from spatial analysis.
* **Editorial inference.** An inference made by the database editor on the basis of explicit reasoning.
* **Cross-source synthesis.** A synthetic claim drawing on multiple attestations.

The provenance category remains permanently attached to the attestation and is never overwritten when new evidence is added.

---

## 6. Confidence Framework

Confidence answers a single question: how sure are we that the claim is true? It is distinct from precision (section 7) and from identification status (section 8).

### Level 5 — Certain

Directly attested and uncontested.

### Level 4 — Highly Probable

Strongly supported by multiple independent lines of evidence.

### Level 3 — Probable

Supported by evidence but not beyond reasonable dispute.

### Level 2 — Possible

Plausible but weakly supported.

### Level 1 — Speculative

Hypothetical or highly uncertain.

Confidence assessments are accompanied by explanatory notes describing the reasons for the assigned rating, including which attestations support the claim and which contradict it.

---

## 7. Temporal Framework

Temporal information is recorded along two independent axes: precision and confidence. Conflating these two axes is one of the most common failure modes in historical databases; the model deliberately separates them.

### 7.1 Temporal Precision

Precision describes how specific the date is, regardless of how sure we are. Permitted precision values form a controlled vocabulary:

* **Exact day.** A specific calendar day is known.
* **Month.** Known to the month.
* **Season.** Known to a season (e.g. "summer 838").
* **Year.** Known to the year.
* **Year range, narrow.** Known to a window of two to five years.
* **Year range, broad.** Known to a window of six to twenty years.
* **Decade.** Known to a decade.
* **Quarter-century.** Known to a span of approximately twenty-five years.
* **Half-century.** Known to a span of approximately fifty years.
* **Century.** Known to a century.
* **Relative before.** Known to occur before a reference event or date.
* **Relative after.** Known to occur after a reference event or date.
* **Relative between.** Known to occur between two reference events or dates.
* **Unknown.** Chronological position cannot be specified.

### 7.2 Temporal Confidence

Confidence describes how sure we are that the recorded date is correct, regardless of its precision. It follows the five-level confidence scale defined in section 6.

### 7.3 Recording Dates

Each dated record stores:

* Start date.
* End date.
* Precision value.
* Confidence value.
* Dating basis (indiction, regnal year, AH, AD, archaeological phase, palaeographic dating, etc.).
* Source(s) supporting the date.
* Alternative dates proposed in the literature.

This structure permits queries such as "events known to the year with confidence level four or higher" or "events located by relative-before dating with low confidence."

### 7.4 Worked Examples

* *838*: precision = year; confidence = 5.
* *Summer 838*: precision = season; confidence = 5.
* *Between 837 and 839*: precision = year range, narrow; confidence = 4.
* *After 838*: precision = relative after; confidence = 4.
* *Before 840*: precision = relative before; confidence = 3.
* *Ninth century*: precision = century; confidence = 5.

---

## 8. Spatial and Identification Framework

Spatial information is recorded along two independent axes that must never be conflated: identification and location.

* **Identification** asks: do we know *which* historical place this is?
* **Location** asks: do we know *where* that place was?

These are separate questions. A place may be confidently identified but poorly located (an attested toponym whose physical site has not been found). A place may be confidently located but poorly identified (a ruin whose ancient name is disputed). The framework records each independently.

### 8.1 Identification Status

A controlled vocabulary for identification status:

* **Identified.** The historical place is known and confidently equated with a specific entity.
* **Probably identified.** A specific identification is supported but not certain.
* **Approximately identified.** The general area is known (e.g. "somewhere near Melitene") but no specific site is fixed.
* **Hypothetically identified.** A tentative identification is proposed in the literature.
* **Unidentified.** The place is named in sources but its location and identification are unknown.
* **Disputed.** Competing identifications are recorded in the literature.

### 8.2 Identification Confidence

The five-level confidence scale from section 6 applied to the identification claim.

### 8.3 Coordinate Confidence

The five-level confidence scale from section 6 applied separately to the recorded coordinates.

### 8.4 Coordinate Metadata

Each coordinate record stores:

* Latitude and longitude.
* Coordinate source.
* Coordinate method (archaeological survey, modern map, satellite imagery, scholarly identification, inference from itinerary).
* Coordinate precision (point, building, site, settlement, locality, region).
* Uncertainty radius in metres.
* Coordinate confidence.

### 8.5 Worked Examples

* *Amorium*: identification status = identified; identification confidence = 5; coordinate confidence = 5; coordinate method = archaeological survey.
* *A village near Melitene*: identification status = approximately identified; identification confidence = 3; coordinate confidence = 2; uncertainty radius = 25 km.
* *A toponym mentioned only in al-Masʿūdī*: identification status = unidentified; coordinate confidence = 1; coordinates may be omitted.
* *A ruin disputed between two ancient toponyms*: identification status = disputed; identification confidence = 2; coordinate confidence = 5; alternative identifications recorded as linked interpretations.

---

## 9. Event Ontology and Controlled Vocabularies

To prevent vocabulary drift across thousands of records and to support consistent querying, events are classified using a controlled, hierarchical event ontology. The ontology is extensible but additions follow a documented governance process.

### 9.1 Top-Level Event Categories

* **Military.**
* **Political.**
* **Diplomatic.**
* **Administrative.**
* **Economic.**
* **Religious.**
* **Cultural.**
* **Demographic.**
* **Environmental.**
* **Construction and Infrastructure.**

### 9.2 Sub-Category Vocabulary

The following sub-categories represent the controlled vocabulary for event classification. Each event is assigned one primary type; secondary types may be added where genuinely warranted.

**Military.** Raid, incursion, siege, assault, battle, skirmish, ambush, naval engagement, occupation, garrisoning, fortification, withdrawal, retreat, surrender, capture of fortress, sack of city, destruction, deportation of population, ransoming, prisoner exchange, military review, mustering.

**Political.** Accession, deposition, succession dispute, revolt, usurpation, civil war, assassination, oath of allegiance, dynastic marriage, regency.

**Diplomatic.** Embassy, treaty, truce, ransom negotiation, gift exchange, formal correspondence, alliance, hostage exchange.

**Administrative.** Appointment, dismissal, creation of administrative unit, dissolution of administrative unit, boundary change, census, fiscal reform.

**Economic.** Trade activity, market establishment, taxation event, tribute payment, coinage reform, famine, surplus, fiscal grant.

**Religious.** Pilgrimage, monastic foundation, church construction, mosque construction, council, synod, ordination, martyrdom, translation of relics, conversion event, persecution, theological controversy.

**Cultural.** Translation activity, manuscript production, scholarly exchange, literary composition.

**Demographic.** Migration, deportation, settlement, depopulation, plague event.

**Environmental.** Earthquake, flood, drought, climatic event, agricultural failure.

**Construction and Infrastructure.** Wall construction, fortress construction, road construction, bridge construction, water-system construction, harbour works, repair, restoration.

### 9.3 Entity Type Vocabulary

A parallel controlled vocabulary governs entity types. The principal entity-type categories are: settlement, fortification, monastery, church, mosque, region, administrative unit, route, pass, river, mountain, frontier zone, person, family, dynasty, ethnic group, religious community, military unit, institution, office, event, campaign, treaty, and source.

### 9.4 Relationship Type Vocabulary

The relationship vocabulary is published as part of the database schema and includes spatial relationships (contains, adjoins, lies on route), political relationships (belongs to, subordinate to, in revolt against), kinship relationships, military relationships (besieged, occupied, defended), source relationships (depends on, contradicts, transmits), and evidential relationships (attests, contradicts attestation, supersedes attestation).

### 9.5 Governance

Controlled vocabularies are versioned. Changes to vocabularies are logged. Older records remain valid under earlier vocabulary versions and may be updated through documented migration.

---

## 10. Methodological Principles

Information is extracted at the level of discrete observations and linked to entities through attestations sourced from identified Sources. Each extracted observation preserves:

* Historical content.
* Context within the source.
* Evidential basis.
* Provenance category.
* Confidence value.
* Temporal precision and temporal confidence.
* Identification status and identification confidence, where applicable.
* Coordinate confidence, where applicable.
* Interpretative implications.

The objective is not simply to capture facts but to preserve historically meaningful information together with the evidence and reasoning that support it.

---

## 11. Three-Layer Record Structure

Every entity record contains three interconnected layers.

### Layer 1 — Structured Analytical Data

Machine-readable information suitable for GIS, network analysis, and quantitative analysis. Examples include coordinates, identification status, identification confidence, coordinate confidence, chronologies, temporal precision, temporal confidence, classifications drawn from controlled vocabularies, relationships, administrative status, political affiliation, environmental variables, and overall confidence values.

### Layer 2 — Analytical Summary

Human-readable synthesis explaining what occurred, why it matters, how it relates to frontier processes, and what conclusions can reasonably be drawn. Summaries may synthesise information across multiple attestations but must reference the attestations they draw upon.

### Layer 3 — Source Evidence

The complete evidential basis of the record. This layer contains direct quotations, paraphrases, references, citations, provenance categories, attestation records, source records, and interpretative notes. No analytical statement exists without evidential support.

---

## 12. Source Integration Framework

### 12.1 Primary Sources

Primary-source attestations preserve direct quotations wherever possible, original-language terminology, precise references including book, chapter, and page or folio, translation notes, and contextual information. Each primary-source attestation is individually identifiable and linked to a Source record.

### 12.2 Secondary Sources

Secondary-source attestations preserve full citation, precise page references, summary of argument, and interpretative significance. Secondary scholarship supplements rather than replaces primary evidence and is similarly linked to a Source record.

### 12.3 Source Records

A Source record carries metadata sufficient to evaluate the source's standing within the network of evidence: author, date or date range of composition, language, genre, transmission history, the specific edition or translation used in this database, scholarly assessments of reliability, known biases, dependence on earlier sources, and the source's place within wider textual traditions.

---

## 13. Managing Repetition and Source Overlap

The same event or place may appear in dozens of primary and secondary sources. When this occurs:

* The existing entity is retained as the master record.
* A new attestation is created and linked to the entity.
* New quotations are appended to the attestation layer.
* Additional references are incorporated.
* Contradictions are preserved rather than silently resolved.
* The cumulative weight of evidence may justify upward revision of confidence values; downward revision is equally permitted where new evidence weakens earlier claims.

The database therefore becomes progressively richer rather than increasingly fragmented.

---

## 14. Recording Scholarly Disagreement

Scholarly disagreement is stored in structured, queryable form rather than embedded within narrative text. Each interpretation record includes:

* Interpretation identifier.
* Associated entity or entities.
* Scholar.
* Publication and source record reference.
* Date.
* Argument.
* Supporting evidence (linked attestations).
* Counter-evidence (linked attestations).
* Confidence assessment.
* Notes.

Interpretations are linked directly to the attestations and evidence upon which they depend, and to the entities they concern.

---

## 15. Data Structure

The database operates as a relational and graph-compatible system. Core entity tables are supplemented by dedicated tables for sources, attestations, observations, interpretations, relationships, political entities, administrative units, routes, environmental features, and controlled vocabularies.

### 15.1 Place Records

Place records capture: unique identifier; standardised name; alternative names; original-language forms; transliteration variants; place type (controlled vocabulary); identification status; identification confidence; geographic coordinates; coordinate source; coordinate method; coordinate precision; coordinate confidence; uncertainty radius; political affiliation; administrative status; frontier role; environmental setting; chronological information with precision and confidence; associated entities; overall confidence assessment; analytical summary; linked attestations; linked interpretations.

### 15.2 Event Records

Event records capture: unique identifier; event type (controlled vocabulary, primary and secondary); start date; end date; temporal precision; temporal confidence; dating basis; associated places; participants; political entities involved; related events; description; historical significance; overall confidence assessment; analytical summary; linked attestations; linked interpretations.

### 15.3 Source Records

Source records capture: unique identifier; standardised title; alternative titles; author; date of composition with precision and confidence; language; genre; transmission history; edition or translation used; scholarly assessment; known biases and dependencies; relationships to other sources; notes.

### 15.4 Observation Records

Observation records capture: unique identifier; propositional content of the claim; associated entity or entities; event or relationship referenced; chronological reference; spatial reference; linked attestations supporting the observation; linked attestations contradicting the observation; notes.

### 15.5 Attestation Records

Attestation records capture: unique identifier; associated entity or entities; associated observation; source (linked to source record); provenance category; direct quotation; paraphrase; citation; location within source (book, chapter, page, folio, line); editor's interpretation of the passage; confidence assessment; notes.

### 15.6 Interpretation Records

Interpretation records capture: unique identifier; associated entity or entities; scholar; publication (linked to source record); argument; supporting evidence (linked attestations); counter-evidence (linked attestations); confidence assessment; notes.

### 15.7 Relationship Records

Relationship records capture: unique identifier; relationship type (controlled vocabulary); source entity; target entity; chronological scope with precision and confidence; spatial scope, where applicable; confidence assessment; linked attestations; notes.

---

## 16. Analytical Objectives

The database supports:

* Spatial analysis of frontier dynamics.
* Temporal modelling of historical change.
* Military activity analysis.
* Administrative geography reconstruction.
* Settlement pattern analysis.
* Route and communication network analysis.
* Economic interaction studies.
* Pilgrimage and mobility studies.
* Diplomatic interaction mapping.
* Environmental correlation studies.
* Comparative source analysis.
* Source-network and textual-dependency analysis.
* Historiographical analysis.
* Identification-history analysis (how scholarly identifications have shifted over time).
* Long-term modelling of frontier transformation between the seventh and eleventh centuries.

---

## 17. Expected Output

The final output consists of a highly structured, relational, provenance-aware historical knowledge system in which every analytical entity is linked to its underlying evidential attestations, source records, observation claims, and interpretative history.

Each record integrates:

1. Structured analytical data suitable for GIS, network analysis, and computational research, using controlled vocabularies, dual-axis temporal modelling (precision and confidence), and dual-axis spatial modelling (identification and location).

2. Human-readable analytical summaries that preserve historical meaning and interpretative context.

3. A comprehensive evidential layer containing attestations, observations, source records, quotations, citations, provenance classifications, confidence assessments, and scholarly interpretations.

The database is governed by a formal identity-resolution rule that treats entities as master records and accumulates evidence against them rather than fragmenting the record. It is governed by a controlled event ontology and a controlled relationship vocabulary that ensure consistency across thousands of records and across multiple contributors. It separates the analytical from the evidential at every layer and preserves the distinction between claim, evidence, and source.

The resulting database allows researchers not only to map historical phenomena but to interrogate the evidence, reasoning, uncertainty, and scholarly debate underlying every mapped feature, event, relationship, and interpretation. It functions simultaneously as a spatial dataset, historical gazetteer, event database, source repository, prosopographical resource, knowledge graph, research platform, and transparent evidential framework for the study of the Byzantine–Islamic frontier.

---

## Appendix A — Summary of Key Distinctions

| Distinction | Axis A | Axis B |
|---|---|---|
| Claim vs. evidence | Observation (the claim) | Attestation (the evidence for it) |
| Evidence vs. work | Attestation (specific evidential record) | Source (the work that generates attestations) |
| Date specificity vs. date reliability | Temporal precision | Temporal confidence |
| Knowing which place vs. knowing where it is | Identification status / confidence | Coordinate confidence |
| Master record vs. variant attestation | Entity (single master record) | Attestations (multiple, attached to entity) |

## Appendix B — Controlled Vocabulary Index

The database maintains versioned controlled vocabularies for:

* Entity types.
* Event types (top-level and sub-categories, per section 9).
* Relationship types.
* Provenance categories (per section 5).
* Confidence values (per section 6).
* Temporal precision values (per section 7).
* Identification status values (per section 8).
* Coordinate precision values (per section 8).
* Source genres.
* Dating bases.

Vocabularies are published with the schema, are versioned, and changes are logged.

---

## Appendix C — Worked End-to-End Example: The Capture of Amorium, 838 CE

### C.0 Purpose of this example

The preceding sections specify the conceptual model, vocabularies, and record types in prose. This appendix instantiates that specification against a single well-attested historical episode — the Abbasid capture of Amorium in 838 — in order to demonstrate that the model is coherent, operationalisable, and capable of carrying the analytical weight the project requires.

The example is deliberately scoped to a single event-complex with five sources, three places, three persons, four sub-events, and a representative selection of observations, attestations, interpretations, and relationships. It is sufficient to exercise every record type and every controlled vocabulary defined in the specification, while remaining short enough to read end-to-end.

Records are presented in YAML for readability. The serialisation format chosen for implementation may be JSON, JSON-LD, RDF/Turtle, or property-graph format; the choice is deferred (and is itself one of the gaps acknowledged in §C.11).

### C.1 The episode in brief

In the spring of 838, the Abbasid caliph al-Muʿtaṣim launched a major retaliatory campaign against the Byzantine Empire, in response to Theophilos's earlier attack on Zibatra (Sozopetra) in 837. The Abbasid army split into two columns. One, under al-Muʿtaṣim himself, advanced on Ancyra; the other, under al-Afshīn, intercepted and defeated a Byzantine relief force under Theophilos at a battle variously named Anzen (in Greek sources) and Dazimon (in Arab sources) on or around 22 July 838. Theophilos withdrew. The reunited Abbasid army then besieged and captured Amorium, the strategically critical city in central Anatolia and the ancestral home of the reigning Byzantine dynasty. The siege culminated in the sack of the city and the deportation of its surviving population. Forty-two of the Byzantine officers taken at Amorium were held in Samarra and eventually executed there, traditionally on 6 March 845, becoming the subjects of an extensive Byzantine hagiographic tradition as the Forty-Two Martyrs of Amorium.

This episode is unusually rich for the period: it is reported in Greek, Arabic, and Syriac historiography, attested archaeologically through the long-running Amorium excavations, and discussed extensively in modern scholarship from Bury to Treadgold to Lightfoot.

### C.2 Source records

The example uses five sources. Source records are abbreviated for space; production records would include fuller transmission and editorial detail.

```yaml
- id: SRC-0001
  standardised_title: "al-Ṭabarī, Taʾrīkh al-rusul wa-l-mulūk"
  alternative_titles: ["Annales", "History of the Prophets and Kings"]
  author_id: ENT-PERS-0023      # → al-Ṭabarī
  persistent_identifiers:
    internal_id: SRC-0001
    external_identifiers:
      # Note: VIAF, Wikidata, and ISNI here identify the author (al-Ṭabarī).
      # When the author is modelled as a full PersonEntity, these move there.
      - { authority: viaf,     identifier: "9854001",       uri: "https://viaf.org/viaf/9854001/" }
      - { authority: wikidata, identifier: "Q192124",       uri: "https://www.wikidata.org/wiki/Q192124" }
  date_of_composition:
    start: 870
    end: 915
    precision: year_range_broad
    confidence: 4
  language: ar
  genre: universal_chronicle
  edition_used: "Cairo: Dār al-Maʿārif, ed. M. Abū al-Faḍl Ibrāhīm, 1960–69"
  translation_used: "Bosworth, C. E. (trans.), The History of al-Ṭabarī XXXIII: Storm and Stress along the Northern Frontiers of the ʿAbbāsid Caliphate, SUNY Press, 1991"
  reliability_assessment: "Highly reliable for Abbasid court and military events; annalistic organisation (by AH year) can split a single campaign across multiple entries."
  known_biases: "Court-centred; pro-Abbasid framing of military outcomes."
  dependencies: []
  notes: "Account of the 838 campaign appears under AH 223."

- id: SRC-0002
  standardised_title: "Theophanes Continuatus"
  alternative_titles: ["Chronographia (continuation)", "Scriptores post Theophanem"]
  author_id: ENT-PERS-0024      # → anonymous; commissioned by Constantine VII
  date_of_composition:
    start: 945
    end: 959
    precision: year_range_narrow
    confidence: 4
  language: grc
  genre: imperial_chronicle
  edition_used: "Featherstone, J. M. & Signes Codoñer, J. (eds.), Chronographiae quae Theophanis Continuati nomine fertur Libri I–IV, CFHB 53, De Gruyter, 2015"
  translation_used: as above (facing-page English)
  reliability_assessment: "Politically motivated reconstruction of the ninth century from the perspective of the Macedonian dynasty; hostile to the Amorian dynasty (including Theophilos)."
  known_biases: "Anti-Amorian; constructs Theophilos's reign through a moralising and at times hostile lens."
  dependencies: []
  notes: |
    Book III treats Theophilos's reign and the Amorium campaign in detail.
    The Continuator draws on now-lost ninth-century material; this
    dependency is acknowledged narratively here but not modelled as a
    Source record (lost sources are recorded only when independently
    cited).

- id: SRC-0003
  standardised_title: "al-Yaʿqūbī, Taʾrīkh"
  author_id: ENT-PERS-0025
  date_of_composition:
    start: 889
    end: 892
    precision: year_range_narrow
    confidence: 4
  language: ar
  genre: universal_chronicle
  edition_used: "Houtsma, M. Th. (ed.), Ibn-Wādhih qui dicitur al-Jaʿqubī Historiae, Leiden, 1883"
  reliability_assessment: "Independent of al-Ṭabarī; shorter but valuable for confirming or qualifying al-Ṭabarī's account."
  known_biases: "Shīʿī sympathies discernible in earlier sections; for ninth-century events generally restrained."
  dependencies: []
  notes: ""

- id: SRC-0004
  standardised_title: "Acta of the Forty-Two Martyrs of Amorium (Euodios recension)"
  alternative_titles: ["Passion of the Forty-Two Martyrs of Amorion"]
  author_id: ENT-PERS-0026      # → Euodios the Monk
  date_of_composition:
    start: 845
    end: 880
    precision: year_range_broad
    confidence: 3
  language: grc
  genre: hagiography
  edition_used: "Vasil'evskij, V. & Nikitin, P. (eds.), Skazaniia o 42 amoriiskikh muchenikakh, St Petersburg, 1905"
  reliability_assessment: "Strong hagiographic shaping; reliable for the existence and broad fate of the officers, much less so for theological dialogue scenes set in Samarra."
  known_biases: "Hagiographic conventions; theological agenda concerning iconoclasm and Islam."
  dependencies: []
  notes: "One of several extant recensions; identification of the Euodios recension as earliest is itself disputed."

- id: SRC-0005
  standardised_title: "Lightfoot, C. S. & Lightfoot, M. A., Amorium: A Byzantine City in Anatolia (Istanbul, 2007); annual preliminary reports in Anatolian Studies"
  author_id: ENT-PERS-0027
  date_of_composition:
    start: 1988
    end: 2026
    precision: year_range_broad
    confidence: 5
  language: en
  genre: archaeological_publication
  edition_used: "as cited"
  reliability_assessment: "Standard archaeological reference for the site."
  known_biases: "Interpretive emphasis on the 838 destruction horizon; ongoing reassessment as excavation continues."
  dependencies: []
  notes: |
    Used here as exemplar of an archaeological source carrying
    material-culture provenance. Builds on R. M. Harrison's 1988
    foundational survey; the dependency is acknowledged narratively
    here but the precursor survey is not modelled as a separate
    Source record.
```

### C.3 Place entity records

Three places are sufficient to demonstrate the spatial framework, including the disputed-identification case (Anzen/Dazimon).

```yaml
- id: ENT-PLC-0001
  standardised_name: "Amorium"
  alternative_names:
    - { form: "Amorion", language: grc, script: Grek }
    - { form: "ʿAmmūriya", language: ar, script: Arab }
    - { form: "Amorion", language: la,  script: Latn }
  persistent_identifiers:
    internal_id: ENT-PLC-0001
    external_identifiers:
      - { authority: pleiades, identifier: "609302", uri: "https://pleiades.stoa.org/places/609302" }
      - { authority: wikidata, identifier: "Q174270", uri: "https://www.wikidata.org/wiki/Q174270" }
      - { authority: geonames, identifier: "312069", uri: "https://sws.geonames.org/312069/" }
      - { authority: tgn,      identifier: "6000247", uri: "http://vocab.getty.edu/tgn/6000247" }
  place_type: settlement
  identification_status: identified
  identification_confidence: 5
  coordinates:
    latitude: 39.0211
    longitude: 31.2867
    crs: EPSG:4326
    coordinate_source: "Amorium excavation project survey data"
    coordinate_method: archaeological_survey
    coordinate_precision: site
    uncertainty_radius_m: 50
    coordinate_confidence: 5
  political_affiliation_history:
    - { value: ENT-POL-0001, valid_from: 600, valid_to: 838, confidence: 5 }
    - { value: ENT-POL-0002, valid_from: 838, valid_to: 841, confidence: 4 }
    - { value: ENT-POL-0001, valid_from: 841, valid_to: 1067, confidence: 3 }
  administrative_status_history:
    - { value: "capital of the Anatolikon theme", valid_from: 669, valid_to: 838, confidence: 5 }
  frontier_role: "Principal Byzantine stronghold and theme capital of central Anatolia; second city of the Empire by some measures."
  environmental_setting: "Central Anatolian plateau, on the route between the Cilician Gates and Constantinople."
  chronology:
    earliest_attestation: -100   # Hellenistic
    latest_significant_activity: 1116
    precision: century
    confidence: 4
  overall_confidence: 5
  analytical_summary: |
    Amorium was the principal Byzantine military and administrative centre of
    central Anatolia from the seventh century onwards and the ancestral home of
    the Amorian dynasty. Its capture by al-Muʿtaṣim in August 838 represents
    the most significant Byzantine territorial loss of the ninth century and is
    archaeologically attested through a destruction horizon at the excavated
    site at Hisarköy, near modern Emirdağ.
  linked_attestations: [ATT-0001, ATT-0002, ATT-0005, ATT-0011]
  linked_interpretations: [INT-0001]

- id: ENT-PLC-0002
  standardised_name: "Anzen / Dazimon (battle site of 22 July 838)"
  alternative_names:
    - { form: "Anzen",        language: grc, script: Grek, attested_in: [SRC-0002] }
    - { form: "Dazimon",      language: grc, script: Grek, attested_in: [SRC-0002] }
    - { form: "Dāzimūn",      language: ar,  script: Arab, attested_in: [SRC-0001] }
  place_type: battle_site
  identification_status: disputed
  identification_confidence: 2
  coordinates:
    # Best modern hypothesis (Treadgold, following local topographic study);
    # not all scholars accept this identification.
    latitude: 40.30
    longitude: 36.50
    crs: EPSG:4326
    coordinate_source: "Modern scholarly identification (Treadgold 1988)"
    coordinate_method: scholarly_identification
    coordinate_precision: locality
    uncertainty_radius_m: 25000
    coordinate_confidence: 2
  frontier_role: "Site of the decisive Byzantine defeat preceding the fall of Amorium."
  overall_confidence: 3
  analytical_summary: |
    The battle in which al-Afshīn defeated a Byzantine field army under
    Theophilos on 22 July 838, opening the way for the siege of Amorium.
    Greek sources name the site Anzen; Arabic sources name the fortress
    Dāzimūn. Whether these refer to the same location, or to a battle and a
    nearby fortress respectively, is disputed in modern scholarship. The
    most widely accepted modern identification places the engagement in the
    Dazimon plain near modern Tokat in north-central Anatolia, but the
    identification is not secure.
  linked_attestations: [ATT-0006, ATT-0007]
  linked_interpretations: [INT-0002]
  notes: |
    This entity exemplifies the use of identification_status = disputed.
    Per §4.3, the competing identifications are recorded within a single
    entity rather than generating duplicate entities. The two named forms
    (Anzen, Dazimon) are recorded as alternative names; the question of
    whether they denote the same place is captured by the disputed status
    and developed in interpretation INT-0002.

- id: ENT-PLC-0003
  standardised_name: "Samarra"
  alternative_names:
    - { form: "Surra man raʾā", language: ar, script: Arab }
    - { form: "Sāmarrāʾ",        language: ar, script: Arab }
  place_type: capital_city
  identification_status: identified
  identification_confidence: 5
  coordinates:
    latitude: 34.1983
    longitude: 43.8742
    crs: EPSG:4326
    coordinate_source: "UNESCO World Heritage Site coordinates"
    coordinate_method: modern_map
    coordinate_precision: site
    uncertainty_radius_m: 1000
    coordinate_confidence: 5
  frontier_role: "Abbasid imperial capital 836–892; place of detention and execution of the Forty-Two Martyrs of Amorium."
  overall_confidence: 5
  analytical_summary: |
    Abbasid imperial capital from 836 to 892, founded by al-Muʿtaṣim some
    125 km north of Baghdad. Place of detention and execution of the
    Forty-Two Martyrs of Amorium and a principal centre of cross-frontier
    diplomatic and prisoner exchange in the ninth century.
  linked_attestations: [ATT-0010]
```

### C.4 Person entity records

```yaml
- id: ENT-PERS-0001
  standardised_name: "al-Muʿtaṣim biʾllāh"
  alternative_names:
    - { form: "Abū Isḥāq Muḥammad ibn Hārūn", language: ar, script: Arab, name_type: kunya_nasab }
    - { form: "Mōtasém",                       language: grc, script: Grek, name_type: transliteration }
  persistent_identifiers:
    internal_id: ENT-PERS-0001
    external_identifiers:
      - { authority: pmbz,     identifier: "16385", uri: "https://www.degruyter.com/database/PMBZ/entry/PMBZ16385/html" }
      - { authority: wikidata, identifier: "Q314037", uri: "https://www.wikidata.org/wiki/Q314037" }
  person_type: caliph
  political_affiliation: ENT-POL-0002
  offices_held:
    - { office: "Caliph of the Abbasid Caliphate", valid_from: 833, valid_to: 842, confidence: 5 }
  birth:
    date: { start: 794, end: 794, precision: year, confidence: 4 }
  death:
    date: { start: 842, end: 842, precision: year, confidence: 5 }
    place_id: ENT-PLC-0003
  overall_confidence: 5
  analytical_summary: |
    Abbasid caliph (r. 833–842), son of Hārūn al-Rashīd. Led the 838
    campaign against Byzantium in person, founded the new caliphal capital
    at Samarra, and is associated with the deportation and detention of
    the Forty-Two Martyrs of Amorium.
  linked_attestations: [ATT-0001, ATT-0003]

- id: ENT-PERS-0002
  standardised_name: "Theophilos"
  alternative_names:
    - { form: "Θεόφιλος",  language: grc, script: Grek }
    - { form: "Tawfīl",    language: ar,  script: Arab }
  persistent_identifiers:
    internal_id: ENT-PERS-0002
    external_identifiers:
      - { authority: pmbz,     identifier: "19429", uri: "https://www.degruyter.com/database/PMBZ/entry/PMBZ19429/html" }
      - { authority: wikidata, identifier: "Q221356", uri: "https://www.wikidata.org/wiki/Q221356" }
  person_type: emperor
  political_affiliation: ENT-POL-0001
  offices_held:
    - { office: "Emperor of the Romans (Byzantine)", valid_from: 829, valid_to: 842, confidence: 5 }
  birth:
    date: { start: 813, end: 813, precision: year, confidence: 3 }
  death:
    date: { start: 842, end: 842, precision: year, confidence: 5 }
  overall_confidence: 5
  analytical_summary: |
    Byzantine emperor (r. 829–842) of the Amorian dynasty. Defeated by
    al-Afshīn at Anzen / Dazimon on 22 July 838, and unable to relieve
    the siege of his ancestral city Amorium the following month. The 838
    campaign permanently damaged his political standing.
  notes: "Member of the Amorian dynasty; native city captured during his reign."
  linked_attestations: [ATT-0002, ATT-0006]
```

### C.5 Event entity records

The episode is modelled as one parent campaign event with three child events, demonstrating how nested chronologies are represented.

```yaml
- id: ENT-EVT-0001
  standardised_name: "Abbasid campaign against Byzantium, 838"
  event_type: { primary: military, sub: campaign }
  start_date:
    start: 838-04-04         # approximate; muster of army at Tarsus per al-Ṭabarī
    precision: month
    confidence: 3
  end_date:
    start: 838-09-15         # approximate; al-Muʿtaṣim's withdrawal
    precision: month
    confidence: 3
  dating_basis:
    - { system: AH, value: "AH 223" }
    - { system: AD, value: "838" }
    - { system: AM_byzantine, value: "AM 6330" }
  associated_places: [ENT-PLC-0001, ENT-PLC-0002]
  participants: [ENT-PERS-0001, ENT-PERS-0002]
  political_entities_involved: [ENT-POL-0001, ENT-POL-0002]
  child_events: [ENT-EVT-0002, ENT-EVT-0003, ENT-EVT-0004]
  description: |
    Major Abbasid retaliatory campaign launched by al-Muʿtaṣim against
    Byzantium in response to Theophilos's attack on Zibatra (Sozopetra) the
    previous year. The campaign involved two columns, the defeat of a
    Byzantine relief army at Anzen/Dazimon, and the siege and capture of
    Amorium.
  historical_significance: |
    The most consequential single campaign of the ninth-century
    Byzantine–Abbasid frontier; widely treated in both modern scholarship
    and contemporary sources as a turning point in the visibility and
    morale of the Amorian dynasty.
  overall_confidence: 5
  analytical_summary: |
    The Abbasid campaign of 838 was the largest single military operation
    on the Byzantine-Islamic frontier of the ninth century. Launched by
    al-Muʿtaṣim in retaliation for Theophilos's attack on Zibatra the
    previous year, it produced the symbolic and strategic disaster of the
    sack of Amorium and reshaped Byzantine perceptions of frontier
    vulnerability for a generation.
  linked_attestations: [ATT-0001, ATT-0002, ATT-0003]
  linked_interpretations: [INT-0001]

- id: ENT-EVT-0002
  standardised_name: "Battle of Anzen / Dazimon"
  event_type: { primary: military, sub: battle }
  parent_event: ENT-EVT-0001
  start_date:
    start: 838-07-22
    precision: exact_day
    confidence: 4
  end_date:
    start: 838-07-22
    precision: exact_day
    confidence: 4
  associated_places: [ENT-PLC-0002]
  participants: [ENT-PERS-0002]
  overall_confidence: 4
  analytical_summary: |
    Decisive engagement of 22 July 838 in which al-Afshīn's column
    defeated a Byzantine field army under Theophilos, opening the road
    to Amorium. The battle is the principal what-if of the campaign:
    a Byzantine victory at Anzen would plausibly have prevented the
    subsequent siege.
  linked_attestations: [ATT-0006, ATT-0007]

- id: ENT-EVT-0003
  standardised_name: "Siege of Amorium"
  event_type: { primary: military, sub: siege }
  parent_event: ENT-EVT-0001
  start_date:
    start: 838-08-01
    precision: month
    confidence: 3
  end_date:
    start: 838-08-12
    end:   838-08-15
    precision: year_range_narrow
    confidence: 2
  associated_places: [ENT-PLC-0001]
  participants: [ENT-PERS-0001, ENT-PERS-0002]
  overall_confidence: 4
  analytical_summary: |
    Siege of Amorium by the reunited Abbasid army following the victory
    at Anzen. Approximate duration two weeks; ended in storming and sack
    after a defector indicated a structurally weak section of the wall.
    Source traditions disagree on duration; the disagreement is preserved
    at the observation level rather than resolved.
  notes: |
    Duration of the siege is disputed in the sources. al-Ṭabarī's account is
    consistent with a siege of approximately twelve to thirteen days;
    Theophanes Continuatus implies a longer duration; modern scholarship
    has settled on roughly two weeks. See observations OBS-0004 and
    OBS-0005 and the contradictions recorded there.
  linked_attestations: [ATT-0001, ATT-0002, ATT-0008, ATT-0009]

- id: ENT-EVT-0004
  standardised_name: "Sack of Amorium and deportation of population"
  event_type: { primary: military, sub: sack_of_city }
  parent_event: ENT-EVT-0001
  start_date:
    start: 838-08-12
    end:   838-08-15
    precision: year_range_narrow
    confidence: 2
  associated_places: [ENT-PLC-0001, ENT-PLC-0003]
  overall_confidence: 5
  analytical_summary: |
    Storming, sack, and depopulation of Amorium following the breach of
    the walls. Surviving population deported; forty-two named officers
    among them eventually executed at Samarra in 845 as the Forty-Two
    Martyrs. The destruction horizon at the excavated site at Hisarköy
    provides archaeological confirmation.
  linked_attestations: [ATT-0001, ATT-0002, ATT-0010, ATT-0011]
```

### C.6 Observation and attestation records

This is the heart of the model. Each observation is a discrete propositional claim; each attestation is the evidential record of one source supporting that claim. Two of the observations below are explicitly contradicted by other observations, demonstrating how contradiction is preserved rather than resolved.

```yaml
# --- Observations ---

- id: OBS-0001
  proposition: "Al-Muʿtaṣim led a major campaign against Byzantium in 838."
  associated_entities: [ENT-EVT-0001, ENT-PERS-0001]
  supporting_attestations: [ATT-0001, ATT-0003]
  contradicting_attestations: []

- id: OBS-0002
  proposition: "Amorium fell to Abbasid forces in August 838."
  associated_entities: [ENT-EVT-0004, ENT-PLC-0001]
  supporting_attestations: [ATT-0001, ATT-0002, ATT-0011]
  contradicting_attestations: []

- id: OBS-0003
  proposition: "Theophilos was defeated at Anzen/Dazimon on 22 July 838 by al-Afshīn."
  associated_entities: [ENT-EVT-0002, ENT-PERS-0002]
  supporting_attestations: [ATT-0006, ATT-0007]
  contradicting_attestations: []

- id: OBS-0004
  proposition: "The siege of Amorium lasted approximately twelve to thirteen days."
  associated_entities: [ENT-EVT-0003]
  supporting_attestations: [ATT-0008]      # al-Ṭabarī
  contradicting_attestations: [ATT-0009]   # Theophanes Continuatus implies longer

- id: OBS-0005
  proposition: "The siege of Amorium lasted approximately fifty-five days."
  associated_entities: [ENT-EVT-0003]
  supporting_attestations: [ATT-0009]
  contradicting_attestations: [ATT-0008]
  notes: |
    Observations OBS-0004 and OBS-0005 are explicitly contradictory and
    are both retained, per §3.4. The event record ENT-EVT-0003 carries a
    duration range broad enough to accommodate either; modern scholarship
    (INT-0001) inclines toward the shorter duration.

- id: OBS-0006
  proposition: |
    A traitor or defector inside Amorium revealed a structurally weak
    section of the city wall to the besiegers.
  associated_entities: [ENT-EVT-0003, ENT-PLC-0001]
  supporting_attestations: [ATT-0001, ATT-0002]
  contradicting_attestations: []
  notes: |
    The detail is reported in both major textual traditions but with
    different attribution and motivation. The shared core ("a weak point
    was revealed") is what the observation captures; tradition-specific
    elaborations are recorded at the attestation level.

- id: OBS-0007
  proposition: |
    Forty-two Byzantine officers captured at Amorium were held in Samarra
    and executed there in 845.
  associated_entities: [ENT-PLC-0003, ENT-EVT-0004]
  supporting_attestations: [ATT-0010]
  contradicting_attestations: []
  notes: "Some sources give 846; recorded at attestation level."

- id: OBS-0008
  proposition: |
    A destruction horizon at the excavated site of Amorium is consistent
    with violent sack in the mid-ninth century.
  associated_entities: [ENT-PLC-0001, ENT-EVT-0004]
  supporting_attestations: [ATT-0011]
  contradicting_attestations: []

# --- Attestations ---

- id: ATT-0001
  source: SRC-0001                              # al-Ṭabarī
  entities_referenced: [ENT-EVT-0001, ENT-PLC-0001, ENT-PERS-0001]
  observations_supported: [OBS-0001, OBS-0002, OBS-0006]
  provenance: primary_paraphrase
  citation: "al-Ṭabarī, Taʾrīkh, sub anno AH 223 (Cairo ed., vol. IX, pp. 56–69; Bosworth trans. XXXIII, pp. 95–123)"
  direct_quotation: ""
  paraphrase: |
    Under AH 223 al-Ṭabarī gives an extended account of al-Muʿtaṣim's
    campaign: the assembly of the army, the route through the Cilician
    Gates, al-Afshīn's victory over Theophilos, the march on Amorium, the
    siege, the role of a defector in indicating the weak section of the
    wall, the storming of the city, and the fate of its inhabitants.
  location_within_source: "AH 223 annal"
  editorial_interpretation: |
    al-Ṭabarī's account is the fullest single source; treated as the
    spine of any reconstruction of the campaign.
  confidence: 5

- id: ATT-0002
  source: SRC-0002                              # Theophanes Continuatus
  entities_referenced: [ENT-EVT-0001, ENT-PLC-0001, ENT-PERS-0002]
  observations_supported: [OBS-0002, OBS-0006]
  provenance: primary_paraphrase
  citation: "Theoph. Cont. III.29–34 (Featherstone–Signes Codoñer eds., pp. 168–195)"
  paraphrase: |
    Theophanes Continuatus narrates the campaign from the Byzantine
    perspective, with elaborate moralising about Theophilos's failures
    and explicit attribution of treachery to a named individual whose
    role corresponds to the defector reported in Arabic sources.
  confidence: 4
  notes: "Anti-Amorian framing strongly affects the interpretive surface."

- id: ATT-0003
  source: SRC-0003                              # al-Yaʿqūbī
  entities_referenced: [ENT-EVT-0001, ENT-PERS-0001]
  observations_supported: [OBS-0001]
  provenance: primary_summary
  citation: "al-Yaʿqūbī, Taʾrīkh (Houtsma ed., vol. II, pp. 581–582)"
  paraphrase: |
    al-Yaʿqūbī's account of the campaign is brief but independent and
    confirms the main outlines.
  confidence: 4

- id: ATT-0006
  source: SRC-0002
  entities_referenced: [ENT-EVT-0002, ENT-PLC-0002, ENT-PERS-0002]
  observations_supported: [OBS-0003]
  provenance: primary_paraphrase
  citation: "Theoph. Cont. III.30"
  paraphrase: |
    Theophanes Continuatus names the battle site Anzen and describes
    Theophilos's near-encirclement and escape.
  confidence: 4

- id: ATT-0007
  source: SRC-0001
  entities_referenced: [ENT-EVT-0002, ENT-PLC-0002]
  observations_supported: [OBS-0003]
  provenance: primary_paraphrase
  citation: "al-Ṭabarī, AH 223"
  paraphrase: |
    al-Ṭabarī names the location Dāzimūn (the fortress) and credits the
    victory to al-Afshīn's wing of the army.
  confidence: 4

- id: ATT-0008
  source: SRC-0001
  entities_referenced: [ENT-EVT-0003]
  observations_supported: [OBS-0004]
  provenance: primary_paraphrase
  citation: "al-Ṭabarī, AH 223"
  paraphrase: |
    The chronology of named days within al-Ṭabarī's account implies a
    siege of approximately twelve to thirteen days from the arrival of
    the Abbasid army before Amorium to the breach.
  confidence: 4

- id: ATT-0009
  source: SRC-0002
  entities_referenced: [ENT-EVT-0003]
  observations_supported: [OBS-0005]
  provenance: primary_summary
  citation: "Theoph. Cont. III.32"
  paraphrase: |
    Theophanes Continuatus's account, read as a continuous narrative,
    implies a substantially longer siege; one reading yields a duration
    of approximately fifty-five days.
  confidence: 2
  notes: |
    The longer figure is not stated explicitly but inferred from the
    narrative pacing; this attestation has lower confidence than the
    competing ATT-0008 and the editorial note records this.

- id: ATT-0010
  source: SRC-0004
  entities_referenced: [ENT-PLC-0003, ENT-EVT-0004]
  observations_supported: [OBS-0007]
  provenance: primary_paraphrase
  citation: "Acta of the Forty-Two Martyrs (Euodios recension), §§1–8"
  paraphrase: |
    The hagiographic account narrates the deportation of named Byzantine
    officers from Amorium, their detention in Samarra, theological
    disputation with Muslim interlocutors, and execution.
  confidence: 3
  notes: "Hagiographic shaping discounts confidence in incidental detail; the broad fact of detention and execution is well supported."

- id: ATT-0011
  source: SRC-0005
  entities_referenced: [ENT-PLC-0001, ENT-EVT-0004]
  observations_supported: [OBS-0002, OBS-0008]
  provenance: archaeological_evidence
  citation: "Lightfoot, C. S., 'Amorium: A Byzantine City in Anatolia', annual reports in Anatolian Studies, 1988–2015"
  paraphrase: |
    Excavations at Hisarköy / Emirdağ have identified a destruction
    horizon datable to the mid-ninth century, consistent with the sack
    of 838 and providing the principal archaeological confirmation of
    the textual record.
  confidence: 5
```

### C.7 Walk-through: from source passage to records

To make the extraction process concrete, consider a single passage. al-Ṭabarī, *Taʾrīkh*, sub anno AH 223 (paraphrased): "Then al-Muʿtaṣim moved against ʿAmmūriya. He invested it, and his men set up the mangonels. The siege lasted some days, until a man came out from the city to the Caliph and showed him a section of the wall where the stones had loosened and the mortar was poor. Al-Muʿtaṣim ordered his men to concentrate their assault on that point. The wall was breached, and the city was taken."

A correctly trained extractor working under this specification produces, from this single passage:

* Reuse, not creation, of the existing entity **ENT-PLC-0001** (Amorium) because "ʿAmmūriya" already appears among that entity's alternative-name forms (per the Master Record rule, §4.1).
* Reuse of **ENT-PERS-0001** (al-Muʿtaṣim) and **ENT-EVT-0003** (Siege of Amorium).
* Attachment of a new attestation **ATT-0001** (already constructed above) linking SRC-0001 to OBS-0002, OBS-0004, and OBS-0006.
* No new place entity for "the section of the wall," because architectural sub-features of an existing settlement are recorded as descriptive content within the parent place record's analytical summary, not as separate place entities (a decision the specification should make explicit and currently does not — see §C.11).
* Identification of the defector remains unnamed in al-Ṭabarī and is not promoted to a separate person entity; it is recorded only as a participant in OBS-0006, marked unidentified.

If a second source — Theophanes Continuatus — is then processed, the extractor encounters Greek "Amorion" and Greek personal names. Both forms resolve, via the Master Record procedure (§4.2), to existing entities. A new attestation **ATT-0002** is created. Where Theophanes Continuatus and al-Ṭabarī agree on the broad fact (the betrayal of a weak wall section), they support the same observation; where they diverge in detail (the identity and motivation of the defector), the differences are recorded at the attestation level rather than the observation level.

This is what cumulative-evidence accumulation actually looks like in operation. The database does not grow new entities; it accumulates attestations against existing entities, while preserving the textures of disagreement between sources.

### C.8 Interpretation records

```yaml
- id: INT-0001
  associated_entities: [ENT-EVT-0001, ENT-PLC-0001]
  scholar: "Treadgold, W."
  publication: "The Byzantine Revival, 780–842 (Stanford, 1988)"
  date: 1988
  argument: |
    The 838 campaign was strategically and symbolically devastating but did
    not produce permanent territorial loss; the siege itself, on Treadgold's
    reconstruction of the chronology, was relatively brief (closer to
    twelve days than fifty-five), and Amorium was reoccupied within years.
    The deeper damage was to Theophilos's prestige and the iconoclast
    programme he represented.
  supporting_evidence: [ATT-0001, ATT-0003, ATT-0008]
  counter_evidence: [ATT-0009]
  confidence: 4

- id: INT-0002
  associated_entities: [ENT-PLC-0002]
  scholar: "Multiple; summarised in Treadgold 1988 and revisited in subsequent literature"
  publication: "Treadgold 1988 et seq."
  date: 1988
  argument: |
    The battle named Anzen in Greek sources and Dāzimūn in Arabic sources
    is most plausibly located in the Dazimon plain near modern Tokat. The
    identification is not, however, universally accepted; alternative
    locations have been proposed, and the question turns on the
    reconstruction of the Abbasid army's route and the reading of
    topographic detail in both source traditions.
  supporting_evidence: [ATT-0006, ATT-0007]
  counter_evidence: []
  confidence: 3
  notes: |
    This interpretation justifies the disputed identification status and
    coordinate values recorded on ENT-PLC-0002. If a future critical
    reconsideration overturns the Treadgold identification, the coordinate
    values change but the entity does not split — per §4.3.
```

### C.9 Relationship records

A minimal but representative set:

```yaml
- id: REL-0001
  type: located_at
  source_entity: ENT-EVT-0003           # Siege of Amorium
  target_entity: ENT-PLC-0001           # Amorium
  temporal_scope: { start: 838-08-01, end: 838-08-15, precision: month, confidence: 4 }
  confidence: 5
  linked_attestations: [ATT-0001, ATT-0002]

- id: REL-0002
  type: participated_in
  source_entity: ENT-PERS-0001          # al-Muʿtaṣim
  target_entity: ENT-EVT-0001           # the campaign
  temporal_scope: { start: 838-04, end: 838-09, precision: month, confidence: 3 }
  confidence: 5
  linked_attestations: [ATT-0001, ATT-0003]

- id: REL-0003
  type: parent_event_of
  source_entity: ENT-EVT-0001
  target_entity: ENT-EVT-0003
  confidence: 5

- id: REL-0004
  type: different_from                  # source-to-source relationship
  source_entity: SRC-0003               # al-Yaʿqūbī
  target_entity: SRC-0001               # al-Ṭabarī
  confidence: 4
  notes: |
    Demonstrates that sources themselves can carry relationships and that
    source-network analysis is supported as a first-class operation.
    al-Yaʿqūbī's account of the 838 campaign is independent of al-Ṭabarī's
    rather than derivative from it, which is significant for evaluating
    the weight of agreement between the two.
```

### C.10 What this example demonstrates

Worked end-to-end, the example exercises and validates the principal mechanisms of the specification:

* **The Source–Attestation–Observation–Entity chain works as designed.** Each source generates attestations, each attestation supports observations, each observation concerns entities, and the many-to-many structure is preserved at every link (one attestation supports several observations; one observation is supported by several attestations).
* **Multilingual and multi-script names are accommodated within single entities** (Amorium / Amorion / ʿAmmūriya; Anzen / Dazimon / Dāzimūn), with the Master Record rule preventing entity duplication.
* **Disputed identification is recorded within a single entity** (the Anzen/Dazimon case) via the identification framework rather than by creating parallel duplicate entities.
* **Dual-axis time is exercised:** the campaign is dated to the month with confidence 3 (we know approximately when), the battle at Anzen to the exact day with confidence 4 (we know precisely, but not entirely beyond dispute), and the siege duration is recorded with a precision/confidence pair that reflects honest scholarly uncertainty.
* **Dual-axis space is exercised:** Amorium has high identification confidence and high coordinate confidence; Anzen/Dazimon has low identification confidence with a derived low coordinate confidence; Samarra has high identification confidence with archaeologically attested coordinates.
* **Contradiction is preserved rather than resolved:** OBS-0004 and OBS-0005 are explicitly contradictory and both retained, with an interpretation record indicating which way modern scholarship leans without suppressing the alternative.
* **Provenance types span the full range:** primary paraphrase, primary summary, and archaeological evidence are all present and behave consistently.
* **Source-network relationships are first-class** (REL-0004), demonstrating that the framework supports historiographical analysis and textual-dependency studies.
* **The Master Record rule operates as the operational backbone:** every attestation attaches to existing entities; no duplicates are generated.
* **The three-layer structure (analytical data, summary, evidence) holds** across all record types, with structured fields on top, prose summaries in the middle, and attestations carrying the evidential layer.

### C.11 What this example reveals as still under-specified

Working the example end-to-end exposes gaps in the prose specification that no amount of further prose elaboration will close. These are recorded honestly here as the agenda for the next round of specification work.

1. **Sub-feature entities.** When al-Ṭabarī mentions "a section of the wall where the stones had loosened," should this be a place entity or a descriptive detail attached to ENT-PLC-0001? The specification does not say. A rule is needed. The working assumption used here is that architectural sub-features below the level of a discrete named building are *not* entities, but this should be formalised.

2. **Unnamed participants.** The defector at Amorium is referred to but unnamed in al-Ṭabarī, and named (differently) in some later sources. The specification offers no clear mechanism for "anonymous participant" entities that may or may not later be identified with named persons.

3. **Persistent identifiers and minting authority.** The example uses ad-hoc identifiers (ENT-PLC-0001, ATT-0001, etc.). For interoperability and citation, these must be URIs minted under a documented policy. The specification does not define this.

4. **Dating-system reconciliation.** The campaign event carries AH, AD, and AM dates side by side, but the specification does not formalise how, for instance, an AH date that crosses a Julian year boundary is normalised into the database's primary timeline. The Amorium campaign is recorded in al-Ṭabarī under AH 223, which spans 4 December 837 to 22 November 838 CE — a real ambiguity that requires a documented conversion and disambiguation rule.

5. **Temporal versioning of attributes.** Amorium's `political_affiliation_history` field used here is a list of time-bounded entries, which the prose specification does not actually mandate. Either the prose must be amended to require this pattern for all attributes that change over time, or a more general temporal-versioning mechanism must be specified.

6. **CRS declaration.** The example records `crs: EPSG:4326` on every coordinate, but the prose specification never says this is required. It must.

7. **Manuscript witnesses.** The Acta of the Forty-Two Martyrs survives in multiple recensions of differing dates and dependencies; SRC-0004 collapses these into a single Source record. A real source-critical project requires witness-level modelling, which the specification does not provide.

8. **Aggregation rule for entity-level confidence.** ENT-EVT-0003 carries `overall_confidence: 4`. How that number is derived from the confidences of its supporting attestations (ranging from 2 to 5) is not specified. Until an aggregation rule is defined, overall_confidence values are editorially imposed rather than algorithmically derived.

9. **CIDOC-CRM and Linked Places alignment.** The example records map readily onto CIDOC-CRM classes (E5_Event for events, E53_Place for places, E21_Person for persons, E33_Linguistic_Object for source passages, P70_documents for the attestation relation) and onto the Linked Places format used by World-Historical Gazetteer and Pelagios. The specification does not commit to either alignment. This is the largest remaining ecosystem-interoperability gap.

10. **Schema artefact.** The records above are valid YAML but conform to no published schema (JSON Schema, SHACL shape, OWL ontology). Until such a schema exists, "the specification" remains a prose document and "the database" cannot be validated.

These ten items constitute the genuine remaining work. Items 4, 5, 6, 8, 9, and 10 in particular cannot be resolved in prose; they require either schema definitions or alignment commitments. The worked example has earned them their place on a real agenda.
