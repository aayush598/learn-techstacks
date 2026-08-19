# Markov Chains for Recommendations

## Overview

Markov chains model user behavior as a stochastic process where the next state (item interaction) depends only on the current state (recent interactions). In recommendation systems, Markov chains capture transition patterns—what items users tend to visit after viewing a particular item—providing a simple yet effective sequential recommendation approach.

---

## First-Order Markov Chains

### Model Definition

A first-order Markov chain assumes the next item depends only on the immediately preceding item:

**P(item_{t+1} | item_1, item_2, ..., item_t) = P(item_{t+1} | item_t)**

### Transition Matrix

The transition matrix T has dimensions |I| × |I|, where T_{ij} = P(item_j | item_i):

| | Item A | Item B | Item C | Item D |
|---|---|---|---|---|
| **Item A** | 0.1 | 0.5 | 0.3 | 0.1 |
| **Item B** | 0.2 | 0.1 | 0.4 | 0.3 |
| **Item C** | 0.3 | 0.2 | 0.1 | 0.4 |
| **Item D** | 0.1 | 0.3 | 0.4 | 0.2 |

**Recommendation**: Given the user is currently on item A, recommend items B (0.5), C (0.3), and D (0.1).

### Advantages

- **Simple**: Easy to understand, implement, and debug.
- **Fast inference**: O(K) per recommendation where K = top-K similar items.
- **Interpretable**: Transition probabilities are intuitive ("users who viewed A are 50% likely to view B").
- **Temporal**: Captures sequential patterns that static CF misses.

### Limitations

- **Memoryless**: Ignores all history beyond the immediate predecessor. A user's 10-item browsing history is reduced to just the last item.
- **Sparse transitions**: Many item pairs have zero co-occurrence, leading to zero transition probabilities.
- **No personalization**: All users share the same transition matrix. Different users viewing the same item get the same recommendations.
- **Cold start**: New items have no transition data.

---

## Higher-Order Markov Chains

### Second-Order Markov Chains

The next item depends on the last two items:

**P(item_{t+1} | item_1, ..., item_t) = P(item_{t+1} | item_{t-1}, item_t)**

This captures patterns like "users who viewed A then B are likely to view C" (but users who viewed D then B are likely to view E).

### N-th Order Markov Chains

Generalizing to order N:

**P(item_{t+1} | item_1, ..., item_t) = P(item_{t+1} | item_{t-N+1}, ..., item_t)**

### Order Selection

| Order | State Space | Transition Matrix Size | Pattern Capture |
|---|---|---|---|
| 1 | |I| | |I| × |I| | Immediate transitions |
| 2 | |I|² | |I|² × |I| | Short-term context |
| 3 | |I|³ | |I|³ × |I| | Medium-term context |
| N | |I|^N | |I|^N × |I| | Long-term context |

**Tradeoff**: Higher order captures more context but exponentially increases the state space, leading to severe sparsity. In practice, orders 2–3 are optimal for most recommendation tasks.

---

## Matrix Factorization with Transitions

### Combining MF and Markov Chains

Matrix factorization captures static user preferences, while Markov chains capture sequential patterns. Combining them provides both:

**r̂_ui = p_u · q_i^T + f(transitions from item i)**

Where:
- **p_u · q_i^T**: MF component (static preference).
- **f(transitions)**: Markov component (sequential pattern).

### Factorized Personalized Markov Chains (FPMC)

FPMC (Rendle et al., 2010) factorizes the transition tensor to handle high-order transitions efficiently:

**P(item_{t+1} = j | item_t = i, user = u) = v_j^T (v_i ⊙ w_u)**

Where:
- **v_j**: Item embedding for the candidate next item.
- **v_i**: Item embedding for the current item.
- **w_u**: User embedding that personalizes the transition.
- **⊙**: Element-wise product.

### FPMC Properties

