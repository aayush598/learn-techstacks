# Random Search for Hyperparameter Optimization

## Overview

Random search samples hyperparameter configurations randomly from specified distributions, rather than exhaustively evaluating a fixed grid. Despite its simplicity, random search is often more efficient than grid search because it explores more of the hyperparameter space with fewer evaluations, especially when only a few hyperparameters significantly affect performance.

---

## Benefits Over Grid Search

### Theoretical Foundation

Bergstra and Bengio (2012) demonstrated that random search is more efficient than grid search when the objective function is sensitive to only a few hyperparameters. This is because:

- Grid search wastes evaluations on grid points that differ only in irrelevant dimensions
- Random search explores each dimension independently, getting more unique values per evaluation
- For k important hyperparameters out of d total, random search needs O(log(n)) evaluations vs O(n^(d/k)) for grid search to find good configurations

### Practical Advantages

| Aspect | Grid Search | Random Search |
|--------|-------------|---------------|
| Unique values per dimension | Fixed (grid resolution) | Increases with more evaluations |
| Alignment bias | Grid may miss optimal points between grid lines | No alignment bias |
| Budget flexibility | Fixed total cost (grid size) | Can stop anytime with valid results |
| Exploration | Limited to grid points | Explores continuous space |
| Scaling | Exponential in dimensions | Linear in number of evaluations |

### Efficiency Analysis

Consider tuning 5 hyperparameters with 10 values each:
- Grid search: 100,000 evaluations, but only 10 unique values per parameter
- Random search with 1,000 evaluations: potentially 1,000 unique values per parameter
- Random search achieves 100x better coverage per dimension with 100x fewer evaluations

---

## Parameter Distributions

### Continuous Parameters

**Uniform Distribution**: `U(a, b)` — Equal probability across the range
- Use for: dropout rate, data augmentation probabilities
- Example: dropout ~ U(0.0, 0.5)

**Log-Uniform Distribution**: `logU(a, b)` — Equal probability across orders of magnitude
- Use for: learning rate, regularization strength, embedding dimensions
- Example: learning_rate ~ logU(1e-5, 1e-1)
- Critical for learning rate: covers [0.00001, 0.1] with equal density per decade

**Normal Distribution**: `N(μ, σ)` — Concentrated around mean
- Use for: parameters with a known good range and expected center
- Example: batch_size ~ N(256, 64) — cluster around 256

**Truncated Normal**: `TN(μ, σ, a, b)` — Normal bounded to [a, b]
- Use for: parameters with physical constraints (e.g., dropout ∈ [0, 1])

### Discrete Parameters

**Integer Uniform**: ` randint(a, b)` — Equal probability for each integer
- Use for: number of layers, attention heads, LSTM units
- Example: num_layers ~ randint(2, 8)

**Categorical**: Weighted random choice from a list
- Use for: optimizer type, activation function, normalization type
- Example: optimizer ~ {Adam: 0.4, AdamW: 0.3, SGD: 0.2, LAMB: 0.1}

### Parameter-Specific Distributions for Recommendation Models

| Hyperparameter | Distribution | Range | Rationale |
|----------------|-------------|-------|-----------|
| Learning rate | Log-uniform | [1e-5, 1e-1] | Orders of magnitude span |
| Embedding dim | Log-uniform integer | [16, 1024] | Wide range, exponential scaling |
| Dropout | Uniform | [0.0, 0.5] | Linear range, bounded |
| Batch size | Categorical (powers of 2) | [64, 128, 256, 512, 1024] | GPU memory alignment |
| Weight decay | Log-uniform | [1e-6, 1e-2] | Orders of magnitude span |
| Attention heads | Categorical | [2, 4, 8, 16] | Must be power of 2 (often) |
| Num layers | Integer uniform | [1, 12] | Small integer range |
| Warmup ratio | Uniform | [0.0, 0.2] | Percentage of total steps |

---

## Random Search Implementation Patterns

### Budget-Aware Random Search

- Define total compute budget in GPU-hours
- Estimate single-run cost (GPU-hours per full training)
- Number of random configurations = total budget / single-run cost
- Remaining budget used for final evaluation of top-K configurations

### Adaptive Random Search

1. Phase 1: Random search with N configurations
2. Phase 2: Analyze results; identify promising regions
3. Phase 3: Random search with M configurations in the narrowed region
4. Repeat phases 2-3 until budget is exhausted

### Stratified Random Search

- Partition continuous space into strata (e.g., learning rate decades: [1e-5, 1e-4], [1e-4, 1e-3], etc.)
- Sample uniformly within strata
- Ensures coverage across the full range even with few samples
- Particularly useful when good ranges are unknown

---

## Efficiency Analysis

### Convergence Properties

- Random search converges to the global optimum with probability 1 as evaluations → ∞
- Convergence rate depends on the fraction of important hyperparameters
- For recommendation models, typically 3-5 hyperparameters dominate performance
- With 5 important parameters and 100 random samples, you get ~100 unique values in each important dimension

### Comparison with Grid Search at Equal Budget

| Budget (evals) | Grid (5 params × 10 vals) | Random (5 params) |
|---------------|--------------------------|-------------------|
| 50 | 50/10000 (0.5%) | 50 unique points |
| 200 | 200/10000 (2%) | 200 unique points |
| 1000 | 1000/10000 (10%) | 1000 unique points |
| 10000 | 100% coverage | 10000 unique points |

At every budget level, random search explores more unique configurations.

### Statistical Confidence

- Random search allows natural confidence intervals via bootstrap resampling
- Multiple random seeds provide variance estimates
- Can quantify the probability of finding a configuration within X% of optimal
- Grid search provides no such statistical framework

---

## When to Prefer Random Search

### Strong Use Cases

- **Unknown parameter importance**: When you don't know which hyperparameters matter most
- **Continuous parameters**: When parameters are truly continuous and need fine-grained exploration
- **Limited budget**: When you can only afford a small number of evaluations
- **Baseline establishment**: Quick baseline before more sophisticated methods
- **Parallel execution**: Embarrassingly parallel like grid search

### Moderate Use Cases

- **Many hyperparameters**: Better than grid search for >6 parameters
- **Initial exploration phase**: Use random search first, then refine with Bayesian optimization
- **Categorical parameters with many options**: Naturally explores the full category space

### Not Ideal When

- **Budget is very large**: Bayesian optimization may be better with unlimited budget
- **Parameters have strong interactions**: Bayesian optimization captures interactions better
- **Real-time feedback needed**: Random search doesn't learn from past evaluations
- **Very few hyperparameters (≤ 3)**: Grid search may be sufficient

---

## Random Search in Recommendation Systems

### Common Tuning Targets

- **Embedding dimensions**: For user/item embedding tables (often log-uniform [32, 512])
- **Learning rate and schedule**: Peak LR, warmup steps, decay schedule
- **Feature interaction parameters**: Number of cross layers, attention heads, hidden dimensions
- **Regularization**: Dropout rates, weight decay, label smoothing
- **Training dynamics**: Batch size, gradient accumulation steps, number of epochs

### Multi-Objective Random Search

- Search for Pareto-optimal configurations across multiple metrics
- Example: maximize NDCG@10 while minimizing inference latency
- Use hypervolume indicator to rank random configurations
- Report Pareto front for stakeholder decision-making

### Best Practices

1. Always use log-uniform for learning rate and regularization parameters
2. Run at least 3 seeds per configuration for variance estimation
3. Use consistent validation protocol across all random evaluations
4. Track and report the full distribution of results, not just the best
5. Consider seeded random search for reproducibility (fix random seed per configuration)
