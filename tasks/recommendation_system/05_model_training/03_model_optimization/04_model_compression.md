# Model Compression Techniques for Recommendation Systems

## Overview

Model compression encompasses techniques that reduce the size, computational cost, and memory footprint of recommendation models without significant quality degradation. At production scale, compression directly impacts serving cost, latency, and infrastructure requirements. This document covers weight sharing, low-rank factorization, compact embeddings, sparse attention, conditional computation, and early exit strategies.

---

## Weight Sharing

### Concept

Weight sharing reduces the number of unique parameters by reusing the same weight values across multiple locations in the model.

### Types of Weight Sharing

**Horizontal Weight Sharing**:
- Share weights across different feature fields
- Useful when features have similar semantic roles
- Reduces parameter count by factor of sharing ratio

**Vertical Weight Sharing**:
- Share weights across layers in deep networks
- Particularly effective in deep MLPs where layers learn similar transformations
- Reduces parameters linearly with number of shared layers

**Codebook-Based Weight Sharing**:
- Quantize weights to a small set of values (codebook)
- Store only codebook indices instead of full-precision weights
- Typical codebook sizes: 16, 32, 64 entries
- Each entry stores a unique weight value shared across many positions

### Compression Ratios

| Method | Compression Ratio | Quality Impact | Implementation |
|--------|------------------|----------------|----------------|
| Horizontal sharing | 2-5x | Low (< 0.5% loss) | Feature group analysis |
| Vertical sharing | 1.5-3x | Low-moderate | Layer pairing |
| Codebook (256 entries) | 4-8x | Low | Quantization + index storage |
| Codebook (16 entries) | 16-32x | Moderate | Aggressive quantization |

---

## Low-Rank Factorization

### Core Idea

Decompose large weight matrices into products of smaller matrices:

```
W (m × n) ≈ U (m × r) × V (r × n)  where r << min(m, n)
```

### Decomposition Methods

**SVD (Singular Value Decomposition)**:
- Optimal in Frobenius norm for given rank r
- Compute: W = UΣV^T, truncate to top-r singular values
- Reconstruction error: σᵣ₊₁² + ... + σₘₙ² (sum of discarded singular values)

**Randomized SVD**:
- Approximate SVD using random projections
- Much faster for large matrices (O(mn log r) vs O(mn min(m,n)))
- Suitable for very large embedding matrices

**CUR Decomposition**:
- Express W using actual columns and rows of W
- More interpretable than SVD (weights correspond to actual data)

### Application to Recommendation Models

**Embedding Matrix Factorization**:
- Large embedding tables: (num_features × embedding_dim)
- Factorize into two smaller matrices: (num_features × rank) × (rank × embedding_dim)
- Typical rank: 8-64 depending on embedding dimension
- Savings: embedding_dim / rank reduction in parameters

**Dense Layer Factorization**:
- Factorize hidden-to-hidden weight matrices
- Particularly effective in deep MLPs where layers are wide
- Example: 512×512 → 512×32 × 32×512 = 16x fewer parameters per layer

**Attention Matrix Factorization**:
- Factorize query-key-value projection matrices in attention layers
- Reduces the cost of attention computation proportionally

### Practical Guidelines

- Start with rank = 10-20% of original dimension
- Evaluate reconstruction error vs quality tradeoff
- Can combine with fine-tuning to recover quality loss
- Low-rank layers can be merged at inference (no overhead)

---

## Compact Embedding Layers

### The Embedding Size Problem

In recommendation models, embedding tables often dominate model size:
- A model with 10M features × 128 embedding dim × 4 bytes = 4.8 GB
- This exceeds typical GPU memory for serving

### Techniques for Compact Embeddings

**Feature Hashing (Hashing Trick)**:
- Map features to fixed-size hash table (e.g., 1M entries)
- Multiple features may collide (same hash bucket)
- Reduces embedding table size to fixed bound regardless of feature cardinality
- Trade-off: hash collisions may hurt quality slightly

**Dimensionality Reduction**:
- Train with large embeddings, then apply PCA/SVD to reduce dimensions
- Retrain or fine-tune with reduced dimensions
- Typical reduction: 128 → 32-64 dimensions

**Embedding Quantization**:
- Quantize embedding vectors to lower precision (INT8, INT4)
- 4-bit quantization: 8x memory reduction with minimal quality loss
- Use product quantization for better approximation

**Mixed-Dimension Embeddings**:
- Assign embedding dimensions proportional to feature frequency
- Popular features: 128-256 dimensions
- Rare features: 8-32 dimensions
- Weighted average: 2-5x overall compression

**Embedding Pruning**:
- Remove embeddings for very rare features (count < threshold)
- Remove low-importance embedding dimensions across all features
- Combined with feature selection for maximum compression

### Comparison

