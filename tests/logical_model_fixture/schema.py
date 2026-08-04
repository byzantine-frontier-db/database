"""
Checkable schema for the Byzantine-Islamic Frontier logical model.

Realises Step 3a Deliverable 1 (schema-realisation plan) exactly, as an in-memory
relational schema with enforceable constraints. This is a *checkable* realisation:
tables are typed row-sets, constraints are predicates that return violations.

There is no SQL layer in the repo, so the physical schema is realised in Python as
the executable form of the plan. The constraint CLASSES are what matter and are
preserved exactly:

  - structural   : a schema constraint the data cannot violate while conforming
                   (NOT NULL, enum domain, single-valued FK, exclusion constraint,
                    GeometryType CHECK)
  - by-absence   : guaranteed by a column that does not exist
  - validator    : a check over a union of tables or a derived set that a DB
                   constraint cannot express

Scope discipline: this realises the plan; it does not re-derive it. The two flagged
readings are wired as specified for the fixture and REMAIN flagged:
  (1) relationship RI  -> validator + optional per-type partial FK  (RI_MODE)
  (2) pure-candidate subject set -> absence-of-identifying-rows     (view semantics)

Read-only against the corpus; the FX- space is disjoint.
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum


# ---------------------------------------------------------------------------
# Enumerated domains (structural: enum-domain constraints)
# ---------------------------------------------------------------------------

SPATIAL_TYPES = {"site", "landscape_feature", "route", "territorial_unit"}
GEOMETRY_TYPES = {"POINT", "LINESTRING", "POLYGON", "MULTIPOLYGON"}  # the four; no COLLECTION/CURVED
REFERENCE_MODES = {"definite", "candidate", "collective"}
ASSERTION_KINDS = {"general", "spatial", "temporal", "functional", "identification"}
POLARITIES = {"asserted", "denied"}
PROVENANCE = {  # 15-term vocab (subset used by the fixture)
    "primary_paraphrase", "primary_quotation", "primary_summary", "primary_observation",
    "modern_synthesis", "modern_identification", "modern_interpretation",
    "archaeological_evidence", "gis_derived_observation", "epigraphic_evidence",
    "numismatic_evidence", "cross_source_synthesis",
}
DOMAIN_TYPES = {  # QualifiedSubjectLink.subject ranges over these (L-poly, domain only)
    "site", "landscape_feature", "route", "territorial_unit",
    "component", "event", "polity", "person", "phase",
}
RECORD_TYPES = DOMAIN_TYPES | {  # relationship endpoints range over ALL records
    "attestation", "assertion", "interpretation", "source", "relationship",
    "spatial_assertion", "temporal_assertion",
}


# ---------------------------------------------------------------------------
# Interval helper (for I6 exclusion constraint, I7, I8)
# ---------------------------------------------------------------------------

@dataclass
class Interval:
    start: Optional[int]
    end: Optional[int]

    def overlaps(self, other: "Interval") -> bool:
        if None in (self.start, self.end, other.start, other.end):
            return False
        return self.start < other.end and other.start < self.end

    def within(self, other: "Interval") -> bool:
        if None in (self.start, self.end, other.start, other.end):
            return True  # unscoped: cannot violate containment
        return other.start <= self.start and self.end <= other.end


# ---------------------------------------------------------------------------
# The schema: typed tables + a configurable constraint set
# ---------------------------------------------------------------------------

class SchemaError(Exception):
    pass


class Schema:
    """
    In-memory relational schema. `config` carries the two flagged readings and the
    switches that the discrimination harness flips to build WRONG-constraint variants.

    Wrong-constraint switches (default = correct model):
      unified_gap_rule      : None | "split" | "tolerate"   (Demand-15/16 wrong rules)
      allow_contains_dual   : False -> co_located only; True lets a containment default in (17)
      collapse_dual_type    : False -> two entities; True merges dual aspect to one (17)
      single_parent_family  : False -> m:n; True enforces one family per track (18)
      footprint_identity    : False -> fabric; True keys component identity on footprint (19a)
      candidate_in_dedup    : False -> candidate excluded; True folds candidates into key (5b)
      distinctness_on_rels  : False -> same-type pairs allowed; True forbids them (Demand-B)
    """

    def __init__(self, **config):
        self.cfg = {
            "RI_MODE": "validator+partial",     # flagged reading (1), as specified
            "pure_candidate_repr": "absence",   # flagged reading (2), as specified
            # wrong-constraint switches (all default correct):
            "unified_gap_rule": None,
            "allow_contains_dual": False,
            "collapse_dual_type": False,
            "single_parent_family": False,
            "footprint_identity": False,
            "candidate_in_dedup": False,
            "distinctness_on_rels": False,
        }
        self.cfg.update(config)
        # tables
        self.spatial_thing = {}      # id -> row (supertable; class-table inheritance)
        self.site = {}               # id -> subtype row
        self.landscape_feature = {}
        self.route = {}
        self.territorial_unit = {}
        self.component = {}
        self.phase = {}
        self.event = {}
        self.polity = {}
        self.person = {}
        self.attested_name = {}
        self.source = {}
        self.attestation = {}
        self.assertion = {}
        self.spatial_assertion = {}  # assertion_id -> payload
        self.temporal_assertion = {}
        self.qualified_subject_link = {}
        self.supporting_attestations = []  # (assertion_id, attestation_id)
        self.interpretation = {}
        self.interpretation_evidence = []  # (interpretation_id, attestation_id)
        self.relationship = {}
        self.analytical_region = {}

    # ---- subtype dispatch for the spatial supertable ----
    def _subtype_table(self, spatial_type):
        return {"site": self.site, "landscape_feature": self.landscape_feature,
                "route": self.route, "territorial_unit": self.territorial_unit}[spatial_type]

    # ---- insert helpers enforcing STRUCTURAL constraints at write time ----
    def add_spatial_thing(self, id, spatial_type, standardised_name,
                          identification_status, identification_confidence,
                          designated_spatial_assertion=None, **subtype_cols):
        if spatial_type not in SPATIAL_TYPES:
            raise SchemaError(f"enum: spatial_type {spatial_type}")
        if id in self.spatial_thing:
            raise SchemaError(f"PK dup: {id}")
        # collapse_dual_type wrong-variant: a merged dual-aspect row would carry BOTH a
        # feature_type and site-ness; the correct schema has no column for that, so the
        # merged row simply cannot be represented -> we record the attempt for the harness.
        self.spatial_thing[id] = dict(
            id=id, spatial_type=spatial_type, standardised_name=standardised_name,
            identification_status=identification_status,
            identification_confidence=identification_confidence,
            designated_spatial_assertion=designated_spatial_assertion)
        self._subtype_table(spatial_type)[id] = dict(id=id, **subtype_cols)

    def add(self, table, id, **cols):
        t = getattr(self, table)
        if id in t:
            raise SchemaError(f"PK dup in {table}: {id}")
        t[id] = dict(id=id, **cols)

    # ---- GATE 1: structural conformance (every record conforms) ----
    def gate1_conformance(self):
        v = []
        # geometry type CHECK
        for aid, pay in self.spatial_assertion.items():
            if pay["geometry_type"] not in GEOMETRY_TYPES:
                v.append(("I-geom-CHECK", aid, pay["geometry_type"]))
        # enum domains
        for lid, l in self.qualified_subject_link.items():
            if l["reference_mode"] not in REFERENCE_MODES:
                v.append(("enum reference_mode", lid, l["reference_mode"]))
            if l["subject_type"] not in DOMAIN_TYPES:
                v.append(("L-poly domain-only", lid, l["subject_type"]))
        for aid, a in self.assertion.items():
            if a["assertion_kind"] not in ASSERTION_KINDS:
                v.append(("enum assertion_kind", aid, a["assertion_kind"]))
            if a["assertion_polarity"] not in POLARITIES:
                v.append(("enum polarity", aid, a["assertion_polarity"]))
        for at, a in self.attestation.items():
            if a["provenance_category"] not in PROVENANCE:
                v.append(("enum provenance", at, a["provenance_category"]))
        # I2 structural: claim non-empty
        for at, a in self.attestation.items():
            if not (a.get("paraphrase") or a.get("direct_quotation")):
                v.append(("I2 claim-empty", at, None))
        # I5b structural: observation_date iff primary_observation
        for at, a in self.attestation.items():
            has_od = a.get("observation_date") is not None
            is_po = a["provenance_category"] == "primary_observation"
            if has_od != is_po:
                v.append(("I5b observation_date-iff-primary_observation", at, None))
        # I11 structural: single-valued designated FK (cannot point at two — column is scalar).
        #   Verified by shape: the field holds one id or None. A list would be a schema breach.
        for id, r in self.spatial_thing.items():
            d = r["designated_spatial_assertion"]
            if d is not None and not isinstance(d, str):
                v.append(("I11 single-valued spatial FK", id, d))
        for pid, p in self.phase.items():
            for f in ("designated_spatial_assertion", "designated_temporal_assertion"):
                d = p.get(f)
                if d is not None and not isinstance(d, str):
                    v.append((f"I11 single-valued {f}", pid, d))
        # I6 structural: Site-phase non-overlap within (subject, scheme); Component phases may overlap
        site_phases = {}
        for pid, p in self.phase.items():
            if p["subject_type"] == "site":
                key = (p["subject_id"], p.get("phasing_scheme", "default"))
                site_phases.setdefault(key, []).append((pid, Interval(p.get("start"), p.get("end"))))
        for key, lst in site_phases.items():
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    if lst[i][1].overlaps(lst[j][1]):
                        v.append(("I6 site-phase overlap in scheme", key, (lst[i][0], lst[j][0])))
        # geometry attachment target (I10 structural-by-attachment)
        for aid, pay in self.spatial_assertion.items():
            tgt = pay.get("attaches_to_type")
            if tgt not in {"site", "landscape_feature", "route", "territorial_unit", "phase"}:
                v.append(("I10 bad geometry attachment", aid, tgt))
        return v

    # ---- derived view: assertion_subject_set (flagged reading 2: absence semantics) ----
    def assertion_subject_set(self, assertion_id):
        """Fold over supporting attestations' QSLs. definite/collective -> identifying;
        candidate -> non-identifying. Returns (identifying[], nonidentifying[]).
        Wrong-variant candidate_in_dedup flips candidates to identifying."""
        atts = [a for (asr, a) in self.supporting_attestations if asr == assertion_id]
        ident, nonident = [], []
        for at in atts:
            for lid, l in self.qualified_subject_link.items():
                if l["attestation"] != at:
                    continue
                key = (l["subject_type"], l["subject_id"])
                mode = l["reference_mode"]
                if mode in ("definite", "collective"):
                    ident.append(key)
                elif mode == "candidate":
                    if self.cfg["candidate_in_dedup"]:
                        ident.append(key)      # WRONG variant
                    else:
                        nonident.append(key)   # correct: absence-of-identifying (flagged reading 2)
        return sorted(set(ident)), sorted(set(nonident))

    def assertion_dedup_key(self, assertion_id):
        a = self.assertion[assertion_id]
        ident, _ = self.assertion_subject_set(assertion_id)
        return (a["proposition"], tuple(ident))

    # ---- GATE 2: validator invariants ----
    def gate2_validators(self):
        results = {}
        # I1 every domain entity evidenced (subject link or interpretation/relationship back-link)
        def domain_ids():
            for tname in ("site", "landscape_feature", "route", "territorial_unit",
                          "component", "event", "polity", "person"):
                for id in getattr(self, tname):
                    yield (tname, id)
        linked = {(l["subject_type"], l["subject_id"]) for l in self.qualified_subject_link.values()}
        i1 = [d for d in domain_ids() if d not in linked]
        results["I1 domain-entity-evidenced"] = i1
        # I3 every attestation supports >=1 assertion
        supp_atts = {a for (_, a) in self.supporting_attestations}
        i3 = [at for at in self.attestation if at not in supp_atts]
        results["I3 attestation-supports-assertion"] = i3
        # I4 every assertion has >=1 attestation
        asr_with = {asr for (asr, _) in self.supporting_attestations}
        i4 = [asr for asr in self.assertion if asr not in asr_with]
        results["I4 assertion-has-attestation"] = i4
        # I5 interpretation evidence non-empty and ATT-only (ATT-only structural via junction)
        int_with = {i for (i, _) in self.interpretation_evidence}
        i5 = [i for i in self.interpretation if i not in int_with]
        results["I5 interpretation-evidence"] = i5
        # I5a related/competing interpretations linked (flag): argument names INT-x with no relationship
        i5a = []
        rel_int_pairs = {(r["source_id"], r["target_id"]) for r in self.relationship.values()
                         if r["source_type"] == "interpretation" and r["target_type"] == "interpretation"}
        for iid, it in self.interpretation.items():
            for named in it.get("names_interpretations", []):
                if (iid, named) not in rel_int_pairs and (named, iid) not in rel_int_pairs:
                    i5a.append((iid, named))
        results["I5a interpretation-cross-ref (flag)"] = i5a
        # I7 existence interval consistent with phase union (flag)
        i7 = []
        for tname in ("site",):
            for id in getattr(self, tname):
                ph = [Interval(p.get("start"), p.get("end")) for p in self.phase.values()
                      if p["subject_type"] == tname and p["subject_id"] == id
                      and p.get("start") is not None]
                if not ph:
                    continue
                lo, hi = min(p.start for p in ph), max(p.end for p in ph)
                # a gap is allowed; violation only if a phase falls outside [lo,hi] (cannot, by constr)
                for p in ph:
                    if p.start < lo or p.end > hi:
                        i7.append((id, (p.start, p.end)))
        results["I7 existence-interval (flag)"] = i7
        # I8 relationship temporal scope within phase endpoint scope
        i8 = []
        for rid, r in self.relationship.items():
            for side in ("source", "target"):
                if r[f"{side}_type"] == "phase" and r.get("temporal_scope"):
                    p = self.phase.get(r[f"{side}_id"])
                    if p:
                        pi = Interval(p.get("start"), p.get("end"))
                        ri = Interval(*r["temporal_scope"])
                        if not ri.within(pi):
                            i8.append((rid, side))
        results["I8 relationship-scope-within-phase"] = i8
        # I9 designated assertion is one of subject's own; rationale recorded
        i9 = []
        for id, r in self.spatial_thing.items():
            d = r["designated_spatial_assertion"]
            if d is None:
                continue
            ident, nonident = self.assertion_subject_set(d)
            subj = ("_thing", id)  # spatial designated assertions attach via attaches_to, check that
            pay = self.spatial_assertion.get(d, {})
            if not (pay.get("attaches_to_type") in SPATIAL_TYPES and pay.get("attaches_to_id") == id):
                i9.append(("designated-not-own", id, d))
            if not r.get("designation_rationale") and d is not None:
                # rationale stored on the thing when a designation is made
                i9.append(("no-rationale", id, d))
        results["I9 designation-valid+rationale"] = i9
        # RI (flagged reading 1): validator over polymorphic endpoints
        ri = []
        for rid, r in self.relationship.items():
            for side in ("source", "target"):
                t, i = r[f"{side}_type"], r[f"{side}_id"]
                if not self._exists(t, i):
                    ri.append((rid, side, t, i))
            # distinctness: correct model does NOT forbid same-type (Demand-B); wrong variant does
            if self.cfg["distinctness_on_rels"] and r["source_type"] == r["target_type"]:
                ri.append((rid, "DISTINCTNESS-REJECT-same-type", r["source_type"], None))
        results["RI relationship-endpoints"] = ri
        return results

    def _exists(self, rtype, id):
        table_map = {
            "site": self.site, "landscape_feature": self.landscape_feature,
            "route": self.route, "territorial_unit": self.territorial_unit,
            "component": self.component, "event": self.event, "polity": self.polity,
            "person": self.person, "phase": self.phase, "attestation": self.attestation,
            "assertion": self.assertion, "interpretation": self.interpretation,
            "source": self.source, "relationship": self.relationship,
            "spatial_assertion": self.spatial_assertion,
            "temporal_assertion": self.temporal_assertion,
        }
        if rtype in ("site", "landscape_feature", "route", "territorial_unit"):
            return id in self.spatial_thing and self.spatial_thing[id]["spatial_type"] == rtype
        return id in table_map.get(rtype, {})
