# Training Deep Learning Recommendation Models

## Overview

Training production deep learning recommendation models presents unique challenges: embedding tables (mapping sparse categorical features to dense vectors) dominate model memory, large-scale negative sampling is essential, ranking-appropriate loss functions are required, and distributed training across clusters is necessary for scale. This document covers the end-to-end training pipeline.

---

## Embedding Table Management

Embedding tables often constitute 90%+ of total model parameters:

| Feature | Vocab Size | Dim | Table Size (FP32) |
|---------|-----------|-----|-------------------|
| User ID | 100M | 128 | ~48 GB |
| Item ID | 10M | 128 | ~4.8 GB |
| Item category | 1K | 32 | ~128 KB |
| Device type | 10 | 8 | ~320 B |

### Memory Strategies

| Strategy | Savings | Quality Impact |
|----------|---------|---------------|
| Hash bucketing | 50–90% | Moderate (collisions) |
| Quantized (INT8/FP16) | 2–4× | Minimal |
| Mixed-dimension | 30–50% | Minimal |
| Feature pruning | Variable | Low if threshold reasonable |
| Embedding factorization (E=W₁×W₂) | Significant | Low with sufficient rank |

**Hash bucketing**: `index = hash(id) % bucket_size`. Bucket size 2–5× unique IDs. Fixed size, handles new IDs, but collisions degrade quality.

**Dynamic growth**: Pre-allocated pool, hash-based (no pre-allocation), or lazy initialization for new IDs.

---

## Negative Sampling Strategies

Full softmax O(|I|) is infeasible; negative sampling reduces to O(K).

| Method | Complexity | Quality | Notes |
|--------|-----------|---------|-------|
| Uniform random | O(1) | Good baseline | Simplest |
| Popularity-weighted | O(1) alias table | Better (harder) | freq^α, α=0.5 common |
| In-batch negatives | O(batch_size) | Strong, efficient | All non-target in batch |
| Hard negative mining | O(N) mining phase | Best quality | Model-scored candidates |

**Popularity sampling**: `P(i) = freq(i)^α / Σ freq(j)^α`. α=0 uniform; α=0.5 sqrt; α=1 pure popularity (hardest).

**In-batch**: Negatives = all other items in batch. Loss: `-log(exp(s(u,i)) / Σ_j exp(s(u,j)))`. Batch size 512–4096 provides many negatives automatically.

**Hard mining**: Retrieve similar items via ANN → score with current model → select highest-scoring non-positives. Mine every N epochs to avoid instability.

---

## Loss Functions

| Loss | Formula | Cost | Best For |
|------|---------|------|----------|
| BCE | `-Σ [y log σ(s) + (1-y) log(1-σ(s))]` | O(K) | CTR prediction |
| BPR | `-log σ(s⁺ - s⁻)` | O(K) | Pairwise ranking |
| Softmax | `-log exp(s⁺) / Σ exp(sⱼ)` | O(|I|) | Small catalogs |
| Sampled Softmax | Softmax over sampled subset | O(K+|S|) | Large catalogs |
| InfoNCE | `-log exp(s⁺/τ) / Σ exp(sⱼ/τ)` | O(batch) | Contrastive learning |

**Sampled softmax correction**: Adjust for sampling bias: `L = -log exp(s(i) - log P(i)) / (exp(s(i) - log P(i)) + Σ_j∈S exp(s(j) - log P(j)))`.

---

## Optimization

### Adam vs Adagrad for Sparse Features

| Optimizer | Dense | Sparse Embeddings | Why |
|-----------|-------|-------------------|-----|
| Adam | Good | Moderate | Momentum can hurt sparse |
| Adagrad | Good | Excellent | Per-parameter LR; infrequent updates get higher LR |
| DLRM hybrid | Good | Excellent | Adam for dense, Adagrad-style for sparse |

**Adagrad for embeddings**: `θ_t = θ_{t-1} - lr × g_t / (√G_{t-1} + ε)`. Rarely-updated embeddings have small G → larger effective LR → faster learning from few examples.

### Learning Rate Scheduling

| Strategy | When | Effect |
|----------|------|--------|
| Warm-up + decay | First M steps | Stable early training |
| Cosine annealing | Continuous | Smooth decay |
| Step decay | Every N epochs | Coarse adjustment |

---

## Regularization

| Technique | Rate/Setting | Purpose |
|-----------|-------------|---------|
| Dropout (hidden) | 0.1–0.5 | Standard regularization |
| Dropout (embedding) | 0.0–0.2 | Prevent ID overfitting |
| Weight decay (dense) | 1e-5 to 1e-4 | L2 on dense params only |
| Label smoothing | 0.9 target | Prevent overconfidence |
| Early stopping | K=3–5 epochs patience | Stop at validation plateau |

