# Section 01: Webhook Event Schema

## Overview

Webhook events follow the same envelope structure as WebSocket events, ensuring consistency across real-time delivery mechanisms. Each webhook event includes a unique ID, event type, timestamp, payload, and security metadata. Event types are versioned for backward compatibility, and an event catalog documents all available events with their schemas.

## Architecture

```
Webhook Event Envelope
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTTP POST to https://customer.com/webhooks/voiceagent
Headers:
  Content-Type: application/json
  User-Agent: VoiceAgent-Webhook/1.0
  X-VoiceAgent-Signature: sha256=abc123...
  X-VoiceAgent-Timestamp: 1684512345
  X-VoiceAgent-Event-Id: evt_abc_123
  X-VoiceAgent-Delivery-Attempt: 1
  X-VoiceAgent-Idempotency-Key: uuid-abc-123

Body:
{
  "type": "call.completed",
  "version": 1,
  "id": "evt_abc_123",
  "timestamp": "2025-06-01T10:00:00.000Z",
  "topic": "calls",
  "data": {
    "call_id": "call_def_456",
    "agent_id": "agent_xyz_789",
    "duration_seconds": 245,
    "status": "completed",
    "transcript_summary": "Customer requested refund...",
    "sentiment": "positive"
  }
}

Event Catalog:
  call.started       → Call initiated
  call.completed     → Call ended normally
  call.failed        → Call failed to connect
  call.recording     → Recording ready for download
  agent.deployed     → Agent deployed to production
  campaign.progress  → Campaign progress update
  campaign.completed → Campaign finished
  transcript.ready   → Transcript processed
```

## Design Decisions

- **Consistent Envelope Across Delivery Methods**: Same event structure for WebSocket and webhook — simplifies handling
- **Delivery Metadata in Headers**: Webhook-specific metadata (attempt number, signature) in HTTP headers, not in the body
- **Idempotency Key Header**: Each webhook delivery includes an idempotency key for receiver-side deduplication
- **Topic-Based Organization**: Events grouped by topic (calls, agents, campaigns) for endpoint subscription filtering

## Implementation Approach

```typescript
// Webhook event types
interface WebhookEventEnvelope<T = unknown> {
  type: string;
  version: number;
  id: string;
  timestamp: string;
  topic: string;
  data: T;
}

interface WebhookHeaders {
  'Content-Type': 'application/json';
  'User-Agent': string;
  'X-VoiceAgent-Signature': string;
  'X-VoiceAgent-Timestamp': string;
  'X-VoiceAgent-Event-Id': string;
  'X-VoiceAgent-Delivery-Attempt': string;
  'X-VoiceAgent-Idempotency-Key': string;
}

// Event catalog registry
interface EventCatalogEntry {
  type: string;
  version: number;
  topic: string;
  description: string;
  schema: Record<string, unknown>;
  examples: Record<string, unknown>[];
}

class EventCatalog {
  private entries: Map<string, EventCatalogEntry> = new Map();

  register(entry: EventCatalogEntry): void {
    this.entries.set(entry.type, entry);
  }

  get(type: string): EventCatalogEntry | undefined {
    return this.entries.get(type);
  }

  getByTopic(topic: string): EventCatalogEntry[] {
    return Array.from(this.entries.values()).filter(e => e.topic === topic);
  }

  getAll(): EventCatalogEntry[] {
    return Array.from(this.entries.values());
  }
}

// Event catalog initialization
const eventCatalog = new EventCatalog();

eventCatalog.register({
  type: 'call.completed',
  version: 1,
  topic: 'calls',
  description: 'Emitted when a call ends normally',
  schema: {
    type: 'object',
    properties: {
      call_id: { type: 'string' },
      agent_id: { type: 'string' },
      duration_seconds: { type: 'number' },
      status: { type: 'string', enum: ['completed', 'failed', 'transferred'] },
    },
  },
  examples: [
    {
      call_id: 'call_def_456',
      agent_id: 'agent_xyz_789',
      duration_seconds: 245,
      status: 'completed',
    },
  ],
});

eventCatalog.register({
  type: 'call.started',
  version: 1,
  topic: 'calls',
  description: 'Emitted when a call is initiated',
  schema: {
    type: 'object',
    properties: {
      call_id: { type: 'string' },
      agent_id: { type: 'string' },
      from_number: { type: 'string' },
      to_number: { type: 'string' },
      direction: { type: 'string', enum: ['inbound', 'outbound'] },
    },
  },
  examples: [
    {
      call_id: 'call_def_456',
      agent_id: 'agent_xyz_789',
      from_number: '+14155551234',
      to_number: '+14155556789',
      direction: 'inbound',
    },
  ],
});
```

## Integration Points

- **Webhook Endpoint Configuration**: Customers select which event types to receive per endpoint
- **SDK Event Handling**: SDK provides typed event handlers matching the webhook event types
- **Developer Portal**: Event catalog displayed in documentation with schema and examples

## Production Considerations

- **Event Type Stability**: Never remove event types; deprecate with advance notice and replacement
- **Schema Versioning**: Breaking schema changes increment version number; receivers must check version
- **Payload Size Limits**: Events exceeding 1MB payload are truncated or delivered as references
- **Unknown Event Handling**: Receivers must gracefully ignore unknown event types for forward compatibility

## Open-Source Tools

- **Zod**: Webhook event payload schema validation
- **JSON Schema**: Schema registry for event type definitions
