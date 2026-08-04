"""
Synthetic fixture — the FX- records instantiating the ratified Step-3a manifest.

Parts A (19 items), B (6 adversarial with second instances), C (2 boundary cases),
and every +add from Part D (register field-2 coverage).

FX- identifier space, disjoint from the corpus. Workspace-only, no corpus record
touched, no migration. Provisional-vocabulary cases use their marked provisional terms
(co_located_aspect, member_of_argued_group, examined, produced_phase/terminated_phase/
damaged, corroborates/parallel_case, subordinate_to/dependent_settlement_of, traverses/
crosses_at, interaction_mechanism); intervisible_with is inputs-only by the manifest.

`build_fixture(schema)` loads all records into a Schema instance. It is called with the
correct schema for conformance, and with wrong-constraint variants for discrimination —
the SAME fixture, different schema config, per Step-3a Deliverable 3.
"""

def build_fixture(s):
    # helpers -----------------------------------------------------------------
    def thing(id, st, name, **cols):
        idc = cols.pop("idconf", 4)
        st_status = cols.pop("status", "identified")
        s.add_spatial_thing(id, st, name, st_status, idc,
                            designated_spatial_assertion=cols.pop("dsa", None), **cols)
        if "rationale" in cols:
            s.spatial_thing[id]["designation_rationale"] = cols["rationale"]

    def spatial_assertion(aid, gtype, attaches_type, attaches_id, prov="archaeological_evidence", conf=3):
        s.add("assertion", aid, proposition=f"geometry of {attaches_id}",
              assertion_kind="spatial", assertion_polarity="asserted")
        s.spatial_assertion[aid] = dict(id=aid, geometry_type=gtype,
              attaches_to_type=attaches_type, attaches_to_id=attaches_id,
              spatial_confidence=conf, coordinate_method="published")
        # a spatial assertion is itself evidenced by an attestation + support link
        at = aid + "-at"
        s.add("attestation", at, source="FX-SRC-1", citation="fixture",
              paraphrase="geom", provenance_category=prov, evidential_confidence=conf)
        s.supporting_attestations.append((aid, at))

    def temporal_assertion(aid, start, end, attaches_type, attaches_id, conf=3, designated=True):
        s.add("assertion", aid, proposition=f"dating of {attaches_id}",
              assertion_kind="temporal", assertion_polarity="asserted")
        s.temporal_assertion[aid] = dict(id=aid, start=start, end=end,
              attaches_to_type=attaches_type, attaches_to_id=attaches_id,
              chronological_confidence=conf)
        at = aid + "-at"
        s.add("attestation", at, source="FX-SRC-1", citation="fixture",
              paraphrase="date", provenance_category="primary_paraphrase", evidential_confidence=conf)
        s.supporting_attestations.append((aid, at))

    def phase(pid, subj_type, subj_id, start, end, scheme="default", **cols):
        s.add("phase", pid, subject_type=subj_type, subject_id=subj_id,
              start=start, end=end, phasing_scheme=scheme, **cols)

    def att(id, prov="primary_paraphrase", conf=3, para="claim", src="FX-SRC-1", **cols):
        s.add("attestation", id, source=src, citation="fixture", paraphrase=para,
              provenance_category=prov, evidential_confidence=conf, **cols)

    def qsl(id, att_id, subj_type, subj_id, mode, conf=3):
        s.add("qualified_subject_link", id, attestation=att_id, subject_type=subj_type,
              subject_id=subj_id, reference_mode=mode, identification_confidence=conf)

    def asr(id, prop, kind="general", pol="asserted"):
        s.add("assertion", id, proposition=prop, assertion_kind=kind, assertion_polarity=pol)

    def support(asr_id, *att_ids):
        for a in att_ids:
            s.supporting_attestations.append((asr_id, a))

    def interp(id, scholar, **cols):
        names = cols.pop("names_interpretations", [])
        s.add("interpretation", id, scholar=scholar, publication="FX-SRC-1",
              argument=cols.pop("argument", "arg"), argumentative_confidence=cols.pop("conf", 3),
              names_interpretations=names)
    def interp_ev(iid, *att_ids):
        for a in att_ids:
            s.interpretation_evidence.append((iid, a))

    def rel(id, rtype, st, sid, tt, tid, temporal_scope=None):
        s.add("relationship", id, rel_type=rtype, source_type=st, source_id=sid,
              target_type=tt, target_id=tid, relationship_confidence=3,
              temporal_scope=temporal_scope)

    def name(id, subj_id, form, lang, temporal_validity=None):
        at = id + "-at"
        att(at, para=f"name {form}")
        s.add("attested_name", id, subject=subj_id, form=form, language=lang,
              name_type="attested", temporal_validity=temporal_validity, supporting_attestation=at)

    # shared source -----------------------------------------------------------
    s.add("source", "FX-SRC-1", author="Fixture", author_unnamed=False)
    s.add("source", "FX-SRC-2", author="Fixture2", author_unnamed=False)

    # ===================== PART A — nineteen items ==========================
    # 1 fort controls pass
    thing("FX-SIT-01", "site", "Fort-1"); thing("FX-LFT-01", "landscape_feature", "Pass-1", feature_type="pass", origin="natural")
    rel("FX-REL-01", "controls", "site", "FX-SIT-01", "landscape_feature", "FX-LFT-01")
    # 2 settlement moves (one Site, two phases displaced)
    thing("FX-SIT-02", "site", "Settle-2")
    spatial_assertion("FX-SPA-02a", "POINT", "phase", "FX-PHA-02a"); spatial_assertion("FX-SPA-02b", "POINT", "phase", "FX-PHA-02b")
    phase("FX-PHA-02a", "site", "FX-SIT-02", 700, 750, designated_spatial_assertion="FX-SPA-02a")
    phase("FX-PHA-02b", "site", "FX-SIT-02", 760, 810, designated_spatial_assertion="FX-SPA-02b")
    # 3 monastery -> fortress
    thing("FX-SIT-03", "site", "Convert-3")
    phase("FX-PHA-03a", "site", "FX-SIT-03", 600, 700, function="monastery", functional_confidence=4, rank="minor")
    phase("FX-PHA-03b", "site", "FX-SIT-03", 710, 800, function="fortress", functional_confidence=3)
    # 4 multiple names
    thing("FX-SIT-04", "site", "Manynames-4")
    name("FX-NAM-04a", "FX-SIT-04", "Nikopolis", "grc"); name("FX-NAM-04b", "FX-SIT-04", "Hisn", "ara")
    name("FX-NAM-04c", "FX-SIT-04", "LateName", "ara", temporal_validity=(900, 1000))
    # 5 one name several places (candidate) -> shared with 5b
    thing("FX-SIT-05p", "site", "Cand-P", status="disputed"); thing("FX-SIT-05q", "site", "Cand-Q", status="disputed")
    att("FX-ATT-05"); qsl("FX-QSL-05p", "FX-ATT-05", "site", "FX-SIT-05p", "candidate"); qsl("FX-QSL-05q", "FX-ATT-05", "site", "FX-SIT-05q", "candidate")
    asr("FX-ASR-05", "a place named X exists"); support("FX-ASR-05", "FX-ATT-05")
    # 6 seasonal, non-contiguous phases
    thing("FX-SIT-06", "site", "Seasonal-6")
    phase("FX-PHA-06a", "site", "FX-SIT-06", 700, 720, occupation_regime="seasonal")
    phase("FX-PHA-06c", "site", "FX-SIT-06", 760, 780, occupation_regime="seasonal")
    # 7 two nuclei -> multipolygon
    thing("FX-SIT-07", "site", "Nuclei-7")
    spatial_assertion("FX-SPA-07", "MULTIPOLYGON", "phase", "FX-PHA-07")
    phase("FX-PHA-07", "site", "FX-SIT-07", 700, 800, designated_spatial_assertion="FX-SPA-07")
    # 8 uncertain location -> zero geometry
    thing("FX-SIT-08", "site", "Unlocated-8", status="unidentified", dsa=None)
    # 9 multiple geometries, one designated
    thing("FX-SIT-09", "site", "Multigeo-9", dsa="FX-SPA-09b", rationale="best published fix")
    spatial_assertion("FX-SPA-09a", "POINT", "site", "FX-SIT-09"); spatial_assertion("FX-SPA-09b", "POINT", "site", "FX-SIT-09"); spatial_assertion("FX-SPA-09c", "POINT", "site", "FX-SIT-09")
    # 10 contested function
    thing("FX-SIT-10", "site", "Contested-10")
    phase("FX-PHA-10", "site", "FX-SIT-10", 700, 800, functional_confidence=2)
    att("FX-ATT-10a"); att("FX-ATT-10b")
    interp("FX-INT-10a", "S1", argument="fort"); interp_ev("FX-INT-10a", "FX-ATT-10a")
    interp("FX-INT-10b", "S2", argument="monastery"); interp_ev("FX-INT-10b", "FX-ATT-10b")
    # 11 conflicting chronologies, neither designated
    thing("FX-SIT-11", "site", "Chron-11"); s.add("component", "FX-CMP-11", parent_site="FX-SIT-11", component_type="wall")
    temporal_assertion("FX-TMP-11a", 700, 750, "component", "FX-CMP-11"); temporal_assertion("FX-TMP-11b", 780, 820, "component", "FX-CMP-11")
    att("FX-ATT-11a"); att("FX-ATT-11b")
    interp("FX-INT-11a", "S1", argument="early", names_interpretations=["FX-INT-11b"]); interp_ev("FX-INT-11a", "FX-ATT-11a")
    interp("FX-INT-11b", "S2", argument="late", names_interpretations=["FX-INT-11a"]); interp_ev("FX-INT-11b", "FX-ATT-11b")
    rel("FX-REL-11", "contradicts", "interpretation", "FX-INT-11a", "interpretation", "FX-INT-11b")
    # 12 misreading -> deprecated attestation
    thing("FX-SIT-12", "site", "Misread-12")
    att("FX-ATT-12", workflow_state="deprecated")
    interp("FX-INT-12", "S3", argument="correction"); interp_ev("FX-INT-12", "FX-ATT-12")
    rel("FX-REL-12", "supersedes_attestation", "interpretation", "FX-INT-12", "attestation", "FX-ATT-12")

    # ===================== PART B — six adversarial ==========================
    # 15 Site gap (one id, non-contiguous, NO restores)
    thing("FX-SIT-15", "site", "Gap-Site-15")
    phase("FX-PHA-15a", "site", "FX-SIT-15", 730, 760); phase("FX-PHA-15c", "site", "FX-SIT-15", 810, 850)
    # 16 TerritorialUnit dissolution-recreation (TWO ids + restores)
    thing("FX-TER-16a", "territorial_unit", "Jund-A", unit_type="jund", constituted_date=700, dissolved_date=750)
    thing("FX-TER-16b", "territorial_unit", "Jund-A-restored", unit_type="jund", constituted_date=800, dissolved_date=None)
    rel("FX-REL-16", "restores", "territorial_unit", "FX-TER-16b", "territorial_unit", "FX-TER-16a")
    # 17 dual aspect: two entities, co_located_aspect [PROV], neither contains
    thing("FX-LFT-17", "landscape_feature", "Pass-17", feature_type="pass", origin="natural")
    thing("FX-SIT-17", "site", "Fort-17")
    rel("FX-REL-17", "co_located_aspect", "landscape_feature", "FX-LFT-17", "site", "FX-SIT-17")  # PROV
    # 18 route braiding: one track, two families
    thing("FX-RTE-18t", "route", "Track-18", route_class="documented")
    thing("FX-RTE-18f1", "route", "Family-1", route_class="family"); thing("FX-RTE-18f2", "route", "Family-2", route_class="family")
    rel("FX-REL-18a", "member_of_route_family", "route", "FX-RTE-18t", "route", "FX-RTE-18f1")
    rel("FX-REL-18b", "member_of_route_family", "route", "FX-RTE-18t", "route", "FX-RTE-18f2")
    # 19a Component demolished/rebuilt SAME footprint, succeeds
    thing("FX-SIT-19", "site", "Rebuild-19")
    fp = "POLYGON-footprint-X"
    s.add("component", "FX-CMP-19a", parent_site="FX-SIT-19", component_type="wall", footprint=fp, fabric="A")
    s.add("component", "FX-CMP-19b", parent_site="FX-SIT-19", component_type="wall", footprint=fp, fabric="B")
    phase("FX-PHA-19a", "component", "FX-CMP-19a", 700, 770); phase("FX-PHA-19b", "component", "FX-CMP-19b", 780, 850)
    rel("FX-REL-19", "succeeds", "component", "FX-CMP-19b", "component", "FX-CMP-19a")  # same-type pair (Demand-B)
    # 5b two pure-candidate attestations, same proposition, disjoint candidate sets -> ONE assertion
    thing("FX-SIT-5br", "site", "Cand-R", status="disputed"); thing("FX-SIT-5bs", "site", "Cand-S", status="disputed")
    PROP = "a fortress named Hisn X did Y"
    att("FX-ATT-5b1"); qsl("FX-QSL-5b1p", "FX-ATT-5b1", "site", "FX-SIT-05p", "candidate"); qsl("FX-QSL-5b1q", "FX-ATT-5b1", "site", "FX-SIT-05q", "candidate")
    att("FX-ATT-5b2"); qsl("FX-QSL-5b2r", "FX-ATT-5b2", "site", "FX-SIT-5br", "candidate"); qsl("FX-QSL-5b2s", "FX-ATT-5b2", "site", "FX-SIT-5bs", "candidate")
    asr("FX-ASR-5b", PROP); support("FX-ASR-5b", "FX-ATT-5b1", "FX-ATT-5b2")

    # ===================== PART C — two boundary cases =======================
    # 13 competing phase divisions: two schemes, NO reconciliation record
    thing("FX-SIT-13", "site", "CompetingPhases-13")
    phase("FX-PHA-13a1", "site", "FX-SIT-13", 700, 760, scheme="A"); phase("FX-PHA-13a2", "site", "FX-SIT-13", 760, 820, scheme="A")
    phase("FX-PHA-13b1", "site", "FX-SIT-13", 700, 730, scheme="B"); phase("FX-PHA-13b2", "site", "FX-SIT-13", 730, 790, scheme="B"); phase("FX-PHA-13b3", "site", "FX-SIT-13", 790, 850, scheme="B")
    # (no relationship reconciles scheme A with scheme B — the boundary)
    # 14 negative evidence: three-way present; residual is a DELIBERATELY EMPTY SLOT
    thing("FX-SIT-14", "site", "NegEv-14"); thing("FX-SIT-14u", "site", "NeverExamined-14u")
    att("FX-ATT-14a"); asr("FX-ASR-14a", "period-X pottery present", pol="asserted"); support("FX-ASR-14a", "FX-ATT-14a")
    att("FX-ATT-14b", prov="archaeological_evidence"); asr("FX-ASR-14b", "period-Y pottery absent", pol="denied"); support("FX-ASR-14b", "FX-ATT-14b")
    s.add("event", "FX-EVT-14", event_type_primary="investigation", event_type_sub="excavation",
          detection_scope={"periods": ["Y"], "materials": ["ceramic"], "methods": ["excavation"]})
    rel("FX-REL-14ex", "examined", "event", "FX-EVT-14", "site", "FX-SIT-14")  # PROV: examined
    # FX-SIT-14u has NO investigation event (absence of evidence, distinct from denied)
    # FX-RESIDUAL-14: examined-and-found-but-never-entered — NO FX-ASR record exists, by construction.
    s.residual_note = "FX-RESIDUAL-14: period-Z found at FX-SIT-14 during FX-EVT-14 but never entered as an assertion — not representable; deliberately absent."

    # ===================== PART D — +add for register field-2 ===============
    # QR-101 non-pass feature + traverses/crosses_at [PROV]
    thing("FX-LFT-101", "landscape_feature", "River-101", feature_type="river", origin="natural")
    rel("FX-REL-101a", "traverses", "route", "FX-RTE-18t", "landscape_feature", "FX-LFT-101")   # PROV
    rel("FX-REL-101b", "crosses_at", "route", "FX-RTE-18t", "landscape_feature", "FX-LFT-101")  # PROV
    rel("FX-REL-102", "overlooks", "site", "FX-SIT-01", "landscape_feature", "FX-LFT-01")       # PROV
    # QR-103 modelled/inferred routes + a route phase
    thing("FX-RTE-103m", "route", "Modelled-103", route_class="modelled"); thing("FX-RTE-103i", "route", "Inferred-103", route_class="inferred")
    phase("FX-PHA-103", "route", "FX-RTE-18t", 700, 800)
    # QR-104 gis-derived route assertion
    spatial_assertion("FX-SPA-104m", "LINESTRING", "route", "FX-RTE-103m", prov="gis_derived_observation")
    # QR-202 functional assertion + att
    att("FX-ATT-202"); asr("FX-ASR-202", "function of phase", kind="functional"); support("FX-ASR-202", "FX-ATT-202")
    # QR-203 rank + subordinate hierarchy [PROV subordinate_to]
    thing("FX-SIT-203sub", "site", "Subordinate-203")
    rel("FX-REL-203", "subordinate_to", "site", "FX-SIT-203sub", "site", "FX-SIT-01")           # PROV
    # QR-204 canal + adjoins/near
    thing("FX-LFT-204canal", "landscape_feature", "Canal-204", feature_type="canal", origin="anthropogenic")
    rel("FX-REL-204a", "adjoins", "site", "FX-SIT-01", "landscape_feature", "FX-LFT-204canal")
    rel("FX-REL-204n", "near", "site", "FX-SIT-01", "site", "FX-SIT-02")
    # QR-205 argued group [PROV member_of_argued_group]
    interp("FX-INT-205", "S4", argument="defensive triad"); att("FX-ATT-205"); interp_ev("FX-INT-205", "FX-ATT-205")
    rel("FX-REL-205a", "member_of_argued_group", "site", "FX-SIT-01", "interpretation", "FX-INT-205")   # PROV
    rel("FX-REL-205b", "member_of_argued_group", "site", "FX-SIT-17", "interpretation", "FX-INT-205")   # PROV
    rel("FX-REL-205c", "member_of_argued_group", "site", "FX-SIT-19", "interpretation", "FX-INT-205")   # PROV
    # QR-301 military event + produced/terminated/damaged [PROV]
    s.add("event", "FX-EVT-301", event_type_primary="military", start_date=838, end_date=838)
    rel("FX-REL-301t", "terminated_phase", "event", "FX-EVT-301", "phase", "FX-PHA-19a")        # PROV
    rel("FX-REL-301p", "produced_phase", "event", "FX-EVT-301", "phase", "FX-PHA-19b")          # PROV
    rel("FX-REL-301d", "damaged", "event", "FX-EVT-301", "site", "FX-SIT-19")                   # PROV
    # QR-302 polity, admin event, belongs_to/held_by [PROV], TER boundary geom
    s.add("polity", "FX-POL-302", standardised_name="Caliphate", identification_confidence=5)
    s.add("event", "FX-EVT-302", event_type_primary="administrative", start_date=786, end_date=786)
    thing("FX-SIT-302", "site", "AdminSeat-302")
    spatial_assertion("FX-SPA-302", "POLYGON", "territorial_unit", "FX-TER-16a")
    rel("FX-REL-302b", "belongs_to", "site", "FX-SIT-302", "territorial_unit", "FX-TER-16a")
    rel("FX-REL-302h", "held_by", "territorial_unit", "FX-TER-16a", "polity", "FX-POL-302")
    # QR-303 economic event + canal contains/depends_on + mill component
    s.add("event", "FX-EVT-303", event_type_primary="construction_infrastructure", start_date=770, end_date=770)
    s.add("component", "FX-CMP-303mill", parent_site="FX-SIT-19", component_type="workshop")
    rel("FX-REL-303c", "contains", "site", "FX-SIT-19", "component", "FX-CMP-303mill")
    rel("FX-REL-303d", "depends_on", "site", "FX-SIT-19", "landscape_feature", "FX-LFT-204canal")
    att("FX-ATT-303"); asr("FX-ASR-303", "irrigation sustains settlement"); support("FX-ASR-303", "FX-ATT-303")
    # QR-304 environmental event
    s.add("event", "FX-EVT-304", event_type_primary="environmental", start_date=749, end_date=749)
    rel("FX-REL-304", "damaged", "event", "FX-EVT-304", "site", "FX-SIT-01")
    # QR-305 mechanism-bearing event + assertion [PROV: uses ratified 'diplomacy']
    s.add("event", "FX-EVT-305", event_type_primary="diplomatic", interaction_mechanism=["diplomacy"], start_date=800, end_date=800)
    s.add("person", "FX-PER-305", standardised_name="Envoy", identification_confidence=3)
    att("FX-ATT-305"); asr("FX-ASR-305", "prisoner exchange occurred"); support("FX-ASR-305", "FX-ATT-305")
    s.assertion["FX-ASR-305"]["interaction_mechanism"] = ["diplomacy"]
    # QR-401 multi-source assertion (3 atts, 2 sources, one mediated)
    att("FX-ATT-401a", src="FX-SRC-1"); att("FX-ATT-401b", src="FX-SRC-1"); att("FX-ATT-401c", src="FX-SRC-2", citation_mediation="reached via al-X")
    asr("FX-ASR-401", "multiply attested claim"); support("FX-ASR-401", "FX-ATT-401a", "FX-ATT-401b", "FX-ATT-401c")
    s.attestation["FX-ATT-401c"]["citation"] = "Y, reached via al-X"
    # QR-402 mediation attestation
    att("FX-ATT-402med", prov="primary_quotation"); s.attestation["FX-ATT-402med"]["citation"] = "Z, reached via al-W"
    asr("FX-ASR-402", "provenance-chain claim"); support("FX-ASR-402", "FX-ATT-402med")
    # QR-403 corroborates/parallel_case [PROV]
    interp("FX-INT-403a", "S5"); interp("FX-INT-403b", "S6")
    att("FX-ATT-403"); interp_ev("FX-INT-403a", "FX-ATT-403"); interp_ev("FX-INT-403b", "FX-ATT-403")
    rel("FX-REL-403co", "corroborates", "interpretation", "FX-INT-403a", "interpretation", "FX-INT-403b")   # PROV
    rel("FX-REL-403p", "parallel_case", "interpretation", "FX-INT-403a", "interpretation", "FX-INT-403b")   # PROV
    # QR-501 gis-derived output assertion (intervisible_with inputs-only)
    spatial_assertion("FX-SPA-501out", "LINESTRING", "site", "FX-SIT-01", prov="gis_derived_observation")
    # QR-502 region temporal extent
    s.add("analytical_region", "FX-RGN-502", author="R", name="win", version="1",
          membership_mode="extensional", member_list=["FX-SIT-01"], temporal_extent=(700, 900))
    # QR-503 investigation survey event + examined [PROV] + three region modes
    s.add("event", "FX-EVT-503survey", event_type_primary="investigation", event_type_sub="survey",
          detection_scope={"periods": ["all"], "materials": ["surface"], "methods": ["survey"]})
    rel("FX-REL-503", "examined", "event", "FX-EVT-503survey", "site", "FX-SIT-14u")            # PROV
    s.add("analytical_region", "FX-RGN-503e", author="R", name="ext", version="1", membership_mode="extensional", member_list=["FX-SIT-14", "FX-SIT-14u"], temporal_extent=None)
    s.add("analytical_region", "FX-RGN-503i", author="R", name="int", version="1", membership_mode="intensional", boundary="poly", predicate="within", temporal_extent=None)
    s.add("analytical_region", "FX-RGN-503h", author="R", name="hyb", version="1", membership_mode="hybrid", member_list=["FX-SIT-14"], boundary="poly", temporal_extent=None)

    # --- ensure every domain entity is evidenced (I1) via a definite subject link ---
    _evidence_all_domain_entities(s)
    # --- I3: every attestation supports >=1 assertion (incl. name/interp/deprecated atts) ---
    _support_all_attestations(s)
    return s


