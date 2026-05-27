# Section 02: Feature Tier Mapping

## Per-Plan Feature Matrix

The feature matrix is the canonical document mapping every product feature to its availability across plans. Each feature receives an availability level: `free`, `starter`, `growth`, `pro`, `enterprise`, or a specific `addon`. The matrix must be comprehensive, machine-readable (used by the feature gating system), and human-readable (used by sales and marketing).

```
┌──────────────────────────────┬───────┬─────────┬────────┬──────┬────────────┐
│ Feature                      │ Free  │ Starter │ Growth │ Pro  │ Enterprise │
├──────────────────────────────┼───────┼─────────┼────────┼──────┼────────────┤
│ Voice Outbound Calls         │ 100/m │ 1,000/m │ 10K/m  │ 50K  │ Custom     │
│ Voice Inbound Calls          │ 50/m  │ 500/m   │ 5K/m   │ 25K  │ Custom     │
│ AI Agents                    │ 1     │ 3       │ 10     │ 25   │ Unlimited  │
│ Voice Clones                 │ -     │ 1       │ 5      │ 20   │ Custom     │
│ Languages                    │ 1     │ 3       │ 10     │ 30   │ All (100+) │
│ Custom Vocabulary            │ -     │ ✓       │ ✓      │ ✓    │ ✓          │
│ Sentiment Analysis           │ -     │ -       │ ✓      │ ✓    │ ✓          │
│ Real-time Transcription      │ ✓     │ ✓       │ ✓      │ ✓    │ ✓          │
│ Post-Call Analytics          │ Basic │ Basic   │ Adv.   │ Adv. │ Custom     │
│ SLA                          │ -     │ 99.9%   │ 99.95% │ 99.99% │ 99.995% │
│ SSO / SAML                   │ -     │ -       │ -      │ ✓    │ ✓          │
│ Audit Logs                   │ -     │ -       │ 30 day │ 90 d │ 365 day    │
│ API Rate Limit (req/s)       │ 10    │ 100     │ 500    │ 2000 │ Custom     │
│ Webhook Inclusions           │ 1,000 │ 10,000  │ 100K   │ 1M   │ Unlimited  │
│ Data Retention               │ 7d    │ 30d     │ 90d    │ 365d │ Custom     │
│ Team Members                 │ 1     │ 3       │ 10     │ 50   │ Unlimited  │
│ Integrations                 │ 2     │ 5       │ 15     │ 50   │ Unlimited  │
│ Priority Support             │ -     │ -       │ -      │ ✓    │ ✓          │
│ Dedicated Account Manager    │ -     │ -       │ -      │ -    │ ✓          │
└──────────────────────────────┴───────┴─────────┴────────┴──────┴────────────┘
```

## Feature Gating Architecture

Feature gating connects the plan catalog to runtime access control. Each API request and UI action checks the tenant's plan against the feature matrix. The gating system uses a hierarchical override model: plan defaults → tenant-specific overrides → feature flags.

```typescript
interface FeatureGate {
  featureKey: string;
  planAccess: PlanAccessLevel[];
  defaultLimit?: number;
  overridable: boolean;
  rollingWindow?: {
    duration: 'monthly' | 'daily' | 'hourly';
    hardCap: boolean;
  };
}

interface PlanAccessLevel {
  planId: string;
  enabled: boolean;
  limit?: number;
  overageAllowed?: boolean;
  overageRate?: number;
}

async function checkFeatureAccess(
  tenantId: string,
  planId: string,
  featureKey: string
): Promise<FeatureAccess> {
  const plan = await planCatalog.getPlan(planId);
  const override = await tenantOverrides.get(tenantId, featureKey);

  const planFeature = plan.features.find(f => f.key === featureKey);
  const effective = override ?? planFeature;

  if (!effective || !effective.enabled) {
    return { granted: false, reason: 'feature_not_in_plan' };
  }

  const usage = await usageAggregator.currentUsage(tenantId, featureKey);
  const withinLimit = effective.limit
    ? usage < effective.limit
    : true;

  return {
    granted: withinLimit,
    limit: effective.limit,
    current: usage,
    overageAllowed: effective.overageAllowed,
  };
}
```

## Add-On Features

Add-ons allow customers to extend their plan without upgrading tiers. Common add-ons include additional minutes packages, extra voice clones, higher API rate limits, and extended data retention. Add-ons have their own SKUs in Stripe and are managed as separate line items.

Add-on pricing should be at a premium to base plan pricing to incentivize tier upgrades (the "decoy effect"). For example, extra Growth minutes might cost $0.05/min vs the base $0.02/min included in Pro.

## Enterprise-Only Features

Enterprise features are not exposed in the self-serve pricing page. These include dedicated infrastructure, custom SLAs, SSO/SAML, audit logs, and personalized onboarding. Sales teams negotiate these features as part of contract discussions, often using them as closing incentives.

```
Enterprise Feature Negotiation Matrix:
┌─────────────────────────────────────────────────────┐
│ Feature                │ Always │ Negotiable │ Rare  │
├────────────────────────┼────────┼────────────┼───────┤
│ Dedicated Infrastructure│   ✓    │            │       │
│ Custom SLA             │        │     ✓      │       │
│ SSO / SAML            │   ✓    │            │       │
│ Custom Integrations    │        │     ✓      │       │
│ On-site Support        │        │            │   ✓   │
│ White-labeling         │        │     ✓      │       │
│ Volume Discounts       │        │     ✓      │       │
│ API Concurrency Boost  │        │     ✓      │       │
└─────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **LaunchDarkly** (proprietary, free tier) — Feature flag management for plan gating
- **Unleash** (Apache 2.0) — Open-source feature toggle system
- **Flagsmith** (BSD-3) — Open-source feature management with plan-based targeting

For the open-source first approach, Unleash provides full control over feature gating without vendor lock-in. It can be self-hosted with PostgreSQL and exposes a REST API and SDKs for runtime evaluation.

## Integration Points

The feature tier mapping directly powers the API middleware (Part 4) that checks feature access before processing requests. It also feeds the plan comparison page rendered by Next.js (Part 2) and the onboarding flow that guides users to the appropriate plan. The feature gate service is called by every rate-limited endpoint and premium feature handler.

## Production Considerations

- Feature matrix changes must be backward compatible
- Plan downgrades must disable features gracefully (not delete data)
- Cache feature access checks aggressively (Redis, 5-minute TTL)
- Audit feature access denials for upselling opportunities
- Test feature gating in CI with plan-specific test suites
- Monitor feature adoption to identify under-valued features

## Open-Source First Philosophy

The feature matrix is stored as a YAML file in the repository, version-controlled alongside the codebase. Changes to the feature matrix go through the standard PR and review process. This eliminates the need for a proprietary pricing database while maintaining full auditability. The Unleash open-source project provides the runtime feature evaluation engine, replacing costly proprietary alternatives.
