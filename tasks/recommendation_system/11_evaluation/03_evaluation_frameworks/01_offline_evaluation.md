# Offline Evaluation Frameworks

## Overview

Offline evaluation is the first line of defense in assessing recommendation quality before exposing changes to real users. A well-designed offline evaluation framework provides rapid feedback during model development, reduces the number of costly online experiments, and catches regressions before they reach production. However, offline metrics correlate imperfectly with online metrics, making the design of evaluation protocols critical.

## Cross-Validation for Recommendations

### Standard K-Fold Cross-Validation

- Split the interaction matrix into K folds.
- Train on K-1 folds, evaluate on the held-out fold.
- Repeat for all folds and average results.
- **Problem for recommendations**: Ignores temporal ordering of interactions, causing data leakage.

### Time-Series Cross-Validation (Forward Chaining)

- Train on all interactions before time t, evaluate on interactions in time window [t, t+Δ].
- Progressively expand the training window.
- Respects temporal causality — the model never sees future interactions.
- Most realistic offline evaluation protocol for production systems.

**Protocol**:

```
Fold 1: Train [t₀, t₁], Evaluate [t₁, t₂]
Fold 2: Train [t₀, t₂], Evaluate [t₂, t₃]
Fold 3: Train [t₀, t₃], Evaluate [t₃, t₄]
...
```

### Leave-One-Out Cross-Validation

- For each user, hold out the last interaction as the test item.
- Train on all other interactions for that user.
- Evaluate whether the model ranks the held-out item highly.
- Fast to compute but only evaluates single-item prediction quality.
- Common in collaborative filtering literature.

### User-Based vs Interaction-Based Splitting

| Splitting Strategy | Pros | Cons |
|-------------------|------|------|
| User-based (leave users out) | Tests generalization to new users | Small test set if few users |
| Interaction-based (leave interactions out) | Large test set, realistic | May not test cold-start well |
| Temporal (time-based split) | Most realistic, no leakage | Requires timestamps |
| Negative sampling | Fast, efficient | Biased evaluation |

## Temporal Splitting

### Why Temporal Splitting Matters

- Recommendation data is inherently temporal — users' preferences evolve over time.
- Standard random splitting causes data leakage (training on future data to predict the past).
- Temporal splitting simulates the real-world scenario of predicting future behavior from past data.

### Temporal Splitting Strategies

**Simple Temporal Split**

- Choose a cutoff timestamp.
- All interactions before cutoff → training set.
- All interactions after cutoff → test set.
- Simple but may have varying training set sizes across users.

**Sliding Window**

- Use a fixed-size training window (e.g., last 90 days).
- Evaluate on interactions in the next time period (e.g., next 7 days).
- Move the window forward and repeat.
- Better captures recency effects and changing user preferences.

**Expanding Window**

- Start with a small training window.
- Progressively expand the training window.
- Evaluate on the next time period after each expansion.
- Shows how model performance improves with more data.

### Temporal Splitting Best Practices

- Always include a gap between training and test periods (e.g., 1 day) to avoid temporal leakage.
- Ensure the test period is long enough to capture weekly patterns (at least 7 days).
- Evaluate across multiple test periods for robustness.
- Report performance as a function of training data recency.

## Leave-One-Out Evaluation

### Standard Leave-One-Out Protocol

1. For each user, identify their last interaction.
2. Remove this interaction from the training data.
3. Train the model on the remaining data.
4. Evaluate whether the model ranks the held-out item in the top-K.

### Evaluation Metrics for Leave-One-Out

- **Hit Rate@K**: Fraction of users for whom the held-out item appears in top-K.
- **MRR (Mean Reciprocal Rank)**: Average reciprocal rank of the held-out item.
- **NDCG@K**: Position-aware metric for the held-out item.

### Leave-One-Out Limitations

- Only evaluates single-item prediction, not list quality.
- Assumes the last interaction is the most relevant (may not always be true).
- Computationally expensive: requires retraining or incremental updates for each user.
- Does not evaluate multi-item recommendation diversity.

## Beyond Accuracy: Beyond-Accuracy Metrics

### Coverage Metrics

**Catalog Coverage**

```
Catalog Coverage = |{items recommended to any user}| / |{total items in catalog}|
```

- Measures what fraction of the item catalog is ever recommended.
- High coverage means the system explores the full catalog.
- Low coverage indicates a "rich get richer" problem.

**User Coverage**

```
User Coverage = |{users who receive recommendations}| / |{total users}|
```

- Measures what fraction of users receive meaningful recommendations.
- Important for evaluating cold-start handling.

**Prediction Coverage**

```
Prediction Coverage = (Number of (user, item) pairs predicted) / (Total possible pairs)
```

- Measures the completeness of the recommendation matrix.
- Full coverage is impractical for large catalogs; focus on relevant subsets.

### Diversity Metrics

**Intra-List Diversity (ILD)**

```
ILD = (1 / C(K,2)) × Σᵢ<ⱼ distance(item_i, item_j)
```

- Measures how dissimilar items within a single recommendation list are.
- Higher ILD means more diverse recommendations.
- Distance can be computed using item features (genre, category, embedding distance).

**Average Category Coverage**

- Number of unique categories represented in recommendation lists.
- Higher category coverage means recommendations span more topics.
- Useful for content platforms with categorical item taxonomies.

