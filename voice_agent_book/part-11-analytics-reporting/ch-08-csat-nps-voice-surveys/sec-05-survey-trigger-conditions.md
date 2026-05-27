# Section 05: Survey Trigger Conditions

## Overview

Survey trigger conditions determine when and to whom surveys are delivered after a call interaction. Rather than sending a survey after every call, the trigger engine evaluates a configurable set of rules — call outcome, duration, agent handle time, transfer count, customer segment, sentiment threshold, and time-based sampling — to selectively dispatch surveys. This prevents survey fatigue and ensures that responses are collected from interactions that provide the most actionable feedback.

The trigger engine supports both deterministic rules (e.g., "send CSAT survey after every successful call with duration > 30 seconds") and probabilistic sampling (e.g., "send NPS survey to 20% of completed calls"). It also manages suppression windows (e.g., "do not send a survey to the same customer within 7 days"), time-of-day restrictions, and holiday calendars. All trigger evaluations happen in real-time within the survey orchestrator, processing the call completion event against the active rule set for the tenant.

## Architecture

```
                Survey Trigger Engine

   Call Complete Event → Kafka → Trigger Evaluator
                                      |
                         ┌────────────┴────────────┐
                         ▼                         ▼
                   Rule Matcher           Sampling Decider
                   (deterministic)        (probabilistic)
                         |                         |
                         ▼                         ▼
                   Suppression Check ←─ Customer History
                         |
                   ┌─────┴─────┐
                   ▼           ▼
              Schedule      Drop Event
              Survey        (no survey)
```

## Design Decisions

- **Rule-based engine with priority ordering over flat evaluation:** Trigger rules are evaluated in priority order (1-100). Higher-priority rules are evaluated first and can short-circuit lower-priority rules. A "suppress all surveys" holiday rule at priority 1 prevents any survey from being sent on holidays. A "send NPS after high-sentiment calls" rule at priority 50 runs only if no higher-priority rule matched. Trade-off: priority ordering requires careful administration to avoid accidental suppression; a misconfigured high-priority rule can silence all surveys.

- **Customer suppression window with configurable duration over no suppression:** The engine maintains a per-customer, per-survey-type suppression window (configurable per tenant, default 7 days for CSAT, 30 days for NPS). If a customer has received a survey of the same type within the window, the trigger is suppressed. Trade-off: suppression tracking requires a fast lookup store (Redis) keyed by customer ID + survey type, and the window can cause low-volume customers to receive too few surveys for statistically significant scoring.

- **Probabilistic sampling for high-volume campaigns over always-send:** For campaigns processing 10,000+ calls per day, sending a survey after every call would overwhelm customers and degrade response quality. Sampling rates are configured per campaign as a percentage (1-100%). The engine uses consistent hashing on customer ID so the same customer is either always sampled or never sampled (deterministic per customer), avoiding partial-survey bias. Trade-off: sampling reduces total response volume, requiring larger sample sizes for statistically significant agent-level scores.

## Implementation Approach

