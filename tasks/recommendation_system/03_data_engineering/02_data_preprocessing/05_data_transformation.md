# Data Transformation — Recommendation System Data Preprocessing

## 1. Categorical Variable Encoding

### 1.1 One-Hot Encoding

Creates a binary column for each category in a categorical feature.

- **Example**: Color = {Red, Blue, Green} → Three columns: is_red, is_blue, is_green.
- **Properties**: Preserves no ordinal relationship between categories; increases dimensionality by the number of unique categories; produces sparse feature vectors for high-cardinality features.
- **When to Use**: Categorical features with low cardinality (< 20 unique values); when the model cannot handle ordinal encoding naturally (linear models, neural networks).
- **When NOT to Use**: High-cardinality features (product_id with millions of values, user_id, zip_code) — one-hot encoding creates millions of sparse columns, increasing memory and computation dramatically.
- **Sparse Representation**: Use scipy.sparse or TensorFlow SparseTensor to store one-hot encoded features efficiently.

### 1.2 Label (Ordinal) Encoding

Assigns a unique integer to each category.

- **Example**: Size = {S, M, L, XL} → {0, 1, 2, 3}.
- **Properties**: Preserves ordinal relationships (if the ordering is meaningful); introduces an artificial numeric relationship (2 is "twice" 0, which may not be meaningful); compact representation.
- **When to Use**: Ordinal features where the ordering is meaningful (education level, size, satisfaction rating); tree-based models that can handle ordinal relationships natively.
- **When NOT to Use**: Nominal features where no ordering exists (color, country, brand) — tree-based models will still work (they find optimal split points), but neural networks and linear models will be confused by the artificial ordering.

### 1.3 Target (Mean) Encoding

Replaces each category with the mean of the target variable for that category.

- **Example**: Product category = "Electronics" → Average purchase rate for electronics = 0.35. Category "Clothing" → Average purchase rate = 0.22.
- **Properties**: Captures the predictive power of the category; low cardinality representation (one number per category); highly prone to overfitting, especially for rare categories.
- **Regularization Strategies**:
  - **Smoothing**: Blend the category mean with the global mean: encoded_value = (n × category_mean + m × global_mean) / (n + m), where n is the category count and m is a smoothing parameter (e.g., 10–100).
  - **Leave-One-Out**: For each observation, compute the target mean excluding that observation to prevent leakage.
  - **K-Fold Target Encoding**: Compute target means using only out-of-fold data to prevent leakage.
- **When to Use**: High-cardinality categorical features in tree-based models; when you want a compact, information-rich representation.
- **When NOT to Use**: When the dataset is small (rare categories have unreliable means); without regularization (overfitting risk); in neural networks without additional regularization.

### 1.4 Hash Encoding (Feature Hashing)

Maps each category to a hash value within a fixed number of buckets.

- **Algorithm**: category → hash(category) % n_buckets → set the corresponding bucket to 1 (or increment count for occurrence encoding).
- **Properties**: Fixed dimensionality regardless of the number of categories; memory-efficient for high-cardinality features; hash collisions may merge distinct categories.
- **Bucket Count**: Typically 2^10 to 2^20 buckets. More buckets = fewer collisions but higher memory usage.
- **When to Use**: Very high-cardinality features (user_id, product_id, query_text); online learning settings where new categories appear at serving time; memory-constrained environments.
- **When NOT to Use**: When interpretability is important (hash encoding is not interpretable); when feature cardinality is low (one-hot or label encoding is simpler and equally effective).

### 1.5 Embedding Encoding (Learned Representations)

Learns a dense, low-dimensional vector representation for each category through neural network training.

- **Example**: Product category with 100K unique values → 64-dimensional embedding vector per category.
- **Properties**: Captures semantic relationships between categories (similar categories have similar embeddings); compact representation; requires sufficient training data to learn meaningful embeddings.
- **Implementation**: An embedding layer in a neural network maps category IDs to dense vectors, trained end-to-end with the recommendation model.
- **When to Use**: In neural network recommendation models; high-cardinality features with semantic structure (product categories, user segments, search queries).
- **When NOT to Use**: In non-neural models (tree-based, linear); when the category space is too large relative to available data (embeddings will be poorly learned).

### 1.6 Encoding Strategy Decision Matrix

