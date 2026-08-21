"""Generate the explainable Phase 4 authenticity-risk report."""

from pathlib import Path

from influencertrust.authenticity_reporting import generate_authenticity_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    output = generate_authenticity_report(
        PROJECT_ROOT / "data" / "sample",
        PROJECT_ROOT / "reports" / "authenticity" / "authenticity_risk.csv",
    )
    print(output.relative_to(PROJECT_ROOT))
