# Research Questions — Byzantine-Islamic Frontier Database (BIFD)

*Design inputs for the conceptual ontology. This document defines the analytical programme the database must support. Every entity type in the eventual schema is justified against a research question stated here; any proposed type that does not enable a query or workflow named in this document does not belong.*

---

## 1. Introduction

### Intellectual framing

This project's underlying premise is that frontier landscapes are not passive settings for historical events but are actively produced and transformed through networks of movement, settlement, political authority and environmental constraint. A frontier is not a line on a map but a zone whose physical, social and political configuration is the cumulative outcome of the processes that operated across it: the routing of raids and trade, the founding and abandonment of fortifications, the extension and contraction of settlement, the imposition and collapse of administrative control, the exploitation and exhaustion of agricultural and pastoral resources. To study such a frontier is to study those processes and their material traces, not merely to catalogue the sites they left behind.

Archaeological sites are the material residues of processes that operated across wider landscapes. Fortifications, settlements, monasteries, roads and agricultural systems cannot be understood in isolation, because their significance derives from the networks of movement, communication, visibility, production and authority within which they were embedded. A fort matters because of the pass it watches, the route it guards and the settlements it protects; a monastery matters because of the roads that served it and the community it drew; an agricultural system matters because of the garrisons it fed. The landscape, rather than the individual site, therefore constitutes the appropriate analytical unit for investigating frontier organisation and transformation. This choice of unit is what makes the ontological apparatus that follows necessary: to study landscapes rather than sites is to require a data model that represents relationships, phases and processes, not merely places.

The database described here is the research instrument through which those landscape processes can be investigated rigorously. It is not a repository of sites and sources but the analytical framework that makes it possible to integrate archaeological, historical and spatial evidence, to represent the same landscape at different moments in time, to hold competing scholarly interpretations transparently, and to trace the relationships — of movement, dependence, control and visibility — through which frontier landscapes were organised. The intellectual contribution of the project and the design of the database are therefore inseparable: the questions the project asks require a data model capable of representing landscapes as evolving systems, and that data model in turn makes new forms of analysis possible.

### Central research question

**How were the Byzantine-Islamic frontier landscapes of Anatolia produced, organised and transformed between c. AD 750 and 950, and how can archaeological, historical and spatial evidence be integrated to reconstruct those processes?**

The verbs are deliberate. *Produced* and *transformed* encode the premise that these landscapes are historical outcomes rather than natural givens; *organised* names the structuring work of movement, settlement and authority. The second clause names the methodological problem the database exists to solve: the integration of three distinct evidence categories — archaeological, historical and spatial — each with its own provenance, granularity and uncertainty.

The framing deliberately avoids *experienced*. Questions of perception, identity and lived experience, while intellectually significant, are difficult to substantiate from the available evidence in the way that questions of production, organisation and transformation are not. Where the evidence later supports claims about how frontier landscapes were perceived or inhabited, those claims can be developed within specific chapters; but the headline question does not promise what the corpus cannot reliably deliver.

### What this document contains and what it is for

This document states five research questions — three substantive (Landscape and Mobility; Settlement Systems; Landscape Transformation) and two concerning the research instrument itself (Evidence Integration; Analytical Infrastructure) — each with subordinate questions. It then sets out the ontology principles that follow from these questions, a catalogue of edge cases against which the eventual ontology must be tested, brief notes on the project's theoretical framework and its comparative scope, and the criteria by which the eventual ontology's success will be judged.

The document is an input to the conceptual ontology work, not the ontology itself. It does not specify entity types, attributes or schemas. It specifies what the database must enable. The ontology that follows will be evaluated against this document at every step: each proposed entity type must name the research question it serves, and any type that serves none will be reconsidered.

---

## 2. Corpus scope and analytical scope

The database corpus and the dissertation's analytical window are deliberately distinct.

**Corpus scope: c. AD 640-1100.** The database holds evidence for the frontier zone from the Arab conquests through to the eve of the Seljuk transformation. This wide range is a design decision, not an accident of collection. It allows the database to support questions that reach beyond the dissertation's immediate focus — how the mature Abbasid frontier differed from its Umayyad precursor, how the tenth-century Byzantine reconquests transformed earlier frontier systems — without any redesign. The ontology should not be constrained by the dissertation's chronology.

