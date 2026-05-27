# Section 01: Custom Pricing Data Model

## Custom Price Definitions

Enterprise customers require custom pricing that overrides standard plan rates. The data model supports per-customer price overrides with complete audit history.

```
[Standard Plan Prices]
    ↓
[Enterprise Customer Created]
    ├── Contract negotiated
    ├── Custom prices defined
    └── Override rules established
    ↓
[Custom Pricing Data Model]
    ├── Overrideable plan prices
    ├── Volume discounts
    ├── Committed usage discounts
    └── Feature-level pricing
    ↓
[Price Resolution]
    ├── Check for custom pricing
    ├── Apply override if exists
    ├── Fall back to standard pricing
    └── Return resolved price
```

```typescript
interface CustomPriceDefinition {
  id: string;
  tenantId: string;
  contractId: string;
  name: string;
  description?: string;
  type: CustomPriceType;
  value: number;
  currency: string;
  billingPeriod: BillingPeriod;
  effectiveDate: string;
  expirationDate?: string;
  status: 'active' | 'pending' | 'expired' | 'cancelled';
  priority: number;               // Higher priority overrides lower
  conditions?: PriceCondition[];
  metadata: Record<string, string>;
}

type CustomPriceType =
  | 'flat_rate'                  // Fixed monthly/annual price
  | 'per_unit'                   // Per-seat or per-resource pricing
  | 'tiered'                     // Tiered volume pricing
  | 'volume_discount'            // Percentage discount at volumes
  | 'committed_usage'            // Committed minimum with discount
  | 'overage_rate'               // Rate for usage beyond commitment;

type BillingPeriod = 'monthly' | 'quarterly' | 'annual' | 'one_time';

interface PriceCondition {
  type: 'min_quantity' | 'max_quantity' | 'min_commitment' | 'time_based';
  operator: 'gte' | 'lte' | 'eq' | 'between';
  value: number | [number, number];
}

interface ResolvedPrice {
  basePrice: number;
  effectivePrice: number;
  discountAmount: number;
  discountType: 'percentage' | 'fixed' | 'tiered';
  appliedRule: string;
  source: 'custom' | 'standard';
  validUntil?: string;
}

class CustomPricingEngine {
  async resolvePrice(
    tenantId: string,
    productId: string,
    quantity: number,
    date: string
  ): Promise<ResolvedPrice> {
    // Check for custom pricing first
    const customPrice = await this.getActiveCustomPrice(tenantId, productId, date);
    if (customPrice) {
      return this.applyCustomPrice(customPrice, quantity);
    }

    // Fall back to standard pricing
    const standardPrice = await this.getStandardPrice(productId);
    return {
      basePrice: standardPrice,
      effectivePrice: standardPrice * quantity,
      discountAmount: 0,
      discountType: 'fixed',
      appliedRule: 'standard_pricing',
      source: 'standard',
    };
  }

  private async applyCustomPrice(
    custom: CustomPriceDefinition,
    quantity: number
  ): Promise<ResolvedPrice> {
    switch (custom.type) {
      case 'flat_rate':
        return {
          basePrice: custom.value,
          effectivePrice: custom.value,
          discountAmount: 0,
          discountType: 'fixed',
          appliedRule: `custom_flat_${custom.id}`,
          source: 'custom',
        };

      case 'per_unit':
        return {
          basePrice: custom.value,
          effectivePrice: custom.value * quantity,
          discountAmount: 0,
          discountType: 'fixed',
          appliedRule: `custom_per_unit_${custom.id}`,
          source: 'custom',
        };

      case 'tiered': {
        const tier = this.findApplicableTier(custom, quantity);
        return {
          basePrice: tier.unitPrice,
          effectivePrice: tier.unitPrice * quantity,
          discountAmount: (custom.value - tier.unitPrice) * quantity,
          discountType: 'tiered',
          appliedRule: `tier_${tier.name}`,
          source: 'custom',
        };
      }

      default:
        throw new Error(`Unsupported custom price type: ${custom.type}`);
    }
  }
}
```

