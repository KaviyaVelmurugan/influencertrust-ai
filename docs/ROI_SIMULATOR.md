# ROI Scenario Simulator

## Purpose

Phase 7 estimates how a campaign funnel could behave under explicit assumptions. It is a planning tool, not a forecast guarantee.

Each campaign has a base assumption set containing audience size, rates, order value, costs, and gross margin. The simulator applies three named factor sets:

| Scenario | Reach | CTR | Conversion rate |
|---|---:|---:|---:|
| Conservative | Base × 0.80 | Base × 0.80 | Base × 0.75 |
| Expected | Base × 1.00 | Base × 1.00 | Base × 1.00 |
| Optimistic | Base × 1.15 | Base × 1.20 | Base × 1.25 |

These multipliers are product hypotheses. They are not confidence intervals and do not assign probabilities.

## Funnel

```text
Reached audience = audience size × reach rate
Clicks = reached audience × click-through rate
Conversions = clicks × conversion rate
Revenue = conversions × average order value
```

Rates are capped at 100%. Expected conversions can be fractional because the result represents an expected value across repeated comparable campaigns.

## Costs and returns

```text
Total campaign cost = influencer fees + production cost + other campaign costs
ROAS = revenue / total campaign cost
Campaign ROI = (revenue − total campaign cost) / total campaign cost × 100
Gross profit = revenue × gross margin
Contribution ROI = (gross profit − total campaign cost) / total campaign cost × 100
```

Contribution ROI is the more commercially realistic indicator when product or service margin is available. A campaign can have attractive ROAS while still producing negative contribution ROI.

## Break-even analysis

```text
Margin per conversion = average order value × gross margin
Break-even conversions = total campaign cost / margin per conversion
Break-even conversion rate = break-even conversions / estimated clicks × 100
```

The break-even rate is unavailable when clicks or margin per conversion equal zero.

## Sensitivity analysis

The report increases each of these inputs independently by 10% and measures the change in contribution ROI:

- Reach rate
- Click-through rate
- Conversion rate
- Average order value
- Gross margin
- Influencer fees
- Production cost
- Other campaign costs

Because the first five revenue drivers are multiplicative in this baseline, an equal percentage change can produce the same local ROI effect. Cost-driver sensitivity helps show which expenditure categories have the largest impact. This is still one-variable-at-a-time sensitivity; it does not model correlations, uncertainty distributions, seasonality, or channel interactions.

## Limitations

- Synthetic assumptions demonstrate calculations only.
- Reach, clicks, and conversions are not guaranteed.
- Attribution and incrementality require tracked experiments or defensible attribution methods.
- Taxes, refunds, discounts, agency fees, customer lifetime value, and fixed overhead are excluded.
- Scenario multipliers require calibration using real campaigns before production use.
