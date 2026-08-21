"""Generate auditable baseline CSV reports from validated sample data."""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from .analytics import (
    click_through_rate_pct,
    conversion_rate_pct,
    cost_per_acquisition,
    cost_per_engagement,
    engagement_rate_pct,
    return_on_ad_spend,
    return_on_investment_pct,
    round_metric,
    view_rate_pct,
)
from .data_validation import validate_directory


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write an empty report: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_influencer_metrics(influencers: list[dict[str, str]]) -> list[dict[str, object]]:
    report: list[dict[str, object]] = []
    for row in influencers:
        engagements = Decimal(row["average_likes"]) + Decimal(row["average_comments"]) + Decimal(row["average_shares"])
        report.append(
            {
                "influencer_id": row["influencer_id"],
                "handle": row["handle"],
                "platform": row["platform"],
                "category": row["category"],
                "followers": row["followers"],
                "average_engagements": round_metric(engagements),
                "calculated_engagement_rate_pct": round_metric(
                    engagement_rate_pct(row["average_likes"], row["average_comments"], row["average_shares"], row["followers"])
                ),
                "view_rate_pct": round_metric(view_rate_pct(row["average_views"], row["followers"])),
                "follower_growth_30d_pct": row["follower_growth_30d_pct"],
                "estimated_fee": row["estimated_fee"],
                "estimated_cost_per_engagement": round_metric(cost_per_engagement(row["estimated_fee"], engagements)),
                "currency": row["currency"],
            }
        )
    return report


def build_outcome_metrics(outcomes: list[dict[str, str]]) -> list[dict[str, object]]:
    report: list[dict[str, object]] = []
    for row in outcomes:
        total_cost = Decimal(row["influencer_fee"]) + Decimal(row["production_cost"])
        revenue = Decimal(row["attributed_revenue"])
        report.append(
            {
                **row,
                "total_cost": round_metric(total_cost),
                "profit": round_metric(revenue - total_cost),
                "click_through_rate_pct": round_metric(click_through_rate_pct(row["clicks"], row["impressions"])),
                "conversion_rate_pct": round_metric(conversion_rate_pct(row["conversions"], row["clicks"])),
                "cost_per_acquisition": round_metric(cost_per_acquisition(total_cost, row["conversions"])),
                "roas_x": round_metric(return_on_ad_spend(revenue, total_cost)),
                "roi_pct": round_metric(return_on_investment_pct(revenue, total_cost)),
            }
        )
    return report


def build_campaign_metrics(outcomes: list[dict[str, str]]) -> list[dict[str, object]]:
    totals: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: defaultdict(Decimal)
    )
    currencies: dict[str, str] = {}
    influencer_sets: dict[str, set[str]] = defaultdict(set)
    for row in outcomes:
        campaign_id = row["campaign_id"]
        for field in (
            "impressions",
            "clicks",
            "conversions",
            "attributed_revenue",
            "influencer_fee",
            "production_cost",
        ):
            totals[campaign_id][field] += Decimal(row[field])
        currencies[campaign_id] = row["currency"]
        influencer_sets[campaign_id].add(row["influencer_id"])

    report: list[dict[str, object]] = []
    for campaign_id in sorted(totals):
        values = totals[campaign_id]
        total_cost = values["influencer_fee"] + values["production_cost"]
        revenue = values["attributed_revenue"]
        report.append(
            {
                "campaign_id": campaign_id,
                "influencer_count": len(influencer_sets[campaign_id]),
                "impressions": round_metric(values["impressions"], 0),
                "clicks": round_metric(values["clicks"], 0),
                "conversions": round_metric(values["conversions"], 0),
                "attributed_revenue": round_metric(revenue),
                "total_cost": round_metric(total_cost),
                "profit": round_metric(revenue - total_cost),
                "click_through_rate_pct": round_metric(click_through_rate_pct(values["clicks"], values["impressions"])),
                "conversion_rate_pct": round_metric(conversion_rate_pct(values["conversions"], values["clicks"])),
                "cost_per_acquisition": round_metric(cost_per_acquisition(total_cost, values["conversions"])),
                "roas_x": round_metric(return_on_ad_spend(revenue, total_cost)),
                "roi_pct": round_metric(return_on_investment_pct(revenue, total_cost)),
                "currency": currencies[campaign_id],
            }
        )
    return report


def generate_reports(data_directory: Path, report_directory: Path) -> dict[str, Path]:
    errors = validate_directory(data_directory)
    if errors:
        messages = "\n".join(str(error) for error in errors)
        raise ValueError(f"Source data failed validation:\n{messages}")

    influencers = _read_csv(data_directory / "influencers.csv")
    outcomes = _read_csv(data_directory / "outcomes.csv")
    reports = {
        "influencer_metrics": report_directory / "influencer_metrics.csv",
        "outcome_metrics": report_directory / "outcome_metrics.csv",
        "campaign_metrics": report_directory / "campaign_metrics.csv",
    }
    _write_csv(reports["influencer_metrics"], build_influencer_metrics(influencers))
    _write_csv(reports["outcome_metrics"], build_outcome_metrics(outcomes))
    _write_csv(reports["campaign_metrics"], build_campaign_metrics(outcomes))
    return reports
