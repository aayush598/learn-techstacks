# Statistical Tests

## Overview

Statistical tests determine whether observed differences between recommendation algorithms are real or due to random chance. In recommendation system evaluation, every comparison—model A vs. model B, treatment vs. control—requires statistical validation. Using the wrong test or misinterpreting results leads to deploying models that don't actually improve performance, or abandoning models that do.

## Paired t-Test

### When to Use

Compare the mean performance of two models across multiple evaluation units (users, queries, items) where each unit is evaluated under both models.

### Assumptions

- Differences between paired observations are approximately normally distributed
- Observations are independent across units (but paired within units)
- Continuous metric (NDCG, MAP, precision)

### Formula

```
t = (d̄ - 0) / (s_d / √n)
```

Where:
- d̄ = mean difference between paired observations
- s_d = standard deviation of differences
- n = number of pairs
- Degrees of freedom = n - 1

### Decision Rule

- Compute p-value from t-distribution
- If p < α (typically 0.05), reject H₀ (models are different)
- Report: t(df) = t_value, p = p_value, d = effect_size

### Example

```
Model A NDCG@10: [0.12, 0.15, 0.11, 0.13, 0.14] (per user)
Model B NDCG@10: [0.10, 0.13, 0.10, 0.12, 0.11] (per user)
Differences:     [0.02, 0.02, 0.01, 0.01, 0.03]
Mean diff: 0.018, SD: 0.008, n: 5
t(4) = 0.018 / (0.008 / √5) = 5.03, p = 0.007
```

### Limitations

- Normality assumption may be violated for highly skewed metrics (e.g., precision at K with few relevant items)
- Sensitive to outliers
- Not suitable for non-continuous metrics (binary outcomes)

## Wilcoxon Signed-Rank Test

### When to Use

Non-parametric alternative to the paired t-test. Use when:
- Differences are not normally distributed
- The metric is ordinal rather than continuous
- The sample size is small
- Outliers are present

### Assumptions

- Differences are symmetric around the median
- Observations are paired and independent across pairs
- At least ordinal data

### Procedure

1. Compute differences d_i = score_A(i) - score_B(i) for each pair
2. Remove pairs where d_i = 0
3. Rank the absolute differences |d_i|
4. Compute W+ = sum of ranks where d_i > 0 and W- = sum of ranks where d_i < 0
5. Test statistic: W = min(W+, W-)

### Decision Rule

- For large samples (n > 25): W is approximately normal
- Compute p-value from the W statistic
- If p < α, reject H₀

### Paired t-Test vs Wilcoxon

| Aspect | Paired t-Test | Wilcoxon Signed-Rank |
|--------|--------------|---------------------|
| Distribution assumption | Normal | Symmetric (no distribution specified) |
| Data type | Continuous | Ordinal or continuous |
| Outlier sensitivity | High | Low |
| Power (normal data) | Higher | Slightly lower |
| Power (non-normal data) | Lower | Higher |
| Interpretability | Mean difference | Median difference |

## McNemar's Test

### When to Use

Compare two classifiers (or recommendation strategies) on binary outcomes. In recommendations, this applies to:
- Click vs. no-click at the item level
- Conversion vs. no-conversion at the session level
- Relevant vs. not-relevant at the item level

### Contingency Table

|  | Model B Correct | Model B Wrong |
|--|----------------|--------------|
| **Model A Correct** | a | b |
| **Model A Wrong** | c | d |

### Formula

```
χ² = (b - c)² / (b + c)
```

### Decision Rule

- χ² with 1 degree of freedom
- If χ² > 3.84 (for α = 0.05), reject H₀
- For small cell counts (< 25), use McNemar's exact test

### Example

```
          | Model B: Click | Model B: No-Click
Model A: Click     |     500     |       80
Model A: No-Click  |      45     |     475

χ² = (80 - 45)² / (80 + 45) = 35² / 125 = 9.8, p = 0.002
```

Model A has significantly more clicks that Model B misses (80) than vice versa (45).

### Limitations

- Only works for binary outcomes
- Ignores the magnitude of differences
- Not suitable for ranked list comparisons (use permutation tests instead)

## Bootstrap Confidence Intervals

### Concept

Bootstrap resampling estimates the sampling distribution of any statistic by repeatedly resampling with replacement from the observed data.

### Procedure

```
For b = 1 to B (typically B = 1000–10000):
    1. Sample n observations with replacement from the original data
    2. Compute the statistic of interest on the bootstrap sample
    3. Store the bootstrap statistic

Confidence interval = [percentile(α/2), percentile(1-α/2)] of bootstrap distribution
```

### Types of Bootstrap CIs

| Type | Method | Pros | Cons |
|------|--------|------|------|
| **Percentile** | Direct percentiles of bootstrap distribution | Simple | May have poor coverage for small n |
| **BCa (Bias-Corrected and Accelerated)** | Adjusts for bias and skewness | Better coverage | More complex |
| **Studentized** | Bootstrap the standard error | Most accurate | Requires inner bootstrap loop |
| **Pivotal** | Uses bootstrap distribution of statistic | Good coverage | Assumes statistic is pivot |

### Bootstrap for Recommendation Metrics

```
For each bootstrap iteration:
    1. Resample users (not items) to maintain user-level structure
    2. Compute NDCG@10 (or other metric) on the resampled user set
    3. Store the metric value

95% CI = [2.5th percentile, 97.5th percentile]
```

