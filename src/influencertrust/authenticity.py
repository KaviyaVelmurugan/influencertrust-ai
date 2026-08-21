"""Explainable heuristic authenticity-risk assessment.

The output is a screening signal, not proof of fraud and not a probability.
Rules are intentionally visible so that a reviewer can challenge every point.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from statistics import median

from .analytics import engagement_rate_pct, view_rate_pct


RULE_VERSION = "auth-risk-rules-v1.0"


@dataclass(frozen=True)
class PeerBenchmark:
    platform: str
    creator_count: int
    median_engagement_rate_pct: Decimal
    lower_quartile_engagement_rate_pct: Decimal
    upper_quartile_view_rate_pct: Decimal
    median_growth_pct: Decimal
    growth_mad: Decimal


@dataclass(frozen=True)
class RiskSignal:
    code: str
    points: int
    explanation: str


@dataclass(frozen=True)
class RiskAssessment:
    risk_score: int
    risk_band: str
    evidence_coverage_pct: int
    signals: tuple[RiskSignal, ...]
    limitations: tuple[str, ...]
    rule_version: str = RULE_VERSION


def _decimal(value: str | int | float | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _quantile(values: list[Decimal], position: Decimal) -> Decimal:
    """Calculate a linearly interpolated quantile for a non-empty list."""

    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = position * Decimal(len(ordered) - 1)
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - Decimal(lower)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _median_absolute_deviation(values: list[Decimal]) -> Decimal:
    centre = _decimal(median(values))
    return _decimal(median([abs(value - centre) for value in values]))


def creator_features(row: dict[str, str]) -> dict[str, Decimal | str | None]:
    followers = _decimal(row["followers"])
    following = _decimal(row["following"])
    calculated_engagement = engagement_rate_pct(
        row["average_likes"],
        row["average_comments"],
        row["average_shares"],
        followers,
    )
    calculated_view_rate = view_rate_pct(row["average_views"], followers)
    return {
        "influencer_id": row["influencer_id"],
        "handle": row["handle"],
        "platform": row["platform"],
        "category": row["category"],
        "followers": followers,
        "following": following,
        "follower_growth_30d_pct": _decimal(row["follower_growth_30d_pct"]),
        "engagement_rate_pct": calculated_engagement,
        "view_rate_pct": calculated_view_rate,
    }


def build_peer_benchmarks(rows: list[dict[str, str]]) -> dict[str, PeerBenchmark]:
    grouped: dict[str, list[dict[str, Decimal | str | None]]] = {}
    for row in rows:
        features = creator_features(row)
        grouped.setdefault(str(features["platform"]), []).append(features)

    benchmarks: dict[str, PeerBenchmark] = {}
    for platform, creators in grouped.items():
        engagement_values = [
            value
            for creator in creators
            if (value := creator["engagement_rate_pct"]) is not None
            and isinstance(value, Decimal)
        ]
        view_values = [
            value
            for creator in creators
            if (value := creator["view_rate_pct"]) is not None
            and isinstance(value, Decimal)
        ]
        growth_values = [
            creator["follower_growth_30d_pct"]
            for creator in creators
            if isinstance(creator["follower_growth_30d_pct"], Decimal)
        ]
        benchmarks[platform] = PeerBenchmark(
            platform=platform,
            creator_count=len(creators),
            median_engagement_rate_pct=_decimal(median(engagement_values)),
            lower_quartile_engagement_rate_pct=_quantile(engagement_values, Decimal("0.25")),
            upper_quartile_view_rate_pct=_quantile(view_values, Decimal("0.75")),
            median_growth_pct=_decimal(median(growth_values)),
            growth_mad=_median_absolute_deviation(growth_values),
        )
    return benchmarks


def assess_creator(
    features: dict[str, Decimal | str | None],
    benchmark: PeerBenchmark,
) -> RiskAssessment:
    signals: list[RiskSignal] = []
    limitations = [
        "Public metrics cannot confirm purchased followers or coordinated behaviour.",
        "Platform definitions and observation windows may differ.",
    ]
    evidence_fields = (
        "followers",
        "following",
        "follower_growth_30d_pct",
        "engagement_rate_pct",
        "view_rate_pct",
    )
    available = sum(features.get(field) is not None for field in evidence_fields)
    coverage = round(available / len(evidence_fields) * 100)

    growth = features.get("follower_growth_30d_pct")
    engagement = features.get("engagement_rate_pct")
    views = features.get("view_rate_pct")
    followers = features.get("followers")
    following = features.get("following")

    if isinstance(growth, Decimal):
        if growth >= Decimal("30"):
            signals.append(RiskSignal("rapid_growth", 30, f"30-day follower growth is unusually high at {growth:.2f}%."))
        elif growth >= Decimal("15"):
            signals.append(RiskSignal("elevated_growth", 15, f"30-day follower growth is elevated at {growth:.2f}%."))

        if benchmark.growth_mad > 0:
            robust_z = Decimal("0.6745") * (growth - benchmark.median_growth_pct) / benchmark.growth_mad
            if robust_z >= Decimal("3"):
                signals.append(
                    RiskSignal(
                        "peer_growth_outlier",
                        10,
                        f"Growth is a strong outlier relative to {benchmark.creator_count} {benchmark.platform} peers.",
                    )
                )

    engagement_ratio: Decimal | None = None
    if isinstance(engagement, Decimal) and benchmark.median_engagement_rate_pct > 0:
        engagement_ratio = engagement / benchmark.median_engagement_rate_pct
        if engagement_ratio <= Decimal("0.40"):
            signals.append(
                RiskSignal(
                    "very_low_peer_engagement",
                    25,
                    f"Engagement rate ({engagement:.2f}%) is below 40% of the {benchmark.platform} peer median.",
                )
            )
        elif engagement_ratio <= Decimal("0.65"):
            signals.append(
                RiskSignal(
                    "low_peer_engagement",
                    12,
                    f"Engagement rate ({engagement:.2f}%) is below 65% of the {benchmark.platform} peer median.",
                )
            )

    if (
        isinstance(growth, Decimal)
        and growth >= Decimal("20")
        and engagement_ratio is not None
        and engagement_ratio <= Decimal("0.65")
    ):
        signals.append(
            RiskSignal(
                "growth_engagement_mismatch",
                20,
                "Rapid follower growth is not accompanied by peer-comparable engagement.",
            )
        )

    if isinstance(followers, Decimal) and isinstance(following, Decimal) and following > 0:
        follower_following_ratio = followers / following
        if follower_following_ratio >= Decimal("1000"):
            signals.append(RiskSignal("extreme_network_ratio", 10, f"Follower-to-following ratio is extreme at {follower_following_ratio:.0f}:1."))
        elif follower_following_ratio >= Decimal("300"):
            signals.append(RiskSignal("high_network_ratio", 5, f"Follower-to-following ratio is high at {follower_following_ratio:.0f}:1."))

    if (
        isinstance(views, Decimal)
        and isinstance(engagement, Decimal)
        and views >= benchmark.upper_quartile_view_rate_pct
        and engagement <= benchmark.lower_quartile_engagement_rate_pct
    ):
        signals.append(
            RiskSignal(
                "views_engagement_mismatch",
                10,
                "View rate is in the upper peer quartile while engagement is in the lower peer quartile.",
            )
        )

    score = min(100, sum(signal.points for signal in signals))
    band = "high" if score >= 60 else "medium" if score >= 30 else "low"
    if benchmark.creator_count < 10:
        limitations.append("Peer group contains fewer than 10 creators, so benchmarks are less stable.")
    return RiskAssessment(
        risk_score=score,
        risk_band=band,
        evidence_coverage_pct=coverage,
        signals=tuple(signals),
        limitations=tuple(limitations),
    )
