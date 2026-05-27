# Section 01: Trial Eligibility Design

## Credit Card Required vs Not

The decision to require a credit card for trial access is one of the most impactful conversion decisions. A card-required trial filters out low-intent users but creates friction that reduces signup volume. A card-not-required trial maximizes signups but risks abuse and lower conversion rates.

Our approach uses a graduated system: the Free plan requires no credit card and provides limited access; the trial of paid plans requires a credit card for verification but doesn't charge until conversion. This balances conversion optimization with abuse prevention.

```typescript
interface TrialEligibilityConfig {
  requirePaymentMethod: boolean;
  authorizationAmount?: number;  // $1 hold for card verification
  authorizationHoldDays: number; // How long to hold the authorization
  refundOnCancel: boolean;
}

const TRIAL_CONFIGS = {
  free_plan: {
    requirePaymentMethod: false,
    authorizationHoldDays: 0,
    refundOnCancel: false,
  },
  starter_trial: {
    requirePaymentMethod: true,
    authorizationAmount: 100,    // $1.00 hold
    authorizationHoldDays: 7,
    refundOnCancel: true,
  },
  growth_trial: {
    requirePaymentMethod: true,
    authorizationAmount: 100,
    authorizationHoldDays: 7,
    refundOnCancel: true,
  },
  enterprise_trial: {
    requirePaymentMethod: false,  // Sales-led, no card needed
    authorizationHoldDays: 0,
    refundOnCancel: true,
  },
};

class TrialEligibilityService {
  async checkEligibility(
    tenantId: string,
    planId: string
  ): Promise<TrialEligibilityResult> {
    const tenant = await this.tenantService.getTenant(tenantId);
    const config = TRIAL_CONFIGS[planId];

    // Check if already used trial
    const previousTrials = await this.db.trials.countDocuments({
      tenantId,
      status: { $in: ['converted', 'expired', 'cancelled'] },
    });

    if (previousTrials > 0) {
      return {
        eligible: false,
        reason: 'Trial already used',
        alternativeAction: 'Subscribe directly',
      };
    }

    // Check for abuse signals
    const abuseCheck = await this.abuseDetectionService.check(tenant);
    if (abuseCheck.isSuspicious) {
      return {
        eligible: false,
        reason: 'Suspicious signup detected',
        alternativeAction: 'Contact support',
      };
    }

    return {
      eligible: true,
      config,
      requirements: config.requirePaymentMethod
        ? ['payment_method']
        : [],
    };
  }

  async startTrial(
    tenantId: string,
    planId: string,
    paymentMethodId?: string
  ): Promise<TrialSession> {
    const eligibility = await this.checkEligibility(tenantId, planId);
    if (!eligibility.eligible) {
      throw new Error(`Trial not eligible: ${eligibility.reason}`);
    }

    const config = TRIAL_CONFIGS[planId];
    const trialDays = await this.getTrialDays(tenantId, planId);

    if (config.requirePaymentMethod && paymentMethodId) {
      // Create SetupIntent for card authorization
      const setupIntent = await stripe.setupIntents.create({
        customer: await this.getStripeCustomerId(tenantId),
        payment_method: paymentMethodId,
        usage: 'off_session',
      });

      // Hold $1 authorization
      if (config.authorizationAmount) {
        await stripe.paymentIntents.create({
          amount: config.authorizationAmount,
          currency: 'usd',
          customer: await this.getStripeCustomerId(tenantId),
          payment_method: paymentMethodId,
          capture_method: 'manual', // Authorize only, don't capture
          confirm: true,
          description: 'Trial card verification',
        });
      }
    }

    // Create trial subscription in Stripe
    const subscription = await stripe.subscriptions.create({
      customer: await this.getStripeCustomerId(tenantId),
      items: [{ price: await this.getPlanStripePrice(planId) }],
      trial_period_days: trialDays,
      metadata: {
        tenant_id: tenantId,
        trial: 'true',
        trial_start: new Date().toISOString(),
      },
      ...(paymentMethodId ? { default_payment_method: paymentMethodId } : {}),
    });

    const trial: TrialSession = {
      id: `trial_${nanoid(16)}`,
      tenantId,
      planId,
      subscriptionId: subscription.id,
      startedAt: new Date().toISOString(),
      endsAt: new Date(Date.now() + trialDays * 86400000).toISOString(),
      status: 'active',
      paymentMethodRequired: config.requirePaymentMethod,
      paymentMethodProvided: !!paymentMethodId,
    };

    await this.db.trials.create(trial);
    return trial;
  }
}
```

