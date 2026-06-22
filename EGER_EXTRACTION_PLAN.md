# Eger 2015 extraction plan

Source: Eger, A. Asa. *The Islamic-Byzantine Frontier: Interaction and Exchange among Muslim and Christian Communities*. London and New York: I.B. Tauris, 2015. (SRC-0007 in corpus)

Order: sequential (with chapter 8 done out of order)
Target pace: one session per day

## Session tracker

| # | Material | Pages | Status | Records | Commit | Verified |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ch. 8 Byzantine Frontier | 246-263 | EXTRACTED | 49 | fa2b5cd | ATT-0058 only |
| 2 | Introduction | 1-22 | EXTRACTED | 11 | d8dc240 | pending |
| 3 | Part 1 intro + Ch. 1 (full) | 23-68 | EXTRACTED | 88 | 62a7c35 | pending |
| 4 | (subsumed into session 3) | - | MERGED | - | - | - |
| 5 | Ch. 2 part A | 69-85 | pending | | | |
| 6 | Ch. 2 part B | 86-101 | pending | | | |
| 7 | Ch. 3 Eastern Thughur (NE Anatolia, dissertation core) | 102-126 | EXTRACTED | 87 | 4926ef9 | pending |
| 8 | Ch. 4 part A (Balikh) | 127-142 | EXTRACTED | 50 | bd09bee | pending |
| 9 | Ch. 4 part B (Khabur) | 143-157 | EXTRACTED | 47 | 42f9277 | pending |
| 10 | Ch. 5 Western Thughur (Cilicia) | 158-182 | EXTRACTED | 114 | 2fbdb8f | pending |
| 11 | Part 2 intro + Ch. 6 (Late Roman prologue) | 183-197 | EXTRACTED | 32 | 9e3f18b | pending |
| 12 | Ch. 7 part A (Hydraulic Villages I) | 198-213 | EXTRACTED | 73 | d5ee70d | pending |
| 13 | Ch. 7 part B (Hydraulic Villages II) | 214-229 | EXTRACTED | 47 | b24ea4f | pending |
| 14 | Ch. 7 part C (Hydraulic Villages III) | 230-245 | EXTRACTED | 97 | 46aa268 | pending |
| 15 | Ch. 9 Epilogue (Middle Byzantine castles, dissertation period) | 264-276 | pending | | | |
| 16 | Ch. 10 part A (Frontier interaction) | 277-293 | EXTRACTED | 54 | 6638855 | pending |
| 17 | Ch. 10 part B | 294-309 | pending | | | |
| 18 | Conclusions | 310-end | EXTRACTED | 22 | 14b36bc | pending |

## Follow-up items (across chapters)

