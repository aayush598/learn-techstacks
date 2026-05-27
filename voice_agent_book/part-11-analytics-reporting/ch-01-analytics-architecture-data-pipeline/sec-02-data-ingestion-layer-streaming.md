# Section 02: Data Ingestion Layer (Streaming)

## Overview

The data ingestion layer is the entry point for all analytics data entering the platform. It receives raw events from multiple sources — the telephony engine (call events), the voice agent runtime (transcription segments, sentiment scores), the payment engine (transaction events), and external integrations (CRM sync events) — and normalizes them into a standard event format before publishing to the event bus. The ingestion layer handles backpressure, data validation, schema enforcement, and dead-letter queuing for malformed events.

The ingestion layer is designed for maximum availability: it must accept and acknowledge events even if downstream components are temporarily unavailable. It achieves this through a write-ahead log pattern — events are written to a durable buffer (Kafka) before any processing occurs. The layer also handles late-arriving data (events that arrive minutes or hours after the event occurred) by preserving the original event timestamp and routing them to the appropriate processing window.

## Architecture

```
               Data Ingestion Layer

   Sources → Ingest API → Buffer → Validator → Event Bus
                |            |          |
                v            v          v
            Rate Limiter  Write-Ahead  Dead-Letter
                          Log          Queue
```

## Design Decisions

