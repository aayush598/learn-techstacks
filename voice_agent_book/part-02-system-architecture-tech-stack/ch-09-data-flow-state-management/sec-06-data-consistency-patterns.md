# Section 06: Data Consistency Patterns

## Consistency Challenges

Distributed transactions across microservices require careful patterns to maintain data consistency. The platform uses **Saga pattern** for multi-step operations, **Outbox pattern** for reliable event publishing, and **Idempotency keys** for safe retries.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA CONSISTENCY PATTERNS                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SAGA PATTERN (Choreography)                                │   │
│  │                                                              │   │
│  │  InitiateCall Saga:                                         │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────┐  │   │
│  │  │  1.      │───→│  2.      │───→│  3.      │───→│  4.  │  │   │
│  │  │ Reserve  │    │ Initiate │    │ Start    │    │ Notify│  │   │
│  │  │ Capacity │    │ Call     │    │ Billing  │    │ User  │  │   │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────┘  │   │
│  │       │                │               │            │       │   │
│  │       ▼                ▼               ▼            ▼       │   │
│  │  Compensating: Release capacity if subsequent steps fail     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  OUTBOX PATTERN                                             │   │
│  │                                                              │   │
│  │  ┌──────────────┐     ┌──────────────┐     ┌────────────┐  │   │
│  │  │  API Request  │────→│  Transaction  │────→│  Database  │  │   │
│  │  │  (Create      │     │  1. Insert    │     │  (Agent +  │  │   │
│  │  │   Agent)      │     │     agent     │     │   Outbox)  │  │   │
│  │  └──────────────┘     │  2. Insert     │     └────────────┘  │   │
│  │                       │     outbox msg │            │         │   │
│  │                       └──────────────┘            │           │   │
│  │                                                     ▼         │   │
│  │                                            ┌──────────────┐   │   │
│  │                                            │  Outbox      │   │   │
│  │                                            │  Relay       │   │   │
│  │                                            │  → Kafka     │   │   │
│  │                                            └──────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  IDEMPOTENCY KEY PATTERN                                    │   │
│  │                                                              │   │
│  │  ┌──────────┐   Idempotency-Key   ┌──────────┐   Hash ───→ │   │
│  │  │  Client  │───: header ─────────→│  Service  │─────────→  │   │
│  │  │  Retry   │                      │           │   Cache    │   │
│  │  └──────────┘                      └──────────┘   Check     │   │
│  │       │                                │            │        │   │
│  │       └────────────────────────────────┘────────────┘        │   │
│  │              Duplicate detected → Return cached response     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Saga Pattern Implementation

```typescript
// Choreographed saga — each service emits events that trigger next step
interface SagaStep<TContext> {
  name: string;
  service: string;
  execute: (context: TContext) => Promise<void>;
  compensate: (context: TContext) => Promise<void>;
}

// Initiate Call Saga
class InitiateCallSaga {
  private steps: SagaStep<CallContext>[] = [
    {
      name: 'reserve-capacity',
      service: 'telephony-service',
      execute: async (ctx) => {
        ctx.capacityReservation = await telephonyService.reserveCapacity(ctx.tenantId);
      },
      compensate: async (ctx) => {
        await telephonyService.releaseCapacity(ctx.capacityReservation!);
      },
    },
    {
      name: 'initiate-call',
      service: 'call-service',
      execute: async (ctx) => {
        ctx.sipCallId = await callService.initiateCall(ctx.phoneNumber, ctx.callerId);
      },
      compensate: async (ctx) => {
        await callService.terminateCall(ctx.sipCallId!);
      },
    },
    {
      name: 'start-billing',
      service: 'billing-service',
      execute: async (ctx) => {
        ctx.billingId = await billingService.startMeter(ctx.tenantId, ctx.agentId);
      },
      compensate: async (ctx) => {
        await billingService.cancelMeter(ctx.billingId!);
      },
    },
  ];

  async execute(context: CallContext): Promise<void> {
    const executedSteps: SagaStep<CallContext>[] = [];

    for (const step of this.steps) {
      try {
        await step.execute(context);
        executedSteps.push(step);
      } catch (error) {
        // Compensate in reverse order
        for (const executed of executedSteps.reverse()) {
          await executed.compensate(context).catch((e) => {
            console.error(`Saga compensation failed for ${executed.name}:`, e);
            // Log compensation failure for manual intervention
          });
        }
        throw new SagaError(`Saga failed at step ${step.name}`, error);
      }
    }
  }
}
```

## Outbox Pattern Implementation

