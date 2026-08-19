# Baseline Comparisons

## Overview

Baseline comparisons establish the performance floor against which new recommendation algorithms are measured. A baseline is a simple, well-understood method that provides a reference point: if your sophisticated deep learning model cannot significantly outperform a popularity-based baseline, either the model is not working or the problem is fundamentally different from what you assumed. Baselines are essential for grounding research and development in reality.

## Popularity-Based Baseline

### Definition

Recommend the most popular items to all users, regardless of individual preferences.

### Variants

| Variant | Description | Formula |
|---------|-------------|---------|
| **Global popularity** | Rank by total interactions across all users | Count(interactions(item_i)) |
| **Time-windowed popularity** | Rank by interactions in recent window | Count(interactions(item_i, last_T_days)) |
| **Decayed popularity** | Weight recent interactions more heavily | Σ exp(-λ × age) per interaction |
| **Segment popularity** | Rank by popularity within user segments | Count(interactions(item_i, segment_s)) |

### When Popularity Baseline Is Competitive

- **Cold-start users**: No personalization signal available
- **Narrow catalogs**: When most items are relevant to most users
- **Short-term trends**: Viral content where popularity IS the signal
- **High-uncertainty domains**: When user preferences are noisy

### Popularity Baseline Performance

| Metric | Typical Range | Interpretation |
|--------|--------------|---------------|
| Precision@10 | 0.01–0.05 | Low but non-trivial |
| Recall@100 | 0.05–0.15 | Captures head items |
| NDCG@10 | 0.02–0.08 | No position optimization |
| Coverage@10 | 0.001–0.01 | Very low (only popular items) |

## Random Baseline

### Definition

Recommend items randomly, either uniformly or weighted by popularity.

### Variants

| Variant | Description | Use Case |
|---------|-------------|---------|
| **Uniform random** | Equal probability for all items | Lower bound for any metric |
| **Popularity-weighted random** | Probability proportional to popularity | Simulates naive personalized system |
| **Category-balanced random** | Random within category proportions | Tests category balance |
| **Constrained random** | Random within business constraints | Tests constraint impact |

### Why Random Baselines Matter

- **Theoretical lower bound**: Any model worse than random is actively harmful
- **A/B test control**: Random recommendations serve as a clean control group
- **Metric calibration**: Understanding what "random" scores look like helps interpret model scores
- **Debugging**: If your model performs similarly to random, something is fundamentally broken

### Random Baseline Expected Metrics

| Metric | Expected Value | Formula |
|--------|---------------|---------|
| Precision@K | \|relevant\| / \|catalog\| | Depends on catalog size |
| Recall@K | K / \|catalog\| (approximately) | For uniform random |
| NDCG@K | Very low | Essentially random ordering |
| AUC | ~0.5 | No discrimination ability |

## Most-Recent Baseline

### Definition

Recommend the most recently added or most recently interacted-with items.

### Variants

| Variant | Description | Application |
|---------|-------------|------------|
| **Newest items** | Items sorted by creation/publication date | News, content platforms |
| **Recently viewed** | Items the user recently interacted with | E-commerce, media |
| **Trending** | Items with rapidly increasing interaction rates | Social media, news |
| **Most recently popular** | Items that were most popular in the last hour/day | Real-time platforms |

### When Most-Recent Is Competitive

- **News and media**: Freshness IS relevance
- **Trend-driven platforms**: Users want what's currently popular
- **Seasonal products**: Recency correlates with relevance during seasons
- **Repeat purchase items**: Users often re-purchase recently consumed items

### Recency Baseline Performance

| Metric | News/Media | E-commerce | Social |
|--------|-----------|-----------|--------|
| Precision@10 | 0.05–0.15 | 0.01–0.03 | 0.02–0.08 |
| NDCG@10 | 0.05–0.12 | 0.01–0.05 | 0.03–0.08 |
| Coverage | High | Medium | Medium |
| Novelty | High | Low | Medium |

## Content-Based Baseline

### Definition

Recommend items similar to what the user has previously interacted with, based on item features (not collaborative signals).

### Implementation

1. Build user profile from interacted items' features (TF-IDF, embeddings, category distributions)
2. Score candidate items by similarity to user profile
3. Rank by similarity score

### Content-Based Baseline Variants

| Variant | Feature Type | Similarity Measure |
|---------|-------------|-------------------|
| **TF-IDF** | Text features | Cosine similarity |
| **Embedding-based** | Learned item embeddings | Cosine / L2 distance |
| **Attribute-based** | Categorical attributes | Jaccard / overlap |
| **Hybrid content** | Mixed feature types | Weighted combination |

### When Content-Based Is Competitive

- **Diverse catalogs**: When collaborative signals are weak
- **Niche interests**: When users have specific, consistent preferences
- **New items**: Content-based can recommend new items immediately
- **Privacy-sensitive domains**: No collaborative data needed

