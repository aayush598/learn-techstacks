# NDCG (Normalized Discounted Cumulative Gain)

## Overview

Normalized Discounted Cumulative Gain (NDCG) is the gold standard metric for evaluating ranked lists in information retrieval and recommendation systems. Unlike precision and recall, NDCG accounts for both graded relevance and position in the ranked list, making it ideally suited for recommendation evaluation where the order of items directly impacts user experience.

## Core Concepts

### Cumulative Gain (CG)

Cumulative Gain is the simplest metric — it sums the relevance scores of all recommended items.

```
CG@K = Σᵢ₌₁ᴷ relᵢ
```

- `relᵢ` is the relevance score of the item at position i.
- CG@K is position-agnostic; it does not consider the order of items.
- Useful as a building block but insufficient alone for ranked evaluation.

### Discounted Cumulative Gain (DCG)

DCG applies a logarithmic discount to penalize relevant items appearing at lower positions. The intuition is that users are less likely to see items deeper in the list, so those items contribute less to the overall quality.

**Standard DCG Formula (for binary relevance)**:

```
DCG@K = Σᵢ₌₁ᴷ (2^relᵢ - 1) / log₂(i + 1)
```

**Alternative DCG Formula (common in industry)**:

```
DCG@K = Σᵢ₌₁ᴷ relᵢ / log₂(i + 1)
```

- The logarithmic discount `1/log₂(i+1)` reduces the contribution of items at lower positions.
- Position 1 receives no discount (log₂(2) = 1).
- Position 10 receives a discount factor of ~0.33 (1/log₂(11)).
- The `2^relᵢ - 1` formulation (used in the original paper) emphasizes highly relevant items exponentially.

### Normalized DCG (NDCG)

NDCG normalizes DCG against the Ideal DCG (IDCG) — the best possible DCG for that user given their relevant items.

```
NDCG@K = DCG@K / IDCG@K
```

- Range: [0, 1], where 1 indicates the ranking matches the ideal ordering.
- IDCG@K is computed by sorting all relevant items by relevance score in descending order.
- NDCG enables comparison across users with different numbers of relevant items.

### IDCG Calculation Example

For a user with relevant items scored [3, 2, 2, 1, 1] and K=4:

```
IDCG@4 = 3/log₂(2) + 2/log₂(3) + 2/log₂(4) + 1/log₂(5)
       = 3/1 + 2/1.585 + 2/2 + 1/2.322
       = 3 + 1.262 + 1 + 0.431
       = 5.693
```

## Position Discount Mechanisms

### Logarithmic Discount (Standard)

- Formula: `1/log₂(i + 1)`
- Widely used and well-understood.
- Provides strong discount for top positions with diminishing effect deeper in the list.
- Used in most academic papers and industry implementations.

### Linear Discount

- Formula: `1/i`
- Stronger penalty for lower positions than logarithmic.
- Used when position sensitivity is more important.
- Rarely used in modern recommendation evaluation.

### Exponential Discount

- Formula: `1/2^i`
- Extremely strong emphasis on top positions.
- Used in scenarios where only the very top items matter (e.g., voice assistants).
- Aggressive: items at position 5+ have negligible contribution.

### No Discount (CG)

- Formula: `1` (constant)
- Equivalent to Cumulative Gain.
- Use only when position is irrelevant to the evaluation.

### Discount Comparison Table

| Position | Linear (1/i) | Log (1/log₂(i+1)) | Exponential (1/2^i) |
|----------|-------------|-------------------|---------------------|
| 1 | 1.000 | 1.000 | 0.500 |
| 2 | 0.500 | 0.631 | 0.250 |
| 3 | 0.333 | 0.500 | 0.125 |
| 5 | 0.200 | 0.387 | 0.031 |
| 10 | 0.100 | 0.289 | 0.001 |
| 20 | 0.050 | 0.230 | 0.000 |

## NDCG@K Variants

### Standard NDCG@K

- Evaluate the top K positions only.
- IDCG is computed considering only the top K items from the ideal ranking.
- Most common variant in recommendation evaluation.

### NDCG with Binary Relevance

- All relevant items have relevance = 1; non-relevant items have relevance = 0.
- Simplifies the metric but loses granularity.
- Useful when relevance is naturally binary (clicked/not clicked).

### NDCG with Graded Relevance

- Relevance scores on a multi-point scale (0-4, 0-1, or continuous).
- Captures nuanced differences in item quality.
- Requires careful calibration of relevance scores.

### NDCG with Exponential Relevance

- Uses `2^relᵢ` instead of `relᵢ` in the DCG formula.
- Amplifies the contribution of highly relevant items.
- Original formulation from the Jarvelin & Kekalainen paper.
- Better suited when high-relevance items are significantly more valuable.

## Comparison with Precision/Recall

| Aspect | Precision/Recall | NDCG |
|--------|-----------------|------|
| **Position awareness** | No — treats all K positions equally | Yes — logarithmic discount |
| **Relevance granularity** | Binary (relevant/not) | Graded (continuous scores) |
| **Score range** | [0, 1] | [0, 1] |
| **Interpretability** | High — intuitive meaning | Medium — requires explanation |
| **Sensitivity to swap** | Low — same P/R regardless of order | High — swapping changes score |
| **Computational complexity** | O(K) per user | O(K) per user |
| **Industry standard** | Yes | Yes (preferred for ranking) |

