# Section 06: Adaptive Thresholding

## Overview

Adaptive thresholding dynamically adjusts anomaly detection thresholds based on recent metric behavior, user feedback, and alert volume. Instead of static thresholds that require manual tuning, adaptive thresholds learn from historical patterns and adjust to changes in metric distribution.

## Architecture

```
Adaptive Threshold Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Metric Stream] → [Threshold Engine] → [Adjusted Threshold] → [Anomaly Detection]
       │                  │                        │                  │
  Current values      Learning rate            New upper/lower     Fewer false
  Historical stats    Feedback loop            bounds based on     positives
  Alert outcomes      Convergence              recent window       Better recall
                      monitoring               + learning

Threshold Adjustment Process:
  Initial: Static baseline from historical data
           │
  Learning: Adjust per metric based on:
    ├── Recent metric distribution (last 7 days)
    ├── False positive rate (last 24 hours)
    ├── Current alert volume vs target
    └── Seasonal factors
           │
  Convergence: Threshold stabilizes after ~14 days
               │
  Monitor: Detect when threshold drifts too far
           and reset if needed

Visual:
  Thresholds over time:
  ┌─────────────────────────────────────────┐
  │  Value                                  │
  │  ╮          ╭──── upper (adaptive)      │
  │  │  ╱╲  ╱╲╱│                           │
  │  ╰──╯  ╰╯  ╰──── lower (adaptive)      │
  │  ═══════════════ baseline               │
  │                                         │
  └─────────────────────────────────────────┘
     Time →
```

## Design Decisions

- **Exponential Decay Learning**: Recent observations weighted more heavily
- **Feedback Incorporation**: User feedback directly adjusts future thresholds
- **Safety Bounds**: Thresholds clamped within min/max ranges to prevent runaway values
- **Convergence Detection**: Threshold marked as stable when variance drops below threshold

## Implementation Approach

