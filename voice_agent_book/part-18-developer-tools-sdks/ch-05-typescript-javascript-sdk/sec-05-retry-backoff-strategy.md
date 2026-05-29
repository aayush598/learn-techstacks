# Section 05: Retry & Backoff Strategy

## Overview

The SDK includes automatic retry with exponential backoff and jitter for transient failures. Retry logic covers rate limit responses (429), server errors (5xx), and network failures. A circuit breaker pattern prevents overwhelming failing services, and a retry budget limits total retry time.

## Architecture

```
Retry Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Retry Decision Matrix:
  Status    Description         Retry?   Backoff
  ────────────────────────────────────────────────────
  200-299   Success             No       —
  400-404   Client error        No       — (won't succeed)
  408       Timeout             Yes      Exponential
  429       Rate limited        Yes      With Retry-After
  500       Internal error      Yes      Exponential
  502       Bad gateway         Yes      Exponential
  503       Service unavail.    Yes      Exponential
  Network   Fetch failed        Yes      Exponential
  Timeout   AbortController     Yes      Exponential

Backoff Calculation:
  attempt 1:  1,000ms × 2^0 + jitter(0-500ms)  = ~1,000-1,500ms
  attempt 2:  1,000ms × 2^1 + jitter(0-500ms)  = ~2,000-2,500ms
  attempt 3:  1,000ms × 2^2 + jitter(0-500ms)  = ~4,000-4,500ms
  Max: 30 seconds

Circuit Breaker States:
  ┌─────────┐     Failure     ┌─────────┐    Timeout    ┌─────────┐
  │  CLOSED  │───Threshold──▶│  OPEN   │───(30s)────▶│ HALF_OPEN│
  │(normal)  │               │(reject) │               │(testing) │
  └─────────┘                └─────────┘               └─────────┘
       ↑                         │                         │
       └───────Success──────────┘                         │
       ◀───────────Success───────────────────────────────┘
```

## Design Decisions

- **Exponential Backoff with Jitter**: Prevents thundering herd when multiple clients retry simultaneously
- **Retry-After Respect**: For 429 responses, use Retry-After header value instead of computed backoff
- **Circuit Breaker**: Stops retries when error rate exceeds 50% in 30-second window — protects both client and server
- **Retry Budget**: Maximum 30 seconds of retry time before giving up

## Implementation Approach

```typescript
// Retry configuration
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
  retryBudgetMs: number;
  circuitBreakerThreshold: number; // Error rate % to open circuit
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30_000,
  jitterMs: 500,
  retryBudgetMs: 30_000,
  circuitBreakerThreshold: 50, // 50% error rate
};

// Backoff calculator
class BackoffCalculator {
  constructor(private config: RetryConfig) {}

  getDelay(attempt: number, retryAfterHeader?: number): number {
    // Respect Retry-After header
    if (retryAfterHeader !== undefined && retryAfterHeader > 0) {
      return Math.min(retryAfterHeader * 1000, this.config.maxDelayMs);
    }

    const exponential = this.config.baseDelayMs * Math.pow(2, attempt - 1);
    const capped = Math.min(exponential, this.config.maxDelayMs);
    const jitter = Math.random() * this.config.jitterMs;

    return Math.floor(capped + jitter);
  }
}

// Circuit breaker
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime = 0;
  private openTime = 0;
  private readonly OPEN_TIMEOUT = 30_000; // 30 seconds

  constructor(private threshold: number) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.openTime >= this.OPEN_TIMEOUT) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN — request blocked');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.successCount++;

    if (this.state === 'HALF_OPEN') {
      // Successful call in half-open state closes the circuit
      this.state = 'CLOSED';
      this.failureCount = 0;
      this.successCount = 0;
    }

    // Reset counters periodically
    if (this.successCount > 100) {
      this.failureCount = 0;
      this.successCount = 0;
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    const totalCalls = this.failureCount + this.successCount;
    const errorRate = totalCalls > 0 ? (this.failureCount / totalCalls) * 100 : 0;

    if (errorRate >= this.threshold) {
      this.state = 'OPEN';
      this.openTime = Date.now();
    }
  }

  get isOpen(): boolean {
    return this.state === 'OPEN';
  }
}

// Retry handler
class RetryHandler {
  private backoff: BackoffCalculator;
  private circuitBreaker: CircuitBreaker;
  private budget: number;

  constructor(private config: RetryConfig = DEFAULT_RETRY_CONFIG) {
    this.backoff = new BackoffCalculator(config);
    this.circuitBreaker = new CircuitBreaker(config.circuitBreakerThreshold);
    this.budget = config.retryBudgetMs;
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    return this.circuitBreaker.call(async () => {
      let lastError: Error;
      const startTime = Date.now();

      for (let attempt = 1; attempt <= this.config.maxRetries; attempt++) {
        try {
          return await fn();
        } catch (error) {
          lastError = error as Error;

          // Check if we should retry
          if (!this.shouldRetry(error as ApiError, attempt)) {
            throw error;
          }

          // Check retry budget
          if (Date.now() - startTime > this.budget) {
            throw new Error('Retry budget exceeded');
          }

          // Extract Retry-After from error
          const retryAfter = error instanceof RateLimitError
            ? error.retryAfter
            : undefined;

          // Wait before retrying
          const delay = this.backoff.getDelay(attempt, retryAfter);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }

      throw lastError!;
    });
  }

  private shouldRetry(error: Error, attempt: number): boolean {
    if (attempt >= this.config.maxRetries) return false;

    if (error instanceof RateLimitError) return true;
    if (error instanceof ServerError) return true;
    if (error instanceof NetworkError) return true;
    if (error instanceof TimeoutError) return true;

    // Retry on generic network errors
    if ((error as ApiError).statusCode === 0) return true;

    return false;
  }
}
```

## Integration Points

- **HTTP Client**: RetryHandler wraps all HTTP requests in the client
- **Plugin System**: Retry behavior is configurable via plugin options
- **Monitoring**: Retry attempts and circuit breaker state changes are emitted as events

## Production Considerations

- **Retry Budget**: 30 seconds prevents runaway retries; configure per-environment
- **Circuit Breaker Reset**: Test with synthetic requests after open timeout before resuming normal traffic
- **Retry Metrics**: Track retry count, success rate, and circuit breaker state for operational visibility
- **Idempotency**: All retried requests carry idempotency keys to prevent duplicate side effects

## Open-Source Tools

- **Opossum**: Circuit breaker library for Node.js
- **p-retry**: Promise-based retry with exponential backoff
