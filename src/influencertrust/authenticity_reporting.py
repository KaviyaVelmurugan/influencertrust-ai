"""Generate the Phase 4 explainable authenticity-risk report."""

from __future__ import annotations

import csv
from pathlib import Path

from .analytics import round_metric
from .authenticity import assess_creator, build_peer_benchmarks, creator_features
from .data_validation import validate_directory


def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def generate_authenticity_report(data_directory: Path, output_path: Path) -> Path:
    errors = validate_directory(data_directory)
    if errors:
        raise ValueError("Source data failed validation:\n" + "\n".join(map(str, errors)))

    rows = _read(data_directory / "influencers.csv")
    benchmarks = build_peer_benchmarks(rows)
    report: list[dict[str, object]] = []
    for row in rows:
        features = creator_features(row)
        benchmark = benchmarks[row["platform"]]
        assessment = assess_creator(features, benchmark)
        report.append(
            {
                "influencer_id": row["influencer_id"],
                "handle": row["handle"],
                "platform": row["platform"],
                "category": row["category"],
                "risk_score": assessment.risk_score,
                "risk_band": assessment.risk_band,
                "evidence_coverage_pct": assessment.evidence_coverage_pct,
                "calculated_engagement_rate_pct": round_metric(features["engagement_rate_pct"]),
                "view_rate_pct": round_metric(features["view_rate_pct"]),
                "follower_growth_30d_pct": row["follower_growth_30d_pct"],
                "platform_median_engagement_rate_pct": round_metric(benchmark.median_engagement_rate_pct),
                "signal_count": len(assessment.signals),
                "signals": " | ".join(f"{signal.code} (+{signal.points}): {signal.explanation}" for signal in assessment.signals),
                "limitations": " | ".join(assessment.limitations),
                "rule_version": assessment.rule_version,
            }
        )

    report.sort(key=lambda item: (-int(item["risk_score"]), str(item["influencer_id"])))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(report[0]))
        writer.writeheader()
        writer.writerows(report)
    return output_path
