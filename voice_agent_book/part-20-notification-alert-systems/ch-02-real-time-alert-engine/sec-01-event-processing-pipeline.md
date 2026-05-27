# Section 01: Event Processing Pipeline

## Overview

The event processing pipeline ingests raw events from multiple sources, enriches them with context, and transforms them into standardized alert candidates. Events flow through stages: ingestion → normalization → enrichment → filtering → evaluation. Apache Kafka provides durable event storage and stream processing capabilities.

## Architecture

```
┌──────────┐   ┌─────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐
│ Ingestion │   │Normalize│   │ Enrich    │   │ Filter    │   │ Evaluate │
│           │   │         │   │           │   │           │   │          │
│ REST API  │──▶│ Formats │──▶│ Add meta │──▶│ Dedup    │──▶│ Rules    │
│ Kafka     │──▶│ Schema  │──▶│ User ctx │──▶│ Throttle │──▶│ Match    │
│ SDK       │──▶│ Validate│   │ Tenants  │   │ Sampler  │   │ Score    │
└──────────┘   └─────────┘   └──────────┘   └───────────┘   └──────────┘
```

## Implementation Approach

```typescript
interface RawEvent {
  source: string;
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

interface NormalizedEvent {
  id: string;
  source: string;
  type: string;
  tenantId: string;
  userId?: string;
  metricName: string;
  metricValue: number;
  dimensions: Record<string, string>;
  timestamp: string;
}

class EventPipeline {
  async process(raw: RawEvent): Promise<void> {
    const normalized = await this.normalize(raw);
    const enriched = await this.enrich(normalized);
    const shouldProcess = await this.filter(enriched);
    if (shouldProcess) {
      await this.forwardToEvaluation(enriched);
    }
  }

  private async normalize(raw: RawEvent): Promise<NormalizedEvent> {
    const schema = this.schemaRegistry.getSchema(raw.type);
    const validated = schema.validate(raw.payload);
    return {
      id: generateId(),
      source: raw.source,
      type: raw.type,
      tenantId: validated.tenantId,
      metricName: validated.metric,
      metricValue: validated.value,
      dimensions: validated.dimensions || {},
      timestamp: raw.timestamp,
    };
  }

  private async enrich(event: NormalizedEvent): Promise<EnrichedEvent> {
    const [user, tenant, metadata] = await Promise.all([
      this.userService.getUser(event.userId),
      this.tenantService.getTenant(event.tenantId),
      this.metadataService.getMetadata(event.type),
    ]);
    return {
      ...event,
      userContext: user,
      tenantConfig: tenant,
      metadata,
    };
  }

  private async filter(event: EnrichedEvent): Promise<boolean> {
    const filters = [
      this.dedupFilter.isDuplicate(event),
      this.throttleFilter.isThrottled(event),
      this.sampleFilter.shouldSample(event),
    ];
    const results = await Promise.all(filters);
    return results.every(r => r);
  }
}
```

## Integration Points

- **Kafka Streams**: Source events published to Kafka topics
- **Schema Registry**: Event type schemas for validation
- **Pipeline Metrics**: Throughput and latency tracked per stage

## Production Considerations

- **Backpressure**: Kafka consumer lag monitoring
- **Schema Evolution**: Backward-compatible schema changes
- **Event Ordering**: Partition by tenant ID for ordered processing
