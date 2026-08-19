# Matrix Factorization for Recommendations

## Overview

Matrix factorization (MF) decomposes the user-item interaction matrix into low-rank factor matrices, revealing latent features that capture user preferences and item characteristics. MF is the foundation of modern collaborative filtering and won the Netflix Prize competition. It addresses the sparsity problem of neighbor-based methods by learning a dense, continuous representation of users and items in a shared latent space.

---

## Mathematical Foundation

### The User-Item Matrix

The interaction matrix R has dimensions |U| × |I|, where R_ui represents user u's interaction with item i. In explicit feedback, R_ui is a rating (1–5 stars). In implicit feedback, R_ui is a count (clicks, views, purchases) or binary indicator.

**Key challenge**: R is extremely sparse—typically < 1% of entries are observed. MF must predict the unobserved entries.

### Low-Rank Factorization

MF approximates R as the product of two low-rank matrices:

**R ≈ P × Q^T**

Where:
- **P** (|U| × k): User factor matrix. Each row p_u is a k-dimensional vector representing user u.
- **Q** (|I| × k): Item factor matrix. Each row q_i is a k-dimensional vector representing item i.
- **k**: Latent dimension (typically 50–200). Trades off expressiveness vs. overfitting.

The predicted rating for user u and item i is: **r̂_ui = p_u · q_i^T**

### Objective Function

MF minimizes the regularized squared error on observed entries:

**L = Σ_{(u,i)∈observed} (r_ui - p_u · q_i^T)² + λ(||p_u||² + ||q_i||²)**

The regularization term (λ) prevents overfitting by penalizing large factor values.

---

## Variants of Matrix Factorization

### SVD (Singular Value Decomposition)

SVD decomposes a matrix into U × Κ × V^T. For recommendation:

1. Fill missing values with a default (e.g., global mean).
2. Compute SVD of the filled matrix.
3. Truncate to the top-k singular values/vectors.

**Limitations:**
- Cannot handle missing values natively—imputation biases the result.
- Computationally expensive for large matrices: O(min(mn², m²n)).
- Not suitable for online learning or incremental updates.

### Funk SVD

Simon Funk's approach (popularized by the Netflix Prize) learns P and Q directly from observed entries using stochastic gradient descent (SGD):

**For each observed (u, i, r_ui):**
1. Compute prediction: r̂_ui = p_u · q_i^T
2. Compute error: e_ui = r_ui - r̂_ui
3. Update factors: p_u ← p_u + η(e_ui · q_i - λp_u), q_i ← q_i + η(e_ui · p_u - λq_i)

**Advantages over classical SVD:**
- Handles missing values naturally—only trains on observed entries.
- Scalable to very large matrices via mini-batch SGD.
- Can incorporate biases, side information, and custom loss functions.

### Biased MF

Add global, user, and item biases to capture systematic rating patterns:

**r̂_ui = μ + b_u + b_i + p_u · q_i^T**

Where:
- **μ**: Global average rating.
- **b_u**: User bias (some users rate higher/lower on average).
- **b_i**: Item bias (some items receive higher/lower ratings on average).

Biased MF significantly improves accuracy by capturing these first-order effects before modeling latent interactions.

---

## Optimization Methods

### Stochastic Gradient Descent (SGD)

SGD updates factors one observation at a time (or in mini-batches):

**Update rule**: θ ← θ - η∇L(θ)

**Advantages:**
- Simple to implement and tune.
- Fast convergence for moderate-sized problems.
- Easily extensible to custom loss functions and regularizers.

**Hyperparameters:**
- **Learning rate (η)**: Typically 0.001–0.01. Use learning rate schedules or adaptive optimizers (Adam, Adagrad).
- **Regularization (λ)**: Typically 0.01–0.1. Tune via cross-validation.
- **Epochs**: 10–50 typically sufficient. Monitor validation loss for early stopping.
- **Factor initialization**: Random initialization from a normal distribution with small standard deviation (0.01–0.1).

### Alternating Least Squares (ALS)

