# Section 03: CQRS (Command Query Responsibility Segregation)

## CQRS Architecture

CQRS separates the **write path** (commands that change state) from the **read path** (queries that return data). Writes go to PostgreSQL (normalized, ACID-compliant), while reads come from materialized views and ClickHouse (denormalized, optimized for queries).

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CQRS ARCHITECTURE                                │
│                                                                     │
│  ┌──────────────────┐               ┌──────────────────┐           │
│  │    COMMAND SIDE   │               │     QUERY SIDE    │           │
│  │    (Writes)       │               │     (Reads)       │           │
│  │                   │               │                   │           │
│  │  POST /api/v1/    │               │  GET /api/v1/     │           │
│  │  calls/initiate   │               │  calls?status=... │           │
│  │       │           │               │       │           │           │
│  │       ▼           │               │       ▼           │           │
│  │  ┌──────────┐     │               │  ┌──────────┐     │           │
│  │  │ Command  │     │               │  │  Query   │     │           │
│  │  │ Handler  │     │               │  │  Handler │     │           │
│  │  └────┬─────┘     │               │  └────┬─────┘     │           │
│  │       │           │               │       │           │           │
│  │       ▼           │               │       ▼           │           │
│  │  ┌──────────┐     │               │  ┌──────────┐     │           │
│  │  │ Validate │     │               │  │ Material │     │           │
│  │  │ (Zod)    │     │               │  │ View     │     │           │
│  │  └────┬─────┘     │               │  │ (Read    │     │           │
│  │       │           │               │  │  Model)  │     │           │
│  │       ▼           │               │  └────┬─────┘     │           │
│  │  ┌──────────┐     │               │       │           │           │
│  │  │  Write   │     │               │  ┌────┴────┐      │           │
│  │  │  to      │     │               │  │PostgreSQL│      │           │
│  │  │PostgreSQL│     │               │  │ClickHouse│      │           │
│  │  └────┬─────┘     │               │  │  Redis   │      │           │
│  │       │           │               │  └─────────┘      │           │
│  │       ▼           │               └──────────────────┘           │
│  │  ┌──────────┐     │                                             │
│  │  │ Emit     │     │  ┌──────────────────────────────────────┐   │
│  │  │ Event to │─────│─→│  Event → Kafka → Materialized View   │   │
│  │  │ Kafka    │     │  │  Builder updates read models          │   │
│  │  └──────────┘     │  └──────────────────────────────────────┘   │
│  └──────────────────┘                                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Command Handler Pattern

```typescript
// Commands — imperative, side-effectful
interface Command<TResult = void> {
  type: string;
  handler: (payload: unknown) => Promise<TResult>;
}

// Command: InitiateCall
interface InitiateCallCommand {
  type: 'INITIATE_CALL';
  payload: {
    tenantId: string;
    agentId: string;
    phoneNumber: string;
    callerId?: string;
    scheduledAt?: Date;
  };
}

class InitiateCallHandler implements Command<CallResponse> {
  constructor(
    private callRepo: CallRepository,
    private agentRepo: AgentRepository,
    private telephonyService: TelephonyService,
    private eventBus: EventProducer
  ) {}

  async execute(payload: InitiateCallCommand['payload']): Promise<CallResponse> {
    // 1. Validate
    const agent = await this.agentRepo.getById(payload.agentId);
    if (!agent || !agent.isActive) {
      throw new Error('Agent not found or inactive');
    }

    if (agent.tenantId !== payload.tenantId) {
      throw new Error('Agent does not belong to tenant');
    }

    // 2. Check rate limits
    const canInitiate = await this.telephonyService.checkRateLimit(payload.tenantId);
    if (!canInitiate) {
      throw new Error('Rate limit exceeded');
    }

    // 3. Create call record
    const call = await this.callRepo.create({
      tenantId: payload.tenantId,
      agentId: payload.agentId,
      phoneNumber: payload.phoneNumber,
      status: 'queued',
      createdAt: new Date(),
    });

    // 4. Initiate outbound call
    const telephonyResult = await this.telephonyService.initiateCall({
      callId: call.id,
      from: payload.callerId ?? agent.defaultCallerId,
      to: payload.phoneNumber,
    });

    // 5. Update state
    await this.callRepo.updateState(call.id, 'ringing', telephonyResult.sipCallId);

    // 6. Emit event
    await this.eventBus.publish('call.initiated', {
      callId: call.id,
      tenantId: payload.tenantId,
      agentId: payload.agentId,
    }, payload.tenantId);

    return { callId: call.id, status: 'ringing' };
  }
}
```

