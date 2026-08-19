# Blending Ensemble for Recommendations

## Overview

Blending is an ensemble technique that combines multiple recommendation models using a holdout validation set. Unlike stacking (which uses cross-validation), blending uses a simple train/validation split, making it computationally efficient and easy to implement. The blending weights are learned from the validation set predictions of each base model.

---

## Holdout Validation Set

### Data Split

| Set | Purpose | Typical Size |
|---|---|---|
| **Training set** | Train base models | 60–70% |
| **Blending set** (validation) | Learn blending weights | 15–20% |
| **Test set** | Final evaluation | 15–20% |

### Critical Requirements

- **Independence**: The blending set must not be used for training any base model. Any data leakage invalidates the blending weights.
- **Representativeness**: The blending set should be representative of the production data distribution.
- **Temporal split**: For time-dependent data, use a temporal split (earlier data for training, later data for blending).

### Why Holdout Instead of Cross-Validation?

| Aspect | Holdout (Blending) | Cross-Validation (Stacking) |
|---|---|---|
| Computational cost | Lower (single split) | Higher (K splits) |
| Implementation simplicity | Simple | More complex |
| Data efficiency | Lower (less data for training) | Higher (each sample used in training) |
| Variance of weights | Higher (single split) | Lower (averaged over folds) |
| Risk of leakage | Lower (simple split) | Higher (must carefully manage folds) |

---

## Blending Weights

### Linear Blending

The simplest form: a weighted linear combination of base model predictions:

**final_score = Σ_i w_i × score_i**

Where:
- **score_i**: Prediction from base model i.
- **w_i**: Blending weight for model i.
- **Constraint**: Σ w_i = 1, w_i ≥ 0.

### Learning Blending Weights

Solve a regression problem on the blending set:

**min_w Σ_{(u,i,r) in blending set} (r - Σ_j w_j × score_j(u,i))² + λ||w||²**

This is a standard regularized linear regression problem with a closed-form solution.

### Weight Interpretation

| Weight Pattern | Interpretation |
|---|---|
| One model dominates (w₁ > 0.9) | Other models are not contributing meaningfully |
| Roughly equal weights | All models contribute similarly |
| Negative weight | Model is anti-correlated with others (useful for diversity) |
| Sum of weights far from 1 | Scaling issue or data quality problem |

---

## Multi-Layer Blending

### Two-Layer Blending

Instead of a single combination, use a two-stage approach:

1. **Layer 1**: Group base models into clusters (e.g., CF models, content models, deep learning models).
2. **Layer 2**: Combine cluster outputs using learned weights.

### Why Multi-Layer?

- **Reduces overfitting**: Fewer weights to learn at each layer.
- **Interpretability**: Understand which model families contribute most.
- **Modularity**: Add or remove models within a cluster without retraining the full ensemble.

### Multi-Layer Architecture

| Layer | Models | Output |
|---|---|---|
| **Layer 1A** | CF models (MF, ALS, item-based) | CF ensemble score |
| **Layer 1B** | Content models (text similarity, image similarity) | Content ensemble score |
| **Layer 1C** | Deep learning models (DNN, Transformer) | DL ensemble score |
| **Layer 2** | Combine CF, Content, DL ensemble scores | Final blended score |

---

## Blending vs. Stacking vs. Weighted Average

| Technique | Weight Learning | Data Usage | Complexity | Flexibility |
|---|---|---|---|---|
| **Weighted average** | Fixed or heuristic | No learning | Very low | Low |
| **Blending** | Regression on holdout set | Single validation set | Low | Moderate |
| **Stacking** | Meta-learner on CV predictions | Cross-validation | Moderate | High |
| **Bayesian model averaging** | Posterior model weights | Full dataset | High | High |

### When to Use Blending

- **Rapid prototyping**: Quickly combine multiple models to evaluate ensemble potential.
- **Resource constraints**: Limited compute for cross-validation or complex meta-learning.
- **Model diversity**: Base models are already well-tuned and diverse.
- **Production simplicity**: Simple to implement, debug, and maintain.

### Blending Best Practices

1. **Regularize**: Use L2 regularization on blending weights to prevent overfitting to the blending set.
2. **Monitor**: Track blending weights over time. Drifting weights indicate changing model performance.
3. **Constrain**: Enforce non-negativity and sum-to-one constraints for interpretability.
4. **Validate**: Compare blending performance against the best single model. If blending doesn't improve, the base models may not be diverse enough.
5. **Retrain**: Periodically retrain blending weights as new data arrives.

---

## Non-Linear Blending

### Beyond Linear Combination

Linear blending assumes models contribute independently. Non-linear blending captures model interactions:

| Method | Description | Complexity |
|---|---|---|
| **GBM blender** | Use gradient boosted trees to combine model predictions | Medium |
| **Neural blender** | Train a small neural network on model predictions | Medium-High |
| **Rule-based blender** | Use conditional rules to select model based on context | Low |
| **Meta-learning blender** | Learn blending policy from data with contextual features | High |

### Non-Linear Blending Example

A GBM blender takes as input the predictions of all base models plus contextual features:

- Base model predictions (scores from CF, content, deep learning models).
- User features (interaction count, segment, activity level).
- Item features (popularity, category, age).
- Context features (time of day, device, session depth).

The GBM learns complex blending rules like "trust CF when user is active and item is popular, but trust content-based when the item is new."

---

## Blending for Different Recommendation Stages

| Stage | Blending Approach | Rationale |
|---|---|---|
| **Candidate generation** | Union of candidates from multiple sources | Maximize recall |
| **Pre-ranking** | Linear blending of lightweight models | Fast, simple |
| **Final ranking** | Non-linear blending or stacking | Complex interactions |
| **Re-ranking** | Rule-based blending with diversity | Business constraints |

---

## Common Pitfalls

- **Data leakage**: Using the blending set for model training invalidates the blending weights. Always maintain strict separation.
- **Overfitting to blending set**: With many base models and a small blending set, the learned weights may overfit. Use regularization and monitor test set performance.
- **Model redundancy**: If base models are highly correlated, blending provides little improvement. Measure model diversity before investing in blending.
- **Stale weights**: Model performance changes over time. Blending weights trained on historical data may not reflect current performance. Retrain regularly.
- **Interpretability loss**: Non-linear blending makes it harder to understand why specific recommendations are made. Consider interpretability when choosing blending complexity.
