# Section 04: Retention & Engagement Metrics

## Retention Framework

Retention measures whether customers continue to find value over time. It's the most important growth lever — improving retention by 5% increases profits by 25-95% (Bain & Co).

```
Retention Cohorts Analysis
┌─────────────────────────────────────────────────────────────────────────┐
│ Weekly Retention Cohorts (Users who made at least 1 call)              │
│                                                                         │
│ Week │ W0   W1   W2   W3   W4   W5   W6   W7   W8   W9  W10          │
│ ─────┼──────────────────────────────────────────────────────────────  │
│ Jan  │ 100% 52%  42%  38%  35%  32%  30%  28%  27%  26%  25%          │
│ Feb  │ 100% 55%  45%  40%  37%  34%  31%  29%  28%                    │
│ Mar  │ 100% 58%  48%  43%  40%  37%  34%                              │
│ Apr  │ 100% 61%  51%  46%  42%                                        │
│ May  │ 100% 64%  54%                                                  │
│ Jun  │ 100% 66%                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Retention Metrics

### Overall Retention
- **D1 Retention:** Users returning Day 1 (target: >40%)
- **D7 Retention:** Users active within 7 days (target: >55%)
- **D30 Retention:** Users active within 30 days (target: >50%)
- **D90 Retention:** Users active within 90 days (target: >40%)

### Engagement Metrics
- **DAU/MAU (Stickiness):** Daily active / monthly active users (target: >30%)
- **Sessions per user:** Average weekly sessions (target: >3)
- **Calls per user:** Average weekly calls per active user (target: >20)
- **Minutes per user:** Average weekly minutes (target: >60 min)
- **Feature stickiness:** % of users using key features weekly

### Cohort Retention
- **Weekly retention curve:** How usage decays over 12 weeks
- **Power user curve:** % of users who become power users (>100 calls/month)
- **Resurrection rate:** % of churned users who return

## Retention Data Model

```typescript
interface RetentionMetrics {
  overall: {
    d1: number;
    d7: number;
    d30: number;
    d90: number;
    d365: number;
  };
  
  engagement: {
    dau: number;
    mau: number;
    stickiness: number; // DAU/MAU
    weeklySessionsPerUser: number;
    weeklyCallsPerUser: number;
    weeklyMinutesPerUser: number;
  };
  
  cohorts: CohortRetention[];
  
  segmentation: {
    byPlan: Record<string, RetentionMetrics>;
    byVertical: Record<string, RetentionMetrics>;
    byAcquisitionSource: Record<string, RetentionMetrics>;
    byActivationTime: Record<string, RetentionMetrics>;
  };
}

function analyzeChurnRisk(metrics: RetentionMetrics): ChurnRiskAnalysis {
  const riskFactors = [];
  
  if (metrics.engagement.weeklyCallsPerUser < 5) {
    riskFactors.push({ factor: 'Low call volume', severity: 'high', intervention: 'Usage tips email' });
  }
  if (metrics.engagement.stickiness < 0.2) {
    riskFactors.push({ factor: 'Low stickiness', severity: 'high', intervention: 'Feature re-engagement' });
  }
  if (metrics.overall.d7 < 0.4) {
    riskFactors.push({ factor: 'Poor week-1 retention', severity: 'critical', intervention: 'Early onboarding fix' });
  }
  
  return {
    riskScore: calculateRiskScore(riskFactors),
    factors: riskFactors,
    atRiskUsers: getAtRiskUsers(riskFactors),
    recommendedActions: generateActions(riskFactors),
  };
}
```

## Power User Curve

The power user curve shows the distribution of user engagement. A healthy product has a "smile" shape: many power users and many engaged users.

```
Power User Curve (Weekly Active Minutes)
Distribution of weekly active minutes across user base

Top 10%: 1,500+ minutes (Power users — building agents for many calls)
Next 25%: 300-1,500 minutes (Regular users — production use)
Middle 40%: 50-300 minutes (Casual users — testing, light use)
Bottom 25%: 0-50 minutes (At-risk — barely using)
```

## Engagement Features by User Segment

| Segment | Weekly Minutes | Engagement Strategy | Key Feature to Push |
|---------|---------------|--------------------|-------------------|
| Power users | 1,500+ | Early access, feedback calls, case study | Advanced analytics, API |
| Regular users | 300-1,500 | Usage reports, tips, community | Team invites, integrations |
| Casual users | 50-300 | Feature discovery, seasonal prompts | Templates, new voices |
| At-risk users | <50 | Re-engagement campaign, win-back offer | Quick start again |

## Retention Levers

**Top retention drivers (by impact):** (1) Call quality (accuracy, latency, naturalness), (2) First call success rate, (3) Time to first value (<5 min), (4) Integration with existing tools, (5) Team collaboration features.

**Retention playbook:** (1) Week 1: Ensure successful first call, (2) Week 2: Send usage report with ROI comparison, (3) Week 3: Invite team member, (4) Week 4: Feature discovery (something they haven't tried), (5) Month 2: Case studies, community invite, (6) Month 3: Quarterly business review (for paid).

## Retention Dashboard

```
Retention Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ D1: 42%   D7: 58%   D30: 52%   D90: 38%   Stickiness: 0.32           │
│                                                                         │
│ Retention Curve (Cohort: April 2026)                                    │
│ 100% ┤████████████████████████████████████                             │
│  80% ┤███████████████████████                                          │
│  60% ┤████████████████                                                  │
│  40% ┤██████████                                                        │
│  20% ┤█████                                                             │
│   0% ┤────────────────────────────────────────────────────              │
│      W0   W1   W2   W3   W4   W5   W6   W7   W8   W9  W10            │
│                                                                         │
│ At-Risk Users: 247 (8.2%)                                              │
│ Top Intervention: Send personalized usage report + ROI comparison      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tools & Resources

- **Retention analytics:** PostHog (cohorts), Amplitude, Mixpanel
- **Engagement tracking:** PostHog (DAU/MAU, stickiness)
- **Power user analysis:** Amplitude, PostHog
- **User segmentation:** PostHog, HubSpot
- **Re-engagement emails:** Loops, Resend, Customer.io
- **In-app messaging:** Appcues, Chameleon, Userflow
- **Win-back offers:** Stripe (discounts), Intercom (outreach)
