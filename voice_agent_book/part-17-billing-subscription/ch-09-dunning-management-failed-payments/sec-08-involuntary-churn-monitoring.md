# Section 08: Involuntary Churn Monitoring

## Churn Cause Tracking

Involuntary churn monitoring tracks every cancellation caused by payment failures and categorizes the root cause.

```
[Payment Failure]
    ↓
[Classify Failure Reason]
    ├── Insufficient funds
    ├── Card expired
    ├── Card declined (bank)
    ├── Network error
    ├── Fraud block
    ├── Invalid CVV
    └── Processing error
    ↓
[Track Dunning Outcome]
    ├── Recovered during grace
    ├── Recovered after downgrade
    ├── Recovered via win-back
    └── Lost (involuntary churn)
    ↓
[Analyze Churn Reasons]
    ├── By plan tier
    ├── By customer segment
    ├── By payment method
    └── By failure reason
    ↓
[Generate Insights]
    ├── Recovery rate by stage
    ├── Average recovery time
    ├── Top failure reasons
    └── Revenue at risk
```

```typescript
interface InvoluntaryChurnEvent {
  id: string;
  subscriptionId: string;
  customerId: string;
  tenantId: string;
  planId: string;
  churnDate: string;
  churnType: InvoluntaryChurnType;
  failureReason: string;
  dunningHistory: DunningStageHistory[];
  totalRetryAttempts: number;
  totalGraceDays: number;
  communicationSent: number;
  revenueLost: number;
  recoveredLater: boolean;
  recoveryMethod?: 'dunning' | 'winback' | 'manual';
}

type InvoluntaryChurnType =
  | 'grace_expired'
  | 'max_retries_exceeded'
  | 'payment_method_not_updated'
  | 'downgrade_rejected'
  | 'fraud_blocked';

interface DunningStageHistory {
  stage: DunningStage;
  enteredAt: string;
  exitedAt?: string;
  exitReason?: 'payment_received' | 'escalated' | 'timeout';
  attemptsInStage: number;
  communicationsSent: number;
}

class InvoluntaryChurnTracker {
  async recordChurn(
    subscription: Subscription,
    finalState: DunningState
  ): Promise<InvoluntaryChurnEvent> {
    const event: InvoluntaryChurnEvent = {
      id: generateId('churn'),
      subscriptionId: subscription.id,
      customerId: subscription.customerId,
      tenantId: subscription.tenantId,
      planId: subscription.planId,
      churnDate: new Date().toISOString(),
      churnType: this.classifyChurnType(finalState),
      failureReason: finalState.lastFailureReason,
      dunningHistory: finalState.stageHistory,
      totalRetryAttempts: finalState.totalRetryAttempts,
      totalGraceDays: this.calculateTotalGraceDays(finalState),
      communicationSent: finalState.totalCommunicationsSent,
      revenueLost: subscription.monthlyPrice,
      recoveredLater: false,
    };

    await this.storeChurnEvent(event);
    await this.updateChurnMetrics(event);

    return event;
  }

  private classifyChurnType(state: DunningState): InvoluntaryChurnType {
    if (state.lastFailureReason === 'fraud_block') return 'fraud_blocked';
    if (state.currentStage === DunningStage.GRACE_PERIOD && this.graceExpired(state)) {
      return 'grace_expired';
    }
    if (state.totalRetryAttempts >= 10) return 'max_retries_exceeded';
    return 'payment_method_not_updated';
  }

  async trackRecovery(
    churnId: string,
    method: InvoluntaryChurnEvent['recoveryMethod']
  ): Promise<void> {
    await this.updateChurnEvent(churnId, {
      recoveredLater: true,
      recoveryMethod: method,
    });

    // Update metrics
    await this.incrementRecoveryCount(method);
  }

  private async updateChurnMetrics(event: InvoluntaryChurnEvent): Promise<void> {
    await this.incrementTotalChurn();
    await this.addRevenueLost(event.revenueLost);
    await this.recordChurnByPlan(event.planId);
    await this.recordChurnByReason(event.failureReason);
  }
}
```

## Failure Reason Analysis

Deep analysis of failure reasons to identify patterns and systemic issues.

