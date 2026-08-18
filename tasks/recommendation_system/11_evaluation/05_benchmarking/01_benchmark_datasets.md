# Benchmark Datasets for Recommendations

## Overview

Benchmark datasets provide standardized evaluation environments for comparing recommendation algorithms. They enable reproducible experiments, fair comparisons across methods, and rapid prototyping. However, benchmarks have significant limitations — they may not reflect production data distributions, lack critical metadata, and can create misleading impressions of algorithm performance. Understanding benchmark characteristics and limitations is essential for meaningful research and development.

## Major Benchmark Datasets

### MovieLens

**MovieLens 100K**

- Source: GroupLens Research, University of Minnesota.
- Size: 100,000 ratings from 943 users on 1,682 movies.
- Rating Scale: 1-5 stars (explicit feedback).
- Time Period: September 1997 - April 1998.
- Sparsity: 93.69% (100,000 / (943 × 1,682)).
- Use Case: Small-scale algorithm development and debugging.

**MovieLens 1M**

- Size: 1,000,209 ratings from 6,040 users on 3,952 movies.
- Additional Data: User demographics (age, gender, occupation, zip code).
- Rating Scale: 1-5 stars.
- Sparsity: 95.81%.
- Use Case: Standard academic benchmark, most widely used.

**MovieLens 10M**

- Size: 10,000,054 ratings from 71,567 users on 10,681 movies.
- Additional Data: Tags applied by users.
- Rating Scale: 0.5-5.0 stars (half-star increments).
- Sparsity: 98.69%.
- Use Case: Medium-scale evaluation, tag-based recommendations.

**MovieLens 20M**

- Size: 20,000,263 ratings from 138,493 movies from 27,278 users.
- Additional Data: Tags, genome scores (item similarity scores).
- Rating Scale: 0.5-5.0 stars.
- Sparsity: 99.49%.
- Use Case: Large-scale evaluation, tag-based and content-based methods.

**MovieLens 25M**

- Size: 25,000,095 ratings from 162,541 users on 59,047 movies.
- Additional Data: Tags, genome scores.
- Rating Scale: 0.5-5.0 stars.
- Sparsity: 99.73%.
- Use Case: Current standard large-scale benchmark.

### Amazon Reviews

**Overview**: Product reviews from Amazon.com covering multiple product categories.

**Dataset Variants**:

| Variant | Users | Items | Ratings | Category | Use Case |
|---------|-------|-------|---------|----------|----------|
| Amazon-5 (small) | ~6K | ~2K | ~50K | Electronics | Quick prototyping |
| Amazon-5 (medium) | ~82K | ~50K | ~1.7M | Electronics | Medium-scale evaluation |
| Amazon-5 (large) | ~233K | ~104K | ~4.5M | Electronics | Full-scale evaluation |
| Amazon-23 (full) | ~33M | ~10M | ~233M | All categories | Massive-scale evaluation |

**Characteristics**:

- Rating Scale: 1-5 stars (explicit feedback).
- Additional Data: Review text, helpfulness votes, timestamps, product metadata.
- Highly sparse (typical sparsity > 99.9%).
- Temporal information enables time-based evaluation protocols.
- Category-specific subsets enable domain-specific analysis.

**Evaluation Protocols**:

- Review-based: Predict the rating a user would give a product.
- Purchase prediction: Predict whether a user will purchase an item.
- Temporal split: Train on past reviews, predict future reviews.

### Netflix Prize

**Overview**: Released by Netflix in 2006 for a $1M competition to improve their recommendation algorithm by 10%.

**Characteristics**:

- Size: 100,480,507 ratings from 480,189 users on 17,770 movies.
- Rating Scale: 1-5 stars (explicit feedback).
- Time Period: November 1999 - December 2005.
- Training Set: 100,480,507 ratings.
- Probe Set: 1,408,241 ratings (for leaderboard evaluation).
- Qualifying Set: 2,817,131 ratings (for final submission).
- No movie titles provided (only anonymized IDs).

**Significance**:

- First large-scale public benchmark for collaborative filtering.
- Led to the development of matrix factorization methods (SVD, ALS).
- Established the RMSE as the standard evaluation metric for rating prediction.
- No longer actively used for new research but remains historically important.

