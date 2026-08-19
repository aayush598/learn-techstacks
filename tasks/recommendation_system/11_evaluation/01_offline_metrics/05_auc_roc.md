# AUC-ROC

## Overview

The Area Under the Receiver Operating Characteristic Curve (AUC-ROC) is a threshold-independent metric that evaluates a model's ability to distinguish between positive and negative classes across all possible classification thresholds. In recommendation systems, AUC-ROC measures how well a model ranks positive interactions (relevant items) above negative ones (irrelevant items).

AUC-ROC provides a single scalar value between 0 and 1, where:
- **1.0** = perfect separation (all positives ranked above all negatives)
- **0.5** = random discrimination (no ranking ability)
- **0.0** = perfect inversion (all negatives ranked above all positives)

## ROC Curve Construction

### True Positive Rate (TPR) and False Positive Rate (FPR)

The ROC curve plots TPR against FPR at various threshold settings:

```
TPR (Sensitivity / Recall) = TP / (TP + FN)
FPR (1 - Specificity) = FP / (FP + TN)
```

Where:
- TP = True Positives (relevant items ranked above threshold)
- FP = False Positives (irrelevant items ranked above threshold)
- TN = True Negatives (irrelevant items ranked below threshold)
- FN = False Negatives (relevant items ranked below threshold)

### Construction Algorithm

1. Score all items using the model (predicted relevance scores)
2. Sort items by score in descending order
3. Iterate through possible thresholds (each unique score value)
4. At each threshold, compute TPR and FPR
5. Plot the resulting (FPR, TPR) pairs
6. Connect points with line segments

For a ranked list, the ROC curve is equivalent to plotting the cumulativeTP rate against the cumulative FP rate as we move down the ranked list.

### Mathematical Definition

```
AUC = ∫₀¹ TPR(FPR⁻¹(t)) dt
```

This integral represents the probability that a randomly chosen positive item is ranked higher than a randomly chosen negative item.

## AUC Interpretation

### Probabilistic Interpretation
AUC equals the probability that a randomly selected positive instance receives a higher score than a randomly selected negative instance:

```
AUC = P(score(pos) > score(neg))
```

This interpretation is powerful because it is threshold-independent and intuitive to stakeholders.

### Common AUC Ranges

| AUC Range | Interpretation |
|-----------|---------------|
| 0.90–1.00 | Excellent discrimination |
| 0.80–0.90 | Good discrimination |
| 0.70–0.80 | Fair discrimination |
| 0.60–0.70 | Poor discrimination |
| 0.50–0.60 | No discrimination (random) |

### What AUC Does Not Tell You
- **Threshold selection**: AUC does not indicate the optimal operating point
- **Calibration**: A model with high AUC may have poorly calibrated probabilities
- **Per-position quality**: AUC treats all ranking positions equally
- **Class distribution sensitivity**: AUC can be misleading with extreme class imbalance

## AUC for Ranking vs Classification

### Classification AUC
In traditional classification, AUC evaluates how well a model separates two classes. Each sample gets exactly one score, and the metric compares scores across all positive-negative pairs.

### Ranking AUC (pAUC or Ranking-Metric)
In recommendation, we evaluate ranked lists. The "ranking AUC" differs from classification AUC:

| Aspect | Classification AUC | Ranking AUC |
|--------|-------------------|-------------|
| Input | Individual scores per sample | Ranked list per query/user |
| Positive class | Actual positive samples | Items the user interacted with |
| Negative class | Actual negative samples | Items the user did not interact with |
| Independence | Samples are independent | Items within a list are correlated |
| Aggregation | One AUC over all samples | Per-user AUC, then averaged |

### Per-User AUC
For recommendations, compute AUC for each user independently:

```
AUC_u = P(score(pos_item_u) > score(neg_item_u))
AUC = (1/|U|) * Σ AUC_u
```

This ensures each user contributes equally to the metric regardless of their number of interactions.

### Macro vs Micro AUC
- **Macro AUC**: Average per-user AUC (each user weighted equally)
- **Micro AUC**: Pool all user-item pairs and compute a single AUC (users with more interactions contribute more)

## AUC Limitations for Recommendations

