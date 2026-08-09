#!/usr/bin/env python3
"""
Migration Step-1 validator suite — I2, I3, I5, I5a, I5b, I11, plus the ratified-vocabulary
validator that PARSES byzfrontier_vocabularies_v1_1.ttl as the single source of truth.

Run against the live corpus at the step-1 tip to CONFIRM the plan's predicted pre-remediation
counts. This suite moves no record; it reads records/ and reports counts. A count that does
not match its prediction is a finding to report before commit, not to reconcile silently.

check-first-then-data: step 1 builds these and confirms the numbers; later passes drive the
remediable ones (I3 -> 0 at step 5; I5/I5a at step 6) to their targets.

rdflib dependency (Board environment note):
  The vocabulary validator needs to parse Turtle. rdflib is NOT installed in the Editorial
  Board's environment. This suite is EXPLICIT about that:
    - the six record invariants (I2, I3, I5, I5a, I5b, I11) use ONLY the standard library
      plus PyYAML, which the corpus already requires — they run with no extra dependency;
    - the vocabulary validator tries rdflib first (full SKOS parse); if rdflib is absent it
      falls back to a SELF-CONTAINED minimal Turtle reader (parse_ratified_terms_fallback)
      that reads the relationship-types skos:inScheme members directly. Either path reads the
      TTL as the source of truth — NEITHER hardcodes the term list. The suite therefore runs
      end to end whether or not rdflib is present, and says which path it used.

Usage:
  python3 run_step1_validators.py [--records DIR] [--ttl PATH]
  Exit 0 iff every predicted count matches; non-zero (with a FINDINGS block) otherwise.
"""
import sys, os, glob, argparse, re

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required (the corpus already depends on it): pip install pyyaml\n")
    sys.exit(2)


# ---- predicted pre-remediation counts (from the migration plan) --------------
PREDICTED = {
    "I2":  0,     # attestation claim non-empty
    "I5b": 0,     # observation_date iff primary_observation
    "I3":  208,   # attestations supporting no assertion  (step-5 target: 0)
    "I11": 0,     # <=1 designated spatial + <=1 designated temporal per subject (structural)
    # I5 and I5a are "report whatever is found" (step-6 targets), not fixed predictions:
    "I5":  None,
    "I5a": None,
}


def load(path):
    d = yaml.safe_load(open(path, encoding="utf-8"))
    return d[0] if isinstance(d, list) else d


def load_corpus(records_dir):
    def coll(name):
        return [load(p) for p in glob.glob(os.path.join(records_dir, name, "*.yaml"))]
    return {
        "attestations":   coll("attestations"),
        "observations":   coll("observations"),   # = assertions pre-M1-rename
        "interpretations":coll("interpretations"),
        "places":         coll("places"),
        "relationships":  coll("relationships"),
    }


# ---- the six record invariants (stdlib + PyYAML only) ------------------------

def check_I2(c):
    """Attestation claim non-empty: paraphrase OR direct_quotation present."""
    v = [a["id"] for a in c["attestations"]
         if not ((a.get("paraphrase") or "").strip() or (a.get("direct_quotation") or "").strip())]
    return v

def check_I5b(c):
    """observation_date present IFF provenance == primary_observation."""
    v = []
    for a in c["attestations"]:
        has_od = a.get("observation_date") is not None
        is_po = a.get("provenance") == "primary_observation"
        if has_od != is_po:
            v.append(a["id"])
    return v

def check_I3(c):
    """Every attestation supports >=1 assertion: its id appears in some observation's
    supporting_attestations. (Measured observation-side, the corpus's actual link direction.)"""
    supported = set()
    for o in c["observations"]:
        for aid in (o.get("supporting_attestations") or []):
            supported.add(aid)
    return [a["id"] for a in c["attestations"] if a["id"] not in supported]

def check_I5(c):
    """Interpretation evidence non-empty AND ATT-only (rule 9).
    Pre-migration: the corpus has no structured supporting_evidence field yet — interpretations
    carry associated_entities (ENT- subjects) and publication_source_id, not attestation evidence.
    So every interpretation currently lacks structured ATT- evidence: this is the M6 rule-9
    back-fill gap, reported here as the step-6 target."""
    v = []
    for i in c["interpretations"]:
        ev = i.get("supporting_evidence") or []
        att_only = ev and all(str(e).startswith("ATT-") for e in ev)
        if not att_only:
            v.append(i["id"])
    return v

def check_I5a(c):
    """Flag-class: an interpretation naming another INT- in prose (argument/notes) with no
    corresponding relationship linking them. Reported as a flag count (step-6/7 target)."""
    rel_pairs = set()
    for r in c["relationships"]:
        st = (r.get("source_entity") or r.get("source") or "")
        tt = (r.get("target_entity") or r.get("target") or "")
        rel_pairs.add((str(st), str(tt)))
    flags = []
    for i in c["interpretations"]:
        prose = str(i.get("argument", "")) + " " + str(i.get("notes", ""))
        named = set(re.findall(r"INT-\d{4}", prose)) - {i["id"]}
        for n in named:
            if (i["id"], n) not in rel_pairs and (n, i["id"]) not in rel_pairs:
                flags.append((i["id"], n))
    return flags

