# Section 06: Plan Configuration Schema

## Plan Definition Data Model

The plan configuration schema is the canonical data model that defines every aspect of a subscription plan. It must be expressive enough to capture all pricing models, feature rules, limits, and metadata, while remaining simple enough to maintain and version.

```typescript
// Core plan configuration schema
interface PlanConfiguration {
  id: string;
  name: string;
  slug: string;
  rank: number;
  segment: 'free' | 'starter' | 'growth' | 'pro' | 'enterprise';
  visibility: 'public' | 'hidden' | 'sales_only';

  pricing: PricingConfiguration;

  features: FeatureConfiguration[];
  limits: LimitConfiguration[];

  metadata: {
    displayName: string;
    tagline: string;
    description: string;
    popular?: boolean; // Highlight as "most popular" on pricing page
    ctaLabel: string;
  };

  localization: Record<string, LocalizedPlanConfig>;
  availability: PlanAvailability;
}

interface PricingConfiguration {
  models: PricingModel[];
  currencies: Record<string, CurrencyPrice>;
  billingPeriods: {
    monthly?: BillingPeriodConfig;
    annual?: BillingPeriodConfig;
    quarterly?: BillingPeriodConfig;
  };
  freeTrial?: {
    days: number;
    requirePaymentMethod: boolean;
    features: string[]; // Features available during trial
  };
}

interface PricingModel {
  type: 'flat' | 'per_seat' | 'per_agent' | 'usage_tiered' | 'hybrid';
  components: PricingComponent[];
}

interface PricingComponent {
  metric?: string;           // e.g., 'minutes', 'agents'
  included: number;          // Units included in base price
  unitPrice: number;         // Price per unit in cents
  tiered?: TierConfig[];     // Tiered pricing structure
  overageRate?: number;      // Overage price per unit
}

interface TierConfig {
  from: number;
  to: number | 'inf';
  unitPrice: number;
  flatFee?: number;
}

interface LimitConfiguration {
  metric: string;            // e.g., 'monthly_minutes'
  softLimit: number;         // Included amount
  hardLimit?: number;        // Absolute maximum
  overageAllowed: boolean;
  overageRate?: number;
  resetPeriod: 'monthly' | 'daily' | 'hourly' | 'never';
}
```

## Feature Flag Binding

Each plan feature maps to a feature flag in the runtime feature management system. The binding defines whether the feature is enabled, what limit applies, and whether overage is permitted. This creates a clean separation between plan configuration and runtime evaluation.

```typescript
interface FeatureConfiguration {
  key: string;
  enabled: boolean;
  limit?: FeatureLimit;
  dependencies?: string[]; // Features that must be enabled
  addonAvailable?: boolean;
  addonPrice?: AddonPrice;
}

interface FeatureLimit {
  type: 'count' | 'rate' | 'boolean' | 'duration';
  value: number | boolean;
  unit?: string;
}

interface AddonPrice {
  metric: string;
  unitPrice: number;
  tiered?: TierConfig[];
}
```

The binding is stored as YAML files in a configuration repository. Each plan has its own YAML file that defines the complete feature configuration.

## Quota Definitions

Quotas define how much of a resource a tenant can consume within a time window. They are stricter than limits — quotas enforce hard boundaries while limits have overage allowances.

```typescript
interface QuotaDefinition {
  resource: string;           // 'api_requests', 'concurrent_calls', 'storage'
  window: {
    type: 'sliding' | 'fixed';
    duration: 'hourly' | 'daily' | 'monthly';
    windowSize?: number;      // For sliding windows (ms)
  };
  defaults: {
    soft: number;             // Warning threshold
    hard: number;             // Enforcement threshold
  };
  overageAllowed: boolean;
  overageCost?: number;
  actionOnExceeded: 'block' | 'throttle' | 'notify' | 'upgrade_prompt';
  cooldownPeriod?: number;    // How long after hitting cap before reset
}
```

```
Example Quota Configuration (YAML):
quotas:
  monthly_minutes:
    window:
      type: fixed
      duration: monthly
    defaults:
      soft: 9000  # 90% alert
      hard: 10000 # Hard limit
    overageAllowed: true
    overageCost: 0.049 # Per minute in cents
    actionOnExceeded: upgrade_prompt

  concurrent_calls:
    window:
      type: sliding
      duration: hourly
    defaults:
      soft: 25
      hard: 50
    overageAllowed: false
    actionOnExceeded: block

  api_rate_limit:
    window:
      type: sliding
      duration: hourly
    defaults:
      soft: 90000
      hard: 100000
    overageAllowed: false
    actionOnExceeded: throttle
```

## Rate Limit Tiers

Rate limits scale with plan tier. Higher-tier plans get higher API request limits, more concurrent connections, and faster processing priorities. Rate limits are enforced at the API gateway level (Kong/NGINX) using configuration synced from the plan schema.

```typescript
interface RateLimitTier {
  planId: string;
  requestsPerSecond: number;
  burstLimit: number;
  concurrentCalls: number;
  priority: number; // Higher = more priority in queue
  rateLimitHeaders: boolean;
}
```

## Open-Source Tools

- **YAML** — Human-readable plan configuration files
- **PostgreSQL JSONB** — Runtime plan catalog storage
- **Unleash** — Feature flag evaluation engine
- **Stripe API** — Product and price synchronization
- **JSON Schema** — Validate plan configuration against schema

## Integration Points

The plan configuration schema is consumed by the subscription service (for Stripe sync), the feature gate service (for runtime authorization), the rate limiter (for API enforcement), and the billing engine (for invoice calculation). Changes to the schema must be backward compatible or versioned.

## Production Considerations

- Validate plan configurations against JSON Schema at deploy time
- Test plan changes in staging with synthetic tenants
- Cache plan configurations aggressively (Redis, 1-hour TTL)
- Monitor plan configuration errors in production
- Audit all plan configuration changes
- Provide a plan configuration preview tool for sales teams

## Open-Source First Philosophy

The plan configuration schema is defined in YAML and validated with JSON Schema, both open standards. PostgreSQL with JSONB provides flexible storage without a content management system. Unleash (Apache 2.0) handles feature flag evaluation without proprietary software. This stack uses only open-source and free-tier tools.
