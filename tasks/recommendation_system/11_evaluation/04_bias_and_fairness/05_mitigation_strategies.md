# Debiasing Strategies

## Overview

Debiasing strategies for recommendation systems address the systematic biases that arise from how data is collected, how models are trained, and how recommendations are presented. These strategies span the entire pipeline—from causal inference for understanding bias origins, to adversarial training for removing protected attribute effects, to re-ranking and post-processing for ensuring fairness in final outputs.

## Causal Inference for Recommendations

### The Causal Perspective

Traditional recommendation models learn associations from observational data. Causal inference distinguishes correlation from causation, identifying which user behaviors are caused by recommendations versus other factors.

### Causal Graph for Recommendations

```
User Preferences (Z) → User Actions (Y)
         ↓                    ↑
  Recommendation shown (T) → Observed Click (C)
         ↑
  Model Predictions (M) ← Training Data (D) ← Observed Clicks (C)
```

This graph reveals the feedback loop: observed clicks influence the model, which influences what is shown, which influences future clicks.

### Causal Estimands

| Estimand | Definition | Question |
|----------|-----------|----------|
| **ATE** (Average Treatment Effect) | E[Y(1) - Y(0)] | What is the average effect of showing an item? |
| **CATE** (Conditional ATE) | E[Y(1) - Y(0) \| X] | What is the effect for specific user/item types? |
| **ITE** (Individual Treatment Effect) | Y_i(1) - Y_i(0) | What is the effect for a specific user? |
| **ATT** (Average Treatment on Treated) | E[Y(1) - Y(0) \| T=1] | What is the effect for users who actually saw the item? |

### Backdoor Adjustment

If we can measure all confounders Z (variables that affect both treatment and outcome):

```
P(Y | do(T)) = Σ_z P(Y | T, Z=z) × P(Z=z)
```

In practice: control for user features, item features, and context when estimating recommendation effects.

### Front-Door Adjustment

When confounders are unmeasurable, use a mediator M:

```
P(Y | do(T)) = Σ_m P(M=m | T) × Σ_t P(Y | M=m, T=t) × P(T=t)
```

Requires a mediator that fully mediates the effect of T on Y and is not affected by confounders.

## Counterfactual Reasoning

### Definition

Counterfactual reasoning asks: "What would have happened if a different recommendation had been made?" This enables evaluating alternative policies without deploying them.

### Counterfactual Policy Evaluation

Given data collected under policy π_old, estimate the value of a new policy π_new:

```
V(π_new) = Σ_u Σ_i π_new(i|u) / π_old(i|u) × r(u,i)
```

This is importance sampling: reweight observed rewards by the ratio of new to old policy probabilities.

### Counterfactual Data Augmentation

1. For each observed interaction (user u, item i, outcome y):
   - Sample a counterfactual item j that could have been shown
   - Estimate what the outcome would have been: ŷ(u, j)
   - Create a training pair (u, j, ŷ(u, j))
2. Train the model on both observed and counterfactual data

### Doubly Robust Counterfactual Estimation

Combine a predictive model with importance sampling:

```
DR_estimate = f(u, i) + w(u, i) × (y(u, i) - f(u, i))
```

Where f is a direct method model and w is the importance weight. The estimate is consistent if either f or w is correct.

## Adversarial Debiasing

### Concept

Train a recommendation model jointly with an adversary that tries to predict a protected attribute from the model's representations. The goal is to learn representations that are predictive of user preferences but not of protected attributes.

### Architecture

```
User Features → Encoder → Latent Representation → Recommender → Predictions
                              ↓
                        Adversary → Protected Attribute Prediction
```

### Training Objective

```
Loss = L_recommendation - λ × L_adversary
```

Where:
- L_recommendation = standard recommendation loss (BPR, cross-entropy)
- L_adversary = adversary's loss for predicting the protected attribute
- λ = tradeoff parameter controlling fairness vs. accuracy

The adversary tries to minimize its loss (predict protected attributes well), while the encoder tries to maximize the adversary's loss (make protected attributes unpredictable).

### Adversarial Debiasing Variants

| Variant | Approach | Pros | Cons |
|---------|----------|------|------|
| **Gradient reversal** | Reverse adversary gradient during encoder training | Simple, end-to-end | Can destabilize training |
| **Alternating training** | Alternate between adversary and encoder updates | More stable | Slower convergence |
| **Wasserstein GAN** | Use Wasserstein distance for adversary | Better gradient signals | More complex |
| **Fair representations** | Learn fair latent space before recommendation | Modular | May lose important information |

### Limitations

- Adversarial debiasing may reduce recommendation quality significantly for small fairness improvements
- The tradeoff parameter λ is hard to tune
- Adversarial training can be unstable and requires careful hyperparameter tuning
- May not satisfy formal fairness definitions (demographic parity, equalized odds)

## Re-Ranking for Fairness

### Concept

Generate recommendations using an unconstrained model, then re-rank the list to satisfy fairness constraints while preserving as much relevance as possible.

### Re-Ranking Approaches

