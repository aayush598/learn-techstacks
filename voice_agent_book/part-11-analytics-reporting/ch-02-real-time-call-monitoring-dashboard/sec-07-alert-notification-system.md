# Section 07: Alert and Notification System

## Overview

The alert and notification system proactively notifies supervisors and operators when metric thresholds are breached or anomalous patterns are detected in the call center. Alerts are triggered by configurable rules — for example, "alert when queue depth exceeds 50 for more than 2 minutes" or "alert when average sentiment drops below -0.3 in the last 5 minutes." Notifications are delivered through multiple channels: in-dashboard toast and banner alerts, email, Slack/Teams webhooks, SMS (for critical alerts), and push notifications via the WebSocket connection.

Each alert has a severity level (info, warning, critical), a lifecycle (firing → acknowledged → resolved), and an escalation policy (if not acknowledged within 5 minutes, notify the next tier). The alert engine evaluates rules against the real-time metric stream every 30 seconds, using a sliding window approach to avoid flapping (alert → clear → alert oscillation). Alert history is stored in ClickHouse for trend analysis and compliance reporting.

## Architecture

```
               Alert and Notification System

   Metrics Stream → Alert Engine (30s evaluation)
                         |
          ┌──────────────┼──────────────┐
          |              |              |
    In-App Toast    Email/Slack     SMS/Push
    (WebSocket)     (SMTP/Webhook)  (Twilio/FCM)
          |              |              |
    Alert History (ClickHouse)
          |
    Escalation Manager
          |
    Alert Rules Config (PostgreSQL)
```

## Design Decisions

- **Rule-based alerting over ML-based anomaly detection initially:** Rule-based alerts (thresholds, rate-of-change, duration) are simpler to implement, easier for operators to understand, and require no training data. ML-based anomaly detection is added in a later phase for detecting subtle patterns (e.g., gradual degradation in sentiment that would not trigger a threshold rule). Trade-off: rule-based alerts only catch known conditions; they cannot detect novel anomalies without manual rule creation.

- **Sliding window evaluation with cooldown over point-in-time evaluation:** A rule like "queue depth > 50" evaluated every 30 seconds would continuously re-fire if the condition persists. Instead, the alert engine evaluates over a sliding window (e.g., "queue depth > 50 for at least 2 consecutive minutes"). Once fired, the alert enters a cooldown period (configurable, default 5 minutes) during which re-evaluation is suppressed. This prevents alert fatigue. Trade-off: the cooldown period may delay notification of a second distinct incident that occurs within the cooldown window.

- **Multi-channel delivery with channel routing rules over uniform delivery:** Not all alerts need to wake someone up at 3 AM. The system supports channel routing rules: info alerts go to in-app notifications only, warning alerts go to in-app + email with 15-minute digest, critical alerts go to in-app + email + Slack + SMS with immediate delivery, and P1 (system-down) alerts additionally trigger a phone call via Twilio Voice. Each user configures their own notification preferences. Trade-off: multi-channel delivery increases integration complexity and cost (SMS, phone calls), but ensures critical alerts reach the right person.

## Implementation Approach

