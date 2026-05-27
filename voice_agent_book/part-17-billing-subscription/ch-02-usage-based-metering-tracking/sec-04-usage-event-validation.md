# Section 04: Usage Event Validation

## Schema Validation

Every usage event must pass schema validation before ingestion. Invalid events are routed to a dead letter queue for inspection and possible replay. Schema validation ensures data quality and prevents billing errors.

Validation uses JSON Schema with additional business rules:

```typescript
const usageEventSchema = {
  type: 'object',
  required: ['idempotencyKey', 'tenantId', 'eventType', 'meter', 'quantity', 'timestamp'],
  properties: {
    idempotencyKey: {
      type: 'string',
      pattern: '^[a-zA-Z0-9_-]{8,128}$',
    },
    tenantId: {
      type: 'string',
      pattern: '^tenant_[a-zA-Z0-9]{16}$',
    },
    eventType: {
      type: 'string',
      enum: [
        'voice.call_minute',
        'voice.transcription_second',
        'voice.tts_character',
        'storage.gigabyte_month',
        'api.request',
      ],
    },
    meter: {
      type: 'string',
      pattern: '^[a-z_]+$',
    },
    quantity: {
      type: 'number',
      minimum: 0,
      maximum: 1000000,
    },
    timestamp: {
      type: 'string',
      format: 'date-time',
    },
    metadata: {
      type: 'object',
      maxProperties: 20,
    },
  },
};

class UsageEventValidator {
  private validators: Map<string, ValidateFunction>;

  constructor() {
    this.validators = new Map();
    this.registerSchema('usage_event', usageEventSchema);
  }

  validate(event: UsageEvent): ValidationResult {
    const validator = this.validators.get('usage_event');
    const valid = validator(event);

    if (!valid) {
      return {
        valid: false,
        errors: validator.errors.map(e => ({
          path: e.instancePath,
          message: e.message,
          params: e.params,
        })),
      };
    }

    return { valid: true, errors: [] };
  }

  async validateAndProcess(event: UsageEvent): Promise<void> {
    // 1. Schema validation
    const schemaResult = this.validate(event);
    if (!schemaResult.valid) {
      await this.deadLetterQueue.send(event, schemaResult.errors);
      return;
    }

    // 2. Tenant verification
    const tenant = await this.tenantService.getTenant(event.tenantId);
    if (!tenant || tenant.status !== 'active') {
      await this.deadLetterQueue.send(event, {
        reason: `Tenant ${event.tenantId} not found or inactive`,
      });
      return;
    }

    // 3. Meter verification
    const meter = await this.meterRegistry.getMeter(event.meter);
    if (!meter) {
      await this.deadLetterQueue.send(event, {
        reason: `Unknown meter: ${event.meter}`,
      });
      return;
    }

    // 4. Duplicate check
    const isDuplicate = await this.dedupService.check(event.idempotencyKey);
    if (isDuplicate) {
      logger.warn('Duplicate event', { key: event.idempotencyKey });
      return; // Silently skip
    }

    // 5. Quota check at ingestion
    const currentUsage = await this.realtimeCounter.getCurrentUsage(
      event.tenantId, event.meter, currentPeriod()
    );
    const plan = await this.planService.getTenantPlan(event.tenantId);

    if (currentUsage + event.quantity > plan.limits[event.meter]?.hardCap) {
      if (plan.limits[event.meter]?.actionOnExceeded === 'block') {
        logger.warn('Usage blocked — hard cap exceeded', {
          tenant: event.tenantId,
          meter: event.meter,
          current: currentUsage,
          attempted: event.quantity,
          cap: plan.limits[event.meter].hardCap,
        });
        return; // Block the event
      }
    }

    // 6. Process
    await this.pipeline.process(event);
  }
}
```

## Duplicate Detection

Duplicate events are the most common source of billing errors. They occur when services retry event emission after a timeout (the event was actually processed) or when the event bus delivers a message twice (at-least-once delivery).

```
Duplicate Detection Flow:
[Event Arrives]
    ↓
[Extract idempotency_key]
    ↓
[Check Redis: key exists?]
    ├── YES → Log duplicate, discard event
    └── NO  → SET key with TTL, continue processing
                  ↓
         [Process event normally]
                  ↓
         [On failure: don't clear key — retry will skip]
```

The dedup window is 7 days by default, matching the billing period boundary buffer. Keys are stored in Redis with automatic TTL expiration.

## Out-of-Order Handling

Events may arrive out of order due to network delays or service restarts. The metering system must handle late-arriving events gracefully.

```typescript
class OutOfOrderHandler {
  private readonly LATE_WINDOW_HOURS = 72;

  async handleEvent(event: UsageEvent): Promise<void> {
    const now = new Date();
    const eventTime = new Date(event.timestamp);
    const delayHours = (now.getTime() - eventTime.getTime()) / (1000 * 60 * 60);

    if (delayHours < 0) {
      // Future event — reject
      await this.deadLetterQueue.send(event, {
        reason: 'Event timestamp is in the future',
      });
      return;
    }

    if (delayHours > this.LATE_WINDOW_HOURS) {
      // Very late event — log and route to manual review
      await this.manualReviewQueue.send(event, {
        reason: `Event is ${delayHours}h late, beyond ${this.LATE_WINDOW_HOURS}h window`,
      });
      return;
    }

    if (delayHours > 1) {
      // Late but within window — process but mark as late
      logger.warn('Late event processed', {
        key: event.idempotencyKey,
        delayHours,
      });
      event.metadata['late_arrival'] = 'true';
      event.metadata['original_delay_hours'] = delayHours.toString();
    }

    // Process the event (may update a closed billing period)
    await this.pipeline.process(event);

    // Check if billing period is already closed
    const periodClosed = await this.billingService.isPeriodClosed(
      event.tenantId, event.billingPeriodStart, event.billingPeriodEnd
    );
    if (periodClosed) {
      await this.reconciliationService.recordLateEvent(event);
    }
  }
}
```

## Quota Check at Ingestion

Each event triggers a quota check before processing. If the tenant's usage would exceed their plan's hard cap, the event can be blocked. This prevents runaway usage and bill shock.

```typescript
interface QuotaCheckResult {
  allowed: boolean;
  currentUsage: number;
  limit: number;
  remaining: number;
  action: 'allow' | 'warn' | 'block' | 'upgrade_prompt';
}
```

## Open-Source Tools

- **Ajv** (MIT) — JSON Schema validation for usage events
- **Redis** — Idempotency key storage and deduplication
- **RabbitMQ** — Dead letter queues for invalid events
- **Prometheus** — Validation metrics and error rate monitoring

## Integration Points

Event validation connects to the tenant service (for tenant status verification), the plan service (for quota checks), the deduplication service (idempotency), and the dead letter queue (for manual reconciliation).

## Production Considerations

- Monitor validation failure rates by error type
- Set up alerts for sudden drops in event volume (pipeline failure)
- Implement circuit breakers for downstream service failures
- Log all validation failures with full event context
- Provide a manual replay UI for dead letter queue events
- Test schema changes against historical event data

## Open-Source First Philosophy

Ajv (MIT) provides industry-standard JSON Schema validation without licensing costs. Redis handles deduplication at massive scale. RabbitMQ's dead letter queues provide reliable failure handling. Prometheus and Grafana (both open-source) monitor the pipeline's health. This all-open-source stack replaces proprietary validation and monitoring tools while maintaining enterprise-grade reliability.
