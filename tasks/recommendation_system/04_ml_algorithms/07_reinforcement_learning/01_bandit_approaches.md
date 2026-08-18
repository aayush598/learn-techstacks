# Multi-Armed Bandits for Recommendations

## Overview

Multi-Armed Bandits (MABs) provide a principled framework for the exploration-exploitation tradeoff in recommendation systems. Unlike traditional A/B testing which requires fixed experiment durations, bandit algorithms dynamically allocate traffic to better-performing options while continuing to explore alternatives. This makes them ideal for real-time personalization, cold-start scenarios, and situations where the cost of exploration is high.

---

## The Exploration-Exploitation Tradeoff

### Fundamental Dilemma

- **Exploitation**: Recommend items known to perform well (maximize immediate reward)
- **Exploration**: Try new or uncertain items to discover potentially better options (maximize long-term reward)

### Why Bandits Over A/B Tests

| Aspect | A/B Testing | Multi-Armed Bandit |
|--------|------------|-------------------|
| Traffic allocation | Fixed (50/50) | Adaptive (weighted by performance) |
| Exploration cost | High (50% on potentially bad variant) | Lower (minimal traffic to poor options) |
| Duration | Fixed, predetermined | Adaptive, converges dynamically |
| Sequential decisions | No | Yes |
| Regret minimization | Not explicitly optimized | Core objective |
| Multiple variants | Limited (significant dilution) | Handles many variants well |

### Regret

The core metric for bandit algorithms is **cumulative regret** — the difference between the reward of the optimal arm and the reward actually obtained:

```
R(T) = Σ_{t=1}^{T} (μ* - μ_{a_t})
```

Where:
- `μ*`: Reward of the best arm
- `μ_{a_t}`: Reward of the arm chosen at time t
- `T`: Total number of rounds

The goal is to minimize cumulative regret. Sub-linear regret (O(√T) or O(log T)) indicates the algorithm converges to the optimal arm.

---

## Classic Bandit Algorithms

### Epsilon-Greedy

#### Algorithm

```
With probability ε: Explore (choose random arm)
With probability 1-ε: Exploit (choose arm with highest estimated reward)
```

#### Variants

| Variant | Description | Pros | Cons |
|---------|-------------|------|------|
| Fixed ε | Constant exploration rate | Simple | May over/under-explore |
| Decaying ε | ε decreases over time | Adapts | Requires tuning decay schedule |
| Optimistic ε | Start with high ε, decay | Good initial exploration | Decay rate sensitive |

#### Decay Schedules

- **Linear decay**: `ε_t = max(ε_min, ε_0 - ct)`
- **Exponential decay**: `ε_t = ε_0 × α^t` where α < 1
- **1/t decay**: `ε_t = c/t` (theoretically optimal, converges slowly)

#### When to Use

- Many arms with similar performance
- Simple baseline is sufficient
- Real-time decisions with minimal compute

### Upper Confidence Bound (UCB)

#### UCB1 Algorithm

```
Choose arm with maximum: X̄_a + √(2 × ln(t) / N_a)
```

Where:
- `X̄_a`: Average reward of arm a
- `t`: Current round number
- `N_a`: Number of times arm a has been pulled

The second term is the **exploration bonus** — arms pulled fewer times get a higher bonus, encouraging exploration.

#### UCB Variants

| Variant | Exploration Term | Properties |
|---------|-----------------|------------|
| UCB1 | √(2 ln(t) / N_a) | Standard, log(T) regret |
| UCB2 | Uses confidence intervals | Tighter bounds |
| UCB-V | Variance-adaptive | Better for variable rewards |
| Discounted UCB | Discounted history | Adapts to non-stationary |

#### Advantages over Epsilon-Greedy

- No hyperparameter to tune (exploration is automatic)
- Provably optimal regret bounds (O(log T))
- Naturally balances exploration and exploitation

#### Limitations

- Assumes bounded rewards in [0, 1]
- May over-explore in the beginning (high exploration bonus for all arms)
- Does not handle non-stationary environments well without modification

### Thompson Sampling (Posterior Sampling)

#### Algorithm

1. Maintain a probability distribution (posterior) for each arm's reward
2. Sample from each arm's posterior distribution
3. Choose the arm with the highest sampled value
4. Update the posterior with observed reward

#### For Bernoulli Rewards (Click/No-Click)