### When NDCG is Superior

- Evaluating different ranking orders with the same set of recommended items.
- When items have graded relevance (not just binary).
- When position in the list significantly impacts user engagement.
- Comparing models that produce different ranking orders.

### When Precision/Recall is Preferable

- Binary relevance scenarios with clear relevant/not-relevant distinction.
- Stakeholder communication where simplicity matters.
- When the number of relevant items is very small (NDCG can be unstable).
- Evaluating retrieval quality before ranking (candidate generation stage).

## When to Use NDCG

### Primary Use Cases

- **Model Comparison**: Comparing different ranking models or hyperparameter configurations.
- **Feature Importance**: Measuring the impact of individual features on ranking quality.
- **A/B Test Validation**: Offline proxy for online ranking quality changes.
- **Production Monitoring**: Tracking ranking quality degradation over time.

### Recommended K Values

| K Value | Application | Notes |
|---------|------------|-------|
| 3 | Voice assistants, featured content | Very few items displayed |
| 5 | Homepage recommendations | Common for personalized feeds |
| 10 | Standard recommendation lists | Most common evaluation cutoff |
| 20 | Extended lists, email recommendations | When more items are shown |
| 50 | Precomputed batch recommendations | Offline serving scenarios |
| 100 | Full catalog ranking | Candidate retrieval quality |

### Reporting Best Practices

- Always report NDCG at the K matching production display.
- Report mean NDCG across all users (macro-averaged).
- Report NDCG distribution (percentiles) not just the mean.
- Include confidence intervals when comparing models.
- Report NDCG alongside precision/recall for comprehensive evaluation.

## Implementation Considerations

### Computational Efficiency

- DCG computation is O(K) per user, where K is the cutoff.
- IDCG computation requires sorting relevant items, O(R log R) where R is the number of relevant items.
- For large-scale evaluation, use vectorized implementations (NumPy, pandas).
- Cache IDCG values when evaluating multiple models against the same test set.

### Handling Edge Cases

- **No relevant items**: NDCG is undefined. Exclude these users or set NDCG = 0.
- **All items relevant**: NDCG = 1 regardless of ranking (IDCG = DCG).
- **Single relevant item**: NDCG reduces to binary relevance metric.
- **Tied relevance scores**: Multiple valid ideal orderings; use any.

### Statistical Considerations

- Use bootstrap resampling to compute confidence intervals for NDCG.
- Report p-values when comparing models (paired t-test or Wilcoxon signed-rank).
- Account for multiple comparisons when testing many model variants.
- Use effect size (Cohen's d) alongside p-values for practical significance.

## Interleaving Metrics

### Online Interleaving

- Interleaving combines recommendations from two models (A and B) into a single list.
- User interaction with the interleaved list reveals which model's recommendations are preferred.
- More sensitive than A/B testing for detecting small performance differences.

### Interleaving Methods

**Team Draft Interleaving (TDI)**

- Each model (team) takes turns drafting items into the interleaved list.
- The model whose items are clicked more wins the comparison.
- Simple to implement but may introduce position bias.

**Probabilistic Interleaving (PI)**

- Each position in the interleaved list is randomly assigned to model A or B.
- Clicks are attributed probabilistically based on which model proposed each item.
- More unbiased than TDI but more complex to implement.

**Balanced Interleaving**

- Ensures equal representation of both models in the interleaved list.
- Reduces position bias compared to TDI.
- Used in production at major tech companies.

### Interleaving vs A/B Testing

| Aspect | Interleaving | A/B Testing |
|--------|-------------|-------------|
| Sensitivity | 10-100x more sensitive | Standard sensitivity |
| Sample size needed | ~100-1,000 users | ~10,000-100,000 users |
| Duration | Hours to days | Days to weeks |
| Metric | Relative preference | Absolute metric difference |
| Deployment complexity | Higher (dual-model serving) | Lower (traffic splitting) |
| Statistical method | Click attribution | Standard hypothesis testing |

### When to Use Interleaving

- Comparing two similar models with uncertain performance differences.
- Rapid iteration cycles where A/B testing is too slow.
- Early-stage model evaluation before committing to expensive A/B tests.
- Detecting small but meaningful improvements that justify production deployment.

## Advanced NDCG Variants

### Expected Reciprocal Rank (ERR)

```
ERR@K = Σᵢ₌₁ᴷ (1/i) × P(relevant at i | not relevant before i)
```

- Models the expected position of the first relevant item.
- More intuitive than NDCG for single-relevance-position evaluation.
- Useful when the first relevant item matters most (search-like scenarios).

### Weighted NDCG (WNDCG)

- Apply position-specific weights to account for position-dependent click probabilities.
- Weights can be learned from historical click data.
- Better reflects actual user behavior than fixed logarithmic discount.

### Intent-Aware NDCG

- Weight NDCG by the probability that the user has a specific intent.
- Useful when users have multiple intents in a single session.
- Requires intent detection as an additional component.
