# InfluencerTrust AI

InfluencerTrust AI is an explainable MarTech application for screening creators, comparing live YouTube performance, checking campaign requirements, and exploring ROI scenarios. It supports decisions; it does not claim to prove fraud or guarantee campaign outcomes.

**Release:** v1.0.0

**License:** [MIT](LICENSE)

## Why this project exists

Influencer selection often combines inconsistent spreadsheets, vanity metrics, subjective judgment, and uncertain financial assumptions. InfluencerTrust AI brings those steps into one reproducible workflow while exposing how every score is calculated and where evidence is missing.

## v1.0 capabilities

- Analyze campaign and influencer CSV files locally in the browser
- Rank creators using campaign fit, quality, risk signals, and cost efficiency
- Retrieve current public channel and recent-video statistics from YouTube Data API v3
- Compare multiple YouTube channels with objective-aware scoring
- Show engagement, reach efficiency, consistency, activity, and evidence confidence
- Audit captions for disclosures, hashtags, mentions, links, and prohibited terms
- Explore conservative, expected, and optimistic ROI scenarios
- Export rankings and YouTube shortlists to CSV
- Generate print-ready campaign reports for PDF saving
- Sign in with ChatGPT to save private project workspaces
- Install the dashboard as a Progressive Web App

## How scoring works

Connected YouTube channels are screened using public observations from up to 10 recent videos. Awareness campaigns emphasize reach, conversion campaigns emphasize engagement, and traffic campaigns balance both. The dashboard exposes every component and weight. Demographics, brand safety, content relevance, and conversion attribution remain explicit human-review requirements.

See [metric definitions](docs/METRICS.md), [matching and ranking](docs/MATCHING_AND_RANKING.md), and [data connectors](docs/DATA_CONNECTORS.md).

## Architecture

The release uses a Next.js/TypeScript Progressive Web App with Cloudflare-compatible server routes, YouTube Data API v3, Sign in with ChatGPT, and a D1-backed private project store. The Python analytics package remains available for reproducible batch reports and tests.

See the [architecture guide](docs/ARCHITECTURE.md) and [security guide](SECURITY.md).

## Run locally

```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:3000`. For live YouTube data, create `web/.env.local`:

```text
YOUTUBE_API_KEY=your_restricted_key
```

Environment files are ignored by Git. Restrict the key to YouTube Data API v3 and never commit it.

## Run tests

```powershell
cd web
npm test
```

For the Python analytics tests:

```powershell
$env:PYTHONPATH="src"
pytest
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Project requirements](docs/PROJECT_REQUIREMENTS.md)
- [Development roadmap](docs/ROADMAP.md)
- [Decision log](docs/DECISIONS.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Data connectors](docs/DATA_CONNECTORS.md)
- [Metric definitions](docs/METRICS.md)
- [Authenticity-risk design](docs/AUTHENTICITY_RISK.md)
- [Campaign matching and ranking](docs/MATCHING_AND_RANKING.md)
- [Caption compliance](docs/COMPLIANCE.md)
- [ROI simulator](docs/ROI_SIMULATOR.md)
- [Automated analysis pipeline](docs/AUTOMATED_PIPELINE.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)

## Responsible use

Scores are decision-support signals, not facts about a person's character or proof of fraudulent behavior. Financial outputs are sensitivity scenarios rather than forecasts. Review creator content, audience evidence, contracts, disclosures, brand safety, and campaign attribution before making a commercial decision.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. Report suspected vulnerabilities using the private process described in [SECURITY.md](SECURITY.md); do not publish secrets or exploit details in a public issue.

## License

Original source code is licensed under the [MIT License](LICENSE). YouTube content, platform data, trademarks, third-party datasets, and services remain subject to their respective terms.
