# Section 07: Multi-Dimensional Anomaly Detection

## Overview

Multi-dimensional anomaly detection analyzes correlations across multiple metrics simultaneously to identify complex failure patterns. A single metric anomaly may be benign, but anomalies across correlated metrics indicate genuine incidents. Cross-metric correlation and root cause hint generation reduce mean time to resolution.

## Architecture

```
Multi-Dimensional Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Metric A] ─────┐
[Metric B] ─────┤
[Metric C] ─────┤
[Metric D] ─────┘
       │
  [Correlation Engine]
       │
  ├── Pairwise correlation matrix
  ├── Anomaly vector (all metrics)
  ├── Correlation deviation score
  └── Root cause hints
       │
  [Anomaly Decision]
  ├── Isolated anomaly → low priority
  ├── Correlated anomaly cluster → high priority
  └── Known pattern match → automated response

Dimension Types:
  - System: CPU, memory, disk, network
  - Application: latency, error rate, throughput
  - Business: call volume, conversion rate, user count
  - Voice: STT accuracy, TTS latency, NLU confidence

Example Correlation Matrix:
           CPU  Mem  Lat  Err  Vol
  CPU      1.0  0.8  0.6  0.5 -0.2
  Mem      0.8  1.0  0.4  0.3 -0.1
  Latency  0.6  0.4  1.0  0.9 -0.5
  Error    0.5  0.3  0.9  1.0 -0.4
  Volume  -0.2 -0.1 -0.5 -0.4  1.0
```

## Design Decisions

- **Correlation Matrix**: Pearson correlation across all metric pairs
- **Correlation Deviation**: Detect when expected correlations break
- **Root Cause Hints**: Highest-deviation metric flagged as primary suspect
- **Known Pattern Library**: Pre-defined multi-metric failure signatures

## Implementation Approach

