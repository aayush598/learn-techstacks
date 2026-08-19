# Feature Engineering Tests

## 1. Overview

Feature engineering is the process of transforming raw data into meaningful inputs for
recommendation models. In a production recommendation system, feature engineering tests are
arguably the most important testing category because feature quality directly determines
recommendation quality. The principle "garbage in, garbage out" applies precisely here.

### 1.1 Why Feature Engineering Testing is Critical

- Feature errors propagate silently through the entire ML pipeline
- A single incorrect feature can significantly degrade recommendation quality
- Feature engineering code often involves complex temporal and statistical logic
- Feature freshness and correctness are orthogonal concerns requiring separate testing
- Feature distributions affect model training stability and convergence

### 1.2 Feature Categories in Recommendation Systems

| Category | Examples | Computation | Test Priority |
|---|---|---|---|
| User behavioral | Click history, purchase frequency | Aggregation over time windows | Critical |
| Item content | Title embeddings, category, price | Pre-computed or on-the-fly | High |
| Contextual | Time of day, device type, location | Direct from request | High |
| Collaborative | User-item interaction patterns | Matrix factorization, embeddings | Critical |
| Cross-feature | User-category affinity, user-price sensitivity | Derived from multiple sources | High |
| Real-time | Recent interactions, trending items | Streaming computation | Critical |

---

## 2. Feature Computation Correctness

### 2.1 Numerical Accuracy Testing

Every feature must be tested against a reference implementation, typically a manual
calculation or a known-correct Python implementation.

**Testing methodology:**

```
Step 1: Construct input data with known values
Step 2: Execute feature computation pipeline
Step 3: Compare pipeline output against reference computation
Step 4: Assert difference is within acceptable tolerance
Step 5: Log any discrepancies for investigation
```

**Tolerance levels by feature type:**

| Feature Type | Tolerance | Rationale |
|---|---|---|
| Count features | Exactly 0 | Integer counts must be exact |
| Ratio features | 1e-6 | Floating-point division precision |
| Normalized features | 1e-4 | Min-max or z-score normalization |
| Probability features | 1e-4 | Softmax or sigmoid outputs |
| Embedding features | 1e-3 | Neural network computations |
| Rank features | Exactly 0 | Ordinal positions must be exact |

### 2.2 Time Window Correctness

Time-windowed features are the most common source of bugs in recommendation feature engineering.

**Common time window errors:**

- **Off-by-one in start boundary**: Including or excluding the boundary event
- **Off-by-one in end boundary**: Whether "last 7 days" includes today
- **Timezone inconsistency**: Computing features in UTC vs local time
- **Daylight saving transitions**: Incorrect window during DST changes
- **Leap second handling**: Rare but can cause window misalignment
- **Inclusive vs exclusive boundaries**: `>=` vs `>` for timestamp comparisons

**Test scenarios for time windows:**

| Scenario | Description | Expected Behavior |
|---|---|---|
| Exact boundary | Event at window boundary timestamp | Include/exclude per specification |
| Multi-timezone | Events across timezone boundaries | All computed in consistent timezone |
| DST transition | Window spans DST change | Window duration unaffected by DST |
| Midnight boundary | Feature computed at midnight | Correct day assignment |
| Month boundary | Monthly aggregation crosses month | Items correctly assigned to months |
| Empty window | No events in time window | Return default/null value |

### 2.3 Edge Case Testing

| Edge Case | Input | Expected Output |
|---|---|---|
| No interaction history | New user with zero events | Default feature values |
| Single interaction | User with exactly one event | Correctly computed from single data point |
| All identical values | All clicks on same item | Correct aggregation |
| Maximum values | Very large counts (overflow risk) | Correct handling without overflow |
| Negative values | Negative dwell time (data error) | Filtered or clamped per policy |
| Null values in source | Missing required fields | Default values or null propagation |
| Duplicate events | Same event appearing twice | Deduplicated correctly |
| Future timestamps | Events with timestamps in future | Excluded from computation |
| Very old events | Events years in the past | Correctly included/excluded per window |

---

## 3. Feature Freshness Validation

### 3.1 Batch Feature Freshness

