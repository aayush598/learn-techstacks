# Few-Shot Learning for Recommendation Systems

## Overview

Few-shot learning enables recommendation models to make accurate predictions with very few interaction examples (1-50 shots). This is critical for cold-start scenarios: new users, new items, and new markets where historical interaction data is scarce. Meta-learning approaches learn to learn from few examples, enabling rapid adaptation to new contexts.

---

## Cold-Start Problem in Recommendations

### Cold-Start Categories

| Type | Description | Available Data |
|------|-------------|---------------|
| New user cold start | No interaction history | Profile features only |
| New item cold start | No interaction history | Item attributes only |
| New system cold start | No data at all | Domain knowledge only |
| Context cold start | New context (e.g., new device) | Previous data in other contexts |

### Few-Shot vs Zero-Shot vs Warm-Start

- **Zero-shot**: No target domain interactions; predict based on attributes/knowledge alone
- **Few-shot**: 1-50 interactions per user/item; rapid adaptation required
- **Warm-start**: 50+ interactions; standard collaborative filtering works

---

## Meta-Learning Approaches

### MAML (Model-Agnostic Meta-Learning)

**Core Idea**: Learn an initialization that can be quickly fine-tuned to new tasks with few gradient steps.

**Algorithm**:
1. Sample a batch of tasks (each task = a user with few interactions)
2. For each task, simulate few-shot learning:
   - Split task data into support set (few examples) and query set
   - Compute inner-loop gradient update on support set
   - Evaluate on query set
3. Update meta-parameters based on query set performance
4. Repeat until convergence

**Application to Recommendations**:
- Each task: a user's preference learning problem
- Support set: user's few interactions
- Query set: held-out interactions for evaluation
- Meta-parameters: model initialization that enables fast user-specific adaptation

**Inner Loop (Task Adaptation)**:
```
θ_task = θ_meta - α × ∇θ L_support(θ_meta)
```

**Outer Loop (Meta-Update)**:
```
θ_meta = θ_meta - β × Σ L_query(θ_task)
```

### Prototypical Networks

**Core Idea**: Learn an embedding space where classes (items, categories) are represented by prototypes (class centroids).

**Algorithm**:
1. Embed all support set examples into a shared space
2. Compute prototype for each class: centroid of embeddings
3. Classify query examples by distance to nearest prototype
4. Train with episodic training (simulate few-shot tasks)

**Application to Recommendations**:
- Embed user interactions into preference space
- Compute user preference prototype from few interactions
- Recommend items closest to user prototype in embedding space
- Naturally handles new items if item embeddings are available

**Distance Metrics**:
| Metric | Formula | Properties |
|--------|---------|-----------|
| Euclidean | √Σ(x-y)² | Simple, widely used |
| Cosine | x·y / (||x||·||y||) | Scale-invariant |
| Mahalanobis | √((x-y)ᵀΣ⁻¹(x-y)) | Accounts for correlations |

### Matching Networks

- Use attention mechanism to weight support examples when classifying queries
- Full context embedding: encode support set as context for predictions
- Similar to prototypical but with learned distance/attention

---

## Learning to Learn from Few Interactions

### Episodic Training

The key training paradigm for meta-learning: simulate few-shot tasks during training.

**Episode Structure**:
1. Sample a task (user from training data)
2. Split into support set S (K examples) and query set Q
3. Model adaptation on S (one or few gradient steps)
4. Compute loss on Q
5. Aggregate loss across tasks and update meta-parameters

**K-shot Training**: K examples per class in support set
**N-way Classification**: N candidate items to choose from per query

### Feature-Based Meta-Learning

- Learn feature representations that are transferable across tasks
- User features: demographics, session context, device type
- Item features: category, brand, price, text description
- Interaction features: time of day, sequence context
- These features enable few-shot learning even without interaction history

### Task-Agnostic vs Task-Specific

| Approach | Description | Advantage |
|----------|-------------|-----------|
| Task-agnostic | Same model for all tasks | Simple deployment |
| Task-specific | Separate adaptation per task type | Better performance per task |
| Hierarchical | Shared base + task-specific heads | Balance of both |

---

## Metric Learning for Recommendations

### Triplet Loss

Learn embeddings where similar user-item pairs are close and dissimilar pairs are far:

```
L = max(0, d(anchor, positive) - d(anchor, negative) + margin)
```

**Anchor**: user embedding
**Positive**: item the user interacted with
**Negative**: item the user didn't interact with

### Contrastive Learning

- Pull together representations of same user across sessions
- Push apart representations of different users
- Self-supervised: no explicit labels needed
- Pre-training objective for few-shot adaptation

### Application to Cold Start

1. Pre-train metric space using warm users (many interactions)
2. For cold-start users, embed their few interactions
3. Find nearest items in the learned metric space
4. The metric space generalizes to unseen users because it captures preference structure

---

## Application to Cold Start

### User Cold Start Pipeline

1. **Feature extraction**: Extract available user features (demographics, context, device)
2. **Meta-model adaptation**: Use MAML or prototypical network to adapt to user
3. **Hybrid scoring**: Combine meta-learned preferences with content-based signals
4. **Exploration**: Use exploration strategies to gather more interactions quickly
5. **Transition**: Gradually shift from few-shot model to standard collaborative model as data accumulates

### Item Cold Start Pipeline

1. **Attribute embedding**: Embed item features (category, brand, text, images)
2. **Attribute-to-interaction mapping**: Map attributes to predicted user preferences
3. **Prototype matching**: Find similar existing items and borrow their interaction patterns
4. **Content-based scoring**: Use item features for initial recommendation quality
5. **Learning from feedback**: Update item representation as interactions arrive

### Multi-Task Cold Start

- Simultaneously cold-start users and items
- Use attribute-based features for both sides
- Meta-learning across both user and item tasks
- Transfer knowledge from warm user-item pairs to cold ones

---

## Practical Implementation

### Training Data Requirements

- Need many users/items with sufficient interactions to form meta-tasks
- At least 1000+ tasks for stable meta-learning
- Each task needs enough data for support/query split
- Data augmentation through task sampling strategies

### Evaluation Protocol

- Held-out cold-start users/items with artificially limited interactions
- Evaluate at K-shot levels: 1, 5, 10, 20, 50 interactions
- Compare against baselines: popularity, content-based, standard CF
- Measure adaptation speed (performance improvement per additional interaction)

### Common Pitfalls

- Overfitting to meta-training tasks (insufficient task diversity)
- Inner loop gradient steps too many (overfits to support set)
- Support set too small (< 3 examples per class in prototypical networks)
- Task distribution mismatch between meta-training and deployment
- Ignoring feature cold start (user/item features unavailable in new domain)