```typescript
interface MultiDimensionalConfig {
  metrics: string[];
  correlationWindowSize: number; // data points
  correlationThreshold: number; // minimum |r| for meaningful correlation
  deviationThreshold: number; // how much correlation can deviate
  patternLibrary: FailurePattern[];
}

interface FailurePattern {
  name: string;
  description: string;
  signature: Array<{ metric: string; direction: 'up' | 'down'; magnitude: number }>;
}

interface CorrelationResult {
  matrix: Record<string, Record<string, number>>;
  anomalies: MetricAnomaly[];
  clusterScore: number; // 0-1 how well anomalies cluster
  rootCauseHints: string[];
  matchedPattern?: FailurePattern;
}

interface MetricAnomaly {
  metric: string;
  zscore: number;
  isAnomalous: boolean;
  correlatedMetrics: string[];
}

class MultiDimensionalDetector {
  private history: Map<string, number[]> = new Map();
  private baselineMatrix: Record<string, Record<string, number>> = {};

  async trainBaseline(config: MultiDimensionalConfig): Promise<void> {
    const historicalData = await this.fetchMultiMetricHistory(config.metrics, 30);
    this.baselineMatrix = this.computeCorrelationMatrix(historicalData, config.metrics);
  }

  async detect(
    currentValues: Record<string, number>,
    config: MultiDimensionalConfig
  ): Promise<CorrelationResult> {
    // Store current values
    for (const [metric, value] of Object.entries(currentValues)) {
      const history = this.history.get(metric) || [];
      history.push(value);
      if (history.length > config.correlationWindowSize) {
        history.shift();
      }
      this.history.set(metric, history);
    }

    // Detect anomalies per metric
    const anomalies: MetricAnomaly[] = [];
    for (const metric of config.metrics) {
      const history = this.history.get(metric) || [];
      if (history.length < 10) continue;

      const mean = history.reduce((s, v) => s + v, 0) / history.length;
      const std = Math.sqrt(history.reduce((s, v) => s + (v - mean) ** 2, 0) / history.length);
      const zscore = std > 0 ? (currentValues[metric] - mean) / std : 0;

      if (Math.abs(zscore) > 2) {
        anomalies.push({
          metric,
          zscore,
          isAnomalous: true,
          correlatedMetrics: [],
        });
      }
    }

    if (anomalies.length === 0) {
      return { matrix: {}, anomalies: [], clusterScore: 0, rootCauseHints: [] };
    }

    // Compute current correlation matrix
    const currentMatrix = this.computeCorrelationMatrixFromHistory(config.metrics);

    // Find correlations among anomalous metrics
    for (const anomaly of anomalies) {
      for (const other of anomalies) {
        if (anomaly.metric === other.metric) continue;
        const correlation = currentMatrix[anomaly.metric]?.[other.metric] || 0;
        if (Math.abs(correlation) > config.correlationThreshold) {
          anomaly.correlatedMetrics.push(other.metric);
        }
      }
    }

    // Compute cluster score
    const clusteredAnomalies = anomalies.filter(a => a.correlatedMetrics.length > 0);
    const clusterScore = anomalies.length > 0
      ? clusteredAnomalies.length / anomalies.length
      : 0;

    // Detect correlation deviation (baseline vs current)
    const rootCauseHints = this.identifyRootCause(anomalies, currentMatrix, config);

    // Match against known patterns
    const matchedPattern = this.matchPattern(anomalies, config.patternLibrary);

    return {
      matrix: currentMatrix,
      anomalies,
      clusterScore,
      rootCauseHints,
      matchedPattern,
    };
  }

  private computeCorrelationMatrixFromHistory(
    metrics: string[]
  ): Record<string, Record<string, number>> {
    const matrix: Record<string, Record<string, number>> = {};

    for (const m1 of metrics) {
      matrix[m1] = {};
      const h1 = this.history.get(m1) || [];
      if (h1.length < 10) continue;

      for (const m2 of metrics) {
        if (m1 === m2) { matrix[m1][m2] = 1.0; continue; }
        const h2 = this.history.get(m2) || [];
        if (h2.length < 10) continue;

        const n = Math.min(h1.length, h2.length);
        const mean1 = h1.slice(0, n).reduce((s, v) => s + v, 0) / n;
        const mean2 = h2.slice(0, n).reduce((s, v) => s + v, 0) / n;

        let numerator = 0, d1 = 0, d2 = 0;
        for (let i = 0; i < n; i++) {
          const diff1 = h1[i] - mean1;
          const diff2 = h2[i] - mean2;
          numerator += diff1 * diff2;
          d1 += diff1 ** 2;
          d2 += diff2 ** 2;
        }

        matrix[m1][m2] = (d1 > 0 && d2 > 0) ? numerator / Math.sqrt(d1 * d2) : 0;
      }
    }

    return matrix;
  }

  private identifyRootCause(
    anomalies: MetricAnomaly[],
    matrix: Record<string, Record<string, number>>,
    config: MultiDimensionalConfig
  ): string[] {
    // Root cause is the metric with highest z-score that is correlated with most others
    return anomalies
      .sort((a, b) => b.correlatedMetrics.length - a.correlatedMetrics.length || Math.abs(b.zscore) - Math.abs(a.zscore))
      .slice(0, 3)
      .map(a => `${a.metric} (z=${a.zscore.toFixed(2)}, correlated with ${a.correlatedMetrics.length} metrics)`);
  }

  private matchPattern(
    anomalies: MetricAnomaly[],
    patternLibrary: FailurePattern[]
  ): FailurePattern | undefined {
    const anomalySignatures = anomalies.map(a => ({
      metric: a.metric,
      direction: a.zscore > 0 ? 'up' as const : 'down' as const,
      magnitude: Math.abs(a.zscore),
    }));

    for (const pattern of patternLibrary) {
      const matches = pattern.signature.filter(sig =>
        anomalySignatures.some(a =>
          a.metric === sig.metric && a.direction === sig.direction && a.magnitude >= sig.magnitude
        )
      );

      if (matches.length / pattern.signature.length >= 0.6) {
        return pattern;
      }
    }

    return undefined;
  }
}
```

## Integration Points

- **Metrics Pipeline**: Multi-metric snapshots from monitoring
- **Root Cause Engine**: Hints passed to incident management
- **Runbook Automation**: Pattern-matched incidents trigger automated responses

## Production Considerations

- **Dimensionality Limits**: Maximum 20 correlated metrics per analysis
- **Computation Cost**: Correlation matrix O(n²) — cache results for 5 minutes
- **Baseline Drift**: Recompute baseline correlation matrix weekly
- **Pattern Library**: Curated from historical incident post-mortems

## Open-Source Tools

- **simple-statistics**: Correlation coefficient computation
- **Lodash**: Data windowing and statistical helpers
