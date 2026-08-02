# Working Migration Scope — Logical-Model Phase

**Status:** working scope for the logical-model phase. **Subordinate to the frozen `conceptual_ontology.md` (v0.2).** This file captures reconciliations settled during Step 1 so they survive outside the working session. It makes **no claim about the frozen ontology and proposes no change to §17**; it records how §17's own figures fit together and how its two numbering namespaces relate. **Amendable without governance §5.8**, since it is neither a frozen document nor a rule.

**Source:** all figures below are §17 of the frozen ontology, cited but not restated. Where a derivation is given, it composes §17's own numbers; it introduces none.

---

## 1. The dedup identity, stated explicitly

Recorded so no reader re-derives it. All quantities are §17.1's.

> **1,423** nominal record-migrations collapse to **1,157** distinct records.
> The gap is **266 duplicate touches** — a record migrated under more than one migration unit — of which **264 fall on the 190 place records**.
>
> **1,157** distinct content-migrated records **+ 296** residual-sweep-only records (a `schema_version` bump only, no content change) **= 1,453**, the full corpus.

Two figures in §17.1 count different things and must not be differenced against each other:

- **1,423** counts *nominal content-migrations* — every (record, migration-unit) pairing. A record touched by three migration units contributes three.
- **1,157** counts *distinct content-migrated records*. The same record contributes once.
- **1,453** is the *whole corpus*: the 1,157 content-migrated records plus the 296 that receive only a mechanical version bump.

There is no clean `1,453 − 1,423 = 30` relationship, and no such relationship is intended: the two numbers live in different namespaces (nominal touches vs distinct records), and 266 of the 1,423 are duplicate touches. The only identity that holds is **1,157 + 296 = 1,453**.

---

## 2. Two-namespace sequencing convention

§17 uses two numbering systems for two different purposes. They are not aligned one-to-one, and reading one as the other is the error this section prevents.

- **M-labels (§17.2)** identify migration *content*: M1–M8, each a distinct transformation with its own record count. **They are content identifiers, not an execution order.**
- **Step-numbers (§17.6)** order *execution*: steps 0–9. **Step 5 sequences commits by these.**

Several M-units execute within one step; some steps execute no M-unit (they are prerequisites or net-new construction). The mapping is many-to-one from M-units into steps, and it is **quoted verbatim from §17.6 below**, not reconstructed:

| Step (§17.6) | Work, as §17.6 states it | M-units executed | Records |
|---|---|---|---|
| **0** | Ratify and document rules 9, 10, 11, 14, 15 in `editorial_workflow.md` | none (prerequisite) | 0 |
| **1** | Schema v3 + validators for I2, I3, I5, I5a, I5b, I11 | none (checks-first) | 0 |
| **2** | **M1 rename**, alone | **M1** | 537 |
| **3** | **Place pass**: M4 + M5 + M7 + M3(places) + name field + schema migration | **M4, M5, M7, M3 (places portion)** | 190 |
| **4** | **Person/Event pass**: M3 + schema migration | **M3 (persons+events portion)** | 135 |
| **5** | **Attestation pass**: M2 + reference mode + polarity + schema migration | **M2** | 477 |
| **6** | **Interpretation pass**: rule-9 back-fill + rule-10 promotion + unbundling + schema migration | **M6** | 74 |
| **7** | **Relationship pass**: `contains` narrowing + vocabulary extension + new relationships from step 6 | **M8** | 27 + ~29 new |
| **8** | **Residual schema sweep**: 79 sources + 117 relationships + 100 interpretations | none (version bump only) | 296 |
| **9** | **Net-new construction**: Phase, Component, examination Events | none (not a migration) | — |

Two consequences worth stating, both derived from the table above:

- **M3 is split across steps 3 and 4.** The 325-record `overall_confidence` retirement executes in two passes — its 190 places in step 3, its 81 persons + 54 events in step 4 — because those record sets are opened for other reasons in different steps. "M3 = 325" is correct as a content total and never executes as one commit.
- **"M8" (§17.2, `contains` narrowing, 27 records) and "step 8" (§17.6, residual sweep, 296 records) denote different things.** They are not a mislabelling; they are one number in each of two namespaces. M8 executes in **step 7**.

---

## 3. M6 = 74 — provisional, pending a Step-5 record-level read

§17.2 gives M6 as a set union:

> rule-9 back-fill (57) ∪ rule-10 promotion (29) ∪ dossier unbundling (4)

The **disjoint sum is 57 + 29 + 4 = 90**; the stated **74** implies a **16-record overlap** — interpretations that are simultaneously targets of more than one of the three operations (e.g. an interpretation that is both a rule-9 back-fill target and a rule-10 promotion source is counted once in 74 but twice in 90).

**The 74 is a union figure and is marked provisional.** Confirming the 16-record overlap requires a record-level read of the 174 interpretations, which belongs at **Step 5** (the read-only scoping sweep that precedes the interpretation pass), not here. **Flagged, not resolved.** M6 stands at 74 as §17.2 states it, pending that read.

---

*End of working scope notes. Subordinate to the frozen ontology; amendable without §5.8.*
