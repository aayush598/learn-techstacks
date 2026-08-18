# A/B Testing Framework for Recommendations

## Overview

A/B testing (controlled experimentation) is the gold standard for evaluating recommendation system changes in production. It provides statistically rigorous evidence of whether a proposed change improves or degrades user experience and business metrics. This document covers experiment design, traffic allocation, statistical analysis, multi-armed bandit experiments, and guardrail metrics for recommendation systems.

---

## Experiment Design

### Anatomy of a Recommendation A/B Test

```
┌─────────────────────────────────────────┐
│            Experiment Design             │
├─────────────────────────────────────────┤
│ Hypothesis: New ranking model increases  │
│             CTR by ≥ 2% relative         │
│                                          │
│ Treatment: DeepFM with content features  │
│ Control: Matrix Factorization baseline   │
│                                          │
│ Primary metric: CTR (click-through rate) │
│ Secondary metrics: Conversion, revenue   │
│ Guardrail metrics: Latency, error rate   │
│                                          │
│ Traffic split: 50/50                     │
│ Duration: 2 weeks                        │
│ Unit of randomization: User              │
└─────────────────────────────────────────┘
```

### Experiment Types

| Type | Description | Use Case |
|------|-------------|----------|
| Feature test | Test a specific feature change | New ranking algorithm |
| Algorithm test | Compare two complete algorithms | CF vs hybrid model |
| UI/Layout test | Test recommendation presentation | Card design, number of slots |
| Policy test | Test business rules | Diversity requirements |
| Personalization test | Test personalization level | Segment-specific models |

### Hypothesis Formulation

| Component | Example |
|-----------|---------|
| Null hypothesis (H₀) | New model has no effect on CTR (Δ = 0) |
| Alternative hypothesis (H₁) | New model increases CTR by ≥ 1% relative |
| Minimum detectable effect (MDE) | 1% relative improvement |
| Significance level (α) | 0.05 (5% false positive rate) |
| Power (1-β) | 0.80 (80% chance of detecting true effect) |

### Sample Size Calculation

```
For binary metric (CTR):
  n = (Z_{α/2} + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₁ - p₂)²

Where:
  p₁ = baseline CTR (e.g., 0.05)
  p₂ = expected CTR (e.g., 0.051 for 2% relative lift)
  Z_{α/2} = 1.96 (for α = 0.05)
  Z_β = 0.84 (for power = 0.80)

Example:
  n = (1.96 + 0.84)² × (0.05×0.95 + 0.051×0.949) / (0.05 - 0.051)²
  n ≈ 1,836,000 per variant

With 10% daily users: ~184 days needed (too long!)
Solution: Increase MDE or reduce α, or use sequential testing
```

---

## Traffic Allocation

### Randomization Unit

| Unit | Description | Pros | Cons |
|------|-------------|------|------|
| User ID | Each user in one variant | Clean analysis | User sees one experience |
| Device ID | Each device in one variant | Multi-device users | Cross-device tracking |
| Session | Each session randomized | Tests within user | Intra-user variance |
| Request | Each request randomized | Maximum sample size | Users may see different variants |

**Recommendation:** User-level randomization for most cases (avoids within-user contamination).

### Traffic Splitting Methods

#### Deterministic Hashing

```python
import hashlib

def get_variant(user_id, experiment_id, num_variants=2):
    hash_input = f"{user_id}_{experiment_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    variant = hash_value % num_variants
    return variant  # 0 = control, 1 = treatment
```

**Properties:**
- Consistent: Same user always gets same variant
- Uniform: Equal probability per variant
- Deterministic: No storage needed

#### Feature Flag Integration

```
LaunchDarkly / Optimizely / custom feature flag:
  experiment_id: "ranking_model_v3"
  variants:
    control: { model: "mf_v2", traffic: 50% }
    treatment: { model: "deepfm_v3", traffic: 50% }
  targeting:
    - include: all_users
    - exclude: internal_users, bot_users
```

