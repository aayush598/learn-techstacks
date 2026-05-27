# Section 01: Dunning Workflow Design

## Dunning Process Stages

The dunning workflow manages failed payment recovery through a series of escalating stages. Each stage has specific actions, communications, and business rules.

```
[Payment Failure]
    ↓
[Stage 1: Immediate Retry]
    ├── Attempt payment immediately
    ├── Card network retry logic
    └── Log failure reason
    ↓
[Stage 2: Soft Reminder]
    ├── Day 1-3: Email notification
    ├── In-app banner
    └── No service restriction
    ↓
[Stage 3: Active Recovery]
    ├── Day 4-7: Escalated communication
    ├── SMS + Email
    ├── Payment link generation
    └── Retry schedule active
    ↓
[Stage 4: Grace Period]
    ├── Day 8-14: Service read-only
    ├── Final notices
    └── Payment method update requested
    ↓
[Stage 5: Suspension]
    ├── Day 15-21: Service suspended
    ├── Data retention period begins
    └── Win-back workflow starts
```

```typescript
enum DunningStage {
  IMMEDIATE_RETRY = 'immediate_retry',
  SOFT_REMINDER = 'soft_reminder',
  ACTIVE_RECOVERY = 'active_recovery',
  GRACE_PERIOD = 'grace_period',
  SUSPENSION = 'suspension',
  CANCELLATION = 'cancellation',
}

interface DunningState {
  subscriptionId: string;
  tenantId: string;
  customerId: string;
  currentStage: DunningStage;
  failureCount: number;
  consecutiveFailures: number;
  lastFailureReason: string;
  lastFailureDate: string;
  stageEnteredAt: string;
  escalationLevel: number;
  totalRetryAttempts: number;
  paymentMethodId: string;
  gracePeriodEndsAt?: string;
  suspensionDate?: string;
}

interface DunningStageConfig {
  stage: DunningStage;
  maxDurationHours: number;
  retrySchedule: number[];       // Hours after stage start
  communicationChannels: CommunicationChannel[];
  serviceRestriction: 'none' | 'read_only' | 'suspended';
  attemptsBeforeEscalation: number;
}

class DunningWorkflow {
  private stages: Map<DunningStage, DunningStageConfig>;

  constructor() {
    this.stages = new Map([
      [DunningStage.IMMEDIATE_RETRY, {
        stage: DunningStage.IMMEDIATE_RETRY,
        maxDurationHours: 24,
        retrySchedule: [0, 1, 2, 4],
        communicationChannels: [],
        serviceRestriction: 'none',
        attemptsBeforeEscalation: 3,
      }],
      [DunningStage.SOFT_REMINDER, {
        stage: DunningStage.SOFT_REMINDER,
        maxDurationHours: 72,
        retrySchedule: [24, 48],
        communicationChannels: ['email', 'in_app'],
        serviceRestriction: 'none',
        attemptsBeforeEscalation: 2,
      }],
      [DunningStage.ACTIVE_RECOVERY, {
        stage: DunningStage.ACTIVE_RECOVERY,
        maxDurationHours: 96,
        retrySchedule: [72],
        communicationChannels: ['email', 'sms', 'in_app'],
        serviceRestriction: 'none',
        attemptsBeforeEscalation: 3,
      }],
      [DunningStage.GRACE_PERIOD, {
        stage: DunningStage.GRACE_PERIOD,
        maxDurationHours: 168,
        retrySchedule: [120, 144, 168],
        communicationChannels: ['email', 'sms', 'push'],
        serviceRestriction: 'read_only',
        attemptsBeforeEscalation: 3,
      }],
      [DunningStage.SUSPENSION, {
        stage: DunningStage.SUSPENSION,
        maxDurationHours: 168,
        retrySchedule: [],
        communicationChannels: ['email'],
        serviceRestriction: 'suspended',
        attemptsBeforeEscalation: 1,
      }],
    ]);
  }

  async transitionStage(
    state: DunningState,
    toStage: DunningStage
  ): Promise<DunningState> {
    const config = this.stages.get(toStage);
    if (!config) throw new Error(`Unknown stage: ${toStage}`);

    state.currentStage = toStage;
    state.stageEnteredAt = new Date().toISOString();
    state.escalationLevel += 1;

    if (toStage === DunningStage.GRACE_PERIOD) {
      state.gracePeriodEndsAt = this.calculateGraceEnd();
    }

    if (toStage === DunningStage.SUSPENSION) {
      state.suspensionDate = new Date().toISOString();
    }

    await this.persistState(state);
    await this.executeStageActions(state, config);

    return state;
  }

  private async executeStageActions(
    state: DunningState,
    config: DunningStageConfig
  ): Promise<void> {
    // Apply service restriction
    await this.applyServiceRestriction(state.subscriptionId, config.serviceRestriction);

    // Schedule retries
    for (const delayHours of config.retrySchedule) {
      await this.scheduleRetry(state, delayHours);
    }

    // Send communications
    for (const channel of config.communicationChannels) {
      await this.dispatchCommunication(state, channel);
    }
  }
}
```

