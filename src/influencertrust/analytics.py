"""Transparent baseline marketing metrics for InfluencerTrust AI.

All ratios return ``None`` when the denominator is zero. Returning a missing
value is more honest than silently inventing a zero or infinite result.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


ZERO = Decimal("0")
HUNDRED = Decimal("100")


def as_decimal(value: Decimal | int | float | str) -> Decimal:
    """Convert supported numeric input to Decimal without float artefacts."""

    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def safe_divide(
    numerator: Decimal | int | float | str,
    denominator: Decimal | int | float | str,
) -> Decimal | None:
    """Divide two values, returning None when the denominator is zero."""

    denominator_decimal = as_decimal(denominator)
    if denominator_decimal == ZERO:
        return None
    return as_decimal(numerator) / denominator_decimal


def percentage(
    numerator: Decimal | int | float | str,
    denominator: Decimal | int | float | str,
) -> Decimal | None:
    ratio = safe_divide(numerator, denominator)
    return None if ratio is None else ratio * HUNDRED


def engagement_rate_pct(
    likes: Decimal | int | float | str,
    comments: Decimal | int | float | str,
    shares: Decimal | int | float | str,
    followers: Decimal | int | float | str,
) -> Decimal | None:
    """Average visible interactions as a percentage of followers."""

    interactions = as_decimal(likes) + as_decimal(comments) + as_decimal(shares)
    return percentage(interactions, followers)


def view_rate_pct(
    views: Decimal | int | float | str,
    followers: Decimal | int | float | str,
) -> Decimal | None:
    return percentage(views, followers)


def click_through_rate_pct(
    clicks: Decimal | int | float | str,
    impressions: Decimal | int | float | str,
) -> Decimal | None:
    return percentage(clicks, impressions)


def conversion_rate_pct(
    conversions: Decimal | int | float | str,
    clicks: Decimal | int | float | str,
) -> Decimal | None:
    return percentage(conversions, clicks)


def cost_per_engagement(
    campaign_cost: Decimal | int | float | str,
    engagements: Decimal | int | float | str,
) -> Decimal | None:
    return safe_divide(campaign_cost, engagements)


def cost_per_acquisition(
    campaign_cost: Decimal | int | float | str,
    conversions: Decimal | int | float | str,
) -> Decimal | None:
    return safe_divide(campaign_cost, conversions)


def return_on_ad_spend(
    attributed_revenue: Decimal | int | float | str,
    campaign_cost: Decimal | int | float | str,
) -> Decimal | None:
    """Revenue divided by campaign cost, expressed as a multiplier."""

    return safe_divide(attributed_revenue, campaign_cost)


def return_on_investment_pct(
    attributed_revenue: Decimal | int | float | str,
    campaign_cost: Decimal | int | float | str,
) -> Decimal | None:
    """Profit relative to campaign cost, expressed as a percentage."""

    cost = as_decimal(campaign_cost)
    return percentage(as_decimal(attributed_revenue) - cost, cost)


def round_metric(value: Decimal | None, places: int = 2) -> str:
    """Format a metric consistently for CSV reports."""

    if value is None:
        return ""
    quantum = Decimal("1").scaleb(-places)
    return str(value.quantize(quantum, rounding=ROUND_HALF_UP))
