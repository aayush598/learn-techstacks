# Section 01: Post-Call Survey Framework

## Overview

The post-call survey framework is the core engine that manages the lifecycle of customer satisfaction surveys triggered after a call ends. It handles survey creation, delivery channel selection (voice IVR, SMS, email, in-app), response collection, and integration with the analytics pipeline. The framework is designed to support multiple survey methodologies — CSAT, NPS, CES, and custom questionnaires — with a consistent event-driven architecture.

When a call completes, the call completion event on Kafka triggers the survey orchestrator, which evaluates trigger conditions (e.g., call duration > 30 seconds, agent transfer occurred) and selects the appropriate survey template. The survey is then delivered via the configured channel, and the response is streamed back into the analytics pipeline for correlation with call metadata, sentiment scores, and agent performance metrics. The framework processes over 10,000 surveys per hour per tenant with end-to-end latency under 5 seconds from call completion to survey delivery.

## Architecture

```
               Post-Call Survey Framework

   Call Complete Event → Kafka → Survey Orchestrator
                                      |
                           Trigger Evaluator (rules engine)
                                      |
                           Survey Template Selector
                                      |
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                    Voice IVR      SMS/Email     In-App
                    Delivery       Delivery      Delivery
                         |            |            |
                         ▼            ▼            ▼
                    Response Collector → Kafka → Analytics Pipeline
                                                    |
                                          Survey Response Store
                                                    |
                                          Reporting / Dashboards
```

## Design Decisions

- **Event-driven orchestration over scheduled polling:** The framework subscribes to call completion events from Kafka rather than polling for completed calls on a timer. This ensures sub-second survey trigger latency and reduces database load. Trade-off: if the Kafka consumer falls behind during traffic spikes, survey delivery may be delayed; a dead-letter queue with retry logic handles failed events.

- **Template-based surveys over hard-coded questions:** Survey templates are stored as JSON schemas in a database, allowing non-technical teams to create and modify surveys without code changes. Templates support skip logic, weighted scoring, and multi-language content. Trade-off: template evaluation requires a rules engine at runtime, adding 10-20 ms per survey trigger compared to hard-coded logic.

- **Multi-channel delivery with fallback over single-channel:** The framework attempts primary channel delivery (e.g., voice IVR) and falls back to secondary channels (SMS, email) if the primary fails or times out. This increases response rates by 15-25% compared to single-channel delivery. Trade-off: multi-channel delivery requires managing channel-specific state machines and deduplication to prevent a customer from receiving duplicate surveys across channels.

## Implementation Approach

```typescript
interface SurveyTemplate {
  id: string;
  tenantId: string;
  name: string;
  methodology: 'CSAT' | 'NPS' | 'CES' | 'custom';
  questions: SurveyQuestion[];
  channels: DeliveryChannel[];
  triggerConditions: TriggerRule[];
  scoringConfig: ScoringConfig;
  language: string;
  version: number;
}

interface SurveyQuestion {
  id: string;
  text: string;
  type: 'rating' | 'binary' | 'open_ended' | 'multiple_choice' | 'nps_scale';
  required: boolean;
  skipLogic?: SkipCondition[];
  weight?: number;
}

interface TriggerRule {
  field: string;
  operator: 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'in' | 'contains';
  value: unknown;
}

interface DeliveryChannel {
  type: 'voice_ivr' | 'sms' | 'email' | 'in_app';
  priority: number;
  config: Record<string, unknown>;
  fallbackChannels: string[];
}

class SurveyOrchestrator {
  private templates: Map<string, SurveyTemplate> = new Map();
  private consumer: KafkaConsumer;
  private deliveryDispatcher: DeliveryDispatcher;

  async onCallCompleted(event: CallCompletedEvent): Promise<void> {
    const template = await this.selectTemplate(event);
    if (!template) return;

    const response = await this.deliveryDispatcher.dispatch({
      template,
      customer: event.customer,
      channel: template.channels[0],
      callSid: event.callSid,
      tenantId: event.tenantId,
    });

    await this.recordDelivery({
      surveyId: template.id,
      callSid: event.callSid,
      channel: response.channel,
      status: response.status,
      timestamp: Date.now(),
    });
  }

  private async selectTemplate(event: CallCompletedEvent): Promise<SurveyTemplate | null> {
    for (const template of this.templates.values()) {
      if (template.tenantId !== event.tenantId) continue;
      const matches = template.triggerConditions.every(rule =>
        this.evaluateRule(event, rule)
      );
      if (matches) return template;
    }
    return null;
  }

  private evaluateRule(event: CallCompletedEvent, rule: TriggerRule): boolean {
    const value = (event as Record<string, unknown>)[rule.field];
    switch (rule.operator) {
      case 'eq': return value === rule.value;
      case 'gt': return typeof value === 'number' && value > (rule.value as number);
      case 'gte': return typeof value === 'number' && value >= (rule.value as number);
      case 'lt': return typeof value === 'number' && value < (rule.value as number);
      case 'lte': return typeof value === 'number' && value <= (rule.value as number);
      case 'in': return Array.isArray(rule.value) && rule.value.includes(value);
      case 'contains': return typeof value === 'string' && value.includes(rule.value as string);
      default: return false;
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| JSON Schema (MIT) | Server | Survey template validation |
| Twilio (Apache 2.0) | Server | Voice IVR survey delivery |
| Kafka (Apache 2.0) | Server | Event bus for call completion events |
| i18next (MIT) | Server/Client | Multi-language survey translation |

## Production Considerations

**Scaling:** Survey templates are cached in Redis with TTL-based invalidation to reduce database load during high-traffic periods. The delivery dispatcher uses a priority queue per channel with backpressure: if the SMS delivery queue exceeds 10,000 messages, lower-priority surveys are temporarily deferred. Each tenant's survey responses are partitioned by tenant ID in Kafka to ensure isolated processing.

**Security:** Survey responses containing PII (phone numbers, caller names) are encrypted at rest and in transit. The template API requires admin-level authentication and validates that templates cannot access fields outside the allowed call event schema. Rate-limit survey deliveries per customer to at most 1 survey per 24 hours to prevent spam.

**Monitoring:** Track survey delivery latency (p99 under 5 seconds), response rate per channel per template, delivery failure rate by channel, and trigger-to-delivery conversion. Alert if the response rate drops below 10% for any active template, if SMS delivery failure exceeds 5%, or if the orchestrator consumer lag exceeds 10,000 events.