### Why Bootstrap Over Normal Approximation

- Metric distributions are often skewed (especially precision, recall at small K)
- Confidence intervals are valid without distributional assumptions
- Works for any statistic, including non-smooth metrics
- Captures the actual shape of the sampling distribution

## Multiple Testing Correction

### The Problem

When comparing k models or testing k hypotheses, the probability of at least one false positive increases:

```
P(at least one false positive) = 1 - (1 - α)^k
```

For k = 10 tests at α = 0.05: P(at least one false positive) = 1 - 0.95^10 = 0.40

### Bonferroni Correction

```
α_adj = α / k
```

- **Pros**: Simple, controls family-wise error rate (FWER)
- **Cons**: Very conservative; reduces power for all tests
- **Use when**: Small number of tests (k < 5) and strong control needed

### Holm-Bonferroni (Step-Down) Procedure

```
1. Sort p-values: p_(1) ≤ p_(2) ≤ ... ≤ p_(k)
2. For each i from 1 to k:
   If p_(i) < α / (k - i + 1), reject hypothesis i
   Else, stop (all remaining hypotheses are not rejected)
```

- **Pros**: Less conservative than Bonferroni, same FWER control
- **Cons**: Still conservative for large k
- **Use when**: Moderate number of tests (k = 5–20)

### Benjamini-Hochberg (FDR Control)

```
1. Sort p-values: p_(1) ≤ p_(2) ≤ ... ≤ p_(k)
2. Find largest i such that p_(i) ≤ (i/k) × α
3. Reject all hypotheses 1, 2, ..., i
```

- **Pros**: More powerful; controls false discovery rate (FDR) instead of FWER
- **Cons**: May allow more false positives
- **Use when**: Large number of tests (k > 20) and false discoveries are tolerable

### Comparison

| Method | Error Rate Controlled | Conservatism | Power | Use Case |
|--------|----------------------|-------------|-------|----------|
| Bonferroni | FWER | Very conservative | Low | Few critical tests |
| Holm | FWER | Conservative | Moderate | Moderate test count |
| Benjamini-Hochberg | FDR | Moderate | High | Many tests |
| Benjamini-Yekutieli | FDR (dependent tests) | Conservative | Moderate | Correlated tests |

### Recommendation Evaluation Context

| Scenario | Recommended Correction |
|----------|----------------------|
| Comparing 2–3 models | No correction needed (or Bonferroni) |
| Comparing 5–10 models | Holm-Bonferroni |
| Testing across 20+ user segments | Benjamini-Hochberg |
| Multiple metrics + multiple models | Benjamini-Hochberg per metric family |

## Effect Size (Cohen's d)

### Definition

Cohen's d measures the standardized difference between two means:

```
d = (M₁ - M₂) / SD_pooled
```

Where:

```
SD_pooled = √[((n₁-1)×SD₁² + (n₂-1)×SD₂²) / (n₁+n₂-2)]
```

### Interpretation

| Cohen's d | Interpretation |
|-----------|---------------|
| 0.2 | Small effect |
| 0.5 | Medium effect |
| 0.8 | Large effect |
| > 1.0 | Very large effect |

### Why Effect Size Matters

Statistical significance (p-value) depends on sample size:
- With n = 1,000,000, a trivially small difference (d = 0.01) is "statistically significant"
- With n = 10, even a large difference (d = 0.8) may not be significant

Effect size captures the PRACTICAL magnitude of the difference regardless of sample size.

### Effect Size in Recommendations

| Metric | Typical d for meaningful improvement |
|--------|--------------------------------------|
| NDCG@10 | 0.1–0.3 (small to medium) |
| CTR | 0.05–0.2 (very small to small) |
| Conversion rate | 0.1–0.4 (small to medium) |
| Revenue per user | 0.1–0.3 (small to medium) |

### Reporting Effect Size

Always report effect size alongside p-values:

```
Model B outperformed Model A on NDCG@10:
    Mean A = 0.112, Mean B = 0.128
    Cohen's d = 0.25 (small-to-medium effect)
    t(998) = 3.94, p < 0.001
    95% CI for difference: [0.008, 0.024]
```

## Practical Significance vs Statistical Significance

### The Distinction

| Type | Question | Metric |
|------|----------|--------|
| **Statistical significance** | Is the difference likely real? | p-value, confidence interval |
| **Practical significance** | Is the difference meaningful? | Effect size, business impact |

### Decision Framework

```
1. Is the result statistically significant? (p < α)
   No → Cannot conclude difference exists
   Yes → Proceed to step 2

2. Is the effect size meaningful? (d > minimum meaningful effect)
   No → Difference exists but is too small to matter
   Yes → Proceed to step 3

3. Is the improvement worth the cost? (complexity, latency, maintenance)
   No → Keep the simpler model
   Yes → Deploy the new model
```

### Common Mistakes

1. **Ignoring sample size**: Large samples can make trivial differences "significant"
2. **Equating p < 0.05 with "important"**: p-values don't measure importance
3. **Not reporting confidence intervals**: p-values alone don't show the range of plausible effects
4. **Post-hoc hypothesis testing**: Formulating hypotheses after seeing results inflates false positive rate
5. **Ignoring practical costs**: A statistically significant improvement that adds 200ms latency may not be worth deploying