```typescript
interface FailureAnalysis {
  period: { start: string; end: string };
  totalFailures: number;
  byReason: Record<string, FailureReasonStat>;
  byCardNetwork: Record<string, CardNetworkStat>;
  byPlanTier: Record<string, PlanTierStat>;
  trends: FailureTrend[];
  recommendations: string[];
}

interface FailureReasonStat {
  reason: string;
  count: number;
  percentage: number;
  recoveryRate: number;
  avgRetryAttempts: number;
}

class FailureAnalyzer {
  async analyzeFailureReasons(
    startDate: string,
    endDate: string
  ): Promise<FailureAnalysis> {
    const failures = await this.getFailuresInRange(startDate, endDate);

    const byReason: Record<string, FailureReasonStat> = {};
    for (const failure of failures) {
      if (!byReason[failure.reason]) {
        byReason[failure.reason] = {
          reason: failure.reason,
          count: 0,
          percentage: 0,
          recoveryRate: 0,
          avgRetryAttempts: 0,
        };
      }
      byReason[failure.reason].count++;
    }

    // Calculate percentages and recovery rates
    for (const [reason, stat] of Object.entries(byReason)) {
      stat.percentage = (stat.count / failures.length) * 100;
      const recovered = failures.filter(f => f.reason === reason && f.recovered).length;
      stat.recoveryRate = stat.count > 0 ? (recovered / stat.count) * 100 : 0;
      stat.avgRetryAttempts = failures
        .filter(f => f.reason === reason)
        .reduce((sum, f) => sum + f.retryAttempts, 0) / stat.count;
    }

    return {
      period: { start: startDate, end: endDate },
      totalFailures: failures.length,
      byReason,
      byCardNetwork: await this.analyzeByCardNetwork(failures),
      byPlanTier: await this.analyzeByPlanTier(failures),
      trends: await this.analyzeTrends(startDate, endDate),
      recommendations: this.generateRecommendations(byReason),
    };
  }

  private generateRecommendations(
    byReason: Record<string, FailureReasonStat>
  ): string[] {
    const recommendations: string[] = [];

    if (byReason['card_expired']?.percentage > 20) {
      recommendations.push('Implement proactive card expiry notifications 30 days before expiry');
    }
    if (byReason['insufficient_funds']?.percentage > 30) {
      recommendations.push('Consider offering payment plans or partial payment options');
    }
    if (byReason['fraud_block']?.percentage > 5) {
      recommendations.push('Review fraud detection rules — may be blocking legitimate transactions');
    }

    return recommendations;
  }
}
```

## Recovery Rate Metrics

Monitor the effectiveness of dunning and recovery efforts.

```typescript
interface RecoveryMetrics {
  period: { start: string; end: string };
  totalChurned: number;
  totalRecovered: number;
  overallRecoveryRate: number;
  byStage: StageRecovery[];
  byFailureReason: ReasonRecovery[];
  byPlan: PlanRecovery[];
  recoveryTimeDistribution: RecoveryTimeBucket[];
  revenueRecovered: number;
}

class RecoveryMetricsCollector {
  async getMetrics(
    startDate: string,
    endDate: string
  ): Promise<RecoveryMetrics> {
    const churns = await this.getChurnsInRange(startDate, endDate);
    const recovered = churns.filter(c => c.recoveredLater);

    // Recovery by dunning stage
    const byStage: StageRecovery[] = [
      { stage: DunningStage.IMMEDIATE_RETRY, recovered: 0, total: 0, rate: 0 },
      { stage: DunningStage.SOFT_REMINDER, recovered: 0, total: 0, rate: 0 },
      { stage: DunningStage.ACTIVE_RECOVERY, recovered: 0, total: 0, rate: 0 },
      { stage: DunningStage.GRACE_PERIOD, recovered: 0, total: 0, rate: 0 },
    ];

    for (const churn of churns) {
      const lastStage = churn.dunningHistory[churn.dunningHistory.length - 1];
      const stageMetric = byStage.find(s => s.stage === lastStage?.stage);
      if (stageMetric) {
        stageMetric.total++;
        if (churn.recoveredLater) stageMetric.recovered++;
      }
    }

    for (const stage of byStage) {
      stage.rate = stage.total > 0 ? (stage.recovered / stage.total) * 100 : 0;
    }

    // Revenue recovered
    const revenueRecovered = recovered.reduce(
      (sum, c) => sum + c.revenueLost, 0
    );

    return {
      period: { start: startDate, end: endDate },
      totalChurned: churns.length,
      totalRecovered: recovered.length,
      overallRecoveryRate: churns.length > 0
        ? (recovered.length / churns.length) * 100 : 0,
      byStage,
      byFailureReason: await this.groupByFailureReason(churns),
      byPlan: await this.groupByPlan(churns),
      recoveryTimeDistribution: await this.calculateRecoveryTimeDistribution(churns),
      revenueRecovered,
    };
  }
}
```

