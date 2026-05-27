# Section 04: Subscription Downgrade Rules

## Automatic Downgrade on Failure

When payment failures persist past the grace period, the system automatically downgrades the subscription to a lower tier or free plan.

```
[Payment Failed]
    ↓
[Enter Grace Period]
    ├── Service continues (read-only or full)
    ├── Retry attempts continue
    └── Customer notified of pending downgrade
    ↓
[Grace Period Expires]
    ↓
[Evaluate Downgrade Path]
    ├── Enterprise → Pro (if Enterprise plan exists)
    ├── Pro → Free (with feature restrictions)
    └── Free → Suspended (no further downgrade possible)
    ↓
[Apply Downgrade]
    ├── Update subscription tier
    ├── Restrict features
    ├── Adjust rate limits
    └── Notify customer
    ↓
[Continue Retry]
    ├── Payment retries continue on new tier
    └── Auto-upgrade on successful payment
```

```typescript
interface DowngradeRule {
  fromPlan: string;
  toPlan: string;
  condition: DowngradeCondition;
  waitPeriodDays: number;
  featureChanges: FeatureChange[];
  rateLimitChanges: RateLimitChange[];
  dataRetentionPolicy: DataRetentionPolicy;
}

interface DowngradeCondition {
  type: 'payment_failure' | 'grace_expired' | 'manual' | 'usage_exceeded';
  failureThreshold: number;
  gracePeriodDays: number;
  maxDowngradeAttempts: number;
}

interface FeatureChange {
  featureId: string;
  action: 'disable' | 'reduce' | 'cap' | 'unchanged';
  newValue?: string | number | boolean;
}

interface DataRetentionPolicy {
  deletedAfterDays: number;
  archiveBeforeDelete: boolean;
  exportAvailable: boolean;
}

const DOWNGRADE_RULES: DowngradeRule[] = [
  {
    fromPlan: 'enterprise',
    toPlan: 'pro',
    condition: {
      type: 'payment_failure',
      failureThreshold: 5,
      gracePeriodDays: 14,
      maxDowngradeAttempts: 1,
    },
    waitPeriodDays: 30,          // Wait before offering downgrade
    featureChanges: [
      { featureId: 'dedicated_support', action: 'disable' },
      { featureId: 'custom_sla', action: 'disable' },
      { featureId: 'max_seats', action: 'reduce', newValue: 10 },
      { featureId: 'api_rate_limit', action: 'reduce', newValue: 1000 },
      { featureId: 'voice_minutes', action: 'reduce', newValue: 50000 },
    ],
    rateLimitChanges: [
      { name: 'api_rate', from: 10000, to: 1000 },
      { name: 'concurrent_calls', from: 100, to: 20 },
    ],
    dataRetentionPolicy: {
      deletedAfterDays: 90,
      archiveBeforeDelete: true,
      exportAvailable: true,
    },
  },
  {
    fromPlan: 'pro',
    toPlan: 'free',
    condition: {
      type: 'payment_failure',
      failureThreshold: 3,
      gracePeriodDays: 7,
      maxDowngradeAttempts: 1,
    },
    waitPeriodDays: 14,
    featureChanges: [
      { featureId: 'custom_voice', action: 'disable' },
      { featureId: 'analytics', action: 'reduce', newValue: 'basic' },
      { featureId: 'max_seats', action: 'reduce', newValue: 1 },
      { featureId: 'voice_minutes', action: 'reduce', newValue: 100 },
      { featureId: 'api_access', action: 'reduce', newValue: false },
      { featureId: 'team_collaboration', action: 'disable' },
    ],
    rateLimitChanges: [
      { name: 'api_rate', from: 1000, to: 10 },
      { name: 'concurrent_calls', from: 20, to: 1 },
    ],
    dataRetentionPolicy: {
      deletedAfterDays: 30,
      archiveBeforeDelete: true,
      exportAvailable: true,
    },
  },
];
```

## Feature Restriction Enforcement

When a downgrade occurs, feature restrictions must be enforced immediately across all services.

