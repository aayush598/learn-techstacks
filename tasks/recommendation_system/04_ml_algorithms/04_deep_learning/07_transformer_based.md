# Transformer-Based Recommendation Models

## Overview

Transformer architectures, originally designed for natural language processing, have been adapted for sequential recommendation by modeling user interaction histories as sequences. Self-attention mechanisms enable these models to capture long-range dependencies, complex preference patterns, and temporal dynamics without the sequential processing constraints of RNNs. This document covers the foundational concepts, key architectures, training strategies, and production considerations for transformer-based recommender systems.

---

## Self-Attention for Interaction Sequences

### Mechanism

Self-attention computes a weighted representation of all items in a user's interaction history, where the weight between any two items depends on their relevance to each other.

Given a sequence of item embeddings `[x₁, x₂, ..., xₙ]`:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

Where:
- **Q (Query)**: Current item or position being predicted
- **K (Key)**: All items in the sequence that could provide context
- **V (Value)**: Information carried from each item to the representation

### Why Self-Attention for Recommendations

| Property | Benefit |
|----------|---------|
| Global context | Each item attends to all others regardless of distance |
| Parallel computation | Processes all positions simultaneously (unlike RNNs) |
| Dynamic weighting | Attention weights adapt per query position |
| Interpretability | Attention weights reveal which past items influenced the prediction |
| Variable-length handling | Padding masks allow variable-length sequences |

### Multi-Head Attention

Multiple attention heads capture different types of relationships:

- **Head 1**: May learn category-based affinity (user prefers sci-fi items when sci-fi is in history)
- **Head 2**: May learn temporal patterns (recent items matter more)
- **Head 3**: May learn diversity patterns (avoid recommending same type repeatedly)

```
MultiHead(Q, K, V) = Concat(head₁, ..., head_h) × W^O
where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

Typical configuration: 2–8 attention heads with `d_k = d_model / h`.

---

## Positional Encoding for Sequences

### Why Positional Encoding Matters

Self-attention is permutation-invariant — it treats the input as a set, not a sequence. For recommendations, order matters: the most recent interaction is typically more predictive than older ones.

### Encoding Strategies

#### Absolute Positional Encoding

**Sinusoidal (fixed):**
```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```
- Does not require training
- Generalizes to unseen sequence lengths
- Assumes position information is smooth and periodic

**Learned (trainable):**
- Embedding table mapping position index → vector
- Model learns position-specific representations during training
- Typically outperforms sinusoidal for fixed-length sequences
- Cannot generalize beyond trained maximum length

#### Relative Positional Encoding

Instead of absolute positions, encode the relative distance between items:

**Shaw et al. (2018):**
- Add relative position embeddings to attention computation
- `Attention(i, j) = softmax((q_i × k_j + q_i × r_{i-j}) / √d_k) × v_j`
- `r_{i-j}` is a learned embedding for the relative distance `i - j`

**ALiBi (Attention with Linear Biases):**
- Add a linear penalty based on distance: `score += -m × |i - j|`
- No additional parameters; simple and effective
- Naturally biases attention toward nearby items

#### Rotary Position Encoding (RoPE)

- Rotates query and key vectors in 2D subspaces based on position
- Relative position emerges naturally from the rotation: `⟨RoPE(q, i), RoPE(k, j)⟩ = ⟨q, k⟩_relative`
- Used in LLaMA, GPT-NeoX, and many modern transformers
- Supports extrapolation to longer sequences with NTK-aware scaling

### Position Encoding Comparison

| Method | Parameters | Extrapolation | Quality | Compute |
|--------|-----------|---------------|---------|---------|
| Sinusoidal | 0 | Good | Moderate | Negligible |
| Learned | O(L × d) | Poor | Good | Negligible |
| Relative (Shaw) | O(L × d) | Moderate | Very Good | Moderate |
| ALiBi | 0 | Excellent | Good | Negligible |
| RoPE | 0 | Good (with scaling) | Excellent | Low |

---

## Masked Language Modeling for Recommendations

### Concept

Inspired by BERT's masked language model (MLM), this approach randomly masks items in a user's interaction sequence and trains the model to predict the masked items from the surrounding context.

### Training Procedure

1. **Input**: User interaction sequence `[i₁, i₂, i₃, i₄, i₅, i₆, i₇]`
2. **Mask**: Randomly select 15% of items → `[i₁, [M], i₃, [M], i₅, [M], i₇]`
3. **Predict**: Model outputs probability distribution over item vocabulary for each masked position
4. **Loss**: Cross-entropy between predicted and actual masked items

### Masking Strategies

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Random mask | 15% random items | Simple, effective | May mask important items |
| Predict-only mask | Mask last item(s) | Aligns with recommendation task | Less context available |
| Segment mask | Mask contiguous blocks | Tests sequential reasoning | Harder task |
| Time-aware mask | Mask items based on temporal gaps | Captures temporal patterns | Complex implementation |

### Comparison with Predict-Next

| Aspect | Masked LM (Bidirectional) | Predict-Next (Autoregressive) |
|--------|--------------------------|------------------------------|
| Context | Past + future items | Only past items |
| Training efficiency | Parallel (all positions) | Parallel with causal mask |
| Inference | Single forward pass | Can generate sequences |
| Task alignment | Understanding preferences | Predicting next action |
| Borrowed from | BERT | GPT |

---

## Autoregressive vs Bidirectional Models

### Autoregressive (GPT-style)

- Uses causal (triangular) attention mask: each position can only attend to previous positions
- Trained to predict the next item given all previous items
- Naturally suited for sequential prediction tasks

```
Attention mask (autoregressive):
1 0 0 0 0
1 1 0 0 0
1 1 1 0 0
1 1 1 1 0
1 1 1 1 1
```

**Advantages:**
- Matches the recommendation task (predict next item from history)
- Can generate diverse recommendation sequences
- Naturally handles causal inference

**Disadvantages:**
- Each position sees different context (computation not fully parallelizable in inference)
- Cannot leverage future context (which may contain useful signals)

### Bidirectional (BERT-style)

- Uses no attention mask (or padding mask only): every position can attend to every other position
- Trained to predict masked items given the full surrounding context

```
Attention mask (bidirectional):
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
```

**Advantages:**
- Full context available for every position
- Better representation learning for item embeddings
- Can capture both past and future influence on preferences

**Disadvantages:**
- Not directly predicting the next item (requires adaptation for recommendation)
- Training/inference asymmetry (trained bidirectional, used for next-item prediction)

### Prefix-LM (Hybrid)

- Uses a bidirectional mask for a prefix (context) and causal mask for the suffix (prediction)
- Combines bidirectional understanding with autoregressive generation
- T5 and UniLM use this pattern

### Practical Recommendation

- **Representation learning**: Bidirectional models produce richer item embeddings
- **Next-item prediction**: Autoregressive models are more natural
- **Both**: Many systems use bidirectional for embedding pre-training, autoregressive for fine-tuning

---

## Key Architectures

### SASRec (Self-Attentive Sequential Recommendation)

#### Architecture

```
Input: [i₁, i₂, ..., iₙ] (item ID embeddings + positional embeddings)
         ↓
