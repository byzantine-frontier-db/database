# Editorial Workflow

This document describes the workflow for adding, validating, and reviewing records in the Byzantine-Islamic Frontier Database. The same procedural rules apply to any contributor — human, AI-assisted, or a mixture.

## Scope

The workflow covers record extraction from primary and secondary sources, validation against schema and cross-reference rules, and editorial review prior to release.

## Hard rules

These rules are non-negotiable. Their **enforcement**, however, differs by rule: some are rejected at
validation, some become validation checks only once deliberately encoded, and some cannot be checked
mechanically at all and rest on editorial judgement plus scheduled audit. "Rule enforcement
classification" below states which is which. **No rule should be assumed validator-enforced unless it
is classified there as such** — the assumption that a written rule is a checked rule is what allowed
the rule-8 and rule-9 breaches recorded below to accumulate unseen.

1. **No fabricated citations.** Every `citation` field must point to a real, verifiable location in a real source. If the exact page or folio is uncertain, the citation reads `[citation needed: exact page]` and `editorial_review_required: true`. Speculative or approximate citations dressed as exact are prohibited.

2. **No fabricated external identifiers.** Pleiades, PMBZ, VIAF, TGN, AAT, Wikidata, and similar identifiers are inserted only when the contributor has verified the identifier resolves to the correct entity. Plausible-looking IDs invented to fill a field are prohibited.

3. **Distinct evidential levels.** Observation, Attestation, and Source records remain distinct. An observation (e.g. a coin find, an inscription, a stratigraphic context) is not collapsed into an attestation; an attestation (a textual mention) is not collapsed into the source that contains it; a source (the textual artefact) is not collapsed into the author or work it transmits.

4. **Provenance honesty.** Where a primary source is reached via a secondary work, the attestation records the primary source with provenance `primary_paraphrase` or `primary_quotation`, and the `notes` field records the secondary route. Where a secondary work is the subject of its own assessment, that becomes an Interpretation record against the secondary work itself.

5. **Editorial review flag.** Any record where the contributor has not directly verified the cited source against the printed page carries `editorial_review_required: true`. Records may be published in this state; they may not move to `workflow_state: published` without verification.

6. **Validate before commit.** Every contribution runs `tools/byzfrontier_validate.py` and `tools/byzfrontier_xref.py` against the affected records before being committed. Records that do not pass validation are not committed.

7. **Honest framing in summaries.** Where a record set is described in writing — a release note, a publication, a presentation — the framing reflects what was actually done, including the role of any AI-assisted extraction and the proportion of records currently in `editorial_review_required: true` state.

8. **Claim placement.** The evidential claim of an attestation lives in `paraphrase` or `direct_quotation`. It never lives only in `notes`, which carries editorial metadata, route pointers and asides. Every attestation carries a non-empty `paraphrase` or `direct_quotation`, regardless of provenance.

   *Provenance: ratified in the Session-5 rule set. Universal validator check added 2026-07-15 (post-Phase-2 Item G2a); back-fill of the 22 pre-identified records the same day (Item G2b).*

9. **Interpretation evidence is attestation-level.** An `InterpretationRecord`'s `supporting_evidence` cites Attestations, never raw Sources. An interpretation rests on at least one attestation of support.

   *Provenance: **RECOVERED 2026-07-23.** A pre-existing rule, previously undocumented in this repository, recovered from the project design record. It had been referenced twice in `docs/schema/backlog.md` — at the Bālis coordinate work and at the Al-Muthaqqab ceramic dossier — without ever having been stated. A reconstruction of the rule from those two usages was proposed in conceptual ontology v0.1 (2026-07-23) and was subsequently confirmed correct against the design record.*

10. **Cross-reference related interpretations.** Related and competing interpretations are explicitly cross-referenced.

    *Provenance: **RECOVERED 2026-07-23.** A pre-existing rule, previously undocumented in this repository, recovered from the project design record.*