```typescript
class FeatureRestrictionEnforcer {
  async applyDowngrade(subscriptionId: string, rule: DowngradeRule): Promise<void> {
    // Update subscription plan
    await this.updateSubscriptionPlan(subscriptionId, rule.toPlan);

    // Apply feature changes
    for (const change of rule.featureChanges) {
      await this.applyFeatureChange(subscriptionId, change);
    }

    // Apply rate limit changes
    for (const change of rule.rateLimitChanges) {
      await this.applyRateLimit(subscriptionId, change);
    }

    // Schedule data retention policy
    await this.scheduleDataRetention(subscriptionId, rule.dataRetentionPolicy);

    // Notify all services of the change
    await this.invalidateServiceCache(subscriptionId);
  }

  private async applyFeatureChange(
    subscriptionId: string,
    change: FeatureChange
  ): Promise<void> {
    switch (change.action) {
      case 'disable':
        await this.featureFlagService.disable(subscriptionId, change.featureId);
        break;
      case 'reduce':
        await this.featureFlagService.setLimit(subscriptionId, change.featureId, change.newValue!);
        break;
      case 'cap':
        await this.featureFlagService.setCap(subscriptionId, change.featureId, change.newValue!);
        break;
    }
  }

  private async invalidateServiceCache(subscriptionId: string): Promise<void> {
    // Invalidate Redis cache keys for this subscription
    const keys = await redis.keys(`features:${subscriptionId}:*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }

    // Broadcast change to all services
    await pubSub.publish('subscription:downgraded', {
      subscriptionId,
      timestamp: new Date().toISOString(),
    });
  }
}

// Middleware that checks feature access after downgrade
class FeatureAccessMiddleware {
  async checkAccess(
    tenantId: string,
    featureId: string,
    context: RequestContext
  ): Promise<boolean> {
    const activeFeatures = await this.getActiveFeatures(tenantId);

    // Check if feature is enabled
    if (!activeFeatures.includes(featureId)) {
      // Check if feature was available on previous plan
      const previousPlan = await this.getPreviousPlan(tenantId);
      if (previousPlan?.features.includes(featureId)) {
        await this.logFeatureRestriction(tenantId, featureId, context);
      }
      return false;
    }

    // Check feature limits
    const limit = await this.getFeatureLimit(tenantId, featureId);
    if (limit && context.usage > limit) {
      return false;
    }

    return true;
  }
}
```

## Grace Period

The grace period provides time for customers to resolve payment issues before downgrade.

```typescript
interface GracePeriodState {
  subscriptionId: string;
  startDate: string;
  endDate: string;
  status: 'active' | 'expiring' | 'expired';
  serviceLevel: 'full' | 'read_only';
  notificationsSent: GraceNotification[];
  paymentAttempts: number;
}

class GracePeriodManager {
  async startGracePeriod(subscription: Subscription): Promise<GracePeriodState> {
    const rule = this.getDowngradeRule(subscription.planId);

    const state: GracePeriodState = {
      subscriptionId: subscription.id,
      startDate: new Date().toISOString(),
      endDate: this.calculateEndDate(rule.condition.gracePeriodDays),
      status: 'active',
      serviceLevel: 'read_only',
      notificationsSent: [],
      paymentAttempts: 0,
    };

    // Set service to read-only during grace
    await this.setServiceLevel(subscription.id, state.serviceLevel);

    // Schedule grace period expiry
    await this.scheduleGraceExpiry(state);

    return state;
  }

  async extendGracePeriod(
    subscriptionId: string,
    additionalDays: number
  ): Promise<void> {
    const state = await this.getGraceState(subscriptionId);
    if (!state) return;

    const newEnd = new Date(state.endDate);
    newEnd.setDate(newEnd.getDate() + additionalDays);
    state.endDate = newEnd.toISOString();

    await this.updateGraceState(state);
    await this.rescheduleGraceExpiry(state);
  }

  async resolveGracePeriod(
    subscriptionId: string,
    resolution: 'payment_received' | 'payment_method_updated' | 'admin_override'
  ): Promise<void> {
    await this.endGracePeriod(subscriptionId, resolution);
    await this.restoreServiceLevel(subscriptionId);
    await this.cancelPendingDowngrade(subscriptionId);
  }

  private calculateEndDate(graceDays: number): string {
    const end = new Date();
    end.setDate(end.getDate() + graceDays);
    return end.toISOString();
  }
}
```

## Downgrade Tiers

The downgrade path follows a tiered approach to minimize customer impact.

```typescript
type DowngradeTier = 'none' | 'feature_restricted' | 'rate_limited' | 'read_only' | 'suspended';

