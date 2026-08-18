# Model Drift Detection for Recommendation Systems

## Overview

Model drift occurs when a trained recommendation model's performance degrades over time due to
changes in data distributions, user behavior, or the underlying environment. Drift detection
is essential for maintaining recommendation quality — a model trained on historical data will
gradually become less relevant as user preferences evolve, new items are introduced, and
seasonal patterns shift. This covers drift types, statistical detection methods, automated
pipelines, alerting, and retraining triggers.

## Types of Drift

### Data Drift (Covariate Shift)

Data drift occurs when the distribution of input features changes between training and serving:

```
Training Data Distribution:
  user_age: mean=32, std=8
  session_duration: mean=450s, std=120s
  purchase_frequency: mean=2.3/week, std=1.1

Serving Data Distribution (6 months later):
  user_age: mean=35, std=9          ← shifted (new user demographic)
  session_duration: mean=380s, std=150s  ← shifted (mobile usage increase)
  purchase_frequency: mean=1.8/week, std=1.3  ← shifted (economic change)
```

### Concept Drift

Concept drift occurs when the relationship between features and the target variable changes:

```
Before drift:
  High session duration → High purchase probability (users browse and buy)

After drift:
  High session duration → Low purchase probability (users browse but comparison-shop)
```

### Prediction Drift

Prediction drift occurs when the distribution of model outputs changes, even if inputs are stable:

```
Before drift:
  Recommendation scores: mean=0.72, std=0.15
  Top category distribution: Electronics 30%, Clothing 25%, Home 20%, Other 25%

After drift:
  Recommendation scores: mean=0.58, std=0.22  ← scores declining
  Top category distribution: Electronics 45%, Clothing 15%, Home 15%, Other 25%
                              ← concentrating on one category
```

### User Behavior Drift

Recommendation-specific drift patterns:
- **Seasonal shifts**: Holiday shopping vs. everyday browsing
- **Event-driven shifts**: Viral product trends, flash sales
- **Demographic shifts**: New user segments joining the platform
- **Preference evolution**: User interests changing over time
- **Platform changes**: New features changing how users interact

## Statistical Tests for Drift Detection

### Kolmogorov-Smirnov (KS) Test

Tests whether two samples come from the same distribution:

- Non-parametric (no distribution assumption)
- Works for continuous features
- Sensitive to distribution shape differences
- KS statistic ranges from 0 (identical) to 1 (completely different)

| KS Statistic Range | Interpretation                   | Action           |
|-------------------|----------------------------------|-------------------|
| 0.0 - 0.05        | No significant drift              | No action         |
| 0.05 - 0.10       | Mild drift                        | Monitor closely   |
| 0.10 - 0.20       | Moderate drift                    | Investigate       |
| 0.20+             | Severe drift                      | Retraining needed |

### Population Stability Index (PSI)

Measures how much a variable's distribution has shifted:

- Designed for population stability analysis
- Works with binned distributions
- Common in credit scoring, applicable to recommendations
- PSI < 0.1: No significant change
- PSI 0.1-0.25: Moderate change
- PSI > 0.25: Significant change requiring action

### Jensen-Shannon Divergence (JSD)

Symmetric measure of distribution similarity:

- Bounded between 0 (identical) and 1 (maximally different)
- Handles high-dimensional distributions
- Suitable for comparing embedding distributions
- More stable than KL divergence for small sample sizes

### Chi-Squared Test

Tests whether categorical feature distributions have changed:

- Applicable to categorical features (item categories, user segments)
- Compares observed vs. expected frequencies
- Requires sufficient sample size per category

### Comparison of Methods

| Method              | Data Type       | Sensitivity | Speed    | Use Case                     |
|--------------------|-----------------|-------------|----------|------------------------------|
| KS Test            | Continuous       | High        | Fast     | Feature distribution drift    |
| PSI                | Continuous/Binned| Medium      | Fast     | Population stability          |
| JSD                | Any distribution | High        | Medium   | Embedding drift               |
| Chi-Squared        | Categorical      | Medium      | Fast     | Category distribution drift   |
| Wasserstein Distance| Continuous      | High        | Slow     | Distribution shift magnitude  |
| MMD (Maximum Mean) | High-dimensional | High        | Slow     | Embedding space drift          |

## Automated Drift Detection Pipelines

### Pipeline Architecture

```
Data Sources:
├── Training data snapshots (baseline)
├── Production serving logs (current)
├── Feature store history
└── Model prediction logs

Drift Detection Pipeline:
├── Feature extraction and comparison
│   ├── Numerical features → KS test, PSI
│   ├── Categorical features → Chi-squared, PSI
│   └── Embeddings → JSD, MMD
├── Prediction drift detection
│   ├── Score distribution comparison
│   ├── Recommendation diversity metrics
│   └── Category distribution analysis
├── Statistical aggregation
│   ├── Per-feature drift scores
│   ├── Composite drift index
│   └── Confidence intervals
└── Decision engine
    ├── Drift score vs. threshold comparison
    ├── Trend analysis (is drift increasing?)
    └── Retraining trigger decision

Output:
├── Drift dashboard (Grafana)
├── Drift alerts (Prometheus)
├── Drift reports (daily/weekly)
└── Retraining pipeline trigger
```

### Baseline Management

