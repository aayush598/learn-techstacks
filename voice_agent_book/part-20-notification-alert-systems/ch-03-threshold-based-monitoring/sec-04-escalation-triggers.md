# Section 04: Escalation Triggers

## Overview

Escalation triggers define what happens when a breach isn't addressed within SLA. Escalation chains specify sequential or parallel notifications to increasingly senior responders. Time-based escalation escalates after configured duration, and severity-based escalation promotes alert severity.

## Implementation Approach

```typescript
interface EscalationPolicy {
  id: string;
  name: string;
  rules: EscalationRule[];
  defaultTarget: RouteTarget;
}

interface EscalationRule {
  level: number;
  afterMinutes: number;
  target: RouteTarget;
  notifyMethod: 'sequential' | 'parallel';
  promoteSeverity?: boolean;
}

class EscalationEngine {
  private activeEscalations: Map<string, ActiveEscalation> = new Map();

  async startEscalation(alert: Alert, policy: EscalationPolicy): Promise<void> {
    const escalation: ActiveEscalation = {
      alertId: alert.id,
      policyId: policy.id,
      currentLevel: 0,
      startedAt: new Date().toISOString(),
      timer: this.scheduleNextLevel(alert, policy, 0),
    };
    this.activeEscalations.set(alert.id, escalation);
    await this.notifyLevel(alert, policy.rules[0]);
  }

  private scheduleNextLevel(alert: Alert, policy: EscalationPolicy, level: number): NodeJS.Timeout {
    if (level >= policy.rules.length) return null as unknown as NodeJS.Timeout;

    const rule = policy.rules[level];
    return setTimeout(async () => {
      const escalation = this.activeEscalations.get(alert.id);
      if (!escalation || alert.status === 'resolved') return;

      // Check if alert was acknowledged
      if (alert.status === 'acknowledged') return;

      // Escalate
      if (rule.promoteSeverity) {
        await this.alertService.updateSeverity(alert.id, 'critical');
      }

      await this.notifyLevel(alert, rule);
      escalation.currentLevel = level + 1;
      escalation.timer = this.scheduleNextLevel(alert, policy, level + 1);
    }, rule.afterMinutes * 60 * 1000);
  }

  private async notifyLevel(alert: Alert, rule: EscalationRule): Promise<void> {
    if (rule.notifyMethod === 'parallel') {
      const targets = await this.resolveParallelTargets(rule.target);
      await Promise.all(targets.map(t => this.notificationService.send(alert, t)));
    } else {
      await this.notificationService.send(alert, rule.target);
    }

    await this.auditLogger.log({
      event: 'escalation',
      alertId: alert.id,
      level: rule.level,
      target: rule.target,
      timestamp: new Date().toISOString(),
    });
  }

  async cancelEscalation(alertId: string): Promise<void> {
    const escalation = this.activeEscalations.get(alertId);
    if (escalation) {
      clearTimeout(escalation.timer);
      this.activeEscalations.delete(alertId);
    }
  }

  private async resolveParallelTargets(target: RouteTarget): Promise<RouteTarget[]> {
    // For 'team' targets, notify all members
    if (target.type === 'team') {
      const team = await this.teamService.getTeam(target.id);
      return team.members.map(m => ({ type: 'user', id: m, channel: target.channel }));
    }
    return [target];
  }
}
```

## Integration Points

- **Alert Lifecycle**: Escalation starts on alert creation, cancels on ack/resolve
- **Notification Service**: Sends escalation notifications
- **Audit Trail**: Escalation events logged for compliance

## Production Considerations

- **Escalation Fatigue**: Too many escalations desensitize responders
- **Override**: Allow manual escalation or de-escalation
- **Alert Dependencies**: Prevent escalation if dependent alert is already escalated