interface DowngradePath {
  currentTier: DowngradeTier;
  nextTier: DowngradeTier;
  conditions: DowngradeCondition[];
  reversalCondition: DowngradeCondition;
}

const DOWNGRADE_PATHS: Record<string, DowngradePath[]> = {
  enterprise: [
    { currentTier: 'none', nextTier: 'feature_restricted', conditions: [{ type: 'payment_failure', threshold: 3, gracePeriodDays: 7, maxDowngradeAttempts: 1 }], reversalCondition: { type: 'payment_failure', threshold: 3, gracePeriodDays: 7, maxDowngradeAttempts: 1 } },
    { currentTier: 'feature_restricted', nextTier: 'rate_limited', conditions: [{ type: 'payment_failure', threshold: 5, gracePeriodDays: 14, maxDowngradeAttempts: 1 }], reversalCondition: { type: 'payment_failure', threshold: 5, gracePeriodDays: 14, maxDowngradeAttempts: 1 } },
    { currentTier: 'rate_limited', nextTier: 'read_only', conditions: [{ type: 'payment_failure', threshold: 7, gracePeriodDays: 21, maxDowngradeAttempts: 1 }], reversalCondition: { type: 'payment_failure', threshold: 7, gracePeriodDays: 21, maxDowngradeAttempts: 1 } },
    { currentTier: 'read_only', nextTier: 'suspended', conditions: [{ type: 'payment_failure', threshold: 10, gracePeriodDays: 30, maxDowngradeAttempts: 1 }], reversalCondition: { type: 'payment_failure', threshold: 10, gracePeriodDays: 30, maxDowngradeAttempts: 1 } },
  ],
};

class DowngradeExecutor {
  async executeDowngrade(subscriptionId: string): Promise<DowngradeResult> {
    const subscription = await this.getSubscription(subscriptionId);
    const currentPath = this.getDowngradePath(subscription.planId, subscription.currentTier);
    if (!currentPath) {
      return { downgraded: false, reason: 'No downgrade path available' };
    }

    // Apply the downgrade
    await this.applyDowngradeTier(subscriptionId, currentPath.nextTier);

    // Start retry timer for reversal
    await this.scheduleReversalCheck(subscriptionId, currentPath.reversalCondition);

    return {
      downgraded: true,
      fromTier: currentPath.currentTier,
      toTier: currentPath.nextTier,
      effectiveDate: new Date().toISOString(),
    };
  }

  private async applyDowngradeTier(
    subscriptionId: string,
    tier: DowngradeTier
  ): Promise<void> {
    switch (tier) {
      case 'feature_restricted':
        await this.restrictPremiumFeatures(subscriptionId);
        break;
      case 'rate_limited':
        await this.applyRateLimits(subscriptionId, 'reduced');
        break;
      case 'read_only':
        await this.setReadOnlyMode(subscriptionId);
        break;
      case 'suspended':
        await this.suspendService(subscriptionId);
        break;
    }
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Downgrade rules and subscription state
- **BullMQ** — Schedule downgrade execution and grace expiry
- **Redis** — Cache feature flags and rate limits
- **Unleash** (Apache 2.0) — Feature flag management for downgrade enforcement
- **OpenTelemetry** — Downgrade event tracing

## Integration Points

Downgrade rules integrate with the subscription management system (plan changes), feature flag service (feature restrictions), rate limiter (API throttling), notification service (downgrade alerts), and data retention (archive and cleanup).

## Production Considerations

- Always notify customers before downgrade execution
- Provide data export window before account suspension
- Allow manual override for enterprise customers
- Re-evaluate downgrade on successful payment
- Track downgrade effectiveness for churn analysis
- Implement pause instead of cancel for temporary issues
- Offer subscription pause as alternative to downgrade
- Maintain feature parity data for reversal

## Open-Source First Philosophy

Unleash manages feature flag changes during downgrades with instant propagation. BullMQ schedules downgrade execution and grace period expiry with precise timing. PostgreSQL stores downgrade rules and history for analysis. This open-source stack replaces proprietary subscription management platforms while giving full control over downgrade logic and customer retention strategies.
