# Section 05: Grace Period Handling

## Service Continuation During Grace

During the grace period, customers continue to receive service while efforts to recover payment proceed in the background.

```
[Payment Failure]
    ↓
[Enter Grace Period]
    ├── Service level set (full / read-only)
    ├── Timer starts (7-30 days)
    ├── Feature restrictions (if any) applied
    └── Data retention timer starts
    ↓
[During Grace Period]
    ├── Background retries continue
    ├── Customer notified of grace status
    ├── In-app banner showing grace status
    └── Support team can extend grace
    ↓
[Grace Period Expires]
    ├── If payment recovered → Full service restored
    └── If payment not recovered → Suspend or downgrade
```

```typescript
interface GracePeriodConfig {
  maxDurationDays: number;
  serviceLevel: 'full' | 'read_only';
  featureRestrictions: string[];
  communicationCadence: GraceCommunication[];
  retryDuringGrace: boolean;
  extendableBySupport: boolean;
  maxExtensionDays: number;
}

interface GraceCommunication {
  day: number;                   // Day of grace period
  channel: 'email' | 'sms' | 'in_app' | 'push';
  template: string;
  urgency: 'low' | 'medium' | 'high';
}

class GracePeriodService {
  private configs: Map<string, GracePeriodConfig>;

  constructor() {
    this.configs = new Map([
      ['default', {
        maxDurationDays: 7,
        serviceLevel: 'read_only',
        featureRestrictions: ['api_write', 'new_deployments'],
        communicationCadence: [
          { day: 1, channel: 'email', template: 'grace_started', urgency: 'medium' },
          { day: 3, channel: 'email', template: 'grace_reminder', urgency: 'medium' },
          { day: 5, channel: 'email', template: 'grace_expiring', urgency: 'high' },
          { day: 7, channel: 'sms', template: 'grace_final', urgency: 'high' },
        ],
        retryDuringGrace: true,
        extendableBySupport: true,
        maxExtensionDays: 14,
      }],
      ['enterprise', {
        maxDurationDays: 30,
        serviceLevel: 'full',
        featureRestrictions: [],
        communicationCadence: [
          { day: 7, channel: 'email', template: 'grace_enterprise_reminder', urgency: 'low' },
          { day: 21, channel: 'email', template: 'grace_enterprise_expiring', urgency: 'medium' },
        ],
        retryDuringGrace: true,
        extendableBySupport: true,
        maxExtensionDays: 60,
      }],
    ]);
  }

  async startGracePeriod(
    subscription: Subscription,
    configOverride?: Partial<GracePeriodConfig>
  ): Promise<GracePeriod> {
    const config = this.getConfig(subscription.planId);
    const mergedConfig = { ...config, ...configOverride };

    const gracePeriod: GracePeriod = {
      id: generateId('grace'),
      subscriptionId: subscription.id,
      customerId: subscription.customerId,
      tenantId: subscription.tenantId,
      startDate: new Date().toISOString(),
      endDate: this.calculateEndDate(mergedConfig.maxDurationDays),
      serviceLevel: mergedConfig.serviceLevel,
      status: 'active',
      featureRestrictions: mergedConfig.featureRestrictions,
      communicationsSent: [],
      createdAt: new Date().toISOString(),
    };

    // Apply service level restrictions
    await this.applyServiceLevel(subscription.id, mergedConfig.serviceLevel);

    // Apply feature restrictions
    for (const featureId of mergedConfig.featureRestrictions) {
      await this.featureFlagService.disable(subscription.id, featureId);
    }

    // Store grace period
    await this.storeGracePeriod(gracePeriod);

    // Schedule grace expiry
    await this.scheduleGraceExpiry(gracePeriod);

    // Schedule communications
    for (const comm of mergedConfig.communicationCadence) {
      await this.scheduleGraceCommunication(gracePeriod, comm);
    }

    return gracePeriod;
  }

  async extendGracePeriod(
    gracePeriodId: string,
    additionalDays: number,
    reason: string
  ): Promise<GracePeriod> {
    const grace = await this.getGracePeriod(gracePeriodId);
    if (!grace) throw new Error('Grace period not found');

    const config = this.getConfigForGrace(grace);
    if (!grace.extendableBySupport) throw new Error('Grace period not extendable');

    const maxExtension = config.maxExtensionDays;
    const totalExtension = this.getTotalExtension(grace);
    if (totalExtension + additionalDays > maxExtension) {
      throw new Error(`Maximum extension of ${maxExtension} days exceeded`);
    }

    grace.endDate = this.addDays(grace.endDate, additionalDays);
    grace.extensionHistory.push({
      additionalDays,
      reason,
      extendedBy: 'support_agent',
      extendedAt: new Date().toISOString(),
    });

    await this.updateGracePeriod(grace);
    await this.rescheduleGraceExpiry(grace);

    return grace;
  }

  async resolveGracePeriod(
    gracePeriodId: string,
    resolution: GraceResolution
  ): Promise<void> {
    const grace = await this.getGracePeriod(gracePeriodId);
    if (!grace) return;

    grace.status = 'resolved';
    grace.resolvedAt = new Date().toISOString();
    grace.resolution = resolution;

    await this.updateGracePeriod(grace);

    // Restore full service
    await this.restoreServiceLevel(grace.subscriptionId);
    await this.restoreFeatures(grace.subscriptionId, grace.featureRestrictions);

    // Cancel scheduled communications
    await this.cancelScheduledCommunications(grace.id);
  }

  private calculateEndDate(maxDays: number): string {
    const end = new Date();
    end.setDate(end.getDate() + maxDays);
    return end.toISOString();
  }
}
```

