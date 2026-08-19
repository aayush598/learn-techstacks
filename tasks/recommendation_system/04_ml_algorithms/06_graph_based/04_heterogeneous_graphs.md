# Heterogeneous Information Networks for Recommendations

## Overview

Heterogeneous Information Networks (HINs) represent recommendation systems as graphs with multiple node types (users, items, categories, brands, tags) and multiple edge types (purchased, viewed, belongs-to, created-by). Unlike homogeneous graphs (only users and items), HINs capture rich relational structure that provides deeper understanding of user preferences and item characteristics.

---

## Meta-Paths

### What are Meta-Paths?

A meta-path is a sequence of node types and edge types that defines a specific type of relationship between nodes:

| Meta-Path | Node Types | Edge Types | Relationship |
|---|---|---|---|
| **User-Item-User** | U → I → U | purchased → purchased | Users who bought the same items |
| **User-Item-Category-Item** | U → I → C → I | viewed → belongs-to → viewed | Items in the same category |
| **User-Item-Brand-Item** | U → I → B → I | purchased → made-by → purchased | Items from the same brand |
| **User-User-Item** | U → U → I | friends → purchased | Items purchased by friends |
| **Item-User-Item** | I → U → I | purchased → purchased | Co-purchased items |

### Meta-Path Based Similarity

Compute similarity between nodes based on meta-path constrained random walks:

1. **Random walk**: Starting from a node, perform a random walk constrained by the meta-path.
2. **Visit frequency**: Count how often the walk visits each target node.
3. **Similarity**: Nodes visited frequently are similar under that meta-path.

### Meta-Path Selection

Not all meta-paths are equally useful. Selection strategies:

| Strategy | Method | Rationale |
|---|---|---|
| **Manual** | Domain expert selection | Leverages domain knowledge |
| **Automatic** | Learn meta-path importance from data | Adapts to the dataset |
| **Ablation** | Test each meta-path's contribution | Empirical validation |
| **Attention** | Learn soft weights over meta-paths | Flexible, no hard selection |

---

## HAN (Heterogeneous Graph Attention Network)

### Architecture

HAN (Wang et al., 2019) applies attention at two levels:

1. **Node-level attention**: Learn the importance of different neighbors within a meta-path.
2. **Semantic-level attention**: Learn the importance of different meta-paths.

### Node-Level Attention

For each meta-path, compute attention-weighted aggregation:

**z_i^Φ = Σ_{j∈N_i^Φ} α_{ij}^Φ × h_j^Φ**

Where:
- **N_i^Φ**: Neighbors of node i under meta-path Φ.
- **α_{ij}^Φ**: Attention weight for neighbor j.
- **h_j^Φ**: Hidden representation of neighbor j.

### Semantic-Level Attention

Combine representations from different meta-paths:

**Z = Σ_{Φ∈P} β_Φ × z^Φ**

Where β_Φ is the learned importance of meta-path Φ.

### HAN for Recommendations

| Meta-Path | Node-Level Attention | Semantic-Level Attention |
|---|---|---|
| U-I-U | Weights different co-purchasers | Moderate importance |
| U-I-C-I-U | Weights different category paths | High importance (category affinity) |
| U-U-I | Weights different friends | Variable (trust-dependent) |

---

## Relation-Type Aware Models

### R-GCN (Relational GCN)

R-GCN applies separate weight matrices for each relation type:

**h_i^{(l+1)} = σ(Σ_{r∈R} Σ_{j∈N_i^r} (1/|N_i^r|) × W_r^{(l)} × h_j^{(l)} + W_0^{(l)} × h_i^{(l)})**

Where:
- **R**: Set of relation types.
- **N_i^r**: Neighbors of node i via relation r.
- **W_r^{(l)}**: Relation-specific weight matrix.

### HGT (Heterogeneous Graph Transformer)

HGT (Hu et al., 2020) applies transformer-style attention with relation-type specific parameters:

- **Type-specific QKV**: Each node and relation type has its own Query, Key, Value projections.
- **Type-aware attention**: Attention scores depend on both node types and relation types.
- **Message passing**: Messages are type-specific, enabling fine-grained relational modeling.

