# Section 07: Notification Logging & Audit Trail

## Overview

Comprehensive logging captures every notification event throughout its lifecycle: creation, queuing, delivery attempt, success, failure, and user interaction (read/click). The audit trail provides immutable records for compliance, debugging, and analytics. Delivery analytics power reporting on notification effectiveness.

## Implementation Approach

```typescript
interface NotificationLog {
  id: string;
  notificationId: string;
  event: 'created' | 'queued' | 'delivery_attempt' | 'delivered' | 'failed' | 'read' | 'clicked';
  timestamp: string;
  channel: string;
  tenantId: string;
  userId: string;
  metadata: Record<string, unknown>;
  error?: string;
}

interface DeliveryAnalytics {
  totalSent: number;
  delivered: number;
  failed: number;
  deliveryRate: number;
  avgDeliveryLatency: number;
  readRate: number;
  clickRate: number;
  channelBreakdown: ChannelStats[];
}

class NotificationAuditLogger {
  private eventStore: EventStore;

  async log(event: NotificationLog): Promise<void> {
    await this.eventStore.append(event);
    await this.updateAnalytics(event);
  }

  async getNotificationTimeline(notificationId: string): Promise<NotificationLog[]> {
    return this.eventStore.query({ notificationId }, { sort: 'timestamp' });
  }

  async getDeliveryAnalytics(period: TimeRange, tenantId: string): Promise<DeliveryAnalytics> {
    const events = await this.eventStore.query({
      tenantId,
      timestamp: { $gte: period.start, $lte: period.end },
    });
    return this.computeAnalytics(events);
  }

  private computeAnalytics(events: NotificationLog[]): DeliveryAnalytics {
    const sent = events.filter(e => e.event === 'created').length;
    const delivered = events.filter(e => e.event === 'delivered').length;
    const reads = events.filter(e => e.event === 'read').length;
    const clicks = events.filter(e => e.event === 'clicked').length;

    return {
      totalSent: sent,
      delivered,
      failed: events.filter(e => e.event === 'failed').length,
      deliveryRate: sent > 0 ? delivered / sent : 0,
      avgDeliveryLatency: this.computeAvgLatency(events),
      readRate: delivered > 0 ? reads / delivered : 0,
      clickRate: delivered > 0 ? clicks / delivered : 0,
      channelBreakdown: this.computeChannelStats(events),
    };
  }

  private computeAvgLatency(events: NotificationLog[]): number {
    const deliveries = events.filter(e => e.event === 'delivered');
    if (deliveries.length === 0) return 0;
    const latencies = deliveries.map(d => {
      const created = events.find(e => e.notificationId === d.notificationId && e.event === 'created');
      return created ? new Date(d.timestamp).getTime() - new Date(created.timestamp).getTime() : 0;
    });
    return latencies.reduce((a, b) => a + b, 0) / latencies.length;
  }
}
```

## Integration Points

- **Event Store**: PostgreSQL or TimescaleDB for time-series audit logs
- **Analytics API**: Endpoints for dashboard queries
- **Export**: CSV/JSON export for compliance reporting

## Production Considerations

- **Retention Policy**: Keep raw logs for 90 days, aggregated stats indefinitely
- **Storage Volume**: High-volume notifications generate significant log data
- **Indexing**: Index on tenantId + timestamp for efficient queries
