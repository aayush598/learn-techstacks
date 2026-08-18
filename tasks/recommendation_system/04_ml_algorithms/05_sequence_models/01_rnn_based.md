# RNN-Based Sequential Recommendations

## Overview

Recurrent Neural Networks (RNNs) and their variants (GRU, LSTM) were among the first deep learning architectures applied to sequential recommendation. They process user interaction histories as ordered sequences, maintaining a hidden state that captures cumulative preference information. While transformer-based models have largely superseded RNNs for long sequences, RNN-based approaches remain relevant for session-based recommendations, real-time processing, and resource-constrained environments.

---

## Vanilla RNN Architecture

### Basic Formulation

```
h_t = tanh(W_hh × h_{t-1} + W_xh × x_t + b_h)
y_t = W_hy × h_t + b_y
```

Where:
- `h_t`: Hidden state at time step t
- `x_t`: Input embedding at time step t (item embedding)
- `y_t`: Output prediction at time step t
- `W_hh`, `W_xh`, `W_hy`: Weight matrices

### Vanilla RNN Limitations

| Problem | Description | Impact on Recommendations |
|---------|-------------|--------------------------|
| Vanishing gradient | Gradients shrink exponentially through time | Cannot learn long-range dependencies |
| Exploding gradient | Gradients grow exponentially | Training instability |
| No memory gating | All information equally weighted | Recent and old items treated the same |
| Sequential processing | Cannot parallelize across time steps | Slow training on long sequences |
| Fixed representation | Same computation for all positions | No focus mechanism |

**Example in recommendations:** A user's interest in "science fiction" from 50 interactions ago gets diluted by 49 subsequent interactions, making it nearly invisible to the model.

---

## LSTM (Long Short-Term Memory)

### Architecture

LSTM introduces three gates and a cell state to control information flow:

```
f_t = σ(W_f × [h_{t-1}, x_t] + b_f)          # Forget gate
i_t = σ(W_i × [h_{t-1}, x_t] + b_i)          # Input gate
c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c)       # Candidate cell state
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t              # Cell state update
o_t = σ(W_o × [h_{t-1}, x_t] + b_o)          # Output gate
h_t = o_t ⊙ tanh(c_t)                         # Hidden state
```

### Gate Functions for Recommendations

| Gate | Function | Recommendation Analogy |
|------|----------|----------------------|
| Forget gate | Controls what to discard from memory | Forget outdated preferences |
| Input gate | Controls what new information to store | Incorporate new item signals |
| Cell state | Long-term memory | Persistent user interests |
| Output gate | Controls what to expose | Relevant preferences for current prediction |

### LSTM Cell State as Preference Memory

The cell state acts as a persistent memory of user preferences:
- **High cell state values**: Strong, persistent preferences (e.g., always likes horror movies)
- **Forget gate activation**: Forgetting when preferences shift (e.g., stopped liking a genre)
- **Input gate activation**: Learning new preferences from recent interactions

---

## GRU (Gated Recurrent Unit)

### Architecture

GRU simplifies LSTM by merging the forget and input gates into an update gate:

```
z_t = σ(W_z × [h_{t-1}, x_t] + b_z)          # Update gate
r_t = σ(W_r × [h_{t-1}, x_t] + b_r)          # Reset gate
h̃_t = tanh(W_h × [r_t ⊙ h_{t-1}, x_t] + b_h) # Candidate hidden state
h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t        # Hidden state update
```

### GRU vs LSTM Comparison

| Aspect | GRU | LSTM |
|--------|-----|------|
| Parameters | Fewer (~3 parameter groups) | More (~4 parameter groups) |
| Gates | 2 (update, reset) | 3 (forget, input, output) |
| Cell state | No separate cell state | Dedicated cell state |
| Training speed | Faster | Slower |
| Memory usage | Lower | Higher |
| Long sequences | Moderate performance | Better performance |
| Recommendation quality | Comparable for short sequences | Better for long histories |

---

## GRU4Rec Architecture

### Pioneering Work

GRU4Rec (Hidasi et al., 2016) was the first to apply RNNs to session-based recommendations, establishing the paradigm for deep sequential recommendation.

### Architecture

```
Session interactions: [i₁, i₂, ..., iₙ]
         ↓
Embedding layer: [e₁, e₂, ..., eₙ]  (item embeddings, dimension d)
         ↓
GRU layer: [h₁, h₂, ..., hₙ]  (hidden states, dimension d)
         ↓
Output layer: h_n → softmax over items → P(i_{n+1} | i₁, ..., iₙ)
```

