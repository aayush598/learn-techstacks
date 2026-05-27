# Section 08: Regression Trend Analysis

## Overview

Regression trend analysis tracks how agent behavior quality changes over time, identifying patterns in regression occurrences, severity, and root causes. Trend data helps teams understand whether quality is improving or degrading, which types of changes most commonly introduce regressions, and where testing investments should be focused.

Trends are visualized on dashboards showing regression rates over time, breakdowns by severity, common root causes, and time-to-detection. The analysis system automatically generates weekly quality reports with recommendations for improvement.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class RegressionTrendAnalyzer {
  async analyze(period: { start: Date; end: Date }): Promise<TrendReport> {
    const events = await this.loadRegressionEvents(period);
    
    return {
      period,
      summary: {
        totalRegressions: events.length,
        criticalCount: events.filter(e => e.severity === 'critical').length,
        highCount: events.filter(e => e.severity === 'high').length,
        mediumCount: events.filter(e => e.severity === 'medium').length,
      },
      trends: {
        dailyRate: this.calculateDailyRate(events),
        weekOverWeek: this.calculateWoW(events),
        monthOverMonth: this.calculateMoM(events),
      },
      breakdowns: {
        byAgent: this.breakdownBy(events, 'agentId'),
        byFlow: this.breakdownBy(events, 'flowName'),
        byChangeType: this.breakdownBy(events, 'changeType'),
        byTeam: this.breakdownBy(events, 'team'),
      },
      topCauses: this.identifyTopCauses(events),
      recommendations: this.generateRecommendations(events),
    };
  }

  private calculateDailyRate(events: RegressionEvent[]): TimeSeriesPoint[] {
    const daily: Map<string, number> = new Map();
    
    for (const event of events) {
      const date = event.createdAt.toISOString().split('T')[0];
      daily.set(date, (daily.get(date) || 0) + 1);
    }
    
    return Array.from(daily.entries()).map(([date, count]) => ({
      date: new Date(date),
      value: count,
    }));
  }

  private identifyTopCauses(events: RegressionEvent[]): CauseAnalysis[] {
    const causeCounts: Map<string, { count: number; severity: string[] }> = new Map();
    
    for (const event of events) {
      const cause = event.rootCause || 'unknown';
      const existing = causeCounts.get(cause) || { count: 0, severity: [] };
      existing.count++;
      existing.severity.push(event.severity);
      causeCounts.set(cause, existing);
    }
    
    return Array.from(causeCounts.entries())
      .map(([cause, data]) => ({
        cause,
        count: data.count,
        percentage: data.count / events.length * 100,
        severities: this.severityDistribution(data.severity),
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
  }

  private generateRecommendations(events: RegressionEvent[]): string[] {
    const recs: string[] = [];
    const causes = this.identifyTopCauses(events);
    
    if (causes.find(c => c.cause === 'prompt_change')) {
      recs.push('Increase prompt change review requirements');
    }
    if (causes.find(c => c.cause === 'knowledge_base_update')) {
      recs.push('Add automated KB update validation tests');
    }
    if (this.calculateDailyRate(events).length > 10) {
      recs.push('Regression rate exceeds target; schedule quality review');
    }
    
    return recs;
  }
}
```

## Integration Points

- **Dashboard**: Trend visualizations in Grafana
- **Reporting**: Weekly automated quality reports
- **Alerting**: Unusual trends trigger investigations
- **Planning**: Trend data informs testing investment decisions
- **Performance Reviews**: Used in team performance evaluations

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Data Quality**: Trend accuracy depends on complete data collection
- **Lagging Indicators**: Regression events are lagging; combine with leading indicators
- **Context Matters**: Raw regression counts need context (code change volume)
- **Actionability**: Trends should drive specific improvement actions
- **Stakeholder Communication**: Tailor trend reports to different audiences
