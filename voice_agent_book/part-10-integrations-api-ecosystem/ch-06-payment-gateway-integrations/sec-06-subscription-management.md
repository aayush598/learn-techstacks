# Section 06: Subscription Management

## Overview

Subscription management handles recurring billing for voice agent customers enrolled in ongoing plans. The subscription engine integrates with each payment gateway's recurring billing APIs (Stripe Subscriptions, Braintree Recurring Billing, Square Subscriptions, Adyen Recurring) and provides a unified subscription lifecycle: plan creation, customer enrollment, recurring charge execution, billing failure handling, upgrade/downgrade proration, and cancellation processing.

The subscription system works hand-in-hand with the voice agent platform to enable use cases like monthly SaaS billing, weekly meal plan deliveries, or annual membership renewals — all managed through voice interactions. Customers can subscribe, upgrade, downgrade, or cancel using natural language, and the subscription engine translates these intents into gateway-specific subscription API calls. The engine also handles the financial complexities of prorated charges, trial periods, coupons, and tax calculations.

## Architecture

```
                   Subscription Management Engine

   Voice Agent ←→ Subscriptions Engine ←→ Payment Adapter ←→ Gateway
                      |
   +----------------------------------------------------------+
   |               Subscription Lifecycle State               |
   |                                                          |
   |  +--------+    +----------+    +----------+             |
   |  | Create |--->| Active   |--->| Cancel   |             |
   |  | Trial  |    | (billing)|    | (end     |             |
   |  |        |    |          |    |  period) |             |
   |  +--------+    +----------+    +----------+             |
   |       |             |                                      |
   |       v             v                                      |
   |  +--------+    +----------+    +----------+             |
   |  | Expired |    | Past Due |    | Paused   |             |
   |  | (trial  |    | (retry)  |    | (hold)   |             |
   |  |  ended) |    |          |    |          |             |
   |  +--------+    +----------+    +----------+             |
   |                                                          |
   |  Billing Operations:                                     |
   |  • Invoice generation (immediate + recurring)            |
   |  • Proration calculation (upgrade/downgrade)             |
   |  • Dunning management (retry + escalation)               |
   |  • Tax calculation (integration with TaxJar/Stripe Tax)  |
   +----------------------------------------------------------+
```

## Design Decisions

- **Immediate invoice finalization over open invoices:** When a subscription renews, the invoice is immediately finalized and payment attempted. If payment fails, the invoice remains open and the dunning cycle begins. This ensures clean accounting — no invoices are left in draft state beyond the billing period. Trade-off: immediate finalization prevents manual adjustments before charging but ensures billing accuracy and reduces abandoned receivables.

- **Proration via credit memo vs. immediate refund for downgrades:** When a customer downgrades mid-cycle, a credit memo is issued for the unused portion and applied to the next invoice. For upgrades, the prorated difference is charged immediately. This approach avoids refund processing fees and keeps money movement simple. Trade-off: credits are less satisfying for customers expecting immediate refunds but reduce transaction costs and reconciliation complexity.

- **Dunning as a configurable workflow over hard-coded retry:** The dunning process (handling failed payments) is configurable per subscription plan: number of retry attempts, interval between retries, escalation actions (send email, notify agent, suspend service). Default is 3 retries at days 3, 7, and 14 after failure, with service suspension on day 21 and final cancellation on day 30. Trade-off: configurable dunning adds complexity but accommodates different collection strategies for different customer segments.

## Implementation Approach

