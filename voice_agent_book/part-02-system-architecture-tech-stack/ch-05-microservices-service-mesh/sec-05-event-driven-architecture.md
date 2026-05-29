# Section 05: Event-Driven Architecture

## Event Storming & Design

The platform is fundamentally **event-driven**. Every state change produces an event that other services can consume. This enables loose coupling, auditability, and async workflows. Events are the "source of truth" for the call lifecycle.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      EVENT-DRIVEN ARCHITECTURE MAP                     │
│                                                                         │
│  CALL LIFECYCLE EVENTS:                                                │
│                                                                         │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐       │
│  │ Call   │   │ Call   │   │ Call   │   │ Call   │   │ Call   │       │
│  │Created │──▶│Ringing │──▶│Answerd │──▶│Updated │──▶│ End    │       │
│  └───┬────┘   └───┬────┘   └───┬────┘   └───┬────┘   └───┬────┘       │
│      │            │            │            │            │            │
│      ▼            ▼            ▼            ▼            ▼            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    EVENT PROCESSORS                             │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │  Billing │  │   AI     │  │ Campaign │  │Notify    │        │   │
│  │  │  Meter   │  │  Log     │  │  Update  │  │ Webhook  │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ Analytics│  │  Audit   │  │  Voice   │  │ Recording│        │   │
│  │  │  (CH)    │  │  Log     │  │  Stats   │  │  Store   │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  EVENT CATALOG (Partial):                                              │
│  ┌────────────────────┬─────────────────────┬─────────────────────────┐│
│  │ Event              │ Producer            │ Consumers                ││
│  ├────────────────────┼─────────────────────┼─────────────────────────┤│
│  │ call.initiated     │ Call Service        │ Voice, AI, Billing       ││
│  │ call.answered      │ Call Service        │ Voice, Billing, WebSocket││
│  │ call.ended         │ Call Service        │ AI, Billing, Campaign,   ││
│  │                    │                     │ Analytics, Notifications  ││
│  │ agent.deployed     │ Agent Service       │ Voice, AI, WebSocket     ││
│  │ subscription.      │ Billing Service     │ API Gateway, Notify      ││
│  │   changed          │                     │                          ││
│  │ campaign.contact   │ Campaign Service    │ Analytics, Notifications  ││
│  │   result           │                     │                          ││
│  └────────────────────┴─────────────────────┴─────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

## Event Definitions

```typescript
// Complete event type definitions

export interface BaseEvent {
  eventId: string
  source: string
  timestamp: string
  version: number
  correlationId: string
  tenantId: string
}

// ── Call Events ──
export interface CallInitiatedEvent extends BaseEvent {
  type: 'call.initiated'
  data: {
    callId: string
    agentId: string
    direction: 'inbound' | 'outbound'
    callerNumber: string
    calledNumber: string
    campaignId?: string
    initiatedAt: string
  }
}

export interface CallAnsweredEvent extends BaseEvent {
  type: 'call.answered'
  data: {
    callId: string
    agentId: string
    answeredAt: string
    setupTimeMs: number
    mediaServer: string
  }
}

export interface CallEndedEvent extends BaseEvent {
  type: 'call.ended'
  data: {
    callId: string
    agentId: string
    status: 'completed' | 'failed' | 'no_answer' | 'busy' | 'error'
    duration: number
    reason?: string
    costMicroUs: number
    recordingUrl?: string
    endedAt: string
  }
}

export interface CallTransferredEvent extends BaseEvent {
  type: 'call.transferred'
  data: {
    callId: string
    fromAgentId: string
    toAgentId?: string
    toQueue?: string
    reason: string
    transferredAt: string
  }
}

export interface TranscriptAvailableEvent extends BaseEvent {
  type: 'call.transcript.available'
  data: {
    callId: string
    transcriptUrl: string
    wordCount: number
    turnCount: number
    language: string
    confidence: number
  }
}

// ── Agent Events ──
export interface AgentDeployedEvent extends BaseEvent {
  type: 'agent.deployed'
  data: {
    agentId: string
    version: number
    voiceId: string
    promptId: string
    config: Record<string, unknown>
    deployedBy: string
    deployedAt: string
  }
}

export interface AgentPerformanceEvent extends BaseEvent {
  type: 'agent.performance.snapshot'
  data: {
    agentId: string
    periodStart: string
    periodEnd: string
    totalCalls: number
    avgDuration: number
    avgSentiment: number
    avgCost: number
    successRate: number
    errorRate: number
  }
}

// ── Billing Events ──
export interface SubscriptionChangedEvent extends BaseEvent {
  type: 'subscription.changed'
  data: {
    tenantId: string
    previousPlanId: string
    newPlanId: string
    effectiveDate: string
    reason: 'upgrade' | 'downgrade' | 'cancel' | 'renew'
  }
}

export interface UsageRecordedEvent extends BaseEvent {
  type: 'usage.recorded'
  data: {
    tenantId: string
    metric: string
    amount: number
    unit: string
    recordedAt: string
    source: string
  }
}

// ── Campaign Events ──
export interface ContactResultEvent extends BaseEvent {
  type: 'campaign.contact.result'
  data: {
    campaignId: string
    contactId: string
    callId: string
    result: 'answered' | 'no_answer' | 'busy' | 'callback' | 'opt_out' | 'invalid'
    duration: number
    attemptNumber: number
    timestamp: string
  }
}

// ── System Events ──
export interface SystemAlertEvent extends BaseEvent {
  type: 'system.alert'
  data: {
    severity: 'critical' | 'warning' | 'info'
    title: string
    message: string
    service: string
    component: string
    metrics?: Record<string, number>
    alertAt: string
  }
}
```

