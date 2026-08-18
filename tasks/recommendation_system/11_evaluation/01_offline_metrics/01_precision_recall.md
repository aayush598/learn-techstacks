# Precision and Recall for Recommendations

## Overview

Precision and recall are foundational evaluation metrics adapted from information retrieval. In the recommendation context, they measure the accuracy of a model's ability to surface relevant items among the top-K recommendations. While conceptually simple, their application to recommendation systems requires careful consideration of relevance definitions, cutoff thresholds, and averaging strategies.

## Fundamental Definitions

### Precision

Precision measures the fraction of recommended items that are relevant to the user. It answers: "Of the items I recommended, how many did the user actually want?"

**Formal Definition**:

```
Precision@K = |{relevant items} ∩ {top-K recommended items}| / K
```

- Range: [0, 1], where 1 indicates all recommended items are relevant.
- K is the number of top recommendations evaluated.
- Precision@K does not consider items that were relevant but not recommended.

### Recall

Recall measures the fraction of relevant items that were successfully recommended. It answers: "Of all the items the user wanted, how many did I recommend?"

**Formal Definition**:

```
Recall@K = |{relevant items} ∩ {top-K recommended items}| / |{relevant items}|
```

- Range: [0, 1], where 1 indicates all relevant items were recommended.
- Recall depends on the total number of relevant items, which may be unknown.
- Recall@K increases monotonically with K (recommending more items captures more relevant ones).

### F1 Score

The F1 score is the harmonic mean of precision and recall, providing a single metric that balances both concerns.

```
F1@K = 2 × (Precision@K × Recall@K) / (Precision@K + Recall@K)
```

- Range: [0, 1], where 1 indicates perfect precision and recall.
- The harmonic mean penalizes extreme imbalances between precision and recall.
- More informative than arithmetic mean when precision and recall differ significantly.

## Calculation Methodology

### Per-User Calculation

For a single user u and recommendation list of size K:

1. Identify the set of relevant items for user u (based on relevance threshold).
2. Identify the top-K recommended items for user u.
3. Compute the intersection of relevant and recommended items.
4. Precision@K = |intersection| / K.
5. Recall@K = |intersection| / |relevant items for u|.
6. F1@K = harmonic mean of precision and recall.

### Aggregation Across Users

**Micro-Averaging**

- Pool all user predictions together before computing metrics.
- Treats every (user, item) pair equally regardless of user activity level.
- Biased toward active users (users with many interactions) because they contribute more pairs.
- Formula: micro-precision = Σ|intersection_i| / (N × K), where N is the number of users.

**Macro-Averaging**

- Compute precision and recall for each user independently, then average.
- Treats every user equally regardless of activity level.
- Sensitive to users with few relevant items (may have artificially high or low scores).
- Formula: macro-precision = (1/N) × Σ precision_i, where N is the number of users.

**Weighted Averaging**

- Weight each user's metric by their interaction count or importance score.
- Balances between micro and macro approaches.
- Useful when user importance varies (e.g., paying users weighted higher).

### Sample Metrics Table

| User | Relevant Items | Recommended@5 | Intersection | P@5 | R@5 | F1@5 |
|------|---------------|---------------|--------------|-----|-----|------|
| Alice | 10 | 5 | 4 | 0.80 | 0.40 | 0.53 |
| Bob | 5 | 5 | 3 | 0.60 | 0.60 | 0.60 |
| Carol | 20 | 5 | 5 | 1.00 | 0.25 | 0.40 |
| **Micro** | 35 | 25 | 12 | **0.48** | **0.34** | **0.40** |
| **Macro** | - | - | - | **0.80** | **0.42** | **0.51** |

## Precision@K and Recall@K Variants

### Varying K

| K Value | Interpretation | Typical Use Case |
|---------|---------------|------------------|
| 1 | Top recommendation only | Notification, featured content |
| 3 | Top 3 | Homepage carousel |
| 5 | Top 5 | Search results page |
| 10 | Top 10 | Standard recommendation list |
| 20 | Top 20 | Exploration/discovery sections |
| 50 | Top 50 | Email recommendations |
| 100 | Top 100 | Catalog browsing, precomputed |

### Precision-Recall Tradeoff

