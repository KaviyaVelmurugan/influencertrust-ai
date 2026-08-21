"""Explainable weighted influencer ranking."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


WEIGHT_VERSION = "ranking-weights-v1.0"


@dataclass(frozen=True)
class RankingWeights:
    campaign_fit: Decimal = Decimal("0.50")
    authenticity: Decimal = Decimal("0.25")
    engagement_quality: Decimal = Decimal("0.15")
    cost_efficiency: Decimal = Decimal("0.10")

    def __post_init__(self) -> None:
        values = (
            self.campaign_fit,
            self.authenticity,
            self.engagement_quality,
            self.cost_efficiency,
        )
        if any(value < 0 for value in values):
            raise ValueError("Ranking weights cannot be negative")
        if sum(values) != Decimal("1"):
            raise ValueError("Ranking weights must sum to exactly 1")


@dataclass(frozen=True)
class RankingResult:
    overall_score: Decimal
    campaign_fit_score: Decimal
    authenticity_score: Decimal
    engagement_quality_score: Decimal
    cost_efficiency_score: Decimal
    contributions: tuple[str, ...]
    weight_version: str = WEIGHT_VERSION


def percentile_score(
    value: Decimal,
    peer_values: list[Decimal],
    *,
    higher_is_better: bool,
) -> Decimal:
    """Return a 0–100 mid-rank percentile against a non-empty peer group."""

    if not peer_values:
        raise ValueError("Peer values cannot be empty")
    better_direction_count = sum(
        peer < value if higher_is_better else peer > value
        for peer in peer_values
    )
    equal_count = sum(peer == value for peer in peer_values)
    return (
        (Decimal(better_direction_count) + Decimal(equal_count) / Decimal("2"))
        / Decimal(len(peer_values))
        * Decimal("100")
    )


def calculate_ranking(
    campaign_fit_score: Decimal,
    authenticity_score: Decimal,
    engagement_quality_score: Decimal,
    cost_efficiency_score: Decimal,
    weights: RankingWeights | None = None,
) -> RankingResult:
    selected = weights or RankingWeights()
    components = (
        ("campaign fit", campaign_fit_score, selected.campaign_fit),
        ("authenticity", authenticity_score, selected.authenticity),
        ("engagement quality", engagement_quality_score, selected.engagement_quality),
        ("cost efficiency", cost_efficiency_score, selected.cost_efficiency),
    )
    overall = sum(score * weight for _, score, weight in components)
    contributions = tuple(
        f"{name}: {score:.2f} × {weight:.0%} = {(score * weight):.2f}"
        for name, score, weight in components
    )
    return RankingResult(
        overall_score=overall,
        campaign_fit_score=campaign_fit_score,
        authenticity_score=authenticity_score,
        engagement_quality_score=engagement_quality_score,
        cost_efficiency_score=cost_efficiency_score,
        contributions=contributions,
    )
