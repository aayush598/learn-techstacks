# Section 08: Rate Limiting & Compliance

## Overview

Rate limiting ensures compliance with Slack and Teams API rate limits while maintaining reliable notification delivery. The rate limiter tracks API usage per workspace, implements token bucket algorithms, and queues messages when limits are reached. Compliance features include message retention policies and data archiving.

## Implementation Approach

```typescript
interface RateLimitConfig {
  platform: string;
  maxRequestsPerSecond: number;
  maxRequestsPerMinute: number;
  burstLimit: number;
  retryAfter: number; // seconds
}

class PlatformRateLimiter {
  private buckets: Map<string, TokenBucket> = new Map();
  private queues: Map<string, QueuedMessage[]> = new Map();

  constructor() {
    this.startQueueProcessor();
  }

  async sendWithRateLimit(platform: string, workspaceId: string, sendFn: () => Promise<void>): Promise<void> {
    const key = `${platform}:${workspaceId}`;
    const bucket = this.getOrCreateBucket(key);

    if (bucket.tryConsume()) {
      await sendFn();
    } else {
      return this.enqueue(key, sendFn);
    }
  }

  private getOrCreateBucket(key: string): TokenBucket {
    if (!this.buckets.has(key)) {
      this.buckets.set(key, new TokenBucket({
        capacity: 10,
        refillRate: 1,
        refillInterval: 100, // 1 token per 100ms
      }));
    }
    return this.buckets.get(key)!;
  }

  private async enqueue(key: string, sendFn: () => Promise<void>): Promise<void> {
    return new Promise((resolve, reject) => {
      const queue = this.queues.get(key) || [];
      queue.push({ sendFn, resolve, reject, queuedAt: Date.now() });
      this.queues.set(key, queue);
    });
  }

  private startQueueProcessor(): void {
    setInterval(() => {
      for (const [key, queue] of this.queues) {
        if (queue.length === 0) continue;
        const bucket = this.buckets.get(key);
        if (bucket?.tryConsume()) {
          const item = queue.shift()!;
          item.sendFn().then(item.resolve).catch(item.reject);
          this.queues.set(key, queue);
        }
      }
    }, 100);
  }
}

// Compliance: Data retention and archiving
class ComplianceManager {
  private retentionPolicies: Map<string, RetentionPolicy> = new Map();

  async archiveMessages(olderThan: Date): Promise<void> {
    const messages = await this.messageStore.query({
      sentAt: { $lt: olderThan.toISOString() },
      archived: false,
    });

    for (const message of messages) {
      await this.archiveService.archive(message);
      await this.messageStore.update(message.id, { archived: true });
    }
  }

  async purgeMessages(olderThan: Date): Promise<void> {
    const retention = this.retentionPolicies.get('default') || { maxAgeDays: 90 };
    const cutoff = new Date(Date.now() - retention.maxAgeDays * 24 * 3600 * 1000);
    await this.messageStore.deleteMany({ sentAt: { $lt: cutoff.toISOString() } });
  }
}
```

## Integration Points

- **Rate Limit Monitoring**: Track rate limit usage in dashboards
- **Retry Logic**: Automatic retry with backoff on rate limit errors
- **Compliance Reporting**: Archive exports for regulatory compliance

## Production Considerations

- **Slack Rate Limits**: 1 message per second per channel, ~50 per minute
- **Teams Rate Limits**: 30 requests per 10 seconds per app
- **Queue Growth**: Monitor queue depth; scale workers if needed
