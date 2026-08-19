# Graph Neural Networks for Recommendations

## Overview

Graph Neural Networks (GNNs) model the user-item interaction graph and auxiliary graphs (social, item similarity, knowledge) to learn node embeddings that capture both collaborative and structural information. GNNs propagate information across graph edges, enabling each node (user or item) to aggregate signals from its neighbors, neighbors' neighbors, and beyond. This captures high-order connectivity patterns that matrix factorization and sequence models cannot.

---

## Message Passing Framework

### Core Concept

GNNs operate through iterative message passing:

1. **Message**: Each node computes a message to send to its neighbors (typically a transformation of its current embedding).
2. **Aggregate**: Each node aggregates messages from its neighbors (sum, mean, max, attention-weighted).
3. **Update**: Each node updates its embedding based on the aggregated messages and its current state.

### Message Passing in Recsys

| Step | User Node | Item Node |
|---|---|---|
| **Message** | User sends preference signal to interacted items | Item sends popularity/quality signal to interacting users |
| **Aggregate** | User aggregates signals from interacted items | Item aggregates signals from interacting users |
| **Update** | User embedding incorporates item neighborhood info | Item embedding incorporates user neighborhood info |

After K rounds of message passing, each node's embedding incorporates information from its K-hop neighborhood.

---

## GCN (Graph Convolutional Networks)

### Spectral GCN

GCN (Kipf & Welling, 2017) applies spectral graph convolutions in the node domain:

**H^{(l+1)} = σ(D̃^{-1/2} Ã D̃^{-1/2} H^{(l)} W^{(l)})**

Where:
- **Ã**: Adjacency matrix with self-loops (A + I).
- **D̃**: Degree matrix of Ã.
- **H^{(l)}**: Node embeddings at layer l.
- **W^{(l)}**: Learnable weight matrix.
- **σ**: Activation function.

### GCN for Recommendations

- **User-item bipartite graph**: Nodes are users and items; edges are interactions.
- **Message propagation**: User embeddings aggregate item embeddings from interacted items, and vice versa.
- **K-layer GCN**: K layers capture K-hop connectivity (K=2–3 is typical).

### Limitations of Vanilla GCN

- **Over-smoothing**: With many layers, all node embeddings converge to the same vector.
- **Transductive**: Requires the full graph at training time; new nodes need retraining.
- **Uniform weighting**: All neighbors contribute equally (no attention).

---

## GraphSAGE

### SAmple and aggreGatE

GraphSAGE (Hamilton et al., 2017) addresses GCN's limitations:

- **Inductive**: Can generate embeddings for unseen nodes using their local neighborhood.
- **Sampling**: Only samples a fixed number of neighbors (instead of using all neighbors).
- **Multiple aggregators**: Supports mean, LSTM, and pooling aggregators.

### GraphSAGE Architecture

1. **Sample neighbors**: For each node, randomly sample K neighbors at each layer.
2. **Aggregate**: Compute the aggregated message from sampled neighbors.
3. **Update**: Combine the node's current embedding with the aggregated message.
4. **Repeat**: Stack L layers for L-hop neighborhood information.

### GraphSAGE for Recsys

| Property | Benefit |
|---|---|
| **Inductive** | New users/items get embeddings without retraining |
| **Sampling** | Scales to large graphs (millions of nodes) |
| **Multiple aggregators** | Different aggregators capture different neighborhood patterns |
| **Feature-rich** | Can incorporate node features (content, metadata) |

---

## PinSage

### Industrial-Scale GNN

PinSage (Ying et al., 2018) was developed at Pinterest for recommendations on a graph with 3 billion nodes and 18 billion edges:

- **Production GNN**: Designed for industrial deployment at scale.
- **Curriculum learning**: Train with increasing neighborhood sizes.
- **Negative sampling**: Uses hard negative mining (random walks to find informative negatives).
- **MapReduce-friendly**: Aggregation is parallelized across the graph.

### PinSage Key Innovations

| Innovation | Description |
|---|---|
| **Constructing convolutions via random walks** | Use random walk visit counts instead of fixed graph structure |
| **Production embedding pipeline** | GNN generates embeddings that are cached and served |
| **Hard negative mining** | Sample negatives that are structurally close to the node |
| **Curriculum training** | Start with small neighborhoods, increase during training |

