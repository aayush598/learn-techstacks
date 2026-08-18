# TF-IDF Approach for Content-Based Recommendations

## Overview

Term Frequency-Inverse Document Frequency (TF-IDF) is a statistical measure used to evaluate the importance of a word within a document relative to a corpus. In recommendation systems, TF-IDF serves as a foundational technique for content-based filtering, enabling item similarity computation based on textual metadata such as titles, descriptions, categories, and tags.

TF-IDF converts raw text into numerical feature vectors that capture semantic importance without requiring deep learning infrastructure. This makes it an excellent baseline and a production-viable solution for many recommendation scenarios.

---

## Mathematical Foundation

### TF-IDF Formula

The TF-IDF score for term `t` in document `d` is computed as:

```
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

Where:

- **Term Frequency (TF)**: Measures how frequently a term appears in a document
  ```
  TF(t, d) = (count of t in d) / (total terms in d)
  ```
  Variants include logarithmic TF, augmented TF, and boolean TF.

- **Inverse Document Frequency (IDF)**: Measures how rare or common a term is across the corpus
  ```
  IDF(t) = log(N / df(t))
  ```
  Where `N` is the total number of documents and `df(t)` is the number of documents containing term `t`.

### Variants of TF

| Variant | Formula | Use Case |
|---------|---------|----------|
| Raw Count | TF = count(t, d) | Simple frequency |
| Normalized | TF = count(t, d) / |d| | Length normalization |
| Logarithmic | TF = 1 + log(count(t, d)) | Dampens high frequency |
| Augmented | TF = 0.5 + 0.5 × (count(t, d) / max(count(t, d'))) | Prevents bias toward long docs |
| Boolean | TF = 1 if count(t, d) > 0 else 0 | Presence/absence |

### Variants of IDF

| Variant | Formula | Use Case |
|---------|---------|----------|
| Standard | IDF = log(N / df(t)) | General purpose |
| Smoothed | IDF = log(1 + N / df(t)) | Avoids zero division |
| Probabilistic | IDF = log((N - df(t)) / df(t)) | Probabilistic model |

---

## Document Vector Representation

### Sparse Vector Space Model

Each document (item) is represented as a sparse vector in a high-dimensional space where each dimension corresponds to a unique term in the vocabulary.

**Key characteristics:**
- Dimensionality equals vocabulary size (typically 50K–500K)
- Most entries are zero (sparsity > 99.9%)
- Memory-efficient representations using compressed sparse row (CSR) or coordinate (COO) formats
- Dot product between vectors approximates semantic similarity

### TF-IDF Matrix Construction

The document-term matrix `M` is constructed where:
- Rows represent documents (items)
- Columns represent terms (vocabulary)
- Values are TF-IDF scores

```
M ∈ R^(n × d)
where n = number of documents, d = vocabulary size
```

In production systems, this matrix is stored using sparse matrix formats to minimize memory footprint.

---

## Cosine Similarity

### Definition

Cosine similarity measures the angle between two vectors, providing a similarity score invariant to document length:

```
cosine_sim(A, B) = (A · B) / (||A|| × ||B||)
```

### Properties

- Range: [-1, 1] for general vectors; [0, 1] for TF-IDF vectors (non-negative)
- 1.0 = identical direction (maximum similarity)
- 0.0 = orthogonal (no similarity)
- Length-invariant: short and long documents can be compared directly

### Scalability Optimizations

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Inverted Index | Map terms → document IDs | O(1) term lookup |
| MinHash / LSH | Locality-sensitive hashing for approximate NN | Sub-linear search |
| Blocking | Partition vocabulary into blocks | Parallel computation |
| Truncated SVD | Reduce dimensionality to 100–300 | Dense fast matrix ops |
| Sparse matrix multiplication | Exploit sparsity in dot products | 10–100× over dense |

### Production Considerations

- **Exact search**: Brute-force cosine similarity over all items. Viable for catalogs < 100K items.
- **Approximate nearest neighbor (ANN)**: Libraries like FAISS, Annoy, or ScaNN enable sub-millisecond retrieval over millions of items.
- **Pre-filtering**: Apply category/attribute filters before similarity computation to reduce search space.

---

## Vocabulary Design

### Tokenization Strategies

1. **Whitespace tokenization**: Split on whitespace. Simple but ignores punctuation and casing.
2. **WordPunkt / Treebank**: Language-aware tokenization handling contractions, abbreviations.
3. **Subword tokenization (BPE, WordPiece)**: Handles out-of-vocabulary terms; used in hybrid systems.
4. **Character n-gram tokenization**: Captures morphological patterns (e.g., "recomm" in "recommendation").

### Stopword Removal

- Remove high-frequency, low-information words (e.g., "the", "is", "and")
- Use domain-specific stopword lists (e.g., in e-commerce, "buy", "shop" may be stopwords)
- Beware: some stopwords carry sentiment or intent signals in certain domains

### Stemming vs Lemmatization

| Approach | Method | Speed | Quality |
|----------|--------|-------|---------|
| Stemming (Porter, Snowball) | Rule-based suffix stripping | Very fast | May produce non-words |
| Lemmatization (WordNet, spaCy) | Dictionary-based normalization | Slower | Produces valid words |
| No normalization | Keep original forms | Fastest | Higher vocabulary size |

### Vocabulary Size Management

- **Minimum document frequency**: Filter terms appearing in fewer than `k` documents (e.g., k = 3–10)
- **Maximum document frequency**: Filter terms appearing in more than 80–90% of documents
- **Feature hashing (hashing trick)**: Map terms to fixed-size vector without building vocabulary; eliminates OOV issues
- **Vocabulary pruning**: Keep top-K terms by TF-IDF variance across corpus

---

## N-gram Features

### Unigrams, Bigrams, and Beyond

N-grams capture local word order and multi-word expressions:

- **Unigram** (n=1): "machine", "learning" → independent features
- **Bigram** (n=2): "machine learning" → captures phrase
- **Trigram** (n=3): "natural language processing" → longer phrases

### Practical Guidelines

- Bigrams often provide the best cost-benefit ratio for recommendation systems
- Trigrams and higher create extreme sparsity; use with caution
- Use `max_features` or `min_df` to control vocabulary explosion from n-grams
- Character n-grams (3–5 chars) useful for handling typos and abbreviations in user-generated content

### Implementation Notes

- Scikit-learn's `TfidfVectorizer` supports `ngram_range=(1, 2)` for combined unigram + bigram
- HashingVectorizer with n-grams avoids memory explosion but loses inverse mapping
- Domain-specific phrases (e.g., "deep learning", "neural network") should be treated as single tokens via custom analyzer

---

## Field Weighting

### Motivation

Not all textual fields contribute equally to item relevance. A product title is typically more informative than its description; a movie director name may be more distinctive than its plot summary.

### Weighting Strategies

#### Static Field Weights

Assign fixed multipliers to each field before concatenation:

```
weighted_text = α × title + β × category + γ × description + δ × tags
```

Typical weight ranges:

| Field | Recommended Weight | Rationale |
|-------|-------------------|-----------|
| Title | 3.0–5.0 | Highest information density |
| Category / Genre | 2.0–3.0 | Strong signal for preferences |
| Tags | 1.5–2.5 | User-curated, high relevance |
| Description | 1.0 | Noisy, contains marketing language |
| Brand / Author | 1.5–2.0 | Identity signal |

#### Learned Field Weights

Train a model to learn optimal field contributions:
- Use click-through rate (CTR) as the target variable
- Learn per-field TF-IDF weights via logistic regression or gradient boosting
- Update weights periodically as user behavior evolves

#### Field-Level TF-IDF

Compute separate TF-IDF matrices per field, then combine:

```
similarity(item_i, item_j) = Σ_k w_k × cosine_sim(TF-IDF_k(i), TF-IDF_k(j))
```

This approach preserves field-specific term distributions and allows independent tuning.

---

## BM25 vs TF-IDF

### BM25 Formula

BM25 (Best Matching 25) is a ranking function that extends TF-IDF with length normalization and term frequency saturation:

```
BM25(q, d) = Σ IDF(q_i) × [f(q_i, d) × (k₁ + 1)] / [f(q_i, d) + k₁ × (1 - b + b × |d| / avgdl)]
```

Where:
- `k₁` (typically 1.2–2.0): Controls term frequency saturation
- `b` (typically 0.75): Controls length normalization
- `avgdl`: Average document length in the corpus
- `f(q_i, d)`: Term frequency of query term `i` in document `d`

### Comparison

| Aspect | TF-IDF | BM25 |
|--------|--------|------|
| Term frequency | Linear growth | Saturation (diminishing returns) |
| Length normalization | Division by |d| | Parameterized (b) |
| IDF variant | log(N/df) | Probabilistic IDF |
| Field weighting | Manual | Built-in length normalization |
| Performance | Good baseline | Generally superior |
| Implementation complexity | Simple | Moderate |
| Scalability | Excellent | Excellent |
| Industry adoption | Legacy systems | Search engines (Elasticsearch, Lucene) |

### When to Use BM25 Over TF-IDF

- Documents have significant length variation (e.g., product descriptions from 10 to 5000 words)
- Query-document matching requires term frequency saturation
- You need built-in length normalization without manual tuning
- Integration with search engines (Elasticsearch uses BM25 as default)

---

## Scalability with Sparse Vectors

### Memory Efficiency

| Representation | Memory per entry | Notes |
|---------------|-----------------|-------|
| Dense float32 | 4 bytes | Full matrix |
| Sparse CSR | ~12 bytes (value + indices) | 10–100× savings for TF-IDF |
| Compressed sparse | ~8 bytes | With delta encoding |
| Feature hashing | Fixed size | No vocabulary storage |

### Distributed Computation

- **MapReduce paradigm**: Compute TF-IDF in parallel across document partitions
- **Apache Spark MLlib**: Built-in `HashingTF` and `IDF` for distributed TF-IDF
- **Block matrix multiplication**: Partition the TF-IDF matrix into blocks for distributed cosine similarity
- **Parameter servers**: Store sparse TF-IDF vectors on parameter servers for real-time retrieval

### Indexing Strategies

1. **Inverted index**: For each term, store list of (document_id, tfidf_score) pairs
2. **Partitioned index**: Shard index across machines by document ID or term hash
3. **Hierarchical index**: Cluster documents, build intra-cluster and inter-cluster indices
4. **ANN index**: Build HNSW, IVF, or product quantization index on TF-IDF vectors

---

## Hybrid TF-IDF with Collaborative Signals

### Combining Content and Collaborative Filtering

Pure TF-IDF approaches suffer from the cold-start problem for new users but handle new items well. Combining with collaborative filtering addresses this gap.

#### Feature-Level Fusion

Append TF-IDF features to collaborative filtering input features:

```
combined_features = [CF_user_embedding || TF-IDF_item_vector]
```

- Train a single model on the combined feature space
- Models like Factorization Machines or Deep & Cross Networks handle heterogeneous features natively

#### Score-Level Fusion

Generate scores from both systems and combine:

```
final_score = α × CF_score + (1 - α) × content_score
```

- α can be learned, context-dependent, or fixed
- Simple to implement; each system can be developed and tuned independently

#### Two-Tower Architecture

- **User tower**: Processes user interaction history → user embedding
- **Item tower**: Processes item TF-IDF vector + metadata → item embedding
- Train with contrastive loss (e.g., InfoNCE) on user-item interaction pairs
- Enables efficient ANN retrieval at serving time

#### Iterative Refinement

1. Use TF-IDF to generate initial candidate set for cold-start users
2. As user interactions accumulate, blend in collaborative signals
3. Gradually shift weight from content-based to collaborative as data increases

### Cold-Start Handling

| Scenario | TF-IDF Contribution | CF Contribution |
|----------|---------------------|-----------------|
| New user, existing items | High (item similarity) | Low (no history) |
| Existing user, new item | High (item metadata) | Low (no interactions) |
| Existing user, existing items | Low-Medium (fallback) | High (behavioral signals) |
| New user, new item | Very High (only signal) | None |

---

## Production Deployment Patterns

### Pre-computation Pipeline

1. **Daily/weekly batch**: Recompute TF-IDF vectors for entire catalog
2. **Real-time incremental**: Update TF-IDF for newly added items without full recompute
3. **Vocabulary management**: Maintain vocabulary snapshots for reproducibility

### Serving Architecture

```
Item Catalog → TF-IDF Vectorizer → Sparse Vectors → ANN Index
                                                          ↓
