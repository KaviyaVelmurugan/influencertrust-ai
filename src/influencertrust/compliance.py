"""Evidence-based sponsored-caption compliance checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from .matching import tokenize


COMPLIANCE_VERSION = "caption-compliance-v1.0"
HASHTAG_PATTERN = re.compile(r"#[a-z0-9_]+", re.IGNORECASE)
MENTION_PATTERN = re.compile(r"@[a-z0-9_.]+", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://[^\s]+", re.IGNORECASE)


@dataclass(frozen=True)
class RequirementResult:
    requirement_type: str
    required: tuple[str, ...]
    found: tuple[str, ...]
    missing: tuple[str, ...]
    score: Decimal
    weight: Decimal
    check_type: str


@dataclass(frozen=True)
class ComplianceAssessment:
    compliance_score: Decimal
    status: str
    requirements: tuple[RequirementResult, ...]
    prohibited_matches: tuple[str, ...]
    topic_coverage_pct: Decimal
    evidence: tuple[str, ...]
    limitations: tuple[str, ...]
    version: str = COMPLIANCE_VERSION


def _split(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split("|") if item.strip())


def _normalize_url(value: str) -> str:
    return value.lower().rstrip("/.,;:!?)")


def _contains_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text, re.IGNORECASE) is not None


def _exact_requirement(
    requirement_type: str,
    required: tuple[str, ...],
    observed: set[str],
    weight: Decimal,
) -> RequirementResult:
    normalized_required = {item.lower(): item for item in required}
    found_keys = sorted(set(normalized_required) & observed)
    missing_keys = sorted(set(normalized_required) - observed)
    score = (
        Decimal(len(found_keys)) / Decimal(len(required)) * Decimal("100")
        if required
        else Decimal("100")
    )
    return RequirementResult(
        requirement_type=requirement_type,
        required=required,
        found=tuple(normalized_required[key] for key in found_keys),
        missing=tuple(normalized_required[key] for key in missing_keys),
        score=score,
        weight=weight,
        check_type="deterministic",
    )


def assess_caption(campaign: dict[str, str], caption: str) -> ComplianceAssessment:
    hashtags = {item.lower() for item in HASHTAG_PATTERN.findall(caption)}
    mentions = {item.lower() for item in MENTION_PATTERN.findall(caption)}
    links = {_normalize_url(item) for item in URL_PATTERN.findall(caption)}

    checks = [
        _exact_requirement("hashtags", _split(campaign["required_hashtags"]), hashtags, Decimal("20")),
        _exact_requirement("mentions", _split(campaign["required_mentions"]), mentions, Decimal("15")),
        _exact_requirement(
            "links",
            tuple(_normalize_url(item) for item in _split(campaign["required_links"])),
            links,
            Decimal("15"),
        ),
    ]
    disclosure_required = (campaign["required_disclosure"],)
    disclosure_key = campaign["required_disclosure"].lower()
    if disclosure_key.startswith("#"):
        disclosure_found = disclosure_key in hashtags
    elif disclosure_key.startswith("@"):
        disclosure_found = disclosure_key in mentions
    else:
        disclosure_found = _contains_phrase(caption, campaign["required_disclosure"])
    checks.append(
        RequirementResult(
            requirement_type="disclosure",
            required=disclosure_required,
            found=disclosure_required if disclosure_found else (),
            missing=() if disclosure_found else disclosure_required,
            score=Decimal("100") if disclosure_found else Decimal("0"),
            weight=Decimal("20"),
            check_type="deterministic",
        )
    )

    target_terms = tokenize(campaign["target_topics"])
    caption_terms = tokenize(caption)
    matched_topics = target_terms & caption_terms
    missing_topics = target_terms - caption_terms
    topic_score = (
        Decimal(len(matched_topics)) / Decimal(len(target_terms)) * Decimal("100")
        if target_terms
        else Decimal("100")
    )
    checks.append(
        RequirementResult(
            requirement_type="campaign topics",
            required=tuple(sorted(target_terms)),
            found=tuple(sorted(matched_topics)),
            missing=tuple(sorted(missing_topics)),
            score=topic_score,
            weight=Decimal("20"),
            check_type="lexical interpretation",
        )
    )

    prohibited = tuple(
        term for term in _split(campaign["prohibited_terms"])
        if _contains_phrase(caption, term)
    )
    safety_score = Decimal("0") if prohibited else Decimal("100")
    checks.append(
        RequirementResult(
            requirement_type="prohibited terms",
            required=_split(campaign["prohibited_terms"]),
            found=prohibited,
            missing=(),
            score=safety_score,
            weight=Decimal("10"),
            check_type="deterministic",
        )
    )

    total = sum(check.score * check.weight / Decimal("100") for check in checks)
    deterministic_complete = all(not check.missing for check in checks if check.check_type == "deterministic" and check.requirement_type != "prohibited terms")
    if prohibited or total < Decimal("50"):
        status = "non_compliant"
    elif deterministic_complete and topic_score >= Decimal("50") and total >= Decimal("80"):
        status = "compliant"
    else:
        status = "needs_review"

    evidence = tuple(
        f"{check.requirement_type}: found {', '.join(check.found) if check.found else 'none'}; missing {', '.join(check.missing) if check.missing else 'none'}"
        for check in checks
    )
    return ComplianceAssessment(
        compliance_score=total,
        status=status,
        requirements=tuple(checks),
        prohibited_matches=prohibited,
        topic_coverage_pct=topic_score,
        evidence=evidence,
        limitations=(
            "Topic coverage is lexical and may miss paraphrases or context.",
            "Caption checks do not inspect images, video, audio, destination pages, or legal sufficiency.",
        ),
    )
