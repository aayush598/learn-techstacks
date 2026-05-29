# Section 04: Event Sourcing for Audit

## Event Store Architecture

Event sourcing stores every state change as an **append-only event log**. The current state is derived by replaying events. This provides a complete audit trail, enables time-travel debugging, and supports rebuilding read models from scratch.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EVENT SOURCING ARCHITECTURE                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    EVENT STORE                                │   │
│  │  (Append-only log in PostgreSQL + Kafka)                     │   │
│  │                                                              │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │   │
│  │  │Event │ │Event │ │Event │ │Event │ │Event │ │Event │    │   │
│  │  │  #1  │ │  #2  │ │  #3  │ │  #4  │ │  #5  │ │  #6  │    │   │
│  │  │Call  │ │Call  │ │Call  │ │Call  │ │Call  │ │Call  │    │   │
│  │  │Init  │ │Ring  │ │Conn  │ │Pause │ │Resume│ │Comp  │    │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │  ↑ Appended (immutable)                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│          ┌───────────────────┼───────────────────┐                │
│          ▼                   ▼                   ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐        │
│  │  Read Model  │  │  Snapshot    │  │  Audit Trail     │        │
│  │  (Current    │  │  (Point-in-  │  │  (Immutable      │        │
│  │   State)     │  │   time)      │  │   Record)        │        │
│  └──────────────┘  └──────────────┘  └──────────────────┘        │
│                                                                     │
│  Example: Replaying events for call ABC-123                        │
│  1. CallInitiated    → { status: 'queued', createdAt: T1 }       │
│  2. CallRinging      → { status: 'ringing' }                      │
│  3. CallConnected    → { status: 'connected', connectedAt: T3 }  │
│  4. CallPaused       → { status: 'paused', pauseDuration: 30 }   │
│  5. CallResumed      → { status: 'in_progress' }                  │
│  6. CallCompleted    → { status: 'completed', duration: 245 }     │
│  ──────────────────────────────────────────────────────────────    │
│  Final state: Completed, duration 245s                            │
└─────────────────────────────────────────────────────────────────────┘
```

## Event Store Implementation

```typescript
// Event store table
// PostgreSQL schema
// CREATE TABLE event_store (
//   id BIGSERIAL PRIMARY KEY,
//   aggregate_type VARCHAR(50) NOT NULL,
//   aggregate_id VARCHAR(100) NOT NULL,
//   version INTEGER NOT NULL,
//   event_type VARCHAR(100) NOT NULL,
//   event_data JSONB NOT NULL,
//   metadata JSONB NOT NULL DEFAULT '{}',
//   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//   UNIQUE(aggregate_type, aggregate_id, version)
// );

interface StoredEvent {
  id: number;
  aggregateType: string;
  aggregateId: string;
  version: number;
  eventType: string;
  eventData: unknown;
  metadata: {
    tenantId: string;
    userId: string;
    correlationId: string;
    causationId?: string;    // Event that caused this event
    timestamp: string;
  };
  createdAt: Date;
}

class EventStore {
  constructor(private db: PrismaClient) {}

  async appendEvents(
    aggregateType: string,
    aggregateId: string,
    expectedVersion: number,
    events: NewEvent[]
  ): Promise<StoredEvent[]> {
    // Optimistic concurrency: version must match
    const stored = await this.db.$transaction(async (tx) => {
      const current = await tx.eventStore.findFirst({
        where: { aggregateType, aggregateId },
        orderBy: { version: 'desc' },
        select: { version: true },
      });

      if (current && current.version !== expectedVersion) {
        throw new ConcurrencyError(
          `Expected version ${expectedVersion}, got ${current.version}`
        );
      }

      const startVersion = (current?.version ?? 0) + 1;
      const created = [];

      for (let i = 0; i < events.length; i++) {
        const event = await tx.eventStore.create({
          data: {
            aggregateType,
            aggregateId,
            version: startVersion + i,
            eventType: events[i].type,
            eventData: events[i].data,
            metadata: events[i].metadata,
          },
        });
        created.push(event);
      }

      return created;
    });

    return stored;
  }

  async getEvents(
    aggregateType: string,
    aggregateId: string,
    fromVersion?: number
  ): Promise<StoredEvent[]> {
    return this.db.eventStore.findMany({
      where: {
        aggregateType,
        aggregateId,
        version: fromVersion ? { gte: fromVersion } : undefined,
      },
      orderBy: { version: 'asc' },
    });
  }
}
```

## Aggregate Root Pattern

```typescript
// Aggregate root — loads state from events, applies commands, produces events
abstract class AggregateRoot {
  protected version = 0;
  protected changes: NewEvent[] = [];

  abstract get aggregateType(): string;
  abstract get aggregateId(): string;