def _support_all_attestations(s):
    """I3: every attestation supports at least one assertion. Name-attestations,
    interpretation-evidence attestations, and the deprecated ATT-12 support propositions
    too (a name IS a proposition about the entity; a deprecated attestation still made a
    claim). Wrap each orphan attestation in a minimal assertion. Fixture bookkeeping that
    realises the manifest's 'every FX-ATT carries source+provenance by construction' and
    the model's I3 (every attestation supports >=1 assertion)."""
    supported = {a for (_, a) in s.supporting_attestations}
    n = 0
    for at in list(s.attestation):
        if at in supported:
            continue
        n += 1
        asrid = f"FX-ASR-wrap{n}"
        # a deprecated attestation supports a (correspondingly deprecated) assertion;
        # for others, a general asserted proposition.
        dep = s.attestation[at].get("workflow_state") == "deprecated"
        s.add("assertion", asrid, proposition=f"claim of {at}",
              assertion_kind="general", assertion_polarity="asserted")
        if dep:
            s.assertion[asrid]["workflow_state"] = "deprecated"
        s.supporting_attestations.append((asrid, at))
        supported.add(at)


def _evidence_all_domain_entities(s):
    """I1: every domain entity referenced by >=1 attestation via a definite QSL.
    Adds one definite link per otherwise-unlinked domain entity (fixture bookkeeping,
    mirrors the manifest's 'every entity has >=1 attestation by construction')."""
    linked = {(l["subject_type"], l["subject_id"]) for l in s.qualified_subject_link.values()}
    n = 0
    def ensure(tp, id):
        nonlocal n
        if (tp, id) in linked:
            return
        n += 1
        at = f"FX-ATT-ev{n}"
        s.add("attestation", at, source="FX-SRC-1", citation="fixture", paraphrase="exists",
              provenance_category="primary_paraphrase", evidential_confidence=3)
        asrid = f"FX-ASR-ev{n}"
        s.add("assertion", asrid, proposition=f"{tp} {id} exists", assertion_kind="general", assertion_polarity="asserted")
        s.supporting_attestations.append((asrid, at))
        s.add("qualified_subject_link", f"FX-QSL-ev{n}", attestation=at, subject_type=tp,
              subject_id=id, reference_mode="definite", identification_confidence=3)
        linked.add((tp, id))
    for tp in ("site", "landscape_feature", "route", "territorial_unit"):
        for id in list(getattr(s, tp)):
            ensure(tp, id)
    for tp in ("component", "event", "polity", "person"):
        for id in list(getattr(s, tp)):
            ensure(tp, id)
