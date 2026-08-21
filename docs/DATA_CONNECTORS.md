# Data connectors

InfluencerTrust AI uses official APIs rather than scraping. The Phase 14 YouTube connector retrieves public channel statistics, locates the channel's uploads playlist, and summarizes up to 10 recent public videos.

## YouTube setup

1. Create a Google Cloud project and enable **YouTube Data API v3**.
2. Create an API key and restrict it to the YouTube Data API.
3. Add the key to the hosted application's server environment as `YOUTUBE_API_KEY`.
4. Never commit the key to GitHub or expose it in browser code.

Without this server-side secret, the connector returns a clear `connector_not_configured` response while the rest of the dashboard remains available.

## Provenance and limitations

Connected results display their source and refresh timestamp. Channel-level totals and recent-video statistics are public API observations, not guaranteed campaign attribution. Private analytics, audience demographics, watch time, and conversions require creator authorization and are deliberately not inferred.

## Explainable campaign screening

After connection, the dashboard calculates a campaign-candidate score from four observable components: recent-video engagement, average-view reach relative to subscribers, view consistency, and the available sample size. Weights change with the selected objective: awareness emphasizes reach, conversions emphasize engagement, and traffic balances both.

The result is a screening recommendation—not an automatic hiring decision. It intentionally excludes inferred demographics, unverified authenticity claims, subjective brand safety, and conversion attribution.

## Multi-channel shortlist

Multiple connected channels can be ranked side by side for the active campaign. Switching campaigns recalculates every score with the new objective weights. The comparison exposes component scores, recommendation, evidence confidence, subscribers, average views, and engagement, and it can be exported as CSV for review.

Connected data remains session-based until the user explicitly selects **Save current** inside the private Projects workspace. A saved project includes its shortlist, source timestamps, and public YouTube observations. Loading the project restores the comparison, while deleting the project removes the saved copy.
