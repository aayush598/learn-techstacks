# Section 04: Plan Versioning & Migration

## Version History Management

Plans evolve over time as the product matures, costs change, and competitive dynamics shift. A plan versioning strategy ensures that changes are tracked, communicated, and applied appropriately to new vs existing customers.

Each plan version includes a snapshot of the feature matrix, pricing, and limits. Versions are immutable once published — changes create a new version rather than mutating the existing one. This provides a complete history of what each customer was sold.

```typescript
interface PlanVersion {
  id: string;
  planId: string;
  version: number;
  effectiveDate: string;
  status: 'draft' | 'active' | 'archived';
  features: FeatureDefinition[];
  pricing: PricingDefinition;
  changelog: string;
  migrationStrategy?: MigrationStrategy;
  createdBy: string;
}

interface MigrationStrategy {
  type: 'grandfather' | 'migrate_all' | 'opt_in' | 'opt_out';
  gracePeriodDays?: number;
  newPrice?: number;
  oldPrice?: number;
  notificationTemplate?: string;
}

interface PriceChange {
  changeId: string;
  planId: string;
  versionFrom: number;
  versionTo: number;
  affectedTenants: number;
  changePercentage: number;
  notificationSent?: string;
}
```

## Grandfathering Existing Customers

When pricing changes, existing customers should be grandfathered on their current pricing for a period or indefinitely. Grandfathering preserves trust and prevents churn from price increases. The key trade-off is between revenue maximization (forcing upgrades) and customer retention (preserving pricing).

```
Grandfathering Strategies:
┌─────────────────────────────────────────────────────────────────┐
│ Strategy        │ Revenue Impact  │ Churn Risk    │ Complexity  │
├─────────────────┼─────────────────┼───────────────┼─────────────┤
│ Indefinite      │ Low (upfront)   │ Minimal       │ High        │
│ Fixed Period    │ Medium          │ Low           │ Medium      │
│ 12-month freeze │ Good            │ Low           │ Medium      │
│ Force Migration │ High            │ High          │ Low         │
│ Opt-in to new   │ Low             │ Low           │ Low         │
│ Opt-out from new│ Medium          │ Medium        │ High        │
└─────────────────────────────────────────────────────────────────┘
```

Indefinite grandfathering is the most customer-friendly but creates technical debt: you must maintain support for old pricing tiers indefinitely. A 12-month price freeze followed by a planned migration balances retention with revenue goals.

## Migration Paths

Plan migrations (upgrade or downgrade) happen at billing period boundaries. Upgrades take effect immediately with proration. Downgrades apply at the next period end. The migration logic calculates prorated credits, adjusts feature access, and updates the Stripe subscription.

```typescript
async function migratePlan(
  tenantId: string,
  subscriptionId: string,
  newPlanId: string,
  options: { immediate: boolean; prorate: boolean }
): Promise<MigrationResult> {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const currentPlan = await planCatalog.getCurrentPlan(subscription.metadata.plan_id);
  const targetPlan = await planCatalog.getPlan(newPlanId);

  if (options.immediate && currentPlan.price > targetPlan.price) {
    throw new Error('Immediate downgrade not supported');
  }

  const proration = await calculateProration(subscription, currentPlan, targetPlan);
  const migration = {
    fromPlan: currentPlan.id,
    toPlan: targetPlan.id,
    effectiveDate: options.immediate ? new Date() : subscription.current_period_end,
    credit: proration.credit,
    charge: proration.charge,
  };

  await subscription.update({
    items: [{ id: subscription.items.data[0].id, price: targetPlan.stripePriceId }],
    proration_behavior: options.prorate ? 'always_invoice' : 'none',
    billing_cycle_anchor: options.immediate ? 'now' : 'unchanged',
  });

  await featureGateService.applyPlanChange(tenantId, currentPlan, targetPlan);
  await notificationService.sendPlanChangeConfirmation(tenantId, migration);

  return migration;
}

function calculateProration(
  subscription: Stripe.Subscription,
  currentPlan: PlanDefinition,
  targetPlan: PlanDefinition
): { credit: number; charge: number } {
  const daysRemaining = daysBetween(new Date(), subscription.current_period_end);
  const daysTotal = daysBetween(subscription.current_period_start, subscription.current_period_end);
  const dailyRate = currentPlan.price / daysTotal;

  const credit = dailyRate * daysRemaining * (currentPlan.price > targetPlan.price ? 1 : 0);
  const charge = dailyRate * daysRemaining * (targetPlan.price > currentPlan.price ? 1 : 0);

  return { credit, charge: Math.abs(charge) };
}
```

## Price Increase Handling

Price increases require careful communication and execution. The standard approach is a 30-60 day notice period, clear communication of the value added, and a grandfathering option for existing customers. Legally, terms of service should allow price changes with notice.

```
Price Increase Timeline:
┌─────────────────────────────────────────────────────────────────┐
│ Day -60: Announce price increase via email and in-app banner      │
│ Day -45: Send reminder with value comparison                     │
│ Day -30: Final notice with effective date                        │
│ Day  0:  New pricing takes effect for renewals                   │
│ Day +7:  Follow-up survey for customers who downgraded           │
└─────────────────────────────────────────────────────────────────┘
```

## Stripe Subscription Versioning

Stripe doesn't natively support plan versioning. The approach is to create new price IDs for each version and map them to internal plan versions. When a plan version changes, new customers get the new price ID while existing customers keep their old price ID until migration.

```typescript
interface PlanVersionMapping {
  internalPlanId: string;
  version: number;
  stripeProductId: string;
  stripeMonthlyPriceId: string;
  stripeAnnualPriceId: string;
  stripeUsagePriceId?: string; // For metered components
}
```

## Open-Source Tools

- **PostgreSQL JSONB columns** store plan version snapshots
- **Liquibase** (Apache 2.0) — Database migration tool for plan catalog changes
- **BullMQ** — Schedule migration notifications and processing
- **Stripe API** — Idempotent subscription updates for mass migrations

## Integration Points

Plan versioning integrates with the subscription service (Chapter 3) for Stripe updates, the notification service (Part 10) for migration communications, and the feature gate service (Chapter 1 Section 2) for applying plan changes at runtime.

## Production Considerations

- Always test migrations on a subset of tenants first (canary)
- Monitor migration failure rates and roll back if > 1%
- Maintain a migration audit log for compliance
- Handle partial failures gracefully (some customers migrate, others don't)
- Allow customers to choose their migration timing

## Open-Source First Philosophy

Plan version history is stored entirely in PostgreSQL using schema-less JSONB columns, eliminating the need for a specialized version management system. Migration campaigns are orchestrated via BullMQ job queues rather than expensive marketing automation platforms. The entire migration workflow is auditable through database logs rather than proprietary audit tools.
