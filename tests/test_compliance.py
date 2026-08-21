import csv
import tempfile
import unittest
from pathlib import Path

from influencertrust.compliance import assess_caption
from influencertrust.compliance_reporting import generate_compliance_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIRECTORY = PROJECT_ROOT / "data" / "sample"


class ComplianceTests(unittest.TestCase):
    def setUp(self) -> None:
        with (SAMPLE_DIRECTORY / "campaigns.csv").open("r", encoding="utf-8", newline="") as handle:
            self.campaign = next(csv.DictReader(handle))

    def test_complete_caption_is_compliant(self) -> None:
        caption = "Summer sustainable skincare. #EcoGlow #SummerSkin @ecoglow https://example.com/ecoglow #ad"
        assessment = assess_caption(self.campaign, caption)
        self.assertEqual(assessment.status, "compliant")
        self.assertEqual(assessment.compliance_score, 100)

    def test_missing_disclosure_needs_review(self) -> None:
        caption = "Summer sustainable skincare. #EcoGlow #SummerSkin @ecoglow https://example.com/ecoglow"
        assessment = assess_caption(self.campaign, caption)
        self.assertEqual(assessment.status, "needs_review")
        self.assertIn("#ad", next(item for item in assessment.requirements if item.requirement_type == "disclosure").missing)

    def test_prohibited_term_forces_non_compliance(self) -> None:
        caption = "Summer sustainable skincare and skin whitening. #EcoGlow #SummerSkin @ecoglow https://example.com/ecoglow #ad"
        assessment = assess_caption(self.campaign, caption)
        self.assertEqual(assessment.status, "non_compliant")
        self.assertIn("skin whitening", assessment.prohibited_matches)

    def test_exact_tokens_are_case_insensitive(self) -> None:
        caption = "Summer sustainable skincare. #ECOGLOW #SUMMERSKIN @ECOGLOW https://example.com/ecoglow/ #AD"
        assessment = assess_caption(self.campaign, caption)
        self.assertEqual(assessment.status, "compliant")

    def test_disclosure_hashtag_does_not_match_longer_hashtag(self) -> None:
        caption = "Summer sustainable skincare. #EcoGlow #SummerSkin @ecoglow https://example.com/ecoglow #adventure"
        assessment = assess_caption(self.campaign, caption)
        self.assertEqual(assessment.status, "needs_review")
        disclosure = next(item for item in assessment.requirements if item.requirement_type == "disclosure")
        self.assertEqual(disclosure.found, ())

    def test_report_covers_every_submission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = generate_compliance_report(SAMPLE_DIRECTORY, Path(directory) / "compliance.csv")
            with output.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 12)
            self.assertEqual({row["status"] for row in rows}, {"compliant", "needs_review", "non_compliant"})


if __name__ == "__main__":
    unittest.main()