## Event Processing Patterns

```typescript
// 1. Event Sourcing — append-only event store for call state
class CallEventStore {
  async appendEvent(callId: string, event: CallEvent): Promise<void> {
    await prisma.conversationEvent.create({
      data: {
        callId: event.data.callId,
        type: event.type,
        payload: event.data,
        timestamp: new Date(event.timestamp)
      }
    })
  }

  async getEvents(callId: string): Promise<CallEvent[]> {
    const events = await prisma.conversationEvent.findMany({
      where: { callId },
      orderBy: { timestamp: 'asc' }
    })
    return events.map(e => ({
      type: e.type,
      data: e.payload as any,
      timestamp: e.timestamp.toISOString()
    }))
  }

  // Rebuild state by replaying events
  async rebuildState(callId: string): Promise<CallState> {
    const events = await this.getEvents(callId)
    let state: CallState = { status: 'pending', duration: 0, cost: 0 }

    for (const event of events) {
      state = this.applyEvent(state, event)
    }

    return state
  }

  private applyEvent(state: CallState, event: CallEvent): CallState {
    switch (event.type) {
      case 'call.initiated':
        return { ...state, status: 'ringing', ...event.data }
      case 'call.answered':
        return { ...state, status: 'in_progress', answeredAt: event.data.answeredAt }
      case 'call.ended':
        return {
          ...state,
          status: event.data.status,
          duration: event.data.duration,
          cost: event.data.costMicroUs,
          endedAt: event.data.endedAt
        }
      default:
        return state
    }
  }
}

// 2. Competing Consumers — multiple workers process same events
class CompetingConsumerGroup {
  async processEvents(events: CallEvent[]): Promise<void> {
    // Use Redis for distributed locking
    const lockKey = `lock:event:${events[0].eventId}`
    const acquired = await redis.set(lockKey, process.env.HOSTNAME, {
      nx: true,
      ex: 30
    })

    if (!acquired) {
      // Another instance is processing this batch
      return
    }

    try {
      for (const event of events) {
        await this.handleEvent(event)
      }
    } finally {
      await redis.del(lockKey)
    }
  }

  private async handleEvent(event: CallEvent): Promise<void> {
    switch (event.type) {
      case 'call.ended':
        await Promise.all([
          this.recordUsage(event),
          this.triggerPostCallWorkflow(event),
          this.updateCampaignMetrics(event),
          this.sendWebhooks(event)
        ])
        break
    }
  }
}

// 3. Saga Pattern — distributed transaction coordination
class CallWorkflowSaga {
  // Example: End call saga
  async endCallSaga(callId: string): Promise<void> {
    const sagaId = crypto.randomUUID()

    try {
      // Step 1: Stop voice processing
      await this.sendCommand('voice-service', 'stop-processing', { callId })
      await this.recordStep(sagaId, 'voice-stopped')

      // Step 2: Save recording
      await this.sendCommand('media-server', 'save-recording', { callId })
      await this.recordStep(sagaId, 'recording-saved')

      // Step 3: Generate transcript
      await this.sendCommand('ai-service', 'generate-transcript', { callId })
      await this.recordStep(sagaId, 'transcript-generated')

      // Step 4: Record billing usage
      await this.sendCommand('billing-service', 'record-usage', { callId })
      await this.recordStep(sagaId, 'usage-recorded')

      // Step 5: Notify webhooks
      await this.sendCommand('notification-service', 'notify-call-ended', { callId })
      await this.recordStep(sagaId, 'notified')

      // Mark saga complete
      await this.completeSaga(sagaId)

    } catch (error) {
      // Compensate: rollback completed steps
      await this.compensateSaga(sagaId, error)
    }
  }

  private async compensateSaga(sagaId: string, error: unknown): Promise<void> {
    const steps = await this.getCompletedSteps(sagaId)

    // Compensate in reverse order
    for (const step of steps.reverse()) {
      switch (step) {
        case 'usage-recorded':
          await this.sendCommand('billing-service', 'reverse-usage', { sagaId })
          break
        case 'recording-saved':
          await this.sendCommand('media-server', 'delete-recording', { sagaId })
          break
        case 'voice-stopped':
          await this.sendCommand('voice-service', 'resume-processing', { sagaId })
          break
      }
    }

    logger.error({ sagaId, error }, 'Saga compensated')
  }
}
```

