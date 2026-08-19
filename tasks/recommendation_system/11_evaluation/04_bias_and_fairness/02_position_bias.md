# Position Bias

## Overview

Position bias is one of the most pervasive and damaging biases in recommendation and search systems. It refers to the tendency of users to click, view, or interact with items based on their position in a ranked list, independent of the item's actual relevance. Users disproportionately click on top-positioned items because they are more visible, not necessarily because they are more relevant. This creates a feedback loop: items at the top get more clicks, which makes them appear more relevant, which causes the model to rank them even higher.

## Causes of Position Bias

### Visibility Bias
- Users scan lists from top to bottom
- Items at positions 1–3 receive significantly more visual attention than items at positions 7–10
- Eye-tracking studies show users spend 70–80% of their time looking at the top 3 results

### Examination Hypothesis
The probability of clicking an item is the product of two independent probabilities:

```
P(click_i) = P(examine_position_i) × P(relevant_i | examined)
```

Where:
- P(examine_position_i) decreases sharply with position
- P(relevant_i | examined) is the true relevance signal

This decomposition reveals that observed clicks conflate visibility with relevance.

### Position Bias by Platform

| Platform | Bias Magnitude | Typical CTR Decay |
|----------|---------------|-------------------|
| Search engines | Very high | 50% drop from pos 1 to pos 2 |
| E-commerce | High | 30–40% drop per position |
| News feeds | Moderate | 20–30% drop per position |
| Social media | Lower | 10–15% drop per position (infinite scroll) |
| Mobile apps | Variable | Depends on screen real estate |

### Quantitative Position Effects

| Position | Relative CTR (normalized to pos 1) |
|----------|-------------------------------------|
| 1 | 1.00 |
| 2 | 0.60–0.80 |
| 3 | 0.40–0.65 |
| 5 | 0.20–0.40 |
| 10 | 0.05–0.15 |
| 20 | 0.01–0.05 |

## Measurement of Position Bias

### Randomized Position Experiment

The gold standard for measuring position bias is a randomized experiment:

1. **Randomly shuffle** the order of recommendations for a subset of users
2. **Measure CTR** at each position in the randomized list
3. **Compare** randomized CTR to production CTR

```
Position_Bias(position_i) = CTR_production(position_i) / CTR_random(position_i)
```

In the randomized condition, all items have equal relevance on average, so any variation in CTR across positions is purely due to position bias.

### Interleaving-Based Measurement

1. Take two ranked lists from different algorithms
2. Interleave items randomly
3. Measure which positions receive more clicks
4. The position effect is estimated from the interleaved clicks

### Click Model Approaches

| Model | Assumption | Estimation |
|-------|-----------|------------|
| **Cascade model** | Users examine items top-to-bottom, click at most one | EM algorithm |
| **PBM (Position-Based Model)** | P(click) = P(examine) × P(relevance) | EM algorithm |
| **DBN (Dynamic Bayesian Network)** | Users can stop, skip, and continue examining | Bayesian inference |
| **UBM (User Browsing Model)** | Examination depends on previous clicks | EM algorithm |

### PBM Estimation

The Position-Based Model estimates position bias parameters using Expectation-Maximization:

**E-step**: Estimate the probability that each item was examined:
```
P(examine_i | click_i) = 1
P(examine_i | no_click) = position_weight_i × relevance_i / Σ(position_weight_j × relevance_j)
```

**M-step**: Update position weights and relevance estimates from the E-step estimates.

Convergence typically requires 10–50 iterations on millions of click records.

## Mitigation Strategies

### Position-Aware Models

Include position as a feature in the click model:

```
P(click_i) = f(relevance_i, position_i)
```

During prediction, exclude the position feature (since the model will assign positions). This decomposes the click probability into relevance and position components.

### Inverse Propensity Scoring (IPS)

Weight each click by the inverse of the probability of examining its position:

```
IPS_weight(click_i) = 1 / P(examine_position_i)
```

For unbiased training:
```
Loss = Σ IPS_weight(click_i) × log(P(model | click_i))
```

IPS amplifies the signal from clicks at low positions (where examination probability is low), giving them appropriate weight.

### Unbiased Learning to Rank

| Method | Approach | Pros | Cons |
|--------|----------|------|------|
| **IPS-based** | Weight clicks by inverse position propensity | Theoretically grounded | High variance for low-position items |
| **Unbiased LambdaMART** | Modify lambda gradients with position correction | Integrates with gradient boosting | Requires position propensity estimates |
| **PAL (Position-Aware Learning)** | Jointly model relevance and position bias | End-to-end training | More complex architecture |
| **HED (Hedged Estimation)** | Debias using exploration data | Requires exploration traffic | Traffic cost |

### Position Debiasing in Training Data

| Strategy | Description | Data Requirement |
|----------|-------------|-----------------|
| **Randomized data** | Collect a small set of randomized recommendations | Requires production traffic |
| **Click model debiasing** | Apply PBM/DBN to debias click logs | Large click log dataset |
| **IPS reweighting** | Weight training examples by inverse propensity | Position propensity model |
| **Counterfactual evaluation** | Estimate what would have happened with different rankings | Causal inference framework |

### Practical Debiasing Pipeline

```
1. Collect position propensity estimates (from randomized data or click models)
2. Apply IPS weighting to training data
3. Train recommendation model with weighted loss
4. Evaluate with position-agnostic metrics (NDCG@K with unbiased relevance labels)
5. Monitor position bias in production using holdout randomization
```

## Position Debiasing in Production

### Randomization Infrastructure

Maintain a small randomization traffic allocation (1–5% of users) to continuously estimate position propensities:

| Component | Purpose | Cost |
|-----------|---------|------|
| Random traffic splitter | Route 1–5% of users to randomized lists | Negligible |
| Position propensity estimator | Compute P(examine_i) from randomized data | Compute cost |
| Propensity store | Cache propensities for real-time IPS weighting | Storage cost |

### Monitoring Position Bias

| Metric | Formula | Alert Condition |
|--------|---------|----------------|
| Position CTR gap | CTR(pos1) / CTR(pos10) | Ratio > 10 (excessive bias) |
| IPS weight variance | Var(1/P(examine_i)) | Variance > threshold (unstable training) |
| Randomization CTR | CTR in randomized traffic | CTR < 50% of production (strong bias) |
| NDCG lift from debiasing | NDCG(debiased) / NDCG(biased) | Lift < 1.01 (minimal improvement) |

### Common Pitfalls in Position Debiasing

1. **Ignoring position bias in evaluation**: Computing NDCG on biased click data overestimates model performance
2. **Over-debiasing**: Removing too much position signal can harm performance if position is a legitimate relevance signal (e.g., editorial rankings)
3. **Non-stationary propensities**: Position bias changes as UI evolves; propensities must be updated regularly
4. **Platform-specific patterns**: Mobile has different position bias than desktop; don't share propensity models across platforms
5. **Click-through fraud**: Invalid clicks (bots, accidental clicks) introduce noise that IPS amplifies
