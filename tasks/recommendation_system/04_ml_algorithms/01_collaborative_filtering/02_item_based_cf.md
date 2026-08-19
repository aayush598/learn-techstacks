# Item-Based Collaborative Filtering

## Overview

Item-based collaborative filtering (Item-based CF) generates recommendations by computing similarity between items based on user interaction patterns. The core insight: "users who interacted with item A also interacted with item B" implies items A and B are similar. Unlike user-based CF, item-based CF is more stable (items change less frequently than users) and more scalable (item catalog is typically smaller than the user base).

Amazon pioneered item-to-item collaborative filtering in the late 1990s, and it remains one of the most widely deployed recommendation algorithms due to its simplicity, interpretability, and strong performance.

---

## Item Similarity Computation

### Similarity Metrics

| Metric | Formula Characteristics | Best For |
|---|---|---|
| **Cosine similarity** | Angle between item vectors, ignores magnitude | Binary and count data |
| **Pearson correlation** | Centroid-adjusted cosine, handles rating bias | Explicit ratings |
| **Jaccard similarity** | Intersection over union of user sets | Binary implicit feedback |
| **Adjusted cosine** | Cosine with user-mean centering | Mixed user rating scales |
| **Dice coefficient** | 2×intersection / (|A| + |B|) | Similar to Jaccard, different weighting |

### Cosine Similarity

Cosine similarity measures the angle between two item vectors in user space. For items i and j with user interaction vectors v_i and v_j:

**sim(i,j) = (v_i · v_j) / (||v_i|| × ||v_j||)**

- Range: [-1, 1] for centered data, [0, 1] for non-negative data.
- Interpretation: 0 means no overlap in user interactions, 1 means identical interaction patterns.
- Advantage: Insensitive to interaction volume differences. An item with 100 clicks and an item with 10 clicks can be highly similar if the same users clicked both.

### Pearson Correlation

Pearson correlation adjusts for user rating bias by centering ratings around each user's mean:

**sim(i,j) = Σ(r_ui - r̄_u)(r_uj - r̄_u) / √(Σ(r_ui - r̄_u)² × Σ(r_uj - r̄_u)²)**

- Handles the tendency of some users to rate higher or lower than average.
- More appropriate for explicit ratings (1–5 stars) than implicit feedback.
- Can produce unexpected results when items have very few co-rated users.

### Jaccard Similarity

Jaccard similarity measures the overlap between the sets of users who interacted with each item:

**sim(i,j) = |U_i ∩ U_j| / |U_i ∪ U_j|**

- Range: [0, 1].
- Ignores interaction intensity—only considers whether a user interacted or not.
- Well-suited for binary implicit feedback (clicks, views, purchases).
- Fast to compute for sparse interaction matrices.

### Computing Similarity at Scale

| Approach | Complexity | Scale | Accuracy |
|---|---|---|---|
| **Brute force** | O(n² × m) | Small catalogs (< 100K items) | Exact |
| **Inverted index** | O(m × k²) where k = avg co-occurrences | Medium catalogs | Exact |
| **LSH (Locality-Sensitive Hashing)** | O(n × log n) | Large catalogs | Approximate |
| **Random projection** | O(n × d) where d = projection dim | Very large catalogs | Approximate |
| **Spark/MapReduce** | Parallel O(n² / p) | Distributed | Exact |

---

## Pre-Computation Strategies

### Offline Pre-Computation

The most common approach: compute the full item-item similarity matrix offline and store it for online serving.

**Advantages:**
- Online serving is a simple lookup—no computation at request time.
- Similarity matrix can be filtered, cached, and indexed for fast retrieval.
- Full access to the entire interaction history for similarity computation.

**Disadvantages:**
- Similarity matrix is stale until the next computation.
- Storage cost is O(n²) for n items (mitigated by sparsity—store only top-K similar items).
- Computation time grows quadratically with catalog size.

### Incremental Update

Rather than recomputing the full similarity matrix, update similarities incrementally as new interactions arrive:

- **Additive update**: When a new interaction (user u, item i) arrives, update similarities involving item i and all items in user u's history.
- **Decay-based**: Apply time decay to older interactions, causing similarities to naturally evolve.
- **Periodic recompute**: Combine incremental updates with periodic full recomputation to prevent drift.

