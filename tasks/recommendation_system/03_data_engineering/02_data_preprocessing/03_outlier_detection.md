# Outlier Detection — Recommendation System Data Preprocessing

## 1. Understanding Outliers in Recommendation Data

### 1.1 Types of Outliers

| Outlier Type | Description | Example in RecSys | Severity |
|-------------|-------------|-------------------|----------|
| **Point Outlier** | A single data point is extreme relative to other observations | A user who viewed 10,000 items in one day (bot behavior) | Medium |
| **Contextual Outlier** | A data point is extreme given its context | A user who usually buys budget items purchasing a $10,000 luxury watch | High |
| **Collective Outlier** | A group of data points is anomalous together | A coordinated group of fake accounts leaving 5-star reviews | High |
| **Global Outlier** | An observation deviates significantly from the overall distribution | A product with 1M reviews (every other product has <10K) | Low-Medium |
| **Local Outlier** | An observation is anomalous relative to its local neighborhood | A $5 product in a $500–$1000 product category | Medium |

### 1.2 Why Outliers Matter in Recommendation Systems

- **Model Training Bias**: Extreme interaction counts or ratings from bot accounts can skew collaborative filtering models, producing recommendations biased toward bot-preferred items.
- **Feature Scaling Distortion**: Outliers in numerical features (e.g., session duration, click count) distort feature scaling (z-score, min-max), affecting all downstream models.
- **Popularity Distortion**: A single viral item or bot-inflated view count can distort popularity-based recommendations and collaborative filtering similarity computations.
- **A/B Test Contamination**: Outlier users (bots, power users) in A/B tests can skew experiment results, leading to incorrect conclusions about treatment effects.

### 1.3 Outlier Sources in Recommendation Data

| Source | Mechanism | Detection Difficulty |
|--------|-----------|---------------------|
| Bot / Automated Traffic | Scripts generating fake interactions | Medium — behavioral patterns differ from humans |
| Power Users | Genuine but extreme usage patterns | Low — identifiable but should not be removed |
| Data Entry Errors | Manual data entry mistakes in item metadata | Low — easy to detect via validation rules |
| System Errors | Logging failures, duplicate event emission | Medium — requires deduplication and validation |
| Fraud / Manipulation | Fake reviews, click fraud, review bombing | High — adversarial, actively evades detection |
| Natural Variation | Genuine extreme values in heavy-tailed distributions | Low — should be handled, not removed |

---

## 2. Statistical Methods for Outlier Detection

### 2.1 Z-Score Method

Flag observations where the absolute z-score exceeds a threshold (typically 2.5 or 3.0).

```
z = (x - μ) / σ
Outlier if |z| > threshold
```

- **Assumptions**: Data is approximately normally distributed. Z-score is sensitive to the mean and standard deviation, which are themselves influenced by outliers.
- **Modified Z-Score**: Uses median and Median Absolute Deviation (MAD) instead of mean and standard deviation for robustness:
  ```
  Modified Z = 0.6745 × (x - median) / MAD
  Outlier if |Modified Z| > 3.5
  ```
- **When to Use**: Features with approximately symmetric, unimodal distributions (e.g., session duration after log transformation, normalized ratings).
- **When NOT to Use**: Heavily skewed distributions (common in recommendation data — power-law distributions for views, clicks, purchases), multimodal distributions, or very small sample sizes.
- **Recommendation Data Consideration**: Most user interaction metrics (views, clicks, session duration) follow power-law distributions where z-score is inappropriate without log transformation first.

### 2.2 Interquartile Range (IQR) Method

Flag observations below Q1 - 1.5×IQR or above Q3 + 1.5×IQR, where IQR = Q3 - Q1.

- **Outlier Boundaries**:
  - Lower fence: Q1 - 1.5 × IQR
  - Upper fence: Q3 + 1.5 × IQR
  - "Far outlier" boundaries: Q1 - 3 × IQR and Q3 + 3 × IQR

- **Advantages Over Z-Score**: Does not assume normality; robust to outliers in the calculation itself (uses quartiles rather than mean/std).
- **Disadvantages**: Assumes symmetric distribution of the central 50% of data; may not work well for multimodal distributions.
- **When to Use**: General-purpose outlier detection for numerical features where the distribution shape is unknown or skewed.
- **When NOT to Use**: Highly skewed distributions where the IQR does not capture the distribution's tail behavior (e.g., view counts with 99th percentile at 100× median).

