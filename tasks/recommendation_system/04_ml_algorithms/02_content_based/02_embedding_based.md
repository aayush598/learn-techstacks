# Embedding-Based Content Recommendations

## Overview

Embedding-based approaches represent items as dense, low-dimensional vectors learned from their content (text, images, audio). Unlike sparse TF-IDF representations, embeddings capture semantic meaning, contextual relationships, and cross-modal information. This enables more nuanced similarity computation and powers modern recommendation systems at scale.

---

## Word-Level Embeddings

### Word2Vec

#### Architecture

Word2Vec (Mikolov et al., 2013) learns word embeddings through two architectures:

**CBOW (Continuous Bag of Words):**
- Predicts a target word from its surrounding context window
- Faster to train; better for frequent words
- Architecture: Context words → averaged embeddings → hidden layer → softmax over vocabulary

**Skip-gram:**
- Predicts context words from a target word
- Better for rare words and smaller datasets
- Architecture: Target word embedding → hidden layer → softmax over context positions

#### Training Optimization

- **Negative sampling**: Instead of full softmax over entire vocabulary, sample K negative examples (typically K = 5–20). Reduces training from O(V) to O(K) per word.
- **Hierarchical softmax**: Build Huffman tree over vocabulary; compute probability via path from root to leaf. O(log(V)) per word.
- **Subsampling of frequent words**: Discard high-frequency words (e.g., "the") with probability `P(discard) = 1 - sqrt(t/f)` where `f` is word frequency.

#### Limitations for Recommendations

- Produces a single vector per word (no polysemy handling)
- Does not capture word order beyond the context window
- Word-level averaging for document embeddings loses structural information

### GloVe (Global Vectors for Word Representation)

- Factorizes the word co-occurrence matrix directly
- Combines global matrix factorization with local context window methods
- Training objective: `J = Σ f(X_ij)(w_i^T w_j + b_i + b_j - log(X_ij))^2`
- Weight function `f(x)` caps the influence of very high co-occurrence counts

### FastText

- Extends Word2Vec by representing words as bags of character n-grams
- Each word vector = sum of its n-gram vectors + word vector
- Handles out-of-vocabulary words via subword composition
- Particularly useful for morphologically rich languages and noisy text (social media, product titles)

---

## Sentence and Document Embeddings

### Sentence-BERT (SBERT)

#### Architecture

- Based on a pre-trained BERT network (or RoBERTa, DistilBERT)
- Adds a pooling strategy to produce fixed-length sentence embeddings:
  - **CLS token**: Use the [CLS] token output as sentence embedding
  - **Mean pooling**: Average all token embeddings (most common)
  - **Max pooling**: Element-wise max over token embeddings
- Trained with siamese/triplet network objective to produce semantically meaningful sentence vectors

#### Training Objectives

**Classification objective:**
- Concatenate sentence embeddings [u; v; |u-v|] and classify entailment
- Fine-tune on NLI (Natural Language Inference) datasets (SNLI, MultiNLI)

**Regression objective:**
- Minimize cosine similarity loss between related sentence pairs
- Fine-tune on STS (Semantic Textual Similarity) benchmarks

**Triplet objective:**
- Minimize distance between anchor-positive pair, maximize distance from anchor-negative pair
- Requires careful negative mining to avoid trivial solutions

#### Model Variants

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | General-purpose, production |
| all-mpnet-base-v2 | 768 | Moderate | Best | When quality matters |
| all-distilroberta-v1 | 768 | Moderate | Good | Balance of speed/quality |
| paraphrase-multilingual | 384 | Moderate | Good | Multi-language |

### Average Embeddings (Word2Vec/BERT → Document)

#### Simple Averaging

```
doc_embedding = (1/n) × Σ word_embedding_i
```

- Fast but ignores word importance and order
- Works surprisingly well when combined with IDF weighting: `doc_emb = Σ (tfidf_i × word_emb_i) / Σ tfidf_i`

#### Weighted Averaging Strategies

1. **TF-IDF weighted**: Weight word embeddings by their TF-IDF scores
2. **Attention-weighted**: Learn attention weights over words for task-specific pooling
3. **SIF (Smooth Inverse Frequency)**: `emb = Σ (a/(a + p(w))) × word_emb` where `a` is a smooth parameter and `p(w)` is word frequency

---

## Pre-trained Language Models for Content Understanding

### BERT and Variants

