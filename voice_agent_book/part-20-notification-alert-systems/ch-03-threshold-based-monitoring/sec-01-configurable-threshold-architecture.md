# Section 01: Configurable Threshold Architecture

## Overview

The threshold configuration system defines how metric values are compared against thresholds to trigger alerts. Thresholds are defined with data source bindings, comparison operators, evaluation windows, and severity levels. The architecture supports simple static thresholds, dynamic thresholds, and composite multi-metric thresholds.

## Implementation Approach

```typescript
interface Threshold {
  id: string;
  name: string;
  metricSource: MetricSource;
  conditions: ThresholdCondition[];
  severity: string;
  evaluationWindow: number; // seconds
  cooldown: number; // seconds
  enabled: boolean;
}

interface MetricSource {
  type: 'prometheus' | 'otel' | 'custom' | 'log';
  query: string;
  aggregation: 'avg' | 'sum' | 'max' | 'min' | 'count' | 'p95' | 'p99';
  interval: number; // seconds
}

interface ThresholdCondition {
  operator: '>' | '>=' | '<' | '<=' | '==' | '!=' | 'within_range' | 'outside_range';
  value: number;
  range?: [number, number];
  sustainedFor: number; // consecutive evaluations
}

class ThresholdEvaluator {
  async evaluate(threshold: Threshold): Promise<ThresholdResult> {
    const metricValue = await this.queryMetric(threshold.metricSource);
    const conditionsMet = threshold.conditions.map(c => this.evaluateCondition(metricValue, c));
    const allMet = conditionsMet.every(c => c);
    return { thresholdId: threshold.id, metricValue, conditionsMet, triggered: allMet };
  }

  private async queryMetric(source: MetricSource): Promise<number> {
    switch (source.type) {
      case 'prometheus':
        return this.prometheusClient.query(source.query);
      case 'otel':
        return this.otelClient.query(source.query, source.aggregation);
      case 'log':
        return this.logClient.count(source.query, source.interval);
      default:
        throw new Error(`Unknown source: ${source.type}`);
    }
  }

  private evaluateCondition(value: number, condition: ThresholdCondition): boolean {
    switch (condition.operator) {
      case '>': return value > condition.value;
      case '>=': return value >= condition.value;
      case '<': return value < condition.value;
      case '<=': return value <= condition.value;
      case '==': return value === condition.value;
      case 'within_range': return value >= condition.range![0] && value <= condition.range![1];
      case 'outside_range': return value < condition.range![0] || value > condition.range![1];
      default: return false;
    }
  }
}

class ThresholdManager {
  private thresholds: Map<string, Threshold> = new Map();
  private evaluationCounts: Map<string, number> = new Map();

  async createThreshold(config: CreateThresholdInput): Promise<Threshold> {
    const threshold: Threshold = { id: generateId(), ...config, enabled: true };
    this.thresholds.set(threshold.id, threshold);
    await this.storage.save(threshold);
    return threshold;
  }

  async updateThreshold(id: string, config: Partial<Threshold>): Promise<Threshold> {
    const existing = this.thresholds.get(id);
    if (!existing) throw new Error('Threshold not found');
    const updated = { ...existing, ...config };
    this.thresholds.set(id, updated);
    await this.storage.update(updated);
    return updated;
  }
}
```

## Integration Points

- **Metrics Pipeline**: Thresholds bind to metric sources
- **Alert Engine**: Threshold breaches trigger alert creation
- **Configuration UI**: Web interface for threshold management

## Production Considerations

- **Threshold Validation**: Validate thresholds before saving (test query syntax)
- **Evaluation Scheduling**: Stagger evaluations to prevent thundering herd
- **Versioning**: Track threshold changes for audit
