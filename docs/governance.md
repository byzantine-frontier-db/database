# Governance Charter

## Byzantine-Islamic Frontier Database

**Version:** 1.0.0
**Applies to:** schema v1.0.0, specification v2

---

## 1. Mission and Scope

The Byzantine-Islamic Frontier Database is a long-running collaborative scholarly project. Its records will outlive any individual contributor; its decisions will be revisited by successors. This charter exists so that those decisions are made consistently, transparently, and reversibly, and so that contributions from many hands produce a coherent dataset rather than a sedimented mass of editorial preferences.

The charter is binding on all contributors and on all records bearing the project's identifiers. It is itself versioned and is itself revisable, under the procedure defined in §11.

---

## 2. Production methodology

The initial v1.0.0 pilot corpus of 85 records on the 838 Abbasid campaign against Amorium was produced through an AI-assisted extraction workflow against the primary sources catalogued in `records/sources/`. The workflow, schema, ontology alignment, vocabularies, and theoretical framework are the work of the maintainer. AI assistance was used for the bulk extraction phase against pre-selected sources, applied to a schema and editorial framework defined in advance, and constrained by the hard rules set out in `editorial_workflow.md`. All records produced through AI-assisted extraction carry `editorial_review_required: true` until verified by the maintainer against the printed source; records in this state are explicitly marked in the data and may not progress to `workflow_state: published` without verification. Future contributors, human or otherwise, are bound by the same workflow.

---

## 3. Editorial Structure

### 3.1 Roles

**Editor-in-Chief.** Holds final responsibility for the integrity of the published database. Convenes the Editorial Board. Casts the deciding vote in tied Board decisions. Serves a renewable three-year term.

**Editorial Board.** Three to seven Senior Editors covering the principal source traditions and regions: Greek-language Byzantine sources, Arabic-language sources, Syriac and Christian-Arabic sources, archaeology, and historical geography. The Board makes all decisions requiring editorial judgement (entity merges, vocabulary extensions, disputed identifications elevated for review).

**Senior Editors.** Members of the Editorial Board with topical or regional responsibility. Each Senior Editor is the first point of review for records within their remit.

**Contributors.** Anyone — internal or external — submitting records to the database. Contributors are credited per §7.

**Reviewers.** Senior Editors or appointed deputies who carry out structured review of submitted records.

**Technical Lead.** Responsible for the schema, vocabularies, identifier minting infrastructure, and the database's technical operation. Reports to the Editor-in-Chief on operational matters; consults the Editorial Board on substantive schema changes.

### 3.2 Appointment

The Editor-in-Chief is selected by consensus of the Editorial Board, with confirmation by the project's institutional host (if any). Senior Editors are appointed by the Editor-in-Chief in consultation with the existing Board. Appointments are documented in the project's change log.

### 3.3 Conflict of Interest

A reviewer who is also a contributor of the record under review recuses themselves from that review. A Senior Editor with a substantial published scholarly position on a disputed identification refers decisions on that identification to a Board colleague.

---

## 4. Record Lifecycle

Every record passes through documented workflow states. The state is recorded in the record's `metadata.workflow_state` field.

### 4.1 States

- **draft** — Created but not submitted for review. May be modified freely by its creator.
- **under_review** — Submitted for editorial review. Modifications are tracked; reviewer feedback is appended to `metadata.review_history`.
- **published** — Accepted into the public database. Becomes part of the official record set and receives a stable URI.
- **deprecated** — Superseded by a successor record (typically through merge or split). The record remains accessible via its URI but is flagged in queries.
- **withdrawn** — Removed from the active dataset for documented cause (factual error, copyright issue, withdrawal of contributor consent). The URI continues to resolve to a tombstone notice; no successor is implied.

### 4.2 Transitions

- `draft → under_review`: by contributor submission.
- `under_review → published`: by reviewer acceptance.
- `under_review → draft`: by reviewer request for revision.
- `published → deprecated`: by Editorial Board decision following merge, split, or factual supersession.
- `published → withdrawn`: by Editorial Board decision; documented rationale required.
- `deprecated → published`: only by reversal of the originating Board decision, with documented rationale.

