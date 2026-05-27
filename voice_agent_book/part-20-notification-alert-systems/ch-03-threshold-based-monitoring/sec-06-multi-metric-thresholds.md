# Section 06: Multi-Metric Thresholds

## Overview

Multi-metric thresholds combine multiple metric conditions using AND/OR logic for more precise alerting. Composite thresholds evaluate complex conditions like "error rate > 5% AND latency > 500ms". Ratio-based thresholds compare two metrics, and trend-based thresholds detect directional changes.

## Implementation Approach

```typescript
type CompositeOperator = 'AND' | 'OR';
type ThresholdType = 'simple' | 'composite' | 'ratio' | 'trend';

interface MultiMetricThreshold {
  id: string;
  type: ThresholdType;
  conditions: SubCondition[];
  operator: CompositeOperator;
  severity: string;
}

interface SubCondition {
  metricSource: MetricSource;
  operator: string;
  value: number;
  weight?: number; // for weighted scoring
}

class MultiMetricEvaluator {
  async evaluate(threshold: MultiMetricThreshold): Promise<MultiMetricResult> {
    const results = await Promise.all(
      threshold.conditions.map(c => this.evaluateSubCondition(c))
    );

    let triggered: boolean;
    switch (threshold.operator) {
      case 'AND':
        triggered = results.every(r => r.met);
        break;
      case 'OR':
        triggered = results.some(r => r.met);
        break;
    }

    return {
      triggered,
      conditions: results,
      score: triggered ? this.computeScore(results) : 0,
    };
  }

  private async evaluateSubCondition(condition: SubCondition): Promise<SubConditionResult> {
    const value = await this.queryMetric(condition.metricSource);
    const met = this.evaluateSimpleCondition(value, condition.operator, condition.value);
    return { metricSource: condition.metricSource, value, threshold: condition.value, met };
  }

  async evaluateRatio(threshold: MultiMetricThreshold): Promise<MultiMetricResult> {
    const [numerator, denominator] = threshold.conditions;
    const [numVal, denVal] = await Promise.all([
      this.queryMetric(numerator.metricSource),
      this.queryMetric(denominator.metricSource),
    ]);
    const ratio = denVal > 0 ? numVal / denVal : 0;
    const met = this.evaluateSimpleCondition(ratio, numerator.operator, numerator.value);
    return { triggered: met, conditions: [{ ...numerator, value: numVal, met }], score: ratio };
  }

  async evaluateTrend(threshold: MultiMetricThreshold, history: number[]): Promise<MultiMetricResult> {
    const recentValues = this.getRecentWindow(history, 5); // last 5 values
    const trend = this.computeTrend(recentValues);
    const condition = threshold.conditions[0];
    const met = condition.operator === '>'
      ? trend > condition.value
      : Math.abs(trend) > condition.value;
    return { triggered: met, conditions: [{ ...condition, value: trend, met }], score: Math.abs(trend) };
  }

  private computeTrend(values: number[]): number {
    if (values.length < 2) return 0;
    const x = Array.from({ length: values.length }, (_, i) => i);
    const xMean = x.reduce((a, b) => a + b, 0) / x.length;
    const yMean = values.reduce((a, b) => a + b, 0) / values.length;
    const numerator = x.reduce((sum, xi, i) => sum + (xi - xMean) * (values[i] - yMean), 0);
    const denominator = x.reduce((sum, xi) => sum + Math.pow(xi - xMean, 2), 0);
    return denominator > 0 ? numerator / denominator : 0;
  }
}
```

## Integration Points

- **Threshold Configuration UI**: Multi-condition editor
- **Metric Queries**: Multiple metric sources queried independently
- **Alert Context**: Breach includes all sub-condition values

## Production Considerations

- **Query Performance**: Multiple metric queries increase evaluation latency
- **Coordinated Breaches**: AND thresholds may delay alerting on purpose
- **Complexity Management**: Limit number of sub-conditions per threshold
