# Section 02: Rule Evaluation Engine

## Overview

The rule evaluation engine processes events against defined alert rules. Rules are expressed in a DSL that supports conditions, aggregations, thresholds, and multi-rule chaining. The engine evaluates rules efficiently using indexing, pre-compilation, and incremental evaluation.

## Implementation Approach

```typescript
interface AlertRule {
  id: string;
  name: string;
  enabled: boolean;
  conditions: RuleCondition[];
  aggregations: AggregationConfig[];
  evalWindow: number; // seconds
  cooldown: number; // seconds
  severity: 'critical' | 'major' | 'minor' | 'warning';
  actions: RuleAction[];
}

interface RuleCondition {
  field: string;
  operator: 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'in' | 'contains' | 'regex';
  value: unknown;
}

class RuleEngine {
  async evaluate(event: EnrichedEvent): Promise<RuleEvaluation[]> {
    const applicableRules = await this.findApplicableRules(event);
    const evaluations: RuleEvaluation[] = [];

    for (const rule of applicableRules) {
      if (await this.isInCooldown(rule, event)) continue;
      const result = await this.evaluateRule(rule, event);
      if (result.triggered) {
        evaluations.push(result);
        await this.setCooldown(rule, event);
      }
    }
    return evaluations;
  }

  private async evaluateRule(rule: AlertRule, event: EnrichedEvent): Promise<RuleEvaluation> {
    // Evaluate all conditions
    const conditionResults = rule.conditions.map(c => this.evaluateCondition(c, event));
    const allConditionsMet = conditionResults.every(r => r);

    if (!allConditionsMet) {
      return { ruleId: rule.id, triggered: false };
    }

    // Check aggregations if any
    if (rule.aggregations.length > 0) {
      const windowData = await this.getWindowData(rule.evalWindow, event);
      const aggResults = rule.aggregations.map(a => this.evaluateAggregation(a, windowData));
      const aggMet = aggResults.every(r => r);
      if (!aggMet) return { ruleId: rule.id, triggered: false };
    }

    return {
      ruleId: rule.id,
      triggered: true,
      severity: rule.severity,
      evaluatedAt: new Date().toISOString(),
      event,
    };
  }

  private evaluateCondition(condition: RuleCondition, event: EnrichedEvent): boolean {
    const value = this.resolveField(condition.field, event);
    switch (condition.operator) {
      case 'gt': return value > condition.value;
      case 'gte': return value >= condition.value;
      case 'lt': return value < condition.value;
      case 'lte': return value <= condition.value;
      case 'eq': return value === condition.value;
      case 'in': return (condition.value as unknown[]).includes(value);
      default: return false;
    }
  }
}
```

## Integration Points

- **Rule Management UI**: CRUD for alert rules
- **Rule Testing**: Test rules against historical events
- **Performance Metrics**: Rule evaluation latency tracked

## Production Considerations

- **Rule Compilation**: Pre-compile rules for fast evaluation
- **Indexing**: Index rules by event type and metric
- **Cooldown Escalation**: Prevent alert storms with cooldown periods