| Model | Parameters | Context Length | Key Advantage |
|-------|-----------|---------------|---------------|
| BERT-base | 110M | 512 | Foundational bidirectional model |
| BERT-large | 340M | 512 | Higher quality, more compute |
| RoBERTa-large | 355M | 512 | Optimized training, robust |
| DistilBERT | 66M | 512 | 60% faster, 97% quality |
| DeBERTa-v3 | 86M | 512 | Disentangled attention, SOTA |
| ModernBERT | 395M | 8192 | Long context, modern architecture |

### Feature Extraction vs Fine-tuning

**Feature extraction (frozen):**
- Run pre-trained model once, store embeddings
- Fast inference; no GPU required at serving time
- Suitable when domain matches pre-training data
- Typical: Use last 4 layers' hidden states, concatenate or pool

**Fine-tuning:**
- Update model weights on domain-specific data
- Higher quality but requires retraining pipeline
- Essential for domain-specific vocabularies (medical, legal, technical)
- Use discriminative learning rates: lower LR for earlier layers

### Domain-Specific Pre-training

1. **Continue pre-training** on domain corpus (masked language modeling)
2. **Domain-adaptive pre-training**: Start from general model, adapt to domain
3. **Task-adaptive pre-training**: Further pre-train on task-relevant data before fine-tuning

**Examples in recommendations:**
- E-commerce: Pre-train on product titles, descriptions, reviews
- Movies: Pre-train on scripts, reviews, plot summaries
- News: Pre-train on article bodies, headlines, categories

---

## Fine-tuning Domain-Specific Embeddings

### Training Data Sources

- **Positive pairs**: Items co-purchased, co-viewed, or rated similarly by users
- **Hard negatives**: Items from the same category but different sub-category
- **Sentence pairs**: Title-description pairs from the same item
- **Contrastive triplets**: (anchor, positive, negative) from user interaction logs

### Training Strategies

#### Contrastive Learning

```
Loss = -log(exp(sim(anchor, positive)/τ) / Σ exp(sim(anchor, j)/τ))
```

Where `τ` is the temperature parameter controlling the sharpness of the distribution.

#### Margin-based Triplet Loss

```
Loss = max(0, sim(anchor, negative) - sim(anchor, positive) + margin)
```

#### Hard Negative Mining

