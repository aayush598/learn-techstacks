# Section 01: Statistical Anomaly Detection

## Overview

Statistical anomaly detection identifies unusual patterns in metrics using techniques like Z-score analysis, moving averages, and standard deviation thresholds. These methods establish normal behavior baselines and flag significant deviations without requiring machine learning models.

## Architecture

```
Statistical Detection Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Metrics Stream] → [Sliding Window] → [Statistical Calculator] → [Anomaly Score]
      │                   │                       │                     │
  Time-series         Configurable           Compute mean,        Compare current
  data points         window size            stddev, Z-score      against threshold
  (per metric)        (10 min/1 hr)                               and emit alert

Detection Methods:
  ┌─────────────────────┬──────────────────┬──────────────────────┐
  │ Method              │ Use Case          │ Threshold            │
  ├─────────────────────┼──────────────────┼──────────────────────┤
  │ Z-Score             │ Call volume       │ |Z| > 3              │
  │                     │ Error rates       │                      │
  ├─────────────────────┼──────────────────┼──────────────────────┤
  │ Moving Average      │ Latency spikes    │ Deviation > 2σ      │
  │                     │ Resource usage    │ from moving avg      │
  ├─────────────────────┼──────────────────┼──────────────────────┤
  │ IQR (Interquartile) │ Outlier detection │ Below Q1 - 1.5*IQR  │
  │                     │ in distributions  │ Above Q3 + 1.5*IQR  │
  ├─────────────────────┼──────────────────┼──────────────────────┤
  │ CUSUM              │ Small persistent  │ Cumulative sum       │
  │                     │ shifts in mean    │ exceeds threshold    │
  └─────────────────────┴──────────────────┴──────────────────────┘
```

## Design Decisions

- **Window-Based Analysis**: Sliding window for adaptive baselines
- **Configurable Thresholds**: Per-metric threshold configuration
- **Multiple Methods**: Support different methods for different metric types

## Implementation Approach

```typescript
interface AnomalyDetectionConfig {
  metric: string;
  method: 'zscore' | 'moving_average' | 'iqr' | 'cusum';
  windowSize: number; // data points
  threshold: number;
  minDataPoints: number;
}

interface AnomalyScore {
  metric: string;
  timestamp: Date;
  value: number;
  baseline: number;
  deviation: number;
  threshold: number;
  isAnomaly: boolean;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

class StatisticalDetector {
  private windows: Map<string, number[]> = new Map();
  private configs: Map<string, AnomalyDetectionConfig> = new Map();

  setConfig(config: AnomalyDetectionConfig): void {
    this.configs.set(config.metric, config);
    this.windows.set(config.metric, []);
  }

  async evaluate(metric: string, value: number): Promise<AnomalyScore | null> {
    const config = this.configs.get(metric);
    if (!config) return null;

    let window = this.windows.get(metric) || [];
    window.push(value);
    if (window.length > config.windowSize) {
      window = window.slice(-config.windowSize);
    }
    this.windows.set(metric, window);

    if (window.length < config.minDataPoints) return null;

    let score: AnomalyScore;

    switch (config.method) {
      case 'zscore':
        score = this.zscoreAnalysis(metric, value, window, config);
        break;
      case 'moving_average':
        score = this.movingAverageAnalysis(metric, value, window, config);
        break;
      case 'iqr':
        score = this.iqrAnalysis(metric, value, window, config);
        break;
      case 'cusum':
        score = this.cusumAnalysis(metric, value, window, config);
        break;
    }

    return score;
  }

  private zscoreAnalysis(
    metric: string, value: number, window: number[], config: AnomalyDetectionConfig
  ): AnomalyScore {
    const mean = window.reduce((s, v) => s + v, 0) / window.length;
    const variance = window.reduce((s, v) => s + (v - mean) ** 2, 0) / window.length;
    const stddev = Math.sqrt(variance);
    const zscore = stddev > 0 ? (value - mean) / stddev : 0;

    return {
      metric, timestamp: new Date(), value, baseline: mean,
      deviation: Math.abs(zscore), threshold: config.threshold,
      isAnomaly: Math.abs(zscore) > config.threshold,
      severity: this.calculateSeverity(Math.abs(zscore)),
    };
  }

  private movingAverageAnalysis(
    metric: string, value: number, window: number[], config: AnomalyDetectionConfig
  ): AnomalyScore {
    const ma = window.slice(-Math.min(10, window.length)).reduce((s, v) => s + v, 0) / Math.min(10, window.length);
    const deviation = ma > 0 ? Math.abs(value - ma) / ma : 0;

    return {
      metric, timestamp: new Date(), value, baseline: ma,
      deviation, threshold: config.threshold,
      isAnomaly: deviation > config.threshold,
      severity: this.calculateSeverity(deviation / config.threshold),
    };
  }

  private calculateSeverity(normalizedDeviation: number): 'low' | 'medium' | 'high' | 'critical' {
    if (normalizedDeviation >= 5) return 'critical';
    if (normalizedDeviation >= 3) return 'high';
    if (normalizedDeviation >= 2) return 'medium';
    return 'low';
  }
}
```

## Integration Points

- **Metrics Pipeline**: Receives time-series data from monitoring
- **Alert Engine**: Fires alerts when anomalies detected
- **Dashboard**: Visualizes anomaly scores and baselines

## Production Considerations

- **Cold Start**: Min data points required before detection begins
- **Data Resolution**: 1-minute data points for real-time detection
- **Method Selection**: Different methods for different metric characteristics

## Open-Source Tools

- **simple-statistics**: JavaScript statistical functions
- **Lodash**: Utility functions for data windowing
