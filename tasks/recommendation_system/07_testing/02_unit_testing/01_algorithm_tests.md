# Unit Testing Recommendation Algorithms

## Overview

Unit testing recommendation algorithms validates individual algorithmic components in isolation.
Unlike integration or end-to-end tests, unit tests focus on verifying that each algorithm produces
mathematically correct outputs given known inputs. This covers collaborative filtering, content-based
filtering, matrix factorization, and hybrid approaches — with specific test cases, mocking
strategies, and numerical precision handling for each.

## Fundamental Principles

### What to Test in Algorithm Code

1. **Mathematical correctness**: The algorithm implements the intended mathematical operation
2. **Boundary conditions**: Behavior at edges of the input domain
3. **Numerical stability**: Graceful handling of zeros, infinities, NaN, and extreme values
4. **Determinism**: Same input produces same output (or output within expected variance)
5. **Performance contracts**: Algorithm completes within expected time complexity

### Test Isolation Requirements

Each unit test must exercise exactly one algorithmic component. Dependencies on external systems,
pre-trained models, or live data sources must be replaced with test doubles. The test should be
self-contained, fast (milliseconds), and reproducible.

## Test Data Management

### Synthetic Test Data Generation

Unit tests should use small, hand-crafted datasets where the expected output is analytically
determinable. For a user-item interaction matrix:

```
User-Item Matrix (3 users, 4 items):
         Item_A  Item_B  Item_C  Item_D
User_1     5.0     3.0     4.0     4.0
User_2     3.0     1.0     2.0     3.0
User_3     4.0     3.0     4.0     3.0
```

### Test Data Patterns

| Pattern             | Description                                        | When to Use                      |
|---------------------|---------------------------------------------------|----------------------------------|
| Minimal matrix      | Smallest possible input that exercises the path   | Core algorithm logic             |
| Known-answer dataset| Input where output can be computed by hand         | Mathematical correctness         |
| Edge case matrix    | Sparse, dense, single-row, single-column           | Boundary condition testing       |
| Degenerate cases    | All zeros, all ones, uniform distribution          | Numerical stability              |
| Large sparse matrix | 1000x1000 with 1% density                         | Memory and performance testing   |

### Data Versioning for Tests

Test datasets should be versioned alongside code. Use content-addressable storage (hash of data
as version key) to detect accidental modifications. Test fixtures stored in a `testdata/` directory
with checksums provide reproducibility guarantees.

## Collaborative Filtering Test Cases

### User-Based Collaborative Filtering

**Test: Cosine Similarity Computation**
- Input: Two user rating vectors with known angle
- Expected: Cosine similarity equals analytical result within tolerance
- Edge cases: Orthogonal vectors (similarity = 0), identical vectors (similarity = 1), zero vectors

**Test: Pearson Correlation Computation**
- Input: Two users with overlapping but different rating patterns
- Expected: Correlation coefficient matches hand-calculated value
- Edge cases: No overlapping items (should return 0 or neutral), single overlapping item

**Test: Neighbor Selection**
- Input: Similarity scores for all users relative to target user
- Expected: Top-K neighbors are selected correctly
- Edge cases: K larger than available users, K=0, all similarities identical

**Test: Prediction Aggregation**
- Input: Neighbors' ratings and similarity weights
- Expected: Weighted average prediction matches expected value
- Edge cases: All neighbors have same rating, one dominant neighbor, negative similarities

### Item-Based Collaborative Filtering

**Test: Item-Item Similarity Matrix**
- Input: User-item interaction matrix
- Expected: Symmetric similarity matrix with diagonal = 1
- Edge cases: Items with no co-occurring users, items rated by only one user

**Test: Item Recommendation Generation**
- Input: Target user's rated items and item similarity matrix
- Expected: Recommendations are unrated items sorted by predicted score
- Edge cases: User has rated all items, user has rated only one item

## Content-Based Filtering Test Cases

### Feature Vector Operations

**Test: TF-IDF Computation**
- Input: Document-term matrix
- Expected: TF-IDF values match formula: TF(t,d) * log(N/DF(t))
- Edge cases: Terms appearing in all documents (IDF = 0), single-document corpus

**Test: Cosine Similarity Between Item Features**
- Input: Two item feature vectors (e.g., genre, director, year)
- Expected: Similarity score within [0, 1] for non-negative features
- Edge cases: Identical items (similarity = 1), completely disjoint features (similarity = 0)

**Test: User Profile Construction**
- Input: User's interaction history with item features
- Expected: User profile is weighted average of interacted item features
- Edge cases: User with single interaction, user with uniform interaction distribution

### Content-Based Recommendation Generation

**Test: Profile-Item Matching**
- Input: User profile vector and candidate item feature vectors
- Expected: Items ranked by similarity to user profile
- Edge cases: All items equally similar, no items match profile, profile is zero vector

**Test: Feature Weighting**
- Input: Feature importance weights and item features
- Expected: Weighted features produce different rankings than unweighted
- Edge cases: All weights zero, single non-zero weight, negative weights

## Matrix Factorization Test Cases

### SVD-Based Factorization

**Test: Factorization Reconstruction**
- Input: Sparse user-item matrix
- Expected: Reconstructed dense matrix approximates original within specified error
- Verification: `||R - U * V^T||_F / ||R||_F < epsilon`

**Test: Low-Rank Approximation Quality**
- Input: Matrix with known low-rank structure
- Expected: Factorization recovers the underlying structure
- Edge cases: Full-rank matrix, rank-1 matrix, matrix with noise

