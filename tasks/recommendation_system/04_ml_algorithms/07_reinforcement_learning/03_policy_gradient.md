# Policy Gradient Methods for Recommendations

## Overview

Policy gradient methods directly optimize the recommendation policy (mapping from states to actions) by estimating the gradient of expected reward with respect to policy parameters. Unlike Q-learning, which learns value functions and derives a policy, policy gradient methods learn the policy directly, enabling handling of continuous action spaces, stochastic policies, and complex reward structures.

---

## REINFORCE Algorithm

### Core Idea

REINFORCE (Williams, 1992) estimates the gradient of expected reward:

**∇_θ J(θ) = E_π [Σ_t ∇_θ log π_θ(a_t|s_t) × G_t]**

Where:
- **π_θ(a|s)**: Policy parameterized by θ, giving the probability of action a in state s.
- **G_t**: Cumulative reward from time step t (return).
- **∇_θ log π_θ**: Score function (direction of parameter change).

### REINFORCE for Recommendations

1. **State**: User context and interaction history.
2. **Policy**: Neural network that outputs a probability distribution over items.
3. **Action**: Sample an item from the policy distribution.
4. **Reward**: User engagement signal (click, purchase, etc.).
5. **Update**: After the episode (session) ends, update policy parameters using cumulative rewards.

### REINFORCE Limitations

| Limitation | Description | Impact |
|---|---|---|
| **High variance** | Gradient estimates have high variance | Slow convergence, unstable training |
| **No bootstrapping** | Must wait until episode ends to compute returns | Sample inefficient |
| **No baseline** | Raw returns have high variance | Can be mitigated with baselines |

---

## Actor-Critic Methods

### Architecture

Actor-critic methods combine policy gradient (actor) with value function estimation (critic):

| Component | Role | Output |
|---|---|---|
| **Actor** | Policy network | Action probabilities π_θ(a\|s) |
| **Critic** | Value network | State value V_φ(s) or Q-value Q_φ(s,a) |

### Advantage Function

The critic provides a baseline to reduce variance:

**A(s, a) = Q(s, a) - V(s)**

The advantage A(s, a) measures how much better action a is compared to the average action in state s. Using advantages instead of raw returns reduces gradient variance significantly.

### Actor-Critic Update

**Actor update**: ∇_θ J(θ) = E_π [∇_θ log π_θ(a_t|s_t) × A(s_t, a_t)]

**Critic update**: Minimize (Q_φ(s, a) - (r + γ × V_φ(s'))²)

### Actor-Critic for Recommendations

| Advantage | Benefit for Recsys |
|---|---|
| Lower variance | More stable training with sparse rewards |
| Online learning | Can update after each interaction (no need to wait for episode end) |
| Continuous updates | Adapt to changing user behavior in real-time |

---

## A3C (Asynchronous Advantage Actor-Critic)

### Architecture

A3C runs multiple actors in parallel, each interacting with a different user/environment:

- **Parallel actors**: Multiple workers, each with their own copy of the actor and critic.
- **Asynchronous updates**: Workers independently compute gradients and update shared parameters.
- **Global network**: Shared parameter server that aggregates worker updates.

### A3C for Recommendations

| Feature | Benefit |
|---|---|
| **Parallel data collection** | Multiple simulated or real user interactions simultaneously |
| **Diverse experiences** | Different workers explore different parts of the state space |
| **Faster training** | Parallel computation accelerates gradient estimation |
| **More stable** | Averaging across workers reduces variance |

### A3C vs. Other Methods

| Method | Training Mode | Sample Efficiency | Stability |
|---|---|---|---|
| **REINFORCE** | Single episode | Low | Low |
| **Actor-Critic** | Single trajectory | Moderate | Moderate |
| **A3C** | Parallel trajectories | Moderate | High |
| **PPO** | Multiple epochs | High | High |

---

## Continuous Action Spaces

### The Problem

In some recommendation settings, actions are continuous:

- **Ranked list generation**: Assigning a continuous score to each item for ranking.
- **Feature-weighted recommendations**: Continuous weights for combining recommendation signals.
- **Exploration parameters**: Continuous exploration rates for different user segments.

### Continuous Policy Gradients

For continuous actions, the policy outputs a distribution (e.g., Gaussian):

**π_θ(a|s) = N(μ_θ(s), σ²_θ(s))**

Where:
- **μ_θ(s)**: Mean action (e.g., optimal ranking score) predicted by the policy.
- **σ²_θ(s)**: Variance (exploration noise).

### Deterministic Policy Gradient (DPG)

DPG learns a deterministic policy μ_θ(s) without the variance of stochastic policies:

**∇_θ J(θ) = E_π [∇_θ μ_θ(s) × ∇_a Q_φ(s, a)|_{a=μ_θ(s)}]**

DPG is combined with experience replay and target networks in DDPG (Deep Deterministic Policy Gradient) for stable training.

---

## Baseline Estimation

### Why Baselines?

Baselines reduce the variance of gradient estimates without introducing bias:

**∇_θ J(θ) = E_π [∇_θ log π_θ(a_t|s_t) × (G_t - b(s_t))]**

Where b(s_t) is the baseline. The baseline can be any function of the state (not dependent on the action).

### Baseline Types

| Baseline | Description | Variance Reduction |
|---|---|---|
| **State value V(s)** | Expected return from state s | High (standard choice) |
| **Moving average** | Average recent returns | Moderate |
| **Critic network** | Learned value function | High (actor-critic) |
| **Action-independent baseline** | Any function of state only | Varies |

### Recommended Baseline for Recsys

Use the critic network (value function) as the baseline in actor-critic methods. This provides the best variance reduction while maintaining unbiased gradient estimates.

---

## Policy Gradient Training Considerations

| Consideration | Approach |
|---|---|
| **Sparse rewards** | Reward shaping, curiosity-driven exploration |
| **Large action spaces** | Hierarchical policies, attention-based selection |
| **Off-policy correction** | Importance sampling, experience replay |
| **Safety constraints** | Constrained policy optimization (CPO) |
| **Multi-objective** | Pareto-optimal policies, scalarization |