| Method | Compression | Quality Loss | Complexity |
|--------|------------|-------------|-----------|
| Feature hashing | Fixed table size | Low (collisions) | Low |
| Dimension reduction | 2-8x | Low-moderate | Low |
| INT8 quantization | 4x | Very low | Low |
| INT4 quantization | 8x | Low | Moderate |
| Mixed dimensions | 2-5x | Low | Moderate |
| Embedding pruning | 2-10x | Moderate | Low |

---

## Sparse Attention

### Standard Attention Cost

Full self-attention: O(N² × d) where N = sequence length, d = dimension
- For N = 512, d = 128: 33.5M operations per attention head
- Multiple heads multiply this cost

### Sparse Attention Patterns

**Fixed Patterns**:
- **Local/Sliding window**: Attend to K nearest neighbors → O(N × K × d)
- **Strided/Dilated**: Attend at regular intervals → O(N × K × d)
- **Global tokens**: A few tokens attend to all; others attend locally

**Learned Patterns**:
- **Adaptive span**: Learn optimal attention span per layer
- **Routing attention**: Route tokens to attend to specific groups
- **Top-k attention**: Keep only top-k attention scores per token

**Hybrid Patterns**:
- Combine local and global attention in alternating layers
- Local layers for fine-grained patterns; global layers for long-range dependencies
- Example: every 3rd layer uses global attention, others use local

### Sparse Attention for Sequential Recommendations

| Pattern | Complexity | Captures |
|---------|-----------|----------|
| Full attention | O(N²) | All pairwise interactions |
| Local window | O(N×K) | Recent behavior patterns |
| Strided | O(N×K) | Periodic patterns (daily, weekly) |
| Global + local | O(N×K+G×N) | Long-term and recent preferences |
| Adaptive span | O(N×K_eff) | Optimal coverage per layer |

---

## Conditional Computation

### Concept

Conditionally execute parts of the model based on the input, reducing average computational cost.

### Mixture of Experts (MoE)

- Multiple expert networks; only top-K activated per input
- Gating network learns input-dependent expert selection
- Reduces FLOPs by factor of (total experts / active experts)
- Must balance expert utilization to avoid collapse

**MoE for Recommendation Models**:
- Experts specialized by user segment, item category, or interaction type
- Top-2 gating: activate 2 experts out of 8-16
- Router regularization to prevent expert collapse
- Expert-specific embeddings for feature interaction layers

### Early Exit

- Add classification heads at intermediate layers
- Low-complexity inputs exit early (easier predictions)
- High-complexity inputs use deeper layers
- Reduces average latency by 30-50% for typical distributions

**Early Exit Design for Recommendation**:
- Add scoring head after each feature interaction block
- Confidence-based gating: exit if top score > threshold
- Must calibrate thresholds per layer for consistent quality
- Training: add auxiliary losses at each exit point

### Dynamic Network Width

- Vary the hidden dimension per input based on complexity
- Simple users: narrow layers (fast inference)
- Complex users: wide layers (more capacity)
- Gating network controls width dynamically

---

## Quantization

### Precision Levels

| Precision | Bits | Memory Reduction | Speedup | Quality Impact |
|-----------|------|-----------------|---------|---------------|
| FP32 | 32 | 1x (baseline) | 1x | None |
| FP16/BF16 | 16 | 2x | 1.5-2x | Negligible |
| INT8 | 8 | 4x | 2-4x | Very low (<0.5%) |
| INT4 | 4 | 8x | 3-6x | Low (0.5-1.5%) |
| Binary | 1 | 32x | 10-30x | Moderate (1-3%) |

### Quantization-Aware Training (QAT)

- Simulate quantization during training
- Add fake quantization nodes in forward pass
- Straight-through estimator for backward pass
- Model learns to be robust to quantization error

### Post-Training Quantization (PTQ)

- Quantize after training is complete
- Requires calibration dataset (100-1000 samples)
- Faster than QAT but may lose more quality
- Suitable for straightforward models

---

## Combining Compression Techniques

### Compression Pipeline

1. **Prune** embedding tables (remove rare features)
2. **Quantize** embeddings to INT8 or INT4
3. **Factorize** dense layers using low-rank decomposition
4. **Prune** dense layers to target sparsity
5. **Quantize** dense weights to INT8
6. **Apply** sparse attention if applicable
7. **Evaluate** combined compression ratio and quality

### Typical Achievable Compression

| Combination | Total Compression | Quality Retention |
|------------|------------------|-------------------|
| INT8 quantization only | 4x | >99% |
| Pruning (50%) + INT8 | 8x | >98% |
| Low-rank (4x) + INT8 | 8x | >98% |
| All techniques | 16-32x | >95% |

### Measurement and Validation

- Always measure end-to-end inference latency, not just model size
- Validate quality across all user segments (not just aggregate)
- Profile memory usage during inference (peak and steady state)
- A/B test compressed model against baseline before full deployment