State transitions are immutable in their record: a transition log is appended, never overwritten.

### 4.3 Versioning of Records

Each record carries a SemVer version in `metadata.record_version`. The convention:

- **PATCH** (1.0.x): typographical fixes, formatting adjustments, addition of a citation that does not change the analytical content.
- **MINOR** (1.x.0): addition of attestations, refinement of confidence values, addition of alternative names, expansion of analytical summary.
- **MAJOR** (x.0.0): change of identification, change of coordinates outside the original uncertainty radius, change of overall confidence by more than one level, restructuring of the record's relationship to other records.

Every modification creates a new version; the prior version is preserved and accessible by version-qualified URI (e.g. `/place/ENT-PLC-0001@1.2.0`).

---

## 5. Decision Procedures

### 5.1 New Entity Creation

A contributor proposing a new entity must, per specification §4.2:

1. Search existing entities by standardised name, alternative names, transliterations, geographic proximity, chronological window, and associated entities.
2. Document the search and its outcome in the proposed record's `notes` field.
3. If no plausible existing entity is found, create a new entity with a provisional `PROV-` prefixed identifier.
4. Submit for review.

The reviewer's role is to confirm or challenge the absence of an existing match. If a match is identified, the proposed entity's content becomes a new attestation against the existing entity. If no match exists, the provisional identifier is replaced with a canonical identifier upon publication.

### 5.2 Merge

When two entities are determined to refer to the same historical object:

1. A merge proposal is filed, identifying both entities and providing reasoning.
2. The proposal is reviewed by at least two Senior Editors.
3. If approved, the merged record is created, attestations are reassigned, both predecessor URIs become redirect tombstones pointing to the merged URI, and both predecessor records transition to `deprecated`.
4. The merge is logged with full audit trail.
5. Merges are reversible by Editorial Board decision.

### 5.3 Split

When a single entity is determined to conflate two distinct historical objects:

1. A split proposal is filed, identifying the entity and explaining the conflation.
2. The proposal is reviewed by at least two Senior Editors.
3. If approved, two new entity records are created with new identifiers, each attestation is reassigned to whichever successor it actually concerns (a third "ambiguous" pool may be maintained for attestations that cannot be assigned with confidence), and the predecessor's URI becomes a disambiguation tombstone listing both successor URIs.
4. The split is logged with full audit trail and is reversible.

### 5.4 Disputed Identification

Per specification §4.3, scholarly disagreement about whether two designations refer to the same entity is recorded *within* a single entity by setting `identification_status` to `disputed` and creating an Interpretation record articulating the dispute. Splitting a record solely to express disagreement is prohibited. Only when the dispute is resolved in favour of separation does §4.3 apply.

### 5.5 Vocabulary Extension

Adding a term to a controlled vocabulary (event sub-categories, place types, relationship types, etc.) requires:

1. A proposal from any contributor, with rationale and at least three concrete cases the new term would describe.
2. Review by the Editorial Board.
3. Board majority approval.
4. Update to the vocabulary file with the new term, a SKOS definition, and any external alignment (AAT, Pleiades types, etc.).
5. Increment of the vocabulary's MINOR version.

Renaming or removing a vocabulary term requires MAJOR version increment of the vocabulary and a documented migration path for affected records.

### 5.6 Schema Change

Changes to the JSON Schema are categorised:

- **PATCH** schema changes (clarifications, additions of optional fields, error-message improvements): Technical Lead may apply with notification to the Editorial Board.
- **MINOR** schema changes (additions of new record types, new non-required fields, broadened enums): require Editorial Board approval.
- **MAJOR** schema changes (changes to required fields, narrowed enums, structural reorganisation): require Editorial Board approval, a migration path for existing records, and a transition period during which both schema versions are accepted.

The schema is itself a published artefact; every change is announced in the change log.

