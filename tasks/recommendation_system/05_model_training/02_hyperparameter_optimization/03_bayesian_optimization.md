# Bayesian Optimization for Hyperparameter Optimization

## Overview

Bayesian Optimization (BO) is a sample-efficient strategy for optimizing black-box functions where evaluations are expensive. In recommendation systems, hyperparameter optimization (HPO) can involve training models that take hours or days per evaluation. Bayesian Optimization builds a probabilistic surrogate model of the objective function and uses an acquisition function to intelligently select the next hyperparameter configuration to evaluate, dramatically reducing the number of trials needed compared to grid search or random search.

---

## Problem Formulation

### The HPO Objective

```
x* = argmin_{x ∈ X} f(x)
```

Where:
- `x`: Hyperparameter configuration (vector of continuous, integer, and categorical values)
- `f(x)`: Objective function (e.g., negative NDCG@10 on validation set)
- `X`: Hyperparameter search space
- Evaluations of `f(x)` are expensive (hours of GPU training)

### Search Space Design for Recommendations

| Hyperparameter | Type | Typical Range | Log-scale? |
|---------------|------|---------------|------------|
| Learning rate | Continuous | 1e-5 to 1e-1 | Yes |
| Embedding dimension | Integer | 32 to 512 | No |
| Number of layers | Integer | 1 to 8 | No |
| Dropout rate | Continuous | 0.0 to 0.5 | No |
| Batch size | Categorical | {64, 128, 256, 512, 1024} | No |
| Weight decay | Continuous | 1e-6 to 1e-2 | Yes |
| Negative sampling ratio | Integer | 1 to 100 | Yes |
| Sequence length | Integer | 10 to 200 | No |

---

## Gaussian Process Surrogate

### Core Idea

A Gaussian Process (GP) models the objective function as a distribution over functions, providing both mean predictions and uncertainty estimates at any point in the search space.

### GP Definition

A GP is fully defined by its mean function `μ(x)` and covariance (kernel) function `k(x, x')`:

```
f(x) ~ GP(μ(x), k(x, x'))
```

For observed points `X_obs = {x₁, ..., xₙ}` with values `y = [f(x₁), ..., f(xₙ)]`:

```
Predictive distribution at new point x*:
  μ(x*) = k(x*, X_obs) [K(X_obs, X_obs) + σ²I]⁻¹ y
  σ²(x*) = k(x*, x*) - k(x*, X_obs) [K(X_obs, X_obs) + σ²I]⁻¹ k(X_obs, x*)
```

Where `K(X_obs, X_obs)` is the kernel matrix and `σ²` is observation noise.

### Kernel Choice

| Kernel | Formula | Properties | When to Use |
|--------|---------|-----------|-------------|
| Matérn 5/2 | `(1 + √5r + 5r²/3) exp(-√5r)` | Smooth, common default | General purpose |
| RBF (Squared Exponential) | `exp(-r²/2l²)` | Very smooth | Smooth objectives |
| Matérn 3/2 | `(1 + √3r) exp(-√3r)` | Less smooth | Noisy objectives |
| Rational Quadratic | `(1 + r²/(2αl²))^(-α)` | Mixture of RBFs | Multiple length scales |

### GP Limitations for High Dimensions

- GP scales as O(n³) in number of observations (n = number of trials)
- Kernels struggle in dimensions > 20
- Cannot handle categorical hyperparameters natively (require encoding)

### Practical Mitigations

- **Low-dimensional projections**: Optimize subsets of hyperparameters
- **ARD (Automatic Relevance Determination)**: Learn per-dimension length scales
- **Sparse GP approximations**: Use inducing points to reduce computation
- **Categorical encoding**: One-hot or embedding for categorical parameters

---

## Acquisition Functions

Acquisition functions determine which point to evaluate next by balancing exploration and exploitation.

### Expected Improvement (EI)

```
EI(x) = E[max(f(x) - f(x⁺), 0)]
```

Where `f(x⁺)` is the best observed value.

