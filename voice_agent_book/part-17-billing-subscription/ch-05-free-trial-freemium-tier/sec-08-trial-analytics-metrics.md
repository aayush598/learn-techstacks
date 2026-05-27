# Section 08: Trial Analytics Metrics

## Trial-to-Paid Conversion Rate

The trial-to-paid conversion rate is the most important trial metric. It measures the percentage of trial users who become paying customers. Industry benchmarks for SaaS range from 15-25% for self-serve trials with credit card required, and 2-5% for trials without credit card.

```typescript
interface TrialConversionMetrics {
  period: string;
  startedTrials: number;
  convertedToPaid: number;
  conversionRate: number;
  expiredWithoutConversion: number;
  stillActive: number;
  averageDaysToConversion: number;
  conversionByPlan: Record<string, {
    started: number;
    converted: number;
    rate: number;
  }>;
}

class TrialAnalyticsService {
  async getConversionMetrics(
    periodStart: string,
    periodEnd: string
  ): Promise<TrialConversionMetrics> {
    const trials = await this.db.trials.find({
      startedAt: {
        $gte: periodStart,
        $lte: periodEnd,
      },
    }).toArray();

    const total = trials.length;
    const converted = trials.filter(t => t.status === 'converted').length;
    const expired = trials.filter(t => t.status === 'expired').length;
    const active = trials.filter(t => t.status === 'active').length;

    // Conversion by plan
    const byPlan: Record<string, { started: number; converted: number; rate: number }> = {};
    for (const trial of trials) {
      if (!byPlan[trial.planId]) {
        byPlan[trial.planId] = { started: 0, converted: 0, rate: 0 };
      }
      byPlan[trial.planId].started++;
      if (trial.status === 'converted') {
        byPlan[trial.planId].converted++;
      }
    }
    for (const [plan, data] of Object.entries(byPlan)) {
      data.rate = data.started > 0 ? data.converted / data.started : 0;
    }

    // Average days to conversion
    const conversionDays = trials
      .filter(t => t.status === 'converted' && t.convertedAt)
      .map(t => {
        const start = new Date(t.startedAt);
        const end = new Date(t.convertedAt);
        return (end.getTime() - start.getTime()) / 86400000;
      });

    const avgDays = conversionDays.length > 0
      ? conversionDays.reduce((a, b) => a + b, 0) / conversionDays.length
      : 0;

    return {
      period: `${periodStart} — ${periodEnd}`,
      startedTrials: total,
      convertedToPaid: converted,
      conversionRate: total > 0 ? converted / total : 0,
      expiredWithoutConversion: expired,
      stillActive: active,
      averageDaysToConversion: avgDays,
      conversionByPlan: byPlan,
    };
  }
}
```

## Time-to-Conversion

Time-to-conversion measures how long it takes trial users to become paying customers. Short time-to-conversion (1-7 days) indicates strong product-market fit. Long time-to-conversion (7-14 days) suggests users need more time to evaluate.

```
Time-to-Conversion Distribution:
┌──────────────────────────────────────────────────────────────────┐
│ Conversion Day │ Users │ Cumulative %                            │
├────────────────┼───────┼────────────────────────────────────────┤
│ Day 1          │ 8%    │ ████ 8%                                 │
│ Day 2-3        │ 15%   │ ███████ 23%                             │
│ Day 4-7        │ 32%   │ ████████████████ 55%                    │
│ Day 8-14       │ 28%   │ ██████████████ 83%                      │
│ Day 14+        │ 17%   │ ████████ 100%                           │
└──────────────────────────────────────────────────────────────────┘
```

## Trial Drop-Off Analysis

Drop-off analysis identifies where in the trial journey users lose interest. Common drop-off points include signup, first-time setup, first call, and payment method entry.

