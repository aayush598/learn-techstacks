# Section 03: Pricing Model Selection

## Flat-Rate Pricing

Flat-rate pricing charges a fixed amount per billing period regardless of usage. It is the simplest model to implement and the easiest for customers to understand. Flat-rate works best when the product has clear value that doesn't vary significantly with usage, or when the target segment prefers predictable costs.

For our voice agent platform, flat-rate is used for the Starter tier ($49/month for 1,000 minutes). The simplicity reduces friction at signup but limits revenue upside from heavy users. The trade-off is predictable revenue against potential underpricing.

```typescript
interface FlatRatePlan {
  type: 'flat';
  price: number;
  billingCycle: 'monthly' | 'annual';
  includedUsage: {
    metric: string;
    amount: number;
  };
  overageEnabled: boolean;
}
```

## Per-Seat Pricing

Per-seat pricing charges per user or per agent. It scales naturally with team size and is common in collaborative products. For voice agents, per-seat pricing aligns with the value of team collaboration but fails to capture value from high-volume individual usage.

The Growth plan uses a hybrid per-seat + usage model: $199/month for 10 agents and 10,000 minutes included. Additional agents cost $20/seat/month. This combines predictability (base fee) with variable costs for heavy usage.

## Usage-Based Pricing

Usage-based pricing charges per unit of consumption (per minute, per call, per API request). It is the fairest model because customers only pay for what they use. Stripe calls this "metered billing" and supports it natively through usage records.

Pure usage-based pricing is ideal for the voice agent platform because:
- Usage directly correlates with value delivered
- Low barrier to entry (start small, scale up)
- Revenue scales with customer success
- No need to predict usage patterns

The trade-off is unpredictable bills for customers, which can cause churn anxiety. To mitigate this, we use caps and alerts (Chapter 7).

```
Flat vs Usage-Based Comparison:
┌─────────────────────────────────────────────────────────────────┐
│ Feature          │ Flat Rate       │ Usage-Based   │ Hybrid     │
├──────────────────┼─────────────────┼───────────────┼────────────┤
│ Predictability   │ High            │ Low           │ Medium     │
│ Revenue Potential│ Capped          │ Unlimited     │ High       │
│ Customer Trust   │ High            │ Medium        │ High       │
│ Implementation   │ Simple          │ Complex       │ Complex    │
│ Barrier to Entry │ Low             │ Lowest        │ Low        │
│ Upside Capture   │ Low             │ High          │ Medium     │
│ Churn Risk       │ Low             │ Medium-High   │ Low        │
│ Billing Ops Cost │ Low             │ Medium        │ Medium     │
└─────────────────────────────────────────────────────────────────┘
```

## Hybrid Pricing

Hybrid models combine an included base with usage-based overage. This provides predictability for normal usage while capturing upside from heavy usage. It is the dominant model in modern SaaS and the one we recommend for voice agent platforms.

Our pricing uses a three-part hybrid structure:

```typescript
interface HybridPrice {
  baseFee: number;           // Monthly platform fee
  includedUnits: number;     // Minutes in base fee
  overageRate: number;       // Per-minute overage cost
  seatFee?: number;          // Per-agent fee (if applicable)
  seatIncluded?: number;     // Agents included in base
}
```

The Starter plan: $49 base → 1,000 min included → $0.049/min overage
The Growth plan: $199 base → 10,000 min included → $0.025/min overage
The Pro plan: $999 base → 50,000 min included → $0.015/min overage

## Price Anchoring

Price anchoring is a cognitive bias where the first price seen becomes the reference point for all subsequent evaluations. In SaaS pricing, anchoring is implemented by placing the highest-priced option first (or furthest left) so that the middle option appears reasonable.

Our pricing page anchors with the Enterprise plan (Custom pricing) followed by Pro ($999), Growth ($199), and Starter ($49). This creates a contrast effect where Growth appears affordable compared to Enterprise, and Starter feels very accessible.

## Psychological Pricing

Research shows that certain price points perform better: $49 vs $50, $199 vs $200. The left-digit effect means that $49 feels significantly cheaper than $50, even though the difference is only $1. In B2B SaaS, however, overly rounded prices ($200, $1,000) can signal quality and simplicity.

For our voice agent platform, we use $0.99-ending prices for self-serve plans and round numbers for enterprise tiers. The Starter plan is $49/month (not $49.99) to signal professionalism. The Growth plan is $199/month, and Pro is $999/month.

```
Psychological Pricing Effects:
Price     → Perception
$49       → "Under $50, feels like a deal"
$199      → "Under $200, feels premium but accessible"
$999      → "Under $1,000, high-end but not outrageous"
$0.049/min → "Under 5 cents, feels cheap per unit"
```

## Open-Source Tools for Pricing Analysis

- **Price Intelligently** (proprietary) — Willingness-to-pay research tools
- **ProfitWell** (proprietary) — Pricing optimization metrics
- **PostgreSQL + Metabase** (open-source) — Self-hosted pricing analytics

Using Metabase (Apache 2.0) with PostgreSQL allows free-form pricing analysis without vendor lock-in. Connect your subscription data, usage data, and churn events to build custom pricing dashboards.

## Integration Points

The pricing model selection determines the billing engine design (Chapter 3), the usage metering pipeline (Chapter 2), and the overage calculation logic (Chapter 7). The chosen model also affects the invoice generation (Chapter 4) and the Stripe price catalog (Chapter 3 Section 3).

## Production Considerations

- Run pricing experiments with A/B testing framework
- Monitor conversion rates by plan
- Track average revenue per user (ARPU) by tier
- Analyze willingness-to-pay with Van Westendorp surveys
- Review pricing effectiveness quarterly
- Consider grandfathered pricing for existing customers

## Open-Source First Philosophy

Rather than expensive pricing optimization SaaS tools, we combine PostgreSQL analytics with open-source Metabase for dashboards. Pricing experiments are managed through standard A/B testing infrastructure (feature flags in Unleash) rather than proprietary pricing engines. This approach saves thousands per month while maintaining analytical rigor.