Maintain reference distributions for drift comparison:

```
Baseline Dataset:
├── Version: v2.3-training-2024-01
├── Date range: 2023-10-01 to 2023-12-31
├── Sample size: 10M interactions
├── Feature statistics:
│   ├── user_age: {mean: 32.1, std: 8.3, p5: 18, p95: 55}
│   ├── session_duration: {mean: 452, std: 118, p5: 30, p95: 890}
│   ├── purchase_count_30d: {mean: 2.3, std: 1.1, p5: 0, p95: 6}
│   └── category_distribution: {Electronics: 0.28, Clothing: 0.24, ...}
└── Prediction statistics:
    ├── score_mean: 0.72
    ├── score_std: 0.15
    ├── ndcg_at_10: 0.42
    └── diversity_index: 0.65
```

### Sliding Window Comparison

Compare current data against baseline using sliding windows:

| Window Size    | Comparison Target            | Latency    | Sensitivity |
|---------------|------------------------------|------------|-------------|
| 1 hour        | Short-term anomalies          | Near real-time | Low       |
| 1 day         | Daily patterns                | Daily      | Medium       |
| 1 week        | Weekly seasonality            | Weekly     | High         |
| 1 month       | Long-term trends              | Monthly    | Very High    |

## Drift Alerting

### Alert Thresholds

| Alert                         | Condition                                    | Severity |
|------------------------------|----------------------------------------------|----------|
| Feature drift detected       | Any feature PSI > 0.25                        | Warning  |
| Multiple features drifting   | > 3 features PSI > 0.15                       | Warning  |
| Prediction drift             | Score distribution PSI > 0.2                  | Warning  |
| Model accuracy degraded      | Offline metric < threshold for 24 hours       | Critical |
| Severe concept drift         | JSD > 0.3 for label distribution              | Critical |
| Embedding drift              | MMD > threshold for user/item embeddings      | Warning  |

### Drift Dashboard Panels

| Panel                        | Visualization   | Purpose                           |
|-----------------------------|----------------|-----------------------------------|
| Per-feature PSI heatmap      | Heatmap         | Identify which features are drifting|
| Drift score trend            | Time series     | Track drift progression over time |
| Prediction score distribution| Histogram       | Compare current vs. baseline      |
| Category distribution        | Bar chart       | Recommendation category balance   |
| Model accuracy trend         | Time series     | Track quality degradation         |
| Feature importance + drift   | Scatter plot    | High-importance features drifting?|

## Retraining Triggers

### Trigger Conditions

```
Automatic Retraining Triggers:
├── Scheduled: Every 2 weeks (regular refresh)
├── Drift-based: Composite drift score > threshold for 48 hours
├── Performance: NDCG@10 drops below 0.35 for 24 hours
├── Event-based: Major feature pipeline change deployed
└── Manual: Data scientist request after investigation

Retraining Process:
1. Validate new training data quality
2. Train model with updated data
3. Evaluate on holdout set (must exceed minimum quality bar)
4. Shadow deployment (serve predictions without showing to users)
5. A/B test against current model
6. Promote if A/B test shows improvement
7. Rollback if issues detected within 48 hours
```

### Model Performance Degradation Detection

Monitor online metrics that indicate degradation:

| Metric                        | Healthy Range      | Degradation Signal               |
|------------------------------|-------------------|----------------------------------|
| Click-through rate (CTR)      | > 2%              | Drop > 20% from baseline         |
| Conversion rate               | > 0.5%            | Drop > 15% from baseline         |
| Recommendation diversity      | > 0.6             | Drop below 0.4                   |
| Coverage (% items recommended)| > 30%             | Drop below 15%                   |
| User session duration         | Baseline ± 10%    | Drop > 20%                       |
| Repeat visit rate             | Baseline ± 5%     | Drop > 10%                       |

## Feature Drift Monitoring

### Per-Feature Monitoring

Every feature used by the model should be monitored:

```
Feature Monitoring Configuration:
├── user_avg_purchase_value:
│   ├── drift_test: KS
│   ├── alert_threshold: 0.10
│   ├── retrain_threshold: 0.20
│   ├── comparison_window: 7 days
│   └── baseline: training_data_snapshot
│
├── item_category:
│   ├── drift_test: chi_squared
│   ├── alert_threshold: PSI 0.25
│   ├── retrain_threshold: PSI 0.40
│   ├── comparison_window: 7 days
│   └── baseline: training_data_snapshot
│
└── user_embedding:
    ├── drift_test: MMD
    ├── alert_threshold: 0.15
│   ├── retrain_threshold: 0.25
│   ├── comparison_window: 7 days
│   └── baseline: model_checkpoint_embeddings
```

### Feature Importance + Drift Analysis

Prioritize monitoring for high-impact features:

1. Compute feature importance (SHAP values, permutation importance)
2. Compute drift score per feature
3. Plot importance vs. drift — top-right quadrant is highest priority
4. Features with high importance AND high drift require immediate attention

### Embedding Drift Detection

Neural recommendation models produce embeddings that can drift:

- Monitor cosine similarity between current and baseline embedding clusters
- Detect if embedding space is collapsing (reduced diversity)
- Track nearest-neighbor stability (are the same items clustering together?)
- Use UMAP/t-SNE visualization for qualitative analysis
