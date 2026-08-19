# Conversion Rate

## Overview

Conversion rate is the percentage of users who complete a desired action after interacting with a recommendation. It is one of the most commercially important online metrics because it directly measures business impact. Unlike click-through rate (which measures interest), conversion rate measures whether recommendations drive meaningful outcomes—purchases, sign-ups, subscriptions, content creation, or any other defined goal.

## Definition

### Basic Conversion Rate

```
Conversion Rate = (Number of Conversions / Number of Exposures) × 100
```

Where:
- **Exposures**: Number of times a recommendation was shown to a user (or number of users who saw it)
- **Conversions**: Number of times the desired action was completed

### Conversion Rate by Recommendation Type

```
CR_recommendation = (Conversions from recommended items) / (Impressions of recommended items)
```

This isolates the conversion impact of recommendations from organic user behavior.

### Time-Windowed Conversion Rate

```
CR(T) = (Conversions within T hours of impression) / (Impressions)
```

The time window T depends on the product:
- **E-commerce**: T = 24–72 hours (users may browse now, purchase later)
- **Media**: T = 1–24 hours (immediate or same-day consumption)
- **SaaS**: T = 7–30 days (longer consideration cycles)

## Attribution Models

Attribution determines how credit for a conversion is distributed across multiple touchpoints (recommendation impressions) in the user's journey.

### First-Click Attribution

```
Credit = 1.0 for the first touchpoint, 0 for all subsequent touchpoints
```

- **Pros**: Credits the recommendation that initiated the user journey
- **Cons**: Ignores all subsequent interactions; over-credits awareness-stage touchpoints
- **Use when**: Understanding which recommendations spark initial interest

### Last-Click Attribution

```
Credit = 0 for all touchpoints except the last, which gets 1.0
```

- **Pros**: Simple, directly ties conversion to the final interaction
- **Cons**: Ignores the contribution of earlier touchpoints; "robs" discovery touchpoints
- **Use when**: Short decision cycles with minimal multi-touch consideration

### Linear Attribution

```
Credit = 1/N for each of N touchpoints in the conversion path
```

- **Pros**: Simple, gives equal credit to all touchpoints
- **Cons**: Treats all touchpoints as equally important regardless of position or influence
- **Use when**: All touchpoints are genuinely equal in importance

### Time-Decay Attribution

```
Credit_i = e^(-λ * (T_convert - T_i)) / Σ e^(-λ * (T_convert - T_j))
```

Where λ is the decay rate and T_i is the time of touchpoint i.

- **Pros**: More credit to recent touchpoints, accounts for temporal relevance
- **Cons**: Requires tuning the decay parameter λ; may over-credit remarketing
- **Use when**: Recent touchpoints are genuinely more influential

### Position-Based Attribution (U-Shaped)

```
Credit = 0.4 for first touchpoint
         0.4 for last touchpoint
         0.2 distributed equally among middle touchpoints
```

- **Pros**: Balances discovery and conversion credit
- **Cons**: Arbitrary 40/40/20 split; may not reflect actual influence
- **Use when**: Both discovery and closing touchpoints matter

### Data-Driven Attribution

Uses machine learning (e.g., Shapley values, Markov chains) to assign credit based on actual conversion patterns:

```
Shapley value for touchpoint i = Σ [|S|!(|N|-|S|-1)!/|N|!] * (v(S ∪ {i}) - v(S))
```

- **Pros**: Learns the actual contribution of each touchpoint from data
- **Cons**: Requires sufficient data; harder to explain; model-dependent
- **Use when**: Large datasets and complex multi-touch journeys

### Attribution Model Comparison

| Model | Complexity | Data Requirements | Best For |
|-------|-----------|------------------|----------|
| First-click | Low | Low | Awareness measurement |
| Last-click | Low | Low | Quick conversion analysis |
| Linear | Low | Low | Equal-touchpoint journeys |
| Time-decay | Medium | Low | Recent-influence-heavy journeys |
| Position-based | Medium | Low | Balanced first/last credit |
| Data-driven | High | High | Complex multi-touch journeys |

## Attribution Windows

The attribution window defines how long after a recommendation impression a conversion can be attributed to that impression.

### Common Window Sizes

| Window | Typical Use | Considerations |
|--------|------------|---------------|
| 24 hours | Mobile apps, media | Short cycle; ignores delayed purchases |
| 7 days | E-commerce | Standard retail window |
| 14 days | Considered purchases | Furniture, electronics |
| 30 days | SaaS, subscriptions | Long evaluation cycles |
| 90 days | High-value B2B | Enterprise sales cycles |

