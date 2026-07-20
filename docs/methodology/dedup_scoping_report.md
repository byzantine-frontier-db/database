# Primary-Source Dedup — Scoping Report (Item F)

**Read-only pass. No records changed.** Corpus at 1453 records, 1246 attestations.

## Headline

The dedup problem is **far smaller than the raw counts suggest, and mostly illusory.** Of 203
(entity, source) pairs with ≥2 attestations, the flagged Phase-1/Phase-2 overlap accounts for only
**11 cases**, and on inspection **almost none are redundant** — the Phase-2 (Eger-2008-gazetteer)
attestations overwhelmingly record *different data* than the Phase-1 (Eger-2015) ones. The "duplication"
is the same *primary source* cited for *different facts* through two different Eger works. Expected
remediation is a **single ~2–3 hour pass** that mostly **adds cross-reference notes**, with perhaps
one genuine consolidation.

---

## 1. Diagnostic

1246 attestations → 753 (entity, source) pairs → **203 pairs with ≥2 attestations**. But the ≥2 count
is dominated by two non-problems:

- **SRC-0007 (Eger 2015), 114 entities** — a *modern-synthesis* source; multiple synthesis
  attestations per entity are different facets of Eger's argument, by design. Not a dedup target.
- **SRC-0065 (Eger 2008 gazetteer), 23 entities** — the Phase-2 extraction source; the ≥2 is the
  `gis_derived_observation` (coordinate) + `primary_observation` (autopsy) pair. Different evidential
  roles. Not a dedup target.

Filtering to **primary sources** and to the true overlap signature — a **Phase-1 direct citation**
*and* a **Phase-2 "reached via Eger 2008" citation** on the same (entity, source) — yields the whole
problem set:

| Primary source | Entities w/ ≥2 | **P1+P2 split cases** (the overlap) |
|---|---|---|
| SRC-0016 al-Balādhurī | 16 | **4** — ENT-PLC-0016, -0043, -0063, -0118 |
| SRC-0009 Ibn Ḥawqal | 6 | **4** — ENT-PLC-0004, -0070, -0073, -0074 |
| SRC-0023 Ibn Shaddād | 3 | **1** — ENT-PLC-0073 |
| SRC-0008 al-Yaʿqūbī (Buldān) | 1 | **1** — ENT-PLC-0016 |
| SRC-0010 Ibn Khurradādhbih | 1 | **1** — ENT-PLC-0072 |
| SRC-0001 al-Ṭabarī | 20 | **0** (never a Phase-2 gazetteer source) |
| SRC-0020 Yāqūt, others | 1–2 | 0 |

**11 P1+P2 split cases total.** The 20 al-Ṭabarī multi-att entities and the non-split Balādhurī
groups are intra-Phase-1 — multiple *distinct* primary claims sharing a source, not the flagged
overlap (a separate, lower-priority question addressed in §3).

---

## 2. Deep-dive (8 cases)

Classification: **R** = redundant (same claim), **C** = complementary (different aspect of one
claim), **I** = independent (different claims, shared source).