ALS alternates between fixing P and optimizing Q, then fixing Q and optimizing P. Each sub-problem is a regularized least squares problem with a closed-form solution.

**Advantages over SGD:**
- Parallelizable—each user (or item) factor can be updated independently.
- No learning rate to tune.
- Convergence is guaranteed (monotonically decreasing objective).

**Disadvantages:**
- Each iteration is more expensive than an SGD step.
- Requires matrix operations that may not fit in memory for very large problems.
- Less flexible for custom loss functions.

### Weighted ALS (for Implicit Feedback)

For implicit feedback (clicks, views, purchases), the interaction matrix contains counts rather than ratings. Weighted ALS (Hu, Koren, Volinsky, 2008) transforms the problem:

**Minimize: Σ_{u,i} c_ui (p_ui - x_u · y_i)² + λ(Σ_u ||x_u||² + Σ_i ||y_i||²)**

Where:
- **p_ui**: Binarized preference (1 if r_ui > 0, else 0).
- **c_ui**: Confidence in the preference: c_ui = 1 + α × r_ui (higher count → higher confidence).
- **x_u**: User factor (analogous to p_u in explicit MF).
- **y_i**: Item factor (analogous to q_i in explicit MF).

The key insight: observed non-interactions are not absence of preference but low-confidence evidence. Confidence weighting gives more importance to frequently interacted items.

---

## Advanced Loss Functions

### BPR (Bayesian Personalized Ranking)

BPR optimizes for ranking quality rather than rating prediction:

**Loss = -Σ_{(u,i,j)} ln σ(x̂_uij)**

Where:
- (u, i, j) is a triplet: user u, positive item i, negative item j.
- x̂_uij = x̂_ui - x̂_uj (score difference between positive and negative items).
- σ is the sigmoid function.

BPR learns to rank positive items above negative items, which is more aligned with the actual recommendation objective than minimizing squared error.

### WARP (Weighted Approximate-Rank Pairwise)

WARP optimizes for top-K ranking quality by focusing on the items that matter most:

**Loss = Σ_u Σ_i max(0, 1 - σ(x̂_ui - x̂_uj) + margin)**

Where j is the highest-ranked negative item that is ranked above the positive item i. WARP uses a hinge loss with a margin, and the weighting scheme focuses on the most impactful ranking errors.

**Key difference from BPR**: WARP explicitly considers the rank of the positive item and focuses training on difficult negatives that are ranked higher than the positive item.

### Pointwise vs. Pairwise vs. Listwise

| Approach | Loss Function | Optimization Target |
|---|---|---|
| **Pointwise** | MSE, log loss | Predict individual ratings accurately |
| **Pairwise** | BPR, WARP | Rank positive items above negative items |
| **Listwise** | ListMLE, LambdaRank | Optimize the entire ranked list |

---

## Distributed Matrix Factorization

### Spark MLlib ALS

Apache Spark's MLlib provides a distributed ALS implementation:

- **Partitioning**: Users and items are partitioned across the cluster. Each partition stores a subset of factors.
- **Communication**: In each ALS iteration, factor updates require a shuffle (users need item factors and vice versa).
- **Checkpointing**: ALS iterations are checkpointed to disk to enable fault tolerance without re-computing from scratch.
- **Implicit support**: Built-in support for implicit feedback via weighted ALS.

### Scaling Considerations

| Factor | Impact on Scale |
|---|---|
| Number of users/items | Determines factor matrix dimensions |
| Number of interactions | Determines training data size |
| Latent dimension k | Determines factor vector size and computation per update |
| Number of iterations | Determines total computation time |
| Cluster size | Determines parallelism and memory |

### Communication Optimization

ALS requires synchronization between user and item factor updates. Strategies to reduce communication:

- **Row-wise partitioning**: Each worker stores complete rows of P or Q. Updates are local, requiring only partial results to be aggregated.
- **Block decomposition**: Partition users and items into blocks. Process blocks independently, with periodic synchronization.
- **Asynchronous updates**: Allow workers to update factors without waiting for all others. Reduces idle time but may slow convergence.
