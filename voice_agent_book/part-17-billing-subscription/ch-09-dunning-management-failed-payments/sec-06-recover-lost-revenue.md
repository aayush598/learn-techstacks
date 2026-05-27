# Section 06: Recover Lost Revenue

## Win-Back Email Sequences

After a subscription is cancelled due to payment failure, automated win-back sequences attempt to re-engage the customer.

```
[Cancellation Due to Payment]
    ↓
[Day 1: Soft Win-Back]
    ├── "We miss you" email
    ├── Reactivation link
    └── No discount (standard offer)
    ↓
[Day 7: Incentive Offer]
    ├── "Come back with 1 month free"
    ├── Discount code generated
    └── Limited time (14 days)
    ↓
[Day 30: Final Offer]
    ├── "Last chance: 50% off first 3 months"
    ├── High-value incentive
    └── Limited time (7 days)
    ↓
[Day 60: Sunset]
    ├── Data retention notice
    ├── Export reminder
    └── Customer moved to dormant
```

```typescript
interface WinBackSequence {
  id: string;
  customerId: string;
  tenantId: string;
  originalPlanId: string;
  cancelledAt: string;
  stages: WinBackStage[];
  currentStage: number;
  status: 'active' | 'converted' | 'expired' | 'suppressed';
  incentives: Incentive[];
  createdAt: string;
  updatedAt: string;
}

interface WinBackStage {
  day: number;
  channel: 'email' | 'sms' | 'push';
  template: string;
  incentive?: IncentiveOffer;
  delayAfterPreviousDays: number;
  maxSends: number;
}

interface IncentiveOffer {
  type: 'discount_percentage' | 'free_months' | 'waive_fees' | 'upgrade_trial';
  value: number;
  durationMonths: number;
  code: string;
  expiresAt: string;
  maxRedemptions: number;
  currentRedemptions: number;
}

class WinBackService {
  private readonly sequences: Map<string, WinBackStage[]>;

  constructor() {
    this.sequences = new Map([
      ['default', [
        { day: 1, channel: 'email', template: 'winback_day1', delayAfterPreviousDays: 1, maxSends: 2 },
        { day: 7, channel: 'email', template: 'winback_day7', incentive: { type: 'free_months', value: 1, durationMonths: 1, code: '', expiresAt: '', maxRedemptions: 1, currentRedemptions: 0 }, delayAfterPreviousDays: 6, maxSends: 1 },
        { day: 30, channel: 'email', template: 'winback_day30', incentive: { type: 'discount_percentage', value: 50, durationMonths: 3, code: '', expiresAt: '', maxRedemptions: 1, currentRedemptions: 0 }, delayAfterPreviousDays: 23, maxSends: 1 },
        { day: 60, channel: 'email', template: 'winback_day60_final', delayAfterPreviousDays: 30, maxSends: 1 },
      ]],
      ['enterprise', [
        { day: 1, channel: 'email', template: 'winback_ent_day1', delayAfterPreviousDays: 1, maxSends: 2 },
        { day: 14, channel: 'email', template: 'winback_ent_day14', incentive: { type: 'free_months', value: 2, durationMonths: 2, code: '', expiresAt: '', maxRedemptions: 1, currentRedemptions: 0 }, delayAfterPreviousDays: 13, maxSends: 2 },
        { day: 45, channel: 'email', template: 'winback_ent_day45', incentive: { type: 'discount_percentage', value: 30, durationMonths: 6, code: '', expiresAt: '', maxRedemptions: 1, currentRedemptions: 0 }, delayAfterPreviousDays: 31, maxSends: 1 },
      ]],
    ]);
  }

  async startWinBackSequence(
    customerId: string,
    subscription: Subscription
  ): Promise<WinBackSequence> {
    const sequence: WinBackSequence = {
      id: generateId('winback'),
      customerId,
      tenantId: subscription.tenantId,
      originalPlanId: subscription.planId,
      cancelledAt: new Date().toISOString(),
      stages: this.getSequenceForPlan(subscription.planId),
      currentStage: 0,
      status: 'active',
      incentives: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    await this.storeSequence(sequence);

    // Schedule first stage
    await this.scheduleStage(sequence, 0);

    return sequence;
  }

  async processReactivation(
    code: string,
    customerId: string
  ): Promise<ReactivationResult> {
    const incentive = await this.validateIncentiveCode(code, customerId);
    if (!incentive) {
      return { success: false, reason: 'invalid_or_expired_code' };
    }

    // Apply incentive to new subscription
    const subscription = await this.createReactivationSubscription(
      customerId,
      incentive
    );

    // Mark win-back as converted
    await this.markConverted(customerId);

    return {
      success: true,
      subscriptionId: subscription.id,
      appliedIncentive: incentive,
    };
  }

  private async scheduleStage(sequence: WinBackSequence, stageIndex: number): Promise<void> {
    const stage = sequence.stages[stageIndex];
    if (!stage) return;

    const delayMs = stage.day * 24 * 60 * 60 * 1000;

    await this.winbackQueue.add(
      'send-winback',
      {
        sequenceId: sequence.id,
        stageIndex,
        customerId: sequence.customerId,
        template: stage.template,
      },
      { delay: delayMs }
    );
  }
}
```

