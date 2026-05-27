# Section 04: Acknowledgment Tracking

## Overview

Acknowledgment tracking monitors when responders acknowledge alerts. Timely acknowledgment prevents escalation. The system tracks acknowledgment timeout, escalates on no-acknowledgment, provides acknowledgment proofs (timestamp, user, method), and maintains an audit trail.

## Implementation Approach

```typescript
interface Acknowledgment {
  id: string;
  alertId: string;
  userId: string;
  method: 'slack' | 'sms' | 'web' | 'api' | 'phone';
  timestamp: string;
  ipAddress?: string;
  userAgent?: string;
  note?: string;
}

interface AckConfig {
  timeout: number; // minutes
  requireNote: boolean;
  autoAckOnView: boolean;
  allowedMethods: string[];
}

class AcknowledgmentTracker {
  async acknowledge(alertId: string, userId: string, method: string, options?: AckOptions): Promise<Acknowledgment> {
    const ack: Acknowledgment = {
      id: generateId(),
      alertId,
      userId,
      method: method as Acknowledgment['method'],
      timestamp: new Date().toISOString(),
      ipAddress: options?.ipAddress,
      userAgent: options?.userAgent,
      note: options?.note,
    };

    await this.storage.save(ack);
    await this.alertService.updateStatus(alertId, 'acknowledged');
    await this.cancelEscalation(alertId);
    await this.notifyTeam(alertId, userId);

    return ack;
  }

  async checkTimeout(alert: Alert, config: AckConfig): Promise<TimeoutResult> {
    const elapsed = (Date.now() - new Date(alert.createdAt).getTime()) / 60000;
    const isAcknowledged = await this.isAcknowledged(alert.id);

    if (!isAcknowledged && elapsed > config.timeout) {
      return { timeout: true, elapsed };
    }

    return { timeout: false, elapsed };
  }

  async isAcknowledged(alertId: string): Promise<boolean> {
    const acks = await this.storage.query({ alertId });
    return acks.length > 0;
  }

  async getAcknowledgmentHistory(alertId: string): Promise<Acknowledgment[]> {
    return this.storage.query({ alertId }, { sort: { timestamp: -1 } });
  }

  async getAcknowledgmentMetrics(period: TimeRange): Promise<AckMetrics> {
    const acknowledgments = await this.storage.query({
      timestamp: { $gte: period.start, $lte: period.end },
    });

    const alerts = await this.alertService.query({
      createdAt: { $gte: period.start, $lte: period.end },
    });

    const ackByMethod = this.groupBy(acknowledgments, 'method');
    const ackTimeDistribution = this.computeAckTimeDistribution(alerts, acknowledgments);

    return {
      totalAcknowledged: acknowledgments.length,
      totalAlerts: alerts.length,
      ackRate: alerts.length > 0 ? acknowledgments.length / alerts.length : 0,
      avgAckTime: ackTimeDistribution.average,
      medianAckTime: ackTimeDistribution.median,
      ackByMethod: Object.fromEntries(
        Object.entries(ackByMethod).map(([method, acks]) => [method, acks.length])
      ),
      slaBreachCount: ackTimeDistribution.slaBreaches,
    };
  }

  private computeAckTimeDistribution(alerts: Alert[], acks: Acknowledgment[]): AckTimeDistribution {
    const ackTimes: number[] = alerts
      .filter(a => acks.some(ack => ack.alertId === a.id))
      .map(a => {
        const firstAck = acks.find(ack => ack.alertId === a.id)!;
        return (new Date(firstAck.timestamp).getTime() - new Date(a.createdAt).getTime()) / 60000;
      });

    if (ackTimes.length === 0) return { average: 0, median: 0, slaBreaches: 0 };

    const sorted = [...ackTimes].sort((a, b) => a - b);
    return {
      average: ackTimes.reduce((a, b) => a + b, 0) / ackTimes.length,
      median: sorted[Math.floor(sorted.length / 2)],
      slaBreaches: ackTimes.filter(t => t > 15).length, // >15 min SLA breach
    };
  }

  private async cancelEscalation(alertId: string): Promise<void> {
    await this.escalationService.cancel(alertId);
  }

  private async notifyTeam(alertId: string, userId: string): Promise<void> {
    const alert = await this.alertService.get(alertId);
    await this.notificationService.send({
      type: 'alert_acknowledged',
      alertId,
      acknowledgedBy: userId,
      channels: alert.notificationChannels,
    });
  }
}
```

## Integration Points

- **Alert Service**: Updates alert status on acknowledgment
- **Escalation Service**: Cancels pending escalations
- **Notification Service**: Notifies team of acknowledgment

## Production Considerations

- **Auto-Acknowledge**: Allow auto-ack on viewing alert details
- **Note Requirement**: Require resolution notes for critical alerts
- **Acknowledgment Proofs**: Timestamp and method stored for compliance