## Overrideable Plan Prices

Plan prices can be overridden at the customer level while maintaining the standard price structure.

```typescript
interface PlanPriceOverride {
  id: string;
  planId: string;
  tenantId: string;
  contractId: string;
  overrides: {
    monthlyPrice?: number;
    annualPrice?: number;
    perSeatPrice?: number;
    overageRate?: number;
    includedUnits?: number;
  };
  effectiveDate: string;
  expirationDate?: string;
  approvalRequired: boolean;
  approvedBy?: string;
  approvedAt?: string;
}

interface PriceOverrideAudit {
  id: string;
  planId: string;
  tenantId: string;
  previousPrices: Record<string, number>;
  newPrices: Record<string, number>;
  changedBy: string;
  changedAt: string;
  reason: string;
  approvalId?: string;
}

class PlanPriceOverrideService {
  async setOverride(
    override: PlanPriceOverride
  ): Promise<PlanPriceOverride> {
    // Validate override doesn't exceed max discount limits
    await this.validateOverrideLimits(override);

    // Store override
    const stored = await this.storeOverride(override);

    // Invalidate price cache for this tenant
    await this.invalidatePriceCache(override.tenantId, override.planId);

    return stored;
  }

  async getEffectivePrice(
    tenantId: string,
    planId: string,
    billingPeriod: 'monthly' | 'annual'
  ): Promise<number> {
    // Check cache first
    const cached = await this.getCachedPrice(tenantId, planId, billingPeriod);
    if (cached) return cached;

    // Check for override
    const override = await this.getActiveOverride(tenantId, planId);
    if (override) {
      const price = billingPeriod === 'monthly'
        ? (override.overrides.monthlyPrice ?? await this.getStandardPrice(planId, billingPeriod))
        : (override.overrides.annualPrice ?? await this.getStandardPrice(planId, billingPeriod));

      // Cache the result
      await this.cachePrice(tenantId, planId, billingPeriod, price);

      return price;
    }

    // Use standard pricing
    return this.getStandardPrice(planId, billingPeriod);
  }
}
```

## Volume Discounts

Volume discounts provide reduced pricing as usage increases across defined tiers.

```typescript
interface VolumeDiscountTier {
  id: string;
  name: string;
  minQuantity: number;
  maxQuantity?: number;
  discountPercent: number;
  unitPrice: number;
}

interface VolumeDiscountSchedule {
  id: string;
  tenantId: string;
  contractId: string;
  productId: string;
  tiers: VolumeDiscountTier[];
  accumulationPeriod: 'monthly' | 'quarterly' | 'annual';
  applyTo: 'all_units' | 'incremental_units';
}

class VolumeDiscountCalculator {
  async calculateVolumePrice(
    totalQuantity: number,
    schedule: VolumeDiscountSchedule
  ): Promise<VolumePriceResult> {
    const sortedTiers = schedule.tiers.sort((a, b) => a.minQuantity - b.minQuantity);
    const applicableTier = sortedTiers
      .reverse()
      .find(t => totalQuantity >= t.minQuantity);

    if (!applicableTier) {
      return {
        totalPrice: 0,
        unitPrice: 0,
        discountPercent: 0,
        discountAmount: 0,
        tier: 'no_tier',
      };
    }

    if (schedule.applyTo === 'all_units') {
      // Discount applies to all units
      const totalPrice = totalQuantity * applicableTier.unitPrice;
      return {
        totalPrice,
        unitPrice: applicableTier.unitPrice,
        discountPercent: applicableTier.discountPercent,
        discountAmount: totalPrice * (applicableTier.discountPercent / 100),
        tier: applicableTier.name,
      };
    } else {
      // Discount applies incrementally (only units in this tier)
      let totalPrice = 0;
      let remainingQuantity = totalQuantity;

      for (const tier of sortedTiers) {
        const tierQuantity = tier.maxQuantity
          ? Math.min(remainingQuantity, tier.maxQuantity - tier.minQuantity + 1)
          : remainingQuantity;

        totalPrice += tierQuantity * tier.unitPrice;
        remainingQuantity -= tierQuantity;

        if (remainingQuantity <= 0) break;
      }

      return {
        totalPrice,
        unitPrice: totalPrice / totalQuantity,
        discountPercent: 0,
        discountAmount: 0,
        tier: applicableTier.name,
      };
    }
  }
}
```

