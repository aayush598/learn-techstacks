# Wide & Deep Learning for Recommendations

## Overview

Wide & Deep Learning (Google, 2016) formalizes the dual objectives of recommendations: **memorization** (direct feature interactions from history) and **generalization** (novel combinations from learned representations). Two components are trained jointly — a wide linear model for memorization and a deep neural network for generalization. This spawned DeepFM, DCN, and DCN V2 that address the original's limitations.

---

## Wide Component

### Generalized Linear Model

```
ŷ_wide = σ(W_wide × x + b_wide)
```

### Feature Crosses

Conjunctions of features encoding meaningful interactions:

| Cross Example | Raw Features | Cross |
|--------------|--------------|-------|
| User likes action AND item is action | user_genre=action, item_genre=action | user_action × item_action |
| User is young AND item is cheap | user_age=young, item_price=low | user_young × item_cheap |

**Cross product**: `cross(x₁, x₂) = {x₁=1 AND x₂=1}` — binary feature active when both inputs active.

**Memorization** captures high-frequency specific correlations; **limitation**: requires manual feature engineering, limited to first-order interactions.

---

## Deep Component

### Architecture

```
Sparse features → Embedding layers → Concatenation → Hidden layers → Output
Dense features  → Projection ─────→
```

| Layer | Transformation |
|-------|---------------|
| Embedding | Categorical → dense vector (e.g., 64–256 dim) |
| Concat | All embeddings + projected dense features |
| Hidden 1 | ReLU(W₁ × concat + b₁) |
| Hidden 2 | ReLU(W₂ × h₁ + b₂) |
| Output | σ(W_out × h_L + b_out) |

**Generalization** learns abstract patterns from representations — e.g., sci-fi book lovers may also like sci-fi movies without explicit cross features. Limitation: may not capture important specific correlations.

---

## Joint Training

```
P(y=1 | x) = σ(wide^T × [x, x_cross] + deep^T × h_deep + b)
```

Both components process the same input; gradients flow through a single loss. Joint training regularizes the wide component via the deep path and allows the wide component to capture patterns the deep misses.

| Aspect | Separate | Joint |
|--------|----------|-------|
| Feature sharing | No | Embeddings shared |
| Regularization | Independent | Mutual regularization |
| Optimization | Two optima | Single global optimum |

---

## Wide & Deep for Recommendations

### Feature Engineering

**Wide (manual crosses)**: User×Category, User×DayOfWeek, User×Device, Query×TitleMatch
**Deep (embeddings)**: User embedding, Item embedding, Context embeddings, History average

Google Play Store: +2.3% AUC, +3.9% download rate lift over either component alone.

---

## DeepFM: Replacing Wide with FM

Replaces manual feature crosses with Factorization Machine that automatically learns second-order interactions:

```
FM = w₀ + Σᵢ wᵢxᵢ + Σᵢ Σⱼ>i ⟨vᵢ, vⱼ⟩ xᵢxⱼ
```

Efficient computation: `Σᵢ Σⱼ>i ⟨vᵢ, vⱼ⟩ = 0.5 × [(Σᵢ vᵢ)² - Σᵢ vᵢ²]` in O(kn).

| Aspect | Wide & Deep | DeepFM |
|--------|------------|--------|
| Low-order crosses | Manual (wide) | Automatic (FM) |
| Feature engineering | Heavy | Minimal |
| Embedding sharing | Separate | FM and DNN share embeddings |

---

## DCN: Deep & Cross Network

### Cross Layer

```
x_{l+1} = x₀ × x_l^T × w_l + x_l + b_l
```

- `x₀` fed to every cross layer; `x_l` is previous cross layer output
- After L layers: feature crosses up to degree L+1
- O(d) parameters per layer vs O(d²) for dense layers

### DCN Architecture

```
Input → Embedding → x₀ → Cross Network (L layers) → x_L
                                        ↓
                          Deep Network (M layers) → h_M
                                        ↓
                          Concat [x_L; h_M] → Output
```

---

## DCN V2

| Aspect | DCN | DCN V2 |
|--------|-----|--------|
| Cross layer | Outer product O(d²) | Low-rank decomposition O(d×d') |
| Scalability | Limited | Large feature spaces |
| Expressiveness | Linear crosses | Non-linear crosses |
| MoE option | No | Yes for further scaling |

**Cross V2**: `x_{l+1} = σ(W₂ × ReLU(W₁ × x_l) + x_l) + x_l` where W₁ ∈ R^{d'×d}, W₂ ∈ R^{d×d'}, d' << d.

**MoE-DCN V2**: Routes different feature groups to expert cross networks; each expert specializes in crossing a feature subset.

---

## Feature Crossing Comparison

| Model | Crossing | Order | Automation | Parameters |
|-------|---------|-------|-----------|------------|
| Wide & Deep | Manual crosses | 1st | Manual | O(features × crosses) |
| DeepFM | FM products | 2nd | Automatic | O(features × dim) |
| DCN/DCN V2 | Cross network | (L+1)-th | Automatic | O(d × d' × L) |
| AutoInt | Self-attention | Arbitrary | Automatic | O(n² × d) |

---

## Production Architecture

### Embedding Serving

| Strategy | Memory | Latency | Use Case |
|----------|--------|---------|----------|
| In-memory | O(|V| × d) | < 1ms | Small-medium vocabulary |
| Distributed PS | O(|V| × d / N) | 1–5ms | Large vocabulary |
| Quantized | O(|V| × d / 4) | < 1ms | Memory-constrained |

### Training Infrastructure

- **Data pipeline**: Apache Beam/Spark for feature engineering
- **Training**: TensorFlow/PyTorch on GPU clusters
- **Serving**: Embedding lookup + model forward pass + ranking (< 50ms total)
- **Evaluation**: Offline AUC then online A/B test

### Online vs Batch

| Aspect | Batch | Online |
|--------|-------|--------|
| Freshness | Hours–days | Minutes–seconds |
| Stability | High | May be noisy |
| Infrastructure | Standard | Complex (streaming) |

---

## Summary

Wide & Deep formalizes memorization-generalization duality through jointly trained linear and deep components. DeepFM automates wide's feature crossing via FM. DCN/DCN V2 provide explicit learnable high-order crosses with controlled complexity. Production centers on efficient embedding serving, real-time features, and latency management.