**Properties:**
- Favors points with high expected improvement over current best
- Naturally balances exploration (uncertain regions) and exploitation (good regions)
- Analytical form available for GP surrogate
- Can be noisy when the objective is noisy

### Upper Confidence Bound (UCB)

```
UCB(x) = μ(x) + κ × σ(x)
```

Where `κ` controls the exploration-exploitation tradeoff.

**Properties:**
- Simple to compute and understand
- `κ` is a tunable hyperparameter (typically 2.0–3.0)
- `κ = 0`: Pure exploitation
- `κ → ∞`: Pure exploration
- Commonly used with linearly increasing `κ` over time

### Probability of Improvement (PI)

```
PI(x) = P(f(x) > f(x⁺) + ξ)
```

Where `ξ` is a small positive constant (exploration parameter).

**Properties:**
- Can get stuck in local optima (aggressive exploitation)
- Less commonly used than EI or UCB
- Useful when you want to focus on improving the best known result

### Thompson Sampling

```
Sample f_sample from GP posterior
x_next = argmax_x f_sample(x)
```

**Properties:**
- Simple to implement
- Naturally balances exploration and exploitation
- Can be used with any surrogate model (not just GP)
- Works well in practice

### Comparison

| Function | Exploration | Computation | Robustness | Best For |
|----------|------------|-------------|------------|----------|
| EI | Balanced | Moderate | Good | Most HPO tasks |
| UCB | Tunable | Low | Very Good | When control is desired |
| PI | Low (aggressive) | Low | Moderate | Local refinement |
| Thompson | Balanced | Low | Good | General purpose |

### Handling Multi-Objective

When optimizing multiple objectives (e.g., accuracy and latency):

```
Multi-objective EI:
  EI(x) = E[max(s(x) - s(x⁺), 0)]
  where s(x) = weighted combination of objectives

Pareto-based:
  Optimize Pareto front of non-dominated solutions
  Use hypervolume improvement as acquisition function
```

---

## Optuna Integration

### Why Optuna

Optuna is a modern HPO framework that supports Bayesian optimization (among other strategies) with a clean API, efficient pruning, and distributed execution.

### Basic Usage

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    n_layers = trial.suggest_int("n_layers", 1, 4)
    embedding_dim = trial.suggest_categorical("embedding_dim", [64, 128, 256])
    dropout = trial.suggest_float("dropout", 0.0, 0.5)
    
    model = build_model(n_layers, embedding_dim, dropout)
    score = train_and_evaluate(model, lr)
    return score  # Optuna minimizes by default; negate for maximization

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)
```

### Optuna Samplers

| Sampler | Strategy | Best When |
|---------|----------|-----------|
| TPESampler | Tree-Parzen Estimator (default) | Most cases |
| GP sampler | Gaussian Process | Low-dimensional, continuous |
| CMA-ES | Evolutionary strategy | Continuous spaces |
| RandomSampler | Random search | Baseline / high-dimensional |
| GridSampler | Grid search | Small discrete spaces |

### Pruning with Optuna

Stop unpromising trials early to save compute:

```python
def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    
    model = build_model(lr)
    for epoch in range(100):
        train_epoch(model)
        score = evaluate(model)
        trial.report(score, epoch)
        
        if trial.should_prune():
            raise optuna.TrialPruned()
    
    return score

