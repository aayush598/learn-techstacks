# Neural Collaborative Filtering

## Overview

Neural Collaborative Filtering (NCF) replaces the fixed inner-product in matrix factorization with a neural network that learns arbitrary non-linear feature interactions. Traditional MF is limited to linear interactions in a latent space; NCF uses multi-layer perceptrons to capture complex preference patterns. The framework decomposes into Generalized Matrix Factorization (GMF) for linear interactions and an MLP for non-linear interactions, fused in the NeuMF architecture.

---

## Traditional Matrix Factorization Recap

**Standard MF**: `score(u, i) = p_u^T × q_i + b_u + b_i + μ`

| Limitation of MF | NCF Solution |
|-----------------|--------------|
| Linear interaction (dot product only) | Non-linear via neural network |
| Fixed interaction function | Learned interaction function |
| No side information | Natural feature concatenation |
| Shallow representation | Deep layered architecture |

---

## Generalized Matrix Factorization (GMF)

GMF preserves MF's linear interaction via element-wise product instead of inner product:

```
User embedding: p_u ∈ R^d
Item embedding: q_i ∈ R^d
GMF output: p_u ⊙ q_i (element-wise product → vector)
Prediction: a^T (p_u ⊙ q_i)
```

| MF | GMF |
|----|-----|
| `p^T q` (inner product → scalar) | `p ⊙ q` (element-wise product → vector) |
| Single interaction weight | Per-dimension interaction weights |

---

## MLP Component

Concatenates user/item embeddings and feeds through a deep network:

```
[p_u; q_i] ∈ R^{2d}
  ↓ ReLU(W₁ [p_u; q_i] + b₁) → R^{h₁}
  ↓ ReLU(W₂ h₁ + b₂) → R^{h₂}
  ↓ ...
  ↓ a^T h_L → prediction
```

| Choice | Typical |
|--------|---------|
| Activation | ReLU |
| Hidden sizes | 256 → 128 → 64 |
| Layers | 2–5 |
| Dropout | 0.2 |

MLP can theoretically approximate any continuous function, learning non-linear interactions automatically without assuming a specific interaction structure.

---

## NeuMF: Fusion of GMF and MLP

```
GMF path: p_u ⊙ q_i → output_gmf
MLP path: [p_u; q_i] → MLP → output_mlp
NeuMF: σ(W_o [output_gmf; output_mlp] + b_o)
```

**Training objective (BCE):**

```
L = -Σ_{(u,i)∈S⁺∪S⁻} [y_ui log σ(x_ui) + (1 - y_ui) log(1 - σ(x_ui))]
```

**Pre-training strategy** (He et al., 2017): Pre-train GMF and MLP separately, combine, then fine-tune jointly. Prevents one component from dominating early training.

---

## NCF vs Traditional MF

| Aspect | Traditional MF | NCF (NeuMF) |
|--------|---------------|-------------|
| Interaction function | Inner product (linear) | Neural network (non-linear) |
| Expressiveness | Limited by dot product | Universal approximation |
| Parameters | O((n_u + n_i) × k) | Higher (includes MLP weights) |
| Training complexity | Low (closed-form possible) | Higher (backpropagation) |
| Interpretability | High (factor analysis) | Low (black-box) |
| Side information | Difficult to integrate | Natural concatenation |

---

## User/Item Embedding Learning

### Embedding Table Scale

| Scenario | Users | Items | Dim | Table Size |
|----------|-------|-------|-----|------------|
| Small (MovieLens) | 100K | 20K | 64 | ~8 MB |
| Medium (E-commerce) | 10M | 1M | 128 | ~5 GB |
| Large (YouTube) | 1B | 100M | 256 | ~500 GB |

### Compression Strategies

- **Hash embeddings**: Map IDs to fixed-size table via hash; collision-tolerant
- **Quantized embeddings**: FP32 → INT8/FP16
- **Pruned embeddings**: Remove rarely-seen item embeddings
- **Low-rank factorization**: `E = W₁ × W₂` where W₁ ∈ R^{|I|×r}, W₂ ∈ R^{r×d}, r << d

---

## NCF at Scale

### Negative Sampling Strategies

| Strategy | Description | Complexity |
|----------|-------------|------------|
| Uniform random | Sample from catalog uniformly | O(1) |
| Popularity-weighted | Sample proportional to popularity | O(1) with alias table |
| Hard negative mining | Sample items model scores highly | O(N) for mining |
| In-batch negatives | All non-target items in batch as negatives | O(batch_size) |

Popularity weighting with α ∈ [0,1] on frequency: α=0.5 (sqrt) is common default. Too easy negatives provide weak gradients; too hard may be false negatives.

### Mini-batch Construction

For batch of B positives: sample K negatives per positive → B×(1+K) examples. Typical K: 4–10. Forward pass computes all scores; loss over positive/negative pairs.

---

## Feature Interaction Modeling

| Interaction Type | Example | NCF Modeling |
|-----------------|---------|-------------|
| First-order | User likes item | Bias terms, GMF |
| Second-order | User likes comedy + item is comedy | Embedding dot product |
| High-order | User likes comedy AND recent AND cheap | MLP layers |
| Cross-feature | User-young ∩ item-action | NeuMF concatenation |

---

## NCF Extensions

### Deep & Cross Network (DCN)

Explicitly models bounded-degree feature crosses: `x_{l+1} = x₀ × x_l^T × w_l + x_l + b_l`. Parallel to a deep network; outputs concatenated. Guarantees explicit crosses up to polynomial degree equal to cross layers.

### Deep Interest Network (DIN)

Extends NCF with attention over user behavior sequence. Target-item-aware attention weights each historical item by relevance to target. Captures diverse user interests (different items activate different interests). Used extensively in e-commerce CTR (Alibaba).

### Deep Interest Evolution Network (DIEN)

Adds temporal evolution via GRU + AUGRU. Interest extractor GRU processes behavior sequence; attention-guided GRU (AUGRU) models how interests change over time.

### Multi-Task Extensions

Shared embedding layers across prediction tasks (CTR, conversion, dwell time). MMoE for flexible task-specific routing via mixture-of-experts gating.

---

## Production Considerations

### Serving Pipeline

```
Request → Feature Lookup → Embedding Lookup → Model Forward → Score → Ranking
```

- Embedding lookup: ~1 ms (cached)
- Forward pass: ~0.5 ms (small NeuMF on CPU)
- Total: < 5 ms per prediction

### Online Learning

Update embeddings incrementally for active users. Sparse gradient updates for embeddings that received gradients. Periodic full retraining (daily/weekly) to prevent drift.

### A/B Testing

NCF variants show modest offline improvement over MF; online metrics (CTR, conversion) may show larger gains. Monitor recommendation diversity — NCF can over-specialize without regularization.
