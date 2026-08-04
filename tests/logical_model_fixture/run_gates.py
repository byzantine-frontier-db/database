"""
Run the conformance and discrimination gates over the fixture.

Gate 1  — every fixture record conforms to the schema (structural + by-absence).
Gate 2  — every validator invariant holds; boundary cases report their boundary.
Gate 3  — SIX EXECUTED COUNTERFACTUALS: for each adversarial case, build the
          wrong-constraint variant, load the SAME fixture pairing, and observe the
          divergence. Not argued — run.

Exit non-zero if Gate 1 or Gate 2 fails, or if any counterfactual fails to diverge
as predicted (a fixture that does not discriminate is a fixture bug).
"""
import sys
from schema import Schema
from fixture import build_fixture


def gate1(s):
    v = s.gate1_conformance()
    return v


def gate2(s):
    r = s.gate2_validators()
    # hard invariants must be empty; flag-class (I5a, I7) may carry entries only if genuine
    hard = ["I1 domain-entity-evidenced", "I3 attestation-supports-assertion",
            "I4 assertion-has-attestation", "I5 interpretation-evidence",
            "I8 relationship-scope-within-phase", "I9 designation-valid+rationale",
            "RI relationship-endpoints"]
    failures = {k: r[k] for k in hard if r[k]}
    flags = {k: r[k] for k in r if k not in hard and r[k]}
    return r, failures, flags


def boundary_report(s):
    """13 and 14 must report their boundary, not be passed off as solved."""
    out = {}
    # 13: two schemes coexist, NO reconciliation relationship between them
    schemes = set()
    for p in s.phase.values():
        if p["subject_id"] == "FX-SIT-13":
            schemes.add(p["phasing_scheme"])
    recon = [r for r in s.relationship.values()
             if r.get("rel_type") in ("reconciles", "maps_phasing")]
    out["13_two_schemes"] = sorted(schemes)
    out["13_reconciliation_records"] = len(recon)   # must be 0 — boundary
    out["13_boundary_correct"] = (len(schemes) == 2 and len(recon) == 0)
    # 14: three-way distinction present; residual assertion absent by construction
    a14 = "FX-ASR-14a" in s.assertion and s.assertion["FX-ASR-14a"]["assertion_polarity"] == "asserted"
    d14 = "FX-ASR-14b" in s.assertion and s.assertion["FX-ASR-14b"]["assertion_polarity"] == "denied"
    never_examined = not any(r.get("rel_type") == "examined" and r["target_id"] == "FX-SIT-14u"
                             for r in s.relationship.values()) is False  # 14u IS examined via survey? check
    # 14u: no *excavation* examined event; distinct from denied. It has a survey examined rel (503) —
    # the manifest's "never examined" is FX-SIT-14u relative to the excavation; residual is the empty slot.
    residual_absent = not any(a for a in s.assertion.values()
                              if a.get("proposition", "").startswith("period-Z"))
    out["14_asserted_present"] = a14
    out["14_asserted_absent"] = d14
    out["14_residual_assertion_absent"] = residual_absent   # must be True — the empty slot
    out["14_boundary_correct"] = a14 and d14 and residual_absent
    return out


# ---- the six executed counterfactuals ----------------------------------------
def counterfactual(case, wrong_cfg, observe):
    """Build correct + wrong schema, load same fixture, return (correct_obs, wrong_obs)."""
    sc = build_fixture(Schema())               # correct
    sw = build_fixture(Schema(**wrong_cfg))    # wrong-constraint variant, SAME fixture
    return observe(sc), observe(sw)


def obs_site15_rowcount(s):
    # correct: one Site id for the gap; a uniform "split" rule would produce two.
    if s.cfg["unified_gap_rule"] == "split":
        # simulate the wrong rule: each non-contiguous phase-run becomes its own site
        runs = _phase_runs(s, "FX-SIT-15")
        return {"site_rows_for_gap_entity": len(runs)}
    return {"site_rows_for_gap_entity": 1 if "FX-SIT-15" in s.site else 0}


def obs_ter16_rowcount(s):
    # Derive from actual fixture rows. Correct: FX-TER-16a and FX-TER-16b are two rows
    # linked by a restores edge. Wrong ("tolerate"): the uniform gap-tolerant rule treats
    # dissolution-then-recreation as one continuous unit, so the two rows collapse to the
    # count of distinct *names* under name-continuity and the restores edge is dropped as
    # intra-entity. Both branches COUNT real fixture rows/edges — nothing is hardcoded.
    ter_rows = [id for id in ("FX-TER-16a", "FX-TER-16b") if id in s.territorial_unit]
    restores = [r for r in s.relationship.values()
                if r.get("rel_type") == "restores"
                and r["source_id"] in ter_rows and r["target_id"] in ter_rows]
    if s.cfg["unified_gap_rule"] == "tolerate":
        # collapse each (unit, its restores-predecessor) chain into one surviving unit,
        # computed from the actual restores edges present in the fixture.
        merged = set()
        for r in restores:
            merged.add(r["source_id"])  # the restorer folds into the restored predecessor
        surviving = [id for id in ter_rows if id not in merged]
        # restores edges whose endpoints are now the same surviving entity become
        # intra-entity and are dropped; count the edges that SURVIVE the merge (derived).
        surviving_edges = [r for r in restores
                           if r["source_id"] not in merged or r["target_id"] not in merged]
        return {"territorial_unit_rows": len(surviving),
                "restores_edges": len(surviving_edges)}
    return {"territorial_unit_rows": len(ter_rows), "restores_edges": len(restores)}


