# Automated browser analysis

Phase 10 lets a user select `campaigns.csv` and `influencers.csv` together. Files are parsed and analyzed inside the browser; the MVP does not upload or persist them.

## Validation

- Campaign data must contain `campaign_name` and `target_topics`.
- Influencer data must contain `handle`, `followers`, and `estimated_fee`.
- If either dataset is absent, the existing dashboard remains unchanged and shows a validation message.

## Explainable ranking

Each creator receives four components:

- Campaign fit (50%): lexical topic coverage, location match, and language match.
- Authenticity (25%): transparent screening deductions for unusually high following ratios, rapid growth paired with weak engagement, and very low engagement.
- Engagement quality (15%): engagement rate normalized to a 0–100 range.
- Cost efficiency (10%): fee position relative to the imported creator pool.

The score is decision support—not proof of authenticity, fraud, campaign success, or legal compliance.

## ROI scenarios

The three scenarios use explicit reach, click-through, and conversion assumptions. Revenue equals estimated conversions multiplied by average order value. Contribution profit applies a 65% contribution margin and subtracts the estimated fees of the top three creators.

These are sensitivity scenarios, not forecast probabilities. Production use should expose and calibrate the assumptions with observed campaign data.
