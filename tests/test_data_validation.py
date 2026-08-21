import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from influencertrust.data_validation import validate_directory


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA = PROJECT_ROOT / "data" / "sample"


class DataValidationTests(unittest.TestCase):
    def test_sample_dataset_is_valid(self) -> None:
        self.assertEqual(validate_directory(SAMPLE_DATA), [])

    def test_unknown_influencer_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            target = Path(temp_directory)
            shutil.copytree(SAMPLE_DATA, target, dirs_exist_ok=True)
            posts_path = target / "posts.csv"
            with posts_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
                fields = list(rows[0])
            rows[0]["influencer_id"] = "INF-DOES-NOT-EXIST"
            with posts_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            messages = [str(error) for error in validate_directory(target)]
            self.assertTrue(any("does not exist in influencers.csv" in message for message in messages))

    def test_impossible_conversion_funnel_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_directory:
            target = Path(temp_directory)
            shutil.copytree(SAMPLE_DATA, target, dirs_exist_ok=True)
            outcomes_path = target / "outcomes.csv"
            with outcomes_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
                fields = list(rows[0])
            rows[0]["conversions"] = str(int(rows[0]["clicks"]) + 1)
            with outcomes_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            messages = [str(error) for error in validate_directory(target)]
            self.assertTrue(any("must not exceed clicks" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
