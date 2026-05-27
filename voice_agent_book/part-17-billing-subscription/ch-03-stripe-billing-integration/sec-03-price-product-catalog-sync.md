# Section 03: Price & Product Catalog Sync

## Internal Plan → Stripe Product Sync

The internal plan catalog must stay synchronized with Stripe's product and price objects. When a plan is created or updated in our system, corresponding Stripe objects must be created or updated. This sync is critical for subscription creation and invoice generation.

```typescript
interface StripeProductMapping {
  internalPlanId: string;
  internalVersion: number;
  stripeProductId: string;
  stripePrices: {
    month: string;   // Price ID for monthly
    year: string;    // Price ID for annual
    metered?: string; // Price ID for metered component
  };
  lastSyncedAt: string;
  syncStatus: 'synced' | 'pending' | 'failed';
}

class CatalogSyncService {
  async syncPlanToStripe(plan: PlanConfiguration): Promise<StripeProductMapping> {
    // Create or update product
    let product: Stripe.Product;
    const existingMapping = await this.db.stripeProductMappings.findOne({
      internalPlanId: plan.id,
    });

    if (existingMapping) {
      product = await stripe.products.update(existingMapping.stripeProductId, {
        name: plan.name,
        description: plan.metadata.description,
        metadata: {
          internal_plan_id: plan.id,
          plan_version: plan.version.toString(),
          plan_segment: plan.segment,
          plan_rank: plan.rank.toString(),
        },
        active: plan.status === 'active',
      });

      // Update prices if needed
      if (plan.pricing.billingPeriods.monthly) {
        await this.syncPrice(
          existingMapping.stripePrices.month,
          plan.pricing.billingPeriods.monthly,
          product.id
        );
      }
    } else {
      product = await stripe.products.create({
        name: plan.name,
        description: plan.metadata.description,
        metadata: {
          internal_plan_id: plan.id,
          plan_version: plan.version.toString(),
          plan_segment: plan.segment,
          plan_rank: plan.rank.toString(),
        },
      });

      // Create prices
      const monthlyPrice = await this.createPrice(
        product.id,
        plan.pricing.billingPeriods.monthly,
        'month'
      );

      const annualPrice = plan.pricing.billingPeriods.annual
        ? await this.createPrice(
            product.id,
            plan.pricing.billingPeriods.annual,
            'year'
          )
        : null;

      const mapping: StripeProductMapping = {
        internalPlanId: plan.id,
        internalVersion: plan.version,
        stripeProductId: product.id,
        stripePrices: {
          month: monthlyPrice.id,
          year: annualPrice?.id,
        },
        lastSyncedAt: new Date().toISOString(),
        syncStatus: 'synced',
      };

      await this.db.stripeProductMappings.create(mapping);
      return mapping;
    }
  }

  private async createPrice(
    productId: string,
    config: BillingPeriodConfig,
    interval: 'month' | 'year'
  ): Promise<Stripe.Price> {
    const priceData: Stripe.PriceCreateParams = {
      product: productId,
      currency: config.currency || 'usd',
      recurring: {
        interval,
        usage_type: config.type === 'metered' ? 'metered' : 'licensed',
      },
      metadata: {
        billing_model: config.type,
      },
    };

    if (config.type === 'flat' || config.type === 'hybrid') {
      priceData.billing_scheme = 'per_unit';
      priceData.unit_amount = config.basePrice;
    } else if (config.type === 'tiered') {
      priceData.billing_scheme = 'tiered';
      priceData.tiers_mode = 'graduated';
      priceData.tiers = config.tiers.map(t => ({
        up_to: t.to === 'inf' ? undefined : t.to,
        unit_amount: t.unitPrice,
        flat_amount: t.flatFee,
      }));
    }

    return await stripe.prices.create(priceData);
  }
}
```

## Price ID Mapping

A mapping table connects internal plans and prices to their Stripe equivalents. This is used by the subscription service when creating subscriptions and by the invoice service when generating invoices.

```typescript
interface PriceMapping {
  internalPlanId: string;
  internalPriceKey: string;   // e.g., 'starter_monthly', 'growth_annual'
  stripePriceId: string;
  currency: string;
  interval: 'month' | 'year';
  active: boolean;
  validFrom: string;
  validTo?: string;
}
```

## Tiered Pricing

Stripe supports tiered pricing natively. Tiers can be graduated (different rate per tier bracket) or volume-based (all units at a blended rate). Our usage-based pricing uses graduated tiers.

```typescript
async function createTieredPrice(
  productId: string,
  tiers: TierConfig[],
  interval: 'month' | 'year'
): Promise<Stripe.Price> {
  const stripeTiers = tiers.map(t => ({
    up_to: t.to === 'inf' ? undefined : t.to,
    unit_amount: t.unitPrice,
    flat_amount: t.flatFee,
  }));

  return await stripe.prices.create({
    product: productId,
    currency: 'usd',
    billing_scheme: 'tiered',
    tiers_mode: 'graduated',
    tiers: stripeTiers,
    recurring: { interval, usage_type: 'metered' },
  });
}
```

## Metered Prices

Metered prices in Stripe are created with `usage_type: 'metered'`. They accept usage records during the billing period and aggregate them at invoice time. Metered prices cannot have a flat fee component — the flat fee is charged via a separate licensed price.

```typescript
interface MeteredPriceConfig {
  productId: string;
  unitAmount: number;
  currency: string;
  interval: 'month' | 'year';
  aggregateUsage: 'sum' | 'last_during_period' | 'last_ever' | 'max';
}

async function createMeteredPrice(config: MeteredPriceConfig): Promise<Stripe.Price> {
  return await stripe.prices.create({
    product: config.productId,
    currency: config.currency,
    unit_amount: config.unitAmount,
    recurring: {
      interval: config.interval,
      usage_type: 'metered',
      aggregate_usage: config.aggregateUsage,
    },
  });
}
```

## Open-Source Tools

- **Stripe API** — Product and price CRUD
- **BullMQ** — Background catalog sync jobs
- **PostgreSQL** — Mapping tables for internal → Stripe references
- **YAML** — Plan catalog source of truth (git-based)

## Integration Points

Catalog sync integrates with the plan catalog service (Section 6), the subscription service (Section 2), the invoice service (Chapter 4), and the Stripe webhook handler (Section 4).

## Production Considerations

- Validate Stripe price consistency with internal plans
- Handle Stripe API rate limits during batch sync
- Test price sync in Stripe test mode before production
- Monitor sync failures and retry with exponential backoff
- Version price mappings and archive old ones

## Open-Source First Philosophy

The plan catalog starts as YAML in a git repository, gets validated and promoted through CI/CD, and syncs to Stripe via API. This eliminates the need for a proprietary pricing management system. All sync state is tracked in PostgreSQL, and BullMQ handles background sync jobs. The entire catalog management pipeline is built on open-source and free-tier tools.
