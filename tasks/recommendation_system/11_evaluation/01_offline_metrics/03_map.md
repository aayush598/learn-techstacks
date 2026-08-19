# Mean Average Precision (MAP)

## Overview

Mean Average Precision (MAP) is a set-based metric that evaluates the quality of ranked recommendation lists by considering both precision and the order in which relevant items appear. It is one of the most widely used metrics in information retrieval and recommendation evaluation, providing a single-number summary of ranking quality across all queries.

MAP extends Average Precision (AP), which itself extends Precision@K by averaging precision values at every relevant position in the ranked list. The "mean" in MAP refers to averaging AP scores across all users or queries in the evaluation set.

## Core Definitions

### Precision at Position K

Precision at position K measures the fraction of the top-K recommended items that are relevant:

```
Precision@K = (Number of relevant items in top-K) / K
```

For example, if a recommendation list of 5 items contains 3 relevant items, Precision@5 = 3/5 = 0.6.

### Average Precision (AP)

Average Precision computes the mean of precision values measured at each relevant item's position in the ranked list. Formally:

```
AP(Q) = (1 / |R|) * Σ (k=1 to n) [P(k) * rel(k)]
```

Where:
- `|R|` is the total number of relevant items for query Q
- `n` is the length of the ranked list
- `P(k)` is the precision at position k
- `rel(k)` is an indicator function (1 if item at position k is relevant, 0 otherwise)

A key subtlety: AP only considers precision values at positions where a relevant item actually appears. Positions between relevant items do not contribute new precision measurements—instead, the last measured precision is carried forward. This means AP rewards systems that place relevant items earlier in the list.

### Mean Average Precision (MAP)

MAP is the arithmetic mean of AP scores across all queries or users:

```
MAP = (1 / |Q|) * Σ (i=1 to |Q|) AP(Q_i)
```

Where `|Q|` is the total number of queries in the evaluation set.

## MAP@K Variant

In practice, we rarely evaluate infinitely long ranked lists. MAP@K truncates the evaluation at position K, computing AP only within the top-K recommendations:

```
MAP@K = (1 / |Q|) * Σ AP@K(Q_i)
```

The choice of K depends on the application:
- **Search engines**: K = 10 or 20 (users rarely scroll past the first page)
- **E-commerce**: K = 10–50 (depending on UI layout)
- **Content feeds**: K = 20–100 (infinite scroll scenarios)

Setting K too large can dilute the metric with irrelevant tail items; setting K too small may miss important ranking differences.

## Worked Example

Consider two recommendation systems evaluated on 3 users with the following ranked lists (R = relevant, N = non-relevant):

| Position | System A | System B |
|----------|----------|----------|
| 1        | R        | N        |
| 2        | N        | R        |
| 3        | R        | R        |
| 4        | R        | N        |
| 5        | N        | R        |

**System A AP calculation:**
- Position 1: P(1) = 1/1 = 1.0, relevant → contribution: 1.0
- Position 3: P(3) = 2/3 = 0.667, relevant → contribution: 0.667
- Position 4: P(4) = 3/4 = 0.75, relevant → contribution: 0.75
- AP(A) = (1.0 + 0.667 + 0.75) / 3 = 0.806

**System B AP calculation:**
- Position 2: P(2) = 1/2 = 0.5, relevant → contribution: 0.5
- Position 3: P(3) = 2/3 = 0.667, relevant → contribution: 0.667
- Position 5: P(5) = 3/5 = 0.6, relevant → contribution: 0.6
- AP(B) = (0.5 + 0.667 + 0.6) / 3 = 0.589

System A has higher MAP, correctly reflecting that it surfaces relevant items earlier.

## MAP for Recommendations

In the recommendation context, MAP has specific characteristics:

### Relevance Judgment Levels
- **Binary relevance**: Items are either relevant or not (most common)
- **Graded relevance**: Items have multiple relevance levels (e.g., 0–4). AP can be adapted by treating each relevance level as a binary threshold

