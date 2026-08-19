# Statistical Significance for A/B Testing

## Overview

Statistical significance determines whether observed differences between experiment variants are real effects or due to random chance. Proper statistical methodology prevents false conclusions and ensures experiment decisions are reliable. This covers p-values, confidence intervals, multiple testing correction, and common pitfalls.

---

## P-Values

### Definition

The p-value is the probability of observing a difference at least as extreme as the measured difference, assuming there is no true difference (null hypothesis).

### Interpretation

| P-Value | Interpretation | Action |
|---------|---------------|--------|
| p < 0.01 | Very strong evidence against null | Deploy variant |
| 0.01 ≤ p < 0.05 | Strong evidence against null | Deploy with monitoring |
| 0.05 ≤ p < 0.10 | Weak evidence against null | Continue experiment |
| p ≥ 0.10 | No evidence against null | Likely no real difference |

### Common Mistakes with P-Values

- **p = 0.04 does NOT mean 96% chance variant is better** (common misconception)
- P-values depend on sample size; large samples can make tiny differences significant
- P-values don't measure effect size or practical significance
- Always report effect size alongside p-value

### Computing P-Value for Recommendation Metrics

**For continuous metrics (NDCG, AUC)**:
- Use two-sample t-test or Mann-Whitney U test
- Compute test statistic from variant means and variances
- Two-sided test (we don't assume direction beforehand)

**For ratio metrics (CTR, conversion rate)**:
- Use two-proportion z-test
- Compute pooled standard error
- Apply continuity correction for small samples

---

## Confidence Intervals

### Construction

A 95% confidence interval means: if we repeated the experiment 100 times, 95 of those intervals would contain the true effect.

```
CI = point_estimate ± critical_value × standard_error
```

### Interpretation for Recommendation Experiments

| CI Width | Interpretation | Action |
|----------|---------------|--------|
| Narrow, excludes 0 | Strong, precise effect | Deploy with confidence |
| Wide, excludes 0 | Real effect, but imprecise size | Deploy, monitor effect size |
| Includes 0 | Inconclusive | Continue experiment or increase sample |
| Narrow, near 0 | Precisely measured small/no effect | Stop experiment |

### Effect Size Metrics

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| Cohen's d | (mean_A - mean_B) / pooled_std | 0.2=small, 0.5=medium, 0.8=large |
| Relative lift | (metric_B - metric_A) / metric_A | % improvement |
| Absolute difference | metric_B - metric_A | Raw difference |

### Reporting Standards

Always report:
- Point estimate of effect size
- 95% confidence interval
- Sample size per variant
- Duration of experiment
- Whether result is practically significant (not just statistically significant)

---

## Multiple Testing Correction

### The Problem

Running multiple experiments or checking multiple metrics inflates false positive rate:

| Tests Run | False Positive Rate (without correction) |
|-----------|----------------------------------------|
| 1 | 5% |
| 5 | 23% |
| 10 | 40% |
| 20 | 64% |

### Correction Methods

**Bonferroni Correction**:
- Divide significance threshold by number of tests: α' = α / m
- Very conservative; may miss real effects
- Best when: few tests, strong control needed

**Holm-Bonferroni (Step-Down)**:
- Less conservative than Bonferroni
- Sort p-values, compare each to adjusted threshold
- Stop when first non-significant p-value is found

**Benjamini-Hochberg (FDR)**:
- Controls false discovery rate (not false positive rate)
- More powerful than Bonferroni
- Best when: many tests, acceptable to have some false discoveries
- FDR target: typically 5-10%

### Recommendation for Practice

- Use Benjamini-Hochberg for multiple metrics within one experiment
- Use Bonferroni for independent experiments running simultaneously
- Pre-specify primary metric (no correction needed for primary)
- Apply correction only for secondary/exploratory metrics

---

## Sequential Testing

### Problem with Fixed-Horizon Testing

Traditional A/B testing requires fixed sample size before analyzing results. peeking at results before reaching the sample size inflates false positive rate.

### Sequential Testing Methods

**Always-Valid Confidence Intervals**:
- Use confidence intervals that remain valid at any point in time
- Based on mixture-based likelihood ratios
- Can peek at results anytime without inflating error rate

**Group Sequential Testing**:
- Pre-specify interim analysis points (e.g., after 25%, 50%, 75%, 100% of data)
- Use adjusted significance thresholds at each look
- Stop early if result is clearly significant or futile

**Bayesian Sequential Testing**:
- Compute posterior probability of variant being better
- Stop when posterior exceeds threshold (e.g., 95% probability variant is better)
- Natural interpretation: "95% chance variant B is better than A"

### Benefits for Recommendation Systems

- Faster iteration: stop experiments early when results are clear
- Resource savings: don't waste traffic on clearly losing variants
- Better user experience: deploy winning variants sooner
- Reduced experiment backlog

---

## Sample Size Estimation

### Formula for Continuous Metrics

```
n = (Z_α/2 + Z_β)² × 2σ² / δ²
```

Where:
- α = significance level (typically 0.05)
- β = power (typically 0.8, so Z_β = 0.84)
- σ = standard deviation of metric
- δ = minimum detectable effect (smallest difference you care about)

### Sample Size for Recommendation Metrics

| Metric | Typical σ | MDE | Samples Needed (per variant) |
|--------|----------|-----|---------------------------|
| CTR | 0.05 | 1% relative | ~50,000 |
| Conversion rate | 0.02 | 2% relative | ~200,000 |
| NDCG@10 | 0.15 | 1% relative | ~400,000 |
| Session duration | 300s | 2% relative | ~150,000 |

### Estimating Variance

- Use variance from previous experiments on same metric
- If no history, run a 1-week A/A test to measure natural variance
- Conservative estimate: use larger variance (requires more samples)

### Power Analysis

- 80% power: standard (80% chance of detecting real effect)
- 90% power: high-stakes experiments (fewer false negatives)
- 50% power: screening experiments (accept high miss rate)

---

## Common Pitfalls

### Peeking Problem

- Checking results before reaching target sample size
- Inflates false positive rate (can reach 30%+ with frequent peeking)
- Solution: use sequential testing methods or wait for target sample size

### Simpson's Paradox

- Overall result contradicts segment-level results
- Example: variant appears better overall, but worse in every user segment
- Cause: uneven traffic distribution across segments
- Solution: ensure balanced randomization, analyze by segment

### Novelty Effect

- Users click new variant because it's different, not because it's better
- Effect diminishes over time (typically 1-2 weeks)
- Solution: run experiment long enough for novelty to wear off

### Selection Bias

- Experiment only captures users who were active during test period
- May miss effects on users who become active after experiment
- Solution: define analysis population before starting experiment

### Ignoring Multiple Metrics

- Optimizing one metric may degrade another
- Example: CTR improves but conversion rate drops
- Solution: define guardrail metrics that must not degrade

### Sample Ratio Mismatch (SRM)

- Actual traffic split differs from intended split
- Indicates bug in randomization or data pipeline
- Solution: always check SRM before analyzing results; chi-squared test

---

## Decision Framework

### Before Experiment

1. Define hypothesis and primary metric
2. Calculate required sample size
3. Pre-register analysis plan
4. Verify no existing experiments conflict

### During Experiment

1. Monitor for SRM (sample ratio mismatch)
2. Check for data quality issues
3. Monitor guardrail metrics
4. Use sequential testing for early stopping if applicable

### After Experiment

1. Verify SRM is acceptable
2. Analyze primary metric with appropriate test
3. Apply multiple testing correction if needed
4. Compute confidence intervals and effect sizes
5. Analyze segments for heterogeneous effects
6. Make deployment decision based on statistical + practical significance
