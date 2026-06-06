# Dating Systems — Methods Note

## Byzantine-Islamic Frontier Database

**Version:** 1.0.0
**Data file:** `dating_systems_v1.json`
**Specification reference:** §7 (Temporal Framework), Appendix C §C.11 item 4

---

## 1. The problem

The database covers a region and a period in which sources use at least five distinct chronological systems concurrently:

- **Julian / Anno Domini** in some Greek and almost all modern sources.
- **Anno Mundi (Byzantine)**, beginning 1 September 5509 BCE, in the principal Byzantine chronicles.
- **Anno Hegirae**, a purely lunar calendar of approximately 354.367 days per year, beginning 16 July 622 CE, in all Arabic sources.
- **Roman/Byzantine indiction**, a fifteen-year cycle of fiscal reckoning, common in Byzantine documentary practice and occasional in chronicles.
- **Regnal years**, attached to named emperors or caliphs, in both source traditions.

For the Battle of Anzen on 22 July 838 CE, all five systems describe the same day from different angles:

| System | Designation |
|---|---|
| Julian | 22 July 838 CE |
| Anno Mundi (Byzantine) | AM 6346, indiction 1 |
| Anno Hegirae | 29 Rabīʿ II AH 223 |
| Indiction alone | 1 (1 Sept 837 – 31 Aug 838) |
| Byzantine regnal | year 10 of Theophilos |
| Abbasid regnal | year 6 of al-Muʿtaṣim |

Reconciling these is unavoidable for any database that aspires to cross-tradition analysis. The conversion is mathematically straightforward; the subtleties are editorial.

## 2. The primary timeline

The database stores dates against a single canonical timeline: the **proleptic Julian calendar with CE numbering**. Every other dating system converts into this. Two consequences follow:

First, the Julian calendar — not the Gregorian — is canonical. This reflects the calendar actually in use during the period covered. Gregorian conversion is computed only when needed for display and is never stored as a primary value. The choice of Julian over Gregorian is documented here so that consumers of the database who expect Gregorian dates can convert as needed.

Second, every `TemporalValue` in the database carries a `precision` and a `confidence`, and these reflect the conversion uncertainty as well as the source uncertainty. An AH year converts to a Julian range; the resulting `TemporalValue` therefore has `precision: year_range_narrow` at best, even if the source itself states only the AH year with high confidence.

## 3. AH conversion: the canonical algorithm

The project uses the **Type I tabular Islamic calendar** (the al-Khwārizmī variant): a 30-year cycle with leap years at positions 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, and 29.

The Julian Day Number for the first day of an AH year is:

```
JDN(1 Muharram AH n) = 1948440 + 354 × (n - 1) + floor((11n + 3) / 30)
```

This anchor matches the convention that 1 Muharram AH 1 = Friday 16 July 622 CE (Julian). The corresponding JDN is 1948440.

For an arbitrary day in the Islamic calendar, the JDN is the year-start JDN plus the cumulative day count for that month within the year. Conversion to Julian CE proceeds by the standard JDN-to-date algorithm. The project's reference implementation must produce, for the worked examples in `dating_systems_v1.json`, the exact Julian dates documented there.

### 3.1 The boundary problem

An AH year never aligns with a Julian year, and the misalignment is approximately 11 days per year. **AH 223 = 4 December 837 CE – 22 November 838 CE.** An event al-Ṭabarī assigns to AH 223 may therefore have occurred anywhere in approximately a Julian year, straddling two Julian years.

This is the most common source of error in cross-tradition chronology. The database addresses it by an explicit rule:

> When a source provides only an AH year, the corresponding `TemporalValue` carries the full Julian range as `start` and `end`, with `precision: year_range_narrow`. Editorial narrowing to a Julian sub-range requires an additional attestation that supplies the supplementary information (month, season, regnal year, indiction, or correlation with a Julian-dated event).

The siege of Amorium illustrates: al-Ṭabarī's AH 223 entry alone places the siege somewhere between 4 December 837 and 22 November 838. Theophanes Continuatus's AM 6346 entry narrows the range to 1 September 837 – 31 August 838. Combining the two yields 4 December 837 – 31 August 838, an approximate nine-month window. The 22 July battle date for Anzen comes from the explicit day-numbered Greek tradition; the August timing of the siege itself is derived by working forward from there.

### 3.2 Variant calendars

Type I is the project's default. Sources that demonstrably use a different variant (Type II–IV, or observational variants) require an editorial flag on the relevant attestation. Variant detection is an editorial judgement, not an automatic conversion.

## 4. Byzantine AM conversion

The Byzantine Anno Mundi era begins 1 September 5509 BCE (proleptic Julian). The Byzantine year begins on 1 September, the indictional new year. The conversion is therefore split:

- For dates from **1 September to 31 December**: `AD = AM - 5508`
- For dates from **1 January to 31 August**: `AD = AM - 5509`

