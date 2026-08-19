# Bagging for Recommendations

## Overview

Bagging (Bootstrap Aggregating) is an ensemble method that trains multiple models on different bootstrap samples of the training data and combines their predictions by averaging or voting. In recommendation systems, bagging reduces variance, improves robustness, and provides feature importance estimates. It is the foundation of random forests and is widely used for ranking with gradient boosted trees.

---

## Bootstrap Aggregating

### Bootstrap Sampling

Each base model is trained on a bootstrap sample—random sampling with replacement from the original training set:

- **Sample size**: Each bootstrap sample has the same size as the original dataset (N samples).
- **Expected unique samples**: ~63.2% of the original data (each sample has a 63.2% chance of being included at least once).
- **Out-of-bag (OOB) samples**: The remaining ~36.8% of data not in each bootstrap sample.

### Aggregation

| Prediction Type | Aggregation Method |
|---|---|
| **Regression** | Average of all model predictions |
| **Classification** | Majority vote across all models |
| **Ranking** | Average of ranking scores, then re-rank |

### Why Bagging Reduces Variance

- **Decorrelation**: Training on different data subsets decorrelates the base models.
- **Averaging**: Averaging K models with variance σ² and pairwise correlation ρ reduces variance to ρσ² + (1-ρ)σ²/K.
- **Key insight**: Lower correlation ρ between models → greater variance reduction.

### Out-of-Bag Estimation

OOB samples provide a built-in validation mechanism:

1. For each training sample, collect predictions from models that did NOT train on that sample (their OOB predictions).
2. Average OOB predictions to get an OOB estimate of the ensemble's performance.
3. OOB performance approximates cross-validation performance without the computational cost.

---

## Random Forests for Feature Importance

### Random Forest Architecture

A random forest is a bagged ensemble of decision trees with an additional source of randomness—each tree considers only a random subset of features at each split:

| Parameter | Description | Typical Value |
|---|---|---|
| **Number of trees** | Ensemble size | 100–1000 |
| **Max depth** | Depth of each tree | 10–30 or unlimited |
| **Max features** | Features considered per split | √(total features) for classification, total/3 for regression |
| **Min samples leaf** | Minimum samples in a leaf | 1–10 |
| **Bootstrap** | Whether to bootstrap data | True (standard bagging) |

### Feature Importance Methods

| Method | Description | Use Case |
|---|---|---|
| **Mean decrease in impurity (MDI)** | Sum of impurity decreases from each feature across all trees | Fast, built-in |
| **Mean decrease in accuracy (MDA)** | Drop in accuracy when a feature is permuted | More reliable, slower |
| **Permutation importance** | Drop in performance when feature values are shuffled | Model-agnostic |
| **SHAP values** | Shapley values for each feature prediction | Most principled, expensive |

### Feature Importance for Recommendations

| Application | Benefit |
|---|---|
| **Feature selection** | Identify which features drive recommendations |
| **Model understanding** | Explain why certain recommendations are made |
| **Data collection** | Prioritize collecting features with high importance |
| **Debugging** | Identify features that are unexpectedly important (data leakage) |
| **A/B test analysis** | Understand which features contributed to performance differences |

---

## Parallel Model Training

### Parallelism in Bagging

Bagging is embarrassingly parallel—each model can be trained independently:

| Framework | Parallelism Strategy |
|---|---|
| **Spark MLlib** | Data parallelism across cluster nodes |
| **scikit-learn** | Joblib-based parallelism across CPU cores |
| **XGBoost/LightGBM** | Built-in multi-threading + data parallelism |
| **Dask** | Distributed parallelism across cluster |

### Resource Allocation

| Resource | Strategy |
|---|---|
| **CPU cores** | Assign each model to a separate core |
| **Memory** | Each model needs the full feature space but only its bootstrap sample |
| **Network** | Minimal communication (only aggregation at the end) |
| **GPU** | Can parallelize individual tree training on GPU |

### Scaling Bagged Ensembles

- **Model parallelism**: Each tree in the forest is trained on a different worker.
- **Data parallelism**: Each worker trains a complete forest on a partition of data.
- **Hybrid**: Combine model and data parallelism for very large datasets.

---

## Variance Reduction

### Bias-Variance Tradeoff

| Component | Effect of Bagging |
|---|---|
| **Bias** | Unchanged (each tree has the same bias as a single tree) |
| **Variance** | Reduced (averaging decorrelated models reduces variance) |
| **Total error** | Reduced (lower variance → lower total error for unstable learners) |

### When Bagging Helps Most

| Scenario | Impact |
|---|---|
| **Unstable base learners** | High variance reduction (decision trees, neural networks) |
| **Correlated features** | Moderate reduction (feature randomness helps) |
| **Noisy data** | Moderate reduction (averaging smooths noise) |
| **Small datasets** | High impact (reduces overfitting risk) |
| **Stable base learners** | Low impact (linear regression, k-NN with large k) |

### Bagging vs. Boosting for Recommendations

| Aspect | Bagging | Boosting |
|---|---|---|
| **Bias reduction** | No | Yes |
| **Variance reduction** | Yes | Moderate |
| **Training** | Parallel (independent) | Sequential (dependent) |
| **Overfitting risk** | Low | Higher (sequential fitting) |
| **Robustness** | High (averaging) | Lower (sequential dependence) |
| **Interpretability** | Feature importance | Feature importance + error analysis |

---

## Bagging for Recommendation Models

### Bagging Neural Network Recommenders

Neural network recommenders can be bagged by training multiple networks on different bootstrap samples:

- **Architecture diversity**: Use different architectures for each bag (e.g., different hidden layer sizes, different activation functions).
- **Initialization diversity**: Train identical architectures with different random initializations on different bootstrap samples.
- **Feature diversity**: Each bag uses a different random subset of features (similar to random forests).

### Bagging for Learning-to-Rank

In learning-to-rank, bagging reduces the variance of ranking predictions:

- **Tree-based bagging**: Train multiple ranking trees on bootstrap samples and average their scores.
- **LambdaMART bagging**: Bag multiple LambdaMART models for more stable rankings.
- **Neural ranker bagging**: Bag multiple neural ranking models with different architectures or initializations.

### Bagging with Feature Subsampling

Feature subsampling (used in random forests) further decorrelates models:

| Feature Subsampling Rate | Effect |
|---|---|
| **100% (no subsampling)** | Standard bagging, higher correlation |
| **50%** | Moderate decorrelation |
| **sqrt(total features)** | Strong decorrelation (standard for classification) |
| **log2(total features)** | Very strong decorrelation |

### Bagging in Production

| Consideration | Approach |
|---|---|
| **Model storage** | Store K models (one per bag) |
| **Inference latency** | Average predictions from K models (Kx latency) |
| **Model compression** | Use knowledge distillation to compress ensemble into a single model |
| **Incremental updates** | Retrain individual bags on new data without retraining the entire ensemble |
| **Monitoring** | Track individual bag predictions to detect degradation in specific bags |

### When to Use Bagging in Recsys

- **Small to medium datasets**: Where overfitting is a concern.
- **Unstable models**: Neural networks, deep trees, and other high-variance models benefit most.
- **Feature importance analysis**: When understanding feature contributions is important.
- **Robustness requirements**: When production stability is more important than maximum accuracy.
- **Baseline establishment**: When you need a reliable baseline before trying more complex methods.