### Content-Based Baseline Performance

| Metric | Typical Range | Advantage |
|--------|--------------|-----------|
| Precision@10 | 0.03–0.10 | Good for niche users |
| Recall@100 | 0.05–0.15 | Good catalog coverage |
| Coverage | High | Can recommend any item with features |
| Novelty | Moderate | Limited by feature similarity |

## Collaborative Filtering Baseline

### Definition

Use historical user-item interactions to find similar users or items, then recommend based on collaborative signals.

### Standard CF Baselines

| Method | Description | Complexity |
|--------|-------------|-----------|
| **User-based KNN** | Find similar users, recommend their items | O(n²) |
| **Item-based KNN** | Find similar items to those user interacted with | O(m²) |
| **Matrix factorization (SVD)** | Low-rank decomposition of user-item matrix | O(nmk) |
| **ALS (Alternating Least Squares)** | Scalable matrix factorization | O(nmk) |

### When CF Baseline Is Competitive

- **Dense interaction data**: Many users, many interactions
- **Homogeneous user base**: Users share common interests
- **Established platforms**: Enough interaction history for reliable similarity computation
- **Mainstream content**: Popular items benefit from collaborative signal

### CF Baseline Performance

| Metric | User-KNN | Item-KNN | SVD | ALS |
|--------|---------|---------|-----|-----|
| Precision@10 | 0.05–0.12 | 0.06–0.13 | 0.07–0.15 | 0.07–0.15 |
| NDCG@10 | 0.05–0.10 | 0.06–0.12 | 0.07–0.13 | 0.07–0.13 |
| Coverage | Moderate | Moderate | Low–Moderate | Low–Moderate |
| Scalability | Poor | Moderate | Good | Excellent |

## Comparing New Model Against Baselines

### Experimental Protocol

```
1. Define baselines (at minimum: popularity, random, one CF method)
2. Implement all baselines with the same data split
3. Tune each baseline's hyperparameters on validation data
4. Evaluate all methods on the same test set using the same metrics
5. Report results with confidence intervals
6. Perform statistical significance tests
```

### Minimum Baseline Set

| Required Baseline | Purpose |
|-------------------|---------|
| **Random** | Theoretical lower bound |
| **Popularity** | Simple but often competitive baseline |
| **Best simple CF** | Item-KNN or ALS (well-understood reference) |
| **Previous production model** | The real-world comparison that matters |

### Improvement Thresholds

| Metric | Minimum Meaningful Improvement |
|--------|-------------------------------|
| NDCG@10 | > 1–2% relative |
| Precision@10 | > 2–3% relative |
| Recall@100 | > 3–5% relative |
| Click-through rate | > 1–2% relative |
| Conversion rate | > 0.5–1% relative |

Improvements below these thresholds may not be worth the complexity cost.

### Ablation as Baseline Comparison

When introducing a new model with multiple components:

| Comparison | What It Tests |
|-----------|--------------|
| Full model vs. CF baseline | Overall improvement |
| Full model vs. Full model - component X | Contribution of component X |
| Full model vs. Full model - component Y | Contribution of component Y |
| Full model vs. Full model - both X and Y | Joint contribution |

## Statistical Significance of Improvements

### Required Analyses

1. **Point estimates**: Mean metric value for each method
2. **Confidence intervals**: 95% CI for each metric
3. **Significance tests**: Paired t-test or Wilcoxon signed-rank test
4. **Effect size**: Cohen's d to measure practical significance
5. **Multiple comparison correction**: Bonferroni or Holm when comparing multiple methods

### Common Mistakes

1. **Reporting only the best metric**: Report ALL metrics, not just the one where your model wins
2. **Ignoring computational cost**: A 1% improvement with 10× more compute may not be worthwhile
3. **Cherry-picking datasets**: Test on multiple datasets to ensure generalizability
4. **Overfitting to the test set**: Use held-out test sets only for final evaluation
5. **Ignoring variance**: High variance across users may mask the true improvement

### Result Reporting Template

```
Method          | NDCG@10     | Precision@10 | Recall@100   | Coverage
----------------|-------------|--------------|--------------|----------
Random          | 0.021±0.002 | 0.008±0.001  | 0.052±0.005  | 0.95
Popularity      | 0.064±0.003 | 0.032±0.002  | 0.118±0.008  | 0.02
Item-KNN        | 0.098±0.004 | 0.051±0.003  | 0.143±0.010  | 0.35
ALS             | 0.112±0.004 | 0.058±0.003  | 0.156±0.011  | 0.42
Our Model       | 0.128±0.004 | 0.067±0.003  | 0.171±0.011  | 0.48
```

With notes on statistical significance (p-values) and effect sizes.
