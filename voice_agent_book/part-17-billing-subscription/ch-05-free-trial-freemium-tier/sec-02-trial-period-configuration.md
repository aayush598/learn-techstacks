# Section 02: Trial Period Configuration

## Configurable Trial Days

Trial periods are fully configurable through the plan catalog. Each plan can have a different trial duration, and the duration can be overridden for specific tenants or promotional campaigns.

```typescript
interface TrialPeriodConfig {
  planId: string;
  defaultDays: number;
  promotionalDays?: number;
  enterpriseDays: number;
  maxExtensions: number;
  extensionDaysPerRequest: number;
  autoConvert: boolean;  // Auto-convert to paid at end
  graceDaysAfterExpiry: number;
}

class TrialPeriodService {
  async getTrialDays(
    tenantId: string,
    planId: string,
    promoCode?: string
  ): Promise<number> {
    const config = await this.getConfig(planId);
    let days = config.defaultDays;

    // Check for promotional override
    if (promoCode) {
      const promo = await this.promotionService.getPromotion(promoCode);
      if (promo?.trialExtensionDays) {
        days = config.defaultDays + promo.trialExtensionDays;
      }
    }

    // Check for sales override
    const override = await this.db.trialOverrides.findOne({
      tenantId,
      active: true,
    });
    if (override?.trialDays) {
      days = override.trialDays;
    }

    return Math.min(days, config.maxDays);
  }

  async extendTrial(
    tenantId: string,
    additionalDays: number,
    reason: string,
    extendedBy: string
  ): Promise<void> {
    const trial = await this.db.trials.findOne({
      tenantId,
      status: 'active',
    });

    if (!trial) throw new Error('No active trial found');

    const config = await this.getConfig(trial.planId);
    const totalExtensions = await this.db.trialExtensions.countDocuments({
      trialId: trial.id,
    });

    if (totalExtensions >= config.maxExtensions) {
      throw new Error('Maximum trial extensions reached');
    }

    const newEndDate = new Date(
      Date.parse(trial.endsAt) + additionalDays * 86400000
    );

    // Update Stripe trial
    await stripe.subscriptions.update(trial.subscriptionId, {
      trial_end: Math.floor(newEndDate.getTime() / 1000),
    });

    // Update internal record
    await this.db.trials.updateOne(
      { id: trial.id },
      { $set: { endsAt: newEndDate.toISOString() } }
    );

    // Log extension
    await this.db.trialExtensions.create({
      id: `ext_${nanoid(16)}`,
      trialId: trial.id,
      tenantId,
      additionalDays,
      newEndDate: newEndDate.toISOString(),
      reason,
      extendedBy,
      createdAt: new Date().toISOString(),
    });
  }

  async pauseTrial(
    tenantId: string,
    pauseDays: number
  ): Promise<void> {
    const trial = await this.db.trials.findOne({
      tenantId,
      status: 'active',
    });

    if (!trial) throw new Error('No active trial');
    if (trial.paused) throw new Error('Trial is already paused');

    const remainingDays = Math.ceil(
      (Date.parse(trial.endsAt) - Date.now()) / 86400000
    );

    const newEndDate = new Date(
      Date.now() + (remainingDays + pauseDays) * 86400000
    );

    await this.db.trials.updateOne(
      { id: trial.id },
      {
        $set: {
          paused: true,
          pausedAt: new Date().toISOString(),
          endsAt: newEndDate.toISOString(),
          pauseDurationDays: pauseDays,
        },
      }
    );

    // Restore access if was restricted
    await this.featureGateService.applyPlan(tenantId, trial.planId);
  }
}
```

## Per-Plan Trial Settings

Each plan defines its own trial settings: duration, feature access level, payment method requirements, and conversion behavior.

```yaml
# Plan catalog trial configuration
starter:
  trial:
    days: 14
    payment_method_required: true
    feature_access: full
    usage_limits:
      minutes: 500  # Lower than paid to encourage conversion
      agents: 1
    auto_convert: true
    grace_period_days: 3

growth:
  trial:
    days: 14
    payment_method_required: true
    feature_access: full
    usage_limits:
      minutes: 5000
      agents: 5
    auto_convert: true
    grace_period_days: 3

enterprise:
  trial:
    days: 30
    payment_method_required: false
    feature_access: full
    usage_limits: ~  # No limits during enterprise trial
    auto_convert: false
    grace_period_days: 7
```

## Extended Trial for Enterprise

Enterprise trials are managed by the sales team and can be significantly longer. They don't require payment method and often include onboarding assistance.

```typescript
async function createEnterpriseTrial(
  tenantId: string,
  planId: string,
  trialDays: number,
  salesRepId: string,
  notes?: string
): Promise<TrialSession> {
  // Enterprise trials bypass normal eligibility
  const subscription = await stripe.subscriptions.create({
    customer: await getStripeCustomerId(tenantId),
    items: [{ price: await getPlanStripePrice(planId) }],
    trial_period_days: trialDays,
    metadata: {
      tenant_id: tenantId,
      trial: 'enterprise',
      sales_rep: salesRepId,
      trial_notes: notes || '',
    },
    billing_cycle_anchor: 'unchanged',
  });

  return {
    id: `trial_${nanoid(16)}`,
    tenantId,
    planId,
    subscriptionId: subscription.id,
    startedAt: new Date().toISOString(),
    endsAt: new Date(Date.now() + trialDays * 86400000).toISOString(),
    status: 'active',
    isEnterprise: true,
    salesRepId,
  };
}
```

## Trial Pause

Trial pause allows users to temporarily stop their trial clock without losing progress. This is useful when users need more time to evaluate or when they hit implementation delays.

```typescript
async function pauseTrial(tenantId: string): Promise<void> {
  const trial = await getActiveTrial(tenantId);
  const remainingMs = Date.parse(trial.endsAt) - Date.now();

  // Pause the subscription in Stripe (set trial end to far future)
  await stripe.subscriptions.update(trial.subscriptionId, {
    trial_end: 'now',  // End trial, start paid? No — pause differently
    pause_collection: {
      behavior: 'void',
      resumes_at: Math.floor((Date.now() + 30 * 86400000) / 1000),
    },
  });

  trial.paused = true;
  trial.pausedAt = new Date().toISOString();
  trial.remainingMs = remainingMs;

  await saveTrial(trial);
}
```

## Open-Source Tools

- **Stripe API** — Trial period management on subscriptions
- **BullMQ** (MIT) — Schedule trial expiry and reminder jobs
- **Redis** (BSD-3) — Cache trial status for fast access
- **PostgreSQL** — Trial period configuration and session storage

## Integration Points

Trial period configuration integrates with the subscription service (Stripe trial management), the feature gate service (trial access), the notification service (trial expiry reminders), and the sales CRM (enterprise trial tracking).

## Production Considerations

- Test trial period boundaries extensively (leap years, time zones)
- Handle trial expiry gracefully with data retention periods
- Monitor trial length impact on conversion rates
- A/B test different trial durations for optimal conversion
- Provide clear trial status indicators in the UI

## Open-Source First Philosophy

Stripe's subscription trial management handles the complex timing and billing logic. PostgreSQL stores trial configurations that are managed through code (YAML in git). BullMQ schedules all trial lifecycle events reliably. This open-source stack provides flexible trial management without proprietary subscription management software.