```
Prior: Beta(α, β) for each arm
After observing a click: Beta(α + 1, β)
After observing no click: Beta(α, β + 1)
Sample: Draw from Beta(α, β) for each arm
Select: Arm with highest sample
```

#### Advantages

- Naturally balances exploration and exploitation
- Adapts to changing environments (posteriors update continuously)
- Can incorporate prior knowledge (informative priors)
- Empirically outperforms UCB in many settings
- Easy to implement for common reward distributions

#### Bayesian Updating

| Reward Distribution | Prior | Update | Posterior |
|--------------------|-------|--------|-----------|
| Bernoulli (click/no-click) | Beta(α, β) | α += click, β += no-click | Beta(α', β') |
| Gaussian (ratings) | Normal(μ₀, σ₀²) | Update mean and variance | Normal(μ', σ'²) |
| Poisson (count data) | Gamma(α, β) | α += count, β += 1 | Gamma(α', β') |

---

## Contextual Bandits

### Motivation

Classic bandits assume arm performance is static. In recommendations, arm performance depends on context (user features, time, device). Contextual bandits use context to make personalized decisions.

### LinUCB (Linear Upper Confidence Bound)

#### Assumptions

- Expected reward is a linear function of context features: `E[r] = θ^T × x`
- Context features `x` are available for each decision

#### Algorithm

```
For each arm a:
  UCB_score_a = θ_a^T × x_a + α × √(x_a^T × A_a^{-1} × x_a)

Choose arm with highest UCB_score
Update: A_a += x_a × x_a^T, b_a += r × x_a
θ_a = A_a^{-1} × b_a
```

Where:
- `A_a`: d × d matrix (initialized to identity)
- `b_a`: d × 1 vector (initialized to zeros)
- `α`: Exploration parameter
- `d`: Feature dimensionality

#### Disjoint vs Hybrid LinUCB

| Variant | Description | Use Case |
|---------|-------------|----------|
| Disjoint | Separate θ per arm | Arms are independent items |
| Hybrid | Shared θ across arms + arm-specific features | Arms share structure (e.g., item categories) |

#### Scalability Considerations

- Matrix inversion `A_a^{-1}` is O(d³) per update — use Sherman-Morrison for O(d²) incremental update
- For large feature spaces, use low-rank approximations
- Distributed computation: maintain A_a and b_a per arm across parameter servers

### Neural Contextual Bandits

Use neural networks to model the reward function:

```
Context → Neural Network → Expected Reward per Arm
         (with uncertainty estimation)
```

Methods:
- **Neural UCB**: Use neural network with uncertainty from last layer
- **Neural Thompson Sampling**: Bayesian neural network or MC Dropout
- **Bootstrapped neural bandits**: Multiple neural networks trained on bootstrapped samples

---

## Exploration Strategies for Recommendations

### Exploration Types

| Type | Description | Example |
|------|-------------|---------|
| Item exploration | Try new items | Recommend newly added products |
| User exploration | Learn about new users | Show diverse items to new users |
| Context exploration | Learn context-reward mapping | Test different recommendations per context |
| Feature exploration | Learn feature importance | Try items with different attribute combinations |

### Thompson Sampling for Item Exploration

```
For each candidate item i:
  estimated_ctr_i ~ Beta(clicks_i + 1, non_clicks_i + 1)
  
Rank items by estimated_ctr samples
Return top-K
```

Items with fewer observations have wider posteriors, leading to more variable samples and thus more exploration.

### Exploration in Practice

#### Catalog-Level Exploration

- Reserve 5–15% of recommendation slots for exploration
- Use Thompson Sampling to allocate exploration budget across items
- Track exploration quality to ensure it converges to exploitation

#### User-Level Exploration

- New users: 50–80% exploration (high ε or broad posteriors)
- Active users: 5–10% exploration (mostly exploitation)
- Transition smoothly as user accumulates interaction data

#### Contextual Exploration

- Different exploration rates per context (time of day, device)
- Feature-based exploration: explore items with under-represented features
- Demographic exploration: ensure recommendations cover diverse user groups

### Cold Start with Bandits

#### New Item Cold Start

