# Online Evaluation

## Overview

Online evaluation measures recommendation system performance using live user interactions in production. Unlike offline evaluation (which uses historical data), online evaluation captures real user behavior in real environments, accounting for factors that offline metrics cannot: user interface effects, temporal dynamics, network effects, and the cold-start problem. Online evaluation is the definitive way to determine whether a new recommendation algorithm should be deployed to all users.

## A/B Testing Framework

### Core Concept

A/B testing randomly splits users into groups, exposing each group to a different recommendation variant, and compares performance on pre-defined metrics.

### Framework Components

| Component | Description | Implementation |
|-----------|-------------|---------------|
| **Traffic splitter** | Routes users to variants deterministically | Hash-based user ID assignment |
| **Variant config** | Defines what each variant receives | Feature flags, model version, config params |
| **Metric collector** | Logs impressions, clicks, conversions per variant | Event logging pipeline |
| **Statistical engine** | Computes significance, confidence intervals | Sequential or fixed-horizon testing |
| **Dashboard** | Visualizes results in real-time | Monitoring + alerting system |

### Variant Design

#### Model Comparison Test
```
Control (A): Current production model (e.g., collaborative filtering)
Treatment (B): New model (e.g., deep learning ranking)
```

#### Feature Test
```
Control (A): Model without feature X
Treatment (B): Model with feature X
```

#### UI Test
```
Control (A): Recommendation carousel layout
Treatment (B): Recommendation grid layout
```

### Traffic Splitting

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| **User-level split** | Each user consistently sees one variant | No within-user confusion | Slower to reach significance |
| **Session-level split** | Each session randomly assigned | Faster convergence | Inconsistent user experience |
| **Request-level split** | Each API request randomly assigned | Fastest convergence | Most inconsistent experience |

**Best practice**: Use user-level splits for recommendation tests to avoid confusing users.

### Guardrail Metrics

During A/B tests, monitor guardrail metrics to ensure the treatment does not harm core product metrics:

| Guardrail | Purpose | Alert Threshold |
|-----------|---------|----------------|
| Overall revenue | Ensure no revenue decline | < 0% vs control |
| Page load time | Ensure model doesn't slow responses | > 200ms increase |
| Error rate | Ensure model doesn't increase errors | > 0.1% increase |
| User-reported issues | Catch UX problems | Spike in support tickets |

## Interleaving Experiments

### Concept

Interleaving presents items from multiple recommendation algorithms within a single list, rather than splitting users across separate lists. This provides more sensitive comparisons with fewer users.

### Interleaving Methods

#### Team Draft Interleaving (TDI)
1. Each algorithm generates a ranked list
2. Alternately pick items from each list, "drafting" items as they are shown
3. Count which algorithm's items receive more engagement

#### Monointerleaving
1. Merge items from both algorithms using interleaving
2. Assign credit based on which algorithm's item was clicked
3. Score = (clicks on algorithm A items) - (clicks on algorithm B items)

#### Probabilistic Interleaving
1. Each algorithm has a sampling distribution over items
2. Items are drawn probabilistically from both distributions
3. Credit is assigned proportional to the probability each algorithm would have shown the clicked item

### Interleaving vs A/B Testing

| Aspect | A/B Testing | Interleaving |
|--------|------------|-------------|
| Sensitivity | Lower (between-user) | Higher (within-user) |
| Sample size needed | ~10K–100K users per variant | ~100–1K users |
| User experience | Consistent per user | Mixed recommendations |
| Metric interpretability | Direct business metrics | Relative preference signal |
| Deployment readiness | Ready for production | Not suitable for production |

### When to Use Interleaving
- **Early-stage model comparison**: Quickly screen many model candidates
- **Research evaluation**: Academic-style comparison with limited users
- **Algorithm selection**: Choose the best algorithm before full A/B test

## Switchback Experiments

### Concept

Switchback experiments alternate treatment and control conditions over time rather than over users. All users receive the same variant at any given time, but the variant switches periodically.

### Design

```
Time block 1: All users → Control
Time block 2: All users → Treatment
Time block 3: All users → Control
Time block 4: All users → Treatment
...
```

### When Switchback Is Appropriate

| Scenario | Why Switchback |
|----------|---------------|
| **Network effects** | User-to-user interactions contaminate A/B splits |
| **Marketplace balance** | Splitting supply/demand sides creates imbalance |
| **Limited user pool** | Too few users for parallel testing |
| **Carryover effects** | Previous recommendations influence future behavior |

### Switchback Analysis

Use a within-period comparison:
```
Treatment Effect = (Metric during treatment periods) - (Metric during control periods)
```

Account for:
- **Period effects**: Trends over time (e.g., holiday shopping)
- **Order effects**: First period may differ from later periods
- **Washout periods**: Time needed for the previous condition to wear off

### Switchback vs A/B Testing

| Aspect | A/B Testing | Switchback |
|--------|------------|-----------|
| Network effects | Vulnerable | Robust |
| Statistical power | Higher | Lower (fewer independent periods) |
| User experience | Consistent | Varies over time |
| Analysis complexity | Simple | Moderate (time effects) |
| Duration | Shorter | Longer (need many periods) |

## Bandit-Based Evaluation

### Multi-Armed Bandits for Online Evaluation

Instead of fixed 50/50 splits, bandits dynamically allocate traffic to better-performing variants.

### Types

