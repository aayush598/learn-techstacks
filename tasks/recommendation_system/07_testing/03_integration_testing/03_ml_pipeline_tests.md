# ML Pipeline Tests

## 1. Overview

ML pipeline tests validate the complete machine learning lifecycle—from data preparation
through training, evaluation, deployment, and serving. For recommendation systems, the ML
pipeline is uniquely complex because it involves offline training, online serving, feature
computation, A/B testing, and continuous model updates. This document covers training
pipeline validation, model serving integration, feature serving integration, experiment
service integration, and end-to-end recommendation flow tests.

### 1.1 ML Pipeline Architecture

```
Training Pipeline:
Data Prep → Feature Engineering → Model Training → Evaluation → Registry → Deployment

Serving Pipeline:
User Request → Feature Fetch → Model Inference → Post-processing → Response

Feedback Loop:
User Interaction → Event Processing → Feature Update → Model Retraining
```

### 1.2 ML Pipeline Test Layers

| Layer | Scope | Execution | Purpose |
|---|---|---|---|
| Training validation | Training pipeline correctness | Nightly/weekly | Ensure training produces valid models |
| Model serving integration | Inference path correctness | Per deploy | Ensure serving returns correct results |
| Feature serving integration | Feature pipeline end-to-end | Per deploy | Ensure features are correct and fresh |
| Experiment service | A/B test framework correctness | Per deploy | Ensure experiments run correctly |
| E2E recommendation flow | Complete user journey | Pre-deploy | Ensure full system works together |

---

## 2. Training Pipeline Validation

### 2.1 Data Preparation Tests

**Input data validation:**

| Test | Description | Acceptance Criteria |
|---|---|---|
| Data loading | Training data loads without errors | 0 load failures |
| Schema compliance | Data matches expected schema | 100% schema match |
| Label correctness | Target labels are valid | No invalid label values |
| Feature completeness | Required features present | < 1% missing rate |
| Train/test split | Correct splitting strategy | No data leakage between splits |

**Data quality checks in training pipeline:**

- **Class balance**: Verify label distribution is within acceptable range
- **Feature variance**: Remove zero-variance features before training
- **Duplicate detection**: No duplicate training examples across splits
- **Temporal split correctness**: Training data is strictly before validation data
- **Stratification**: Category distribution consistent across splits

### 2.2 Training Execution Tests

| Test | Method | Acceptance Criteria |
|---|---|---|
| Convergence | Monitor training loss | Loss decreases monotonically after warmup |
| Overfitting | Compare train/test metrics | Test metric within 5% of train metric |
| Training time | Measure wall-clock time | Completes within time budget |
| Resource usage | Monitor GPU/CPU/memory | No OOM, no GPU memory leaks |
| Checkpointing | Save/load checkpoints | Model state correctly restored |
| Reproducibility | Same seed + data = same model | Model weights match within tolerance |

### 2.3 Model Evaluation Tests

**Offline metric validation:**

| Metric | Target | Test Method |
|---|---|---|
| NDCG@10 | > 0.35 | Evaluate on held-out test set |
| Recall@20 | > 0.45 | Evaluate on held-out test set |
| MAP@10 | > 0.25 | Evaluate on held-out test set |
| Coverage | > 60% of catalog | Measure unique items recommended |
| Diversity | > 0.5 intra-list diversity | Average pairwise distance in recommendations |
| Popularity bias | Gini coefficient < 0.7 | Measure recommendation distribution |

**Evaluation sanity checks:**

- Model performs better than random baseline
- Model performs better than popularity baseline
- Model performs better than previous production model
- Metrics are stable across multiple evaluation runs
- Metrics are consistent across user segments

### 2.4 Model Artifact Tests

- **Model serialization**: Model saves and loads without corruption
- **Model size**: Model artifact within deployment size limits
- **Inference compatibility**: Saved model produces same predictions as training model
- **Version metadata**: Model metadata (hyperparameters, data version, metrics) recorded correctly
- **Dependency tracking**: All dependencies (feature libraries, model libraries) tracked

### 2.5 Hyperparameter Validation

| Validation | Method | Criteria |
|---|---|---|
| Parameter ranges | Check against search space | All parameters within defined bounds |
| Learning rate schedule | Monitor loss curve | No divergence, reasonable convergence |
| Regularization | Compare with/without regularization | Regularized model generalizes better |
| Architecture parameters | Check model dimensions | Layer sizes match configuration |

