# Security policy

## Supported version

Security fixes are applied to the latest v1.x release.

## Reporting a vulnerability

Do not publish API keys, personal data, bypass instructions, or exploitable details in a public GitHub issue. Contact the repository owner privately with the affected feature, reproduction steps, impact, and suggested mitigation. Remove all real credentials and personal information from screenshots and logs.

## Security controls

- YouTube credentials are stored as server-side secrets and excluded from client bundles.
- `.env*`, build output, and local work files are ignored by Git.
- The YouTube key should be restricted to YouTube Data API v3 and rotated if exposed.
- Connector input accepts only 24-character channel IDs beginning with `UC`.
- External requests have timeouts and return normalized errors.
- API observations are not cached by the service worker.
- Private project endpoints require ChatGPT identity and enforce record ownership server-side.
- Saved project payloads are size-limited.
- Responses set content-type, framing, referrer, camera, microphone, and geolocation protections.

## Data and privacy

CSV analysis is browser-local by default. Saving a project is explicit and stores its campaigns, analysis state, and public YouTube observations in the signed-in user's private workspace. Users can delete saved projects from the application.

## Known limits

v1.0 does not provide enterprise audit logs, organization-level retention controls, private YouTube Analytics, or independent penetration-test certification. Deployments handling regulated or sensitive data require additional review.
