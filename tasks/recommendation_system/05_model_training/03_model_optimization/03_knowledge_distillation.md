# Knowledge Distillation for Recommendation Systems

## Overview

Knowledge distillation transfers knowledge from a large, complex "teacher" model to a smaller, faster "student" model. For recommendation systems, this enables deploying lightweight models that maintain the quality of large research models, reducing serving costs while preserving user experience. The student learns not just from the teacher's predictions but from its internal representations and learned patterns.

---

## Teacher-Student Framework

### Architecture Design

**Teacher Model**: Large, high-capacity model trained to convergence
- May be an ensemble of models
- May use expensive features not available at inference
- Optimized for quality, not latency
- Typical: Deep & Cross Network V2, multi-tower with attention, large transformer

**Student Model**: Smaller, faster model to be deployed
- Must meet inference latency/memory constraints
- May have simpler architecture (fewer layers, narrower hidden dims)
- Optimized for the deployment environment
- Typical: shallow MLP, single-tower, lightweight attention

### Distillation Pipeline

1. Train teacher model to convergence on full dataset
2. Freeze teacher parameters; extract soft targets during inference
3. Train student model on combination of hard labels and soft targets
4. Evaluate student on held-out test set
5. Iterate on student architecture/hyperparameters if quality gap is too large

### Knowledge Types

| Knowledge Type | Description | Extraction Method |
|---------------|-------------|------------------|
| Output-level | Soft prediction probabilities | Teacher logits |
| Feature-level | Intermediate representations | Layer activations |
| Relational | Relationships between samples | Pairwise similarities |
| Attention | Cross-feature attention patterns | Attention weights |

---

## Soft Targets and Temperature Scaling

### Soft Target Generation

The teacher's output logits are converted to soft probability distributions:

```
soft_target_i = softmax(logit_i / T)
```

Where T is the temperature parameter.

### Temperature Scaling

| Temperature | Effect | When to Use |
|-------------|--------|------------|
| T = 1 | Standard softmax (hard-like) | Default starting point |
| T = 2-5 | Softens probability distribution | Typical range for distillation |
| T = 10-20 | Very uniform distribution | When teacher is very confident |
| T → ∞ | Uniform distribution | Maximum softening (rare) |

### Why Soft Targets Help

- Soft targets contain dark knowledge: information about relative similarities between classes
- A teacher predicting [0.7, 0.2, 0.1] for three items encodes that item 2 is more similar to item 1 than item 3
- Hard targets [1, 0, 0] lose this relational information
- For recommendation: soft targets across candidate items encode fine-grained preference structure

### Multi-Temperature Distillation

- Use different temperatures for different output components
- Higher temperature for item categories (more diffusion)
- Lower temperature for top-ranked items (preserve sharp distinctions)
- Tune temperature as a distillation hyperparameter

---

## Feature-Level Distillation

### Intermediate Layer Matching

Match student intermediate representations to teacher intermediate representations:

```
distillation_loss = Σᵢ λᵢ × MSE(student_layerᵢ, project(teacher_layerⱼ))
```

Where `project` is a linear projection to match dimensions.

### Matching Strategies

| Strategy | Description | Pros |
|----------|-------------|------|
| Layer-by-layer | Match corresponding layers | Simple, effective |
| Attention transfer | Match attention maps | Captures focus patterns |
| Relational KD | Match pairwise distances between samples | Captures structure |
|_pkt| Match kernel matrices | Captures nonlinear relationships |

### Hidden Layer Projection

When teacher and student have different hidden dimensions:
- Use a learnable linear projection: `W_proj × student_hidden → teacher_dim`
- Can add LayerNorm for stabilization
- Projection is trained jointly with the student
- Discard projection after training (inference uses student only)

### Feature Distillation for Recommendation Models

- **Embedding distillation**: Match user/item embedding spaces between teacher and student
- **Attention distillation**: Transfer cross-feature attention patterns
- **Tower distillation**: Match prediction tower intermediate representations
- **Sequence distillation**: Transfer sequential pattern representations in sequential models