- **Separate ingestion API over direct Kafka writes:** Instead of allowing services to write directly to Kafka topics (which couples them to Kafka's API and schema), the ingestion layer provides an HTTP/gRPC ingestion API. Services send events to `/ingest/{eventType}` and the ingestion layer handles serialization, schema validation, partitioning, and publishing. This decouples event producers from the event bus technology. Trade-off: ingestion API adds a network hop and latency (~5ms per event) but provides schema enforcement and producer isolation.

- **Batched ingestion with configurable flush interval over single-event publishing:** The ingestion API buffers events in memory and flushes them to Kafka in batches (configurable: max 1000 events or 1 second, whichever comes first). Batching improves throughput by 10-100x compared to single-event publishing (fewer Kafka requests, better compression). The buffer is carefully sized to avoid memory pressure — each tenant has a dedicated buffer with a maximum capacity. Trade-off: batching adds up to 1 second of latency per event but dramatically improves throughput and reduces Kafka partition write amplification.

- **Schema validation at ingestion time over downstream validation:** Events are validated against the schema registry at the point of ingestion, before they enter the event bus. Invalid events are rejected with a clear error code (schema_violation, missing_required_field, type_mismatch). This prevents corrupted data from entering the analytics pipeline and ensures downstream consumers can rely on schema compliance. Schema validation uses a pre-compiled Avro/JSON Schema validator for performance. Trade-off: strict schema validation at ingress can reject valid events that use a schema version the registry has not yet been updated to recognize, requiring careful schema update coordination.

## Implementation Approach

```
interface IngestionRequest {
  eventType: string;
  events: Record<string, any>[];
  source: string;           // "telephony", "agent_runtime", "payment", "integration"
  tenantId: string;
  idempotencyKey?: string;
}

interface IngestionResponse {
  accepted: number;
  rejected: number;
  errors?: { index: number; code: string; message: string }[];
}

class DataIngestionLayer {
  private kafkaProducer: KafkaProducer;
  private schemaRegistry: SchemaRegistry;
  private rateLimiter: RateLimiter;
  private dlq: DeadLetterQueue;
  private buffers: Map<string, EventBuffer>;

  async ingest(request: IngestionRequest): Promise<IngestionResponse> {
    // Rate limit
    const allowed = await this.rateLimiter.check(`ingest:${request.tenantId}`, 1000, 1000);
    if (!allowed) {
      throw new RateLimitError('Ingestion rate limit exceeded');
    }

    const accepted: number[] = [];
    const errors: IngestionResponse['errors'] = [];

    for (let i = 0; i < request.events.length; i++) {
      const event = request.events[i];

      // Schema validation
      const schema = this.schemaRegistry.getSchema(request.eventType);
      if (!schema) {
        errors.push({ index: i, code: 'unknown_event_type', message: `Unknown event type: ${request.eventType}` });
        continue;
      }

      if (!schema.validate(event)) {
        errors.push({ index: i, code: 'schema_violation', message: schema.errors?.join(', ') || 'Validation failed' });
        continue;
      }

      // Add system fields
      event._metadata = {
        ingestedAt: new Date().toISOString(),
        source: request.source,
        tenantId: request.tenantId,
        eventType: request.eventType,
        schemaVersion: schema.version,
      };

      accepted.push(i);
    }

    // Publish accepted events to buffer
    if (accepted.length > 0) {
      const buffer = this.getBuffer(request.tenantId, request.eventType);
      const eventsToPublish = accepted.map(i => request.events[i]);
      await buffer.add(eventsToPublish);
    }

    return {
      accepted: accepted.length,
      rejected: errors.length,
      errors: errors.length > 0 ? errors : undefined,
    };
  }

  private getBuffer(tenantId: string, eventType: string): EventBuffer {
    const key = `${tenantId}:${eventType}`;
    if (!this.buffers.has(key)) {
      this.buffers.set(key, new EventBuffer({
        maxSize: 1000,
        maxAgeMs: 1000,
        topic: this.resolveTopic(eventType),
        producer: this.kafkaProducer,
        onFlush: (events) => this.onBufferFlush(events, tenantId, eventType),
      }));
    }
    return this.buffers.get(key)!;
  }

  private resolveTopic(eventType: string): string {
    const topicMap: Record<string, string> = {
      'call.started': 'events.call.started',
      'call.ended': 'events.call.ended',
      'call.transcription': 'events.call.transcription',
      'payment.succeeded': 'events.payment.succeeded',
      'payment.failed': 'events.payment.failed',
    };
    return topicMap[eventType] || `events.${eventType}`;
  }

  private async onBufferFlush(events: any[], tenantId: string, eventType: string): Promise<void> {
    try {
      await this.kafkaProducer.sendBatch({
        topic: this.resolveTopic(eventType),
        messages: events.map(e => ({
          key: e.callSid || e.transactionId || e.id,
          value: JSON.stringify(e),
          headers: {
            tenantId,
            eventType,
            schemaVersion: e._metadata.schemaVersion,
          },
        })),
      });
    } catch (error) {
      logger.error('Failed to flush events to Kafka', { tenantId, eventType, count: events.length, error });
      // Move to dead-letter queue
      await this.dlq.send(events.map(e => ({
        topic: this.resolveTopic(eventType),
        value: JSON.stringify(e),
        error: (error as Error).message,
      })));
    }
  }

  // Separate endpoint for late-arriving data
  async ingestLateEvent(request: IngestionRequest, originalTimestamp: number): Promise<IngestionResponse> {
    // Tag events as late and route to a "late events" topic
    const lateTagged = request.events.map(e => ({
      ...e,
      _metadata: {
        ...e._metadata,
        originalTimestamp,
        lateArrival: true,
      },
    }));

    return this.ingest({ ...request, events: lateTagged });
  }
}

class EventBuffer {
  private events: any[] = [];
  private lastFlush = Date.now();
  private timer: NodeJS.Timeout | null = null;

  constructor(private config: {
    maxSize: number;
    maxAgeMs: number;
    topic: string;
    producer: KafkaProducer;
    onFlush: (events: any[]) => Promise<void>;
  }) {}

  async add(events: any[]): Promise<void> {
    this.events.push(...events);

    if (this.events.length >= this.config.maxSize) {
      await this.flush();
    } else if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.config.maxAgeMs);
    }
  }

  private async flush(): Promise<void> {
    if (this.timer) { clearTimeout(this.timer); this.timer = null; }
    if (this.events.length === 0) return;

    const batch = this.events.splice(0);
    await this.config.onFlush(batch);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| KafkaJS (MIT) | Node.js | Kafka producer |
| Avro (Apache 2.0) | Schemas | Event schema serialization |
| Pino (MIT) | Logging | Ingestion audit logs |

## Production Considerations

**Scaling:** The ingestion API must be horizontally scalable — each instance maintains its own event buffers. Partition the ingestion API by tenant ID using consistent hashing to ensure events from the same tenant are processed by the same instance (improving buffer efficiency). Configure Kafka producer `acks=all` for durability and `compression.type=snappy` for throughput. Monitor event buffer sizes and flush latency — oversized buffers increase memory pressure and flush latency.

**Security:** Validate event payload size (max 1MB per event, 10MB per batch). Reject events that contain executable code or scripts. Authenticate ingestion requests using service-to-service API keys or mTLS. Log all rejected events with rejection reason for debugging. Implement field-level allowlisting — some event types may only contain specific fields. Rate limit per source service, not just per tenant.

**Monitoring:** Track events ingested per second per event type and source, schema validation pass/fail rates, buffer flush size distribution and latency, Kafka produce latency, and DLQ event count. Alert on high rejection rates (>5%), buffer flush latency exceeding 5 seconds, DLQ growth, and Kafka producer errors. Monitor per-event-type throughput to detect anomalies.
