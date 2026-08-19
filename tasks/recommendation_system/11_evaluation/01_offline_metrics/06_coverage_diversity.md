# Coverage and Diversity Metrics

## Overview

Coverage and diversity metrics evaluate aspects of recommendation quality that accuracy-focused metrics (precision, recall, NDCG) miss entirely. Coverage measures the breadth of items the system recommends, while diversity measures how dissimilar items within a recommendation list are from each other. Together, they capture whether a system provides varied, comprehensive recommendations rather than repeatedly surfacing the same popular items.

## Catalog Coverage

Catalog coverage measures what fraction of the total item catalog is ever recommended to any user.

### Item Coverage (Reach)

```
Item Coverage = |{items recommended to at least one user}| / |{all items}|
```

This is the most basic coverage metric. A system that recommends only the top-10 most popular items to every user has extremely low catalog coverage, even if those items are highly relevant.

### Coverage@K

To account for list length:

```
Coverage@K = |{items appearing in any user's top-K list}| / |{all items}|
```

### Gini-Style Coverage

Beyond binary coverage (recommended or not), we can measure how evenly recommendations are distributed across items:

```
Item Distribution = [count(item_1), count(item_2), ..., count(item_N)]
Gini = (1/N) * Σ (2i - N - 1) * p(i) / Σ p(i)
```

Where p(i) is the proportion of total recommendations assigned to item i, sorted in ascending order.

| Gini Value | Interpretation |
|-----------|---------------|
| 0 | Perfectly even distribution (all items recommended equally) |
| 1 | Maximum inequality (one item receives all recommendations) |

## User Coverage

User coverage measures what fraction of users receive at least one personalized recommendation.

```
User Coverage = |{users who received personalized recommendations}| / |{all active users}|
```

### Why User Coverage Matters
- Cold-start users may receive only popular-item fallbacks
- New users with no interaction history may not get personalized lists
- Low user coverage indicates the system fails to serve a significant portion of the user base

### User Coverage Segmentation
Report user coverage by segment:
- **By tenure**: New users (0–7 days) vs. established users (30+ days)
- **By activity level**: Low, medium, high engagement tiers
- **By device**: Mobile vs. desktop vs. tablet
- **By geography**: Different regions may have different catalog availability

## Long-Tail Coverage

Long-tail coverage specifically measures whether niche and less popular items are recommended.

### Defining the Long Tail
- **Head items**: Top 10–20% of items by popularity (often 80% of interactions)
- **Torso items**: Middle 30–40% of items by popularity
- **Tail items**: Bottom 40–60% of items by popularity (often <5% of interactions)

### Long-Tail Coverage Metric

```
Long-Tail Coverage = |{tail items recommended}| / |{all tail items}|
```

### Why Long-Tail Coverage Matters
- **Catalog monetization**: Many items in the catalog generate revenue; recommending only head items leaves revenue on the table
- **User satisfaction**: Power users discover niche items; low long-tail coverage frustrates them
- **Supplier fairness**: Content creators and sellers in the tail deserve exposure
- **Diversity**: Long-tail items tend to be more diverse than head items

### Coverage vs. Relevance Tradeoff
Recommending long-tail items often trades off against short-term accuracy. The key insight is that long-tail recommendations may improve user satisfaction and retention even if they lower immediate click-through rates.

## Intra-List Diversity (ILD)

Intra-List Diversity measures how dissimilar items are within a single recommendation list.

### Jaccard-Based ILD (Binary Features)

```
ILD(L) = (1 / C(|L|, 2)) * Σ Σ (1 - Jaccard(i, j))
```

Where L is the recommendation list, and Jaccard(i,j) is the Jaccard similarity between items i and j based on their binary feature vectors (e.g., genre tags, categories).

### Cosine-Based ILD (Continuous Features)

```
ILD(L) = (1 / C(|L|, 2)) * Σ Σ (1 - cos(v_i, v_j))
```

Where v_i and v_j are continuous feature vectors (e.g., embeddings) for items i and j.

### Average ILD (ILD_avg)

```
ILD_avg = (1 / |U|) * Σ ILD(L_u)
```

### ILD Properties
- **Range**: [0, 1], where 0 means all items are identical and 1 means all items are completely dissimilar
- **Symmetric**: ILD does not depend on item ordering within the list
- **Feature-dependent**: ILD values are only meaningful when computed with the same feature set

### Choosing the Similarity Function

| Feature Type | Similarity Function | Example |
|-------------|-------------------|---------|
| Binary tags | Jaccard, Overlap | Genre tags, categories |
| Continuous embeddings | Cosine distance | Item2Vec, BERT embeddings |
| Hierarchical categories | Path-based distance | Category taxonomy distance |
| Mixed features | Weighted combination | Combine tag + embedding similarity |

## Inter-List Diversity

Inter-list diversity measures how different recommendation lists are across users.

### User-Pair Diversity

```
Inter-List Diversity = (1 / C(|U|, 2)) * Σ Σ (1 - ListSimilarity(L_u, L_v))
```

