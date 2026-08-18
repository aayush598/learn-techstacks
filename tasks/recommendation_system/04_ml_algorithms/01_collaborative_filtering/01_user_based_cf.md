# Collaborative Filtering for Recommendation Systems

## 1. User-Based Collaborative Filtering

### 1.1 Core Idea
"Users who agreed in the past will agree in the future." Find users similar to the target user and recommend items they liked.

### 1.2 Algorithm Steps
1. **Build User-Item Interaction Matrix**: Rows = users, columns = items, values = ratings/interactions
2. **Compute User Similarity**: Cosine similarity, Pearson correlation, or Jaccard similarity between user vectors
3. **Find K-Nearest Neighbors**: Select top-K most similar users
4. **Generate Predictions**: Weighted average of similar users' ratings for unrated items
5. **Rank and Recommend**: Sort predicted ratings and return top-N

### 1.3 Similarity Metrics
- **Cosine Similarity**: Measures angle between user vectors; handles different rating scales
- **Pearson Correlation**: Measures linear correlation; handles mean-centering
- **Jaccard Similarity**: Intersection over union of interaction sets; good for implicit feedback
- **Adjusted Cosine**: Subtracts item mean to handle item popularity bias

### 1.4 Strengths and Weaknesses
**Strengths**:
- Intuitive and easy to understand
- No domain knowledge needed (works with any interaction data)
- Can discover unexpected recommendations (serendipity)
- Works well when user-item matrix is dense

**Weaknesses**:
- **Scalability**: O(n²) similarity computation for n users
- **Sparsity**: Performance degrades with sparse interaction matrices
- **Cold Start**: Cannot recommend for new users with no history
- **Popularity Bias**: Tends to recommend popular items

---

## 2. Item-Based Collaborative Filtering

### 2.1 Core Idea
"Items that are similar tend to be rated similarly by the same users." Find items similar to what the user liked and recommend those.

### 2.2 Algorithm Steps
1. **Build User-Item Matrix**: Same as user-based CF
2. **Compute Item Similarity**: Cosine similarity between item vectors (column vectors)
3. **For Each Target Item**: Find K most similar items
4. **Predict Rating**: Weighted combination of similar items' ratings by the user
5. **Rank and Recommend**: Sort predictions and return top-N

### 2.3 Why Item-Based Over User-Based
- **More Stable**: Item similarity changes less frequently than user similarity
- **Scalable**: Item catalog typically smaller than user base
- **Interpretable**: "Because you liked X" is more intuitive than "Because users like you liked X"
- **Pre-computable**: Item similarity can be precomputed and cached

### 2.4 Amazon's Item-to-Item Algorithm
- Amazon pioneered item-based CF at scale
- Key insight: Precompute item-item similarities offline; use for online serving
- Similarity: Cosine similarity on purchase vectors
- Optimization: Only consider items with overlapping purchasers
- Scale: Handles billions of items and hundreds of millions of users

---

## 3. Matrix Factorization

### 3.1 Core Idea
Decompose the user-item interaction matrix into two lower-dimensional matrices: user factors and item factors. The dot product of user and item factors predicts the rating.

### 3.2 Mathematical Formulation
```
R ≈ P × Q^T

Where:
  R: User-Item matrix (m users × n items)
  P: User latent factor matrix (m × k)
  Q: Item latent factor matrix (n × k)
  k: Number of latent factors (typically 50-200)
```

### 3.3 SVD (Singular Value Decomposition)
- Exact factorization of the user-item matrix
- Handles missing values through regularization
- **Funk SVD**: Gradient descent optimization on observed entries only
- **Bias SVD**: Includes user and item biases
- **SVD++**: Incorporates implicit feedback signals

### 3.4 Alternating Least Squares (ALS)
- Alternates between fixing P and optimizing Q, then fixing Q and optimizing P
- Each sub-problem is a regularized least squares problem (closed-form solution)
- **Parallelizable**: Each user/item factor can be computed independently
- **Implicit Feedback**: Weighted regularized ALS for implicit feedback (Hu, Koren, Volinsky)
- **Scalable**: Distributed implementation in Apache Spark MLlib

### 3.5 Stochastic Gradient Descent (SGD)
- Randomly sample observed entries
- Update user and item factors in direction of error
- Learning rate schedule for convergence
- More flexible than ALS (supports any differentiable loss function)
- Often achieves better accuracy than ALS

### 3.6 Loss Functions
- **RMSE**: Root Mean Squared Error for rating prediction
- **BPR (Bayesian Personalized Ranking)**: Pairwise ranking loss for implicit feedback
- **WARP (Weighted Approximate-Rank Pairwise)**: Optimizes top-N ranking directly
- **Hinge Loss**: Margin-based ranking loss

---

## 4. Scalability Considerations

### 4.1 Distributed Matrix Factorization
- **Spark MLlib ALS**: Distributed ALS on Spark clusters
- **Distributed SGD**: Parameter server architecture for distributed SGD
- **Mini-batch SGD**: Process mini-batches of interactions for efficiency

### 4.2 Approximate Nearest Neighbor (ANN) Search
- **FAISS**: Facebook AI Similarity Search; GPU-accelerated ANN
- **Annoy**: Spotify's Approximate Nearest Neighbors library
- **ScaNN**: Google's best ANN library
- **HNSW**: Hierarchical Navigable Small World graphs
- **Milvus**: Open-source vector database for ANN search

### 4.3 Sparse Matrix Optimization
- Store only non-zero entries (interaction matrix is >99% sparse)
- Use sparse matrix formats (CSR, CSC) for efficient computation
- Feature hashing for high-cardinality categorical features

---

## 5. Cold Start Problem

### 5.1 User Cold Start
- **Solution**: Use content-based features until enough interactions accumulated
- **Approach**: Hybrid model that weighs content features more for new users
- **Onboarding**: Collect explicit preferences during registration
- **Transfer Learning**: Use embeddings from similar users

### 5.2 Item Cold Start
- **Solution**: Use item metadata and content features
- **Approach**: Content-based model for new items; switch to CF as interactions accumulate
- **Exploration**: Randomly show new items to collect initial feedback
- **Metadata Matching**: Find similar existing items and use their interaction patterns

### 5.3 System Cold Start
- **Solution**: Start with content-based or popularity-based recommendations
- **Bootstrap**: Import ratings from external sources
- **Seed Data**: Use editorial curated recommendations initially
- **Progressive Deployment**: Gradually introduce personalized recommendations as data accumulates

---

## 6. Implementation Best Practices

### 6.1 Data Preparation
- Handle implicit feedback conversion (view → low confidence positive)
- Remove bots and spam users
- Apply time decay to old interactions
- Normalize ratings by user (z-score) or item

### 6.2 Model Evaluation
- **Offline**: RMSE, MAE, Precision@K, Recall@K, NDCG@K
- **Temporal Split**: Train on past, test on future (no future leakage)
- **Positive-Only**: For implicit feedback, evaluate ranking quality
- **Cross-Validation**: K-fold for small datasets; temporal split for large

### 6.3 Production Considerations
- **Pre-computation**: Pre-compute recommendations for all users periodically
- **Incremental Updates**: Update user/item factors incrementally as new interactions arrive
- **Caching**: Cache recommendations and similarity computations
- **Fallback**: Popular items for cold-start users
