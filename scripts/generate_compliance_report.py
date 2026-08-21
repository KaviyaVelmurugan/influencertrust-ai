"""Generate the Phase 6 campaign-caption compliance report."""

from pathlib import Path

from influencertrust.compliance_reporting import generate_compliance_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    output = generate_compliance_report(
        PROJECT_ROOT / "data" / "sample",
        PROJECT_ROOT / "reports" / "compliance" / "caption_compliance.csv",
    )
    print(output.relative_to(PROJECT_ROOT))