```typescript
// Outbox table: stores events atomically with domain data
// CREATE TABLE outbox_messages (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   aggregate_type VARCHAR(100) NOT NULL,
//   aggregate_id VARCHAR(100) NOT NULL,
//   event_type VARCHAR(100) NOT NULL,
//   event_data JSONB NOT NULL,
//   metadata JSONB NOT NULL DEFAULT '{}',
//   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//   processed_at TIMESTAMPTZ,
//   retry_count INTEGER DEFAULT 0,
//   last_error TEXT
// );

class OutboxRelay {
  private readonly BATCH_SIZE = 100;
  private readonly POLL_INTERVAL = 1000; // 1 second

  constructor(
    private db: PrismaClient,
    private kafka: Producer
  ) {
    setInterval(() => this.processOutbox(), this.POLL_INTERVAL);
  }

  async processOutbox(): Promise<void> {
    const messages = await this.db.outboxMessage.findMany({
      where: { processedAt: null, retryCount: { lt: 3 } },
      orderBy: { createdAt: 'asc' },
      take: this.BATCH_SIZE,
    });

    for (const message of messages) {
      try {
        await this.kafka.produce({
          topic: this.getTopic(message.eventType),
          key: message.aggregateId,
          value: JSON.stringify({
            id: message.id,
            type: message.eventType,
            data: message.eventData,
            metadata: message.metadata,
            timestamp: message.createdAt.toISOString(),
          }),
        });

        await this.db.outboxMessage.update({
          where: { id: message.id },
          data: { processedAt: new Date() },
        });
      } catch (error) {
        await this.db.outboxMessage.update({
          where: { id: message.id },
          data: {
            retryCount: { increment: 1 },
            lastError: String(error),
          },
        });
      }
    }
  }
}

// Usage: Insert agent and outbox message in same transaction
async function createAgent(data: CreateAgentInput, tenantId: string): Promise<Agent> {
  return await prisma.$transaction(async (tx) => {
    const agent = await tx.agent.create({
      data: { ...data, tenantId },
    });

    await tx.outboxMessage.create({
      data: {
        aggregateType: 'agent',
        aggregateId: agent.id,
        eventType: 'agent.created',
        eventData: agent,
        metadata: { tenantId },
      },
    });

    return agent;
  });
}
```

## Idempotency Key Pattern

```typescript
// Idempotency middleware
class IdempotencyMiddleware {
  private readonly KEY_TTL = 60 * 60 * 24; // 24 hours

  async process(request: NextRequest, handler: () => Promise<NextResponse>): Promise<NextResponse> {
    const idempotencyKey = request.headers.get('Idempotency-Key');
    if (!idempotencyKey) {
      return handler(); // No key → normal processing
    }

    // Check if already processed
    const cached = await this.redis.get(`idempotency:${idempotencyKey}`);
    if (cached) {
      const cachedResponse = JSON.parse(cached);
      return NextResponse.json(cachedResponse.body, {
        status: cachedResponse.status,
        headers: { 'Idempotency-Key-Replayed': 'true' },
      });
    }

    // Process and cache result
    const response = await handler();
    const body = await response.clone().json();

    await this.redis.set(
      `idempotency:${idempotencyKey}`,
      JSON.stringify({ status: response.status, body }),
      { EX: this.KEY_TTL }
    );

    return response;
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Saga type | Choreography (event-driven) | No central orchestrator, services are loosely coupled |
| Event reliability | Outbox pattern | Guaranteed delivery, no dual-write problem |
| Retry safety | Idempotency keys | Safe client retries without duplicate side effects |
| Compensating actions | Reverse order execution | Clean rollback of partial operations |
| Dead letter queue | Failed events with retry count | Manual intervention for persistent failures |

## Integration Points

- **Ch 05 (Microservices)** — Sagas coordinate across service boundaries
- **Ch 09 (Event-Driven Data Flow)** — Outbox feeds Kafka events
- **Ch 09 (State Recovery)** — Idempotency supports crash recovery
- **Ch 09 (Event Sourcing)** — Saga events are part of the event log

## Production Considerations

- **Saga Timeout**: Each saga step has a 30-second timeout; total saga timeout: 5 minutes
- **Compensation Reliability**: Compensating actions are retried with exponential backoff; manual queue for failures
- **Outbox Scalability**: Outbox partitioned by aggregate type; each partition has dedicated relay
- **Idempotency Key Conflict**: Duplicate key within TTL returns cached response; duplicate key after TTL returns 409 Conflict
- **Monitoring**: Saga duration, step success/failure, outbox queue depth, idempotency hit rate tracked in Prometheus
