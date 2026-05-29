# Section 01: Revenue Stream Architecture

## Multi-Layered Revenue Model

Our revenue model is designed with three tiers of revenue streams: primary (high volume, predictable), secondary (high margin, growing), and tertiary (strategic, ecosystem-building).

```
Revenue Stream Architecture
┌────────────────────────────────────────────────────────────────────┐
│ Primary Revenue Streams (85% of total revenue)                    │
│ ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│ │ Subscription (40% of total) │  │ Usage-Based (45% of total) │  │
│ │ • Monthly/Annual plans      │  │ • Per-minute voice         │  │
│ │ • Tiered by features        │  │ • Per-transcription        │  │
│ │ • Enterprise contracts      │  │ • Per-LLM-call             │  │
│ │ • White-label licenses      │  │ • Storage usage            │  │
│ └─────────────────────────────┘  └────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Secondary Revenue Streams (10% of total revenue)                  │
│ ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│ │ Marketplace (5% of total)   │  │ Professional Services (5%) │  │
│ │ • Template revenue share    │  │ • Implementation           │  │
│ │ • Voice pack sales          │  │ • Custom development       │  │
│ │ • Plugin marketplace        │  │ • Training & workshops     │  │
│ └─────────────────────────────┘  └────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Tertiary Revenue Streams (5% of total revenue)                    │
│ ┌─────────────────────────────┐  ┌────────────────────────────┐  │
│ │ API Access (3% of total)    │  │ Partner Revenue (2%)       │  │
│ │ • Pay-as-you-go API         │  │ • Telecom referral fees    │  │
│ │ • Webhook premium           │  │ • CRM integration fees     │  │
│ │ • Rate-limit overage        │  │ • Affiliate program        │  │
│ └─────────────────────────────┘  └────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## Revenue Model Design Decisions

**Why subscription + usage:** Subscription provides predictable baseline revenue for financial planning. Usage captures value from high-volume customers. Combined, they optimize for both stability and growth.

**Why marketplace:** Competitors (Retell, Vapi) have no marketplace. This creates a moat and community engagement. Comparable: Shopify's marketplace drives 15% of GMV.

**Why professional services:** Early-stage customers need implementation help. Services build relationships that lead to expansion. Comparable: Twilio's services arm.

## Revenue Stream Details

### Primary: Subscription Tiers

| Tier | Price | Target Segment | Target ARR Contribution |
|------|-------|----------------|------------------------|
| Free | $0 | Solo developers, evaluation | 0% (acquisition cost) |
| Starter | $49/mo | SMB, single location | 15% |
| Pro | $199/mo | Growing business, multi-agent | 25% |
| Business | $499/mo | Mid-market, teams | 30% |
| Enterprise | Custom ($2K-20K/mo) | Large enterprises | 30% |

### Primary: Usage-Based Pricing

| Service | Unit | Price | Margin |
|---------|------|-------|--------|
| Voice minutes (STT + TTS + LLM) | Per minute | $0.03-0.08 | 65-75% |
| Transcription only | Per minute | $0.01-0.02 | 80% |
| LLM call (no voice) | Per request | $0.001-0.005 | 75% |
| Storage | Per GB/month | $0.50-2.00 | 90% |
| SMS messages | Per message | $0.0075-0.02 | 20% (pass-through) |

### Secondary: Marketplace Commission

| Item | Commission | Volume (Y1) | Revenue (Y1) |
|------|-----------|-------------|--------------|
| Agent templates | 30% | 500 sales @ $49 avg | $7,350 |
| Voice packs | 20% | 1,000 sales @ $19 avg | $3,800 |
| Integrations/plugins | 25% | 200 sales @ $99 avg | $4,950 |
| UI themes | 15% | 300 sales @ $29 avg | $1,305 |

## Revenue Stream Data Model

```typescript
interface RevenueStream {
  id: string;
  name: string;
  type: 'subscription' | 'usage' | 'marketplace' | 'services' | 'api' | 'partner';
  contribution: number; // percentage of total revenue
  margin: number;
  growthRate: number;
  recurring: boolean;
  scalability: 'high' | 'medium' | 'low';
}

interface RevenueProjection {
  stream: string;
  monthly: number[];
  quarterly: number[];
  annual: number[];
  arr: number;
  mrr: number;
}

function calculateRevenueMix(streams: RevenueStream[]): RevenueMix {
  const totalContribution = streams.reduce((sum, s) => sum + s.contribution, 0);
  const totalMargin = streams.reduce((sum, s) => sum + (s.margin * s.contribution / 100), 0);
  
  return {
    weightedMargin: totalMargin,
    primaryPercent: streams.filter(s => s.type === 'subscription' || s.type === 'usage')
      .reduce((sum, s) => sum + s.contribution, 0),
    recurringPercent: streams.filter(s => s.recurring)
      .reduce((sum, s) => sum + s.contribution, 0),
    scalabilityScore: streams.reduce((sum, s) => {
      const scale = s.scalability === 'high' ? 3 : s.scalability === 'medium' ? 2 : 1;
      return sum + scale * s.contribution / 100;
    }, 0),
  };
}
```

## Revenue Stream Timeline

```
Revenue Build-Up Over 36 Months
Month 1-3:   Subscriptions only (Starter/Pro)          → $2K MRR
Month 4-6:   + Usage-based revenue                     → $8K MRR
Month 7-9:   + Marketplace (template sales)            → $20K MRR
Month 10-12: + Professional services                   → $50K MRR
Month 13-18: + Enterprise contracts, white-label       → $120K MRR
Month 19-24: + API access, partner revenue             → $250K MRR
Month 25-36: + International expansion                 → $500K MRR
```

## Competitive Pricing Comparison

| Pricing Element | Us | Retell AI | Vapi | Bland AI | Twilio |
|----------------|-----|-----------|------|----------|--------|
| Voice per minute | $0.03-0.08 | $0.12-0.18 | $0.08-0.12 | $0.06-0.10 | $0.014 (raw) |
| Free tier | 100 min | None | 5 min | 30 min | None |
| Starter monthly | $49 | None | $0 (Pay as you go) | $29 | None |
| Enterprise minimum | $2K/mo | $5K/mo | Custom | None | $1K/mo |
| White-label | Included | Custom quote | None | None | None |

## Revenue Optimization Strategies

- **Bundling:** Voice + transcription + analytics as bundle vs individual pricing
- **Tiered usage:** Lower per-unit price at higher volumes (incentivizes growth)
- **Annual prepay:** 20% discount for annual billing (improves cash flow, reduces churn)
- **Usage alerts:** Proactive notifications when approaching plan limits (triggers upgrades)
- **Credit system:** Pre-paid credit packs with expiration (captures upfront cash)

## Tools & Resources

- **Billing infrastructure:** Stripe, Lago, Metronome (usage-based)
- **Revenue analytics:** ChartMogul, ProfitWell, Baremetrics
- **Financial modeling:** Causal, Pigment, spreadsheet templates
- **Usage metering:** OpenMeter, Stripe Metering
- **Marketplace payments:** Stripe Connect, Paddle
