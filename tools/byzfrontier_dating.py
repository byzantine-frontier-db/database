"""
byzfrontier_dating.py
======================

Reference implementation of dating-system conversions for the
Byzantine-Islamic Frontier Database.

Implements:
  - AH ↔ Julian (Type II tabular Islamic calendar)
  - AM (Byzantine) ↔ Julian
  - Indiction for a given Julian date
  - Regnal year lookup for named Byzantine emperors and Abbasid caliphs
  - JDN ↔ Julian-calendar date conversion (low-level)

Tested against the four worked examples in dating_systems_v1.json.

CLI:
  python byzfrontier_dating.py ah-to-julian 223
  python byzfrontier_dating.py am-to-julian 6346
  python byzfrontier_dating.py indiction-on 0838-07-22
  python byzfrontier_dating.py regnal Theophilos 10
"""

from __future__ import annotations
import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# --- Anchors --------------------------------------------------------------

AH_EPOCH_JDN = 1948440        # 1 Muharram AH 1 = 16 July 622 CE (Julian)
AM_BYZ_EPOCH_AD = -5508       # AM = AD + 5508 (Sept-Dec) / AD + 5509 (Jan-Aug)
INDICTION_ANCHOR_AD = 312     # Indictional year AD 312 (1 Sept 312 onwards) = indiction 1


# --- Low-level: Julian Day Number ↔ Julian-calendar date ------------------

def julian_to_jdn(year: int, month: int, day: int) -> int:
    """Convert a proleptic Julian-calendar date (Y, M, D) to JDN.

    Returns the integer Julian Day Number for the given Julian-calendar date.
    Handles negative (BCE) years using astronomical year numbering (year 0 = 1 BCE).
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083


def jdn_to_julian(jdn: int) -> tuple[int, int, int]:
    """Convert JDN to proleptic Julian-calendar date.

    Inverse of julian_to_jdn. Returns (year, month, day).
    """
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + (m // 10)
    return (year, month, day)


# --- AH (Islamic lunar, Type II tabular) ----------------------------------

def ah_year_start_jdn(ah_year: int) -> int:
    """JDN of 1 Muharram of the given AH year."""
    if ah_year < 1:
        raise ValueError("AH years are 1-indexed; year must be >= 1")
    return AH_EPOCH_JDN + 354 * (ah_year - 1) + (11 * ah_year + 3) // 30


def ah_year_end_jdn(ah_year: int) -> int:
    """JDN of the last day of the given AH year."""
    return ah_year_start_jdn(ah_year + 1) - 1


def ah_year_to_julian_range(ah_year: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Return ((Y, M, D), (Y, M, D)) for start and end of the AH year as Julian-calendar dates."""
    return jdn_to_julian(ah_year_start_jdn(ah_year)), jdn_to_julian(ah_year_end_jdn(ah_year))


def is_ah_leap_year(ah_year: int) -> bool:
    """Type II tabular leap year: positions 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
    within each 30-year cycle."""
    return (11 * ah_year + 14) % 30 < 11


# --- AM Byzantine ---------------------------------------------------------