| Feature Cardinality | Feature Type | Tree-Based Model | Neural Network | Linear Model |
|--------------------|-------------|------------------|----------------|--------------|
| Low (< 20) | Nominal | One-Hot or Label | One-Hot + Embedding | One-Hot |
| Low (< 20) | Ordinal | Label | Label + Embedding | One-Hot |
| Medium (20–1000) | Nominal | Label or Target | Embedding | Target + One-Hot |
| Medium (20–1000) | Ordinal | Label | Embedding | One-Hot |
| High (1000–1M) | Nominal | Target or Hash | Embedding | Target |
| Very High (> 1M) | Nominal | Hash or Embedding | Embedding | Hash |

---

## 2. Text Preprocessing for Item Metadata

### 2.1 Basic NLP Pipeline

For item titles, descriptions, and other text metadata:

1. **Lowercase**: Convert all text to lowercase to normalize case variations.
2. **Remove HTML Tags**: Strip HTML markup from descriptions (common in e-commerce data).
3. **Remove Special Characters**: Remove or replace special characters, keeping alphanumeric and basic punctuation.
4. **Tokenization**: Split text into individual tokens (words or subwords).
5. **Stop Word Removal**: Remove common words (the, is, at, which, on) that carry little semantic meaning.
6. **Stemming/Lemmatization**: Reduce words to their root form (running → run, better → good).

### 2.2 TF-IDF (Term Frequency-Inverse Document Frequency)

Converts text into numerical features based on word importance.

- **Formula**: TF-IDF(t, d) = TF(t, d) × IDF(t), where:
  - TF(t, d) = count of term t in document d / total terms in document d
  - IDF(t) = log(total documents / documents containing term t)
- **Properties**: Weighs words by their importance to a document relative to the corpus; produces sparse, high-dimensional feature vectors; does not capture word order or semantics.
- **Hyperparameters**:
  - **max_features**: Maximum vocabulary size (typically 10K–50K). Limits feature dimensionality.
  - **ngram_range**: Range of n-grams to consider. (1,1) for unigrams, (1,2) for unigrams + bigrams.
  - **min_df / max_df**: Minimum/maximum document frequency. Filter very rare or very common terms.
- **When to Use**: As input features for non-neural models (XGBoost, logistic regression); as a baseline text representation; when interpretability of text features is important.

### 2.3 Word Embeddings

Dense, low-dimensional vector representations of words that capture semantic meaning.

- **Pre-trained Embeddings**: Word2Vec (Google), GloVe (Stanford), FastText (Facebook) provide pre-trained word vectors trained on large corpora.
- **Document Embeddings**: Average word embeddings to get a document-level representation, or use Doc2Vec for learned document vectors.
- **Advantages Over TF-IDF**: Capture semantic similarity (king - man + woman ≈ queen); dense representation; capture word relationships.

### 2.4 Sentence/Document Embeddings

For representing item descriptions and titles as fixed-length vectors:

- **Sentence-BERT (SBERT)**: Fine-tuned BERT model specifically designed for producing semantically meaningful sentence embeddings. Produces 384–768 dimensional vectors.
- **Universal Sentence Encoder (USE)**: Google's pre-trained model for computing sentence embeddings. Produces 512-dimensional vectors.
- **Average of Word Embeddings**: Simple but effective baseline — average the word2vec/glove embeddings of all words in the text.
- **When to Use**: When the semantic meaning of the full text matters (not just keyword matching); for computing item similarity in embedding space; as input features to neural ranking models.

---

## 3. Numerical Feature Binning

### 3.1 Why Bin Numerical Features?

- **Non-Linear Relationships**: Linear models cannot capture non-linear relationships between a numerical feature and the target. Binning converts the numerical feature into a categorical feature that can capture non-linear effects.
- **Outlier Robustness**: Binning groups extreme values with nearby values, reducing the influence of outliers.
- **Interpretability**: Binned features are more interpretable — "users aged 25–34" is more interpretable than "users with age feature scaled to 0.42."
- **Interaction Effects**: Binned features can capture interaction effects when combined with other features in tree-based models.

### 3.2 Binning Methods

