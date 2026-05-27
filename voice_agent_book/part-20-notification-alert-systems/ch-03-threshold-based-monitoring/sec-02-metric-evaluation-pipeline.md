# Section 02: Metric Evaluation Pipeline

## Overview

The metric evaluation pipeline collects metrics at configured intervals, applies aggregation windows, and evaluates them against thresholds. The pipeline supports sliding windows (continuous evaluation) and tumbling windows (fixed intervals). Evaluation frequency adapts based on metric volatility.

## Architecture

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Collect   │   │ Aggregate│   │ Evaluate │   │ Check    │   │ Trigger  │
│           │   │          │   │          │   │          │   │          │
│ PromQL   │──▶│ Sliding  │──▶│ vs       │──▶│ Cooldown │──▶│ Alert    │
│ OTEL     │──▶│ Tumbling │   │ Threshold│   │ Dedup    │   │ Creation │
│ Custom   │──▶│ Windows  │   │          │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## Implementation Approach

```typescript
type WindowType = 'sliding' | 'tumbling';

interface WindowConfig {
  type: WindowType;
  size: number; // seconds
  slideInterval?: number; // for sliding windows
  evaluationInterval: number; // how often to evaluate
}

class MetricEvaluationPipeline {
  async startThreshold(threshold: Threshold): Promise<void> {
    const { evaluationInterval } = this.getWindowConfig(threshold);

    setInterval(async () => {
      const aggregated = await this.collectAndAggregate(threshold);
      const result = await this.evaluator.evaluate(threshold, aggregated);
      if (result.triggered) {
        await this.handleBreach(threshold, aggregated, result);
      }
    }, evaluationInterval * 1000);
  }

  private async collectAndAggregate(threshold: Threshold): Promise<AggregatedMetric> {
    const config = this.getWindowConfig(threshold);
    const rawMetrics = await this.collectRawMetrics(threshold, config);

    let aggregated: number;
    switch (threshold.metricSource.aggregation) {
      case 'avg':
        aggregated = rawMetrics.reduce((a, b) => a + b, 0) / rawMetrics.length;
        break;
      case 'sum':
        aggregated = rawMetrics.reduce((a, b) => a + b, 0);
        break;
      case 'max':
        aggregated = Math.max(...rawMetrics);
        break;
      case 'min':
        aggregated = Math.min(...rawMetrics);
        break;
      case 'p95':
        aggregated = this.percentile(rawMetrics, 95);
        break;
      case 'p99':
        aggregated = this.percentile(rawMetrics, 99);
        break;
      default:
        aggregated = rawMetrics[rawMetrics.length - 1];
    }

    return { value: aggregated, sampleCount: rawMetrics.length, window: config };
  }

  private async collectRawMetrics(threshold: Threshold, config: WindowConfig): Promise<number[]> {
    const now = Date.now() / 1000;
    const startTime = config.type === 'sliding'
      ? now - config.size
      : Math.floor(now / config.size) * config.size;

    return this.metricStore.query({
      source: threshold.metricSource.query,
      start: startTime,
      end: now,
    });
  }

  private getWindowConfig(threshold: Threshold): WindowConfig {
    return {
      type: 'sliding',
      size: threshold.evaluationWindow || 300,
      slideInterval: Math.min(threshold.evaluationWindow || 300, 60),
      evaluationInterval: Math.min(threshold.evaluationWindow || 300, 60),
    };
  }

  private percentile(values: number[], p: number): number {
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[index];
  }
}
```

## Integration Points

- **Metric Store**: Time-series database (Prometheus, TimescaleDB)
- **Threshold Evaluator**: Evaluates aggregated values
- **Alert Trigger**: Breach → alert creation

## Production Considerations

- **Evaluation Lag**: Account for metric collection delay
- **Window Alignment**: Tumbling windows align to clock boundaries
- **Performance**: Cache recent metric values to reduce query load
