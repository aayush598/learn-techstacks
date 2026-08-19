# Missing Value Treatment — Recommendation System Data Preprocessing

## 1. Understanding Missing Data Mechanisms

### 1.1 MCAR (Missing Completely at Random)

Missingness is independent of both observed and unobserved data. The probability of a value being missing is the same for all observations.

- **Example**: A user's age is missing because the form field had a technical bug — the missingness is unrelated to the user's actual age or any other variable.
- **Statistical Property**: Listwise deletion (removing rows with missing values) does not introduce bias under MCAR, but reduces statistical power.
- **Detection**: Little's MCAR test can formally test whether data is MCAR. If p-value > 0.05, we fail to reject the null hypothesis that data is MCAR.
- **Implication**: Simple deletion or mean imputation is acceptable under MCAR, though more sophisticated methods still improve power.

### 1.2 MAR (Missing at Random)

Missingness depends on observed data but not on the missing values themselves. The probability of missingness can be explained by other observed variables.

- **Example**: Female users are less likely to disclose their age than male users. The missingness in age depends on gender (observed), but not on the actual age value (unobserved).
- **Statistical Property**: Listwise deletion under MAR introduces bias. Multiple imputation or model-based methods that condition on observed covariates produce unbiased estimates.
- **Detection**: Compare the distribution of observed variables between rows with and without missing values. If distributions differ significantly, MAR is likely.
- **Implication**: Must use imputation methods that account for the observed variables related to missingness.

### 1.3 MNAR (Missing Not at Random)

Missingness depends on the unobserved (missing) values themselves. The missingness is informative about the value that would have been observed.

- **Example**: Users with very low income are less likely to report their income. The missingness in income is directly related to the missing income value itself.
- **Another Example**: Users who dislike a product are less likely to rate it, creating a systematic bias in rating data — "survivorship bias" in recommendation data.
- **Statistical Property**: MNAR is the most problematic mechanism — no statistical method can fully correct for MNAR without additional assumptions or external data.
- **Detection**: Cannot be formally tested with the data alone. Requires domain knowledge or external validation data.
- **Implication**: Must model the missingness mechanism explicitly (e.g., selection models, pattern-mixture models) or collect additional data to make the MNAR assumption less likely.

### 1.4 Missingness in Recommendation Data

| Data Type | Typical Missingness Mechanism | Severity |
|-----------|------------------------------|----------|
| User ratings | MNAR — users rate items they feel strongly about | High |
| User demographics (age, gender) | MAR — depends on user segment, registration channel | Medium |
| Item attributes (category, description) | MCAR — depends on data ingestion completeness | Low |
| Implicit signals (clicks, views) | MAR/MNAR — depends on UI layout, item visibility | Medium |
| Missing timestamps | MCAR — logging gaps | Low |
| Missing prices | MCAR/MAR — some items have variable pricing | Low-Medium |

---

## 2. Deletion Strategies

### 2.1 Listwise Deletion (Complete Case Analysis)

Remove any row that contains a missing value in any feature.

- **When to Use**: Data is MCAR, missingness rate is <5%, and the dataset is large enough that the reduction in sample size is not impactful.
- **When NOT to Use**: Data is MAR or MNAR; missingness rate is >10%; the dataset is small or the variable with missing values is important.
- **Risk**: If data is not MCAR, listwise deletion produces biased estimates. Even under MCAR, it reduces statistical power.

### 2.2 Pairwise Deletion

Use all available data for each specific computation. For example, when computing the correlation between age and rating, use only rows where both age and rating are observed.

- **When to Use**: When different analyses require different variable combinations, and you want to maximize the sample size for each analysis.
- **When NOT to Use**: When downstream models require a complete feature matrix (most ML models do).
- **Risk**: Can produce non-positive-definite covariance matrices; results from different pairwise analyses are based on different sample sizes.

### 2.3 Column Deletion

Remove an entire feature column if the missingness rate exceeds a threshold (e.g., >50%).

- **When to Use**: A feature has >50% missing values and is not critical to the recommendation model.
- **When NOT to Use**: The feature is important even with sparse observations (e.g., user rating history for a collaborative filtering model).
- **Risk**: Losing potentially valuable information; introducing bias if the missingness is not MCAR.

---

## 3. Imputation Strategies

### 3.1 Simple Imputation

