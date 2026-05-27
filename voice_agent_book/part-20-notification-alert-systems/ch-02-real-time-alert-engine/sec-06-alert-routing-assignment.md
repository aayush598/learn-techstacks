# Section 06: Alert Routing & Assignment

## Overview

Alert routing ensures alerts reach the right team or individual. Routing rules consider alert type, severity, tenant, time of day, and team schedules. Assignment strategies include round-robin, skills-based, load-balanced, and manual assignment. The router integrates with the on-call schedule for direct assignment.

## Implementation Approach

```typescript
interface RoutingRule {
  id: string;
  priority: number;
  conditions: RouteCondition[];
  target: RouteTarget;
  fallback: RouteTarget;
}

interface RouteTarget {
  type: 'team' | 'user' | 'schedule' | 'webhook';
  id: string;
  channel: string;
}

class AlertRouter {
  async route(alert: Alert): Promise<RouteResult> {
    const rules = await this.getRoutingRules(alert.tenantId);
    const sorted = rules.sort((a, b) => a.priority - b.priority);

    for (const rule of sorted) {
      if (this.matchesConditions(rule.conditions, alert)) {
        const target = await this.resolveTarget(rule.target, alert);
        if (target) return { alert, target, rule };
      }
    }

    // Fallback to default
    return this.routeToFallback(alert);
  }

  private matchesConditions(conditions: RouteCondition[], alert: Alert): boolean {
    return conditions.every(c => {
      switch (c.field) {
        case 'severity': return c.values.includes(alert.severity);
        case 'tenantId': return c.values.includes(alert.tenantId);
        case 'ruleId': return c.values.includes(alert.ruleId);
        case 'timeOfDay': {
          const hour = new Date().getHours();
          if (c.operator === 'between') return hour >= c.values[0] && hour <= c.values[1];
          return true;
        }
        default: return true;
      }
    });
  }

  private async resolveTarget(target: RouteTarget, alert: Alert): Promise<ResolvedTarget | null> {
    switch (target.type) {
      case 'user':
        return { userId: target.id, channels: this.getUserChannels(target.id) };
      case 'team':
        return this.assignToTeam(target.id, alert);
      case 'schedule':
        return this.assignFromSchedule(target.id, alert);
      case 'webhook':
        return { webhookUrl: target.id, channels: [] };
      default:
        return null;
    }
  }

  private async assignToTeam(teamId: string, alert: Alert): Promise<ResolvedTarget> {
    const team = await this.teamService.getTeam(teamId);
    const assignee = this.roundRobinAssignment(team.members, alert);
    return { userId: assignee, channels: ['slack', 'email'] };
  }

  private roundRobinAssignment(members: string[], alert: Alert): string {
    const lastIndex = this.assignmentStore.getLastAssignee(alert.tenantId);
    const nextIndex = (lastIndex + 1) % members.length;
    this.assignmentStore.setLastAssignee(alert.tenantId, nextIndex);
    return members[nextIndex];
  }
}
```

## Integration Points

- **On-Call Schedule**: Routes alerts to on-call engineer
- **Team Service**: Team membership and skills database
- **Assignment Store**: Tracks last assignee for round-robin

## Production Considerations

- **Fallback Chain**: Ensure fallback targets exist for every routing rule
- **Skills Matching**: Route complex alerts to senior engineers
- **Load Balancing**: Prevent alert fatigue by distributing fairly
