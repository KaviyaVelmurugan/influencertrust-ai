# Decision Log

This file records important product and engineering decisions so that the project remains understandable and the final article can explain why each choice was made.

## D-001: Build an original implementation

**Decision:** Use existing influencer-analysis projects for problem research only. Do not copy their code, model artifacts, datasets, branding, or repository structure.

**Reason:** The goal is to build a defensible portfolio project and understand every component.

## D-002: Begin with uploaded data

**Decision:** The MVP uses CSV uploads and synthetic sample data instead of requiring live social-platform integrations.

**Reason:** Platform access is restricted, changes frequently, and can prevent reviewers from reproducing the project.

## D-003: Treat authenticity as risk

**Decision:** Report suspicious-behaviour risk and supporting evidence rather than declaring accounts fake or fraudulent.

**Reason:** Available signals are incomplete and models can produce harmful false positives.

## D-004: Start with transparent baselines

**Decision:** Implement formulas, rules, and lexical matching before introducing more complex machine-learning components.

**Reason:** A complex model is useful only if it improves on a verified baseline.

## D-005: Separate ROI estimates from measured attribution

**Decision:** The MVP provides a scenario simulator. It will not claim that simulated revenue was caused by an influencer campaign.

**Reason:** Causal attribution requires tracked outcomes or controlled experiments that the initial dataset will not contain.

## D-006: Separate campaigns, influencers, posts, and outcomes

**Decision:** Store the four entities in linked CSV files with stable identifiers.

**Reason:** This preserves source-style observations, reduces duplication, and prevents calculated recommendation scores from contaminating raw inputs.

## D-007: Make sample data deterministic and synthetic

**Decision:** Generate the public sample with a fixed pseudo-random seed and clearly label it as synthetic.

**Reason:** Every contributor should obtain the same test data, while no real creator is profiled or misrepresented.

## D-008: Report undefined ratios as missing

**Decision:** A metric with a zero denominator returns a missing value rather than zero or infinity.

**Reason:** Zero would incorrectly imply poor performance, while infinity is not useful for decisions. The missing result makes insufficient evidence explicit.

## D-009: Aggregate totals before calculating rates

**Decision:** Campaign CTR, conversion rate, CPA, ROI, and ROAS are calculated from summed campaign inputs.

**Reason:** Averaging row-level ratios gives small and large observations equal weight and can materially misstate campaign performance.

## D-010: Establish an explainable risk baseline before machine learning

**Decision:** Phase 4 uses visible, versioned rules and platform peer benchmarks.

**Reason:** We do not yet have a licensed, trustworthy labelled dataset for training or evaluating a fraud classifier. A transparent baseline prevents unsupported accuracy claims and gives future models something meaningful to beat.

## D-011: Separate evidence coverage from confidence

**Decision:** Report the percentage of expected evidence present, not a model-confidence percentage.

**Reason:** A rule score is not a calibrated probability. Calling data coverage “confidence” would mislead users about certainty.