### Traffic Ramp-up Strategy

```
Phase 1: 1% traffic (1 day) → Verify no errors
Phase 2: 10% traffic (2 days) → Initial metrics check
Phase 3: 50% traffic (1 week) → Statistical significance check
Phase 4: 100% traffic (if winner) → Full rollout
```

| Phase | Duration | Purpose | Risk Level |
|-------|----------|---------|------------|
| Canary | 1-2 days | Catch critical bugs | Very low |
| Early evaluation | 3-5 days | Initial directional signal | Low |
| Full experiment | 1-2 weeks | Statistical significance | Controlled |
| Rollout | 1 week | Confirm online metrics | Monitored |

---

## Metric Collection

### Metric Hierarchy

```
Primary Metrics (Decision-making)
├── CTR (Click-Through Rate)
├── Conversion Rate
├── Revenue per user
└── User engagement (time spent)

Secondary Metrics (Understanding)
├── Recommendation diversity
├── Catalog coverage
├── New item discovery rate
├── Long-tail item exposure
└── User satisfaction (surveys)

Guardrail Metrics (Protecting)
├── P99 latency
├── Error rate
├── Server cost per request
├── User retention (long-term)
└──投诉率 (complaint rate)
```

### Metric Definitions

| Metric | Formula | Type | Minimum Sample |
|--------|---------|------|----------------|
| CTR | clicks / impressions | Rate | 100K impressions |
| Conversion rate | conversions / impressions | Rate | 50K impressions |
| Revenue per user | total_revenue / users | Continuous | 10K users |
| NDCG@10 | Normalized DCG at rank 10 | Ranking quality | 10K users |
| Diversity | 1 - avg_pairwise_similarity | Continuous | 5K users |
| Coverage | unique_items_recommended / catalog_size | Ratio | 10K users |
| Latency P99 | 99th percentile response time | Performance | Continuous |

### Data Collection Pipeline

```
User Action (click, view, purchase)
      ↓
Event Logger (client-side)
      ↓
Event Stream (Kafka/Kinesis)
      ↓
Real-time Processing (Flink/Spark Streaming)
      ↓
Experiment Metrics Table (per user, per variant, per metric)
      ↓
Analytics Dashboard (Looker/Tableau/custom)
      ↓
Statistical Analysis (Python/R)
```

### Event Schema

```json
{
  "event_id": "uuid",
  "user_id": "u123",
  "experiment_id": "ranking_v3",
  "variant": "treatment",
  "timestamp": "2024-01-15T10:30:00Z",
  "event_type": "impression",
  "item_id": "i456",
  "position": 3,
  "context": {
    "device": "mobile",
    "session_id": "s789",
    "page": "homepage"
  }
}
```

---

## Statistical Analysis

### Frequentist Approach

#### Two-Sample T-Test

```python
from scipy import stats

control_ctr = [0.052, 0.048, 0.051, ...]  # Daily CTR for control
treatment_ctr = [0.054, 0.050, 0.053, ...]  # Daily CTR for treatment

t_stat, p_value = stats.ttest_ind(treatment_ctr, control_ctr)
relative_lift = (np.mean(treatment_ctr) - np.mean(control_ctr)) / np.mean(control_ctr)

print(f"Relative lift: {relative_lift:.2%}")
print(f"P-value: {p_value:.4f}")
print(f"Significant at α=0.05: {p_value < 0.05}")
```

#### Confidence Intervals

```
95% CI for CTR difference = (point_estimate - 1.96 × SE, point_estimate + 1.96 × SE)

Where SE = sqrt(p₁(1-p₁)/n₁ + p₂(1-p₂)/n₂)

Interpretation: We are 95% confident the true CTR difference is within this interval.
```

#### Multiple Testing Correction

When testing multiple metrics simultaneously:

| Method | Description | Conservative Level |
|--------|-------------|-------------------|
| Bonferroni | α/m per test | Very conservative |
| Holm-Bonferroni | Step-down correction | Moderate |
| Benjamini-Hochberg | FDR control | Less conservative |
| No correction | Use raw p-values | Liberal (high false positive) |

### Bayesian Approach

#### Bayesian A/B Testing

```
P(treatment > control | data) = ∫∫ I(θ_t > θ_c) × p(θ_t | data) × p(θ_c | data) dθ_t dθ_c

For CTR (Beta-Binomial model):
  Prior: Beta(1, 1) for both variants
  Posterior: Beta(1 + clicks, 1 + non-clicks)
  P(treatment > control): Monte Carlo sampling from posteriors
```

```python
import numpy as np

# Posterior distributions
control_clicks, control_non_clicks = 5000, 95000
treatment_clicks, treatment_non_clicks = 5200, 94800

# Sample from posteriors
n_samples = 1_000_000
control_samples = np.random.beta(control_clicks + 1, control_non_clicks + 1, n_samples)
treatment_samples = np.random.beta(treatment_clicks + 1, treatment_non_clicks + 1, n_samples)

# Probability that treatment is better
prob_better = np.mean(treatment_samples > control_samples)
print(f"P(treatment > control) = {prob_better:.3f}")

# Expected loss of choosing treatment
expected_loss = np.mean(np.maximum(control_samples - treatment_samples, 0))
print(f"Expected loss = {expected_loss:.5f}")
```

#### Advantages of Bayesian Approach

- Intuitive: "95% probability treatment is better" vs "p < 0.05"
- No multiple testing correction needed
- Can compute expected loss (risk of choosing wrong variant)
- Naturally handles sequential data

---

## Multi-Armed Bandit Experiments

### When to Use Bandits vs Fixed A/B

| Factor | Fixed A/B Test | Bandit Experiment |
|--------|---------------|-------------------|
| Statistical rigor | High (proper hypothesis test) | Lower (continuous adaptation) |
| Exploration efficiency | Low (50% on control) | High (minimal waste) |
| Decision timing | Fixed duration | Adaptive, converges early |
| Multiple variants | Traffic diluted | Proportionally allocated |
| Best for | Proving causation | Optimizing a metric |

### Bandit Configuration

```python
# Thompson Sampling for recommendation variants
import numpy as np

variants = {
    "control_mf": {"clicks": 0, "impressions": 0},
    "treatment_deepfm": {"clicks": 0, "impressions": 0},
    "treatment_transformer": {"clicks": 0, "impressions": 0},
}

def select_variant(variants):
    samples = {}
    for name, stats in variants.items():
        samples[name] = np.random.beta(
            stats["clicks"] + 1,
            stats["impressions"] - stats["clicks"] + 1
        )
    return max(samples, key=samples.get)

def update_variant(variants, name, clicked):
    variants[name]["impressions"] += 1
    if clicked:
        variants[name]["clicks"] += 1
```

---

## Sequential Testing

### Problem with Fixed-Horizon Testing

- Must wait for predetermined sample size
- Cannot peek at results without inflating false positive rate
- Experiments run longer than necessary if effect is large

### Sequential Testing Methods

#### Group Sequential Design