**Analytical scope: c. AD 750-950.** The dissertation's analytical heart is the mature raiding frontier of the Abbasid-Byzantine period: the thughūr and ʿawāṣim as a functioning system, the seasonal rhythm of raid and counter-raid, the settlement and defensive structures that sustained it. This is the period for which the evidence is richest and the frontier's character most distinctive.

The distinction matters for the schema because temporal boundaries are properties of the analysis, not of the data model. A site occupied from the sixth century to the fourteenth has phases spanning that whole range; the database records all of them, and the dissertation attends to those falling within 750-950. The ontology must therefore model time without privileging any particular window.

The same distinction holds spatially. The database is designed as a research infrastructure for the Byzantine-Islamic frontier as a whole. Individual studies, including the dissertation this specification serves, analyse particular frontier sectors within that wider corpus; sectoral boundaries are therefore analytical groupings imposed by a study, not divisions of the domain model. The database's first substantive application is the northeast Anatolian corridor, but the corpus already holds southern (Cilician and Jaziran) material that serves both as foundation and as comparative baseline, and it is not built around any single sector. Just as temporal windows are selected by the analysis rather than encoded in the data, so are spatial ones: the ontology models the frontier as a domain, and sectors, regions and study areas are researcher-defined groupings over that domain rather than fixed features of it.

---

## 3. Substantive research questions

### RQ1 — Landscape and Mobility

**How did landscape structure movement, communication and control across the Byzantine-Islamic frontier?**

The frontier was above all a zone of movement: of raiding armies, of trade, of pilgrims and prisoners, of pastoralists and their flocks. That movement was shaped by topography — the passes through the Taurus and Anti-Taurus, the river crossings of the Euphrates and its tributaries, the corridors that mountainous terrain left open or closed — and it was in turn the object of control, monitoring and exploitation by both Byzantine and Islamic polities.

Subordinate questions:

- How did topography, hydrology and environmental constraint condition the routes available for movement across the frontier?
- How were passes, river crossings and other critical landscape features controlled, monitored and exploited, and by what installations (fortifications, watch-posts, kleisourai)?
- Can recurring corridors of movement — route families that persisted even as specific tracks shifted — be identified from the combined archaeological, historical and spatial evidence?
- How did the routes attested in the geographical and historical sources relate to the routes that least-cost analysis of the terrain would predict?

This theme motivates the project's spatial analysis most directly. Least-cost path modelling, route-corridor identification and viewshed analysis are the analytical operations through which these questions are answered, and they require the database to hold landscape features, routes and geometries as first-class spatial objects with their own chronology and provenance.

### RQ2 — Settlement Systems

**How did frontier settlements, fortifications and associated infrastructure develop, function and change through time?**

Frontier settlement was not static. A site might begin as a Late Roman fort, expand under Umayyad or early Abbasid patronage, contract in the face of Byzantine pressure, shift function from garrison to monastery to village, and change its physical extent and morphology at each stage. Understanding the frontier requires the ability to represent this change rather than flattening a site to a single set of properties.

Subordinate questions:

- How did the morphology and extent of frontier settlements change between the eighth and tenth centuries?
- How did the function of sites change — between military, ecclesiastical, agricultural and administrative roles — and how are those functional shifts evidenced?
- Can settlement hierarchies be reconstructed, distinguishing major fortified centres from subordinate installations and open settlements?
- How did fortifications, settlements, monasteries, agricultural landscapes and communications infrastructure relate to one another spatially and functionally?
- Can regional defensive systems — coordinated networks of fortification rather than isolated sites — be identified?

This theme directly motivates the temporal and componential structure of the ontology: sites with phases, phases with their own geometry and function, constituent components (walls, towers, gates, churches, cisterns) with independent chronologies, and relationships linking sites to one another and to the wider landscape.

### RQ3 — Landscape Transformation

**How did military, political, economic and environmental processes reshape frontier landscapes?**

Frontier landscapes were produced and transformed by identifiable processes: warfare and its destructions and refoundations; administrative reorganisation such as the creation of the ʿawāṣim; the economic conditions — agricultural productivity, resource extraction, the fiscal demands of maintaining garrisons — that sustained or undermined settlement; and environmental events and constraints from earthquakes to the limits of cultivable land. Understanding transformation requires modelling these processes explicitly, as events and conditions that act upon the landscape, rather than merely recording their outcomes.

Subordinate questions:

- How did military conflict — siege, capture, destruction, refoundation — drive the development, contraction and abandonment of frontier sites?
- How did administrative and political reorganisation reshape the frontier's structure and the distribution of authority across it?
- How did economic processes — agricultural exploitation, resource extraction, the fiscal burden of defence — sustain or undermine frontier settlement?
- How did environmental conditions and events condition the possibilities of settlement and movement?
- Through what mechanisms did the frontier facilitate interaction as well as conflict?

The final subordinate question requires operationalisation, since *interaction* is otherwise too vague to guide evidence collection. The frontier facilitated interaction through identifiable mechanisms, each producing distinct evidence: **trade and exchange; pilgrimage; diplomacy; prisoner exchange; raiding; taxation; pastoral movement; agricultural exploitation; military logistics; communication; and migration.** Naming these mechanisms specifies what the database must be able to capture and resists the simplistic model of the frontier as a barrier that only divided.

This theme motivates event modelling: the database must represent foundations, destructions, sieges, reoccupations, abandonments and administrative changes as first-class objects that act upon sites and landscapes, linked to the evidence attesting them and to the phases they produce.

---

## 4. Research questions concerning the instrument

The following two questions concern the research instrument itself. They are not lesser questions. A research instrument that makes previously infeasible analysis possible is a genuine contribution to knowledge, in the way that a new analytical method is: the instrument does not merely organise what is already known but enables new questions to be asked and answered. These two questions are answered by the design and existence of the database and by what its use reveals, rather than by empirical findings about the frontier alone.

### RQ4 — Evidence Integration

**How can archaeological, historical and spatial evidence be integrated to reconstruct frontier landscapes while preserving uncertainty, provenance and competing interpretations?**

The frontier is known through radically heterogeneous evidence: excavation and survey reports, the Arabic and Byzantine geographical and historical traditions, inscriptions and seals, the volumes of the Tabula Imperii Byzantini, travellers' accounts, and increasingly remote sensing and spatial analysis. These sources complement, contradict and refine one another. A fortress may be described by al-Ṭabarī, located by Ibn Khurradādhbih, surveyed by one team and excavated by another, each producing statements that do not straightforwardly agree. Most databases treat such disagreement as a problem to be resolved by editorial fiat; this project treats it as a phenomenon to be represented.

Subordinate questions:

- How do archaeological, historical and spatial sources complement, contradict or refine one another in reconstructing the frontier?
- How can the provenance of every statement — which source, reached through which chain of transmission, at what evidential level — be preserved rather than flattened?
- How can competing scholarly interpretations of the same evidence be represented transparently, without the database privileging one reading?
- How can uncertainty be represented as the multidimensional quantity it is, rather than as a single confidence score?

This theme is the intellectual justification for the attestation-provenance model that the existing corpus already embodies, and for the distinction, developed below, between observations (what a source records, with provenance) and interpretations (scholarly readings of one or more observations). It is where the database's methodological contribution is most concentrated.

### RQ5 — Analytical Infrastructure

**What new forms of archaeological analysis become possible through the development of an integrated spatiotemporal research information system for the Byzantine-Islamic frontier?**

The database is a research instrument, and this question asks what that instrument makes possible. The claim is not merely that an integrated system is more convenient than dispersed scholarly resources, but that certain analytical operations become feasible only when archaeological, historical and spatial evidence are held together in an ontologically consistent structure that represents time, space, evidence and interpretation as first-class objects.

Subordinate questions:

- What spatial and network analyses — least-cost path modelling, viewshed and intervisibility analysis, catchment and territory reconstruction, network analysis of relationships between sites and landscape features — become possible when the evidence is integrated spatially?
- What temporal analyses — the tracing of settlement expansion and contraction, the correlation of destructions and refoundations with attested events, the reconstruction of a site's or a region's phased development — become possible when the evidence is modelled with explicit chronology?
- How does holding provenance and competing interpretations as first-class data change what can be asked of the evidence, compared with a database that stores only resolved conclusions?
- What publication-quality outputs — phased maps, gazetteers, network diagrams, analytical tables — can the integrated system generate directly from its data?

This theme justifies the ambition of the whole enterprise. It is answered by demonstrating analyses that would not have been possible without the instrument.

---

## 5. Ontology principles

Before the principles themselves, the following table records, at a glance, which ontology capabilities each research question requires. It exists so that every entity type, relationship type and attribute in the eventual ontology can be traced back to the research question it serves — the operational form of principle 1. It is deliberately coarse; its purpose is not to specify the ontology but to make the justification for each of its parts immediately legible.