## Discount Offers

Targeted discount offers based on customer history and plan tier.

```typescript
interface DiscountRule {
  id: string;
  name: string;
  type: 'percentage' | 'fixed_amount' | 'free_period';
  value: number;
  durationMonths: number;
  eligibilityCriteria: EligibilityCriteria;
  maxRedemptions: number;
  budget: number;                // Total budget for this offer
  currentSpend: number;
}

interface EligibilityCriteria {
  minTenureDays: number;
  previousPlanTiers: string[];
  maxPreviousDiscounts: number;
  riskScoreMax: number;
  segments: string[];
}

class DiscountOfferEngine {
  private rules: DiscountRule[];

  async getEligibleOffers(customer: Customer): Promise<DiscountOffer[]> {
    const eligible: DiscountOffer[] = [];

    for (const rule of this.rules) {
      if (await this.isEligible(customer, rule)) {
        eligible.push({
          ruleId: rule.id,
          name: rule.name,
          description: rule.description,
          type: rule.type,
          value: rule.value,
          durationMonths: rule.durationMonths,
          code: await this.generateCode(),
          expiresAt: this.addDays(new Date(), 14).toISOString(),
        });
      }
    }

    return eligible;
  }

  private async isEligible(customer: Customer, rule: DiscountRule): Promise<boolean> {
    const criteria = rule.eligibilityCriteria;

    // Check tenure
    const tenureDays = daysBetween(customer.createdAt, new Date());
    if (tenureDays < criteria.minTenureDays) return false;

    // Check previous plan
    if (!criteria.previousPlanTiers.includes(customer.previousPlan)) return false;

    // Check previous discounts
    const discountsUsed = await this.getDiscountCount(customer.id);
    if (discountsUsed >= criteria.maxPreviousDiscounts) return false;

    // Check budget
    if (rule.currentSpend >= rule.budget) return false;

    return true;
  }

  async applyDiscount(
    customerId: string,
    offerCode: string
  ): Promise<DiscountApplication> {
    const offer = await this.validateOffer(offerCode, customerId);
    if (!offer) {
      return { success: false, reason: 'offer_not_valid' };
    }

    // Create discount on Stripe
    const coupon = await stripe.coupons.create({
      [offer.type === 'percentage' ? 'percent_off' : 'amount_off']: offer.value,
      duration: 'repeating',
      duration_in_months: offer.durationMonths,
      metadata: {
        customer_id: customerId,
        offer_code: offerCode,
        source: 'winback',
      },
    });

    // Apply to customer
    await stripe.customers.update(customerId, {
      coupon: coupon.id,
    });

    return {
      success: true,
      couponId: coupon.id,
      offer: offer,
    };
  }
}
```

## Re-Activation Flow

The re-activation flow allows customers to restore their subscription with all previous data.

