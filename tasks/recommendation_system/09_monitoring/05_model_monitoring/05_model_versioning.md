# Model Versioning in Production

## 1. Overview

Model versioning tracks every version of a model from training through deployment, enabling reproducibility, rollback, comparison, and audit. In recommendation systems with frequent model updates (weekly or daily retraining), robust versioning is essential for maintaining system reliability and understanding model behavior over time.

### 1.1 Why Model Versioning Matters

- **Reproducibility**: Any prediction can be traced back to the exact model version, features, and data that produced it
- **Rollback**: Quickly revert to a previous model version if the new version degrades performance
- **Comparison**: Compare performance across model versions for informed promotion decisions
- **Audit**: Regulatory requirements often mandate tracking which model produced which prediction
- **Debugging**: When issues arise, versioning helps identify when the issue started

### 1.2 Versioning Scope

A complete model version encompasses:

```
Model Version = Code + Data + Features + Configuration + Environment

Components:
- Model weights/parameters
- Feature pipeline version
- Feature schema/version
- Training data version
- Hyperparameters
- Runtime configuration
- Infrastructure version (GPU type, library versions)
```

---

## 2. Version Tracking

### 2.1 Version Naming Convention

```
Format: {model_name}-{date}-{variant}

Examples:
  ranking-v3-2026.08.15-stable
  ranking-v3-2026.08.15-canary
  ranking-v3-2026.08.15-experiment-42
  candidate-gen-v2-2026.08.10-rc1
```

### 2.2 Version Metadata

Every model version should store:

```json
{
  "version_id": "ranking-v3-2026.08.15-stable",
  "model_name": "ranking-v3",
  "created_at": "2026-08-15T10:30:00Z",
  "created_by": "ml-pipeline",
  "training_data_version": "dataset-2026.08.10-v2",
  "feature_pipeline_version": "features-v4.2",
  "feature_schema_version": "schema-v3.1",
  "framework": "xgboost",
  "framework_version": "2.0.3",
  "hyperparameters": {
    "num_trees": 500,
    "max_depth": 8,
    "learning_rate": 0.1
  },
  "training_metrics": {
    "ndcg@10": 0.435,
    "map@10": 0.312,
    "recall@50": 0.682
  },
  "model_size_bytes": 125000000,
  "inference_latency_ms": 23,
  "artifacts": {
    "model_path": "s3://models/ranking/v3/2026.08.15/model.xgb",
    "config_path": "s3://models/ranking/v3/2026.08.15/config.yaml",
    "feature_list_path": "s3://models/ranking/v3/2026.08.15/features.json"
  }
}
```

### 2.3 Version State Machine

```
Training -> Validation -> Staging -> Canary -> Production -> Retired
    |           |            |          |           |            |
    v           v            v          v           v            v
  Failed    Failed/       Failed    Failed/     Deprecated   Archived
            Rejected               Rejected
```

| State | Description | Duration |
|---|---|---|
| Training | Model being trained | Hours to days |
| Validation | Offline evaluation in progress | Hours |
| Staging | Ready for deployment, awaiting approval | Hours to days |
| Canary | Deployed to 5-10% of traffic | Hours to days |
| Production | Serving 100% of traffic | Weeks to months |
| Retired | No longer serving traffic | Permanent |
| Archived | Stored for historical reference | Permanent |

---

## 3. Comparison Tools

### 3.1 Offline Comparison

Compare model versions on held-out test data:

| Metric | Current (v2) | Candidate (v3) | Delta | Status |
|---|---|---|---|---|
| NDCG@10 | 0.421 | 0.435 | +3.3% | Improved |
| MAP@10 | 0.298 | 0.312 | +4.7% | Improved |
| Recall@50 | 0.687 | 0.682 | -0.7% | Minor regression |
| Calibration error | 0.032 | 0.041 | +28% | Warning |
| Inference latency P99 | 45ms | 52ms | +15.6% | Warning |
| Model size | 120MB | 180MB | +50% | Monitor |

### 3.2 Online Comparison (A/B Test)

Compare model versions on live traffic:

```
Traffic split:
  Control (v2): 50% of traffic
  Treatment (v3): 50% of traffic

Primary metric: CTR
  v2 CTR: 3.21%
  v3 CTR: 3.38%
  Lift: +5.3%
  p-value: 0.003
  Status: Statistically significant improvement

Guardrail metrics:
  Latency: v2=145ms, v3=162ms (+11.7%)
  Error rate: v2=0.12%, v3=0.14% (not significant)
  Coverage: v2=65%, v3=67% (+3.1%)
```

### 3.3 Feature Importance Comparison

Compare which features the model relies on:

```
Feature importance comparison (top 10):

Feature                    v2    v3    Change
user_engagement_score     0.28  0.25  -0.03
content_popularity         0.22  0.19  -0.03
recency_score             0.15  0.18  +0.03
user_purchase_history     0.12  0.14  +0.02
content_category_match    0.08  0.10  +0.02
user_follow_count         0.05  0.06  +0.01
content_length            0.04  0.04   0.00
time_of_day               0.03  0.02  -0.01
device_type               0.02  0.01  -0.01
content_age_hours         0.01  0.01   0.00
```

### 3.4 Prediction Distribution Comparison

Compare how model outputs differ:

```
Score distribution comparison:

Score Range    v2 (%)    v3 (%)    Difference
0.0 - 0.2      15%       12%       -3%
0.2 - 0.4      20%       18%       -2%
0.4 - 0.6      30%       28%       -2%
0.6 - 0.8      25%       27%       +2%
0.8 - 1.0      10%       15%       +5%

v3 is more confident (shifted toward higher scores)
KS test p-value: 0.002 (significantly different distributions)
```

---

## 4. Rollback Procedures

### 4.1 Rollback Triggers

| Trigger | Condition | Response Time |
|---|---|---|
| Error rate spike | > 5% for 5 minutes | Immediate rollback |
| Latency spike | P99 > 500ms for 10 minutes | Immediate rollback |
| CTR drop | > 20% vs. baseline for 1 hour | Automatic rollback |
| Feature completeness drop | < 80% for 5 minutes | Rollback or feature fallback |
| Prediction collapse | All scores near 0.5 | Immediate rollback |
| User complaints | > 10 per minute | Investigate, potentially rollback |

### 4.2 Rollback Procedure

```
Automatic rollback:
1. Alert fires (threshold exceeded for duration)
2. Verify alert is genuine (check 2+ metric sources)
3. Execute rollback:
   a. Update traffic routing to previous version
   b. Update model server configuration
   c. Verify traffic is on previous version
4. Monitor for 15 minutes to confirm recovery
5. Create incident ticket
6. Notify ML team

Manual rollback:
1. Engineer decides rollback is needed
2. Execute rollback command:
   kubectl set env deployment/rec-ranking MODEL_VERSION=previous-version
3. Verify traffic routing updated
4. Monitor metrics for recovery
5. Document rollback reason
```

### 4.3 Rollback Safety

- **Version compatibility**: Ensure previous version is compatible with current features
- **Feature compatibility**: Previous model version must support current feature schema
- **Infrastructure compatibility**: Previous model must work on current infrastructure
- **Rollback window**: Keep previous version available for at least 7 days
- **Rollback testing**: Test rollback procedure in staging before production

---

## 5. Lineage Tracking

### 5.1 End-to-End Lineage

Track the complete lineage from training data to serving:

```
Training Data (dataset-2026.08.10-v2)
  |
  v
Feature Pipeline (features-v4.2)
  |
  v
Training Pipeline (ranking-v3-training-2026.08.15)
  |
  v
Model Artifacts (s3://models/ranking/v3/2026.08.15/)
  |
  v
Model Registry (ranking-v3-2026.08.15-stable)
  |
  v
Deployment Pipeline (ranking-v3-deploy-2026.08.15)
  |
  v
Serving Infrastructure (ranking-service v3.2.1)
  |
  v
User Requests (with prediction logging)
```

### 5.2 Lineage Metadata

Every prediction should carry lineage information:

```json
{
  "prediction_id": "pred-abc123",
  "model_version": "ranking-v3-2026.08.15-stable",
  "feature_pipeline_version": "features-v4.2",
  "feature_schema_version": "schema-v3.1",
  "training_data_version": "dataset-2026.08.10-v2",
  "training_date": "2026-08-15",
  "serving_infrastructure": {
    "instance_type": "g4dn.xlarge",
    "gpu": "T4",
    "framework_runtime": "tensorrt-8.6"
  }
}
```

### 5.3 Lineage Querying

Enable queries like:
- "Which predictions were made by model version X?"
- "Which training data influenced model version Y?"
- "What features were used for predictions in the last hour?"
- "Which model version was serving when incident Z occurred?"

### 5.4 Lineage Storage

| Storage | Purpose | Retention |
|---|---|---|
| Model registry | Version metadata and artifacts | Permanent |
| Prediction logs | Per-prediction lineage | 30-90 days |
| Training logs | Training run metadata | Permanent |
| Deployment logs | Deployment history | 1 year |
| Audit logs | Compliance trail | Per regulation |

---

## 6. Promotion Workflows

### 6.1 Promotion Stages

