# Deep Interest Network (DIN) and Deep Interest Evolution Network (DIEN)

## Overview

DIN and DIEN address a fundamental limitation of CTR prediction models: they treat a user's behavior history as a fixed representation, ignoring that interests are diverse, multi-faceted, and evolve over time. DIN introduces target-item-aware attention over the behavior sequence. DIEN extends this with GRU-based interest extraction and attention-guided interest evolution. Both developed at Alibaba for large-scale e-commerce CTR prediction.

---

## Deep Interest Network (DIN)

### Core Insight

When predicting CTR for a target item, only a subset of the user's historical behaviors are relevant. DIN computes attention weights between the target and each historical item, producing a tailored representation per prediction.

### Architecture

```
User features: [user_id, age, gender, ...] → MLP → user_repr
Target item: [item_id, category, brand, ...] → target_repr
Behavior sequence: [item₁, ..., itemₙ] → Embedding → [e₁, ..., eₙ]
                                                        ↓ Attention (query = target_repr)
                                                   Weighted sum: a = Σᵢ αᵢ × eᵢ
                                                        ↓
                                        [user_repr; a; target_repr] → MLP → CTR
```

### Activation Attention (Query-Aware)

| Scoring Function | Formula | Properties |
|-----------------|---------|-----------|
| Dot product | `eᵢ^T × t` | Simple, fast |
| Element-wise product | `eᵢ ⊙ t` | Dimension-wise similarity |
| MLP | `MLP([eᵢ; t])` | Most expressive |
| Adaptive (DIN default) | `MLP([eᵢ; t; eᵢ - t; eᵢ ⊙ t])` | Best expressiveness |

The adaptive function concatenates four signals: two embeddings, their difference, and element-wise product — giving multiple views of the relationship.

### Local Activation Unit

DIN's attention is a "local activation unit" because it locally activates (weights) the behavior sequence based on the target. Properties: target-dependent, sparse activation (most items near-zero weight), interpretable, efficient single forward pass.

### DIN Feature Extraction

| Feature Group | Examples | Type |
|--------------|----------|------|
| User profile | ID, age, gender, city | Categorical |
| Behavior | Click/purchase/search history | Sequence |
| Item | ID, category, brand, price | Categorical |
| Context | Time, device, position | Categorical |

---

## Deep Interest Evolution Network (DIEN)

### Motivation

DIN captures which items are relevant but not how interests change. A user interested in "running shoes" last month may now prefer "hiking boots" — DIEN models this temporal evolution.

### Architecture

```
Behavior sequence: [item₁, ..., itemₙ]
         ↓ Interest Extractor Layer (GRU): [h₁, ..., hₙ]
         ↓ Interest Attention Layer (AUGRU): [h'₁, ..., h'ₙ]
         ↓ Final interest: h'ₙ
         ↓ MLP → CTR
```

### Interest Extractor Layer

Standard GRU processes behavior sequence:

```
z_t = σ(W_z × [h_{t-1}, e_t])      (update gate)
r_t = σ(W_r × [h_{t-1}, e_t])      (reset gate)
h̃_t = tanh(W × [r_t ⊙ h_{t-1}, e_t])
h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t
```

Hidden state `h_t` represents interest state after observing item `t`. **Auxiliary loss** supervises GRU to predict the next item: `L_aux = -Σₜ log σ(h_t^T × e_{t+1})`.

### Interest Attention Layer (AUGRU)

Modifies GRU gate with attention weights from target item:

```
Standard:  z_t = σ(W_z × [h_{t-1}, e_t])
AUGRU:     z̃_t = α_t × z_t
           h'_t = (1 - z̃_t) ⊙ h'_{t-1} + z̃_t ⊙ h_t
```

Where `α_t = softmax(score(h_t, target_embedding))`.

- High α_t (relevant time step): gate allows current interest to flow through
- Low α_t (irrelevant): gate blocks current state, preserves previous

### DIEN Layer Summary

| Layer | Input → Output | Purpose |
|-------|---------------|---------|
| Embedding | Raw features → dense vectors | Feature representation |
| Interest extractor | Behavior seq → interest states [h₁,...,hₙ] | Temporal encoding |
| Interest attention | Interest states + target → [h'₁,...,h'ₙ] | Target-aware selection |
| MLP | User features + final interest → CTR score | Final prediction |

---

## User Behavior Sequence Modeling

### Sequence Construction

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Ordering | Chronological | Captures temporal dynamics |
| Truncation | Last N (20–200) | Balances context and compute |
| Clicks vs purchases | Separate sequences | Different interest signals |
| Session vs global | Global with recency weighting | Broader context |
| Filtering | Remove duplicates, bots | Clean signal |

### Handling Long Sequences

- **Truncation**: Most recent N items (loses long-term signal)
- **Subsampling**: Random sample from full sequence (preserves distribution)
- **Hierarchical attention**: Segment-level then within-segment attention
- **Time-aware subsampling**: Denser sampling from recent history

---

## Long/Short-Term Interest Separation

User behavior contains two signals: **short-term** (recent, specific, volatile) and **long-term** (historical, general, stable).

| Strategy | Implementation | Model |
|----------|---------------|-------|
| Time-windowed sequences | Separate recent and historical | Multi-sequence DIN |
| GRU state decay | Weight recent states higher | DIEN with decay |
| Dual-channel attention | Two attention mechanisms | Custom architectures |
| Explicit separation | Separate networks for long/short | BST, SIM |

DIN implicitly separates via attention (recent relevant items get higher weight). DIEN makes this explicit through AUGRU's selective gating.

---

## Production Considerations

### Serving Latency

| Component | DIN | DIEN |
|-----------|-----|------|
| Embedding lookup | ~1 ms | ~1 ms |
| Attention | ~2–5 ms | ~2–5 ms |
| GRU inference | N/A | ~3–8 ms |
| MLP | ~1 ms | ~1 ms |
| **Total** | **~5–8 ms** | **~8–15 ms** |

DIEN slower due to sequential GRU (O(N) steps, not parallelizable).

### Optimization

- **Pre-compute GRU states**: Run once per session; cache intermediate states
- **Attention caching**: Pre-compute for frequently queried targets
- **Sequence compression**: Every k-th item for long histories
- **ONNX/TensorRT**: Optimized inference graphs
- **Batch inference**: Multiple user-target pairs per forward pass

### Memory

| Component | Per User | Notes |
|-----------|----------|-------|
| Behavior (200 × 64) | ~50 KB | Embedding lookup |
| GRU states (200 × 128) | ~100 KB | Can recompute |
| Attention weights (200) | ~0.8 KB | On-the-fly |

For 100M users, store only latest N items; recompute GRU states or use session-level interest.

### A/B Testing Insights

- DIN: 1–3% CTR lift over non-attention baselines
- DIEN: additional 0.5–1.5% over DIN on temporally-rich data
- For short sequences (< 10 items), simpler models suffice
- Benefit of DIEN increases with sequence length

### Monitoring

- Attention weight distribution (should not be uniform or concentrated on first/last)
- GRU hidden state norms (vanishing/exploding = training issues)
- Attention entropy (too low = over-concentrated; too high = under-informative)
- Prediction latency P50/P95/P99

---

## Summary

DIN introduces target-aware attention to capture diverse user interests per prediction. DIEN extends this with GRU-based interest extraction and AUGRU for temporal evolution modeling. Both achieve significant CTR improvements in e-commerce. Production challenges center on GRU serving latency (addressable via pre-computation and caching) and managing long behavior sequences through truncation or subsampling.
