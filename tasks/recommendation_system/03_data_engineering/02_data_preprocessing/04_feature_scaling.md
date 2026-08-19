# Feature Scaling — Recommendation System Data Preprocessing

## 1. Why Feature Scaling Matters

### 1.1 The Core Problem

Features in recommendation data have vastly different scales — user age (18–80), session duration (0–7200 seconds), purchase count (0–1000), and price (0.99–9999.99). Without scaling, distance-based algorithms and gradient-based optimization will be dominated by features with larger magnitudes.

### 1.2 Algorithms Sensitive to Feature Scaling

| Algorithm | Sensitive? | Reason |
|-----------|-----------|--------|
| K-Nearest Neighbors | Yes | Distance metric dominated by large-scale features |
| K-Means Clustering | Yes | Centroid computation affected by scale |
| Logistic Regression (with L1/L2) | Yes | Regularization penalizes large-magnitude coefficients |
| Neural Networks (all) | Yes | Gradient descent convergence depends on feature scale |
| Support Vector Machines | Yes | Margin computation affected by feature scale |
| PCA | Yes | Variance maximization is scale-dependent |
| Gradient Boosted Trees | **No** | Split decisions are scale-invariant |
| Random Forest | **No** | Split decisions are scale-invariant |
| Naive Bayes | **No** | Probability estimation is scale-invariant |

**Key Insight**: Tree-based models (XGBoost, LightGBM, Random Forest) do not require feature scaling because they make split decisions based on feature thresholds, which are invariant to monotonic transformations. Neural networks, linear models, and distance-based methods do require scaling.

---

## 2. Scaling Methods

### 2.1 Min-Max Normalization

Scales features to a fixed range, typically [0, 1].

```
x_scaled = (x - x_min) / (x_max - x_min)
```

- **Properties**:
  - Preserves the shape of the original distribution.
  - Does not reduce the influence of outliers (outliers determine the min/max range).
  - Produces bounded output, which is useful for neural network inputs with bounded activation functions (sigmoid, tanh).

- **When to Use**: When the feature has a known, bounded range; when you need values in [0, 1] for neural network inputs; when the feature distribution is roughly uniform.
- **When NOT to Use**: When the feature has outliers (outliers compress the majority of values into a narrow range); when the feature distribution is highly skewed.

- **Example**: User age (18–80):
  - User A (age 30): (30 - 18) / (80 - 18) = 0.194
  - User B (age 65): (65 - 18) / (80 - 18) = 0.758

### 2.2 Z-Score Standardization (Standard Scaling)

Transforms features to have zero mean and unit variance.

```
x_scaled = (x - μ) / σ
```

- **Properties**:
  - Centers the distribution at zero.
  - Scales by standard deviation, so the output has mean ≈ 0 and std ≈ 1.
  - Does not bound the output range — extreme values remain extreme.
  - Sensitive to outliers because μ and σ are computed from all data points.

- **When to Use**: When the feature is approximately normally distributed; when the algorithm assumes zero-centered features (e.g., PCA, SVM); when outliers are not a concern (or have been handled separately).
- **When NOT to Use**: When the feature has significant outliers; when the feature is not approximately Gaussian; when bounded output is required.

- **Example**: Session duration (μ=300s, σ=150s):
  - Session A (120s): (120 - 300) / 150 = -1.2 (below average)
  - Session B (600s): (600 - 300) / 150 = 2.0 (well above average)

### 2.3 Robust Scaling

Uses median and IQR instead of mean and standard deviation, making it robust to outliers.

```
x_scaled = (x - median) / IQR
```

- **Properties**:
  - Centered at the median (robust to outliers).
  - Scaled by IQR (range of the middle 50% of data, robust to outliers).
  - Output distribution is centered at 0 but not necessarily with unit variance.
  - Bounded outliers do not influence the scaling.

- **When to Use**: When the feature has significant outliers; when the feature distribution is skewed; when you want scaling that is not influenced by extreme values.
- **When NOT to Use**: When the median and IQR are not representative of the "typical" feature range (e.g., bimodal distributions); when the algorithm specifically requires zero-mean, unit-variance features.

