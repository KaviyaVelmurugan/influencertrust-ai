import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from influencertrust.baseline_reporting import build_campaign_metrics, generate_reports


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class BaselineReportingTests(unittest.TestCase):
    def test_campaign_metrics_use_ratio_of_totals(self) -> None:
        outcomes = [
            {
                "campaign_id": "CAM-001",
                "influencer_id": "INF-001",
                "impressions": "100",
                "clicks": "10",
                "conversions": "1",
                "attributed_revenue": "200",
                "influencer_fee": "50",
                "production_cost": "50",
                "currency": "INR",
            },
            {
                "campaign_id": "CAM-001",
                "influencer_id": "INF-002",
                "impressions": "900",
                "clicks": "45",
                "conversions": "9",
                "attributed_revenue": "1800",
                "influencer_fee": "400",
                "production_cost": "500",
                "currency": "INR",
            },
        ]
        report = build_campaign_metrics(outcomes)[0]
        self.assertEqual(Decimal(report["click_through_rate_pct"]), Decimal("5.50"))
        self.assertEqual(Decimal(report["roas_x"]), Decimal("2.00"))
        self.assertEqual(Decimal(report["roi_pct"]), Decimal("100.00"))

    def test_reports_are_generated_from_valid_sample_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            generated = generate_reports(PROJECT_ROOT / "data" / "sample", Path(directory))
            self.assertEqual(set(generated), {"influencer_metrics", "outcome_metrics", "campaign_metrics"})
            for path in generated.values():
                self.assertTrue(path.exists())
                with path.open("r", encoding="utf-8", newline="") as handle:
                    self.assertGreater(len(list(csv.DictReader(handle))), 0)


if __name__ == "__main__":
    unittest.main()