- Initialize new item with prior distribution (e.g., Beta(1, 1) uniform)
- Bandit naturally explores new items due to high uncertainty
- Prior can be informed by content features (similar items' performance)

#### New User Cold Start

- Start with high exploration rate
- Use contextual features (demographics, device, entry point) for initial decisions
- Gradually shift to personalized recommendations as data accumulates

#### Cold Start Timeline

```
Day 0-3: High exploration (ε=0.5 or wide Thompson posteriors)
Day 3-7: Moderate exploration (ε=0.2)
Day 7-14: Low exploration (ε=0.05)
Day 14+: Minimal exploration (ε=0.01, Thompson Sampling handles naturally)
```

---

## Non-Stationary Bandits

### Problem

In recommendations, reward distributions change over time (trending items, seasonal preferences, user behavior shifts).

### Sliding Window UCB

- Only consider rewards from the last W rounds
- Adapts to distribution changes
- Window size W controls adaptation speed

### Discounted UCB

- Apply a discount factor γ < 1 to older rewards
- `X̄_a = Σ γ^{t-s} × r_s / Σ γ^{t-s}` (where s indexes time steps)
- Exponentially downweights old observations

### Switching Bandits

- Explicitly model distribution change points
- Use change-point detection (e.g., CUSUM, Bayesian change-point detection)
- Reset posteriors when a change is detected

### Meta-Algorithm Approach

Maintain multiple bandit instances with different time horizons:

```
Bandit 1: Recent data only (fast adaptation)
Bandit 2: Medium-term data (balanced)
Bandit 3: Long-term data (stable)
Meta-bandit: Dynamically selects which bandit to follow
```

---

## Production Deployment

### Architecture

```
User Request → Context Extractor → Bandit Controller → Arm Selection
                                                          ↓
                                              ┌───────────┼───────────┐
                                              │           │           │
                                         Arm 1       Arm 2       Arm 3
                                       (CF model)  (Content)  (Trending)
                                                          ↓
                                              Reward Collector → Posterior Updater
```

### Arm Design

| Arm Type | Description | Reward Signal |
|----------|-------------|---------------|
| Algorithm arms | Different recommendation algorithms | CTR, conversion |
| Parameter arms | Different hyperparameter configurations | Quality metrics |
| Content type arms | Different content categories | Engagement |
| Ranking strategy arms | Different re-ranking approaches | User satisfaction |
| Exploration arms | Novelty/serendipity focused | Long-term retention |

### Logging and Monitoring

- Log every decision: context, chosen arm, reward, posterior state
- Track per-arm metrics: pull count, average reward, uncertainty
- Monitor convergence: are posteriors concentrating?
- Dashboard: arm performance over time, exploration rate, regret estimates

### Infrastructure Considerations

- **Latency**: Thompson Sampling with Beta distribution is O(K) for K arms
- **Storage**: Posterior parameters per arm (2 floats for Beta)
- **Consistency**: Ensure posterior updates are atomic (no race conditions)
- **Backfilling**: Handle delayed rewards (conversion may happen hours later)

---

## Evaluation

### Offline Evaluation

| Metric | Description | Ideal |
|--------|-------------|-------|
| Cumulative regret | Total missed reward | Minimize |
| Arm selection distribution | How often each arm is chosen | Converge to optimal |
| Convergence speed | Rounds to identify best arm | Fast |
| Robustness | Performance under distribution shift | Stable |

### Simulation Testing

- Create synthetic reward distributions
- Run bandit algorithms offline to compare
- Test with known optimal arms to measure regret
- Simulate non-stationary environments

### Online Evaluation

- Measure CTR, conversion, and revenue impact vs A/B test baseline
- Monitor exploration quality: are explored items better than exploit-only?
- Track long-term user engagement (not just immediate reward)
- Ensure guardrail metrics (load time, error rate) are not degraded

---

## Advanced Topics

### Combinatorial Bandits

- Select K items simultaneously (not just one)
- Consider joint effects of item combinations
- Applications: multi-slot recommendation pages

### Fairness-Aware Bandits

- Ensure exploration is distributed fairly across item categories
- Demographic parity constraints in arm selection
- Conservation constraints: every arm gets minimum exploration

### Bandits with Delayed Feedback

- Conversion may happen minutes to days after recommendation
- Use delayed reward updating
- Predictive models for immediate reward estimation

### Batched Bandits

- Make decisions in batches (not one at a time)
- More hardware-efficient (batch inference)
- Requires careful batch construction to maintain exploration
