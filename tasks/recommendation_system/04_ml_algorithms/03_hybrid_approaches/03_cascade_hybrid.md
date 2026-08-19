# Cascade Hybrid for Recommendations

## Overview

A cascade hybrid applies multiple recommendation models in a sequential pipeline, where the output of one model feeds into the next. Each stage refines, filters, or re-ranks the candidates from the previous stage. This architecture is the dominant pattern in production recommendation systems because it naturally handles the candidate generation → scoring → ranking pipeline that most systems require.

---

## Primary and Secondary Models

### Model Roles

| Role | Function | Example Models | Output |
|---|---|---|---|
| **Primary (generator)** | Produce broad candidate set | ANN retrieval, content-based, popularity | 100–10,000 candidates |
| **Secondary (ranker)** | Score and rank candidates | GBM, neural ranker, CF-based scorer | Top-N ranked list |
| **Tertiary (re-ranker)** | Apply business rules and diversity | Business logic, diversity optimizer | Final presentation list |

### Why Cascade Works

- **Separation of concerns**: Each model focuses on what it does best—broad retrieval, precise scoring, or business rule application.
- **Computational efficiency**: Early stages can be approximate (ANN), while later stages can be exact (neural ranking).
- **Fail-safe design**: If a later stage fails, earlier stages provide a reasonable fallback.
- **Modularity**: Individual models can be updated independently without retraining the entire pipeline.

---

## Multi-Stage Recommendation Pipeline

### Typical Stages

```
Stage 1: Candidate Generation (10,000 → 1,000)
  - Collaborative filtering retrieval (ANN search)
  - Content-based retrieval (keyword/tag matching)
  - Popularity-based retrieval (trending, top items)

Stage 2: Pre-Ranking (1,000 → 200)
  - Lightweight scoring model (logistic regression, shallow GBM)
  - Basic filtering (availability, region, age-appropriate)

Stage 3: Ranking (200 → 50)
  - Complex ranking model (deep neural network, gradient boosted trees)
  - Feature-rich scoring with hundreds of features

Stage 4: Re-Ranking (50 → 10)
  - Business rules (diversity, freshness, vendor agreements)
  - Editorial overrides
  - Exploration injection
```

### Stage Design Principles

| Principle | Description |
|---|---|
| **Progressive narrowing** | Each stage reduces the candidate set |
| **Increasing model complexity** | Later stages use more complex (and expensive) models |
| **Increasing feature richness** | Later stages have access to more features |
| **Guaranteed output** | Each stage must produce at least some candidates |
| **Time budget allocation** | More time budget for later (more impactful) stages |

### Time Budget Allocation

For a 100ms total latency budget:

| Stage | Time Budget | Strategy |
|---|---|---|
| Candidate generation | 20ms | Pre-computed embeddings, ANN index |
| Pre-ranking | 15ms | Lightweight model, batch inference |
| Ranking | 50ms | Complex model, GPU inference |
| Re-ranking | 15ms | Business rules, simple logic |

---

## Confidence-Based Model Selection

### Confidence Thresholds

At each cascade stage, the model produces a confidence score. If confidence is below a threshold, the stage can skip or use a fallback:

| Confidence Level | Action |
|---|---|
| **High** (> 0.9) | Proceed to next stage with full candidate set |
| **Medium** (0.5–0.9) | Proceed but add backup candidates from alternative sources |
| **Low** (< 0.5) | Fall back to a simpler model or broaden the candidate set |

### Dynamic Confidence Thresholds

Thresholds should adapt based on context:

- **User segment**: Lower thresholds for new users (less reliable predictions).
- **Item popularity**: Higher thresholds for popular items (more data, more reliable).
- **Time of day**: Adjust thresholds based on traffic patterns and latency constraints.
- **A/B test variant**: Different thresholds for different experimental configurations.

---

## Production Cascade Architecture

### Feature Store Integration

Each stage accesses the feature store differently:

| Stage | Feature Requirements | Access Pattern |
|---|---|---|
| Candidate generation | Item embeddings, user embeddings | ANN index (pre-computed) |
| Pre-ranking | Basic user-item features | Online feature store (Redis) |
| Ranking | Rich cross features, context features | Online feature store (batch lookup) |
| Re-ranking | Business rules, diversity features | In-memory cache |

### Model Serving at Each Stage

| Stage | Serving Framework | Model Type |
|---|---|---|
| Candidate generation | FAISS/ScaNN + custom retrieval | Embedding model |
| Pre-ranking | TensorFlow Serving, ONNX Runtime | Lightweight GBM |
| Ranking | GPU inference (TensorRT, Triton) | Deep neural network |
| Re-ranking | Custom rules engine | Business logic |

### Monitoring Each Stage

Track metrics per stage to identify bottlenecks and quality issues:

- **Candidate generation**: Recall@K (are relevant items making it into the candidate set?), latency, throughput.
- **Pre-ranking**: Precision@K of the pre-ranked set, latency, filter pass-through rate.
- **Ranking**: NDCG, MAP, MRR of the final ranking, latency, feature coverage.
- **Re-ranking**: Diversity metrics, freshness distribution, business rule compliance.

---

## Cascade Failure Modes

### Common Failure Patterns

| Failure | Symptom | Root Cause | Mitigation |
|---|---|---|---|
| **Cand. generation miss** | Relevant items absent from final results | Low recall at candidate stage | Diversify retrieval sources |
| **Pre-ranking filter** | Good candidates removed | Overly aggressive filtering | Relax filter thresholds |
| **Ranking miscalibration** | Top-ranked items are poor | Model drift or feature staleness | Retrain ranking model |
| **Re-ranking degradation** | Diversity too high, relevance too low | Business rules override ranking | Tune rule weights |
| **Latency timeout** | Slow stage causes timeout | Insufficient compute resources | Scale the bottleneck stage |

### End-to-End Quality Monitoring

- **Pipeline health score**: Aggregate metric combining latency, throughput, and error rate across all stages.
- **Stage contribution analysis**: Measure how much each stage improves or degrades the candidate set quality.
- **A/B test by stage**: Isolate the impact of changes to individual stages through targeted experiments.
- **User satisfaction correlation**: Track how cascade metrics correlate with downstream user engagement.

### Cascade Optimization Strategies

- **Latency optimization**: Profile each stage to identify the slowest component. Use batch inference, caching, or model distillation for bottleneck stages.
- **Quality optimization**: Use recall@K analysis to identify where relevant items are lost. Improve the weakest stage first.
- **Cost optimization**: Balance compute cost across stages. Use cheaper models for earlier stages where approximate retrieval is acceptable.
- **A/B testing by stage**: Test changes to individual stages without affecting the entire pipeline.