**Limitations**:

- Only contains explicit ratings (no implicit feedback).
- Movie metadata not provided (only anonymized IDs).
- Data is quite old (1999-2005) and may not reflect modern user behavior.
- Size is now modest compared to modern datasets.

### Book-Crossing

**Source**: Cai-Nicolas Ziegler, University of Freiburg.

**Characteristics**:

- Size: 1,149,780 ratings from 278,858 users on 271,379 books.
- Rating Scale: 1-10 (explicit), 0 (implicit "not rated").
- Sparsity: 99.998%.
- Very sparse even for a recommendation dataset.
- Includes explicit and implicit rating types.

**Use Cases**:

- Book recommendation research.
- Extremely sparse data scenarios.
- Cross-domain recommendation (books + reviews).

### Yelp

**Overview**: Business reviews from the Yelp platform.

**Dataset Variants**:

| Version | Users | Businesses | Reviews | Tips | Check-ins |
|---------|-------|-----------|---------|------|-----------|
| Yelp Academic (small) | ~6K | ~5K | ~500K | ~50K | ~100K |
| Yelp Open Dataset | ~7M | ~185K | ~7M | ~1.3M | ~1.3M |

**Characteristics**:

- Rating Scale: 1-5 stars (explicit feedback).
- Additional Data: Business metadata (category, location, hours), user friends, photos.
- Multi-attribute reviews (useful for aspect-based recommendations).
- Geographic data enables location-aware recommendations.
- Active, regularly updated dataset.

**Use Cases**:

- Location-based recommendations.
- Multi-attribute recommendation (food quality, service, ambiance).
- Social network-based recommendations (friend connections).

### Goodreads

**Overview**: Book reviews and reading data from the Goodreads platform.

**Characteristics**:

- Size: ~12M ratings from ~1.5M users on ~1.5M books.
- Additional Data: Book shelves, reviews, reading status, author information.
- Rating Scale: 1-5 stars.
- Temporal data available for time-based evaluation.

**Use Cases**:

- Book recommendation with rich metadata.
- Reading list prediction.
- Social recommendation (friend-based).

### Other Notified Datasets

| Dataset | Domain | Size | Notable Feature |
|---------|--------|------|-----------------|
| Steam | Games | ~7.8M reviews | Game recommendation |
| Last.fm | Music | ~19M events | Music listening history |
| Pinterest | Visual | ~1.5B pins | Visual recommendation |
| MIND | News | ~1M impressions | News recommendation |
| Ali-CCP | E-commerce | ~84M clicks | Click-through prediction |

## Dataset Characteristics Comparison

### Scale Comparison

| Dataset | Users | Items | Interactions | Density | Rating Type |
|---------|-------|-------|-------------|---------|-------------|
| ML-100K | 943 | 1,682 | 100K | 6.3% | Explicit (1-5) |
| ML-1M | 6,040 | 3,952 | 1M | 4.2% | Explicit (1-5) |
| ML-10M | 72K | 10K | 10M | 1.3% | Explicit (0.5-5) |
| ML-25M | 163K | 59K | 25M | 0.3% | Explicit (0.5-5) |
| Amazon-5 | 233K | 104K | 4.5M | 0.02% | Explicit (1-5) |
| Netflix | 480K | 18K | 100M | 1.2% | Explicit (1-5) |
| Yelp | 7M | 185K | 7M | 0.005% | Explicit (1-5) |
| Goodreads | 1.5M | 1.5M | 12M | 0.5% | Explicit (1-5) |

### Metadata Richness

| Dataset | User Demographics | Item Metadata | Text Reviews | Temporal | Social |
|---------|------------------|---------------|-------------|----------|--------|
| MovieLens | Yes (age, gender, occupation) | Yes (genre, year) | No | Yes | No |
| Amazon | No | Yes (category, brand) | Yes | Yes | No |
| Netflix | No | No | No | Yes | No |
| Book-Crossing | No | Yes (author, year) | No | No | No |
| Yelp | Limited | Yes (category, location) | Yes | Yes | Yes |
| Goodreads | No | Yes (author, genre) | Yes | Yes | Yes |