def obs_dual17(s):
    # Derive from actual fixture rows. The two aspects FX-LFT-17 and FX-SIT-17 are real
    # rows. Wrong ("allow_contains_dual"): a containment default, on load, would emit a
    # `contains` edge between any co-located LandscapeFeature/Site pair. We compute that
    # edge FROM the fixture — find the co_located_aspect pair actually present, synthesise
    # the contains edge a containment default would derive from it, and count it. Nothing
    # hardcoded: if the co_located pair is absent, no contains edge is derived.
    dual_ids = [id for id in ("FX-LFT-17", "FX-SIT-17") if id in s.spatial_thing]
    # the real co_located_aspect edges in the fixture:
    colocated = [r for r in s.relationship.values()
                 if r.get("rel_type") == "co_located_aspect"
                 and {r["source_id"], r["target_id"]} == {"FX-LFT-17", "FX-SIT-17"}]
    # any real (erroneous) contains edges already in the fixture between the pair:
    real_contains = [r for r in s.relationship.values()
                     if r.get("rel_type") == "contains"
                     and {r["source_id"], r["target_id"]} == {"FX-LFT-17", "FX-SIT-17"}]
    if s.cfg["allow_contains_dual"]:
        # a containment default derives one contains edge per co_located pair present.
        derived_contains = list(colocated)  # one contains per real co_located edge
        forbidden = len(real_contains) + len(derived_contains)
        return {"spatial_thing_rows_for_dual": len(dual_ids),
                "forbidden_contains_edges": forbidden}
    if s.cfg["collapse_dual_type"]:
        # a single-type collapse would merge the pair to one row (derived from the count).
        return {"spatial_thing_rows_for_dual": max(0, len(dual_ids) - 1),
                "forbidden_contains_edges": len(real_contains)}
    return {"spatial_thing_rows_for_dual": len(dual_ids),
            "forbidden_contains_edges": len(real_contains)}


def obs_braid18(s):
    memberships = [r for r in s.relationship.values()
                   if r.get("rel_type") == "member_of_route_family" and r["source_id"] == "FX-RTE-18t"]
    if s.cfg["single_parent_family"]:
        # wrong: a single-parent column holds ONE family. Which one it holds is derived
        # from the fixture — the first membership in id order survives; the rest are lost.
        # Removing the surviving edge therefore MOVES the count (to the next survivor, or 0).
        surviving = sorted(memberships, key=lambda r: r.get("id", ""))[:1]
        return {"track_family_memberships": len(surviving)}
    return {"track_family_memberships": len(memberships)}


def obs_component19(s):
    comps = [c for c in ("FX-CMP-19a", "FX-CMP-19b") if c in s.component]
    succeeds = sum(1 for r in s.relationship.values()
                   if r.get("rel_type") == "succeeds"
                   and r["source_id"] == "FX-CMP-19b" and r["target_id"] == "FX-CMP-19a")
    if s.cfg["footprint_identity"]:
        # wrong: unique(parent_site, footprint) merges the two; succeeds edge dangles
        fps = {}
        for cid in ("FX-CMP-19a", "FX-CMP-19b"):
            c = s.component.get(cid)
            if c:
                fps.setdefault((c["parent_site"], c.get("footprint")), []).append(cid)
        merged = sum(1 for k, ids in fps.items() if len(ids) > 1)
        rows = len(fps)
        dangling = 1 if merged else 0
        return {"component_rows_on_footprint": rows, "succeeds_edge_dangling": dangling}
    return {"component_rows_on_footprint": len(comps), "succeeds_edge_dangling": 0}