```typescript
interface TriggerRule {
  id: string;
  tenantId: string;
  surveyType: 'CSAT' | 'NPS' | 'CES' | 'custom';
  priority: number;
  enabled: boolean;
  conditions: Condition[];
  samplingRate?: number; // 0-100, null for deterministic
  suppressionWindowMs?: number;
}

interface Condition {
  field: string;
  operator: 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'in' | 'not_in' | 'between';
  value: unknown;
}

interface TriggerContext {
  call: CallCompletedEvent;
  customer: CustomerProfile;
  tenantConfig: TenantConfig;
  recentSurveys: SurveyDeliveryRecord[];
}

class TriggerEvaluator {
  async evaluate(context: TriggerContext): Promise<SurveyDecision | null> {
    const rules = await this.getActiveRules(context.tenantId);

    // Sort by priority descending (highest first)
    const sorted = rules.sort((a, b) => b.priority - a.priority);

    for (const rule of sorted) {
      if (!rule.enabled) continue;

      // Check conditions
      const conditionsMet = rule.conditions.every(c =>
        this.evaluateCondition(context, c)
      );
      if (!conditionsMet) continue;

      // Check suppression window
      if (rule.suppressionWindowMs) {
        const lastSurvey = this.findRecentSurvey(
          context.recentSurveys,
          rule.surveyType,
          rule.suppressionWindowMs
        );
        if (lastSurvey) {
          const timeUntilEligible = lastSurvey.timestamp + rule.suppressionWindowMs - Date.now();
          return {
            decision: 'suppressed',
            ruleId: rule.id,
            reason: `suppression_window:${Math.ceil(timeUntilEligible / 3600000)}h`,
          };
        }
      }

      // Check sampling
      if (rule.samplingRate !== undefined && rule.samplingRate < 100) {
        const hash = this.consistentHash(context.customer.id, rule.id);
        if (hash >= rule.samplingRate / 100) {
          return {
            decision: 'skipped_sampling',
            ruleId: rule.id,
            reason: `sampling_rate:${rule.samplingRate}%`,
          };
        }
      }

      return {
        decision: 'send',
        ruleId: rule.id,
        surveyType: rule.surveyType,
      };
    }

    return null; // No matching rule
  }

  private evaluateCondition(context: TriggerContext, condition: Condition): boolean {
    const value = this.getFieldValue(context, condition.field);
    if (value === undefined || value === null) return false;

    switch (condition.operator) {
      case 'eq': return value === condition.value;
      case 'neq': return value !== condition.value;
      case 'gt': return typeof value === 'number' && value > (condition.value as number);
      case 'gte': return typeof value === 'number' && value >= (condition.value as number);
      case 'lt': return typeof value === 'number' && value < (condition.value as number);
      case 'lte': return typeof value === 'number' && value <= (condition.value as number);
      case 'in': return Array.isArray(condition.value) && condition.value.includes(value);
      case 'not_in': return Array.isArray(condition.value) && !condition.value.includes(value);
      case 'between': {
        if (!Array.isArray(condition.value) || condition.value.length !== 2) return false;
        return typeof value === 'number' && value >= condition.value[0] && value <= condition.value[1];
      }
      default: return false;
    }
  }

  private consistentHash(customerId: string, ruleId: string): number {
    const key = `${customerId}:${ruleId}`;
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      const char = key.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash % 100) / 100;
  }

  private getFieldValue(context: TriggerContext, field: string): unknown {
    const parts = field.split('.');
    let current: Record<string, unknown> = context as unknown as Record<string, unknown>;
    for (const part of parts) {
      if (current && typeof current === 'object' && part in current) {
        current = current[part] as Record<string, unknown>;
      } else {
        return undefined;
      }
    }
    return current;
  }

  private findRecentSurvey(
    surveys: SurveyDeliveryRecord[],
    type: string,
    windowMs: number
  ): SurveyDeliveryRecord | undefined {
    const cutoff = Date.now() - windowMs;
    return surveys.find(s => s.surveyType === type && s.timestamp > cutoff);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis (RSAL) | Server | Suppression window and customer history cache |
| Apache Kafka (Apache 2.0) | Server | Event trigger source |
| JSON Logic (MIT) | Server | Advanced condition evaluation |
| Node.js Crypto (MIT) | Server | Consistent hashing for sampling |

## Production Considerations

**Scaling:** Trigger rules are cached in Redis with per-tenant versioning. When a rule is updated, the cache version increments and the evaluator reloads rules asynchronously. For high-throughput tenants (100+ calls/second), trigger evaluation must complete in under 50 ms; pre-compile conditions into executable functions at load time rather than interpreting JSON structures on every evaluation.

**Security:** Trigger rules are tenant-scoped and validated against a schema that restricts which call event fields can be referenced. Prevent rules from accessing PII fields (customer name, phone number) in conditions. Rule creation requires admin privileges with audit logging for all rule changes, including enable/disable toggles.

**Monitoring:** Track trigger evaluation latency, match rate per rule (percentage of evaluations that matched), sampling rate accuracy (actual vs. configured), suppression rate per window, and total surveys triggered vs. suppressed. Alert if a high-priority rule matches zero times in a 24-hour period (possible misconfiguration) or if evaluation latency exceeds 200 ms at p99.
