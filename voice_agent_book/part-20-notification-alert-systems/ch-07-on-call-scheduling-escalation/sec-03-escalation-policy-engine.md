# Section 03: Escalation Policy Engine

## Overview

The escalation policy engine defines what happens when alerts are not acknowledged within SLA. Policies define escalation chains with time-based triggers, multi-level escalation, and parallel notification. Each level notifies a different target (team, manager, executive) with increasing urgency.

## Implementation Approach

```typescript
interface EscalationPolicy {
  id: string;
  name: string;
  rules: EscalationRule[];
  defaultAction: 'escalate' | 'auto_resolve' | 'page_emergency';
  maxLevels: number;
}

interface EscalationRule {
  level: number;
  name: string;
  afterMinutes: number;
  target: EscalationTarget;
  notifyMethod: 'sequential' | 'parallel';
  promoteSeverityTo?: string;
  requireAck: boolean;
}

interface EscalationTarget {
  type: 'user' | 'team' | 'schedule' | 'webhook' | 'email_list';
  id: string;
  channels: string[];
  messageTemplate?: string;
}

class EscalationEngine {
  async evaluate(alert: Alert, policy: EscalationPolicy): Promise<EscalationResult> {
    const elapsed = (Date.now() - new Date(alert.createdAt).getTime()) / 60000;
    const currentLevel = this.findCurrentLevel(policy, elapsed);
    const target = this.resolveTarget(policy.rules[currentLevel]);

    return {
      shouldEscalate: currentLevel > 0,
      level: currentLevel,
      target,
      action: policy.rules[currentLevel]?.notifyMethod || 'sequential',
      promoteSeverity: policy.rules[currentLevel]?.promoteSeverityTo,
    };
  }

  private findCurrentLevel(policy: EscalationPolicy, elapsedMinutes: number): number {
    for (let i = policy.rules.length - 1; i >= 0; i--) {
      if (elapsedMinutes >= policy.rules[i].afterMinutes) {
        return i;
      }
    }
    return 0;
  }

  private async resolveTarget(rule: EscalationRule | undefined): Promise<ResolvedTarget[]> {
    if (!rule) return [];

    switch (rule.target.type) {
      case 'user':
        return [{ userId: rule.target.id, channels: rule.target.channels }];
      case 'team': {
        const team = await this.teamService.getTeam(rule.target.id);
        return team.members.map(m => ({ userId: m, channels: rule.target.channels }));
      }
      case 'schedule': {
        const onCall = await this.onCallService.getCurrentOnCall(rule.target.id);
        return [{ userId: onCall.userId, channels: rule.target.channels }];
      }
      case 'webhook':
        return [{ webhookUrl: rule.target.id, channels: rule.target.channels }];
      default:
        return [];
    }
  }

  async execute(alert: Alert, policy: EscalationPolicy): Promise<void> {
    const escalation = await this.evaluate(alert, policy);
    if (!escalation.shouldEscalate) return;

    // Mark escalation attempt
    await this.alertService.addEscalation(alert.id, {
      level: escalation.level,
      timestamp: new Date().toISOString(),
      target: escalation.target,
    });

    // Promote severity if configured
    if (escalation.promoteSeverity) {
      await this.alertService.updateSeverity(alert.id, escalation.promoteSeverity);
    }

    // Notify targets
    if (escalation.action === 'parallel') {
      await Promise.all(escalation.target.map(t =>
        this.notificationService.send(alert, t, { urgent: true })
      ));
    } else {
      for (const target of escalation.target) {
        await this.notificationService.send(alert, target);
      }
    }

    // Schedule next level check
    if (policy.rules.length > escalation.level + 1) {
      const nextRule = policy.rules[escalation.level + 1];
      setTimeout(() => this.execute(alert, policy), (nextRule.afterMinutes - this.findCurrentLevel(policy, 0)) * 60000);
    }
  }

  async cancelEscalation(alertId: string): Promise<void> {
    // Cancel scheduled escalations
    await this.escalationScheduler.cancel(alertId);
  }
}
```

## Integration Points

- **Alert Service**: Updates alert severity and tracks escalation history
- **On-Call Service**: Resolves on-call targets
- **Notification Service**: Delivers escalation notifications

## Production Considerations

- **Escalation Fatigue**: Limit escalation levels to prevent over-notification
- **Override**: Allow manual escalation override
- **Audit Trail**: Log all escalation events for compliance