```typescript
interface ReactivationFlow {
  subscriptionId: string;
  customerId: string;
  status: 'pending' | 'reactivating' | 'completed' | 'failed';
  dataRestore: {
    restoreConfigurations: boolean;
    restoreHistory: boolean;
    restoreAnalytics: boolean;
  };
  originalSubscription: {
    planId: string;
    startDate: string;
    endDate: string;
    featureFlags: Record<string, boolean>;
  };
}

class ReactivationService {
  async initiateReactivation(
    customerId: string,
    originalSubscriptionId: string
  ): Promise<ReactivationFlow> {
    // Get original subscription details
    const original = await this.getArchivedSubscription(originalSubscriptionId);
    if (!original) {
      throw new Error('Original subscription not found');
    }

    // Create new subscription
    const newSubscription = await this.createSubscription({
      customerId,
      planId: original.planId,
      metadata: {
        reactivation: 'true',
        originalSubscriptionId,
        reactivatedAt: new Date().toISOString(),
      },
    });

    // Schedule data restoration
    const flow: ReactivationFlow = {
      subscriptionId: newSubscription.id,
      customerId,
      status: 'reactivating',
      dataRestore: {
        restoreConfigurations: true,
        restoreHistory: true,
        restoreAnalytics: true,
      },
      originalSubscription: {
        planId: original.planId,
        startDate: original.startDate,
        endDate: original.endDate,
        featureFlags: original.featureFlags,
      },
    };

    // Restore data asynchronously
    await this.reactivationQueue.add('restore-data', {
      customerId,
      originalSubscriptionId,
      newSubscriptionId: newSubscription.id,
    });

    return flow;
  }

  async restoreData(
    customerId: string,
    originalId: string,
    newId: string
  ): Promise<void> {
    // Restore configurations
    const configs = await this.getArchivedConfigs(customerId, originalId);
    for (const config of configs) {
      await this.restoreConfig(customerId, newId, config);
    }

    // Restore history
    const history = await this.getArchivedHistory(customerId, originalId);
    await this.restoreHistory(customerId, newId, history);

    // Restore analytics data
    const analytics = await this.getArchivedAnalytics(customerId, originalId);
    await this.restoreAnalytics(customerId, newId, analytics);
  }
}
```

## Payment Retry Campaigns

Targeted retry campaigns for specific customer segments.

```typescript
interface RetryCampaign {
  id: string;
  name: string;
  targetSegment: RetrySegment;
  schedule: RetrySchedule;
  maxAttempts: number;
  incentives?: RetryIncentive[];
  active: boolean;
}

interface RetrySegment {
  failureReasonPattern: string[];
  minAccountAge: number;
  previousPaymentHistory: 'good' | 'mixed' | 'poor';
  planTiers: string[];
}

class PaymentRetryCampaign {
  async executeCampaign(campaign: RetryCampaign): Promise<CampaignResult> {
    const eligibleCustomers = await this.findEligibleCustomers(campaign.targetSegment);

    let successes = 0;
    let failures = 0;

    for (const customer of eligibleCustomers) {
      try {
        // Apply any incentives first
        if (campaign.incentives?.length) {
          await this.applyIncentive(customer, campaign.incentives[0]);
        }

        // Attempt payment
        const result = await this.retryPayment(customer.id);
        if (result.success) {
          successes++;
        } else {
          failures++;
        }
      } catch (error) {
        failures++;
      }
    }

    return {
      campaignId: campaign.id,
      totalEligible: eligibleCustomers.length,
      successes,
      failures,
      revenueRecovered: successes * this.getAverageRevenue(),
    };
  }
}
```

## Open-Source Tools

- **BullMQ** — Win-back sequence scheduling and retry campaigns
- **PostgreSQL** — Win-back state and incentive tracking
- **Redis** — Incentive code validation cache
- **Handlebars** (MIT) — Win-back email templates
- **Metabase** (Apache 2.0) — Revenue recovery dashboards
- **Stripe** — Discount coupon and subscription management

## Integration Points

Revenue recovery integrates with the subscription system (re-activation), payment gateway (retry campaigns), notification service (win-back sequences), CRM (customer segmentation), and analytics (recovery metrics).

## Production Considerations

- A/B test win-back offers to optimize conversion rates
- Track incentive ROI (revenue recovered vs discount cost)
- Suppress win-back sequences for known fraudulent accounts
- Honor unsubscribe preferences for win-back communications
- Limit discount frequency to prevent gaming
- Provide data export before final sunset
- Monitor reactivation quality (do reactivated customers stay?)
- Automatically suppress sequences after reactivation

## Open-Source First Philosophy

BullMQ orchestrates the entire win-back sequence lifecycle with scheduled email campaigns. PostgreSQL tracks incentive usage and prevents abuse. Metabase provides dashboards for revenue recovery analysis. Handlebars renders targeted win-back email templates. This open-source stack replaces proprietary retention platforms like Recoverly or ChurnZero while providing complete control over recovery strategies and customer data.