```typescript
interface DropOffFunnel {
  stage: string;
  users: number;
  dropOff: number;
  dropOffRate: number;
  conversionRate: number;
}

async function analyzeDropOff(
  periodStart: string,
  periodEnd: string
): Promise<DropOffFunnel[]> {
  const stages = [
    { name: 'Sign Up', event: 'user.signed_up' },
    { name: 'Account Activated', event: 'user.activated' },
    { name: 'First Agent Created', event: 'agent.created' },
    { name: 'First Call Made', event: 'call.completed_first' },
    { name: 'Team Member Added', event: 'team.invited_first' },
    { name: 'Payment Method Entered', event: 'billing.payment_method_added' },
    { name: 'Converted to Paid', event: 'trial.converted' },
  ];

  const funnel: DropOffFunnel[] = [];
  let previousUsers = 0;

  for (let i = 0; i < stages.length; i++) {
    const stage = stages[i];
    const users = await this.analyticsService.countUniqueUsers(
      stage.event,
      periodStart,
      periodEnd
    );

    const dropOff = i > 0 ? previousUsers - users : 0;
    const dropOffRate = i > 0 && previousUsers > 0
      ? dropOff / previousUsers
      : 0;
    const conversionRate = users / (funnel[0]?.users || users);

    funnel.push({
      stage: stage.name,
      users,
      dropOff,
      dropOffRate,
      conversionRate,
    });

    previousUsers = users;
  }

  return funnel;
}
```

## Feature Usage During Trial

Analyzing which features trial users engage with predicts conversion likelihood. Users who complete key actions (first call, configure agent, add team members) convert at much higher rates.

```typescript
interface FeatureUsagePrediction {
  feature: string;
  usersWithFeature: number;
  conversionRateWithFeature: number;
  conversionRateWithoutFeature: number;
  liftMultiplier: number;
}

async function getConversionPredictors(
  periodStart: string,
  periodEnd: string
): Promise<FeatureUsagePrediction[]> {
  const features = [
    'first_call_completed',
    'agent_configured',
    'voice_clone_created',
    'team_member_invited',
    'api_key_created',
    'integration_connected',
    'analytics_viewed',
  ];

  const predictions: FeatureUsagePrediction[] = [];

  for (const feature of features) {
    const withFeature = await this.analyticsService.countUsersWithFeature(
      feature, periodStart, periodEnd
    );
    const withoutFeature = await this.analyticsService.countUsersWithoutFeature(
      feature, periodStart, periodEnd
    );

    const convertedWith = await this.analyticsService.countConvertedUsersWithFeature(
      feature, periodStart, periodEnd
    );
    const convertedWithout = await this.analyticsService.countConvertedUsersWithoutFeature(
      feature, periodStart, periodEnd
    );

    const rateWith = withFeature > 0 ? convertedWith / withFeature : 0;
    const rateWithout = withoutFeature > 0 ? convertedWithout / withoutFeature : 0;

    predictions.push({
      feature,
      usersWithFeature: withFeature,
      conversionRateWithFeature: rateWith,
      conversionRateWithoutFeature: rateWithout,
      liftMultiplier: rateWithout > 0 ? rateWith / rateWithout : 1,
    });
  }

  return predictions.sort((a, b) => b.liftMultiplier - a.liftMultiplier);
}
```

## Open-Source Tools

- **ClickHouse** (Apache 2.0) — Analytics database for trial metrics
- **PostgreSQL** — Trial event and conversion data
- **Metabase** (Apache 2.0) — Trial analytics dashboards
- **dbt** (Apache 2.0) — Data transformation for trial metrics
- **Redis** — Real-time conversion counter caching

## Integration Points

Trial analytics connects to the event tracking system (Part 12), the trial service (Section 1-7), the subscription service (conversion events), and the CRM (sales pipeline data).

## Production Considerations

- Track trial metrics daily with automated reporting
- Set up alerts for conversion rate drops
- Segment analysis by signup source, plan, and customer segment
- Correlate trial metrics with product changes
- Use time-to-conversion data to optimize reminder timing

## Open-Source First Philosophy

ClickHouse provides high-performance analytics for trial data at zero licensing cost. Metabase offers self-service dashboards for the growth team. dbt transforms raw trial events into business metrics. This all-open-source analytics stack replaces expensive product analytics platforms (Amplitude, Mixpanel) while providing equivalent trial insights.