**Test: Handling Missing Values**
- Input: Sparse matrix with known missing pattern
- Expected: Factorization only minimizes loss over observed entries
- Edge cases: Very sparse matrix (< 1% density), single observation per user

### ALS (Alternating Least Squares)

**Test: Convergence Behavior**
- Input: Fixed user-item matrix
- Expected: Loss decreases monotonically across iterations
- Verification: Loss at iteration N+1 <= Loss at iteration N

**Test: Regularization Effect**
- Input: Same matrix with different lambda values
- Expected: Higher regularization produces factor matrices with smaller norms
- Edge cases: Lambda = 0 (overfitting), very large lambda (underfitting)

**Test: Cold Start Handling**
- Input: New user with 1-2 interactions
- Expected: Model produces reasonable recommendations (not NaN, not all-zero)
- Edge cases: New user with zero interactions, new item with zero interactions

### SGD-Based Factorization

**Test: Learning Rate Schedule**
- Input: Fixed matrix, learning rate schedule
- Expected: Convergence to local minimum regardless of initialization
- Edge cases: Learning rate too high (divergence), too slow (no convergence in budget)

**Test: Negative Sampling**
- Input: Implicit feedback matrix with negative sampling ratio
- Expected: Sampled negatives are uniformly distributed from non-interacted items
- Verification: No sampled negative is an actual positive interaction

## Hybrid Algorithm Test Cases

**Test: Weight Combination**
- Input: Scores from collaborative and content-based models
- Expected: Hybrid score is convex combination with specified weights
- Edge cases: Weight = 1.0 for one model (pure model), weight = 0.5 (equal contribution)

**Test: Score Normalization**
- Input: Scores from models operating on different scales
- Expected: Normalized scores are in [0, 1] and preserve ranking
- Edge cases: All scores identical, single score, negative scores

**Test: Model Selection Logic**
- Input: User context with varying data availability
- Expected: System selects content-based for cold-start, collaborative for warm users
- Edge cases: Boundary between cold-start and warm, user at exact threshold

## Feature Computation Tests

### User Feature Tests

**Test: Aggregated Features**
- Input: User interaction history
- Expected: `avg_rating`, `total_purchases`, `session_count` computed correctly
- Edge cases: Empty history (should return defaults, not crash), single interaction

**Test: Temporal Features**
- Input: Timestamped user actions
- Expected: `days_since_last_active`, `recency_score` computed against current time
- Edge cases: Future timestamps, extremely old timestamps, timezone handling

**Test: Behavioral Features**
- Input: Sequence of user actions
- Expected: `browse_to_buy_ratio`, `category_affinity` scores are valid probabilities
- Edge cases: Zero total actions, actions in single category only

### Item Feature Tests

**Test: Popularity Features**
- Input: Item interaction logs
- Expected: `view_count`, `purchase_count`, `rating_mean` are monotonically correct
- Edge cases: Item with zero interactions, item with single 5-star rating

**Test: Content Features**
- Input: Item metadata
- Expected: Category encoding, text embeddings, image features are normalized
- Edge cases: Missing optional fields, extremely long text, corrupted image

## Mocking External Dependencies

### Database Mocks

Pattern: In-memory data store replacing Redis or feature store:

- Implement the same interface as the real feature store
- Accept a dictionary of pre-populated features in the constructor
- Return empty dict for unknown keys (mimics cache miss behavior)
- No network I/O, no serialization overhead

### Model Artifact Mocks

When testing inference pipelines, mock the model loading step:
- Provide a pre-serialized small model in test fixtures
- Mock the model server health check endpoint
- Simulate model version metadata responses

### External API Mocks

For tests that depend on external services (catalog API, user service):
- Record real responses as JSON fixtures
- Replay fixtures during test execution
- Verify request payloads match expected format
- Use libraries like `responses` (Python) or `msw` (JavaScript)

## Numerical Precision Testing

ML algorithms involve floating-point arithmetic. Tests must account for:

1. **Tolerance-based comparison**: Use `abs(actual - expected) < atol + rtol * abs(expected)`
2. **Relative vs. absolute tolerance**: Large values need relative tolerance; small values need absolute
3. **Accumulated error**: Longer computation chains accumulate more error
4. **Platform differences**: GPU vs. CPU results may differ at 6th+ decimal place

| Value Range        | Absolute Tolerance | Relative Tolerance |
|--------------------|--------------------|--------------------|
| 0.0 - 0.001        | 1e-7               | 1e-5               |
| 0.001 - 1.0        | 1e-5               | 1e-5               |
| 1.0 - 100.0        | 1e-3               | 1e-4               |
| 100.0 - 10000.0    | 1e-1               | 1e-4               |

## Performance Unit Tests

Some unit tests validate performance contracts, not just correctness:

- **Time complexity**: Matrix factorization on 100x100 matrix completes in < 100ms
- **Space complexity**: Feature computation for 10K users uses < 500MB memory
- **Batch vs. single**: Batch prediction for 1000 items is faster than 1000 individual predictions
- **Cache effectiveness**: Second call to same prediction is faster than first (when caching enabled)

## Test Organization and Naming

Follow a consistent naming convention:

- `test_[algorithm]_[operation]_[condition]`
- Example: `test_cosine_similarity_orthogonal_vectors`
- Example: `test_als_convergence_monotonic_decrease`
- Example: `test_content_filter_zero_vector_profile`

Group tests by algorithm family within test modules. Use `pytest.mark.parametrize` for
parameterized tests that exercise the same logic across multiple input configurations.