| Method | Formula | When to Use | Limitation |
|--------|---------|-------------|------------|
| Mean Imputation | x̂ = mean(x_observed) | Numerical features, MCAR, symmetric distribution | Reduces variance, distorts correlations |
| Median Imputation | x̂ = median(x_observed) | Numerical features, skewed distribution, outliers present | Same variance reduction issue |
| Mode Imputation | x̂ = mode(x_observed) | Categorical features | Creates artificial majority class |
| Constant Imputation | x̂ = specified constant | When "missing" has a semantic meaning (e.g., "unknown") | Can distort feature distributions |

### 3.2 K-Nearest Neighbors (KNN) Imputation

Impute missing values using the weighted average of the K most similar observed instances, where similarity is computed on the observed features.

- **Algorithm**:
  1. For each instance with a missing value, find K nearest neighbors using observed features (Euclidean distance, Minkowski distance, or Gower distance for mixed types).
  2. Impute the missing value as the weighted average (for numerical) or weighted mode (for categorical) of the K neighbors' values for that feature.
  3. Weight by inverse distance to give closer neighbors more influence.

- **Hyperparameters**:
  - **K**: Typically 5–10. Larger K reduces variance but increases bias. Small K captures local patterns but is sensitive to noise.
  - **Distance Metric**: Euclidean for numerical, Gower for mixed numerical/categorical, Manhattan for robustness to outliers.
  - **Weighting**: Inverse distance weighting, uniform weighting, or Gaussian kernel weighting.

- **When to Use**: Dataset size < 1M rows; features have meaningful similarity structure; missingness is MAR.
- **When NOT to Use**: Very high-dimensional data (curse of dimensionality); datasets > 1M rows (computationally expensive); all features are missing for some instances.

### 3.3 Matrix Factorization Imputation

Treat the data matrix as a partially observed matrix and factorize it to recover missing entries. This is particularly natural for recommendation data (user-item interaction matrix).

- **Algorithm**:
  1. Decompose the partially observed matrix R into low-rank matrices P (user factors) and Q (item factors) such that R ≈ P × Q^T.
  2. Use alternating least squares (ALS), stochastic gradient descent (SGD), or Bayesian matrix factorization to learn P and Q.
  3. Missing entries are imputed as the dot product of the corresponding user and item factors.

- **Key Parameters**:
  - **Rank (k)**: Number of latent factors. Typical range: 50–200. Higher rank captures more complex patterns but risks overfitting.
  - **Regularization**: L2 regularization on P and Q to prevent overfitting. Typical λ: 0.01–0.1.
  - **Learning Rate**: For SGD-based optimization. Typical: 0.001–0.01.

- **Advantages Over Simple Imputation**: Captures latent structure in the data; produces unbiased estimates under MAR; naturally handles the sparsity pattern in recommendation data.
- **Limitations**: Assumes low-rank structure; may not capture non-linear relationships; computationally expensive for very large matrices.

### 3.4 Model-Based Imputation

Train a predictive model to predict missing values from observed values. This is the most flexible approach.

- **Iterative Imputation (MICE — Multiple Imputation by Chained Equations)**:
  1. Initialize missing values with simple imputation (mean/median).
  2. For each feature with missing values:
     a. Treat that feature as the target variable.
     b. Train a model (linear regression, random forest, gradient boosting) using all other features as predictors, on the subset where this feature is observed.
     c. Predict missing values using the trained model.
  3. Repeat steps 2 for M iterations (typically 5–10) until convergence.
  4. For multiple imputation, repeat the entire process M times with different random seeds to create M completed datasets.

- **Recommended Models for Imputation**:
  - **Random Forest**: Handles non-linear relationships, interactions, and mixed feature types. Robust to outliers.
  - **Gradient Boosting (XGBoost/LightGBM)**: High predictive accuracy, handles missing values natively in some implementations.
  - **Neural Networks**: For complex, high-dimensional data. Can model non-linear relationships that tree-based methods miss.

### 3.5 Deep Learning Imputation

For very high-dimensional or complex data, deep learning-based imputation methods can capture intricate patterns:

