# Knowledge Graph Embeddings for Recommendations

## Overview

Knowledge Graphs (KGs) represent entities and their relationships as a graph structure, providing rich semantic information about items, users, and their connections. In recommendation systems, KGs bridge the gap between content-based and collaborative approaches by encoding domain knowledge, item relationships, and user preferences as structured, interpretable connections. This document covers knowledge graph construction, embedding techniques, reasoning methods, and production integration patterns.

---

## Knowledge Graph Fundamentals

### Structure

A Knowledge Graph is defined as a set of triples `(head, relation, tail)` or `(h, r, t)`:

```
(movie, genre, sci-fi)
(movie, directed_by, nolan)
(movie, starring, bale)
(user, watched, movie)
(user, prefers, genre)
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| Entity | Node in the graph | Movie, Actor, Genre, User |
| Relation | Typed edge between entities | "directed_by", "belongs_to", "similar_to" |
| Attribute | Entity property | Release year, rating, price |
| Path | Sequence of connected triples | User → watched → Movie → genre → Genre |

### Knowledge Graph Construction for Recommendations

#### Sources

| Source | Type | Entities | Relations |
|--------|------|----------|-----------|
| Product catalogs | Structured | Items, categories, brands | Hierarchical, attribute |
| IMDb / Wikipedia | Semi-structured | Movies, actors, directors | Collaboration, biographical |
| User reviews | Unstructured | Extracted entities, sentiment | Co-occurrence, opinion |
| Social networks | Structured | Users, groups, connections | Social, follow, like |
| Domain ontologies | Structured | All entity types | Formal relationships |

#### Construction Pipeline

1. **Entity extraction**: NER from text (titles, descriptions, reviews)
2. **Relation extraction**: Identify relationships between entities
3. **Entity linking**: Map extracted entities to canonical KG entities
4. **Deduplication**: Merge duplicate entities (same movie, different titles)
5. **Schema alignment**: Map to a unified ontology
6. **Quality assurance**: Validate triples, resolve conflicts

### KG Properties Relevant to Recommendations

- **Heterogeneity**: Multiple entity and relation types
- **Sparsity**: Not all entity pairs are connected
- **Noise**: Extracted triples may be incorrect
- **Dynamism**: New entities and relations added continuously
- **Scale**: Millions of entities, billions of triples

---

## Knowledge Graph Embedding Methods

### TransE (Translating Embeddings)

#### Principle

Model relations as translations in embedding space:

```
h + r ≈ t  (for true triples)
```

The scoring function: `f(h, r, t) = -||h + r - t||_p`

#### Training Objective

Margin-based ranking loss:

```
L = Σ max(0, γ + f(h, r, t) - f(h', r, t'))
```

Where `(h', r, t')` is a corrupted triple (negative sample).

#### Limitations

- Cannot model symmetric relations (e.g., "similar_to") well
- Struggles with 1-to-N and N-to-1 relations
- Assumes all relations are translations (overly simplistic)

### TransR

#### Principle

Embed entities and relations in separate spaces, with a projection matrix per relation:

```
h_r = M_r × h
t_r = M_r × t
f(h, r, t) = -||h_r + r - t_r||
```

- Each relation `r` has its own projection matrix `M_r`
- Entities are projected into relation-specific spaces before comparison
- Better handles relations with different semantics

### RotatE

#### Principle

Model relations as rotations in complex-valued embedding space:

```
h ∘ r ≈ t  (element-wise complex multiplication)
```

Where `r` is a rotation: `|r_i| = 1` for all dimensions.

#### Scoring Function

```
f(h, r, t) = -||h ∘ r - t||
```

#### Advantages

- Can model symmetric, antisymmetric, inverse, and composition relations
- Handles 1-to-N relations better than TransE
- No additional parameters for relation-specific transformations

#### Relation Modeling

| Relation Type | Rotation Angle | Example |
|--------------|---------------|---------|
| Symmetric | θ = π (180°) | "similar_to", "same_as" |
| Antisymmetric | θ ≠ 0, θ ≠ π | "parent_of", "directed_by" |
| Inverse | θ_r2 = -θ_r1 | "watched" vs "watched_by" |
| Composition | θ_r3 = θ_r1 + θ_r2 | "friend_of" ∘ "friend_of" |

### Other Notable Methods

| Method | Principle | Strengths | Weaknesses |
|--------|-----------|-----------|------------|
| DistMult | Bilinear: f = h^T diag(r) t | Simple, effective | Symmetric relations only |
| ComplEx | Complex bilinear | Handles asymmetry | Sensitive to negative sampling |
| ConvE | 2D convolution over embeddings | Captures complex patterns | More parameters, slower |
| R-GCN | Graph neural network on KG | Captures graph structure | Expensive for large KGs |
| CompGCN | Composition-based GCN | Unified relation modeling | Complex implementation |

---

## Path-Based Reasoning

### Concept

Path-based reasoning traverses the knowledge graph from a user entity to item entities through meaningful paths, providing explainable recommendations.

### Path Types

```
User → watched → Movie₁ → directed_by → Director → directed_by_inverse → Movie₂ (recommended)