An AM year always overlaps two AD years. AM 6346 = 1 September 837 to 31 August 838.

When a source provides only an AM year, the `TemporalValue` carries the full split-Julian range, again at `year_range_narrow` precision.

The Alexandrian AM (epoch 25 March 5493 BCE) is a separate system used in some Greek chronographic traditions (notably George Syncellus). The project tags it as `AM_alexandrian` and stores it distinctly; confusion between Byzantine and Alexandrian AM is a known source of error in modern scholarship and the project does not propagate it.

## 5. Indiction

Indictions are a 15-year fiscal cycle. For a Byzantine date in CE year y after 1 September:

```
indiction = ((y + 3 + 312) mod 15) + 1
```

For Byzantine reckoning (1 September new year), an indiction of *n* in (say) the ninth century is consistent with multiple Julian years differing by 15. Indiction alone is therefore insufficient; the database records indictions as a `DatingValue` alongside whatever supplementary information is available. The resulting `TemporalValue` carries `precision: year_range_broad` until disambiguated by cross-reference.

## 6. Regnal years

Regnal years are reign-specific. The project maintains lookup tables for the principal Byzantine and Abbasid rulers of the period (see `reign_table_byzantine` and `caliph_table_abbasid` in `dating_systems_v1.json`). For each named ruler:

- The accession date (start of regnal year 1) is recorded in both AH (where applicable) and Julian.
- Regnal year *n* corresponds to the *n*-th anniversary of accession.
- Where multiple conventions exist (reckoning from coronation rather than accession, or from the start of the calendar year following accession), the project's default is **accession-anniversary reckoning** unless the source clearly uses an alternative.

The convention used for each named ruler is documented in the lookup table.

## 7. Editorial rules for cross-system dates

The following rules govern how attestations carrying dates from multiple systems are reconciled:

1. **Native form preserved.** Every `Attestation` records the date in the source's native form (e.g. "AH 223", "Theophilos year 10") as a `DatingValue`. The native form is never overwritten.
2. **Normalised range computed.** A normalised Julian range is computed from the native form and stored on the parent `Event` or `Place` record's `TemporalValue`, with appropriate `precision`.
3. **Multi-system corroboration.** When multiple attestations supply dates in different systems and the converted ranges intersect, the intersection is the editorial best estimate. The individual native datings remain visible at the attestation level.
4. **Multi-system contradiction.** When the converted ranges from different systems do not intersect, the contradiction is flagged. The database does not silently resolve it. An editorial note records the contradiction and the principal hypothesis (typically: which source is using a non-default variant, or which conversion involves a known correction).
5. **Conversion confidence.** The `confidence` of a converted Julian range is at most the minimum of the source confidence and the conversion confidence. If a source attests "AH 223" with confidence 5, but the conversion produces a 354-day range, the resulting Julian-range confidence remains 5 because the conversion is exact within its precision.

## 8. Implementation requirements

A reference implementation must:

1. Convert AH year *n* to its Julian start and end dates, exactly matching the worked examples in `dating_systems_v1.json`.
2. Convert AM (Byzantine) year *m* to its split Julian range (1 September of (m-5509) to 31 August of (m-5508)).
3. Resolve indiction *i* + decade *d* to the unique Julian range in that decade.
4. Compute regnal year *r* of ruler R from the lookup table.
5. Compute the indiction for a given Julian date, for round-tripping.
6. Pass all four cases in `worked_examples`.

The project does not mandate a specific implementation language; the canonical test cases in `dating_systems_v1.json` are the correctness criterion.

## 9. Open issues

Four matters are documented in `open_issues` and remain for editorial resolution:

- **AH leap-year variants.** The Type I default is correct for the vast majority of historiographical sources but not for all. Detecting Type II–IV usage in a source is an editorial judgement.
- **Indictional reckoning variants.** Bedan / Caesarean indictions exist and differ from Byzantine indictions. The project uses Byzantine reckoning by default.
- **Regnal year reckoning conventions.** Accession-anniversary is the default; departures are documented per ruler.
- **Post-quem and ante-quem.** Relative dates (`relative_after`, `relative_before`, `relative_between`) do not produce a Julian range at conversion time; the database stores the relation and the consumer computes the range when needed.

These are not blockers for v1.0. They are flagged here so that they receive explicit editorial attention rather than being silently absorbed into the conversion code.

## 10. Citation

When citing this methods note or the accompanying conversion data, please cite:

> Byzantine-Islamic Frontier Database, "Dating Systems Reference Data v1.0.0," `dating_systems_v1.json` and `dating_systems_methods.md`, 2026.

The conversions follow Reingold and Dershowitz, *Calendrical Calculations: The Ultimate Edition* (Cambridge, 2018), with anchor dates verified against Grumel, *La Chronologie* (Paris, 1958) and Bosworth, *The New Islamic Dynasties* (Edinburgh, 1996).
