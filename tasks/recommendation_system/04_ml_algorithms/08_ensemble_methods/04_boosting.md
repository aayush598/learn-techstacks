# Boosting for Recommendations

## Overview

Boosting is an ensemble method that sequentially trains models, where each subsequent model focuses on the errors of previous models. In recommendation systems, gradient boosted trees (XGBoost, LightGBM, CatBoost) are among the most powerful models for learning-to-rank tasks, CTR prediction, and feature-based recommendation. Boosting reduces both bias and variance, making it a strong choice as both a standalone model and a meta-learner in ensemble pipelines.

---

## Gradient Boosting

### Core Algorithm

Gradient boosting builds an ensemble of weak learners (typically shallow decision trees) sequentially:

1. **Initialize**: Start with a constant prediction (e.g., global mean).
2. **Compute residuals**: Calculate the difference between predictions and actual values.
3. **Fit weak learner**: Train a new tree to predict the residuals (pseudo-residuals).
4. **Update ensemble**: Add the new tree's predictions to the ensemble (scaled by learning rate).
5. **Repeat**: Continue until the maximum number of trees is reached or validation performance stops improving.

### Gradient Boosting for Ranking

For learning-to-rank in recommendations, gradient boosting optimizes ranking-specific objectives:

| Objective | Description | Use Case |
|---|---|---|
| **LambdaMART** | Lambda gradients + MART | Top-K ranking |
| **RankNet** | Pairwise cross-entropy | Pairwise preference learning |
| **ListNet** | Listwise cross-entropy | List-level optimization |
| **NDCG loss** | Approximate NDCG gradient | Direct NDCG optimization |

---

## XGBoost

### Key Features

XGBoost (eXtreme Gradient Boosting) is a scalable, regularized gradient boosting framework:

- **Regularized objective**: L1/L2 regularization on leaf weights prevents overfitting.
- **Newton-Raphson updates**: Uses second-order gradient information for faster convergence.
- **Sparsity-aware**: Handles missing values natively without imputation.
- **Column subsampling**: Random feature selection per tree decorrelates trees.
- **Cache-aware**: Optimized for CPU cache hierarchy for faster training.
- **Distributed**: Multi-machine training scales to large datasets.

### XGBoost for CTR Prediction

| Aspect | Configuration |
|---|---|
| **Objective** | Binary:logistic for CTR, pairwise:pairwise for ranking |
| **Max depth** | 6-10 (deeper than typical due to feature interactions) |
| **Learning rate** | 0.01-0.1 (lower = more trees, better generalization) |
| **Number of trees** | 500-2000 |
| **Regularization** | L2 lambda = 1-10, L1 alpha = 0-1 |
| **Min child weight** | 1-10 (controls tree complexity) |

---

## LightGBM

### Key Innovations

LightGBM introduces several innovations for faster and more efficient training:

- **GOSS (Gradient-based One-Side Sampling)**: Retains instances with large gradients and randomly samples instances with small gradients, reducing data volume while maintaining accuracy.
- **EFB (Exclusive Feature Bundling)**: Bundles mutually exclusive sparse features into a single feature, reducing dimensionality.
- **Leaf-wise growth**: Grows the leaf with maximum loss reduction (vs. level-wise in XGBoost), producing deeper trees with fewer total leaves.
- **Histogram-based splits**: Bins continuous features into histograms for faster split finding.
- **Categorical features**: Native categorical feature handling without one-hot encoding.

### LightGBM vs. XGBoost

| Aspect | XGBoost | LightGBM |
|---|---|---|
| **Training speed** | Moderate | 2-10x faster |
| **Memory usage** | Higher | Lower (histogram-based) |
| **Accuracy** | Excellent | Excellent (often slightly better) |
| **Categorical features** | Requires encoding | Native support |
| **Small datasets** | Better | May overfit with leaf-wise growth |
| **Large datasets** | Good | Excellent (GOSS, EFB) |

---

## CatBoost

### Key Features

CatBoost (Categorical Boosting) specializes in handling categorical features:

- **Ordered boosting**: Processes data in a random permutation order to avoid target leakage during training.
- **Ordered target statistics**: Native categorical encoding that prevents information leakage.
- **Symmetric trees**: Balanced tree structure for faster inference.
- **Oblivious decision trees**: Same split condition at each level enables GPU-optimized training.
- **Built-in overfitting detection**: Automatic early stopping without a separate validation set.

