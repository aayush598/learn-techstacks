# Metadata-Based Recommendations

## Overview

Metadata-based recommendations leverage structured and unstructured attributes associated with items and users to generate recommendations without requiring interaction history. This approach is fundamental for cold-start scenarios, serves as a strong baseline for all recommendation tasks, and provides interpretable, controllable recommendations that can be aligned with business objectives.

## Metadata Types

### Categorical Metadata

Categorical features take on discrete, unordered values from a finite set.

| Category | Examples | Cardinality |
|----------|----------|-------------|
| Product category | Electronics, Clothing, Home | Low (10-100) |
| Genre | Action, Drama, Comedy | Low-Medium (10-50) |
| Brand | Nike, Samsung, Apple | Medium (100-10K) |
| User location | Country, City | Medium (100-50K) |
| Item tags | User-generated labels | High (10K-1M) |
| Product ID | SKU identifiers | Very High (100K-100M) |

### Numerical Metadata

Numerical features represent quantitative measurements.

- **Continuous**: Price, rating, temperature, duration
- **Discrete**: Number of reviews, word count, page count
- **Ordinal**: Star rating (1-5), size (S/M/L/XL), priority level

### Text Metadata

Unstructured text fields that require NLP processing.

- Product descriptions and titles
- User reviews and comments
- Article body text
- Technical specifications
- Search queries

### Temporal Metadata

Time-based features that capture recency and trends.

- Item publication/creation date
- Last interaction timestamp
- Seasonality indicators (month, day of week)
- Time since last update
- Trending score (velocity of engagement)

### Hierarchical Metadata

Tree-structured categorical data with parent-child relationships.

- Category taxonomy: Electronics → Mobile → Smartphone → Android
- Organizational structure: Company → Department → Team
- Geographic hierarchy: Country → State → City
- Knowledge graphs: Entity → Concept → Domain

## Categorical Feature Encoding

### One-Hot Encoding

Maps each category to a binary vector where only the matching category is set to 1.

- **Advantages**: Simple, no information loss, works with linear models
- **Disadvantages**: Sparse vectors for high cardinality, no similarity between categories
- **When to use**: Low cardinality features (< 100 categories), linear models

For a feature with K categories, one-hot encoding produces K-dimensional sparse vectors. With 10,000 brands, this creates 10,000-dimensional vectors with only one non-zero entry — extremely inefficient.

### Multi-Hot Encoding

Extends one-hot to features that can have multiple values simultaneously (e.g., product tags).

```
Product tags: ["wireless", "bluetooth", "noise-cancelling"]
Encoding: [0, 0, 1, 0, 1, 0, 1, 0, 0] (3 out of 9 possible tags)
```

### Target Encoding

Replaces each category with the mean of the target variable for that category.

- **Advantages**: Compact representation (1-dimensional), captures predictive signal
- **Disadvantages**: Risk of data leakage, sensitive to rare categories
- **Mitigation**: Use leave-one-out encoding, add noise, or use Bayesian target encoding

**Bayesian target encoding formula**:
```
encoded_value(category) = (count * category_mean + prior * global_mean) / (count + prior)
```

Where `prior` is a smoothing parameter (typically global_mean or a tuned hyperparameter).

### Entity Embeddings

Learn dense, low-dimensional representations for categorical variables through a neural network.

- **Advantages**: Captures non-linear relationships, similarity between categories, compact
- **Disadvantages**: Requires neural network training, less interpretable
- **Dimensions**: Typically 8-64 dimensions per feature

**When to use entity embeddings**:
- High cardinality features where one-hot is impractical
- Categories with inherent similarity structure
- Deep learning-based recommendation models

### Feature Hashing (Hashing Trick)

Maps categories to a fixed-size vector using a hash function, regardless of cardinality.

- **Advantages**: Fixed memory footprint, handles unseen categories, no encoding step
- **Disadvantages**: Hash collisions, no category-specific optimization
- **Typical size**: 2^16 to 2^20 buckets

## Numerical Feature Processing

### Normalization

Standardize numerical features to comparable scales.