```
interface SubscriptionPlan {
  id: string;
  name: string;
  amount: number;
  currency: string;
  interval: 'day' | 'week' | 'month' | 'year';
  intervalCount: number;
  trialDays: number;
  metadata: Record<string, string>;
}

interface Subscription {
  id: string;
  customerId: string;
  planId: string;
  status: 'active' | 'past_due' | 'canceled' | 'paused' | 'trialing' | 'expired';
  currentPeriodStart: Date;
  currentPeriodEnd: Date;
  trialEnd?: Date;
  canceledAt?: Date;
  metadata: Record<string, string>;
}

class SubscriptionEngine {
  private adapters: Map<string, BasePaymentAdapter>;
  private dunningConfig: DunningConfig;

  async createSubscription(
    adapterType: string,
    params: {
      customerId: string;
      planId: string;
      paymentMethodId: string;
      trialDays?: number;
      metadata?: Record<string, string>;
    }
  ): Promise<AdapterResponse<Subscription>> {
    const adapter = this.adapters.get(adapterType)!;
    const result = await adapter.createSubscription(params);
    if (result.success) {
      await this.emitEvent('subscription.created', {
        subscriptionId: result.data.id,
        customerId: params.customerId,
        planId: params.planId,
      });
    }
    return result;
  }

  async changePlan(
    adapterType: string,
    subscriptionId: string,
    newPlanId: string
  ): Promise<AdapterResponse<{ subscription: Subscription; proratedAmount: number; invoice?: Invoice }>> {
    const adapter = this.adapters.get(adapterType)!;
    const currentSub = await adapter.getSubscription(subscriptionId);
    const currentPlan = await this.getPlan(currentSub.data.planId);
    const newPlan = await this.getPlan(newPlanId);

    const proration = this.calculateProration(currentPlan!, newPlan!, currentSub.data);

    const result = await adapter.updateSubscription(subscriptionId, {
      planId: newPlanId,
      prorationBehavior: proration.amount >= 0 ? 'create_prorations' : 'create_prorations',
    });

    if (proration.amount > 0) {
      const invoice = await adapter.createInvoice({
        customerId: currentSub.data.customerId,
        amount: proration.amount,
        description: `Prorated upgrade: ${currentPlan!.name} to ${newPlan!.name}`,
        subscriptionId,
      });
      return { success: true, data: { ...result.data, proratedAmount: proration.amount, invoice } };
    }

    if (proration.amount < 0) {
      await this.createCreditMemo(currentSub.data.customerId, Math.abs(proration.amount));
    }

    return { success: true, data: { subscription: result.data, proratedAmount: proration.amount } };
  }

  private calculateProration(
    currentPlan: SubscriptionPlan,
    newPlan: SubscriptionPlan,
    subscription: Subscription
  ): { amount: number } {
    const now = new Date();
    const periodEnd = subscription.currentPeriodEnd;
    const daysRemaining = differenceInDays(periodEnd, now);
    const daysTotal = differenceInDays(periodEnd, subscription.currentPeriodStart);

    if (daysTotal <= 0) return { amount: 0 };

    const dailyRateCurrent = currentPlan.amount / daysTotal;
    const dailyRateNew = newPlan.amount / daysTotal;
    const unusedAmount = dailyRateCurrent * daysRemaining;
    const proratedNewAmount = dailyRateNew * daysRemaining;

    return { amount: Math.round(proratedNewAmount - unusedAmount) };
  }

  async handleBillingFailure(event: BillingFailureEvent): Promise<void> {
    const subscription = await this.getSubscription(event.subscriptionId);
    const attempts = event.attemptNumber;

    await this.notifyCustomer(subscription.customerId, `Payment failed (attempt ${attempts})`);

    if (attempts >= this.dunningConfig.maxAttempts) {
      await this.suspendSubscription(event.subscriptionId);
      await this.notifyCustomer(subscription.customerId, 'Service suspended due to payment failure');
      this.scheduleCancellation(event.subscriptionId, this.dunningConfig.gracePeriodDays);
    } else {
      const nextRetry = addDays(new Date(), this.dunningConfig.retryIntervalDays);
      this.scheduleRetry(event.subscriptionId, nextRetry);
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Later (MIT) | Node.js | Scheduled dunning tasks |
| Date-fns (MIT) | Dates | Proration calculations |
| TaxJar SDK (MIT) | Taxes | Sales tax calculation |

## Production Considerations

**Scaling:** Subscription billing is a batch operation — at midnight (or configured time), the system evaluates all subscriptions due for renewal. This creates a burst of API calls. Use a queue-based approach: enqueue individual renewal jobs, process through worker pools with configurable concurrency (default 20). Implement idempotency to safely retry failed renewals. Cache plan and customer data to reduce database lookups during the billing run.

**Security:** Subscription management involves financial operations — audit all state changes with actor identity (system vs. admin vs. customer). Never allow proration or cancellation of subscriptions without proper authorization checks. Implement a "tombstone" for cancelled subscriptions (retain metadata but prevent reactivation after 90 days). Ensure PCI scope is limited to the payment adapter layer.

**Monitoring:** Track MRR (Monthly Recurring Revenue), ARR, churn rate (voluntary and involuntary), failed payment rate, dunning recovery rate, average subscription lifetime, and upgrade/downgrade ratio. Alert on churn spikes, failed payment rates exceeding 10%, and dunning recovery below 50%. Monitor proration accuracy against expected revenue. Set up daily MRR change reports.
