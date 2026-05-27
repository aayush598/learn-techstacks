# Section 03: Alert Generation & Lifecycle

## Overview

Alerts progress through a defined lifecycle: created → firing → acknowledged → resolved. The lifecycle manager handles state transitions, deduplication, and status updates. Each alert maintains its state in a persistent store, and state changes trigger appropriate notifications.

## Implementation Approach

```typescript
type AlertStatus = 'firing' | 'acknowledged' | 'resolved' | 'closed';

interface Alert {
  id: string;
  ruleId: string;
  tenantId: string;
  status: AlertStatus;
  severity: string;
  title: string;
  message: string;
  events: RichEvent[];
  createdAt: string;
  acknowledgedAt?: string;
  acknowledgedBy?: string;
  resolvedAt?: string;
  resolvedBy?: string;
  metadata: Record<string, unknown>;
}

class AlertLifecycleManager {
  async createAlert(evaluation: RuleEvaluation): Promise<Alert> {
    const existing = await this.findActiveAlert(evaluation.ruleId);
    if (existing) {
      return this.updateExistingAlert(existing, evaluation);
    }

    const alert: Alert = {
      id: generateId(),
      ruleId: evaluation.ruleId,
      tenantId: evaluation.event.tenantId,
      status: 'firing',
      severity: evaluation.severity,
      title: this.generateTitle(evaluation),
      message: this.generateMessage(evaluation),
      events: [evaluation.event],
      createdAt: new Date().toISOString(),
      metadata: evaluation.event.metadata,
    };

    await this.storage.save(alert);
    await this.emitAlertEvent('alert.created', alert);
    return alert;
  }

  async acknowledge(alertId: string, userId: string): Promise<Alert> {
    const alert = await this.storage.get(alertId);
    if (alert.status !== 'firing') throw new InvalidTransitionError(alert.status, 'acknowledged');

    alert.status = 'acknowledged';
    alert.acknowledgedAt = new Date().toISOString();
    alert.acknowledgedBy = userId;

    await this.storage.update(alert);
    await this.emitAlertEvent('alert.acknowledged', alert);
    return alert;
  }

  async resolve(alertId: string, userId: string): Promise<Alert> {
    const alert = await this.storage.get(alertId);
    if (alert.status === 'resolved') return alert;

    alert.status = 'resolved';
    alert.resolvedAt = new Date().toISOString();
    alert.resolvedBy = userId;

    await this.storage.update(alert);
    await this.emitAlertEvent('alert.resolved', alert);
    return alert;
  }

  private async findActiveAlert(ruleId: string): Promise<Alert | null> {
    return this.storage.findOne({
      ruleId,
      status: { $in: ['firing', 'acknowledged'] },
    });
  }

  private async emitAlertEvent(eventType: string, alert: Alert): Promise<void> {
    await this.eventBus.publish({
      id: generateId(),
      topic: 'alert_events',
      type: eventType,
      payload: alert,
      metadata: { tenantId: alert.tenantId, source: 'alert_lifecycle' },
    });
  }
}
```

## Integration Points

- **Event Bus**: Alert lifecycle events published for downstream consumers
- **Notification Trigger**: Alert creation triggers notification dispatch
- **Dashboard**: Active alerts displayed in operations dashboard

## Production Considerations

- **Concurrent Updates**: Use optimistic locking for alert state changes
- **Auto-Resolve**: Automatically resolve alerts when condition clears
- **Archival**: Move resolved alerts to cold storage after 30 days
