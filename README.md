# InfluencerTrust AI

InfluencerTrust AI is an explainable MarTech platform for evaluating influencer authenticity, matching creators to campaign briefs, checking sponsored-content requirements, and estimating campaign ROI.

The project is being developed as an original, portfolio-quality application. It uses public, synthetic, or user-uploaded data for its first release so that the demo remains reproducible without restricted social-media API access.

## Project status

**Phase 7 — ROI scenario simulator**

The MVP requirements, boundaries, success criteria, and development roadmap are documented in [`docs/PROJECT_REQUIREMENTS.md`](docs/PROJECT_REQUIREMENTS.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md).

The first data contract is documented in [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md). The committed sample data is deterministic and entirely synthetic.

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
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Metric definitions](docs/METRICS.md)
- [Authenticity-risk design](docs/AUTHENTICITY_RISK.md)
- [Campaign matching and ranking](docs/MATCHING_AND_RANKING.md)
- [Caption compliance](docs/COMPLIANCE.md)
- [ROI scenario simulator](docs/ROI_SIMULATOR.md)
- [Sample-data notes](data/README.md)

## Generate baseline reports

```powershell
$env:PYTHONPATH="src"
python scripts/generate_baseline_reports.py
```

The generated reports separate influencer-level attention metrics, outcome-level funnel metrics, and correctly aggregated campaign metrics.

## Generate authenticity-risk report

```powershell
$env:PYTHONPATH="src"
python scripts/generate_authenticity_report.py
```

The report contains rule-based screening signals, evidence coverage, limitations, and a versioned explanation. It must not be interpreted as proof of fraud.

## Generate campaign rankings

```powershell
$env:PYTHONPATH="src"
python scripts/generate_campaign_rankings.py
```

The ranking report exposes campaign-fit, authenticity, engagement-quality, and cost-efficiency components with their exact weighted contributions.

## Generate caption-compliance report

```powershell
$env:PYTHONPATH="src"
python scripts/generate_compliance_report.py
```

The report separates exact campaign requirements from lexical topic interpretation and includes evidence and limitations for every submission.

## Generate ROI simulations

```powershell
$env:PYTHONPATH="src"
python scripts/generate_roi_simulation.py
```

The simulator produces conservative, expected, and optimistic funnel outcomes plus contribution-margin sensitivity analysis. Scenarios are assumptions, not forecast probabilities.

## Open the web dashboard

The responsive dashboard combines campaign selection, explainable creator rankings, compliance health, and interactive ROI scenarios.

```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:3000` in a browser. The hosted version uses the same interface through a normal public link.

## License

The original source code in this repository is licensed under the [MIT License](LICENSE). Third-party datasets, models, platform content, and trademarks remain subject to their respective licenses and terms.
