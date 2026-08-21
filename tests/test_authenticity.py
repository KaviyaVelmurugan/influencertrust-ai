import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from influencertrust.authenticity import PeerBenchmark, assess_creator, build_peer_benchmarks, creator_features
from influencertrust.authenticity_reporting import generate_authenticity_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRECTORY = PROJECT_ROOT / "data" / "sample"


class AuthenticityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.benchmark = PeerBenchmark(
            platform="instagram",
            creator_count=20,
            median_engagement_rate_pct=Decimal("4"),
            lower_quartile_engagement_rate_pct=Decimal("2"),
            upper_quartile_view_rate_pct=Decimal("80"),
            median_growth_pct=Decimal("4"),
            growth_mad=Decimal("2"),
        )

    def test_rapid_growth_with_weak_engagement_is_high_risk(self) -> None:
        features = {
            "followers": Decimal("500000"),
            "following": Decimal("1000"),
            "follower_growth_30d_pct": Decimal("55"),
            "engagement_rate_pct": Decimal("1"),
            "view_rate_pct": Decimal("30"),
        }
        assessment = assess_creator(features, self.benchmark)
        self.assertEqual(assessment.risk_band, "high")
        self.assertGreaterEqual(assessment.risk_score, 60)
        self.assertIn("growth_engagement_mismatch", {signal.code for signal in assessment.signals})

    def test_stable_creator_with_typical_metrics_is_low_risk(self) -> None:
        features = {
            "followers": Decimal("100000"),
            "following": Decimal("1000"),
            "follower_growth_30d_pct": Decimal("4"),
            "engagement_rate_pct": Decimal("4"),
            "view_rate_pct": Decimal("50"),
        }
        assessment = assess_creator(features, self.benchmark)
        self.assertEqual(assessment.risk_score, 0)
        self.assertEqual(assessment.risk_band, "low")

    def test_missing_evidence_reduces_coverage_without_crashing(self) -> None:
        features = {
            "followers": Decimal("100000"),
            "following": Decimal("0"),
            "follower_growth_30d_pct": Decimal("4"),
            "engagement_rate_pct": Decimal("4"),
            "view_rate_pct": None,
        }
        assessment = assess_creator(features, self.benchmark)
        self.assertEqual(assessment.evidence_coverage_pct, 80)
        self.assertNotIn("extreme_network_ratio", {signal.code for signal in assessment.signals})

    def test_report_flags_intentional_synthetic_scenarios(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = generate_authenticity_report(SAMPLE_DIRECTORY, Path(directory) / "risk.csv")
            with output.open("r", encoding="utf-8", newline="") as handle:
                rows = {row["influencer_id"]: row for row in csv.DictReader(handle)}
            for influencer_id in ("INF-010", "INF-020", "INF-030"):
                self.assertEqual(rows[influencer_id]["risk_band"], "high")
                self.assertIn("rapid_growth", rows[influencer_id]["signals"])

    def test_peer_benchmarks_are_platform_specific(self) -> None:
        with (SAMPLE_DIRECTORY / "influencers.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        benchmarks = build_peer_benchmarks(rows)
        self.assertEqual(set(benchmarks), {"instagram", "youtube", "tiktok"})
        self.assertEqual(sum(item.creator_count for item in benchmarks.values()), 30)
        self.assertIsNotNone(creator_features(rows[0])["engagement_rate_pct"])


if __name__ == "__main__":
    unittest.main()