## Grace Period Duration

Duration varies by plan, customer history, and payment failure reason.

```typescript
interface GraceDurationCalculator {
  baseDays: number;
  loyaltyMultiplier: number;             // Increases with customer tenure
  riskMultiplier: number;                // Decreases with risk score
  failureReasonAdjustments: Record<string, number>;
}

const GRACE_DURATION: GraceDurationCalculator = {
  baseDays: 7,
  loyaltyMultiplier: 1.5,               // Long-term customers get 50% more
  riskMultiplier: 0.5,                  // High risk customers get 50% less
  failureReasonAdjustments: {
    insufficient_funds: 0,               // No adjustment
    card_expired: 14,                    // Extra time to update card
    processing_error: 7,                 // System issue, generous grace
    fraud_block: -7,                     // Suspicious activity, shorter grace
    network_error: 3,                    // Temporary, shorter grace
  },
};

function calculateGraceDuration(
  customer: Customer,
  failure: PaymentFailure,
  plan: Plan
): number {
  const calc = GRACE_DURATION;

  // Start with base
  let duration = calc.baseDays;

  // Apply loyalty multiplier
  const tenureMonths = getCustomerTenureMonths(customer);
  if (tenureMonths > 12) {
    duration *= calc.loyaltyMultiplier;
  }

  // Apply risk multiplier
  const riskScore = getCustomerRiskScore(customer);
  if (riskScore > 70) {
    duration *= calc.riskMultiplier;
  }

  // Apply failure reason adjustment
  const adjustment = calc.failureReasonAdjustments[failure.reason];
  if (adjustment) {
    duration += adjustment;
  }

  // Apply plan-level overrides
  if (plan.tier === 'enterprise') {
    duration = Math.max(duration, 30);
  }

  return Math.max(duration, 1);          // Minimum 1 day
}
```

## Feature Restrictions During Grace

During grace, certain features may be restricted to encourage payment resolution.