- **Small K (1-5)**: High precision, low recall. Good for user-facing surfaces where quality matters.
- **Medium K (10-20)**: Balanced precision and recall. Standard for most recommendation lists.
- **Large K (50-100)**: Lower precision, higher recall. Good for offline use cases (email, push notifications).

### Choosing the Right K

- Match K to the actual number of items shown to the user in production.
- If the UI shows 10 items, evaluate precision@10 and recall@10.
- Report metrics at multiple K values for comprehensive evaluation.
- Never evaluate at K larger than the number of items you actually serve.

## Relevance Thresholds

### Binary Relevance

- Items are either relevant (1) or not relevant (0).
- Simple to define but may not capture nuanced user preferences.
- Common thresholds: click = relevant, purchase = relevant, rating > 3 = relevant.

### Graded Relevance

- Items receive a relevance score on a scale (e.g., 0-4 or 0-1).
- Enables more nuanced evaluation of recommendation quality.
- Requires extending precision/recall to handle graded relevance (see NDCG).

### Common Relevance Definitions

| Signal | Binary Threshold | Graded Scale | Caveats |
|--------|-----------------|--------------|---------|
| Click | clicked = 1 | dwell time based | Clickbait inflates relevance |
| Like/Heart | liked = 1 | N/A | Only positive signal |
| Purchase | purchased = 1 | N/A | High precision, low recall |
| Rating | rating ≥ 4 | 1-5 scale | Sparse, biased |
| View Duration | >30 seconds | Continuous | Varies by content type |
| Multi-signal | Weighted combination | 0-1 score | Complex, requires tuning |

### Implicit vs Explicit Feedback

- **Explicit Feedback** (ratings, likes): Direct relevance signal but sparse and biased.
- **Implicit Feedback** (clicks, views, purchases): Abundant but noisy and one-sided (absence of interaction does not mean dislike).

## Limitations of Precision/Recall for Recommendations

### Fundamental Limitations

- **Position Blindness**: Standard precision@K treats all positions equally. A relevant item at position 1 is worth the same as at position K.
- **No Ranking Awareness**: Precision@K does not capture whether the most relevant items appear first.
- **Binary Assumption**: Basic precision/recall assumes binary relevance, which oversimplifies user preferences.
- **Dependence on K**: Metrics change significantly with different K values, making comparison difficult.
- **Unknown Relevant Items**: Recall requires knowing all relevant items, which is typically impossible.

### Recommendation-Specific Challenges

- **Missing Not-Relevant Data**: We only observe positive interactions; missing data is ambiguous (not interested vs. not exposed).
- **Position Bias**: Users are more likely to interact with items shown in top positions, inflating apparent relevance.
- **Popularity Bias**: Popular items appear relevant more often, skewing precision calculations.
- **Exposure Bias**: Items never shown to users cannot be evaluated as relevant or irrelevant.

### Mitigation Strategies

- Combine precision/recall with ranking-aware metrics (NDCG, MAP).
- Use calibrated propensity scoring to correct for position and exposure bias.
- Evaluate at realistic K values matching production UI constraints.
- Supplement with online metrics (CTR, engagement) for validation.

## Comparison with Other Metrics

### Precision/Recall vs NDCG

| Aspect | Precision/Recall | NDCG |
|--------|-----------------|------|
| Position awareness | No | Yes (discount factor) |
| Relevance granularity | Binary | Graded |
| Interpretability | High | Medium |
| Computational cost | Low | Low |
| Industry adoption | High | High |

### Precision/Recall vs MAP

| Aspect | Precision/Recall | MAP |
|--------|-----------------|-----|
| Ranking consideration | No | Yes (average precision) |
| Single cutoff | Yes (at K) | No (all positions) |
| User-level metric | Yes | Yes |
| Requires relevance ordering | No | Yes |

### When to Use Precision/Recall

- When you need simple, interpretable metrics for stakeholder communication.
- When evaluating binary relevance (relevant/not relevant).
- When the position of recommendations does not significantly impact user experience.
- As a baseline metric for comparing model iterations.
- When combined with other metrics for comprehensive evaluation.

## Best Practices

- Always report both precision and recall together; one alone is insufficient.
- Report metrics at the K value matching your production UI.
- Use micro-averaging for system-level metrics and macro-averaging for user-fairness metrics.
- Define relevance thresholds clearly and document them alongside reported metrics.
- Complement offline precision/recall with online A/B testing results.
- Track precision/recall trends over time to detect model degradation.