## Dunning Effectiveness

Evaluate which dunning strategies are most effective for different customer segments.

```typescript
interface DunningEffectiveness {
  strategy: string;
  segment: string;
  contactRate: number;
  recoveryRate: number;
  avgDaysToRecover: number;
  costPerCommunication: number;
  roi: number;
}

class DunningEffectivenessAnalyzer {
  async analyzeDunningEffectiveness(
    startDate: string,
    endDate: string
  ): Promise<DunningEffectiveness[]> {
    const strategies = [
      { name: 'email_only', segments: ['low_value', 'self_service'] },
      { name: 'email_sms', segments: ['medium_value'] },
      { name: 'omni_channel', segments: ['high_value', 'enterprise'] },
    ];

    const results: DunningEffectiveness[] = [];

    for (const strategy of strategies) {
      for (const segment of strategy.segments) {
        const customers = await this.getCustomersInSegment(segment);
        const churns = customers.filter(c =>
          c.churnDate >= startDate && c.churnDate <= endDate
        );

        if (churns.length === 0) continue;

        const recovered = churns.filter(c => c.recoveredLater);
        const totalCommunications = churns.reduce(
          (sum, c) => sum + c.dunningState.totalCommunicationsSent, 0
        );

        results.push({
          strategy: strategy.name,
          segment,
          contactRate: churns.length / customers.length,
          recoveryRate: recovered.length / churns.length,
          avgDaysToRecover: this.calculateAvgDaysToRecover(recovered),
          costPerCommunication: 0.01, // SMS/email cost
          roi: this.calculateROI(recovered, totalCommunications),
        });
      }
    }

    return results;
  }
}

// Dashboard for involuntary churn monitoring
function InvoluntaryChurnDashboard({ metrics }: { metrics: RecoveryMetrics }) {
  return (
    <div className="churn-dashboard">
      <h2>Involuntary Churn Monitoring</h2>

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Overall Recovery Rate</h3>
          <p className={`metric-value ${getRateColor(metrics.overallRecoveryRate)}`}>
            {metrics.overallRecoveryRate.toFixed(1)}%
          </p>
          <p>{metrics.totalRecovered} of {metrics.totalChurned} recovered</p>
        </div>

        <div className="metric-card">
          <h3>Revenue Recovered</h3>
          <p className="metric-value">${metrics.revenueRecovered.toLocaleString()}</p>
        </div>
      </div>

      <h3>Recovery by Stage</h3>
      <table>
        <thead>
          <tr>
            <th>Stage</th>
            <th>Total</th>
            <th>Recovered</th>
            <th>Rate</th>
          </tr>
        </thead>
        <tbody>
          {metrics.byStage.map(stage => (
            <tr key={stage.stage}>
              <td>{stage.stage}</td>
              <td>{stage.total}</td>
              <td>{stage.recovered}</td>
              <td className={getRateColor(stage.rate)}>{stage.rate.toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Open-Source Tools

- **PostgreSQL** — Churn event storage and analytical queries
- **Metabase** (Apache 2.0) — Churn analytics dashboards
- **BullMQ** — Scheduled churn analysis jobs
- **Redis** — Real-time churn rate caching
- **OpenTelemetry** — Churn event tracing and alerting
- **Apache ECharts** (Apache 2.0) — Churn visualization charts

## Integration Points

Involuntary churn monitoring integrates with the dunning system (event data), subscription management (cancellation events), payment gateway (failure reasons), CRM (customer segments), and analytics (reporting dashboards).

## Production Considerations

- Track churn cause with sufficient granularity for actionable insights
- Set up alerts for unusual churn rate spikes
- Segment analysis by plan tier, acquisition channel, and customer lifetime value
- Monitor recovery rate trends weekly
- Correlate churn with product changes or pricing updates
- Calculate churn cost including recovery campaign expenses
- Build predictive models to identify at-risk customers before churn
- Share churn insights with product and customer success teams

## Open-Source First Philosophy

PostgreSQL stores the complete churn event data model for deep analytical queries. Metabase provides self-serve dashboards for the finance and customer success teams to monitor involuntary churn in real time. BullMQ schedules regular churn analysis jobs. ECharts renders churn trend visualizations. This stack replaces proprietary analytics platforms like ChartMogul or Baremetrics while providing full control over churn metrics definitions and data.
