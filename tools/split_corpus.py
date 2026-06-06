#!/usr/bin/env python3
"""Split a single YAML corpus file into one-record-per-file by type."""
import sys
import yaml
from pathlib import Path

TYPE_DIRS = {
    "source": "sources", "place": "places", "person": "persons",
    "event": "events", "observation": "observations",
    "attestation": "attestations", "interpretation": "interpretations",
    "relationship": "relationships",
}

if len(sys.argv) != 3:
    print("Usage: split_corpus.py <input.yaml> <records-dir>", file=sys.stderr)
    sys.exit(1)

corpus = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(sys.argv[2])
for rec in corpus:
    if not isinstance(rec, dict) or "id" not in rec:
        continue
    rtype = rec.get("record_type", "")
    subdir = TYPE_DIRS.get(rtype, "misc")
    target = out / subdir / f"{rec['id']}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump([rec], allow_unicode=True, sort_keys=False), encoding="utf-8")

print(f"Split {len(corpus)} records into {out}/")
