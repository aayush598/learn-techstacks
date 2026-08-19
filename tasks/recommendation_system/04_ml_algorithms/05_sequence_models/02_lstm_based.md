# LSTM-Based Sequential Recommendations

## Overview

Long Short-Term Memory (LSTM) networks are recurrent neural networks (RNNs) designed to learn long-term dependencies in sequential data. In recommendation systems, LSTMs model user behavior as a sequence of interactions, capturing temporal patterns, evolving preferences, and short-term intent that static models (matrix factorization) cannot represent.

---

## LSTM Cells

### Cell Architecture

An LSTM cell contains three gates that control information flow:

| Gate | Function | Formula |
|---|---|---|
| **Forget gate** | Decides what information to discard from the cell state | f_t = σ(W_f · [h_{t-1}, x_t] + b_f) |
| **Input gate** | Decides what new information to store in the cell state | i_t = σ(W_i · [h_{t-1}, x_t] + b_i) |
| **Output gate** | Decides what information to output from the cell state | o_t = σ(W_o · [h_{t-1}, x_t] + b_o) |

**Cell state update**: C_t = f_t * C_{t-1} + i_t * tanh(W_C · [h_{t-1}, x_t] + b_C)

**Hidden state**: h_t = o_t * tanh(C_t)

### Why LSTM for Recommendations

| Capability | Relevance to Recommendations |
|---|---|
| **Long-term memory** | Remember user preferences from weeks/months ago |
| **Short-term adaptation** | Adapt to current session intent |
| **Variable-length sequences** | Handle users with 5 or 500 interactions |
| **Sequential ordering** | Capture the order of interactions (browsing → considering → purchasing) |
| **Missing time gaps** | Gate mechanism handles irregular time intervals |

### LSTM vs. Standard RNN

| Aspect | Standard RNN | LSTM |
|---|---|---|
| Gradient flow | Vanishing/exploding gradients | Stable gradient flow via cell state |
| Long-range dependencies | Poor (10–20 steps) | Good (100+ steps) |
| Training stability | Unstable for long sequences | More stable |
| Parameters | Fewer (k² + kn) | More (4 × (k² + kn)) |
| Recommendation performance | Baseline | 10–30% improvement |

---

## Bidirectional LSTM

### Architecture

A bidirectional LSTM processes the sequence in both directions simultaneously:

- **Forward LSTM**: Processes interactions from oldest to newest (t=1 to t=T).
- **Backward LSTM**: Processes interactions from newest to oldest (t=T to t=1).
- **Combined representation**: Concatenate (or sum) the forward and backward hidden states: h_t = [h_t^forward; h_t^backward].

### Use Cases in Recommendations

| Use Case | Why Bidirectional |
|---|---|
| **Next-item prediction** | Forward context captures preference evolution; backward context captures what items led to the current position |
| **Sequence classification** | Full sequence context for intent classification (e.g., browsing vs. buying) |
| **Session understanding** | Understanding the complete session before making recommendations |

### Limitations

- **Not suitable for real-time**: Requires the full sequence to be available. Cannot make predictions during an ongoing session (only forward LSTM can do that).
- **Higher computational cost**: Two LSTMs instead of one.
- **Overfitting risk**: More parameters with the same amount of training data.

---

## Attention-LSTM

### Attention Mechanism

Attention allows the model to focus on specific items in the history when making predictions:

**Context vector = Σ_t α_t × h_t**

Where α_t = softmax(score(h_t, h_T)) and the score function measures the relevance of each historical hidden state to the current state.

### Types of Attention for LSTM Recommendations

| Attention Type | Description | Advantage |
|---|---|---|
| **Self-attention** | Each item attends to all other items in the sequence | Captures item-item dependencies |
| **User attention** | Items attend to the user's global representation | Personalized attention weights |
| **Temporal attention** | Attention weights decay with time recency | Recency bias for fresh recommendations |
| **Multi-head attention** | Multiple attention heads capture different patterns | Richer representation |

### Attention-LSTM Architecture

1. **LSTM encoder**: Process the interaction sequence with LSTM, producing hidden states h_1, ..., h_T.
2. **Attention layer**: Compute attention weights over all hidden states.
3. **Context vector**: Weighted sum of hidden states using attention weights.
4. **Prediction layer**: Combine context vector with item features to score candidate items.

---

## GRU vs. LSTM

### Gated Recurrent Unit (GRU)

GRU is a simplified variant of LSTM with two gates instead of three:

| Gate | Function |
|---|---|
| **Reset gate** | Controls how much of the previous hidden state to forget |
| **Update gate** | Controls the balance between old and new information |

**GRU equations:**
- z_t = σ(W_z · [h_{t-1}, x_t]) (update gate)
- r_t = σ(W_r · [h_{t-1}, x_t]) (reset gate)
- h̃_t = tanh(W · [r_t * h_{t-1}, x_t]) (candidate)
- h_t = (1 - z_t) * h_{t-1} + z_t * h̃_t

### Comparison

| Aspect | LSTM | GRU |
|---|---|---|
| Parameters | 4 × (k² + kn) | 3 × (k² + kn) |
| Training speed | Slower | 20–30% faster |
| Memory usage | Higher | Lower |
| Long sequences (> 100) | Better | Slightly worse |
| Short sequences (< 50) | Similar | Similar |
| Recommendation quality | Slight edge | Competitive |

**Practical recommendation**: Use GRU for resource-constrained deployments or when training speed is critical. Use LSTM for maximum accuracy with sufficient resources.

---

## Sequence-to-Sequence Recommendations

### Seq2Seq Architecture

An encoder-decoder architecture where:

- **Encoder**: Processes the user's interaction history into a fixed-length representation.
- **Decoder**: Generates the next item(s) in the sequence, one at a time.

### Seq2Seq for Recommendations

| Application | Encoder Input | Decoder Output |
|---|---|---|
| **Next-item prediction** | User history | Single next item |
| **Session recommendation** | Current session items | Next item in session |
| **Sequential top-K** | User history | Top-K recommended items |
| **Code/product recommendation** | Previous actions | Next action/item |

### Teacher Forcing

During training, the decoder receives the ground-truth previous item as input (teacher forcing). During inference, it uses its own predictions as input (autoregressive generation).

**Exposure bias**: The mismatch between training (ground truth) and inference (model predictions) can degrade performance. Mitigation techniques include scheduled sampling (gradually transitioning from teacher forcing to autoregressive) and beam search at inference time.

### Training Sequence Models

| Technique | Purpose |
|---|---|
| **Cross-entropy loss** | Next-item classification |
| **BPR loss** | Pairwise ranking |
| **Negative sampling** | Efficient training with large item vocabularies |
| **Label smoothing** | Prevent overconfident predictions |
| **Scheduled sampling** | Reduce exposure bias |
| **Beam search** | Improve inference quality |
