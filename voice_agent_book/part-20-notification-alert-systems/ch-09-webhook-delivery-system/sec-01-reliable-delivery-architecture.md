# Section 01: Reliable Delivery Architecture

## Overview

The webhook delivery system reliably delivers event notifications to consumer endpoints. Events are queued, processed by delivery workers, and retried on failure. Idempotency keys prevent duplicate processing, and delivery ordering guarantees are provided per event type.

## Architecture

```
Webhook Delivery Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Event Source] → [Webhook Queue] → [Delivery Worker] → [Consumer Endpoint]
      │                 │                   │                  │
  System events     BullMQ/Redis       HTTP POST with      User's server
  Alert events     Persistent queue    retry logic          Accepts webhook
  Agent events     Ordered by type     + signature          Returns 200 OK
  Custom events                        + idempotency key
                                             │
                                    [On Failure]
                                         │
                                   ┌──────┴──────┐
                                   │              │
                              Retry with      Dead Letter
                              exponential     Queue (DLQ)
                              backoff         Manual retry
                                              via dashboard

Delivery Guarantees:
  - At-least-once delivery (may retry)
  - Ordered per event type + endpoint
  - 24-hour delivery window
  - 5s timeout per attempt
```

## Design Decisions

- **Queue-Based Architecture**: Decouples event production from delivery
- **Redis-Backed Queue**: BullMQ for persistence and reliability
- **Idempotency Keys**: Consumer uses key to detect duplicates
- **Ordered Delivery**: Per-endpoint sequential delivery for consistency

## Implementation Approach

```typescript
interface WebhookEvent {
  id: string;
  type: string;
  payload: Record<string, unknown>;
  idempotencyKey: string;
  timestamp: string;
  tenantId: string;
}

interface DeliveryAttempt {
  eventId: string;
  endpointId: string;
  attemptNumber: number;
  status: 'success' | 'failed' | 'retrying';
  statusCode?: number;
  error?: string;
  durationMs: number;
  timestamp: Date;
}

class WebhookDeliveryService {
  private queue: BullQueue;
  private maxRetries = 5;

  async enqueue(event: WebhookEvent, endpoints: WebhookEndpoint[]): Promise<void> {
    const jobs = endpoints.map(endpoint => ({
      name: 'deliver-webhook',
      data: { event, endpoint },
      opts: {
        attempts: this.maxRetries,
        backoff: { type: 'exponential', delay: 1000 },
        removeOnComplete: false,
        removeOnFail: false,
      },
    }));

    await this.queue.addBulk(jobs);
  }

  async processDelivery(job: BullJob): Promise<void> {
    const { event, endpoint } = job.data;
    const startTime = Date.now();

    try {
      const signature = this.signPayload(event, endpoint.secret);
      const headers = {
        'Content-Type': 'application/json',
        'X-Webhook-ID': event.id,
        'X-Webhook-Signature': signature,
        'X-Idempotency-Key': event.idempotencyKey,
        'X-Delivery-Attempt': job.attemptsMade + 1,
      };

      const response = await fetch(endpoint.url, {
        method: 'POST',
        headers,
        body: JSON.stringify(event),
        signal: AbortSignal.timeout(5000),
      });

      if (response.status >= 200 && response.status < 300) {
        await this.recordSuccess(event, endpoint, Date.now() - startTime);
        return;
      }

      throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    } catch (error) {
      await this.recordFailure(event, endpoint, error, Date.now() - startTime);

      if (job.attemptsMade >= this.maxRetries - 1) {
        await this.moveToDeadLetter(event, endpoint, error);
      }

      throw error; // BullMQ handles retry
    }
  }

  private signPayload(event: WebhookEvent, secret: string): string {
    const hmac = crypto.createHmac('sha256', secret);
    hmac.update(JSON.stringify(event));
    return hmac.digest('hex');
  }

  private async moveToDeadLetter(event: WebhookEvent, endpoint: WebhookEndpoint, error: Error): Promise<void> {
    await this.db.insert('webhook_dead_letter', {
      eventId: event.id,
      endpointId: endpoint.id,
      payload: event,
      error: error.message,
      failedAt: new Date(),
      retryCount: this.maxRetries,
    });
  }

  async retryDeadLetter(dlqId: string): Promise<void> {
    const entry = await this.db.findOne('webhook_dead_letter', { id: dlqId });
    if (!entry) throw new Error('DLQ entry not found');

    await this.enqueue(entry.payload, [entry.endpoint]);
    await this.db.update('webhook_dead_letter', { id: dlqId }, { status: 'retried' });
  }
}
```

## Integration Points

- **Event Bus**: Producers publish events to bus
- **Endpoint Registry**: Consumer endpoint configuration
- **Dashboard**: Webhook delivery logs and dead letter queue management

## Production Considerations

- **Queue Monitoring**: Alert on queue depth > 1000
- **Delivery Timeout**: 5 second HTTP timeout per attempt
- **DLQ Cleanup**: Auto-clean DLQ entries older than 30 days

## Open-Source Tools

- **BullMQ**: Redis-backed job queue
- **Node.js crypto**: HMAC signing for payload verification