| Research question | Ontology capability required |
|---|---|
| RQ1 — Landscape and Mobility | Spatial entities (sites, landscape features, routes); geometries; first-class relationships (control, visibility, proximity); least-cost path and viewshed analysis |
| RQ2 — Settlement Systems | Persistent sites; site phases; components and component phases; multiple and phased geometries; settlement-hierarchy and defensive-system relationships |
| RQ3 — Landscape Transformation | Events as first-class objects; temporal relationships between events and phases; interaction mechanisms; links from events to the phases they produce |
| RQ4 — Evidence Integration | Observations with provenance; assertions; interpretations over observations; multidimensional certainty; competing-interpretation representation |
| RQ5 — Analytical Infrastructure | Directly queryable spatial, temporal and relational structures; GIS and network outputs generated from stored data without remodelling |

The following design commitments follow from the research questions above. They constrain the conceptual ontology and are stated here so that the ontology work can be held to them.

1. **Research questions before ontology.** Every entity type in the eventual schema must be justified against a research question in this document. A type that enables no query or workflow named here does not belong, however elegant it might be. The test is not whether a thing could be modelled but whether modelling it changes what can be searched, analysed or interpreted.

2. **Persistent identity is independent of changing properties.** Persistent entities retain their identity despite changes in geometry, function, chronology or interpretation. Change is represented through associated temporal, spatial and interpretative records rather than by replacing the underlying entity. A site that shifts its footprint, changes function from fortress to monastery, is redated by a new excavation or is reinterpreted by a new reading remains the same site; the changes are carried by its phases, geometries and interpretations, not by its destruction and replacement. This is the ontological commitment that makes the database spatiotemporal rather than a gazetteer, and it is the single principle from which site phases, component phases, multiple geometries, changing names, functional shift and reinterpretation all follow.

3. **Space and time are co-equal dimensions.** Spatial and temporal properties are modelled independently, and neither is privileged over the other. No entity possesses a single geometry or a single date by default; both may vary through successive phases, and each geometry and each date carries its own provenance and uncertainty. This principle is the spatiotemporal corollary of persistent identity: because an entity persists through change, its location and its chronology are not fixed attributes but sequences of dated, sourced states. It is what makes phased geometry, multiple contemporaneous geometries, temporal GIS and independent spatial and chronological uncertainty possible within a single model.

4. **Ontology is distinct from epistemology: the object is not its interpretation.** A structure exists independently of what is known or believed about it. When scholars disagree whether a building was a monastery, a palace or a caravanserai, the building itself is not in dispute; only knowledge of it is. Physical objects — sites, components, landscape features — are therefore stable records representing what exists, while assertions and interpretations represent what is known or argued about them and accumulate around the object through observations. The object is never made uncertain by interpretive disagreement about its function. This separation of the thing from knowledge of the thing underpins nearly every later design decision.

5. **Two-level evidence: observation to interpretation.** The database distinguishes observations from interpretations, but no further. An observation is what a source records — an excavation finding, a survey result, a textual statement, an inscription, a remote-sensing interpretation — carried with its provenance. An interpretation is a scholarly reading of one or more observations. The intermediate "evidence claim" layer that some models insert between these is rejected as too granular for archaeological practice. Archaeological observations are rarely theory-free: excavation records, survey reports and historical texts already embody acts of interpretation at the point of recording. Attempting to separate every observation into a putatively "raw" observation and a subsequent evidential claim would introduce complexity without corresponding analytical benefit.

6. **Certainty is multidimensional.** A single confidence score conflates independent quantities. The database distinguishes, where each applies, identification certainty (is this really the historical place X?), chronological certainty (how secure are the dates?), spatial certainty (how accurate is the geometry?), functional certainty (was it really a church?) and relationship certainty (does this fort really overlook that pass?). These dimensions are independent and are recorded separately. The ontology must specify which dimensions apply to which entity types rather than forcing all five onto every record.

7. **Landscape entities are spatial equals to sites.** Sites do not have privileged ontological status among spatial things. Sites, landscape features, routes, administrative areas and waterbodies are all spatial entities sharing the same spatial primitives (geometry, phase, uncertainty) and differing in conceptual category. A fortified pass involves both a landscape feature (the pass, which exists regardless of fortification) and a site (the fort controlling it), linked by a relationship, rather than an awkward decision about which single type the thing is.

