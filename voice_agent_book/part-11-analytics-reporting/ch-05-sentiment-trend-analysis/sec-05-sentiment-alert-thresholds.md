# Section 05: Sentiment Alert Thresholds

## Overview

Sentiment alert thresholds enable proactive monitoring of customer sentiment by triggering notifications when sentiment metrics cross predefined boundaries. Alerts can be configured at multiple levels: per-call (a single call with extremely negative sentiment), per-agent (an agent's rolling average sentiment drops below threshold), per-campaign (campaign sentiment drops significantly), or per-tenant (overall tenant sentiment trend turns negative). Alert rules define the metric, threshold direction, evaluation window, cooldown period, and notification channels.

The alert engine evaluates sentiment metrics every 5 minutes against active rules. When triggered, alerts create an incident record, send notifications (in-app, email, Slack, SMS depending on severity), and optionally pause the agent or route future calls differently (for critical alerts like "agent showing consistently negative sentiment that may indicate burnout or hostile behavior"). Alert history is stored in ClickHouse for analysis and compliance.

## Architecture

```
           Sentiment Alert Engine

   Sentiment Pipeline → Metrics → Alert Evaluator (5min)
                                       |
                            Rule Config (PostgreSQL)
                                       |
                            ┌──────────┴──────────┐
                            |                     |
                      Alert Triggered        Cooldown Check
                            |                     |
                    Notification Router    Alert Instance Created
                     (Slack, Email,         (ClickHouse)
                      SMS, In-app)
```

## Design Decisions

- **Multi-window evaluation (5min, 30min, 4h) over single-window:** Different alert types need different lookback windows. A per-call alert ("negative sentiment detected") evaluates immediately on the current segment. An agent-level alert ("weekly sentiment decline") looks back 7 days. The engine supports configurable evaluation windows from 5 minutes to 30 days. Trade-off: multiple windows increase the evaluation complexity — each window requires a separate query or computation.

- **Threshold with hysteresis over single threshold:** A single threshold ("alert when sentiment < -0.5") causes alert flapping — the sentiment might dip to -0.51, trigger an alert, then return to -0.49 a minute later. Hysteresis uses two thresholds: a trigger threshold (-0.5) and a clear threshold (-0.3). The alert fires when sentiment crosses the trigger threshold and clears only when it returns above the clear threshold. Trade-off: hysteresis delays the resolution notification, which may keep supervisors monitoring a call that has already improved.

- **Severity-based escalation over uniform alert handling:** Alert rules have a severity level (info, warning, critical, P1). Info alerts go to the dashboard notification panel only. Warning alerts send email + in-app. Critical alerts send Slack + email + SMS. P1 alerts additionally trigger a phone call via Twilio Voice and page the on-call engineer. Escalation policies define the delay before escalating from one severity to the next. Trade-off: multi-severity escalation adds configuration complexity but prevents alert fatigue for low-severity issues.

## Implementation Approach

```typescript
interface SentimentAlertRule {
  id: string;
  tenantId: string;
  name: string;
  enabled: boolean;
  severity: 'info' | 'warning' | 'critical' | 'p1';
  level: 'call' | 'agent' | 'campaign' | 'tenant';
  targetId?: string;           // agentId, campaignId, or null for tenant
  metric: 'customer_sentiment' | 'agent_sentiment' | 'overall_sentiment' | 'sentiment_volatility';
  condition: {
    operator: 'lt' | 'gt' | 'lte' | 'gte';
    value: number;
    windowMinutes: number;
  };
  hysteresis: {
    triggerValue: number;
    clearValue: number;
  };
  cooldownMinutes: number;
  notification: {
    channels: ('in_app' | 'email' | 'slack' | 'sms')[];
    escalationDelayMinutes?: number;
    escalationSeverity?: string;
  };
  createdAt: number;
  updatedAt: number;
}

interface SentimentAlertInstance {
  id: string;
  ruleId: string;
  tenantId: string;
  severity: string;
  level: string;
  targetId?: string;
  status: 'firing' | 'acknowledged' | 'resolved';
  triggeredAt: number;
  resolvedAt?: number;
  currentValue: number;
  thresholdValue: number;
  callSid?: string;           // for call-level alerts
  message: string;
}

class SentimentAlertEngine {
  private rules: Map<string, SentimentAlertRule[]> = new Map();
  private firingAlerts: Map<string, SentimentAlertInstance> = new Map();
  private clickhouse: ClickHouseClient;
  private notificationService: NotificationService;

  async evaluate(tenantId: string): Promise<void> {
    const rules = this.rules.get(tenantId) ?? [];
    const now = Date.now();

    for (const rule of rules) {
      if (!rule.enabled) continue;

      const value = await this.getCurrentValue(tenantId, rule);
      if (value == null) continue;

      const existingAlert = this.firingAlerts.get(rule.id);

      if (!existingAlert) {
        // Check if we should fire
        if (this.shouldFire(value, rule)) {
          await this.fireAlert(rule, value, now);
        }
      } else {
        // Check if we should resolve
        if (this.shouldResolve(value, rule)) {
          await this.resolveAlert(existingAlert, now);
        } else if (this.shouldEscalate(existingAlert, rule, now)) {
          await this.escalateAlert(existingAlert, rule);
        }
      }
    }
  }

  private async getCurrentValue(
    tenantId: string,
    rule: SentimentAlertRule
  ): Promise<number | null> {
    const windowStart = Date.now() - rule.condition.windowMinutes * 60 * 1000;

    let query: string;

    switch (rule.level) {
      case 'call':
        // Get latest segment sentiment for a specific call
        if (!rule.targetId) return null;
        const sent = await this.getCallSentiment(rule.targetId);
        return sent?.score ?? null;

      case 'agent':
        // Average sentiment for agent in window
        query = `
          SELECT avg(customerSentiment) as val
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND agentId = '${rule.targetId}'
            AND timestamp >= ${windowStart}
        `;
        break;

      case 'campaign':
        query = `
          SELECT avg(customerSentiment) as val
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND campaignId = '${rule.targetId}'
            AND timestamp >= ${windowStart}
        `;
        break;

      case 'tenant':
        query = `
          SELECT avg(customerSentiment) as val
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND timestamp >= ${windowStart}
        `;
        break;

      default:
        return null;
    }

    const result = await this.clickhouse.query(query);
    return result[0]?.val ?? null;
  }

  private shouldFire(value: number, rule: SentimentAlertRule): boolean {
    if (rule.hysteresis) {
      return this.compare(value, rule.hysteresis.triggerValue, rule.condition.operator);
    }
    return this.compare(value, rule.condition.value, rule.condition.operator);
  }

  private shouldResolve(value: number, rule: SentimentAlertRule): boolean {
    if (rule.hysteresis) {
      // Resolve when value is back above clear threshold
      const clearOperator = rule.condition.operator === 'lt' ? 'gte' : 'lte';
      return this.compare(value, rule.hysteresis.clearValue, clearOperator);
    }
    // Without hysteresis, resolve when condition is no longer met
    return !this.shouldFire(value, rule);
  }

  private compare(value: number, threshold: number, operator: string): boolean {
    switch (operator) {
      case 'lt': return value < threshold;
      case 'gt': return value > threshold;
      case 'lte': return value <= threshold;
      case 'gte': return value >= threshold;
      default: return false;
    }
  }

  private async fireAlert(rule: SentimentAlertRule, value: number, now: number): Promise<void> {
    const alert: SentimentAlertInstance = {
      id: generateId(),
      ruleId: rule.id,
      tenantId: rule.tenantId,
      severity: rule.severity,
      level: rule.level,
      targetId: rule.targetId,
      status: 'firing',
      triggeredAt: now,
      currentValue: value,
      thresholdValue: rule.condition.value,
      message: this.formatAlertMessage(rule, value),
    };

    this.firingAlerts.set(rule.id, alert);
    await this.clickhouse.insert('sentiment_alerts', alert);

    // Send notifications
    for (const channel of rule.notification.channels) {
      await this.notificationService.send(channel, alert);
    }

    // Start escalation timer
    if (rule.notification.escalationDelayMinutes) {
      setTimeout(() => this.escalateIfNotAcknowledged(alert, rule), rule.notification.escalationDelayMinutes * 60 * 1000);
    }
  }

  private async resolveAlert(alert: SentimentAlertInstance, now: number): Promise<void> {
    alert.status = 'resolved';
    alert.resolvedAt = now;
    this.firingAlerts.delete(alert.ruleId);
    await this.clickhouse.query(
      `UPDATE sentiment_alerts SET status = 'resolved', resolvedAt = ${now} WHERE id = '${alert.id}'`
    );
  }

  private async escalateAlert(alert: SentimentAlertInstance, rule: SentimentAlertRule): Promise<void> {
    alert.severity = rule.notification.escalationSeverity ?? 'critical';
    alert.message = `[ESCALATED] ${alert.message}`;
    await this.clickhouse.query(
      `UPDATE sentiment_alerts SET severity = '${alert.severity}', message = '${alert.message}' WHERE id = '${alert.id}'`
    );

    // Send escalation notifications
    for (const channel of rule.notification.channels) {
      await this.notificationService.send(channel, alert);
    }
  }

  private shouldEscalate(alert: SentimentAlertInstance, rule: SentimentAlertRule, now: number): boolean {
    if (!rule.notification.escalationDelayMinutes) return false;
    if (alert.status !== 'firing') return false;
    const elapsedMinutes = (now - alert.triggeredAt) / (60 * 1000);
    return elapsedMinutes >= rule.notification.escalationDelayMinutes
      && alert.severity !== (rule.notification.escalationSeverity ?? 'critical');
  }

  private formatAlertMessage(rule: SentimentAlertRule, value: number): string {
    const targetLabel = rule.targetId ? ` for ${rule.targetId}` : '';
    const direction = rule.condition.operator === 'lt' ? 'below' : 'above';
    return `[${rule.severity.toUpperCase()}] ${rule.name}: ${rule.metric} is ${value.toFixed(3)} (${direction} threshold ${rule.condition.value})${targetLabel}`;
  }

  private async getCallSentiment(callSid: string): Promise<{ score: number; label: string } | null> {
    const result = await this.clickhouse.query(`
      SELECT overallScore, overallLabel
      FROM call_sentiment_analysis
      WHERE callSid = '${callSid}'
    `);
    if (result.length === 0) return null;
    return { score: result[0].overallScore, label: result[0].overallLabel };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Alert rule storage and evaluation |
| PostgreSQL (PostgreSQL) | Server | Alert rule configuration |
| Slack Webhook API | Service | Alert notifications |
| Nodemailer (MIT) | Server | Email alert delivery |

## Production Considerations

**Scaling:** The alert evaluator runs every 5 minutes per tenant. For 1000 tenants, this would be 200 evaluations/minute — each querying ClickHouse for the current metric value. Use a scheduling queue (BullMQ) to distribute evaluations across workers. Cache metric values for 30 seconds to prevent redundant queries when multiple rules share the same metric. Alert instances are time-series data — partition ClickHouse tables by month and set TTL to 90 days (compliance may require longer retention).

**Security:** Alert rules are tenant-scoped. Call-level alerts include the call SID and may trigger for any call — ensure notification channels (Slack, email) do not expose call content (transcription snippets should not be included in alert messages). Per-agent sentiment alerts require the `agent-performance:view` permission to configure. Alert history is sensitive — access requires `analytics:alerts` permission.

**Monitoring:** Track alert firing rate per rule, false positive rate (alerts that fire but are resolved without action), MTTA and MTTR for sentiment alerts, and alert notification delivery success rate. Alert if any rule fires more than 10 times per day (indicates threshold is too sensitive). Monitor sentiment alert engine CPU usage and ClickHouse query performance.
