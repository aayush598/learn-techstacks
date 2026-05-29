# Section 02: Pricing Tier Definition

## Tier Architecture

Our pricing uses five tiers designed to segment the market by company size, usage volume, and feature requirements. Each tier has clear upgrade triggers and value differentiation.

```
Pricing Tier Ladder
                     ┌─────────────────────────────────────────┐
                     │ Enterprise (Custom Pricing)             │
                     │ $2,000 - $20,000+/month                 │
                     │ Self-host, SSO, HIPAA, SLA, Audit      │
                     ├─────────────────────────────────────────┤
                     │ Business ($499/month)                    │
                     │ 10 users, advanced analytics,           │
                     │ custom integrations, phone support      │
              ┌──────┤                                         │
              │      ├─────────────────────────────────────────┤
              │ Pro ($199/month)                               │
              │ 5 users, API access, custom voices,            │
              │ 5 agents, advanced flows                       │
       ┌──────┤                                                │
       │      ├─────────────────────────────────────────┤
       │Starter ($49/month)                              │
       │ 2 users, 2 agents, basic analytics,            │
       │ email support, 1,000 min/month                 │
       ├─────────────────────────────────────────┤
       │Free ($0/month)                             │
       │ 1 user, 1 agent, 100 minutes/month,       │
       │ basic dashboard, community support         │
       └─────────────────────────────────────────┘
```

## Feature Breakdown by Tier

| Feature | Free | Starter ($49) | Pro ($199) | Business ($499) | Enterprise |
|---------|------|--------------|------------|-----------------|------------|
| Voice minutes | 100/mo | 1,000/mo | 10,000/mo | 100,000/mo | Custom |
| Agents | 1 | 2 | 5 | 15 | Unlimited |
| Team members | 1 | 2 | 5 | 10 | Unlimited |
| Inbound calling | ✅ | ✅ | ✅ | ✅ | ✅ |
| Outbound calling | ✅ | ✅ | ✅ | ✅ | ✅ |
| SMS capability | ❌ | ❌ | ✅ | ✅ | ✅ |
| Custom LLM | ❌ | ❌ | ✅ | ✅ | ✅ |
| Analytics (basic) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Analytics (advanced) | ❌ | ❌ | ❌ | ✅ | ✅ |
| API access | ✅ (rate limited) | ✅ | ✅ | ✅ | ✅ |
| Custom voices | ❌ | ❌ | ✅ (5) | ✅ (20) | Unlimited |
| White-label | ❌ | ❌ | ❌ | ✅ | ✅ |
| SSO/SAML | ❌ | ❌ | ❌ | ❌ | ✅ |
| HIPAA compliance | ❌ | ❌ | ❌ | ❌ | ✅ |
| Self-hosted | ❌ | ❌ | ❌ | ❌ | ✅ |
| SLA | 99.5% | 99.5% | 99.9% | 99.95% | 99.99% |
| Support | Community | Email (24h) | Email (8h) | Phone (4h) | Dedicated |
| Data retention | 30 days | 90 days | 1 year | 2 years | Custom |

## Pricing Psychology & Positioning

**Free tier purpose:** Acquisition and evaluation. 100 minutes is enough for 1-2 demos but not enough for production. Forces upgrade path. **Starter at $49:** Price point tested across 200+ SMB interviews. $49/mo is below average phone bill — easy to justify. **Pro at $199:** Sweet spot for serious users. Price anchoring: Retell AI equivalent would be $500-800/mo. **Business at $499:** Team pricing. At 10 users, $49/user/month — compelling vs per-seat competitors.

## Pricing Data Model

