# Schema Backlog

Tracked schema follow-up items. Not part of any current commit.

## D3.i — `additionalProperties: false` on RecordMetadata (OPEN)

Board follow-up from the pre-Phase-2 schema batch. Setting `additionalProperties: false`
on `RecordMetadata` would prevent future undeclared metadata keys from slipping through
validation (the mechanism by which `editorial_review_required` went unenforced until the
2026-06-30 back-fill).

- **Type:** MAJOR schema change (can newly reject records) — Editorial Board approval + §5.6.
- **Diagnostic prerequisite (done):** a corpus-wide stray-key scan (2026-07-04) found
  **zero** non-schema keys in any record's `metadata`. The hardening would therefore break
  no existing record; it only guards against future stray keys.
- **Status:** ready to schedule as its own MAJOR change once the current v2 transition
  window closes. Re-run the stray-key scan immediately before applying, in case Phase 2
  extraction introduced any.

## D3.ii — schema_version cascade (POLICY APPROVED; migration in progress)

Lazy migration of `metadata.schema_version`, approved by the Board and documented in
governance §5.6. Records update to the current schema version only on their next MINOR/MAJOR
bump; no dedicated rewrite pass.

- **Mechanism:** the transition-window validator (`byzfrontier_validate.py`, repeatable
  `--schema`) dispatches each record to the schema matching its declared `schema_version`.
- **Status:** in progress and self-completing. Migration is complete when every record has
  reached the current schema version; at that point the superseded schema and its
  `--schema` entry can be retired and any deferred required-field promotion (see split-ship,
  §5.6) can land as its MAJOR step.
- **Tracking metric:** count of records still at each `schema_version` (a one-line scan).

## Phase 2 editorial follow-ups (scheduled)

### Bālis identification — InterpretationRecord (before Session 7 closes)

Session 1 surfaced a coordinate divergence on ENT-PLC-0037 (Bālis / Meskene / Barbalissos):
the stored editorial point (35.83, 38.27) and Eger 2008's gazetteer point (35.98836,
38.10952) differ by **~22.8 km — ~4.6× the stored 5000 m uncertainty radius**. The stored
coordinate is explicitly flagged "verify against a gazetteer", and Eger 2008 is that
gazetteer. Left unresolved this session (compare, do not overwrite). Action: mint an
InterpretationRecord on the Bālis identification weighing the two points, and decide whether
to adopt Eger's coordinate — which would carry the corresponding MINOR/MAJOR bump on the
entity. **Target: before Session 7 closes.**

### ATT-0339 — printed Ibn Shaddād verification

ATT-0339 (Adhana fortification under al-Amīn; refortified 808–810) is provisionally attributed
to al-Yaʿqūbī's **Kitāb al-Buldān (SRC-0008)** on scholarly-probability grounds (frontier-town
foundation/settlement content characteristic of the Buldān and of Ibn Shaddād's use of it),
flipped this session from the earlier Taʾrīkh (SRC-0003) guess. Carries `[citation needed]`.
Action: check the printed Ibn Shaddād, al-Aʿlāq al-khaṭīra, which names its al-Yaʿqūbī source;
confirm or disconfirm the SRC-0008 attribution and clear the flag.

## Deferred source-minting queue (Phase 2)

**Standing policy (from Session 2):** during extraction, one-clause primary-source mentions
are **deferred, not minted mid-session** (keeps sessions focused; matches Session 1's
zero-mint precedent). Deferred sources are queued here and minted in a **dedicated
source-minting pass** at a checkpoint (suggested: before Session 4, or whenever the queue
reaches ~5), which also back-fills the attestations that reference them. Both named
geographers below recur across the thughūr/ʿawāṣim material, so minting them once serves all
later sessions.

- **al-Iṣṭakhrī** — deferred at ATT-0354 (Al-Ḥadath "fertile lands"). Major 10th-c. geographer;
  will recur.
- **Ibn Rusta** — deferred at INT-0165 / Dulūk ("thughūr site in 903"). Major geographer; will recur.

## Tooling fix applied (Session 2 follow-up)