- **Example**: Purchase count (median=5, IQR=8):
  - User with 3 purchases: (3 - 5) / 8 = -0.25
  - User with 50 purchases: (50 - 5) / 8 = 5.625 (extreme, but not distorted by this user's value)

### 2.4 Log Transformation

Applies a logarithmic function to compress the range of heavy-tailed distributions.

```
x_scaled = log(1 + x)    # For non-negative values
x_scaled = log(x)         # For strictly positive values
```

- **Properties**:
  - Converts multiplicative relationships to additive relationships.
  - Compresses the right tail of right-skewed distributions (common in recommendation data).
  - Does not produce bounded output; handles zero values with log(1+x).
  - Reduces the influence of extreme values while preserving relative ordering.

- **When to Use**: When the feature follows a power-law or log-normal distribution (view counts, click counts, purchase amounts, session durations); when the feature spans multiple orders of magnitude.
- **When NOT to Use**: When the feature has zero or negative values (without adjustment); when the distribution is already approximately symmetric; when the algorithm requires linear relationships.

- **Example**: View count (skewed: median=10, max=100,000):
  - Item with 10 views: log(1 + 10) = 2.40
  - Item with 1,000 views: log(1 + 1000) = 6.91
  - Item with 100,000 views: log(1 + 100000) = 11.51
  - Without log transform, the range would be 10–100,000 (10,000×). With log transform, the range is 2.40–11.51 (4.8×).

### 2.5 Box-Cox Transformation

A parametric power transformation that finds the optimal exponent λ to make the data as close to normal as possible.

```
x_scaled = (x^λ - 1) / λ      if λ ≠ 0
x_scaled = log(x)              if λ = 0
```

- **Properties**:
  - Automatically selects the optimal λ to maximize normality (minimizes skewness).
  - Requires strictly positive values.
  - λ = 1: no transformation; λ = 0.5: square root; λ = 0: log; λ = -1: reciprocal.
  - Inverse transform is available for recovering original scale.

- **When to Use**: When you want an automated, data-driven transformation; when you need the transformed feature to be approximately normal (e.g., for linear models, PCA); when the feature is strictly positive.
- **When NOT to Use**: When the feature has zero or negative values; when interpretability of the transformation is important (Box-Cox λ is not intuitive); when the distribution change is too drastic for downstream interpretation.

### 2.6 Yeo-Johnson Transformation

An extension of Box-Cox that handles zero and negative values.

```
For x ≥ 0: ((x + 1)^λ - 1) / λ     if λ ≠ 0
            log(x + 1)                if λ = 0

For x < 0: -((-x + 1)^(2-λ) - 1) / (2-λ)    if λ ≠ 2
            -log(-x + 1)                        if λ = 2
```

- **When to Use**: Same as Box-Cox, but when the feature contains zero or negative values.
- **When NOT to Use**: When interpretability is critical; when the optimal λ is extreme (λ > 2 or λ < -2), indicating the transformation may be too aggressive.

---

## 3. Scaling by Feature Type in Recommendation Systems

### 3.1 Feature Type and Recommended Scaling

| Feature Type | Examples | Recommended Scaling | Rationale |
|-------------|---------|--------------------|-----------| 
| **User Age** | 18–80 | Min-Max or Z-Score | Bounded range, roughly symmetric |
| **Session Duration** | 0–7200s | Log + Z-Score | Power-law distribution |
| **View/Click Count** | 0–1M+ | Log + Z-Score | Heavily right-skewed (power law) |
| **Purchase Count** | 0–1000+ | Log + Robust Scaling | Right-skewed, with outlier power users |
| **Price** | 0.01–10,000+ | Log + Robust Scaling | Power-law across categories |
| **Rating** | 1–5 | None or Min-Max | Already bounded, approximately symmetric |
| **CTR** | 0–1 | None | Already bounded in [0, 1] |
| **Embedding Dimensions** | -∞ to +∞ | Z-Score or None | Neural network embeddings are typically zero-centered |
| **Categorical (one-hot)** | 0/1 | None | Already binary; no scaling needed |
| **Time Since Last Activity** | 0–∞ | Log + Robust Scaling | Power-law (many recent, few very old) |
| **Cosine Similarity** | -1 to +1 | None or Min-Max | Already bounded |
| **Distance (ANN)** | 0 to +∞ | Log + Z-Score | Often exponentially distributed |

### 3.2 Interaction Features

- **Cross-Features**: When creating interaction features (e.g., user_age × item_price), scale the input features before crossing to prevent the interaction term from being dominated by the larger-scale feature.
- **Polynomial Features**: Higher-order features (x², x³) amplify scale differences. Always scale the base feature before computing polynomial expansions.
- **Ratios**: Features computed as ratios (e.g., purchase_count / view_count) may not require additional scaling if both numerator and denominator are already scaled, but verify empirically.

---

## 4. Data Leakage Prevention

### 4.1 The Leakage Problem

Scaling parameters (mean, standard deviation, min, max, median, IQR) must be computed from the **training data only**, never from the test data or the full dataset. Using test data statistics for scaling leaks information about the test distribution into the training process, producing overly optimistic evaluation metrics.

### 4.2 Correct Scaling Pipeline

```
Training Data → Fit Scaler (compute statistics) → Transform Training Data
                                                         ↓
Test Data → Transform Test Data (using training statistics) → Evaluate
                                                         ↓
Production Data → Transform Production Data (using training statistics) → Serve
```

### 4.3 Common Leakage Scenarios

| Scenario | Problem | Correct Approach |
|----------|---------|-----------------|
| Scaling before train/test split | Test data statistics influence scaling parameters | Split first, then fit scaler on training data only |
| Re-fitting scaler on each batch | Online scaling parameters drift from training parameters | Use training statistics; update only in periodic retraining |
| Scaling target variable | Target leakage if scaler is fit on full data | Scale target using training statistics only |
| Scaling categorical embeddings | Embedding weights should not be "scaled" like numerical features | Do not scale learned embeddings; they are already normalized in the latent space |

### 4.4 Online Scaling

For real-time features that arrive in production:

- **Streaming Statistics**: Maintain running mean, variance, min, max, and count using Welford's algorithm or a count-min sketch. Update statistics with each new observation.
- **Bounded Update Rate**: Limit how frequently scaling parameters are updated to prevent concept drift from destabilizing the model.
- **Reference Statistics**: Use the training-set statistics as a fixed reference; update streaming statistics only for monitoring and alerting, not for active scaling.

---

## 5. Practical Implementation Guidelines

### 5.1 Scaling Pipeline Order

1. **Split Data**: Separate into train/validation/test sets BEFORE any scaling.
2. **Fit Scaler**: Compute scaling parameters on training data only.
3. **Transform Training Data**: Apply the fitted scaler to training data.
4. **Transform Validation/Test Data**: Apply the SAME fitted scaler (no re-fitting).
5. **Persist Scaler**: Save the fitted scaler object (parameters, fitted state) alongside the model for serving-time transformation.

### 5.2 Scaling for Multi-Stage Models

In the two-stage recommendation architecture (candidate generation + ranking):

- **Candidate Generation**: May use a different set of features and scaling than the ranking model. Each stage needs its own scaler.
- **Feature Store Consistency**: Features served in the feature store must be scaled using the same scaler that was fit during model training. The scaler must be versioned alongside the model.
- **Cross-Model Sharing**: If multiple models share the same features, they can share the same scaler, but only if all models were trained on the same data partition.

### 5.3 Scaling Validation

After scaling, validate that the transformed features have the expected properties:

- **Distribution Check**: Plot histograms of scaled features to verify they are approximately in the expected range and shape.
- **Statistical Tests**: Verify that the mean is approximately 0 and standard deviation approximately 1 (for z-score), or that the min is 0 and max is 1 (for min-max).
- **NaN/Inf Check**: Ensure no NaN or Inf values were introduced by the scaling operation (e.g., division by zero in z-score for zero-variance features).
- **Feature Importance Stability**: Compare feature importances before and after scaling. If the ranking of features changes dramatically, the scaling may be distorting the data.