- Pre-define interim analysis points
- Use adjusted significance boundaries (O'Brien-Fleming, Pocock)
- Can stop early for efficacy or futility

| Analysis | Information Fraction | O'Brien-Fleming α | Pocock α |
|----------|---------------------|-------------------|----------|
| 1 | 25% | 0.0001 | 0.016 |
| 2 | 50% | 0.004 | 0.018 |
| 3 | 75% | 0.019 | 0.020 |
| 4 (final) | 100% | 0.043 | 0.022 |

#### Always-Valid P-Values

- Use always-valid confidence sequences
- Can stop at any time and report valid p-value
- Based on mixture martingale or mixture tests

#### Sample Size Re-estimation

- Calculate required sample size at interim analysis
- Adjust based on observed variance
- Can increase power without inflating false positives

---

## Guardrail Metrics

### Purpose

Guardrail metrics ensure that experiment variants don't degrade critical system properties, even if the primary metric improves.

### Common Guardrails

| Guardrail | Threshold | Measurement | Action if Breached |
|-----------|----------|-------------|-------------------|
| P99 Latency | < 50ms | Server-side monitoring | Pause experiment |
| Error Rate | < 0.1% | Error logging | Pause experiment |
| Server Cost | < 10% increase | Infrastructure billing | Investigate |
| User Retention | No degradation | 7-day retention | Pause experiment |
|投诉率 | No increase | Support tickets | Investigate |
| Crash Rate | No increase | Client-side crash reporting | Pause experiment |

### Guardrail Implementation

```python
class ExperimentGuardrails:
    def __init__(self, config):
        self.latency_threshold = config.max_p99_latency
        self.error_threshold = config.max_error_rate
        self.retention_threshold = config.min_retention
    
    def check(self, metrics):
        violations = []
        
        if metrics.p99_latency > self.latency_threshold:
            violations.append(f"Latency: {metrics.p99_latency}ms > {self.latency_threshold}ms")
        
        if metrics.error_rate > self.error_threshold:
            violations.append(f"Error rate: {metrics.error_rate} > {self.error_threshold}")
        
        if metrics.retention_7d < self.retention_threshold:
            violations.append(f"Retention: {metrics.retention_7d} < {self.retention_threshold}")
        
        if violations:
            self.pause_experiment(violations)
        
        return len(violations) == 0
```

---

## Experiment Lifecycle

### Pre-Experiment

1. **Hypothesis review**: Team agrees on hypothesis, metrics, and duration
2. **Sample size estimation**: Ensure sufficient traffic for detection
3. **Implementation review**: Code review for experiment assignment logic
4. **Metrics validation**: Verify metrics pipeline captures all needed data
5. **Guardrail setup**: Configure alerting for guardrail metrics

### During Experiment

1. **Daily monitoring**: Check primary metrics, guardrails, and system health
2. **Week 1 check**: Early directional signal; abort if catastrophic
3. **Midpoint analysis**: Assess progress toward significance
4. **Data quality checks**: Verify randomization, sample ratio, metric computation

### Post-Experiment

1. **Statistical analysis**: Full analysis with confidence intervals
2. **Segment analysis**: Breakdown by user type, device, geography
3. **Long-term effects**: Check if effects persist after initial novelty
4. **Decision documentation**: Record decision, rationale, and follow-up actions
5. **Learnings share**: Present results to broader team

### Documentation Template

```markdown
# Experiment: [Name]

## Hypothesis
[What we expect and why]

## Design
- Control: [Description]
- Treatment: [Description]
- Traffic: [Split %]
- Duration: [Dates]

## Results
- Primary metric: [Result with CI]
- Secondary metrics: [Results]
- Guardrails: [All passed?]

## Decision
[Launch / Iterate / Kill]

## Learnings
[Key insights for future experiments]

## Follow-up
[Next experiments or monitoring plan]
```

---

## Common Pitfalls

| Pitfall | Description | Prevention |
|---------|-------------|------------|
| Peeking | Checking results too early without correction | Use sequential testing |
| Sample ratio mismatch | Unequal traffic despite 50/50 split | Monitor allocation daily |
| Novelty effect | Initial boost from change that fades | Run experiment 2+ weeks |
| Interaction effects | Multiple experiments affecting each other | Use mutual exclusion groups |
| Simpson's paradox | Aggregate shows improvement but segments don't | Always check segments |
| Metric gaming | Improving metric without improving user experience | Use multiple complementary metrics |
| Network effects | Control users affected by treatment users | Cluster randomization |
| Seasonality | Results confounded by time patterns | Run during representative period |