```
Stage 1: Training Complete
  Criteria: Offline metrics meet threshold
  Gate: Automated validation
  Duration: Immediate

Stage 2: Validation Passed
  Criteria: Offline evaluation on holdout set
  Gate: Automated comparison with baseline
  Duration: 1-4 hours

Stage 3: Staging Deployed
  Criteria: Validation passed
  Gate: Manual review (or automated for routine retraining)
  Duration: 1-24 hours

Stage 4: Canary Deployed
  Criteria: Staging smoke tests pass
  Gate: Automated traffic splitting
  Duration: 4-48 hours

Stage 5: Production
  Criteria: Canary shows improvement or no regression
  Gate: Automated promotion (or manual for major changes)
  Duration: Weeks to months
```

### 6.2 Promotion Gates

```yaml
promotion_gates:
  validation_to_staging:
    - metric: "ndcg@10"
      condition: ">= baseline * 0.98"
    - metric: "inference_latency_p99"
      condition: "<= baseline * 1.2"
    - metric: "model_size"
      condition: "<= baseline * 1.5"

  staging_to_canary:
    - check: "smoke_tests_pass"
    - check: "feature_compatibility_verified"
    - check: "infrastructure_requirements_met"

  canary_to_production:
    - metric: "ctr"
      condition: ">= control * 0.98"
      duration: "4h"
    - metric: "error_rate"
      condition: "<= control * 1.1"
      duration: "4h"
    - metric: "p99_latency"
      condition: "<= 200ms"
      duration: "4h"
```

### 6.3 Promotion Monitoring

Track promotion status in real-time:

```
Model: ranking-v3-2026.08.15-stable
Status: Canary (Stage 4)
Started: 2026-08-15T14:00:00Z
Traffic: 10% treatment, 90% control
Duration so far: 6 hours

Metrics (treatment vs. control):
  CTR: 3.38% vs 3.21% (+5.3%) [PASS]
  Conversion: 1.79% vs 1.82% (-1.6%) [PASS]
  Error rate: 0.14% vs 0.12% (+16.7%) [MONITOR]
  P99 latency: 162ms vs 145ms (+11.7%) [MONITOR]

Next gate: Increase to 25% traffic
Required: 2 more hours of stable metrics
```

---

## 7. Shadow Mode Testing

### 7.1 What is Shadow Mode?

Shadow mode runs a new model alongside the production model, comparing predictions without affecting users:

```
User Request
    |
    v
Production Model (v2) -> Returns response to user
    |
    v
Shadow Model (v3) -> Logs predictions (not served to user)
    |
    v
Comparison Engine -> Compares v2 and v3 predictions
```

### 7.2 Shadow Mode Benefits

- **Zero user risk**: Shadow predictions don't affect users
- **Real traffic testing**: Uses actual production traffic patterns
- **Feature validation**: Verifies feature pipeline compatibility
- **Performance benchmarking**: Measures latency and throughput under real load
- **Prediction comparison**: Identifies systematic differences between models

### 7.3 Shadow Mode Metrics

```promql
# Shadow model prediction comparison
rec_shadow_model_prediction_agreement{model="ranking-v3-shadow"} gauge  # 0-1
rec_shadow_model_latency_ms{model="ranking-v3-shadow"} histogram
rec_shadow_model_error_rate{model="ranking-v3-shadow"} gauge
rec_shadow_model_feature_completeness{model="ranking-v3-shadow"} gauge
rec_shadow_model_score_distribution{model="ranking-v3-shadow"} histogram
```

### 7.4 Shadow Mode Decision Framework

```
After 7 days of shadow mode:
  Agreement rate > 90% AND no systematic bias -> Proceed to A/B test
  Agreement rate > 90% BUT systematic bias -> Investigate bias before A/B
  Agreement rate 70-90% -> Investigate differences, may need retraining
  Agreement rate < 70% -> Major model change, requires thorough evaluation
  Shadow errors > 5% -> Fix model before proceeding
  Shadow latency > 2x production -> Optimize before proceeding
```

---

## 8. Key Takeaways

1. **Version every model component** — weights, features, data, configuration, and environment
2. **Use clear version naming** — date-based versions with variant suffixes
3. **Implement comparison tools** — offline metrics, A/B tests, and prediction distribution analysis
4. **Automate rollback triggers** — protect users from degraded model performance
5. **Track end-to-end lineage** — from training data to serving predictions
6. **Use promotion gates** — staged deployment with automated and manual checkpoints
7. **Test in shadow mode** — zero-risk validation with real traffic
8. **Maintain version history** — keep previous versions available for rollback
9. **Document version decisions** — track why each promotion or rollback was made
10. **Audit model lineage** — regulatory compliance requires traceable model provenance