```typescript
interface GraceFeaturePolicy {
  featureId: string;
  restriction: 'none' | 'read_only' | 'disabled' | 'capped';
  capValue?: number;
  appliesAfterDays: number;              // Days into grace period
}

const GRACE_FEATURE_POLICIES: GraceFeaturePolicy[] = [
  { featureId: 'api_write_access', restriction: 'disabled', appliesAfterDays: 0 },
  { featureId: 'new_deployments', restriction: 'disabled', appliesAfterDays: 0 },
  { featureId: 'team_members', restriction: 'read_only', appliesAfterDays: 3 },
  { featureId: 'voice_minutes', restriction: 'capped', capValue: 1000, appliesAfterDays: 0 },
  { featureId: 'data_export', restriction: 'none', appliesAfterDays: 0 },
  { featureId: 'analytics', restriction: 'read_only', appliesAfterDays: 3 },
  { featureId: 'custom_models', restriction: 'disabled', appliesAfterDays: 5 },
];

class GraceFeatureRestrictor {
  async applyGraceRestrictions(
    subscriptionId: string,
    graceStartDate: string
  ): Promise<void> {
    const daysSinceStart = this.daysSince(graceStartDate);

    for (const policy of GRACE_FEATURE_POLICIES) {
      if (daysSinceStart >= policy.appliesAfterDays) {
        await this.applyFeatureRestriction(subscriptionId, policy);
      }
    }
  }

  private async applyFeatureRestriction(
    subscriptionId: string,
    policy: GraceFeaturePolicy
  ): Promise<void> {
    switch (policy.restriction) {
      case 'disabled':
        await this.disableFeature(subscriptionId, policy.featureId);
        break;
      case 'read_only':
        await this.setFeatureReadOnly(subscriptionId, policy.featureId);
        break;
      case 'capped':
        await this.capFeature(subscriptionId, policy.featureId, policy.capValue!);
        break;
    }
  }
}

// In-app banner showing grace status
function GracePeriodBanner({ gracePeriod }: { gracePeriod: GracePeriod }) {
  const daysRemaining = getDaysRemaining(gracePeriod.endDate);
  const percentageUsed = getPercentageUsed(gracePeriod.startDate, gracePeriod.endDate);

  return (
    <div className={`grace-banner ${getUrgencyClass(percentageUsed)}`}>
      <div className="grace-banner-content">
        <p>
          Your payment is past due. Service will be restricted in {daysRemaining} days.
        </p>
        <div className="grace-progress-bar">
          <div
            className="grace-progress-fill"
            style={{ width: `${percentageUsed}%` }}
          />
        </div>
        <div className="grace-banner-actions">
          <Link to="/billing" className="button-primary">
            Update Payment
          </Link>
          <Link to="/contact-support" className="button-secondary">
            Contact Support
          </Link>
        </div>
      </div>
    </div>
  );
}
```

## Grace Period Monitoring

Track grace period metrics and customer behavior during grace.

```typescript
interface GracePeriodMetrics {
  totalActive: number;
  byPlan: Record<string, number>;
  recoveryRate: number;
  averageResolutionTime: number;         // Hours
  extensionRate: number;
  churnDuringGrace: number;
}

class GraceMetricsCollector {
  async getMetrics(): Promise<GracePeriodMetrics> {
    const activeGracePeriods = await this.getActiveGracePeriods();
    const resolvedGracePeriods = await this.getResolvedGracePeriods();

    return {
      totalActive: activeGracePeriods.length,
      byPlan: this.groupByPlan(activeGracePeriods),
      recoveryRate: this.calculateRecoveryRate(resolvedGracePeriods),
      averageResolutionTime: this.calculateAvgResolutionTime(resolvedGracePeriods),
      extensionRate: this.calculateExtensionRate(resolvedGracePeriods),
      churnDuringGrace: this.calculateChurnDuringGrace(resolvedGracePeriods),
    };
  }

  private calculateRecoveryRate(resolved: GracePeriod[]): number {
    const recovered = resolved.filter(r =>
      r.resolution?.type === 'payment_received' || r.resolution?.type === 'payment_updated'
    ).length;
    return resolved.length > 0 ? recovered / resolved.length : 0;
  }
}
```

## Open-Source Tools

- **BullMQ** — Grace period expiry scheduling and communication delays
- **PostgreSQL** — Grace period state and history
- **Redis** — Real-time grace status for in-app display
- **Handlebars** (MIT) — Grace period email templates
- **Unleash** (Apache 2.0) — Feature restriction toggle management
- **Metabase** (Apache 2.0) — Grace period metrics dashboards

## Integration Points

Grace period handling integrates with the dunning workflow (stage transitions), feature flag service (restrictions), subscription management (status changes), notification service (grace communications), and billing system (payment recovery).

## Production Considerations

- Always show clear in-app banner with days remaining
- Allow support team to override grace duration per customer
- Track grace period resolution metrics by plan
- Automatically restore service on successful payment
- Send daily reminders approaching expiry
- Provide self-service extension for low-risk customers
- Monitor for abuse of grace period extensions
- Include grace status in API responses for integrations

## Open-Source First Philosophy

BullMQ manages grace period timing and communication scheduling with precise delay jobs. Unleash toggles feature restrictions instantly during grace. PostgreSQL keeps the definitive grace period state with full history. Metabase provides dashboards for monitoring grace effectiveness. This stack replaces proprietary retention tools while maintaining full control over the customer recovery experience.
