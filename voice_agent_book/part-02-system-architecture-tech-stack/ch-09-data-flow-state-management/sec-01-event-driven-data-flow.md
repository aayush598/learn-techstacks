# Section 01: Event-Driven Data Flow

## Event Architecture

Events are **first-class citizens** in the architecture, enabling decoupled communication between services. Every state change is published as an event to Kafka, consumed by interested services, and stored in the event log for audit and replay.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN DATA FLOW                           │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │  Agent   │    │   Call   │    │  Voice   │    │  Billing │     │
│  │  Service │    │  Service │    │  Service │    │  Service │     │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘     │
│       │               │               │               │            │
│       ▼               ▼               ▼               ▼            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    APACHE KAFKA (Event Bus)                 │   │
│  │                                                              │   │
│  │  ┌──────────────┐  agent:created   ┌────────────────────┐  │   │
│  │  │  Agent Topic  │  agent:updated   │  Call Initiated   │  │   │
│  │  │  (6 parts)    │  agent:deleted   │  Call Ringing     │  │   │
│  │  └──────────────┘                   │  Call Connected   │  │   │
│  │  ┌──────────────┐   call:*          │  Call Completed   │  │   │
│  │  │  Call Topic   │                  │  Call Failed      │  │   │
│  │  │  (12 parts)   │                  └────────────────────┘  │   │
│  │  └──────────────┘                                           │   │
│  │  ┌──────────────┐   transcription:ready                    │   │
│  │  │  Voice Topic  │   analysis:complete                      │   │
│  │  │  (6 parts)    │                                          │   │
│  │  └──────────────┘                                           │   │
│  │  ┌──────────────┐   usage:metered                          │   │
│  │  │  Billing Topic│   invoice:generated                      │   │
│  │  │  (3 parts)    │   payment:processed                     │   │
│  │  └──────────────┘                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │               │               │               │            │
│       ▼               ▼               ▼               ▼            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │   AI     │    │  Notif.  │    │Analytics │    │  Audit   │     │
│  │  Service │    │  Service │    │(ClickHouse)│   │  Log    │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## Event Catalog

```typescript
interface EventDefinition {
  name: string;
  version: number;
  topic: string;
  producer: string;
  consumers: string[];
  schema: Record<string, unknown>;
  retention: string;        // Kafka retention period
  keySchema: string;        // Partition key
  deliverySemantics: 'at-least-once' | 'exactly-once';
}

const EVENT_CATALOG: EventDefinition[] = [
  // Agent events
  {
    name: 'agent.created',
    version: 1,
    topic: 'agent-events',
    producer: 'agent-service',
    consumers: ['search-indexer', 'analytics-service'],
    schema: {
      id: 'string',
      tenantId: 'string',
      name: 'string',
      voiceModel: 'string',
      createdAt: 'string (ISO 8601)',
    },
    keySchema: 'tenantId',
    retention: '30 days',
    deliverySemantics: 'at-least-once',
  },
  // Call events
  {
    name: 'call.completed',
    version: 2,
    topic: 'call-events',
    producer: 'call-service',
    consumers: ['billing-service', 'voice-service', 'analytics-service', 'notification-service'],
    schema: {
      callId: 'string',
      tenantId: 'string',
      agentId: 'string',
      duration: 'number (seconds)',
      status: 'enum(completed, failed, transferred)',
      startedAt: 'string',
      endedAt: 'string',
      cost: 'number',
    },
    keySchema: 'callId',
    retention: '90 days',
    deliverySemantics: 'at-least-once',
  },
];
```

## Producer/Consumer Patterns

```typescript
// Event producer pattern
class EventProducer {
  constructor(private kafka: Producer) {}

  async publish<T>(eventName: string, data: T, key: string): Promise<void> {
    const event = {
      id: crypto.randomUUID(),
      name: eventName,
      version: this.getSchemaVersion(eventName),
      timestamp: new Date().toISOString(),
      data,
      traceId: asyncLocalStorage.getStore()?.traceId,
    };

    await this.kafka.produce({
      topic: this.getTopic(eventName),
      key,
      value: JSON.stringify(event),
      headers: {
        'event-type': eventName,
        'event-version': String(event.version),
        'trace-id': event.traceId ?? '',
      },
    });
  }

  private getTopic(eventName: string): string {
    const [domain] = eventName.split('.');
    return `${domain}-events`;
  }
}

// Event consumer pattern
abstract class EventConsumer {
  abstract topic: string;
  abstract groupId: string;
  abstract handlers: Record<string, (event: EventEnvelope) => Promise<void>>;

  async process(message: KafkaMessage): Promise<void> {
    const event: EventEnvelope = JSON.parse(message.value.toString());
    const handler = this.handlers[event.name];

    if (!handler) {
      console.warn(`No handler for event: ${event.name}`);
      return;
    }

    try {
      await handler(event);
      await message.commit();
    } catch (error) {
      // Dead letter queue after retries
      await this.sendToDLQ(event, error);
    }
  }
}
```

## Event Versioning

```typescript
interface EventVersion {
  eventName: string;
  currentVersion: number;
  schema: Record<string, FieldType>;
  migrations: {
    fromVersion: number;
    toVersion: number;
    transform: (data: unknown) => unknown;
  }[];
}

// Schema evolution — always additive
const CALL_COMPLETED_VERSIONS: EventVersion = {
  eventName: 'call.completed',
  currentVersion: 2,
  schema: {
    callId: 'string',
    tenantId: 'string',
    agentId: 'string',
    duration: 'number',
    status: 'string',
    startedAt: 'string',
    endedAt: 'string',
    cost: 'number',
    // v2 additions (optional for backwards compat)
    satisfactionScore: 'number?',
    transferCount: 'number?',
  },
  migrations: [
    {
      fromVersion: 1,
      toVersion: 2,
      transform: (data: any) => ({
        ...data,
        satisfactionScore: null,
        transferCount: 0,
      }),
    },
  ],
};
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event bus | Apache Kafka | Durability, replay, high throughput, strong ordering |
| Schema evolution | Additive only, optional fields | Backward compatibility without coordination |
| Partition key | Tenant ID or entity ID | Ordered events per entity, no global ordering needed |
| Delivery semantics | At-least-once (standard), exactly-once (billing) | Performance vs accuracy trade-off per use case |
| Event format | CloudEvents spec compatible | Industry standard, schema registry ready |

## Integration Points

- **Ch 05 (Microservices)** — Kafka topics link microservices
- **Ch 09 (Event Sourcing)** — Event log feeds event store
- **Ch 09 (CQRS)** — Write path emits events consumed by read model builders
- **Ch 09 (Real-Time Pipeline)** — Events → Stream Processor → Dashboard

## Production Considerations

- **Retention**: Standard topics: 7 days; audit topics: 1 year; billing topics: 7 years
- **Partition Count**: Based on expected throughput — call-events: 12 partitions (max 12 consumers)
- **Consumer Lag**: Monitored via Prometheus; alert if > 10K messages behind
- **Dead Letter Queue**: Failed messages sent to `<topic>-dlq` with original headers for replay
- **Schema Registry**: Confluent Schema Registry (or Apicurio) for schema validation at write time
- **Idempotency**: Consumers implement idempotency keys to handle duplicate delivery
