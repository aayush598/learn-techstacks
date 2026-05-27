# Section 03: Trial-to-Paid Conversion

## Conversion Flow

The trial-to-paid conversion is the most critical revenue event in the customer lifecycle. The conversion flow must be seamless, frictionless, and strategically timed to maximize conversion rates.

```typescript
interface ConversionFlow {
  type: 'automatic' | 'manual' | 'sales_assisted';
  events: ConversionEvent[];
  timing: {
    preConversionReminders: number[];  // Days before expiry
    conversionWindow: number;           // Hours to complete payment
    gracePeriodDays: number;
  };
}

class TrialConversionService {
  async processAutomaticConversion(
    trialId: string
  ): Promise<ConversionResult> {
    const trial = await this.db.trials.findOne({ id: trialId });

    if (!trial.paymentMethodProvided) {
      return {
        converted: false,
        reason: 'No payment method on file',
        action: 'request_payment_method',
      };
    }

    try {
      // Stripe will automatically charge the default payment method
      // at the end of the trial period
      const subscription = await stripe.subscriptions.retrieve(
        trial.subscriptionId
      );

      if (subscription.status === 'active' && !subscription.trial_end) {
        // Trial converted successfully
        await this.completeConversion(trial);
        return {
          converted: true,
          subscriptionId: subscription.id,
          nextBillingDate: new Date(
            subscription.current_period_end * 1000
          ).toISOString(),
        };
      }

      if (subscription.status === 'past_due') {
        return {
          converted: false,
          reason: 'Payment failed',
          action: 'retry_payment',
          paymentIntentId: subscription.latest_invoice?.payment_intent as string,
        };
      }

      return {
        converted: false,
        reason: 'Unexpected subscription status',
        status: subscription.status,
        action: 'contact_support',
      };
    } catch (error) {
      logger.error('Automatic conversion failed', {
        trialId,
        error: error.message,
      });
      return {
        converted: false,
        reason: 'Conversion processing error',
        action: 'retry',
      };
    }
  }

  async completeConversion(trial: TrialSession): Promise<void> {
    // Update trial status
    await this.db.trials.updateOne(
      { id: trial.id },
      {
        $set: {
          status: 'converted',
          convertedAt: new Date().toISOString(),
        },
      }
    );

    // Remove trial feature restrictions (if any)
    await this.featureGateService.removeTrialRestrictions(trial.tenantId);

    // Trigger post-conversion actions
    await this.postConversionActions(trial);
  }

  private async postConversionActions(trial: TrialSession): Promise<void> {
    // Send welcome email
    await this.notificationService.sendConversionWelcome(
      trial.tenantId,
      trial.planId
    );

    // Update Salesforce/CRM
    await this.crmService.updateDealStage(trial.tenantId, 'closed_won');

    // Schedule onboarding call
    await this.bullQueue.add('scheduleOnboarding', {
      tenantId: trial.tenantId,
      planId: trial.planId,
    });

    // Track conversion event
    await this.analyticsService.track('trial.converted', {
      tenantId: trial.tenantId,
      planId: trial.planId,
      trialDuration: calculateDuration(trial.startedAt, trial.convertedAt),
    });
  }
}
```

## Payment Method Collection

Collecting payment method before the trial ends is critical for automatic conversion. The system proactively requests payment method during the trial period rather than waiting until the last day.

```typescript
class PaymentMethodCollectionService {
  async requestPaymentMethod(
    tenantId: string,
    trialId: string
  ): Promise<PaymentMethodRequest> {
    const customerId = await this.getStripeCustomerId(tenantId);

    // Create SetupIntent for secure payment method collection
    const setupIntent = await stripe.setupIntents.create({
      customer: customerId,
      usage: 'off_session',
      metadata: {
        tenant_id: tenantId,
        trial_id: trialId,
      },
    });

    return {
      clientSecret: setupIntent.client_secret,
      setupIntentId: setupIntent.id,
      expiresAt: new Date(
        setupIntent.created * 1000 + 3600000
      ).toISOString(),
    };
  }

  async handlePaymentMethodCollected(
    setupIntentId: string
  ): Promise<void> {
    const setupIntent = await stripe.setupIntents.retrieve(setupIntentId);

    if (setupIntent.status !== 'succeeded') {
      throw new Error('Payment method setup did not succeed');
    }

    const tenantId = setupIntent.metadata.tenant_id;
    const paymentMethodId = setupIntent.payment_method as string;

    // Set as default payment method
    await stripe.customers.update(
      setupIntent.customer as string,
      {
        invoice_settings: {
          default_payment_method: paymentMethodId,
        },
      }
    );

    // Update trial record
    await this.db.trials.updateOne(
      { id: setupIntent.metadata.trial_id },
      {
        $set: {
          paymentMethodProvided: true,
          paymentMethodId,
          paymentMethodProvidedAt: new Date().toISOString(),
        },
      }
    );

    // Send confirmation
    await this.notificationService.sendPaymentMethodConfirmation(tenantId);
  }
}
```

## Seamless Transition

The transition from trial to paid should be invisible to the customer. The service continues uninterrupted, feature access remains the same, and the first paid invoice arrives quietly.

```
Trial → Paid Transition Timeline:
┌────────────────────────────────────────────────────────────────┐
│ Day -14: Trial starts, full feature access granted              │
│ Day -7:  "7 days remaining" email with upgrade preview          │
│ Day -3:  "3 days remaining" email, payment method check         │
│ Day -1:  "Tomorrow: your trial ends" email                      │
│ Day 0:   Trial ends, auto-convert (if payment method on file)   │
│          – No service interruption                              │
│          – Feature access continues unchanged                   │
│          – First invoice generated and charged                  │
│ Day +1:  "Welcome to paid plan" email with receipt              │
└────────────────────────────────────────────────────────────────┘
```

## Feature Unlock on Conversion

Some features are locked during trial and unlock on conversion. These "conversion carrots" include advanced analytics, custom integrations, and higher rate limits.

```typescript
async function unlockConversionFeatures(
  tenantId: string,
  planId: string
): Promise<void> {
  const plan = await planCatalog.getPlan(planId);

  // Enable post-conversion features
  const conversionFeatures = plan.features.filter(f => f.conversionUnlock);

  for (const feature of conversionFeatures) {
    await this.featureGateService.enableFeature(tenantId, feature.key, {
      limit: feature.postConversionLimit,
    });
  }

  // Increase rate limits to paid tier
  await this.rateLimitService.applyTier(tenantId, planId);

  // Enable analytics with full data
  await this.analyticsService.enableFullAnalytics(tenantId);
}
```

## Open-Source Tools

- **Stripe API** — Automatic trial conversion and payment
- **BullMQ** (MIT) — Schedule trial expiry and conversion jobs
- **PostgreSQL** — Trial and conversion tracking
- **Redis** — Conversion status caching

## Integration Points

Trial conversion integrates with the subscription service (Stripe conversion), the feature gate service (post-conversion feature unlock), the notification service (conversion communications), and the analytics service (conversion tracking).

## Production Considerations

- Monitor automatic conversion success rate
- Track payment method collection rate during trial
- Set up alerts for conversion failures
- Test conversion flow with Stripe test clock
- Optimize conversion reminder timing through A/B testing

## Open-Source First Philosophy

Stripe handles the complex payment orchestration for trial conversion, including automatic charging at trial end. PostgreSQL tracks conversion analytics. BullMQ schedules reminder jobs. This open-source approach provides enterprise-grade trial conversion without proprietary subscription management platforms.
