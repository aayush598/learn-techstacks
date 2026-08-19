# Neural Architecture Search for Recommendation Models

## Overview

Neural Architecture Search (NAS) automates the design of neural network architectures, replacing manual expert intuition with systematic exploration. For recommendation systems, NAS can discover optimal combinations of feature interaction layers, attention mechanisms, and embedding strategies that human designers might not consider. This covers search space design, efficient NAS algorithms, and production considerations.

---

## Search Space Design for Recommendation Models

### Component Search Spaces

**Feature Interaction Space**:
- Number of cross-network layers: [1, 2, 3, 4, 5, 6]
- Interaction type per layer: {cross, attention, bilinear, field-aware}
- Residual connections: {none, skip-1, skip-2, dense}
- Feature grouping strategy: {none, field-group, adaptive}

**Embedding Space**:
- Embedding dimension per feature group: [16, 32, 64, 128, 256]
- Embedding sharing: {independent, shared, hierarchical}
- Feature hashing: {none, hash-10k, hash-100k}

**Sequence Modeling Space**:
- Architecture type: {Transformer, GRU, TCN, self-attention}
- Number of attention layers: [1, 2, 3, 4]
- Attention heads: [2, 4, 8, 16]
- Sequence length: [20, 50, 100, 200]
- Positional encoding: {learned, sinusoidal, relative}

**Output Space**:
- Tower architecture: {MLP, ResNet, highway}
- Tower depth: [1, 2, 3, 4, 5]
- Tower width: [64, 128, 256, 512]
- Output activation: {sigmoid, softmax, identity}

### Hierarchical Search Spaces

- Level 1: Overall architecture topology (which components to include)
- Level 2: Component hyperparameters (depth, width, type)
- Level 3: Training hyperparameters (learning rate, regularization)
- Search at each level sequentially or jointly

### Search Space Constraints

- Minimum parameter count: prevent degenerate architectures
- Maximum latency budget: ensure inference SLA compliance
- Memory constraints: embedding table size limits
- Compatibility rules: some architecture choices are mutually exclusive

---

## DARTS (Differentiable Architecture Search)

### Core Mechanism

DARTS relaxes the discrete architecture choice into a continuous optimization problem using architecture parameters α:

```
Output = Σ softmax(αᵢ) × opᵢ(input)
```

Where opᵢ represents all candidate operations applied in parallel, and α determines the mix.

### DARTS Training Loop

1. Initialize architecture parameters α randomly
2. Split training data into training and validation sets
3. Alternate between:
   - Update model weights w on training set (standard gradient descent)
   - Update architecture parameters α on validation set (gradient ascent)
4. After convergence, discretize: select the operation with highest α per edge

### DARTS Variants for Recommendation Models

| Variant | Key Change | Benefit |
|---------|-----------|---------|
| DARTS- | Drop operations with low α early | Reduces search cost |
| P-DARTS | Progressive depth search | Better for deep architectures |
| GDAS | Gumbel-Softmax for discrete sampling | More stable training |
| fair DARTS | Uniform operation selection during search | Reduces skip-connection bias |
| SDARTS | Stochastic during search | Better exploration |

### Limitations of DARTS

- **Skip-connection bias**: DARTS tends to select skip connections disproportionately
- **Performance collapse**: Architecture may degrade after convergence
- **Memory intensive**: Must store all candidate operations simultaneously
- **Search space dependent**: Quality of results depends heavily on search space design

---

## Weight Sharing and One-Shot NAS

### Supernet Approach

1. Build a supernet containing all candidate architectures as subgraphs
2. Train the supernet once (shared weights across all sub-architectures)
3. Evaluate candidate architectures by loading shared weights (zero-cost)
4. Fine-tune the top candidates for final evaluation

### Weight Sharing Strategies

- **Path sharing**: Operations on the same edge share weights across architectures
- **Progressive shrinking**: Train full supernet, then progressively remove weak paths
- **Fair sampling**: Equal training time for all architecture paths
- **Hardware-aware sampling**: Sample architectures proportional to hardware efficiency