Layer 1: Multi-Head Self-Attention + Layer Norm + FFN
         ↓
Layer 2: Multi-Head Self-Attention + Layer Norm + FFN
         ↓
...
         ↓
Layer L: Output → Point-wise prediction over all items
```

#### Key Design Choices

- **Causal masking**: Autoregressive (lower triangular mask)
- **Position encoding**: Learned positional embeddings
- **Embedding**: Item embedding + positional embedding (element-wise addition)
- **Prediction**: Dot product between final hidden state and item embedding matrix
- **Regularization**: Dropout on embeddings, attention weights, and hidden states

#### Training

- Binary Cross-Entropy loss (BPR-style) or Cross-Entropy loss over all items
- Negative sampling: Random negative items not in user's history
- Point-wise: Predict whether user will interact with each item

#### Hyperparameters (Typical)

| Parameter | Value Range | Notes |
|-----------|------------|-------|
| Number of layers | 1–3 | More layers = more capacity |
| Hidden dimension | 50–256 | Match embedding dimension |
| Number of heads | 1–4 | 2–4 for short sequences |
| Max sequence length | 50–200 | Truncate or pad user histories |
| Dropout rate | 0.1–0.3 | Higher for small datasets |
| Learning rate | 1e-4–1e-3 | Adam optimizer |

### BERT4Rec (BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations)

#### Architecture

- Based on BERT architecture (bidirectional self-attention)
- Uses Cloze task: mask items in sequence, predict masked items

#### Key Differences from SASRec

| Aspect | SASRec | BERT4Rec |
|--------|--------|----------|
| Attention | Causal (unidirectional) | Bidirectional |
| Training objective | Next-item prediction | Masked item prediction |
| Context utilization | Past items only | Full sequence context |
| Inference | Direct next-item | Masked position prediction |
| Position encoding | Learned | Learned (absolute) |

#### Training Details

- **Masking**: 15% of items (same as BERT)
  - 80% replaced with [MASK] token
  - 10% replaced with random item
  - 10% kept unchanged
- **Candidate items**: For each masked position, predict over all items (or sampled subset)
- **Loss**: Cross-entropy over item vocabulary

#### Advantages over SASRec

- Bidirectional context captures richer patterns
- Better performance on datasets with long-range dependencies
- [CLS] token provides a global sequence representation

#### Disadvantages

- Training-inference mismatch (masked items during training, not during inference)
- More computationally expensive than unidirectional models
- [MASK] token doesn't exist during inference (requires adaptation)

### Transformers4Rec (Transformer-based Sequential Recommendation)

#### Overview

A modular framework by NVIDIA for building transformer-based recommender systems, built on Hugging Face Transformers.

#### Key Features

- **Flexible architecture**: Supports GPT, BERT, XLNet, and custom architectures
- **Multi-feature support**: Handles categorical, numerical, and text features
- **Integration with NVTabular**: End-to-end GPU-accelerated pipeline
- **Mixed-precision training**: FP16 for faster training

#### Architecture Components

1. **Input block**: Embedding layers for categorical features + projection for numerical features
2. **Transformer block**: Configurable transformer (GPT-2, BERT, XLNet)
3. **Pooling block**: Session pooling or sequence-level pooling
4. **Prediction block**: Multi-class, binary, or regression head

#### Comparison Table

| Feature | SASRec | BERT4Rec | Transformers4Rec |
|---------|--------|----------|-------------------|
| Attention type | Causal | Bidirectional | Configurable |
| Framework | Custom PyTorch | Custom PyTorch | Hugging Face |
| Multi-feature | Item IDs only | Item IDs only | Multiple feature types |
| Production ready | Manual | Manual | NVTabular integration |
| Training efficiency | High | Moderate | High (GPU-optimized) |
| Pre-training support | No | MLM objective | Multiple objectives |

---

## Training Strategies

### Loss Functions

| Loss | Formula | Use Case |
|------|---------|----------|
| Cross-Entropy | `-Σ log(p(target))` | Full vocabulary prediction |
| BPR Loss | `-log σ(score⁺ - score⁻)` | Pairwise ranking |
| InfoNCE | `-log(exp(s⁺/τ) / Σ exp(sⱼ/τ))` | Contrastive learning |
| Sampled Softmax | Cross-entropy over sampled subset | Large vocabulary efficiency |

### Negative Sampling Strategies

- **Random sampling**: Sample items uniformly from the catalog
- **Popularity-weighted sampling**: Sample negatives proportional to popularity (harder negatives)
- **Batch negatives**: Use all non-target items in the batch as negatives (efficient)
- **Hard negative mining**: Sample items similar to the positive but not interacted with

### Regularization Techniques

- **Dropout**: 0.1–0.3 on embeddings, attention, and hidden states
- **Weight decay**: L2 regularization on model parameters (1e-5 to 1e-4)
- **Label smoothing**: Soften target distribution to prevent overconfidence
- **Data augmentation**: Random masking, item dropout, sequence reordering
- **Early stopping**: Monitor validation NDCG; stop when no improvement for K epochs

---

## Scalability Considerations

### Training Efficiency

| Technique | Speedup | Quality Impact |
|-----------|---------|---------------|
| Mixed precision (FP16) | 1.5–3× | Negligible |
| Gradient accumulation | Memory savings | None |
| Flash Attention | 2–4× for long sequences | None (mathematically equivalent) |
| Sparse attention | Sub-quadratic compute | Moderate quality loss |
| Knowledge distillation | Faster training of smaller models | Moderate quality loss |

### Serving Efficiency

- **Pre-compute item embeddings**: Store transformer-derived item embeddings; compute similarity at serving time
- **ONNX export**: Convert PyTorch model to ONNX for optimized inference
- **Quantization**: INT8 quantization for 2–4× speedup with < 1% quality loss
- **KV-cache**: Cache key-value pairs for autoregressive models to avoid recomputation

---

## Evaluation

### Offline Metrics

| Metric | Description | SASRec vs BERT4Rec typical |
|--------|-------------|---------------------------|
| HR@K | Hit Rate in top-K | BERT4Rec slightly better |
| NDCG@K | Normalized Discounted Cumulative Gain | BERT4Rec slightly better |
| MRR | Mean Reciprocal Rank | Comparable |
| Recall@K | Recall in top-K | BERT4Rec better for long sequences |

### Online Metrics

- **CTR**: Click-through rate on recommended items
- **Conversion rate**: Purchase/signup rate
- **Session length**: Engagement duration
- **Return visits**: User retention
- **Diversity**: Intra-list diversity of recommendations

---

## Best Practices

1. **Start with SASRec**: Simple, fast, strong baseline
2. **Sequence length**: 20–50 items covers most user intent; longer sequences add noise
3. **Embedding dimension**: 64–256; match with downstream task requirements
4. **Batch size**: 256–1024 for stable training with contrastive losses
5. **Negative sampling ratio**: 4:1 to 10:1 negatives-to-positives
6. **A/B test thoroughly**: Transformer models may not always outperform simpler baselines on all metrics
7. **Monitor attention patterns**: Verify the model learns meaningful attention (not uniform or degenerate)