---

## 3. Model Serving Integration

### 3.1 Inference Correctness Tests

Validate that the serving system produces identical results to offline evaluation:

```
Offline Evaluation:
Training Data → Trained Model → Evaluate on Test Set → Metrics

Online Serving:
Same Test Users → Serving API → Compare Predictions → Consistency Check
```

**Consistency checks:**

- Same user + same context → same recommendations (deterministic serving)
- Offline NDCG ≈ Online NDCG (within 2% tolerance)
- Feature values used in serving match feature values from training
- Model version deployed matches evaluated model

### 3.2 Model Loading Tests

| Test | Scenario | Expected Behavior |
|---|---|---|
| Cold start | Start serving from empty state | Model loads within SLA (30s) |
| Hot reload | Update model without restart | New model active within 60s |
| Rollback | Revert to previous model | Previous model active within 30s |
| Failed load | Corrupt model artifact | Error logged, previous model stays active |
| Multiple models | Serve multiple models simultaneously | Each model independently accessible |

### 3.3 Inference Latency Tests

| Metric | Target | Measurement |
|---|---|---|
| P50 latency | < 30ms | All inference requests |
| P99 latency | < 100ms | All inference requests |
| P999 latency | < 200ms | All inference requests |
| Cold start latency | < 30s | First request after deployment |
| Batch inference latency | < 500ms for 1000 items | Batch prediction requests |

### 3.4 Fallback Behavior Tests

| Failure | Expected Fallback | Quality Impact |
|---|---|---|
| Model unavailable | Serve popularity-based recs | Moderate degradation |
| Feature unavailable | Use default feature values | Minor degradation |
| Timeout | Return cached recommendations | Minor degradation |
| Partial failure | Return partial results | Acceptable degradation |
| Model corrupted | Rollback to previous version | Temporary degradation |

### 3.5 A/B Test Model Deployment

Test that model deployments correctly support A/B testing:

- **Traffic splitting**: Correct percentage of users routed to each model version
- **Consistent hashing**: Same user always sees same model version within experiment
- **Metric isolation**: Experiment metrics correctly attributed to each model version
- **Quick rollback**: Can revert experiment without affecting other experiments
- **Statistical validity**: Sample size sufficient for meaningful comparison

---

## 4. Feature Serving Integration

### 4.1 Feature Serving Path Tests

Validate the complete feature serving path:

```
User Request → Identify Required Features → Fetch from Feature Store → Assemble Feature Vector → Return
```

**Test scenarios:**

| Scenario | Expected Behavior |
|---|---|
| All features available | Feature vector complete, correct values |
| Some features missing | Default values used for missing features |
| Feature store down | Cached features served, freshness degraded |
| Feature store slow | Timeout with cached/default fallback |
| New user (no history) | Cold-start feature values applied |
| Feature schema change | New schema handled gracefully |

### 4.2 Feature Consistency Tests

Ensure features used in serving match features used in training:

- **Feature name mapping**: Serving feature names map correctly to training features
- **Feature value range**: Serving feature values within range seen during training
- **Feature transformation**: Same transformations applied in serving as in training
- **Feature normalization**: Same normalization parameters used (mean, std from training)
- **Categorical encoding**: Same category-to-index mapping used

### 4.3 Feature Freshness in Serving

| Metric | Target | Alert Threshold |
|---|---|---|
| Feature staleness (real-time) | < 5 seconds | > 10 seconds |
| Feature staleness (batch) | < 4 hours | > 8 hours |
| Feature serving latency | < 5ms p99 | > 10ms p99 |
| Feature cache hit rate | > 95% | < 90% |
| Feature freshness SLA compliance | > 99.9% | < 99.5% |

### 4.4 Feature Store Integration Tests

- **Write path**: Features written by pipeline are readable by serving
- **Read path**: Serving reads correct features for given user/item
- **Batch operations**: Bulk feature fetches for batch prediction work correctly
- **Concurrent access**: Feature store handles serving QPS without degradation
- **Cache coherence**: Cached features invalidate when underlying data changes

---

## 5. Experiment Service Integration

### 5.1 Experiment Framework Tests