## Retry Schedule

The retry schedule follows payment network best practices with exponential backoff.

```typescript
interface RetrySchedule {
  attemptNumber: number;
  delayHours: number;
  retryWindow: string;           // Best time window for this attempt
  failureAction: 'retry' | 'escalate' | 'notify_only';
}

function buildRetrySchedule(): RetrySchedule[] {
  return [
    { attemptNumber: 1, delayHours: 0, retryWindow: 'immediate', failureAction: 'retry' },
    { attemptNumber: 2, delayHours: 2, retryWindow: 'evening', failureAction: 'retry' },
    { attemptNumber: 3, delayHours: 24, retryWindow: 'next_day', failureAction: 'retry' },
    { attemptNumber: 4, delayHours: 72, retryWindow: 'weekend', failureAction: 'retry' },
    { attemptNumber: 5, delayHours: 168, retryWindow: 'next_week', failureAction: 'notify_only' },
  ];
}
```

## Escalation Path

When retry attempts fail, the dunning process escalates through communication intensity and service restrictions.

```typescript
interface EscalationAction {
  stage: DunningStage;
  action: string;
  responsibleParty: 'system' | 'support_agent' | 'finance_team';
  autoTrigger: boolean;
  notifyCustomer: boolean;
}

const ESCALATION_PATH: EscalationAction[] = [
  { stage: DunningStage.SOFT_REMINDER, action: 'Send soft reminder email', responsibleParty: 'system', autoTrigger: true, notifyCustomer: true },
  { stage: DunningStage.ACTIVE_RECOVERY, action: 'Send escalation email with payment link', responsibleParty: 'system', autoTrigger: true, notifyCustomer: true },
  { stage: DunningStage.GRACE_PERIOD, action: 'Assign to support for review', responsibleParty: 'support_agent', autoTrigger: false, notifyCustomer: false },
  { stage: DunningStage.SUSPENSION, action: 'Notify finance team of potential churn', responsibleParty: 'finance_team', autoTrigger: true, notifyCustomer: false },
];

class EscalationManager {
  async escalate(state: DunningState): Promise<void> {
    const actions = ESCALATION_PATH.filter(a => a.stage === state.currentStage);

    for (const action of actions) {
      if (action.autoTrigger) {
        await this.executeAction(action, state);
      } else {
        await this.createTicket(action, state);
      }
    }
  }
}
```

## Communication Timing

Each communication is timed based on the dunning stage and customer timezone.

```typescript
interface CommunicationTiming {
  stage: DunningStage;
  channels: ChannelTiming[];
}

interface ChannelTiming {
  channel: CommunicationChannel;
  sendAfterHours: number;
  businessHoursOnly: boolean;
  maxPerDay: number;
}

function getNextCommunicationTime(
  state: DunningState,
  channel: CommunicationChannel
): Date {
  const timing = getChannelTiming(state.currentStage, channel);
  const sendTime = new Date(state.stageEnteredAt);
  sendTime.setHours(sendTime.getHours() + timing.sendAfterHours);

  if (timing.businessHoursOnly) {
    return adjustToBusinessHours(sendTime, state.customerId);
  }

  return sendTime;
}
```

## Open-Source Tools

- **BullMQ** — Dunning workflow orchestration and retry scheduling
- **PostgreSQL** — Dunning state persistence
- **Redis** — Real-time dunning state cache
- **Trigger.dev** (MIT) — Dunning event handling
- **Inbucket** (MIT) — Email preview and testing for dunning communications

## Integration Points

Dunning workflow integrates with the payment gateway (retry attempts), notification service (email/SMS/push), subscription management (service restrictions), customer portal (payment method updates), and CRM (escalation tickets).

## Production Considerations

- Respect customer timezone for communication timing
- Implement rate limiting on retry attempts per card network rules
- Track dunning effectiveness metrics by stage
- Monitor for fraudulent retry patterns
- Allow manual override for enterprise customers
- Sync with card network retry windows (Visa: 3 attempts, Mastercard: 5 attempts)
- Handle concurrent payment updates during dunning

## Open-Source First Philosophy

BullMQ manages the entire dunning workflow with retry queues and delayed jobs. PostgreSQL stores dunning state with full audit history. Redis provides low-latency state lookups for real-time service restriction decisions. This stack replaces proprietary dunning management platforms like Chargebee or Recurly at a fraction of the cost while maintaining full control over the dunning logic.