11. **Direct observation.** An author's own direct observations are represented as `primary_observation` carrying an `observation_date`.

    *Provenance: **RATIFIED 2026-07-23. This is a ratification, not a recovery, and the distinction is deliberate.** The archived wording was specific to a single extraction phase: "Section-4 personal observations use `primary_observation` + `observation_date` at `schema_version` 2.0.0", scoped to the Eger 2008 gazetteer (SRC-0065). The general form stated above is a **new rule**, ratified 2026-07-23, and it **supersedes** that phase-specific wording. Its scope is deliberately widened from one source to any author reporting their own direct observation. The widening is recorded here, with its date, rather than applied silently: quietly broadening a rule's scope without an audit trail is the failure mode the Ṭaranda correction exists to prevent.*

12. **Attest existing sources inline.** Thin one-clause primaries citing a `SourceRecord` already in the corpus are attested at extraction time, not deferred. Deferral — defer-then-batch — applies only to *mint* decisions.

    *Provenance: ratified Session 5; retroactively applied to the Al-Muthaqqab deferrals (ATT-0450, ATT-0451). Text transcribed from `docs/schema/backlog.md`.*

13. **al-Yaʿqūbī work attribution.** Topographic and administrative content is routed to *Kitāb al-Buldān* (SRC-0008); narrative-historical content to the *Taʾrīkh* (SRC-0003). Each routed attestation states that it follows a convention, not a determination.

    *Provenance: ratified Session 5; retroactively applied to ATT-0339, ATT-0413, ATT-0427. **Provisional**, pending printed verification of one representative case. Text transcribed from `docs/schema/backlog.md`.*

14. **Site displacement.** A displaced occupation is the **same Site** when its footprint overlaps or abuts the earlier one, or when the documentary or stratigraphic evidence treats the move as continuous. It is a **new Site** when the footprints are disjoint and the separation between their nearest edges exceeds the greatest dimension of the larger footprint. Where footprints are unknown — the majority case — the test rests on documentary and stratigraphic evidence of continuity alone. Where no test settles the case, it is recorded as a single Site, the alternative construal is recorded as an Interpretation, and the record is flagged for editorial review.

    *Provenance: **RATIFIED 2026-07-23**, as worded in conceptual ontology v0.2 §15.1.*

    **Guidance.**

    - **The continuity indicators are illustrative, not exhaustive.** "Documentary or stratigraphic evidence" names the two commonest kinds; it does not close the list. Alternative evidence may be adduced — ceramic continuity, toponymic continuity, an epigraphic sequence, a continuous administrative record — provided its relevance to *physical* continuity of the occupied locus is explained in the record rather than assumed. The identity criterion is physical continuity; any evidence bearing on it is admissible, and any evidence adduced must be shown to bear on it.
    - **The threshold and the continuity assessment address different evidence conditions and are not alternative routes to the same judgement.** The displacement threshold applies where reliable spatial footprints exist for both occupations and a geometric comparison is therefore meaningful. The continuity assessment applies where the judgement rests instead on documentary, stratigraphic or interpretative evidence. They are not ranked, and neither overrides the other; they are the tests appropriate to two different evidential situations.
    - **The continuity clause governs the majority of cases.** Seventy per cent of place records in the corpus carry no geometry at all (57 of 190 have coordinates, measured 2026-07-23). For most records the threshold cannot be applied even in principle, and the continuity assessment is not a fallback but the primary and usually the only available test. Contributors should not treat a case as unresolvable merely because footprints are unavailable.
    - **No fixed distance is specified, and none should be introduced.** The threshold is "the greatest dimension of the larger footprint", which is a property of the sites being compared and scales with them: a 400 m displacement makes a new Site of an 80 m hilltop fort and leaves a 600 m lower town unchanged. "Nearest edges" rather than centroid separation is deliberate, since centroid distance is misleading for elongated or irregular sites.

15. **Dual aspect.** Where a thing is both a feature of the terrain and a locus of occupation — a bridge, a fortified pass, a tell that also serves as a landmark — create both a LandscapeFeature and a Site **only when the evidence distinguishes them**: that is, when there are attestations about the terrain feature and separately about the installation. Otherwise create only the aspect the evidence speaks to, and add the second when it earns records of its own. The two are linked by an explicit relationship; neither contains the other.

    *Provenance: **RATIFIED 2026-07-23**, as worded in conceptual ontology v0.2 §15.2.*