**Transition window and lazy migration.** During a transition period the validators accept multiple schema versions at once: `tools/byzfrontier_validate.py` is given each active schema (e.g. `--schema` for both v1 and v2) and dispatches every record to the schema whose `RecordMetadata.schema_version` const matches that record's declared `metadata.schema_version`. Records under different schema versions therefore coexist and all validate.

Schema-version migration is **lazy, not a mass rewrite**. A record's `metadata.schema_version` is updated to whichever schema is current only when the record next receives a MINOR or MAJOR version bump for some other reason. Over time the corpus migrates onto the current schema without a dedicated rewrite pass; records not otherwise touched remain valid under their original schema for the duration of the transition window.

**Split-ship of required-field changes.** Promoting a field to `required` is a MAJOR change that would otherwise break every record producer simultaneously. Such changes ship in two stages: first the field is added as an optional property definition (PATCH/MINOR); then, once lazy migration has carried the corpus onto the new schema version, the field is promoted to `required` (MAJOR). Consumers adopt the field during the interval between the two stages.

### 5.7 Decision-Making Procedure

The default Board procedure is:

1. Proposal circulated in writing.
2. Discussion period of at least two weeks.
3. Decision by simple majority of voting Senior Editors.
4. Tied votes: Editor-in-Chief casts deciding vote.
5. Decision and rationale logged in the change log.

Time-sensitive decisions (vandalism response, urgent error correction) may be handled by the Editor-in-Chief unilaterally, with the decision presented for ratification at the next Board meeting.

### 5.8 Amendment of Frozen Documents

*Adopted 2026-07-23. This section confers frozen status; it is therefore adopted before, and as a precondition of, any document claiming that status.*

Certain documents are declared **frozen**: they are stable inputs that later work is designed against, and their value depends on their not moving silently underneath that work.

**Scope of the freeze.** Frozen at adoption of this section, and no others:

- `docs/research_questions.md` — the design contract
- `docs/methodology/conceptual_ontology.md` — the conceptual specification

Further documents may be declared frozen by the Board. **`docs/editorial_workflow.md` and this charter are not frozen.** They are live operational documents and remain amendable under their own procedures — this charter under §11. (`editorial_workflow.md` has no stated amendment procedure; that gap is noted here, not resolved.) The commit adopting this section itself gives substantive new content to both, which is the intended distinction: the frozen documents are what the project designs *against*, the live documents are how it works.

**Standing convention.** Any commit touching a frozen document declares **in its first line** which of two things it is:

- **Status transition** — a change to lifecycle metadata only: a freeze, an unfreeze, a supersession notice, a pointer to a successor document. A status transition makes no change to the document's substance. *A commit declaring itself a status transition that also alters substance is malformed and is to be rejected at review.*
- **Content amendment** — any change to the document's substance. Content amendments to frozen conceptual documents require Board approval and must identify the demonstrated defect that justifies reopening under this governance framework. A demonstrated defect that does not result in amendment is recorded as an accepted limitation, with the reasoning for accepting it. "Clarification", "tidy-up", "minor edit" and "consistency" are not defects and do not justify reopening a frozen document.

**Rationale.** A frozen document edited without explanation forces every later reader to reconstruct whether the design they built on still holds; requiring the declaration up front makes that answer readable from `git log` alone, without diffing, and without depending on the memory of whoever made the change.

The load-bearing gate is the **demonstrated defect**, not the approval. A unanimously approved elegant refinement is not a reason to reopen a frozen document; a demonstrated inability to express a registered query is, whatever anyone's preference. Approval without a defect is not sufficient, and a defect that the Board declines to fix does not simply lapse — it is recorded as an accepted limitation with its reasoning, on the model of the limitations already carried in the conceptual specification. The record must show what was found, not only what was changed.

### 5.9 Pre-migration validation

*Adopted 2026-07-23.*

**A corpus migration is not executed until the logical model has been validated against the query register.** Validation is performed on a **synthetic fixture corpus**, not on the live corpus, and precedes any transformation of records.