| Test | Description | Acceptance Criteria |
|---|---|---|
| Traffic allocation | Users assigned to variants | Assignment matches configured percentages |
| Consistent assignment | Same user → same variant | 100% consistent assignment |
| Metric collection | Metrics recorded per variant | All metrics captured correctly |
| Statistical significance | Tests detect meaningful differences | Type I error < 5%, power > 80% |
| Experiment isolation | Concurrent experiments independent | No cross-contamination between experiments |

### 5.2 Experiment Lifecycle Tests

```
Create Experiment → Configure Variants → Start Experiment → Collect Metrics → Analyze → Conclude
       ↓                  ↓                  ↓                 ↓             ↓          ↓
  Setup test         Traffic rules      Begin serving      Track events    Statistical  Choose
  groups             and features       variant-specific   per variant    analysis     winner
```

### 5.3 Experiment Safety Tests

- **Guardrail metrics**: Experiment stops if key metrics degrade beyond threshold
- **Sample ratio mismatch**: Detect if actual traffic split differs from configured
- **Novelty effect**: Detect initial metric changes that regress over time
- **Interaction effects**: Detect when concurrent experiments interfere
- **Duration validation**: Ensure experiment runs long enough for significance

---

## 6. End-to-End Recommendation Flow Tests

### 6.1 Complete User Journey Tests

| Journey | Steps | Expected Outcome |
|---|---|---|
| New user recommendation | Register → First visit → View recommendations | Cold-start recommendations served |
| Personalized recommendation | Login → Browse → View personalized recs | History-based recommendations |
| Post-interaction update | Click item → Request new recommendations | Updated recommendations reflect interaction |
| Search-integrated recommendation | Search → View search results + recommendations | Contextual recommendations alongside search |
| Notification-triggered | Receive push → Open app → View recommendations | Time-sensitive recommendations |

### 6.2 Recommendation Quality Tests

| Quality Dimension | Test Method | Target |
|---|---|---|
| Relevance | Human evaluation on sample | > 70% relevant |
| Diversity | Intra-list diversity metric | > 0.5 average distance |
| Freshness | Percentage of recent items | > 20% items from last 30 days |
| Serendipity | Unexpected but relevant recommendations | > 10% non-obvious recommendations |
| Fairness | Distribution across categories | No category > 50% of recommendations |

### 6.3 Cross-System Integration Tests

Verify that all systems work together:

- **User service + recommendation engine**: User profile correctly influences recommendations
- **Content service + recommendation engine**: Item metadata correctly used in features
- **Analytics service + recommendation engine**: User interactions correctly tracked
- **Experiment service + recommendation engine**: A/B test variants correctly applied
- **Notification service + recommendation engine**: Triggered notifications use correct recommendations

### 6.4 Regression Detection

End-to-end tests must detect quality regressions:

- **Metric regression**: Current model metrics below previous production model
- **Latency regression**: End-to-end latency exceeds baseline
- **Coverage regression**: Fewer unique items recommended than baseline
- **Diversity regression**: Recommendations more concentrated than baseline
- **Fairness regression**: Unfair treatment of user or item segments

---

## 7. Test Automation and CI/CD

### 7.1 ML Pipeline Test Execution

| Test Category | Trigger | Environment | Timeout |
|---|---|---|---|
| Training validation | New model training | Training cluster | 4 hours |
| Model serving integration | Model deployment | Staging | 30 minutes |
| Feature serving integration | Feature pipeline change | Staging | 30 minutes |
| Experiment service | Framework change | Staging | 1 hour |
| E2E recommendation flow | Pre-deploy | Pre-production | 2 hours |

### 7.2 Model Validation Gate

Before any model reaches production:

1. **Offline metrics gate**: All metrics meet minimum thresholds
2. **Fairness gate**: No fairness violations detected
3. **Latency gate**: Inference latency within SLA
4. **Size gate**: Model artifact within deployment limits
5. **Integration gate**: All integration tests pass
6. **A/B test plan**: Experiment plan reviewed and approved
7. **Rollback plan**: Rollback procedure documented and tested

### 7.3 Continuous ML Monitoring

Post-deployment monitoring complements testing:

- **Online metric tracking**: Real-time model performance monitoring
- **Feature drift detection**: Automated detection of feature distribution changes
- **Prediction distribution monitoring**: Track recommendation distribution over time
- **User feedback integration**: Incorporate user signals into quality assessment
- **Automated retraining triggers**: Retrain when metrics degrade below threshold
