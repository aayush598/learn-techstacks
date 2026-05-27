# Section 03: Delivery Guarantees

## Overview

Notification delivery guarantees ensure messages are delivered reliably. Three delivery semantics exist: at-most-once (best effort), at-least-once (guaranteed delivery with potential duplicates), and exactly-once (guaranteed delivery without duplicates). The system implements at-least-once delivery with idempotency for exactly-once semantics. Delivery receipts confirm successful delivery.

## Implementation Approach

```typescript
interface DeliveryReceipt {
  notificationId: string;
  channelId: string;
  status: 'pending' | 'delivered' | 'failed' | 'read';
  deliveredAt?: string;
  error?: string;
  attemptCount: number;
}

class DeliveryManager {
  async sendWithGuarantee(notification: Notification, channel: NotificationChannel): Promise<DeliveryResult> {
    const delivery = await this.createDeliveryRecord(notification, channel);

    while (delivery.attemptCount < this.config.maxDeliveryAttempts) {
      try {
        const result = await channel.send(notification.payload);
        if (result.success) {
          await this.markDelivered(delivery, result);
          return result;
        }
      } catch (error) {
        await this.logFailure(delivery, error);
      }

      delivery.attemptCount++;
      if (delivery.attemptCount < this.config.maxDeliveryAttempts) {
        await this.backoff(delivery.attemptCount);
      }
    }

    await this.sendToDeadLetter(delivery);
    throw new Error('Max delivery attempts exceeded');
  }

  private async createDeliveryRecord(notification: Notification, channel: NotificationChannel): Promise<DeliveryRecord> {
    // Deduplication check
    const existing = await this.findDuplicate(notification.idempotencyKey);
    if (existing) throw new DuplicateDeliveryError(existing);
    // Create record
    return this.storage.create({
      notificationId: notification.id,
      channelId: channel.id,
      status: 'pending',
      attemptCount: 0,
      createdAt: new Date().toISOString(),
    });
  }

  private async findDuplicate(idempotencyKey: string): Promise<DeliveryRecord | null> {
    return this.storage.findOne({ idempotencyKey, status: 'delivered' });
  }

  private async backoff(attempt: number): Promise<void> {
    const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 1000, 30000);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

## Integration Points

- **Dead Letter Queue**: Failed deliveries stored for manual retry
- **Delivery Receipts**: Callbacks from channels confirm delivery
- **Retry Queue**: Scheduled retries for failed deliveries

## Production Considerations

- **Duplicate Handling**: Idempotency keys prevent duplicate processing
- **Delivery Windows**: Time-limited delivery attempts
- **Storage Backend**: PostgreSQL or Redis for delivery state
