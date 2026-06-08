# Editorial Workflow

This document describes the workflow for adding, validating, and reviewing records in the Byzantine-Islamic Frontier Database. The same procedural rules apply to any contributor — human, AI-assisted, or a mixture.

## Scope

The workflow covers record extraction from primary and secondary sources, validation against schema and cross-reference rules, and editorial review prior to release.

## Hard rules

These rules are non-negotiable. Records produced in violation of any of them are rejected at validation.

1. **No fabricated citations.** Every `citation` field must point to a real, verifiable location in a real source. If the exact page or folio is uncertain, the citation reads `[citation needed: exact page]` and `editorial_review_required: true`. Speculative or approximate citations dressed as exact are prohibited.

2. **No fabricated external identifiers.** Pleiades, PMBZ, VIAF, TGN, AAT, Wikidata, and similar identifiers are inserted only when the contributor has verified the identifier resolves to the correct entity. Plausible-looking IDs invented to fill a field are prohibited.

3. **Distinct evidential levels.** Observation, Attestation, and Source records remain distinct. An observation (e.g. a coin find, an inscription, a stratigraphic context) is not collapsed into an attestation; an attestation (a textual mention) is not collapsed into the source that contains it; a source (the textual artefact) is not collapsed into the author or work it transmits.

4. **Provenance honesty.** Where a primary source is reached via a secondary work, the attestation records the primary source with provenance `primary_paraphrase` or `primary_quotation`, and the `notes` field records the secondary route. Where a secondary work is the subject of its own assessment, that becomes an Interpretation record against the secondary work itself.

5. **Editorial review flag.** Any record where the contributor has not directly verified the cited source against the printed page carries `editorial_review_required: true`. Records may be published in this state; they may not move to `workflow_state: published` without verification.

6. **Validate before commit.** Every contribution runs `tools/byzfrontier_validate.py` and `tools/byzfrontier_xref.py` against the affected records before being committed. Records that do not pass validation are not committed.

7. **Honest framing in summaries.** Where a record set is described in writing — a release note, a publication, a presentation — the framing reflects what was actually done, including the role of any AI-assisted extraction and the proportion of records currently in `editorial_review_required: true` state.

## Extraction procedure

For a new record set drawn from a source:

1. The contributor identifies the source (edition, translation, page range) and confirms it is represented by a `SourceRecord` in `records/sources/`. If not, the SourceRecord is created first.

2. The contributor extracts attestations against the source. Each attestation includes the `direct_quotation` field where the quotation is short and unambiguous, or a `paraphrase` field where the content is summarised. Direct quotations are verified against the printed source before commit; paraphrases mark `editorial_review_required: true` until verified.

3. For each attestation, the contributor either links to an existing entity (place, person, event) in the corpus or proposes a new EntityRecord with full provenance.

4. Interpretations — claims about what the evidence means — are recorded separately as InterpretationRecord, linked to the attestations and entities they draw on, and attributed to the scholar making the interpretation.

5. The contributor runs the validators locally. Where they pass with zero errors, the records are committed with a descriptive message indicating the source and the count of records added.

## Secondary-source-mediated extraction

When a primary source is read via a secondary work (e.g. a passage of al-Ṭabarī reached via Treadgold 1988):

1. The attestation is created against the primary `SourceRecord` (al-Ṭabarī), not against the secondary work (Treadgold).
2. The `citation` field records the full transmission chain: the primary edition consulted, the translation if any, and the secondary work as the route through which the contributor reached the passage.
3. The `provenance` field is `primary_paraphrase` or `primary_quotation`, never the name of the secondary author.
4. If the secondary work itself makes an interpretive claim worth preserving (as opposed to merely transmitting primary content), that claim becomes an InterpretationRecord against the secondary work.

This pattern preserves the evidential structure: primary content attests primary facts; secondary interpretation is its own object of study.

## Identity resolution

When a person, place, or event is mentioned in multiple sources under different names (al-Afshīn / Aphsiné, Amorium / Ἀμόριον / ʿAmmūriya, the 838 sack / the Anatolian campaign of AH 223), the contributor checks whether an existing record already covers the entity before proposing a new one. The Master Record rule (specification §4.1) requires that a single EntityRecord aggregates all attestations to a single underlying entity; alternative names are recorded in `alternative_names` and provenance fields, not in parallel records.

## Validation

Two validators run on every record set:

- `tools/byzfrontier_validate.py` checks each YAML file against `schema/byzfrontier_schema_v1.json`. It flags missing required fields, malformed types, and constraint violations.

- `tools/byzfrontier_xref.py` checks that every internal ID referenced in a record (in `attested_in`, `interprets`, `related_to`, etc.) resolves to an actual record in the corpus.

Both run automatically on every push and pull request via GitHub Actions (`.github/workflows/validate_records.yml`). A record set that fails either validator is not merged.

## Editorial review

Records with `editorial_review_required: true` are flagged for human verification against the original cited source. Verification involves:

1. Locating the cited page or folio in the printed source.
2. Confirming the quoted or paraphrased text accurately represents the source.
3. Confirming the citation is accurate (correct edition, volume, page).
4. Removing the `editorial_review_required` flag and committing.

Records in this state may be released as `workflow_state: draft`. They do not progress to `workflow_state: published` until verified.