User → belongs_to → Group → member → User₂ → liked → Item (recommended)

User → prefers → Genre → contains → Movie (recommended)
```

### Path Encoding

#### RNN-Based Path Encoding

- Encode each path as a sequence of (relation, entity) pairs
- Use GRU/LSTM to encode the path into a vector
- Aggregate multiple path encodings for final score

#### Attention-Based Path Encoding

- Compute attention over all paths from user to candidate item
- Weighted sum of path encodings as the recommendation score
- Attention weights provide interpretability (which reasoning path matters most)

### Path Ranking Algorithm (PRA)

1. For each user-item pair, enumerate all paths up to length L
2. Learn a weight for each path type
3. Score = weighted sum of path features
4. Scale to large KGs with random walk path finding

### Meta-Path Guided Reasoning

Define domain-specific meta-paths:

| Domain | Meta-Path | Meaning |
|--------|-----------|---------|
| Movies | User → Movie → Actor → Movie | "Actors you like" |
| Movies | User → Movie → Genre → Movie | "Same genre" |
| E-commerce | User → Product → Brand → Product | "Same brand preference" |
| E-commerce | User → Product → Category → Product | "Category browsing" |
| Books | User → Book → Author → Book | "Author you enjoy" |
| Music | User → Artist → Genre → Artist | "Genre affinity" |

---

## KGAT (Knowledge Graph Attention Network)

### Architecture

KGAT jointly learns embeddings from the knowledge graph structure and performs message passing with attention:

```
Layer 0: Initial entity and relation embeddings
         ↓
Layer 1: Attentive aggregation of neighbor information
         ↓
Layer 2: Further aggregation with attention
         ↓
...
         ↓