#### Greedy Re-Ranking
```
For each position in the list:
    Select the item that maximizes relevance subject to:
    - Fairness constraint not violated
    - Diversity constraint satisfied
    - Business rules respected
```

#### Constrained Optimization

```
Maximize: Σ_i relevance(i) × position_weight(i)
Subject to:
    - Demographic parity: |exposure(group A) - exposure(group B)| ≤ ε
    - Minimum exposure: exposure(provider_i) ≥ min_threshold
    - Diversity: ILD(list) ≥ diversity_threshold
    - Budget: total_cost ≤ budget
```

#### Learning to Re-Rank

Train a re-ranking model that takes the initial ranking and fairness constraints as input and produces a fair ranking:

```
Fair_list = ReRanker(initial_list, constraints, user_context)
```

### Re-Ranking Methods Comparison

| Method | Quality Preservation | Constraint Satisfaction | Computational Cost |
|--------|---------------------|------------------------|-------------------|
| Greedy | Moderate | Exact | Low |
| ILP (Integer Linear Programming) | High | Exact | High |
| Markov Chain Monte Carlo | High | Approximate | Medium |
| RL-based re-ranking | High | Approximate | High |
| Determinantal Point Processes | High | Soft | Medium |

## Exploration for Exposure Fairness

### Concept

Explore less-shown items to gather feedback and provide exposure opportunities. This addresses exposure bias by intentionally deviating from the exploitation-only strategy.

### Exploration Strategies

| Strategy | Mechanism | Pros | Cons |
|----------|----------|------|------|
| **ε-Greedy** | Randomly show a non-top item with probability ε | Simple | May show irrelevant items |
| **Thompson Sampling** | Sample from posterior, explore uncertain items | Bayesian, principled | Complex implementation |
| **Upper Confidence Bound** | Select items with highest UCB score | Balances exploration/exploitation | Requires uncertainty estimates |
| **Information gain** | Explore items that provide maximum information | Efficient exploration | Expensive computation |
| **Fairness-constrained exploration** | Explore only enough to satisfy fairness constraints | Targeted | Requires fairness thresholds |

### Exploration for New Items

| Phase | Strategy | Duration |
|-------|----------|----------|
| **Cold start** | Random exposure to all new items | First 1–7 days |
| **Early feedback** | Thompson sampling with uniform prior | Days 7–30 |
| **Stable exploitation** | Standard model with exploration bonus for undershown items | Ongoing |

### Exploration Budget

```
Exploration_Users = ε × Total_Users
Exploration_Impressions = ε × Total_Impressions
Typical ε: 1–5% of traffic
```

## Post-Processing Calibration

### Concept

After the model produces scores, adjust them to satisfy fairness and calibration constraints.

### Calibration Methods

#### Platt Scaling per Group

Fit a separate sigmoid calibration for each protected group:

```
P_adjusted = σ(a_group × raw_score + b_group)
```

Where a_group and b_group are learned from calibration data.

#### Temperature Scaling

```
P_adjusted = softmax(raw_scores / temperature)
```

Adjust temperature per group to equalize calibration.

#### Isotonic Regression per Group

Non-parametric calibration using isotonic regression separately for each group.

### Post-Processing for Equalized Odds

1. Compute the ROC curve for each group
2. Find the operating point that equalizes TPR and FPR across groups
3. Adjust decision thresholds per group

### Post-Processing Tradeoffs

| Method | Accuracy Cost | Fairness Gain | Complexity |
|--------|-------------|--------------|-----------|
| Threshold adjustment | Low (1–3%) | Moderate | Low |
| Platt scaling | Very low (<1%) | Moderate | Low |
| Isotonic regression | Low (1–2%) | High | Medium |
| Reject option | High (5–15%) | High | Low |
| Re-ranking | Low (2–5%) | High | High |

## End-to-End Debiasing Pipeline

### Recommended Approach

```
Stage 1: Data Collection
    - Collect randomized exposure data (1–5% traffic)
    - Estimate position propensities
    - Identify protected attributes and fairness requirements

Stage 2: Training
    - Apply IPS reweighting to training data
    - Consider adversarial debiasing for protected attributes
    - Train with fairness-aware loss functions

Stage 3: Post-Processing
    - Re-rank for fairness constraints
    - Apply calibration per group
    - Ensure minimum exposure guarantees

Stage 4: Online Evaluation
    - A/B test debiased model vs. baseline
    - Monitor fairness metrics in production
    - Use exploration traffic to continuously update propensity estimates

Stage 5: Monitoring
    - Automated fairness checks per training cycle
    - Quarterly comprehensive fairness audits
    - Incident-driven audits when issues arise
```

### Debiasing Strategy Selection Guide

| Bias Type | Primary Strategy | Secondary Strategy |
|-----------|-----------------|-------------------|
| Position bias | IPS reweighting | Position-aware model |
| Exposure bias | Exploration + IPS | Doubly robust estimation |
| Popularity bias | Exposure fairness constraints | Re-ranking |
| Demographic bias | Adversarial debiasing | Calibration per group |
| Provider bias | Exposure guarantees | Re-ranking for fairness |
| Self-selection bias | Doubly robust estimation | Randomized data collection |
