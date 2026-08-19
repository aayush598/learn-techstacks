# Session-Based Recommendations

## Overview

Session-based recommendations generate suggestions based on the current user session rather than long-term history. This is critical for anonymous users (no login), first-time visitors, and contexts where short-term intent dominates over long-term preferences. Session-based models process a sequence of interactions within a single session and predict the next action.

---

## GRU4Rec

### Architecture

GRU4Rec (Hidasi et al., 2016) was the first RNN-based model for session-based recommendations:

1. **Input**: Sequence of item interactions within a session (item IDs, optionally with features).
2. **GRU layer**: Process the sequence with a GRU network.
3. **Output layer**: Score all items in the catalog using the final hidden state.
4. **Loss functions**: Session-based variants of ranking losses.

### Loss Functions

| Loss | Formula | Characteristics |
|---|---|---|
| **BPR** | -ln σ(score_pos - score_neg) | Pairwise, one negative sample |
| **TOP1** | σ(score_neg - score_pos) + σ(score_neg²) | Approximation of full ranking |
| **TOP1-Multiple negatives** | Use multiple negative samples | More stable training |
| **Cross-entropy** | -log(softmax(score_pos)) | Full vocabulary softmax (expensive) |

### GRU4Rec Improvements Over Time

| Version | Year | Key Improvement |
|---|---|---|
| GRU4Rec | 2016 | First RNN for session-based recs |
| GRU4Rec+ | 2017 | Improved loss functions (TOP1-Multiple) |
| GRU4Rec (original v2) | 2018 | Better training tricks, data augmentation |

### Session-Level Features

| Feature | Description | Impact |
|---|---|---|
| Session length | Number of items in the session | Longer sessions have more context |
| Session time span | Duration from first to last interaction | Indicates engagement level |
| Inter-item time gaps | Time between consecutive interactions | Indicates browsing speed/intent |
| Session outcome | Purchase, add-to-cart, bounce | Labels for supervised learning |
| Referral source | How the user entered the site | Context for intent inference |

---

## STAMP (Short-Term Attention/Memory Priority)

### Architecture

STAMP (Song et al., 2018) combines attention mechanisms with a memory network:

1. **Long-term memory**: User's historical preferences (global interest).
2. **Short-term memory**: Current session's interactions (session interest).
3. **Attention mechanism**: Weights the importance of each historical item relative to the current session.
4. **Output**: Combines long-term and short-term interests for prediction.

### Key Innovation

STAMP explicitly models the interaction between long-term and short-term interests:

**Attention weight**: α_i = softmax(f(h_i, s_T))

Where h_i is the long-term memory (historical item embeddings) and s_T is the short-term memory (current session state).

### STAMP vs. GRU4Rec

| Aspect | GRU4Rec | STAMP |
|---|---|---|
| Memory | Hidden state only | Explicit long-term and short-term memory |
| Attention | None (GRU gates only) | Explicit attention over history |
| Interpretability | Low (hidden state is opaque) | Higher (attention weights are interpretable) |
| Training complexity | Lower | Moderate |
| Performance | Good | Better for sessions with long history |

---

## NARM (Neural Attentive Session-Based Recommendation)

### Architecture

NARM (Li et al., 2017) uses an RNN encoder with an attention mechanism:

1. **RNN encoder**: Process the session sequence with a GRU.
2. **Attention mechanism**: Compute attention weights over all hidden states.
3. **Global representation**: Weighted sum of hidden states using attention weights.
4. **Local representation**: Final hidden state of the GRU.
5. **Combined representation**: Concatenate global and local representations.
6. **Prediction**: Score all items using the combined representation.

### Attention in NARM

**Attention weight**: α_k = q^T tanh(W_a h_k)

Where:
- h_k: Hidden state at position k.
- W_a, q: Learned attention parameters.

The attention mechanism identifies which items in the session are most influential for the next prediction.

### NARM Design Choices

| Choice | Value | Rationale |
|---|---|---|
| **RNN type** | GRU | Faster training, competitive with LSTM |
| **Attention type** | Additive (Bahdanau) | Simple, effective |
| **Representation** | Global + Local concatenation | Captures both overall session intent and recent momentum |
| **Loss** | Cross-entropy with negative sampling | Standard for large item vocabularies |

---

## Session Partitioning

### Why Partition?

User sessions must be properly defined before modeling. Poor session boundaries lead to mixed intents and degraded recommendation quality.

### Partitioning Strategies

| Strategy | Rule | Use Case |
|---|---|---|
| **Time-based** | Split after 30 min inactivity | General web browsing |
| **Action-based** | Split on specific actions (logout, purchase) | E-commerce |
| **Page-type** | Split when navigating between categories | Content sites |
| **Fixed window** | Fixed 1-hour or 24-hour windows | Simple implementation |
| **Adaptive** | Learn optimal boundaries from data | Complex, high-value applications |

### Session Boundary Detection

Advanced approaches learn session boundaries from data:

- **Predict the next interaction type**: If the model predicts a "new session" action, split the sequence.
- **Time-gap modeling**: Model inter-item time gaps explicitly and let the model learn when gaps indicate session breaks.
- **Graph-based**: Build a session graph and detect natural breaks using community detection.

### Session Features

| Feature | Description | Use |
|---|---|---|
| Session start time | When the session began | Time-of-day patterns |
| Entry page | First item/page in the session | Intent signal |
| Referral source | How the user arrived | Context (search, ad, direct) |
| Device type | Mobile, desktop, tablet | Behavioral patterns |
| Geographic location | User's location | Local preferences |
| Session depth | Items viewed so far | Engagement level |

---

## Handling Short vs. Long Sessions

### Short Sessions (< 5 interactions)

**Challenges:**
- Limited context for preference inference.
- High noise-to-signal ratio.
- May represent exploration rather than intent.

**Strategies:**
- Rely more on content features (item attributes, categories).
- Use popularity-based fallback for the first 1–2 items.
- Incorporate contextual features (time, device, referral) to compensate.
- Use session-level features (entry page, referral) as additional signals.

### Long Sessions (> 50 interactions)

**Challenges:**
- Session may contain multiple sub-intents (browsing different categories).
- RNN/LSTM may struggle with very long sequences (vanishing gradients).
- Older interactions may be less relevant.

**Strategies:**
- Split long sessions into sub-sessions based on time gaps or topic shifts.
- Use attention mechanisms to focus on relevant parts of the session.
- Apply temporal decay to weight recent interactions more heavily.
- Use hierarchical models (item-level → sub-session-level → session-level).

### Adaptive Session Modeling

| Session Length | Model Strategy | Context Weight |
|---|---|---|
| 1–3 items | Content-based + popularity | High (context-driven) |
| 4–20 items | Session-based RNN/Transformer | Medium |
| 20–50 items | Attention-based model | Balanced |
| 50+ items | Hierarchical model with sub-session detection | Lower (diluted context) |

### Cold-Start Sessions

For sessions with only 1–2 interactions:

1. **Context-only**: Use time, device, location, and referral source to infer intent.
2. **Content-based**: Recommend items similar to the one or two items viewed.
3. **Popular items**: Fall back to popularity within the detected category/context.
4. **Progressive refinement**: As the session continues, switch to session-based model predictions.
