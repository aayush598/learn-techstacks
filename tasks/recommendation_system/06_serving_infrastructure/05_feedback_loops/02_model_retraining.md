# Model Retraining for Recommendation Systems

## Overview

Model retraining refreshes recommendation models with new data, adapts to changing user preferences, and incorporates feedback from production. A well-designed retraining pipeline balances model freshness with computational cost and stability. This covers trigger-based retraining, incremental vs full retraining, pipeline design, and rollback strategies.

---

## Trigger-Based Retraining

### Retraining Triggers

| Trigger | Condition | Priority | Response Time |
|---------|-----------|----------|---------------|
| Schedule | Daily/weekly cron | Medium | Within batch window |
| Performance degradation | Metric drops below threshold | Critical | < 1 hour |
| Data volume | New data exceeds threshold | Medium | Next batch window |
| Model staleness | Model age exceeds TTL | High | Within SLA |
| External event | New product launch, seasonality | Medium | On-demand |
| Feedback signal | User complaint spike | High | < 4 hours |

### Performance-Based Triggers

**Monitoring Metrics**:
- NDCG@10 drops > 2% from baseline
- CTR drops > 5% week-over-week
- Conversion rate drops > 3% week-over-week
- User engagement time drops > 10%

**Trigger Implementation**:
1. Continuously monitor production metrics
2. Compare against rolling baseline (7-day or 30-day average)
3. Apply statistical test to confirm degradation is real (not noise)
4. If confirmed, trigger retraining pipeline
5. Notify team for manual review if degradation is severe

### Data Volume Triggers

- Retrain after N new interactions accumulated (e.g., 1M new clicks)
- Retrain when data distribution shifts significantly (detected by drift monitors)
- Retrain when new feature sources become available
- Retrain when negative feedback (hides, reports) exceeds threshold

---

## Incremental vs Full Retraining

### Full Retraining

Retrain model from scratch on the complete dataset (historical + new data).

| Aspect | Full Retraining |
|--------|----------------|
| Data usage | All historical data |
| Compute cost | High (full training pipeline) |
| Training time | Hours to days |
| Quality | Highest (sees all data) |
| Stability | High (no drift accumulation) |
| Best for | Weekly/monthly retraining cycles |

### Incremental Retraining

Update existing model with new data only (online learning or fine-tuning).

| Aspect | Incremental Retraining |
|--------|----------------------|
| Data usage | New data since last update |
| Compute cost | Low (delta update) |
| Training time | Minutes to hours |
| Quality | Good (may miss long-term patterns) |
| Stability | Risk of drift accumulation |
| Best for | Hourly/daily updates |

### Hybrid Approach

```
Full retrain (weekly) → baseline model
  ↓
Incremental update (daily) → adapted model
  ↓
Online update (hourly) → fine-tuned model
  ↓
Serving → latest model
```

### Decision Framework

| Factor | Prefer Full | Prefer Incremental |
|--------|------------|-------------------|
| Data distribution | Stable | Rapidly changing |
| Compute budget | Large | Limited |
| Latency requirement | Not urgent | Need freshness |
| Model complexity | Simple enough to retrain | Too expensive to retrain fully |
| Concept drift | Low | High |

---

## Retraining Pipelines

### Pipeline Architecture

```
Data Ingestion → Feature Engineering → Training → Evaluation → Deployment
     ↓                ↓                  ↓           ↓            ↓
  Data Quality    Feature Store      Model Reg    A/B Test    Serving
     Check         Update            Registry     Results     Update
```

### Pipeline Stages

**Stage 1: Data Preparation**
- Ingest new interaction data
- Apply feature transformations
- Update feature store with new features
- Validate data quality (schema, ranges, completeness)

**Stage 2: Training**
- Load previous model checkpoint (for incremental) or initialize (for full)
- Train on prepared data
- Save checkpoints at regular intervals
- Log training metrics to experiment tracker

**Stage 3: Evaluation**
- Evaluate on held-out test set
- Compare against current production model
- Run fairness and bias checks
- Generate evaluation report

**Stage 4: Deployment**
- Register model in model registry
- Promote through staging → production
- Update serving infrastructure
- Monitor post-deployment metrics

### Pipeline Orchestration

- Use workflow orchestrator (Airflow, Prefect, Dagster)
- Define pipeline as DAG with dependencies
- Implement retry logic for transient failures
- Alert on pipeline failures or quality regressions

---

## Rollback on Quality Degradation

### Rollback Triggers

- Production metric drops > 5% from pre-deployment baseline
- User complaints spike related to recommendations
- Fairness metric degrades beyond threshold
- Latency increases beyond SLA
- Model serving errors exceed threshold

### Rollback Process

1. **Detection**: Automated monitoring detects degradation
2. **Confirmation**: Verify degradation is due to model change (not external factor)
3. **Decision**: Auto-rollback for critical issues; manual decision for moderate issues
4. **Execution**: Switch serving to previous model version
5. **Validation**: Verify rollback resolves the issue
6. **Communication**: Notify stakeholders
7. **Investigation**: Root cause analysis
8. **Fix**: Address root cause before next deployment

### Rollback Safety

- Keep previous model version loaded in serving infrastructure
- Test rollback procedure regularly (chaos engineering)
- Maintain compatibility between consecutive model versions
- Monitor both old and new model during gradual rollout
- Document rollback criteria before deployment

### Rollback Prevention

- Extensive pre-deployment testing (offline + online)
- Gradual rollout (canary → 10% → 50% → 100%)
- Monitoring at each rollout stage
- Quick decision criteria defined before rollout
- Automated rollback for critical thresholds

---

## Monitoring Post-Retraining

### Short-Term Monitoring (0-24 hours)

- Real-time metric dashboards
- Latency and error rate monitoring
- User engagement metrics
- A/B test results (if applicable)

### Medium-Term Monitoring (1-7 days)

- Metric trend analysis
- Segment-level performance
- Comparison against pre-retraining baseline
- User feedback and complaints

### Long-Term Monitoring (1-4 weeks)

- Model drift detection
- Feature importance stability
- Fairness metric tracking
- Cost-per-recommendation tracking

### Retraining Quality Gates

| Gate | Metric | Threshold | Action |
|------|--------|-----------|--------|
| Offline quality | NDCG@10 vs baseline | > 99% of baseline | Proceed |
| Fairness | Disparate impact ratio | > 0.8 | Proceed |
| Latency | P99 inference latency | < SLA | Proceed |
| Coverage | Catalog coverage | > 90% | Proceed |
| Online quality | CTR (after 24h) | > 95% of baseline | Full deploy |