### Note on rule provenance

Rules 1–7 originated with this document. Rules 8, 12 and 13 were ratified during Phase 2 and their canonical text is transcribed here from `docs/schema/backlog.md`; the backlog entries remain as the historical record of their ratification, and this document is now the canonical statement. Rules 9 and 10 were recovered on 2026-07-23. Rule 11 was ratified in general form on 2026-07-23, superseding a phase-specific predecessor. Rules 14 and 15 were ratified on 2026-07-23.

**Unnumbered standing rules.** The **bare-mention rule** — a source named without a datum yields a note or a downgraded provenance, never a substantive attestation — is a live standing rule with no number. It is classified below alongside the numbered rules. Assigning it a number is a small outstanding decision.

## Rule enforcement classification

Every rule is classified by **how it can be enforced**, not by how important it is. The scheme is three-way:

- **(a) Negative constraint.** The rule forbids a state that is detectable in the data. Once a check exists it is self-preserving: violations cannot enter.
- **(b) Presence-checkable positive obligation.** The rule requires something to be present, and its presence is mechanically detectable — but only after the rule has been **deliberately encoded** as a check. Until encoded, a rule in this class is invisible to validation and can be breached silently at scale.
- **(c) Judgement-requiring positive obligation.** The rule requires an assessment that cannot be made from the data. Enforcement is editorial workflow plus **scheduled audit**. A cadence is stated for every rule in this class; an audit location without a cadence documents a weakness rather than controlling it.

Several rules split across classes. Where they do, the table gives the dominant class and states the checkable fragment separately, because the fragment is what can be encoded now and the remainder is what must be audited.

### Classification

| Rule | Class | Encoded? | What validation can check | What must be judged |
|---|---|---|---|---|
| 1 — No fabricated citations | **(c)** with (b) fragment | fragment: no | `citation` non-empty; `[citation needed` implies `editorial_review_required: true` | whether the citation resolves to the real passage |
| 2 — No fabricated external identifiers | **(b)** with (c) residue | no | that each external identifier resolves at its authority | whether it resolves to the *correct* entity |
| 3 — Distinct evidential levels | **(c)** with (a) fragment | fragment: yes (schema) | exactly one `source` per attestation; rule-8 claim presence | whether a datum is one attestation or two |
| 4 — Provenance honesty | **(c)** | — | — | whether the transmission chain is correctly recorded and secondary interpretive claims are routed to Interpretations |
| 5 — Editorial review flag | **(a)** + **(c)** | (a): **no** | no record may hold `editorial_review_required: true` **and** `workflow_state: published` | whether the contributor genuinely verified before clearing the flag |
| 6 — Validate before commit | **(a)** | **yes** (CI) | the validators run and pass before merge | — |
| 7 — Honest framing in summaries | **(c)** | — | — | whether external prose reflects what was actually done |
| 8 — Claim placement | **(b)** with (c) residue | **yes**, 2026-07-15 | every attestation carries a non-empty `paraphrase` or `direct_quotation` | whether the claim was *fully* relocated, with no claim material left in `notes` |
| 9 — Interpretation evidence | **(a)** + **(b)** | (a): no · (b): **no** | (a) `supporting_evidence` contains no non-`ATT-` identifiers; (b) `supporting_evidence` non-empty | — |
| 10 — Cross-reference interpretations | **(c)** with (b) fragment | fragment: no | an interpretation naming another `INT-` in prose with no corresponding Relationship | which interpretations are *related* |
| 11 — Direct observation | **(b)** with (c) residue | no | `provenance: primary_observation` implies `observation_date` present, and conversely | whether a passage *is* the author's own direct observation |
| 12 — Attest existing sources inline | **(c)** | — | — | whether a mention is a thin one-clause primary |
| 13 — al-Yaʿqūbī attribution | **(c)** with (b) fragment | fragment: no | attestations against SRC-0003/SRC-0008 **whose own citation does not name the work** carry the rule-13 convention note (see note below) | whether content is topographic/administrative or narrative-historical |
| 14 — Site displacement | **(c)** with (b) fragment | fragment: no | a Site recorded as an unresolved displacement carries a linked Interpretation and a review flag | the displacement judgement itself |
| 15 — Dual aspect | **(c)** | — | — | whether the evidence distinguishes feature from installation |
| *bare-mention (unnumbered)* | **(a)** | **yes**, via rule 8 | a contentless attestation fails the rule-8 check | — |

