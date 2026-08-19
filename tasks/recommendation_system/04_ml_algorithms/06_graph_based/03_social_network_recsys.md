# Social Network Recommendations

## Overview

Social graph recommendations leverage the structure and dynamics of social networks to improve recommendation quality. Users' social connections provide rich signals about their preferences—friends often share similar tastes, trusted contacts influence purchasing decisions, and community membership reveals shared interests. This document covers trust-based CF, social regularization, influence propagation, friend recommendations, and community detection.

---

## Trust-Based Collaborative Filtering

### Trust Signals

| Trust Type | Source | Strength |
|---|---|---|
| **Explicit trust** | User declares trust in another user | Strong (direct signal) |
| **Implicit trust** | Inferred from interaction patterns | Moderate (derived signal) |
| **Social connection** | Friendship, follow relationship | Weak to moderate |
| **Professional trust** | Endorsements, recommendations | Moderate to strong |
| **Review trust** | Consistently helpful reviews | Moderate |

### Trust-Weighted CF

Standard CF averages ratings from similar users. Trust-based CF weights contributions by trust:

**r̂_ui = r̄_u + Σ_{v∈T(u)} t_uv × (r_vi - r̄_v) / Σ_{v∈T(u)} |t_uv|**

Where:
- **T(u)**: Set of users that u trusts.
- **t_uv**: Trust score from u to v.
- **r_vi**: User v's rating of item i.
- **r̄_v**: User v's average rating.

### Trust Propagation

Direct trust is sparse—most user pairs have no explicit trust. Trust propagation infers indirect trust through social paths:

**t_uv = Π_{edges in path} t_edge × decay^{path_length}**

- **Path length decay**: Trust decreases with each hop (friends of friends are less trusted than direct friends).
- **Path redundancy**: Multiple paths between users reinforce trust.
- **Trust aggregation**: When multiple paths exist, combine using averaging, maximum, or product.

---

## Social Regularization

### Social Regularization Framework

Social regularization adds a social consistency term to the MF objective:

**L = L_MF + λ_social × Σ_{u,v∈Social} s_uv × ||p_u - p_v||²**

Where:
- **s_uv**: Social connection strength between users u and v.
- **p_u, p_v**: User latent factors.
- **||p_u - p_v||²**: Penalizes dissimilar factors for socially connected users.

### Social Regularization Variants

| Variant | Constraint | Effect |
|---|---|---|
| **Social nuclear norm** | Low-rank social matrix | Captures community structure |
| **Social Laplacian** | Graph Laplacian regularization | Smooths embeddings across social graph |
| **SocialMF** | Trust matrix factorization | Factors encode social trust |
| **PTR** | Probabilistic trust relations | Bayesian social regularization |

### Impact of Social Regularization

| Aspect | Without Social Reg | With Social Reg |
|---|---|---|
| Cold-start users | Poor (no interaction data) | Improved (social neighbors provide signal) |
| Sparse data | Limited by interaction sparsity | Social connections fill gaps |
| Overfitting | More likely | Social regularization acts as regularizer |
| Interpretability | Latent factors only | Social connections explain preferences |

---

## Influence Propagation

### Social Influence in Recommendations

Social influence captures how users' preferences change due to social connections:

| Influence Type | Mechanism | Example |
|---|---|---|
| **Direct influence** | Friend directly recommends an item | "You should watch this movie" |
| **Indirect influence** | Observing friend's behavior | Seeing a friend's check-in at a restaurant |
| **Homophily** | Similar users become friends | Users with similar taste follow each other |
| **Conformity** | Adopting group norms | Listening to popular music among friend group |

### Influence Modeling

**Independent Cascade Model**: Each interaction has a probability of triggering friend interactions:

1. User u interacts with item i.
2. For each friend v of u, with probability p_uv, v is "activated" (exposed to the item).
3. Activated users may interact with the item, potentially triggering further cascades.

**Linear Threshold Model**: User v interacts with item i when the weighted influence from friends who already interacted exceeds a threshold:

**Σ_{u∈N(v) who interacted} b_uv ≥ θ_v**

Where b_uv is the influence weight and θ_v is v's threshold.

### Influence-Aware Recommendations

- **Influence potential**: Recommend items that are likely to propagate through the social network.
- **Targeted influence**: Recommend to users who are influential in their communities.
- **Cascade prediction**: Predict the reach of a recommendation through social propagation.

---

## Friend Recommendations

### Friend Recommendation Algorithms

| Approach | Method | Signal |
|---|---|---|
| **Structural** | Common friends, triadic closure | Graph topology |
| **Content-based** | Similar interests, profiles | User attributes |
| **Behavioral** | Similar interaction patterns | Usage patterns |
| **Hybrid** | Combine structural, content, behavioral | Multiple signals |

### Structural Methods

- **Common friends**: Users with many mutual friends are likely to become friends.
- **Jaccard coefficient**: |N(u) ∩ N(v)| / |N(u) ∪ N(v)| where N(u) is the friend set.
- **Adamic-Adar**: Σ_{w∈N(u)∩N(v)} 1/log(|N(w)|). Weight common friends by their rarity.
- **Friend-of-friend**: Recommend users connected through a friend path of length 2.

### Friend Recommendation Quality

| Metric | Description | Target |
|---|---|---|
| **Precision@K** | Fraction of recommended friends that are actual friends | > 10% |
| **Recall@K** | Fraction of actual friends that are recommended | > 5% |
| **Acceptance rate** | Fraction of recommendations accepted | > 5% |
| **Diversity** | Variety of recommended friend types | High |

---

## Community Detection

### Community Detection Methods

| Method | Description | Scalability | Quality |
|---|---|---|---|
| **Louvain** | Modularity optimization | High | High |
| **Label Propagation** | Iterative label assignment | Very high | Moderate |
| **Spectral clustering** | Graph Laplacian eigenvectors | Low | High |
| **Deep learning** | GNN-based community detection | Moderate | High |
| **Infomap** | Information flow-based | High | High |

### Community-Aware Recommendations

| Strategy | Description | Use Case |
|---|---|---|
| **Intra-community** | Recommend items popular within the user's community | Niche preferences |
| **Cross-community** | Recommend items from adjacent communities | Discovery and exploration |
| **Community trends** | Recommend trending items within the community | timely recommendations |
| **Community-based CF** | Use community members as the neighbor pool | Improved CF accuracy |

### Community Detection for Recsys

- **User communities**: Group users with similar preferences for community-based CF.
- **Item communities**: Group items with similar interaction patterns for item-based recommendations.
- **Hybrid communities**: Detect communities in the user-item bipartite graph for holistic recommendations.
