# Section 05: Alert Severity Levels

## Overview

Alert severity classification determines response urgency and notification channel. Levels include: Critical (immediate response, P0), Major (urgent response, P1), Minor (same-day response, P2), Warning (awareness, P3). Dynamic severity adjusts based on context, and escalation rules define what happens when severity thresholds are crossed.

## Implementation Approach

```typescript
type SeverityLevel = 'critical' | 'major' | 'minor' | 'warning';

interface SeverityConfig {
  level: SeverityLevel;
  responseSLA: number; // minutes
  notificationChannels: string[];
  autoEscalate: boolean;
  escalateAfter: number; // minutes
  escalateTo: SeverityLevel;
}

class SeverityClassifier {
  private severityConfigs: Record<SeverityLevel, SeverityConfig> = {
    critical: { level: 'critical', responseSLA: 15, notificationChannels: ['sms', 'phone', 'slack'], autoEscalate: true, escalateAfter: 30, escalateTo: 'critical' },
    major: { level: 'major', responseSLA: 60, notificationChannels: ['slack', 'email'], autoEscalate: true, escalateAfter: 45, escalateTo: 'critical' },
    minor: { level: 'minor', responseSLA: 480, notificationChannels: ['email'], autoEscalate: false, escalateAfter: 0, escalateTo: 'major' },
    warning: { level: 'warning', responseSLA: 1440, notificationChannels: ['dashboard'], autoEscalate: false, escalateAfter: 0, escalateTo: 'minor' },
  };

  async classify(event: EnrichedEvent, rule: AlertRule): Promise<SeverityLevel> {
    let severity = rule.severity;

    // Dynamic severity adjustment
    if (rule.severity === 'major' || rule.severity === 'minor') {
      const dynamicFactors = await this.evaluateDynamicFactors(event);
      if (dynamicFactors.affectedUsers > 100) severity = this.escalate(severity);
      if (dynamicFactors.revenueImpact > 1000) severity = this.escalate(severity);
      if (dynamicFactors.timeSinceLastIncident < 3600) severity = this.escalate(severity);
    }

    return severity;
  }

  private async evaluateDynamicFactors(event: EnrichedEvent): Promise<DynamicFactors> {
    const [affectedUsers, revenueImpact, lastIncident] = await Promise.all([
      this.getAffectedUsers(event),
      this.getRevenueImpact(event),
      this.getTimeSinceLastIncident(event),
    ]);
    return { affectedUsers, revenueImpact, timeSinceLastIncident: lastIncident };
  }

  private escalate(severity: SeverityLevel): SeverityLevel {
    const escalationMap: Record<SeverityLevel, SeverityLevel> = {
      warning: 'minor',
      minor: 'major',
      major: 'critical',
      critical: 'critical',
    };
    return escalationMap[severity];
  }

  getSeverityConfig(severity: SeverityLevel): SeverityConfig {
    return this.severityConfigs[severity];
  }
}
```

## Integration Points

- **Notification Routing**: Severity determines which channels to notify
- **Escalation Engine**: Time-based escalation triggers on SLA breach
- **Dashboard**: Active alerts grouped by severity

## Production Considerations

- **Severity Drift**: Monitor severity distribution; too many critical alerts indicate tuning needed
- **Dynamic Factors**: Regularly review and adjust dynamic severity rules
- **SLA Compliance**: Track response time per severity level
