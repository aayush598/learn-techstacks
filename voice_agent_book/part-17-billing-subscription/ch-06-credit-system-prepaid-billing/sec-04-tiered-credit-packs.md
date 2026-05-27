# Section 04: Tiered Credit Packs

## Volume Discount Tiers

Credit packs are priced with volume discounts — larger packs offer better per-credit rates. This incentivizes larger purchases, improves cash flow, and reduces transaction costs.

```typescript
interface TieredCreditPack {
  id: string;
  name: string;
  credits: number;
  price: number;             // Price in cents
  perCreditRate: number;     // Price per credit (cents)
  discountPercent: number;   // Discount vs base rate
  bonusCredits?: number;
  popular?: boolean;
  maxPurchases?: number;     // Limit on purchases per period
}

const CREDIT_PACK_TIERS: TieredCreditPack[] = [
  {
    id: 'credits_500',
    name: '500 Credits',
    credits: 500,
    price: 500,              // $5.00
    perCreditRate: 1.0,      // $0.01/credit
    discountPercent: 0,
    popular: false,
  },
  {
    id: 'credits_2000',
    name: '2,000 Credits',
    credits: 2000,
    price: 1800,             // $18.00
    perCreditRate: 0.9,      // $0.009/credit
    discountPercent: 10,
    bonusCredits: 200,
    popular: false,
  },
  {
    id: 'credits_10000',
    name: '10,000 Credits',
    credits: 10000,
    price: 8000,             // $80.00
    perCreditRate: 0.8,      // $0.008/credit
    discountPercent: 20,
    bonusCredits: 2000,
    popular: true,
  },
  {
    id: 'credits_50000',
    name: '50,000 Credits',
    credits: 50000,
    price: 35000,            // $350.00
    perCreditRate: 0.7,      // $0.007/credit
    discountPercent: 30,
    bonusCredits: 15000,
    popular: false,
  },
  {
    id: 'credits_250000',
    name: '250,000 Credits',
    credits: 250000,
    price: 150000,           // $1,500.00
    perCreditRate: 0.6,      // $0.006/credit
    discountPercent: 40,
    bonusCredits: 100000,
    popular: false,
  },
];
```

## Bundle Options

Bundles combine credits with feature unlocks. For example, a "Voice + Analytics" bundle includes credits for voice calls plus advanced analytics access.

```typescript
interface CreditBundle {
  id: string;
  name: string;
  description: string;
  credits: number;
  includedFeatures: BundleFeature[];
  price: number;
  savingsPercent: number;    // vs buying separately
}

interface BundleFeature {
  featureKey: string;
  name: string;
  value: string;
  standalonePrice: number;
}

async function purchaseBundle(
  tenantId: string,
  bundleId: string
): Promise<void> {
  const bundle = getBundle(bundleId);
  const totalCredits = bundle.credits;

  // Process payment
  const paymentIntent = await stripe.paymentIntents.create({
    amount: bundle.price,
    currency: 'usd',
    customer: await getStripeCustomerId(tenantId),
    metadata: {
      tenant_id: tenantId,
      purchase_type: 'credit_bundle',
      bundle_id: bundleId,
    },
  });

  // On success, issue credits AND unlock features
  await ledgerService.recordTransaction({
    tenantId,
    type: CreditTransactionType.PURCHASE,
    amount: totalCredits,
    currency: 'credits',
    description: `Bundle: ${bundle.name}`,
    metadata: { source: 'bundle_purchase', reference: bundleId },
    effectiveAt: new Date().toISOString(),
  });

  for (const feature of bundle.includedFeatures) {
    await featureGateService.enableFeature(tenantId, feature.featureKey);
  }
}
```

## Promotional Packs

Promotional packs offer limited-time discounts or bonus credits. They are used for seasonal campaigns, reactivation offers, and customer retention.

```typescript
interface PromotionalPack {
  basePackId: string;
  bonusPercent: number;        // Bonus credits as percentage
  discountPercent: number;     // Price discount
  maxRedemptions: number;
  validFrom: string;
  validTo: string;
  campaignId: string;
  targetSegments?: string[];   // Target specific customer segments
}

async function createPromotionalPack(
  basePackId: string,
  campaign: PromotionalPack
): Promise<CreditPack> {
  const basePack = CREDIT_PACK_TIERS.find(p => p.id === basePackId);
  if (!basePack) throw new Error('Base pack not found');

  const bonusCredits = Math.floor(basePack.credits * (campaign.bonusPercent / 100));
  const discountedPrice = Math.floor(basePack.price * (1 - campaign.discountPercent / 100));

  return {
    id: `promo_${campaign.campaignId}_${basePackId}`,
    name: `${basePack.name} + ${bonusCredits} Bonus`,
    credits: basePack.credits + bonusCredits,
    price: discountedPrice,
    currency: basePack.currency,
    bonusCredits,
    description: `Limited time: ${campaign.bonusPercent}% bonus credits`,
    validityDays: basePack.validityDays,
    metadata: {
      isPromotional: true,
      campaignId: campaign.campaignId,
      originalPackId: basePackId,
      validFrom: campaign.validFrom,
      validTo: campaign.validTo,
    },
  };
}
```

## Credit Pack Pricing Strategy

Pricing credits involves balancing customer psychology with unit economics. Key considerations:

- **Perceived value**: Credit packs should feel like getting a deal
- **Anchoring**: Show the most expensive pack first to make mid-tier seem reasonable
- **Decoy effect**: Include a pack that makes the target pack look better
- **Breakage**: Some credits will expire unused, improving margins

```
Credit Pack Pricing Analysis:
┌──────────────────────────────────────────────────────────────────┐
│ Pack           │ Credits │ Price │ Per-Credit │ Discount │ Margin │
├────────────────┼─────────┼───────┼────────────┼──────────┼────────┤
│ 500 Credits    │ 500     │ $5    │ $0.0100    │ 0%       │ 70%    │
│ 2,000 Credits  │ 2,200*  │ $18   │ $0.0082    │ 18%      │ 74%    │
│ 10,000 Credits │ 12,000* │ $80   │ $0.0067    │ 33%      │ 78%    │
│ 50,000 Credits │ 65,000* │ $350  │ $0.0054    │ 46%      │ 82%    │
│ 250K Credits   │ 350,000*│ $1,500│ $0.0043    │ 57%      │ 85%    │
└─────────────────────────────────────────────────────────────────┘
*Includes bonus credits
```

## Open-Source Tools

- **PostgreSQL** — Credit pack catalog and promotion storage
- **BullMQ** (MIT) — Schedule promotional pack expiration
- **Redis** — Cache active promotions for fast retrieval
- **Stripe API** — Payment processing for pack purchases

## Integration Points

Tiered credit packs connect to the credit purchase flow (Section 2), the feature gate service (bundle unlocks), the promotion service (campaign management), and the billing UI (pack display).

## Production Considerations

- A/B test pack pricing and positioning
- Monitor average purchase value trends
- Track promotional pack redemption rates
- Analyze customer lifetime value by pack purchased
- Review per-credit cost and margin regularly

## Open-Source First Philosophy

Credit pack configuration is stored in version-controlled YAML files in the repository. PostgreSQL powers the runtime catalog. This eliminates the need for a pricing management system while maintaining full control over pack offerings and promotions.
