# Section 02: Baseline Comparison

## Overview

Baseline comparison compares current metric values against computed baselines to detect significant deviations. Baselines are computed from historical data using various strategies — fixed, dynamic, seasonal, and trend-adjusted — to accommodate different metric behaviors and patterns.

## Architecture

```
Baseline Computation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Historical Metrics] → [Baseline Calculator] → [Baseline Store] → [Comparison Engine]
         │                       │                     │                  │
   30-90 days of           Configured            Redis cache        Current value
   metric data             strategy              + DB snapshot       vs baseline
                                                  (persistent)       → deviation %

Baseline Strategies:
  Fixed:      Static threshold (e.g., max 1000 calls/hr)
  ──── metric
  Dynamic:    Rolling 7-day median
  /\/\/ metric
  Seasonal:   Same time, same day-of-week for 4 weeks
  ~ ~ ~ metric
  Trend:      Linear regression projection
  /   metric (upward trend)

When to Use Which:
  ┌─────────────┬────────────────────────────────────┐
  │ Strategy    │ Best For                            │
  ├─────────────┼────────────────────────────────────┤
  │ Fixed       │ Hard limits (rate limits, quotas)   │
  │ Dynamic     │ Gradual behavior changes            │
  │ Seasonal    │ Business-hour patterns              │
  │ Trend       │ Growing/declining metrics            │
  └─────────────┴────────────────────────────────────┘
```

## Design Decisions

- **Multi-Strategy Support**: Different metrics use different baseline strategies
- **Automatic Strategy Selection**: Recommend strategy based on metric characteristics
- **Baseline Drift Detection**: Alert when baseline itself changes significantly
- **Caching**: Baselines cached for performance, recomputed on schedule

## Implementation Approach

