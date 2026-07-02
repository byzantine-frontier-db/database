#!/usr/bin/env python3
"""
export_geojson.py — export place records as a GeoJSON FeatureCollection.

Read-only and idempotent. Walks records/places/*.yaml, emits every place that has
usable geometry as a GeoJSON Feature on stdout (RFC 7946, WGS84 / EPSG:4326).

Geometry:
  - Point from the `coordinates` block (the v1 case).
  - Polygon / MultiPolygon from `temporal_polygons` if present (v2 FuzzyRegion).
    No live record carries these yet; support is forward-compatible.

Feature properties: canonical_id, standardised_name, place_type,
identification_confidence, overall_confidence, linked_attestations_count
(a quick "evidence weight" indicator for visualization).

Usage:
    python tools/export_geojson.py > places.geojson
    python tools/export_geojson.py --stats > places.geojson     # stats to stderr
    python tools/export_geojson.py --output places.geojson       # write to file
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

PLACES_DIR = Path(__file__).resolve().parent.parent / "records" / "places"


def is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def coordinate_issue(coords: dict):
    """Return a human-readable reason string if the coordinates block is malformed,
    else None. Belt-and-suspenders: schema validation should already exclude these."""
    lat, lon = coords.get("latitude"), coords.get("longitude")
    if (lat is None) ^ (lon is None):
        return f"partial coordinates (lat={lat!r}, lon={lon!r})"
    if not is_number(lat):
        return f"latitude not numeric: {lat!r}"
    if not is_number(lon):
        return f"longitude not numeric: {lon!r}"
    if not -90 <= lat <= 90:
        return f"latitude out of range: {lat}"
    if not -180 <= lon <= 180:
        return f"longitude out of range: {lon}"
    crs = coords.get("crs")
    if crs not in (None, "EPSG:4326"):
        return f"unexpected crs: {crs!r} (expected EPSG:4326)"
    return None


def build_geometry(rec: dict):
    """Point from coordinates, or Polygon/MultiPolygon from temporal_polygons.
    Returns (geometry_dict, None) on success or (None, reason) if unusable."""
    tps = rec.get("temporal_polygons")
    if tps:  # v2 FuzzyRegion — prefer polygon geometry when present
        rings = []
        for tp in tps:
            poly = (tp or {}).get("polygon") or {}
            coords = poly.get("coordinates")
            if coords:
                rings.append(coords)
        if not rings:
            return None, "temporal_polygons present but no polygon coordinates"
        if len(rings) == 1:
            return {"type": "Polygon", "coordinates": rings[0]}, None
        return {"type": "MultiPolygon", "coordinates": rings}, None

    coords = rec.get("coordinates")
    if not coords:
        return None, "no coordinates"
    issue = coordinate_issue(coords)
    if issue:
        return None, issue
    # GeoJSON is [longitude, latitude]
    return {"type": "Point", "coordinates": [coords["longitude"], coords["latitude"]]}, None


def build_feature(rec: dict, geometry: dict) -> dict:
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "canonical_id": rec.get("id"),
            "standardised_name": rec.get("standardised_name"),
            "place_type": rec.get("place_type"),
            "identification_confidence": rec.get("identification_confidence"),
            "overall_confidence": rec.get("overall_confidence"),
            "linked_attestations_count": len(rec.get("linked_attestations") or []),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Export place records as GeoJSON.")
    ap.add_argument("--stats", action="store_true",
                    help="Report coverage statistics to stderr.")
    ap.add_argument("--output", metavar="PATH",
                    help="Write GeoJSON to PATH instead of stdout.")
    args = ap.parse_args()

    if not PLACES_DIR.is_dir():
        sys.exit(f"places directory not found: {PLACES_DIR}")

    features, without_geom, malformed = [], [], []
    total = 0
    for f in sorted(PLACES_DIR.glob("*.yaml")):
        docs = yaml.safe_load(f.read_text(encoding="utf-8"))
        for rec in (docs if isinstance(docs, list) else [docs]):
            total += 1
            geom, reason = build_geometry(rec)
            if geom is None:
                if reason == "no coordinates":
                    without_geom.append(rec.get("id"))
                else:
                    malformed.append((rec.get("id"), reason))
                continue
            features.append(build_feature(rec, geom))

    # Deterministic ordering -> idempotent output, stable diffs.
    features.sort(key=lambda ft: ft["properties"]["canonical_id"] or "")
    fc = {"type": "FeatureCollection", "features": features}

    out = json.dumps(fc, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)

    if args.stats:
        with_geom = len(features)
        pct = (with_geom / total * 100) if total else 0.0
        s = sys.stderr
        print("--- GeoJSON export statistics ---", file=s)
        print(f"  place records total:       {total}", file=s)
        print(f"  exported (had geometry):   {with_geom} ({pct:.1f}%)", file=s)
        print(f"  no coordinates:            {len(without_geom)}", file=s)
        print(f"  malformed coordinates:     {len(malformed)}", file=s)
        if malformed:
            print("  malformed detail:", file=s)
            for rid, reason in malformed:
                print(f"    {rid}: {reason}", file=s)
        # coverage-to-target guidance
        for target in (0.90,):
            need = max(0, round(target * total) - with_geom)
            print(f"  to reach {int(target*100)}% coverage: "
                  f"+{need} places need coordinates", file=s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
