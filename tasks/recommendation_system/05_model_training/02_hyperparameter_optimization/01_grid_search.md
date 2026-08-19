# Grid Search for Hyperparameter Optimization

## Overview

Grid search is the most straightforward approach to hyperparameter optimization: define a discrete set of values for each hyperparameter, exhaustively evaluate every combination, and select the configuration with the best validation performance. While conceptually simple, grid search has important properties—both strengths and limitations—that make it suitable or unsuitable depending on the problem context.

---

## Fundamentals of Grid Search

### Definition

Given hyperparameter spaces H₁, H₂, ..., Hₖ, grid search evaluates the model at every point in the Cartesian product H₁ × H₂ × ... × Hₖ. For each combination, a full training and evaluation cycle is performed.

### Parameter Grid Design

| Hyperparameter Type | Example Values | Grid Size |
|--------------------|----------------|-----------|
| Learning rate | [1e-2, 1e-3, 1e-4, 1e-5] | 4 |
| Batch size | [128, 256, 512, 1024] | 4 |
| Dropout rate | [0.1, 0.3, 0.5] | 3 |
| Embedding dim | [64, 128, 256, 512] | 4 |
| Num attention heads | [4, 8, 16] | 3 |

**Total combinations**: 4 × 4 × 3 × 4 × 3 = 576 experiments

### Grid Construction Principles

- Start with coarse grids spanning wide ranges; refine around promising regions
- Use logarithmic spacing for learning rates and regularization strengths
- Include boundary values (they are sometimes optimal)
- For categorical parameters (optimizer type, activation function), enumerate all options
- Consider interaction effects: some hyperparameters only matter in combination

---

## Parallelization of Grid Search

### Embarrassingly Parallel Execution

- Each grid point is independent; all can run simultaneously given sufficient resources
- Perfect for distributed computing: assign grid points across workers
- No inter-worker communication needed (pure parallelism)

### Parallel Execution Strategies

1. **Worker-based**: Each worker gets a subset of grid points; processes them sequentially
2. **Queue-based**: Central scheduler assigns next grid point to first available worker
3. **Batch-based**: Process grid points in batches; evaluate batch, then decide next batch (with early stopping)

### Resource Allocation

| Total Grid Points | Available GPUs | Runs per GPU | Total Batches | Wall Clock Time |
|-------------------|---------------|--------------|---------------|-----------------|
| 576 | 32 | 18 | 1 | 18 × single_run_time |
| 576 | 64 | 9 | 1 | 9 × single_run_time |
| 576 | 32 | 3 | 6 | 6 × single_run_time (with early stopping) |

### Parallelization Overhead

- No communication overhead between workers (independent runs)
- Shared data loading: ensure training data is accessible at high throughput (NFS, S3, local NVMe cache)
- Result aggregation: collect metrics from all workers after completion
- Failure handling: if a worker dies, reassign its remaining grid points

---

## Early Stopping Integration

### Principles

Early stopping terminates unpromising grid points before full training, saving compute resources.

### Strategies for Grid Search Early Stopping

1. **Fixed epoch threshold**: Stop all runs at the same epoch if validation metric hasn't improved
2. **Successive halving**: Allocate small budgets first, promote top performers to larger budgets
3. **Median pruning**: Stop runs whose validation metric is below the median of completed runs at the same epoch
4. **Statistical pruning**: Use hypothesis testing to determine if a run can be ruled out with confidence

### Integration with Grid Search

- Early stopping reduces total compute by 50-80% in practice
- Must be applied consistently: same stopping criterion for all grid points
- Risk: early stopping may incorrectly eliminate a configuration that would have improved later
- Mitigate: use generous patience (at least 10-20% of total epochs)

---

## Covering Interactions Between Hyperparameters

### Why Interactions Matter

Hyperparameter interactions occur when the optimal value of one hyperparameter depends on the value of another. Grid search naturally captures these because it evaluates all combinations.

### Common Interactions in Recommendation Models