### Novelty Metrics

**Mean Self-Information**

```
Novelty(item) = -log₂(P(item))
Novelty@K = (1/K) × Σᵢ₌₁ᴷ -log₂(P(item_i))
```

- Measures how "surprising" each recommended item is to the user.
- Items that are rarely consumed globally have higher novelty.
- Balances between relevance and serendipity.

**Item Popularity Bias**

```
Avg Popularity = (1/K) × Σᵢ₌₁^K popularity(item_i)
```

- Average popularity rank of recommended items.
- Lower average popularity means less popularity bias.
- Complementary to novelty metrics.

### Serendipity Metrics

**User-Serendipity**

```
Serendipity = (1/K) × Σ relevance(item_i) × unexpectedness(item_i)
```

- Measures how relevant yet unexpected recommendations are.
- Unexpectedness is defined relative to what the user would find with a baseline recommender.
- Requires a baseline recommender for comparison.

**Serendipity Components**

- **Relevance**: The item must be genuinely useful to the user.
- **Unexpectedness**: The item should not be easily predicted from the user's history.
- **Novelty**: The item should not be globally popular (optional component).

### Coverage-Diversity-Novelty Tradeoff

| Metric | High Value Meaning | Typical Tradeoff |
|--------|-------------------|-----------------|
| Accuracy (NDCG) | Relevant items ranked highly | Often conflicts with diversity |
| Diversity | Items in list are dissimilar | May reduce relevance |
| Novelty | Items are not globally popular | May reduce relevance |
| Coverage | Many catalog items recommended | May reduce per-user accuracy |
| Serendipity | Relevant but surprising | Hardest to optimize |

## Evaluation Pipeline Design

### Pipeline Architecture

```
Raw Data → Data Validation → Split Generation → Model Training → 
Prediction Generation → Metric Computation → Report Generation → 
Comparison Against Baseline → Gate Decision (pass/fail)
```

### Data Validation Step

- Verify interaction data schema (user_id, item_id, timestamp, rating/score).
- Check for data quality issues (missing values, duplicates, anomalies).
- Validate temporal ordering of interactions.
- Compute and report data statistics (user count, item count, interaction count, sparsity).

### Split Generation Step

- Generate train/validation/test splits using the specified temporal protocol.
- Ensure no data leakage between splits.
- Save split metadata (timestamps, sizes, random seeds) for reproducibility.
- Validate splits by checking that no test interaction appears in training data.

### Prediction Generation Step

- Load the trained model and generate predictions for all test users.
- Handle cold-start users (users not in training data) appropriately.
- Generate full ranked lists, not just top-K (for metric flexibility).
- Save predictions with timestamps for reproducibility.

### Metric Computation Step

- Compute all metrics at the user level first, then aggregate.
- Compute both micro-averaged and macro-averaged values.
- Compute confidence intervals using bootstrap resampling.
- Generate per-segment metrics (user activity level, item popularity, etc.).

### Report Generation Step

- Produce a standardized report with all metrics and their confidence intervals.
- Compare against the baseline model and previous production model.
- Highlight statistically significant improvements and regressions.
- Generate visualizations (metric distributions, segment-level breakdowns).

## Offline-to-Online Correlation

### Correlation Gap

- Offline metrics correlate imperfectly with online metrics.
- A model that improves NDCG@10 may not improve CTR in production.
- The correlation gap arises from: position bias, exposure bias, and user adaptation.

### Improving Correlation

- Use temporal splitting to simulate production conditions more realistically.
- Evaluate at the same K used in production.
- Include coverage and diversity metrics alongside accuracy metrics.
- Use propensity-weighted metrics to correct for position and exposure bias.
- Validate offline-to-online correlation empirically by tracking historical model changes.

### Offline Evaluation Gates

- Set minimum thresholds for offline metrics before allowing online experiments.
- Example gate: NDCG@10 must improve by ≥ 2% with 95% confidence to proceed to A/B test.
- Include diversity/coverage minimums to prevent degenerate solutions.
- Combine multiple offline metrics into a composite score for gate decisions.

### Correlation Tracking

- Maintain a database of historical model changes with both offline and online metric deltas.
- Compute correlation coefficients between offline and online metrics.
- Use this data to calibrate offline evaluation thresholds.
- Regularly review and update correlation models as the system evolves.

## Evaluation Framework Comparison

| Framework | Pros | Cons | Best For |
|-----------|------|------|----------|
| Standard cross-validation | Simple, fast | Temporal leakage | Non-temporal data |
| Temporal splitting | Realistic, no leakage | Slower, complex setup | Production systems |
| Leave-one-out | Precise per-item eval | Only tests single item | Research baselines |
| Full online A/B test | Gold standard truth | Expensive, slow | Final validation |

## Best Practices

- Use temporal splitting as the default evaluation protocol for production systems.
- Report multiple metrics at multiple K values for comprehensive evaluation.
- Always compare against a meaningful baseline (previous model, non-personalized, random).
- Include beyond-accuracy metrics (coverage, diversity, novelty) in every evaluation.
- Validate offline-to-online correlation regularly with historical data.
- Automate the evaluation pipeline to ensure consistency and reproducibility.
- Document all evaluation choices (splitting protocol, relevance definitions, K values).