**Rule 9 is the scheme's clearest illustration and is worth reading as such.** Its (a) half — the ATT-only constraint — is a negative constraint and is **fully compliant: zero of 174 interpretations cite non-attestation evidence**, without ever having been checked. Its (b) half — that support be non-empty — is a presence-checkable positive obligation that **was never encoded, and is breached by 57 of 174 interpretations (33%)**. The same rule, observed perfectly in what it forbids and neglected at scale in what it requires. This is the pattern Item G found for rule 8, recurring, and it is the reason class (b) is worth naming separately: an unencoded (b) rule is not a weak rule, it is an invisible one.

**Note on the rule-13 predicate (amended 2026-07-23).** The clause *"whose own citation does not name the work"* is a correction to the check specification, not to rule 13. Rule 13 governs attestations whose al-Yaʿqūbī work attribution was supplied **by convention** — the case where a secondary names "al-Yaʿqūbī" without the work and the extractor routes by content type. Where an attestation's own citation names the work (e.g. `al-Yaʿqūbī, Kitāb al-Buldān (de Goeje ed., BGA VII)`), the attribution was **determined, not routed**, and no convention note is owed. The unqualified predicate produced two false positives on measurement — ATT-0003 and ATT-0051, both Phase-1 records naming their work in the citation and both correctly routed on content. Under the amended predicate the corpus returns **0 violations across 5 routed attestations**, with the 3 expected notes present (ATT-0339, ATT-0413, ATT-0427).

### Checks that are currently vacuous, and their activation triggers

A check that cannot presently fail is not a check that has passed. Four of the checks classified above return zero violations **because their triggering condition does not yet exist in the corpus**, and recording them as compliant would reproduce the false assurance the preamble correction addresses. Each is listed with the event that makes it exercisable. Measured 2026-07-23.

| Check | Why it cannot presently fail | Activation trigger |
|---|---|---|
| **Rule 2** — no fabricated external identifiers | **Zero external identifiers exist in the corpus** (0 across all 1,453 records). There is nothing to resolve, correctly or otherwise. | The first Pleiades, PMBZ, VIAF, TGN, AAT or Wikidata identifier added to any record. Expected soon: both the CIDOC alignment work and the vocabulary-file external alignments require them. |
| **Rule 5(a)** — no record `published` while `editorial_review_required: true` | **Zero records are published.** All 1,453 are `draft`, and all 1,453 carry the flag, so the conjunction has never been satisfiable. | First publication. **Implement as a release gate, not a corpus scan** — a corpus scan will report zero indefinitely and give false assurance precisely when the risk begins. |
| **Rule 14** — site displacement | No Site records exist; the spatial-type migration has not begun, and no record carries phase-level displacement. | The spatial-type migration introduces Site records with phases. |
| **Rule 15** — dual aspect | No LandscapeFeature/Site pairs exist as such, so no dual-aspect case can be tested. | The spatial-type migration introduces the first dual-aspect case. |

All other checks classified above **are** exercisable against the present corpus and their results are real: rule 8 (477 attestations under test), rule 9(a) and 9(b) (174 interpretations), rule 10 (174 interpretations, 144 relationships), rule 11 (477 attestations), rule 3(a) (477 attestations), rule 13(b) (5 routed attestations), rule 6 (CI, every commit).

### Review cadences for class (c)

