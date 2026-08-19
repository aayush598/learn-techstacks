# SVD-Based Methods for Recommendations

## Overview

Singular Value Decomposition (SVD) and its variants provide the mathematical foundation for latent factor models in recommendation systems. While classical SVD has limitations for sparse, incomplete matrices, several variants have been developed specifically for the recommendation setting. This document covers truncated SVD, SVD++, time-SVD++, and biased MF, along with convergence analysis and missing value handling.

---

## Truncated SVD

### Classical SVD

For any real matrix A of dimensions m × n, SVD decomposes it as:

**A = U Σ V^T**

Where:
- **U** (m × m): Left singular vectors (user space).
- **Σ** (m × n): Diagonal matrix of singular values in decreasing order.
- **V** (n × n): Right singular vectors (item space).

### Truncated SVD for Recommendations

Truncated SVD keeps only the top-k singular values and corresponding vectors:

**A ≈ U_k Σ_k V_k^T**

This is the best rank-k approximation of A in the Frobenius norm (Eckart-Young theorem).

**For recommendations:**
- U_k rows are user latent factors.
- V_k rows are item latent factors.
- Σ_k provides scaling (often absorbed into U_k or V_k).

### Imputation Required

Classical SVD cannot handle missing values—the full matrix is required. For recommendation:

1. **Fill missing entries**: Replace unobserved ratings with a default value (global mean, 0, or a learned baseline).
2. **Compute SVD**: Apply SVD to the filled matrix.
3. **Truncate**: Keep top-k components.

**Problem**: The imputed values bias the decomposition. Items with more observed ratings have more influence. This leads to suboptimal latent factors compared to methods that handle missing values natively.

### Computational Complexity

| Operation | Complexity | Bottleneck |
|---|---|---|
| Full SVD | O(mn × min(m,n)) | Matrix construction |
| Truncated SVD (randomized) | O(mn × k) | Iterative computation |
| Incremental SVD | O(k² × (m+n)) | Rank update |

For large matrices (millions of users × items), full SVD is intractable. Randomized SVD algorithms (Halko et al., 2011) provide approximate truncated SVD in O(mn × k) time, making it feasible for recommendation-scale problems.

---

## SVD++

### Motivation

Standard MF models capture only the interaction pattern—which users like which items. SVD++ (Koren, 2008) additionally captures implicit feedback signals: the set of items a user has interacted with, regardless of the rating.

### Model Formulation

**r̂_ui = μ + b_u + b_i + q_i^T(p_u + |N(u)|^{-1/2} Σ_{j∈N(u)} y_j)**

Where:
- **N(u)**: Set of items user u has interacted with (implicit feedback).
- **y_j**: Implicit feedback factor for item j (separate from the explicit rating factor q_j).
- **|N(u)|^{-1/2}**: Normalization factor to prevent bias from users with many interactions.

### Key Insight

The term Σ_{j∈N(u)} y_j represents a user's "taste profile" derived purely from their interaction history (which items they've seen/rated), independent of the specific ratings given. This captures the intuition that the set of items a user engages with reveals their preferences, even without explicit ratings.

### Training SVD++

SVD++ is trained using SGD on observed ratings:

**For each observed (u, i, r_ui):**
1. Compute prediction with implicit feedback term.
2. Compute error e_ui = r_ui - r̂_ui.
3. Update all parameters: b_u, b_i, p_u, q_i, and y_j for all j ∈ N(u).

**Computational challenge**: Each update requires iterating over all items in N(u), making training O(|N(u)|) per observation rather than O(1) for basic MF. For users with long histories, this significantly increases training time.

### SVD++ vs. Standard MF

| Aspect | Standard MF | SVD++ |
|---|---|---|
| Parameters | p_u, q_i | p_u, q_i, y_j, b_u, b_i |
| Implicit feedback | Not captured | Captured via y_j terms |
| Training complexity | O(1) per observation | O(|N(u)|) per observation |
| Accuracy improvement | Baseline | 5–15% RMSE reduction |
| Recommendation quality | Good | Better, especially for sparse data |

---

## Time-SVD++ (TimeSVD++)

### Motivation

User preferences evolve over time. A user who liked action movies 5 years ago may prefer documentaries now. TimeSVD++ (Koren, 2009) extends SVD++ to capture temporal dynamics.

### Temporal Components

TimeSVD++ makes several parameters time-dependent:

**r̂_ui(t) = μ + b_u(t) + b_i + q_i^T(p_u(t) + |N(u)|^{-1/2} Σ_{j∈N(u)} y_j)**

