# Section 05: Regression Alert System

## Overview

The regression alert system automatically notifies teams when conversation behavior changes unexpectedly. Alerts are categorized by severity (critical, major, minor, warning) and routed to appropriate channels (Slack, PagerDuty, email). The alert system integrates with the CI pipeline to block deployments that introduce high-severity regressions.

Alert configuration is per-agent and per-flow, allowing teams to define what constitutes a critical regression for their specific use case. The system supports gradual rollout of alert rules, with the ability to tune sensitivity based on observed false positive rates.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class RegressionAlertSystem {
  async evaluate(regressionReport: RegressionReport): Promise<Alert[]> {
    const alerts: Alert[] = [];

    // Critical regressions
    const criticalRegressions = regressionReport.regressions.filter(
      r => r.severity === 'critical'
    );
    if (criticalRegressions.length > 0) {
      alerts.push({
        id: uuid(),
        type: 'regression',
        severity: 'critical',
        title: `${criticalRegressions.length} critical regression(s) in ${regressionReport.agentId}`,
        message: this.formatRegressionSummary(criticalRegressions),
        channels: ['slack-critical', 'pagerduty', 'email'],
        createdAt: new Date(),
        metadata: {
          agentId: regressionReport.agentId,
          baselineId: regressionReport.baselineId,
          commitSha: regressionReport.commitSha,
        },
      });
    }

    // High severity regressions
    const highRegressions = regressionReport.regressions.filter(
      r => r.severity === 'high'
    );
    if (highRegressions.length > 0) {
      alerts.push({
        ...baseAlert,
        severity: 'high',
        title: `${highRegressions.length} regression(s) detected`,
        channels: ['slack-alerts'],
      });
    }

    // Trend-based alerts
    const trendViolation = await this.checkTrendThresholds(regressionReport);
    if (trendViolation) {
      alerts.push({
        ...baseAlert,
        severity: 'warning',
        title: `Regression rate exceeded threshold: ${trendViolation.message}`,
      });
    }

    return alerts;
  }

  private async sendAlert(alert: Alert): Promise<void> {
    for (const channel of alert.channels) {
      switch (channel) {
        case 'slack-critical':
          await this.slack.send({
            channel: '#alerts-critical',
            blocks: this.buildSlackBlocks(alert, 'critical'),
          });
          break;
        case 'pagerduty':
          await this.pagerduty.trigger({
            severity: 'critical',
            summary: alert.title,
            source: 'regression-detector',
          });
          break;
        case 'email':
          await this.email.send({
            to: 'engineering@company.com',
            subject: `[CRITICAL] ${alert.title}`,
            body: alert.message,
          });
          break;
      }
    }
  }
}
```

## Integration Points

- **CI Pipeline**: Alerts block deployment on critical regressions
- **Slack/PagerDuty**: Real-time notifications
- **Dashboard**: Alert history displayed
- **Issue Tracker**: Critical regressions auto-create tickets
- **On-Call**: PagerDuty integration for after-hours alerts

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Alert Fatigue**: Too many alerts desensitize teams; tune thresholds carefully
- **False Positives**: Track false positive rate; auto-adjust thresholds
- **Escalation Path**: Ensure critical alerts always reach a human
- **Maintenance Windows**: Suppress alerts during known maintenance
- **Postmortem Integration**: Alerts link to postmortem templates
