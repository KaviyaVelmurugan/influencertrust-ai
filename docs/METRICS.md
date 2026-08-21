# Baseline Marketing Metrics

Phase 3 establishes transparent calculations before machine learning. The reports are generated from validated source CSV files and contain no recommendation or authenticity score.

## Attention and efficiency metrics

### Engagement rate

```text
Engagement rate (%) =
    (average likes + average comments + average shares)
    / followers × 100
```

This MVP definition uses visible interactions and followers because those fields exist in the sample contract. It does not measure saves, unique reach, watch duration, or engagement quality. Cross-platform comparisons must therefore be treated cautiously.

### View rate

```text
View rate (%) = average views / followers × 100
```

A view rate above 100% is possible because non-followers can view content and one account may generate more than one platform-defined view.

### Estimated cost per engagement

```text
Estimated CPE = estimated influencer fee / average engagements
```

This is a planning approximation. It assumes a campaign post performs like the creator's historical average and excludes production cost unless explicitly added later.

## Funnel metrics

### Click-through rate

```text
CTR (%) = clicks / impressions × 100
```

### Conversion rate

```text
Conversion rate (%) = conversions / clicks × 100
```

### Cost per acquisition

```text
CPA = (influencer fee + production cost) / conversions
```

When conversions equal zero, CPA is reported as missing rather than zero or infinity.

## Financial metrics

### Profit

```text
Profit = attributed revenue − total campaign cost
```

### Return on ad spend

```text
ROAS = attributed revenue / total campaign cost
```

A ROAS of `1.60×` means ₹1.60 of attributed revenue for every ₹1.00 of campaign cost. It does not account for product costs or business overhead.

### Return on investment

```text
ROI (%) =
    (attributed revenue − total campaign cost)
    / total campaign cost × 100
```

ROI differs from ROAS because ROI uses the remaining profit in the numerator.

## Aggregation rule

Campaign-level rates are calculated from campaign totals:

```text
Campaign CTR = total clicks / total impressions
```

The application does not average creator-level percentages because small creators would otherwise receive the same influence on the result as large creators.

## Interpretation boundary

The sample `attributed_revenue` values are synthetic. Even with real data, attribution is not automatically causal: a tracked conversion may have been influenced by other channels. Phase 3 reports what the dataset assigns to the campaign; it does not prove incremental lift.
