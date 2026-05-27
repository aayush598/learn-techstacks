# Section 05: Billing Period Alignment

## Monthly/Annual Billing Cycles

Usage tracking must align with billing periods. Monthly subscriptions track usage from the subscription start date (or billing anniversary) to the same date next month. Annual subscriptions track usage over a 365-day period.

The billing period anchor is the subscription start date. For example, a subscription starting June 15 has periods of June 15-July 14, July 15-August 14, etc. This differs from calendar month billing, which would be June 1-June 30.

```typescript
interface BillingPeriod {
  subscriptionId: string;
  periodStart: string;     // ISO 8601
  periodEnd: string;       // ISO 8601
  status: 'open' | 'processing' | 'closed';
  usageTotals: Record<string, number>;
}

function getCurrentPeriod(subscription: Subscription): BillingPeriod {
  const now = new Date();
  const anchor = new Date(subscription.currentPeriodStart);
  const interval = subscription.billingInterval; // 'month' | 'year'

  // Calculate period start based on anchor
  const periodStart = new Date(anchor);
  while (periodStart <= now) {
    if (interval === 'month') {
      periodStart.setMonth(periodStart.getMonth() + 1);
    } else {
      periodStart.setFullYear(periodStart.getFullYear() + 1);
    }
  }
  periodStart.setMonth(periodStart.getMonth() - 1);

  // Calculate period end
  const periodEnd = new Date(periodStart);
  if (interval === 'month') {
    periodEnd.setMonth(periodEnd.getMonth() + 1);
  } else {
    periodEnd.setFullYear(periodEnd.getFullYear() + 1);
  }

  return {
    subscriptionId: subscription.id,
    periodStart: periodStart.toISOString(),
    periodEnd: periodEnd.toISOString(),
    status: 'open',
    usageTotals: {},
  };
}
```

## Usage Reset at Period Boundaries

Metered usage is reset at each billing period boundary. The reset is not a deletion of data (we keep full history for audit) but a logical reset for quota tracking. Redis counter keys include the period identifier so they naturally reset when the period changes.

```typescript
class PeriodManager {
  async closePeriod(subscriptionId: string): Promise<void> {
    const sub = await this.stripe.subscriptions.retrieve(subscriptionId);
    const periodEnd = new Date(sub.current_period_end * 1000);
    const periodKey = this.formatPeriodKey(periodEnd);

    // 1. Finalize usage totals
    const usage = await this.getPeriodUsage(subscriptionId, periodKey);

    // 2. Generate invoice (if not already generated)
    if (!await this.invoiceService.hasInvoiceForPeriod(subscriptionId, periodKey)) {
      await this.invoiceService.generateInvoice(subscriptionId, periodKey, usage);
    }

    // 3. Submit metered usage to Stripe
    for (const [meter, total] of Object.entries(usage)) {
      await this.stripe.subscriptionItems.createUsageRecord(
        sub.items.data.find(i => i.metadata.meter === meter).id,
        {
          quantity: Math.round(total),
          timestamp: Math.floor(periodEnd.getTime() / 1000),
          action: 'set', // Overwrite any previously submitted usage
        }
      );
    }

    // 4. Mark period as closed
    await this.db.billingPeriods.updateOne(
      { subscriptionId, periodKey },
      { $set: { status: 'closed', closedAt: new Date() } }
    );

    // 5. Trigger post-period tasks
    await this.queue.add('postBillingTasks', {
      subscriptionId,
      periodKey,
      usage,
    });
  }

  private formatPeriodKey(date: Date): string {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
  }
}
```

## Proration for Mid-Cycle Changes

When a customer changes plans mid-cycle, their usage allowances and charges must be prorated. The proration algorithm calculates the proportion of the billing period remaining and applies it to both plan charges and usage allowances.

```typescript
interface ProrationResult {
  daysInPeriod: number;
  daysRemaining: number;
  oldPlan: {
    charge: number;          // Credit for unused days
    usageAllowance: number;  // Prorated allowance
  };
  newPlan: {
    charge: number;          // Charge for remaining days
    usageAllowance: number;  // Prorated allowance
  };
  netAmount: number;         // Positive = charge, Negative = credit
}

function calculateProration(
  subscription: Subscription,
  oldPlan: PlanDefinition,
  newPlan: PlanDefinition,
  changeDate: Date
): ProrationResult {
  const periodStart = new Date(subscription.currentPeriodStart);
  const periodEnd = new Date(subscription.currentPeriodEnd);
  const daysInPeriod = daysBetween(periodStart, periodEnd);
  const daysRemaining = daysBetween(changeDate, periodEnd);
  const daysUsed = daysInPeriod - daysRemaining;

  const oldDailyRate = oldPlan.price / daysInPeriod;
  const newDailyRate = newPlan.price / daysInPeriod;

  // Credit for unused old plan days
  const oldCredit = oldDailyRate * daysRemaining;

  // Charge for remaining days on new plan
  const newCharge = newDailyRate * daysRemaining;

  // Prorated usage allowances
  const oldAllowance = oldPlan.includedMinutes * (daysUsed / daysInPeriod);
  const newAllowance = newPlan.includedMinutes * (daysRemaining / daysInPeriod);
  const totalAllowance = oldAllowance + newAllowance;

  return {
    daysInPeriod,
    daysRemaining,
    oldPlan: {
      charge: oldPlan.price,
      usageAllowance: oldAllowance,
    },
    newPlan: {
      charge: newPlan.price,
      usageAllowance: newAllowance,
    },
    netAmount: newCharge - oldCredit,
  };
}
```

```
Mid-Cycle Upgrade Example:
┌────────────────────────────────────────────────────────────────┐
│  June 1 (Period Start)                                          │
│  ├────────────────────────────────────────────────────────────┤  │
│  │  Starter: $49      │         Upgrade to Growth             │  │
│  │  1,000 min incl.   │   June 15 (Change)                    │  │
│  │                     │         ├───────────────────────────┤  │
│  │                     │         │ Growth: Prorated $99.50   │  │
│  │                     │         │ 5,000 min (prorated)      │  │
│  │  Credit: $24.50     │         │                           │  │
│  │  (15 days unused)   │         │                           │  │
│  └─────────────────────┴─────────┴───────────────────────────┘  │
│                           July 1 (Period End)                    │
│  Net charge: $99.50 - $24.50 = $75.00                            │
│  Total allowance: 500 (used) + 5,000 = 5,500 min                 │
└────────────────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **BullMQ** (MIT) — Schedule period-end billing jobs
- **Redis** (BSD-3) — Period-scoped counter keys with TTL
- **Stripe API** — Subscription management with proration
- **node-cron** (ISC) — Period boundary cron jobs

## Integration Points

Period alignment integrates with the subscription service (Chapter 3), the usage aggregation system (Section 3), the invoice generation service (Chapter 4), and the Stripe metered billing API.

## Production Considerations

- Handle period boundary race conditions (events arriving during period switchover)
- Implement a grace period for late-arriving events (72h window)
- Monitor proration calculation accuracy
- Test period boundary scenarios extensively (leap years, time zones)
- Log all period closure events for audit
- Send period-end usage summaries to customers

## Open-Source First Philosophy

Period management relies on BullMQ for job scheduling, Redis for period-scoped counters, and PostgreSQL for period metadata. The Stripe API handles subscription proration natively, eliminating the need for custom proration logic. This open-source stack replaces proprietary billing engines while providing equivalent functionality.
