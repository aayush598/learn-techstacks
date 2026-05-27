# Section 05: Error Handling & Retry

## Overview

Error handling and retry logic ensure integration reliability in the face of network failures, API errors, rate limiting, and transient service degradation. External API calls fail for many reasons: network timeouts, DNS resolution failures, TLS negotiation errors, HTTP 5xx server errors, HTTP 429 rate limits, authentication expiry, request validation errors (4xx), and data format mismatches. Each error type requires a different response — some are retryable (timeouts, 5xx, 429), some are not (4xx validation errors), and some require special handling (auth expiry triggers re-authentication before retry).

The retry engine implements exponential backoff with jitter (to prevent thundering herd), configurable max retries (per integration, per operation), retry budgets (to prevent overload during systemic failures), and idempotency (to safely retry write operations). Errors are classified into categories with specific handling policies. The system also supports circuit breaker integration — repeated failures in a short window open the circuit, preventing further requests until the external service recovers.

## Architecture

```
                  Error Handling & Retry Architecture

   Request → Execute → Error? → Classify → Retryable? → Retry → Backoff
      |          |        |          |          |          |
      |          |        |          |          v          v
      |          |        |          |       +----------------------+
      |          |        |          |       |  Backoff Calculator  |
      |          |        |          |       |  • Exponential       |
      |          |        |          |       |  • Jitter            |
      |          |        |          |       |  • Per-integration   |
      |          |        |          |       |  • Max retries       |
      |          |        |          |       +----------------------+
      |          |        |          |                |
      |          v        v          v                v
      |     +-------------------------------------------+
      |     |         Error Classifier                   |
      |     |                                            |
      |     |  Retryable:                                |
      |     |  - HTTP 429 (rate limit)                   |
      |     |  - HTTP 5xx (server error)                 |
      |     |  - Network error (timeout, DNS, TCP)       |
      |     |  - Auth expired (refresh then retry)       |
      |     |                                            |
      |     |  Non-retryable:                            |
      |     |  - HTTP 4xx (validation error)             |
      |     |  - HTTP 401/403 (auth denied)              |
      |     |  - Data format error                       |
      |     |  - Circuit breaker open                    |
      |     +-------------------------------------------+
      v
   Return Response / Error
```

## Design Decisions

- **Idempotency keys for safe retry of write operations over fire-and-forget:** Write operations (create, update, delete) include an idempotency key header that the external API uses to detect and reject duplicate requests. If a request times out (response not received), the retry sends the same idempotency key. The API processes it only once. This enables safe retry without risk of duplicate charges, duplicate records, or inconsistent state. Trade-off: requires external API idempotency support (Stripe, Shopify support it; many legacy APIs do not).

- **Per-operation retry budgets over global retry limits:** Each integration operation type has a retry budget (e.g., 50 retries per 5-minute window for Salesforce contact creation). If the budget is exhausted, further retries are queued rather than executed, preventing retry storms from overwhelming a struggling API. Budgets replenish over time. This is more nuanced than a simple max retries count and prevents cascading failures. Trade-off: retry budgets add complexity to configuration and monitoring.

- **Graceful degradation with fallback responses over hard failures:** When an integration is unavailable after exhausting retries, the system returns a fallback response (cached data, default values, or a "service unavailable" indication to the agent) rather than failing the entire call operation. The agent can continue the conversation with partial information, and the system retries in the background. Trade-off: fallback responses may contain stale data, requiring clear communication to agents and customers about data freshness.

## Implementation Approach

```
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  multiplier: number;       // Exponential factor (default 2)
  jitter: boolean;          // Add random jitter
  retryableStatuses: number[];
  retryBudget: {
    maxRetriesInWindow: number;
    windowMs: number;
  };
}

class RetryEngine {
  async executeWithRetry<T>(
    operation: () => Promise<AdapterResponse<T>>,
    config: RetryConfig,
    context: { integrationId: string; tenantId: string; operation: string }
  ): Promise<AdapterResponse<T>> {
    const budget = new RetryBudget(config.retryBudget);

    for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
      try {
        const response = await operation();
        await budget.recordSuccess(context);
        return response;
      } catch (error) {
        const classified = this.classifyError(error);
        if (!classified.retryable || attempt === config.maxRetries || !budget.canRetry(context)) {
          throw classified.toException();
        }
        await budget.recordFailure(context);
        const delay = this.calculateDelay(attempt, config);
        await this.sleep(delay);
        if (classified.needsReauth) {
          await this.authManager.refreshToken(context.integrationId, context.tenantId);
        }
      }
    }
    throw new Error('Max retries exceeded');
  }

  private calculateDelay(attempt: number, config: RetryConfig): number {
    const exponential = config.baseDelayMs * Math.pow(config.multiplier, attempt);
    const capped = Math.min(exponential, config.maxDelayMs);
    const jitter = config.jitter ? capped * (0.5 + Math.random() * 0.5) : capped;
    return Math.floor(jitter);
  }

  private classifyError(error: any): ClassifiedError {
    if (error.response?.status === 429) {
      return { retryable: true, needsReauth: false, retryAfter: error.response.headers['retry-after'] };
    }
    if (error.response?.status >= 500) {
      return { retryable: true, needsReauth: false };
    }
    if (error.response?.status === 401) {
      return { retryable: true, needsReauth: true };
    }
    if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') {
      return { retryable: true, needsReauth: false };
    }
    return { retryable: false, needsReauth: false };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Opossum** (MIT) | Node.js | Circuit breaker with retry |
| **p-retry** (MIT) | Node.js | Promise-based retry |
| **BullMQ** (MIT) | Queue | Async retry queue |
| **Redis** (BSD) | Data store | Retry budget counters |

## Production Considerations

**Scaling:** Retry state (budget counters, circuit breaker state) must be shared across instances via Redis. Exponential backoff with jitter naturally distributes retry load. For systemic failures (entire API down), use a dead letter queue for requests that exceed retry budgets rather than discarding them. Implement rate-limited retry — if an API is returning 429, obey the Retry-After header rather than the configured backoff schedule.

**Security:** Retry logic must not retry on authentication errors (401/403) unless the retry handler explicitly refreshes credentials. Repeated auth failures may indicate compromised credentials — alert and disable the integration after 3 consecutive auth failures. Never include authentication tokens in error logs.

**Monitoring:** Track retry rate (% of requests that require at least one retry), average retries per request, retry success rate, retry budget exhaustion events, dead letter queue depth, and circuit breaker transitions. Alert on retry rate > 10% (indicates API or network issues), retry budget exhaustion, and dead letter queue not draining.