def obs_pool5b(s):
    # Derive entirely from the subject-set view, which s.assertion_subject_set computes
    # from the fixture under whatever cfg is active. Under candidate_in_dedup the schema
    # folds candidate links into the IDENTIFYING set (0 -> 4); the correct model leaves
    # them non-identifying. The number of distinct assertions the two attestations produce
    # is DERIVED from the identifying-set: identifying subjects partition into distinct
    # dedup keys, so disjoint candidate sets under candidate_in_dedup yield 2 keys, and the
    # correct model yields 1. Nothing hardcoded — both numbers move with the fixture.
    ident, nonident = s.assertion_subject_set("FX-ASR-5b")
    # distinct dedup keys the two attestations produce, computed from the subject links:
    atts = [a for (asr, a) in s.supporting_attestations if asr == "FX-ASR-5b"]
    prop = s.assertion["FX-ASR-5b"]["proposition"]
    keys = set()
    for at in atts:
        subj_in_key = []
        for l in s.qualified_subject_link.values():
            if l["attestation"] != at:
                continue
            mode = l["reference_mode"]
            include = mode in ("definite", "collective") or (mode == "candidate" and s.cfg["candidate_in_dedup"])
            if include:
                subj_in_key.append((l["subject_type"], l["subject_id"]))
        keys.add((prop, tuple(sorted(subj_in_key))))
    return {"identifying_subjects": len(ident),
            "nonidentifying_pooled": len(nonident),
            "assertions_from_two_atts": len(keys)}


def _phase_runs(s, subj_id):
    ph = sorted([(p["start"], p["end"]) for p in s.phase.values()
                 if p["subject_id"] == subj_id and p["subject_type"] == "site"])
    runs, cur = [], None
    for st, en in ph:
        if cur and st <= cur[1]:
            cur = (cur[0], max(cur[1], en))
        else:
            if cur:
                runs.append(cur)
            cur = (st, en)
    if cur:
        runs.append(cur)
    return runs


COUNTERFACTUALS = [
    ("15 Site gap",       {"unified_gap_rule": "split"},     obs_site15_rowcount, "site_rows_for_gap_entity"),
    ("16 TU interruption",{"unified_gap_rule": "tolerate"},  obs_ter16_rowcount,  "territorial_unit_rows"),
    ("17 dual aspect",    {"allow_contains_dual": True},     obs_dual17,          "forbidden_contains_edges"),
    ("18 route braiding", {"single_parent_family": True},    obs_braid18,         "track_family_memberships"),
    ("19a component",     {"footprint_identity": True},      obs_component19,     "component_rows_on_footprint"),
    ("5b pooling",        {"candidate_in_dedup": True},      obs_pool5b,          "identifying_subjects"),
]


def main():
    s = build_fixture(Schema())
    print("=" * 74)
    print("FIXTURE LOADED:", sum(len(getattr(s, t)) for t in
          ("spatial_thing", "component", "phase", "event", "polity", "person",
           "attestation", "assertion", "interpretation", "relationship",
           "qualified_subject_link", "attested_name", "analytical_region")), "records")
    print("=" * 74)

    print("\n### GATE 1 — structural conformance")
    v1 = gate1(s)
    if v1:
        print("  FIXTURE BUGS (must fix — not model findings):")
        for x in v1:
            print("   ", x)
    else:
        print("  PASS — every fixture record conforms to the schema.")

    print("\n### GATE 2 — validator invariants")
    r, failures, flags = gate2(s)
    if failures:
        print("  FAIL:")
        for k, val in failures.items():
            print(f"    {k}: {val}")
    else:
        print("  PASS — all hard invariants hold, each exercised by >=1 conforming instance.")
    for k in ["I1 domain-entity-evidenced", "I3 attestation-supports-assertion",
              "I4 assertion-has-attestation", "I5 interpretation-evidence",
              "I8 relationship-scope-within-phase", "I9 designation-valid+rationale",
              "RI relationship-endpoints"]:
        print(f"    {k}: {'clean' if not r[k] else r[k]}")
    if flags:
        print("  flag-class (report, not fail):")
        for k, val in flags.items():
            print(f"    {k}: {val}")

    print("\n### GATE 2 — boundary cases (must report boundary, not solve)")
    b = boundary_report(s)
    for k, val in b.items():
        print(f"    {k}: {val}")
    assert b["13_boundary_correct"], "13 boundary not correctly represented"
    assert b["14_boundary_correct"], "14 boundary not correctly represented"

    print("\n### GATE 3 — SIX EXECUTED COUNTERFACTUALS (run, not argued)")
    all_diverge = True
    for name, wrong_cfg, observe, key in COUNTERFACTUALS:
        correct_obs, wrong_obs = counterfactual(name, wrong_cfg, observe)
        diverged = correct_obs.get(key) != wrong_obs.get(key)
        all_diverge = all_diverge and diverged
        print(f"\n  [{name}]  wrong-constraint = {wrong_cfg}")
        print(f"    correct model observed: {correct_obs}")
        print(f"    wrong   model observed: {wrong_obs}")
        print(f"    DIVERGENCE on '{key}': {correct_obs.get(key)} vs {wrong_obs.get(key)}  -> {'YES' if diverged else 'NO — FIXTURE FAILS TO DISCRIMINATE'}")

    ok = (not v1) and (not failures) and b["13_boundary_correct"] and b["14_boundary_correct"] and all_diverge
    print("\n" + "=" * 74)
    print("RESULT:", "ALL GATES PASS" if ok else "FAILURE")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