Batch features must be computed and available within defined SLAs.

**Freshness requirements:**

| Feature Group | Computation Frequency | Maximum Latency | Availability Target |
|---|---|---|---|
| Daily behavioral | Daily (2 AM) | 4 hours | 99.9% |
| Hourly trending | Hourly | 30 minutes | 99.5% |
| Weekly aggregates | Weekly (Sunday) | 8 hours | 99.9% |
| User profile | On event | 5 minutes | 99.0% |
| Item features | On catalog update | 1 hour | 99.5% |

### 3.2 Real-Time Feature Freshness

Real-time features must update within seconds of source events.

**Freshness measurement:**

1. **Event timestamp**: Record when the source event occurred
2. **Feature store timestamp**: Record when the feature was updated
3. **Serving timestamp**: Record when the feature was served
4. **End-to-end latency**: Difference between event and serving timestamps
5. **Freshness SLA compliance**: Percentage of features served within SLA

**Freshness validation approach:**

```
Inject known event at time T
    ↓
Wait for feature update notification
    ↓
Read feature value from feature store
    ↓
Assert feature timestamp >= T
    ↓
Assert feature timestamp - T < SLA (e.g., 5 seconds)
    ↓
Assert feature value reflects the injected event
```

### 3.3 Feature Staleness Detection

- **Age monitoring**: Track time since last update for each feature
- **Staleness alerts**: Alert when feature age exceeds threshold
- **Staleness metrics**: Dashboard showing feature freshness distribution
- **Automatic fallback**: Serve cached/default values when features are stale

---

## 4. Feature Distribution Tests

### 4.1 Distribution Monitoring

Feature distributions should be monitored for unexpected changes that indicate bugs
or data quality issues.

**Distribution metrics to track:**

| Metric | Description | Alert Threshold |
|---|---|---|
| Mean | Average feature value | > 2σ from baseline |
| Standard deviation | Feature value spread | > 2σ from baseline |
| Skewness | Distribution asymmetry | Significant change |
| Kurtosis | Tail heaviness | Significant change |
| Null rate | Percentage of null values | > 1% increase |
| Zero rate | Percentage of zero values | > 5% change |
| Outlier rate | Percentage of extreme values | > 2x baseline |

### 4.2 Distribution Shift Detection

Statistical tests to detect unexpected distribution shifts:

- **Kolmogorov-Smirnov test**: Compare current distribution against baseline
- **Chi-squared test**: Compare categorical feature distributions
- **Population Stability Index (PSI)**: Measure distribution drift magnitude
- **Jensen-Shannon divergence**: Symmetric divergence between distributions

**PSI interpretation:**

| PSI Value | Interpretation | Action |
|---|---|---|
| < 0.1 | No significant change | Monitor |
| 0.1 - 0.25 | Moderate change | Investigate |
| > 0.25 | Significant change | Alert and investigate |

### 4.3 Distribution Test Automation

```
Daily Pipeline:
1. Compute feature distributions from latest data
2. Load baseline distributions from version-controlled store
3. Compute statistical tests and PSI for each feature
4. Generate distribution comparison report
5. Alert if any feature exceeds thresholds
6. Publish metrics to monitoring dashboard
```

### 4.4 Correlation Preservation

Features should maintain expected correlations:

- **Feature-target correlation**: Features maintain expected correlation with prediction target
- **Feature-feature correlation**: No unexpected collinearity introduced
- **Temporal correlation**: Feature trends align with business expectations
- **Cross-feature consistency**: Derived features maintain mathematical relationships

---

## 5. Feature Importance Tests

### 5.1 Offline Importance Validation

Validate that feature importance rankings match expectations:

**Importance measurement methods:**

| Method | Description | When to Use |
|---|---|---|
| Permutation importance | Feature shuffle impact on metric | Model-agnostic, reliable |
| SHAP values | Game-theoretic feature attribution | Explainable, detailed |
| Tree feature importance | Built-in tree model importance | Fast, tree models only |
| Correlation analysis | Simple feature-target correlation | Quick baseline |
| Ablation study | Remove feature and retrain | Definitive but expensive |

### 5.2 Importance Regression Detection

