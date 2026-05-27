# Real-Time Monitoring

## Overview

Real-time activity monitoring provides a streaming feed of user actions, enables anomaly detection on live events, triggers suspicious activity alerts, and supports webhook-based notifications for security team integration.

## Streaming Feed

```typescript
class RealTimeMonitorService {
  async streamActivity(tenantId: string, callback: (event: ActivityEvent) => void): Promise<() => void> {
    const stream = await this.eventBus.subscribe(`activity:${tenantId}`);

    const handler = (event: ActivityEvent) => {
      callback(event);
    };

    stream.on('message', handler);
    return () => stream.off('message', handler);
  }

  async processEvent(event: ActivityEvent): Promise<void> {
    // Publish to tenant-specific channel
    await this.eventBus.publish(`activity:${event.context.tenantId}`, event);

    // Run anomaly detection
    const anomalies = await this.anomalyDetector.analyze(event);
    if (anomalies.length > 0) {
      await this.handleAnomalies(event, anomalies);
    }
  }
}
```

## Anomaly Detection on Live Events

```typescript
class LiveAnomalyDetector {
  async analyze(event: ActivityEvent): Promise<Anomaly[]> {
    const anomalies: Anomaly[] = [];

    // Rapid successive failures
    if (event.severity === 'error') {
      const recentFailures = await this.getRecentEvents(event.context.tenantId, {
        action: event.action,
        actorId: event.actor.id,
        since: new Date(Date.now() - 300000), // 5 min
      });

      if (recentFailures.length >= 10) {
        anomalies.push({
          type: 'rapid_failures',
          severity: 'high',
          message: `User ${event.actor.email} has ${recentFailures.length} recent failures`,
          event,
        });
      }
    }

    // Bulk delete operations
    if (event.action.endsWith('.deleted')) {
      const recentDeletes = await this.getRecentEvents(event.context.tenantId, {
        action: event.action,
        since: new Date(Date.now() - 60000),
      });

      if (recentDeletes.length >= 50) {
        anomalies.push({
          type: 'bulk_delete',
          severity: 'critical',
          message: `Bulk delete detected: ${recentDeletes.length} ${event.target.type} deleted in 1 minute`,
          event,
        });
      }
    }

    // Off-hours admin actions
    if (event.context.source === 'admin') {
      const hour = new Date().getHours();
      if (hour < 6 || hour > 22) {
        anomalies.push({
          type: 'off_hours_admin',
          severity: 'medium',
          message: `Admin action during off-hours: ${event.action} by ${event.actor.email}`,
          event,
        });
      }
    }

    return anomalies;
  }
}
```

## Alert Webhooks

```typescript
class AlertWebhookService {
  async sendAlert(anomaly: Anomaly): Promise<void> {
    const payload = {
      id: generateId('alert'),
      timestamp: new Date().toISOString(),
      type: anomaly.type,
      severity: anomaly.severity,
      message: anomaly.message,
      event: {
        action: anomaly.event.action,
        actor: anomaly.event.actor.email || anomaly.event.actor.id,
        target: `${anomaly.event.target.type}:${anomaly.event.target.id}`,
        timestamp: anomaly.event.timestamp,
      },
      _links: {
        investigate: `${APP_URL}/admin/audit?eventId=${anomaly.event.id}`,
      },
    };

    // Send to configured webhooks
    const webhooks = await this.db.find('alert_webhooks', {
      tenantId: anomaly.event.context.tenantId,
      enabled: true,
      minSeverity: anomaly.severity,
    });

    for (const wh of webhooks) {
      await this.webhookService.deliver(wh.url, payload, wh.secret);
    }
  }
}
```

## Dashboard

```
Real-Time Activity Monitor
┌─────────────────────────────────────────────────────────────┐
│  🟢 2,345 events/min    ⚠ 3 anomalies    🚨 1 critical    │
├─────────────────────────────────────────────────────────────┤
│  Live Feed                                                  │
│  14:32:15  [API] campaign.created by alice@co               │
│  14:32:14  [APP] call.ended by bob@co (dur: 3:22)          │
│  14:32:12  [API] ⚠ agent.delete x50 in 60s (BULK_DELETE)   │
│  14:32:10  [ADM] 🚨 role.modified - admin escalation        │
│  14:32:08  [APP] login.success by charlie@co (new device)   │
│  ...                                                        │
│                                                            │
│  [⏸ Pause]  [🔍 Filter]  [📊 Analytics]                    │
└─────────────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **Redis Pub/Sub** — Real-time event streaming
- **WebSocket** (ws) — Browser real-time feed
- **Server-Sent Events** — Lightweight streaming alternative

## Production Considerations

- Stream events at tenant level only (no cross-tenant data leakage)
- Sample high-volume events (1% for non-critical actions)
- Rate-limit webhook delivery: max 10 per minute per tenant
- Anomaly detection runs with <100ms latency
- Dashboard auto-refresh with 2-second polling
- Filter events by source, severity, action type
- Alert fatigue prevention: max 5 alerts per tenant per minute
- Archive real-time feed for replay and investigation