### Training with BPR Loss

GRU4Rec introduced using ranking-aware loss functions instead of cross-entropy:

**BPR (Bayesian Personalized Ranking) Loss:**
```
L = -Σ log(σ(r̂_u,i⁺ - r̂_u,i⁻))
```

Where:
- `r̂_u,i⁺`: Score for the positive (next) item
- `r̂_u,i⁻`: Score for a randomly sampled negative item
- `σ`: Sigmoid function

**Extended Loss with Multiple Negatives:**
```
L = -Σ log(exp(r̂_u,i⁺) / (exp(r̂_u,i⁺) + Σ_j exp(r̂_u,i⁻ⱼ)))
```

This is equivalent to a softmax over the positive item and all negatives.

### GRU4Rec Variants

| Variant | Year | Key Innovation |
|---------|------|----------------|
| GRU4Rec (original) | 2016 | First RNN-based session recommender |
| GRU4Rec+ | 2017 | Improved loss functions (BPR, TOP1) |
| GRU4Rec++ | 2018 | Better negative sampling, layer normalization |
| Minimal GRU4Rec | 2019 | Simplified architecture, competitive results |

### Training Loss Comparison

| Loss Function | Formula | Properties |
|--------------|---------|------------|
| BPR | `-log(σ(pos - neg))` | Pairwise ranking; good for implicit feedback |
| TOP1 | `σ(neg - pos) + regularization` | Approximates rank; includes regularization |
| TOP1-MDD | Modified TOP1 | Better approximation with multiple negatives |
| Sampled Softmax | Cross-entropy over sampled items | Scales well; commonly used |

---

## Session-Based Recommendations

### What Are Sessions?

A session is a sequence of interactions (views, clicks, purchases) within a bounded time window, typically representing a single visit or intent.

**Characteristics:**
- No user identity (anonymous browsing)
- Short sequences (5–50 interactions)
- Single intent or evolving intent
- No long-term history available

### RNN for Session-Based Recs

```
Session: [item₁, item₂, ..., itemₖ]
         ↓
GRU: h₁ → h₂ → ... → hₖ
         ↓
hₖ → Prediction layer → Next item scores
```

**Key adaptations:**
- Reset hidden state at session boundaries
- Use dropout between sessions
- Shorter maximum sequence length (20–50 items)
- Faster training cycles (sessions are abundant)

### Session Features

| Feature | Description | Impact |
|---------|-------------|--------|
| Session length | Number of interactions | Longer = more signal |
| Time between interactions | Inter-action intervals | Speed indicates intent strength |
| Time of day | When session occurred | Context for preferences |
| Entry point | First item in session | Determines initial hidden state |
| Device type | Mobile/desktop | Different browsing behaviors |

---

## Handling Variable-Length Sequences

### Padding

- Pad shorter sequences to a fixed length with a special [PAD] token
- Use padding masks in the RNN to ignore padded positions
- Choose `max_length` based on the 90th–95th percentile of sequence lengths

### Packing

- Pack variable-length sequences into a single tensor
- More memory-efficient than padding
- PyTorch: `pack_padded_sequence` and `pad_packed_sequence`
- Avoids computing hidden states for padded positions

### Truncation Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Head truncation | Keep last N items | Most recent behavior is most relevant |
| Tail truncation | Keep first N items | Session start matters (e.g., search intent) |
| Sliding window | Multiple windows per sequence | Maximize training examples |
| Importance-based | Keep most "important" items | Requires importance scoring |

### Bucketing

- Group sequences of similar length together
- Reduces padding waste within each batch
- Dynamic batching: adjust batch composition per training step
- Typical: 5–10 buckets covering the sequence length distribution

---

## Training with BPR Loss

### BPR Formulation

The core idea: for each user, a positive item should score higher than a negative item:

```
P(i⁺ > i⁻ | u) = σ(score(u, i⁺) - score(u, i⁻))
```

The BPR objective maximizes the AUC:

```
L_BPR = -Σ_{(u, i⁺, i⁻)} log σ(score(u, i⁺) - score(u, i⁻))
```

