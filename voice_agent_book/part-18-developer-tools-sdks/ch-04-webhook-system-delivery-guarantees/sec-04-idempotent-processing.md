# Section 04: Idempotent Processing

## Overview

Webhook events may be delivered multiple times due to network retries or duplicate processing. The webhook system includes idempotency keys in every delivery, enabling receivers to detect and ignore duplicate events. Receivers should store processed event IDs and check for duplicates before processing.

## Architecture

```
Receiver-Side Idempotency
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Webhook Delivery 1] ──→ [Receiver]
                            │
                      Check idempotency key
                            │
                    ┌───────┴───────┐
                    │ New            │ Already Processed
                    ▼               ▼
              [Process Event]  [Return 200 OK]
                    │               (no-op)
              [Store idempotency
               key in database]
                    │
              [Return 200 OK]

[Webhook Delivery 2 (Retry)] ──→ [Receiver]
                                      │
                                Check idempotency key
                                      │
                                [Already Processed]
                                      │
                                [Return 200 OK]

Deduplication Window:
  Idempotency keys stored for 7 days
  Keys older than 7 days are eligible for reprocessing

Deduplication Key:
  Namespace: webhook:dedup:{tenant_id}
  Key: {event_id}
  Value: {processed_at, status}
```

## Design Decisions

- **Event ID as Idempotency Key**: Each event has a globally unique ID; receivers deduplicate on event ID
- **Receiver-Side Responsibility**: The platform guarantees at-least-once delivery; receivers implement deduplication
- **7-Day Deduplication Window**: Matches the webhook event retention period
- **200 OK for Duplicates**: Receiver returns 200 for duplicate events — signals successful delivery without reprocessing

## Implementation Approach

```typescript
// Idempotency checker (for receiver implementation)
interface IdempotencyRecord {
  eventId: string;
  processedAt: Date;
  status: 'processing' | 'completed' | 'failed';
  response?: Record<string, unknown>;
}

class WebhookIdempotencyChecker {
  constructor(
    private store: IdempotencyStore,
    private ttlMs = 7 * 24 * 60 * 60 * 1000, // 7 days
  ) {}

  async isDuplicate(eventId: string): Promise<boolean> {
    const record = await this.store.get(eventId);
    return record !== null && record.status === 'completed';
  }

  async startProcessing(eventId: string): Promise<boolean> {
    // Atomic check-and-set to prevent concurrent processing
    const existing = await this.store.get(eventId);

    if (existing && existing.status === 'processing') {
      return false; // Already being processed
    }

    if (existing && existing.status === 'completed') {
      return false; // Already completed
    }

    await this.store.set(eventId, {
      eventId,
      processedAt: new Date(),
      status: 'processing',
    }, this.ttlMs);

    return true;
  }

  async markCompleted(eventId: string, response?: Record<string, unknown>): Promise<void> {
    await this.store.set(eventId, {
      eventId,
      processedAt: new Date(),
      status: 'completed',
      response,
    }, this.ttlMs);
  }

  async markFailed(eventId: string): Promise<void> {
    await this.store.set(eventId, {
      eventId,
      processedAt: new Date(),
      status: 'failed',
    }, this.ttlMs);
  }
}

// Example receiver implementation
async function handleWebhookEvent(event: WebhookEventEnvelope, idempotency: WebhookIdempotencyChecker): Promise<void> {
  // Check if already processed
  if (await idempotency.isDuplicate(event.id)) {
    console.log(`Skipping duplicate event: ${event.id}`);
    return;
  }

  // Start processing
  const canProcess = await idempotency.startProcessing(event.id);
  if (!canProcess) {
    console.log(`Event ${event.id} already being processed`);
    return;
  }

  try {
    // Process the event
    switch (event.type) {
      case 'call.completed':
        await processCallCompleted(event.data);
        break;
      case 'agent.deployed':
        await processAgentDeployed(event.data);
        break;
      default:
        console.warn(`Unknown event type: ${event.type}`);
    }

    await idempotency.markCompleted(event.id, { received: true });
  } catch (error) {
    await idempotency.markFailed(event.id);
    throw error; // Re-throw to trigger webhook retry
  }
}

// Express/Hono receiver endpoint
app.post('/webhooks/voiceagent', async (c) => {
  const signature = c.req.header('X-VoiceAgent-Signature');
  const timestamp = c.req.header('X-VoiceAgent-Timestamp');
  const eventId = c.req.header('X-VoiceAgent-Event-Id');
  const body = await c.req.json();

  // Verify signature
  const verifier = new WebhookVerifier();
  const isValid = verifier.verify(
    JSON.stringify(body),
    signature,
    timestamp,
    process.env.WEBHOOK_SECRET!,
  );

  if (!isValid) {
    return c.json({ error: 'Invalid signature' }, 401);
  }

  // Idempotent processing
  await handleWebhookEvent(body, idempotencyChecker);

  return c.json({ received: true });
});
```

## Integration Points

- **Database/Redis**: Idempotency record storage; Redis for high-throughput, SQL for durable storage
- **Distributed Locking**: For multi-instance receivers, use Redis-based distributed lock during processing
- **Monitoring**: Track duplicate event ratio — high ratio may indicate connectivity issues at receiver

## Production Considerations

- **Storage Requirements**: 7-day deduplication window with potentially millions of events/day requires storage planning
- **TTL Cleanup**: Idempotency records should have TTL for automatic cleanup; use DynamoDB TTL or Redis EXPIRE
- **Atomic Operations**: Use conditional writes (DynamoDB condition expression, Redis SETNX) to prevent race conditions
- **Graceful Handling**: If idempotency store is unavailable, receivers should reject webhook (non-200) to trigger retry

## Open-Source Tools

- **Redis**: SETNX for atomic idempotency key creation with TTL
- **DynamoDB**: Conditional writes with TTL for idempotency records
