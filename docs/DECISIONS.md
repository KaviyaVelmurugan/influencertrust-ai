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

## D-012: Start campaign matching with a lexical baseline

**Decision:** Rank topic relevance using visible token overlap and language matching before introducing embeddings.

**Reason:** We can inspect every match and later measure whether a semantic model produces a genuine improvement over this baseline.

## D-013: Normalize engagement and cost within platforms

**Decision:** Convert engagement rate and estimated cost per engagement into platform-specific percentiles.

**Reason:** Raw platform metrics are not directly comparable because platforms use different content formats, discovery systems, and view definitions.

## D-014: Separate deterministic compliance from interpretation

**Decision:** Hashtags, mentions, links, disclosures, and prohibited terms use exact checks; topic coverage is labelled as lexical interpretation.

**Reason:** Users should be able to distinguish objective missing elements from uncertain language understanding.

## D-015: Treat configured brand safety as narrower than legal compliance

**Decision:** Call the output campaign-rule compliance and include explicit legal and multimodal limitations.

**Reason:** A caption checker cannot establish compliance across jurisdictions or inspect claims made in images, audio, video, or linked pages.

## D-016: Show campaign ROI and contribution ROI separately

**Decision:** Preserve the simple revenue-based campaign ROI while adding gross-margin-based contribution ROI.

**Reason:** ROAS and revenue-based ROI can look attractive even when direct product or service costs make a campaign economically unprofitable.

## D-017: Treat scenarios as assumptions, not probabilities

**Decision:** Publish the exact conservative, expected, and optimistic multipliers without assigning likelihoods.

**Reason:** The synthetic dataset cannot support statistical confidence intervals or calibrated outcome distributions.
