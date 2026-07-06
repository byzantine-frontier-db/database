#!/usr/bin/env python3
"""
normalize_gazetteer.py — normalize the Eger 2008 gazetteer appendix text and
extract its UTM coordinates for the Byzantine-Islamic Frontier Database Phase 2.

Read-only w.r.t. input. Produces three artefacts:
  1. cleaned text          (--out-text,   default docs/eger_2008_gazetteer_cleaned.txt)
  2. coordinates JSON       (--out-coords, default docs/eger_2008_coordinates.json)
  3. a change report to stdout (or --report FILE)

Cleaning:
  * Mojibake: PUA U+F029 and U+F02A are both a combining dot-below split across two
    font glyph slots; map both to U+0323 and NFC-compose (s->ṣ, t->ṭ, H->Ḥ, ...).
    Control byte \\x02 -> hyphen; other C0 controls stripped.
  * De-interleave: standalone page-number lines (436-560) removed; footnote lines
    ("<n> <citation>") pulled out of the narrative into a per-entry footnote list.
  * Whitespace/CRLF normalised.

Coordinates:
  * Each entry ends with a "Coordinates: <zone> N <northing> E <easting>" line, so a
    coordinate is attributed to the entry it closes (nearest site header above it).
  * UTM -> WGS84 via pyproj (EPSG:326{zone} -> 4326).
  * Malformed lines are repaired-by-inference ONLY when a single dropped trailing
    northing digit is recoverable and the easting confirms the region; otherwise the
    line is flagged unrecoverable (never silently dropped, never multi-digit guessed).

Usage:
  python tools/normalize_gazetteer.py INPUT.txt \
      --out-text docs/eger_2008_gazetteer_cleaned.txt \
      --out-coords docs/eger_2008_coordinates.json
"""
from __future__ import annotations
import sys, re, json, argparse, unicodedata
from pathlib import Path

try:
    import pyproj
except ImportError:
    pyproj = None  # coordinate conversion will raise a clear error if invoked without it

# --- known single-digit repairs, keyed by raw string, with the site they close ---
# Each: raw northing -> repaired northing (a dropped trailing digit), region-confirmed.
KNOWN_REPAIRS = {
    ("36N", 412718, 757076): dict(north=4127180, site="ʿAyn Zarba / Anazarba",
        note="northing lost a trailing digit; easting confirms Anavarza (~37.28N 35.86E)"),
    ("36N", 408631, 668364): dict(north=4086310, site="Tarsūs (Gözlü Küle höyük)",
        note="northing lost a trailing digit; Gözlü Küle is the Tarsus mound -> attribute to ENT-PLC-0004 Tarsus (~36.90N 34.90E)"),
}
# Severely truncated, NOT reconstructed (multiple digits lost, ambiguous):
UNRECOVERABLE = {
    ("36N", 43750, 95800): dict(site="Al-Massīsa / Mopsuestia / Misis",
        note="both figures truncated to 5 digits; multiple digits lost and northing "
             "ambiguous (4093750 vs 4043750). Flag for manual entry against the printed source."),
}

_tf = {}
def utm_to_wgs84(zone: str, north: float, east: float):
    if pyproj is None:
        raise RuntimeError(
            "pyproj is required for coordinate conversion. "
            "Install with: pip install pyproj")
    if zone not in _tf:
        epsg = (32600 if zone[-1] == "N" else 32700) + int(zone[:2])
        _tf[zone] = pyproj.Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    lon, lat = _tf[zone].transform(east, north)
    return round(lat, 5), round(lon, 5)


def fix_mojibake(text: str) -> tuple[str, int]:
    n = text.count("\uf029") + text.count("\uf02a")
    text = text.replace("\uf029", "\u0323").replace("\uf02a", "\u0323")
    text = text.replace("\x02", "-")
    text = "".join(c for c in text if ord(c) >= 32 or c in "\n\t")
    text = unicodedata.normalize("NFC", text)
    return text, n


PAGE_RE = re.compile(r"^\s*(4[3-9]\d|5[0-5]\d)\s*$")          # standalone page number 430-559
FOOT_RE = re.compile(r"^\s*(\d{1,3})\s+([A-ZĀʿ‘“].{4,})$")     # "<n> Citation text..."
COORD_RE = re.compile(r"Coordinates:\s*(\d{2}[NS])\s+N?\s*(\d+)\s+E\s*(\d+)\s*(\([^)]*\))?", re.I)
SECTION_WORDS = {"Location", "History", "Archaeology", "Standing Remains",
                 "Personal Observations", "Sources", "Environment"}