def am_byzantine_to_julian_range(am_year: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Byzantine AM year: 1 Sept (AM - 5509) to 31 Aug (AM - 5508)."""
    start_ad = am_year - 5509
    end_ad = am_year - 5508
    return (start_ad, 9, 1), (end_ad, 8, 31)


def julian_to_am_byzantine(year: int, month: int, day: int) -> int:
    """Given a Julian-calendar date, return the Byzantine AM year that contains it."""
    if month >= 9:
        return year + 5509
    return year + 5508


# --- Indiction ------------------------------------------------------------

def indiction_for_julian(year: int, month: int, day: int) -> int:
    """Indiction number for a given Julian-calendar date (Byzantine reckoning,
    1 September new year). Returns 1..15.

    Anchored to AD 312: the indictional year that began 1 September 312 CE is
    indiction 1. The formula is ((y - 312) mod 15) + 1 where y is the AD year
    of the indictional new year (i.e. the year whose September is the start
    of the indictional year containing the date).
    """
    indiction_year = year if month >= 9 else year - 1
    return ((indiction_year - INDICTION_ANCHOR_AD) % 15) + 1


# --- Regnal years ---------------------------------------------------------

# Lookup table from dating_systems_v1.json. Loaded lazily.
_RULER_TABLE: dict[str, tuple[int, int, int]] = {}  # name -> (Y, M, D) of accession


def _load_ruler_table():
    """Populate the ruler accession table from the bundled JSON."""
    global _RULER_TABLE
    if _RULER_TABLE:
        return
    here = Path(__file__).parent
    json_path = here / "dating_systems_v1.json"
    if not json_path.exists():
        # Fall back to a hard-coded mini-table for testing
        _RULER_TABLE = {
            "Theophilos": (829, 10, 2),
            "Michael III": (842, 1, 20),
            "Basil I": (867, 9, 23),
            "Leo VI": (886, 8, 29),
            "Romanos I Lakapenos": (920, 12, 17),
            "al-Muʿtaṣim": (833, 8, 9),
            "al-Wāthiq": (842, 1, 5),
            "al-Mutawakkil": (847, 8, 10),
        }
        return
    data = json.loads(json_path.read_text())
    for reign in data.get("reign_table_byzantine", {}).get("reigns", []):
        name = reign["name"]
        ad = reign["accession"]
        y, m, d = map(int, ad.split("-"))
        _RULER_TABLE[name] = (y, m, d)
    for reign in data.get("caliph_table_abbasid", {}).get("reigns", []):
        name = reign["name"]
        ad = reign["accession_civil"]
        y, m, d = map(int, ad.split("-"))
        _RULER_TABLE[name] = (y, m, d)


def regnal_year_to_julian(ruler: str, regnal_year: int) -> tuple[int, int, int]:
    """Return the Julian-calendar date of the regnal-year anniversary.

    Convention: regnal year 1 starts at accession; year n starts on the
    (n-1)-th anniversary of accession.
    """
    _load_ruler_table()
    if ruler not in _RULER_TABLE:
        raise KeyError(f"Unknown ruler: {ruler}. Known: {sorted(_RULER_TABLE.keys())}")
    if regnal_year < 1:
        raise ValueError("Regnal years are 1-indexed")
    y, m, d = _RULER_TABLE[ruler]
    return (y + regnal_year - 1, m, d)


# --- High-level: normalise any DatingValue to a Julian range --------------

@dataclass
class JulianRange:
    """A normalised Julian-calendar range derived from a native date form."""
    start_year: int
    start_month: int
    start_day: int
    end_year: int
    end_month: int
    end_day: int
    precision: str   # 'exact_day' | 'month' | 'year_range_narrow' | etc.
    source_system: str
    source_value: str

    def __str__(self) -> str:
        s = f"{self.start_year:04d}-{self.start_month:02d}-{self.start_day:02d}"
        e = f"{self.end_year:04d}-{self.end_month:02d}-{self.end_day:02d}"
        return f"{self.source_system}:{self.source_value} -> Julian {s} to {e} (precision: {self.precision})"


def normalise_ah_year(ah_year: int) -> JulianRange:
    (sy, sm, sd), (ey, em, ed) = ah_year_to_julian_range(ah_year)
    return JulianRange(sy, sm, sd, ey, em, ed, "year_range_narrow", "AH", f"AH {ah_year}")


def normalise_am_byzantine_year(am_year: int) -> JulianRange:
    (sy, sm, sd), (ey, em, ed) = am_byzantine_to_julian_range(am_year)
    return JulianRange(sy, sm, sd, ey, em, ed, "year_range_narrow", "AM_byzantine", f"AM {am_year}")


def normalise_regnal_year(ruler: str, regnal_year: int) -> JulianRange:
    sy, sm, sd = regnal_year_to_julian(ruler, regnal_year)
    # Regnal year ends one day before the (n+1)-th anniversary
    next_y, next_m, next_d = regnal_year_to_julian(ruler, regnal_year + 1)
    end_jdn = julian_to_jdn(next_y, next_m, next_d) - 1
    ey, em, ed = jdn_to_julian(end_jdn)
    return JulianRange(sy, sm, sd, ey, em, ed, "year_range_narrow",
                       f"regnal({ruler})", f"year {regnal_year} of {ruler}")


# --- Tests against the four worked examples from dating_systems_v1.json --

def _test():
    print("--- Test 1: AH 1 anchor ---")
    s, e = ah_year_to_julian_range(1)
    print(f"  AH 1: {s} to {e}")
    assert s == (622, 7, 16), f"AH 1 start should be 16 July 622, got {s}"
    print("  ✓ AH 1 anchors correctly to 16 July 622 CE")

    print("\n--- Test 2: AH 223 (Amorium campaign) ---")
    s, e = ah_year_to_julian_range(223)
    print(f"  AH 223: {s} to {e}")
    # The methods note documents 3 December 837 - 22 November 838
    assert s == (837, 12, 3), f"AH 223 start should be 3 Dec 837, got {s}"
    assert e == (838, 11, 22), f"AH 223 end should be 22 Nov 838, got {e}"
    print("  ✓ AH 223 matches the documented range")

    print("\n--- Test 3: AM Byzantine 6346 (the campaign year) ---")
    s, e = am_byzantine_to_julian_range(6346)
    print(f"  AM 6346: {s} to {e}")
    assert s == (837, 9, 1), f"AM 6346 start should be 1 Sept 837, got {s}"
    assert e == (838, 8, 31), f"AM 6346 end should be 31 Aug 838, got {e}"
    print("  ✓ AM 6346 matches the documented range")

    print("\n--- Test 4: Indiction for 22 July 838 (Battle of Anzen) ---")
    ind = indiction_for_julian(838, 7, 22)
    print(f"  Indiction on 22 July 838 = {ind}")
    assert ind == 1, f"Indiction should be 1, got {ind}"
    print("  ✓ Indiction matches worked example")

    print("\n--- Test 5: Round-trip of arbitrary Julian dates ---")
    test_dates = [(622, 7, 16), (838, 7, 22), (1000, 1, 1), (2026, 6, 1)]
    for y, m, d in test_dates:
        jdn = julian_to_jdn(y, m, d)
        rt = jdn_to_julian(jdn)
        assert rt == (y, m, d), f"Round-trip failed: {(y,m,d)} -> {jdn} -> {rt}"
    print("  ✓ JDN round-trip preserves all test dates")

    print("\n--- Test 6: Regnal year lookup ---")
    theo_y10 = regnal_year_to_julian("Theophilos", 10)
    print(f"  Year 10 of Theophilos starts: {theo_y10}")
    assert theo_y10 == (838, 10, 2), f"Year 10 should be 2 Oct 838, got {theo_y10}"
    print("  ✓ Regnal year 10 of Theophilos starts 2 October 838")

    print("\n--- Test 7: Multi-system coincidence for 22 July 838 ---")
    target_y, target_m, target_d = 838, 7, 22
    target_jdn = julian_to_jdn(target_y, target_m, target_d)
    # AH year containing this date
    for ah in range(220, 230):
        if ah_year_start_jdn(ah) <= target_jdn <= ah_year_end_jdn(ah):
            print(f"  AH year: {ah}")
            assert ah == 223
            break
    am = julian_to_am_byzantine(target_y, target_m, target_d)
    print(f"  AM Byzantine: {am}")
    assert am == 6346
    ind = indiction_for_julian(target_y, target_m, target_d)
    print(f"  Indiction: {ind}")
    assert ind == 1
    print("  ✓ All systems agree on 22 July 838")

    print("\n--- Test 8: AH leap-year identification ---")
    # Type II leap years: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29 in 30-year cycle
    leap_in_first_cycle = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]
    for n in leap_in_first_cycle:
        assert is_ah_leap_year(n), f"AH {n} should be leap"
    for n in [1, 3, 4, 6, 8, 9, 11, 12, 14, 15, 17, 19, 20, 22, 23, 25, 27, 28, 30]:
        assert not is_ah_leap_year(n), f"AH {n} should NOT be leap"
    print("  ✓ Type II leap-year cycle correct")

    print("\n✓ All 8 dating-system tests pass")


# --- CLI ------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Dating-system conversion utility")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("ah-to-julian", help="Convert AH year to Julian range")
    s1.add_argument("year", type=int)

    s2 = sub.add_parser("am-to-julian", help="Convert Byzantine AM year to Julian range")
    s2.add_argument("year", type=int)

    s3 = sub.add_parser("indiction-on", help="Indiction for a Julian-calendar date YYYY-MM-DD")
    s3.add_argument("date")

    s4 = sub.add_parser("regnal", help="Julian date of a regnal year")
    s4.add_argument("ruler")
    s4.add_argument("year", type=int)

    s5 = sub.add_parser("test", help="Run unit tests")

    args = p.parse_args()

    if args.cmd == "ah-to-julian":
        print(normalise_ah_year(args.year))
    elif args.cmd == "am-to-julian":
        print(normalise_am_byzantine_year(args.year))
    elif args.cmd == "indiction-on":
        y, m, d = map(int, args.date.split("-"))
        print(f"Indiction for {y:04d}-{m:02d}-{d:02d} = {indiction_for_julian(y, m, d)}")
    elif args.cmd == "regnal":
        print(normalise_regnal_year(args.ruler, args.year))
    elif args.cmd == "test":
        _test()


if __name__ == "__main__":
    main()