**The fixture.** The fixture instantiates the **edge-case catalogue** of the frozen conceptual specification — every catalogued case, and the limitations recorded alongside them — not merely one instance of each entity type. A fixture holding one of each type is a smoke test: it establishes that the model can store the ontology's vocabulary, which is not what is in question. What is in question is whether the model can express the cases the ontology was designed around, and only a fixture built from the catalogue tests that.

**Which register entries execute.** Validation runs **every** register entry. Acceptance criteria concern structural expressibility — which, per register §3.6, is true of every entry — so there is no exempt category:

- **Category 1** entries execute against the live corpus as well as the fixture.
- **Category 3 and 4** entries execute against the fixture. Their dependencies block *analysis*, not acceptance testing: a fixture supplies the instances the corpus lacks, and the question the register asks of the model is whether it can express the query, not whether the corpus can answer it.
- **Category 2** entries execute **with provisional vocabulary**. A term filed under §5.5 and awaiting decision is admitted to the fixture as provisional, because the acceptance criterion is structural expressibility and a pending Board decision on a term's name or scope does not bear on whether the model can hold a relationship of that shape. Provisional terms are marked as such in the fixture and carry no force outside it.

**Failure routes.** A failed entry routes to the **query register's §7 discrepancy procedure**, and not to §5.8. A logical-model defect is not a frozen-document event: the model is not a frozen document, and reopening the conceptual specification is warranted only where §7 classifies the failure as **(iv)**, an ontology defect. Classifications (i), (ii) and (iii) are resolved within the register and the model. Only a classification (iv) finding engages §5.8, and it does so through §5.8's own demonstrated-defect gate rather than automatically.

**Completion.** Migration may proceed when every executed entry passes or is recorded as a partial attributable to a stated limitation, and every failure has been classified under §7. An unclassified failure blocks migration.

---

## 6. Identifier Minting

The Technical Lead is the sole minting authority for canonical identifiers and URIs (see Ontology Alignment §6). Identifiers are sequential within type and are never reassigned.

Contributors propose entities using provisional identifiers prefixed `PROV-`. Upon publication, the provisional identifier is replaced with a canonical one. The provisional identifier is recorded in the published record's `notes` for traceability but does not itself become a URL.

---

## 7. Contribution and Attribution

### 7.1 External Contribution

Contributions are welcomed from any scholar. The submission workflow:

1. Submitter provides one or more records as YAML or JSON conforming to the schema.
2. Submission is reviewed by the appropriate Senior Editor.
3. Reviewer may accept, request revisions, or decline (with reasons).
4. Accepted records carry the contributor's name in `metadata.created_by`.

### 7.2 Attribution

Every record's `metadata` block carries `created_by` and `modified_by` fields with the contributor's full name and (where available) ORCID iD or other identifier. The project commits to maintaining this attribution permanently; aggregated contributor statistics are published with each release.

### 7.3 Authorship and the Public Database

Inclusion of a record in the published database does not transfer authorship of the underlying scholarship. Contributors retain the right to cite their database contributions in their own publications. The project undertakes to provide stable, citable URIs and recommended citation formats for every published record.

### 7.4 Disagreements with Editorial Decisions

A contributor whose submission is declined, or whose published record is later deprecated or merged, may file a formal disagreement. The disagreement is logged in the record's notes and is publicly accessible. If the contributor wishes to withdraw their attribution from the affected record, that wish is honoured; the record itself, however, remains in the database where editorial judgement supports it.

---

## 8. Licensing

### 8.1 Data Licence

The structured database contents (records, vocabularies, schema) are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Attribution is fulfilled by citing the project and the canonical URI of the relevant record.

### 8.2 Schema and Vocabulary Licence

Schemas and SKOS vocabularies are released under **Creative Commons Zero (CC0)** to maximise interoperability. Reuse without attribution is permitted, although attribution is appreciated.

### 8.3 Source Quotation Licensing