  // Rebuild state from events
  protected abstract applyEvent(event: StoredEvent): void;

  loadFromHistory(events: StoredEvent[]): void {
    for (const event of events) {
      this.applyEvent(event);
      this.version = event.version;
    }
  }

  // Record a new event
  protected recordEvent(type: string, data: unknown): void {
    this.changes.push({
      type,
      data,
      metadata: {
        tenantId: this.getTenantId(),
        userId: this.getUserId(),
      },
    });
  }

  // Flush to event store
  async flush(eventStore: EventStore): Promise<StoredEvent[]> {
    if (this.changes.length === 0) return [];

    const stored = await eventStore.appendEvents(
      this.aggregateType,
      this.aggregateId,
      this.version,
      this.changes
    );

    // Apply new events to state
    for (const event of stored) {
      this.applyEvent(event);
    }

    this.version = stored[stored.length - 1].version;
    this.changes = [];

    return stored;
  }
}

// Call aggregate example
class CallAggregate extends AggregateRoot {
  private id: string;
  private tenantId: string;
  private status: CallState = 'idle';
  private duration = 0;

  get aggregateType(): string { return 'call'; }
  get aggregateId(): string { return this.id; }

  initiateCall(phoneNumber: string, agentId: string): void {
    if (this.status !== 'idle') {
      throw new Error('Call already initiated');
    }
    this.recordEvent('call.initiated', { phoneNumber, agentId });
  }

  completeCall(): void {
    if (this.status !== 'in_progress') {
      throw new Error('Call must be in progress to complete');
    }
    this.recordEvent('call.completed', { duration: this.duration });
  }

  protected applyEvent(event: StoredEvent): void {
    switch (event.eventType) {
      case 'call.initiated':
        this.id = event.aggregateId;
        this.tenantId = event.metadata.tenantId;
        this.status = 'queued';
        break;
      case 'call.completed':
        this.status = 'completed';
        this.duration = (event.eventData as any).duration;
        break;
    }
  }
}
```

## Snapshots

```typescript
// Snapshot to avoid replaying millions of events
interface Snapshot {
  aggregateType: string;
  aggregateId: string;
  version: number;
  state: unknown;
  createdAt: Date;
}

class SnapshotRepository {
  private SNAPSHOT_INTERVAL = 100; // Snapshot every 100 events

  async getWithSnapshot(aggregateType: string, aggregateId: string): Promise<{
    snapshot: Snapshot | null;
    eventsSinceSnapshot: StoredEvent[];
  }> {
    const snapshot = await this.db.snapshot.findFirst({
      where: { aggregateType, aggregateId },
      orderBy: { version: 'desc' },
    });

    const events = await this.eventStore.getEvents(
      aggregateType,
      aggregateId,
      snapshot ? snapshot.version + 1 : undefined
    );

    return { snapshot, eventsSinceSnapshot: events };
  }

  async createSnapshot(
    aggregate: AggregateRoot,
    currentState: unknown
  ): Promise<void> {
    if (aggregate.version % this.SNAPSHOT_INTERVAL !== 0) return;

    await this.db.snapshot.upsert({
      where: {
        aggregateType_aggregateId_version: {
          aggregateType: aggregate.aggregateType,
          aggregateId: aggregate.aggregateId,
          version: aggregate.version,
        },
      },
      update: { state: currentState },
      create: {
        aggregateType: aggregate.aggregateType,
        aggregateId: aggregate.aggregateId,
        version: aggregate.version,
        state: currentState,
      },
    });
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event store | PostgreSQL (relational) + Kafka (pub/sub) | PG for durable storage, Kafka for event distribution |
| Schema | JSONB for event data | Flexible schema, indexable via GIN |
| Concurrency | Optimistic concurrency (version check) | No locks, retry on conflict |
| Snapshot strategy | Every 100 events | Balances replay performance vs storage overhead |
| Audit compliance | Append-only, no deletes, TTL-based archival | Immutable audit trail for compliance |

## Integration Points

- **Ch 09 (CQRS)** — Event store feeds read model builders
- **Ch 09 (Event-Driven Data Flow)** — Events published to Kafka after append
- **Ch 09 (State Recovery)** — Replay events to rebuild state after crash
- **Ch 10 (Security)** — Audit trail for security incidents

## Production Considerations

- **Storage Growth**: ~1KB per event, 1M events/day = ~1GB/day; archived to ClickHouse after 90 days
- **Replay Performance**: Snapshot every 100 events keeps replay < 100ms for aggregates with 10K events
- **Data Retention**: Event store retained for 7 years (compliance); archived to MinIO after 1 year
- **Debugging**: Time-travel debugging — replay events up to a specific timestamp to reproduce state
- **GDPR Compliance**: Events are pseudonymized; PII stored separately with foreign key references