**Note**: Embeddings are typically NOT regularized with weight decay — it degrades quality for rare features.

---

## Mixed Precision Training

| Aspect | FP32 | FP16 |
|--------|------|------|
| Memory/param | 4 bytes | 2 bytes |
| Throughput | Baseline | 1.5–3× faster |
| Numerical range | ±3.4 × 10³⁸ | ±65,504 |

**AMP strategy**: Forward pass in FP16, loss in FP32, gradients in FP16, parameter updates in FP32 master copy, embedding lookups in FP32 (sparse gradients lose precision in FP16).

---

## Distributed Training

### Embedding Parallelism (Primary Challenge)

| Strategy | Description | Communication |
|----------|-------------|---------------|
| Table partitioning | Split rows across workers | All-to-all for lookups |
| Row-wise sharding | Contiguous rows per worker | All-to-all gather |
| Column-wise sharding | Dimensions per worker | All-reduce for combines |
| Replicated | Full table on each worker | Only for small tables |

**All-to-all**: Each worker needs embeddings from others for its local batch — dominant communication bottleneck.

### Data Parallelism for Dense Parameters

Dense parameters replicated on all workers; gradients synchronized via AllReduce. Scales well.

### Hybrid Parallelism (Production)

```
Embedding tables: Partitioned (embedding parallelism)
Dense parameters: Replicated (data parallelism)
Gradient sync: AllReduce (dense) + All-to-all (sparse)
```

---

## Training Data Construction

### Positive/Negative Sources

| Source | Positive | Negative |
|--------|----------|----------|
| Click logs | Clicked items | Shown but not clicked |
| Purchase logs | Purchased | Viewed but not purchased |
| Impression logs | Clicked from impression | Non-clicked from same impression |
| Explicit feedback | Rating ≥ 4 | Rating ≤ 2 |

### Sequence Construction (for DIN/DIEN/SASRec)

```
Behavior log: [item₁, ..., item_T] (chronological)
Training: (target=item_T, context=[item₁,...,item_{T-1}])
          (target=item_{T-1}, context=[item₁,...,item_{T-2}])
```

**Temporal splitting**: Sort by timestamp; train before cutoff, validate next window, test final window. Never random split for sequential models (causes data leakage).

### Feature Pipeline

```
Raw logs → Dedup → Feature extraction → Encoding → Split
                           ↓              ↓
                    Negative sampling  Sequence construction
```

---

## Convergence Monitoring

### Key Metrics

| Metric | Tells You | Healthy |
|--------|----------|---------|
| Training loss | Learning progress | Decreasing |
| Validation AUC | Generalization | Increasing then plateau |
| Embedding norm | Embedding health | Stable after warm-up |
| Gradient norm | Training stability | Stable, not exploding |
| Pos/neg score gap | Discrimination ability | Widening |

### Diagnosing Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Loss plateaus early | LR too high/low | LR sweep |
| Train ↓, val ↑ | Overfitting | More regularization, data |
| Both high | Underfitting | Larger model |
| Embedding norms → 0 | Collapse | Check init, reduce LR |
| Score explosion | Gradient explosion | Gradient clipping |

### Essential Dashboard Plots

1. Loss curves (train + val)
2. AUC/NDCG (validation)
3. Gradient histograms per layer
4. Embedding norm distribution
5. Learning rate schedule
6. GPU utilization
7. Score distribution (positive vs negative)

---

## Best Practice Defaults

| Parameter | Recommended |
|-----------|-------------|
| LR (dense) | 1e-3 (Adam) |
| LR (sparse) | 1e-1 (Adagrad-style) |
| Batch size | 1024–4096 |
| Embedding dim | 64–256 |
| Hidden layers | 3–5 (256→128→64) |
| Dropout | 0.1–0.3 |
| Negative ratio | 4:1 to 10:1 |
| Weight decay | 1e-5 to 1e-4 |
| Gradient clipping | 5.0–10.0 |

---

## Summary

Training recommendation models requires specialized infrastructure for large embedding tables (hash bucketing, quantization), ranking-appropriate losses (BPR, sampled softmax), Adagrad for sparse embeddings, hybrid distributed training (embedding parallelism + data parallelism for dense), and careful monitoring of embedding health alongside standard metrics. The pipeline from raw logs through negative sampling, sequence construction, and temporal splitting is as critical as the model architecture itself.