Layer L: Final entity representations → Recommendation score
```

### Attention Mechanism

#### Entity-Level Attention

For entity `h` aggregating information from neighbors:

```
α(h, h') = softmax(LeakyReLU(a^T [W h ⊕ W h' ⊕ r_{h,h'}]))
```

Where:
- `a`: Attention vector
- `W`: Transformation matrix
- `⊕`: Concatenation
- `r_{h,h'}`: Relation embedding between h and h'

#### Relation-Level Attention

Weight different relation types differently:

```
α(r_k) = softmax(w_r_k^T × r_k_embedding)
```

This allows the model to learn which relation types are most important for prediction.

### Message Passing Framework

```
For each layer l:
  For each entity h:
    Aggregate: m_h = Σ_{h' ∈ N(h)} α(h, h') × (W_l × h' + r_{h,h'})
    Update: h^{l+1} = LeakyReLU(m_h + h^l)
```

### Advantages of KGAT

- **End-to-end**: Jointly learns KG embeddings and recommendation
- **Interpretable**: Attention weights reveal reasoning paths
- **Scalable**: Can handle large KGs with sparse attention
- **Heterogeneous**: Handles multiple entity and relation types natively

---

## Integrating KG with Collaborative Filtering

### KG-Based Feature Enhancement

Enrich CF models with KG-derived features:

| Feature Type | Description | Example |
|-------------|-------------|---------|
| Entity embeddings | KG embedding vectors as item features | 128-dim TransE vector |
| Path features | Path-based features for user-item pairs | "3 paths through genre" |
| Relation features | Statistical features of entity relations | "item has 5 genre connections" |
| Community features | KG community detection results | "item belongs to community C3" |

### KGNN (Knowledge Graph Neural Network)

```
Step 1: Initialize item embeddings from KG embeddings
Step 2: For each user-item pair, extract relevant KG subgraph
Step 3: Apply GNN over the subgraph to refine item embedding
Step 4: Compute recommendation score using refined embeddings
```

### RippleNet

- Propagates user preferences on the KG like "ripples" in water
- Starting from user's interacted items, preferences spread outward
- Attention mechanism controls propagation strength per relation
- Captures multi-hop reasoning without explicit path enumeration

### CKAN (Collaborative Knowledge Graph Attention Network)

- Combines collaborative signals with KG structure
- Two attention mechanisms: KG attention + CF attention
- Fuses both signals for final prediction

---

## Production Integration

### KG Construction Pipeline

```
Raw Data Sources
      ↓
Entity Extraction (NER + Entity Linking)
      ↓
Relation Extraction (Pattern matching + ML)
      ↓
Knowledge Fusion (Deduplication + Conflict Resolution)
      ↓
KG Store (Neo4j, Neptune, JanusGraph)
      ↓
Embedding Training (Offline batch job)
      ↓
Feature Store (Embeddings + Path features)
      ↓
Recommendation Model (Consumes KG features)
```

### Embedding Computation Strategy

| Approach | Freshness | Compute | When to Use |
|----------|----------|---------|-------------|
| Full retraining | Low (weekly) | High | Stable KG, large updates |
| Incremental update | Medium (daily) | Moderate | Dynamic KG, new entities |
| Online embedding | High (real-time) | Low per request | Real-time entity linking |
| Pre-computed + cache | Based on TTL | Very low | Serving time |

### Serving Architecture

```
User Request
      ↓
Candidate Generation (CF + KG-based candidates)
      ↓
KG Feature Extraction (Pre-computed KG embeddings)
      ↓
Ranking Model (Features from CF + KG + Context)
      ↓
Re-ranking (Diversity, business rules)
      ↓
Response
```

### Graph Database Selection

| Database | Type | KG Size | Query Latency | Best For |
|----------|------|---------|---------------|----------|
| Neo4j | Native graph | < 1B triples | < 10ms | Complex traversals |
| Amazon Neptune | Managed graph | < 10B triples | < 50ms | AWS ecosystem |
| JanusGraph | Distributed graph | > 10B triples | Variable | Very large KGs |
| TigerGraph | In-memory graph | < 10B triples | < 5ms | Real-time analytics |
| Dgraph | Distributed graph | > 100B triples | < 100ms | Global scale |

---

## Challenges and Solutions

### Cold Start for New Entities

- **Content-based initialization**: Generate KG embeddings from item content immediately
- **Transfer learning**: Use pre-trained language models to initialize entity embeddings
- **Attribute-based linking**: Connect new entities to existing ones via shared attributes
- **Active learning**: Prioritize exploration of entities with few connections

### KG Quality Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Missing triples | Incomplete reasoning | Link prediction models |
| Noisy triples | Incorrect reasoning | Confidence-weighted edges |
| Outdated triples | Stale recommendations | Continuous KG update pipeline |
| Inconsistent schemas | Integration failures | Schema alignment algorithms |

### Scalability

- **Sampling**: Only use relevant subgraphs for each prediction (not the full KG)
- **Partitioning**: Shard the KG by entity type or community
- **Caching**: Cache frequent KG queries and embeddings
- **Approximate reasoning**: Use approximate graph algorithms for large-scale inference

---

## Evaluation

### KG Embedding Quality

| Metric | Description | Target |
|--------|-------------|--------|
| Link Prediction (MRR) | Predict missing triples | > 0.3 (dataset-dependent) |
| Link Prediction (Hits@10) | Correct entity in top 10 | > 0.4 |
| Triple Classification | Classify triples as true/false | > 0.85 |

### End-to-End Recommendation Quality

| Metric | Description | Expected Improvement |
|--------|-------------|---------------------|
| NDCG@K | Ranking quality | +5–15% over CF alone |
| Coverage | % of catalog recommended | +10–20% over CF alone |
| Diversity | Intra-list diversity | +15–30% over CF alone |
| Explainability | % of recommendations with valid path | Qualitative assessment |

### Explainability Assessment

- **Path existence**: % of recommendations with valid KG path
- **Path length**: Average path length (shorter = more interpretable)
- **Path diversity**: Variety of reasoning paths used
- **User evaluation**: Survey users on explanation quality and trust
