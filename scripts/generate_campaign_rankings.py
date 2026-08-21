"""Generate Phase 5 campaign-specific influencer rankings."""

from pathlib import Path

from influencertrust.ranking_reporting import generate_ranking_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    output = generate_ranking_report(
        PROJECT_ROOT / "data" / "sample",
        PROJECT_ROOT / "reports" / "rankings" / "campaign_rankings.csv",
    )
    print(output.relative_to(PROJECT_ROOT))
