# Transformers for Recommendations

## Overview

Transformer architectures, originally designed for natural language processing, have been successfully adapted for sequential recommendation. Their self-attention mechanism captures long-range dependencies without the sequential processing bottleneck of RNNs, enabling parallel training and superior performance on long interaction sequences. Key models include SASRec, BERT4Rec, and Transformers4Rec.

---

## Self-Attention Mechanism

### Multi-Head Self-Attention

Self-attention computes relationships between all items in a sequence simultaneously:

**Attention(Q, K, V) = softmax(QK^T / √d_k) × V**

Where:
- **Q (Query)**: Represents what each item is "looking for."
- **K (Key)**: Represents what each item "offers."
- **V (Value)**: Represents the information each item carries.
- **d_k**: Key dimension (scaling factor to prevent softmax saturation).

### Multi-Head Attention

Multiple attention heads capture different types of relationships:

| Head | Relationship Type | Example |
|---|---|---|
| Head 1 | Sequential adjacency | Item t-1 is relevant to item t |
| Head 2 | Category affinity | Items in the same category attend to each other |
| Head 3 | Price sensitivity | Items in a similar price range attend to each other |
| Head 4 | Long-range dependency | Items from much earlier in the sequence |

**Multi-head output**: Concatenate all head outputs and project: MultiHead = Concat(head_1, ..., head_h) × W^O

### Complexity

Standard self-attention has O(n²) complexity in sequence length n. For recommendation sequences (typically 20–200 items), this is manageable. For very long sequences, sparse attention or linear attention variants can reduce complexity.

---

## Positional Encoding

### Why Positional Encoding?

Self-attention is permutation-invariant—it treats the sequence as a set. Positional encoding injects order information so the model knows that item A appeared before item B.

### Positional Encoding Types

| Type | Description | Advantage |
|---|---|---|
| **Sinusoidal** | Fixed sinusoidal functions of position | No additional parameters, generalizes to unseen lengths |
| **Learned** | Trainable embedding for each position | Captures task-specific positional patterns |
| **Relative** | Encode relative distances between positions | Better generalization to different sequence lengths |
| **Rotary (RoPE)** | Encode position via rotation in embedding space | Efficient, captures relative positions naturally |

### Positional Encoding for Recommendations

Unlike NLP where word order is critical, in recommendations:
- **Position represents recency**: Later positions are more important (recent interactions reflect current intent).
- **Relative position matters more**: The gap between items (in time) is more informative than absolute position.
- **Variable-length sequences**: Users have different history lengths; the model must generalize across lengths.

---

## SASRec (Self-Attentive Sequential Recommendation)

### Architecture

SASRec (Kang & McAuley, 2018) is a self-attentive sequential recommendation model:

1. **Embedding layer**: Map item IDs to dense vectors.
2. **Positional encoding**: Add learned positional embeddings.
3. **Self-attention blocks**: Stack of multi-head self-attention + feed-forward layers with residual connections and layer normalization.
4. **Point-wise prediction**: Use the final hidden state to score all candidate items.

### Key Design Choices

| Choice | SASRec | Rationale |
|---|---|---|
| **Causal masking** | Only attend to past items | Prevents information leakage from future items |
| **Unidirectional** | Left-to-right processing | Matches the prediction task (predict next item) |
| **Position embeddings** | Learned per-position | Captures recency patterns |
| **Output** | Point-wise scoring over all items | Efficient for large item vocabularies |

### SASRec vs. LSTM

| Aspect | LSTM | SASRec |
|---|---|---|
| Parallelization | Sequential (cannot parallelize) | Parallel (all positions processed simultaneously) |
| Long-range dependencies | Limited by gradient flow | Direct attention to any position |
| Training speed | Slower (sequential) | Faster (parallel) |
| Memory | O(n) for hidden states | O(n²) for attention matrix |
| Performance | Good | 5–15% better on standard benchmarks |

---

## BERT4Rec

### Masked Item Prediction

