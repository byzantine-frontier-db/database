# Dedup Micro-Sweep (intra-Phase-1) — Report (Item F, part 2)

**Read-only. No records changed.** Follows the Item-F scoping report.

## Result in one line

The dedup hypothesis is **confirmed** — the al-Ṭabarī and non-split Balādhurī multi-attestation groups
are all **independent claims or complementary facets, with zero redundancy.** But the sweep surfaced a
**separate, substantive issue unrelated to dedup**: a contiguous block of **22 attestations
(ATT-0218–ATT-0239)** whose evidential claim sits in `notes` with a null `paraphrase` — a rule-8
placement violation the validators don't catch (the field is schema-nullable).

---

## 1. Dedup confirmation

**al-Ṭabarī (SRC-0001), 20 multi-att entities — all independent.** Every group is distinct events
sharing al-Ṭabarī as source: the Amorium campaign (ATT-0001), the Zuṭṭ "frogs" revolt (ATT-0324),
Heraklios's retreat with the fortress populations (ATT-0065), al-Muʿtaḍid's 900 itinerary (ATT-0116),
the Ancyra capture vs its refugees (ATT-0030 vs ATT-0058), and so on. Where one attestation recurs
across several entities (e.g. ATT-0116 across ENT-PLC-0034/-0037/-0050) it is a single multi-entity
attestation, correctly linked — not a duplicate. **No merge candidates.**

**Balādhurī (SRC-0016), non-split groups — independent, with a few complementary facets.** Distinct
data throughout (Muʿāwiya's Persian resettlement of Anṭākiya; the Jarājima; the Slav settlements;
al-Manṣūr's 4,000 Jaziran fighters; Būqā built by Hishām). The only *complementary* pairs — same event,
two facets — are:
- **Maslama's Balis canal:** ATT-0243 (the villagers' petition) + ATT-0097 (its construction),
  recurring on ENT-PERS-0025, ENT-PLC-0037, ENT-PLC-0045, ENT-POL-0003.
- **The Zuṭṭ/Sayābija:** ATT-0322 (their Indian/Sindī origin) + ATT-0323 (their frontier settlement),
  on ENT-PLC-0173.

Both are retain-both-with-optional-cross-ref, exactly like the three pairs in the scoping report —
not merges. So the corpus-wide "complementary, cross-ref-worthy" set grows from 3 to ~5, and the
**true-merge count stays at ~0–1** (still only the ATT-0152/0299 Malaṭya settlement pair).

**Scholarship note (endorsed):** this is the substantive result — the evidential-separation discipline
(rule 3) didn't merely "work," it captured the *right granularity*. Each Balādhurī or Ṭabarī citation
was attested at the level of the individual datum, so the same source naturally carries many
non-overlapping attestations per entity without collision. Duplication was structurally prevented, not
cleaned up after the fact.

---

## 2. New finding (NOT dedup): 22 attestations with the claim in `notes`

Scanning corpus-wide for attestations with **both** `paraphrase` and `direct_quotation` null:

**22 attestations, all in the contiguous block ATT-0218 – ATT-0239**, each with the evidential claim
written into `notes` instead. Split 15 `primary_paraphrase` / 7 `modern_synthesis`. Examples:
- **ATT-0223** (al-Ṭabarī): claim ("Hishām's money-generating estate at Dawrīn…") is in notes; paraphrase null.
- **ATT-0236** (Balādhurī): claim ("ʿIyāḍ ibn Ghanm left Raqqa's land with its established farmers…") in notes; paraphrase null.

**Why it matters:** rule 8 requires the claim in `paraphrase`/`direct_quotation`, never only `notes`.
The distinction is not cosmetic — `paraphrase` is the evidential payload (what the source asserts);
`notes` is editorial metadata. Collapsing them means the payload isn't where consumers, exports, or a
rule-8 check expect it. The validators pass only because the schema leaves `paraphrase` nullable, so
this is invisible to the current tooling — a **gap worth a validator rule** (`primary_*` provenance ⇒
non-null `paraphrase`/`direct_quotation`).

**Why it's a Phase-1 block:** the contiguous ID range (0218–0239) points to a single early extraction
batch that put content in notes before the rule-8 convention was firmly in place. It is unrelated to
the Balādhurī/Phase-2 overlap that Item F was scoped around.

---

## 3. Recommendation / re-scope

- **Item F (dedup) can close** on the scoping report + this confirmation. The genuine dedup surface is
  ~0–1 merges and ~5 optional complementary cross-refs (Malaṭya ATT-0152/0299 aside). Executing the
  cross-reference notes remains a small, opportunistic patch whenever you want it.
- **New item (suggest "Item G — rule-8 back-fill"):** move the claim from `notes` into `paraphrase`
  for the 22 attestations ATT-0218–0239, leaving genuine metadata in `notes`. This needs per-record
  judgment (separate the asserted datum from any editorial aside), so ~**1–2 hours**, one patch
  (PATCH bumps — content relocation, not a claim change). Pair it with a **validator addition** so the
  class can't recur: for `primary_paraphrase`/`primary_quotation`/`primary_observation`, require a
  non-empty `paraphrase` or `direct_quotation`. That converts a silent convention into an enforced one.

No patches produced this pass, per the read-only scope. If you want, the natural next move is Item G
(the rule-8 back-fill + validator rule) since it's now the highest-value hygiene item the sweep exposed;
the dedup cross-refs are lower-value and can ride along or wait.
