# Section 08: Product-Led Growth Strategy

## PLG Framework

Product-Led Growth (PLG) is our primary go-to-market motion. We leverage the product itself to drive acquisition, retention, and expansion through self-serve onboarding, viral loops, and community effects.

```
PLG Flywheel
                    ┌──────────────────────┐
                    │                      │
                    ▼                      │
           ┌──────────────────────┐       │
           │   Open-Source       │       │
           │   Community         │───────│──→ More contributors
           │   Edition           │       │    → Better product
           └──────────────────────┘       │
                    │                      │
                    ▼                      │
           ┌──────────────────────┐       │
           │   Self-Serve        │       │
           │   Onboarding        │───────│──→ More signups
           │   (<5min to value)  │       │    → More data
           └──────────────────────┘       │
                    │                      │
                    ▼                      │
           ┌──────────────────────┐       │
           │   Viral Loop        │       │
           │   (Share agent,     │───────│──→ More referrals
           │   invite team)      │       │    → More users
           └──────────────────────┘       │
                    │                      │
                    ▼                      │
           ┌──────────────────────┐       │
           │   Self-Serve        │       │
           │   Upgrade to Paid   │───────┘
           │   (Usage-based)     │
           └──────────────────────┘
```

## Growth Loop 1: Open-Source to Product

**Mechanism:** Developer discovers open-source edition on GitHub → tries it locally → needs managed hosting → signs up for cloud → becomes paid customer → contributes code → improves product for everyone.

**Key metrics:** GitHub stars → download → cloud signup conversion. **Target:** 20k GitHub stars, 10k downloads/month, 5% cloud signup conversion from downloads.

## Growth Loop 2: Self-Serve Onboarding

**Mechanism:** User signs up → guided wizard (10 min) → first test call succeeds → delight → share with team → invite colleagues → organic expansion.

**Key metrics:** Time to first call (target: <5 min), onboarding completion rate (target: >60%), team invite rate (target: 1.5 invites/user).

## Growth Loop 3: Agent Sharing

**Mechanism:** User builds an agent → shares public link → anyone can test the agent → testers become users → builders get visibility → network effects.

**Viral factor:** K-factor = (agent shares per user) × (conversion rate from share). Target K > 1.0.

## Growth Loop 4: Marketplace Contributions

**Mechanism:** Power users create templates → publish to marketplace → other users install → creators get revenue share → more templates → platform stickiness.

## Growth Strategy Phases

### Phase 1: Foundation (Months 1-3)
**Focus:** Open-source community edition, basic self-serve signup, minimal onboarding wizard. **Target:** 500 GitHub stars, 100 active users.

### Phase 2: Acceleration (Months 4-6)
**Focus:** Viral loops (agent sharing), automated onboarding email series, first referral program. **Target:** 2K GitHub stars, 1K active users.

### Phase 3: Monetization (Months 7-9)
**Focus:** Self-serve upgrade flow, usage-based billing, free tier with limits. **Target:** $10K MRR, 5K active users.

### Phase 4: Ecosystem (Months 10-12)
**Focus:** Marketplace launch, agency partner program, community advocacy program. **Target:** $50K MRR, 15K active users.

## PLG Metrics Data Model

```typescript
interface PLGMetrics {
  acquisition: {
   OrganicTraffic: number;
    DirectSignups: number;
    GitHubToCloud: number;
    ReferralConversion: number;
    ViralKFactor: number;
  };
  activation: {
    SignupToOnboarded: number;
    OnboardedToFirstCall: number;
    TimeToValue: number; // minutes
    ActivationScore: number; // composite
  };
  retention: {
    D1Retention: number;
    D7Retention: number;
    D30Retention: number;
    MAU: number;
    Stickiness: number; // DAU/MAU
  };
  revenue: {
    FreeToPaid: number;
    ExpansionRevenue: number;
    NetRevenueRetention: number;
    ARPU: number;
  };
}

function computePLGHealth(metrics: PLGMetrics): PLGScore {
  const scores = {
    acquisition: metrics.Acquisition.ViralKFactor > 1 ? 100 : 
      metrics.Acquisition.ViralKFactor * 100,
    activation: metrics.Activation.TimeToValue < 5 ? 100 : 
      Math.max(0, 100 - (metrics.Activation.TimeToValue - 5) * 10),
    retention: metrics.Retention.D30Retention * 100,
    revenue: metrics.Revenue.NetRevenueRetention * 100,
  };
  
  return {
    overall: Object.values(scores).reduce((a, b) => a + b) / 4,
    components: scores,
    recommendations: generatePLGRecommendations(scores),
  };
}
```

## Funnel Conversion Targets

| Stage | Current Baseline | Target | Improvement Strategy |
|-------|-----------------|--------|---------------------|
| Website visitor → signup | 3% | 8% | ROI calculator, social proof |
| Signup → activated | 40% | 65% | Better wizard, progress tracking |
| Activated → paid | 8% | 15% | Usage limit nudges, upgrade prompts |
| Paid → expansion | 12% | 25% | Team invites, usage alerts |
| Churn (monthly) | 8% | 3% | Onboarding success, value delivery |

## Community-Led Growth

**GitHub strategy:** MIT license, comprehensive CONTRIBUTING.md, good first issues, community calls, Discord for real-time chat.

**Content strategy:** Technical blog posts (2x/week), comparison pieces, tutorials, architecture deep-dives. SEO-optimized for voice AI keywords.

**Advocacy program:** Beta testers → early access → case studies → referral rewards. Tiered: Bronze (3 referrals), Silver (10), Gold (25+).

## Freemium to Paid Conversion

```
Free Tier (Always Free)      Starter ($49/mo)        Pro ($199/mo)
┌─────────────────────┐     ┌──────────────────┐    ┌──────────────────┐
│ 100 min/month       │     │ 1,000 min/month  │    │ 10,000 min/month │
│ 1 agent             │     │ 5 agents         │    │ Unlimited agents │
│ Basic analytics     │     │ Advanced analytics│   │ Custom analytics │
│ Community support   │     │ Email support    │    │ Priority support │
│ 1 voice             │     │ 5 voices         │    │ Custom voices    │
└─────────────────────┘     └──────────────────┘    └──────────────────┘
```

## Tools & Resources

- **PLG analytics:** PostHog, Amplitude, Mixpanel
- **Onboarding:** Userflow, Appcues, Chameleon
- **Email automation:** Loops, Resend, Customer.io
- **Referral programs:** Viral Loops, GrowSurf, ReferralCandy
- **Community:** Discord, Discourse, GitHub Discussions
- **Documentation:** Docusaurus, Nextra, Mintlify