8. **Controlled vocabulary through attributes, not proliferating subtypes.** Where things differ in kind but not in structure, the difference is captured by a typed attribute on a single entity, not by separate entity types. A route is one entity type with a class attribute distinguishing documented, modelled, inferred and route-family routes. An event is one entity type with a type attribute distinguishing sieges, battles, earthquakes, administrative reforms, reoccupations and abandonments. Component types (fortification, church, tower, gate, road, quarry, bridge, reservoir, kiln, field system, cemetery, workshop) are likewise a controlled vocabulary on a single component type. Vocabularies are extensible through the closed-enum-with-growth mechanism already established in the corpus. New entity types are created only when a thing genuinely behaves differently, not merely when it is nameably distinct.

9. **Relationships are first-class records with their own metadata.** Much of the frontier's structure — and most of its analytical interest — lies in relationships: which forts overlook which passes, which settlements lie within a day's march of which fortresses, which monasteries cluster around which roads, which sites are intervisible. These are not properties of sites but relationships between them, and they carry their own metadata: type, temporal validity, confidence, supporting evidence and notes. Modelling relationships as first-class records is what makes network analysis of the frontier possible.

10. **CIDOC CRM is a crosswalk target, not the internal master.** CIDOC CRM is an excellent interoperability standard and the ontology will map to it. But the internal data model is designed for this project's research questions first and mapped to CIDOC CRM afterwards. The question at each design decision is whether it makes archaeological interpretation easier, not whether it satisfies CIDOC CRM.

11. **Assertions, not claims.** The term for what a source or scholar states on the basis of an observation is *assertion*, which captures the epistemic status honestly: an assertion is what someone maintains on the basis of evidence, without the implication of definitiveness that *claim* can carry.

12. **Edge cases are a design test, not a design driver.** The ontology is designed for typical cases, which are the overwhelming majority of records, and then tested against the edge cases catalogued below. Refinement is made only where a genuine edge case cannot be represented within a small extension of the typical-case design. Designing for edge cases first produces a schema optimised for hard cases and awkward for normal ones.

13. **Theoretical framework is analytical lens, not ontology.** The project's historical-materialist framework governs how the evidence is analysed, not what the database records. The ontology remains framework-neutral so that the same data can be analysed through different interpretive traditions, including by future researchers who do not share this project's theoretical commitments. Historical materialism appears in the analysis, not in the schema.

14. **Time is modelled without privileging the analytical window.** The corpus spans c. 640-1100; the dissertation attends to 750-950. Temporal boundaries are properties of particular analyses, not of the data model. The ontology models phases, dates and events across the full corpus range and lets analysis select temporal windows.

## 6. Edge cases catalogue

The eventual ontology must be tested against the following cases. Each is a real situation the frontier evidence presents, and each stresses a different aspect of the model. The catalogue is a test suite, not a specification: the ontology is designed for the typical case and refined only where one of these cannot be represented.

- **A fort controlling a mountain pass.** The pass is a landscape feature existing independently; the fort is a site whose function is to control it. The two are distinct entities linked by a relationship, not a single ambiguous object.
- **A settlement that moves a short distance.** A site whose occupation shifts several hundred metres with no break in occupation: one persistent site with a spatial change between phases, or a new site in succession? The governing principle is physical continuity, with the specific distance a matter of judgement scaled to the site's size.
- **A monastery that becomes a fortress, or a fortress that becomes a village.** Functional transformation with physical continuity: one site with successive phases of differing function, the physical identity persisting through the functional change.
- **Multiple names for one place.** A single physical site attested under different names in different sources or periods (Byzantine, Arabic, Syriac, modern). One site entity carrying multiple attested names, each with its source.
- **One name referring to different places.** A single toponym that the sources apply to two or more distinct physical locations. Distinct site entities, with the shared name recorded on each and the ambiguity represented rather than resolved by fiat.
- **Seasonal or intermittent occupation.** A site occupied only at certain times, whether seasonally or with gaps between occupations. Phases that need not be continuous, and a model of occupation that does not assume permanence.
- **Two contemporaneous occupation nuclei.** A settlement occupying two or more distinct areas at the same time. A phase whose geometry is a multipolygon rather than a single footprint.
- **Uncertain site location.** A place attested in the sources but not securely located on the ground. A site entity with low spatial certainty and possibly several candidate geometries, the uncertainty recorded rather than a false precision imposed.
- **Multiple possible geometries.** A site for which different sources or methods (a survey polygon, a digitised TIB outline, a remote-sensing interpretation, an excavation plan) propose different extents. Multiple geometries attached to the site or phase, each with its own source, method and confidence.
- **A physical thing whose function is contested but whose existence is not.** A structure that certainly exists but whose interpretation as monastery, palace or caravanserai is disputed. A stable physical entity with competing interpretations attached through observations, the entity itself not made uncertain by the interpretive dispute.
- **Conflicting chronologies for the same material.** The same site or deposit dated differently by different examinations — the Al-Muthaqqab ceramic case, where surveys and re-examinations across two decades disagreed and a single scholar changed position. Multiple dated assertions held together with their provenance, the disagreement represented as a dossier rather than resolved.
- **An attestation that misreads an earlier scholarly statement.** A position in the corpus that derives not from the primary evidence but from a misreading of a modern source — the Ṭaranda case, where a route description in a synthesis was misread as an identification. The correction recorded with its reasoning, so that a future reader sees the misreading, the source passage and why it was corrected, rather than a silent overwrite.

