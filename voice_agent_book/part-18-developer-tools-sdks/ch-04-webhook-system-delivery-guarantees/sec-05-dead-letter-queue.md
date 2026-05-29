# Section 05: Dead Letter Queue

## Overview

When webhook deliveries exhaust all retry attempts, the event is moved to a Dead Letter Queue (DLQ). The DLQ stores failed events with full metadata including the endpoint, event payload, failure reason, and retry history. Operators can inspect, replay, or discard DLQ entries through the management dashboard.

## Architecture

```
Dead Letter Queue Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Delivery Failed — Max Retries] ──→ [Dead Letter Queue]
                                         │
                                    ┌─────┴──────┐
                                    │ DLQ Storage │
                                    │             │
                                    │ Event:      │
                                    │ - id        │
                                    │ - type      │
                                    │ - endpoint  │
                                    │ - payload   │
                                    │ - attempts  │
                                    │ - lastError │
                                    │ - timestamp │
                                    └─────────────┘
                                         │
                                    [DLQ Dashboard]
                                         │
                              ┌──────────┼──────────┐
                              │          │          │
                              ▼          ▼          ▼
                         [Replay]   [Inspect]   [Discard]
                              │          │
                              │    View full payload
                              │    + retry history
                              │    + response body
                              ▼
                    [Reschedule delivery]
                    [Reset retry count]

DLQ Alerting:
  DLQ count > threshold → Alert on-call team
  DLQ age > 1 hour → Escalate
  High DLQ rate → Possible endpoint misconfiguration
```

## Design Decisions

- **DLQ as Separate Store**: Isolated from the main delivery queue to prevent poisoned messages from blocking healthy deliveries
- **Full Payload Retention**: DLQ stores the complete event envelope and delivery metadata for debugging
- **Manual Replay Only**: No automatic retry from DLQ — human intervention ensures someone investigates the failure
- **DLQ Alerting**: Alerts trigger when DLQ grows beyond threshold or events age without resolution

## Implementation Approach

```typescript
// DLQ record structure
interface DeadLetterRecord {
  id: string;
  eventId: string;
  eventType: string;
  endpointId: string;
  endpointUrl: string;
  tenantId: string;
  payload: Record<string, unknown>;
  attempts: DeliveryAttempt[];
  lastError: string;
  lastStatusCode?: number;
  createdAt: Date;
  status: 'pending' | 'replaying' | 'replayed' | 'discarded';
  replayedAt?: Date;
}

interface DeliveryAttempt {
  attempt: number;
  timestamp: Date;
  statusCode?: number;
  error?: string;
  responseBody?: string;
}

// DLQ storage service
class DeadLetterQueueService {
  constructor(
    private db: Database,
    private alertService: AlertService,
  ) {}

  async send(
    eventId: string,
    eventType: string,
    endpointId: string,
    endpointUrl: string,
    tenantId: string,
    payload: Record<string, unknown>,
    attempts: DeliveryAttempt[],
    lastError: string,
  ): Promise<void> {
    const record: DeadLetterRecord = {
      id: crypto.randomUUID(),
      eventId,
      eventType,
      endpointId,
      endpointUrl,
      tenantId,
      payload,
      attempts,
      lastError,
      createdAt: new Date(),
      status: 'pending',
    };

    await this.db.insert('dead_letter_queue', record);

    // Check alert thresholds
    const count = await this.getPendingCount(tenantId);
    if (count >= 10) {
      await this.alertService.sendAlert({
        type: 'dlq_threshold_exceeded',
        tenantId,
        count,
        message: `Dead letter queue has ${count} pending events for tenant`,
      });
    }
  }

  async list(tenantId: string, status?: string): Promise<DeadLetterRecord[]> {
    const query = { tenantId };
    if (status) {
      (query as Record<string, unknown>).status = status;
    }
    return this.db.find('dead_letter_queue', query, { createdAt: -1 });
  }

  async get(id: string): Promise<DeadLetterRecord | null> {
    return this.db.findOne('dead_letter_queue', { id });
  }

  async replay(id: string): Promise<void> {
    const record = await this.get(id);
    if (!record) throw new Error(`DLQ record ${id} not found`);

    await this.db.update('dead_letter_queue', { id }, {
      status: 'replaying',
    });

    try {
      // Resubmit to delivery queue with reset retry count
      await this.deliveryQueue.add({
        eventId: record.eventId,
        eventType: record.eventType,
        endpointId: record.endpointId,
        payload: record.payload,
        attempt: 0,
        firstAttemptAt: new Date().toISOString(),
      });

      await this.db.update('dead_letter_queue', { id }, {
        status: 'replayed',
        replayedAt: new Date(),
      });
    } catch (error) {
      await this.db.update('dead_letter_queue', { id }, {
        status: 'pending',
      });
      throw error;
    }
  }

  async bulkReplay(ids: string[]): Promise<void> {
    for (const id of ids) {
      await this.replay(id);
    }
  }

  async discard(id: string): Promise<void> {
    await this.db.update('dead_letter_queue', { id }, {
      status: 'discarded',
    });
  }

  async getPendingCount(tenantId: string): Promise<number> {
    return this.db.count('dead_letter_queue', { tenantId, status: 'pending' });
  }

  async getDeliveryHistory(eventId: string): Promise<DeliveryAttempt[]> {
    const record = await this.db.findOne('dead_letter_queue', { eventId });
    return record?.attempts || [];
  }
}

// DLQ cleanup job — archive records older than 30 days
async function dlqCleanupJob(service: DeadLetterQueueService): Promise<void> {
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

  const oldRecords = await service.db.find('dead_letter_queue', {
    createdAt: { $lt: thirtyDaysAgo },
  });

  for (const record of oldRecords) {
    await service.db.moveToArchive('dead_letter_queue', record);
    await service.db.delete('dead_letter_queue', { id: record.id });
  }
}
```

## Integration Points

- **Webhook Dashboard**: DLQ management UI — list, inspect, replay, discard
- **Alert Engine**: DLQ threshold alerts routed to Slack/email/PagerDuty
- **Audit Log**: All DLQ operations (replay, discard) are logged for compliance

## Production Considerations

- **DLQ Event Retention**: 30-day retention in primary store; 1 year in archive for compliance
- **Replay Rate Limiting**: Max 100 replays per minute to prevent overwhelming endpoint
- **DLQ Size Monitoring**: Alert when DLQ exceeds 1000 pending events per tenant
- **Poison Event Detection**: Events that fail after 3 replays are automatically quarantined

## Open-Source Tools

- **BullMQ**: Dead letter queue support for failed jobs
- **Novu**: Webhook delivery engine with DLQ capabilities
