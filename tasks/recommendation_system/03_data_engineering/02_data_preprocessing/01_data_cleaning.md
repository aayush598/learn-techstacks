# Data Preprocessing for Recommendation Systems

## 1. Data Cleaning

### 1.1 Duplicate Detection and Removal
- **Exact Duplicates**: Identical event records (same event_id)
- **Near Duplicates**: Similar events with minor differences (timestamps, metadata)
- **Detection Methods**: Hash-based deduplication, Bloom filters, fuzzy matching
- **Deduplication Window**: Time-based window (e.g., deduplicate within 1 hour)
- **Preservation**: Keep first occurrence; log duplicates for analysis

### 1.2 Data Type Validation
- Ensure user_id, item_id are valid format (UUID, string)
- Ensure timestamps are valid and in expected timezone
- Ensure numeric fields (ratings, prices) are within valid ranges
- Ensure categorical fields have valid values
- Type coercion for mismatched types

### 1.3 Outlier Detection and Handling
- **Statistical Methods**: Z-score, IQR-based outlier detection
- **Domain-Specific Rules**: Dwell time > 24 hours likely erroneous
- **Isolation Forest**: ML-based anomaly detection for complex patterns
- **Handling Strategies**: Cap at threshold, remove, impute, flag for review

---

## 2. Missing Value Treatment

### 2.1 Types of Missing Data
- **Missing Completely at Random (MCAR)**: Missingness unrelated to any variable
- **Missing at Random (MAR)**: Missingness related to observed variables
- **Missing Not at Random (MNAR)**: Missingness related to unobserved variables (common in recommendations)

### 2.2 Imputation Strategies
- **Mean/Median Imputation**: For numerical features; simple but reduces variance
- **Mode Imputation**: For categorical features
- **KNN Imputation**: Use similar users/items to estimate missing values
- **Matrix Factorization**: Decompose user-item matrix to fill missing values
- **Model-Based Imputation**: Train model to predict missing values
- **Forward/Backward Fill**: For time-series data; carry forward/backward last known value

### 2.3 Missing Value Indicators
- Create binary feature indicating whether value was missing
- Missingness itself may be informative (e.g., user who doesn't rate may have different preferences)

---

## 3. Feature Scaling

### 3.1 Normalization Techniques
- **Min-Max Scaling**: Scale to [0,1] range; sensitive to outliers
- **Z-Score Standardization**: Zero mean, unit variance; assumes normal distribution
- **Robust Scaling**: Use median and IQR; resistant to outliers
- **Log Transform**: For right-skewed distributions (e.g., dwell time, purchase amount)
- **Box-Cox Transform**: Power transform toward normality

### 3.2 Scaling by Feature Type
- **User Interaction Counts**: Log transform + standardization
- **Ratings**: Min-max scaling or keep as-is for neural models
- **Timestamps**: Relative encoding (time since epoch, time of day)
- **Categorical**: Embedding or one-hot encoding (no scaling needed)
- **Text Embeddings**: L2 normalization for cosine similarity

### 3.3 Scaling Pitfalls
- **Data Leakage**: Fit scaler on training data only; transform test data with training scaler
- **Different Scales**: Some models (tree-based) don't need scaling
- **Online Scaling**: Maintain running statistics for online feature scaling
- **Inverse Scaling**: Maintain inverse transform for interpretable outputs

---

## 4. Data Transformation

### 4.1 Encoding Categorical Variables
- **One-Hot Encoding**: For low-cardinality categories (<20 values)
- **Label Encoding**: For ordinal categories
- **Target Encoding**: Mean target value per category (regularized)
- **Hash Encoding**: For high-cardinality categories (user_id, item_id)
- **Embedding Encoding**: Learned dense representations for categories

### 4.2 Text Preprocessing for Item Metadata
- **Tokenization**: Split text into tokens
- **Lowercasing**: Normalize case
- **Stop Word Removal**: Remove common words
- **Stemming/Lemmatization**: Reduce words to root form
- **TF-IDF**: Term frequency-inverse document frequency vectors
- **Word Embeddings**: Word2Vec, GloVe dense representations
- **Sentence Embeddings**: Sentence-BERT for item descriptions

### 4.3 Numerical Feature Binning
- **Equal-Width Binning**: Divide range into equal-width bins
- **Equal-Frequency Binning**: Divide into bins with equal number of values
- **Domain-Specific Binning**: Age groups, price ranges
- **Advantages**: Captures non-linear relationships; reduces noise

### 4.4 Feature Crossing
- **User × Item Cross**: User preferences × item attributes
- **Time × Category**: Time-of-day preferences for different categories
- **Device × Content**: Device-specific content preferences
- **Location × Item**: Location-relevant item features

---

## 5. Data Validation

### 5.1 Schema Validation
- Verify all required fields present
- Validate data types match schema
- Check enum values are within allowed set
- Validate referential integrity (user_id exists, item_id exists)

### 5.2 Statistical Validation
- Distribution checks: Features should have expected distributions
- Correlation checks: Highly correlated features may indicate data issues
- Trend checks: No unexpected changes in data patterns
- Volume checks: Expected number of records per time period

### 5.3 Business Logic Validation
- Rating values within valid range (e.g., 1-5)
- Prices are positive
- Timestamps are not in the future
- User-item pairs are valid (user hasn't been deleted)
- No data leakage (future data in training set)