### CatBoost for Recommendations

| Aspect | Configuration |
|---|---|
| **Categorical features** | Provide column names; CatBoost handles encoding automatically |
| **Text features** | Provide text columns; CatBoost extracts features |
| **Embedding features** | Provide pre-computed embeddings as features |
| **Loss function** | Logloss (CTR), QueryCrossEntropy (ranking) |

---

## Learning Rate and Early Stopping

### Learning Rate

The learning rate scales each tree's contribution to the ensemble. Lower learning rates require more trees but produce better generalization:

| Learning Rate | Number of Trees | Generalization | Training Time |
|---|---|---|---|
| 0.1 | 100-500 | Good | Fast |
| 0.05 | 500-1000 | Better | Moderate |
| 0.01 | 1000-5000 | Best | Slow |
| 0.005 | 2000-10000 | Diminishing returns | Very slow |

**Best practice**: Use a low learning rate (0.01-0.05) with a large number of trees, combined with early stopping.

### Early Stopping

Monitor validation loss during training and stop when it stops improving. This prevents overfitting and saves training time:

| Parameter | Description | Typical Value |
|---|---|---|
| **early_stopping_rounds** | Stop after N rounds without improvement | 50-200 |
| **eval_metric** | Metric to monitor | AUC, logloss, NDCG |
| **validation_set** | Held-out data for monitoring | 10-20% of training data |

---

## Feature Importance in Boosted Trees

### Importance Metrics

| Metric | Description | Best For |
|---|---|---|
| **Gain** | Total loss reduction from splits using the feature | Identifying impactful features |
| **Frequency** | Number of splits using the feature | Identifying commonly used features |
| **Coverage** | Number of samples affected by splits using the feature | Identifying broadly useful features |
| **Permutation** | Drop in performance when feature is shuffled | Model-agnostic, reliable |

### Feature Importance for Recommendations

- **Feature selection**: Remove features with near-zero importance to simplify the model.
- **Debugging**: If a trivial feature (e.g., item ID) has highest importance, the model may be memorizing.
- **A/B test analysis**: Compare feature importance across experimental groups.
- **Feature engineering**: High importance for derived features validates the engineering effort.

---

## Ranking with Boosted Trees

### Learning-to-Rank Pipeline

1. **Feature engineering**: Create user-item-context features.
2. **Label definition**: Define relevance labels (click=1, purchase=2, etc.).
3. **Training data**: Generate (query, document, label) triples from logged interactions.
4. **Model training**: Train XGBoost/LightGBM with ranking objective.
5. **Inference**: Score all candidate items and rank by predicted score.
6. **Post-processing**: Apply business rules, diversity constraints.

### Ranking-Specific Considerations

- **Query structure**: Group training samples by user (query) so the model learns per-user ranking preferences.
- **Position bias**: Include position as a feature or apply position debiasing to avoid learning position effects.
- **Label grading**: Use graded relevance (not just binary click) for richer training signal.
- **Pairwise vs. listwise**: Pairwise for simple cases, listwise for complex ranking where list-level context matters.
- **Feature interactions**: Boosted trees naturally capture feature interactions without explicit feature crossing.
- **Sparse features**: Use feature hashing or embedding for high-cardinality categorical features.

### Boosted Trees in the Serving Pipeline

| Stage | Role of Boosted Trees |
|---|---|
| **Candidate generation** | Score initial candidates using features |
| **Pre-ranking** | Lightweight GBM for fast initial scoring |
| **Final ranking** | Deep GBM with rich features for final ranking |
| **Re-ranking** | GBM scores combined with business rules |

---

## When to Use Boosted Trees

| Scenario | Suitability |
|---|---|
| Rich tabular features available | Excellent |
| Need for interpretable model | Good (feature importance, SHAP) |
| Large dataset with sparse features | Excellent (LightGBM, CatBoost) |
| Need for fast inference | Good (tree traversal is fast) |
| Non-linear feature interactions | Excellent (trees capture interactions) |
| Very high-dimensional embeddings | Moderate (prefer neural models) |
| Sequential/temporal patterns | Moderate (combine with sequence features) |