```typescript
interface AlertRule {
  id: string;
  name: string;
  description: string;
  tenantId: string;
  enabled: boolean;
  severity: 'info' | 'warning' | 'critical' | 'p1';
  metricKey: string;
  condition: {
    operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq' | 'rate_increase' | 'rate_decrease';
    value: number;
    windowSeconds: number;     // evaluation window
    durationSeconds: number;   // how long condition must persist
  };
  notification: {
    channels: ('in_app' | 'email' | 'slack' | 'sms' | 'phone')[];
    escalationDelay: number;   // seconds before escalating
    escalationTargets: string[]; // user IDs or roles
  };
  cooldownSeconds: number;
  createdAt: number;
  updatedAt: number;
}

interface AlertInstance {
  id: string;
  ruleId: string;
  severity: string;
  status: 'firing' | 'acknowledged' | 'resolved' | 'escalated';
  triggeredAt: number;
  acknowledgedAt?: number;
  acknowledgedBy?: string;
  resolvedAt?: number;
  resolvedBy?: string;
  value: number;
  threshold: number;
  message: string;
}

class AlertEngine {
  private rules: Map<string, AlertRule[]> = new Map();
  private alertHistory: ClickHouseClient;

  async evaluate(tenantId: string, metrics: Map<string, number>): Promise<void> {
    const tenantRules = this.rules.get(tenantId) ?? [];

    for (const rule of tenantRules) {
      if (!rule.enabled) continue;

      const currentValue = metrics.get(rule.metricKey);
      if (currentValue == null) continue;

      const isBreached = this.evaluateCondition(currentValue, rule.condition);

      if (isBreached) {
        const firing = await this.checkCurrentlyFiring(rule.id);
        if (!firing) {
          await this.fireAlert(rule, currentValue);
        }
      } else {
        const firing = await this.checkCurrentlyFiring(rule.id);
        if (firing) {
          await this.resolveAlert(rule.id);
        }
      }
    }
  }

  private evaluateCondition(
    value: number,
    condition: AlertRule['condition']
  ): boolean {
    switch (condition.operator) {
      case 'gt': return value > condition.value;
      case 'lt': return value < condition.value;
      case 'gte': return value >= condition.value;
      case 'lte': return value <= condition.value;
      case 'eq': return value === condition.value;
      case 'rate_increase':
        // Value represents % increase over window
        return value >= condition.value;
      case 'rate_decrease':
        return value <= -condition.value;
      default: return false;
    }
  }

  private async fireAlert(rule: AlertRule, value: number): Promise<void> {
    const alert: AlertInstance = {
      id: generateId(),
      ruleId: rule.id,
      severity: rule.severity,
      status: 'firing',
      triggeredAt: Date.now(),
      value,
      threshold: rule.condition.value,
      message: `${rule.name}: ${rule.metricKey} is ${value} (threshold: ${rule.condition.value})`,
    };

    // Store alert instance
    await this.alertHistory.insert('alerts', alert);

    // Route notification
    await this.notify(alert, rule.notification);
  }

  private async notify(alert: AlertInstance, config: AlertRule['notification']): Promise<void> {
    const channelPromises = config.channels.map(channel => {
      switch (channel) {
        case 'in_app':
          return this.broadcastWebSocket(alert);
        case 'email':
          return this.sendEmail(alert, config.escalationTargets);
        case 'slack':
          return this.sendSlackWebhook(alert);
        case 'sms':
          return this.sendSms(alert, config.escalationTargets);
        case 'phone':
          return this.makePhoneCall(alert, config.escalationTargets);
        default:
          return Promise.resolve();
      }
    });

    await Promise.allSettled(channelPromises);
  }

  private async sendSlackWebhook(alert: AlertInstance): Promise<void> {
    const color = alert.severity === 'critical' ? '#FF0000'
      : alert.severity === 'warning' ? '#FFA500'
      : '#3498DB';

    await fetch(process.env.SLACK_WEBHOOK_URL!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        attachments: [{
          color,
          title: `[${alert.severity.toUpperCase()}] ${alert.message}`,
          fields: [
            { title: 'Value', value: alert.value.toString(), short: true },
            { title: 'Threshold', value: alert.threshold.toString(), short: true },
            { title: 'Triggered', value: new Date(alert.triggeredAt).toISOString(), short: true },
          ],
          actions: [
            { type: 'button', text: 'Acknowledge', url: `${APP_URL}/alerts/${alert.id}/acknowledge` },
            { type: 'button', text: 'View Dashboard', url: `${APP_URL}/dashboard` },
          ],
        }],
      }),
    });
  }
}

// Escalation manager
class EscalationManager {
  private timers: Map<string, NodeJS.Timeout> = new Map();

  async startEscalation(alert: AlertInstance, rule: AlertRule): Promise<void> {
    const timer = setTimeout(async () => {
      const currentAlert = await this.getAlertStatus(alert.id);
      if (currentAlert?.status === 'firing') {
        // Escalate to next tier
        await this.escalate(alert, rule);
      }
    }, rule.notification.escalationDelay * 1000);

    this.timers.set(alert.id, timer);
  }

  async acknowledge(alertId: string, userId: string): Promise<void> {
    const timer = this.timers.get(alertId);
    if (timer) {
      clearTimeout(timer);
      this.timers.delete(alertId);
    }
    // Update alert status
    await this.updateAlert(alertId, { status: 'acknowledged', acknowledgedBy: userId, acknowledgedAt: Date.now() });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Alert history storage |
| Slack Webhook API | Service | Slack notification delivery |
| Twilio (SIP) | Service | SMS and voice call alerts |
| Nodemailer (MIT) | Server | Email notification delivery |

## Production Considerations

**Scaling:** The alert engine evaluates rules in batches per tenant every 30 seconds, processing all rules in a single ClickHouse query. For tenants with 500+ rules, partition evaluation across worker processes using Redis locks to prevent duplicate evaluation. Alert instances are time-series data — use ClickHouse TTL to auto-delete alerts older than 90 days (or keep forever for compliance).

**Security:** Alert rules are tenant-scoped — a user can only create/manage rules for their own tenant. The Slack webhook URL is stored encrypted at rest and decrypted only when sending notifications. SMS and phone call notifications use Twilio Verify to ensure phone numbers are opted in. Alert history access is logged and auditable — all acknowledge/resolve actions record the user ID and timestamp.

**Monitoring:** Track alert firing rate per rule, mean time to acknowledge (MTTA), mean time to resolve (MTTR), and notification delivery success rate per channel. Alert if any critical alert is not acknowledged within 5 minutes. Monitor the alert engine's evaluation latency — if it exceeds 60 seconds, consider splitting evaluation into smaller batches. Send a weekly digest to supervisors summarizing the alert volume, top-triggered rules, and MTTA/MTTR trends.
