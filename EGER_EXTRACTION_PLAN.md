# Eger 2015 extraction plan

Source: Eger, A. Asa. *The Islamic-Byzantine Frontier: Interaction and Exchange among Muslim and Christian Communities*. London and New York: I.B. Tauris, 2015. (SRC-0007 in corpus)

Order: sequential (with chapter 8 done out of order)
Target pace: one session per day

## Session tracker

| # | Material | Pages | Status | Records | Commit | Verified |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ch. 8 Byzantine Frontier | 246-263 | EXTRACTED | 49 | fa2b5cd | ATT-0058 only |
| 2 | Introduction | 1-22 | pending | | | |
| 3 | Part 1 intro + Ch. 1 part A | 23-50 | pending | | | |
| 4 | Ch. 1 part B | 51-68 | pending | | | |
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
| 2 | Introduction | 1-22 | pending | | | |
| 3 | Part 1 intro + Ch. 1 part A | 23-50 | pending | | | |
| 4 | Ch. 1 part B | 51-68 | pending | | | |
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
