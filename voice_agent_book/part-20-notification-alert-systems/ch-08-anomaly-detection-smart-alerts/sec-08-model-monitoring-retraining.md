# Section 08: Model Monitoring & Retraining

## Overview

ML models for anomaly detection require continuous monitoring to maintain accuracy. Model performance tracking detects drift in data distributions and prediction quality. An automated retraining pipeline refreshes models on new labeled data, and A/B testing validates new models before deployment.

## Architecture

```
Model Lifecycle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Training Pipeline] → [Model Registry] → [Deployment] → [Monitoring]
         │                    │                 │              │
  Historical labeled      Model version       Production     Track metrics:
  data + new feedback     with metadata       inference      - Prediction drift
  Automated feature       staging/prod        endpoint       - Feature drift
  engineering             tags                               - Accuracy vs feedback
                                                             - Latency
                                                                  │
                                                             [Retrain Trigger]
                                                              ├── Drift detected
                                                              ├── Accuracy drop
                                                              └── New data available

Monitoring Dashboard:
  ┌──────────────────────────────────────────────────────────┐
  │ Model: isolation-forest-v3                                │
  │ Status: ● Healthy                                         │
  │                                                           │
  │ Anomaly Rate:  2.3%  (▼ 0.1% from baseline)              │
  │ False Positive: 8.1%  (▲ 2.3% — above threshold!)        │
  │ Feature Drift:  3/8 features drifted                      │
  │ Prediction Drift: 0.12 (KS test, p < 0.05)               │
  │ Inference Latency: 23ms (p99: 45ms)                      │
  │                                                           │
  │ [Retrain Now] [Rollback to v2] [A/B Test v4]             │
  └──────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Drift Detection**: KS test for feature drift, PSI for prediction drift
- **Automated Retraining**: Scheduled weekly retraining with new feedback data
- **A/B Testing**: Shadow deployment of new model alongside production
- **Rollback Capability**: Previous model version kept for 30 days

## Implementation Approach

```typescript
interface ModelMonitorConfig {
  modelId: string;
  inputFeatures: string[];
  driftThresholds: {
    featureDrift: number; // KS test p-value threshold
    predictionDrift: number; // PSI threshold
    accuracyDrop: number; // percentage drop
    falsePositiveRate: number; // maximum acceptable rate
  };
  retrainingSchedule: string; // cron expression
  abTestConfig?: {
    trafficPercentage: number; // 0-100
    durationDays: number;
  };
}

interface ModelHealthReport {
  modelId: string;
  version: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  metrics: {
    anomalyRate: number;
    falsePositiveRate: number;
    accuracy: number;
    precision: number;
    recall: number;
    inferenceLatencyMs: number;
  };
  drift: {
    featureDrift: Array<{ feature: string; ksStatistic: number; pValue: number; drifted: boolean }>;
    predictionDrift: number;
    predictionDriftExceeded: boolean;
  };
  dataFreshness: {
    lastTrainingDate: Date;
    newFeedbackCount: number;
    daysSinceTraining: number;
  };
}

class ModelMonitor {
  private feedbackStore: FeedbackStore;
  private featureStore: FeatureStore;

  async assessHealth(config: ModelMonitorConfig): Promise<ModelHealthReport> {
    const [featureDrift, predictionDrift, feedbackMetrics] = await Promise.all([
      this.detectFeatureDrift(config),
      this.detectPredictionDrift(config),
      this.computeFeedbackMetrics(config),
    ]);

    const driftExceeded = featureDrift.some(f => f.drifted)
      || predictionDrift.predictionDriftExceeded;
    const accuracyDegraded = feedbackMetrics.accuracy < 1 - config.driftThresholds.accuracyDrop / 100;
    const fpDegraded = feedbackMetrics.falsePositiveRate > config.driftThresholds.falsePositiveRate / 100;

    let status: 'healthy' | 'degraded' | 'unhealthy';
    if (driftExceeded || accuracyDegraded || fpDegraded) {
      status = 'degraded';
    }
    if (driftExceeded && accuracyDegraded) {
      status = 'unhealthy';
    } else {
      status = 'healthy';
    }

    const recentFeedback = await this.feedbackStore.getRecentFeedback(config.modelId, 7);
    const modelMeta = await this.getModelMetadata(config.modelId);

    return {
      modelId: config.modelId,
      version: modelMeta.version,
      status,
      metrics: {
        ...feedbackMetrics,
        inferenceLatencyMs: modelMeta.inferenceLatencyMs,
      },
      drift: {
        featureDrift,
        predictionDrift: predictionDrift.psi,
        predictionDriftExceeded: predictionDrift.predictionDriftExceeded,
      },
      dataFreshness: {
        lastTrainingDate: modelMeta.lastTrainingDate,
        newFeedbackCount: recentFeedback.length,
        daysSinceTraining: Math.floor((Date.now() - modelMeta.lastTrainingDate.getTime()) / 86400000),
      },
    };
  }

