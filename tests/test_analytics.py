import unittest
from decimal import Decimal

from influencertrust.analytics import (
    click_through_rate_pct,
    conversion_rate_pct,
    cost_per_acquisition,
    engagement_rate_pct,
    return_on_ad_spend,
    return_on_investment_pct,
)


class AnalyticsTests(unittest.TestCase):
    def test_engagement_rate_includes_likes_comments_and_shares(self) -> None:
        self.assertEqual(engagement_rate_pct(80, 10, 10, 1000), Decimal("10"))

    def test_click_through_rate(self) -> None:
        self.assertEqual(click_through_rate_pct(250, 10000), Decimal("2.500"))

    def test_conversion_rate(self) -> None:
        self.assertEqual(conversion_rate_pct(20, 500), Decimal("4.00"))

    def test_cost_per_acquisition_uses_all_campaign_cost(self) -> None:
        self.assertEqual(cost_per_acquisition(12000, 30), Decimal("400"))

    def test_roas_and_roi_are_not_the_same_metric(self) -> None:
        self.assertEqual(return_on_ad_spend(80000, 50000), Decimal("1.6"))
        self.assertEqual(return_on_investment_pct(80000, 50000), Decimal("60.0"))

    def test_zero_denominator_returns_missing_value(self) -> None:
        self.assertIsNone(click_through_rate_pct(0, 0))
        self.assertIsNone(conversion_rate_pct(0, 0))
        self.assertIsNone(cost_per_acquisition(5000, 0))
        self.assertIsNone(return_on_ad_spend(10000, 0))
        self.assertIsNone(return_on_investment_pct(10000, 0))


if __name__ == "__main__":
    unittest.main()
