# Click-Through Rate and Online Metrics

## Overview

Online metrics are the ultimate arbiter of recommendation system quality. While offline metrics (precision, recall, NDCG) provide useful signals during development, online metrics capture real user behavior in response to live recommendations. Click-through rate (CTR) is the most widely used online metric, but a comprehensive evaluation framework requires multiple complementary metrics.

## Click-Through Rate (CTR)

### Definition and Calculation

```
CTR = (Number of clicks on recommendations) / (Number of recommendation impressions)
```

- Range: [0, 1] or expressed as a percentage.
- A single impression is one recommendation shown to one user.
- A click is any user interaction that navigates to the recommended item.

### CTR Variants

**Gross CTR**: Includes all clicks, even accidental or unintended clicks.

**Unique CTR**: Counts only one click per user per recommendation session.

**Qualified CTR**: Excludes clicks with very short dwell time (< 3 seconds) as likely accidental.

**CTR by Position**: Measures CTR separately for each position in the recommendation list.

| Position | Impressions | Clicks | Position CTR |
|----------|------------|--------|-------------|
| 1 | 100,000 | 5,000 | 5.0% |
| 2 | 100,000 | 3,500 | 3.5% |
| 3 | 100,000 | 2,500 | 2.5% |
| 5 | 100,000 | 1,500 | 1.5% |
| 10 | 100,000 | 800 | 0.8% |

### CTR Interpretation

- A higher CTR does not always mean better recommendations (clickbait problem).
- CTR should be interpreted alongside engagement and satisfaction metrics.
- Compare CTR against a baseline (previous model, non-personalized, or random).
- Segment CTR by user type, content type, and traffic source for actionable insights.

## Conversion Rate

### Definition

```
Conversion Rate = (Number of conversions) / (Number of recommendation impressions)
```

A conversion is a valuable user action beyond a click (purchase, sign-up, content creation, subscription).

### Conversion Funnel

```
Impression → Click → Engagement → Conversion → Retention
  100%        5%       2%          1%          0.5%
```

### Micro-Conversion vs Macro-Conversion

| Type | Examples | Measurement Window |
|------|----------|-------------------|
| Micro-conversion | Add to cart, watch video, read article | Session-level |
| Macro-conversion | Purchase, subscription, account creation | Days to weeks |
| Soft conversion | Newsletter signup, profile completion | Session-level |

### Conversion Attribution

- **Last-click attribution**: Conversion attributed to the last recommendation clicked.
- **First-click attribution**: Conversion attributed to the first recommendation clicked.
- **Linear attribution**: Conversion split equally across all clicked recommendations.
- **Time-decay attribution**: More credit to recommendations closer in time to conversion.
- **Algorithmic attribution**: Data-driven model that assigns credit based on contribution.

## Session Metrics

### Session Duration

- Total time a user spends in a session after interacting with a recommendation.
- Longer sessions may indicate higher engagement but can also indicate confusion.
- Correlate with content consumption metrics for meaningful interpretation.

### Session Depth

- Number of items a user views in a single session.
- Higher depth suggests recommendations are successfully guiding discovery.
- Track depth distribution, not just average.

### Bounce Rate

```
Bounce Rate = (Sessions with only one page view) / (Total sessions)
```

- High bounce rate from recommendation pages suggests poor relevance.
- Low bounce rate suggests recommendations are engaging users to explore further.

### Pages Per Session

- Average number of recommended items viewed per session.
- Correlated with recommendation diversity and exploration quality.

## User Retention

### Definition

```
Day-N Retention = (Users active on day N after first visit) / (Users active on first visit)
```

### Retention Metrics

| Metric | Calculation | Timeframe |
|--------|------------|-----------|
| Day-1 Retention | Return within 24 hours | Daily |
| Day-7 Retention | Return within 7 days | Weekly |
| Day-30 Retention | Return within 30 days | Monthly |
| Cohort Retention | Retention by signup cohort | Ongoing |

### Retention and Recommendations

- Better recommendations should improve retention by providing consistent value.
- Retention is a lagging metric — changes take weeks to manifest.
- Use cohort analysis to isolate the impact of recommendation changes.
- Compare retention between users who interact with recommendations vs. those who do not.

## Revenue Per User

### ARPU (Average Revenue Per User)

```
ARPU = Total Revenue / Number of Active Users
```

### Revenue Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| ARPU | Revenue / Active Users | Overall monetization health |
| ARPPU | Revenue / Paying Users | Paying user value |
| LTV | ARPU × Average Lifetime | Long-term user value |
| Revenue per Session | Revenue / Sessions | Session monetization |
| Revenue per Click | Revenue / Clicks | Recommendation monetization efficiency |

### Recommendation Impact on Revenue

- Track revenue attribution to specific recommendation surfaces.
- Measure incremental revenue from personalized vs. non-personalized recommendations.
- Use A/B testing to isolate the revenue impact of recommendation changes.
- Monitor revenue cannibalization (one recommendation surface cannibalizing another).

