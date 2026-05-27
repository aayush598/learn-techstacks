# Section 07: Alert Correlation & Grouping

## Overview

Alert correlation groups related alerts to reduce noise and identify root causes. Correlation strategies include: time-window (alerts within N minutes), metric-dependency (alerts on related metrics), topology-based (alerts from dependent services), and cause-effect (one alert likely caused others). Grouped alerts surface as a single incident.

## Implementation Approach

```typescript
interface AlertGroup {
  id: string;
  name: string;
  rootAlert?: string;
  alerts: Alert[];
  severity: string;
  status: 'open' | 'investigating' | 'resolved';
  correlationType: string;
  createdAt: string;
  metadata: Record<string, unknown>;
}

class AlertCorrelationEngine {
  private correlationStrategies: CorrelationStrategy[] = [
    new TimeWindowStrategy(300), // 5 minute window
    new MetricDependencyStrategy(),
    new TopologyStrategy(),
  ];

  async process(newAlert: Alert): Promise<CorrelationResult> {
    const candidates = await this.findCorrelationCandidates(newAlert);

    for (const strategy of this.correlationStrategies) {
      const correlated = await strategy.correlate(newAlert, candidates);
      if (correlated) {
        return this.handleCorrelation(newAlert, correlated, strategy.name);
      }
    }

    return { action: 'new_group', alert: newAlert };
  }

  private async findCorrelationCandidates(alert: Alert): Promise<Alert[]> {
    return this.alertStore.query({
      status: { $in: ['firing', 'acknowledged'] },
      tenantId: alert.tenantId,
      createdAt: { $gte: this.getTimeWindowStart(alert.createdAt) },
    });
  }

  private async handleCorrelation(alert: Alert, group: AlertGroup, strategy: string): Promise<CorrelationResult> {
    group.alerts.push(alert);
    group.severity = this.getHighestSeverity(group.alerts);
    await this.alertStore.updateGroup(group);

    // Determine root cause
    if (this.isLikelyRootCause(alert, group, strategy)) {
      group.rootAlert = alert.id;
      await this.alertStore.updateGroup(group);
    }

    return { action: 'grouped', group, alert, strategy };
  }

  private isLikelyRootCause(alert: Alert, group: AlertGroup, strategy: string): boolean {
    // Root cause is typically the earliest alert in the group
    const sorted = [...group.alerts].sort((a, b) =>
      new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
    );
    return sorted[0].id === alert.id;
  }
}

class TimeWindowStrategy implements CorrelationStrategy {
  constructor(private window: number) {}

  async correlate(alert: Alert, candidates: Alert[]): Promise<AlertGroup | null> {
    const matching = candidates.filter(c =>
      Math.abs(new Date(c.createdAt).getTime() - new Date(alert.createdAt).getTime()) < this.window * 1000
    );
    if (matching.length === 0) return null;
    return this.findOrCreateGroup(matching);
  }
}
```

## Integration Points

- **Incident Management**: Correlated groups create incidents
- **Dashboard**: Grouped alerts shown as single incident
- **Monitoring**: Correlation rate tracked

## Production Considerations

- **Over-Correlation**: Grouping unrelated alerts creates confusion
- **Under-Correlation**: Missing relationships increases noise
- **Strategy Tuning**: Correlation windows need adjustment per environment
