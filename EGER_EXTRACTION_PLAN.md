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
| 7 | Ch. 3 Eastern Thughur (NE Anatolia, dissertation core) | 102-126 | pending | | | |
| 8 | Ch. 4 part A (Balikh) | 127-142 | pending | | | |
| 9 | Ch. 4 part B (Khabur) | 143-157 | pending | | | |
| 10 | Ch. 5 Western Thughur (Cilicia) | 158-182 | pending | | | |
| 11 | Part 2 intro + Ch. 6 (Late Roman prologue) | 183-197 | pending | | | |
| 12 | Ch. 7 part A (Hydraulic Villages) | 198-220 | pending | | | |
| 13 | Ch. 7 part B | 221-245 | pending | | | |
| 14 | Ch. 9 Epilogue (Middle Byzantine castles, dissertation period) | 264-276 | pending | | | |
| 15 | Ch. 10 part A (Frontier interaction) | 277-293 | pending | | | |
| 16 | Ch. 10 part B | 294-309 | pending | | | |
| 17 | Conclusions | 310-end | pending | | | |

## Follow-up items (across chapters)

- ATT-0058 (salt-mines): verified per Option 1 verification session.
- INT-0012 (Cappadocian elite acculturation): split Ball 2005 dissent into separate attestation against new Ball SourceRecord.
- ATT-0061 (Heraklios speech): confirm SUNY al-Tabari vol. XI translator (Blankinship?).
- Sis-departure dating contradiction (Ibn Shaddad 711-12 vs Baladhuri after al-Waqidi 808-9): create two primary SourceRecords + Interpretation per governance section 5.4.
- Deferred from ch.8: Hisn Hiraqla, Lu'lu'a, Safsaf forts; c.831 al-Matmura raid; Kibyrrhaiōtōn maritime theme; Michael Maleinos; Pseudo-Jahiz, Ibn al-Faqih, Ibn al-Adim corroborating sources; Selime-Yaprakhisar, Canli Kilise, Acik Saray, Gumuskoy/B16 archaeological sites.

## Project layout notes

- Polity records (ENT-POL-NNNN) live in `records/places/`, not in a dedicated `records/polities/` folder.

cd ~/Projects/byzantine-frontier-db
cat > EGER_EXTRACTION_PLAN.md << 'EOF'
# Eger 2015 extraction plan

Source: Eger, A. Asa. *The Islamic-Byzantine Frontier: Interaction and Exchange among Muslim and Christian Communities*. London and New York: I.B. Tauris, 2015. (SRC-0007 in corpus)

Order: sequential (with chapter 8 done out of order)
Target pace: one session per day

## Session tracker

| # | Material | Pages | Status | Records | Commit | Verified |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ch. 8 Byzantine Frontier | 246-263 | EXTRACTED | 49 | fa2b5cd | ATT-0058 only |
| 2 | Introduction | 1-22 | EXTRACTED | | | |
| 3 | Part 1 intro + Ch. 1 (full) | 23-68 | EXTRACTED | 88 | 62a7c35 | pending |
| 4 | (subsumed into session 3) | - | MERGED | - | - | - |
| 5 | Ch. 2 part A | 69-85 | pending | | | |
| 6 | Ch. 2 part B | 86-101 | pending | | | |
| 7 | Ch. 3 Eastern Thughur (NE Anatolia, dissertation core) | 102-126 | pending | | | |
| 8 | Ch. 4 part A (Balikh) | 127-142 | pending | | | |
| 9 | Ch. 4 part B (Khabur) | 143-157 | pending | | | |
| 10 | Ch. 5 Western Thughur (Cilicia) | 158-182 | pending | | | |
| 11 | Part 2 intro + Ch. 6 (Late Roman prologue) | 183-197 | pending | | | |
| 12 | Ch. 7 part A (Hydraulic Villages) | 198-220 | pending | | | |
| 13 | Ch. 7 part B | 221-245 | pending | | | |
| 14 | Ch. 9 Epilogue (Middle Byzantine castles, dissertation period) | 264-276 | pending | | | |
| 15 | Ch. 10 part A (Frontier interaction) | 277-293 | pending | | | |
| 16 | Ch. 10 part B | 294-309 | pending | | | |
| 17 | Conclusions | 310-end | pending | | | |