```typescript
type BaselineStrategy = 'fixed' | 'dynamic' | 'seasonal' | 'trend';

interface BaselineConfig {
  metric: string;
  strategy: BaselineStrategy;
  fixedValue?: number;
  windowDays?: number;
  seasonalPeriodDays?: number;
  minDataPoints: number;
  deviationThreshold: number; // percentage
}

interface Baseline {
  metric: string;
  value: number;
  upperBound: number;
  lowerBound: number;
  strategy: BaselineStrategy;
  computedAt: Date;
  confidenceInterval: number; // e.g., 0.95 for 95%
  dataPointsUsed: number;
}

class BaselineService {
  private baselineStore: Map<string, Baseline> = new Map();

  async computeBaseline(config: BaselineConfig): Promise<Baseline> {
    const historicalData = await this.fetchHistoricalData(config.metric, config.windowDays || 30);

    let baseline: Baseline;

    switch (config.strategy) {
      case 'fixed':
        baseline = this.computeFixed(config);
        break;
      case 'dynamic':
        baseline = this.computeDynamic(historicalData, config);
        break;
      case 'seasonal':
        baseline = this.computeSeasonal(historicalData, config);
        break;
      case 'trend':
        baseline = this.computeTrend(historicalData, config);
        break;
    }

    this.baselineStore.set(config.metric, baseline);
    return baseline;
  }

  private computeDynamic(data: number[], config: BaselineConfig): Baseline {
    const sorted = [...data].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const deviations = data.map(v => Math.abs(v - median));
    const mad = deviations.sort((a, b) => a - b)[Math.floor(deviations.length / 2)];
    const upper = median + 3 * mad;
    const lower = Math.max(0, median - 3 * mad);

    return {
      metric: config.metric, value: median,
      upperBound: upper, lowerBound: lower,
      strategy: 'dynamic', computedAt: new Date(),
      confidenceInterval: 0.95, dataPointsUsed: data.length,
    };
  }

  private computeSeasonal(data: number[], config: BaselineConfig): Baseline {
    // Group by day-of-week + hour and compute median per slot
    const period = config.seasonalPeriodDays || 7;
    const slotSize = data.length / period;
    const slots: number[][] = Array.from({ length: period }, () => []);

    data.forEach((val, i) => {
      slots[i % period].push(val);
    });

    const slotMedians = slots.map(slot => {
      const sorted = [...slot].sort((a, b) => a - b);
      return sorted[Math.floor(sorted.length / 2)];
    });

    const overallMedian = slotMedians.reduce((s, v) => s + v, 0) / slotMedians.length;
    const maxDeviation = Math.max(...slotMedians.map(v => Math.abs(v - overallMedian)));

    return {
      metric: config.metric, value: overallMedian,
      upperBound: overallMedian + maxDeviation * 1.5,
      lowerBound: Math.max(0, overallMedian - maxDeviation * 1.5),
      strategy: 'seasonal', computedAt: new Date(),
      confidenceInterval: 0.9, dataPointsUsed: data.length,
    };
  }

  private computeTrend(data: number[], config: BaselineConfig): Baseline {
    const n = data.length;
    const xMean = (n - 1) / 2;
    const yMean = data.reduce((s, v) => s + v, 0) / n;

    let numerator = 0;
    let denominator = 0;
    for (let i = 0; i < n; i++) {
      numerator += (i - xMean) * (data[i] - yMean);
      denominator += (i - xMean) ** 2;
    }

    const slope = denominator > 0 ? numerator / denominator : 0;
    const intercept = yMean - slope * xMean;
    const projectedValue = intercept + slope * n;

    // Compute residuals for confidence bands
    const residuals = data.map((v, i) => Math.abs(v - (intercept + slope * i)));
    const mad = residuals.sort((a, b) => a - b)[Math.floor(residuals.length / 2)];

    return {
      metric: config.metric, value: projectedValue,
      upperBound: projectedValue + 3 * mad,
      lowerBound: Math.max(0, projectedValue - 3 * mad),
      strategy: 'trend', computedAt: new Date(),
      confidenceInterval: 0.9, dataPointsUsed: data.length,
    };
  }

  async compare(baseline: Baseline, currentValue: number): Promise<ComparisonResult> {
    const deviation = baseline.value > 0
      ? ((currentValue - baseline.value) / baseline.value) * 100
      : currentValue > 0 ? 100 : 0;

    const isAboveUpper = currentValue > baseline.upperBound;
    const isBelowLower = currentValue < baseline.lowerBound;

    return {
      metric: baseline.metric,
      currentValue,
      baselineValue: baseline.value,
      deviationPercent: deviation,
      isAnomaly: isAboveUpper || isBelowLower,
      direction: isAboveUpper ? 'high' : isBelowLower ? 'low' : 'normal',
      upperBound: baseline.upperBound,
      lowerBound: baseline.lowerBound,
    };
  }

  async detectBaselineDrift(metric: string): Promise<boolean> {
    const historical = await this.fetchHistoricalData(metric, 90);
    const recent = historical.slice(-Math.min(30, historical.length));
    const older = historical.slice(0, Math.min(30, historical.length));

    if (recent.length < 10 || older.length < 10) return false;

    const recentMean = recent.reduce((s, v) => s + v, 0) / recent.length;
    const olderMean = older.reduce((s, v) => s + v, 0) / older.length;
    const driftPercent = olderMean > 0
      ? Math.abs(recentMean - olderMean) / olderMean * 100
      : 100;

    return driftPercent > 20; // 20% drift threshold
  }
}
```

## Integration Points

- **Metrics Store**: Historical data from time-series database
- **Anomaly Detection Pipeline**: Baselines used as input for detection
- **Dashboard**: Baseline visualization with confidence bands

## Production Considerations

- **Recalculation Schedule**: Baselines recomputed daily or on demand
- **Data Sufficiency**: Minimum 2 weeks of data before seasonal baseline
- **Baseline Versioning**: Track baseline changes for audit trail

## Open-Source Tools

- **simple-statistics**: Statistical functions for baseline computation
- **Redis**: Caching for frequently accessed baselines
