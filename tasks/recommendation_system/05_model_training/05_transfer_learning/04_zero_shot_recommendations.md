# Zero-Shot Recommendations

## Overview

Zero-shot recommendations make predictions for items or users with no interaction data at all, relying entirely on semantic understanding, knowledge graphs, and attribute-based matching. This is the ultimate cold-start solution: recommend new items immediately upon arrival without waiting for any user interactions.

---

## CLIP-Based Matching

### Concept

CLIP (Contrastive Language-Image Pre-training) learns a shared embedding space for images and text. For recommendations, this enables matching user preferences (expressed as text queries or behavioral patterns) to item content (images, descriptions).

### Architecture for Recommendations

```
User Context (text) → CLIP Text Encoder → User Embedding
                                               ↓
Item Image → CLIP Image Encoder → Item Embedding → Similarity Score
```

### Zero-Shot Capability

- No training on user-item interactions needed
- Match user intent to item content directly in CLIP space
- Works for any item category CLIP was pre-trained on
- Can combine with other signals (popularity, freshness) for hybrid scoring

### Application Scenarios

| Scenario | User Signal | Item Signal | Method |
|----------|-----------|------------|--------|
| Visual search | Upload image | Product catalog | Image-to-image similarity |
| Text query | Search query | Item descriptions | Text-to-text similarity |
| Contextual | Session context | Item images+text | Multimodal matching |
| Preference transfer | User favorites | New item content | Embedding nearest neighbors |

### Limitations

- CLIP may not capture domain-specific visual features (e.g., fabric texture for fashion)
- Text descriptions may be noisy or inconsistent across items
- Semantic gap between CLIP's general knowledge and specific recommendation tasks
- Cannot capture collaborative signals (what other users liked)

---

## Knowledge Graph Reasoning

### Knowledge Graph Structure for Recommendations

```
(User) --[purchased]--→ (Item) --[belongs_to]--→ (Category)
   ↓                        ↓                        ↓
[has_age]              [has_brand]              [parent_category]
   ↓                        ↓                        ↓
(Demographic)          (Brand Entity)          (Category Hierarchy)
```

### Zero-Shot Reasoning Methods

**Graph Neural Networks (GNNs)**:
- Propagate information through knowledge graph structure
- Learn node embeddings from graph topology
- New items automatically get embeddings via their graph connections
- No interaction data needed; structure alone provides recommendations

**Rule-Based Reasoning**:
- Define recommendation rules based on knowledge graph paths
- "Users who liked X also liked Y" encoded as graph rules
- New items inherit recommendations through graph connections
- Interpretable but limited in expressiveness

**Embedding-Based Reasoning**:
- Pre-train knowledge graph embeddings (TransE, RotatE, CompGCN)
- Score user-item pairs based on embedding compatibility
- Generalizes to new items through their graph neighbors
- Combines structural and semantic information

### Knowledge Graph Construction

- Extract entities and relations from item metadata
- Link to external knowledge bases (Wikipedia, domain ontologies)
- Include user demographic nodes for user-side reasoning
- Temporal relations for time-aware recommendations

---

## Attribute-Based Matching

### Feature-to-Preference Mapping

Map item attributes directly to user preferences without interaction history:

**Explicit Attributes**:
| Attribute Type | Example | Matching Method |
|---------------|---------|----------------|
| Category | "Science Fiction" | Category preference model |
| Brand | "Apple" | Brand affinity score |
| Price range | "$50-$100" | Price sensitivity profile |
| Color | "Blue" | Color preference model |
| Rating | "4.5 stars" | Quality threshold filter |

**Derived Attributes**:
| Attribute | Derivation | Use |
|-----------|-----------|-----|
| Popularity | Interaction count | Social proof signal |
| Freshness | Time since publication | Novelty preference |
| Diversity score | Attribute entropy | Exploration signal |
| Price trend | Price change over time | Deal-seeking signal |

### Attribute Embedding Spaces

1. Learn attribute-specific embedding spaces during pre-training
2. Project user preferences into each attribute space
3. Score items based on distance in each attribute space
4. Combine attribute-specific scores for final recommendation

### Multi-Modal Attribute Matching

- Combine text descriptions, images, and structured attributes
- Learn joint embedding space across modalities
- Use cross-modal attention to align user text queries with item images
- Particularly effective for fashion, food, and media recommendations

---

## Semantic Matching Without Training Data

### Pre-Trained Language Model Matching

- Use BERT/LLaMA to encode item descriptions and user queries
- Compute semantic similarity between encoded representations
- No recommendation-specific training needed
- Works for any domain with text descriptions

### Embedding Space Transfer

1. Use pre-trained embeddings from general-domain model
2. Project into recommendation-specific space (learned on source domain)
3. Zero-shot predictions via nearest neighbor search
4. Quality depends on embedding transferability

### Hybrid Semantic-Collaborative

- Use semantic matching for cold-start items
- Blend with collaborative signals as interaction data accumulates
- Weight semantic vs collaborative based on data availability
- Smooth transition from zero-shot to data-driven recommendations

---

## Evaluation of Zero-Shot Recommendations

### Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Hit rate@K | Fraction of relevant items in top-K | > 0.3 for K=10 |
| NDCG@K | Ranking quality of relevant items | > 0.2 for K=10 |
| Coverage | Fraction of catalog recommended | > 80% |
| Novelty | Average inverse popularity of recommended items | High |
| Semantic alignment | Human evaluation of recommendation relevance | Qualitative |

### Evaluation Protocol

- Test on truly new items (not seen during any training)
- Evaluate user satisfaction with zero-shot recommendations
- Compare against popularity baseline (hard to beat for cold start)
- Measure transition quality as interaction data accumulates

---

## Practical Considerations

### When to Use Zero-Shot

- New item catalog items with no interaction history
- New market launch with no historical data
- Long-tail items rarely interacted with
- Real-time recommendations during trending events

### Combining with Other Approaches

- **Ensemble**: Average zero-shot scores with collaborative filtering scores
- **Cascade**: Use zero-shot for ranking, collaborative for re-ranking
- **Fallback**: Use zero-shot when collaborative model has insufficient data
- **Warm-start**: Use zero-shot to bootstrap collaborative model training

### Best Practices

1. Always validate zero-shot quality on a human evaluation set
2. Monitor for semantic drift (pre-trained model's domain mismatch)
3. Combine multiple zero-shot signals (semantic, attribute, knowledge graph)
4. Plan for smooth transition to data-driven recommendations
5. Use zero-shot as initialization, not final production system