## Read Model / Materialized View

```typescript
// Read models — optimized for specific query patterns
interface CallsListReadModel {
  id: string;
  agentName: string;
  phoneNumber: string;
  status: string;
  duration: number;
  cost: number;
  startedAt: Date;
  endedAt?: Date;
  sentiment?: string;
}

// Materialized view builder — subscribes to events and updates read models
class CallsReadModelBuilder {
  constructor(
    private db: PrismaClient,
    private clickhouse: ClickHouseClient,
    private redis: RedisClient
  ) {}

  async onCallInitiated(event: CallEvent<'initiated'>): Promise<void> {
    await this.db.callReadModel.upsert({
      where: { id: event.data.callId },
      update: { status: 'ringing' },
      create: {
        id: event.data.callId,
        tenantId: event.data.tenantId,
        agentId: event.data.agentId,
        status: 'ringing',
        startedAt: new Date(event.timestamp),
      },
    });

    // Update aggregate in ClickHouse
    await this.clickhouse.insert({
      table: 'call_metrics_hourly',
      values: [{
        tenant_id: event.data.tenantId,
        agent_id: event.data.agentId,
        hour: truncateToHour(event.timestamp),
        initiated_count: 1,
      }],
    });
  }

  async onCallCompleted(event: CallEvent<'completed'>): Promise<void> {
    await this.db.callReadModel.update({
      where: { id: event.data.callId },
      data: {
        status: 'completed',
        duration: event.data.duration,
        cost: event.data.cost,
        endedAt: new Date(event.timestamp),
      },
    });
  }
}
```

## Query Handler

```typescript
// Query handlers — pure, no side effects
interface Query<TResult> {
  type: string;
  handler: (params: unknown) => Promise<TResult>;
}

class GetCallsListQuery implements Query<PaginatedResult<CallsListReadModel>> {
  constructor(private db: PrismaClient) {}

  async execute(params: {
    tenantId: string;
    status?: string;
    agentId?: string;
    fromDate?: string;
    toDate?: string;
    page: number;
    pageSize: number;
  }): Promise<PaginatedResult<CallsListReadModel>> {
    const where: any = { tenantId: params.tenantId };

    if (params.status) where.status = params.status;
    if (params.agentId) where.agentId = params.agentId;
    if (params.fromDate || params.toDate) {
      where.startedAt = {};
      if (params.fromDate) where.startedAt.gte = new Date(params.fromDate);
      if (params.toDate) where.startedAt.lte = new Date(params.toDate);
    }

    const [items, total] = await Promise.all([
      this.db.callReadModel.findMany({
        where,
        skip: (params.page - 1) * params.pageSize,
        take: params.pageSize,
        orderBy: { startedAt: 'desc' },
      }),
      this.db.callReadModel.count({ where }),
    ]);

    return { items, total, page: params.page, pageSize: params.pageSize };
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CQRS scope | Per-service (not global) | Each service decides its own read/write separation |
| Read model storage | PostgreSQL (same instance, different tables) | Simple, consistent, no cross-database complexity |
| Analytics reads | ClickHouse | Optimized for time-series aggregations |
| Cache layer | Redis for hot data | Dashboard summaries, active calls, real-time metrics |
| Eventual consistency | Seconds-level lag for read models | Acceptable for dashboard, not for call state machine |

## Integration Points

- **Ch 09 (Event-Driven Data Flow)** — Events trigger read model updates
- **Ch 09 (Event Sourcing)** — Event store is the write-side source of truth
- **Ch 03 (Database)** — PostgreSQL write schema vs read schema
- **Ch 06 (Frontend)** — TanStack Query prefetches read models for SSR

## Production Considerations

- **Consistency Guarantees**: Call state machine reads its own writes (strong consistency); dashboard reads are eventually consistent
- **Read Model Freshness**: Dashboard shows "last updated 2s ago" indicator for eventual consistency
- **Cache Invalidation**: Redis cache evicted on read model update event; stale-while-revalidate pattern
- **Write Scaling**: Command handlers are the bottleneck — scale horizontally with partitioned Kafka consumers
- **Read Scaling**: Read models served from read replicas; ClickHouse for analytics; Redis for hot data