| Method | Formula | Range | When to Use |
|--------|---------|-------|-------------|
| Min-Max | (x - min) / (max - min) | [0, 1] | Bounded features, neural networks |
| Z-Score | (x - mean) / std | ~[-3, 3] | Gaussian-distributed features |
| Robust | (x - median) / IQR | Varies | Features with outliers |
| Log | log(1 + x) | [0, ∞) | Power-law distributed features |
| Quantile | Rank transform | [0, 1] | Non-linear relationships |

### Feature Binning

Convert continuous features into discrete bins for tree-based models or interpretable recommendations.

- **Equal-width bins**: Divide range into K equal intervals
- **Equal-frequency bins**: Each bin contains approximately the same number of items
- **Custom bins**: Domain-driven boundaries (price ranges, age groups)
- **Optimal bins**: Use decision tree splits to find optimal boundaries

### Numerical Feature Transformations

- **Power transformations**: Box-Cox, Yeo-Johnson to reduce skewness
- **Polynomial features**: x², x³, interaction terms for capturing non-linear relationships
- **Binning + encoding**: Discretize then one-hot encode for linear models
- **Log-transform**: Essential for power-law distributions (price, popularity)

### Practical Considerations

- Always handle zero and negative values before log transformations
- Impute missing numerical values with median (robust to outliers) or model-based imputation
- Consider clipping extreme values (e.g., 99th percentile) to prevent dominance
- Standardize features before distance-based similarity computations

## Metadata Similarity Computation

### Jaccard Similarity

Measures overlap between two sets, ideal for multi-valued categorical features.

```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

- **Range**: [0, 1] where 1 means identical sets
- **Best for**: Tags, categories, multi-label features
- **Limitation**: Does not consider element importance or frequency

### Cosine Similarity

Measures the angle between two feature vectors, ignoring magnitude.

```
cosine(A, B) = (A · B) / (||A|| * ||B||)
```

- **Best for**: High-dimensional sparse features (TF-IDF, one-hot)
- **Advantage**: Handles vectors of different lengths naturally
- **Limitation**: Only captures orientation, not magnitude

### Weighted Similarity

Combine multiple similarity signals with learned or tuned weights.

```
similarity = w1 * jaccard_categories + w2 * cosine_text + w3 * price_similarity + w4 * brand_match
```

**Weight learning approaches**:
- Grid search on held-out validation set
- Learn weights via linear regression on engagement labels
- Use attention mechanisms in neural models to learn dynamic weights

### Similarity Metrics Comparison

| Metric | Best For | Scale | Handles Sparsity | Interpretability |
|--------|----------|-------|-------------------|------------------|
| Jaccard | Set overlap | [0, 1] | Yes | High |
| Cosine | Vector space | [-1, 1] | Yes | Medium |
| Euclidean | Dense features | [0, ∞) | No | Medium |
| Pearson | Correlated features | [-1, 1] | No | Medium |
| Dice | Overweighting overlap | [0, 1] | Yes | High |

## Cross-Metadata Features

Cross-features capture interactions between metadata fields that individual features miss.

### Feature Cross Examples

| Feature Pair | Cross-Feature | Insight |
|-------------|---------------|---------|
| Category × Price | "Electronics > $100" | Premium electronics segment |
| Brand × Rating | "Nike ≥ 4.5 stars" | High-rated Nike products |
| Day × Hour | "Weekday evening" | Time-based usage patterns |
| User_age × Category | "Young adult + Gaming" | Demographic preferences |

### Automated Feature Crossing

- **Polynomial features**: Automatic 2-way and 3-way interactions
- **Factorization machines**: Learn feature interactions implicitly
- **Deep networks**: Neural layers learn complex feature interactions
- **FM-based encoding**: Use FM embeddings as cross-features for downstream models

## Metadata Quality Issues

### Missing Metadata

Common in production systems where metadata comes from multiple sources.

**Impact**: Incomplete similarity computation, biased recommendations, model degradation.

**Strategies**:
- **Default values**: Use mode for categorical, median for numerical
- **Model-based imputation**: KNN imputation, matrix factorization
- **Multi-task learning**: Predict missing metadata as auxiliary task
- **Partial similarity**: Compute similarity only on available features, weight by completeness
- **Explicit handling**: Add binary "is_missing" indicators as features

### Inconsistent Metadata

Data from multiple sources often has conflicting values for the same item.

**Common issues**:
- Category mismatch (same product in different categories across sources)
- Duplicate items with slightly different metadata
- Encoding inconsistencies (UTF-8 vs ASCII, case sensitivity)
- Unit inconsistencies (USD vs EUR, kg vs lbs)

**Resolution strategies**:
- Canonical data model with source priority rules
- Entity resolution / deduplication pipeline
- Automated consistency checks in ETL
- Human review queue for high-confidence conflicts

### Stale Metadata

Metadata that becomes outdated over time, reducing recommendation quality.

**Examples**:
- Price changes not reflected in recommendation features
- Outdated category assignments
- Discontinued products still in catalog
- Changed availability status

**Mitigation**:
- Freshness signals in ranking models
- Automated staleness detection (time since last update)
- Periodic re-indexing of metadata
- Real-time metadata streaming for high-value fields

## Metadata Enrichment Strategies

### Internal Enrichment

Leverage existing data within the organization to augment sparse metadata.

- **User-generated content**: Reviews, ratings, tags → extract features
- **Behavioral signals**: Click patterns, purchase history → infer preferences
- **Cross-referencing**: Match items across databases to fill gaps
- **Association mining**: Discover item relationships from co-purchase patterns

### External Enrichment

Supplement internal metadata with external data sources.

- **Knowledge graphs**: Wikidata, Google Knowledge Graph for entity linking
- **Taxonomies**: Industry-standard category systems (UNSPSC, GPC)
- **Third-party APIs**: Product databases, review aggregators
- **Web scraping**: Extract structured data from manufacturer sites

### Enrichment Pipeline Architecture

```
Raw Metadata → Quality Check → Gap Detection → Source Selection → 
Enrichment → Validation → Update → Re-indexing
```

**Key principles**:
- Enrichment should be idempotent (safe to re-run)
- Track data provenance (which source provided which field)
- Version metadata changes for rollback capability
- Monitor enrichment coverage and quality metrics

## Hierarchical Metadata

### Category Trees

Most product catalogs have multi-level category hierarchies:

```
Electronics
├── Mobile Phones
│   ├── Smartphones
│   │   ├── Android
│   │   └── iOS
│   └── Feature Phones
├── Laptops
│   ├── Gaming
│   ├── Ultrabooks
│   └── Business
└── Accessories
    ├── Cases
    └── Chargers