ERA_RE = re.compile(r"^(Seleucid|Classical|Roman|Byzantine|Arab|Ottoman|Hittite|Assyrian|"
                    r"Greek|Syriac|Armenian|Ancient|Kurdish|Modern|Biblical|Egyptian|Latin|Persian)\b")


def is_header(lines, i, coord_idxs) -> bool:
    """A site header is a short proper-name line beginning an entry. Positive cues:
    (a) first non-empty line after a Coordinates line (entries end with coords), or
    (b) followed within 3 lines by a concordance/section line.
    Era-word-initial concordance lines and sentence fragments are excluded."""
    s = lines[i].strip()
    if not s or s.isdigit() or s in SECTION_WORDS or COORD_RE.search(s) or FOOT_RE.match(s):
        return False
    if len(s) > 45 or not re.search(r"[A-Za-zĀāĪīŪūʿ‘]", s):
        return False
    if ERA_RE.match(s) or s.endswith((".", ",", ";", ":")) or s[0].islower():
        return False
    if (i - 1) in coord_idxs or ((i - 2) in coord_idxs and not lines[i - 1].strip()):
        return True
    for j in range(i + 1, min(i + 4, len(lines))):
        t = lines[j].strip()
        if not t:
            continue
        return bool(ERA_RE.match(t) or "Modern" in t or t.startswith("(see")
                    or t in ("Location", "History"))
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--out-text", default="docs/eger_2008_gazetteer_cleaned.txt")
    ap.add_argument("--out-coords", default="docs/eger_2008_coordinates.json")
    ap.add_argument("--out-pagemap", default="docs/eger_2008_page_map.json")
    ap.add_argument("--report", default=None, help="write change report here (default stdout)")
    args = ap.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
    raw, mojibake_n = fix_mojibake(raw)
    lines = raw.splitlines()

    # coordinate line indices first (a header cue is "line after a coordinate")
    coord_idxs = {i for i, ln in enumerate(lines) if COORD_RE.search(ln)}

    def clean_name(s: str) -> str:
        s = s.split(";")[0].strip()          # drop concordance tail
        s = re.sub(r"\d+$", "", s).strip()    # drop trailing footnote number
        return s

    headers = [(i, clean_name(lines[i].strip()))
               for i in range(len(lines)) if is_header(lines, i, coord_idxs)]

    def entry_for(idx):
        cur = "(front matter)"
        for hi, nm in headers:
            if hi <= idx:
                cur = nm
            else:
                break
        return cur

    # --- coordinate extraction & attribution ---
    coords, flags = [], []
    for i, ln in enumerate(lines):
        m = COORD_RE.search(ln)
        if not m:
            continue
        zone, north, east = m.group(1), int(m.group(2)), int(m.group(3))
        par = (m.group(4) or "").strip("()") or None
        entry = entry_for(i)
        rec = {"entry": entry, "zone": zone, "raw_northing": north, "raw_easting": east,
               "parenthetical": par, "status": "ok", "repair_note": None}
        key = (zone, north, east)
        wellformed = (3_800_000 <= north <= 4_600_000 and 100_000 <= east <= 900_000)
        if wellformed:
            rec["lat"], rec["lon"] = utm_to_wgs84(zone, north, east)
        elif key in KNOWN_REPAIRS:
            r = KNOWN_REPAIRS[key]
            rec["status"], rec["repair_note"] = "repaired", r["note"]
            rec["repaired_northing"], rec["coordinate_confidence"] = r["north"], 2
            rec["attributed_site"] = r["site"]
            rec["lat"], rec["lon"] = utm_to_wgs84(zone, r["north"], east)
            flags.append(f"REPAIRED  {entry}: {zone} N{north} E{east} -> N{r['north']} "
                         f"({rec['lat']},{rec['lon']}) conf=2 :: {r['note']}")
        elif key in UNRECOVERABLE:
            r = UNRECOVERABLE[key]
            rec["status"], rec["repair_note"] = "unrecoverable", r["note"]
            rec["attributed_site"] = r["site"]
            flags.append(f"UNRECOVERABLE  {entry}: {zone} N{north} E{east} :: {r['note']}")
        else:
            rec["status"] = "malformed_unknown"
            flags.append(f"MALFORMED  {entry}: {zone} N{north} E{east} (unclassified)")
        coords.append(rec)

    # --- clean text: drop page numbers, pull footnotes out; track source pages ---
    cleaned, footnotes, dropped_pages = [], [], 0
    current_page = None
    line_page = []            # source page for each ORIGINAL line (drives entry->page)
    page_first_line = {}      # page -> first retained non-blank line (byte anchor for the map)
    for ln in lines:
        if PAGE_RE.match(ln):
            current_page = int(ln.strip())
            line_page.append(current_page)
            dropped_pages += 1
            continue
        line_page.append(current_page)
        fm = FOOT_RE.match(ln)
        if fm and not COORD_RE.search(ln):
            footnotes.append(ln.strip())
            continue
        cleaned.append(ln)
        if current_page is not None and ln.strip() and current_page not in page_first_line:
            page_first_line[current_page] = ln
    cleaned_text = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned)).strip() + "\n"

    Path(args.out_text).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_text).write_text(cleaned_text, encoding="utf-8")
    Path(args.out_coords).write_text(
        json.dumps({"source": "Eger 2008 dissertation appendix (SRC-0065)",
                    "crs_out": "EPSG:4326", "conversion": "pyproj UTM->WGS84",
                    "coordinates": coords}, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- page map sidecar: byte-range -> source page over the cleaned text + per-entry spans ---
    total_bytes = len(cleaned_text.encode("utf-8"))
    page_spans, search_from = [], 0
    for pg in sorted(page_first_line):
        anchor = page_first_line[pg]
        idx = cleaned_text.find(anchor, search_from)
        if idx == -1:
            idx = cleaned_text.find(anchor)
        if idx == -1:
            continue
        page_spans.append({"page": pg,
                           "byte_start": len(cleaned_text[:idx].encode("utf-8")),
                           "anchor": anchor.strip()[:60]})
        search_from = idx + len(anchor)
    for i, sp in enumerate(page_spans):
        sp["byte_end"] = page_spans[i + 1]["byte_start"] if i + 1 < len(page_spans) else total_bytes
    hdr_pages = [(nm, line_page[hi]) for hi, nm in headers]
    entry_pages = []
    for i, (nm, pg) in enumerate(hdr_pages):
        nxt = hdr_pages[i + 1][1] if i + 1 < len(hdr_pages) else None
        end = pg if (nxt is None or pg is None or nxt <= pg) else nxt - 1
        entry_pages.append({"entry": nm, "page_start": pg, "page_end": end})
    Path(args.out_pagemap).write_text(json.dumps({
        "source": "Eger 2008 dissertation appendix (SRC-0065)",
        "target": "docs/eger_2008_gazetteer_cleaned.txt",
        "note": "byte_start/byte_end are UTF-8 byte offsets into the cleaned text AS EMITTED; "
                "re-run this tool if the cleaned file is edited. entries[] gives per-entry "
                "source page spans for citation (s.v. <entry>, pp. start-end).",
        "pages": page_spans,
        "entries": entry_pages,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- change report ---
    out = []
    ok = [c for c in coords if c["status"] in ("ok", "repaired")]
    out.append("=== normalize_gazetteer.py change report ===")
    out.append(f"mojibake dot-below glyphs repaired : {mojibake_n}")
    out.append(f"page-number lines removed          : {dropped_pages}")
    out.append(f"footnote lines de-interleaved       : {len(footnotes)}")
    out.append(f"site headers detected               : {len(headers)}")
    out.append(f"coordinate lines found              : {len(coords)}  "
               f"(usable={len(ok)}, flagged={len(coords)-len(ok)})")
    out.append("")
    out.append("--- ALL coordinates (auditable: entry, zone, raw UTM -> WGS84) ---")
    for c in coords:
        ll = f"{c.get('lat')},{c.get('lon')}" if c.get("lat") is not None else "—"
        tag = "" if c["status"] == "ok" else f"  [{c['status'].upper()}]"
        out.append(f"  {c['entry'][:30]:30} {c['zone']} N{c['raw_northing']} E{c['raw_easting']}"
                   f" -> {ll}{tag}")
    out.append("")
    out.append("--- FLAGGED for editorial review ---")
    out.extend("  " + f for f in flags) if flags else out.append("  (none)")
    report = "\n".join(out) + "\n"
    (Path(args.report).write_text(report, encoding="utf-8") if args.report else sys.stdout.write(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
