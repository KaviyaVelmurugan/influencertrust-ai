"""Generate Phase 6 caption-compliance evidence reports."""

from __future__ import annotations

import csv
from pathlib import Path

from .analytics import round_metric
from .compliance import assess_caption
from .data_validation import validate_directory


def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def generate_compliance_report(data_directory: Path, output_path: Path) -> Path:
    errors = validate_directory(data_directory)
    if errors:
        raise ValueError("Source data failed validation:\n" + "\n".join(map(str, errors)))

    campaigns = {row["campaign_id"]: row for row in _read(data_directory / "campaigns.csv")}
    submissions = _read(data_directory / "campaign_submissions.csv")
    report: list[dict[str, object]] = []
    for submission in submissions:
        assessment = assess_caption(campaigns[submission["campaign_id"]], submission["caption"])
        deterministic_missing = [
            f"{item.requirement_type}: {', '.join(item.missing)}"
            for item in assessment.requirements
            if item.check_type == "deterministic" and item.missing
        ]
        report.append(
            {
                "submission_id": submission["submission_id"],
                "campaign_id": submission["campaign_id"],
                "influencer_id": submission["influencer_id"],
                "compliance_score": round_metric(assessment.compliance_score),
                "status": assessment.status,
                "topic_coverage_pct": round_metric(assessment.topic_coverage_pct),
                "deterministic_missing": " | ".join(deterministic_missing),
                "prohibited_matches": "|".join(assessment.prohibited_matches),
                "evidence": " | ".join(assessment.evidence),
                "limitations": " | ".join(assessment.limitations),
                "version": assessment.version,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(report[0]))
        writer.writeheader()
        writer.writerows(report)
    return output_path
