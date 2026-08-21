# I Built InfluencerTrust AI: An Explainable MarTech Platform for Influencer Campaign Decisions

Influencer marketing decisions often begin with a spreadsheet full of followers, likes, fees, and engagement rates. The difficult part is not collecting numbers—it is deciding which numbers deserve trust, how a creator fits a campaign, and whether the expected business return justifies the cost.

I built **InfluencerTrust AI** to explore that problem as an end-to-end MarTech product rather than a collection of disconnected analytics scripts.

## The problem I wanted to solve

Brands need to answer several questions before working with a creator:

- Does this creator match the campaign objective?
- Are recent views and interactions reasonably consistent?
- What evidence supports the recommendation?
- Does the content meet sponsorship and disclosure requirements?
- Under different assumptions, what could ROI and ROAS look like?

A single unexplained “AI score” would not be enough. I wanted the application to expose its factors, weights, evidence coverage, and limitations.

## What I built

InfluencerTrust AI combines:

- Explainable creator ranking
- Live public YouTube channel and recent-video analysis
- Multi-creator campaign shortlists
- Caption and disclosure compliance checks
- Conservative, expected, and optimistic ROI scenarios
- CSV and PDF reporting
- Private saved projects through ChatGPT sign-in
- An installable Progressive Web App experience

The YouTube comparison adapts its weights to the campaign objective. Awareness emphasizes reach, conversions emphasize engagement, and traffic balances both. Every result shows the underlying engagement, reach efficiency, view consistency, activity, and evidence confidence.

## Responsible AI choices

One of the most important design decisions was defining what the system should not claim.

The application does not label a person as fraudulent. Authenticity outputs are screening signals, not proof. ROI values are sensitivity scenarios, not promises. Public YouTube data cannot establish private demographics, brand safety, or sales attribution, so those remain explicit review requirements.

I also used the official YouTube Data API rather than scraping, kept the API key in server-side secret storage, excluded API responses from offline caching, and enforced ownership checks for private saved projects.

## What I learned

This project strengthened my understanding of:

- Translating a marketing decision into measurable product requirements
- Building explainable scoring instead of opaque rankings
- Separating public observations from inferred or unavailable evidence
- Designing API integrations, error handling, data provenance, and privacy boundaries
- Connecting technical metrics to campaign ROI and business decisions
- Delivering a product through iterative phases, documentation, testing, and deployment

## Try the project

Live application: https://influencertrust-ai.kashvivelmurugan.chatgpt.site/

GitHub: https://github.com/KaviyaVelmurugan/influencertrust-ai

I would welcome feedback from people working in MarTech, influencer marketing, analytics, responsible AI, and product engineering—especially on which evidence should matter most when brands compare creators.

#MarTech #InfluencerMarketing #DataAnalytics #ResponsibleAI #NextJS #TypeScript #Python #PortfolioProject
