"""Generate Phase 3 baseline reports using only the Python standard library."""

from pathlib import Path

from influencertrust.baseline_reporting import generate_reports


PROJECT_ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    generated = generate_reports(
        PROJECT_ROOT / "data" / "sample",
        PROJECT_ROOT / "reports" / "baseline",
    )
    for name, path in generated.items():
        print(f"{name}: {path.relative_to(PROJECT_ROOT)}")
