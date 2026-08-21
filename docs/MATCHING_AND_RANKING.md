# Campaign Matching and Explainable Ranking

## Purpose

Phase 5 ranks creators for a particular campaign. It answers:

> Given the evidence currently available, which creators should a marketer review first, and why?

The score is a prioritization aid. It is not a conversion forecast or a guarantee of campaign success.

## Lexical campaign-fit baseline

Campaign terms come from:

- Target topics
- Product description
- Target language

Creator terms come from:

- Content topics
- Profile description
- Content category

Text is lowercased, tokenized, stripped of common stop words, and passed through a small visible suffix normalizer. The engine reports both matched and missing campaign terms.

```text
Topic coverage = matched campaign terms / campaign terms × 100

Campaign fit = topic coverage × 85% + language match × 15%
```

This baseline intentionally avoids opaque embeddings. Semantic embeddings will be considered only after we can measure whether they improve ranking relevance.

## Ranking components

The default overall score is:

```text
Campaign fit       × 50%
Authenticity       × 25%
Engagement quality × 15%
Cost efficiency    × 10%
```

### Authenticity

```text
Authenticity component = 100 − authenticity-risk score
```

This is a scoring transformation, not an authenticity probability.

### Engagement quality

The creator's calculated engagement rate is converted to a percentile within the same platform. Platform peer normalization prevents raw TikTok, Instagram, and YouTube engagement from being treated as directly equivalent.

### Cost efficiency

Estimated cost per engagement is converted to a reversed platform percentile: lower estimated cost receives a higher component score.

The estimate assumes a sponsored post performs like the creator's historical average. It is not a negotiated quote or observed campaign result.

## Explainability

Every ranked record includes:

- Overall score and rank
- Four component scores
- Authenticity-risk band
- Matched campaign terms
- Missing campaign terms
- Exact component weights and contributions
- Weight-policy version

## Current exclusions

- Location fit is not scored because the campaign uses country-level targeting while creator records contain city-level text without a verified geographic hierarchy.
- Audience demographics are not inferred.
- Historical conversions are not yet used to predict future conversions.
- Caption compliance is introduced separately in Phase 6.
- Semantic similarity and multilingual translation are deferred.

## Evaluation requirement

The current rankings demonstrate system behaviour on synthetic data. Before claiming recommendation quality, we need human relevance judgements or historical campaign-selection outcomes and ranking metrics such as Precision@K or NDCG@K.
