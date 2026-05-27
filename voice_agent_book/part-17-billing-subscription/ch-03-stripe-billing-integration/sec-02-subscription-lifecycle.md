# Section 02: Subscription Lifecycle

## Create/Update/Cancel Subscription

The subscription lifecycle encompasses creation, updates (upgrade/downgrade), cancellation, and reactivation. Each phase has specific behaviors for billing, feature access, and customer communication.

```typescript
class SubscriptionService {
  async createSubscription(
    tenantId: string,
    planId: string,
    paymentMethodId: string,
    options?: {
      trialDays?: number;
      coupon?: string;
      metadata?: Record<string, string>;
    }
  ): Promise<Subscription> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);
    const plan = await this.planCatalog.getPlan(planId);

    const subscription = await stripe.subscriptions.create({
      customer: stripeCustomerId,
      items: [{
        price: plan.stripeMonthlyPriceId,
      }],
      default_payment_method: paymentMethodId,
      trial_period_days: options?.trialDays,
      coupon: options?.coupon,
      metadata: {
        tenant_id: tenantId,
        plan_id: planId,
        ...options?.metadata,
      },
      payment_behavior: 'default_incomplete',
      expand: ['latest_invoice.payment_intent'],
    });

    // Store internal subscription reference
    await this.db.subscriptions.create({
      id: subscription.id,
      tenantId,
      planId,
      status: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000).toISOString(),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000).toISOString(),
      trialStart: subscription.trial_start
        ? new Date(subscription.trial_start * 1000).toISOString()
        : null,
      trialEnd: subscription.trial_end
        ? new Date(subscription.trial_end * 1000).toISOString()
        : null,
      metadata: options?.metadata,
    });

    // Apply feature gates
    await this.featureGateService.applyPlan(tenantId, planId);

    return subscription;
  }

  async cancelSubscription(
    subscriptionId: string,
    options: { atPeriodEnd: boolean; reason?: string }
  ): Promise<void> {
    // Schedule cancellation
    const subscription = await stripe.subscriptions.update(subscriptionId, {
      cancel_at_period_end: options.atPeriodEnd,
      metadata: {
        cancellation_reason: options.reason,
        cancelled_at: new Date().toISOString(),
      },
    });

    if (!options.atPeriodEnd) {
      // Immediate cancellation — process refund
      await this.handleImmediateCancellation(subscription, options.reason);
    }

    // Update internal status
    await this.db.subscriptions.updateOne(
      { id: subscriptionId },
      {
        $set: {
          cancelAtPeriodEnd: options.atPeriodEnd,
          cancellationReason: options.reason,
          status: options.atPeriodEnd ? 'active' : 'canceled',
        },
      }
    );
  }
}
```

## Plan Change Proration

When a customer changes plans mid-cycle, Stripe calculates the prorated credit or charge. The proration logic considers the unused portion of the current plan and the remaining portion of the new plan.

```typescript
async function changePlan(
  subscriptionId: string,
  newPlanId: string,
  options: {
    prorate: boolean;
    effectiveDate?: 'now' | 'period_end';
    billingCycleAnchor?: 'now' | 'unchanged';
  }
): Promise<ChangePlanResult> {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const newPlan = await planCatalog.getPlan(newPlanId);

  const updateParams: Stripe.SubscriptionUpdateParams = {
    items: [{
      id: subscription.items.data[0].id,
      price: newPlan.stripeMonthlyPriceId,
    }],
    proration_behavior: options.prorate ? 'always_invoice' : 'none',
    billing_cycle_anchor: options.effectiveDate === 'now' ? 'now' : 'unchanged',
    metadata: {
      plan_change_from: subscription.metadata.plan_id,
      plan_change_to: newPlanId,
      plan_change_date: new Date().toISOString(),
    },
  };

  if (options.prorate) {
    // Preview proration
    const preview = await stripe.invoices.retrieveUpcoming({
      subscription: subscriptionId,
      subscription_items: [{
        id: subscription.items.data[0].id,
        price: newPlan.stripeMonthlyPriceId,
      }],
    });

    const prorationItems = preview.lines.data.filter(
      line => line.proration
    );

    const totalProration = prorationItems.reduce(
      (sum, item) => sum + item.amount,
      0
    );

    logger.info('Plan change proration', {
      subscriptionId,
      fromPlan: subscription.metadata.plan_id,
      toPlan: newPlanId,
      prorationAmount: totalProration,
    });
  }

  const updated = await stripe.subscriptions.update(subscriptionId, updateParams);

  // Apply feature gates for new plan
  await featureGateService.applyPlan(subscription.metadata.tenant_id, newPlanId);

  return {
    subscription: updated,
    prorationAmount: options.prorate ? await calculateProration(subscription, newPlan) : 0,
    effectiveDate: options.effectiveDate === 'now' ? new Date() : new Date(subscription.current_period_end * 1000),
  };
}
```

## Trial Handling

Trials in Stripe are configured at subscription creation with `trial_period_days`. During the trial, the customer has full feature access but no payment is collected. Trial handling includes:

- Trial start/end tracking
- Feature access during trial (full or restricted)
- Payment method collection during trial (optional)
- Automatic conversion at trial end

```
┌──────────────────────────────────────────────────────────────────┐
│ Subscription Status State Machine:                                │
│                                                                    │
│  ┌───────┐    start     ┌──────────┐                             │
│  │ None  │─────────────→│ Incomplete│                             │
│  └───────┘              └────┬─────┘                             │
│                              │                                    │
│                    ┌─────────┴─────────┐                          │
│                    ▼                   ▼                           │
│              ┌──────────┐      ┌──────────┐                       │
│              │  Trial   │      │  Active  │                       │
│              └────┬─────┘      └────┬─────┘                       │
│                   │                 │                             │
│         expires   │         payment │ fails                       │
│                   ▼                 ▼                             │
│              ┌──────────┐      ┌──────────┐                       │
│              │  Active  │─────→│ Past Due │                       │
│              └────┬─────┘      └────┬─────┘                       │
│                   │                 │                             │
│           cancel  │         overdue │                             │
│                   ▼                 ▼                             │
│              ┌──────────┐      ┌──────────┐                       │
│              │ Canceled │      │  Unpaid  │                       │
│              └──────────┘      └────┬─────┘                       │
│                                      │                            │
│                              expired │                            │
│                                      ▼                            │
│                               ┌──────────┐                        │
│                               │ Canceled │                        │
│                               └──────────┘                        │
└──────────────────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **Stripe API** — Subscription CRUD operations
- **BullMQ** — Schedule subscription lifecycle jobs (trial expiry, renewal)
- **PostgreSQL** — Internal subscription state tracking
- **Redis** — Subscription status caching for fast access control

## Integration Points

Subscription lifecycle integrates with the feature gate service (Part 8), the usage metering pipeline (Chapter 2), the invoice generation system (Chapter 4), the trial system (Chapter 5), and the dunning system (Chapter 9).

## Production Considerations

- Handle Stripe webhook events for subscription status changes
- Test subscription lifecycle scenarios thoroughly (upgrade, downgrade, cancel, reactivate)
- Monitor subscription status transitions for anomalies
- Implement grace period for failed payments before cancellation
- Log all subscription changes for audit trail

## Open-Source First Philosophy

Stripe's subscription management API eliminates the need to build a custom subscription engine. PostgreSQL provides the internal subscription state store, BullMQ schedules lifecycle jobs, and Redis caches subscription status for fast access checks. This all-open-source (plus Stripe) stack provides enterprise subscription management at a fraction of the cost of building from scratch.
