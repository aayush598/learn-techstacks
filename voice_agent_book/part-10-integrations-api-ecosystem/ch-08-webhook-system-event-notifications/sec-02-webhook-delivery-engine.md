# Section 02: Webhook Delivery Engine

## Overview

The Webhook Delivery Engine is the core execution component that takes events from the webhook router and delivers them to registered external endpoints. It manages the complete lifecycle of a webhook delivery: serializing the event into the standard envelope, signing the payload, executing the HTTP POST request with configurable timeout, processing the response, handling retries with exponential backoff, and moving permanently failed deliveries to a dead-letter queue (DLQ) for manual inspection.

The delivery engine operates as a set of worker processes that consume from per-endpoint delivery queues. Each worker is responsible for a subset of endpoints, ensuring that delivery to one endpoint does not block others. The engine supports synchronous delivery (for immediate acknowledgment requirements) and asynchronous delivery (for fire-and-forget event notifications). It also provides a webhook replay capability — redelivering events from the DLQ after the consumer has fixed the issue.

## Architecture

```
                 Webhook Delivery Engine

   Event Router → Delivery Queues → Workers → External Endpoint
                                        |
   +----------------------------------------------------------+
   |              Delivery Engine Internals                   |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Queue Consumer   |  | HTTP Dispatcher   |            |
   |  | • Dequeue        |  | • POST request    |            |
   |  | • Lock (TTL)     |  | • TLS 1.3         |            |
   |  | • Ack on success |  | • Connection pool |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Retry Scheduler  |  | Dead Letter Queue |             |
   |  | • Backoff calc   |  | • Failed events   |            |
   |  | • Delayed queue  |  | • Manual replay   |            |
   |  | • Max attempts   |  | • TTL-based purge |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Rate Limiter     |  | Metrics Recorder  |             |
   |  | • Per endpoint   |  | • Delivery time   |            |
   |  | • Token bucket   |  | • Status codes    |            |
   |  | • Backpressure   |  | • Error types     |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Lease-based queue consumption over traditional pub/sub:** Each delivery worker acquires a lease on a queue item when processing. If the worker crashes, the lease expires and the item becomes available for another worker. This provides at-least-once delivery without the complexity of exactly-once semantics. Lease duration is configurable (default 60 seconds, longer than the max expected delivery time including retries). Trade-off: lease expiry can cause duplicate processing (if the original worker succeeds after lease expiry) but prevents permanent message loss on worker failure.

- **Exponential backoff with jitter over fixed interval retry:** Retry timing follows the formula: `baseDelay * 2^(attempt - 1) + random(0, 1000ms)`. The jitter prevents thundering herd when an endpoint recovers and all queued retries fire simultaneously. Default configuration: base delay 1 second, max delay 300 seconds (5 minutes), max retries 5. After the 5th retry, the event moves to the DLQ. Trade-off: jitter-based backoff increases average delivery time for retried events but prevents endpoint overload during recovery.

- **Per-endpoint rate limiting with token bucket algorithm:** Each endpoint has a token bucket rate limiter that prevents the delivery engine from overwhelming consumer endpoints. The bucket is configured based on the endpoint's declared capacity (default 100 requests per minute). The rate limiter also protects the platform from endpoints that become slow — if an endpoint takes 10 seconds per request, the rate limiter reduces concurrency automatically. Trade-off: rate limiting increases delivery latency when an endpoint is slow but prevents cascading failures from endpoint overload.

## Implementation Approach

```
interface DeliveryJob {
  id: string;
  envelope: WebhookEventEnvelope;
  endpointId: string;
  attempt: number;
  lastError?: string;
  enqueuedAt: Date;
  nextRetryAt?: Date;
}

interface DeliveryResult {
  success: boolean;
  statusCode?: number;
  error?: string;
  durationMs: number;
}

class WebhookDeliveryEngine {
  private workers: Worker[];
  private rateLimiters: Map<string, TokenBucket>;
  private dlq: DeadLetterQueue;

  constructor(private config: DeliveryEngineConfig) {
    this.rateLimiters = new Map();
    this.dlq = new DeadLetterQueue(this.config.dlq);
  }

  async start(): Promise<void> {
    const endpointIds = await this.db.webhookEndpoints.find({ status: 'active' }).map(e => e.id);
    for (const endpointId of endpointIds) {
      this.startWorker(endpointId);
    }
  }