| Property | Description |
|---|---|
| **Personalization** | User-specific transition patterns via w_u |
| **Scalability** | O(|I| × k) per recommendation (linear in item count) |
| **Factorization** | Transition tensor factorized to O(k) dimensions per user-item pair |
| **Sequential** | Captures item-to-item transitions |
| **Interpretable** | Embeddings capture latent item and user characteristics |

---

## Limitations of Markov Chains

### Fundamental Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| **Memoryless assumption** | Ignores long-term history | Higher-order chains, MF hybrid |
| **State space explosion** | Higher orders intractable | Factorization (FPMC), approximation |
| **No content features** | Cannot handle new items | Content-augmented Markov chains |
| **Stationarity assumption** | Transition probabilities don't change over time | Time-varying Markov chains |
| **No personalization** | Same transitions for all users | Personalized MF Markov (FPMC) |
| **Sparse data** | Many zero transitions | Smoothing, backoff, regularization |

### When Markov Chains Work Well

- **Short sessions**: Limited history makes the memoryless assumption reasonable.
- **Strong sequential patterns**: Navigation paths, purchase sequences, browsing flows.
- **Large catalogs**: Simple model scales well to millions of items.
- **Real-time serving**: Fast inference enables low-latency recommendations.
- **Baseline establishment**: Good baseline for evaluating more complex models.

### When Markov Chains Are Insufficient

- **Long-term preferences**: User's stable preferences are not captured.
- **Complex patterns**: Non-Markovian patterns (long-range dependencies, conditional transitions).
- **Cold start**: No transitions for new items.
- **Multi-intent sessions**: Users with mixed interests within a session.

---

## Smoothing and Backoff for Sparse Transitions

### Smoothing Techniques

When transition counts are low, raw frequency estimates are unreliable:

| Technique | Description | Use Case |
|---|---|---|
| **Additive smoothing** | Add a constant to all counts | Very sparse data |
| **Jelinek-Mercer** | Interpolate with uniform distribution | Moderate sparsity |
| **Kneser-Ney** | Discount frequent transitions, backoff to lower-order | Language modeling, sequence data |
| **Bayesian smoothing** | Use prior distributions over transitions | Incorporating domain knowledge |

### Backoff Strategies

When higher-order transitions are unavailable, fall back to lower-order estimates:

- **Stupid backoff**: Use frequency ratio from the highest available order without normalization.
- **Katz backoff**: Use discounted higher-order estimates, backoff to lower-order for missing transitions.
- **Interpolation**: Linearly combine estimates from multiple orders: P = lambda_1 * P_1 + lambda_2 * P_2 + lambda_3 * P_3.

### Time-Varying Markov Chains

Standard Markov chains assume stationary transition probabilities, but user behavior evolves:

- **Time-windowed**: Compute transitions only from recent interactions (e.g., last 30 days).
- **Exponentially weighted**: Apply exponential decay to older interactions.
- **Periodic reestimation**: Recompute transition matrices on a regular schedule.
- **Online updating**: Update transition counts incrementally as new interactions arrive.

---

## Markov Chain Serving Architecture

### Online Serving

| Component | Description |
|---|---|
| **Transition matrix store** | Distributed key-value store (Redis) with top-K transitions per item |
| **User state tracker** | Maintains the current session state (last N items viewed) |
| **Candidate scorer** | Looks up transitions for the user's recent items and aggregates scores |
| **Filter and rank** | Applies business rules, deduplication, and diversity constraints |

### Pre-Computation

- **Transition matrix**: Compute offline daily or hourly using batch processing (Spark).
- **Top-K transitions**: For each item, store only the top-K most probable next items.
- **Personalized transitions**: Pre-compute user-specific transition adjustments using FPMC factors.

### Latency Profile

- **Transition lookup**: O(K) where K is the top-K transitions per item.
- **User state update**: O(1) append to session history.
- **Score aggregation**: O(|H| * K) where |H| is the session history size.
- **Total**: Sub-millisecond for typical sessions with proper caching.