## Evaluation Protocol Standards

### Standard Protocols

**Rating Prediction Protocol**:

- Split data into training (80%) and test (20%) sets.
- Use RMSE and MAE as evaluation metrics.
- Report results on the Netflix-style hold-out set.

**Top-K Recommendation Protocol**:

- For each user, hold out the last interaction as the test item.
- Recommend top-K items and evaluate with Recall@K, NDCG@K, Hit Rate@K.
- Typical K values: 5, 10, 20.

**Leave-One-Out Protocol**:

- Hold out the last interaction for each user.
- Train on all remaining interactions.
- Evaluate ranking quality of the held-out item.
- Common in collaborative filtering literature.

**Temporal Split Protocol**:

- Use a cutoff timestamp for train/test split.
- All interactions before cutoff → training.
- All interactions after cutoff → test.
- Most realistic for production systems.

### Evaluation Metrics by Protocol

| Protocol | Primary Metrics | Secondary Metrics | Recommended K |
|----------|----------------|-------------------|---------------|
| Rating Prediction | RMSE, MAE | MAPE, R² | N/A |
| Top-K Recommendation | NDCG@K, Recall@K | Precision@K, MRR, Hit Rate | 5, 10, 20 |
| Leave-One-Out | MRR, Hit Rate@K | NDCG@K, Precision@K | 10 |
| Temporal Split | NDCG@K, Recall@K | Coverage, Diversity, Novelty | 5, 10, 20 |

## Reproducibility Considerations

### Reproducibility Checklist

- **Random Seeds**: Fix all random seeds for train/test splitting and model initialization.
- **Data Preprocessing**: Document all preprocessing steps (filtering, normalization, splitting).
- **Evaluation Code**: Share complete evaluation code, not just results.
- **Environment**: Specify Python version, library versions, and hardware.
- **Hyperparameters**: Report all hyperparameters including those that did not improve results.
- **Multiple Runs**: Report mean and standard deviation over multiple runs (minimum 5).

### Common Reproducibility Issues

- Different train/test splits produce significantly different results.
- Hyperparameter tuning on the test set inflates reported performance.
- Negative sampling strategies affect ranking metrics.
- Different preprocessing pipelines (e.g., minimum interaction thresholds) change results.
- Missing handling of cold-start users/items in evaluation.

### Best Practices for Reproducible Research

- Use standard benchmark datasets with published evaluation protocols.
- Share code and configurations alongside published results.
- Report results with confidence intervals or standard deviations.
- Use well-established evaluation libraries (Cornac, RecBole, Surprise).
- Pre-register evaluation methodology before running experiments.

## Limitations of Benchmarks

### Data Limitations

- **Temporal Obsolescence**: Most benchmarks are 5-15 years old and may not reflect modern user behavior.
- **Domain Specificity**: MovieLens is movie-specific; results may not transfer to other domains.
- **Missing Metadata**: Many benchmarks lack important metadata (content features, user demographics).
- **Synthetic Filtering**: Real-world data is filtered for quality and minimum activity thresholds.
- **Implicit Feedback Gap**: Many benchmarks only contain explicit ratings, not implicit signals.

### Evaluation Limitations

- **Offline-Online Gap**: Offline metrics correlate imperfectly with online user satisfaction.
- **Simplified Scenario**: Benchmarks don't capture real-time dynamics, cold-start, or temporal evolution.
- **Missing Position Bias**: Standard evaluation doesn't account for position effects in real interfaces.
- **Static Evaluation**: Benchmarks are snapshots; they don't evaluate system evolution over time.
- **Neglect of Business Metrics**: Benchmark metrics don't capture revenue, engagement, or retention.

### Recommendation for Practitioners

- Use benchmarks for initial algorithm comparison and prototyping.
- Always validate findings on your own production data before deployment.
- Supplement benchmarks with synthetic datasets for specific scenarios (cold-start, temporal dynamics).
- Consider creating internal benchmarks from production data for realistic evaluation.
- Report results on multiple benchmarks for generalizability.
- Be skeptical of large improvements on small benchmarks; validate on larger, more realistic datasets.
