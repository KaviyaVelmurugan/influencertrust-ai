# Project Requirements

## 1. Product definition

**Product name:** InfluencerTrust AI  
**Category:** MarTech / influencer marketing intelligence  
**Primary user:** A brand or marketing analyst planning an influencer campaign

### Problem

Brands frequently compare influencers using follower count and raw engagement. Those measurements do not reliably reveal audience authenticity, campaign relevance, content compliance, or likely financial value.

### Proposed solution

InfluencerTrust AI combines transparent analytics with explainable AI to help a marketer shortlist creators for a specific campaign. It evaluates available evidence, ranks candidates, identifies risks, and simulates potential campaign outcomes.

### Product promise

> Help a marketer understand which influencer fits a campaign, why the influencer was recommended, what risks exist, and what outcome range may be financially reasonable.

## 2. Objectives

1. Make influencer comparison campaign-specific instead of follower-count driven.
2. Detect suspicious patterns without making unsupported accusations.
3. Explain every recommendation using visible metrics and evidence.
4. Check whether a proposed or published caption satisfies campaign rules.
5. connect marketing performance to costs, conversions, revenue, ROI, and ROAS.
6. Produce a reproducible public demo that does not require private platform credentials.

## 3. Target users

### Primary persona: Marketing analyst

- Creates campaign briefs
- Uploads candidate influencer data
- Compares creators
- Reviews risk signals
- Estimates campaign outcomes
- Exports a recommendation

### Secondary persona: Small-business owner

- Has limited analytics expertise
- Needs simple explanations
- Wants to understand whether an influencer's fee is financially reasonable

### Future persona: Agency campaign manager

- Manages multiple clients and campaigns
- Requires collaboration, history, permissions, and reporting
- This persona is not fully supported in the MVP

## 4. Core user journey

1. The user creates a campaign brief.
2. The user uploads a CSV containing candidate influencer and content metrics.
3. The application validates the data and reports missing or unreliable fields.
4. The application calculates baseline marketing metrics.
5. The authenticity module identifies suspicious patterns and explains them.
6. The matching module compares creator content with the campaign brief.
7. The ranking engine combines campaign fit, authenticity, engagement quality, brand safety, and cost efficiency.
8. The user changes ranking weights to reflect campaign priorities.
9. The compliance checker evaluates a candidate caption.
10. The ROI simulator shows conservative, expected, and optimistic outcomes.
11. The user reviews and exports the recommendation.

## 5. MVP functional requirements

### FR-01: Campaign brief

The user can define:

- Campaign name and objective
- Product or service description
- Target location and language
- Relevant topics or keywords
- Prohibited topics or competitor terms
- Required hashtags, mentions, links, and disclosure text
- Budget and expected average order value

### FR-02: CSV ingestion

The system must:

- Accept a documented CSV schema
- Validate types, ranges, required columns, and duplicate identifiers
- Display actionable validation errors
- Preserve the original uploaded values separately from derived metrics
- Provide a synthetic sample dataset

### FR-03: Baseline analytics

The system calculates, where supported by the data:

- Engagement rate
- Comment-to-like ratio
- View-to-follower ratio
- Follower growth rate
- Cost per engagement
- Conversion rate
- ROI and ROAS

Every formula must be documented and unit tested.

### FR-04: Authenticity-risk analysis

The system evaluates signals such as:

- Follower-growth spikes
- Engagement inconsistency
- Implausible view/follower relationships
- Repetitive or low-information comments when comment data is present
- Extreme follower/following ratios

The response must contain:

- Risk score from 0 to 100
- Low, medium, or high risk band
- Contributing signals
- Data coverage and missing evidence
- Model or rule-set version

The UI must not label an account as fraudulent based only on this output.

### FR-05: Campaign matching

The system compares campaign requirements with influencer categories, profile text, and available captions. It returns a campaign-fit score and evidence showing the strongest matches and mismatches.

### FR-06: Explainable ranking

The overall recommendation score uses visible components:

- Campaign fit
- Authenticity confidence
- Engagement quality
- Brand-safety/compliance score
- Cost efficiency

Users can change component weights. The system must display the score formula and must not silently alter weights.

### FR-07: Caption compliance