BERT4Rec (Sun et al., 2019) applies BERT's masked language modeling to sequential recommendation:

1. **Input**: Sequence of item IDs (like a sentence of words).
2. **Masking**: Randomly mask a percentage of items in the sequence.
3. **Prediction**: Predict the masked items using bidirectional context.
4. **Training**: Minimize the prediction loss on masked positions.

### Bidirectional Context

Unlike SASRec (unidirectional), BERT4Rec uses bidirectional attention—each item attends to both past and future items in the sequence.

**Advantage**: Future items provide additional context. For example, if a user bought a phone case after a phone, the phone case helps predict the phone was a deliberate purchase.

**Disadvantage**: Not suitable for real-time next-item prediction during an ongoing session (future items are not yet available).

### BERT4Rec Architecture

| Component | Configuration |
|---|---|
| **Embedding** | Item embedding + positional embedding |
| **Attention** | Bidirectional multi-head self-attention |
| **Masking** | 15% of items masked (same as BERT) |
| **Prediction** | Project masked positions to item vocabulary |
| **Loss** | Cross-entropy on masked positions |

---

## Transformers4Rec

### Unified Framework

Transformers4Rec (de Oliveira et al., 2021) provides a modular framework for applying Transformer architectures to sequential recommendation:

- **Flexible input features**: Supports item IDs, categorical features, numerical features, and time features.
- **Multiple attention mechanisms**: Self-attention, causal attention, cross-attention.
- **Multiple training objectives**: Next-item prediction, masked item prediction, future prediction.
- **Integration with NVIDIA Merlin**: Designed for GPU-accelerated training and inference.

### Architecture Components

| Component | Options |
|---|---|
| **Feature processing** | Embedding layers for categorical, normalization for numerical |
| **Sequence modeling** | Transformer blocks with configurable attention type |
| **Masking** | Causal (SASRec-style), masked (BERT4Rec-style), none |
| **Prediction** | Item scoring, next-item classification |
| **Loss** | Cross-entropy, BPR, sample-based softmax |

---

## Masked LM for Recommendations

### Masked Language Modeling Adaptation

The masked LM paradigm adapted for recommendations:

1. **Input sequence**: User interaction history: [item_1, item_2, ..., item_n].
2. **Masking strategy**: Randomly select 15% of positions and replace with a [MASK] token.
3. **Bidirectional context**: Each position attends to all other positions.
4. **Prediction**: Predict the original item at each masked position.

### Masking Strategies

| Strategy | Description | Effect |
|---|---|---|
| **Random masking** | 15% of items randomly masked | Standard BERT approach |
| **Last-k masking** | Mask the last k items | More challenging, tests recent understanding |
| **Diverse masking** | Mask items from different parts of the sequence | Ensures coverage of long-range dependencies |
| **Temporal masking** | Mask items based on time gaps | Emphasizes temporal patterns |

### Training vs. Inference

| Phase | Input | Task |
|---|---|---|
| **Training** | Sequence with masked items | Predict masked items |
| **Inference (next-item)** | Full history (no mask) | Predict the next item |
| **Inference (completion)** | Partial sequence with masks | Fill in missing items |

### Advantages of Masked LM for Recommendations

- **Bidirectional context**: Better understanding of user intent from full sequence context.
- **Denoising objective**: Learning to reconstruct masked items is a form of denoising, which improves robustness.
- **Transfer learning**: Pre-trained models can be fine-tuned for specific recommendation tasks.
- **Multiple predictions**: Can predict multiple masked items simultaneously, enabling batch inference.

### Limitations

- **Training-inference mismatch**: Training uses masked input, inference uses full input (similar to exposure bias in seq2seq).
- **Not autoregressive**: Cannot generate sequences item-by-item (unlike SASRec).
- **Computational cost**: Bidirectional attention is more expensive than unidirectional.
- **Masking hyperparameter**: The masking ratio (15%) may need tuning for recommendation tasks.