## Trial Length Configuration

Trial length varies by plan and segment. Self-serve trials are 14 days. Sales-led enterprise trials can be 30-90 days. The trial length is configurable per plan and can be extended by sales admins.

```typescript
interface TrialLengthConfig {
  planId: string;
  defaultDays: number;
  minDays: number;
  maxDays: number;
  extendableBySales: boolean;
  maxExtensionDays: number;
}

const trialLengths: TrialLengthConfig[] = [
  { planId: 'starter', defaultDays: 14, minDays: 7, maxDays: 30, extendableBySales: true, maxExtensionDays: 60 },
  { planId: 'growth', defaultDays: 14, minDays: 7, maxDays: 30, extendableBySales: true, maxExtensionDays: 60 },
  { planId: 'pro', defaultDays: 14, minDays: 7, maxDays: 30, extendableBySales: true, maxExtensionDays: 90 },
  { planId: 'enterprise', defaultDays: 30, minDays: 14, maxDays: 90, extendableBySales: true, maxExtensionDays: 180 },
];
```

## Feature Access During Trial

Trial users get full access to the plan they're trialing, not a restricted preview. This allows users to evaluate the complete product experience and increases conversion likelihood. The only limitation is time.

```typescript
async function applyTrialFeatureAccess(tenantId: string, planId: string): Promise<void> {
  const plan = await planCatalog.getPlan(planId);

  // Grant full plan features for the trial period
  await featureGateService.applyPlan(tenantId, planId, {
    duration: 'trial',
    watermarkingEnabled: false,    // No watermarks during trial
    analyticsDelay: false,         // Real-time analytics during trial
    supportLevel: plan.supportLevel, // Full support during trial
  });
}
```

## Eligibility Rules

Eligibility rules determine who can start a trial. Rules include domain restrictions, existing subscription check, and geographic availability.

```typescript
interface TrialEligibilityRule {
  type: 'domain' | 'email' | 'ip' | 'region' | 'existing_customer';
  action: 'allow' | 'block' | 'flag';
  value: string | string[];
  priority: number;
}

const eligibilityRules: TrialEligibilityRule[] = [
  { type: 'domain', action: 'block', value: ['tempmail.com', 'mailinator.com'], priority: 100 },
  { type: 'region', action: 'allow', value: ['US', 'CA', 'UK', 'EU', 'AU'], priority: 50 },
  { type: 'existing_customer', action: 'block', value: 'true', priority: 10 },
];
```

## Open-Source Tools

- **Stripe API** — Trial subscription management
- **Redis** — Trial session caching
- **BullMQ** — Schedule trial expiry jobs
- **PostgreSQL** — Trial eligibility rules and session storage

## Integration Points

Trial eligibility connects to the authentication service (signup flow), the subscription service (Stripe trial creation), the abuse detection service (Section 6), and the notification service (trial communications).

## Production Considerations

- A/B test card-required vs card-not-required trials
- Monitor trial-to-paid conversion rates by segment
- Track average time-to-conversion for optimization
- Set up alerts for unusually high trial signup rates
- Review abuse detection rules regularly

## Open-Source First Philosophy

Stripe's trial management capabilities eliminate the need for a custom trial system. PostgreSQL stores eligibility rules that are managed through the application rather than a proprietary rules engine. BullMQ schedules trial lifecycle events. This open-source approach provides enterprise trial management without proprietary subscription software.