| Method | Description | Advantage | Disadvantage |
|--------|-------------|-----------|--------------|
| **Equal-Width** | Divide range into N equal-width bins | Simple; intuitive | Sensitive to outliers; uneven bin populations |
| **Equal-Frequency (Quantile)** | Each bin has approximately the same number of observations | Balanced bin populations; robust to outliers | May merge values with different meanings; sensitive to ties |
| **K-Means** | Cluster values into K groups using k-means | Groups naturally similar values | Requires choosing K; may not produce meaningful bins |
| **Decision Tree** | Use a decision tree to find optimal split points that maximize target prediction | Supervised; finds optimal bins | Overfitting risk; less interpretable |
| **Custom (Domain-Driven)** | Define bins based on business knowledge | Highly interpretable; captures domain semantics | Requires domain expertise; may miss data patterns |

### 3.3 Binning for Recommendation Features

| Feature | Binning Strategy | Example Bins |
|---------|-----------------|--------------|
| Age | Domain-driven | 18–24, 25–34, 35–44, 45–54, 55–64, 65+ |
| Session Duration | Quantile-based | Q1 (short), Q2 (medium), Q3 (long), Q4 (very long) |
| Price | Domain-driven + log | Budget (<$20), Mid ($20–100), Premium ($100–500), Luxury ($500+) |
| View Count | Log + quantile | 0, 1–10, 11–100, 101–1000, 1000+ |
| Time Since Last Visit | Domain-driven | Today, 1–7 days, 8–30 days, 31–90 days, 90+ days |

---

## 4. Feature Crossing

### 4.1 What is Feature Crossing?

Feature crossing creates new features by combining two or more existing features, capturing interactions that individual features cannot represent.

### 4.2 Types of Feature Crosses

| Cross Type | Example | Captures |
|-----------|---------|----------|
| **Categorical × Categorical** | gender × age_bucket | Segment-level preferences |
| **Categorical × Numerical** | category × price | Category-specific price sensitivity |
| **Numerical × Numerical** | session_duration × items_viewed | Browsing intensity |
| **Temporal × Categorical** | day_of_week × category | Temporal category preferences |
| **User × Item** | user_age_bucket × item_category | Demographic-item affinity |

### 4.3 Feature Crossing for Recommendation Systems

- **User-Item Cross Features**: `user_price_preference × item_price` captures the alignment between the user's typical spending level and the item's price.
- **Context Cross Features**: `time_of_day × device_type × content_category` captures context-dependent preferences (e.g., mobile users prefer short videos in the evening).
- **Behavioral Cross Features**: `recent_category_affinity × item_category` captures whether the item aligns with the user's recent browsing behavior.
- **Popularity Cross Features**: `item_popularity_bucket × user_activity_bucket` captures how different user segments interact with items of different popularity levels.

### 4.4 Cross Features in Neural Networks

- **Explicit Cross Layers**: architectures like DCN (Deep & Cross Network) automatically learn cross features of arbitrary order.
- **Attention Mechanisms**: Transformers can learn cross-feature interactions through attention weights.
- **Factorization Machines**: FM and FNN architectures explicitly model pairwise feature interactions.
- **Advantage Over Manual Crossing**: Neural approaches learn cross features automatically, avoiding the combinatorial explosion of manual feature engineering.

---

## 5. Data Transformation Pipeline Architecture

### 5.1 Batch Transformation Pipeline

```
Raw Data Ingestion
    ↓
Schema Validation
    ↓
Type Casting and Parsing
    ↓
Missing Value Treatment
    ↓
Outlier Detection and Handling
    ↓
Feature Scaling (fit on training data)
    ↓
Categorical Encoding (fit on training data)
    ↓
Text Preprocessing and Embedding
    ↓
Feature Crossing
    ↓
Feature Selection / Importance Ranking
    ↓
Transformed Dataset → Model Training / Feature Store
```

### 5.2 Online Transformation Pipeline (Serving)

```
Raw Request
    ↓
Schema Validation (fast path)
    ↓
Type Casting
    ↓
Feature Lookup from Feature Store (pre-computed features)
    ↓
Real-Time Feature Computation (session features, context features)
    ↓
Categorical Encoding (using saved encoders)
    ↓
Feature Scaling (using saved scalers)
    ↓
Feature Crossing
    ↓
Transformed Feature Vector → Model Inference
```

### 5.3 Training-Serving Consistency

- **Same Code**: The transformation logic must be identical between training and serving. Use shared transformation libraries, not separate implementations.
- **Versioned Artifacts**: All transformation artifacts (scalers, encoders, embedding tables, imputation values) must be versioned alongside the model.
- **Schema Enforcement**: The serving pipeline must validate that all expected features are present and have the correct types, catching transformation bugs before they reach the model.
