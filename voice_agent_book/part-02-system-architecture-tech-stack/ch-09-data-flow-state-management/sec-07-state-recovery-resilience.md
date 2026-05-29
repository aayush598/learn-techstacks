# Section 07: State Recovery & Resilience

## Recovery Architecture

The platform implements **crash recovery**, **event replay**, **dead letter queues**, and **state reconciliation** to ensure system resilience. Services are designed to recover from failures without data loss or inconsistency.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STATE RECOVERY & RESILIENCE                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  CRASH RECOVERY FLOW                                        │   │
│  │                                                              │   │
│  │  ┌──────────┐                                                │   │
│  │  │ Service  │     Node failure → Pod restart                │   │
│  │  │ Crashes  │                                                │   │
│  │  └────┬─────┘                                                │   │
│  │       │                                                      │   │
│  │       ▼                                                      │   │
│  │  ┌──────────┐    1. Recover last committed offset           │   │
│  │  │ Recover  │    2. Replay event store from snapshot        │   │
│  │  │ State    │    3. Rebuild in-memory state                 │   │
│  │  └────┬─────┘    4. Resume processing from last offset      │   │
│  │       │                                                      │   │
│  │       ▼                                                      │   │
│  │  ┌──────────┐                                                │   │
│  │  │ Resume   │    Service back to full operation             │   │
│  │  │ Normal   │                                                │   │
│  │  │ Operation│                                                │   │
│  │  └──────────┘                                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  EVENT REPLAY                                                │   │
│  │                                                              │   │
│  │  ┌──────────────┐     ┌──────────────┐    ┌──────────────┐  │   │
│  │  │  Select     │────→│  Replay      │───→│  Rebuild     │  │   │
│  │  │  Aggregate  │     │  Events      │    │  State       │  │   │
│  │  └────────────┘     └──────────────┘    └──────────────┘  │   │
│  │       │                                                     │   │
│  │       │  Replay scenarios:                                  │   │
│  │       │  • Bug fix: Replay events with fixed handler       │   │
│  │       │  • New read model: Replay all events               │   │
│  │       │  • Data recovery: Replay from last snapshot        │   │
│  │       │  • Audit: Replay events for time range             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  DEAD LETTER QUEUE                                          │   │
│  │                                                              │   │
│  │  ┌──────────┐   Retry(3)   ┌──────────┐   Final    ┌────┐  │   │
│  │  │  Event   │────────────→│  Retry   │───────────→│ DLQ │  │   │
│  │  │  Handler │ 1s→4s→16s  │  Handler │             └──┬──┘  │   │
│  │  └──────────┘              └──────────┘                │     │   │
│  │                                                     Manual   │   │
│  │                                                     Review   │   │
│  │                                                        │     │   │
│  │  DLQ Remediation:                                       │     │   │
│  │  • Fix bug → Replay from DLQ                           │     │   │
│  │  • Skip event → Acknowledge and discard                │     │   │
│  │  • Manual correction → Insert compensating event       │     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Crash Recovery

```typescript
interface RecoverableService {
  name: string;
  stateType: 'event-sourced' | 'stateful' | 'stateless';
  lastCommittedOffset?: string;
  lastSnapshotVersion?: number;

  // Called on startup after crash
  async recover(): Promise<void>;
}

class EventSourcedService implements RecoverableService {
  name = 'call-service';
  stateType = 'event-sourced' as const;

  constructor(
    private eventStore: EventStore,
    private snapshotRepo: SnapshotRepository,
    private kafkaConsumer: Consumer,
    private callRepository: CallRepository
  ) {}

  async recover(): Promise<void> {
    // 1. Get all active (incomplete) calls from persistent storage
    const activeCalls = await this.callRepository.getActiveCalls();

    // 2. For each active call, restore state from event store
    for (const call of activeCalls) {
      const { snapshot, eventsSinceSnapshot } = await this.snapshotRepo.getWithSnapshot(
        'call',
        call.id
      );

      const aggregate = new CallAggregate();

      if (snapshot) {
        aggregate.loadFromSnapshot(snapshot.state);
      }

      if (eventsSinceSnapshot.length > 0) {
        aggregate.loadFromHistory(eventsSinceSnapshot);
      }

      // 3. Check if call timed out during crash
      const now = Date.now();
      const lastActivity = eventsSinceSnapshot[eventsSinceSnapshot.length - 1]?.createdAt ?? snapshot?.createdAt;

      if (lastActivity && now - lastActivity.getTime() > 30_000) {
        // Call stuck during crash → auto-terminate
        aggregate.terminateAfterCrash('service_restart');
        const newEvents = aggregate.flushEvents();
        await this.eventStore.appendEvents('call', call.id, aggregate.version, newEvents);
      }

      // 4. Restore in-memory state
      this.callRepository.restoreToMemory(aggregate);
    }

    // 5. Resume Kafka consumer from last committed offset
    await this.kafkaConsumer.resume({
      fromOffset: this.lastCommittedOffset,
    });
  }
}
```

## Dead Letter Queue