**① Malaṭya / Balādhurī [Session-4 flag] — I.** ATT-0152 + ATT-0299 (P1) are both *settlement*
(al-Manṣūr's 4,000 Jaziran fighters); ATT-0412 (P2) is the *conquest* (ʿIyāḍ b. Ghanm under ʿUmar I).
The P2 attestation is a **different event**, not a duplicate. ATT-0152 vs ATT-0299 (both P1) are the
closest thing to redundancy in the whole set — same settlement theme — but 0299 is a `primary_quotation`
with the specific 4,000 figure and a different edition/page than 0152's paraphrase. → the one **C→possible-R**
consolidation candidate; the P2 att is I.

**② Al-Maṣṣīṣa / Balādhurī [Session-5 flag] — I.** ATT-0323 (P1) is marsh-population resettlement
(Zuṭṭ/Sayābija, a 9-entity list); ATT-0426 (P2) is al-Manṣūr's post-earthquake *rebuild* of al-Maṣṣīṣa.
Different facts. Retain both.

**③ Manbij / Balādhurī — I/C.** ATT-0126 (P1) is a **toponym-list** mention (Manbij among Tīzīn,
Qūrus, Anṭākiya…); ATT-0417 (P2) is the *conquest* (ʿIyāḍ b. al-Ghanm subdued the Euphrates villages).
List-membership vs conquest event. Retain both.

**④ Qūrus / Balādhurī — I.** Three *different* Balādhurī data: ATT-0126 (list mention), ATT-0311
(Slav settlement under Muʿāwiya/ʿAbd al-Malik), ATT-0442 (Abū ʿUbayda's conquest of the province).
All independent. Retain all.

**⑤ Sumaysāṭ / Ibn Ḥawqal — C.** ATT-0127 (P1) is a **list** ("lists only Balis, Sanjah, Sumaysāṭ");
ATT-0470 (P2) is a **description** (small Euphrates city, irrigation, fortress). Same source, list vs
description — complementary. Foldable (list-mention → note on the description) but valid as-is.

**⑥ Malaṭya / Yaʿqūbī-Buldān — I.** ATT-0051 (P1) is geographic (border districts of fortresses;
Malaṭya ringed by mountains); ATT-0413 (P2, via Ibn Shaddād) is administrative (seven tribal quarters).
Different claims *and* different transmission chains. Retain both.

**⑦ Ṭarsūs / Ibn Ḥawqal — I.** ATT-0187 (P1) is Ibn Ḥawqal's **map** (Cilician rivers, riverine
settlements); ATT-0491 (P2) is his **city description** (Early Islamic vs Byzantine-held Ṭarsūs,
garrison). Map-geography vs city-description. Retain both.

**⑧ al-Jūma / Ibn Khurradādhbih — C.** ATT-0124 (P1) is ʿawāṣim **list membership**; ATT-0397 (P2)
adds the **specific location** (hill over the Amuq, south of Qūrus). Complementary. Foldable but valid.

**Tally of the 8:** Redundant 0 · Complementary 3 (⑤ ⑧ and the 0152/0299 half of ①) · Independent 5.

**Transmission-chain pattern that explains it all:** P1 attestations are routed *via Eger 2015*
(his interpretive monograph, which cites primaries in **thematic lists** — settlement waves, ʿawāṣim
rosters, toponym strings). P2 attestations are routed *via Eger 2008* (the **site-by-site gazetteer**,
which cites the same primaries for **place-specific** conquest/description data). Two different secondary
routes to one primary, carrying different payloads. That is why they coexist rather than duplicate.

---

## 3. Proposed methodology

**Merge (delete one, keep the other) — only when all three hold:** same source **and** same entity
**and** the same specific claim (same event/datum), **and** the same or compatible transmission chain.
On the evidence above this is **rare-to-nonexistent** in the P1/P2 set. Apply only after reading both
paraphrases in full; never merge on source-match alone.

**Retain-both (default) — when any of:** different claim (conquest vs settlement vs description),
different aspect (list-membership vs full description), or different transmission chain (direct vs
via-Ibn-Shaddād). This covers ~8 of the 11 cases. Optionally add a reciprocal `cross-reference` note so
a reader sees both are the same source at different granularity.

**Edit-not-delete (fold) — for complementary list/description pairs (⑤, ⑧):** keep the richer
attestation; fold the thin list-mention's unique detail into its notes and **de-link the thin one from
the entity** *only if* it carries no independent page/edition value. Because these thin mentions cite
their own Eger-2015 page, the safer default is **retain-both + cross-ref**, reserving folding for cases
where the list-mention adds nothing the description doesn't.

**Never delete across a transmission boundary.** A "reached via Eger 2008" and a "via Eger 2015"
attestation encode *which Eger work* surfaced the datum — provenance information worth keeping even when
the underlying claim is close (cf. rule 4). Consolidate the *claim*, never the *provenance trail*.

**Ordering:** (a) the two originally-flagged entities first — Malaṭya (ENT-PLC-0016), Al-Maṣṣīṣa
(ENT-PLC-0118) — to close the Session-4/5 flags; (b) the remaining Balādhurī splits (-0043, -0063);
(c) the Ibn Ḥawqal / Ibn Shaddād / Yaʿqūbī / Ibn Khurradādhbih splits; (d) a *separate, optional*
secondary sweep of the intra-Phase-1 multi-att groups (esp. the one true-consolidation candidate,
ATT-0152 vs ATT-0299 on Malaṭya, and the al-Ṭabarī groups) to confirm they are independent claims.

---

## 4. Scope estimate

- **Likely-duplicate (true merge) cases corpus-wide:** ~**0–1** (only the ATT-0152/0299 Malaṭya
  settlement pair is even a candidate, and that is a consolidation, not a clean dup).
- **Complementary fold-or-cross-ref cases:** ~**3–4** (⑤, ⑧, and possibly the ①/④ list-mentions).
- **Independent, no action beyond an optional cross-ref note:** the remaining ~**7**.
- **Intra-Phase-1 secondary sweep** (Ṭabarī ×20 + non-split Balādhurī): a separate scoping micro-pass;
  expected to confirm independence, low duplicate yield.

**Effort:** one **~2–3 hour session**, single pass — the set is small enough (11 cases) that
session-by-session or source-by-source slicing would add overhead without benefit. Deliverable would be
one small patch: mostly reciprocal cross-reference notes (PATCH bumps), at most one consolidation
(a MAJOR on the surviving attestation + de-link).

**Recommendation:** this is closer to a **cross-reference-and-confirm** pass than a dedup. The corpus's
evidential-separation discipline (attest each datum, keep provenance trails) already prevented real
duplication; the Session-4/5 flags were appropriately cautious but, on inspection, the attestations they
worried about are carrying different freight. I'd suggest doing it as one session, leading with the two
flagged entities so the original flags are formally closed, and treating "retain-both + cross-ref" as the
default outcome rather than merging.
