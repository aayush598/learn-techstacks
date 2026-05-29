# Section 07: Rate Limiting Outgoing Webhooks

## Overview

Outgoing webhooks are rate-limited per endpoint to prevent overwhelming downstream services. The rate limiter uses a token bucket algorithm that respects endpoint capacity and supports batch delivery for high-throughput scenarios. Rate limit configuration is per-endpoint and adjustable by the customer.

## Architecture

```
Outgoing Webhook Rate Limiting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Per-Endpoint Token Bucket:
  ┌─────────────────────────────────────────┐
  │ Endpoint: https://customer.com/webhooks  │
  │ Capacity: 100 events                     │
  │ Refill Rate: 10 events/second            │
  │ Backpressure: queue overflow → DLQ       │
  └─────────────────────────────────────────┘

Flow:
  [Event Published] → [Rate Limiter] → [Queue] → [Delivery Worker]
                           │
                    [Bucket Check]
                    ├── Tokens available? → Consume 1 → Deliver
                    └── No tokens? → Queue until tokens refill

Batch Delivery (High Throughput):
  ┌──────────────────────────────────────────┐
  │ Batch Queue (max 10 events / 5 seconds)  │
  │                                          │
  │ When full OR timer expires:               │
  │   POST /webhooks                          │
  │   [                                        │
  │     { event 1 },                          │
  │     { event 2 },                          │
  │     ...                                   │
  │   ]                                        │
  └──────────────────────────────────────────┘

Queue Backpressure:
  Queue Depth > 1000 → Alert + Send to DLQ
  Queue Age > 1 hour → Alert + Send to DLQ
```

## Design Decisions

- **Token Bucket Per Endpoint**: Each endpoint has independent rate limits — one busy endpoint doesn't affect others
- **Configurable Limits**: Customers can adjust rate limits based on their infrastructure capacity
- **Backpressure Protection**: When queue exceeds thresholds, excess events go to DLQ rather than unbounded memory
- **Batch Delivery**: For high-volume endpoints, batch delivery reduces HTTP overhead and connection overhead

## Implementation Approach

```typescript
// Outgoing rate limiter configuration
interface OutgoingRateLimit {
  endpointId: string;
  capacity: number;      // Burst capacity
  refillRate: number;    // Tokens per second
  batchSize?: number;    // Max events per batch (0 = no batching)
  batchWindow?: number;  // Max wait time for batch (ms)
}

// Rate limiter for outgoing webhooks
class OutgoingWebhookRateLimiter {
  private buckets: Map<string, TokenBucket> = new Map();
  private batchQueues: Map<string, BatchQueue> = new Map();

  constructor(private redis: Redis) {}

  async check(endpointId: string): Promise<{ allowed: boolean; waitMs: number }> {
    const config = await this.getRateLimitConfig(endpointId);
    const bucket = await this.getBucket(endpointId, config);

    const result = await bucket.consume(1);
    return result;
  }

  async enqueue(endpointId: string, event: WebhookEventEnvelope): Promise<void> {
    const config = await this.getRateLimitConfig(endpointId);

    if (config.batchSize && config.batchSize > 1) {
      // Use batch queue
      return this.enqueueBatch(endpointId, event, config);
    }

    // Check rate limit
    const { allowed, waitMs } = await this.check(endpointId);

    if (allowed) {
      await this.deliverImmediately(endpointId, event);
    } else {
      // Schedule delivery after wait
      await this.scheduleDelayed(endpointId, event, waitMs);
    }
  }

  private async enqueueBatch(
    endpointId: string,
    event: WebhookEventEnvelope,
    config: OutgoingRateLimit,
  ): Promise<void> {
    if (!this.batchQueues.has(endpointId)) {
      const queue = new BatchQueue(endpointId, config.batchSize!, config.batchWindow || 5000);
      queue.onFlush(async (events) => {
        await this.deliverBatch(endpointId, events);
      });
      this.batchQueues.set(endpointId, queue);
    }

    this.batchQueues.get(endpointId)!.add(event);
  }

  private async deliverBatch(endpointId: string, events: WebhookEventEnvelope[]): Promise<void> {
    const config = await this.getRateLimitConfig(endpointId);

    // Check rate limit for batch
    const { allowed } = await this.check(endpointId);
    if (!allowed) {
      // Re-enqueue all events individually
      for (const event of events) {
        await this.enqueue(endpointId, event);
      }
      return;
    }

    // Deliver batch
    const endpoint = await this.endpointRepository.findById(endpointId);
    try {
      await fetch(endpoint.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-VoiceAgent-Batch': 'true',
          'X-VoiceAgent-Batch-Size': events.length.toString(),
        },
        body: JSON.stringify({ events }),
      });
    } catch (error) {
      // If batch fails, fall back to individual delivery
      for (const event of events) {
        await this.deliverWithRetry(endpointId, event);
      }
    }
  }

  private async getRateLimitConfig(endpointId: string): Promise<OutgoingRateLimit> {
    const cached = await this.redis.get(`ratelimit:config:${endpointId}`);
    if (cached) return JSON.parse(cached);

    const endpoint = await this.endpointRepository.findById(endpointId);
    const config: OutgoingRateLimit = {
      endpointId,
      capacity: endpoint.rateLimitCapacity || 100,
      refillRate: endpoint.rateLimitRefillRate || 10,
      batchSize: endpoint.batchSize || 0,
      batchWindow: endpoint.batchWindow || 5000,
    };

    await this.redis.setex(`ratelimit:config:${endpointId}`, 300, JSON.stringify(config));
    return config;
  }
}

// Batch queue implementation
class BatchQueue {
  private buffer: WebhookEventEnvelope[] = [];
  private timer: NodeJS.Timeout | null = null;
  private onFlushCallback: (events: WebhookEventEnvelope[]) => Promise<void>;

  constructor(
    private endpointId: string,
    private batchSize: number,
    private batchWindow: number,
  ) {}

  add(event: WebhookEventEnvelope): void {
    this.buffer.push(event);

    if (this.buffer.length >= this.batchSize) {
      this.flush();
    } else if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.batchWindow);
    }
  }

  onFlush(callback: (events: WebhookEventEnvelope[]) => Promise<void>): void {
    this.onFlushCallback = callback;
  }

  private async flush(): Promise<void> {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }

    if (this.buffer.length === 0) return;

    const events = [...this.buffer];
    this.buffer = [];

    try {
      await this.onFlushCallback(events);
    } catch (error) {
      console.error(`Batch delivery failed for ${this.endpointId}:`, error);
    }
  }
}
```

## Integration Points

- **Endpoint Configuration**: Rate limit settings in endpoint creation/edit UI
- **Queue Management**: BullMQ for delayed delivery scheduling
- **Monitoring**: Track queue depth, delivery latency, and rate limit hit rate per endpoint

## Production Considerations

- **Queue Depth Limits**: Maximum 10,000 queued events per endpoint before triggering DLQ
- **Batch Fallback**: If batch delivery fails, fall back to individual delivery with rate limiting
- **Dynamic Rate Adjustment**: Monitor endpoint response times and auto-advertise rate limits
- **Fairness**: Tenant-level rate limit ensures one tenant's high volume doesn't starve others

## Open-Source Tools

- **BullMQ**: Queue management for scheduled deliveries with rate limiting
- **Redis**: Token bucket state for distributed rate limiting