## Committed Usage Discounts

Customers commit to a minimum usage level in exchange for discounted rates.

```typescript
interface CommittedUsageDiscount {
  id: string;
  tenantId: string;
  contractId: string;
  productId: string;
  committedUnits: number;
  committedAmount: number;
  committedPeriod: 'monthly' | 'quarterly' | 'annual';
  discountRate: number;
  overageRate: number;
  trueUpSchedule: 'monthly' | 'quarterly' | 'annual';
  shortfallRate: number;         // Rate applied to un-used commitment
}

interface CommitmentTracking {
  period: { start: string; end: string };
  committed: number;
  actualUsage: number;
  variance: number;
  shortfallHours?: number;
  shortfallAmount?: number;
  overageUnits?: number;
  overageAmount?: number;
  trueUpAmount: number;
  status: 'met' | 'shortfall' | 'overage';
}

class CommitmentCalculator {
  async calculateTrueUp(
    commitment: CommittedUsageDiscount,
    actualUsage: number
  ): Promise<CommitmentTracking> {
    const committed = commitment.committedUnits;
    const variance = actualUsage - committed;

    let shortfallUnits = 0;
    let overageUnits = 0;
    let shortfallAmount = 0;
    let overageAmount = 0;

    if (variance < 0) {
      // Customer didn't meet commitment
      shortfallUnits = Math.abs(variance);
      shortfallAmount = shortfallUnits * commitment.shortfallRate;
    } else if (variance > 0) {
      // Customer exceeded commitment
      overageUnits = variance;
      overageAmount = overageUnits * commitment.overageRate;
    }

    const trueUpAmount = shortfallAmount + overageAmount;

    return {
      period: { start: '', end: '' },
      committed,
      actualUsage,
      variance,
      shortfallUnits,
      shortfallAmount,
      overageUnits,
      overageAmount,
      trueUpAmount,
      status: variance < 0 ? 'shortfall' : variance > 0 ? 'overage' : 'met',
    };
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Custom pricing data model with JSONB for flexible overrides
- **Redis** — Price resolution cache for low-latency lookups
- **BullMQ** — Price override audit log processing
- **Stripe** — Custom price objects and customer-specific pricing
- **Metabase** (Apache 2.0) — Custom pricing analysis dashboards
- **OpenTelemetry** — Pricing resolution tracing

## Integration Points

Custom pricing data model integrates with the subscription system (plan assignment), billing engine (invoice line items), contract management (price schedules), and analytics (revenue reporting).

## Production Considerations

- Cache resolved prices aggressively to avoid per-request database lookups
- Implement price override audit trail for compliance
- Validate overrides against minimum margin requirements
- Support price override approval workflows
- Handle concurrent price changes during billing runs
- Maintain price history for revenue recognition
- Support mid-period price changes with proration
- Test price resolution logic thoroughly with all override combinations

## Open-Source First Philosophy

PostgreSQL's JSONB columns store flexible custom price definitions without schema migrations. Redis provides sub-millisecond price resolution for subscription creation and invoice generation. BullMQ processes price override audit events asynchronously. Metabase provides the finance team with self-serve custom pricing reports. This stack replaces proprietary CPQ (Configure, Price, Quote) tools while maintaining complete control over pricing logic.
