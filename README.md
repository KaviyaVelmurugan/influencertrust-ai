# InfluencerTrust AI

InfluencerTrust AI is an explainable MarTech platform for evaluating influencer authenticity, matching creators to campaign briefs, checking sponsored-content requirements, and estimating campaign ROI.

The project is being developed as an original, portfolio-quality application. It uses public, synthetic, or user-uploaded data for its first release so that the demo remains reproducible without restricted social-media API access.

## Project status

**Phase 1 — Product definition**

The MVP requirements, boundaries, success criteria, and development roadmap are documented in [`docs/PROJECT_REQUIREMENTS.md`](docs/PROJECT_REQUIREMENTS.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md).

## MVP capabilities

- Import and validate influencer data from CSV
- Calculate transparent engagement and efficiency metrics
- Identify suspicious activity and explain the risk signals
- Match influencers to a campaign brief
- Rank candidates using configurable, explainable scoring
- Check captions for hashtags, mentions, links, disclosures, and prohibited terms
- Simulate campaign revenue, ROI, and ROAS under multiple scenarios
- Compare candidates in a web dashboard

## Planned technology

- **Frontend:** Next.js and TypeScript
- **Backend:** FastAPI and Python
- **Database:** PostgreSQL with pgvector when semantic search is introduced
- **Analytics and ML:** pandas, scikit-learn, and sentence embeddings
- **Testing:** pytest and frontend component/end-to-end tests
- **Packaging:** Docker Compose

## Responsible use

Authenticity output will be presented as a risk estimate, not proof that a creator is fraudulent. Recommendations will expose their supporting factors, data coverage, uncertainty, and model version. Sensitive demographic inference is outside the MVP.

## Documentation

- [Project requirements](docs/PROJECT_REQUIREMENTS.md)
- [Development roadmap](docs/ROADMAP.md)
- [Decision log](docs/DECISIONS.md)

## License

The original source code in this repository is licensed under the [MIT License](LICENSE). Third-party datasets, models, platform content, and trademarks remain subject to their respective licenses and terms.
