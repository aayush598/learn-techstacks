# Section 02: Event Schema Design

## Overview

WebSocket events follow a standardized envelope structure that includes event type, unique ID, timestamp, channel routing, and typed payload. Every event is versioned, and the event catalog defines all supported event types with their schemas. This consistent structure enables clients to write generic event handlers that work across all event types.

## Architecture

```
Event Envelope Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{
  "type": "call.status_changed",
  "version": 1,
  "id": "evt_a1b2c3d4e5f6",
  "timestamp": "2025-06-01T10:00:00.000Z",
  "channel": "tenant:tenant_xyz",
  "security": {
    "signature": "hmac_sha256_signature",
    "keyId": "key_abc_123"
  },
  "data": {
    "call_id": "call_def_456",
    "previous_status": "ringing",
    "current_status": "in_progress",
    "duration_seconds": 120
  }
}

Event Type Naming:
  {domain}.{entity}.{action}

  call.status_changed         → Call status transition
  call.transcript_ready       → Transcription available
  agent.deployed              → Agent deployed to production
  campaign.started            → Campaign execution started
  campaign.progress           → Campaign progress update
  call.recording_ready        → Recording processed
  error.transcription_failed  → Transcription failure
  system.maintenance          → Scheduled maintenance notice
```

## Design Decisions

- **Semantic Event Types**: Domain-first naming (`call.status_changed`) — groups related events and prevents naming collisions
- **Event ID for Deduplication**: Clients use event ID for deduplication; server guarantees at-least-once delivery per ID
- **Versioned Payloads**: Each event type has a version number; backward-compatible payload changes increment minor version
- **Channel Routing**: Events are published to channels; clients subscribe to channels, not individual event types

## Implementation Approach

```typescript
// Event type definitions
type EventType = string; // "{domain}.{entity}.{action}"

interface EventEnvelope<T = unknown> {
  type: EventType;
  version: number;
  id: string;
  timestamp: string; // ISO 8601
  channel: string;
  security?: {
    signature?: string;
    keyId?: string;
  };
  data: T;
}

interface EventPayloads {
  'call.status_changed': {
    call_id: string;
    previous_status: CallStatus;
    current_status: CallStatus;
    duration_seconds: number;
  };
  'call.transcript_ready': {
    call_id: string;
    transcript_id: string;
    language: string;
    segments: TranscriptSegment[];
  };
  'agent.deployed': {
    agent_id: string;
    agent_name: string;
    deployed_at: string;
    version: string;
  };
  'campaign.progress': {
    campaign_id: string;
    total_calls: number;
    completed_calls: number;
    failed_calls: number;
    progress_percent: number;
  };
}

// Event bus implementation
class EventBus {
  private publishers: Map<EventType, Set<(event: EventEnvelope) => void>> = new Map();

  publish<T>(event: Omit<EventEnvelope<T>, 'id' | 'timestamp'>): void {
    const envelope: EventEnvelope<T> = {
      ...event,
      id: this.generateEventId(),
      timestamp: new Date().toISOString(),
    };

    const handlers = this.publishers.get(event.type);
    if (handlers) {
      for (const handler of handlers) {
        try {
          handler(envelope);
        } catch (error) {
          console.error(`Event handler failed for ${event.type}:`, error);
        }
      }
    }
  }

  subscribe(type: EventType, handler: (event: EventEnvelope) => void): () => void {
    if (!this.publishers.has(type)) {
      this.publishers.set(type, new Set());
    }
    this.publishers.get(type)!.add(handler);

    return () => this.publishers.get(type)?.delete(handler);
  }

  private generateEventId(): string {
    const timestamp = Date.now().toString(36);
    const random = crypto.randomBytes(12).toString('base64url');
    return `evt_${timestamp}${random}`;
  }
}

// Event catalog
const EVENT_CATALOG: Record<EventType, { version: number; description: string }> = {
  'call.status_changed': {
    version: 1,
    description: 'Emitted when a call transitions between statuses',
  },
  'call.transcript_ready': {
    version: 1,
    description: 'Emitted when transcription is available for a completed call',
  },
  'agent.deployed': {
    version: 1,
    description: 'Emitted when an agent is deployed to an environment',
  },
  'campaign.progress': {
    version: 1,
    description: 'Periodic progress update during campaign execution',
  },
};
```

## Integration Points

- **SDK Event Handling**: SDK parses event envelopes and dispatches typed event handlers
- **Webhook Delivery**: Same event envelope format used for webhook delivery — consistent abstraction
- **Event Store**: Events can be persisted to event store for replay and audit

## Production Considerations

- **Schema Registry**: Store event schemas in a registry for validation and documentation
- **Backward Compatibility**: New fields must be optional; field removal requires new event version
- **Event Size Limits**: Maximum 256KB per event; larger payloads are split or referenced via URL
- **Unknown Event Types**: Clients must gracefully ignore unknown event types for forward compatibility

## Open-Source Tools

- **Zod**: Event payload schema validation and type inference
- **JSON Schema**: Schema registry and validation for event types
