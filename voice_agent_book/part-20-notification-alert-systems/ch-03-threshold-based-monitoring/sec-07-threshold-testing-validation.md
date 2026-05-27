# Section 07: Threshold Testing & Validation

## Overview

Threshold testing validates that thresholds will fire correctly before deployment. Simulation replays historical metric data through proposed thresholds to detect false positives and missed alerts. The testing framework helps tune thresholds to minimize alert fatigue.

## Implementation Approach

```typescript
interface ThresholdTest {
  threshold: Threshold;
  testWindow: TimeRange;
  results: ThresholdTestResult[];
  summary: TestSummary;
}

interface TestSummary {
  totalEvaluations: number;
  alertsWouldFire: number;
  estimatedFalsePositives: number;
  estimatedMissedAlerts: number;
  recommendation: 'accept' | 'tune' | 'reject';
}

class ThresholdTester {
  async simulate(threshold: Threshold, historyWindow: TimeRange): Promise<ThresholdTest> {
    const historicalMetrics = await this.getHistoricalData(threshold.metricSource, historyWindow);
    const results: ThresholdTestResult[] = [];

    for (const dataPoint of historicalMetrics) {
      const result = this.evaluator.evaluateCondition(dataPoint.value, threshold.conditions[0]);
      results.push({ timestamp: dataPoint.timestamp, value: dataPoint.value, triggered: result });
    }

    const summary = this.computeSummary(results, threshold);
    return { threshold, testWindow: historyWindow, results, summary };
  }

  private computeSummary(results: ThresholdTestResult[], threshold: Threshold): TestSummary {
    const triggeredCount = results.filter(r => r.triggered).length;
    const totalCount = results.length;

    // Estimate false positives by analyzing triggered periods
    const falsePositives = this.estimateFalsePositives(results, threshold);

    return {
      totalEvaluations: totalCount,
      alertsWouldFire: triggeredCount,
      estimatedFalsePositives: falsePositives,
      estimatedMissedAlerts: this.estimateMissedAlerts(results, threshold),
      recommendation: this.generateRecommendation(triggeredCount, totalCount, falsePositives),
    };
  }

  private estimateFalsePositives(results: ThresholdTestResult[], threshold: Threshold): number {
    // Consider a triggered alert a false positive if:
    // 1. Duration is less than threshold cooldown
    // 2. Value is just barely over threshold
    // 3. There's a known pattern (deploy, maintenance)
    return results.filter(r => {
      if (!r.triggered) return false;
      const margin = (r.value - threshold.conditions[0].value) / threshold.conditions[0].value;
      return margin < 0.05; // within 5% of threshold
    }).length;
  }

  private estimateMissedAlerts(results: ThresholdTestResult[], threshold: Threshold): number {
    // Check for sustained high values that didn't trigger due to conditions
    let missed = 0;
    let sustainedCount = 0;
    for (const r of results) {
      if (r.value > threshold.conditions[0].value * 0.9) {
        sustainedCount++;
        if (sustainedCount >= (threshold.conditions[0]?.sustainedFor || 1) && !r.triggered) {
          missed++;
        }
      } else {
        sustainedCount = 0;
      }
    }
    return missed;
  }

  private generateRecommendation(triggered: number, total: number, falsePositives: number): 'accept' | 'tune' | 'reject' {
    const alertRate = triggered / total;
    const fpRate = falsePositives / total;

    if (fpRate > 0.1) return 'reject'; // >10% false positive rate
    if (alertRate > 0.5 || fpRate > 0.05) return 'tune'; // >50% would alert or >5% false positive
    return 'accept';
  }

  async findOptimalThreshold(metricSource: MetricSource, historyWindow: TimeRange, targetAlertRate: number): Promise<number> {
    const data = await this.getHistoricalData(metricSource, historyWindow);
    const values = data.map(d => d.value).sort((a, b) => a - b);
    const percentileIndex = Math.floor((1 - targetAlertRate) * values.length);
    return values[percentileIndex];
  }
}
```

## Integration Points

- **Historical Data Store**: TimescaleDB or Prometheus for replay data
- **UI Integration**: Test thresholds from configuration interface
- **CI Pipeline**: Automated threshold testing in CI

## Production Considerations

- **Data Freshness**: Use recent data for relevant testing
- **False Positive Analysis**: Review triggered periods manually
- **Tuning Iterations**: Multiple test-tune cycles before deploying
