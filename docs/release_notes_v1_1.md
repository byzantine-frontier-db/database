# Release Notes — v1.1.0

## Byzantine-Islamic Frontier Database

**Release date:** 2026-06-01
**Previous version:** v1.0.0

This release moves the project from documentation-complete to operation-ready. All seven action items from the v1.0 "next steps" list are delivered.

---

## What's new in v1.1

### Items 1-3: Validators, vocabularies, and dating

- **Cross-reference validator (`byzfrontier_xref.py`).** Second-pass validator that catches dangling references, orphan attestations, duplicate IDs, cycles in parent_event chains, type mismatches in cross-references, and parent/child consistency. Found 13 real defects in Appendix C of v1.0 that schema validation alone missed.
- **AAT-aligned vocabularies (`byzfrontier_vocabularies_v1_1.ttl`).** SKOS vocabulary file with verified AAT `closeMatch` links for two concepts (`military` → `aat:300055314` "wars"; `pt-fortification` → `aat:300164060` "military installations"). Approximately 25 additional concepts carry `bzfdb:aat_search_term` hints and `bzfdb:aat_match_status: pending` for editorial follow-up. Project policy is to not fabricate AAT IDs; the framework supports incremental verified additions.
- **Dating conversion library (`byzfrontier_dating.py`).** Full reference implementation of AH ↔ Julian, AM Byzantine ↔ Julian, indiction-for-Julian, and regnal-year-to-Julian conversions. CLI for contributor use (e.g. `byzfrontier_dating.py ah-to-julian 223`). Eight unit tests pass; all four worked examples from the v1 methods note match exactly. **One real bug caught and fixed during development:** the original indiction formula was using `+` instead of `-` against the AD 312 anchor, producing wrong results. The unit tests now guard against regression.

### Item 4: Pilot corpus

- **85-record pilot corpus (`pilot_corpus_838_v1.yaml`).** End-to-end records covering the 838 Abbasid campaign: 6 sources, 14 persons, 14 places, 8 events, 12 observations, 13 attestations, 6 interpretations, 12 relationships. All records validate against the schema. All records pass cross-reference validation. ~25 records flagged `editorial_review_required: true` where I worked from general scholarly knowledge rather than direct source consultation. The flagged records are explicit candidates for verification before promotion to `published`.

### Item 5: Hosting

- **Institutional prospectus + self-hosting fallback (`institutional_prospectus.md`).** Outreach package for target institutions (KCL, BBAW, ISAW, et al.), including a draft outreach letter. Plus a complete self-hosting plan using GitHub + w3id.org + Zenodo + GitHub Pages + Software Heritage. The self-hosting stack costs zero and provides everything the governance charter's interoperability commitments require. Migration to an institutional host is one operation: update the w3id.org `.htaccess` file.

### Items 6-7: v2 schema preview

- **`byzfrontier_schema_v2_preview.json`** introduces two new types:
  - `FuzzyRegion`: a polygon-per-time-slice place subtype for themes, *ajnād*, *kūras*, and frontier zones, with explicit boundary confidence and uncertainty buffer in kilometres.
  - `WitnessRecord`: a manuscript-witness type aligned to LRMoo (F5 Item / F3 Manifestation) for source-critical work.
- **`v2_preview_examples.yaml`**: one fully worked FuzzyRegion (the Anatolikon theme with three temporal polygons) and three WitnessRecords (two for Theophanes Continuatus, one for al-Ṭabarī). Demonstrates that the v2 model handles the cases v1 collapsed.
- v2 records can coexist with v1 in the same repository. Formal v2.0.0 release will integrate them into the unified schema; the preview is for early review and feedback.

### Deployment

- **`DEPLOYMENT_GUIDE.md`.** Step-by-step setup for the Claude project, the local repository, GitHub + CI integration, and day-to-day editorial workflow. Includes a 4-week first-month checklist.

### Schema fixes

Two real bugs in v1.0 caught during validation work:

1. `TemporalValue` start/end pattern was too restrictive — rejected three-digit Byzantine years like `838-08-01`. Pattern loosened to accept partial dates and 1-4 digit years.
2. `RelationshipRecord.linked_attestations` had `minItems: 1`, blocking structural relationships (`parent_event_of`, `contains`) that inherit evidence rather than carrying it directly. Now optional.
3. `PersistentIdentifier` was referenced but never defined in `$defs`. Now defined.

These fixes are in `byzfrontier_schema_v1.json` and are non-breaking (no v1.0 record that previously validated will now fail).

---

## Verification status

All artefacts in this release have been tested and verified:

| Artefact | Verification | Result |
|---|---|---|
| Schema (v1.0.0 with fixes) | Validates as JSON; 35 $defs; 8 record types | ✓ |
| Schema validator | Catches all 11 introduced defects in test fixtures | ✓ |
| Xref validator | Catches all 13 dangling-reference defects in v1.0 Appendix C | ✓ |
| Pilot corpus | 85 records, schema validation: 0 errors | ✓ |
| Pilot corpus | 85 records, xref validation: 0 errors | ✓ |
| Dating library | 8 unit tests including the four worked examples | ✓ all pass |
| Confidence aggregation | 5 test cases including asymmetric contradiction | ✓ all pass |
| Vocabularies | Cross-checked against schema enums | ✓ full coverage |
| External identifiers | Pleiades 609302 (Amorium), PMBZ 19429 (Theophilos), PMBZ 16385 (al-Muʿtaṣim), VIAF 9854001 (al-Ṭabarī) | ✓ verified via web |
| Dating arithmetic | AH 223 = 837-12-03 to 838-11-22 | ✓ matches docs |
| Dating arithmetic | AM 6346 = 837-09-01 to 838-08-31 | ✓ matches docs |
| Dating arithmetic | Indiction for 22 July 838 = 1 | ✓ matches docs |

The 25 records in the pilot corpus flagged `editorial_review_required` are deliberate calls for editorial verification, not defects.

---

## Known limitations

These are documented openly rather than papered over:

1. **AAT alignment is mostly pending.** Verified AAT links are added only where confirmed; ~25 concepts carry `aat_match_status: pending` flags for editorial sprint work. This is by policy: do not fabricate external identifiers.
2. **The pilot corpus needs editorial review.** ~25 records were composed from general scholarly knowledge rather than verified against cited editions. They validate cleanly but need consulting the actual texts before publication.
3. **v2 features are preview only.** FuzzyRegion and WitnessRecord work and validate against the v2 preview schema, but the formal v2.0.0 release integrating them with the unified schema is future work.
4. **Manuscript-witness coverage in v1 sources is illustrative.** The three v2 WitnessRecord examples cover the principal witnesses for Theophanes Continuatus and one for al-Ṭabarī. Real source-critical coverage requires hundreds of witness records per major source.
5. **No institutional host yet.** The governance charter assumes one; the prospectus and self-hosting fallback together provide the immediate workaround.

---

## Upgrade path from v1.0

If you have an existing v1.0 setup:

1. Replace `byzfrontier_schema_v1.json` with the v1.0.x version in this release (contains the three bug fixes).
2. Replace `byzfrontier_vocabularies_v1.ttl` with `byzfrontier_vocabularies_v1_1.ttl`.
3. Add the new tools: `byzfrontier_xref.py`, `byzfrontier_dating.py`.
4. Add the pilot corpus and v2 preview to the repository structure per the deployment guide.
5. Update the Claude project's custom instructions to the v1.1 version.

No v1.0 records become invalid; the schema changes are non-breaking.

---

## What's next

Per the deployment guide §6, the recommended first-month agenda is:

- Week 1: setup (Claude project + local repository + GitHub + CI + Zenodo DOI)
- Week 2: cleanup (typos, README, licences)
- Week 3: editorial work (first 5 review-flagged records cleared)
- Week 4: outreach (institutional letters) + extension (first 10 new records)

Beyond month one, the project is no longer in setup. It is in operation. The framework's job is done; the editorial work begins.