### Type-Specific Embeddings

| Component | Description |
|---|---|
| **Node type embeddings** | Separate embedding tables per node type (user, item, category) |
| **Edge type embeddings** | Separate transformations per edge type (purchase, view, like) |
| **Type projection** | Project all node types to a shared space for cross-type interactions |
| **Type attention** | Learn which types are most relevant for each prediction |

### Relation-Type Aware Training

| Strategy | Description |
|---|---|
| **Multi-task learning** | Predict multiple relation types simultaneously |
| **Negative sampling per relation** | Sample negatives specific to each relation type |
| **Relation-type weighting** | Weight loss by relation type frequency |
| **Transfer across relations** | Share parameters across similar relation types |

---

## HIN Applications in Recsys

| Application | HIN Structure | Meta-Paths Used |
|---|---|---|
| Movie recommendation | User-Movie-Director-Actor-Genre | U-M-D-M, U-M-A-M, U-M-G-M |
| E-commerce | User-Product-Brand-Category-Seller | U-P-B-P, U-P-C-P, U-P-S-P |
| Academic recommendation | Author-Paper-Venue-Keyword | A-P-A, A-P-V-P, A-P-K-P |
| Content recommendation | User-Author-Topic-Source | U-A-T-A, U-A-S-A |

---

## Scalability of HIN Models

| Challenge | Solution |
|---|---|
| Large number of relation types | Relation sampling, attention-based selection |
| Many meta-paths | Automatic meta-path learning, soft attention |
| High computational cost | Mini-batch training, neighbor sampling |
| Cold start for new types | Transfer learning from existing types |
| Memory for type-specific parameters | Parameter sharing, low-rank approximations |

---

## HIN Construction and Maintenance

### Building a HIN from Recommendation Data

1. **Identify entity types**: Users, items, categories, brands, tags, sellers, locations.
2. **Identify relation types**: Purchase, view, click, like, belongs-to, made-by, located-in.
3. **Extract entities**: NER and entity linking from text data, structured extraction from databases.
4. **Build edges**: Create edges from interaction logs, catalog relationships, and social connections.
5. **Assign features**: Attach feature vectors to each entity (content embeddings, metadata).
6. **Validate**: Check for orphan nodes, missing edges, and data quality issues.

### HIN Maintenance

- **Incremental updates**: Add new entities and edges without rebuilding the entire graph.
- **Edge weighting**: Update edge weights based on interaction recency and frequency.
- **Entity resolution**: Merge duplicate entities (same item listed under different names).
- **Graph pruning**: Remove low-weight edges to reduce noise and computational cost.
- **Version management**: Track graph versions for reproducibility and rollback.

### HIN Quality Metrics

| Metric | Description | Target |
|---|---|---|
| **Connectivity** | Fraction of nodes reachable from any node | > 95% |
| **Edge coverage** | Fraction of expected edges that exist | > 80% |
| **Entity resolution accuracy** | Correctness of entity merging | > 99% |
| **Freshness** | Age of the most recent edge update | < 24 hours |
| **Feature completeness** | Fraction of nodes with complete features | > 90% |

---

## HIN vs. Homogeneous Graph Approaches

| Aspect | Homogeneous Graph | HIN |
|---|---|---|
| **Information richness** | Limited to user-item interactions | Rich multi-type relationships |
| **Cold start** | No signal for new entity types | Content and relation features available |
| **Interpretability** | Latent factors only | Meta-paths provide interpretable reasoning |
| **Computational cost** | Lower (simpler graph) | Higher (multiple types and relations) |
| **Model complexity** | Simpler (uniform message passing) | More complex (type-specific operations) |
| **Scalability** | Easier to scale | Harder due to type diversity |

---

## Open Challenges in HIN for Recsys

- **Dynamic HINs**: Modeling temporal evolution of entity types and relations.
- **Cross-platform HINs**: Integrating data from multiple platforms into a unified HIN.
- **Privacy-preserving HINs**: Learning on HINs without exposing sensitive entity attributes.
- **Few-shot HIN learning**: Adapting to new entity types with very few examples.
- **Explainable HIN recommendations**: Generating natural language explanations from meta-path reasoning.
