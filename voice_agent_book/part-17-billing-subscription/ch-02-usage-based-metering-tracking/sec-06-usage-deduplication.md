# Section 06: Usage Deduplication

## Idempotency Keys

Idempotency keys are the foundation of exactly-once processing. Every usage event carries a unique key derived from the source transaction that generated it. If the same key is submitted multiple times, the system recognizes the duplicate and ignores subsequent submissions.

The idempotency key format follows a convention: `{meter}:{source_id}:{action}`. This ensures that retrying the same operation produces the same key, while different operations always produce different keys.

```typescript
interface IdempotencyRecord {
  key: string;
  status: 'processing' | 'completed' | 'failed';
  eventId?: string;
  firstSeen: number;     // Unix timestamp
  lastSeen: number;
  retryCount: number;
  expiresAt: number;     // TTL for key expiration
}

class IdempotencyService {
  private redis: Redis;
  private readonly DEFAULT_TTL = 7 * 24 * 60 * 60; // 7 days
  private readonly PROCESSING_TTL = 60; // 60 seconds

  async processEvent(
    event: UsageEvent,
    processor: (event: UsageEvent) => Promise<void>
  ): Promise<void> {
    const key = this.buildKey(event);

    // Try to acquire processing lock
    const locked = await this.redis.setnx(
      `idempotent:lock:${key}`,
      JSON.stringify({ status: 'processing', firstSeen: Date.now() })
    );

    if (locked === 0) {
      // Key exists — check status
      const existing = await this.getRecord(key);
      switch (existing.status) {
        case 'completed':
          logger.info('Idempotent: already processed', { key });
          return; // Safe to skip
        case 'processing':
          // Check if processing has timed out
          if (Date.now() - existing.firstSeen > this.PROCESSING_TTL * 1000) {
            logger.warn('Idempotent: stale processing lock, retrying', { key });
            break; // Continue to process
          }
          logger.info('Idempotent: currently processing', { key });
          return; // Wait for the other process
        case 'failed':
          // Previous attempt failed — retry
          logger.info('Idempotent: retrying failed event', { key });
          break;
      }
    }

    // Set TTL on lock
    await this.redis.expire(`idempotent:lock:${key}`, this.PROCESSING_TTL);

    try {
      // Process the event
      await processor(event);

      // Mark as completed
      await this.redis.setex(
        `idempotent:status:${key}`,
        this.DEFAULT_TTL,
        JSON.stringify({ status: 'completed', eventId: event.id })
      );

      // Release lock
      await this.redis.del(`idempotent:lock:${key}`);
    } catch (error) {
      // Mark as failed
      await this.redis.setex(
        `idempotent:status:${key}`,
        this.DEFAULT_TTL,
        JSON.stringify({ status: 'failed', error: error.message })
      );

      // Release lock
      await this.redis.del(`idempotent:lock:${key}`);
      throw error;
    }
  }

  private buildKey(event: UsageEvent): string {
    return event.idempotencyKey;
  }

  private async getRecord(key: string): Promise<IdempotencyRecord> {
    const lockData = await this.redis.get(`idempotent:lock:${key}`);
    const statusData = await this.redis.get(`idempotent:status:${key}`);

    return {
      key,
      status: lockData
        ? JSON.parse(lockData).status
        : statusData
          ? JSON.parse(statusData).status
          : 'unknown',
      firstSeen: lockData ? JSON.parse(lockData).firstSeen : 0,
      lastSeen: Date.now(),
      retryCount: lockData ? JSON.parse(lockData).retryCount || 0 : 0,
      expiresAt: Date.now() + this.DEFAULT_TTL * 1000,
    };
  }
}
```

## Exactly-Once Processing

Exactly-once processing guarantees that each event is processed exactly one time, even if the service restarts, the network fails, or the event is delivered multiple times. This is achieved through a combination of idempotency keys, atomic Redis operations, and write-audit logging.