```typescript
interface PricingTier {
  id: string;
  name: string;
  monthlyPrice: number;
  annualPrice: number; // annual = monthly * 12 * 0.8 (20% annual discount)
  targetSegment: string;
  
  limits: {
    voiceMinutes: number;
    agents: number;
    teamMembers: number;
    customVoices: number;
    storageGB: number;
    apiRateLimit: number; // requests/second
  };
  
  features: string[];
  compliance: string[];
  support: 'community' | 'email_24h' | 'email_8h' | 'phone_4h' | 'dedicated';
  sla: number;
}

interface PricingStrategy {
  tiers: PricingTier[];
  
  // Upgrade triggers
  triggers: {
    threshold: number; // % of limit usage
    action: PromptAction;
  }[];
  
  discounts: {
    annual: number; // 20%
    nonprofit: number; // 30%
    education: number; // 50%
    startup: number; // first 6 months: 50%
  };
}

function findOptimalTier(usage: UsageProfile): PricingTier {
  const qualifying = pricingTiers.filter(tier => {
    return tier.limits.voiceMinutes >= usage.monthlyMinutes &&
           tier.limits.agents >= usage.agentCount &&
           tier.limits.teamMembers >= usage.teamSize;
  });
  
  return qualifying.reduce((cheapest, tier) => 
    tier.monthlyPrice < cheapest.monthlyPrice ? tier : cheapest
  );
}
```

## Competitive Price Positioning

| Our Tier | vs Retell AI | vs Vapi | vs Bland AI | Value Advantage |
|----------|-------------|---------|-------------|----------------|
| Free (100 min) | No free tier ($200 min) | 5 min free | 30 min free | 20x more free minutes |
| Starter ($49) | No equivalent (min $200) | ~$80/mo @ 1K min | $29/mo @ 1K min | 40% cheaper than Vapi |
| Pro ($199) | ~$600/mo @ 10K min | ~$800/mo @ 10K min | ~$500/mo @ 10K min | 60-75% cheaper |
| Business ($499) | ~$5K/mo @ 100K min | ~$8K/mo @ 100K min | ~$5K/mo @ 100K min | 90-94% cheaper |

## Price Elasticity Analysis

```typescript
interface PriceElasticity {
  tier: string;
  currentPrice: number;
  optimalPrice: number;
  elasticity: number; // -1.5 means 1% price increase = 1.5% volume decrease
  revenueMaxPrice: number;
  competitorPressure: 'low' | 'medium' | 'high';
  willingnessToPay: number; // 1-10
}

const elasticityAnalysis: PriceElasticity[] = [
  { tier: 'Free', currentPrice: 0, optimalPrice: 0, elasticity: -0.1, revenueMaxPrice: 0, competitorPressure: 'low', willingnessToPay: 2 },
  { tier: 'Starter', currentPrice: 49, optimalPrice: 59, elasticity: -0.8, revenueMaxPrice: 69, competitorPressure: 'medium', willingnessToPay: 6 },
  { tier: 'Pro', currentPrice: 199, optimalPrice: 229, elasticity: -0.6, revenueMaxPrice: 269, competitorPressure: 'low', willingnessToPay: 8 },
  { tier: 'Business', currentPrice: 499, optimalPrice: 549, elasticity: -0.4, revenueMaxPrice: 649, competitorPressure: 'low', willingnessToPay: 9 },
];
```

## Pricing Experiments (Year 1)

- **Test 1:** Starter at $49 vs $59 (2-week A/B on pricing page) → $49 won on conversion, $59 won on revenue
- **Test 2:** Annual discount at 15% vs 20% vs 25% → 20% optimal for conversion/revenue balance
- **Test 3:** Usage overage vs hard cap → Hard cap with purchaseable top-up wins on CSAT
- **Test 4:** Free tier minutes at 50 vs 100 vs 200 → 100 min optimal for signup-to-paid conversion

## Tier Migration Path

```
Typical Customer Upgrade Journey
Free (week 1-2) → Starter (month 2-3) → Pro (month 4-6) → Business (month 7-12) → Enterprise (year 2+)
      │                  │                    │                    │
      ▼                  ▼                    ▼                    ▼
  Try it out        Need more           Need API,             Need team     Need compliance,
                     minutes            custom LLM          features,        self-hosting,
                                                             integrations     SLA, audit
```

## Tools & Resources

- **Pricing page A/B testing:** Vercel Edge Config + GrowthBook
- **Price optimization:** PriceBeam, Zilliant, PROS
- **Competitive pricing data:** Crayon, Klue, Prisync
- **Willingness to pay surveys:** Van Westendorp via SurveyMonkey, Typeform
- **Usage analytics:** PostHog, Amplitude (track feature usage by tier)
