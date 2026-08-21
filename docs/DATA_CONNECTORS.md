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