User Query → TF-IDF Transform → Query Vector → Similarity Search → Top-K Items
```

### Monitoring and Maintenance

- **Vocabulary drift**: Monitor new term emergence; retrain vectorizer periodically
- **Similarity quality**: Sample random item pairs, verify cosine similarity rankings make sense
- **Coverage**: Track % of items retrievable via TF-IDF; investigate zero-vector items
- **Latency**: P99 similarity search latency should be < 50ms for real-time serving

---

## Advanced Techniques

### Sublinear TF Scaling

Apply logarithmic scaling to term frequency to reduce the impact of very high-frequency terms:

```
sublinear_tf(t, d) = 1 + log(count(t, d)) if count(t, d) > 0 else 0
```

This is enabled by default in scikit-learn's `TfidfVectorizer` (`sublinear_tf=True`).

### TF-IDF Variants for Short Text

Standard TF-IDF performs poorly on short texts (titles, tags) due to limited term co-occurrence:

- **TF-IDF with pseudo-relevance feedback**: Expand short text with related terms from top-ranked documents
- **Semantic smoothing**: Blend TF-IDF with word embedding averages
- **Domain-augmented TF-IDF**: Use category-level IDF instead of corpus-level IDF for domain-specific terms

### Multi-lingual TF-IDF

- Use language-specific tokenizers and stemmers per language
- Translate terms to a pivot language (English) before TF-IDF computation
- Use multilingual embeddings (e.g., LASER, LaBSE) to bridge languages in a shared vector space
- Maintain separate vocabularies per language with cross-lingual bridging layer

---

## References

- Sparck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval.
- Robertson, S. & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond.
- Scikit-learn documentation: `TfidfVectorizer`, `HashingVectorizer`
- Elasticsearch documentation: BM25 scoring and field boosting
- Google Research: Feature hashing for large-scale machine learning
