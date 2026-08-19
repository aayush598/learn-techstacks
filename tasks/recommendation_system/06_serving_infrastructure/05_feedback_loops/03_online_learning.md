# Online Learning for Recommendation Systems

## Overview

Online learning continuously updates model parameters as new data arrives, rather than retraining in discrete batches. For recommendation systems, this enables real-time adaptation to changing user preferences, trending content, and shifting behavior patterns. This covers continuous updates, online gradient descent, federated learning, concept drift, and stability-plasticity tradeoffs.

---

## Continuous Model Updates

### Update Granularity

| Level | Frequency | Latency | Complexity |
|-------|-----------|---------|-----------|
| Per-interaction | Real-time | < 100ms | Very high |
| Micro-batch | Seconds | 1-10s | High |
| Mini-batch | Minutes | 1-10 min | Medium |
| Hourly batch | Hourly | 1 hour | Low |

### Per-Interaction Updates

- Update model after each user interaction (click, purchase, skip)
- Immediate adaptation to user behavior
- High computational overhead per update
- Risk of instability from noisy individual signals

### Micro-Batch Updates

- Collect interactions for 1-10 seconds
- Compute aggregate gradient from micro-batch
- Update model parameters
- Balance between freshness and stability

### Implementation Architecture

```
User Event → Event Stream → Online Learning Worker → Model Update → Serving
                    ↓
              Feature Store → Feature Update
```

---

## Online Gradient Descent

### Standard Online GD

```
w_t+1 = w_t - η_t × ∇L(x_t, y_t, w_t)
```

Where:
- w_t = model weights at time t
- η_t = learning rate at time t
- (x_t, y_t) = training example at time t
- ∇L = gradient of loss

### Learning Rate Scheduling

| Strategy | Formula | Properties |
|----------|---------|-----------|
| Constant | η_t = η_0 | Simple, may oscillate |
| Decay | η_t = η_0 / √t | Converges, slow adaptation |
| Adaptive | Per-parameter (Adam-style) | Handles varying gradient magnitudes |
| Warm restart | η_t cycles periodically | Escapes local minima |

### Stochastic Variance Reduced Gradient (SVRG)

- Maintain periodic full gradient snapshot
- Reduce variance of stochastic gradient estimates
- More stable than vanilla online GD
- Better convergence for non-convex objectives

### Application to Embedding Updates

- Update only accessed embeddings per interaction
- Use sparse gradient updates (only modify non-zero gradients)
- Apply embedding regularization to prevent overfitting to recent interactions
- Manage memory for frequently accessed vs rarely accessed embeddings

---

## Federated Online Learning

### Architecture

```
Device → Local Training → Model Update → Aggregation Server → Global Model → Devices
```

### Federated Averaging (FedAvg)

1. Server sends current global model to selected devices
2. Each device trains on local data for multiple steps
3. Devices send model updates to server
4. Server averages updates to produce new global model
5. Repeat

### Federated Recommendations

- Each user's device trains on their own interaction history
- Model updates (gradients) sent to server, not raw data
- Server aggregates across many users
- Updated model pushed to all devices

### Communication Efficiency

- **Gradient compression**: Quantize gradients before sending
- **Gradient sparsification**: Only send top-k gradient values
- **Local steps**: More training on device before sending update
- **Model distillation**: Send distilled knowledge instead of full gradients

### Privacy Preservation

- **Differential privacy**: Add calibrated noise to updates
- **Secure aggregation**: Encrypt updates so server only sees aggregate
- **Trusted execution environment**: Process updates in secure hardware
- **Gradient clipping**: Bound individual contribution magnitude

---

## Concept Drift Adaptation

### Types of Concept Drift

| Type | Description | Example |
|------|-------------|---------|
| Sudden | Immediate change in distribution | New trending topic |
| Gradual | Slow shift over time | Seasonal preference change |
| Incremental | Continuous small changes | Evolving fashion trends |
| Recurring | Cycles that repeat | Daily/weekly patterns |
| Out-of-concept | Temporary deviation | Holiday behavior |

### Drift Detection Methods

**Statistical Tests**:
- Page-Hinkley test: detect mean shift in stream
- ADWIN (Adaptive Windowing): detect distribution change
- KS test: detect distribution shift between windows

**Performance Monitoring**:
- Track model performance over time
- Alert when performance drops below threshold
- Compare recent vs historical performance

**Feature Drift Detection**:
- Monitor feature distributions (PSI, KL divergence)
- Detect when input distribution changes significantly
- Trigger model update when drift detected

### Adaptation Strategies

| Strategy | Response Time | Stability | Best For |
|----------|-------------|-----------|----------|
| Full retrain | Hours-days | High | Slow drift |
| Incremental update | Minutes-hours | Medium | Moderate drift |
| Online learning | Real-time | Low | Fast drift |
| Ensemble refresh | Hours | High | Various drift types |

---

## Stability-Plasticity Tradeoff

### The Dilemma

- **Stability**: Retain knowledge from old data (don't forget)
- **Plasticity**: Adapt to new data quickly (learn new patterns)
- Too stable: model doesn't adapt to new preferences
- Too plastic: model forgets important historical patterns

### Balancing Strategies

**Elastic Weight Consolidation (EWC)**:
- Identify important weights for old tasks
- Apply regularization to protect important weights
- Allow non-important weights to change freely
- Balance between old knowledge retention and new learning

**Learning Rate Separation**:
- Different learning rates for different model components
- Embeddings: lower LR (retain learned representations)
- Output layer: higher LR (adapt quickly to new patterns)
- Middle layers: moderate LR

**Ensemble Approaches**:
- Maintain multiple models trained on different time windows
- Weight predictions by recency and relevance
- Naturally handles stability-plasticity through model diversity

**Memory Replay**:
- Store samples from old data distribution
- Mix old samples with new data during training
- Prevents catastrophic forgetting
- Increases memory requirements

### Practical Guidelines

- Start conservative (lower learning rate, more regularization)
- Monitor for both underfitting (too stable) and overfitting (too plastic)
- Use validation on recent data to measure plasticity
- Use validation on old data to measure stability
- A/B test different stability-plasticity balances

---

## Monitoring Online Learning

### Key Metrics

| Metric | Description | Alert |
|--------|-------------|-------|
| Update frequency | How often model is updated | Below expected rate |
| Gradient norm | Size of parameter updates | Sudden spike |
| Parameter change rate | How much weights change per update | Too high or too low |
| Prediction drift | Distribution of predictions over time | Significant shift |
| Performance trend | Metric over time | Downward trend |

### Online vs Batch Model Comparison

- Maintain batch model as baseline
- Compare online model metrics against batch baseline
- If online model underperforms batch: may need more stability
- If online model outperforms batch: online learning is beneficial

### Safety Mechanisms

- Gradient clipping to prevent large updates
- Maximum update magnitude per time window
- Automatic rollback if performance degrades
- A/B test online model against stable batch model
- Human-in-the-loop approval for significant model changes