- ATT-0058 (salt-mines): verified per Option 1 verification session.
- INT-0012 (Cappadocian elite acculturation): split Ball 2005 dissent into separate attestation against new Ball SourceRecord.
- ATT-0061 (Heraklios speech): confirm SUNY al-Tabari vol. XI translator (Blankinship?).
- Sis-departure dating contradiction (Ibn Shaddad 711-12 vs Baladhuri after al-Waqidi 808-9): create two primary SourceRecords + Interpretation per governance section 5.4.
- Deferred from ch.8: Hisn Hiraqla, Lu'lu'a, Safsaf forts; c.831 al-Matmura raid; Kibyrrhaiotonon maritime theme; Michael Maleinos; Pseudo-Jahiz, Ibn al-Faqih, Ibn al-Adim corroborating sources; Selime-Yaprakhisar, Canli Kilise, Acik Saray, Gumuskoy/B16 archaeological sites.
- Session 17 editorial review queue: (1) possible EVT duplicate — ENT-EVT-0049 (Muʿāwiya transports Zuṭṭ/Sayābija from Baṣra) vs ENT-EVT-0034 (Muʿāwiya transports Persians to Anṭākiya 669/70) — same agent/date, different described population; either Eger's sources use different ethnic terminology for one event, OR two distinct transport events in succession. Documented inline, decision deferred. (2) Bundār/Theodore, Qurra b. Thābit, ʿImrān b. Shāhīn, Ḥabīb ibn Maslama anchored modern_synthesis against SRC-0007 via Cobb/Bonner/Wheatley/Keiko — no primary edition. Worth eventual independent verification. (3) SourceRecord genre enum gap: no value for diplomatic letter (SRC-0059 Hārūn letter to Constantine VI forced to other). Adds to the canal/oration/rhetorical_orations genre gaps logged previously. (4) Rāshidūn polity gap remains open — blocks political_affiliation for Ḥabīb (conquest-era person minted this session). Now affects 3+ persons across sessions 14, 17.
- Hamdanid polity gap (flagged session 15, CLOSED session 16 as ENT-POL-0004 Hamdanid Emirate, place_type administrative_unit): no ENT-POL for the Hamdanid dynasty (Aleppo/Mosul, c.890-1004), recurring across multiple chapters. Sister to Rāshidūn (session 14) and pre-existing Buyid gap. Mint when convenient using bootstrap pattern; non-blocking.
- Buyid polity gap (re-flagged session 15): no ENT-POL for the Buyid dynasty (c.934-1062), occasionally mentioned in chapter 7-9 material. Non-blocking.
- ENT-GRP schema gap (flagged session 15): no $def for group/tribal/dynastic entity type. Blocks first-class entity records for Hamdanids, Mirdasids, Numayrids, ʿUqaylids, Banū Tanūkh, Banū Tamīm, Qays, Asad, Rabīʿah, Kinda, Nabaṭ, Melkites, Taghlib, Zuṭṭ, Jarājima/Mardaites (accumulating across sessions). Polities partially serve this role for dynasties but not for tribal or religious groupings. Logged as Schema v1.1 candidate alongside the dispute-encoding gap.
- Editorial review flags from session 15: ENT-PLC-0058 (Dayr Simʿan) vs Eger's "Qalʿat Simʿān" may be distinct entities — verify; Sebastea (ENT-PLC-0166 ex PROV-PLC-1411) — Eger places in Cappadocia where it is conventionally reckoned Pontus/Sivas, may be a different Sebastea or an Eger error.
- SCHEMA GAP (substantial, flagged session 14): no first-class structural mechanism for encoding inter-interpretation scholarly disputes. RelationshipRecord source_entity/target_entity require entity records (persons, places, events, polities), not interpretations. InterpretationRecord supporting_evidence/counter_evidence accept only ATT references. The corpus has accumulated multiple recorded disputes (Tchalenko/Dead Cities/Dehes in ch.2B; Eger vs Robinson on Site of Aleppo in ch.4B; Berthier vs Samuel & Decker on agricultural revolution in ch.7B; Robinson vs Donner on Raqqa-headquarters report and Bulliet vs Eger on conversion-curve timing in ch.7C). All currently documented inline in INT notes by ID. Proposed for Schema v1.1: either extend RelationshipRecord source/target to permit interpretations, or add a dedicated DisputeRecord type. Lower priority gaps remain: PlaceType.canal/irrigation_work; SourceRecord.genre.rhetorical_orations; EventSubCategory capital/seat_relocation, renaming, death/burial.
- Tigris River absence (flagged session 13, CLOSED session 17 as ENT-PLC-0174 Tigris River, place_type river, alt_name Dijla): the Tigris recurs in passing across multiple chapters but no PlaceRecord exists. Sister gap to the Euphrates (ENT-PLC-0044). Worth minting before any major dissertation use of the corpus, particularly since the Khabūr drains into the Tigris-Euphrates system. Mint when convenient — non-blocking for current extraction pace.
- Session 12 (Ch. 7 part A) modern_synthesis caliphal-grants flag: ATT-0218–0240 contain several caliphal land-grant/canal facts (Nahr Saʿīd, Bālis qaṭīʿa, ʿAbd al-Malik's grants) attested against SRC-0007 as modern_synthesis because Eger routes them through Kennedy/Kātbi rather than naming a clean primary footnote. Decision deferred to editorial review: keep as modern_synthesis (honest about Eger transmission) OR swap to Yāqūt/Balādhurī primaries (requires independent verification of the primary editions). Recommend keeping current state until printed-edition verification possible.
- Schema vocabulary gaps accumulated across sessions: (1) PlaceType enum lacks `canal` / `irrigation_work` (worked around as `other` for Nahr Maslama, Nahr al-Abbāra/Turkmān, Nahr Quwayq, etc., sessions 5-6); (2) SourceRecord genre enum lacks `rhetorical_orations` (worked around as `other` for Libanius SRC-0043, session 11). Worth proposing as Schema v1.1 vocabulary extensions to the Technical Lead.
- Provenance-classification spot-check (audit, 2026-06-17): 6 attestations with unusual provenance values were reviewed:
  - ATT-0085 (modern_interpretation, only record using this value): keep as attestation but harmonise provenance to modern_synthesis. Paired with INT-0022.
  - ATT-0096 (modern_identification): keep as attestation. Flat multi-name historical identification, related interpretive complexity recorded elsewhere.
  - ATT-0108 (modern_identification): reclassify to InterpretationRecord. "Most likely" language signals weighing of alternatives.
  - ATT-0167 (modern_identification): reclassify to InterpretationRecord. Notes explicitly say "Hypothetical identification by Eger."
  - ATT-0181 (modern_identification): reclassify to InterpretationRecord. Argument structure with multi-line corroboration.
  - ATT-0182 (modern_identification): reclassify to InterpretationRecord. Multi-line of evidence supporting identification.
  Action: handle during eventual editorial review pass when records can be reshaped properly (Attestation and Interpretation have different schemas).
- Session 9 (Ch. 4 part B) deferred / flagged: ATT-0183 (Diyar Mudar / Raqqa-Rafiqa-Harran Towns summary, modern_synthesis against Eger) overlaps the Balikh-half session's Towns coverage — editorial de-duplication required against any session 8 ATTs covering the same material. Nahr Said dating reconciliation (INT-0056) and Eger vs Robinson dispute (INT-0050 vs INT-0051, counter_evidence wired) recorded but not adjudicated.
- Session 6 (Ch. 2 part B) deferred: Qenneshre 811 sacking attested as modern_synthesis (no primary named by Eger) — ideal to revisit if Tannous 2010 dissertation becomes available or if a primary source for the event surfaces; Dead Cities Tchalenko-vs-Eger interpretation pair (INT-0036/0037 — record IDs may differ post-renumbering, verify) suitable for a Marxist-archaeological reframing later.
- Chapter 2 deferred items (not blocking; revisit when substantive treatment is encountered elsewhere): bare-list ʿawāṣim towns (Dābiq, Tīzīn, Raʿbān, Dulūk, Kaysūm, Sanjah/Bahasnā); ʿAzāz-district villages (Kfar Lahtha, Mannagh, Yabrīn, Arfād, Tubbal, Innib); Qalʿat Jaʿbar / Dawsar / Qalʿat Najm; Tell Wasta, Qaryat al-Thalj, Tishrin Dam tells, Gaziantep mounds, Tell Qabbasin; Dimashq / Ḥimṣ / al-Ruhā / Bira passing mentions; Naṣr al-ʿUqaylī, Saʿīd al-Khayr, ʿUmar I as persons; modern scholars cited but not minted as PersonRecords (Tchalenko, Magness, Harper, Whitcomb, Wilkinson, Algaze, Northedge, van Loon, Bonner, Straughn, Abu Ezzah, Shaban). Coordinate verification for low-confidence sites also outstanding.
- Session 3 deferrals: source-author PersonEntities (al-Baladhuri, Theodoret, Abu al-Fida, Yaqut, Michael the Syrian, Procopius, Evliya Celebi, Nuaym, Ibn Butlan); Istakhri, Malalas, al-Dimashqi, Mustawfi, Muhallabi, Libanius as cited authorities; individual AS/KM survey-site numbers; Tell al-Judaidah, Gindaros, al-Mina, Sabuniye; al-Abbas b. al-Walid I, Marwan II as persons.

## Project layout notes

- Polity records (ENT-POL-NNNN) live in `records/places/`, not in a dedicated `records/polities/` folder.
- `linked_attestations` and `linked_interpretations` are the correct field names for back-references.
- `metadata.review_history` requires `reviewer`, `decision`, and date-time-format `date`. Look up exact accepted values from an existing reviewed record before writing review_history entries programmatically.
- Back-reference script (governance section 4.3) only walks attestations and interpretations as reference sources, only updates entity records (places, persons, events, polities) and only via `linked_attestations`/`linked_interpretations` fields. Source records do not carry back-references (the source field on attestations is unidirectional). Event-to-event and relationship-based back-references not currently auto-applied.

## Project housekeeping

- Synced Claude Project custom instructions with docs/editorial_workflow.md verbatim. Self-test confirmed the new seven-rule wording.
- Session 1 (ch.8): 49 records, 6 entities back-referenced.
- Session 2 (Introduction): 11 records, 6 entities back-referenced including Heraklios merge into ENT-PERS-0016.
- Session 3 (Part 1 intro + Ch. 1, pp. 23-68): 88 records, 3 entities back-referenced (ENT-PLC-0004, 0009, 0010); ATT-0087 orphan fix on ENT-PLC-0020.

## Part 1 milestone (completed)

**Date of completion**: 2026-06-17 (the day's third extraction; sessions 1, 2, 3, 5, 6, 7, 8, 9, 10 across June 2026).

**Material covered**: Eger 2015 Introduction, Part 1 introduction, Chapters 1-5 of Part 1 ("The Syro-Anatolian Thughur"), and Chapter 8 of Part 2 ("The Byzantine Frontier", extracted out of order as the original pilot extension).

**Pages extracted**: 1-126, 158-182, 246-263 (~166 of Eger's 310 pages, ~54% of the book) — but Part 1 is now complete.

**Corpus state after Part 1 + maintenance**:
- Total records: **739**
- Sources: 41
- Persons: 58
- Places (incl. polities): 143
- Events: 30
- Observations: 144
- Attestations: 172
- Interpretations: 71
- Relationships: 80

**Framework entity hubs** (entities matured into busy cross-reference nodes across multiple sessions):
- SRC-0007 Eger 2015 — secondary anchor for the entire run, cited 100+ times across attestations and interpretations
- ENT-PLC-0004 Tarsus — most heavily-linked place; bridges the 838 campaign material (pilot) and the Cilician frontier material (session 10)
- ENT-PLC-0010 Thughur — abstract framework entity now versioned to 1.5+; references across all sessions
- ENT-PLC-0009 ʿAwasim — companion abstract entity; matured through every chapter
- ENT-PLC-0034 Halab (Aleppo) — central node for Central Thughur sessions 5-6
- ENT-PLC-0094 Jazira — minted session 8, immediately load-bearing for sessions 8-9 Jaziran material
- ENT-PERS-0001 al-Mutasim — pilot-corpus dissertation-core hub; activated by Chapter 3 (Zibatra rebuilding)
- ENT-PLC-0007 Zibatra — pilot-corpus 838-trigger entity, activated by Chapter 3 via Eger's fourfold rebuilding event
- ENT-PERS-0018 Harun al-Rashid — cross-sectional figure threading sessions 3, 5, 6, 7, 8, 9, 10
- ENT-PERS-0038 al-Mansur — minted session 7, immediately active across sessions 8-10
- ENT-POL-0003 Umayyad Caliphate — minted in maintenance, back-fills political_affiliation on 14 persons

**Preserved scholarly disputes (rule 1)**:
- Theophanes vs Theophilus on Siffin water-capture attribution (session 5)
- Maslama alone vs Hisham+Maslama on Nahr Maslama builder (session 5)
- Tchalenko olive-monoculture vs Eger revision on Dead Cities (session 6)
- Magness redating vs older 4th-century chronology on Dehes (session 6)
- Eger vs Robinson on Jaziran settlement (Robinson opportunism-and-desperation vs Eger elite-enthusiasm; session 9)
- Three disputed identifications in Cilicia: al-Harunniyya (Duzici vs Orensehir), Hisn Awlas (Karaduvar vs Elaiussa-Sebaste), Hisn Qatraghash (Sariseki Kalesi) — all session 10
- Nahr Said dating contradiction (Umayyad textual vs 9th-century archaeological signature; session 9)

**Tools and workflows matured**:
- `tools/entity_snapshot.py` — per-session corpus entity snapshot for prompt grounding (mitigates Project-knowledge staleness)
- `tools/validate_batch.py` — subschema-targeted pre-validation with relaxed PROV- prefix support (from session 7)
- Auto-discovering renumbering pattern (Python heredoc using regex over PROV- IDs, handling both PROV-PERS-NNN and PROV-ENT-PERS-NNN formats)
- Auto-discovering back-reference pattern (walks attestations/interpretations as reference sources, updates linked_attestations/linked_interpretations on entities, MINOR version bumps per governance §4.3)
- Master prompt template (session 3 onwards, with entity snapshot baked in)
- Page-budget discipline: 15-25 pages per session reliable; >30 pages risks output truncation (proven by chapter 2 full-chapter failure forcing the part-A/part-B split)
- Provenance pattern for modern scholars: scholar/publication text without publication_source_id (no stub SourceRecords for Bartl, Heidemann, Robinson, Tchalenko, Magness, Lyonnet, Meijer, Wilkinson, Lauffray, etc.)

**Schema-bootstrap note**: ENT-POL-0003 Umayyad Caliphate required bootstrapping with ATT-0099 (Muʿāwiya, dynasty founder) to satisfy linked_attestations minItems:1 constraint. Subsequent back-reference passes will accumulate further attestations naturally.

**Outstanding follow-up at Part 1 close**: see Follow-up items section above.

## Master prompt template (session 3 onwards)

Per-session setup:
1. `cd ~/Projects/byzantine-frontier-db && git pull`
2. `python tools/entity_snapshot.py`
3. `cat current_entities.txt` -- copy contents
4. Open new Claude Project conversation
5. Paste template below, substituting bracketed values:

---

I'm extracting records from Eger, A. Asa, *The Islamic-Byzantine Frontier* (London: I.B. Tauris, 2015), [SECTION DESCRIPTION], pp. [START-END]. Both the chapter PDF and the footnotes PDF are attached.

Eger 2015 is already in the corpus as SRC-0007 -- reference it directly; do not draft a new SourceRecord for Eger himself.

CURRENT CORPUS ENTITIES (auto-generated snapshot -- authoritative for entity matching):

[PASTE FULL CONTENTS OF current_entities.txt HERE]

Use the snapshot above to check for entity matches before minting any new entity. If an entity in the chapter matches an existing record by standardised_name or by any alternative_name, reference the existing canonical ID directly; do not mint a new PROV- record for it.

For any new primary source Eger cites which isn't in the snapshot, draft a new PROV-SRC- SourceRecord with what edition information Eger provides; use [citation needed] for missing edition details.

Apply the editorial workflow rules:
1. Primary-source content reached via Eger -> attestation against the primary SourceRecord, citation field records the transmission chain, provenance primary_quotation or primary_paraphrase, Eger page in notes.
2. Eger's interpretive arguments -> InterpretationRecord linked to SRC-0007.
3. Set editorial_review_required: true on every record.
4. Use [citation needed: ...] placeholders for any uncertain reference rather than inventing one.
5. PROV- provisional identifiers for all new records.
6. Per governance, every record needs a SourceRecord -- if Eger cites a new primary not yet in the snapshot, draft a new PROV-SRC- SourceRecord.
7. created_by field on every record must be the bare string "Curtis" — AI-assisted production methodology is documented at the project level in docs/governance.md §2, not per-record.

Produce all records as a single YAML list. End with a summary noting record counts by type, cross-corpus links to existing entities (by canonical ID from snapshot), items deferred, and any unresolved disagreements.


## High-priority follow-up: Umayyad polity gap

Across sessions 7-10, the corpus has accumulated multiple records whose `political_affiliation` was omitted because no Umayyad polity entity exists in the schema (ENT-POL-0001 Byzantine, ENT-POL-0002 Abbasid only). Affected persons include: Marwān II (ENT-PERS-0043), Yazīd II (0044), ʿAbd al-Malik (0045), ʿUbayd Allāh ibn ʿAbd al-Malik (0046), Sulaymān ibn ʿAbd al-Malik (0035), Maslama (0025), Hishām (0019), al-Walīd I (0056), al-Walīd II (0057), ʿUmar II (0055), Yazīd I (0059), and others. Recommended action: mint **ENT-POL-0003 Umayyad Caliphate** in a dedicated maintenance session, then run a back-fill script to populate `political_affiliation` on all Umayyad-era PersonRecords. Note this should be done before any extraction that adds significant new Umayyad material (none expected in Eger's remaining chapters but worth doing soon for corpus consistency).
