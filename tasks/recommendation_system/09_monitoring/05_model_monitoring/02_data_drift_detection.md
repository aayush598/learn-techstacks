# Data Drift Detection for Recommendation Systems

## 1. What is Data Drift

### 1.1 Types of Drift
- **Data Drift (Covariate Shift)**: Input feature distribution changes over time
- **Concept Drift**: Relationship between features and target changes over time
- **Prediction Drift**: Model prediction distribution changes
- **Label Drift**: Distribution of actual outcomes changes

### 1.2 Why Drift Matters for Recommendations
- User preferences change over time (seasonal, trending)
- New items change the catalog distribution
- External events affect behavior patterns
- Model trained on old data becomes stale
- Drift degrades recommendation quality silently

---

## 2. Statistical Tests for Drift Detection

### 2.1 Population Stability Index (PSI)
- Measures shift in distribution between two periods
- PSI < 0.1: No significant drift
- PSI 0.1-0.25: Moderate drift; investigate
- PSI > 0.25: Significant drift; retrain model
- **Calculation**: Sum of (actual% - expected%) × ln(actual%/expected%)

### 2.2 Kolmogorov-Smirnov (KS) Test
- Non-parametric test for distribution differences
- Tests maximum distance between cumulative distributions
- p-value < 0.05 indicates significant drift
- Works for continuous features
- Limitation: sensitive to sample size

### 2.3 Jensen-Shannon (JS) Divergence
- Measures similarity between two probability distributions
- Symmetric and bounded [0, 1]
- Lower values = more similar distributions
- Good for categorical feature drift detection

### 2.4 Chi-Squared Test
- Tests for distribution differences in categorical features
- Compares observed vs expected frequencies
- Good for category-level drift (e.g., item category distribution)

---

## 3. Drift Detection Implementation

### 3.1 Reference vs Current Window
- **Reference Window**: Baseline distribution (e.g., training data distribution)
- **Current Window**: Recent data distribution (e.g., last 24 hours)
- **Comparison**: Statistical test between reference and current

### 3.2 Detection Frequency
- **Real-time**: Stream processing with sliding windows (every 5 minutes)
- **Hourly**: Batch comparison of hourly distributions
- **Daily**: Full daily distribution comparison
- **Weekly**: Comprehensive drift analysis with root cause

### 3.3 Alerting Strategy
```
Drift Level | PSI Value | Action
No Drift    | < 0.1     | Monitor
Moderate    | 0.1-0.25  | Alert ML team, investigate
Severe      | > 0.25    | Trigger model retraining
Critical    | > 0.5     | Emergency retraining + rollback check
```

---

## 4. Feature-Level Drift

### 4.1 Monitoring Each Feature
- Compute drift metrics for every feature in the model
- Track drift over time per feature
- Identify which features are drifting most
- Correlate feature drift with model performance degradation

### 4.2 Feature Group Drift
- **User Features**: Track user behavior pattern changes
- **Item Features**: Track item catalog distribution changes
- **Interaction Features**: Track user-item interaction pattern changes
- **Context Features**: Track contextual distribution changes

### 4.3 Drift Root Cause Analysis
1. Identify which features have drifted
2. Analyze feature distribution change
3. Trace back to data source changes
4. Determine if drift is natural (seasonal) or anomalous
5. Decide if retraining or feature engineering adjustment needed

---

## 5. Concept Drift Detection

### 5.1 Online Performance Monitoring
- Track CTR/conversion rate over time
- Monitor prediction accuracy on recent data
- Compare online metrics with offline expectations
- Detect performance degradation before business impact

### 5.2 Adaptive Windows
- **ADWIN**: Adaptive windowing that automatically adjusts window size
- **DDM**: Drift Detection Method based on error rate monitoring
- **EDDM**: Early DDM for detecting gradual drift
- **Page-Hinkley**: Detects changes in mean of monitored variable

### 5.3 Model Performance Drift
- Compare model predictions with actual outcomes
- Track calibration drift (predicted probability vs actual frequency)
- Monitor ranking quality degradation
- A/B test continuous monitoring for statistical significance

---

## 6. Drift Mitigation Strategies

### 6.1 Automated Retraining
- Trigger retraining when drift exceeds threshold
- Use recent data for retraining (sliding window)
- Validate retrained model before deployment
- Gradual rollout of retrained model

### 6.2 Feature Engineering Adjustments
- Update feature computation to handle new distributions
- Add new features to capture emerging patterns
- Remove features that are no longer informative
- Adjust feature encoding for distribution changes

### 6.3 Model Adaptation
- Online learning for continuous adaptation
- Ensemble with recent model for freshness
- Context-aware models that adapt to distribution changes
- Multi-armed bandits for exploration of new patterns