| Rule | Cadence |
|---|---|
| **1, 5** (citation accuracy; genuine verification) | Per record, through the existing `editorial_review_required` flow. **Plus a 10% sample audit, at each release, of records where the flag has been *cleared*.** The audit target is cleared flags, not set ones: setting the flag is self-declaring, clearing it is the unverifiable act. |
| **2** (identifier correctness) | On addition; **plus an annual re-resolution sweep**, since upstream authorities merge, redirect and deprecate identifiers after a record is written. |
| **3** (attestation granularity) | Per record at extraction; **plus a corpus-wide sweep at each release** over attestation pairs sharing a source and an entity — the pattern that produced the ATT-0470 split and the Item-F retain-both outcome. |
| **4** (provenance honesty) | Per record at extraction; **plus an audit at each source's completion**, when the whole transmission pattern for that source is visible at once. |
| **7** (honest framing) | At each release note, publication or presentation. Not corpus-scheduled; the trigger is the external text. |
| **8 residue** (claim fully relocated) | Per record at extraction; **plus a sweep at each release** for `notes` fields carrying assertive content. |
| **10** (which interpretations are related) | **Triggered: whenever an entity gains its second or any subsequent interpretation.** Relatedness is only assessable when there is something to relate to, so a calendar cadence would fire mostly on nothing. **Plus a corpus-wide sweep at each release.** |
| **11 residue** (identifying direct observation) | **Per entry at extraction, never by automated detection.** The Session-6 §4 inventory retraction established this: an automated scan for "Personal Observations" sections proved unreliable and its inventory was withdrawn after a 3-of-4 reversal. **Plus an audit at each source's completion.** |
| **12** (thin one-clause mentions) | Per record at extraction; **plus a sweep at each source-minting pass**, when deferral decisions are being reviewed anyway. |
| **13** (topographic vs narrative routing) | Per record at extraction. **Rule 13's provisional status is resolved by a one-off action, not a cadence**: printed verification of one representative case, currently outstanding. Until then every routed attestation carries the convention note. |
| **14** (displacement judgement) | Per record at extraction; **triggered whenever a Site gains a phase whose designated geometry differs from its predecessor's**. |
| **15** (dual aspect) | Per record at extraction; **plus a sweep at each release** over LandscapeFeature/Site pairs sharing a standardised name or coincident geometry. |

Two cadences are load-bearing and are called out. The **cleared-flag sample audit** (rules 1 and 5) is the only check on the one step in the workflow that has no other witness. The **per-entry rule for rule 11** is not a preference but a finding: it is the direct consequence of the §4 inventory retraction, and automated detection should not be reintroduced for it.

### Compliance state as measured

Measured 2026-07-23 against `origin/main`, 1,453 records, by direct scan of the corpus. Rules not listed have not been measured.

| Rule | Measurement | State |
|---|---|---|
| **8** | 477 attestations scanned for a non-empty `paraphrase` or `direct_quotation` | **0 violations.** Check encoded 2026-07-15; the class has not recurred since. |
| **9 (a) — ATT-only** | 174 interpretations scanned for non-`ATT-` identifiers in `supporting_evidence` | **0 violations. Fully compliant**, and compliant before any check existed. |
| **9 (b) — non-empty** | 174 interpretations scanned for empty `supporting_evidence` | **57 violations (33%).** Not yet encoded as a check. |
| **10** | relationships scanned for an `INT-` endpoint; interpretations scanned for prose references to other interpretations | **0 structural cross-references; 29 interpretations cross-reference in prose. Compliance is 100% textual and 0% structural.** The obligation is being met, in a form that is not queryable. |
| **11 (general form)** | 477 attestations scanned in both directions: `primary_observation` without `observation_date`, and `observation_date` without `primary_observation` | **0 violations either way.** 19 attestations carry `primary_observation`, all 19 dated. The general form has an empty back-fill; the ratification takes effect prospectively. |

**Indicated follow-up, not performed here.** Encoding the rule-9(b), rule-5(a), rule-10 and rule-11 checks, and back-filling the 57 rule-9 breaches and promoting the 29 rule-10 prose cross-references, are record and tooling changes outside the scope of this documentation patch. The Item-G sequence discipline applies when they are undertaken: **add each check first and confirm it reports exactly the pre-identified count — 57 for rule 9(b), 29 for rule 10, 0 for rules 5(a) and 11 — before any back-fill**, so that the interval between the two commits is positive confirmation the check catches what was predicted and nothing else.

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
