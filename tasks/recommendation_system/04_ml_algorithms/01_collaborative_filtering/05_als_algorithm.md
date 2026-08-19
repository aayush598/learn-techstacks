# Alternating Least Squares (ALS) Deep Dive

## Overview

Alternating Least Squares (ALS) is an optimization algorithm for matrix factorization that alternates between fixing one factor matrix and solving for the other. ALS is particularly popular for recommendation systems because it parallelizes naturally, has no learning rate to tune, and provides a closed-form solution at each iteration. It is the default MF algorithm in Apache Spark MLlib and is widely used for large-scale implicit feedback recommendations.

---

## Mathematical Formulation

### Objective Function

ALS minimizes the regularized squared error on observed entries:

**L(P, Q) = Σ_{(u,i)∈Ω} (r_ui - p_u · q_i^T)² + λ(Σ_u ||p_u||² + Σ_i ||q_i||²)**

Where:
- **Ω**: Set of observed (user, item) pairs.
- **P**: User factor matrix (|U| × k).
- **Q**: Item factor matrix (|I| × k).
- **k**: Latent dimension.
- **λ**: Regularization parameter.

### Alternating Optimization

The key insight: fixing Q, the objective is quadratic in P (and vice versa). Each sub-problem has a closed-form solution.

**Step 1: Fix Q, solve for P**

For each user u, the optimal p_u is:

**p_u = (Q_u^T Q_u + λI)^{-1} Q_u^T r_u**

Where:
- **Q_u**: The rows of Q corresponding to items that user u has interacted with.
- **r_u**: The ratings/interactions for user u.
- **Q_u^T Q_u**: k × k matrix (small, since k is typically 50–200).
- **Inversion**: O(k³) per user—tractable even for millions of users.

**Step 2: Fix P, solve for Q**

Symmetrically, for each item i:

**q_i = (P_i^T P_i + λI)^{-1} P_i^T r_i**

Where P_i is the rows of P corresponding to users who interacted with item i.

### Convergence Properties

- **Monotonic decrease**: Each ALS step provably reduces (or maintains) the objective. This is because each sub-problem is solved optimally.
- **Bounded below**: The objective is non-negative (sum of squared errors + regularization), so monotonic decrease implies convergence.
- **Convergence rate**: Linear convergence. The convergence rate depends on the condition number of the factor matrices. Well-conditioned problems converge in 10–20 iterations.
- **Local minima**: ALS converges to a local minimum (the objective is non-convex jointly in P and Q). Different initializations may converge to different local minima.

---

## Parallelization

### Natural Parallelism

ALS is embarrassingly parallel—each user (or item) factor can be updated independently once the other factor matrix is fixed.

**User-level parallelism (Step 1):**
- Distribute users across workers.
- Each worker holds a partition of P and the full Q (or the relevant rows of Q).
- Each worker computes p_u for its assigned users independently.
- Synchronize: gather all updated p_u values.

**Item-level parallelism (Step 2):**
- Distribute items across workers.
- Each worker holds a partition of Q and the full P (or the relevant rows of P).
- Each worker computes q_i for its assigned items independently.
- Synchronize: gather all updated q_i values.

### Communication Patterns

| Pattern | Description | Cost |
|---|---|---|
| **All-gather** | Each worker broadcasts its updated factors | O(n × k × p) where p = number of workers |
| **Shuffle** | Workers exchange factor rows needed for the next step | O(|Ω| × k) |
| **Broadcast** | Central coordinator distributes the full factor matrix | O(n × k × p) |

### Partitioning Strategies

**Block decomposition**: Partition both users and items into blocks. Process blocks independently, with periodic cross-block synchronization. This reduces communication but may slow convergence.

**Row-wise partitioning**: Each worker stores complete rows of P or Q. Updates are local. Communication is limited to aggregating partial results.

### Spark MLlib ALS Parallelism

Spark's ALS uses a hybrid approach:

1. **Rating blocks**: Ratings are partitioned into blocks based on user and item partitions.
2. **Coordinate descent**: Within each block, factors are updated using coordinate descent.
3. **Cross-block communication**: After processing local blocks, workers exchange factor updates.
4. **Checkpointing**: Factor matrices are checkpointed to enable fault tolerance.

---

## Implicit Feedback Variant (Hu/Koren/Volinsky)

### The Implicit Feedback Problem

In implicit feedback settings, there are no explicit ratings—only observations of user behavior (clicks, views, purchases, time spent). The key challenges:

- **No negative feedback**: Absence of interaction doesn't mean dislike—it may mean the user never discovered the item.
- **Confidence varies**: A user who clicked an item once has less confidence than a user who purchased it 10 times.
- **Asymmetric meaning**: Observing an interaction is positive evidence; not observing is uncertain.

### Weighted ALS Formulation

Hu, Koren, and Volinsky (2008) proposed:

**Minimize: Σ_{u,i} c_ui (p_ui - x_u · y_i)² + λ(Σ_u ||x_u||² + Σ_i ||y_i||²)**

Where:
- **p_ui**: Binarized preference: p_ui = 1 if r_ui > 0, else p_ui = 0.
- **c_ui**: Confidence: c_ui = 1 + α × r_ui. Higher interaction count → higher confidence.
- **x_u**: User factor.
- **y_i**: Item factor.

