# Graph Neural Networks for Recommendations

## Overview

Graph Neural Networks (GNNs) model the relational structure of recommendations by operating on graph representations of user-item interactions. Traditional CF treats users and items independently; GNNs leverage graph structure to propagate information across nodes, capturing high-order connectivity patterns (e.g., "user A liked item B, also liked by user C, who liked item D") invisible to shallow methods.

---

## Graph Construction

### User-Item Bipartite Graph

| Component | Description |
|-----------|-------------|
| Nodes | Users (U) ∪ Items (I) |
| Edges | Interactions (clicks, purchases, ratings) |
| Edge weight | Interaction frequency or strength |

| Edge Type | Signal Strength |
|-----------|----------------|
| Click | Weak interest |
| Purchase | Strong intent |
| Rating (1–5) | Explicit preference |
| Add to cart | Consideration |

### Knowledge Graph Integration

Adds semantic relationships: `Movie → directed_by → Director → born_in → City`. Benefits: rich side information for cold-start, semantic similarity, explainable recommendations via knowledge paths.

---

## GCN (Graph Convolutional Network)

### Spatial Formulation

```
H^{(l+1)} = σ(D̃^{-1/2} × Ã × D̃^{-1/2} × H^{(l)} × W^{(l)})
```

Where Ã = A + I (adjacency with self-loops), D̃ = degree matrix, W^(l) = learnable weights.

### Message Passing

For node v: `h_v^{(l+1)} = σ(W × Σ_{u ∈ N(v) ∪ {v}} h_u^{(l)} / √(|N(v)| × |N(u)|))`

### GCN Layers for CF

| Layer | Pattern | Information |
|-------|---------|-------------|
| 1 | User ↔ Item (direct) | Direct preferences |
| 2 | User ↔ User ↔ Item | Similar users also liked... |
| K | K-hop neighborhood | High-order CF signals |

### Over-Smoothing

As K increases, all embeddings converge (over-smoothing). Practical limit: 2–3 layers.

**Mitigations**: Use 1–2 layers (LightGCN), residual connections, DropEdge, PairNorm.

---

## GraphSAGE: Inductive Learning

Learns aggregation functions (not fixed embeddings), enabling inductive learning for new nodes.

```
h_v^{(l+1)} = σ(W × CONCAT(h_v^{(l)}, AGG({h_u^{(l)} : u ∈ S_N(v)})))
```

| Aggregator | Formula | Properties |
|-----------|---------|-----------|
| Mean | `mean({h_u})` | Smooth, simple |
| Pool | `MAX({ReLU(W × h_u + b)})` | Captures salient features |
| LSTM | `LSTM(shuffle({h_u}))` | Expressive, order-sensitive |

Sample K neighbors per node at each layer; fan-out manages total computation.

### GraphSAGE vs GCN

| Aspect | GCN | GraphSAGE |
|--------|-----|-----------|
| Training | Transductive (full graph) | Inductive (sampled subgraphs) |
| New nodes | Requires retraining | Handles natively |
| Scalability | Full graph limited | Scales via sampling |

---

## PinSage: Pinterest's GNN at Scale

| Property | Value |
|----------|-------|
| Nodes | 3 billion (pins + boards) |
| Edges | 18 billion |
| Random walks | 50 walks × 20 steps per node |
| Neighborhood | Top 2000 random-walk neighbors |
| GCN layers | 2 |
| Embedding dim | 256 |

**Key innovations**: Random walk-based neighborhood (captures more meaningful connections than raw adjacency), curriculum learning (easy → hard negatives), MapReduce inference for billion-scale graphs.

---

## LightGCN: Simplified GCN for CF

Removes feature transformation and non-linear activation — only neighborhood aggregation with normalization.

```
h_u^{(l+1)} = Σ_{i ∈ N_u} (1/√(|N_u| × |N_i|)) × h_i^{(l)}
Final: h_u = Σ_{l=0}^{L} α_l × h_u^{(l)}  (learnable layer weights)
```

**Why it works**: In CF, interaction signal is binary; feature transform adds parameters without improving quality. Core GNN value for CF is purely information propagation.

| Benchmark | NGCF | LightGCN | Improvement |
|-----------|------|----------|-------------|
| Amazon-Book (HR@20) | 0.634 | 0.649 | +2.4% |
| Yelp2018 (HR@20) | 0.647 | 0.664 | +2.6% |
| Gowalla (HR@20) | 0.662 | 0.678 | +2.4% |

