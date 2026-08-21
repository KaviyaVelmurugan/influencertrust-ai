"""Transparent influencer-campaign ROI scenario simulator."""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal

from .analytics import (
    cost_per_acquisition,
    return_on_ad_spend,
    return_on_investment_pct,
)


SIMULATOR_VERSION = "roi-simulator-v1.0"


def _decimal(value: Decimal | int | float | str) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


@dataclass(frozen=True)
class ScenarioAssumptions:
    campaign_id: str
    audience_size: Decimal
    reach_rate_pct: Decimal
    click_through_rate_pct: Decimal
    conversion_rate_pct: Decimal
    average_order_value: Decimal
    influencer_fees: Decimal
    production_cost: Decimal
    other_campaign_costs: Decimal
    gross_margin_pct: Decimal
    currency: str

    def __post_init__(self) -> None:
        non_negative = (
            self.audience_size,
            self.average_order_value,
            self.influencer_fees,
            self.production_cost,
            self.other_campaign_costs,
        )
        if any(value < 0 for value in non_negative):
            raise ValueError("Audience, value, and cost assumptions cannot be negative")
        rates = (
            self.reach_rate_pct,
            self.click_through_rate_pct,
            self.conversion_rate_pct,
            self.gross_margin_pct,
        )
        if any(value < 0 or value > 100 for value in rates):
            raise ValueError("Rate assumptions must remain between 0 and 100")

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "ScenarioAssumptions":
        return cls(
            campaign_id=row["campaign_id"],
            audience_size=_decimal(row["audience_size"]),
            reach_rate_pct=_decimal(row["reach_rate_pct"]),
            click_through_rate_pct=_decimal(row["click_through_rate_pct"]),
            conversion_rate_pct=_decimal(row["conversion_rate_pct"]),
            average_order_value=_decimal(row["average_order_value"]),
            influencer_fees=_decimal(row["influencer_fees"]),
            production_cost=_decimal(row["production_cost"]),
            other_campaign_costs=_decimal(row["other_campaign_costs"]),
            gross_margin_pct=_decimal(row["gross_margin_pct"]),
            currency=row["currency"],
        )


@dataclass(frozen=True)
class ScenarioFactors:
    name: str
    reach_multiplier: Decimal
    click_through_multiplier: Decimal
    conversion_multiplier: Decimal


@dataclass(frozen=True)
class ScenarioResult:
    campaign_id: str
    scenario: str
    reached_audience: Decimal
    estimated_clicks: Decimal
    estimated_conversions: Decimal
    estimated_revenue: Decimal
    total_campaign_cost: Decimal
    estimated_gross_profit: Decimal
    campaign_profit: Decimal
    contribution_profit: Decimal
    cost_per_acquisition: Decimal | None
    roas_x: Decimal | None
    campaign_roi_pct: Decimal | None
    contribution_roi_pct: Decimal | None
    break_even_conversions: Decimal | None
    break_even_conversion_rate_pct: Decimal | None
    effective_reach_rate_pct: Decimal
    effective_click_through_rate_pct: Decimal
    effective_conversion_rate_pct: Decimal
    currency: str
    version: str = SIMULATOR_VERSION


DEFAULT_SCENARIOS = (
    ScenarioFactors("conservative", Decimal("0.80"), Decimal("0.80"), Decimal("0.75")),
    ScenarioFactors("expected", Decimal("1.00"), Decimal("1.00"), Decimal("1.00")),
    ScenarioFactors("optimistic", Decimal("1.15"), Decimal("1.20"), Decimal("1.25")),
)


def _bounded_rate(rate: Decimal, multiplier: Decimal) -> Decimal:
    return min(Decimal("100"), rate * multiplier)


def simulate(
    assumptions: ScenarioAssumptions,
    factors: ScenarioFactors,
) -> ScenarioResult:
    reach_rate = _bounded_rate(assumptions.reach_rate_pct, factors.reach_multiplier)
    click_rate = _bounded_rate(assumptions.click_through_rate_pct, factors.click_through_multiplier)
    conversion_rate = _bounded_rate(assumptions.conversion_rate_pct, factors.conversion_multiplier)

    reached = assumptions.audience_size * reach_rate / Decimal("100")
    clicks = reached * click_rate / Decimal("100")
    conversions = clicks * conversion_rate / Decimal("100")
    revenue = conversions * assumptions.average_order_value
    total_cost = assumptions.influencer_fees + assumptions.production_cost + assumptions.other_campaign_costs
    gross_profit = revenue * assumptions.gross_margin_pct / Decimal("100")
    campaign_profit = revenue - total_cost
    contribution_profit = gross_profit - total_cost
    contribution_roi = return_on_investment_pct(gross_profit, total_cost)

    margin_per_conversion = assumptions.average_order_value * assumptions.gross_margin_pct / Decimal("100")
    break_even_conversions = total_cost / margin_per_conversion if margin_per_conversion > 0 else None
    break_even_rate = (
        break_even_conversions / clicks * Decimal("100")
        if break_even_conversions is not None and clicks > 0
        else None
    )
    return ScenarioResult(
        campaign_id=assumptions.campaign_id,
        scenario=factors.name,
        reached_audience=reached,
        estimated_clicks=clicks,
        estimated_conversions=conversions,
        estimated_revenue=revenue,
        total_campaign_cost=total_cost,
        estimated_gross_profit=gross_profit,
        campaign_profit=campaign_profit,
        contribution_profit=contribution_profit,
        cost_per_acquisition=cost_per_acquisition(total_cost, conversions),
        roas_x=return_on_ad_spend(revenue, total_cost),
        campaign_roi_pct=return_on_investment_pct(revenue, total_cost),
        contribution_roi_pct=contribution_roi,
        break_even_conversions=break_even_conversions,
        break_even_conversion_rate_pct=break_even_rate,
        effective_reach_rate_pct=reach_rate,
        effective_click_through_rate_pct=click_rate,
        effective_conversion_rate_pct=conversion_rate,
        currency=assumptions.currency,
    )


def change_assumption(
    assumptions: ScenarioAssumptions,
    field: str,
    multiplier: Decimal,
) -> ScenarioAssumptions:
    allowed = {
        "reach_rate_pct",
        "click_through_rate_pct",
        "conversion_rate_pct",
        "average_order_value",
        "gross_margin_pct",
        "influencer_fees",
        "production_cost",
        "other_campaign_costs",
    }
    if field not in allowed:
        raise ValueError(f"Unsupported sensitivity driver: {field}")
    adjusted = min(Decimal("100"), getattr(assumptions, field) * multiplier) if field.endswith("_pct") else getattr(assumptions, field) * multiplier
    return replace(assumptions, **{field: adjusted})
