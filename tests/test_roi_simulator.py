import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from influencertrust.roi_simulator import DEFAULT_SCENARIOS, ScenarioAssumptions, ScenarioFactors, simulate
from influencertrust.simulator_reporting import generate_simulator_reports


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRECTORY = PROJECT_ROOT / "data" / "sample"


class RoiSimulatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assumptions = ScenarioAssumptions(
            campaign_id="CAM-TEST",
            audience_size=Decimal("100000"),
            reach_rate_pct=Decimal("50"),
            click_through_rate_pct=Decimal("4"),
            conversion_rate_pct=Decimal("5"),
            average_order_value=Decimal("1000"),
            influencer_fees=Decimal("50000"),
            production_cost=Decimal("20000"),
            other_campaign_costs=Decimal("10000"),
            gross_margin_pct=Decimal("60"),
            currency="INR",
        )
        self.expected = ScenarioFactors("expected", Decimal("1"), Decimal("1"), Decimal("1"))

    def test_funnel_and_financial_formulas(self) -> None:
        result = simulate(self.assumptions, self.expected)
        self.assertEqual(result.reached_audience, Decimal("50000"))
        self.assertEqual(result.estimated_clicks, Decimal("2000"))
        self.assertEqual(result.estimated_conversions, Decimal("100"))
        self.assertEqual(result.estimated_revenue, Decimal("100000"))
        self.assertEqual(result.total_campaign_cost, Decimal("80000"))
        self.assertEqual(result.roas_x, Decimal("1.25"))
        self.assertEqual(result.campaign_roi_pct, Decimal("25.00"))
        self.assertEqual(result.contribution_roi_pct, Decimal("-25.00"))

    def test_scenario_revenue_is_monotonic(self) -> None:
        results = [simulate(self.assumptions, item) for item in DEFAULT_SCENARIOS]
        self.assertLess(results[0].estimated_revenue, results[1].estimated_revenue)
        self.assertLess(results[1].estimated_revenue, results[2].estimated_revenue)

    def test_invalid_rate_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ScenarioAssumptions(**{**self.assumptions.__dict__, "reach_rate_pct": Decimal("101")})

    def test_reports_cover_three_scenarios_and_eight_drivers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outputs = generate_simulator_reports(SAMPLE_DIRECTORY, Path(directory))
            with outputs["scenarios"].open("r", encoding="utf-8", newline="") as handle:
                scenarios = list(csv.DictReader(handle))
            with outputs["sensitivity"].open("r", encoding="utf-8", newline="") as handle:
                sensitivity = list(csv.DictReader(handle))
            self.assertEqual(len(scenarios), 9)
            self.assertEqual(len(sensitivity), 24)
            self.assertEqual({row["scenario"] for row in scenarios}, {"conservative", "expected", "optimistic"})


if __name__ == "__main__":
    unittest.main()