| Type | Behavior | Exploration Strategy |
|------|----------|---------------------|
| **ε-Greedy** | Exploit best variant with probability 1-ε, explore randomly with ε | Fixed exploration rate |
| **Upper Confidence Bound (UCB)** | Select variant with highest UCB score | Uncertainty-based exploration |
| **Thompson Sampling** | Sample from posterior distributions, select highest sample | Bayesian exploration |
| **Contextual bandits** | Condition allocation on user features | Personalized exploration |

### Bandit Advantages for Evaluation
- **Faster convergence**: Less traffic wasted on clearly inferior variants
- **Adaptive**: Automatically shifts traffic as evidence accumulates
- **Handles non-stationarity**: Adapts when user behavior changes

### Bandit Limitations for Evaluation
- **Biased estimates**: Traffic allocation introduces selection bias
- **Requires correction**: Inverse propensity scoring needed for unbiased estimates
- **Complexity**: More complex to implement and analyze than A/B tests
- **Not suitable for all metrics**: Some metrics require balanced traffic

### Unbiased Estimation with Bandits

```
Unbiased_Metric = (1/n) * Σ (outcome_i / propensity_i)
```

Where propensity_i is the probability that variant i was selected for user u. This is called inverse propensity scoring (IPS).

## Online Metric Selection

### Primary Metrics for Online Tests

| Category | Primary Metric | When to Use |
|----------|---------------|-------------|
| Engagement | Click-through rate (CTR) | Content recommendation, discovery |
| Conversion | Conversion rate | E-commerce, transactional |
| Revenue | Revenue per user | Monetized platforms |
| Retention | Day-7 retention | Long-term value assessment |
| Satisfaction | User satisfaction score | When surveys are available |

### Metric Selection Criteria

1. **Sensitivity**: Can the metric detect a meaningful change with reasonable sample size?
2. **Stability**: Is the metric stable day-to-day (low variance)?
3. **Relevance**: Does the metric align with business objectives?
4. **Manipulation resistance**: Can the metric be gamed by the recommendation system?
5. **Timely**: Does the metric produce results quickly enough for decision-making?

### Metric Hierarchy

```
Level 1 (Primary): One North Star metric for go/no-go decision
Level 2 (Secondary): 2–3 supporting metrics for deeper analysis
Level 3 (Guardrail): Metrics that must not degrade
```

## Experiment Duration

### Factors Affecting Duration

| Factor | Impact | Consideration |
|--------|--------|--------------|
| **Sample size** | More users → shorter experiments | Platform traffic volume |
| **Effect size** | Larger effects detected faster | Minimum detectable effect (MDE) |
| **Metric variance** | Higher variance → longer experiments | Revenue metrics are noisier than CTR |
| **Seasonality** | Must cover full cycle | Weekly, monthly, quarterly patterns |
| **Novelty effect** | Initial novelty wears off | Typically 1–2 weeks |

### Minimum Experiment Duration

| Platform Type | Minimum Duration | Rationale |
|--------------|-----------------|-----------|
| High-traffic (>1M DAU) | 1–2 weeks | Enough samples quickly |
| Medium-traffic (100K–1M DAU) | 2–4 weeks | Need time for statistical power |
| Low-traffic (<100K DAU) | 4–8 weeks | Slow accumulation of samples |
| B2B / enterprise | 4–12 weeks | Small user pools, long sales cycles |

### Duration Best Practices

1. **Run for at least one full business cycle** (typically 1–2 weeks) to capture day-of-week effects
2. **Don't stop early** based on intermediate results (peeking inflates false positive rate)
3. **Account for novelty effects**: Exclude the first 3–7 days from analysis
4. **Check for sufficient power**: If the test is underpowered, extend rather than conclude "no difference"

## Sample Size Calculation

### For Binary Metrics (CTR, Conversion Rate)

```
n = (Z_α/2 + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₁ - p₂)²
```

Where:
- p₁ = baseline rate
- p₂ = p₁ + MDE (minimum detectable effect)
- α = significance level (typically 0.05)
- β = Type II error rate (typically 0.20, giving 80% power)

### For Continuous Metrics (Revenue, Session Duration)

```
n = (Z_α/2 + Z_β)² × 2σ² / δ²
```

Where:
- σ = standard deviation of the metric
- δ = minimum detectable effect (absolute)

### Quick Reference Table

| Baseline Rate | MDE (Relative) | Required n per variant |
|--------------|---------------|----------------------|
| 5% CTR | 10% lift | ~15,000 |
| 5% CTR | 5% lift | ~60,000 |
| 2% conversion | 10% lift | ~38,000 |
| 2% conversion | 20% lift | ~10,000 |
| $50 AOV | 5% lift | ~10,000 (σ=$30) |

### Sequential Testing

For ongoing experiments, use sequential testing to allow early stopping:

| Method | Description | Benefit |
|--------|-------------|---------|
| **Always-valid p-values** | Adjust p-values for repeated looks | Can stop early without inflating FPR |
| **Group sequential designs** | Pre-planned interim analyses | Balanced flexibility and rigor |
| **Bayesian testing** | Posterior probability of superiority | Intuitive; natural stopping rule |

## Common Online Evaluation Pitfalls

1. **Peeking**: Checking results repeatedly inflates false positive rate
2. **Novelty effect**: Initial improvement may not sustain (run for 2+ weeks)
3. **Sample ratio mismatch**: Check that actual split matches intended split
4. **Network effects**: Users in control interact with users in treatment
5. **Interference**: Treatment users affect control users (e.g., marketplace dynamics)
6. **Multiple testing**: Running many A/B tests without correction increases false discoveries
7. **Metric selection bias**: Choosing the metric that shows significance after seeing results
