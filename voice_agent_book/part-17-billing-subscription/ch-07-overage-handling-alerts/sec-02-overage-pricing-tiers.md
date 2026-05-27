# Section 02: Overage Pricing Tiers

## Per-Unit Overage Costs

Overage pricing can be structured in several ways. The simplest approach is a flat per-unit rate for all overage usage. More sophisticated approaches use tiered pricing that decreases per-unit cost at higher volumes.

```typescript
interface OveragePriceTier {
  meterId: string;
  planId: string;
  pricingModel: 'flat' | 'tiered_graduated' | 'tiered_volume' | 'blended';
  tiers: OverageTier[];
  minOverageCharge?: number;     // Minimum overage charge
  maxOverageCharge?: number;     // Cap on overage charges
}

interface OverageTier {
  name: string;
  fromUnits: number;             // Starting unit for this tier
  toUnits: number | 'inf';       // Ending unit for this tier
  perUnitRate: number;           // Price per unit in cents
  description: string;
}

const OVERAGE_PRICING_EXAMPLES = {
  starter_minutes: {
    meterId: 'monthly_minutes',
    planId: 'starter',
    pricingModel: 'flat',
    tiers: [
      { name: 'Overage', fromUnits: 0, toUnits: 'inf', perUnitRate: 0.049, description: 'Per minute overage' },
    ],
    minOverageCharge: 0,
  },
  growth_minutes: {
    meterId: 'monthly_minutes',
    planId: 'growth',
    pricingModel: 'tiered_graduated',
    tiers: [
      { name: 'Tier 1', fromUnits: 0, toUnits: 5000, perUnitRate: 0.035, description: 'First 5,000 overage minutes' },
      { name: 'Tier 2', fromUnits: 5000, toUnits: 20000, perUnitRate: 0.025, description: 'Next 15,000 overage minutes' },
      { name: 'Tier 3', fromUnits: 20000, toUnits: 'inf', perUnitRate: 0.015, description: 'Additional overage minutes' },
    ],
  },
};
```

## Volume-Based Discounting

Volume-based overage pricing reduces the per-unit cost as customers use more. This rewards heavy users and reduces the incentive to churn to a higher plan. The discount structure must be carefully calibrated to not cannibalize plan upgrades.

```typescript
function calculateVolumeDiscount(
  totalOverage: number,
  tiers: OverageTier[]
): number {
  let totalCost = 0;
  let remaining = totalOverage;

  // Graduated tier pricing
  for (const tier of tiers) {
    if (remaining <= 0) break;

    const tierUnits = tier.toUnits === 'inf'
      ? remaining
      : Math.min(tier.toUnits - tier.fromUnits, remaining);

    totalCost += tierUnits * tier.perUnitRate;
    remaining -= tierUnits;
  }

  return Math.round(totalCost * 100) / 100; // Round to cents
}

// Example: 25,000 overage minutes on Growth plan
// Tier 1: 5,000 × $0.035 = $175.00
// Tier 2: 15,000 × $0.025 = $375.00
// Tier 3: 5,000 × $0.015 = $75.00
// Total: $625.00 (Effective rate: $0.025/min)
```

## Flat Overage Fees

Some plans use flat overage fees instead of per-unit pricing. A flat fee grants a bundle of additional usage at a fixed price. This simplifies billing for customers while providing predictable additional revenue.

```typescript
interface FlatOveragePack {
  id: string;
  planId: string;
  meterId: string;
  additionalUnits: number;
  flatFee: number;
  description: string;
  autoApply: boolean;   // Automatically apply when overage detected
}

const FLAT_OVERAGE_PACKS = [
  {
    id: 'starter_extra_500',
    planId: 'starter',
    meterId: 'monthly_minutes',
    additionalUnits: 500,
    flatFee: 1999,    // $19.99
    description: '500 extra minutes',
    autoApply: false,
  },
  {
    id: 'growth_extra_2000',
    planId: 'growth',
    meterId: 'monthly_minutes',
    additionalUnits: 2000,
    flatFee: 4999,    // $49.99
    description: '2,000 extra minutes',
    autoApply: true,
  },
];
```

## Competitive Overage Rates

Overage rates should be benchmarked against competitors to ensure competitiveness. Rates that are too high will cause customer churn; rates that are too low will leave money on the table.

```typescript
interface CompetitiveOverageAnalysis {
  meter: string;
  ourRate: number;
  competitorRates: Array<{
    name: string;
    rate: number;
    notes: string;
  }>;
  position: 'premium' | 'competitive' | 'discount';
}

const competitiveAnalysis: CompetitiveOverageAnalysis[] = [
  {
    meter: 'monthly_minutes',
    ourRate: 0.035,    // Growth tier 1
    competitorRates: [
      { name: 'Twilio', rate: 0.014, notes: 'Infrastructure only, no AI features' },
      { name: 'Retell AI', rate: 0.07, notes: 'Full-featured platform' },
      { name: 'Bland AI', rate: 0.08, notes: 'Enterprise focused' },
      { name: 'Vapi', rate: 0.05, notes: 'Developer platform' },
    ],
    position: 'competitive',
  },
];
```

## Overage Pricing Strategy

The overage pricing strategy balances several factors:

- **Upgrade incentive**: Overage rates should be higher than the per-unit cost of the next tier, incentivizing upgrades
- **Customer satisfaction**: Rates should be fair and transparent
- **Revenue optimization**: Capture value from heavy users without causing churn
- **Simplicity**: Customers should be able to estimate their overage costs

```
Overage Pricing Strategy:
┌──────────────────────────────────────────────────────────────────┐
│ Plan     │ Included │ Overage Rate │ Next Tier │ Upgrade Value  │
├──────────┼──────────┼──────────────┼───────────┼────────────────┤
│ Starter  │ 1,000    │ $0.049/min   │ Growth    │ $150            │
│          │          │              │ (10,000)  │                 │
│ Growth   │ 10,000   │ $0.035/min   │ Pro       │ $800            │
│          │          │ (tiered)     │ (50,000)  │                 │
│ Pro      │ 50,000   │ $0.02/min    │ Enterprise│ Custom          │
│          │          │ (negotiated) │           │                 │
└──────────────────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **PostgreSQL** — Overage pricing configuration storage
- **Redis** — Cache overage pricing for fast calculation
- **Stripe API** — Submit tiered overage prices as usage records
- **Metabase** (Apache 2.0) — Overage revenue analysis dashboards

## Integration Points

Overage pricing connects to the plan catalog (rate configuration), the overage calculation engine (Section 1), the invoice system (Section 5), and the notification system (Section 3).

## Production Considerations

- Review overage rates quarterly against competitor changes
- A/B test different overage pricing structures
- Monitor overage revenue as percentage of total revenue
- Track upgrade rates from overage notifications
- Ensure overage pricing is clearly communicated in the UI

## Open-Source First Philosophy

Overage pricing is configured in the plan catalog YAML files and stored in PostgreSQL. Redis caches rates for fast calculation. This open-source approach avoids proprietary pricing engines while providing sophisticated tiered overage pricing capabilities.