  private startWorker(endpointId: string): void {
    const worker = new Worker(
      `webhook:${endpointId}`,
      async (job: Bull.Job<DeliveryJob>) => {
        const endpoint = await this.getEndpoint(endpointId);
        if (!endpoint || endpoint.status !== 'active') {
          logger.warn(`Endpoint ${endpointId} not active, skipping delivery`);
          return;
        }

        const rateLimiter = this.getRateLimiter(endpointId, endpoint.rateLimit);
        await rateLimiter.wait();

        const start = Date.now();
        let result: DeliveryResult;

        try {
          result = await this.deliver(endpoint, job.data.envelope);
        } catch (error) {
          result = { success: false, error: (error as Error).message, durationMs: Date.now() - start };
        }

        await this.recordMetrics(endpointId, result);

        if (!result.success && job.data.attempt < endpoint.retryConfig.maxRetries) {
          const delay = this.calculateBackoff(job.data.attempt, endpoint.retryConfig.backoffMs);
          job.data.attempt++;
          job.data.lastError = result.error;
          job.data.nextRetryAt = new Date(Date.now() + delay);

          logger.warn(`Webhook delivery failed, scheduling retry ${job.data.attempt}`, {
            endpointId,
            eventId: job.data.envelope.id,
            delay,
            error: result.error,
          });

          // Re-throw to let Bull handle retry with delay
          throw new Error(result.error);
        }

        if (!result.success) {
          logger.error(`Webhook delivery failed, moving to DLQ`, {
            endpointId,
            eventId: job.data.envelope.id,
            attempts: job.data.attempt,
            error: result.error,
          });
          await this.dlq.send(job.data);
        }

        return { delivered: result.success, statusCode: result.statusCode };
      },
      {
        concurrency: this.config.defaultConcurrency,
        lockDuration: 60000,
        attempts: 1, // We handle retry ourselves
        backoff: { type: 'fixed', delay: 0 },
      }
    );

    worker.on('failed', (job, error) => {
      logger.error('Worker job failed permanently', { endpointId, jobId: job.id, error: error.message });
    });

    worker.on('completed', (job, result) => {
      logger.debug('Worker job completed', { endpointId, jobId: job.id, result });
    });

    this.workers.push(worker);
  }

  private async deliver(endpoint: WebhookEndpoint, envelope: WebhookEventEnvelope): Promise<DeliveryResult> {
    const payload = JSON.stringify(envelope);
    const signature = this.signPayload(payload, endpoint.secret);
    const start = Date.now();

    try {
      const response = await axios.post(endpoint.url, payload, {
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'X-Webhook-Id': envelope.id,
          'X-Webhook-Idempotency-Key': envelope.idempotencyKey,
          'X-Webhook-Timestamp': envelope.timestamp,
          'X-Webhook-Event-Type': envelope.type,
          ...endpoint.headers,
        },
        timeout: endpoint.retryConfig.timeoutMs,
        validateStatus: () => true,
      });

      const duration = Date.now() - start;

      if (response.status >= 200 && response.status < 300) {
        return { success: true, statusCode: response.status, durationMs: duration };
      }
      if (response.status >= 400 && response.status < 500) {
        // Consumer error — do not retry
        return { success: false, statusCode: response.status, error: `Consumer rejected: ${response.status}`, durationMs: duration };
      }

      return { success: false, statusCode: response.status, error: `Server error: ${response.status}`, durationMs: duration };
    } catch (error) {
      const duration = Date.now() - start;
      if (axios.isAxiosError(error)) {
        return { success: false, error: error.code || error.message, durationMs: duration };
      }
      return { success: false, error: (error as Error).message, durationMs: duration };
    }
  }

  private calculateBackoff(attempt: number, baseMs: number): number {
    const exponential = baseMs * Math.pow(2, attempt - 1);
    const jitter = Math.random() * 1000;
    return Math.min(exponential + jitter, 300000); // Max 5 minutes
  }

  private getRateLimiter(endpointId: string, rateLimit?: { maxRequests: number; windowMs: number }): TokenBucket {
    if (!this.rateLimiters.has(endpointId)) {
      const config = rateLimit || { maxRequests: 100, windowMs: 60000 };
      this.rateLimiters.set(endpointId, new TokenBucket({
        capacity: config.maxRequests,
        refillRate: config.maxRequests / (config.windowMs / 1000),
        refillInterval: 1000,
      }));
    }
    return this.rateLimiters.get(endpointId)!;
  }

  async replayFromDLQ(endpointId: string, maxEvents?: number): Promise<number> {
    const events = await this.dlq.peek(endpointId, maxEvents || 100);
    let replayed = 0;
    for (const event of events) {
      const endpoint = await this.getEndpoint(endpointId);
      if (!endpoint) continue;
      await this.deliver(endpoint, event.envelope);
      await this.dlq.ack(event.id);
      replayed++;
    }
    return replayed;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Node.js | Delivery queues + workers |
| ioredis (MIT) | Node.js | Redis backend for BullMQ |
| Token Bucket (MIT) | Node.js | Per-endpoint rate limiting |

## Production Considerations

**Scaling:** Delivery engine workers should be deployed as a separate service (webhook-worker) from the webhook API. Scale workers horizontally — each worker instance handles a subset of endpoint queues. Use Redis Cluster for queue storage to support high throughput. Monitor worker utilization and auto-scale based on queue depth. Implement graceful shutdown: workers finish in-flight deliveries before stopping.

**Security:** Workers make outbound HTTP calls to consumer endpoints — implement IP allowlisting for outbound connections. Never include webhook secrets in error messages sent to logs. The DLQ contains failed deliveries with potentially sensitive event data — restrict DLQ access to admin users and implement automatic purge after 30 days. Ensure workers run with the minimum necessary permissions (queues, Redis, and outbound HTTP only).

**Monitoring:** Track deliveries per second, delivery success rate by endpoint, delivery latency (p50/p95/p99), retry rate, DLQ growth, worker concurrency utilization, and rate limiter wait times. Alert on delivery success rate below 90%, DLQ exceeding 1000 events, any endpoint with 0% delivery success in 5 minutes, and worker processing lag exceeding 30 seconds. Set up webhook delivery SLA dashboard for customer-facing metrics.
