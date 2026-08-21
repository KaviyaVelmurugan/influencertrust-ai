"""Generate explained campaign-specific influencer rankings."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

from .analytics import cost_per_engagement, engagement_rate_pct, round_metric
from .authenticity import assess_creator, build_peer_benchmarks, creator_features
from .data_validation import validate_directory
from .matching import calculate_campaign_fit
from .ranking import RankingWeights, calculate_ranking, percentile_score


def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _engagement(row: dict[str, str]) -> Decimal:
    value = engagement_rate_pct(
        row["average_likes"], row["average_comments"], row["average_shares"], row["followers"]
    )
    if value is None:
        return Decimal("0")
    return value


def _cost_per_engagement(row: dict[str, str]) -> Decimal:
    engagements = Decimal(row["average_likes"]) + Decimal(row["average_comments"]) + Decimal(row["average_shares"])
    value = cost_per_engagement(row["estimated_fee"], engagements)
    return value if value is not None else Decimal("Infinity")


def generate_ranking_report(
    data_directory: Path,
    output_path: Path,
    weights: RankingWeights | None = None,
) -> Path:
    errors = validate_directory(data_directory)
    if errors:
        raise ValueError("Source data failed validation:\n" + "\n".join(map(str, errors)))

    campaigns = _read(data_directory / "campaigns.csv")
    influencers = _read(data_directory / "influencers.csv")
    authenticity_benchmarks = build_peer_benchmarks(influencers)
    platform_groups: dict[str, list[dict[str, str]]] = {}
    for influencer in influencers:
        platform_groups.setdefault(influencer["platform"], []).append(influencer)

    report: list[dict[str, object]] = []
    for campaign in campaigns:
        campaign_rows: list[dict[str, object]] = []
        for influencer in influencers:
            peers = platform_groups[influencer["platform"]]
            engagement = _engagement(influencer)
            creator_cpe = _cost_per_engagement(influencer)
            engagement_quality = percentile_score(
                engagement,
                [_engagement(peer) for peer in peers],
                higher_is_better=True,
            )
            cost_efficiency = percentile_score(
                creator_cpe,
                [_cost_per_engagement(peer) for peer in peers],
                higher_is_better=False,
            )
            fit = calculate_campaign_fit(campaign, influencer)
            assessment = assess_creator(
                creator_features(influencer),
                authenticity_benchmarks[influencer["platform"]],
            )
            authenticity_score = Decimal(100 - assessment.risk_score)
            ranking = calculate_ranking(
                fit.fit_score,
                authenticity_score,
                engagement_quality,
                cost_efficiency,
                weights,
            )
            campaign_rows.append(
                {
                    "campaign_id": campaign["campaign_id"],
                    "campaign_name": campaign["campaign_name"],
                    "influencer_id": influencer["influencer_id"],
                    "handle": influencer["handle"],
                    "platform": influencer["platform"],
                    "category": influencer["category"],
                    "overall_score": round_metric(ranking.overall_score),
                    "campaign_fit_score": round_metric(ranking.campaign_fit_score),
                    "authenticity_score": round_metric(ranking.authenticity_score),
                    "engagement_quality_score": round_metric(ranking.engagement_quality_score),
                    "cost_efficiency_score": round_metric(ranking.cost_efficiency_score),
                    "authenticity_risk_band": assessment.risk_band,
                    "matched_terms": "|".join(fit.matched_terms),
                    "missing_campaign_terms": "|".join(fit.missing_terms),
                    "explanation": " | ".join(ranking.contributions),
                    "weight_version": ranking.weight_version,
                }
            )
        campaign_rows.sort(
            key=lambda item: (-Decimal(str(item["overall_score"])), str(item["influencer_id"]))
        )
        for rank, item in enumerate(campaign_rows, start=1):
            item["rank"] = rank
        report.extend(campaign_rows)

    columns = [
        "campaign_id",
        "campaign_name",
        "rank",
        "influencer_id",
        "handle",
        "platform",
        "category",
        "overall_score",
        "campaign_fit_score",
        "authenticity_score",
        "engagement_quality_score",
        "cost_efficiency_score",
        "authenticity_risk_band",
        "matched_terms",
        "missing_campaign_terms",
        "explanation",
        "weight_version",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(report)
    return output_path
