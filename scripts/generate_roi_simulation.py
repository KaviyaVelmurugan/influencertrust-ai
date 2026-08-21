"""Generate Phase 7 ROI scenario and sensitivity reports."""

from pathlib import Path

from influencertrust.simulator_reporting import generate_simulator_reports


PROJECT_ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    outputs = generate_simulator_reports(
        PROJECT_ROOT / "data" / "sample",
        PROJECT_ROOT / "reports" / "simulator",
    )
    for name, path in outputs.items():
        print(f"{name}: {path.relative_to(PROJECT_ROOT)}")
