import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from influencertrust.matching import calculate_campaign_fit, tokenize
from influencertrust.ranking import RankingWeights, calculate_ranking, percentile_score
from influencertrust.ranking_reporting import generate_ranking_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRECTORY = PROJECT_ROOT / "data" / "sample"


class MatchingTests(unittest.TestCase):
    def setUp(self) -> None:
        with (SAMPLE_DIRECTORY / "campaigns.csv").open("r", encoding="utf-8", newline="") as handle:
            self.campaigns = list(csv.DictReader(handle))
        with (SAMPLE_DIRECTORY / "influencers.csv").open("r", encoding="utf-8", newline="") as handle:
            self.influencers = list(csv.DictReader(handle))

    def test_relevant_creator_has_stronger_campaign_fit(self) -> None:
        beauty_campaign = self.campaigns[0]
        beauty_creator = next(row for row in self.influencers if row["category"] == "beauty")
        technology_creator = next(row for row in self.influencers if row["category"] == "technology")
        self.assertGreater(
            calculate_campaign_fit(beauty_campaign, beauty_creator).fit_score,
            calculate_campaign_fit(beauty_campaign, technology_creator).fit_score,
        )

    def test_matching_exposes_terms(self) -> None:
        fit = calculate_campaign_fit(self.campaigns[1], next(row for row in self.influencers if row["category"] == "fitness"))
        self.assertIn("fitness", fit.matched_terms)
        self.assertGreater(fit.topic_score, 0)

    def test_invalid_weights_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RankingWeights(campaign_fit=Decimal("0.9"))

    def test_ranking_contributions_reconcile_to_total(self) -> None:
        result = calculate_ranking(
            Decimal("80"), Decimal("90"), Decimal("70"), Decimal("60")
        )
        self.assertEqual(result.overall_score, Decimal("79.0"))
        self.assertEqual(len(result.contributions), 4)

    def test_percentile_direction_can_be_reversed_for_cost(self) -> None:
        peers = [Decimal("10"), Decimal("20"), Decimal("30")]
        self.assertGreater(
            percentile_score(Decimal("10"), peers, higher_is_better=False),
            percentile_score(Decimal("30"), peers, higher_is_better=False),
        )

    def test_report_has_ranked_candidates_for_every_campaign(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = generate_ranking_report(SAMPLE_DIRECTORY, Path(directory) / "ranking.csv")
            with output.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 90)
            for campaign in self.campaigns:
                ranks = [int(row["rank"]) for row in rows if row["campaign_id"] == campaign["campaign_id"]]
                self.assertEqual(ranks, list(range(1, 31)))

            expected_top_categories = {
                "CAM-001": "beauty",
                "CAM-002": "fitness",
                "CAM-003": "travel",
            }
            for campaign_id, expected_category in expected_top_categories.items():
                top = next(
                    row
                    for row in rows
                    if row["campaign_id"] == campaign_id and row["rank"] == "1"
                )
                self.assertEqual(top["category"], expected_category)

    def test_tokenizer_normalizes_common_suffixes(self) -> None:
        self.assertEqual(tokenize("sustainable sustainability"), {"sustainable"})


if __name__ == "__main__":
    unittest.main()
