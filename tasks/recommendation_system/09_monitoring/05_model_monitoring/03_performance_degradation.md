# Performance Degradation Monitoring for Recommendation Systems

## 1. Overview

Performance degradation monitoring tracks the gradual decline in model quality over time. Unlike data drift (which monitors input distributions), performance degradation monitoring measures whether the model's predictions are still achieving business goals. In recommendation systems, performance degradation is insidious — it happens slowly, often goes unnoticed for weeks, and directly impacts revenue and engagement.

### 1.1 Why Performance Degradation Happens

| Cause | Mechanism | Detection Difficulty |
|---|---|---|
| Data drift | Input distributions change | Medium (statistical tests) |
| Concept drift | Relationship between features and labels changes | Hard (requires ground truth) |
| Model staleness | Model trained on outdated data | Easy (age-based monitoring) |
| Feature staleness | Features not updated recently | Easy (freshness monitoring) |
| External factors | User preferences, market conditions | Very hard (requires causal analysis) |
| Feedback loops | Model recommendations influence future data | Very hard (requires counterfactual analysis) |

### 1.2 Performance Degradation Timeline

```
Week 1-2:  Model performs at baseline level
Week 3-4:  Subtle degradation begins (not yet statistically significant)
Week 5-6:  Degradation becomes noticeable (still within normal variance)
Week 7-8:  Degradation crosses alert threshold
Week 9-10: Significant impact on business metrics
Week 11+:  Model significantly underperforms, requires retraining

Goal: Detect degradation at Week 3-4, not Week 7-8
```

---

## 2. Prediction Quality Monitoring

### 2.1 Online Quality Metrics

Since ground truth is delayed in recommendation systems, use proxy metrics:

| Metric | Definition | Update Frequency |
|---|---|---|
| Prediction score distribution | Distribution of model output scores | Real-time |
| Confidence calibration | Predicted probability vs. observed frequency | Daily |
| Ranking quality (online NDCG) | Relevance of top-K recommendations | Daily (with delayed labels) |
| Click-through rate by model version | CTR per model version | Real-time |
| Feature completeness | Percentage of features available per prediction | Real-time |

### 2.2 Online NDCG Calculation

```
Online NDCG@K = (1/|Q|) * sum relevance(user_i, rec_list_i) / ideal_relevance(user_i)

Where:
- Q: Set of queries with observed outcomes
- relevance: Actual engagement (click, like, purchase) as relevance labels
- rec_list_i: Recommendations shown to user_i
- ideal_relevance: Best possible relevance for user_i
```

### 2.3 Prediction Quality Metrics

```promql
# Prediction score mean over time
rec_prediction_score_mean{model="ranking-v3", window="1h"} gauge

# Prediction score standard deviation
rec_prediction_score_stddev{model="ranking-v3", window="1h"} gauge

# Prediction entropy (uncertainty)
rec_prediction_entropy{model="ranking-v3", window="1h"} gauge

# Score monotonicity (are scores well-ordered by relevance?)
rec_prediction_monotonicity{model="ranking-v3", window="1h"} gauge

# Calibration error (predicted probability vs. observed frequency)
rec_calibration_error{model="ranking-v3", window="24h"} gauge
```

---

## 3. A/B Metric Tracking

### 3.1 A/B Test Framework for Model Comparison

```
Control: Current production model (v2)
Treatment: New model candidate (v3)

Metric targets:
  Primary: CTR lift > 2% (statistically significant)
  Secondary: Conversion rate non-regression (p > 0.05)
  Guardrail: P99 latency < 200ms, error rate < 0.5%

Test duration: Minimum 2 weeks (capture weekly cycles)
Traffic split: 50/50 (or 90/10 for new models)
Statistical power: 80% (minimum detectable effect: 1% CTR lift)
```

### 3.2 A/B Test Metric Dashboard

| Metric | Control (v2) | Treatment (v3) | Delta | p-value | Status |
|---|---|---|---|---|---|
| CTR | 3.21% | 3.38% | +5.3% | 0.003 | Significant |
| Conversion rate | 1.82% | 1.79% | -1.6% | 0.41 | Not significant |
| Avg session duration | 8.2 min | 8.4 min | +2.4% | 0.08 | Marginal |
| P99 latency | 145ms | 162ms | +11.7% | — | Monitor |
| Error rate | 0.12% | 0.14% | +16.7% | 0.32 | Monitor |

