# User Retention

## Overview

User retention measures whether users return to a platform over time. It is arguably the most important long-term metric for recommendation systems because it captures whether recommendations create sustained value. A recommendation system that drives high click-through but low retention is failing—it is optimizing for short-term engagement at the expense of long-term user satisfaction.

## Day 1/7/30 Retention

### Definition

```
Day-N Retention = |{users active on day N after acquisition}| / |{users acquired on cohort day}|
```

### Standard Retention Windows

| Window | What It Measures | Typical Values |
|--------|-----------------|---------------|
| Day 1 (D1) | Immediate return | 30–60% |
| Day 3 (D3) | Short-term habit | 20–40% |
| Day 7 (D7) | Weekly engagement | 15–30% |
| Day 14 (D14) | Bi-weekly habit | 10–25% |
| Day 30 (D30) | Monthly engagement | 8–20% |
| Day 90 (D90) | Long-term retention | 5–15% |

### Retention Curve

Plot retention rate against days since acquisition. The curve typically:
1. **Drops sharply** in days 1–3 (users who don't find value leave)
2. **Flattens** in days 7–30 (remaining users form habits)
3. **Reaches a floor** after day 30 (long-term retained users)

The shape of this curve reveals the recommendation system's ability to hook users and maintain engagement.

### Retention Curve Interpretation

| Curve Shape | Diagnosis | Recommendation System Implication |
|------------|-----------|----------------------------------|
| Sharp drop, high floor | Strong product for retained users | Focus on improving first-session experience |
| Gradual decline, low floor | Recommendations don't create habits | Improve personalization and discovery |
| Sharp drop, low floor | Fundamental value proposition issue | System may need architectural changes |
| Gradual decline, high floor | Good but not great | Incremental improvements to relevance |

## Retention Cohorts

### Cohort Definition

A cohort is a group of users who share a common attribute within a defined time period:

| Cohort Type | Definition | Example |
|------------|-----------|---------|
| Acquisition date | Users who joined on the same day/week/month | Users acquired in January 2024 |
| Acquisition channel | Users who arrived through the same channel | Organic search users |
| First interaction | Users whose first recommendation interaction was the same item type | Users whose first click was on movies |
| Platform | Users on the same device/OS | iOS users |

### Cohort Retention Table

| Cohort | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
|--------|--------|--------|--------|--------|--------|--------|
| Jan W1 | 100% | 45% | 35% | 30% | 28% | 26% |
| Jan W2 | 100% | 48% | 38% | 32% | 30% | — |
| Feb W1 | 100% | 50% | 40% | 34% | — | — |
| Feb W2 | 100% | 52% | 42% | — | — | — |

### Cohort Analysis Insights
- **Improving cohorts over time**: Recommendation system improvements are working
- **Declining cohorts**: Something is degrading (recommendation quality, catalog, competition)
- **Channel-level differences**: Some acquisition channels bring more retainable users

## Retention Drivers

### Recommendation System Factors

| Driver | Impact on Retention | How to Measure |
|--------|-------------------|----------------|
| **Relevance** | Higher relevance → higher retention | NDCG correlation with retention |
| **Diversity** | More diverse recs → broader appeal | ILD correlation with retention |
| **Novelty** | Fresh recommendations → continued interest | Novelty score correlation with retention |
| **Serendipity** | Unexpected good finds → delight | Serendipity score correlation with retention |
| **Consistency** | Reliable quality → trust | Variance of session metrics over time |
| **Cold-start handling** | Good new-user experience → early retention | D1/D7 retention for new users |

### Product Factors Affecting Retention

| Factor | Description |
|--------|------------|
| Core product value | The recommendation system amplifies, not replaces, core product value |
| UX quality | Easy navigation, fast loading, intuitive interface |
| Content quality | The catalog itself must be valuable |
| Social features | Network effects can boost retention |
| Notification strategy | Well-timed reminders vs. spam |

## Recommendation Impact on Retention

### Measuring Impact

#### A/B Test Approach
- **Treatment**: Users receiving personalized recommendations
- **Control**: Users receiving non-personalized recommendations (e.g., popular items)
- **Metric**: Day-7 and Day-30 retention difference

#### Retention Attribution

```
Retention_Lift = (RetTreatment - RetControl) / RetControl × 100%
```

Typical retention lifts from good recommendation systems:
- **Small improvement**: 1–3% relative lift
- **Moderate improvement**: 3–8% relative lift
- **Large improvement**: 8–15% relative lift
- **Transformative**: >15% relative lift (rare; usually involves fundamental product changes)

### Retention by Recommendation Engagement Level

| Engagement Level | Definition | D30 Retention |
|-----------------|-----------|---------------|
| Heavy rec users | >50% of interactions from recommendations | 25–40% |
| Moderate rec users | 20–50% of interactions from recommendations | 15–25% |
| Light rec users | <20% of interactions from recommendations | 10–15% |
| No rec interaction | 0 interactions with recommendations | 5–10% |

This analysis reveals the causal impact of recommendation engagement on retention (observational, not experimental).

## Retention vs Engagement

### Key Distinction

| Metric | Time Horizon | What It Measures | Gaming Risk |
|--------|-------------|-----------------|-------------|
| **Engagement** | Short-term | Clicks, views, time spent | High (clickbait works) |
| **Retention** | Long-term | Return visits over weeks/months | Low (hard to fake sustained value) |

### The Engagement-Retention Paradox

A recommendation system can maximize short-term engagement by:
- Showing controversial or emotionally charged content (high CTR, low retention)
- Creating addictive patterns (high time spent, potential negative sentiment)
- Optimizing for clicks over satisfaction (high engagement, low conversion)

The best recommendation systems optimize for retention, accepting some short-term engagement loss.

### Retention-Respecting Engagement Metrics

| Metric | Formula | Why It's Better |
|--------|---------|----------------|
| Satisfied engagement | Engagements where user rates item ≥4/5 | Measures quality, not just quantity |
| Completion rate | Content fully consumed / content started | Measures true engagement |
| Positive exit rate | Sessions ending with positive action / total sessions | Measures satisfaction at session end |
| Return engagement | Engagements by returning users / total engagements | Filters for retained users |

## Retention Forecasting

### Early Retention as Predictor

Research shows strong correlation between early and late retention:

```
D30_Retention ≈ f(D1_Retention, D3_Retention, D7_Retention)
```

### Retention Prediction Models

| Model | Approach | Accuracy |
|-------|---------|----------|
| Logistic regression on early signals | D1, D3, D7 features → D30 prediction | Moderate |
| Survival analysis | Time-to-churn modeling with Cox PH | Good |
| Deep learning | Sequential interaction patterns → churn probability | Best |
| Markov chains | State transitions between engagement levels | Good, interpretable |

### Retention Forecasting for Recommendation Impact

When deploying a new recommendation model:
1. **Predict D7 retention** using D1 signals from the A/B test
2. **Extrapolate D30** using the retention curve shape
3. **Estimate LTV impact** by integrating predicted retention over the user lifetime

### Retention Dashboard Metrics

| Metric | Frequency | Alert Threshold |
|--------|----------|----------------|
| D1 retention | Daily | Drop > 2% from 7-day average |
| D7 retention | Weekly | Drop > 3% from 4-week average |
| D30 retention | Monthly | Drop > 2% from 3-month average |
| Retention curve slope | Weekly | Steepening slope (faster churn) |
| Retention by cohort | Weekly | Cohort regression over time |
| Retention by segment | Bi-weekly | Segment-specific degradation |

## Common Pitfalls

1. **Confusing activation with retention**: A user completing onboarding (activation) is not the same as returning a week later (retention)
2. **Ignoring churned-user retention**: Some "retained" users may have churned and returned; distinguish sustained retention from resurrected retention
3. **Survivorship bias**: Only analyzing retention for users who completed onboarding excludes those who dropped off during onboarding
4. **Platform differences**: Mobile and desktop retention curves are fundamentally different; never aggregate them
5. **Seasonal effects**: Holiday periods inflate retention; always compare year-over-year
