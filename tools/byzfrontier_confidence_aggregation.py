"""
byzfrontier_confidence_aggregation.py
=====================================

Confidence Aggregation Algorithm v1.0.0
Byzantine-Islamic Frontier Database

This module is both a specification (the docstrings define the rule) and a
reference implementation (the functions compute it). The implementation is the
correctness criterion.

------------------------------------------------------------------------
RULE
------------------------------------------------------------------------

The entity-level `overall_confidence` field is the editorial or algorithmic
synthesis of the confidence values of the attestations that support an entity.
The project commits to a single documented algorithm, with explicit editorial
override permitted.

The algorithm has four stages:

  1. Weight each supporting attestation by an "independence weight":
     independent attestations count more than derivative ones, and primary
     sources count more than modern syntheses.

  2. Compute the weighted median of the supporting attestations' confidence
     levels. This is the "median floor".

  3. Apply two adjustments:
     (a) +1 if there are three or more strong independent attestations
         (confidence ≥ 4) — corroboration bonus, capped at 5.
     (b) Cap the median at 3 if there are any contradicting attestations
         of equal or greater weight — contradiction penalty.

  4. The result is the algorithmic overall_confidence. An editor may set
     overall_confidence to a different value, in which case the record is
     tagged with `confidence_basis: "editorial"` and the algorithmic value
     is preserved in `algorithmic_confidence` for audit.

------------------------------------------------------------------------
WHY THIS RULE
------------------------------------------------------------------------

Weighted median, not mean, because:
  - Median is robust to single outlier attestations.
  - Mean would let one very-low-confidence attestation pull the entity-level
    down disproportionately, especially when most evidence agrees.

Independence-weighted, not flat-weighted, because:
  - A primary source carries more evidential weight than a modern synthesis
    of that primary source.
  - Multiple modern sources echoing one primary source do not constitute
    independent confirmation; treating them as independent would
    systematically inflate confidence.

Corroboration bonus and contradiction penalty, because:
  - Three independent strong attestations are stronger than the median
    suggests on its own.
  - Any genuine contradiction caps confidence below 4 by definition: if
    competent sources disagree, the claim is not "highly probable".

Editorial override permitted, because:
  - The algorithm cannot capture every editorial nuance.
  - The override is logged with explicit `confidence_basis` so users can
    distinguish algorithmic from editorial values.

------------------------------------------------------------------------
INDEPENDENCE WEIGHTS BY PROVENANCE CATEGORY
------------------------------------------------------------------------
"""

from __future__ import annotations
from dataclasses import dataclass
from statistics import median
from typing import Optional


# Independence weights by provenance category. Higher = more evidential weight.
# The values are calibrated so that a primary quotation outweighs the average
# modern synthesis 2-to-1, and archaeological / epigraphic / numismatic /
# papyrological / sigillographic evidence has the highest weight (these are
# materially independent of textual transmission).
PROVENANCE_WEIGHTS = {
    "primary_quotation":       2.0,
    "primary_paraphrase":      1.8,
    "primary_summary":         1.5,
    "archaeological_evidence": 2.5,
    "epigraphic_evidence":     2.5,
    "numismatic_evidence":     2.2,
    "papyrological_evidence":  2.2,
    "sigillographic_evidence": 2.0,
    "modern_synthesis":        1.0,
    "modern_identification":   1.0,
    "modern_interpretation":   0.8,
    "gis_derived_observation": 1.0,
    "editorial_inference":     0.5,
    "cross_source_synthesis":  1.0,
}

DEFAULT_WEIGHT = 1.0


@dataclass(frozen=True)
class AttestationSummary:
    """The minimum information needed about an attestation to aggregate.

    In production, this is derived from an AttestationRecord plus the
    independence relationship to other attestations. For the v1
    algorithm, the independence is assumed by provenance category and by
    explicit `depends_on` source relationships in the database.
    """
    attestation_id: str
    confidence: int                  # 1..5 from schema
    provenance: str
    is_contradicting: bool = False
    independence_override: Optional[float] = None  # editor may override

    @property
    def weight(self) -> float:
        if self.independence_override is not None:
            return self.independence_override
        return PROVENANCE_WEIGHTS.get(self.provenance, DEFAULT_WEIGHT)


