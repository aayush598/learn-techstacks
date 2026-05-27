# Section 07: Plan Catalog Management

## Plan CRUD Operations

The plan catalog requires Create, Read, Update, and Delete operations with strict governance. Unlike typical CRUD, plan changes have downstream effects on active subscriptions, Stripe synchronization, feature gating, and invoicing. Every mutation must go through a controlled workflow.

```typescript
class PlanCatalogService {
  private db: Database;
  private stripeSync: StripeSyncService;
  private featureGate: FeatureGateService;

  async createPlan(config: PlanConfiguration): Promise<Plan> {
    // 1. Validate configuration
    const validation = await this.validatePlanConfig(config);
    if (!validation.valid) throw new Error(validation.errors.join(', '));

    // 2. Create Stripe product and prices
    const stripeProduct = await this.stripeSync.createProduct({
      name: config.name,
      metadata: { internal_plan_id: config.id, version: '1' },
    });

    this.stripeSync.createPrices(stripeProduct.id, config.pricing);

    // 3. Store internal configuration
    const plan = await this.db.plans.create({
      ...config,
      stripeProductId: stripeProduct.id,
      version: 1,
      status: 'draft',
      createdAt: new Date(),
    });

    // 4. Deploy feature gates
    await this.featureGate.deployPlanGates(config);

    // 5. Set as draft until published
    return plan;
  }

  async publishPlan(planId: string): Promise<Plan> {
    const plan = await this.db.plans.update(planId, {
      status: 'active',
      publishedAt: new Date(),
    });

    await this.stripeSync.setPricesActive(plan.stripeProductId);
    await this.featureGate.enablePlanGates(planId);

    return plan;
  }

  async deprecatePlan(
    planId: string,
    replacementPlanId: string,
    migrationStrategy: MigrationStrategy
  ): Promise<void> {
    // Mark as deprecated
    await this.db.plans.update(planId, { status: 'deprecated' });

    // Hide from pricing page
    await this.setPlanVisibility(planId, 'hidden');

    // Execute migration for active subscribers
    const activeSubscribers = await this.db.subscriptions.findByPlan(planId);
    for (const sub of activeSubscribers) {
      await this.migrationService.queueMigration(sub.id, replacementPlanId, migrationStrategy);
    }

    // Archive Stripe prices (stop new signups)
    await this.stripeSync.archivePrices(planId);
  }
}
```

## Staging vs Production Catalog

The plan catalog exists in two environments: staging (for development and testing) and production (for live customers). Changes flow through an environment promotion workflow:

```
Development → Staging → Pre-Production → Production
   │             │            │               │
   └─YAML        └─Stripe     └─Canary        └─Full rollout
   Config         Test Mode    Deploy          Activation
```

Staging uses Stripe test mode with test clock capabilities. All plan changes are tested against synthetic tenants before promotion to production. The promotion workflow is automated via CI/CD pipelines.

## Localization of Plans

SaaS products with global customer bases need localized pricing. Localization includes currency conversion, region-specific pricing, tax-inclusive vs tax-exclusive display, and local payment methods.

```typescript
interface LocalizedPlanConfig {
  locale: string;           // 'en-US', 'de-DE', 'ja-JP'
  currency: string;         // 'USD', 'EUR', 'JPY'
  displayPrice: number;     // Localized price
  taxInclusive: boolean;
  paymentMethods: PaymentMethod[];
  features: LocalizedFeature[];
  metadata: {
    displayName: string;
    tagline: string;
    description: string;
  };
}

interface PaymentMethod {
  type: 'card' | 'sepa_debit' | 'ach_credit_transfer' | 'bancontact' | 'ideal' | 'fpx';
  currency: string;
  enabled: boolean;
}
```

Localized pricing is not just currency conversion — it reflects local willingness-to-pay, competitive landscape, and purchasing power parity. For example, India pricing might be $19/month vs $49/month in the US for the Starter plan.

## Currency Support

Multi-currency support requires Stripe's multi-currency capabilities. Each plan has price IDs for each supported currency. Customers are billed in their local currency based on their billing address or preference.

```typescript
async function getPlanPrice(
  planId: string,
  currency: string,
  tenantRegion: string
): Promise<CurrencyPrice> {
  const plan = await planCatalog.getPlan(planId);

  // Check for regional override
  if (plan.regionalPricing?.[tenantRegion]) {
    return plan.regionalPricing[tenantRegion];
  }

  // Check for currency-specific price
  if (plan.currencyPrices?.[currency]) {
    return plan.currencyPrices[currency];
  }

  // Fall back to default (USD) with conversion hint
  return {
    currency: currency,
    amount: plan.basePrice * await exchangeRateService.getRate('USD', currency),
    source: 'converted',
  };
}
```

## Open-Source Tools

- **pgAdmin** (PostgreSQL GUI) — Plan catalog management during development
- **BullMQ** — Schedule catalog promotions and migrations
- **Stripe CLI** — Test mode catalog synchronization
- **Unleash** — Staging vs production feature gate environments

For local development, the plan catalog is managed via YAML files in a git repository. This provides version control, code review, and CI/CD integration without a proprietary CMS.

## Integration Points

The plan catalog feeds the Stripe product synchronization (Chapter 3 Section 3), the pricing page API (Part 2), the feature gating middleware (Part 8), and the billing engine (Chapter 3). All services reference the catalog by plan ID rather than hardcoding plan details.

## Production Considerations

- Never delete plans — deprecate them
- Maintain a changelog for every plan modification
- Plan catalog changes require multi-environment approval
- Monitor Stripe sync failures with alerts
- Test localized pricing in each target market
- Review currency exchange rates weekly

## Open-Source First Philosophy

The plan catalog is managed entirely through YAML configuration files stored in git, with PostgreSQL providing the runtime storage. There is no dependency on proprietary pricing management software. The Stripe product catalog sync is a straightforward mapping from internal YAML to Stripe API objects, keeping the system simple and auditable.