  private async detectFeatureDrift(
    config: ModelMonitorConfig
  ): Promise<Array<{ feature: string; ksStatistic: number; pValue: number; drifted: boolean }>> {
    const referenceData = await this.featureStore.getTrainingFeatures(config.modelId);
    const currentData = await this.featureStore.getRecentFeatures(config.modelId, 1000);

    return config.inputFeatures.map(feature => {
      const refValues = referenceData.map(r => r[feature]).filter(v => v !== undefined) as number[];
      const currValues = currentData.map(r => r[feature]).filter(v => v !== undefined) as number[];

      if (refValues.length < 50 || currValues.length < 50) {
        return { feature, ksStatistic: 0, pValue: 1, drifted: false };
      }

      // Kolmogorov-Smirnov test
      const ks = this.ksTest(refValues, currValues);
      const drifted = ks.pValue < config.driftThresholds.featureDrift;

      return { feature, ksStatistic: ks.statistic, pValue: ks.pValue, drifted };
    });
  }

  private ksTest(a: number[], b: number[]): { statistic: number; pValue: number } {
    const allValues = [...new Set([...a, ...b])].sort((x, y) => x - y);
    let maxDiff = 0;

    for (const v of allValues) {
      const ecdfA = a.filter(x => x <= v).length / a.length;
      const ecdfB = b.filter(x => x <= v).length / b.length;
      maxDiff = Math.max(maxDiff, Math.abs(ecdfA - ecdfB));
    }

    const n = a.length * b.length / (a.length + b.length);
    const pValue = Math.exp(-2 * n * maxDiff * maxDiff);

    return { statistic: maxDiff, pValue };
  }

  private async detectPredictionDrift(
    config: ModelMonitorConfig
  ): Promise<{ psi: number; predictionDriftExceeded: boolean }> {
    const referenceScores = await this.featureStore.getTrainingScores(config.modelId);
    const currentScores = await this.featureStore.getRecentScores(config.modelId, 1000);

    if (referenceScores.length < 100 || currentScores.length < 100) {
      return { psi: 0, predictionDriftExceeded: false };
    }

    // Population Stability Index
    const bins = 10;
    const binSize = 1 / bins;
    let psi = 0;

    for (let i = 0; i < bins; i++) {
      const lower = i * binSize;
      const upper = (i + 1) * binSize;

      const refPct = referenceScores.filter(s => s >= lower && s < upper).length / referenceScores.length;
      const currPct = currentScores.filter(s => s >= lower && s < upper).length / currentScores.length;

      const actualRefPct = Math.max(refPct, 0.001);
      const actualCurrPct = Math.max(currPct, 0.001);

      psi += (actualCurrPct - actualRefPct) * Math.log(actualCurrPct / actualRefPct);
    }

    return {
      psi,
      predictionDriftExceeded: psi > 0.2, // PSI > 0.2 indicates significant drift
    };
  }

  private async computeFeedbackMetrics(config: ModelMonitorConfig) {
    const feedback = await this.feedbackStore.getRecentFeedback(config.modelId, 7);
    const total = feedback.length;
    if (total === 0) {
      return { anomalyRate: 0, falsePositiveRate: 0, accuracy: 1, precision: 1, recall: 1 };
    }

    const truePositives = feedback.filter(f => f.isAnomaly && !f.isFalsePositive).length;
    const falsePositives = feedback.filter(f => f.isAnomaly && f.isFalsePositive).length;
    const falseNegatives = feedback.filter(f => !f.isAnomaly && !f.wasDetected).length;
    const trueNegatives = feedback.filter(f => !f.isAnomaly && f.wasDetected).length;

    return {
      anomalyRate: feedback.filter(f => f.isAnomaly).length / total,
      falsePositiveRate: total > 0 ? falsePositives / total : 0,
      accuracy: total > 0 ? (truePositives + trueNegatives) / total : 1,
      precision: (truePositives + falsePositives) > 0 ? truePositives / (truePositives + falsePositives) : 1,
      recall: (truePositives + falseNegatives) > 0 ? truePositives / (truePositives + falseNegatives) : 1,
    };
  }

  async triggerRetraining(modelId: string): Promise<void> {
    const newData = await this.feedbackStore.getAllLabeledFeedback(modelId);
    const trainingJob = {
      modelId,
      trainingDataSize: newData.length,
      features: await this.featureStore.getFeatureNames(modelId),
      hyperparameters: await this.getCurrentHyperparameters(modelId),
      triggerReason: 'scheduled',
    };

    await this.submitTrainingJob(trainingJob);
  }
}
```

## Integration Points

- **Model Registry**: MLflow-compatible model version management
- **Training Pipeline**: Automated retraining on feedback data
- **Deployment Service**: Canary deployment for A/B testing
- **Alert System**: Model degradation triggers operator notification

## Production Considerations

- **Computation Budget**: Drift detection runs hourly; retraining weekly
- **Data Retention**: Training data retained for model reproducibility
- **A/B Test Duration**: Minimum 7 days for statistical significance
- **Rollback Automation**: Automatic rollback if new model degrades performance

## Open-Source Tools

- **MLflow**: Model registry and experiment tracking
- **scikit-learn**: KS test and statistical utilities
- **Evidently AI**: Model monitoring and drift detection