study = optuna.create_study(
    pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=10)
)
```

### Pruning Strategies

| Strategy | Description | Sensitivity |
|----------|-------------|------------|
| MedianPruner | Prune if below median of past trials | Moderate |
| HyperbandPruner | Successive halving with early stopping | Aggressive |
| SuccessiveHalvingPruner | Multi-fidelity pruning | Aggressive |
| PercentilePruner | Prune below configurable percentile | Tunable |
| NoPruner | No pruning | Conservative |

### Distributed HPO

```python
# Run optimization across multiple machines
study = optuna.create_study(storage="sqlite:///db.sqlite3")
study.optimize(objective, n_trials=1000, n_jobs=4)
```

Optuna handles trial deduplication and concurrent access automatically.

### Visualization and Analysis

- **Optimization history**: Objective value vs trial number
- **Parameter importance**: Which hyperparameters matter most
- **Parallel coordinate plot**: How hyperparameters interact
- **Slice plot**: Objective vs individual hyperparameters
- **Contour plot**: Objective vs two hyperparameters

---

## Multi-Objective Optimization

### Pareto Front

When optimizing multiple conflicting objectives (e.g., NDCG vs serving latency):

```
Solution A: NDCG=0.85, Latency=50ms  ← Pareto optimal
Solution B: NDCG=0.82, Latency=20ms  ← Pareto optimal
Solution C: NDCG=0.80, Latency=55ms  ← Dominated by A
```

### Multi-Objective Optuna

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    n_layers = trial.suggest_int("n_layers", 1, 6)
    
    ndcg = train_and_get_ndcg(lr, n_layers)
    latency = measure_latency(n_layers)
    
    return ndcg, latency  # Two objectives

study = optuna.create_study(directions=["maximize", "minimize"])
study.optimize(objective, n_trials=200)

# Get Pareto front
pareto_front = study.best_trials  # All non-dominated solutions
```

### Scalarization Methods

Convert multi-objective to single-objective:

| Method | Formula | Properties |
|--------|---------|-----------|
| Weighted sum | `s = Σ w_i × obj_i` | Simple, but misses concave Pareto regions |
| Chebyshev | `s = min_i(w_i × |obj_i - z_i*|)` | Better Pareto coverage |
| ε-constraint | Optimize one, constrain others | Precise constraint control |
| Tchebycheff | Modified Chebyshev with utopia point | Good general-purpose |

---

## Early Stopping with Pruning

### Multi-Fidelity Optimization

Instead of fully training every configuration, use cheaper approximations:

| Approach | Description | Speedup |
|----------|-------------|---------|
| Learning curves | Early stopping based on validation trend | 2-5× |
| Subset training | Train on 10% of data, promote best | 10× |
| Lower resolution | Smaller images, shorter sequences | 2-4× |
| Fewer epochs | Train for fewer epochs initially | N× |

### Successive Halving

```
Start with N configurations, B budget each
Evaluate all N, keep top N/2
Double budget for survivors: 2B
Repeat until one configuration remains

Example: 64 trials → 32 → 16 → 8 → 4 → 2 → 1
Total budget: 64B (vs 64 × full budget)
```

### Hyperband

Combines random search with successive halving:

```
Run R successive halving rounds with different starting budgets:
Round 1: 81 trials × 1 epoch → keep top 27
Round 2: 27 trials × 3 epochs → keep top 9
Round 3: 9 trials × 9 epochs → keep top 3
Round 4: 3 trials × 27 epochs → keep top 1

Best result across all rounds
```

---

## Practical Guidelines

### Starting Points

1. **Random search first**: Run 20-50 random trials to understand the landscape
2. **Then Bayesian optimization**: Use BO for guided search in promising regions
3. **Domain knowledge**: Set informative priors on hyperparameters you understand

### Budget Allocation

| Total Budget | Recommended Strategy |
|-------------|---------------------|
| < 20 trials | Random search |
| 20-100 trials | Bayesian optimization |
| 100-500 trials | BO with pruning |
| > 500 trials | Distributed BO + multi-fidelity |

### Common Mistakes

- **Too large search space**: Narrow down with prior knowledge
- **Ignoring interaction effects**: BO handles this better than grid/random
- **Not enough warm-up**: Start with 5-10 random trials before BO kicks in
- **Wrong metric**: Optimize the metric that correlates with online performance
- **Overfitting validation**: Use nested cross-validation for final model selection

### Reproducibility

- Set random seeds for all sources of randomness
- Log all trial configurations and results
- Record the optimization history for analysis
- Store surrogate model parameters for post-hoc analysis