---

## Progressive Distillation

### Multi-Stage Knowledge Transfer

Instead of distilling directly from teacher to student, use intermediate models:

```
Large Teacher → Medium Model 1 → Medium Model 2 → Small Student
```

### Benefits

- Each step has a smaller capacity gap, easier optimization
- Can be parallelized: train each stage independently
- Intermediate models serve as checkpoints for quality monitoring
- Enables very large compression ratios (100x+)

### Progressive Distillation for Recommendation Systems

1. **Stage 1**: Distill from ensemble teacher to single large model
2. **Stage 2**: Distill from large model to medium model (remove attention, reduce layers)
3. **Stage 3**: Distill from medium to small model (simplify feature interactions)
4. **Stage 4**: Quantize and prune small model for deployment

### Curriculum-Based Progressive Distillation

- Start with easy samples (popular items, active users)
- Gradually increase difficulty (long-tail items, new users)
- Each stage uses both soft targets and hard labels
- Prevents catastrophic forgetting of edge cases

---

## Multi-Teacher Distillation

### Multiple Teacher Combination

Combine knowledge from multiple specialized teachers:

| Teacher Type | Knowledge Provided | Example |
|-------------|-------------------|---------|
| Collaborative filtering | User-item interaction patterns | Matrix factorization model |
| Content-based | Feature similarity patterns | Deep content model |
| Sequential | Temporal behavior patterns | Transformer sequential model |
| Contextual | Context-dependent preferences | Context-aware model |

### Combination Strategies

**Average soft targets**: Average logits from all teachers before computing soft targets
```
combined_logit = (1/K) × Σₖ teacher_k_logit
```

**Mixture of experts**: Each teacher contributes to a weighted combination
```
student_loss = Σₖ αₖ × distillation_loss(student, teacher_k)
```

**Knowledge selection**: Use different teachers for different sample types
- Popularity-based: use popularity model teacher for popular items
- Recency-based: use sequential model teacher for recent interactions
- Content-based: use content model teacher for cold-start items

### Multi-Teacher Advantages

- Each teacher specializes in different aspects of the recommendation task
- Student receives a richer, more diverse knowledge signal
- More robust to any single teacher's biases or blind spots
- Enables combining heterogeneous model architectures

---

## Distillation Loss Functions

### Standard Distillation Loss

```
L_total = α × L_CE(student, hard_labels) + (1-α) × T² × KL(teacher_soft, student_soft)
```

Where:
- α balances hard label and soft target losses (typically 0.1-0.5)
- T² scaling compensates for gradient magnitude reduction at high temperature
- KL divergence measures distribution similarity

### Feature Matching Loss

```
L_feature = Σᵢ ||f_student(x)_ᵢ - Wᵢ × f_teacher(x)_ⱼ||²
```

### Attention Transfer Loss

```
L_attention = Σᵢ ||A_student(x)_ᵢ - A_teacher(x)_ⱼ||²
```

Where A represents attention maps (normalized to sum to 1).

### Combined Loss

```
L_total = α × L_CE + β × L_soft + γ × L_feature + δ × L_attention
```

Tune α, β, γ, δ via validation performance.

---

## Practical Considerations

### When to Use Distillation

- Large teacher model is too slow for production inference
- Need to serve on resource-constrained environments (mobile, edge)
- Ensemble model needs to be compressed to a single model
- Model size must be reduced for cost optimization

### Quality Gap Management

- If student quality drops >2%: increase student capacity
- If student quality drops 0.5-2%: tune distillation hyperparameters
- If student quality is within 0.5%: proceed with deployment
- Monitor quality gap across user segments (not just aggregate)

### Common Pitfalls

- Teacher overconfidence: very confident teachers produce uninformative soft targets (use label smoothing)
- Distribution mismatch: student trained on soft targets may not generalize to hard labels
- Over-regularization: too much distillation can constrain student learning
- Ignoring student-specific strengths: student may excel in areas teacher doesn't