- **Autoencoder Imputation**: Train an autoencoder on the observed portions of the data. The encoder-decoder architecture learns a compressed representation that can reconstruct observed values and predict missing ones.
- **Generative Adversarial Imputation (GAIN)**: Uses a GAN framework where the generator fills in missing values and the discriminator distinguishes observed from imputed values.
- **Variational Autoencoder (VAE) Imputation**: Learns a latent distribution over the data, enabling probabilistic imputation with uncertainty estimates.

---

## 4. Missing Value Indicators

### 4.1 Indicator Features

Create a binary indicator feature for each variable that has missing values, where 1 indicates the value was originally missing and 0 indicates it was observed.

- **Why It Works**: If data is MAR or MNAR, the pattern of missingness itself carries information. The indicator feature allows the model to learn different relationships for observed vs. imputed values.
- **Implementation**: Add a binary column `feature_name_is_missing` for each feature with missing values, alongside the imputed feature.
- **When to Use**: Always, when the missingness rate is >5% and the data is likely MAR or MNAR. The indicator feature costs almost nothing and can significantly improve model performance.

### 4.2 Missingness Pattern Encoding

For datasets with complex missingness patterns, encode the overall pattern of missingness as a feature:

- **Missing Count Feature**: Create a feature that counts the total number of missing values per instance. An instance with 5 missing features may be systematically different from one with 0.
- **Missing Pattern Hash**: Hash the binary missingness pattern across all features to create a categorical feature that captures common missingness profiles.
- **Missingness Embedding**: Use a neural network to learn an embedding of the missingness pattern, capturing complex dependencies between which features are missing.

---

## 5. Feature Engineering with Missing Data

### 5.1 Interaction Features

- **Missing-Value Interactions**: Create interaction features between the missingness indicator and other features. For example, `is_missing × user_age_bucket` captures whether the effect of age on the target differs for users who did not provide their age.
- **Imputation Source Features**: If different imputation methods are used for different data segments (e.g., mean imputation for high-activity users, KNN for low-activity users), create a feature indicating which method was used.

### 5.2 Binning Missing Values

- **Treat "Missing" as a Category**: For categorical features, treat missing as a separate category (e.g., "unknown" or "not_provided"). This is often the simplest and most effective approach for categorical missing data.
- **Numerical Binning with Missing Category**: For numerical features, bin into quantiles and create a separate bin for missing values. This preserves the distribution of observed values while handling missingness.

### 5.3 Recommendation-Specific Missing Data Patterns

- **Implicit Feedback as Missing Data**: In recommendation systems, the absence of a user-item interaction is not necessarily a negative signal — it may simply mean the user has not discovered the item. This is the fundamental challenge of implicit feedback: "missing" data is a mixture of true negatives (disliked items) and unknowns (unseen items).
- **Treatment**: Use confidence weighting rather than binary positive/negative labels. Items the user has interacted with are positive with confidence proportional to interaction strength. Items not interacted with are treated as weak negatives with low confidence weight.

---

## 6. Best Practices for Recommendation Systems

### 6.1 Imputation Pipeline Design

1. **Profile Missing Data**: For each feature, compute missingness rate, missingness mechanism (MCAR/MAR/MNAR), and correlation with other features and the target.
2. **Select Strategy by Feature**:
   - Categorical features with <20% missing: Mode imputation + indicator feature.
   - Numerical features with <10% missing: KNN or model-based imputation + indicator feature.
   - Features with >50% missing: Evaluate column deletion vs. constant imputation ("unknown").
   - User interaction data: Matrix factorization imputation (natural for recommendation data).
3. **Validate Imputation Quality**: Compare the distribution of imputed values against observed values. Use posterior predictive checks to verify that the imputation preserves the data's statistical properties.
4. **Track Imputation Decisions**: Log all imputation decisions for reproducibility. The imputation strategy used during training must be exactly replicated during serving.

### 6.2 Common Pitfalls

- **Data Leakage**: Never use test data statistics (mean, median) for imputation. Compute imputation parameters from the training set only.
- **Imputation Instability**: Single imputation underestimates uncertainty. For critical analyses, use multiple imputation (MICE) to capture imputation uncertainty.
- **Ignoring MNAR**: If data is MNAR (common in recommendation ratings), naive imputation will produce biased estimates. Consider Heckman selection models or pattern-mixture models.
- **Over-Imputation**: Do not impute values when the missingness itself is the signal. A user who never rates a movie may be indifferent — imputing a rating is worse than leaving it missing.