| Hyperparameter A | Hyperparameter B | Interaction |
|------------------|------------------|------------|
| Learning rate | Batch size | Larger batches tolerate higher learning rates |
| Dropout rate | Model capacity | Larger models need more dropout |
| Embedding dim | Regularization strength | Larger embeddings need stronger regularization |
| Warmup steps | Learning rate | Higher LR needs longer warmup |
| Attention heads | Sequence length | More heads help with longer sequences |

### Detecting Interactions

- Plot 2D heatmaps of validation metric for pairs of hyperparameters
- Use ANOVA or mutual information to quantify interaction strength
- If interactions are strong, finer grid resolution is needed for those parameters
- If interactions are weak, consider searching parameters independently (factorial analysis)

---

## Curse of Dimensionality

### The Problem

Grid search scales exponentially with the number of hyperparameters. Each additional hyperparameter multiplies the total number of experiments by the grid resolution for that parameter.

| Hyperparameters | Grid Points per Param | Total Combinations |
|-----------------|----------------------|-------------------|
| 2 | 10 | 100 |
| 3 | 10 | 1,000 |
| 5 | 10 | 100,000 |
| 7 | 10 | 10,000,000 |
| 10 | 10 | 10,000,000,000 |

### Impact on Recommendation Systems

- Modern recommendation models have 10-20+ tunable hyperparameters
- Full grid search becomes infeasible beyond 5-6 parameters at reasonable resolution
- Many hyperparameters have weak effects; searching them wastes resources

### Mitigation Strategies

1. **Reduce dimensionality**: Fix obviously suboptimal parameters, tune only the top 5-7
2. **Coarse-to-fine**: Run coarse grid first, then fine grid around the best region
3. **Factorial design**: Test main effects with a fractional factorial design (O(n) instead of O(nᵏ))
4. **Sensitivity analysis**: Identify which parameters matter most; focus grid on those
5. **Hybrid approach**: Use grid search for categorical parameters, random search for continuous

---

## When to Use Grid Search

### Suitable Scenarios

- Small number of hyperparameters (≤ 5)
- Well-understood parameter ranges with known good values
- Need to comprehensively cover a specific region of parameter space
- Categorical parameters with few options (e.g., optimizer = {Adam, SGD, AdamW})
- Baseline comparison: grid search provides a thorough baseline for benchmarking

### Not Suitable Scenarios

- High-dimensional hyperparameter spaces (> 6 parameters)
- Continuous parameters requiring fine resolution
- Limited compute budget (random search is more sample-efficient)
- Non-smooth objective landscapes where grid alignment matters
- Time-constrained experiments where early stopping on a grid is less effective than successive halving

### Grid Search vs. Alternatives

| Factor | Grid Search | Random Search | Bayesian Optimization |
|--------|-------------|---------------|----------------------|
| Sample efficiency | Low | Medium | High |
| Parallelizability | Excellent | Excellent | Limited |
| Reproducibility | Deterministic | Random seed dependent | Implementation dependent |
| Coverage | Uniform | Random | Focused on promising regions |
| Interaction capture | Full | Partial | Learned |

---

## Best Practices for Grid Search in Practice

### Grid Design

- Use 3-5 values per hyperparameter for continuous parameters
- Include extreme values (they are sometimes optimal in recommendation models)
- Use logarithmic spacing for learning rates, regularization, and embedding dimensions
- For batch size, use powers of 2 (128, 256, 512, 1024, 2048)

### Execution

- Run at least 3 seeds per grid point for statistical significance
- Use consistent validation splits across all grid points
- Log all metrics (not just the primary metric) for post-hoc analysis
- Store complete model checkpoints for the top-K configurations

### Analysis

- Compute mean and standard deviation of validation metric across seeds
- Generate partial dependence plots for each hyperparameter
- Identify interaction effects via 2D heatmaps
- Report confidence intervals, not just point estimates
- Document negative results (which regions performed poorly and why)
