# Section 05: Retry and Dead-Letter Queue

## Overview

The retry and dead-letter queue (DLQ) system handles webhook delivery failures with a robust, configurable retry mechanism that ensures events are eventually delivered or escalated for manual intervention. When a webhook delivery fails (network timeout, consumer 5xx, DNS resolution failure), the retry engine schedules redelivery with exponential backoff and jitter. After exhausting the maximum number of retry attempts, the event is moved to a dead-letter queue for administrative inspection and potential replay.

The retry system is critical for webhook reliability — external systems experience downtime, network partitions occur, deployments cause temporary unavailability. The retry engine ensures that events are not lost during these transient failures. The DLQ provides operational visibility into permanently failed deliveries, allowing admins to diagnose issues (consumer endpoint changed, authentication failure, payload parsing error), fix the problem, and replay the events.

## Architecture

```
               Retry & Dead-Letter Queue System

   Delivery Engine → Retry Scheduler → DLQ → Manual Replay
                        |
   +----------------------------------------------------------+
   |              Retry & DLQ Architecture                   |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Retry Decision   |  | Backoff Calculator|             |
   |  | • Error type     |  | • Exponential     |            |
   |  | • Network vs     |  | • Jitter          |            |
   |  |   application    |  | • Max cap (5min)  |            |
   |  | • 4xx vs 5xx     |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Retry Queue      |  | Dead-Letter Queue |             |
   |  | • Delayed jobs   |  | • Failed events   |            |
   |  | • Priority by    |  | • Error metadata  |            |
   |  |   retry count    |  | • TTL-based purge |            |
   |  | • Concurrency    |  +-------------------+            |
   |  |   limited        |  +-------------------+             |
   |  +------------------+  | DLQ Dashboard     |            |
   |                        | • Browse events    |            |
   |  +------------------+  | • Replay individual|           |
   |  | Retry Metrics    |  | • Replay batch     |            |
   |  | • Attempt dist   |  | • Purge old events |            |
   |  | • Recovery rate  |  +-------------------+            |
   |  | • DLQ growth     |                                    |
   |  +------------------+                                    |
   +----------------------------------------------------------+
```

## Design Decisions

- **Error classification for retry decisions over blanket retry:** Not all errors are retryable. The retry engine classifies errors into retryable (5xx, network timeout, DNS failure, connection refused) and non-retryable (4xx client errors, invalid SSL certificate, payload too large). 4xx errors indicate a consumer-side problem that retrying will not fix — these go directly to the DLQ. 5xx and network errors get retried. Trade-off: error classification requires maintaining error-type mappings but prevents wasted retries on configuration errors.

- **Secondary DLQ per endpoint over shared DLQ:** Each endpoint has its own DLQ partition (tagged by endpoint ID). This isolates failed events per consumer and enables per-endpoint DLQ management — replay all events for a specific endpoint without affecting other endpoints' DLQ events. The DLQ data structure supports browsing by event type, time range, and error type for operational efficiency. Trade-off: per-endpoint DLQ partitioning adds storage overhead but provides independent operational management.

- **Exponential backoff with max-cap and full jitter over fixed intervals:** Retry delays use the formula: `min(cap, base * 2^attempt) + random(0, min(cap, base * 2^attempt))`. Full jitter (randomizing up to the full computed backoff value) distributes retry times more evenly than the more common "jitter as an additive" approach. This prevents the thundering herd problem when an endpoint recovers. Trade-off: full jitter increases maximum delivery time for retried events but provides better load distribution on recovery.

## Implementation Approach

