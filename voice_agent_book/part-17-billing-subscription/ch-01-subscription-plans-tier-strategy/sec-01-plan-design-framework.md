# Section 01: Plan Design Framework

## Tier Definition Methodology

Designing a subscription tier structure requires a systematic methodology that maps customer segments to plan features and pricing. The voice agent SaaS market spans solopreneurs to Fortune 500 enterprises, each with fundamentally different needs, usage patterns, and willingness to pay.

The tier definition methodology follows a top-down approach: identify customer segments through market research, define the value proposition for each segment, determine the features and limits that serve that value, and price according to the perceived value.

```
Customer Segments → Value Proposition → Feature Packaging → Pricing → Plan Names
     ↓                    ↓                    ↓               ↓            ↓
  Solopreneur         Simple voice        Core features    Low price      Free/Starter
  SMB                Team collaboration   Collaboration    Mid price      Growth
  Mid-Market         Scale & reliability  Analytics, SLA   High price     Pro
  Enterprise         Customization        Everything       Custom         Enterprise
```

## Value Metric Selection

The choice of value metric is the most critical decision in plan design. A value metric is the unit by which you measure consumption and set prices. Common SaaS value metrics include per-seat (per user), per-transaction (per call), consumption-based (per minute), or feature-based (per tier).

For a voice agent platform, the natural value metric is **minutes of voice processing** because it directly correlates with the value delivered. Minutes also scale naturally as customers grow. Alternative metrics like per-agent or per-seat may be simpler to understand but may not align with actual value delivered.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Value Metric Comparison                        │
├─────────────┬──────────────┬──────────────────┬──────────────────┤
│   Metric    │  Simplicity  │  Value Alignment  │  Scalability     │
├─────────────┼──────────────┼──────────────────┼──────────────────┤
│ Per-Minute  │    Medium    │      High         │     High         │
│ Per-Seat    │    High      │      Medium       │     Medium       │
│ Per-Agent   │    Medium    │      Low          │     Low          │
│ Flat Rate   │    High      │      Low          │     Low          │
│ Hybrid      │    Complex   │      Very High    │     High         │
└─────────────┴──────────────┴──────────────────┴──────────────────┘
```

## Plan Naming Conventions

Plan names should communicate the target segment and avoid technical jargon. Common conventions use tier descriptors that imply increasing value: Free, Starter, Growth, Pro, Enterprise. Avoid non-descriptive names like Basic, Standard, Premium which lack differentiation cues.

Each plan name should signal its position in the hierarchy. The Free plan attracts top-of-funnel users. Starter serves early-stage companies. Growth targets expanding SMBs. Pro addresses mid-market needs. Enterprise covers custom arrangements.

## Pricing Architecture

The pricing architecture defines how the plans relate to one another and how customers perceive progression. Good plan design creates a "good-better-best" progression where each tier has a clear reason to upgrade. The pricing should follow a power law where each tier is roughly 2-4x the price of the previous tier.

```typescript
interface PlanDefinition {
  id: string;
  name: string;
  rank: number; // Order in hierarchy
  billingModel: 'flat' | 'per_seat' | 'usage_based' | 'hybrid';
  valueMetric: string;
  basePrice: {
    monthly: number;
    annual: number; // Typically 2 months free
  };
  segment: 'individual' | 'team' | 'business' | 'enterprise';
  features: FeatureDefinition[];
  limits: LimitDefinition[];
  availability: 'self_serve' | 'sales_assist' | 'sales_only';
}

interface FeatureDefinition {
  key: string;
  name: string;
  enabled: boolean;
  limit?: number;
  overageAllowed?: boolean;
  overagePrice?: number;
}

interface LimitDefinition {
  metric: 'minutes' | 'agents' | 'voice_clones' | 'languages' | 'integrations';
  included: number;
  hardCap: boolean;
  maxOverage?: number;
}
```

## Plan Design Patterns

Three-tier pricing remains the most effective pattern in SaaS. Four tiers work when the market spans a wide range, but too many tiers create choice paralysis. The anchor pricing technique places the most expensive tier first on the pricing page to make the middle tier appear reasonable.

Good plan design also considers the concept of "feature differentiation" vs "limit differentiation". Feature differentiation restricts entire capabilities behind paywalls (e.g., custom voice cloning is Enterprise-only). Limit differentiation allows access but constrains quantity (e.g., Starter gets 1,000 minutes, Growth gets 10,000).

## Open-Source Tools for Plan Management

The plan catalog can be managed using PostgreSQL with a JSONB configuration table, avoiding the need for a dedicated CMS. The open-source pgAdmin tool provides a UI for managing catalog entries during development. For plan versioning, git-based configuration management using YAML files in a dedicated repository provides a serverless approach that leverages existing tools.

## Integration Points

The plan design framework integrates with the feature gating system (Part 8), the API rate limiter (Part 4), and the usage metering pipeline (Chapter 2 of this Part). The plan catalog must be accessible to the subscription service, the billing engine, and the Stripe product synchronization service.

## Production Considerations

- Plan changes require careful migration strategies
- Grandfather existing customers on old pricing
- Test pricing pages with A/B experiments
- Monitor plan adoption rates monthly
- Review competitive pricing quarterly
- Consider regional pricing adjustments

## Open-Source First Philosophy

Rather than building a proprietary pricing engine, we leverage Stripe's free tier for payment processing, PostgreSQL as our plan catalog database, and YAML files in a public git repository for plan definitions. This approach eliminates the need for a pricing CMS while maintaining full auditability and version control.
