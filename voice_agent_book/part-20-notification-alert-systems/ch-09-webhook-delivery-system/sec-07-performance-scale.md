# Section 07: Performance & Scale

## Overview

High-volume webhook delivery requires batching, parallel processing, and circuit breakers to maintain throughput and reliability. The delivery system scales horizontally across multiple workers, with endpoint health tracking to avoid wasting resources on failing endpoints.

## Architecture

```
High-Volume Delivery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Event Stream] → [Partitioner] → [Worker Pool] → [Endpoint]
      │                │                │              │
  1000s events      Shard by         Multiple      Circuit breaker
  per second        endpoint_id      processes      on failure
                    for ordering     consuming      Health checks
                                     from partitions

Circuit Breaker States:
  ┌──────────┐     failure > threshold    ┌──────────┐
  │  CLOSED  │ ──────────────────────────→│   OPEN   │
  │ (normal) │                            │ (failing)│
  └──────────┘                            └──────────┘
       ↑                                       │
       │                            timeout elapsed
       │                                       │
       │                              ┌────────┴────────┐
       │    success ≥ threshold       │   HALF-OPEN     │
       └─────────────────────────────│ (probing)        │
                                     └─────────────────┘

Batch Delivery:
  Multiple events sent in single HTTP request
  POST /webhooks with array payload
  Reduces connection overhead for high-throughput endpoints
  Consumer acknowledges entire batch
```

## Design Decisions

- **Horizontal Scaling**: Workers scale based on queue depth
- **Per-Endpoint Circuit Breaker**: Failures isolated to individual endpoints
- **Batch Delivery**: Optional for high-volume consumer endpoints
- **Health Probing**: Periodic HEAD/GET requests to check endpoint health

## Implementation Approach

```typescript
interface CircuitBreakerState {
  endpointId: string;
  state: 'closed' | 'open' | 'half-open';
  failureCount: number;
  successCount: number;
  failureThreshold: number;
  successThreshold: number; // to close after half-open
  openTimeoutMs: number;
  lastFailureTime: number;
  lastProbeTime?: number;
}

class CircuitBreaker {
  private breakers: Map<string, CircuitBreakerState> = new Map();

  getState(endpointId: string, config: BreakerConfig): CircuitBreakerState {
    let state = this.breakers.get(endpointId);
    if (!state) {
      state = {
        endpointId,
        state: 'closed',
        failureCount: 0,
        successCount: 0,
        failureThreshold: config.failureThreshold,
        successThreshold: config.successThreshold,
        openTimeoutMs: config.openTimeoutMs,
        lastFailureTime: 0,
      };
      this.breakers.set(endpointId, state);
    }
    return state;
  }

  isAllowed(endpointId: string, config: BreakerConfig): boolean {
    const state = this.getState(endpointId, config);

    if (state.state === 'closed') return true;

    if (state.state === 'open') {
      const elapsed = Date.now() - state.lastFailureTime;
      if (elapsed >= state.openTimeoutMs) {
        state.state = 'half-open';
        state.lastProbeTime = Date.now();
        return true; // Allow probe request
      }
      return false; // Reject request
    }

    // half-open — allow limited requests
    return state.successCount < state.successThreshold;
  }

  recordSuccess(endpointId: string): void {
    const state = this.breakers.get(endpointId);
    if (!state) return;

    state.successCount++;
    state.failureCount = 0;

    if (state.state === 'half-open' && state.successCount >= state.successThreshold) {
      state.state = 'closed';
      state.successCount = 0;
    }
  }

  recordFailure(endpointId: string): void {
    const state = this.breakers.get(endpointId);
    if (!state) return;

    state.failureCount++;
    state.lastFailureTime = Date.now();

    if (state.state === 'closed' && state.failureCount >= state.failureThreshold) {
      state.state = 'open';
    } else if (state.state === 'half-open') {
      state.state = 'open';
      state.successCount = 0;
    }
  }
}

class BatchDeliveryService {
  async deliverBatch(events: WebhookEvent[], endpoint: WebhookEndpoint): Promise<BatchResult> {
    const batchSize = Math.min(events.length, 100);
    const batches: WebhookEvent[][] = [];

    for (let i = 0; i < events.length; i += batchSize) {
      batches.push(events.slice(i, i + batchSize));
    }

    const results: BatchItemResult[] = [];

    for (const batch of batches) {
      try {
        const payload = {
          batch: batch.map(e => ({
            id: e.id,
            type: e.type,
            payload: e.payload,
            timestamp: e.timestamp,
          })),
          meta: {
            batchSize: batch.length,
            batchId: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
          },
        };

        const response = await fetch(endpoint.url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Webhook-Batch': 'true',
            'X-Batch-ID': payload.meta.batchId,
          },
          body: JSON.stringify(payload),
          signal: AbortSignal.timeout(10000),
        });

        const responseBody = await response.json();

        if (response.ok) {
          // Consumer can acknowledge individual events in batch response
          const acked = responseBody.acknowledged || batch.map(e => e.id);
          for (const event of batch) {
            results.push({
              eventId: event.id,
              status: acked.includes(event.id) ? 'success' : 'failed',
            });
          }
        } else {
          // Fall back to individual delivery for this batch
          const individualResults = await this.deliverIndividually(batch, endpoint);
          results.push(...individualResults);
        }
      } catch (error) {
        results.push(...batch.map(e => ({
          eventId: e.id,
          status: 'failed' as const,
          error: error.message,
        })));
      }
    }

    const successful = results.filter(r => r.status === 'success').length;
    return { results, successRate: successful / results.length };
  }

  private async deliverIndividually(
    events: WebhookEvent[],
    endpoint: WebhookEndpoint,
  ): Promise<BatchItemResult[]> {
    return Promise.all(
      events.map(async event => {
        try {
          const response = await fetch(endpoint.url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(event),
            signal: AbortSignal.timeout(5000),
          });
          return {
            eventId: event.id,
            status: response.ok ? 'success' : 'failed',
          };
        } catch (error) {
          return { eventId: event.id, status: 'failed', error: error.message };
        }
      })
    );
  }
}

class ParallelDeliveryWorker {
  private circuitBreaker = new CircuitBreaker();

  async process(job: BullJob): Promise<void> {
    const { events, endpoint } = job.data;

    // Check circuit breaker
    if (!this.circuitBreaker.isAllowed(endpoint.id, endpoint.breakerConfig)) {
      // Re-queue with delay instead of failing
      await job.discard();
      throw new BullError.BullError('Endpoint circuit breaker open');
    }

    // Deliver with health check integration
    try {
      const service = new BatchDeliveryService();
      const result = await service.deliverBatch(events, endpoint);

      if (result.successRate > 0.8) {
        this.circuitBreaker.recordSuccess(endpoint.id);
      } else {
        this.circuitBreaker.recordFailure(endpoint.id);
      }
    } catch (error) {
      this.circuitBreaker.recordFailure(endpoint.id);
      throw error;
    }
  }
}
```

## Integration Points

- **Queue System**: BullMQ for worker pool management
- **Endpoint Registry**: Circuit breaker config per endpoint
- **Monitoring**: Breaker state changes logged and alerted

## Production Considerations

- **Worker Autoscaling**: Scale workers based on queue depth
- **Circuit Breaker Tuning**: Thresholds adjusted per endpoint based on historical behavior
- **Batch Size Optimization**: Tune based on consumer response times
- **Health Probe Interval**: Probe every 60 seconds for open circuits

## Open-Source Tools

- **BullMQ**: Worker concurrency and scaling
- **opossum**: Circuit breaker implementation