```

### Taxonomy-Aware Recommendations

Hierarchical structure enables multi-level similarity:

1. **Exact match**: Same leaf category (strongest signal)
2. **Sibling match**: Same parent category (moderate signal)
3. **Ancestor match**: Share common ancestor (weaker but broader)
4. **Cross-branch match**: Different branches but same root (weakest)

### Hierarchical Similarity Computation

```
hier_sim(A, B) = 2^(-depth(LCA(A, B)))
```

Where LCA is the Lowest Common Ancestor in the taxonomy tree. Items sharing a more specific ancestor (lower LCA depth) are more similar.

### Hierarchy-Aware Embeddings

Encode the tree structure into embedding space:

- **Node2Vec on category graph**: Random walks capture tree structure
- **Path embeddings**: Concatenate parent category embeddings
- **Tree-LSTM**: Recursive neural networks encode tree structure
- **Taxonomic attention**: Attention mechanism over ancestors

### Practical Benefits

- **Cold-start handling**: New items placed in taxonomy immediately get relevant recommendations
- **Explainability**: "Recommended because you viewed items in [Category X]"
- **Navigation**: Category-based browsing and filtering
- **Business rules**: Apply category-level constraints (exclude categories, boost margins)
- **Aggregation**: Compute category-level statistics for normalization

## Summary

Metadata-based recommendations form the backbone of production recommendation systems. They provide the cold-start solution, enable interpretable recommendations, and serve as essential features for complex ranking models. The key challenges are metadata quality (missing, inconsistent, stale data) and encoding high-cardinality categorical features effectively. Production systems should invest in metadata infrastructure — quality pipelines, enrichment processes, and hierarchical taxonomies — as these directly impact recommendation quality across all algorithmic approaches.
