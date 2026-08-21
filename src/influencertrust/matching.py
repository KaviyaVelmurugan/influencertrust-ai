"""Transparent lexical campaign-to-creator matching baseline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "at",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


@dataclass(frozen=True)
class CampaignFit:
    fit_score: Decimal
    topic_score: Decimal
    language_score: Decimal
    matched_terms: tuple[str, ...]
    missing_terms: tuple[str, ...]


def _stem(token: str) -> str:
    """Small, auditable normalizer for the lexical baseline."""

    replacements = (
        ("ability", "able"),
        ("ibility", "ible"),
        ("ality", "al"),
        ("ivity", "ive"),
        ("tion", "te"),
        ("ing", ""),
        ("ies", "y"),
        ("s", ""),
    )
    for suffix, replacement in replacements:
        if suffix == "s" and token.endswith("ss"):
            continue
        if token.endswith(suffix) and len(token) > len(suffix) + 3:
            return token[: -len(suffix)] + replacement
    return token


def tokenize(*values: str) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        for token in TOKEN_PATTERN.findall(value.lower().replace("|", " ")):
            if token not in STOP_WORDS:
                tokens.add(_stem(token))
    return tokens


def calculate_campaign_fit(
    campaign: dict[str, str],
    influencer: dict[str, str],
) -> CampaignFit:
    campaign_terms = tokenize(
        campaign["target_topics"],
        campaign["product_description"],
    )
    influencer_terms = tokenize(
        influencer["content_topics"],
        influencer["profile_text"],
        influencer["category"],
    )
    matched = campaign_terms & influencer_terms
    missing = campaign_terms - influencer_terms
    topic_score = (
        Decimal(len(matched)) / Decimal(len(campaign_terms)) * Decimal("100")
        if campaign_terms
        else Decimal("0")
    )
    language_score = (
        Decimal("100")
        if campaign["target_language"].lower() == influencer["primary_language"].lower()
        else Decimal("0")
    )
    fit_score = topic_score * Decimal("0.85") + language_score * Decimal("0.15")
    return CampaignFit(
        fit_score=fit_score,
        topic_score=topic_score,
        language_score=language_score,
        matched_terms=tuple(sorted(matched)),
        missing_terms=tuple(sorted(missing)),
    )