### User-Level vs Global MAP
- **Per-user MAP**: Compute AP for each user independently, then average. This weights all users equally regardless of their number of relevant items
- **Global MAP**: Pool all user-item pairs and compute a single AP. This weights users with more relevant items more heavily

### Negative Feedback Handling
- Items explicitly disliked by a user are typically treated as non-relevant (rel = 0)
- Items the user has not interacted with present the classic "missing not at random" problem—MAP alone cannot distinguish between truly irrelevant and simply unexposed items

## Limitations of MAP

| Limitation | Description |
|------------|-------------|
| **Binary relevance bias** | Standard MAP treats all non-relevant items equally; it does not distinguish between "somewhat relevant" and "completely irrelevant" |
| **Equal weighting of all relevant items** | AP gives equal weight to each relevant item; in recommendations, the top-1 relevant item may be far more important than the 10th |
| **Ignores graded relevance** | While MAP can be adapted for graded relevance, the standard formulation requires binary judgments |
| **Sensitive to list length** | MAP@K values change significantly with K, making cross-paper comparisons difficult without standardized K |
| **Does not capture diversity** | MAP rewards finding all relevant items but does not penalize redundancy in recommendations |
| **Requires ground truth** | AP needs labeled relevance judgments, which are expensive to obtain at scale |
| **Assumes independence of queries** | MAP averages across users, treating each user's evaluation independently |

## When to Use MAP vs NDCG

### Use MAP When:
- **Binary relevance is sufficient**: Your relevance judgments are naturally binary (clicked/not clicked, purchased/not purchased)
- **Precision matters more than position**: You care about the fraction of relevant items in the top-K more than their exact ordering
- **Search-style evaluation**: The task is closer to information retrieval (finding all relevant documents) than to ranking quality
- **Uniform user importance**: All users should contribute equally to the metric regardless of engagement level
- **Simplicity is valued**: MAP is easier to explain to stakeholders than NDCG

### Use NDCG When:
- **Graded relevance**: You have multi-level relevance judgments (e.g., 5-star ratings, click-through with dwell time)
- **Position weighting matters**: Items at the top of the list should be weighted more heavily than items further down
- **Non-uniform utility**: The utility of showing a relevant item at position 1 is qualitatively different from showing it at position 20

### Side-by-Side Comparison

| Criterion | MAP | NDCG |
|-----------|-----|------|
| Relevance type | Binary | Graded |
| Position weighting | Equal per relevant item | Exponential decay |
| Interpretability | High | Moderate |
| Sensitivity to top positions | Moderate | High |
| Industry adoption | Search engines | Recommendations, ads |
| Theoretical foundation | Precision-recall | Utility theory |

## Practical Considerations

### Implementation Details
- When computing AP, handle tied scores by averaging precision across all possible orderings of tied items
- For MAP@K, ensure that the denominator for AP is `min(|R|, K)`, not `|R|`, to avoid artificially low scores when there are more relevant items than K

### Reporting Best Practices
- Always report MAP@K alongside the specific K value used
- Include confidence intervals (bootstrap or normal approximation) when comparing systems
- Report per-user MAP distribution, not just the mean, to understand variance across users
- Specify whether you are using binary or graded relevance

### Common Pitfalls
- Comparing MAP@10 against MAP@20 without acknowledging the difference
- Computing MAP on a test set where some users have zero relevant items (these users contribute AP = 0, dragging down the mean)
- Failing to exclude training interactions when computing AP on the test set
- Using MAP for cold-start users who have very few interactions, where the metric is unstable

## Advanced Variants

### Precision-Recall Breakdown
MAP provides a single number, but the underlying AP computation implicitly traces a precision-recall curve. Examining precision at multiple recall levels provides richer diagnostic information.

### MAP with Hierarchical Relevance
For applications with hierarchical relevance (e.g., a movie is relevant at the genre level and at the specific title level), weighted AP variants can assign different importance to different relevance levels.

### R-Precision Normalized MAP
R-Precision computes precision at rank R (where R is the total number of relevant items). R-normalized MAP divides each user's AP by their R-Precision, which can help when users have vastly different numbers of relevant items.