---

## LightGCN

### Simplified GCN for Recommendations

LightGCN (He et al., 2020) removes non-linear transformations and feature propagation, keeping only neighborhood aggregation:

**e_u^{(l+1)} = Σ_{i∈N(u)} (1/√(|N(u)| × |N(i)|)) × e_i^{(l)}**

### Key Insight

Non-linear activation functions and feature transformations in GCN hurt recommendation performance. Simple linear neighborhood aggregation (weighted by graph structure) is more effective.

### LightGCN Properties

- **Simplicity**: Only neighborhood aggregation, no feature transformation.
- **Symmetry**: User and item embeddings are updated symmetrically.
- **Layer combination**: Final embedding is a weighted sum of embeddings from all layers.
- **Interpretability**: Each layer captures a different hop of connectivity.

### LightGCN vs. GCN

| Aspect | GCN | LightGCN |
|---|---|---|
| Parameters | More (transformation matrices) | Fewer (only aggregation) |
| Training speed | Slower | Faster |
| Performance | Good | Better on recommendation benchmarks |
| Over-smoothing | Severe | Less severe (no non-linearity) |

---

## NGCF (Neural Graph Collaborative Filtering)

### Architecture

NGCF (Wang et al., 2019) applies GCN to the user-item bipartite graph with propagation rules designed for collaborative filtering:

**e_u^{(l+1)} = σ(Σ_{i∈N(u)} (1/√(|N(u)| × |N(i)|)) × (W_1^{(l)} e_i^{(l)} + W_2^{(l)} (e_i^{(l)} ⊙ e_u^{(l)})))**

### NGCF Innovations

- **Message construction**: Includes both a transformation of the neighbor's embedding and a product of the node and neighbor embeddings (capture collaborative signals).
- **Embedding propagation**: Explicitly models how embeddings propagate through the graph.
- **Multi-layer**: Stacks multiple propagation layers for high-order connectivity.

### NGCF vs. LightGCN

NGCF was later shown to be outperformed by the simpler LightGCN, suggesting that the additional complexity (non-linearities, feature transformations) in NGCF may hurt rather than help recommendation performance.

---

## Heterogeneous GNNs

### Heterogeneous Graphs in Recsys

Real recommendation graphs have multiple node and edge types:

| Node Types | Edge Types |
|---|---|
| Users, Items, Authors, Categories, Tags | Purchase, View, Click, Belongs-to, Created-by |

### Heterogeneous GNN Approaches

| Approach | Description | Example |
|---|---|---|
| **Metapath-based** | Aggregate along predefined meta-paths | User → Item → Category → Item |
| **Relation-type specific** | Different GNN weights for different edge types | R-GCN |
| **Attention over types** | Learn attention weights across relation types | HAN, HGT |
| **Type-specific embeddings** | Separate embedding spaces per node type | HERec |

---

## Scalability Challenges

### Scaling GNNs to Industrial Graphs

| Challenge | Solution |
|---|---|
| **Large graph size** | Mini-batch training with neighborhood sampling |
| **High node degree** | Sample neighbors instead of using all |
| **Feature dimension** | Feature hashing, dimensionality reduction |
| **Training time** | Distributed training (DGL, PyG distributed) |
| **Inference latency** | Pre-compute embeddings, cache and serve |

### Mini-Batch Training

Full-batch GNN training requires the entire graph in memory. Mini-batch approaches:

1. **Sample target nodes**: Select a batch of nodes to update.
2. **Sample neighbors**: For each target node, sample K neighbors per layer.
3. **Build computation graph**: Construct the subgraph needed for the batch.
4. **Forward/backward pass**: Compute embeddings and gradients for the batch.
5. **Update**: Apply gradients to the shared model parameters.

### Sampling Strategies

| Strategy | Description | Trade-off |
|---|---|---|
| **Uniform sampling** | Random neighbor selection | Simple, may miss important neighbors |
| **Importance sampling** | Weight by edge importance | Better quality, more complex |
| **Random walk sampling** | Sample via random walks | Captures graph structure |
| **Degree-based sampling** | Oversample high-degree neighbors | Reduces popularity bias |