### Intuition

- The model learns binary preferences (like/not-like) weighted by confidence.
- Items the user interacted with many times have higher confidence and pull the user factor more strongly.
- Items the user never interacted with have low confidence (c_ui = 1) and have minimal influence.

### ALS Solution for Implicit Feedback

The closed-form solution for the implicit variant:

**x_u = (Y^T C_u Y + λI)^{-1} Y^T C_u p_u**

Where:
- **C_u**: Diagonal matrix of confidence values for user u.
- **p_u**: Binary preference vector for user u.
- **Y**: Item factor matrix.

The difference from explicit ALS: C_u weights the contributions differently—high-confidence items dominate the factor update.

### Scaling Confidence

The confidence parameter α controls how much weight is given to interaction counts:

| α Value | Effect |
|---|---|
| α = 1 | Linear confidence scaling (default) |
| α < 1 | Compress confidence range (less sensitivity to count differences) |
| α > 1 | Expand confidence range (more sensitivity to count differences) |
| α = 0 | Binary only (all interactions treated equally) |

---

## Spark MLlib ALS

### Configuration

| Parameter | Description | Recommended Range |
|---|---|---|
| `rank` | Latent dimension k | 50–200 |
| `numIterations` | Number of ALS iterations | 10–20 |
| `lambda` | Regularization parameter | 0.01–1.0 |
| `implicitPrefs` | Use implicit feedback formulation | true for implicit data |
| `alpha` | Confidence scaling for implicit | 1.0–100.0 |
| `nonnegative` | Constrain factors to non-negative | true for interpretability |
| `regParam` | Regularization (alias for lambda) | 0.01–1.0 |

### Spark-Specific Considerations

- **Checkpointing**: Enable checkpointing for iterative algorithms to avoid stack overflow from lineage growth.
- **Block dimensions**: Configure `userBlocks` and `itemBlocks` to control partitioning. More blocks = more parallelism but more communication.
- **Cachedratings**: Ratings are cached in memory for efficient access during iterations. Ensure sufficient memory for the rating matrix.
- **Cold start strategy**: Set `coldStartStrategy` to "drop" or "nan" to handle users/items not seen during training.

### Training Pipeline

1. **Prepare data**: Convert interactions to Rating objects (user, item, rating).
2. **Split data**: Train/validation/test split (e.g., 70/10/20).
3. **Train model**: `ALS.train(ratings, rank, numIterations, lambda)`.
4. **Evaluate**: Compute RMSE, MAP, or NDCG on the validation set.
5. **Hyperparameter search**: Grid search over rank, lambda, alpha.
6. **Retrain**: Train on full training data with best hyperparameters.
7. **Serve**: Generate factor matrices for online serving.

---

## Hyperparameter Tuning

### Key Hyperparameters

| Hyperparameter | Search Range | Impact |
|---|---|---|
| **Rank (k)** | [10, 50, 100, 200, 500] | Higher = more expressive, more overfitting risk |
| **Regularization (λ)** | [0.001, 0.01, 0.1, 1.0, 10.0] | Higher = more regularization, less overfitting |
| **Iterations** | [10, 15, 20, 30] | More = better convergence, diminishing returns |
| **Alpha (implicit)** | [1.0, 10.0, 40.0, 100.0] | Controls confidence scaling |

### Tuning Strategy

1. **Coarse grid search**: Explore a wide range of values to identify the promising region.
2. **Fine grid search**: Narrow down within the promising region.
3. **Cross-validation**: Use k-fold cross-validation (k=5) to estimate generalization performance.
4. **Early stopping**: Stop training when validation loss stops improving. This acts as implicit regularization.

### Regularization vs. Rank Tradeoff

| Rank | Regularization Needed | Effect |
|---|---|---|
| Low (10–50) | Low | Captures coarse-grained patterns |
| Medium (50–200) | Moderate | Balanced expressiveness and generalization |
| High (200–500) | High | Captures fine-grained patterns, risk overfitting |

---

## Convergence Criteria

### When to Stop ALS

| Criterion | Description | Trade-off |
|---|---|---|
| **Fixed iterations** | Stop after N iterations | Simple, may over/under-train |
| **Validation loss plateau** | Stop when validation loss stops decreasing | Prevents overfitting, requires held-out data |
| **Training loss tolerance** | Stop when objective decrease < ε | May stop before convergence |
| **Factor change tolerance** | Stop when factor change < ε | Measures actual convergence |
| **Time budget** | Stop after a fixed time | Practical for production |

### Monitoring Convergence

- **Objective function**: Plot L(P,Q) per iteration. Should decrease monotonically.
- **Validation RMSE**: Plot per iteration. Should decrease then plateau.
- **Factor norm change**: ||P_new - P_old|| / ||P_old||. Should decrease toward zero.
- **Rank of factor matrices**: Monitor the effective rank to detect overfitting (effective rank approaching k).

### Common Pitfalls

- **Too few iterations**: Model undertrained, poor accuracy.
- **Too many iterations**: Wasted computation after convergence, potential overfitting.
- **Wrong initialization**: Different initializations may converge to different local minima. Try multiple initializations and keep the best.
- **Insufficient regularization**: Factors grow unboundedly, overfitting to noise.
- **Too much regularization**: Factors are too constrained, underfitting.
