# Multi-Armed Bandits for Experiments

## Overview

Multi-armed bandits (MAB) adaptively allocate traffic to experiment variants based on observed performance, unlike A/B testing which uses fixed allocation. Bandits maximize cumulative reward during the experiment by shifting traffic toward better-performing variants while still exploring alternatives. This covers epsilon-greedy, Thompson Sampling, UCB, contextual bandits, and regret minimization.

---

## Epsilon-Greedy Algorithm

### Mechanism

With probability ε, explore a random variant; with probability 1-ε, exploit the current best variant.

### Variants

| Strategy | ε Value | Behavior |
|----------|---------|----------|
| Fixed ε | 0.1 | 10% exploration, 90% exploitation |
| Decaying ε | ε = 1/√t | Exploration decreases over time |
| Adaptive ε | Based on uncertainty | More exploration when uncertain |

### Properties

- **Simple to implement**: Just need to track average reward per variant
- **Tunable**: ε controls exploration-exploitation trade-off
- **No convergence guarantee**: May keep exploring forever with fixed ε
- **Good for**: Quick experiments, non-stationary environments

### Limitations

- Explores uniformly even when variants are clearly different
- Doesn't use uncertainty information to guide exploration
- May over-explore good variants and under-explore promising ones
- Fixed ε doesn't adapt to experiment progress

---

## Thompson Sampling

### Mechanism

Sample from posterior distribution of each variant's reward; select variant with highest sampled value.

### Algorithm

1. Initialize prior distribution for each variant (e.g., Beta(1,1) for binary rewards)
2. For each request:
   - Sample reward from posterior for each variant
   - Select variant with highest sampled value
   - Observe actual reward
   - Update posterior with observed reward

### Bayesian Update

For binary rewards (click/no-click):
```
Prior: Beta(α, β)
After success: Beta(α + 1, β)
After failure: Beta(α, β + 1)
Posterior mean: α / (α + β)
```

### Properties

- **Posterior sampling**: Naturally balances exploration and exploitation
- **Uncertainty-aware**: High uncertainty → more exploration
- **Converges**: Identifies best variant with probability 1
- **Anytime valid**: Can stop experiment at any point

### Advantages for Recommendations

- Naturally handles varying traffic volumes per variant
- Provides posterior probability of each variant being best
- Can incorporate prior knowledge (Beta prior parameters)
- Works well with delayed feedback (update when conversion observed)

---

## Upper Confidence Bound (UCB)

### UCB1 Algorithm

Select variant that maximizes:
```
UCB_i = X̄_i + c × √(ln(N) / N_i)
```

Where:
- X̄_i = average reward of variant i
- N_i = times variant i was selected
- N = total selections across all variants
- c = exploration parameter (typically √2)

### Properties

- **Optimistic exploration**: Selects variants with high upper bound
- **Diminishing exploration**: Less explored variants get bonus
- **Theoretical guarantees**: Logarithmic regret bound
- **Deterministic**: Same history → same decision (no sampling)

### UCB Variants

| Variant | Key Change | Benefit |
|---------|-----------|---------|
| UCB1 | Standard formula | Simple, effective |
| UCB-V | Variance-adjusted | Better for variable rewards |
| Discounted UCB | Weight recent observations | Handles non-stationary |
| Sliding window UCB | Only uses recent window | Adapts to concept drift |

---

## Contextual Bandits

### Concept

Use user context (features) to make personalized variant selection decisions. Each user-context pair is a separate bandit problem, but they share information through the context model.

### Architecture

```
User Context → Context Model → Variant Selection → Reward → Update Model
```

### Context Features for Recommendations

- User demographics (age, location, device)
- User behavior history (recent clicks, purchases)
- Item attributes (category, price, popularity)
- Contextual signals (time of day, day of week)
- Session features (pages viewed, time on site)

### LinUCB

For linear contextual bandits:
```
UCB_a = θ_a^T × x + α × √(x^T × A_a^{-1} × x)
```

Where x is the context vector and A_a is the design matrix for arm a.

### Neural Bandits

- Use neural network to model reward as function of context and variant
- More expressive than linear models
- Handle non-linear context-reward relationships
- Requires more data to train effectively

### Application to Recommendation Experiments

- Select model variant based on user features
- Users likely to benefit from new model get it more often
- Users unlikely to benefit keep seeing control
- Adapts allocation to maximize aggregate reward

---

## Regret Minimization

### Definition

Regret = (reward from optimal variant) - (reward from selected variant)

Cumulative regret over T rounds: R_T = Σ (r* - r_t)

### Regret Bounds

| Algorithm | Regret Bound | Asymptotic |
|-----------|-------------|-----------|
| Epsilon-greedy (fixed ε) | O(T) | Does not converge |
| Epsilon-greedy (decaying) | O(√T log T) | Converges |
| UCB1 | O(√T log T) | Converges |
| Thompson Sampling | O(√T) | Converges (optimal) |

### Minimizing Regret in Practice

- Use Thompson Sampling for best theoretical regret bounds
- Monitor cumulative regret during experiment
- Compare against oracle (always pick best variant)
- Stop experiment when regret plateaus

---

## Adaptive Allocation

### Dynamic Traffic Shifting

Based on observed performance, continuously adjust traffic allocation:

**Performance-Based Shifting**:
- Allocate more traffic to variants with higher observed reward
- Maintain minimum exploration for all variants
- Gradually shift as confidence in rankings increases

**Bayesian Shifting**:
- Use posterior probabilities to set allocation
- Allocate proportionally to P(variant is best)
- Naturally balances exploration and exploitation

### Switching Strategies

| Strategy | Trigger | Action |
|----------|---------|--------|
| Gradual shift | Performance difference observed | Slowly increase allocation to winner |
| Hard switch | Statistical significance reached | Move all traffic to winner |
| Soft switch | Confidence threshold met | Keep small % for continued monitoring |
| Adaptive | Posterior updates | Continuous allocation adjustment |

---

## When to Use Bandits vs A/B Testing

### Use Bandits When

- Experiment duration is costly (lost revenue during test)
- User experience matters during experiment
- Rapid iteration is needed
- Environment is non-stationary (concept drift)
- Many variants to test simultaneously

### Use A/B Testing When

- Statistical rigor is paramount
- Regulatory or compliance requirements
- Need to measure precise effect sizes
- Experiment has clear termination criteria
- Network effects require strict isolation

### Hybrid Approach

1. **Bandit phase**: Quickly identify promising variants
2. **A/B phase**: Rigorously validate top candidates
3. **Deployment**: Deploy validated winner with monitoring

---

## Implementation Considerations

### Tracking Requirements

- Reward signal must be available quickly (click, conversion)
- Handle delayed rewards (conversion may happen hours later)
- Track variant assignment and reward jointly
- Maintain running statistics per variant

### Practical Tips

- Start with Thompson Sampling (best balance of simplicity and performance)
- Set minimum exploration per variant (at least 5% initially)
- Monitor forreward hacking (variants optimizing for proxy metrics)
- Log all decisions for post-hoc analysis
- Combine with statistical testing for final deployment decisions
