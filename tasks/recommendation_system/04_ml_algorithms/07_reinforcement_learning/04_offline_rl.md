# Offline Reinforcement Learning for Recommendations

## Overview

Offline reinforcement learning (offline RL) learns policies from pre-collected datasets without interacting with the environment. For recommendation systems, this is the most practical RL paradigm—live exploration with real users is risky, expensive, and often infeasible. Offline RL must handle distribution shift, limited exploration, and biased data, making it more challenging than online RL but safer for production deployment.

---

## Conservative Q-Learning (CQL)

### The Distribution Shift Problem

A policy trained offline may select actions that were rarely (or never) seen in the training data. The Q-function overestimates the value of these out-of-distribution (OOD) actions, leading to poor performance when deployed.

### CQL Solution

CQL adds a regularization term that penalizes Q-values for actions not supported by the dataset:

**L_CQL = E_{(s,a)~D} [Q(s,a)] - E_{s~D, a~π(a|s)} [Q(s,a)] + L_DQN**

- **First term**: Maximize Q-values for data-supported actions.
- **Second term**: Minimize Q-values for policy-selected actions (prevent overestimation of OOD actions).
- **Third term**: Standard DQN loss.

### CQL Variants

| Variant | Description | Trade-off |
|---|---|---|
| **CQL(α)** | Conservative penalty weight α | Higher α = more conservative |
| **CQL(ρ)** | Use weighted DKL for action distribution | Smoother regularization |
| **CQL-truncated** | Truncate Q-value bounds | More stable training |

### CQL for Recommendations

- **Conservative ranking**: Prefer items the model has seen positive feedback for.
- **Avoid novelty trap**: Don't recommend items with high predicted but unverified value.
- **Safe exploration**: New items are recommended cautiously, with lower confidence.

---

## Batch RL (Batch-Constrained Q-Learning)

### BCQ (Batch-Constrained Deep Q-Learning)

BCQ restricts the policy to actions similar to those in the training batch:

1. **Generative model**: Train a VAE to model the action distribution in the batch.
2. **Constrained policy**: At each step, perturb the generative model's output slightly (within the batch's support).
3. **Q-function**: Learn Q-values with the batch-constrained actions.

### BEAR (Bootstrapping Error Accumulation Reduction)

BEAR uses maximum mean discrepancy (MMD) to keep the learned policy close to the behavioral policy:

**L_BEAR = L_BCQ + λ × MMD(π_θ, π_data)**

The MMD constraint prevents the policy from straying too far from the data distribution.

### Decision Transformer

Decision Transformer reformulates RL as a sequence modeling problem:

- **Input**: (return-to-go, state, action) sequence.
- **Model**: Transformer that predicts the next action given the desired return and current state.
- **Inference**: Specify a desired return, and the model generates actions to achieve it.

---

## Dataset Constraints

### Types of Dataset Bias

| Bias Type | Description | Impact |
|---|---|---|
| **Selection bias** | Only logged actions that were taken | Missing counterfactual data |
| **Position bias** | Items in higher positions get more clicks | Overestimates top-position value |
| **Popularity bias** | Popular items are over-represented | Biased toward popular items |
| **Confounding** | Unobserved factors affect both action and reward | Spurious correlations |
| **Temporal bias** | Older data reflects outdated preferences | Distribution shift over time |

### Debiasing Strategies

| Strategy | Approach | Complexity |
|---|---|---|
| **Importance weighting** | Weight samples by inverse propensity | Low |
| **Doubly robust** | Combine imputation with importance weighting | Medium |
| **Counterfactual evaluation** | Estimate counterfactual outcomes | High |
| **Causal inference** | Model causal structure of the data generating process | High |

### Propensity Scoring

Estimate the probability that each action was taken (propensity score):

**p(a|s) = P(action a was taken in state s)**

Then weight each sample by 1/p(a|s) to correct for the selection bias:

**E_{weighted}[R(s,a)] = E_{biased}[R(s,a) / p(a|s)]**

---

## Reward Shaping for Offline RL

### Why Reward Shaping?

Sparse rewards (only purchase = +1, everything else = 0) make offline RL extremely sample-inefficient. Reward shaping provides denser learning signals:

| Technique | Description | Example |
|---|---|---|
| **Potential-based** | Add potential function differences | +0.1 for each scroll, +0.5 for add-to-cart |
| **Curiosity-driven** | Reward novelty/unexpectedness | Higher reward for novel item interactions |
| **Hierarchy-based** | Decompose into sub-goals | Reward for session engagement milestones |
| **Imitation** | Reward proximity to logged behavior | Reward for mimicking human recommendations |

### Reward Shaping Safety

Poorly designed reward shaping can lead to reward hacking:

- **Avoid shortcuts**: Don't create reward signals that can be maximized without genuine engagement.
- **Validate**: Test reward functions offline before using them for training.
- **Monitor**: Track whether shaped rewards correlate with business metrics.

---

## Counterfactual Evaluation

### What is Counterfactual Evaluation?

Counterfactual evaluation estimates what would have happened if a different policy had been followed, using only logged data:

**V(π) = E_{s~D} [Σ_a π(a|s) × Q(s,a)]**

### Inverse Propensity Scoring (IPS)

**V_IPS(π) = (1/N) Σ_i (π(a_i|s_i) / p(a_i|s_i)) × r_i**

Where:
- **π(a_i|s_i)**: Probability the new policy would take action a_i in state s_i.
- **p(a_i|s_i)**: Probability the logging policy took action a_i (propensity).
- **r_i**: Observed reward.

### Self-Normalized IPS

To reduce variance, normalize by the estimated number of effective samples:

**V_SNIPS(π) = Σ_i w_i × r_i / Σ_i w_i**

Where w_i = π(a_i|s_i) / p(a_i|s_i).

### Doubly Robust Estimator

Combines direct method (Q-function) with IPS for better bias-variance tradeoff:

**V_DR(π) = (1/N) Σ_i [Q(s_i, a_i) + w_i × (r_i - Q(s_i, a_i))]**

This estimator is consistent if either the Q-function or the propensity scores are correct (hence "doubly robust").

---

## Offline RL in Production

### Training Pipeline

1. **Data collection**: Log user interactions with the current policy.
2. **Data preprocessing**: Clean, deduplicate, and filter the logged data.
3. **Propensity estimation**: Estimate action probabilities (propensity scores).
4. **Policy training**: Train offline RL policy with conservative constraints.
5. **Counterfactual evaluation**: Estimate the new policy's performance offline.
6. **A/B testing**: Deploy the new policy in a live A/B test.
7. **Monitoring**: Track online metrics and compare with offline estimates.

### When to Use Offline RL

| Scenario | Suitability |
|---|---|
| Live exploration is risky (medical, financial) | Excellent |
| Large logged dataset available | Excellent |
| Non-stationary environment | Good (retrain periodically) |
| Very sparse rewards | Challenging (need reward shaping) |
| High-dimensional action spaces | Good (with function approximation) |
| Need for explainability | Challenging (RL policies are opaque) |