---

## 7. Theoretical framework

The project is analysed through a historical-materialist framework, drawing on the tributary-mode analyses of Haldon and Wickham and the wider apparatus of modes of production, social reproduction and the relationship between economic base and political form. This framework is an analytical lens, not a component of the database. The distinction is deliberate and important. The research questions — how landscapes were produced, organised and transformed — are framework-neutral in their statement; historical materialism is one powerful way of answering them, particularly well suited to a frontier whose character was shaped by tax regimes, property relations and military-agrarian structures. But the database records the evidence and the scholarly interpretations of it without embedding any single theoretical commitment, so that the same data remains analysable through other traditions and by other researchers. The framework belongs in the analysis and the writing, not in the schema.

---

## 8. Comparative dimension

The project is a study of the Byzantine-Islamic frontier of Anatolia, and comparison with other frontier systems — al-Andalus, the Caucasus, the Roman limes, the Sasanian-Roman precursor — is not a primary research question. Forcing comparison into the dissertation would dilute its focus and expand the corpus beyond what the analysis requires. But comparison should be able to emerge from the work if the ontology is general enough: a data model that represents frontier landscapes as produced and transformed through movement, settlement, authority and environment is not intrinsically specific to Anatolia. The comparative dimension is therefore declined for the dissertation and preserved as a possibility for future research, and the ontology should be general enough to support it without redesign.

---

## 9. Success criteria

The conceptual ontology that follows from this document will be regarded as successful if it meets the following testable criteria. Each is phrased so that its satisfaction can be checked, not merely asserted.

- **Query coverage.** Every top-level research question can be expressed as one or more executable database queries or defined analytical workflows over the ontology's structures. A research question that cannot be so expressed indicates a missing capability.
- **Edge-case coverage without special-casing.** Every edge case in the catalogue can be represented without introducing project-specific entity types or one-off exceptions — using only the ontology's general types, their attributes and a small number of principled extensions.
- **CIDOC CRM mapping.** Every entity type and relationship type has a documented mapping to CIDOC CRM, achieved by translation rather than by having bent the internal model toward CIDOC CRM's abstractions.
- **Dual implementation with lossless correspondence.** The ontology is implementable in both PostgreSQL/PostGIS and YAML, and a round-trip between the two representations preserves all data — no field is expressible in one but not the other.
- **Direct analysis.** Spatial, temporal and network analyses run against the stored data without an intervening remodelling step: geometries are queryable as geometries, dates as dates, relationships as a graph, straight from the store.
- **Evidence-interpretation separation with full provenance.** Every assertion in the store resolves to its source and transmission chain, and observations are separable from the interpretations built on them, such that competing interpretations of the same observations can be retrieved independently.
- **Extension without redesign.** A new source, entity type, relationship type or analytical requirement can be accommodated by adding to the ontology, with no change to existing types' identity or structure required to absorb it.

These criteria give the ontology work an objective definition of done. An ontology that satisfies all seven is ready for logical and physical schema development; one that fails any is not yet finished, and the failing criterion names the work remaining.

---

*End of research questions specification. Next stage: conceptual ontology, designed against these questions and tested against the edge cases catalogue.*