def check_I11(c):
    """Structural in v3: designated_spatial_assertion / designated_temporal_assertion are
    single-valued FK columns and cannot point at two. Confirmed by SHAPE: any record whose
    designated pointer is a list (not a scalar id or null) is a violation. In a conforming v3
    corpus this is 0 by construction; measured here to confirm the schema shape holds."""
    v = []
    for p in c["places"]:
        for f in ("designated_spatial_assertion", "designated_temporal_assertion"):
            val = p.get(f)
            if val is not None and not isinstance(val, str):
                v.append((p.get("id"), f))
    return v


# ---- vocabulary validator: parse the TTL as source of truth ------------------

def parse_ratified_terms_rdflib(ttl_path):
    import rdflib
    g = rdflib.Graph(); g.parse(ttl_path, format="turtle")
    SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    V = rdflib.Namespace("https://byzantine-frontier-db.org/vocab/")
    scheme = V["relationship-types"]
    terms = set()
    for s, _, _ in g.triples((None, SKOS.inScheme, scheme)):
        local = str(s).replace(str(V), "")
        if local.startswith("r-"):
            terms.add(local[2:].replace("-", "_"))
    return terms, len(g)

def parse_ratified_terms_fallback(ttl_path):
    """Self-contained minimal Turtle reader for the relationship-types members.
    Reads lines of the file's own convention:
        :r-<name> a skos:Concept ; skos:inScheme :relationship-types ; skos:prefLabel "..."@en .
    No rdflib. Still reads the TTL as source of truth — no hardcoded term list."""
    terms = set()
    triple_lines = 0
    for line in open(ttl_path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("@prefix") or line.startswith("#"):
            continue
        triple_lines += 1
        m = re.match(r":r-([a-z0-9-]+)\s+a\s+skos:Concept", line)
        if m and ":relationship-types" in line:
            terms.add(m.group(1).replace("-", "_"))
    return terms, triple_lines

def load_ratified_terms(ttl_path):
    """Returns (terms, backend, detail). Tries rdflib, falls back to the self-contained reader."""
    try:
        import rdflib  # noqa
        terms, n = parse_ratified_terms_rdflib(ttl_path)
        return terms, "rdflib", f"{n} triples"
    except ImportError:
        terms, n = parse_ratified_terms_fallback(ttl_path)
        return terms, "self-contained fallback (rdflib absent)", f"{n} triple-lines scanned"

def check_relationship_vocab(c, ratified_terms):
    """Step-7 relationship-vocabulary check, built here so step 1 carries it.
    Every relationship's rel_type must be a ratified term. Reported here as informational
    (step 7 remediates); the point at step 1 is that the validator PARSES the TTL and does not
    hardcode. NOTE: pre-migration relationships use the existing v1/v2 enum, most of which are
    ratified vocabulary members; this reports any rel_type absent from the TTL."""
    unratified = {}
    for r in c["relationships"]:
        rt = (r.get("type") or r.get("rel_type") or "").replace("-", "_")
        if rt and rt not in ratified_terms:
            unratified[rt] = unratified.get(rt, 0) + 1
    return unratified


# ---- runner ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--records", default=os.path.join(here, "..", "..", "records"))
    ap.add_argument("--ttl", default=os.path.join(here, "..", "..", "vocabularies", "byzfrontier_vocabularies_v1_1.ttl"))
    args = ap.parse_args()

    c = load_corpus(args.records)
    print("=" * 72)
    print("MIGRATION STEP-1 VALIDATOR SUITE — confirming predicted pre-remediation counts")
    print("=" * 72)
    print(f"corpus: {len(c['attestations'])} attestations, {len(c['observations'])} assertions(observations), "
          f"{len(c['interpretations'])} interpretations, {len(c['relationships'])} relationships\n")

    results = {
        "I2":  check_I2(c),
        "I5b": check_I5b(c),
        "I3":  check_I3(c),
        "I5":  check_I5(c),
        "I5a": check_I5a(c),
        "I11": check_I11(c),
    }

    findings = []
    print("### Record invariants (stdlib + PyYAML only — no extra dependency)")
    for k in ("I2", "I5b", "I3", "I11", "I5", "I5a"):
        n = len(results[k]); pred = PREDICTED[k]
        if pred is None:
            print(f"  {k:4} = {n:4}   [report -> step-6 target]")
        else:
            ok = (n == pred)
            tag = "MATCH" if ok else "DIVERGENCE"
            print(f"  {k:4} = {n:4}   [predicted {pred}]  {tag}")
            if not ok:
                findings.append((k, n, pred))

    print("\n### Vocabulary validator (parses the TTL — single source of truth)")
    terms, backend, detail = load_ratified_terms(args.ttl)
    print(f"  backend: {backend}  ({detail})")
    print(f"  ratified relationship terms read from TTL: {len(terms)}")
    print(f"  five step-5 ratifications present: "
          f"{sorted(t for t in terms if t in ('controls','overlooks','member_of_argued_group','corroborates','sited_at_crossing'))}")
    unrat = check_relationship_vocab(c, terms)
    if unrat:
        print(f"  relationship rel_types not in TTL (step-7 remediation target): {dict(sorted(unrat.items()))}")
    else:
        print(f"  every existing relationship rel_type is a ratified TTL term")

    print("\n" + "=" * 72)
    if findings:
        print("FINDINGS — counts diverging from prediction (report BEFORE commit):")
        for k, n, pred in findings:
            print(f"  {k}: got {n}, predicted {pred} — check whether the corpus moved or the validator measures differently")
        print("=" * 72)
        return 1
    print("ALL PREDICTED COUNTS CONFIRMED. I3=208 anchored for step-5 closure. No record moved.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
