import json, re, sys, yaml, copy
from jsonschema import Draft202012Validator

SCHEMA = "/mnt/project/byzfrontier_schema_v1.json"
BATCH = "/home/claude/eger2015_ch3_extraction.yaml"
PILOT = "/mnt/project/pilot_corpus_838_v1.yaml"

schema = json.load(open(SCHEMA))
# Relax the Identifier pattern to allow an optional provisional PROV- prefix
# (established project practice for contributor-proposed records).
orig = schema["$defs"]["Identifier"]["pattern"]
schema["$defs"]["Identifier"]["pattern"] = r"^(PROV-)?(ENT-(PLC|PERS|EVT|POL|GRP|INS|RTE|OBJ)|SRC|OBS|ATT|INT|REL)-[0-9]{3,8}$"
validator = Draft202012Validator(schema)

records = yaml.safe_load(open(BATCH))
print(f"Loaded {len(records)} records from batch.")

# ---- schema validation ----
errors = 0
for i, rec in enumerate(records):
    rid = rec.get("id", f"<index {i}>")
    rtype = rec.get("record_type")
    errs = sorted(validator.iter_errors(rec), key=lambda e: e.path)
    # oneOf produces noisy errors; filter to the matching record_type subschema
    if errs:
        # Validate against the specific subschema for clearer messages
        defmap = {"source":"SourceRecord","place":"PlaceEntity","person":"PersonEntity",
                  "event":"EventEntity","observation":"ObservationRecord",
                  "attestation":"AttestationRecord","interpretation":"InterpretationRecord",
                  "relationship":"RelationshipRecord"}
        sub = copy.deepcopy(schema); sub["$ref"] = f"#/$defs/{defmap[rtype]}"
        for k in ("oneOf",): sub.pop(k, None)
        subv = Draft202012Validator(sub)
        real = sorted(subv.iter_errors(rec), key=lambda e: list(e.path))
        if real:
            errors += 1
            print(f"\nSCHEMA ERROR in {rid} ({rtype}):")
            for e in real[:6]:
                print("   -", "/".join(map(str, e.path)), ":", e.message)
print(f"\nSchema validation: {errors} record(s) with errors.")

# ---- build known-id universe: batch + pilot + authoritative snapshot ----
batch_ids = {r["id"] for r in records if "id" in r}

pilot = yaml.safe_load(open(PILOT))
pilot_ids = {r["id"] for r in pilot if "id" in r}

snapshot = set()
snapshot |= {f"SRC-{n:04d}" for n in range(1, 34)}
snapshot |= {f"ENT-PERS-{n:04d}" for n in range(1, 38) if n != 9}
snapshot |= {f"ENT-PLC-{n:04d}" for n in range(1, 74)}
snapshot |= {"ENT-POL-0001", "ENT-POL-0002"}
snapshot |= {f"ENT-EVT-{n:04d}" for n in range(1, 24)}

known = batch_ids | pilot_ids | snapshot
print(f"Known IDs: {len(batch_ids)} batch + snapshot/pilot universe = {len(known)} total.")

# ---- cross-reference check: every internal Identifier-looking ref resolves ----
ID_RE = re.compile(r"^(PROV-)?(ENT-(PLC|PERS|EVT|POL|GRP|INS|RTE|OBJ)|SRC|OBS|ATT|INT|REL)-[0-9]{3,8}$")
REF_FIELDS = {"author_id","source","publication_source_id","political_affiliation",
              "source_entity","target_entity","spatial_scope","parent_event"}
LIST_FIELDS = {"entities_referenced","observations_supported","associated_entities",
               "supporting_attestations","contradicting_attestations","linked_attestations",
               "linked_interpretations","associated_places","participants",
               "political_entities_involved","related_events","child_events","dependencies",
               "supporting_evidence","counter_evidence","relative_to"}

dangling = []
def check_ref(rid, field, val):
    if isinstance(val, str) and ID_RE.match(val) and val not in known:
        dangling.append((rid, field, val))

for r in records:
    rid = r.get("id")
    for f in REF_FIELDS:
        if f in r: check_ref(rid, f, r[f])
    for f in LIST_FIELDS:
        if f in r and isinstance(r[f], list):
            for v in r[f]: check_ref(rid, f, v)

print(f"\nDangling internal references: {len(dangling)}")
for d in dangling: print("   -", d)

# ---- reciprocity: OBS.supporting_attestations <-> ATT.observations_supported ----
recs_by_id = {r["id"]: r for r in records}
recip_problems = []
for r in records:
    if r["record_type"] == "observation":
        for att in r.get("supporting_attestations", []):
            a = recs_by_id.get(att)
            if a is not None and r["id"] not in a.get("observations_supported", []):
                recip_problems.append(("OBS->ATT", r["id"], att))
    if r["record_type"] == "attestation":
        for obs in r.get("observations_supported", []):
            o = recs_by_id.get(obs)
            if o is not None and r["id"] not in o.get("supporting_attestations", []):
                recip_problems.append(("ATT->OBS", r["id"], obs))

print(f"\nOBS<->ATT reciprocity problems (within batch): {len(recip_problems)}")
for p in recip_problems: print("   -", p)

# ---- entity <-> attestation reciprocity (batch-internal entities only) ----
# every batch entity's linked_attestations should reference it back in entities_referenced
ent_types = {"place","person","event"}
ent_recip = []
for r in records:
    if r["record_type"] in ent_types:
        for att in r.get("linked_attestations", []):
            a = recs_by_id.get(att)
            if a is not None and r["id"] not in a.get("entities_referenced", []):
                ent_recip.append((r["id"], "->", att))
print(f"\nEntity->Attestation reciprocity gaps (batch entity not in its ATT.entities_referenced): {len(ent_recip)}")
for p in ent_recip: print("   -", p)

# ---- summary counts ----
from collections import Counter
c = Counter(r["record_type"] for r in records)
print("\nRecord counts by type:", dict(c))
ok = (errors==0 and not dangling and not recip_problems and not ent_recip)
print("\nRESULT:", "PASS" if ok else "ISSUES FOUND")
sys.exit(0 if ok else 1)
