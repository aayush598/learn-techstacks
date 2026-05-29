# Section 02: Call Lifecycle State Machine

## State Machine Design

The call lifecycle is managed by a **deterministic state machine** with well-defined transitions, guards, and side effects. Each state transition emits an event, triggers side effects (billing, notifications), and is persisted to the event log for auditability.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CALL LIFECYCLE STATE MACHINE                     │
│                                                                     │
│                          ┌──────────┐                              │
│                          │  Queued   │                              │
│                          └────┬─────┘                              │
│                               │ dequeue                             │
│                               ▼                                    │
│                          ┌──────────┐                              │
│                   ┌──────│ Ringing  │──────┐                       │
│                   │      └────┬─────┘      │                       │
│                   │           │            │                        │
│              no_answer    answer       timeout                     │
│                   │           │            │                        │
│                   ▼           ▼            ▼                       │
│             ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│             │Voicemail │ │Connected │ │  Failed  │               │
│             └──────────┘ └────┬─────┘ └──────────┘               │
│                               │                                    │
│                        ┌──────┴──────┐                            │
│                        │  InProgress  │                            │
│                        └──────┬──────┘                            │
│                           │   │   │                                │
│                    ┌──────┘   │   └──────┐                        │
│                    ▼          ▼          ▼                         │
│              ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│              │  Paused  │ │Transfer  │ │Escalated│              │
│              └────┬─────┘ └────┬─────┘ └────┬─────┘              │
│                   │            │            │                      │
│               resume       complete     human                      │
│                   │            │         handoff                   │
│                   ▼            ▼            ▼                      │
│              ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│              │InProgress │ │Completed │ │HumanHand │              │
│              └──────────┘ └──────────┘ └──────────┘              │
│                                                                     │
│  Terminal States: Completed, Failed, HumanHandoff, Voicemail      │
│  Transition emit events: call.state.changed.{from}.{to}           │
└─────────────────────────────────────────────────────────────────────┘
```

## State Machine Implementation

```typescript
// State machine definition
type CallState =
  | 'queued'
  | 'ringing'
  | 'connected'
  | 'in_progress'
  | 'paused'
  | 'transferring'
  | 'escalated'
  | 'voicemail'
  | 'completed'
  | 'failed'
  | 'human_handoff';

interface StateTransition {
  from: CallState[];
  to: CallState;
  guard?: (call: CallContext) => boolean | Promise<boolean>;
  sideEffects: SideEffect[];
}

interface CallContext {
  callId: string;
  tenantId: string;
  agentId: string;
  currentState: CallState;
  duration: number;
  userId?: string;
  metadata: Record<string, unknown>;
}

type SideEffect = (call: CallContext) => Promise<void>;

// Transition definitions
const CALL_STATE_MACHINE: Record<string, StateTransition> = {
  queue_call: {
    from: ['idle'],
    to: 'queued',
    sideEffects: [emitQueuedEvent],
  },
  initiate_call: {
    from: ['queued'],
    to: 'ringing',
    guard: (call) => call.metadata.phoneNumber !== undefined,
    sideEffects: [initiateOutboundCall, emitRingingEvent],
  },
  answer_call: {
    from: ['ringing'],
    to: 'connected',
    sideEffects: [emitConnectedEvent, startBillingMeter],
  },
  start_conversation: {
    from: ['connected'],
    to: 'in_progress',
    sideEffects: [emitInProgressEvent, startVoicePipeline],
  },
  pause_call: {
    from: ['in_progress'],
    to: 'paused',
    guard: (call) => call.duration < 3600, // Max 1 hour pause
    sideEffects: [emitPausedEvent, pauseBillingMeter, pauseVoicePipeline],
  },
  resume_call: {
    from: ['paused'],
    to: 'in_progress',
    sideEffects: [emitResumedEvent, resumeBillingMeter, resumeVoicePipeline],
  },
  transfer_call: {
    from: ['in_progress'],
    to: 'transferring',
    sideEffects: [emitTransferEvent, initiateTransfer],
  },
  complete_call: {
    from: ['in_progress', 'connected'],
    to: 'completed',
    sideEffects: [emitCompletedEvent, stopBillingMeter, scheduleTranscription],
  },
  fail_call: {
    from: ['ringing', 'connected', 'in_progress', 'transferring'],
    to: 'failed',
    sideEffects: [emitFailedEvent, stopBillingMeter, scheduleRetryIfApplicable],
  },
};
```

## State Transition Engine

```typescript
class CallStateMachine {
  async transition(callId: string, event: string): Promise<CallState> {
    const call = await this.callRepository.getById(callId);
    const transition = CALL_STATE_MACHINE[event];

    if (!transition) {
      throw new Error(`Unknown transition event: ${event}`);
    }

    if (!transition.from.includes(call.currentState)) {
      throw new Error(
        `Invalid transition: ${call.currentState} → ${event}. ` +
        `Allowed from: ${transition.from.join(', ')}`
      );
    }

    if (transition.guard) {
      const allowed = await transition.guard(call);
      if (!allowed) {
        throw new Error(`Guard rejected transition: ${event} for call ${callId}`);
      }
    }

    // Execute transition atomically with optimistic concurrency
    const updated = await this.callRepository.updateState(callId, {
      from: call.currentState,
      to: transition.to,
      expectedVersion: call.version,
    });

    // Fire side effects after successful state change
    const context: CallContext = {
      ...call,
      currentState: transition.to,
    };

    await Promise.all(transition.sideEffects.map(effect => effect(context)));

    return updated.state;
  }
}
```

## Billing Meter Integration

```typescript
// Side effect: start billing meter when call connects
const startBillingMeter: SideEffect = async (call) => {
  await billingService.startMeter({
    callId: call.callId,
    tenantId: call.tenantId,
    agentId: call.agentId,
    startedAt: new Date(),
    ratePerMinute: await pricingService.getRate(call.tenantId, call.agentId),
  });
};

// Side effect: stop billing and calculate cost
const stopBillingMeter: SideEffect = async (call) => {
  await billingService.stopMeter(call.callId);
};

// Side effect: schedule transcription after completion
const scheduleTranscription: SideEffect = async (call) => {
  await voiceQueue.add('transcribe-job', {
    type: 'transcribe',
    callId: call.callId,
  });
};
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| State machine pattern | Explicit transition table | Auditable, testable, visualizable |
| Concurrency control | Optimistic locking (version field) | Prevents race conditions on rapid transitions |
| Side effects | Async, fire-and-forget after state change | State change is source of truth; effects can be retried |
| Guard conditions | Predicate functions per transition | Complex business rules without polluting state machine |
| Event emission | Every transition emits `call.state.changed` | Downstream services react to state changes |

## Integration Points

- **Ch 05 (Microservices)** — Call state machine lives in call-service
- **Ch 09 (Event-Driven Data Flow)** — State changes emit Kafka events
- **Ch 09 (Event Sourcing)** — State transitions are the core audit trail
- **Ch 03 (Database)** — Call state stored in PostgreSQL `calls` table with version column

## Production Considerations

- **Race Conditions**: Concurrent transitions for same call use PostgreSQL row-level locks
- **Timeout Handling**: Ringing state has 30-second timeout → automatically transitions to voicemail or failed
- **Recovery**: If service restarts mid-call, state machine replays from last persisted state
- **Monitoring**: State transition metrics — count per transition, failure rate, latency
- **Testing**: State machine tested exhaustively — all transitions, invalid transitions, concurrent transitions
