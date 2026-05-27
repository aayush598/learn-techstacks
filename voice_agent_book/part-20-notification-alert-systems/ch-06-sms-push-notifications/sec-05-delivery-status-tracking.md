# Section 05: Delivery Status Tracking

## Overview

Delivery status tracking monitors notifications from send to delivery confirmation. Each channel provides delivery receipts, and the system aggregates status across channels. Status transitions include: pending, sent, delivered, read, failed. Retry logic handles transient failures.

## Implementation Approach

```typescript
type DeliveryStatus = 'pending' | 'queued' | 'sent' | 'delivered' | 'read' | 'clicked' | 'failed' | 'expired';

interface DeliveryRecord {
  notificationId: string;
  channel: string;
  status: DeliveryStatus;
  attempts: DeliveryAttempt[];
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, unknown>;
}

interface DeliveryAttempt {
  timestamp: string;
  status: DeliveryStatus;
  error?: string;
  providerResponse?: Record<string, unknown>;
}

class DeliveryTracker {
  async trackDelivery(notificationId: string, channel: string, initialStatus: DeliveryStatus): Promise<DeliveryRecord> {
    const record: DeliveryRecord = {
      notificationId,
      channel,
      status: initialStatus,
      attempts: [{ timestamp: new Date().toISOString(), status: initialStatus }],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      metadata: {},
    };
    await this.storage.save(record);
    return record;
  }

  async updateStatus(notificationId: string, channel: string, status: DeliveryStatus, metadata?: Record<string, unknown>): Promise<void> {
    const record = await this.storage.findOne({ notificationId, channel });
    if (!record) throw new Error('Delivery record not found');

    record.status = status;
    record.updatedAt = new Date().toISOString();
    record.attempts.push({ timestamp: record.updatedAt, status, ...metadata });
    if (metadata) Object.assign(record.metadata, metadata);

    await this.storage.update(record);
    await this.emitStatusEvent(record);
  }

  async getDeliveryStatus(notificationId: string): Promise<AggregatedStatus> {
    const records = await this.storage.query({ notificationId });
    return {
      notificationId,
      overall: this.getOverallStatus(records),
      channelStatuses: records.map(r => ({ channel: r.channel, status: r.status })),
      deliveredToAny: records.some(r => ['delivered', 'read', 'clicked'].includes(r.status)),
      allFailed: records.every(r => r.status === 'failed'),
      lastAttempt: Math.max(...records.flatMap(r => r.attempts.map(a => new Date(a.timestamp).getTime()))),
    };
  }

  private getOverallStatus(records: DeliveryRecord[]): DeliveryStatus {
    if (records.some(r => r.status === 'clicked')) return 'clicked';
    if (records.some(r => r.status === 'read')) return 'read';
    if (records.some(r => r.status === 'delivered')) return 'delivered';
    if (records.some(r => r.status === 'sent')) return 'sent';
    if (records.some(r => r.status === 'failed')) return 'failed';
    if (records.some(r => r.status === 'pending')) return 'pending';
    return 'queued';
  }

  async retryFailed(notificationId: string, channel: string): Promise<void> {
    const record = await this.storage.findOne({ notificationId, channel });
    if (!record || record.status !== 'failed') throw new Error('Cannot retry non-failed delivery');

    const attemptCount = record.attempts.length;
    if (attemptCount >= this.config.maxRetries) throw new Error('Max retries exceeded');

    await this.retryQueue.enqueue({ notificationId, channel, attempt: attemptCount + 1 });
  }

  private async emitStatusEvent(record: DeliveryRecord): Promise<void> {
    await this.eventBus.publish({
      topic: 'delivery_status',
      type: `delivery.${record.status}`,
      payload: record,
    });
  }
}
```

## Integration Points

- **Provider Webhooks**: Channel providers send status updates
- **Dashboard**: Real-time delivery status display
- **Retry Queue**: Automatic retry for transient failures

## Production Considerations

- **Status Consistency**: Handle out-of-order status updates
- **Timeout Detection**: Mark as failed after delivery timeout
- **Storage Cleanup**: Archive old delivery records