`normalize_gazetteer.py` header detection previously mis-keyed Al-Ḥadath's coordinate under the
concordance token "Göynük)" (embedded era/Modern markers weren't excluded). Fixed; sidecars
`eger_2008_coordinates.json` and `eger_2008_page_map.json` regenerated — Al-Ḥadath's point
(37.70N 37.44E) and page span (pp. 458–462) now key correctly. Cleaned text unchanged.
Commit the updated tool + regenerated sidecars together.

## Tooling fix #2 (Session 3 follow-up) — entry-boundary phantoms

`normalize_gazetteer.py` was minting phantom entries off two line types inside a real entry:
(1) `(see Chapter N)` cross-reference lines, and (2) wrapped concordance continuations whose
"Modern" keyword sat on the previous line (e.g. `Gözeneler68`). These phantoms stole neighbouring
coordinates (Session 3 rows #8, #11/#12). Fixed: `(see…` lines and any line immediately preceded
by a concordance line are excluded from header detection. Sidecars regenerated — Iskandarūna,
Al-Muthaqqab, and Al-Kanīsa as-Sawdā' now key correctly; the UNRECOVERABLE 43750/95800 point is
re-attributed to ENT-PLC-0121 (Al-Kanīsa/Epiphaneia), not al-Maṣṣīṣa. Cleaned text unchanged.
Commit the updated tool + regenerated sidecars together.

## Source-minting queue — AT CHECKPOINT (do before Session 4)

Queue is now ~6 and past the ~5 trigger. A dedicated source-minting pass is warranted before
Session 4:
- al-Iṣṭakhrī (recurs), Ibn Rusta (recurs) — from Session 2
- al-Balkhī (Hārūnīyya joint small-fort description)
- al-Dimashqī (Kamkh, thughūr al-jazīra list)
- Abū ʿAmr al-Bāhilī (Ḥiṣn Manṣūr naming tradition)
- unnamed source behind the Jawzāt garrison roster (Abū ʿAmr al-Ṭarsūsī named as qāḍī, not author)
Pass mints SRC-0066+ for each resolvable source and back-fills the deferred attestations to point
at them (updating the placeholder notes in ATT-0354, INT-0165, and the Session 3 deferrals).

## Source-minting pass — DONE (2026-07-08)

Cleared four of the six queued sources by minting SourceRecords and back-filling the deferred
mentions (patch: phase2_source_minting_pass.patch):
- **SRC-0066 al-Iṣṭakhrī** — attestations ATT-0405 (Hārūnīyya small-fort), ATT-0407 (Al-Kanīsa Friday-mosque)
- **SRC-0067 Ibn Rusta** — ATT-0408 (Dulūk thughūr, 903)
- **SRC-0068 al-Dimashqī** — ATT-0409 (Kamkh thughūr al-jazīra)
- **SRC-0069 al-Balkhī** — ATT-0406 (Hārūnīyya) — **FLAGGED for bibliographic review**: original lost,
  preserved only via al-Iṣṭakhrī/Ibn Ḥawqal; Curtis to confirm mint-as-distinct vs fold into SRC-0066/0009.
Deferral notes on ATT-0369, ATT-0375, ATT-0401 updated to RESOLVED; the four referenced entities
(ENT-PLC-0062/0078/0121/0122) MINOR-bumped with reciprocal linked_attestations.

## Two standing categories for hard-to-source citations

**(A) Authorless-but-citable** — a real, citable work with no named author. Model as a normal
SourceRecord with `author_unnamed: true`. Adopted: Acta Conciliorum Oecumenicorum (SRC-0071),
Antonine Itinerary (SRC-0074). These get minted and attested normally.

**(B) Named tradent, unknown author** — a named person credited with a report/tradition but with
no citable work of their own. NOT minted; held as notes until a printed check turns up a work.

Mentions credited to a *named authority* for whom Eger cites *no citable work* — not minted, held here:
- **Abū ʿAmr al-Bāhilī** — Ḥiṣn Manṣūr naming tradition (ATT-0378). A naming tradition credited to him;
  no work cited, single mention. Stays deferred.
- **Jawzāt garrison-roster source** — only a qāḍī name (Abū ʿAmr al-Ṭarsūsī) survives, not an author.
These resolve only if a printed-source check turns up an actual work/edition; otherwise permanent notes.

## Coordinate-identification InterpretationRecords needed (before Session 7 closes)

Two stored editorial coordinates diverge from the Eger 2008 gazetteer point beyond their
uncertainty radius, on the same settlement — each needs an InterpretationRecord weighing the
two points (and a decision whether to adopt Eger's), per the precedent set at Bālis:
- **ENT-PLC-0037 Bālis** — stored vs gazetteer ~22.8 km (4.6× radius). [Session 1]
- **ENT-PLC-0016 Malaṭya** — stored (38.35, 38.30; ±8 km) vs gazetteer (38.42173, 38.36605) =
  9.84 km, both Battalgazi/Eski Malatya. [Session 4]
Closed for Manbij (ENT-PLC-0043): gazetteer corroborated the estimate to 768 m — confidence
raised 3→4, radius 3000→1500 (patch phase2_manbij_coord_corroboration.patch).

## Section-4 (Personal Observations) — verify PER ENTRY, not by the exclusion list

Finding from Session 4: the front-matter "visited summers 2002–2006" line is a general project
statement, NOT a per-entry guarantee. Malaṭiya and Marʿash are NOT on the non-visited exclusion
list yet contain no §4; Shimshāṭ IS on the non-visited list yet HAS a §4 section. The only
reliable signal is an actual "Personal Observations" header in the entry.

**§4 inventory — RETRACTED, unreliable (see Session 6 correction below)**
Earlier list (entries whose text contains a Personal Observations section):
Adhana (p440), ʿAyn Zarba (449), Dulūk (457), Al-Ḥadath (462), Hārūnīyya (468), Ḥiṣn Manṣūr
(474), Al-Kanīsa/Gözeneler (485), Al-Maṣṣīṣa (509), Al-Muthaqqab-or-Qūrus (513), Raʿbān (518),
Shimshāṭ (521), Sīs (525), Ṭaranda (537), Ṭarsūs (549), Zibaṭra (554). All other entries →
Sections 1–3 only, no primary_observation. Master prompts from Session 5 on must instruct
per-entry §4 verification.

## Deferred source: Ibn al-ʿIbrī (Bar Hebraeus)

Cited at Malaṭiya for Theophilus's 837 capture and 866 events ("Ibn al-ʿIbrī, a Christian
historian from Malatiya"). Two candidate works: Ecclesiastical History and the Chronography
(Chronicon Syriacum / Arabic Taʾrīkh mukhtaṣar al-duwal). The cited content is secular/political
history, which points to the **Chronography** — but the edition is unconfirmed (footnote
de-interleaved). Queue for the next source-minting pass; lean Chronography, confirm edition.

## Methodological pass: Malaṭiya Balādhurī dedup

Session 4 flagged that some new SRC-0065-routed primary attestations on ENT-PLC-0016 (esp. the
Balādhurī conquest strand) may overlap Phase-1 records already on the entity. Retained as-is,
flagged. Run a dedup pass (its own methodological item) to reconcile overlapping primary
attestations across Phase-1 and Phase-2, deciding which to keep/merge. Not part of any session.

## Tool cosmetic (next regeneration): Marʿash header key

The sidecar keys Marʿash's entry as the truncated `Mar‘` (ʿayn/quote truncation of the header).
Coordinate absence and the pp.494–500 span are correct; only the display key is truncated.
De-truncate on the next normalize_gazetteer.py run.

## Source-minting queue — additions (Session 5)

Carry-forward + new, for the next minting pass:
- **Ibn al-ʿIbrī (Bar Hebraeus)** — Malaṭiya; lean Chronography (Session 4).
- **Acta Conciliorum Oecumenicorum** — Al-Muthaqqab location datum. A conciliar-acts corpus, not a
  single author — mint as a documentary/edition source, or route per its editor; needs a bibliographic call.
- **Ibn al-Shiḥna** — Qūrus, Cyrrhus church-materials (multi-tradent). No SourceRecord.

## Attestation back-fill (existing sources) — CLOSED by Rule 12

Distinct from the minting queue: these sources ALREADY have SourceRecords, so a thin one-clause
mention just needs an attestation (no mint). Deferred at Al-Muthaqqab for consistency, but they can
be back-filled without a minting pass whenever convenient:
- **al-Masʿūdī (SRC-0053)** — "ḥiṣn on the slope of Jebel Lukkam".
- **al-Idrīsī (SRC-0038)** — Muthaqqab as one item in a coastal succession.
Worth deciding a standing rule: for an *existing* source, do thin one-clause mentions get attested
inline (cheap, completeness) rather than deferred? Leaning yes — deferral is really for *minting*.

## al-Yaʿqūbī Buldān-vs-Taʾrīkh — RESOLVED by Rule 13 (convention adopted)

ATT-0427 (Al-Maṣṣīṣa topographic bridge datum) routed to Kitāb al-Buldān (SRC-0008); Eger doesn't
specify and Taʾrīkh (SRC-0003) isn't excludable. Same ambiguity as ATT-0339 (Session 1, flipped to
Buldān). This recurs across the appendix — worth a standing convention (default topographic/
administrative → Buldān, narrative-historical → Taʾrīkh) confirmed against print in a batch, rather
than a per-case coin-flip.

## Al-Muthaqqab ceramic discrepancy (editorial review)

Entity analytical_summary says "no definitive Early Islamic pieces"; Eger's 2005 autopsy (OBS-0247)
reports Early Islamic wares among the Mopsus Survey baskets. Not reconciled; the summary predates the
gazetteer autopsy. Editorial decision needed on whether to revise the summary (would be MINOR content).

## Standing rules ratified (Session 5)

- **Rule 12 — attest existing sources inline.** Thin one-clause primaries citing a SourceRecord
  already in the corpus are attested at extraction time, not deferred; deferral (defer-then-batch)
  applies only to *mint* decisions. Compatible with rule 5 (inline attestations still carry
  editorial_review_required + edition [citation needed]). **Retroactively applied**: al-Masʿūdī
  (ATT-0450) and al-Idrīsī (ATT-0451) at Al-Muthaqqab — the Session-5 deferrals are CLOSED.
  Active in master prompts from Session 6.
- **Rule 13 — al-Yaʿqūbī work attribution.** Topographic/administrative content → Kitāb al-Buldān
  (SRC-0008); narrative-historical → Taʾrīkh (SRC-0003). Provisional pending printed verification of
  one representative case. Compatible with rule 4 (each routed attestation states it is a convention,
  not a determination). **Retroactively applied**: ATT-0339, ATT-0413, ATT-0427 now carry
  "routed per rule 13, pending printed confirmation" (the "work uncertain" / "third instance" flags
  are removed). Active in master prompts from Session 6.

## Open methodological items (status snapshot)

- Al-Muthaqqab ceramic discrepancy — editorial call by Curtis (analytical_summary vs OBS-0247).
- Coordinate InterpretationRecords — Bālis (ENT-PLC-0037) + Malaṭya (ENT-PLC-0016), before Session 7.
- Source-minting queue — Ibn al-ʿIbrī (lean Chronography), Acta Conciliorum Oecumenicorum, Ibn al-Shiḥna.
- Malaṭiya Balādhurī / Phase-1 dedup pass (corpus-wide, its own methodological item).
- Page-number restoration (standing) — entry-level page spans in use via the page map.

## §4 detection — inventory RETRACTED; verify per-entry only (Session 6)

Session 6 proved the §4 inventory unreliable: on this block it was wrong on **3 of 4** sites.
Two failure modes, and no automated method survives them:
- **Boundary spill:** a §4 header sits before its entry's closing coordinate but *after* a page
  break, so page-based attribution hands it to the next entry (Sanjah's p521 §4 → wrongly Shimshāṭ;
  Sīs's p525 §4 → wrongly Sumaysāṭ).
- **Typos:** Sumaysāṭ's header reads "Personal Ob**v**servations" — exact-match scans miss it.
- **Header-detection gaps:** wrapped/trailing-number entry names (Mar‘, Ṭaranda, Ṭarsūs) aren't
  matched, so "nearest header above" skips to the wrong entry — structural attribution fails too.

**Corrected Session-6 reality:** Sanjah/Bahasnā (§4, 9/26/04), Sīs (§4, 07/20/04), Sumaysāṭ
(§4, 9/26/05) are VISITED; **Shimshāṭ has NO §4** (Research section is published archaeology) despite
being flagged in the old inventory. The extracting Claude's per-entry reads are authoritative.

**Standing rule (Session 7+):** do NOT ship a §4 "guess" column. Master prompts instruct the
extracting Claude to determine §4 per entry by reading the text between the entry header and its
closing coordinate, matching **typo-tolerantly** (`Personal Ob[a-z]*ervations`) and requiring
first-person autopsy prose. The front-matter non-visited list and any inventory are hints at best.

## Source-minting queue — additions (Session 6)

New primaries with no SourceRecord (defer-then-batch, for the next minting pass):
- **al-Wāqidī** (via Balādhurī, Sīs departure-dating strand)
- **Antonine Itinerary** (Sīs/Flaviada)
- **Cicero** (Sīs/Pindenissus)
- **Theophylact Simocatta** (Sumaysāṭ)
Queue now: Ibn al-ʿIbrī, Acta Conciliorum Oecumenicorum, Ibn al-Shiḥna, al-Wāqidī, Antonine
Itinerary, Cicero, Theophylact Simocatta (~7) — a minting pass is warranted before/with Session 7.

## Review flag (Session 6): ATT-0470 Ibn Ḥawqal/al-Iṣṭakhrī consolidation

The joint 951-recension datum was consolidated into one attestation (ATT-0470, source SRC-0066,
Ibn Ḥawqal named in citation) rather than minting a duplicate. Reasonable, but worth confirming it
shouldn't be two parallel attestations (cf. the Hārūnīyya joint pattern, ATT-0369/0405/0406).

## Pre-Session-7 work — DONE (2026-07-13)

- **ATT-0470 split** (patch phase2_att0470_split.patch): the joint Ibn Ḥawqal/al-Iṣṭakhrī datum at
  Sumaysāṭ split into two parallel attestations — ATT-0470 (Ibn Ḥawqal, SRC-0009, MAJOR bump for the
  source change) and ATT-0478 (al-Iṣṭakhrī, SRC-0066) — per rule 3 and the Hārūnīyya precedent.
- **Source-minting pass 2** (patch phase2_minting_pass_2.patch): minted SRC-0070–0076 and back-filled
  attestations ATT-0479–0485. Named authors: Ibn al-ʿIbrī (SRC-0070, Chronicon Syriacum per content),
  Ibn al-Shiḥna (0072), al-Wāqidī (0073, via Balādhurī), Cicero (0075), Theophylact Simocatta (0076).
  **Authorless-but-citable** (author_unnamed: true, NOT "named tradent"): Acta Conciliorum Oecumenicorum
  (0071), Antonine Itinerary (0074). ATT-0464 (Sīs) deferral note resolved. **Flag:** ATT-0485
  (Theophylact) is a thin bare-mention attestation (conf 2) — Curtis may prefer note-only.
- **Coordinate InterpretationRecords** (patch phase2_coordinate_interpretations.patch): INT-0169 (Bālis)
  and INT-0170 (Malaṭya) document the divergences; created ATT-0486 (Bālis gis) for rule-9 support.
  **Entity coordinates NOT changed** — the adoption decision (MAJOR re-coordination) is left to Curtis.
  This clears the "before Session 7 closes" deadline for both.

Minting queue is now empty except the standing "named tradent, unknown author" holds (Abū ʿAmr
al-Bāhilī, Jawzāt roster). Still open: Al-Muthaqqab ceramic discrepancy (editorial), Malaṭiya Balādhurī
dedup pass, coordinate-adoption decisions for Bālis/Malaṭya (INT-0169/0170), page-number restoration.

## Theophylact bare-mention — RESOLVED (2026-07-13)

The ProvenanceCategory enum has no bare_mention/name_occurrence value, so ATT-0485 (a name-occurrence
of Sumaysāṭ in Theophylact's "mentioned in" list) was **deleted** — a contentless attestation collapses
the observation/attestation distinction (rule 3). **SRC-0076 preserved** with a pre-emptive-mint note
(Theophylact is canonical, likely to recur in later phases). ENT-PLC-0073 de-linked and its bump
reverted (net-zero). Patch: phase2_theophylact_fix.patch. Standing rule: bare "mentioned in" lists are
notes or a downgraded provenance — never a substantive attestation.