## CQRS Separation

```typescript
// Command (Write) side
export class CallCommandHandler {
  async handleCommand(command: CallCommand): Promise<void> {
    // 1. Validate command
    // 2. Write to primary database
    // 3. Publish event
    // 4. Event handler updates read model

    switch (command.type) {
      case 'initiate_call': {
        const call = await prisma.call.create({ data: command.data })
        await kafka.produce('call.initiated', { callId: call.id, ...command.data })
        break
      }
      case 'end_call': {
        await prisma.call.update({
          where: { id: command.data.callId },
          data: { status: 'completed', endedAt: new Date() }
        })
        await kafka.produce('call.ended', command.data)
        break
      }
    }
  }
}

// Query (Read) side — optimized for reading
export class CallQueryHandler {
  async getActiveCalls(tenantId: string): Promise<CallView[]> {
    // Read from materialized view or cache
    return redis.get(`views:active-calls:${tenantId}`)
      ?? await this.rebuildActiveCallsView(tenantId)
  }

  private async rebuildActiveCallsView(tenantId: string): Promise<CallView[]> {
    // Rebuild from event store if cache miss
    const events = await eventStore.getEventsByTenant(tenantId)
    return this.projectActiveCalls(events)
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event Schema | Versioned with backward compatibility | Services evolve independently |
| Event Ordering | Per-partition ordering (by call_id) | Kafka guarantees order per key |
| Processing | At-least-once with idempotency | Reliability without duplicates |
| Saga Compensation | Reverse order, retry 3x | Distributed transaction reliability |
| CQRS | Read model in Redis + ClickHouse | Optimized query performance |

## Integration Points

- **Part 05 (Microservices)** — Event-driven communication between services
- **Part 09 (Data Flow)** — Detailed event sourcing implementation
- **Part 11 (Analytics)** — Events flow to ClickHouse for analytics
- **Part 15 (Security)** — Audit trail from all system events

## Production Considerations

- **Event Volume**: 10M+ events/day at scale; design for 100M+
- **Idempotency Keys**: Essential for exactly-once processing
- **Dead Letter Queue**: Handles processing failures gracefully
- **Event Retention**: 7 days in Kafka, 30 days in PostgreSQL, 12 months in ClickHouse
- **Schema Evolution**: Backward-compatible changes only; new fields are optional
- **Monitoring**: Track event throughput, processing latency, consumer lag per topic