### Window Impact on Metrics
- **Shorter windows**: Lower attributed conversions; less noise; more conservative estimates
- **Longer windows**: Higher attributed conversions; more noise; may include organic conversions
- **Optimal window**: Determined by analyzing the conversion delay distribution

### Conversion Delay Distribution

```
P(attribution | delay = d) = fraction of conversions occurring at delay d
```

Plot the histogram of delays from impression to conversion. The window should capture the vast majority (95%+) of attributable conversions while minimizing false attribution.

## Conversion Funnel Analysis

Recommendation-driven conversions follow a funnel:

```
Impression → View → Click → Engagement → Add to Cart → Checkout → Purchase
```

### Funnel Metrics

| Stage | Metric | Formula |
|-------|--------|---------|
| Impression → View | View Rate | Views / Impressions |
| View → Click | Click-Through Rate | Clicks / Views |
| Click → Engage | Engagement Rate | Engagements / Clicks |
| Engage → Cart | Add-to-Cart Rate | Add-to-Carts / Engagements |
| Cart → Checkout | Checkout Rate | Checkouts / Add-to-Carts |
| Checkout → Purchase | Purchase Rate | Purchases / Checkouts |
| Overall | Conversion Rate | Purchases / Impressions |

### Funnel Drop-Off Analysis
- Identify the largest drop-off stage
- A high impression-to-click but low click-to-purchase suggests the recommendation is compelling but the product page or pricing is problematic
- A low impression-to-click suggests the recommendation itself is not attractive

## Micro-Conversions

Not all conversions are final purchases. Micro-conversions are intermediate actions that indicate progression toward the ultimate goal.

### Types of Micro-Conversions

| Micro-Conversion | Value | Typical Funnel Stage |
|-----------------|-------|---------------------|
| Item page view | Low | Early consideration |
| Add to wishlist | Medium | Interest expression |
| Add to cart | High | Purchase intent |
| Share with friend | Medium | Social validation |
| Review/rate | Medium | Post-purchase engagement |
| Newsletter signup | Medium | Long-term relationship |
| Account creation | High | Commitment signal |

### Micro-Conversion Scoring

Assign weights to micro-conversions:

```
Weighted Conversion = Σ w_i * micro_conversion_i
```

Where w_i is calibrated to reflect the predictive value of each micro-conversion toward the ultimate goal.

## Conversion Rate by Segment

### Segmentation Dimensions

| Dimension | Example Segments | Why It Matters |
|-----------|-----------------|---------------|
| User tenure | New, 7-day, 30-day, loyal | New users may convert differently |
| Device | Mobile, desktop, tablet | Mobile has higher impulse, lower AOV |
| Geography | US, EU, APAC | Cultural differences in purchase behavior |
| Traffic source | Search, social, direct | Different intent levels |
| Time of day | Morning, afternoon, evening | Mood and availability affect conversion |
| Recommendation type | Collaborative, content-based, hybrid | Different recommendation strategies |

### Segment-Specific Optimization
- High-conversion segments: Maintain and protect
- Low-conversion segments: Investigate root cause (UX issue? catalog gap? relevance problem?)
- High-potential segments: Invest in personalized conversion optimization

## Statistical Significance of Conversion Changes

### Hypothesis Testing

```
H₀: CR_treatment = CR_control (no difference)
H₁: CR_treatment ≠ CR_control
```

### Sample Size Calculation

For detecting a minimum detectable effect (MDE) of δ:

```
n = (Z_α/2 + Z_β)² * [p₁(1-p₁) + p₂(1-p₂)] / (p₁ - p₂)²
```

Where:
- p₁ = baseline conversion rate
- p₂ = p₁ + δ (expected treatment conversion rate)
- Z_α/2 = critical value for significance level (1.96 for α = 0.05)
- Z_β = critical value for power (0.84 for 80% power)

### Example Calculation

| Parameter | Value |
|-----------|-------|
| Baseline CR | 5.0% |
| MDE | 0.5% (relative 10% lift) |
| Significance level | 0.05 |
| Power | 80% |
| **Required sample size** | **~30,000 per variant** |

### Multiple Testing Correction
When running multiple A/B tests or testing multiple segments, apply corrections:
- **Bonferroni**: α_adj = α / m (conservative)
- **Holm-Bonferroni**: Step-down procedure (less conservative)
- **Benjamini-Hochberg**: Controls false discovery rate (recommended for many tests)

### Common Pitfalls
- Stopping tests early when results look significant (peeking problem)
- Not accounting for novelty effects in the first few days
- Using conversion rate alone without considering revenue (a 1% CR increase with 20% lower AOV may be net negative)
- Ignoring user-level autocorrelation (the same user sees multiple recommendations)
