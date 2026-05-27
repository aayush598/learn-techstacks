# Section 01: Usage Event Pipeline

## Event Emission from Services

Every service in the voice agent platform emits usage events when billable actions occur. Voice call processing, real-time transcription, sentiment analysis, TTS generation, and API requests all generate usage events that feed into the metering pipeline.

Event emission follows a fire-and-forget pattern to avoid impacting latency-sensitive operations. The calling service publishes an event to the message bus and continues processing without waiting for metering acknowledgment. This decouples billable operations from billing infrastructure.

```typescript
interface UsageEvent {
  id: string;
  idempotencyKey: string;
  tenantId: string;
  subscriptionId?: string;
  eventType: UsageEventType;
  timestamp: string;
  meter: string;
  quantity: number;
  unit: string;
  metadata: Record<string, string>;
}

enum UsageEventType {
  CALL_MINUTE = 'voice.call_minute',
  TRANSCRIPTION_SECOND = 'voice.transcription_second',
  TTS_CHARACTER = 'voice.tts_character',
  STORAGE_GIGABYTE = 'storage.gigabyte_month',
  API_REQUEST = 'api.request',
  AGENT_MINUTE = 'agent.active_minute',
}

// Service-side emission example
class VoiceCallService {
  async processCall(call: Call): Promise<void> {
    // Process the call...
    const result = await this.callEngine.handle(call);

    // Emit usage event asynchronously
    this.eventBus.publish('usage.events', {
      idempotencyKey: `call_minutes_${call.id}`,
      tenantId: call.tenantId,
      eventType: UsageEventType.CALL_MINUTE,
      meter: 'monthly_minutes',
      quantity: result.durationSeconds / 60,
      unit: 'minutes',
      timestamp: new Date().toISOString(),
      metadata: {
        callId: call.id,
        direction: call.direction,
        duration: result.durationSeconds.toString(),
      },
    });

    return result;
  }
}
```

## Event Bus Architecture

The event bus sits between service emission and usage processing. RabbitMQ serves as the message broker with a topic exchange for usage events. Each event type routes to a dedicated queue, allowing independent scaling of processing pipelines.

```
          ┌──────────────────────────────────────────────────┐
          │                  Event Bus (RabbitMQ)             │
          │                                                   │
          │  Topic Exchange: usage.events                     │
          │                                                   │
          │  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
          │  │ voice.*      │  │ storage.*    │  │ api.*  │ │
          │  └──────┬───────┘  └──────┬───────┘  └───┬────┘ │
          │         │                 │               │      │
          │  ┌──────┴───────┐  ┌──────┴───────┐  ┌───┴────┐ │
          │  │ voice.queue  │  │ storage.q    │  │ api.q  │ │
          │  └──────┬───────┘  └──────┬───────┘  └───┬────┘ │
          └─────────┼─────────────────┼───────────────┼──────┘
                    │                 │               │
              ┌─────┴─────┐     ┌─────┴─────┐    ┌───┴────┐
              │ Validator │     │ Validator │    │Validator│
              └───────────┘     └───────────┘    └────────┘
```

RabbitMQ is chosen over Kafka for this use case because the throughput requirements (thousands of events per second) are well within RabbitMQ's capabilities, and the simpler operational model reduces overhead. Kafka would be appropriate if event throughput exceeds 100K/second or if longer event retention is needed.

## Batch vs Streaming

Usage events can be processed in batches (aggregated hourly/daily) or as a stream (real-time). The choice involves a trade-off between operational cost and billing accuracy.

```typescript
interface ProcessingStrategy {
  mode: 'batch' | 'streaming' | 'hybrid';
  batchWindow?: number;    // seconds
  maxBatchSize?: number;   // events
  flushInterval?: number;  // ms
}

const pipelineConfig = {
  realtime_counters: {
    mode: 'streaming',
    // Used for quota checks and alerts
  },
  billing_aggregation: {
    mode: 'hybrid',
    batchWindow: 300,       // 5-minute batches
    maxBatchSize: 10000,
    flushInterval: 60000,   // 60s max wait
    // Final aggregation for Stripe reporting
  },
  analytics: {
    mode: 'batch',
    batchWindow: 3600,      // 1-hour batches
    // Long-term usage analytics
  },
};
```

Streaming is used for real-time quota enforcement and alerts. Batching is used for Stripe metering (which accepts batch usage records) and analytics. The hybrid approach processes events immediately for counters but defers billing aggregation to 5-minute windows.

## Idempotent Event Processing

Idempotency ensures that duplicate events don't result in double-billing. Each event carries an idempotency key derived from the source action. The metering service tracks processed keys in Redis with a TTL matching the deduplication window.

```typescript
class IdempotentProcessor {
  private redis: Redis;

  async processEvent(event: UsageEvent): Promise<boolean> {
    const dedupKey = `processed:${event.idempotencyKey}`;

    // Check if already processed
    const alreadyProcessed = await this.redis.setnx(dedupKey, '1');
    if (alreadyProcessed === 0) {
      logger.warn('Duplicate event detected', { key: event.idempotencyKey });
      return false; // Skip duplicate
    }

    // Set TTL for dedup window (7 days)
    await this.redis.expire(dedupKey, 7 * 24 * 60 * 60);

    // Process the event
    await this.processUsageEvent(event);
    return true;
  }

  private async processUsageEvent(event: UsageEvent): Promise<void> {
    // Increment real-time counter
    await this.realtimeCounter.increment(event.tenantId, event.meter, event.quantity);

    // Add to batch for Stripe metering
    await this.batchCollector.add(event);

    // Check quota thresholds
    await this.quotaChecker.checkThresholds(event.tenantId, event.meter);
  }
}
```

## Open-Source Tools

- **RabbitMQ** (MPL 2.0) — Message broker for usage events
- **Redis** (BSD-3) — Idempotency key storage and real-time counters
- **Stripe API** — Metered billing usage records
- **BullMQ** — Batch processing of usage records for Stripe submission

## Integration Points

The usage event pipeline connects to every billable service (voice, transcription, TTS, storage, API gateway). It feeds the real-time aggregation system (Section 3), the billing engine (Chapter 3), the quota enforcement system (Part 8), and the usage alerts (Chapter 7).

## Production Considerations

- Monitor event bus latency with percentile tracking (p99 < 100ms)
- Set up dead letter queues for failed events with manual replay
- Implement circuit breakers when downstream services (Redis, Stripe) are degraded
- Alert on event processing backlog exceeding 10,000 events
- Test event pipeline resilience with chaos engineering

## Open-Source First Philosophy

Our entire event pipeline uses open-source infrastructure: RabbitMQ for message brokering, Redis for caching and deduplication, and BullMQ for background job processing. This stack handles tens of thousands of events per second on modest hardware, eliminating the need for proprietary event streaming platforms like Confluent or AWS EventBridge.
