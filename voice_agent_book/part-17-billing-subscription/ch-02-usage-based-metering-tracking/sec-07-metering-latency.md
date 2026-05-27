# Section 07: Metering Latency

## Near-Real-Time vs Batch Trade-offs

Metering latency is the time between when a usage event occurs and when it is reflected in the billing system. Different consumers of usage data have different latency requirements:

- **Quota enforcement**: < 1 second (real-time)
- **Usage dashboards**: < 10 seconds (near-real-time)
- **Alert thresholds**: < 30 seconds (near-real-time)
- **Billing aggregation**: < 5 minutes (batch)
- **Analytics**: < 1 hour (batch)

```
Latency Requirements by Consumer:
┌──────────────────────────────────────────────────────────────────┐
│ Consumer           │ Requirement │ Method        │ Stack         │
├────────────────────┼─────────────┼───────────────┼───────────────┤
│ Quota enforcement  │  < 1s       │ Streaming     │ Redis         │
│ Usage dashboard    │  < 10s      │ Streaming     │ Redis → WS    │
│ Alert thresholds   │  < 30s      │ Streaming     │ Redis → BullMQ│
│ Stripe metering    │  < 5 min    │ Micro-batch   │ BullMQ        │
│ Invoice generation │  < 1 hr     │ Batch         │ PostgreSQL    │
│ Analytics (ClickH.)│  < 1 hr     │ Batch         │ ETL pipeline  │
└──────────────────────────────────────────────────────────────────┘
```

Meeting all these latency requirements with a single pipeline is inefficient. Instead, we use a multi-lane approach where events flow through parallel processing paths optimized for each latency SLA.

```typescript
class MultiLanePipeline {
  private realtimeLane: RealtimeLane;
  private nearRealtimeLane: NearRealtimeLane;
  private batchLane: BatchLane;

  async ingest(event: UsageEvent): Promise<void> {
    // All lanes process concurrently
    await Promise.all([
      this.realtimeLane.process(event),     // Redis counters
      this.nearRealtimeLane.process(event), // Dashboard updates
      this.batchLane.queue(event),          // Queue for batch processing
    ]);
  }
}

class RealtimeLane {
  async process(event: UsageEvent): Promise<void> {
    // Redis atomic increment — sub-millisecond
    await this.redis.incrByFloat(
      `usage:${event.tenantId}:${event.meter}:${this.currentPeriod()}`,
      event.quantity
    );

    // Check quota thresholds
    await this.quotaChecker.checkRealtime(event);
  }
}

class NearRealtimeLane {
  async process(event: UsageEvent): Promise<void> {
    // Publish to WebSocket for dashboard updates
    await this.wsPublisher.publish('usage.update', {
      tenantId: event.tenantId,
      meter: event.meter,
      quantity: event.quantity,
      timestamp: event.timestamp,
    });

    // Check alert thresholds
    await this.alertChecker.checkThresholds(event);
  }
}

class BatchLane {
  private queue: Bull.Queue;

  async queue(event: UsageEvent): Promise<void> {
    await this.queue.add('processUsage', event, {
      attempts: 3,
      backoff: { type: 'exponential', delay: 2000 },
    });
  }
}
```

## Latency SLAs

Usage metering latency SLAs define the acceptable delay between event emission and availability in each system. SLAs are measured at p50, p95, and p99 percentiles.

```typescript
interface LatencySLA {
  consumer: string;
  targetP50: number; // milliseconds
  targetP95: number;
  targetP99: number;
  measurementWindow: string; // e.g., '5m', '1h'
}

const latencySLAs: LatencySLA[] = [
  { consumer: 'Redis counter', targetP50: 5, targetP95: 20, targetP99: 100, measurementWindow: '5m' },
  { consumer: 'WebSocket push', targetP50: 50, targetP95: 200, targetP99: 500, measurementWindow: '5m' },
  { consumer: 'BullMQ processing', targetP50: 1000, targetP95: 5000, targetP99: 15000, measurementWindow: '1h' },
  { consumer: 'Stripe usage record', targetP50: 120000, targetP95: 300000, targetP99: 600000, measurementWindow: '1h' },
];
```

## Eventual Consistency Tolerance

Different parts of the system tolerate staleness differently. Quota enforcement requires strong consistency (the counter must be accurate within milliseconds). Invoicing can tolerate minutes of staleness because the invoice isn't generated until the period end. Dashboards can tolerate seconds of staleness.

```
Consistency Tolerance Spectrum:
┌──────────────────────────────────────────────────────────────────┐
│ Strong                    Eventual                                │
│  Quota         Billing     Dashboards    Analytics    Reports     │
│  Enforcement   Period End  (Real-time)   (Hourly)     (Daily)    │
│  │                │            │             │           │        │
│  └────────────────┴────────────┴─────────────┴───────────┴───────  │
│  <1s              <5min        <10s          <1hr        <24hr    │
└──────────────────────────────────────────────────────────────────┘
```

## Monitoring Latency

Latency is measured end-to-end: from event emission at the service, through the event bus, processing, and final storage. Each event carries a `timestamp` field set at emission time. The pipeline records `ingestedAt` and `processedAt` timestamps for latency calculation.

```typescript
interface LatencyMeasurement {
  eventId: string;
  eventType: string;
  emitToIngest: number;     // ms
  ingestToProcess: number;  // ms
  processToStorage: number; // ms
  totalLatency: number;     // ms
}

class LatencyMonitor {
  private prometheus: PrometheusClient;

  recordLatency(event: UsageEvent, stages: LatencyStages): void {
    const emitTime = new Date(event.timestamp).getTime();
    const now = Date.now();

    this.prometheus.histogram('usage_event_latency_ms', now - emitTime, {
      event_type: event.eventType,
      stage: 'total',
    });

    this.prometheus.histogram('usage_event_stage_ms', stages.queueWait, {
      event_type: event.eventType,
      stage: 'queue_wait',
    });

    this.prometheus.histogram('usage_event_stage_ms', stages.processing, {
      event_type: event.eventType,
      stage: 'processing',
    });
  }
}
```

## Open-Source Tools

- **Prometheus** (Apache 2.0) — Latency metrics collection
- **Grafana** (Apache 2.0) — Latency dashboards and alerting
- **OpenTelemetry** (Apache 2.0) — Distributed tracing for end-to-end latency
- **Redis** (BSD-3) — Ultra-low-latency counters
- **RabbitMQ** (MPL 2.0) — Event queue with latency guarantees

## Integration Points

Latency concerns affect all pipeline consumers: real-time dashboards need fast updates, the alert engine needs timely threshold crossing, the billing engine needs accurate but not instant aggregation, and Stripe accepts batch submissions.

## Production Considerations

- Set latency budgets for each pipeline stage
- Implement backpressure when processing falls behind
- Use circuit breakers to protect downstream from overload
- Monitor queue depth as leading indicator of latency issues
- Scale consumers based on queue depth metrics
- Plan for latency degradation during traffic spikes

## Open-Source First Philosophy

OpenTelemetry provides distributed tracing across the entire metering pipeline without vendor lock-in. Prometheus and Grafana deliver enterprise-grade monitoring at zero licensing cost. Redis provides sub-millisecond counter updates that would require expensive in-memory databases from proprietary vendors. This stack achieves sub-second metering latency at a fraction of the cost of commercial APM and caching solutions.
