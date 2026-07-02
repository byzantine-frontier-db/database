# Byzantine-Islamic Frontier Database

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20584723.svg)](https://doi.org/10.5281/zenodo.20584723)
&nbsp;License: data [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · code [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) · vocabularies [CC0](https://creativecommons.org/publicdomain/zero/1.0/)

A provenance-aware historical knowledge graph of the Islamic-Byzantine frontier and its
connected regions, roughly the seventh to eleventh centuries. Records are structured so
that **what was observed, what a source attests, and what the source itself is** stay
distinct — the evidential chain is preserved rather than flattened into assertions. The
data is published as human-readable YAML, validates against a formal JSON Schema, and is
aligned to CIDOC-CRM and external authorities (Pleiades, VIAF, PMBZ, Wikidata) for
cross-project linking.

If you have arrived here from a citation and want to know in five minutes what this is,
how to read it, and whether you can rely on it — this page is for you. The short answer
on reliability: **read the [scope and verification status](#scope-and-verification-status)
section before you cite any individual record.**

---

## Scope and verification status

Two things a user must know before consuming this data:

**1. The current corpus is a structured reading of a single book.** All 1,227 records
were extracted from one secondary work — A. Asa Eger, *The Islamic-Byzantine Frontier:
Interaction and Exchange among Muslim and Christian Communities* (London: I.B. Tauris,
2015), held in the corpus as `SRC-0007`. The project began as an 85-record pilot on the
838 Abbasid campaign against Amorium and was extended across eighteen sessions to cover
the whole monograph. The 64 source records catalogue the primary texts Eger cites
(al-Ṭabarī, Theophanes, al-Balādhurī, and so on), and primary-source content is attested
against those primary `SourceRecord`s with the transmission chain noted — but **no primary
edition has yet been consulted directly.** Everything in the corpus is currently mediated
through Eger. No other monograph is represented yet.

**2. Nothing has been independently verified against a printed page.** Every record
carries `editorial_review_required: true` and `workflow_state: draft`. Under the project's
[editorial workflow](docs/editorial_workflow.md), that flag means a human has *not* yet
checked the cited passage against the printed source; such records may circulate as drafts
but may not be promoted to `published`. Treat the corpus as a rigorously-structured,
fully-traceable **first pass** — excellent for navigation, cross-referencing, and finding
where Eger treats a place, person, or event — not as independently validated scholarship.
Each record tells you exactly where to check it.

### Corpus contents

| Record type    | Count | What it holds |
|----------------|------:|---------------|
| Sources        |    64 | Primary and secondary texts (the bibliographic layer) |
| Places         |   186 | Settlements, forts, rivers, regions — includes the 4 polity/administrative-unit entities (Byzantine, Abbasid, Umayyad, Hamdanid) |
| Persons        |    81 | Caliphs, emperors, generals, scholars, saints |
| Events         |    54 | Campaigns, sieges, foundations, resettlements, construction works |
| Observations   |   235 | Discrete propositional claims |
| Attestations   |   300 | A source's testimony about entities/observations (the evidential link) |
| Interpretations|   163 | Scholarly arguments about what the evidence means, attributed to a named scholar |
| Relationships  |   144 | Typed links between entities (located_at, besieged, allied_with, …) |
| **Total**      | **1,227** | |

---

## How to read the data

**The evidential model.** The corpus deliberately separates three things most datasets
collapse:

- An **observation** is a single claim ("cotton was grown in the Jazīra in 842").
- An **attestation** is a particular source saying so, with a `provenance` category
  (`primary_paraphrase`, `archaeological_evidence`, `modern_synthesis`, …), a `citation`
  string carrying the full transmission chain, and a `confidence` rating.
- A **source** is the text itself (edition, language, genre, known biases), never conflated
  with the author or the work it transmits.

Interpretations — a scholar's argument about meaning — are a fourth, separate object, so
that Eger's claims about *what the frontier was* are never silently mixed into the factual
record. This separation is the project's reason for existing; the trade-offs it imposes are
discussed candidly in the [extraction reflection](docs/extraction_reflection_eger2015.md).

**Entities** (places, persons, events) each carry an `analytical_summary`, a back-reference
list of the `linked_attestations` and `linked_interpretations` that support them, and an
`overall_confidence`. Confidence is a 1–5 scale throughout (5 = certain, 1 = speculative);
places additionally carry an `identification_status` (`identified` … `disputed`) and
`identification_confidence`. Scholarly disagreements are preserved in place, not resolved
away — a disputed identification is marked `disputed` and explained in an interpretation.

**Identifiers.** Records use stable internal IDs (`ENT-PLC-`, `ENT-PERS-`, `ENT-EVT-`,
`SRC-`, `ATT-`, `OBS-`, `INT-`, `REL-`). Provisional IDs are prefixed `PROV-` until minted;
the current corpus contains none.

**Repository layout.**

```
records/        the 1,227 YAML records, one per file, foldered by type
schema/         byzfrontier_schema_v1.json — the formal correctness criterion
tools/          validators (schema + cross-reference), dating, snapshot utilities
vocabularies/   SKOS controlled vocabularies with AAT alignment
data/           dating-system reference data and methods
docs/           specification, governance, workflow, ontology alignment, release notes
v2_preview/     work-in-progress schema v2 (see Roadmap)
EGER_EXTRACTION_PLAN.md   the session-by-session extraction record
```

Validate any change with the two tools before trusting it:

```bash
python tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json records/
python tools/byzfrontier_xref.py records/
```

Both run in CI on every push; see the [validation harness notes](docs/validation_harness_README.md).

---

## How the data was produced

This is a methodological disclosure, not a disclaimer. The schema, ontology alignment,
controlled vocabularies, editorial framework, and theoretical approach are the maintainer's
work. The bulk extraction of records from pre-selected source material was carried out
through an **AI-assisted workflow**, applied to that framework and constrained by a set of
non-negotiable hard rules — no fabricated citations, no fabricated external identifiers,
strict separation of evidential levels, provenance honesty. The full statement is
[governance §2, "Production methodology"](docs/governance.md#2-production-methodology), and
the hard rules are in the [editorial workflow](docs/editorial_workflow.md). The
`editorial_review_required: true` state on every record is the direct, visible consequence
of this methodology: AI-assisted extraction is treated as a draft awaiting human
verification, and the data says so on its face.

---

## Documentation

This README is an orientation, not a manual. The authoritative documents are in [`docs/`](docs/):

- **[Specification](docs/specification.md)** — the formal data model and every record type in full.
- **[Governance Charter](docs/governance.md)** — roles, record lifecycle, decision procedures, licensing.
- **[Editorial Workflow](docs/editorial_workflow.md)** — extraction, validation, and review rules (the hard rules live here).
- **[Ontology Alignment](docs/ontology_alignment.md)** — CIDOC-CRM mapping and external-authority strategy.
- **[Extraction Reflection (Eger 2015)](docs/extraction_reflection_eger2015.md)** — an honest account of where the framework held and where it strained.
- Browsable documentation site: <https://byzantine-frontier-db.github.io/database/>

---

## How to cite

Please cite the dataset, not this repository page. The project is archived on Zenodo.

- **Concept DOI** (always resolves to the latest archived version): [`10.5281/zenodo.20584723`](https://doi.org/10.5281/zenodo.20584723)
- **Version DOI** for the archived v1.0.0 snapshot specifically: [`10.5281/zenodo.20584807`](https://doi.org/10.5281/zenodo.20584807)

For the live dataset as it currently stands (the complete Eger 2015 extraction described
above), cite the **concept DOI**. The contents of the repository's `main` branch are ahead
of the v1.0.0 archive; a versioned Zenodo deposit covering the completed Eger corpus is
forthcoming, and its version DOI should be preferred once released. Machine-readable
metadata is in [`CITATION.cff`](CITATION.cff).

> Lisle, Curtis. *Byzantine-Islamic Frontier Database.* Zenodo. https://doi.org/10.5281/zenodo.20584723

When citing an individual record, cite the database and the record's stable ID (e.g.
`ENT-PLC-0001`), and — because records are currently unverified drafts — consult the
underlying source named in the record's `citation` field before relying on it.

---

## License

- **Data** (records, vocabularies content): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — attribution via the citation above and the record's canonical ID.
- **Schema and SKOS vocabularies**: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
- **Code** (validators and tooling): [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

Direct quotations from modern critical editions and translations are used for evidential
purposes under fair-use / fair-dealing provisions, with the edition and translator
recorded; see [governance §8](docs/governance.md#8-licensing).

---

## Roadmap

**Phase 2 — Eger 2008.** The next extraction target is the site gazetteer from A. Asa
Eger's doctoral dissertation, *The Spaces Between the Teeth: Environment, Settlement, and
Interaction on the Islamic-Byzantine Frontier* (University of Chicago, 2008) — later
published as *The Spaces Between the Teeth: A Gazetteer of Towns on the Islamic-Byzantine
Frontier* (Istanbul: Ege Yayınları). Its town-by-town appendix is a natural structured
counterpart to the 2015 monograph and will deepen the place corpus considerably.

**Schema v2.** A preview schema in [`v2_preview/`](v2_preview/) addresses the limitations
surfaced by the Eger extraction — chiefly a first-class record type for tribal, dynastic,
and religious **groups**, and better encoding of inter-interpretation scholarly disputes.
The reasoning is set out in the [extraction reflection](docs/extraction_reflection_eger2015.md).

**Verification.** The standing priority across all of the above is moving records out of
`editorial_review_required: true` by checking them against the printed sources — the step
that turns this from a structured reading into verified scholarship.
