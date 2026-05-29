# Section 02: Delivery Retry Logic

## Overview

Webhook delivery failures trigger automatic retry with exponential backoff and jitter. The retry system respects endpoint health, delivery windows, and configurable retry limits. After exhausting retries, events are moved to a dead letter queue for manual inspection and replay. Retry logic is designed to handle transient failures while preventing resource exhaustion from persistent errors.

## Architecture

```
Retry Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Event Published] → [Queue]
                         │
                    [Delivery Worker]
                         │
                    [HTTP POST to Endpoint]
                         │
                 ┌───────┴───────┐
                 │ Success       │ Failure
                 ▼               ▼
            [Log + Ack]    [Check Retry Count]
                                  │
                          ┌───────┴───────┐
                          │ < Max Retries │ ≥ Max Retries
                          ▼               ▼
                    [Schedule Retry] [Dead Letter Queue]
                          │
                    [Exponential Backoff + Jitter]

Retry Schedule:
  Attempt 1: 10 seconds + jitter
  Attempt 2: 30 seconds + jitter
  Attempt 3: 2 minutes + jitter
  Attempt 4: 5 minutes + jitter
  Attempt 5: 15 minutes + jitter
  Attempt 6: 30 minutes + jitter
  Attempt 7-10: 1 hour + jitter (capped)
  Total window: 24 hours maximum

HTTP Status Codes and Retry Behavior:
  2xx → Success — stop retry
  400 → Bad request — stop retry (client error, will never succeed)
  401 → Unauthorized — stop retry (invalid credentials)
  404 → Not found — stop retry (endpoint removed)
  408 → Timeout — retry
  429 → Rate limited — retry with Retry-After header respect
  500 → Server error — retry
  503 → Unavailable — retry
```

## Design Decisions

- **Exponential Backoff with Jitter**: Prevents thundering herd when multiple endpoints recover simultaneously
- **Max 10 Retries Over 24 Hours**: Bounds retry overhead while providing ample recovery time
- **Respect Retry-After Header**: If endpoint returns 429 with Retry-After, use that delay instead of computed backoff
- **4xx vs 5xx Discrimination**: Client errors (400, 401, 404) are non-retryable — immediately moved to DLQ

## Implementation Approach

```typescript
// Retry configuration
interface RetryConfig {
  maxRetries: number;
  maxDeliveryWindowMs: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 10,
  maxDeliveryWindowMs: 86_400_000, // 24 hours
  baseDelayMs: 10_000,
  maxDelayMs: 3_600_000, // 1 hour
  jitterMs: 5_000,
};

// Retry calculator
class RetryCalculator {
  constructor(private config: RetryConfig = DEFAULT_RETRY_CONFIG) {}

  getDelay(attempt: number, retryAfterHeader?: number): number {
    // Respect Retry-After header from endpoint
    if (retryAfterHeader !== undefined) {
      return Math.min(retryAfterHeader * 1000, this.config.maxDelayMs);
    }

    const exponential = this.config.baseDelayMs * Math.pow(3, attempt - 1);
    const capped = Math.min(exponential, this.config.maxDelayMs);
    const jitter = Math.random() * this.config.jitterMs;

    return Math.floor(capped + jitter);
  }

  shouldRetry(attempt: number, firstAttemptAt: Date, statusCode: number): { retry: boolean; reason?: string } {
    // Non-retryable status codes
    if ([400, 401, 403, 404, 410].includes(statusCode)) {
      return { retry: false, reason: `Non-retryable status code: ${statusCode}` };
    }

    if (attempt > this.config.maxRetries) {
      return { retry: false, reason: `Max retries (${this.config.maxRetries}) exceeded` };
    }

    const elapsed = Date.now() - firstAttemptAt.getTime();
    if (elapsed > this.config.maxDeliveryWindowMs) {
      return { retry: false, reason: 'Delivery window (24h) exceeded' };
    }

    return { retry: true };
  }

  getNextAttemptTime(attempt: number, firstAttemptAt: Date, retryAfterHeader?: number): Date | null {
    const delay = this.getDelay(attempt, retryAfterHeader);
    const nextTime = new Date(Date.now() + delay);

    if (nextTime.getTime() - firstAttemptAt.getTime() > this.config.maxDeliveryWindowMs) {
      return null; // Would exceed delivery window
    }

    return nextTime;
  }
}

// Delivery worker
class WebhookDeliveryWorker {
  constructor(
    private queue: Queue,
    private httpClient: HttpClient,
    private retryCalculator: RetryCalculator,
    private dlq: DeadLetterQueue,
  ) {}

  async process(job: WebhookDeliveryJob): Promise<void> {
    const { endpoint, event, attempt, firstAttemptAt } = job;

    try {
      const response = await this.httpClient.post(endpoint.url, {
        headers: this.buildHeaders(event, attempt),
        body: event,
        timeout: 30_000,
      });

      // Success
      if (response.status >= 200 && response.status < 300) {
        await this.recordDelivery(endpoint.id, event.id, 'success', attempt);
        return;
      }

      // Check if we should retry
      const retryAfter = response.headers['retry-after']
        ? parseInt(response.headers['retry-after'])
        : undefined;

      const { retry, reason } = this.retryCalculator.shouldRetry(
        attempt, new Date(firstAttemptAt), response.status,
      );

      if (retry) {
        const nextAttempt = this.retryCalculator.getNextAttemptTime(
          attempt + 1, new Date(firstAttemptAt), retryAfter,
        );

        await this.queue.schedule({
          ...job,
          attempt: attempt + 1,
          nextAttemptAt: nextAttempt,
        });

        await this.recordDelivery(endpoint.id, event.id, 'retry', attempt, {
          statusCode: response.status,
          nextAttempt: nextAttempt?.toISOString(),
        });
      } else {
        await this.dlq.send(job, reason || 'Max retries exceeded');
        await this.recordDelivery(endpoint.id, event.id, 'failed', attempt, {
          statusCode: response.status,
          reason,
        });
      }
    } catch (error) {
      // Network error — retry
      const { retry, reason } = this.retryCalculator.shouldRetry(
        attempt, new Date(firstAttemptAt), 0,
      );

      if (retry) {
        const nextAttempt = this.retryCalculator.getNextAttemptTime(
          attempt + 1, new Date(firstAttemptAt),
        );

        await this.queue.schedule({
          ...job,
          attempt: attempt + 1,
          nextAttemptAt: nextAttempt,
        });
      } else {
        await this.dlq.send(job, reason || 'Delivery failed');
      }
    }
  }
}
```

## Integration Points

- **BullMQ**: Queue management for delivery jobs with delayed scheduling
- **DLQ Storage**: Dead letter queue backed by database with replay UI
- **Monitoring**: Delivery attempt metrics tracked per endpoint for health monitoring

## Production Considerations

- **Retry Storm Protection**: If multiple endpoints fail, retries amplify; use circuit breaker pattern
- **Endpoint Health Scoring**: Track recent success rate to adjust retry aggressiveness
- **Delivery SLA**: 99.9% of events delivered within 5 minutes; 99.99% within 24 hours
- **Webhook Jitter**: Add 0-30 second random jitter to first delivery attempt to spread load

## Open-Source Tools

- **BullMQ**: Job queue with delayed scheduling and retry support
- **Redis**: Backing store for BullMQ queues
