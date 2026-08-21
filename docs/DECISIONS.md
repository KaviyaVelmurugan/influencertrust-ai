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