### 2.3 Percentile-Based Capping

Rather than detecting and removing outliers, cap extreme values at specified percentiles (e.g., 1st and 99th, or 5th and 95th).

- **Winsorization**: Replace values below the p-th percentile with the p-th percentile value, and values above the (100-p)-th percentile with that value. Typical p: 1 or 5.
- **Advantages**: Simple, preserves sample size, does not assume a specific distribution.
- **Disadvantages**: Arbitrary threshold choice; may distort the true distribution at the tails; may treat genuine extreme values the same as errors.
- **When to Use**: As a preprocessing step before model training to prevent extreme values from dominating gradient updates; when the exact outlier threshold is not critical.

---

## 3. Advanced Outlier Detection Methods

### 3.1 Isolation Forest

An unsupervised ensemble method that isolates anomalies by randomly selecting a feature and a split value. Anomalies require fewer splits to isolate because they are in sparse regions of the feature space.

- **Algorithm**:
  1. Build an ensemble of isolation trees (iTrees). Each iTree is built by recursively partitioning the data with random feature selection and random split values.
  2. Anomalies have shorter average path lengths in the iTree ensemble (they are isolated faster).
  3. Compute the anomaly score based on the average path length, normalized by the expected path length for a random tree.

- **Hyperparameters**:
  - **n_estimators**: Number of trees. Typical: 100–300. More trees = more stable scores.
  - **contamination**: Expected proportion of outliers in the dataset. Affects the decision threshold. Typical: 0.01–0.1.
  - **max_samples**: Number of samples to draw for each tree. Typical: 256 or min(256, n_samples).

- **Advantages**: Efficient (O(n log n) time complexity); handles high-dimensional data well; does not assume a specific distribution; works with mixed feature types.
- **Disadvantages**: May struggle with datasets where outliers are in dense regions (swamped by normal points); sensitivity to the contamination parameter.

- **When to Use**: High-dimensional feature spaces; unknown contamination rate; when computational efficiency matters (scales to millions of observations).
- **When NOT to Use**: When the dataset has very few outliers (<0.1%); when outlier detection must be interpretable (Isolation Forest provides scores, not easily interpretable explanations).

### 3.2 Local Outlier Factor (LOF)

Measures the local density deviation of a data point relative to its neighbors. Points with significantly lower density than their neighbors are considered outliers.

- **Core Concept**: Compares the local density of a point to the local densities of its K nearest neighbors. If a point's density is much lower than its neighbors', it is an outlier.
- **LOF Score**: A score of approximately 1 indicates the point is in a region of similar density (inlier). A score significantly greater than 1 indicates the point is in a lower-density region (outlier).
- **When to Use**: Datasets with varying local densities; when outliers are in sparse regions but normal data has clusters of different densities.
- **When NOT to Use**: Very high-dimensional data (distance metrics become less meaningful); very large datasets (LOF is computationally expensive, O(n²) for naive implementation).

### 3.3 DBSCAN-Based Detection

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) naturally identifies outliers as noise points — points that do not belong to any cluster.

- **Outlier Identification**: Points labeled as noise (cluster label = -1) by DBSCAN are considered outliers.
- **Advantage**: Provides a cluster-based interpretation of outliers — "this item is an outlier because it does not belong to any meaningful product category."
- **Disadvantage**: Sensitive to hyperparameters (eps, min_samples); does not produce outlier scores (binary in/out classification).

### 3.4 Multivariate Outlier Detection

For recommendation data where outliers may only be apparent in the joint distribution of multiple features:

- **Mahalanobis Distance**: Measures the distance of a point from the center of the distribution, accounting for correlations between features. Points with Mahalanobis distance exceeding a chi-squared threshold are outliers.
- **PCA-Based Detection**: Project data onto the top principal components. Outliers often have high reconstruction error when projected back to the original space.
- **Autoencoder Reconstruction Error**: Train an autoencoder on the data. Outliers have high reconstruction error because the autoencoder learned to reconstruct normal patterns, not anomalous ones.

---

## 4. Domain-Specific Outlier Rules for Recommendation Data

### 4.1 User Interaction Outliers

