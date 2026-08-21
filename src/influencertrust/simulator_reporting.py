"""Generate Phase 7 ROI scenario and sensitivity reports."""

from __future__ import annotations

import csv
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

from .analytics import round_metric
from .data_validation import validate_directory
from .roi_simulator import DEFAULT_SCENARIOS, ScenarioAssumptions, change_assumption, simulate


def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _result_row(result: object) -> dict[str, object]:
    values = asdict(result)
    return {
        key: round_metric(value) if isinstance(value, Decimal) else value
        for key, value in values.items()
    }


def generate_simulator_reports(data_directory: Path, output_directory: Path) -> dict[str, Path]:
    errors = validate_directory(data_directory)
    if errors:
        raise ValueError("Source data failed validation:\n" + "\n".join(map(str, errors)))

    assumptions = [
        ScenarioAssumptions.from_row(row)
        for row in _read(data_directory / "scenario_assumptions.csv")
    ]
    scenario_rows = [
        _result_row(simulate(item, factors))
        for item in assumptions
        for factors in DEFAULT_SCENARIOS
    ]

    sensitivity_rows: list[dict[str, object]] = []
    drivers = (
        "reach_rate_pct",
        "click_through_rate_pct",
        "conversion_rate_pct",
        "average_order_value",
        "gross_margin_pct",
        "influencer_fees",
        "production_cost",
        "other_campaign_costs",
    )
    expected = next(item for item in DEFAULT_SCENARIOS if item.name == "expected")
    for item in assumptions:
        baseline = simulate(item, expected)
        for driver in drivers:
            adjusted = simulate(change_assumption(item, driver, Decimal("1.10")), expected)
            baseline_roi = baseline.contribution_roi_pct
            adjusted_roi = adjusted.contribution_roi_pct
            sensitivity_rows.append(
                {
                    "campaign_id": item.campaign_id,
                    "driver": driver,
                    "change_pct": "10.00",
                    "baseline_contribution_roi_pct": round_metric(baseline_roi),
                    "adjusted_contribution_roi_pct": round_metric(adjusted_roi),
                    "roi_change_percentage_points": round_metric(
                        adjusted_roi - baseline_roi
                        if adjusted_roi is not None and baseline_roi is not None
                        else None
                    ),
                    "version": baseline.version,
                }
            )

    output_directory.mkdir(parents=True, exist_ok=True)
    outputs = {
        "scenarios": output_directory / "roi_scenarios.csv",
        "sensitivity": output_directory / "roi_sensitivity.csv",
    }
    for path, rows in (
        (outputs["scenarios"], scenario_rows),
        (outputs["sensitivity"], sensitivity_rows),
    ):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return outputs
