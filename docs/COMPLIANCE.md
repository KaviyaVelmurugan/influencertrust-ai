# Caption Compliance and Brand-Safety Checks

## Purpose

Phase 6 evaluates whether a campaign caption contains explicitly required elements and avoids configured prohibited terms. It returns evidence for each decision instead of only a score.

## Deterministic checks

The engine checks:

- Required hashtags
- Required account mentions
- Required campaign links
- Advertising disclosure text
- Configured prohibited terms

These checks are case-insensitive. URLs ignore trailing punctuation and slashes. Every missing or found element is shown in the report.

## Lexical topic check

The caption is also compared with campaign target topics using the same transparent token normalizer as the Phase 5 matching baseline.

```text
Topic coverage = matched target-topic terms / target-topic terms × 100
```

This check is explicitly labelled **lexical interpretation** because it can miss paraphrases and cannot understand whether a claim is truthful.

## Score composition

| Component | Weight |
|---|---:|
| Required hashtags | 20% |
| Required mentions | 15% |
| Required links | 15% |
| Advertising disclosure | 20% |
| Campaign-topic coverage | 20% |
| No prohibited terms | 10% |

## Status logic

- **Compliant:** All deterministic requirements pass, no prohibited term is found, topic coverage is at least 50%, and the score is at least 80.
- **Needs review:** The score is at least 50 but one or more requirements need attention.
- **Non-compliant:** A prohibited term is present or the score is below 50.

These statuses reflect configured campaign rules. They are not legal advice or a guarantee of regulatory compliance.

## Limitations

- Captions only; images, video frames, audio, and on-screen text are not inspected.
- A URL is checked for presence, not whether its destination is correct, safe, or available.
- Substring matching cannot understand negation or nuanced claim context.
- Disclosure rules differ by jurisdiction and platform.
- Prohibited-term lists must be supplied and reviewed by the campaign owner.
- Semantic embeddings or language models may improve paraphrase handling later, but must return evidence and be evaluated against this baseline.
