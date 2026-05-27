# Section 05: Delivery Monitoring & Analytics

## Overview

Email delivery monitoring tracks every email through its lifecycle: sent, delivered, opened, clicked, bounced, and complained. Analytics dashboards show delivery rates, engagement metrics, and trends over time. Alerting detects delivery issues like high bounce rates or low open rates.

## Implementation Approach

```typescript
interface EmailDeliveryEvent {
  messageId: string;
  event: 'sent' | 'delivered' | 'opened' | 'clicked' | 'bounced' | 'complained' | 'dropped';
  timestamp: string;
  recipient: string;
  metadata: {
    campaignId?: string;
    templateId?: string;
    tags?: Record<string, string>;
  };
  details?: {
    bounceType?: 'permanent' | 'transient';
    bounceCategory?: string;
    error?: string;
    userAgent?: string;
    ipAddress?: string;
    linkUrl?: string;
  };
}

class DeliveryAnalytics {
  async getCampaignStats(campaignId: string): Promise<CampaignStats> {
    const events = await this.eventStore.query({ 'metadata.campaignId': campaignId });
    return this.computeStats(events);
  }

  async getTimeSeries(period: TimeRange, granularity: string): Promise<TimeSeriesData> {
    const events = await this.eventStore.query({
      timestamp: { $gte: period.start, $lte: period.end },
    });
    return this.aggregateByTime(events, granularity);
  }

  private computeStats(events: EmailDeliveryEvent[]): CampaignStats {
    const counts = {
      sent: events.filter(e => e.event === 'sent').length,
      delivered: events.filter(e => e.event === 'delivered').length,
      opened: events.filter(e => e.event === 'opened').length,
      clicked: events.filter(e => e.event === 'clicked').length,
      bounced: events.filter(e => e.event === 'bounced').length,
      complained: events.filter(e => e.event === 'complained').length,
    };

    // Deduplicate: count unique messages, not events
    const uniqueMessages = new Set(events.map(e => e.messageId));

    return {
      totalSent: counts.sent,
      deliveryRate: counts.delivered / (counts.sent || 1),
      openRate: counts.opened / (counts.delivered || 1),
      clickRate: counts.clicked / (counts.opened || 1),
      bounceRate: counts.bounced / (counts.sent || 1),
      complaintRate: counts.complained / (counts.delivered || 1),
      uniqueOpens: counts.opened,
      uniqueClicks: counts.clicked,
    };
  }

  async detectDeliveryIssues(): Promise<DeliveryAlert[]> {
    const alerts: DeliveryAlert[] = [];
    const recentStats = await this.getTimeSeries(
      { start: new Date(Date.now() - 3600000).toISOString(), end: new Date().toISOString() },
      '1h'
    );

    if (recentStats.bounceRate > 0.05) {
      alerts.push({ type: 'high_bounce', severity: 'critical', rate: recentStats.bounceRate });
    }
    if (recentStats.complaintRate > 0.001) {
      alerts.push({ type: 'high_complaint', severity: 'critical', rate: recentStats.complaintRate });
    }
    if (recentStats.deliveryRate < 0.95) {
      alerts.push({ type: 'low_delivery', severity: 'major', rate: recentStats.deliveryRate });
    }

    return alerts;
  }

  private aggregateByTime(events: EmailDeliveryEvent[], granularity: string): TimeSeriesData {
    const buckets = new Map<string, { sent: number; delivered: number; opened: number }>();
    for (const event of events) {
      const key = this.getTimeBucket(event.timestamp, granularity);
      const bucket = buckets.get(key) || { sent: 0, delivered: 0, opened: 0 };
      bucket[event.event]++;
      if (bucket[event.event] !== undefined) bucket[event.event]++;
      buckets.set(key, bucket);
    }
    return { granularity, buckets: Array.from(buckets.entries()).map(([time, counts]) => ({ time, ...counts })) };
  }
}
```

## Integration Points

- **Webhook Endpoints**: Provider sends delivery events
- **Analytics Dashboard**: Visualize delivery metrics
- **Alert Engine**: Delivery health alerts

## Production Considerations

- **Event Deduplication**: Providers may send duplicate webhooks
- **Data Volume**: High-volume email generates large event streams
- **Privacy**: Open/click tracking requires user consent
