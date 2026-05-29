# Section 02: Retry with Backoff

## Overview

Failed webhook deliveries are retried with exponential backoff and jitter to avoid overwhelming consumer endpoints. Retry limits prevent infinite delivery attempts, and failed deliveries rotate to a dead letter queue for manual inspection.

## Architecture

```
Retry Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Delivery Attempt
       │
  ┌────┴────┐
  │         │
 Success   Failure (4xx/5xx/timeout)
  │         │
  [Done]   Retry with backoff
              │
       ┌──────┴──────┐
       │              │
  4xx (client)    5xx (server)
  No retry (bad   Retry with
  config)         exponential
                  backoff + jitter
       │              │
  Alert user     attempts < max?
  to fix              │
  endpoint       ┌────┴────┐
                 │         │
               Yes        No
                 │         │
           Wait delay   Move to
           + retry     Dead Letter
                       Queue

Backoff Formula:
  delay = baseDelay * (2 ^ attempt) + jitter(0, baseDelay)
  
  Attempt 1: 1s + random(0, 1s) = 1.0-2.0s
  Attempt 2: 2s + random(0, 1s) = 2.0-3.0s
  Attempt 3: 4s + random(0, 1s) = 4.0-5.0s
  Attempt 4: 8s + random(0, 1s) = 8.0-9.0s
  Attempt 5: 16s + random(0, 1s) = 16.0-17.0s
```

## Design Decisions

- **Exponential Backoff**: Prevents thundering herd on recovery
- **Jitter**: Random delay component prevents synchronized retry storms
- **4xx vs 5xx Discrimination**: Client errors not retried; server errors retried
- **Configurable Limits**: Max retries and base delay configurable per endpoint

## Implementation Approach

```typescript
interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  retryOnStatus: number[];
  noRetryStatus: number[]; // 4xx codes that should not be retried
}

class RetryStrategy {
  computeDelay(attempt: number, config: RetryConfig): number {
    const exponentialDelay = config.baseDelayMs * Math.pow(2, attempt);
    const cappedDelay = Math.min(exponentialDelay, config.maxDelayMs);
    const jitter = Math.random() * config.baseDelayMs;
    return Math.floor(cappedDelay + jitter);
  }

  shouldRetry(statusCode: number | null, error: Error | null, config: RetryConfig): boolean {
    if (statusCode) {
      if (config.noRetryStatus.includes(statusCode)) return false;
      if (config.retryOnStatus.length > 0 && !config.retryOnStatus.includes(statusCode)) return false;
    }
    if (error && error.name === 'AbortError') return true; // timeout
    return true;
  }

  getRetryAfterHeader(headers: Headers): number | null {
    const retryAfter = headers.get('Retry-After');
    if (!retryAfter) return null;
    const seconds = parseInt(retryAfter, 10);
    return isNaN(seconds) ? null : seconds * 1000;
  }
}

class RetryWorker {
  private strategy = new RetryStrategy();

  async process(job: BullJob): Promise<void> {
    const { event, endpoint, retryConfig } = job.data;
    const attempt = job.attemptsMade;
    const config = retryConfig || this.defaultConfig;

    if (!this.strategy.shouldRetry(null, null, config)) {
      throw new Error('Max retries exceeded');
    }

    // Respect Retry-After header from previous attempt
    if (job.data.retryAfterMs) {
      const elapsed = Date.now() - job.timestamp;
      const remainingWait = job.data.retryAfterMs - elapsed;
      if (remainingWait > 0) {
        await new Promise(resolve => setTimeout(resolve, remainingWait));
      }
    }

    const delay = this.strategy.computeDelay(attempt, config);
    await new Promise(resolve => setTimeout(resolve, delay));

    // Recalculate if client should still retry
    if (!this.strategy.shouldRetry(null, null, config)) {
      return; // Skip this attempt
    }
  }

  async handleResponse(response: Response, endpoint: WebhookEndpoint): Promise<boolean> {
    const retryAfter = this.strategy.getRetryAfterHeader(response.headers);

    if (response.status >= 400 && response.status < 500) {
      // Client error — only retry on certain statuses
      const retryableClientErrors = [408, 429]; // Timeout, Too Many Requests
      if (retryableClientErrors.includes(response.status)) {
        return true; // Retry
      }
      return false; // Don't retry client errors
    }

    if (response.status >= 500) {
      return true; // Always retry server errors
    }

    return false;
  }
}
```

## Integration Points

- **Delivery Worker**: Retry logic integrated with BullMQ job processing
- **Endpoint Registry**: Per-endpoint retry configuration
- **Dead Letter Queue**: Failed deliveries after max retries

## Production Considerations

- **Retry Budget**: Maximum 5 retries per delivery within 60 seconds
- **Idempotency**: Retries use same idempotency key for duplicate detection
- **Alert on Retry Storm**: Alert if >10% of deliveries are retrying

## Open-Source Tools

- **BullMQ**: Built-in backoff and retry support
- **p-retry**: Promise-based retry utility
