"""
Perturbation self-test — proves each of the six counterfactuals DISCRIMINATES by
derivation, not assertion by literal.

Method: for each case, mutate a fixture record the case depends on, re-run that
counterfactual's wrong-model observe function, and assert the wrong-model observable
CHANGED from its unperturbed value. A derived observable moves under perturbation; a
hardcoded literal does not. This test therefore FAILS on any case whose observable is a
literal — which is exactly the defect Step-3b Gate-3-correction removes.

Each case's discrimination DEPENDENCY (the record whose mutation must move the observable)
is named in PERTURBATIONS and printed, so the dependency is explicit.

Run: python3 perturb_test.py    (exit 0 = all six derive; exit 1 = a literal was found)
Read-only, synthetic, workspace-only.
"""
import sys
from schema import Schema
from fixture import build_fixture
import run_gates as G


def _wrong_schema(wrong_cfg):
    return build_fixture(Schema(**wrong_cfg))


# Each entry: (case name, wrong_cfg, observe fn, key, dependency description, perturb fn)
# perturb(s) mutates the loaded wrong-schema fixture in place.

def drop_ter16_restores_edge(s):
    # Under tolerate-merge, the surviving-row count is derived from the restores edges.
    # Remove the restores edge: with no edge, nothing merges, so BOTH units survive (1 -> 2).
    for rid in [r for r, v in s.relationship.items() if v.get("rel_type") == "restores"]:
        s.relationship.pop(rid)

def drop_surviving_membership18(s):
    # The single-parent wrong-model keeps the FIRST membership by id. Drop that one so the
    # survivor count moves (1 -> either the next survivor is still 1... so drop BOTH to reach 0).
    mem = sorted([(rid, v) for rid, v in s.relationship.items()
                  if v.get("rel_type") == "member_of_route_family" and v["source_id"] == "FX-RTE-18t"],
                 key=lambda kv: kv[0])
    for rid, _ in mem:
        s.relationship.pop(rid)   # drop all memberships -> single-parent survivor count 1 -> 0

def drop_colocated17(s):
    for rid in [r for r, v in s.relationship.items()
                if v.get("rel_type") == "co_located_aspect"
                and {v["source_id"], v["target_id"]} == {"FX-LFT-17", "FX-SIT-17"}]:
        s.relationship.pop(rid)

def change_footprint19(s):
    if "FX-CMP-19b" in s.component:
        s.component["FX-CMP-19b"]["footprint"] = "POLYGON-footprint-DIFFERENT"

def drop_site15_gap_phase(s):
    # remove the second phase run so the split rule sees one run, not two
    s.phase.pop("FX-PHA-15c", None)

def drop_one_candidate_link_5b(s):
    # remove one candidate QSL so the identifying set (under candidate_in_dedup) shrinks
    s.qualified_subject_link.pop("FX-QSL-5b2r", None)
    s.qualified_subject_link.pop("FX-QSL-5b2s", None)


PERTURBATIONS = [
    ("15 Site gap",        {"unified_gap_rule": "split"},    G.obs_site15_rowcount, "site_rows_for_gap_entity",
     "FX-PHA-15c (the second, post-gap phase of FX-SIT-15)", drop_site15_gap_phase),
    ("16 TU interruption", {"unified_gap_rule": "tolerate"}, G.obs_ter16_rowcount,  "territorial_unit_rows",
     "the restores edge FX-REL-16 (present -> merge to 1; absent -> both survive, 2)", drop_ter16_restores_edge),
    ("17 dual aspect",     {"allow_contains_dual": True},    G.obs_dual17,          "forbidden_contains_edges",
     "the co_located_aspect edge between FX-LFT-17 and FX-SIT-17", drop_colocated17),
    ("18 route braiding",  {"single_parent_family": True},   G.obs_braid18,         "track_family_memberships",
     "FX-RTE-18t's member_of_route_family edges (survivor count moves to 0 when removed)", drop_surviving_membership18),
    ("19a component",      {"footprint_identity": True},     G.obs_component19,     "component_rows_on_footprint",
     "FX-CMP-19b's footprint (shared vs distinct)", change_footprint19),
    ("5b pooling",         {"candidate_in_dedup": True},     G.obs_pool5b,          "identifying_subjects",
     "FX-ATT-5b2's two candidate subject links", drop_one_candidate_link_5b),
]


def main():
    print("=" * 74)
    print("PERTURBATION SELF-TEST — each observable must MOVE under fixture mutation")
    print("(a literal cannot move; a derived value must)")
    print("=" * 74)
    all_pass = True
    for name, cfg, observe, key, dep, perturb in PERTURBATIONS:
        base = observe(_wrong_schema(cfg))[key]         # unperturbed wrong-model observable
        s = _wrong_schema(cfg)
        perturb(s)                                       # mutate the dependency record
        moved = observe(s)[key]                          # re-derive
        changed = (moved != base)
        all_pass = all_pass and changed
        print(f"\n  [{name}]")
        print(f"    discrimination depends on: {dep}")
        print(f"    wrong-model '{key}' unperturbed: {base}")
        print(f"    after perturbing that record:    {moved}")
        print(f"    observable MOVED: {'YES — derived' if changed else 'NO — LITERAL, TEST FAILS'}")
    print("\n" + "=" * 74)
    print("PERTURBATION RESULT:", "ALL SIX DERIVE (green)" if all_pass else "A LITERAL WAS FOUND (red)")
    print("=" * 74)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