```typescript
interface AdaptiveThresholdConfig {
  metric: string;
  learningRate: number; // 0.01 - 0.1
  windowSize: number; // data points for recent window
  minThreshold: number;
  maxThreshold: number;
  targetAlertRate: number; // alerts per day
  feedbackWeight: number; // 0.0 - 1.0
}

interface AdaptiveThreshold {
  metric: string;
  upper: number;
  lower: number;
  baseline: number;
  learningRate: number;
  stabilityScore: number; // 0.0 = unstable, 1.0 = converged
  lastUpdated: Date;
  iterations: number;
}

class AdaptiveThresholdEngine {
  private thresholds: Map<string, AdaptiveThreshold> = new Map();
  private recentValues: Map<string, number[]> = new Map();
  private alertCounts: Map<string, number> = new Map();
  private falsePositives: Map<string, number> = new Map();

  async initialize(config: AdaptiveThresholdConfig): Promise<void> {
    const historicalData = await this.fetchHistoricalData(config.metric, 30);
    const sorted = [...historicalData].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const mad = sorted.map(v => Math.abs(v - median)).sort((a, b) => a - b)[Math.floor(sorted.length / 2)];

    this.thresholds.set(config.metric, {
      metric: config.metric,
      upper: median + 3 * mad,
      lower: Math.max(config.minThreshold, median - 3 * mad),
      baseline: median,
      learningRate: config.learningRate,
      stabilityScore: 0.3,
      lastUpdated: new Date(),
      iterations: 0,
    });

    this.recentValues.set(config.metric, historicalData.slice(-config.windowSize));
    this.alertCounts.set(config.metric, 0);
    this.falsePositives.set(config.metric, 0);
  }

  async adapt(config: AdaptiveThresholdConfig): Promise<AdaptiveThreshold> {
    const current = this.thresholds.get(config.metric);
    if (!current) throw new Error(`No threshold for ${config.metric}`);

    const recentValues = this.recentValues.get(config.metric) || [];
    if (recentValues.length < 10) return current;

    // Compute recent distribution
    const recentMean = recentValues.reduce((s, v) => s + v, 0) / recentValues.length;
    const recentStd = Math.sqrt(
      recentValues.reduce((s, v) => s + (v - recentMean) ** 2, 0) / recentValues.length
    );

    // Compute desired threshold based on recent distribution
    const desiredUpper = recentMean + 3 * recentStd;
    const desiredLower = Math.max(config.minThreshold, recentMean - 3 * recentStd);

    // Apply learning rate (exponential smoothing)
    const lr = this.computeEffectiveLearningRate(config);
    const newUpper = current.upper + lr * (desiredUpper - current.upper);
    const newLower = current.lower + lr * (desiredLower - current.lower);

    // Apply feedback adjustment
    const feedbackAdjustment = this.computeFeedbackAdjustment(config);
    const adjustedUpper = newUpper * (1 + feedbackAdjustment);
    const adjustedLower = newLower * (1 - feedbackAdjustment);

    // Clamp to safety bounds
    const clampedUpper = Math.min(config.maxThreshold, Math.max(config.minThreshold, adjustedUpper));
    const clampedLower = Math.min(clampedUpper, Math.max(config.minThreshold, adjustedLower));

    // Compute stability
    const prevUpper = current.upper;
    const stabilityScore = Math.min(1, current.stabilityScore + 0.05 * (1 - Math.abs(clampedUpper - prevUpper) / prevUpper));

    const updated: AdaptiveThreshold = {
      ...current,
      upper: clampedUpper,
      lower: clampedLower,
      baseline: recentMean,
      learningRate: lr,
      stabilityScore,
      lastUpdated: new Date(),
      iterations: current.iterations + 1,
    };

    this.thresholds.set(config.metric, updated);
    return updated;
  }

  private computeEffectiveLearningRate(config: AdaptiveThresholdConfig): number {
    // Reduce learning rate as threshold stabilizes
    const current = this.thresholds.get(config.metric);
    if (!current) return config.learningRate;

    // Increase learning rate if too many false positives
    const fpRate = (this.falsePositives.get(config.metric) || 0) / Math.max(1, this.alertCounts.get(config.metric) || 1);
    const fpMultiplier = fpRate > 0.3 ? 1.5 : 1.0;

    // Decrease learning rate as stability increases
    const stabilityFactor = 1 - current.stabilityScore * 0.5;

    return config.learningRate * fpMultiplier * stabilityFactor;
  }

  private computeFeedbackAdjustment(config: AdaptiveThresholdConfig): number {
    const alertCount = this.alertCounts.get(config.metric) || 0;
    const fpCount = this.falsePositives.get(config.metric) || 0;

    if (alertCount === 0) return 0;

    // If high false positive rate, widen thresholds
    const fpRate = fpCount / alertCount;
    const targetFpRate = 0.1; // target 10% false positive rate

    return (targetFpRate - fpRate) * config.feedbackWeight;
  }

  recordValue(metric: string, value: number): void {
    const values = this.recentValues.get(metric) || [];
    values.push(value);
    const config = this.getConfig(metric);
    if (config && values.length > config.windowSize) {
      values.splice(0, values.length - config.windowSize);
    }
    this.recentValues.set(metric, values);
  }

  recordAlert(metric: string): void {
    this.alertCounts.set(metric, (this.alertCounts.get(metric) || 0) + 1);
  }

  recordFalsePositive(metric: string): void {
    this.falsePositives.set(metric, (this.falsePositives.get(metric) || 0) + 1);
  }
}
```

## Integration Points

- **Metrics Pipeline**: Real-time metric values feed threshold adaptation
- **Alert Feedback**: User false positive reports trigger threshold adjustment
- **Dashboard**: Visualize threshold changes over time for monitoring

## Production Considerations

- **Learning Rate Limits**: Cap learning rate to prevent threshold oscillation
- **Convergence Reset**: Reset threshold if stability degrades after convergence
- **A/B Threshold Testing**: Test different learning rates on shadow metrics
- **Threshold Alerts**: Alert operators if threshold drifts beyond 50% of initial value

## Open-Source Tools

- **Lodash**: Utility for window management and statistical computations
- **BullMQ**: Periodic job queue for threshold recalculation