- **Batch hard**: Within each batch, use the hardest negative (highest similarity to anchor that isn't the positive)
- **In-batch negatives**: Treat all non-target items in the batch as negatives (efficient, used in CLIP, SimCLR)
- **Semantic negatives**: Sample negatives from similar categories to increase difficulty

### Fine-tuning Best Practices

- **Learning rate**: 1e-5 to 5e-5 for full model; 1e-3 to 1e-2 for new layers only
- **Warm-up**: 10% of total steps for learning rate warm-up
- **Batch size**: Large batches (256–4096) for contrastive learning to have enough negatives
- **Temperature**: 0.01–0.1 for contrastive loss (lower = harder boundary)
- **Data augmentation**: Paraphrasing, synonym replacement, back-translation

---

## Multimodal Embeddings (Text + Image)

### CLIP (Contrastive Language-Image Pre-training)

#### Architecture

- **Image encoder**: Vision Transformer (ViT) or ResNet → image embedding
- **Text encoder**: Transformer → text embedding
- Both encoders project to a shared embedding space
- Trained on 400M image-text pairs from the internet

#### How CLIP Works for Recommendations

1. Encode item images with the image encoder
2. Encode item titles/descriptions with the text encoder
3. Compute cross-modal similarity: `sim = image_emb @ text_emb^T`
4. Use either or both embeddings for item representation

#### Advantages

- Zero-shot classification capability (describe categories in natural language)
- Robust to distribution shift (trained on diverse internet data)
- Handles text-image alignment without explicit annotation

### BLIP-2 and Flamingo

- BLIP-2: Efficient pre-training for vision-language understanding
- Flamingo: Few-shot learning with visual and language models
- Useful for generating rich item descriptions from images

### Multi-Modal Fusion Strategies

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Early fusion | Concatenate modalities at input level | Simple | Modality imbalance |
| Late fusion | Combine embeddings at output level | Modality independence | Misses cross-modal patterns |
| Cross-attention | Attend across modalities | Rich interactions | Expensive |
| Co-attention | Parallel attention on both modalities | Balanced | Complex implementation |
| Product of experts | Multiply probability distributions | Modular | Requires calibrated probabilities |

### Practical Architecture for E-Commerce

```
Item → Image Encoder (ViT-B/16) → image_emb (768d) ─┐
                                                      ├→ Concatenate → Linear → item_emb (256d)
       → Text Encoder (SBERT) → text_emb (768d) ────┘
```

- Train the projection layer and fine-tune encoders with click/purchase labels
- Store final 256d vectors in ANN index for serving

---

## Embedding Similarity Search

### Exact Search

- Brute-force cosine similarity: O(n × d) per query
- Viable for catalogs < 1M items with < 1ms latency budget on GPU
- Use optimized BLAS routines (cuBLAS, MKL) for matrix multiplication

### Approximate Nearest Neighbor (ANN) Algorithms

#### Locality-Sensitive Hashing (LSH)

- Hash similar items to the same bucket with high probability
- Multiple hash tables for better recall
- Time complexity: O(n^(1-1/c)) where c is the approximation factor

#### Hierarchical Navigable Small World (HNSW)

- Multi-layer graph where each layer is a navigable small world
- Search starts at the top layer, drills down to the bottom
- Parameters: `M` (connections per node), `efConstruction` (build-time search width)
- Sub-millisecond search with > 95% recall

#### Inverted File Index (IVF)

- Partition vector space into Voronoi cells using k-means
- At query time, search only the closest `nprobe` cells
- Combined with Product Quantization (IVF-PQ) for memory efficiency

#### Product Quantization (PQ)

- Split vector into sub-vectors, quantize each independently
- Reduces memory by 32–64× with minimal quality loss
- Additive Quantization (AQ) and Residual Quantization (RQ) as variants

### Library Comparison

| Library | Algorithm | Memory | Speed | Recall | Language |
|---------|-----------|--------|-------|--------|----------|
| FAISS | IVF, HNSW, PQ | High | Very Fast | High | C++/Python |
| Annoy | LSH-based trees | High | Fast | Medium | C++ |
| ScaNN | Anisotropic quantization | Low | Very Fast | High | C++ |
| Milvus | HNSW, IVF | Configurable | Fast | High | Go/C++ |
| Pinecone | Proprietary ANN | Managed | Fast | High | Cloud |
| pgvector | IVFFlat, HNSW | Moderate | Moderate | Medium | C++/SQL |

---

## Embedding Dimensionality Selection

### Tradeoffs

| Dimensions | Storage/Item | Search Speed | Quality | Use Case |
|-----------|-------------|-------------|---------|----------|
| 32 | 128 bytes | Very fast | Low | Quick prototyping |
| 64 | 256 bytes | Fast | Medium | Mobile/embedded |
| 128 | 512 bytes | Fast | Good | Balanced production |
| 256 | 1 KB | Moderate | Very Good | High-quality serving |
| 512 | 2 KB | Moderate | Excellent | When storage is cheap |
| 768 | 3 KB | Slower | Excellent | Maximum quality |

### Selection Guidelines

1. **Start with 256 dimensions**: Good default for most recommendation tasks
2. **Monitor recall@K vs dimension**: Plot recall curve to find the knee
3. **Consider downstream use**: If embeddings feed into another model, match that model's expected input
4. **Storage budget**: At 100M items, 256d float32 = ~93 GB; 128d = ~47 GB
5. **Dimensionality reduction**: Train with higher dimensions (512–768), compress with PCA or autoencoders to target size

### Compression Techniques

- **PCA**: Linear reduction; retains most variance; fast
- **Autoencoders**: Non-linear reduction; can capture complex patterns
- **Product Quantization**: At query time; no change to stored vectors
- **Binary embeddings**: Each dimension → 1 bit; extreme compression with moderate recall loss
- **Matryoshka representation learning**: Embeddings are meaningful at any prefix dimension (e.g., 32, 64, 128, 256)

---

## Production Considerations

### Embedding Update Strategy

| Approach | Freshness | Compute Cost | Consistency |
|----------|----------|-------------|------------|
| Full retraining | Low (days/weeks) | High | High |
| Incremental fine-tuning | Medium (hours) | Moderate | Good |
| Online learning | High (real-time) | Low per update | Variable |
| Feature store caching | Based on TTL | Low | Eventual |

### Quality Monitoring

- **Embedding drift**: Track average cosine similarity of new items to existing catalog
- **Coverage**: % of items with valid (non-zero, non-NaN) embeddings
- **Recall metrics**: Online A/B test recall@K against ground truth clicks/purchases
- **Diversity**: Measure intra-list diversity (average pairwise distance among recommended items)

### Cold Start with Embeddings

- **New items**: Compute embeddings from content immediately; no interaction data needed
- **New users**: Use liked item embeddings to form user profile; find similar items
- **Sparse content**: Augment with metadata, category hierarchy, or knowledge graph connections
