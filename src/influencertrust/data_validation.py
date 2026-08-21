"""CSV contract validation for the InfluencerTrust AI sample datasets."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ValidationError:
    dataset: str
    row: int
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.dataset}: row {self.row}, {self.field}: {self.message}"


def _text(value: str) -> str:
    if not value.strip():
        raise ValueError("must not be empty")
    return value.strip()


def _integer(minimum: int = 0) -> Callable[[str], int]:
    def parse(value: str) -> int:
        parsed = int(value)
        if parsed < minimum:
            raise ValueError(f"must be at least {minimum}")
        return parsed

    return parse


def _number(minimum: float = 0, maximum: float | None = None) -> Callable[[str], float]:
    def parse(value: str) -> float:
        parsed = float(value)
        if parsed < minimum:
            raise ValueError(f"must be at least {minimum}")
        if maximum is not None and parsed > maximum:
            raise ValueError(f"must not exceed {maximum}")
        return parsed

    return parse


def _choice(*choices: str) -> Callable[[str], str]:
    allowed = set(choices)

    def parse(value: str) -> str:
        if value not in allowed:
            raise ValueError(f"must be one of: {', '.join(sorted(allowed))}")
        return value

    return parse


def _date(value: str) -> date:
    return date.fromisoformat(value)


def _boolean(value: str) -> bool:
    normalized = value.lower()
    if normalized not in {"true", "false"}:
        raise ValueError("must be true or false")
    return normalized == "true"


SCHEMAS: dict[str, dict[str, Callable[[str], object]]] = {
    "campaigns.csv": {
        "campaign_id": _text,
        "campaign_name": _text,
        "objective": _choice("awareness", "traffic", "conversions"),
        "product_description": _text,
        "target_location": _text,
        "target_language": _text,
        "target_topics": _text,
        "prohibited_terms": _text,
        "required_hashtags": _text,
        "required_mentions": _text,
        "required_disclosure": _text,
        "budget": _number(),
        "average_order_value": _number(),
        "start_date": _date,
        "end_date": _date,
        "currency": _choice("INR", "USD", "EUR", "GBP"),
    },
    "influencers.csv": {
        "influencer_id": _text,
        "handle": _text,
        "platform": _choice("instagram", "youtube", "tiktok"),
        "category": _text,
        "profile_text": _text,
        "location": _text,
        "primary_language": _text,
        "followers": _integer(),
        "following": _integer(),
        "average_likes": _number(),
        "average_comments": _number(),
        "average_views": _number(),
        "average_shares": _number(),
        "follower_growth_30d_pct": _number(-100, 1000),
        "engagement_rate_pct": _number(0, 100),
        "estimated_fee": _number(),
        "currency": _choice("INR", "USD", "EUR", "GBP"),
        "content_topics": _text,
    },
    "posts.csv": {
        "post_id": _text,
        "influencer_id": _text,
        "published_at": _date,
        "caption": _text,
        "likes": _integer(),
        "comments": _integer(),
        "views": _integer(),
        "shares": _integer(),
        "is_sponsored": _boolean,
    },
    "outcomes.csv": {
        "outcome_id": _text,
        "campaign_id": _text,
        "influencer_id": _text,
        "impressions": _integer(),
        "clicks": _integer(),
        "conversions": _integer(),
        "attributed_revenue": _number(),
        "influencer_fee": _number(),
        "production_cost": _number(),
        "currency": _choice("INR", "USD", "EUR", "GBP"),
    },
}

PRIMARY_KEYS = {
    "campaigns.csv": "campaign_id",
    "influencers.csv": "influencer_id",
    "posts.csv": "post_id",
    "outcomes.csv": "outcome_id",
}


def read_and_validate(path: Path) -> tuple[list[dict[str, str]], list[ValidationError]]:
    dataset = path.name
    schema = SCHEMAS[dataset]
    errors: list[ValidationError] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        actual_fields = reader.fieldnames or []
        missing = [field for field in schema if field not in actual_fields]
        unexpected = [field for field in actual_fields if field not in schema]
        for field in missing:
            errors.append(ValidationError(dataset, 1, field, "required column is missing"))
        for field in unexpected:
            errors.append(ValidationError(dataset, 1, field, "unexpected column"))
        rows = list(reader)

    seen: set[str] = set()
    primary_key = PRIMARY_KEYS[dataset]
    for row_number, row in enumerate(rows, start=2):
        for field, parser in schema.items():
            if field not in row:
                continue
            try:
                parser(row[field])
            except (TypeError, ValueError) as error:
                errors.append(ValidationError(dataset, row_number, field, str(error)))
        identifier = row.get(primary_key, "")
        if identifier in seen:
            errors.append(ValidationError(dataset, row_number, primary_key, "duplicate identifier"))
        seen.add(identifier)

        if dataset == "campaigns.csv":
            try:
                if _date(row["end_date"]) < _date(row["start_date"]):
                    errors.append(ValidationError(dataset, row_number, "end_date", "must be on or after start_date"))
            except (KeyError, ValueError):
                pass
        elif dataset == "outcomes.csv":
            for child, parent in (("clicks", "impressions"), ("conversions", "clicks")):
                try:
                    if int(row[child]) > int(row[parent]):
                        errors.append(ValidationError(dataset, row_number, child, f"must not exceed {parent}"))
                except (KeyError, ValueError):
                    pass

    return rows, errors


def validate_directory(directory: Path) -> list[ValidationError]:
    loaded: dict[str, list[dict[str, str]]] = {}
    errors: list[ValidationError] = []
    for filename in SCHEMAS:
        path = directory / filename
        if not path.exists():
            errors.append(ValidationError(filename, 0, "file", "required dataset is missing"))
            continue
        rows, dataset_errors = read_and_validate(path)
        loaded[filename] = rows
        errors.extend(dataset_errors)

    influencer_ids = {row["influencer_id"] for row in loaded.get("influencers.csv", [])}
    campaign_ids = {row["campaign_id"] for row in loaded.get("campaigns.csv", [])}
    for filename in ("posts.csv", "outcomes.csv"):
        for row_number, row in enumerate(loaded.get(filename, []), start=2):
            if row.get("influencer_id") not in influencer_ids:
                errors.append(ValidationError(filename, row_number, "influencer_id", "does not exist in influencers.csv"))
    for row_number, row in enumerate(loaded.get("outcomes.csv", []), start=2):
        if row.get("campaign_id") not in campaign_ids:
            errors.append(ValidationError("outcomes.csv", row_number, "campaign_id", "does not exist in campaigns.csv"))
    return errors


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate InfluencerTrust AI CSV datasets")
    parser.add_argument("directory", type=Path)
    arguments = parser.parse_args()
    errors = validate_directory(arguments.directory)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Validated {len(SCHEMAS)} datasets successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
