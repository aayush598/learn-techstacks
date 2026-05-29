# Section 04: ML-Based Detection

## Overview

Machine learning anomaly detection complements statistical methods by finding complex, non-linear patterns that simple threshold-based methods miss. Unsupervised techniques like Isolation Forest and autoencoders detect unknown anomalies, while supervised classification identifies known failure patterns.

## Architecture

```
ML Detection Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Feature Engineering] → [ML Model] → [Anomaly Score] → [Alert Decision]
         │                    │              │                 │
  Raw metrics → features   Inference    0.0 - 1.0 score    Score > threshold
  Rolling statistics      endpoint      with explanation    → fire alert
  Time-based features     (ONNX/TF)     features
  Metric ratios                         contributing
  Text embeddings                       to anomaly
  (for log data)
        │
  [Model Registry]
  ├── Isolation Forest (unsupervised)
  ├── Autoencoder (unsupervised)
  ├── XGBoost (supervised)
  ├── LSTM (time series)
  └── Ensemble (multiple models)

Model Selection Guide:
  ┌──────────────────┬────────────┬───────────┬─────────────┐
  │ Model            │ Data Needs │ Interpret │ Use Case     │
  ├──────────────────┼────────────┼───────────┼─────────────┤
  │ Isolation Forest │ Low        │ Medium    │ General      │
  │ Autoencoder      │ Medium     │ Low       │ Complex      │
  │ XGBoost          │ High(labeled)│ High    │ Known issues │
  │ LSTM             │ High       │ Low       │ Time series  │
  └──────────────────┴────────────┴───────────┴─────────────┘
```

## Design Decisions

- **Ensemble Approach**: Multiple models combined for robust detection
- **ONNX Runtime**: Models exported to ONNX for cross-platform inference
- **Feature Store**: Pre-computed features served from Redis for low-latency inference
- **Explainability**: SHAP values provide feature-level anomaly explanations

## Implementation Approach

```typescript
interface MLDetectionConfig {
  modelId: string;
  modelType: 'isolation_forest' | 'autoencoder' | 'xgboost' | 'lstm' | 'ensemble';
  featureNames: string[];
  threshold: number;
  ensembleWeights?: Record<string, number>;
}

interface MLAnomalyResult {
  score: number;
  isAnomaly: boolean;
  modelId: string;
  featureImportance: Array<{ feature: string; importance: number }>;
  prediction: number;
  threshold: number;
}

class MLAnomalyDetector {
  private models: Map<string, InferenceSession> = new Map();
  private featureStore: FeatureStore;

  async loadModel(config: MLDetectionConfig): Promise<void> {
    const modelPath = `/models/${config.modelId}/model.onnx`;
    const session = await ort.InferenceSession.create(modelPath);
    this.models.set(config.modelId, session);
  }

  async detect(features: number[], config: MLDetectionConfig): Promise<MLAnomalyResult> {
    if (config.modelType === 'ensemble') {
      return this.ensembleDetect(features, config);
    }

    const session = this.models.get(config.modelId)!;
    const tensor = new ort.Tensor('float32', new Float32Array(features), [1, features.length]);
    const results = await session.run({ input: tensor });

    const score = results.anomaly_score.data[0];
    const featureImportance = this.computeFeatureImportance(results, config.featureNames);

    return {
      score, modelId: config.modelId,
      isAnomaly: score > config.threshold,
      featureImportance,
      prediction: results.prediction?.data[0] ?? score,
      threshold: config.threshold,
    };
  }

  private async ensembleDetect(
    features: number[], config: MLDetectionConfig
  ): Promise<MLAnomalyResult> {
    const modelResults = await Promise.all(
      Object.entries(config.ensembleWeights || {}).map(async ([modelId, weight]) => {
        const modelConfig: MLDetectionConfig = {
          modelId, modelType: 'isolation_forest',
          featureNames: config.featureNames,
          threshold: config.threshold,
        };
        const result = await this.detect(features, modelConfig);
        return { ...result, weight };
      })
    );

    const weightedScore = modelResults.reduce(
      (sum, r) => sum + r.score * r.weight, 0
    ) / modelResults.reduce((sum, r) => sum + r.weight, 0);

    // Average feature importance across models
    const featureImportance = config.featureNames.map((feature, i) => ({
      feature,
      importance: modelResults.reduce((sum, r) => sum + r.featureImportance[i].importance, 0) / modelResults.length,
    }));

    return {
      score: weightedScore,
      modelId: 'ensemble',
      isAnomaly: weightedScore > config.threshold,
      featureImportance,
      prediction: weightedScore,
      threshold: config.threshold,
    };
  }

  private computeFeatureImportance(
    results: ort.InferenceSession.OnnxValue,
    featureNames: string[]
  ): Array<{ feature: string; importance: number }> {
    const shapValues = results.shap_values?.data;
    if (!shapValues) {
      return featureNames.map((f, i) => ({ feature: f, importance: 1 / featureNames.length }));
    }

    return featureNames.map((feature, i) => ({
      feature,
      importance: Math.abs(shapValues[i]),
    })).sort((a, b) => b.importance - a.importance);
  }

  async extractFeatures(rawData: Record<string, number>): Promise<number[]> {
    const features: number[] = [];

    // Rolling statistics
    const values = Object.values(rawData);
    const mean = values.reduce((s, v) => s + v, 0) / values.length;
    features.push(mean);

    const sorted = [...values].sort((a, b) => a - b);
    features.push(sorted[Math.floor(sorted.length * 0.5)]); // median
    features.push(sorted[Math.floor(sorted.length * 0.95)]); // p95
    features.push(sorted[Math.floor(sorted.length * 0.99)]); // p99

    // Rate of change
    if (values.length >= 2) {
      features.push(values[values.length - 1] - values[values.length - 2]);
      features.push(values[values.length - 1] / Math.max(values[values.length - 2], 0.001));
    } else {
      features.push(0, 1);
    }

    // Variance
    const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;
    features.push(Math.sqrt(variance));

    return features;
  }
}
```

## Integration Points

- **Feature Store**: Pre-computed features for low-latency inference
- **Model Registry**: Versioned model storage and deployment
- **Training Pipeline**: Automated retraining on labeled data

## Production Considerations

- **Inference Latency**: Target < 50ms per inference
- **Model Versioning**: Canary deployment for new model versions
- **Data Drift Monitoring**: Track feature distribution shifts
- **Fallback to Statistical**: Degrade to statistical methods if ML fails

## Open-Source Tools

- **ONNX Runtime**: Cross-platform ML inference
- **scikit-learn**: Model training (Isolation Forest, XGBoost)
- **SHAP**: Model explainability
- **MLflow**: Model registry and lifecycle management
