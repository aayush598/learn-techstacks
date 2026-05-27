# Section 05: Metered vs Flat Pricing

## Usage-Based Billing Models

Usage-based billing (metered pricing) charges customers per unit of consumption. For voice agents, the natural unit is minutes of audio processed — including both inbound and outbound calls, real-time transcription, and post-call analytics processing.

Metered billing has three primary models:
- **Pay-as-you-go**: No commitment, pay per unit consumed
- **Tiered**: Price per unit decreases at volume thresholds
- **Volume-based**: All units at a blended rate based on total volume

```typescript
// Stripe metered price configuration
interface MeteredPrice {
  id: string;
  product: string;
  nickname: string;
  billing_scheme: 'per_unit' | 'tiered';
  tiers_mode?: 'graduated' | 'volume';
  tiers?: Tier[];
  recurring: {
    interval: 'month' | 'year';
    usage_type: 'metered';
    aggregate_usage: 'sum' | 'last_during_period' | 'last_ever' | 'max';
  };
}

interface Tier {
  up_to: number | 'inf'; // Upper bound of tier
  unit_amount: number; // Price per unit in cents
  flat_amount?: number; // Flat fee for this tier
}
```

Our Pro plan uses graduated tiered pricing: $0.049/min for first 10,000, $0.035/min for next 40,000, $0.025/min for usage beyond. This rewards high-volume customers while maintaining a floor.

## Flat-Rate Simplicity

Flat-rate pricing charges a fixed monthly fee for a defined set of features and usage allowances. It is the simplest model from both implementation and customer understanding perspectives. The primary advantage is predictability — the customer always knows what to expect on their bill.

For the Starter plan, $49/month includes 1,000 minutes regardless of whether the customer uses any minutes. This creates "breakage" revenue (unused included units) that improves margins. The trade-off is that heavy users may churn if they feel their plan doesn't provide sufficient value.

```
Revenue Comparison by Usage Level:
┌─────────────────────────────────────────────────────────────────┐
│ Customer Type  │ Minutes │ Flat Rev │ Metered Rev │ Hybrid Rev  │
├────────────────┼─────────┼──────────┼─────────────┼─────────────┤
│ Light User     │   200   │   $49    │    $9.80    │    $49      │
│ Moderate User  │  1,500  │   $49    │   $73.50    │    $73.50   │
│ Heavy User     │  5,000  │   $49    │   $245.00   │    $174.50  │
│ Power User     │ 15,000  │   $49    │   $735.00   │    $374.50  │
└─────────────────────────────────────────────────────────────────┘
```

Flat-rate makes sense for low-usage segments where the simplicity premium is worth the overpayment. Starter customers are typically evaluating the product and don't mind paying for unused capacity.

## Hybrid Combinations

Hybrid pricing combines a flat base fee with metered overage. This is the optimal model for most SaaS products because it captures the best of both approaches: predictable base revenue plus upside from heavy usage.

Our implementation uses a three-part hybrid structure for Growth and Pro plans:

```typescript
interface HybridBillingConfig {
  components: BillingComponent[];
  consumptionOrder: ConsumptionOrder; // Which component is consumed first
}

interface BillingComponent {
  type: 'flat' | 'metered';
  metric?: string;
  included?: number;
  price: number;
  billingScheme: 'per_unit' | 'tiered' | 'flat_fee';
}

enum ConsumptionOrder {
  INCLUDED_FIRST, // Use included units before metered
  PREPAID_FIRST,  // Use prepaid credits before postpaid
  HYBRID_OPTIMAL, // Smart allocation across buckets
}
```

The Growth plan: $199 base (includes 10,000 min) + $0.025/min overage. Customers pay $199 regardless of usage up to 10,000 minutes, then their bill grows with usage beyond the cap.

## Predictability vs Flexibility

Predictability is the #1 factor in SaaS pricing satisfaction. Customers want to budget accurately, and unpredictable bills cause anxiety. Flexibility is the #2 factor — customers want to scale usage without commitment.

The hybrid model optimizes both: the base fee provides predictability for normal usage, while metered overage provides flexibility for spikes. The key design parameter is setting the included amount relative to typical usage patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Predictability vs Flexibility                   │
│                                                                   │
│ Predictable ←───────────────────┬───────────────────→ Flexible   │
│                                 │                                 │
│ Flat Rate     Base + Overage    │  Tiered Usage    Pay-as-you-go │
│ (Starter)     (Growth/Pro)      │  (Enterprise)    (Free)        │
└─────────────────────────────────────────────────────────────────┘
```

## Open-Source Tools for Metered Pricing

- **Stripe** (proprietary, free tier) — Metered billing with usage records
- **Unleash** (Apache 2.0) — Feature flags for testing pricing models
- **BullMQ** — Metered billing job scheduling
- **Redis** — Real-time usage counter for metering decisions

Stripe's metered billing is free to use (only transaction fees apply). The Stripe API supports creating usage records that are summed at the end of each billing period. This eliminates the need to build a custom billing engine.

## Integration Points

Metered vs flat pricing affects the usage metering pipeline (Chapter 2), Stripe subscription creation (Chapter 3), invoice generation (Chapter 4), overage handling (Chapter 7), and credit system design (Chapter 6). The pricing model choice cascades through the entire billing architecture.

## Production Considerations

- Monitor the ratio of base to overage revenue per plan
- Track customer satisfaction with billing predictability
- A/B test different hybrid structures (different included amounts)
- Analyze usage patterns to optimize included amounts
- Consider "bill smoothing" for customers with seasonal usage
- Provide usage estimates mid-period to prevent bill shock

## Open-Source First Philosophy

Instead of building a custom usage-based pricing engine or purchasing an expensive metering SaaS, we leverage Stripe's free metered billing API combined with open-source Redis for real-time counters. PostgreSQL stores our pricing configuration, and BullMQ handles the scheduled billing jobs. This stack costs nothing beyond infrastructure and Stripe transaction fees, making it accessible for early-stage voice agent startups.