---

## NGCF (Neural Graph Collaborative Filtering)

Explicit high-order connectivity through message passing:

```
Message: m_{u→i} = (1/√(|N_u| × |N_i|)) × (W₁ × h_u + W₂ × (h_u ⊙ h_i))
Aggregate: h_i^{(l+1)} = σ(Σ_{u ∈ N_i} m_{u→i})
```

The interaction term `h_u ⊙ h_i` captures how node pairs influence each other. NGCF's additional components introduce more parameters that can overfit; LightGCN (removing these) often performs better.

---

## Message Passing Framework

Unified view across GNN recommendation models:

```
Message: m_{u→i} = f_msg(h_u, h_i, e_{ui})
Aggregate: M_i = AGG({m_{u→i} : u ∈ N_i})
Update: h_i' = f_update(h_i, M_i)
```

| Component | Options | Models |
|-----------|---------|--------|
| Message | Linear, bilinear, attention | GCN, NGCF, GAT |
| Aggregation | Mean, sum, max, attention | GCN, GraphSAGE |
| Update | Concat+transform, residual, GRU | GCN, GAT |
| Normalization | Symmetric D^{-1/2}AD^{-1/2} | GCN, LightGCN |

---

## Neighbor Sampling for Scalability

Full aggregation: O(|E| × d) per layer — infeasible for billion-edge graphs.

| Strategy | Description | Trade-off |
|----------|-------------|-----------|
| Node sampling | K neighbors per node | Fixed computation; variance |
| Edge sampling | P edges per node | Proportional to degree |
| Random walk | Neighborhoods via walks | Structural similarity |
| Importance sampling | Weighted by edge importance | Better quality; complex |

Multi-layer sampling fans out multiplicatively (K₁ × K₂ × ... × K_L). Managed by reducing sample sizes at deeper layers and caching frequently accessed neighborhoods.

---

## Heterogeneous GNNs

Real graphs contain multiple node/edge types (User, Item, Category, Brand + click/purchase/r浏览 edges).

```
h_i^{(l+1)} = Σ_{r ∈ R} Σ_{u ∈ N_i^r} α_r(h_u, h_i) × W_r × h_u
```

Relation-specific attention and transformation functions. Models: KGAT, KGCN, RippleNet for knowledge graph-enhanced recommendations.

---

## GNN Training Challenges

| Challenge | Symptom | Mitigation |
|-----------|---------|------------|
| Over-smoothing | All embeddings similar at depth > 3 | Limit to 1–2 layers; JumpingKnowledge |
| Scalability (> 100M nodes) | OOM, slow training | Cluster-GCN, PinSage, distributed |
| False negatives | Missing edges treated as negatives | Popularity-weighted sampling, confidence edges |
| Cold-start | New nodes with no edges | Use side information; inductive models |

### Scalability by Graph Size

| Size | Strategy | Framework |
|------|----------|-----------|
| < 1M nodes | Full batch GPU | PyTorch Geometric |
| 1M–100M | Neighbor sampling | DGL, PyG |
| > 100M | Cluster-GCN, PinSage | Custom systems |
| > 1B | MapReduce, edge mini-batch | AliGraph, PinSage |

---

## GNN vs Traditional CF

| Aspect | MF | GCN | LightGCN | PinSage |
|--------|-----|-----|----------|---------|
| Interaction | Dot product | Neighborhood agg. | Simplified agg. | Walk agg. |
| High-order CF | No | Yes (K layers) | Yes | Yes |
| Scalability | Excellent | Moderate | Good | Excellent |
| Cold-start | Side info | Graph neighbors | Graph neighbors | Graph neighbors |
| Interpretability | High | Moderate | Low | Low |
| Inference | < 1 ms | 1–5 ms | 1–3 ms | < 1 ms (pre-computed) |

**When to use GNNs**: Graph structure carries strong signal; high-order connectivity matters; cold-start is a concern. **Start with LightGCN**: simplest baseline, often outperforms complex variants.

---

## Summary

GNNs leverage graph structure for high-order collaborative signals. GCN provides foundational aggregation; GraphSAGE enables inductive learning; PinSage scales to billions via random walks and MapReduce; LightGCN demonstrates that simplifying GCN improves CF performance. Key challenges — over-smoothing and scalability — are addressable through depth limits and sampling strategies.
