# Section 02: Reseller Tier Configuration

## Overview

Reseller tier configuration defines the capabilities, pricing discounts, and feature access for each reseller level. Tiered reseller programs incentivize growth: higher tiers unlock better discounts, more features, dedicated support, and higher sub-account limits. The tier system is managed by the platform and assigned to resellers based on their performance metrics (monthly recurring revenue, number of sub-accounts, tenure).

Each tier defines: discount percentage (off platform list prices), markup allowance (reseller can add margin), feature access (white-labeling, APIs, custom integrations), sub-account limits, support level, and minimum commitment. Tiers are automatically reviewed monthly—a reseller that exceeds tier requirements is upgraded; one that falls below is downgraded with notice.

For a voice agent platform, tier configuration also controls: whether the reseller can white-label the platform, access to the reseller API, ability to set custom pricing for sub-accounts, and access to premium features like advanced analytics and priority support.

## Implementation Approach

```typescript
interface ResellerTier {
  id: string;
  name: string;
  requirements: {
    minMrr: number;        // Monthly recurring revenue
    minSubAccounts: number;
    minTenureMonths: number;
    minSatisfactionScore: number;
  };
  benefits: {
    discountPercent: number;
    maxMarkupPercent: number;
    maxSubAccounts: number;
    whiteLabelEnabled: boolean;
    apiAccess: boolean;
    customPricing: boolean;
    dedicatedSupport: boolean;
    slaTier: string;
  };
}

class ResellerTierManager {
  private tiers: ResellerTier[];

  async evaluateAndAssignTier(resellerId: string): Promise<ResellerTier> {
    const metrics = await this.getResellerMetrics(resellerId);
    
    // Find highest tier the reseller qualifies for
    const eligibleTier = this.tiers
      .filter(t => this.meetsRequirements(metrics, t.requirements))
      .sort((a, b) => b.benefits.discountPercent - a.benefits.discountPercent)[0];

    const currentTier = await this.getCurrentTier(resellerId);
    
    if (eligibleTier?.id !== currentTier?.id) {
      await this.assignTier(resellerId, eligibleTier);
      
      // Notify reseller of tier change
      await this.notificationService.send({
        resellerId,
        type: 'tier_changed',
        data: { newTier: eligibleTier?.name, oldTier: currentTier?.name },
      });
    }

    return eligibleTier;
  }

  async getEffectivePrice(resellerId: string, listPrice: number): Promise<EffectivePrice> {
    const tier = await this.getCurrentTier(resellerId);
    const discountMultiplier = (100 - tier.benefits.discountPercent) / 100;
    
    return {
      costPrice: listPrice * discountMultiplier,
      suggestedRetail: listPrice,
      maxRetail: listPrice * (1 + tier.benefits.maxMarkupPercent / 100),
      margin: (1 - discountMultiplier) * 100,
    };
  }

  async scheduleMonthlyReview(): Promise<void> {
    const resellers = await this.getAllResellers();
    
    for (const reseller of resellers) {
      await this.queue.add('evaluate-tier', { resellerId: reseller.id });
    }
  }
}
```

## Open-Source Tools

- **Rule Engine** (json-rules-engine) — Declarative tier qualification rules
- **node-cron** — Monthly tier review scheduling
- **PostgreSQL Window Functions** — Tier qualification analytics
- **Stripe** — Revenue tracking for tier qualification
- **Metabase / Grafana** — Reseller performance dashboards

## Production Considerations

- **Tier Notification:** Always notify resellers before tier changes. Downgrades should have a grace period (30 days) to allow the reseller to improve metrics.
- **Grandfathering:** Resellers who qualified for a tier historically should be grandfathered if the requirements change. Never downgrade a reseller due to rule changes.
- **Transparent Requirements:** Display tier requirements and current progress in the reseller dashboard. Show what they need to achieve to reach the next tier.
- **Manual Override:** Allow platform admins to manually assign tiers for strategic partners. Log manual overrides with justification and expiry.
- **Tier Period:** Evaluate tiers monthly but consider 3-month rolling averages to avoid volatility from seasonal fluctuations.
