# Explainable Authenticity-Risk Engine

## Purpose

The Phase 4 engine helps a marketer decide which creator accounts deserve additional human review. It does **not** determine that an influencer is fake, dishonest, or fraudulent.

The initial engine is deliberately rule-based. This gives us a transparent baseline to evaluate before introducing anomaly detection or supervised machine learning.

## Signals

The version 1 rule set considers:

- Rapid 30-day follower growth
- Growth that is an outlier relative to platform peers
- Engagement substantially below the platform peer median
- Rapid growth combined with weak engagement
- Extreme follower-to-following ratios
- High view rate combined with lower-quartile engagement

Each triggered signal contributes visible points and a human-readable explanation. The final score is capped at 100.

## Risk bands

| Score | Band | Meaning |
|---:|---|---|
| 0–29 | Low | No strong rule-based warning in the available evidence |
| 30–59 | Medium | One or more signals merit review |
| 60–100 | High | Multiple or strong signals merit closer investigation |

These are screening thresholds, not calibrated probabilities.

## Peer benchmarking

Engagement, views, and growth are interpreted relative to creators on the same platform. Platform separation matters because Instagram, TikTok, and YouTube expose different interaction patterns and view definitions.

The MVP sample has 10 creators per platform. This is sufficient to demonstrate the workflow but not enough to establish production-grade benchmarks. Category-and-platform peer groups are deferred until larger datasets are available.

## Evidence coverage

Every result includes the percentage of expected signals available. A high score with incomplete coverage should be treated with greater caution. Coverage is not prediction confidence.

## Known limitations

- Public aggregate metrics cannot confirm purchased followers.
- The engine cannot currently inspect follower accounts or coordinated comment networks.
- Short observation windows can make legitimate viral growth look suspicious.
- Platform definitions and data-collection periods can differ.
- Rules are hypotheses that require validation on properly labelled and licensed data.
- Synthetic scenarios support software testing only; they do not measure real-world precision or recall.

## Future evaluation gate

Before presenting this engine as a predictive model, we will require:

1. A legally usable labelled dataset.
2. Grouped or time-aware train/test separation.
3. Precision, recall, F1, PR-AUC, calibration, and subgroup reporting.
4. A comparison against this rule-based baseline.
5. Human review of false positives and potentially harmful failure cases.
