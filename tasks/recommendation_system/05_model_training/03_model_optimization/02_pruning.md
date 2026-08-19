# Model Pruning for Recommendation Systems

## Overview

Model pruning reduces the size and computational cost of recommendation models by removing redundant parameters while preserving predictive quality. Pruning is particularly valuable for recommendation systems deployed at scale, where even small per-request efficiency gains translate to significant infrastructure savings across millions of daily requests.

---

## Unstructured vs Structured Pruning

### Unstructured Pruning

Removes individual weights from weight matrices, resulting in sparse matrices.

- **Granularity**: Individual weights (finest granularity)
- **Sparsity patterns**: Can be random, magnitude-based, or structured at the weight level
- **Hardware requirements**: Requires sparse matrix support (cuSPARSE, specialized kernels)
- **Compression**: Achieves 90-95% sparsity with <1% quality loss in many cases
- **Challenge**: Sparse matrices don't accelerate on standard GPUs without sparse-aware kernels

### Structured Pruning

Removes entire groups of parameters (rows, columns, filters, attention heads).

| Structure Type | What's Removed | Compression | Acceleration |
|---------------|---------------|-------------|--------------|
| Filter pruning | Entire convolutional filters | Moderate | Direct |
| Channel pruning | Input/output channels | Moderate | Direct |
| Head pruning | Entire attention heads | Low-moderate | Direct |
| Neuron pruning | Entire hidden neurons | Moderate | Direct |
| Layer pruning | Entire model layers | High | Direct |

### Semi-Structured Pruning (N:M Sparsity)

- NVIDIA's 2:4 sparsity pattern: in every 4 consecutive weights, exactly 2 must be zero
- Hardware-accelerated on A100+ with sparse Tensor Cores
- 2x speedup with minimal accuracy loss
- Represents a practical middle ground between unstructured and structured pruning

---

## Pruning Criteria

### Magnitude Pruning

The most common criterion: remove weights with smallest absolute value.

```
importance(w) = |w|
```

- **Simple and effective**: Low-magnitude weights contribute least to output
- **Global vs local**: Global pruning (sort all weights) vs local (per-layer)
- **Limitation**: Assumes all weights of similar magnitude are equally unimportant
- **Best for**: Initial pruning, establishing baselines

### Movement Pruning

Prunes weights that move least during fine-tuning after being pruned.

- Pruned weights that stay near zero are truly unnecessary
- Weights that recover (move away from zero) should be un-pruned
- Particularly effective for pre-trained model fine-tuning
- Requires iterative pruning with fine-tuning between rounds

### Gradient-Based Pruning

Use gradient magnitude to assess weight importance:
- Weights with consistently small gradients contribute little to learning
- Combines magnitude and gradient information
- More stable than magnitude-only for dynamic pruning schedules

### Second-Order Pruning

Use Hessian information to assess sensitivity:
- Optimal Brain Damage/Optimal Brain Surgeon frameworks
- Prune weights whose removal causes minimal loss change
- More accurate but computationally expensive (requires Hessian inverse)
- Practical approximation: use Fisher information as a proxy

---

## Iterative Pruning Schedules

### One-Shot Pruning

- Prune model to target sparsity in a single pass
- Followed by fine-tuning to recover accuracy
- Simple but often leads to lower accuracy at high sparsity
- Works well up to 50-60% sparsity

### Iterative Magnitude Pruning (IMP)

1. Prune p% of remaining weights
2. Fine-tune for N epochs
3. Repeat steps 1-2 until target sparsity is reached
4. Final fine-tuning to convergence

**Example schedule for 90% sparsity**:
```
Round 1: 0% → 30% sparsity, fine-tune 5 epochs
Round 2: 30% → 55% sparsity, fine-tune 5 epochs
Round 3: 55% → 75% sparsity, fine-tune 10 epochs
Round 4: 75% → 90% sparsity, fine-tune 20 epochs
```

### Sparse-Growing from Scratch

- Initialize a sparse network and train from scratch
- Gradually increase sparsity during training
- Can achieve same accuracy as dense models at higher sparsity
- Requires careful learning rate scheduling

### Lottery Ticket Hypothesis

- Dense networks contain sparse subnetworks ("winning tickets") that can match dense performance
- Finding these subnetworks requires iterative pruning with rewind-to-initialization
- Practical implication: you can train sparse models from scratch if you find the right sparse structure
- Relevance to rec systems: enables sparse embedding tables and sparse dense layers

---

## Fine-Tuning After Pruning

### Recovery Training Strategy

- Reduce learning rate by 2-10x for fine-tuning after pruning
- Use warmup for 10% of fine-tuning steps
- Maintain same batch size as original training
- Monitor validation metric closely; stop if degradation persists beyond warmup

### Learning Rate Scheduling

| Sparsity Level | LR Reduction | Fine-tuning Epochs |
|----------------|-------------|-------------------|
| 50% | 0.5x | 5-10 |
| 70% | 0.25x | 10-20 |
| 90% | 0.1x | 20-50 |
| 95%+ | 0.05x | 50-100 |

### Distillation-Assisted Fine-Tuning

- Use the original dense model as a teacher during fine-tuning
- Combine task loss with distillation loss (soft targets from teacher)
- Helps pruned model recover knowledge lost during pruning
- Particularly effective for high sparsity (>80%)

---

## Sparsity Patterns for Recommendation Models

### Embedding Table Sparsity

- Feature pruning: remove rarely accessed feature values (low-frequency categorical features)
- Embedding dimension pruning: reduce embedding dimensions for less important features
- Hash collision pruning: reduce hash table size for embedding lookup
- Table pruning: remove entire embedding tables for features with low predictive power

### Dense Layer Sparsity

- Uniform sparsity across all dense layers (simplest)
- Layer-wise sparsity: deeper layers get higher sparsity (more redundant)
- Width-wise sparsity: thinner layers with higher per-layer sparsity
- Attention head pruning: remove entire attention heads in sequential models

### Structured Patterns for Hardware Efficiency

| Pattern | Description | Hardware Benefit |
|---------|-------------|-----------------|
| Block sparsity | Prune contiguous blocks of weights | Better cache utilization |
| N:M sparsity | 2 of every 4 weights are zero | Tensor Core acceleration |
| Column sparsity | Prune entire columns | Reduces input dimension |
| Block-diagonal | Prune off-diagonal blocks | Reduces cross-layer communication |

---

## Measuring Pruning Quality

### Metrics

- **Sparsity**: fraction of zero parameters
- **Compression ratio**: original size / pruned size
- **Quality retention**: pruned metric / original metric (target > 99%)
- **Speedup**: actual inference speedup (may be less than compression ratio due to overhead)
- **Memory reduction**: actual GPU/CPU memory reduction

### Evaluation Protocol

1. Prune to target sparsity
2. Fine-tune to convergence
3. Evaluate on held-out test set (not used during pruning or fine-tuning)
4. Compare against original model on identical data and metrics
5. Measure actual inference latency on target hardware
6. Verify no fairness or bias degradation from pruning

### Common Pitfalls

- Evaluating only on training data (pruning can overfit to training set)
- Not accounting for sparse matrix overhead in real inference
- Pruning embedding tables too aggressively (cold-start degradation)
- Ignoring fairness implications of removing features for specific user groups