## Follow-up items (across chapters)

- ATT-0058 (salt-mines): verified per Option 1 verification session.
- INT-0012 (Cappadocian elite acculturation): split Ball 2005 dissent into separate attestation against new Ball SourceRecord.
- ATT-0061 (Heraklios speech): confirm SUNY al-Tabari vol. XI translator (Blankinship?).
- Sis-departure dating contradiction (Ibn Shaddad 711-12 vs Baladhuri after al-Waqidi 808-9): create two primary SourceRecords + Interpretation per governance section 5.4.
- Deferred from ch.8: Hisn Hiraqla, Lu'lu'a, Safsaf forts; c.831 al-Matmura raid; Kibyrrhaiōtōn maritime theme; Michael Maleinos; Pseudo-Jahiz, Ibn al-Faqih, Ibn al-Adim corroborating sources; Selime-Yaprakhisar, Canli Kilise, Acik Saray, Gumuskoy/B16 archaeological sites.

## Project layout notes

- Polity records (ENT-POL-NNNN) live in `records/places/`, not in a dedicated `records/polities/` folder.
- `linked_attestations` and `linked_interpretations` are the correct field names for back-references.
- `metadata.review_history` requires `reviewer`, `decision`, and date-time-format `date`. Look up exact accepted values from an existing reviewed record before writing review_history entries programmatically.

## Project housekeeping

- Synced Claude Project custom instructions with docs/editorial_workflow.md verbatim. Self-test confirmed the new seven-rule wording.

## Master prompt template (session 3 onwards)

Per-session setup:
1. `cd ~/Projects/byzantine-frontier-db && git pull`
2. `python tools/entity_snapshot.py`
3. `cat current_entities.txt` — copy contents
4. Open new Claude Project conversation
5. Paste template below, substituting bracketed values:

---

I'm extracting records from Eger, A. Asa, *The Islamic-Byzantine Frontier* (London: I.B. Tauris, 2015), [SECTION DESCRIPTION], pp. [START-END]. Both the chapter PDF and the footnotes PDF are attached.

Eger 2015 is already in the corpus as SRC-0007 — reference it directly; do not draft a new SourceRecord for Eger himself.

CURRENT CORPUS ENTITIES (auto-generated snapshot — authoritative for entity matching):

[PASTE FULL CONTENTS OF current_entities.txt HERE]

Use the snapshot above to check for entity matches before minting any new entity. If an entity in the chapter matches an existing record by standardised_name or by any alternative_name, reference the existing canonical ID directly; do not mint a new PROV- record for it.

For any new primary source Eger cites which isn't in the snapshot, draft a new PROV-SRC- SourceRecord with what edition information Eger provides; use [citation needed] for missing edition details.

Apply the editorial workflow rules:
1. Primary-source content reached via Eger → attestation against the primary SourceRecord, citation field records the transmission chain, provenance primary_quotation or primary_paraphrase, Eger page in notes.
2. Eger's interpretive arguments → InterpretationRecord linked to SRC-0007.
3. Set editorial_review_required: true on every record.
4. Use [citation needed: ...] placeholders for any uncertain reference rather than inventing one.
5. PROV- provisional identifiers for all new records.
6. Per governance, every record needs a SourceRecord — if Eger cites a new primary not yet in the snapshot, draft a new PROV-SRC- SourceRecord.

Produce all records as a single YAML list. End with a summary noting record counts by type, cross-corpus links to existing entities (by canonical ID from snapshot), items deferred, and any unresolved disagreements.