### Top-K Similarity Storage

Store only the top-K most similar items per item:

| K Value | Storage per Item | Total Storage (100K items) | Quality |
|---|---|---|---|
| 10 | 10 pairs | 1M pairs | Lower coverage |
| 50 | 50 pairs | 5M pairs | Good balance |
| 100 | 100 pairs | 10M pairs | High quality |
| 500 | 500 pairs | 50M pairs | Diminishing returns |

---

## Amazon's Item-to-Item Algorithm

### Original Algorithm

Amazon's item-to-item CF (published by Linden, Smith, and Gregorka in 2003) computes similarity between items based on co-purchase patterns:

1. **For each item**: Find the K most similar items based on co-purchase frequency.
2. **At query time**: For each item in the user's purchase history, retrieve its top-K similar items.
3. **Score and rank**: Aggregate similar items across the user's history, weighted by similarity and recency.

### Key Design Decisions

- **Co-purchase similarity**: Items are similar if they appear in the same orders, not just browsed together. This is a stronger signal of relatedness.
- **Asymmetric similarity**: The similarity from item A to item B may differ from B to A. Amazon uses asymmetric similarity for more accurate recommendations.
- **Real-time generation**: Recommendations are computed at request time by combining pre-computed similarities with the user's real-time history.
- **Personalization through history**: The same item produces different recommendations for different users based on their unique purchase history.

### Scalability at Amazon

- **Pre-computed similarity matrix**: Stored in a distributed key-value store (Dynamo).
- **Partitioned by item**: Each item's top-K similar items stored on a single node.
- **Cache-friendly**: Item similarity lookups are point queries with predictable access patterns.
- **Serves millions of requests per second**: Pre-computation eliminates per-request computation.

---

## Online Serving

### Serving Architecture

| Component | Responsibility |
|---|---|
| **User history store** | Retrieve user's recent interactions |
| **Similarity store** | Retrieve pre-computed similar items |
| **Scoring engine** | Score candidate items using similarities |
| **Ranking/filtering** | Apply business rules, deduplication, diversity |
| **Response formatter** | Format recommendations for the client |

### Scoring Methods

**Simple aggregation**: For each item in the user's history, add the similarity scores of similar items. Items appearing in multiple similarity lists receive higher scores.

**Weighted by recency**: Weight similarity scores by the recency of the user's interaction with the source item. Recent interactions contribute more to the score.

**Weighted by strength**: Weight by the strength of the user's interaction (views < clicks < purchases). Stronger interactions contribute more.

### Online Complexity

- **Per request**: O(|H| × K) where |H| is the user's history size and K is the top-K similar items.
- **Typical values**: |H| = 50 (last 50 interactions), K = 100 → 5,000 similarity lookups per request.
- **Latency**: Sub-millisecond with proper indexing and caching (Redis, Memcached).

---

## Scalability Considerations

### Scaling Item-Based CF

| Challenge | Solution |
|---|---|
| Large item catalog (millions) | LSH for approximate similarity, partitioned computation |
| High interaction volume | Distributed computation (Spark), incremental updates |
| Similarity matrix storage | Sparse storage (top-K only), distributed key-value store |
| Cold start for new items | Content-based similarity fallback, popularity-based bootstrapping |
| Real-time serving latency | Pre-computation, caching, approximate nearest neighbors |

### Parallelization

Item similarity computation is embarrassingly parallel—each item's similarities can be computed independently:

- **Spark**: Distribute items across partitions, compute similarities per partition, merge results.
- **MapReduce**: Map phase generates co-occurrence pairs, reduce phase computes similarity.
- **GPU acceleration**: Batch similarity computation for dense item vectors on GPUs.

### Approximate Methods for Large Catalogs

When the item catalog is too large for exact computation:

- **LSH**: Hash similar items into the same buckets with high probability. O(n) expected time.
- **MinHash**: Approximate Jaccard similarity using min-hash signatures.
- **Random projection**: Project item vectors to lower dimensions and compute similarity in the reduced space.
- **ANN (Approximate Nearest Neighbors)**: Use libraries like FAISS, Annoy, or ScaNN for fast approximate similarity search.