```
enum RetryDecision {
  RETRY = 'retry',
  DLQ = 'dlq',
  SKIP = 'skip',
}

class ErrorClassifier {
  static classify(error: DeliveryError): RetryDecision {
    if (error.type === 'http') {
      // HTTP status-based classification
      if (error.statusCode) {
        if (error.statusCode >= 500) return RetryDecision.RETRY;        // Server error
        if (error.statusCode === 429) return RetryDecision.RETRY;       // Rate limited
        if (error.statusCode >= 400 && error.statusCode < 500) {
          if (error.statusCode === 410) return RetryDecision.SKIP;      // Gone — remove endpoint
          return RetryDecision.DLQ;                                      // Client error — don't retry
        }
      }
    }

    if (error.type === 'network') {
      const retryableNetworkErrors = [
        'ETIMEDOUT', 'ECONNRESET', 'ECONNREFUSED', 'ENOTFOUND',
        'EAI_AGAIN', 'EPIPE', 'ESOCKETTIMEDOUT',
      ];
      if (retryableNetworkErrors.includes(error.code || '')) {
        return RetryDecision.RETRY;
      }
    }

    if (error.type === 'tls') {
      return RetryDecision.DLQ; // TLS errors indicate misconfiguration
    }

    return RetryDecision.RETRY; // Default to retry for unknown errors
  }

  static shouldSkipEndpoint(error: DeliveryError): boolean {
    // Certain errors indicate the endpoint is permanently dead
    return error.statusCode === 410 ||    // Gone
           (error.type === 'dns' && error.code === 'ENOTFOUND') ||  // Domain doesn't exist
           error.statusCode === 401 ||    // Unauthorized (invalid secret)
           error.statusCode === 403;      // Forbidden
  }
}

interface DeadLetterEvent {
  id: string;
  envelope: WebhookEventEnvelope;
  endpointId: string;
  errors: { attempt: number; error: string; timestamp: Date }[];
  lastAttemptAt: Date;
  movedToDLQAt: Date;
  status: 'pending_review' | 'replayed' | 'ignored';
}

class DeadLetterQueue {
  private redis: Redis;
  private dlqPrefix = 'webhook:dlq:';

  async moveToDLQ(job: DeliveryJob): Promise<void> {
    const dlqEvent: DeadLetterEvent = {
      id: job.id,
      envelope: job.envelope,
      endpointId: job.endpointId,
      errors: job.errors || [{ attempt: job.attempt, error: job.lastError || 'Unknown', timestamp: new Date() }],
      lastAttemptAt: new Date(),
      movedToDLQAt: new Date(),
      status: 'pending_review',
    };

    const key = `${this.dlqPrefix}${job.endpointId}`;
    await this.redis.zadd(key, Date.now(), JSON.stringify(dlqEvent));
    // Set TTL for auto-purge (default 30 days)
    await this.redis.expire(key, 30 * 24 * 60 * 60);

    logger.warn('Event moved to DLQ', {
      eventId: job.envelope.id,
      endpointId: job.endpointId,
      eventType: job.envelope.type,
      error: job.lastError,
    });

    // Notify if DLQ threshold exceeded
    const count = await this.redis.zcard(key);
    if (count >= 100) {
      await this.alertDLQThreshold(job.endpointId, count);
    }
  }

  async replayEvent(dlqEventId: string, endpointId: string): Promise<boolean> {
    const key = `${this.dlqPrefix}${endpointId}`;
    const events = await this.redis.zrangebyscore(key, '-inf', '+inf');

    for (const raw of events) {
      const event: DeadLetterEvent = JSON.parse(raw);
      if (event.id === dlqEventId) {
        event.status = 'replayed';
        // Remove from DLQ and re-enqueue to delivery queue
        await this.redis.zrem(key, raw);
        await this.enqueueForDelivery(event);
        return true;
      }
    }
    return false;
  }

  async replayAll(endpointId: string): Promise<number> {
    const key = `${this.dlqPrefix}${endpointId}`;
    const events = await this.redis.zrangebyscore(key, '-inf', '+inf');
    let replayed = 0;

    for (const raw of events) {
      const event: DeadLetterEvent = JSON.parse(raw);
      event.status = 'replayed';
      await this.enqueueForDelivery(event);
      replayed++;
    }

    // Clear DLQ after replay
    await this.redis.del(key);
    logger.info(`Replayed ${replayed} events from DLQ`, { endpointId });
    return replayed;
  }

  async getDLQEvents(endpointId: string, options?: {
    limit?: number; offset?: number; status?: string;
  }): Promise<{ events: DeadLetterEvent[]; total: number }> {
    const key = `${this.dlqPrefix}${endpointId}`;
    const total = await this.redis.zcard(key);
    const raw = await this.redis.zrevrangebyscore(key, '+inf', '-inf', 'LIMIT', options?.offset || 0, options?.limit || 50);

    const events = raw.map(r => JSON.parse(r)).filter((e: DeadLetterEvent) => {
      if (options?.status) return e.status === options.status;
      return true;
    });

    return { events, total };
  }

  async purgeOldEvents(endpointId: string, olderThanDays: number = 30): Promise<number> {
    const key = `${this.dlqPrefix}${endpointId}`;
    const cutoff = Date.now() - (olderThanDays * 24 * 60 * 60 * 1000);
    const removed = await this.redis.zremrangebyscore(key, '-inf', cutoff);
    return removed;
  }

  private async enqueueForDelivery(event: DeadLetterEvent): Promise<void> {
    const queue = this.getDeliveryQueue(event.endpointId);
    await queue.enqueue({
      envelope: event.envelope,
      endpointId: event.endpointId,
      attempt: 0,
      errors: [],
    });
  }
}

// Retry configuration
const DEFAULT_RETRY_CONFIG = {
  maxAttempts: 5,
  baseDelayMs: 1000,
  maxDelayMs: 300000, // 5 minutes
  backoffStrategy: 'exponential_jitter' as const,
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Node.js | Delayed retry queues |
| ioredis (MIT) | Node.js | Redis Sorted Set for DLQ |
| Pino (MIT) | Logging | Retry/DLQ audit logging |

## Production Considerations

**Scaling:** The DLQ stores metadata about failed events indefinitely (up to 30-day TTL). For high-volume webhook delivery, the DLQ can grow large. Implement automatic purging for events older than the configured retention period. Use Redis Sorted Sets with score = timestamp for efficient time-range queries and TTL-based expiration. If Redis memory is constrained, offload DLQ events older than 7 days to S3/Blob storage with a pointer in Redis.

**Security:** DLQ events contain original event payloads that may include PII or sensitive data. Restrict DLQ access to authorized administrators. Implement automatic masking of sensitive fields in the DLQ browser UI. Log all DLQ replay operations with admin identity for audit trails. Never expose DLQ contents in API responses without authentication.

**Monitoring:** Track retry attempt distribution (1st, 2nd, 3rd, ...), retry recovery rate (events that succeed on retry), DLQ growth rate, endpoint error patterns (which endpoints generate the most DLQ events), and replay rate. Alert on DLQ count exceeding thresholds (100 events for critical endpoints, 1000 for standard), retry recovery rate below 50%, and persistent endpoint failures (same endpoint generating DLQ events for 24+ hours).