## Statistical Significance in Online Tests

### A/B Testing Framework

**Hypothesis Formulation**

- Null hypothesis (H₀): The new model has no effect on the metric compared to the baseline.
- Alternative hypothesis (H₁): The new model has a statistically significant effect.
- Significance level (α): Typically 0.05 (5% chance of false positive).
- Power (1-β): Typically 0.80 (80% chance of detecting a real effect).

**Sample Size Calculation**

- Required sample size depends on: effect size, significance level, power, and baseline variance.
- For CTR with baseline 5% and desired minimum detectable effect of 0.5%:
  - Required sample size per group: ~15,000-20,000 users.
  - At 100,000 daily active users, this requires 1-2 days of traffic.
- Use pre-experiment power analysis to determine test duration.

**Statistical Tests**

| Test | Use Case | Assumptions |
|------|----------|-------------|
| Z-test for proportions | CTR comparison | Large sample, independent |
| Chi-squared test | Categorical outcomes | Expected counts > 5 |
| t-test (Welch) | Continuous metrics (revenue, duration) | Approximately normal |
| Mann-Whitney U | Non-normal continuous metrics | No distribution assumption |
| Bayesian testing | When prior information exists | Well-specified prior |

**Common Pitfalls**

- **Peeking problem**: Checking results before reaching target sample size inflates false positive rate.
- **Multiple comparisons**: Testing many variants requires Bonferroni or FDR correction.
- **Simpson's paradox**: Aggregated results can contradict segmented results.
- **Novelty effect**: Users may behave differently with new features initially.
- **Day-of-week effects**: Comparing different time periods introduces confounds.

### Sequential Testing

- Allows early stopping for efficacy or futility without inflating error rates.
- Use group sequential methods (O'Brien-Fleming, Pocock boundaries) or always-valid methods (e-values).
- Pre-define interim analysis schedule and stopping rules.
- Recommended for fast-moving recommendation systems.

## Novelty Effects

### Definition

Novelty effects are temporary changes in user behavior caused by the novelty of a new recommendation algorithm rather than genuine improvement.

### Detection Strategies

- Monitor metric trends over time (novelty effects decay over 2-4 weeks).
- Segment analysis: compare new users (no novelty) vs. existing users (may show novelty).
- Holdback groups: maintain a small control group that never sees the new model.
- Instrument novelty detection by tracking per-user exposure count.

### Mitigation Strategies

- Run A/B tests for at least 2-4 weeks to allow novelty effects to dissipate.
- Use ramp-up periods where the new model is gradually introduced.
- Analyze results excluding the first 3-7 days of user exposure.
- Compare new user behavior (unaffected by novelty) with returning user behavior.

## Long-Term vs Short-Term Metrics

### Short-Term Metrics (Hours to Days)

- CTR, conversion rate, session depth, bounce rate.
- Respond quickly to model changes.
- Subject to noise and novelty effects.
- Useful for quick iteration and detecting regressions.

### Medium-Term Metrics (Weeks to Months)

- User retention (Day-7, Day-30), repeat purchase rate.
- More stable than short-term metrics.
- Better indicators of sustained recommendation quality.
- Require longer test durations and larger sample sizes.

### Long-Term Metrics (Months to Years)

- Customer lifetime value (LTV), brand loyalty, market share.
- Most important for business impact but hardest to measure.
- Require careful cohort analysis and causal inference techniques.
- Often measured through proxy metrics (retention as a proxy for LTV).

### Metric Selection Framework

| Decision Speed | Metric Type | Examples | Test Duration |
|----------------|------------|----------|---------------|
| Fast (days) | Short-term | CTR, conversion | 3-7 days |
| Medium (weeks) | Medium-term | Retention, engagement | 2-4 weeks |
| Slow (months) | Long-term | LTV, satisfaction | 1-3 months |

### Balancing Short and Long Term

- Short-term metrics are leading indicators; long-term metrics are lagging indicators.
- A model that increases CTR but decreases retention is failing long-term.
- Establish guardrail metrics: short-term gains must not trigger long-term metric degradation.
- Use a composite score that weights short-term and long-term metrics appropriately.

## Online Metric Dashboards

### Key Metrics to Monitor

| Category | Metric | Alert Threshold |
|----------|--------|----------------|
| Engagement | CTR | Drop > 10% from baseline |
| Engagement | Session Duration | Drop > 15% from baseline |
| Conversion | Conversion Rate | Drop > 5% from baseline |
| Revenue | ARPU | Drop > 5% from baseline |
| Quality | P99 Latency | Increase > 50% from baseline |
| Quality | Error Rate | Increase > 0.1% absolute |
| Health | Coverage | Drop > 20% from baseline |

### Dashboard Design Principles

- Show trends over time, not just current values.
- Include baseline comparison (previous model, non-personalized control).
- Segment by user type, content category, and traffic source.
- Display statistical confidence alongside metric values.
- Enable drill-down from aggregate to segment-level metrics.