| Rule | Threshold | Action |
|------|-----------|--------|
| Views per session | >500 views in a single session | Flag as potential bot; cap at 500 |
| Click-through rate | >80% CTR sustained over >100 impressions | Flag for review (may be clicking randomly) |
| Session duration | >4 hours continuous | Split into sub-sessions; flag for review |
| Purchase velocity | >20 purchases in 1 hour | Flag as potential fraud; manual review |
| Rating velocity | >50 ratings in 1 hour | Flag as potential manipulation |

### 4.2 Item Metadata Outliers

| Rule | Threshold | Action |
|------|-----------|--------|
| Price | >10× median price in category | Verify data entry; may be legitimate luxury item |
| Description length | >10,000 characters or <10 characters | Flag for data quality review |
| Image count | >50 images or 0 images | Flag for data entry review |
| Review count | >10× 99th percentile | Investigate for review manipulation |

### 4.3 Temporal Outliers

| Rule | Threshold | Action |
|------|-----------|--------|
| Event timestamp in future | timestamp > current time | Correct or remove (logging error) |
| Event timestamp before item creation | timestamp < item.created_at | Remove (impossible event) |
| Session gap | >24 hours between events in same session | Split session at gap |
| Duplicate events | Same user + item + timestamp within 1 second | Deduplicate (logging bug) |

---

## 5. Handling Strategies for Detected Outliers

### 5.1 Removal

- **When to Remove**: Data points are confirmed to be errors (logging bugs, duplicate events, bot traffic) and not genuine observations.
- **Risk of Removal**: Removing genuine extreme values biases the model toward "average" behavior, potentially under-serving power users or missing niche preferences.
- **Documentation**: Always log the number and percentage of removed outliers, with justification for each removal rule.

### 5.2 Capping / Winsorization

- **When to Cap**: Values are genuine but extreme, and the model should not be overly influenced by them. Capping preserves the observation while limiting its influence.
- **Percentile Selection**: Use domain knowledge to set cap levels — e.g., cap view counts at the 99.5th percentile because values above that are power users, not errors.

### 5.3 Imputation

- **When to Impute**: The outlier value is suspected to be an error, and a more "typical" value can be estimated from the context.
- **Method**: Replace with the median, or use model-based imputation conditioned on other features.

### 5.4 Transformation

- **When to Transform**: The outlier is genuine and the feature follows a heavy-tailed distribution (power law, log-normal).
- **Methods**:
  - Log transformation: x' = log(1 + x). Reduces the influence of extreme values in power-law distributions.
  - Square root transformation: x' = √x. Milder than log transformation.
  - Box-Cox transformation: Automatically selects the optimal power transformation to normalize the distribution.

### 5.5 Segmentation

- **When to Segment**: Different user populations have legitimately different distributions (e.g., bots vs. humans, power users vs. casual users).
- **Method**: Build separate models or model segments for different user groups, rather than trying to fit a single model to the combined distribution.

---

## 6. Outlier Detection Pipeline Design

### 6.1 Pipeline Architecture

```
Raw Data → Rule-Based Filtering → Statistical Detection → ML-Based Detection → Domain Validation → Handling
    │              │                      │                      │                      │              │
    │         Remove duplicates,     Z-score, IQR,         Isolation Forest,    Business rule    Cap, remove,
    │         invalid timestamps     percentile checks     LOF, autoencoder     validation       impute, or
    │                                                                                          transform
```

### 6.2 Batch vs Real-Time Detection

- **Batch Detection**: Run outlier detection daily on the full dataset. Suitable for training data preprocessing, where thoroughness matters more than latency.
- **Real-Time Detection**: Run lightweight outlier checks (rule-based + fast statistical methods) on each event as it arrives. Suitable for filtering bot traffic and detecting anomalies in the event ingestion pipeline.
- **Hybrid Approach**: Real-time filtering for critical anomalies (bots, fraud); batch processing for nuanced statistical outlier detection.

### 6.3 Monitoring and Alerting

- **Outlier Rate Monitoring**: Track the percentage of outliers detected per day, per feature, per data source. A sudden increase in outlier rate may indicate a data quality issue or an attack.
- **Anomaly Detection on Outlier Rates**: Apply anomaly detection to the outlier detection metrics themselves — "meta-anomaly detection" — to catch systemic data quality degradation.
- **Alerting Thresholds**: Alert when outlier rate exceeds 2× the historical average for any feature or data source.