The system checks:

- Required hashtags
- Required mentions
- Required links
- Advertising disclosure text
- Required campaign concepts
- Prohibited or competitor terms

The output identifies evidence for each pass, warning, or failure.

### FR-08: ROI simulator

The simulator accepts assumptions for reach, click-through rate, conversion rate, average order value, influencer fee, production cost, and other campaign costs.

It produces conservative, expected, and optimistic scenarios for:

- Reach and engagement
- Clicks and conversions
- Revenue
- Cost per acquisition
- ROI
- ROAS

Predictions must be clearly labelled as estimates based on user-supplied or historical assumptions.

### FR-09: Dashboard

The dashboard supports:

- Influencer table and filters
- Candidate comparison
- Score explanations
- Risk warnings
- Scenario comparison
- Data-quality indicators

## 6. Non-functional requirements

- **Reproducibility:** The public demo works with synthetic sample data.
- **Explainability:** Every score exposes factors, inputs, and limitations.
- **Reliability:** Metric functions and critical ranking logic have automated tests.
- **Security:** Uploaded files are validated; secrets are never committed; input size is limited.
- **Privacy:** The MVP avoids sensitive demographic inference and unnecessary personal data.
- **Accessibility:** Core flows support keyboard navigation and readable contrast.
- **Performance:** A sample of 1,000 influencers should load and rank interactively on a development machine.
- **Maintainability:** Business rules, model code, API handlers, and UI code remain separated.

## 7. MVP exclusions

The following are explicitly deferred:

- Live scraping or bypassing platform restrictions
- Automated accusations of fraud
- Facial recognition or sensitive-attribute inference
- Fully automated campaign purchasing
- Guaranteed revenue predictions
- Real-time Instagram, TikTok, or X integration
- Image, video, OCR, logo, and speech analysis
- Multi-tenant agency billing and enterprise permissions
- Automatic model deployment based on unreviewed user feedback

## 8. Initial scoring design

The first version uses a transparent weighted score:

```text
Overall score =
    campaign-fit score       × campaign-fit weight
  + authenticity confidence × authenticity weight
  + engagement quality      × engagement weight
  + compliance/brand safety × compliance weight
  + cost efficiency         × cost-efficiency weight
```

Default weights will be documented and treated as a product hypothesis. They will not be described as scientifically optimal until evaluated with campaign outcome data.

## 9. Success criteria

### Product success

- A new user can upload the sample data, create a campaign, and obtain an explained ranking.
- Every displayed score can be traced to inputs and documented calculations.
- The user can compare at least three influencers and adjust ranking weights.
- The ROI simulator displays three scenarios and prevents invalid financial inputs.

### Engineering success

- A clean setup works from the README.
- Critical calculation and validation tests pass automatically.
- No credentials, personal datasets, generated caches, or unsafe serialized models are committed.
- API input and output schemas are documented.

### Model success

- Evaluation uses train/test separation without resampling leakage.
- Classification reports precision, recall, F1, PR-AUC, and calibration where applicable.
- Ranking evaluation is defined before claims of recommendation quality are published.
- Known limitations and subgroup checks are included in a model card.

### Publication success

- GitHub contains an MIT license, reproducible demo, screenshots, architecture, tests, and limitations.
- The LinkedIn article reports actual findings and lessons instead of unsupported performance claims.

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Social API access is unavailable or expensive | Use versioned sample uploads for the MVP |
| Synthetic data creates unrealistic model results | Use it only for product demonstration and state that clearly |
| A risk score harms a legitimate creator | Use cautious language, evidence, uncertainty, and human review |
| ROI estimates are interpreted as guarantees | Show assumptions, ranges, sensitivity, and disclaimers |
| Engagement metrics differ by platform | Store platform context and use platform-specific benchmarks later |
| Data leakage inflates results | Use pipelines, grouped/time-aware splits, and independent test data |
| Third-party data cannot be redistributed | Track licenses and publish only permitted or generated samples |

## 11. Definition of MVP complete

The MVP is complete when the documented sample dataset can pass through ingestion, analytics, authenticity assessment, campaign matching, ranking, compliance checking, and ROI simulation in one tested web workflow.