@dataclass
class AggregationResult:
    overall_confidence: int          # 1..5, the final value
    algorithmic_confidence: int      # 1..5, the unmodified algorithmic value
    confidence_basis: str            # "algorithmic" or "editorial"
    median_floor: float              # the weighted median before adjustments
    corroboration_bonus_applied: bool
    contradiction_penalty_applied: bool
    rationale: str                   # human-readable explanation


def weighted_median(values_weights: list[tuple[int, float]]) -> float:
    """Compute the weighted median of (value, weight) pairs.

    Definition: the smallest value v such that the cumulative weight of
    items ≤ v is at least half the total weight.
    """
    if not values_weights:
        raise ValueError("Cannot compute weighted median of empty set")
    sorted_pairs = sorted(values_weights, key=lambda x: x[0])
    total = sum(w for _, w in sorted_pairs)
    half = total / 2.0
    cumulative = 0.0
    for v, w in sorted_pairs:
        cumulative += w
        if cumulative >= half:
            return float(v)
    return float(sorted_pairs[-1][0])


def aggregate_confidence(
    supporting: list[AttestationSummary],
    contradicting: list[AttestationSummary] | None = None,
    editorial_override: Optional[int] = None,
    editorial_rationale: Optional[str] = None,
) -> AggregationResult:
    """Compute the entity-level overall_confidence per the v1 algorithm.

    Args:
        supporting:   non-empty list of attestations that support the entity
        contradicting: list of attestations that contradict the entity
        editorial_override: if set (1..5), overrides the algorithmic result
        editorial_rationale: required when editorial_override is set

    Returns:
        AggregationResult with both the algorithmic and the final value.
    """
    if not supporting:
        raise ValueError("Cannot aggregate confidence with no supporting attestations")
    contradicting = contradicting or []

    # Stage 1+2: weighted median of supporting attestations
    pairs = [(a.confidence, a.weight) for a in supporting]
    floor = weighted_median(pairs)

    # Stage 3a: corroboration bonus
    strong_independent = sum(
        1 for a in supporting if a.confidence >= 4 and a.weight >= 1.5
    )
    bonus = 0
    if strong_independent >= 3:
        bonus = 1

    # Stage 3b: contradiction penalty
    max_contradicting_weight = max((c.weight for c in contradicting), default=0.0)
    max_supporting_weight    = max((a.weight for a in supporting), default=0.0)
    penalty_applied = False
    algorithmic = min(int(round(floor)) + bonus, 5)
    if contradicting and max_contradicting_weight >= max_supporting_weight:
        algorithmic = min(algorithmic, 3)
        penalty_applied = True

    algorithmic = max(1, min(5, algorithmic))

    # Stage 4: editorial override
    if editorial_override is not None:
        if editorial_override < 1 or editorial_override > 5:
            raise ValueError("editorial_override must be 1..5")
        if not editorial_rationale:
            raise ValueError(
                "editorial_rationale is required whenever editorial_override is set"
            )
        final = editorial_override
        basis = "editorial"
        rationale = (
            f"Algorithmic value was {algorithmic} "
            f"(weighted median {floor:.2f}; bonus={bonus}; penalty={penalty_applied}). "
            f"Editorial override to {final}: {editorial_rationale}"
        )
    else:
        final = algorithmic
        basis = "algorithmic"
        rationale = (
            f"Weighted median of {len(supporting)} attestations = {floor:.2f}. "
            + (f"Corroboration bonus +1 (≥3 strong independent attestations). " if bonus else "")
            + (f"Contradiction penalty applied (cap at 3). " if penalty_applied else "")
            + f"Algorithmic result: {algorithmic}."
        )

    return AggregationResult(
        overall_confidence=final,
        algorithmic_confidence=algorithmic,
        confidence_basis=basis,
        median_floor=floor,
        corroboration_bonus_applied=bool(bonus),
        contradiction_penalty_applied=penalty_applied,
        rationale=rationale,
    )