When a new model is trained, validate feature importance hasn't regressed:

- **Ranking stability**: Top-N important features remain in top-N
- **Value stability**: Importance scores haven't changed dramatically
- **New feature validation**: Newly added features show expected importance
- **Removed feature impact**: Removing deprecated features doesn't degrade model

### 5.3 Feature Redundancy Detection

Test for unexpected feature redundancy:

- **Variance Inflation Factor (VIF)**: Identify multicollinearity (VIF > 10 flagged)
- **Mutual information**: Detect redundant feature pairs
- **Principal component analysis**: Identify features explained by other features
- **Correlation matrix monitoring**: Track correlation changes over time

---

## 6. Feature Store Integration Tests

### 6.1 Write Path Testing

Validate features are correctly written to the feature store:

| Test Scenario | Input | Expected Behavior |
|---|---|---|
| Single entity write | One user's features | Feature stored, readable |
| Batch entity write | 10,000 users' features | All features stored atomically |
| Overwrite existing | Update existing user features | New values replace old |
| Concurrent writes | Two pipelines write same entity | Last-writer-wins or conflict error |
| Schema mismatch | Features don't match schema | Write rejected with error |
| Large value write | Feature value > 1MB | Correctly handled or rejected |

### 6.2 Read Path Testing

Validate features are correctly served from the feature store:

| Test Scenario | Expected Behavior |
|---|---|
| Point lookup | Correct feature values returned |
| Batch lookup | Multiple entities' features returned |
| Missing entity | Default/null values returned |
| Stale read | Most recent version served |
| Consistent read | Read-after-write returns new value |
| High-concurrency read | Consistent performance under load |
| Feature group read | All features in a group returned atomically |

### 6.3 Feature Store Consistency Tests

- **Eventual consistency**: Features become available within expected propagation time
- **Read-your-writes**: After writing a feature, immediate reads return the new value
- **Cross-region consistency**: Features available in all regions within SLA
- **Cache coherence**: Cached features invalidate when underlying data changes

### 6.4 Feature Store Failure Tests

| Failure | Expected Behavior |
|---|---|
| Feature store unavailable | Serve from cache or default values |
| Feature store slow (> 100ms) | Timeout and serve cached values |
| Feature store returns corrupt data | Detect corruption, serve defaults |
| Feature store partial failure | Serve available features, default missing |
| Feature store recovery | Resume normal serving without restart |

### 6.5 End-to-End Feature Pipeline Tests

Complete lifecycle test from raw data to served feature:

```
Raw Data → Feature Computation → Feature Store → Feature Serving → Validation
    ↓              ↓                  ↓              ↓              ↓
Interaction    Spark/Flink job     Write to       Read from      Compare with
events         computes features   feature store  feature store  expected values
```

**Lifecycle test checklist:**

- [ ] Raw data triggers feature computation
- [ ] Computed features match expected values
- [ ] Features written to feature store successfully
- [ ] Features readable from feature store
- [ ] Feature serving latency within SLA
- [ ] Feature values consistent between write and read
- [ ] Feature freshness within SLA
- [ ] Feature store failure handled gracefully

---

## 7. Feature Testing Best Practices

### 7.1 Test Data Strategy

- Use known-value fixtures for unit tests (small, deterministic)
- Use production-like distributions for integration tests
- Use golden datasets for regression tests (versioned, curated)
- Use synthetic data for edge case coverage

### 7.2 Test Automation Framework

```
Feature Test Framework Architecture:
├── Feature Registry         → List of all features with metadata
├── Reference Implementations → Known-correct computation logic
├── Test Data Generator      → Creates input data with controlled properties
├── Assertion Library        → Feature-specific comparison functions
├── Distribution Monitor     → Tracks feature distribution over time
└── Report Generator         → Produces test result summaries
```

### 7.3 Continuous Monitoring

Feature testing doesn't end at deployment:

- **Production feature monitoring**: Track distribution, freshness, and quality metrics
- **Anomaly detection**: Automated detection of unexpected feature behavior
- **Impact analysis**: Correlate feature changes with model performance changes
- **Feedback loop**: Production observations feed back into test case improvements