| Limitation | Description |
|------------|-------------|
| **Ignores rank position** | AUC only cares that positives are above negatives, not their exact positions. A model that ranks all positives at position 51 (just above negatives at 52+) gets the same AUC as one ranking them at position 1 |
| **Uniform negative sampling** | Standard AUC computation treats all negatives equally; in reality, some negatives are "hard" (near-misses) and others are "easy" (completely irrelevant) |
| **Threshold agnostic** | AUC does not penalize a model for having all scores clustered in a narrow range, which can cause deployment issues |
| **Interaction-level, not list-level** | AUC evaluates pairwise comparisons, not the quality of the full ranked list as presented to the user |
| **Insensitive to list truncation** | AUC@K is needed to focus on top-K quality; raw AUC considers the entire score space |
| **Misleading with skewed class ratios** | When negatives vastly outnumber positives (common in recommendations), AUC can appear high even when Precision@K is very low |

### The AUC Paradox in Recommendations

A toy example: Consider a system with 1000 items, 5 relevant. A model ranks all 5 relevant items at positions 990–994 (out of 1000). AUC = 0.994 (nearly all negatives are below all positives). But no user would ever see a relevant item—Precision@10 = 0. This paradox illustrates why AUC should never be used as the sole metric for recommendations.

## Partial AUC (pAUC)

Partial AUC focuses on a specific region of the ROC curve, typically the low-FPR region that corresponds to the top of the ranked list.

### pAUC Definition

```
pAUC(FPR_max) = ∫₀^FPR_max TPR(FPR⁻¹(t)) dt / FPR_max
```

The normalization by FPR_max ensures the score is between 0 and 1.

### Why pAUC Matters

In recommendations, users only see the top few items. The low-FPR region of the ROC curve corresponds to these top positions. A model with high overall AUC but poor pAUC at FPR = 0.01 may actually perform poorly for users.

### Choosing the FPR Cutoff

| FPR Cutoff | Corresponds To | Use Case |
|-----------|---------------|----------|
| 0.01 | Top 1% of negatives | Very large catalogs (100K+ items) |
| 0.05 | Top 5% of negatives | Medium catalogs (10K–100K items) |
| 0.10 | Top 10% of negatives | Small catalogs (< 10K items) |

## AUC with Imbalanced Data

Recommendation datasets are heavily imbalanced (100:1 to 1000:1 negative-to-positive ratios). This creates specific challenges:

### Issues
- AUC remains relatively stable under class imbalance (a key advantage over accuracy)
- However, the ranking quality at the top of the list can degrade while AUC stays high
- Confidence intervals become harder to compute with extreme imbalance

### Mitigation Strategies
1. **Use stratified sampling**: Sample negatives to create a balanced evaluation set, then adjust AUC
2. **Report pAUC alongside AUC**: pAUC at a fixed FPR is more robust to imbalance
3. **UseAUROC withPR-AUC**: Precision-Recall AUC is more informative under extreme imbalance
4. **Per-user evaluation**: Compute AUC per user (each user has a balanced positive/negative ratio within their interaction history)

### Complementing AUC with PR-AUC

| Metric | Strengths | Weaknesses |
|--------|----------|------------|
| AUC-ROC | Stable under imbalance, interpretable | Misleading for top-K quality |
| PR-AUC | Sensitive to precision at top ranks | Depends heavily on prevalence |

Reporting both provides a more complete picture of model performance.

## Practical Considerations

### Implementation Notes
- AUC can be computed efficiently using the Mann-Whitney U statistic: `AUC = U / (n_pos * n_neg)`
- For large datasets, approximate AUC using sampled pairs
- Ensure proper handling of tied scores (average the AUC of all possible orderings)

### Common Mistakes
- Computing AUC on training data (inflated by overfitting)
- Ignoring the per-user structure (pooling all interactions together)
- Using AUC as the primary metric for production decisions (use NDCG or MAP instead)
- Not reporting confidence intervals

### When to Use AUC
- **Model development**: Quick comparison of model variants during experimentation
- **Feature importance**: AUC change when removing a feature indicates its discriminative power
- **Ensemble selection**: Combine models that maximize AUC on validation data
- **Calibration check**: Low AUC indicates a fundamental modeling problem, regardless of other metrics