### List Similarity Measures
- **Jaccard on item sets**: What fraction of items are unique to each list?
- **Cosine on score vectors**: How similar are the ranking vectors?
- **Rank correlation**: Spearman's ρ on item positions

### Why Inter-List Diversity Matters
- **User experience**: If all users receive similar lists, the system feels generic
- **Privacy**: Low inter-list diversity can reveal that the system profiles users similarly
- **Market fairness**: Different users should see different perspectives

## Shannon Entropy

Entropy measures the uncertainty or uniformity of the recommendation distribution across items.

### Definition

```
H = -Σ p(i) * log₂(p(i))
```

Where p(i) is the probability (proportion) of item i being recommended.

### Maximum Entropy

```
H_max = log₂(|I|)
```

Where |I| is the total number of items.

### Normalized Entropy

```
H_norm = H / H_max
```

| H_norm Value | Interpretation |
|-------------|---------------|
| 1.0 | Perfectly uniform recommendations (all items equally likely) |
| 0.0 | All recommendations concentrated on a single item |
| >0.8 | Good diversity |
| 0.5–0.8 | Moderate concentration |
| <0.5 | Heavy concentration (potential popularity bias) |

### Entropy vs Gini

| Aspect | Entropy | Gini |
|--------|---------|------|
| Sensitivity to extremes | More sensitive to very uneven distributions | Less sensitive |
| Range | [0, log₂(N)] | [0, 1] |
| Interpretability | Information-theoretic | Economic inequality analogy |
| Preference | When uniformity is critical | When inequality comparison is needed |

## Gini Coefficient for Popularity Bias

The Gini coefficient, borrowed from economics, measures inequality in the distribution of recommendations.

### Computation

```
Gini = (2 * Σ i * y(i)) / (N * Σ y(i)) - (N + 1) / N
```

Where y(i) is the number of times item i is recommended, sorted in ascending order, and N is the total number of items.

### Interpretation
- **Gini = 0**: All items recommended equally (no popularity bias)
- **Gini = 1**: One item receives all recommendations (maximum popularity bias)
- **Typical values**: 0.5–0.9 for most production systems

### Popularity Bias Analysis

| Bias Level | Gini Range | Impact |
|-----------|-----------|--------|
| Low | 0.3–0.5 | Good long-tail coverage, potentially lower accuracy |
| Moderate | 0.5–0.7 | Balanced tradeoff |
| High | 0.7–0.9 | Strong popularity bias, poor long-tail coverage |
| Extreme | >0.9 | Almost no diversity, only top items recommended |

## Novelty Metrics

Novelty measures how unexpected or new the recommendations are to the user.

### Self-Information (Surprise)

```
Novelty(i) = -log₂(p(i))
```

Where p(i) is the global popularity of item i. Rare items have high self-information (high novelty); popular items have low self-information.

### Average List Novelty

```
Novelty(L) = (1/|L|) * Σ (-log₂(p(i)))
```

### Long-Tail Percentage

```
LongTail% = |{tail items in list}| / |L| * 100
```

Where "tail" is defined by a popularity threshold (e.g., bottom 80% of items by interaction count).

### Popularity-Based Novelty vs. Serendipity

| Metric | What It Measures | How |
|--------|-----------------|-----|
| Self-information | Statistical rareness of items | Global item popularity |
| Serendipity | Unexpected yet relevant items | Deviation from user's expected preferences |
| Diversity | Dissimilarity within list | Pairwise item similarity |
| Novelty | Newness to the specific user | User's past interaction history |

### User-Specific Novelty

```
UserNovelty(u) = (1/|L_u|) * Σ (-log₂(p(i | u)))
```

Where p(i | u) is the probability that user u would naturally encounter item i. This requires modeling user behavior patterns.

## Coverage-Diversity-Novelty Tradeoffs

### The Triple Tradeoff
Increasing coverage, diversity, and novelty often trades off against accuracy:

| Metric | Pushing Higher... | Cost |
|--------|------------------|------|
| Coverage | Recommend more items | May recommend irrelevant items |
| Diversity | More dissimilar items in list | May sacrifice relevance for variety |
| Novelty | More obscure items | May confuse users with unfamiliar items |

### Balanced Evaluation Framework

A production recommendation system should report a dashboard of metrics:

| Category | Metrics | Target |
|----------|---------|--------|
| Accuracy | NDCG@10, MAP@10, AUC | Maximize within constraints |
| Coverage | Item coverage, long-tail coverage | >30% catalog, >10% tail |
| Diversity | ILD, normalized entropy | ILD > 0.5, entropy > 0.7 |
| Novelty | Average self-information, long-tail % | Long-tail % > 20% |
| Fairness | Gini coefficient, provider fairness | Gini < 0.7 |

### Optimization Strategies

1. **Re-ranking**: Generate accurate candidates, then re-rank for diversity/novelty (MMR, DPP)
2. **Exploration**: Epsilon-greedy or Thompson sampling to explore tail items
3. **Multi-objective optimization**: Pareto-optimal solutions balancing accuracy and coverage
4. **Constraint-based**: Guarantee minimum coverage/diversity while maximizing accuracy