### 3.3 Automated A/B Test Monitoring

```yaml
ab_test_alerts:
  - name: "A/B test negative CTR"
    condition: "ab_test_delta{metric='ctr'} < -0.02 for 7d"
    severity: warning
    action: "Investigate, consider stopping test"

  - name: "A/B test guardrail breach"
    condition: "ab_test_guardrail{metric='error_rate'} > 0.01"
    severity: critical
    action: "Stop test, rollback treatment"

  - name: "A/B test sample size sufficient"
    condition: "ab_test_sample_size > required_sample_size AND not_significant"
    severity: info
    action: "Consider stopping test (no significant difference)"
```

---

## 4. Regression Detection

### 4.1 Automated Regression Detection

**Statistical process control (SPC):**

```
For each metric:
  1. Calculate baseline mean and standard deviation (30-day window)
  2. Set control limits:
     - Warning: mean + 2 * stddev
     - Critical: mean + 3 * stddev
  3. Monitor current values against control limits
  4. Alert if values exceed limits for sustained period
```

**CUSUM (Cumulative Sum) detection:**

```
CUSUM_t = max(0, CUSUM_{t-1} + (x_t - mu_0 - k))

Where:
- x_t: Current metric value
- mu_0: Target value (baseline mean)
- k: Allowance (typically 0.5 * stddev)

If CUSUM_t > h (decision threshold):
  Signal regression
```

### 4.2 Regression Detection Metrics

```promql
# Metric comparison with baseline
rec_model_metric{metric="ndcg", window="current"} 
/ rec_model_metric{metric="ndcg", window="baseline_30d"}

# CUSUM statistic
rec_regression_cusum{metric="ctr", model="ranking-v3"} gauge

# Control limit breaches
rec_regression_control_breach{metric="ctr", model="ranking-v3", limit="warning|critical"} gauge
```

### 4.3 Regression Root Cause Analysis

```
When regression detected:
1. Check recent deployments (last 7 days)
   - Model version changes
   - Feature pipeline changes
   - Configuration changes

2. Check feature health
   - Feature freshness
   - Feature completeness
   - Feature distribution drift

3. Check traffic patterns
   - Request volume changes
   - User segment mix changes
   - Geographic distribution changes

4. Check external factors
   - Holidays or events
   - Competitor actions
   - News or viral content

5. Compare affected vs. unaffected segments
   - Is regression uniform across all users?
   - Or specific to certain user groups?
```

---

## 5. Automated Rollback Triggers

### 5.1 Rollback Criteria

| Metric | Threshold | Duration | Action |
|---|---|---|---|
| Error rate | > 5% | 5 minutes | Automatic rollback |
| P99 latency | > 500ms | 10 minutes | Automatic rollback |
| CTR drop | > 20% vs. baseline | 1 hour | Automatic rollback |
| Feature completeness | < 80% | 5 minutes | Fallback to cached features |
| Prediction score collapse | stddev < 0.05 | 15 minutes | Automatic rollback |
| User complaints | > 10 per minute | 5 minutes | Automatic rollback |

### 5.2 Rollback Implementation

```
Automatic rollback flow:
1. Alert fires (threshold exceeded for duration)
2. Verify alert is not false positive (require 2/3 metric sources)
3. Execute rollback:
   a. Shift traffic to previous model version
   b. Update deployment status
   c. Notify ML team
4. Verify rollback:
   a. Confirm traffic is on previous version
   b. Monitor metrics for 15 minutes
   c. Confirm metrics recover
5. Post-rollback:
   a. Create incident ticket
   b. Investigate root cause
   c. Fix issue before re-deploying
```

### 5.3 Rollback Safety

- **Gradual rollback**: Shift 25% of traffic first, verify, then 100%
- **Rollback timeout**: If rollback fails, page on-call engineer
- **Rollback cooldown**: Minimum 1 hour between rollback attempts
- **Rollback audit**: Log all rollback decisions and outcomes
- **Manual override**: Allow manual override of automatic rollback

---

## 6. Degradation Root Cause Analysis

### 6.1 Systematic Analysis Framework