```typescript
class DeadLetterQueue {
  private DLQ_TOPIC_SUFFIX = '-dlq';

  constructor(
    private kafka: Admin,
    private redis: RedisClient
  ) {}

  async sendToDLQ(originalTopic: string, event: EventEnvelope, error: Error): Promise<void> {
    const dlqTopic = `${originalTopic}${this.DLQ_TOPIC_SUFFIX}`;

    await this.kafka.produce({
      topic: dlqTopic,
      key: event.id,
      value: JSON.stringify({
        originalEvent: event,
        error: {
          message: error.message,
          stack: error.stack,
          timestamp: new Date().toISOString(),
        },
        retryCount: event.metadata?.retryCount ?? 0,
      }),
      headers: {
        'dlq-reason': error.name,
        'original-topic': originalTopic,
      },
    });

    // Alert on DLQ accumulation
    const dlqCount = await this.redis.incr(`dlq:count:${dlqTopic}`);
    if (dlqCount >= 10) {
      await alertService.sendAlert({
        severity: 'warning',
        message: `DLQ threshold exceeded: ${dlqTopic} has ${dlqCount} messages`,
      });
    }
  }

  async replayFromDLQ(dlqTopic: string, messageId: string): Promise<void> {
    const message = await this.consumeSingleMessage(dlqTopic, messageId);
    if (!message) throw new Error('Message not found in DLQ');

    const event = message.value.originalEvent;

    // Republish to original topic
    await this.kafka.produce({
      topic: message.headers['original-topic'],
      key: event.id,
      value: JSON.stringify(event),
      headers: { 'replayed-from-dlq': 'true' },
    });

    // Acknowledge removal from DLQ
    await this.commitMessage(dlqTopic, message.offset);
  }
}
```

## State Reconciliation

```typescript
// Periodic reconciliation to detect and fix inconsistencies
class StateReconciler {
  private readonly RECONCILIATION_INTERVAL = 60 * 60 * 1000; // 1 hour

  constructor(
    private callService: CallService,
    private billingService: BillingService,
    private telephonyService: TelephonyService
  ) {
    setInterval(() => this.reconcile(), this.RECONCILIATION_INTERVAL);
  }

  async reconcile(): Promise<void> {
    // 1. Find calls active > 2 hours (shouldn't happen)
    const stuckCalls = await this.callService.findCalls({
      status: { in: ['in_progress', 'ringing'] },
      startedAt: { lt: new Date(Date.now() - 2 * 60 * 60 * 1000) },
    });

    for (const call of stuckCalls) {
      // Check if call is still active on telephony provider
      const isActive = await this.telephonyService.checkCallActive(call.sipCallId);

      if (!isActive) {
        // Provider says call is done, but we missed the event
        await this.callService.forceComplete(call.id, {
          reason: 'reconciliation',
          duration: call.duration,
        });
      }
    }

    // 2. Find billing meters without matching active calls
    const activeMeters = await this.billingService.getActiveMeters();
    for (const meter of activeMeters) {
      const call = await this.callService.getCall(meter.callId);
      if (!call || call.status === 'completed' || call.status === 'failed') {
        await this.billingService.stopMeter(meter.id);
      }
    }

    // 3. Log reconciliation results
    await this.logReconciliation({
      timestamp: new Date(),
      stuckCallsFixed: stuckCalls.filter(c => !c.isActive).length,
      metersFixed: activeMeters.length,
    });
  }
}
```

## Idempotency Guarantees

```typescript
// Exactly-once processing for critical events
class ExactlyOnceProcessor {
  private processedIds = new Set<string>();

  async process(event: EventEnvelope, handler: () => Promise<void>): Promise<void> {
    // Check if already processed
    const processed = await this.redis.get(`processed:event:${event.id}`);
    if (processed) {
      return; // Already processed, skip
    }

    try {
      await handler();

      // Mark as processed (with TTL for cleanup)
      await this.redis.set(`processed:event:${event.id}`, '1', {
        EX: 60 * 60 * 24 * 7, // 7 days
      });
    } catch (error) {
      // Will retry via Kafka consumer retry mechanism
      throw error;
    }
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Recovery strategy | Event replay + snapshots | Lossless recovery, time-travel debugging |
| Failure handling | Dead letter queue + retries | No data loss, manual review for complex failures |
| Reconciliation | Periodic background job | Catches edge cases missed by event-driven flow |
| Processing guarantees | Exactly-once (dedup) for billing | Financial accuracy requirement |
| Timeout handling | Auto-termination after 30s of inactivity | Prevent orphaned resources |

## Integration Points

- **Ch 09 (Event Sourcing)** — Event store enables replay-based recovery
- **Ch 09 (Data Consistency)** — Idempotency keys support safe retries
- **Ch 10 (Incident Response)** — Recovery procedures documented in runbooks

## Production Considerations

- **Recovery Time Objective**: < 60 seconds for service restart (from crash to full operation)
- **Recovery Point Objective**: Zero data loss (events flushed to disk before acknowledge)
- **DLQ Monitoring**: Alert on DLQ > 10 messages; weekly DLQ review meeting
- **Reconciliation Scheduling**: Runs hourly during business hours, daily during off-peak
- **Testing**: Chaos engineering — random pod kills, network partitions tested weekly in staging