# ----------------------------------------------------------------------
# Test cases — these define correctness.
# ----------------------------------------------------------------------

def _test():
    # Case 1: Amorium itself.
    # Multiple strong primary attestations + archaeological corroboration → 5.
    amorium = [
        AttestationSummary("ATT-0001", 5, "primary_paraphrase"),   # al-Ṭabarī
        AttestationSummary("ATT-0002", 4, "primary_paraphrase"),   # Theoph. Cont.
        AttestationSummary("ATT-0003", 4, "primary_summary"),      # al-Yaʿqūbī
        AttestationSummary("ATT-0011", 5, "archaeological_evidence"),
    ]
    r = aggregate_confidence(amorium)
    assert r.overall_confidence == 5, f"Amorium expected 5, got {r.overall_confidence}"
    assert r.corroboration_bonus_applied, "Should trigger corroboration bonus"
    print(f"  Amorium: confidence={r.overall_confidence} ({r.rationale})")

    # Case 2: Disputed identification — Anzen/Dazimon location.
    # Two primary paraphrase attestations (confidence 4) but no archaeological
    # confirmation of the identification → should yield 4.
    anzen = [
        AttestationSummary("ATT-0006", 4, "primary_paraphrase"),
        AttestationSummary("ATT-0007", 4, "primary_paraphrase"),
    ]
    r = aggregate_confidence(anzen)
    assert r.overall_confidence == 4, f"Anzen expected 4, got {r.overall_confidence}"
    print(f"  Anzen: confidence={r.overall_confidence} ({r.rationale})")

    # Case 3: Siege duration — contradictory attestations.
    # ATT-0008 supports 12-13 days (confidence 4); ATT-0009 supports 55 days
    # (confidence 2). When viewing OBS-0004 (the 12-13-day claim), ATT-0009
    # contradicts. Supporting weight = 1.8 (primary_paraphrase); contradicting
    # weight = 1.5 (primary_summary). Supporting wins; no penalty.
    obs_0004_supporting = [
        AttestationSummary("ATT-0008", 4, "primary_paraphrase"),
    ]
    obs_0004_contradicting = [
        AttestationSummary("ATT-0009", 2, "primary_summary"),
    ]
    r = aggregate_confidence(obs_0004_supporting, obs_0004_contradicting)
    assert not r.contradiction_penalty_applied, "Supporting should outweigh"
    print(f"  Siege 12-day claim: confidence={r.overall_confidence} ({r.rationale})")

    # Case 4: Reverse — viewing OBS-0005 (the 55-day claim). Now supporting
    # weight is 1.5 (the primary_summary); contradicting weight is 1.8.
    # Contradiction has equal-or-greater weight → cap at 3.
    obs_0005_supporting = [
        AttestationSummary("ATT-0009", 2, "primary_summary"),
    ]
    obs_0005_contradicting = [
        AttestationSummary("ATT-0008", 4, "primary_paraphrase"),
    ]
    r = aggregate_confidence(obs_0005_supporting, obs_0005_contradicting)
    assert r.contradiction_penalty_applied, "Should apply penalty"
    assert r.overall_confidence <= 3, "Penalty caps at 3"
    print(f"  Siege 55-day claim: confidence={r.overall_confidence} ({r.rationale})")

    # Case 5: Editorial override.
    weak_evidence = [
        AttestationSummary("ATT-X01", 2, "modern_interpretation"),
    ]
    r = aggregate_confidence(
        weak_evidence,
        editorial_override=4,
        editorial_rationale="Editor reviewed unpublished archaeological data not yet attested.",
    )
    assert r.confidence_basis == "editorial"
    assert r.overall_confidence == 4
    assert r.algorithmic_confidence == 2
    print(f"  Editorial override: final={r.overall_confidence}, algorithmic={r.algorithmic_confidence}")

    print("\n✓ All confidence-aggregation tests pass")


if __name__ == "__main__":
    _test()