```
Step 1: Quantify degradation
  - Which metrics are degraded?
  - By how much?
  - Since when?

Step 2: Identify affected population
  - All users or specific segments?
  - All content types or specific categories?
  - All regions or specific regions?

Step 3: Check recent changes
  - Deployments (model, feature, infrastructure)
  - Configuration changes
  - Traffic pattern changes

Step 4: Analyze feature health
  - Feature freshness
  - Feature completeness
  - Feature distribution drift

Step 5: Analyze model health
  - Prediction distribution changes
  - Calibration changes
  - Feature importance changes

Step 6: Check external factors
  - Seasonal patterns
  - External events
  - Competitive actions
```

### 6.2 Root Cause Decision Tree

```
Performance degraded?
├── Check data quality
│   ├── Feature staleness? -> Update feature pipeline
│   ├── Feature missing? -> Fix data source
│   └── Feature drift? -> Retrain model
├── Check model health
│   ├── Model staleness? -> Retrain model
│   ├── Concept drift? -> Retrain with recent data
│   └── Model error? -> Debug and fix
├── Check infrastructure
│   ├── Resource exhaustion? -> Scale resources
│   ├── Network issues? -> Fix networking
│   └── Cache issues? -> Fix caching
└── Check external factors
    ├── Seasonal pattern? -> Seasonal adjustment
    ├── External event? -> Monitor and adjust
    └── User behavior change? -> Retrain model
```

---

## 7. Model Staleness Detection

### 7.1 Staleness Definition

A model is stale when it was trained on data that no longer represents current conditions:

```
Staleness score = days_since_training / expected_freshness_days

Where expected_freshness_days varies by domain:
- News/recommendations: 7 days
- E-commerce: 14 days
- Content platforms: 30 days
- Enterprise SaaS: 90 days
```

### 7.2 Staleness Monitoring

```promql
# Model age in days
rec_model_age_days{model="ranking-v3"} gauge

# Model staleness score
rec_model_staleness_score{model="ranking-v3"} gauge  # 0.0 (fresh) to 1.0 (stale)

# Training data freshness
rec_training_data_freshness_days{model="ranking-v3"} gauge

# Last training timestamp
rec_model_last_training_timestamp{model="ranking-v3"} gauge
```

### 7.3 Staleness Thresholds

| Staleness Score | Status | Action |
|---|---|---|
| 0.0 – 0.3 | Fresh | No action needed |
| 0.3 – 0.6 | Aging | Schedule retraining |
| 0.6 – 0.8 | Stale | Prioritize retraining |
| 0.8 – 1.0 | Very stale | Emergency retraining |
| > 1.0 | Expired | Consider rollback to older model |

---

## 8. Performance Degradation Dashboard

### 8.1 Dashboard Panels

**Model Performance Overview:**
- Current model version and age
- NDCG, MAP, recall trends
- Online CTR and conversion trends
- Prediction distribution over time

**Feature Health:**
- Feature freshness heatmap
- Feature completeness trends
- Feature drift scores

**Drift Detection:**
- PSI scores over time
- KS test results
- Prediction distribution changes

**A/B Test Status:**
- Active experiments and results
- Statistical significance indicators
- Guardrail metric status

### 8.2 Alert Integration

```
Dashboard shows:
  Green: Model performing at or above baseline
  Yellow: Model showing early signs of degradation
  Red: Model significantly degraded, action required

Alert firing:
  Warning: Yellow status for > 24 hours
  Critical: Red status for > 1 hour
  Emergency: Automatic rollback triggered
```

---

## 9. Key Takeaways

1. **Monitor prediction quality continuously** — don't wait for business metrics to decline
2. **Implement automated regression detection** — CUSUM and control charts catch drift early
3. **Set automated rollback triggers** — protect users from degraded model performance
4. **Track model staleness** — set maximum age thresholds per domain
5. **Use A/B testing for model validation** — statistical rigor prevents bad deployments
6. **Systematize root cause analysis** — decision trees accelerate debugging
7. **Monitor both feature and model health** — feature degradation causes model degradation
8. **Implement gradual rollback** — shift traffic incrementally to minimize blast radius
9. **Track rollback success rates** — measure how often rollbacks are needed and why
10. **Maintain model version history** — enables rollback and comparison
