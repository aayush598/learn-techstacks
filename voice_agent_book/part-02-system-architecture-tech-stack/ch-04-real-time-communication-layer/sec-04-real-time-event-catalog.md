# Section 04: Real-Time Event Catalog

## Event Architecture

The real-time event system defines every event that flows through the platform. Events are first-class citizens with a consistent schema, versioning, and documentation. This catalog serves as the source of truth for all WebSocket events.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME EVENT CATALOG                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     EVENT CATEGORIES                            │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Call Events │  │ Agent Events │  │ System Events│          │    │
│  │  │  (12 events) │  │  (8 events)  │  │  (6 events)  │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │ Campaign Ev. │  │ Dashboard    │  │ Billing      │          │    │
│  │  │  (5 events)  │  │ Alerts       │  │ Events       │          │    │
│  │  │              │  │  (4 events)  │  │  (4 events)  │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  EVENT SCHEMA (ALL EVENTS)                      │    │
│  │                                                                  │    │
│  │  {                                                               │    │
│  │    "event": "call.updated",          // Event name (dot notation)│    │
│  │    "version": 1,                      // Schema version           │    │
│  │    "id": "evt_abc123",               // Unique event ID          │    │
│  │    "timestamp": "2025-01-15T12:00:00Z", // ISO 8601              │    │
│  │    "tenantId": "tenant_abc",         // Tenant context            │    │
│  │    "source": "call-service",          // Producing service        │    │
│  │    "correlationId": "call_xyz",       // Trace across events      │    │
│  │    "data": { ... }                    // Event-specific payload   │    │
│  │  }                                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Call Events

```typescript
// ──────────────────────────────────────────────
// CALL EVENTS
// ──────────────────────────────────────────────

export interface CallEvents {
  /** Call has been created (queued or ringing) */
  'call.created': {
    callId: string
    agentId: string
    callerNumber: string
    direction: 'inbound' | 'outbound'
    campaignId?: string
    timestamp: string
  }

  /** Call is now ringing on the destination */
  'call.ringing': {
    callId: string
    agentId: string
    ringingAt: string
  }

  /** Call has been answered (media flowing) */
  'call.answered': {
    callId: string
    agentId: string
    answeredAt: string
    latencyMs: number  // Time from init to answer
  }

  /** Call status updated (e.g., paused, resumed) */
  'call.updated': {
    callId: string
    status: string
    previousStatus: string
    duration: number
    timestamp: string
  }

  /** New transcript segment available */
  'call.transcript': {
    callId: string
    speaker: 'user' | 'agent' | 'system'
    text: string
    isFinal: boolean
    startTime: number  // ms from call start
    endTime: number
    confidence: number
  }

  /** Sentiment score updated */
  'call.sentiment': {
    callId: string
    score: number      // -1.0 to 1.0
    label: 'positive' | 'negative' | 'neutral'
    timestamp: string
  }

  /** Call has ended */
  'call.ended': {
    callId: string
    agentId: string
    duration: number    // seconds
    status: 'completed' | 'failed' | 'no_answer' | 'busy'
    reason?: string
    cost: number       // micro-cents
    recordingUrl?: string
  }

  /** Call transferred to another agent/queue */
  'call.transferred': {
    callId: string
    fromAgentId: string
    toAgentId?: string
    toQueue?: string
    reason: string
    timestamp: string
  }

  /** Call escalated to human agent */
  'call.escalated': {
    callId: string
    reason: string
    summary: string
    assignedTo?: string
    timestamp: string
  }

  /** Audio quality metric */
  'call.quality': {
    callId: string
    mos: number           // Mean Opinion Score (1-5)
    jitterMs: number
    packetLossPercent: number
    roundTripTimeMs: number
    timestamp: string
  }

  /** DTMF digit received */
  'call.dtmf': {
    callId: string
    digit: string
    timestamp: string
  }

  /** Recording status */
  'call.recording': {
    callId: string
    status: 'started' | 'paused' | 'completed' | 'failed'
    url?: string
    duration?: number
    size?: number
    timestamp: string
  }

  /** Error during call */
  'call.error': {
    callId: string
    code: string
    message: string
    component: string
    timestamp: string
  }
}
```

## Agent & System Events

