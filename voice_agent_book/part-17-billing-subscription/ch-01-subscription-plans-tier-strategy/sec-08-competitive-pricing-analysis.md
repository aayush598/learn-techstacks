# Section 08: Competitive Pricing Analysis

## Competitor Pricing Benchmarks

Understanding the competitive landscape is essential for pricing decisions. Voice agent platforms range from Twilio's raw infrastructure pricing ($0.014/min) to full-featured platforms like Retell AI ($0.07-$0.15/min) and Bland AI ($0.08-$0.12/min).

```
Competitor Pricing Comparison (per minute):
┌──────────────────────────────────────────────────────────────────┐
│ Company        │ Entry Price │ Mid Price  │ Enterprise │ Model   │
├────────────────┼─────────────┼────────────┼────────────┼─────────┤
│ Twilio         │ $0.014      │ $0.0125    │ Custom     │ Usage   │
│ Retell AI      │ $0.07       │ $0.06      │ Custom     │ Hybrid  │
│ Bland AI       │ $0.08       │ $0.06      │ Custom     │ Usage   │
│ Vapi           │ $0.05       │ $0.04      │ Custom     │ Usage   │
│ Synthflow      │ $39/mo      │ $159/mo    │ Custom     │ Flat    │
│ Air.ai         │ $30/mo      │ $300/mo    │ Custom     │ Hybrid  │
│ Our Platform   │ $49/mo      │ $199/mo    │ Custom     │ Hybrid  │
└─────────────────────────────────────────────────────────────────┘
```

Our strategy positions us in the mid-premium segment — higher than Twilio infrastructure but competitive with full-featured platforms. The bundled value (AI agents, voice cloning, analytics, integrations) justifies the premium.

## Willingness-to-Pay Analysis

Willingness-to-pay (WTP) analysis determines the price range customers accept. The Van Westendorp Price Sensitivity Meter surveys four price points:

- **Too cheap** (quality concern)
- **Cheap** (good value)
- **Expensive** (premium but consider)
- **Too expensive** (won't buy)

```
WTP Results for Voice Agent Platform (SMB Segment):
        Too Cheap          Cheap        Expensive      Too Expensive
          $15               $49           $199            $499
           ↓                 ↓              ↓               ↓
    ├─────────────┬───────────────┬───────────────┬──────────────┤
    │             │               │               │              │
          Indifference Price: $79-$149
          Optimal Price Point: $149-$199
          Point of Marginal Cheapness: $49
          Point of Marginal Expensiveness: $349
```

The optimal price point (OPP) for the Growth plan is $149-$199/month, which aligns with our $199/month price. The indifference price point (IDP) of $79-$149 suggests that Starter at $49 feels like good value.

## Value-Based Pricing

Value-based pricing sets prices based on the value delivered to the customer rather than costs. For voice agents, value is measured in:
- Labor cost replacement (call center agents at $15-30/hr)
- Revenue generation (sales calls converted)
- Operational efficiency (automated customer service)

A customer saving 100 hours of agent time per month (at $25/hr) gets $2,500 in value. Our Growth plan at $199 captures only 8% of that value — a strong value proposition.

```typescript
interface ValueMetric {
  customerSegment: string;
  valueDriver: string;
  valuePerUnit: number;
  ourCostPerUnit: number;
  valueCaptureRatio: number; // Our price / Customer value
  benchmarkUnit: string;
}

const valueAnalysis = [
  {
    customerSegment: 'SMB Call Center (10 agents)',
    valueDriver: 'Agent salary replacement',
    valuePerUnit: 25.00,    // $25/hr saved
    ourCostPerUnit: 0.049,  // $0.049/min
    valueCaptureRatio: 0.002, // 0.2% of value captured
    benchmarkUnit: 'minute',
  },
  {
    customerSegment: 'Enterprise Sales (50 reps)',
    valueDriver: 'Revenue per converted lead',
    valuePerUnit: 100.00,       // $100/lead
    ourCostPerUnit: 0.025,      // $0.025/min (volume)
    valueCaptureRatio: 0.00025, // 0.025% of value captured
    benchmarkUnit: 'minute',
  },
];
```

## Pricing Elasticity

Price elasticity measures how demand changes with price. SaaS products typically have inelastic demand (price increases don't proportionally reduce demand) because of switching costs and integrated workflows.

For our platform:
- Starter ($49): Elastic — customers are price-sensitive at signup
- Growth ($199): Moderate elasticity — value is clear to SMBs
- Pro ($999): Inelastic — switching costs are high for mid-market
- Enterprise (Custom): Highly inelastic — negotiation-based

```
Demand Curve by Segment:
Price ↑
  $999 │                    ┌── Enterprise (Inelastic)
       │                    │
  $199 │              ┌─────┼── Growth (Moderate)
       │              │     │
   $49 │        ┌─────┼─────┼── Starter (Elastic)
       │        │     │     │
    $0 └────────┴─────┴─────┴───→ Volume
              Low   Mid   High
```

## Competitive Positioning Matrix

Our competitive position is defined by two axes: feature completeness vs price. We position as "best value" — high feature completeness at a competitive price point.

```typescript
interface CompetitivePosition {
  featureCompleteness: number; // 1-10
  pricePosition: number;       // 1-10 (10 = most expensive)
  targetSegment: string;
  keyDifferentiator: string;
}

[
  { name: 'Twilio', features: 6, price: 3, segment: 'Developer', differentiator: 'Infrastructure' },
  { name: 'Retell AI', features: 8, price: 6, segment: 'Business', differentiator: 'AI Quality' },
  { name: 'Bland AI', features: 7, price: 5, segment: 'SMB', differentiator: 'Simplicity' },
  { name: 'Vapi', features: 7, price: 4, segment: 'Developer', differentiator: 'API-first' },
  { name: 'Our Platform', features: 9, price: 5, segment: 'Business', differentiator: 'Full Stack' },
];
```

## Open-Source Tools

- **Metabase** (Apache 2.0) — Self-hosted pricing analytics dashboards
- **PostgreSQL** — Store competitive intelligence data
- **SurveyJS** (MIT) — Build willingness-to-pay surveys
- **Google Sheets API** — Collaborative pricing analysis

## Integration Points

Competitive pricing analysis feeds into the plan catalog (Section 7), the pricing page A/B testing framework (Part 2), and the sales negotiation playbook (Chapter 10). It also informs the overage pricing tiers (Chapter 7 Section 2) and the credit pack pricing (Chapter 6 Section 4).

## Production Considerations

- Review competitive landscape quarterly
- Set up price monitoring alerts for competitor changes
- Track price elasticity with cohort analysis
- Survey churning customers about price sensitivity
- Monitor customer satisfaction with value-per-dollar
- Adjust pricing based on customer retention data

## Open-Source First Philosophy

Competitive pricing analysis doesn't require expensive tools. We use PostgreSQL to store competitor pricing data, Metabase for interactive dashboards, and SurveyJS for customer research surveys. All tools are open-source and self-hostable, avoiding thousands in monthly SaaS fees for pricing analytics.