### Negative Sampling for BPR

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Random | Uniform sampling from catalog | Simple, unbiased | Easy negatives, slow learning |
| Popularity-weighted | Sample proportional to popularity | Harder negatives | May over-represent popular items |
| Batch-based | Use other items in batch as negatives | Efficient, many negatives | Depends on batch composition |
| Hard negative | Sample from similar items to positive | Most informative | Risk of false negatives |
| Curriculum | Start easy, increase difficulty | Stable training | Complex scheduling |

### BPR vs Cross-Entropy

| Aspect | BPR Loss | Cross-Entropy |
|--------|---------|---------------|
| Target | Pairwise ranking | Point-wise classification |
| Negatives | Explicit sampled negatives | All non-target items |
| Gradient | Only updates for positive-negative pairs | Updates for all items |
| Scalability | Better with large catalogs | Computationally expensive |
| Calibration | Less calibrated probabilities | Better calibrated |
| Convergence | Slower (fewer gradient updates) | Faster (more gradient updates) |

### Practical BPR Training

- **Negative:positive ratio**: 4:1 to 10:1 works well empirically
- **In-batch negatives**: Treat all non-target items in the batch as negatives (most efficient)
- **Temperature scaling**: Apply temperature to logits before softmax for sharper distributions
- **Hard negative re-sampling**: Periodically resample negatives using the current model to find harder negatives

---

## Multi-Stage RNN Architectures

### Two-Tower with RNN

```
User Tower: RNN over interaction history → user embedding
Item Tower: Embedding lookup → item embedding
Score: dot product(user_emb, item_emb)
```

- User tower captures sequential preference evolution
- Item tower can process content features through additional layers
- Enables pre-computation of item embeddings for fast serving

### Hierarchical RNN

```
Session-level: GRU processes interactions within a session → session embedding
User-level: GRU processes session embeddings across sessions → user embedding
Prediction: user embedding → next item
```

Captures both within-session patterns and cross-session preference evolution.

### Attention-Augmented RNN

```
RNN hidden states: [h₁, h₂, ..., hₙ]
         ↓
Attention: α_i = softmax(v^T tanh(W_a × h_i))
Context: c = Σ α_i × h_i
Prediction: c → next item
```

Adds interpretability and allows the model to focus on the most relevant parts of the history.

---

## RNN vs Transformer Comparison

| Aspect | RNN/GRU | Transformer |
|--------|---------|-------------|
| Sequential computation | Yes (cannot parallelize) | No (parallelizable) |
| Long-range dependencies | Weak (vanishing gradients) | Strong (direct attention) |
| Memory per sequence | O(d) constant | O(n²) attention matrix |
| Inference latency | O(1) per step | O(n) per step (without KV-cache) |
| Training speed | Slower (sequential) | Faster (parallel) |
| Variable-length handling | Natural | Requires masking |
| Session-based recs | Excellent | Good (may be overkill) |
| Long history recs | Weak | Excellent |

---

## Production Deployment

### Real-Time Inference

- Maintain running hidden state per active session
- Update hidden state incrementally with each new interaction
- Generate next-item predictions in O(d²) per step
- Flush hidden state when session expires

### Model Serving Patterns

```
Request (new interaction) →
  Load session hidden state from cache →
  Run single GRU step →
  Get top-K predictions →
  Store updated hidden state to cache →
  Return recommendations
```

### Caching Strategy

| Data | Storage | TTL | Size per session |
|------|---------|-----|-----------------|
| Hidden state | Redis/Memcached | Session timeout | 256–512 bytes (d=256, float32) |
| Recent items | Redis | Session timeout | ~200 bytes (20 item IDs) |
| Embeddings | In-memory | Model lifetime | Pre-loaded in serving process |

### Latency Budget

- Embedding lookup: < 1ms
- GRU forward pass: < 5ms
- Top-K selection: < 2ms
- Cache read/write: < 2ms
- **Total**: < 10ms per prediction request

---

## Lessons Learned and When to Use RNNs

### Use RNNs When:

- Sessions are short (< 30 interactions)
- Real-time, incremental processing is needed
- Resource constraints limit model size
- Interaction latency is critical (< 10ms)
- Session-based recommendations without user accounts

### Consider Alternatives When:

- User histories are long (> 100 interactions) → Use transformers
- Rich content features need complex modeling → Use attention-based models
- Training data is very large → Transformers scale better with data
- Interpretability of attention patterns is needed → Transformers provide explicit attention weights