Direct quotations from primary sources in public-domain editions are unrestricted. Direct quotations from modern critical editions and modern translations are used under fair-use or fair-dealing provisions; the project records the edition cited and the quotation length, and limits quotations to what is necessary for evidential purposes. Where a modern translation is quoted, the translator is credited in the attestation record.

Contributors are responsible for ensuring that quotations they submit comply with applicable copyright law. The Editorial Board may shorten or paraphrase quotations whose length exceeds fair-use norms.

### 8.4 Software Licence

The code that operates the database (if released) is licensed under the **Apache License 2.0**.

---

## 9. Interoperability Commitments

The project commits to:

1. **Open formats.** All data is available in JSON, JSON-LD, Turtle, and CSV. Place data is additionally available in Linked Places Format (GeoJSON-based).
2. **Persistent URIs.** Per Ontology Alignment §6, URIs are stable and resolve indefinitely.
3. **Bulk export.** A full database dump is published with every release.
4. **API access.** A read-only HTTP API exposing records by URI and supporting basic query.
5. **SPARQL endpoint** (target: v1.1) exposing the database as Linked Open Data.
6. **External alignment.** Pleiades, VIAF, Wikidata, PBW, PMBZ, and other external authorities are referenced wherever applicable.
7. **Versioning.** Schema, vocabularies, and the database itself are versioned; previous versions remain accessible.
8. **Change log.** Every release is accompanied by a human-readable change log.

These commitments are part of the project's contract with its users.

---

## 10. Dispute Resolution

Disputes between contributors, or between a contributor and the editorial team, are escalated as follows:

1. **Initial review.** Senior Editor responsible for the disputed record attempts to resolve.
2. **Editorial Board review.** If unresolved, the dispute is referred to the full Board.
3. **External arbitration** (rare). For disputes the Board cannot resolve, the project commits to seeking an independent external scholarly opinion before any irreversible decision.

Throughout, the project's priority is preservation of the historical record rather than vindication of any particular position. Scholarly disagreement is recorded as scholarly disagreement, not suppressed.

---

## 11. Amendment of this Charter

This charter is itself versioned. Amendments require:

1. A written proposal from any Senior Editor.
2. Public posting for community comment for at least four weeks.
3. Approval by two-thirds majority of the Editorial Board.
4. MINOR version increment for clarifications and procedural refinements; MAJOR version increment for structural changes (role redefinitions, decision-procedure changes, licensing changes).

All previous versions of the charter remain accessible. Records produced under earlier charter versions remain valid under those versions.

---

## 12. Change Log

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0.0 | (initial) | Charter adopted. | Founding Editorial Board |
| 1.1.0 | 2026-07-23 | §5.8 Amendment of Frozen Documents adopted; `research_questions.md` and `methodology/conceptual_ontology.md` declared frozen. | Editorial Board |
| 1.2.0 | 2026-07-23 | §5.9 Pre-migration validation adopted. | Editorial Board |
| 1.2.1 | 2026-07-23 | §5.9 wording clarified: validation runs every register entry, removing an implied exemption category that register §3.6 rules out. No change of effect. | Editorial Board |

---

## Appendix A — Quick Reference: Who Decides What

| Decision | Decider | Procedure |
|---|---|---|
| Accept a new record | Senior Editor (region/topic) | §4.2 |
| Merge entities | Two Senior Editors | §5.2 |
| Split an entity | Two Senior Editors | §5.3 |
| Extend a controlled vocabulary | Editorial Board majority | §5.5 |
| Schema PATCH change | Technical Lead | §5.6 |
| Schema MINOR change | Editorial Board majority | §5.6 |
| Schema MAJOR change | Editorial Board majority + migration plan | §5.6 |
| Mint canonical identifier | Technical Lead | §6 |
| Withdraw a published record | Editorial Board majority | §4.2 |
| Resolve dispute | Senior Editor → Board → external | §10 |
| Amend this charter | Two-thirds Editorial Board | §11 |