```
Exactly-Once Processing Flow:
┌────────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
│   Service  │────>│  Event   │────>│  Processor │────>│ Storage  │
│            │     │   Bus    │     │            │     │          │
│ Emit event │     │ RabbitMQ │     │ Check dup  │     │ Write    │
│ with key   │     │ at-least │     │ in Redis   │     │ once     │
│            │     │ once     │     │            │     │          │
└────────────┘     └──────────┘     └─────┬──────┘     └──────────┘
                                          │
                                   ┌──────┴──────┐
                                   │  Idempotent │
                                   │   Registry  │
                                   │  (Redis)    │
                                   │  TTL: 7d    │
                                   └─────────────┘
```

## Dedup Window Configuration

The dedup window defines how long idempotency keys are retained. A 7-day window covers the maximum billing period plus a grace period for late-arriving events. Keys can be extended for specific scenarios (e.g., disputed events under investigation).

```typescript
interface DedupConfig {
  defaultWindowMs: number;
  maxWindowMs: number;
  extensionReason: string;
}

const dedupConfigs: Record<string, DedupConfig> = {
  call_minutes: {
    defaultWindowMs: 7 * 24 * 60 * 60 * 1000,  // 7 days
    maxWindowMs: 30 * 24 * 60 * 60 * 1000,     // 30 days
    extensionReason: 'extended_billing_dispute',
  },
  transcription: {
    defaultWindowMs: 7 * 24 * 60 * 60 * 1000,
    maxWindowMs: 14 * 24 * 60 * 60 * 1000,
    extensionReason: null,
  },
};
```

## Conflict Resolution

When duplicate events are detected but have conflicting data (e.g., different quantities), a conflict resolution strategy determines which data to use. This is rare but must be handled to prevent data corruption.

```typescript
enum ConflictStrategy {
  FIRST_WINS,     // Use the first event received
  LAST_WINS,      // Use the most recent event
  HIGHEST_QUANTITY,  // Use the largest quantity (safer for billing)
  LOWEST_QUANTITY,   // Use the smallest quantity (conservative)
  REJECT_BOTH,    // Flag for manual review
}

class DedupConflictResolver {
  async resolve(
    existing: UsageEvent,
    incoming: UsageEvent,
    strategy: ConflictStrategy
  ): Promise<UsageEvent> {
    switch (strategy) {
      case ConflictStrategy.FIRST_WINS:
        return existing;
      case ConflictStrategy.LAST_WINS:
        return new Date(incoming.timestamp) > new Date(existing.timestamp)
          ? incoming
          : existing;
      case ConflictStrategy.HIGHEST_QUANTITY:
        return incoming.quantity > existing.quantity ? incoming : existing;
      case ConflictStrategy.LOWEST_QUANTITY:
        return incoming.quantity < existing.quantity ? incoming : existing;
      case ConflictStrategy.REJECT_BOTH:
        await this.manualReviewQueue.send({
          existingEvent: existing,
          incomingEvent: incoming,
          reason: 'conflict_resolution_required',
        });
        return null; // Neither is processed
    }
  }
}
```

## Open-Source Tools

- **Redis** (BSD-3) — Idempotency key storage with TTL and atomic operations
- **Redlock** (MIT) — Distributed lock implementation for idempotency
- **BullMQ** (MIT) — Processing queue with built-in dedup support
- **PostgreSQL** (PostgreSQL) — Persistent storage for idempotency audit log

## Integration Points

Deduplication integrates with every usage event producer (voice services, transcription, TTS, API gateway), the event bus ingestion pipeline, and the manual review queue for conflict resolution.

## Production Considerations

- Monitor idempotency key collision rates (should be < 0.01%)
- Set up alerts for processing lock timeout failures
- Regularly purge expired idempotency keys to manage Redis memory
- Log all duplicate events with full context for audit
- Test dedup behavior under load with simulated duplicate scenarios
- Implement idempotency key rotation strategy for long-running events

## Open-Source First Philosophy

Redis provides the atomic operations needed for robust idempotency (SETNX, EXPIRE, GETSET) at a fraction of the cost of proprietary distributed lock services. BullMQ's built-in dedup capabilities complement Redis for queue-level deduplication. This open-source approach reliably handles exactly-once processing at scale without requiring enterprise middleware.