### Evaluation Without Training

| Method | Description | Correlation with Final Performance |
|--------|-------------|-------------------------------------|
| Zero-cost proxies | Score architecture using first-order gradients | Moderate (ρ ≈ 0.5-0.7) |
| NASWOT | Count neural network operations (topology) | Low-moderate (ρ ≈ 0.4-0.6) |
| Training curve extrapolation | Predict final performance from early epochs | High (ρ ≈ 0.7-0.9) |
| Weight sharing accuracy | Accuracy using shared weights | High (ρ ≈ 0.8-0.9) |

---

## Hardware-Aware NAS

### Multi-Objective Optimization

Optimize jointly for accuracy and efficiency:
- Accuracy: NDCG@10, AUC, log-loss
- Latency: inference time per request (ms)
- Memory: model size (MB), embedding table size
- FLOPs: computational cost per forward pass

### Latency Prediction

- Build a latency lookup table for individual operations
- Sum operation latencies to estimate total inference time
- Account for memory bandwidth bottlenecks (embedding lookups)
- Validate predictions with actual measurements on target hardware

### Pareto-Optimal Architecture Selection

- Plot accuracy vs. latency Pareto front
- Select architecture based on deployment constraints:
  - Strict latency SLA: choose fastest architecture above accuracy threshold
  - No latency constraint: choose highest accuracy
  - Balanced: choose knee of Pareto front

### Hardware-Specific Optimizations

| Target Hardware | Optimization Focus |
|----------------|-------------------|
| GPU (server) | Maximize parallelism, tensor core utilization |
| CPU (server) | Minimize FLOPs, optimize cache usage |
| Mobile/Edge | Model size, latency, power consumption |
| Edge TPU | Quantization-friendly operations only |

---

## Efficient NAS Strategies

### Progressive NAS

1. Search simple architectures first (shallow, narrow)
2. Use found architecture as a building block
3. Search for deeper/wider combinations
4. Progressive complexity prevents collapse

### Bayesian Optimization for NAS

- Use BO to guide architecture search instead of random or grid
- Build surrogate model of architecture performance
- Acquisition function balances exploration and exploitation
- Sample-efficient: finds good architectures with fewer evaluations

### Reinforcement Learning for NAS

- Controller RNN generates architecture descriptions
- Train evaluated architecture, report reward (validation accuracy)
- Update controller via REINFORCE or PPO
- Historical approach (NASNet, ENAS); largely superseded by DARTS

### Evolutionary NAS

- Maintain population of architectures
- Mutate/crossover to generate offspring
- Evaluate and select best architectures
- Regularization evolution: jointly search architecture and regularization

---

## Practical NAS Workflow for Recommendation Models

### Phase 1: Search Space Definition

1. Analyze existing best-performing architecture
2. Identify components to search (feature interaction, attention, tower)
3. Define constraints (latency, memory, parameter count)
4. Validate search space with random sampling

### Phase 2: Architecture Search

1. Use DARTS or one-shot NAS for primary search
2. Run for 200-500 architecture evaluations
3. Track Pareto front of accuracy vs. efficiency
4. Apply early stopping to unpromising architectures

### Phase 3: Candidate Selection and Validation

1. Select top-10 architectures from Pareto front
2. Train each from scratch (no weight sharing) for 3-5 seeds
3. Compare with baseline architecture
4. Select final architecture based on mean ± std of metrics

### Phase 4: Production Deployment

1. Fine-tune winning architecture on full training data
2. Export to serving format (ONNX, TorchScript)
3. Benchmark inference latency on production hardware
4. A/B test against current production model

---

## Common Pitfalls

- **Overfitting to search proxy**: Architecture that performs well under weight sharing may not train well independently
- **Overfitting to validation set**: Search uses validation set as oracle; may overfit to it
- **Ignoring data pipeline**: NAS-optimized architecture may have expensive data preprocessing
- **Search cost exceeding training cost**: NAS can be more expensive than training the final model multiple times
- **Reproducibility**: Different random seeds can yield different architectures; always report multiple runs