Where:
- **b_u(t)**: Time-varying user bias. Captures systematic rating changes over time (e.g., a user becomes more critical over time).
- **p_u(t)**: Time-varying user latent factors. Captures evolving preferences.
- **b_i**: Item bias (time-invariant, assuming item quality doesn't change).
- **q_i**: Item factors (time-invariant).

### Temporal Resolution

The time-varying parameters are modeled with a base value plus a time-bucket deviation:

**p_u(t) = p_u + p_{u,bin(t)}**

Where bin(t) maps the timestamp to a time bucket (e.g., weekly or monthly). The base factor p_u captures the user's long-term preferences, while p_{u,bin(t)} captures deviations in each time period.

### Temporal Bucketing

| Bucket Size | Granularity | Use Case |
|---|---|---|
| Daily | Very fine | Rapidly changing preferences |
| Weekly | Fine | Most recommendation systems |
| Monthly | Medium | Stable preferences |
| Quarterly | Coarse | Slow-moving preference shifts |

The bucket size is a hyperparameter. Too fine: overfitting to noise. Too coarse: missing important temporal patterns.

### TimeSVD++ vs. SVD++

| Aspect | SVD++ | TimeSVD++ |
|---|---|---|
| Temporal dynamics | None | User bias and factors vary over time |
| Parameters | O(|U|×k + |I|×k) | O(|U|×k×T + |I|×k) where T = time buckets |
| Training complexity | Moderate | Higher (time-bucket parameters) |
| Accuracy | Good | Better for datasets with temporal drift |
| Interpretability | Static preferences | Preferences + temporal trends |

---

## Biased Matrix Factorization

### Model Components

Biased MF separates systematic effects from latent interactions:

**r̂_ui = μ + b_u + b_i + p_u · q_i^T**

### Bias Terms

| Bias | Captures | Example |
|---|---|---|
| **Global (μ)** | Overall rating level | Average movie rating is 3.5 |
| **User (b_u)** | User rating tendency | User A rates 0.5 above average |
| **Item (b_i)** | Item quality/popularity | Item X receives 0.8 above average |
| **Interaction (p_u · q_i)** | User-item preference beyond biases | User A specifically likes Item X |

### Why Biases Matter

Without biases, the model must explain systematic rating patterns through latent factors alone. This overloads the latent space—the factors must simultaneously capture user tendency, item quality, and genuine preference interactions. Separating biases allows the latent factors to focus on the residual preference signal, improving accuracy.

### Training Biased MF

SGD updates for biased MF:

1. **Global bias**: μ = average of all observed ratings.
2. **User bias**: b_u ← b_u + η(e_ui - λb_u)
3. **Item bias**: b_i ← b_i + η(e_ui - λb_i)
4. **User factor**: p_u ← p_u + η(e_ui · q_i - λp_u)
5. **Item factor**: q_i ← q_i + η(e_ui · p_u - λq_i)

Where e_ui = r_ui - r̂_ui is the prediction error.

---

## Handling Missing Values

### Strategies for Missing Data

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **Global mean imputation** | Fill with overall average | Simple, unbiased for MCAR | Biases factor learning |
| **User mean imputation** | Fill with user's average rating | Accounts for user bias | Biases item factors |
| **Item mean imputation** | Fill with item's average rating | Accounts for item quality | Biases user factors |
| **Default value** | Fill with 0 or a fixed value | Simple | Arbitrary, biases decomposition |
| **Native missing handling** | Train only on observed entries | No imputation bias | Requires specialized algorithms |

### Native Missing Value Handling

Modern MF algorithms handle missing values natively by only computing the loss on observed entries:

- **SGD-based MF**: Updates factors only for observed (user, item) pairs. Unobserved entries have no gradient contribution.
- **ALS**: The least squares formulation naturally handles missing values by only summing over observed entries in the objective.
- **Probabilistic MF**: Models the missing values as a latent variable and marginalizes over them.

### Missing Not At Random (MNAR)

In recommendation data, missing values are not random—users tend to interact with items they like (selection bias). This MNAR pattern means:

- Items with high ratings are over-represented.
- Users who rate more items contribute more data.
- Standard imputation assumptions (missing at random) are violated.

**Mitigation approaches:**
- **Propensity weighting**: Weight observations by the inverse probability of being observed.
- **Missingness models**: Explicitly model the selection process alongside the rating model.
- **Counterfactual reasoning**: Estimate what the rating would have been for an unobserved interaction.

---

## Convergence Analysis

### SGD Convergence

SGD for MF converges under standard conditions:

- **Learning rate schedule**: Decrease η over time (e.g., η_t = η_0 / √t).
- **Regularization**: Sufficient λ prevents overfitting and improves convergence stability.
- **Mini-batch size**: Smaller batches add noise that can help escape local minima but slow convergence.
- **Convergence rate**: Typically O(1/√t) for convex objectives. Non-convex MF problems converge to local minima.

### ALS Convergence

ALS guarantees monotonic decrease of the objective function—each iteration is guaranteed to reduce (or maintain) the training loss:

- **Convergence proof**: Each ALS step solves a convex sub-problem exactly. The joint objective is bounded below (by 0), so monotonic decrease implies convergence.
- **Convergence speed**: Typically converges in 10–20 iterations. The rate depends on the condition number of the factor matrices.
- **Early stopping**: Monitor the validation loss. Stop when the validation loss stops decreasing.

### Monitoring Convergence

| Metric | Description | Target |
|---|---|---|
| Training loss | Sum of squared errors on training set | Monotonically decreasing |
| Validation loss | Sum of squared errors on held-out set | Decrease then plateau |
| RMSE | Root mean squared error on test set | Below baseline (e.g., global mean) |
| Factor norm | L2 norm of factor vectors | Stable, not growing |
| Learning rate | Current learning rate (SGD) | Decreasing over time |

### Overfitting Detection

| Signal | Cause | Mitigation |
|---|---|---|
| Training loss decreasing, validation loss increasing | Model memorizing training data | Increase regularization |
| Factor norms growing | Insufficient regularization | Increase λ |
| Perfect training accuracy | Overfitting to noise | Reduce k (latent dimension) |
| Validation loss oscillating | Learning rate too high | Reduce η or use decay schedule |