```typescript
// ──────────────────────────────────────────────
// AGENT EVENTS
// ──────────────────────────────────────────────

export interface AgentEvents {
  /** Agent status changed */
  'agent.status': {
    agentId: string
    status: 'online' | 'offline' | 'busy' | 'away'
    previousStatus: string
    timestamp: string
  }

  /** Agent deployed new version */
  'agent.deployed': {
    agentId: string
    version: number
    deployedBy: string
    timestamp: string
  }

  /** Agent metrics snapshot */
  'agent.metrics': {
    agentId: string
    activeCalls: number
    totalCallsToday: number
    avgDuration: number
    avgSentiment: number
    timestamp: string
  }

  /** Agent configuration changed */
  'agent.config.updated': {
    agentId: string
    updatedBy: string
    changedFields: string[]
    timestamp: string
  }

  /** Agent error rate alert */
  'agent.alert': {
    agentId: string
    type: 'error_rate' | 'latency' | 'usage_limit'
    severity: 'warning' | 'critical'
    message: string
    value: number
    threshold: number
    timestamp: string
  }
}

// ──────────────────────────────────────────────
// CAMPAIGN EVENTS
// ──────────────────────────────────────────────

export interface CampaignEvents {
  /** Campaign status changed */
  'campaign.status': {
    campaignId: string
    status: 'running' | 'paused' | 'completed' | 'scheduled'
    timestamp: string
  }

  /** Campaign progress update */
  'campaign.progress': {
    campaignId: string
    totalContacts: number
    contacted: number
    completed: number
    failed: number
    percentComplete: number
    timestamp: string
  }

  /** New contact result */
  'campaign.result': {
    campaignId: string
    contactId: string
    result: 'answered' | 'no_answer' | 'busy' | 'callback' | 'opt_out'
    duration: number
    timestamp: string
  }
}

// ──────────────────────────────────────────────
// DASHBOARD & SYSTEM EVENTS
// ──────────────────────────────────────────────

export interface SystemEvents {
  /** System health status */
  'system.health': {
    services: Array<{
      name: string
      status: 'healthy' | 'degraded' | 'down'
      latency: number
    }>
    timestamp: string
  }

  /** Usage threshold alert */
  'system.usage.threshold': {
    metric: string
    currentValue: number
    limit: number
    percentUsed: number
    timestamp: string
  }

  /** Maintenance notification */
  'system.maintenance': {
    type: 'scheduled' | 'emergency'
    startTime: string
    endTime: string
    description: string
    affectedServices: string[]
  }

  /** Error/alert for admin */
  'system.alert': {
    severity: 'info' | 'warning' | 'critical'
    title: string
    message: string
    actionUrl?: string
    timestamp: string
  }
}

// ──────────────────────────────────────────────
// BILLING EVENTS
// ──────────────────────────────────────────────

export interface BillingEvents {
  /** Usage approaching limit */
  'billing.usage.warning': {
    metric: string
    currentUsage: number
    limit: number
    percentUsed: number
    timestamp: string
  }

  /** Invoice generated */
  'billing.invoice.created': {
    invoiceId: string
    amount: number
    dueDate: string
    status: 'open'
    timestamp: string
  }

  /** Payment processed */
  'billing.payment.processed': {
    invoiceId: string
    amount: number
    status: 'succeeded' | 'failed'
    timestamp: string
  }

  /** Subscription changed */
  'billing.subscription.updated': {
    plan: string
    previousPlan: string
    status: string
    effectiveDate: string
    timestamp: string
  }
}
```

## Event Subscription & Filtering

```typescript
// Client-side event subscription with filtering

interface SubscriptionOptions {
  events: string[]           // Event names to subscribe to
  filter?: {
    agentId?: string
    callId?: string
    campaignId?: string
    severity?: ('info' | 'warning' | 'critical')[]
  }
}

// Client subscribes with filter
const sub: SubscriptionOptions = {
  events: ['call.updated', 'call.transcript', 'call.sentiment'],
  filter: { callId: 'call_xyz123' }
}

socket.emit('subscribe', sub)

// Server applies filter
socket.on('subscribe', (options: SubscriptionOptions) => {
  // Join appropriate rooms
  if (options.filter?.callId) {
    socket.join(`call:${options.filter.callId}`)
  }
  if (options.filter?.agentId) {
    socket.join(`agent:${options.filter.agentId}`)
  }

  // Store filter preferences for this socket
  socket.data.eventFilter = new Set(options.events)
})

// Emit with filtering
function emitToSocket(socket: Socket, event: string, data: unknown) {
  if (socket.data.eventFilter && !socket.data.eventFilter.has(event)) {
    return  // Socket not interested in this event
  }
  socket.emit(event, { event, data, timestamp: new Date().toISOString() })
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event Naming | dot.case (call.updated) | Hierarchical, namespaced, easy to filter |
| Schema Versioning | Integer in event envelope | Clients can handle multiple versions |
| Event ID | Prefixed (evt_abc123) | Unique, sortable, identifiable |
| Correlation ID | Derived from call/entity ID | Trace related events across services |
| Timestamp | ISO 8601 UTC | Universal, sortable, parseable |

## Integration Points

- **Part 06 (Frontend)** — Dashboard components subscribe to these events
- **Part 09 (Data Flow)** — Events feed into Kafka for async processing
- **Part 10 (Integrations)** — Webhooks deliver external versions of these events
- **Part 20 (Notifications)** — Alert events trigger notification channels

## Production Considerations

- **Event Volume**: Expect 100+ events per call (transcript chunks are high-frequency)
- **Batching**: Transcript events are batched (5 chunks per message) to reduce message count
- **Rate Limiting**: Client-side: 100 events/sec per socket; server-side: 10K events/sec per room
- **Filtering**: Always filter server-side before emitting; never send all events to all clients
- **Retention**: Events stored in database for 30 days; archived to MinIO as JSON Lines
- **Documentation**: Auto-generate event catalog from TypeScript types using TypeDoc
