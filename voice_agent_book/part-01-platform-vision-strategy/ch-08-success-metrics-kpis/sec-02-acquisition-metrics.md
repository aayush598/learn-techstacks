# Section 02: Acquisition Metrics

## Acquisition Funnel

Acquisition metrics track the journey from first touchpoint to active user. Understanding this funnel reveals where prospects drop off and which channels perform best.

```
Acquisition Funnel
┌────────────────────────────────────────────────────────────────────────────┐
│ Stage              │ Metric              │ Typical Rate │ Target           │
├────────────────────────────────────────────────────────────────────────────┤
│ Website Visit      │ Unique visitors     │ 100%         │ 50K/mo (Y1)     │
│                    │                     │              │                  │
│ ▼                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐  │
│ │ Signup             │ Signup rate       │ 3-8%         │ 5%              │  │
│ └──────────────────────────────────────────────────────────────────────┘  │
│ ▼                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐  │
│ │ Onboarded          │ Onboarding rate   │ 40-70%       │ >60%           │  │
│ └──────────────────────────────────────────────────────────────────────┘  │
│ ▼                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐  │
│ │ Activated          │ Activation rate   │ 20-40%       │ >30%           │  │
│ └──────────────────────────────────────────────────────────────────────┘  │
│ ▼                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐  │
│ │ Paid               │ Paid conversion   │ 5-15%        │ >10%           │  │
│ └──────────────────────────────────────────────────────────────────────┘  │
│ ▼                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐  │
│ │ Retained           │ Retention rate    │ 30-60% (D30) │ >50% (D30)     │  │
│ └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

## Key Acquisition Metrics

### Traffic & Top-of-Funnel
- **Website visitors (unique):** Number of unique visitors to website
- **Traffic by source:** Organic, paid, direct, referral, social, email
- **Bounce rate:** % of visitors leaving without interaction
- **Pages per session:** Engagement depth
- **SEO keyword rankings:** Track target keywords (voice AI, AI phone agent, etc.)

### Signup Conversion
- **Signup rate:** % of visitors who create an account
- **Signup completion rate:** % who complete email verification
- **Signup by plan:** % choosing free vs. paid (direct signup)
- **Signup by source:** Which channels produce highest-quality signups

### Activation
- **Time to activate:** Time from signup to first meaningful action
- **Activation triggers:** Set up first agent, make first test call
- **Activation rate:** % of signups who reach activation trigger within 7 days

## Acquisition Metrics Data Model

```typescript
interface AcquisitionMetrics {
  traffic: {
    totalVisitors: number;
    uniqueVisitors: number;
    pageViews: number;
    bounceRate: number;
    avgSessionDuration: number;
    sources: Record<string, ChannelMetrics>;
  };
  
  conversion: {
    signups: number;
    conversionRate: number;
    signupsBySource: Record<string, number>;
    signupsByPlan: Record<string, number>;
  };
  
  activation: {
    activated: number;
    activationRate: number;
    medianTimeToActivate: number; // hours
    activationSteps: CompletionStats[];
  };
  
  channelEconomics: {
    cac: number;
    cacByChannel: Record<string, CACData>;
    blendedCAC: number;
    paybackPeriod: number; // months
  };
}

interface ChannelMetrics {
  visitors: number;
  signups: number;
  conversionRate: number;
  cac: number;
  quality: 'high' | 'medium' | 'low';
}

interface CACData {
  spend: number;
  signups: number;
  paidCustomers: number;
  cac: number;
  cacPaybackMonths: number;
}
```

## Channel Performance Tracking

| Channel | Visitors/mo | Signups | Conv. Rate | CAC | Quality (30d retention) |
|---------|-------------|---------|------------|-----|------------------------|
| Organic (SEO) | 20,000 | 800 | 4.0% | $50 | 85% |
| Google Ads | 10,000 | 500 | 5.0% | $200 | 75% |
| GitHub (OSS) | 5,000 | 300 | 6.0% | $100 | 88% |
| LinkedIn Ads | 2,000 | 60 | 3.0% | $350 | 80% |
| Direct/Referral | 8,000 | 400 | 5.0% | $75 | 90% |
| Product Hunt | 3,000 | 120 | 4.0% | $150 | 70% |
| Content/Newsletter | 4,000 | 160 | 4.0% | $80 | 82% |

## Acquisition Funnel Optimization

**Top optimization levers:**
1. **Landing page A/B testing:** Test headlines, CTAs, social proof, pricing display
2. **Signup friction reduction:** Google OAuth, minimal form fields, no credit card
3. **Onboarding wizard:** Guided setup with progress indicator, pre-built templates
4. **Email sequences:** Post-signup drip (Day 1: first call, Day 3: analytics, Day 7: team invites)

## Weekly Acquisition Dashboard

```
Acquisition Weekly Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Metric                │ This Week │ Last Week │ Change    │ Target     │
├─────────────────────────────────────────────────────────────────────────┤
│ Website Visitors      │ 12,847    │ 11,234    │ +14.4%    │ 12,000     │
│ Signups               │ 547       │ 489       │ +11.9%    │ 600        │
│ Signup Rate           │ 4.3%      │ 4.4%      │ -0.1pp    │ 5.0%       │
│ Activated Users       │ 312       │ 278       │ +12.2%    │ 360        │
│ Activation Rate       │ 57.0%     │ 56.9%     │ +0.1pp    │ 60%        │
│ Paid Signups          │ 47        │ 42        │ +11.9%    │ 50         │
│ Free→Paid Conversion  │ 8.6%      │ 8.6%      │ 0.0pp     │ 10%        │
│ Total CAC (blended)   │ $198      │ $205      │ -3.4%     │ <$250      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tools & Resources

- **Web analytics:** PostHog, Plausible, Google Analytics 4
- **Conversion tracking:** PostHog (events), Google Tag Manager
- **SEO:** Ahrefs, SEMrush, Google Search Console
- **Paid ads:** Google Ads, LinkedIn Campaign Manager
- **Landing page A/B:** GrowthBook, Vercel Edge Config
- **Attribution:** PostHog, Wicked Reports, Dreamdata
