# Development Roadmap

## Phase 1 — Product definition

**Status:** Complete

- Define the problem and target users
- Establish the MVP and explicit exclusions
- Define functional and non-functional requirements
- Define success criteria and responsible-use boundaries
- Add GitHub foundation and MIT license

## Phase 2 — Data contract and synthetic dataset

**Status:** Complete

- Design campaign, influencer, post, and outcome schemas
- Document every column and unit
- Create realistic synthetic sample data
- Implement schema validation
- Add data-quality tests

**Exit criterion:** Invalid data receives understandable errors, and valid sample data loads reproducibly.

## Phase 3 — Baseline analytics

**Status:** Complete

- Implement engagement, growth, efficiency, ROI, and ROAS formulas
- Write unit tests for edge cases
- Produce exploratory analysis
- Establish platform-aware normalization strategy

**Exit criterion:** All published metrics are documented, deterministic, and tested.

## Phase 4 — Authenticity-risk engine

**Status:** Complete

- Start with transparent rules and anomaly features
- Establish evaluation protocol
- Add an anomaly-detection baseline
- Return explanations and data coverage
- Publish an initial model card

**Exit criterion:** Every risk result includes evidence and no data leakage exists in evaluation.

## Phase 5 — Campaign matching and ranking

- Represent campaign briefs and influencer content
- Build a lexical baseline before semantic embeddings
- Add weighted, configurable ranking
- Explain matches, mismatches, and score contributions
- Evaluate ranking on a labelled test set when available

**Exit criterion:** A user can create a campaign and compare explained candidate rankings.

## Phase 6 — Caption compliance

- Implement deterministic hashtag, mention, link, and disclosure checks
- Add prohibited-term detection
- Add semantic requirement matching
- Display evidence per requirement

**Exit criterion:** Compliance output distinguishes deterministic checks from AI interpretations.

## Phase 7 — ROI simulator

- Define financial inputs and validation
- Implement conservative, expected, and optimistic cases
- Add sensitivity analysis
- Visualize how assumptions affect outcomes

**Exit criterion:** ROI outputs are mathematically verified and show all assumptions.

## Phase 8 — Web application

- Build the campaign workflow
- Build influencer exploration and comparison
- Add score explanations and warnings
- Add charts and scenario controls
- Meet accessibility and performance targets

**Exit criterion:** The complete MVP user journey works from one web interface.

## Phase 9 — Quality and release

- Complete automated testing
- Add security and privacy review
- Add Docker-based local setup
- Add screenshots, architecture, API docs, and model card
- Tag the first GitHub release

**Exit criterion:** A new contributor can reproduce the demo using only repository instructions.

## Phase 10 — LinkedIn publication

- Summarize the real problem and design decisions
- Present actual results and limitations
- Add architecture and dashboard visuals
- Explain lessons learned
- Link the GitHub release

**Exit criterion:** The article is evidence-based, understandable, and ready to publish.

## Future enhancements

- Approved live platform integrations
- Image and video compliance analysis
- OCR, speech transcription, and logo detection
- Audience overlap and graph analysis
- Campaign outcome attribution
- Budget optimization across creator portfolios
- Multi-tenant agency workflows
- Human-reviewed active learning and model monitoring
