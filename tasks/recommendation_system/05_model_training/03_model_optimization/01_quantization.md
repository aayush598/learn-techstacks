# Model Quantization for Serving

## Overview

Model quantization reduces the numerical precision of model parameters and computations, enabling faster inference, lower memory usage, and reduced energy consumption. For recommendation systems serving millions of requests per second, quantization is a critical optimization that can reduce serving costs by 2-4× with minimal quality degradation.

---

## Numerical Precision Formats

### Format Comparison

| Format | Bits | Range | Precision | Speedup vs FP32 | Use Case |
|--------|------|-------|-----------|-----------------|----------|
| FP32 | 32 | ±3.4×10³⁸ | ~7 decimal digits | 1× (baseline) | Training, master weights |
| FP16 | 16 | ±65504 | ~3 decimal digits | 2-3× | Training, inference |
| BF16 | 16 | ±3.4×10³⁸ | ~3 decimal digits | 2-3× | Training, inference |
| TF32 | 19 | ±3.4×10³⁸ | ~3 decimal digits | 2× (A100) | A100 default |
| FP8 (E4M3) | 8 | ±448 | ~1-2 digits | 4-8× | H100 inference |
| FP8 (E5M2) | 8 | ±57344 | Lower | 4-8× | Gradient communication |
| INT8 | 8 | -128 to 127 | Integer only | 3-4× | Inference |
| INT4 | 4 | -8 to 7 | Integer only | 6-8× | Edge deployment |
| NF4 | 4 | NormalFloat | Quantized | 6-8× | QLoRA fine-tuning |

### Precision-Performance Tradeoff

```
Accuracy
  ↑
  │  ████ FP32 (baseline)
  │  ████ BF16 (~0% loss)
  │  ████ FP16 (~0.01% loss)
  │  ████ INT8 (~0.1-0.5% loss)
  │  ████ INT4 (~0.5-2% loss)
  └──────────────────────────→ Speed
```

---

## Post-Training Quantization (PTQ)

### Overview

PTQ quantizes a pre-trained model without retraining. It's fast (minutes to hours) and requires only a small calibration dataset.

### Uniform Quantization

The most common approach maps floating-point values to integers uniformly:

```
Quantize: q = round(x / scale + zero_point)
Dequantize: x ≈ scale × (q - zero_point)

Where:
  scale = (x_max - x_min) / (q_max - q_min)
  zero_point = round(-x_min / scale)
```

### Per-Tensor vs Per-Channel Quantization

| Method | Description | Quality | Overhead |
|--------|-------------|---------|----------|
| Per-tensor | One scale/zero_point per tensor | Lower | Minimal |
| Per-channel | One scale/zero_point per output channel | Higher | Small |
| Per-group | One scale/zero_point per group of channels | Highest | Moderate |

**Recommendation:** Per-channel quantization is the standard choice for weight quantization.

### Quantization Granularity for Embeddings

Recommendation models have large embedding tables. Quantization strategies:

| Strategy | Description | Memory Reduction |
|----------|-------------|-----------------|
| Per-row quantization | Each embedding row has its own scale | 2-4× |
| Per-table quantization | One scale per embedding table | 2-4× (simpler) |
| Clustering | Cluster embeddings, store centroids | 8-16× |
| Product quantization | Split vectors, quantize sub-vectors | 8-32× |

### INT8 Calibration

Calibration determines the quantization ranges using a small representative dataset:

#### Calibration Methods

| Method | Description | Quality | Speed |
|--------|-------------|---------|-------|
| Min-Max | Use observed min/max as range | Poor (outliers) | Fast |
| Percentile | Use 99.99th percentile as range | Good | Fast |
| KL-Divergence | Minimize KL divergence between FP32 and INT8 distributions | Excellent | Moderate |
| MSE | Minimize mean squared error | Very Good | Moderate |
| Entropy | Minimize information loss | Excellent | Slow |

#### Calibration Dataset

- 500–1000 representative samples typically sufficient
- Must reflect the actual serving data distribution
- Include edge cases and long-tail items
- Re-calibrate periodically if data distribution shifts

### Accuracy Recovery Techniques

| Technique | Description | Effectiveness |
|-----------|-------------|--------------|
| Sensitivity analysis | Identify layers sensitive to quantization | Essential first step |
| Mixed-precision | Keep sensitive layers in higher precision | High |
| Equalization | Equalize weight/activation ranges across layers | Moderate |
| SmoothQuant | Migrate quantization difficulty from activations to weights | High |

---

## Quantization-Aware Training (QAT)

### Overview

QAT simulates quantization during training, allowing the model to learn to compensate for quantization error. Generally produces better results than PTQ, especially at low bit widths.

### QAT Process

```
Forward pass:
  Full-precision weights → Fake quantization → Quantized forward pass
  
Fake quantization:
  x_q = clamp(round(x / scale), q_min, q_max)
  x_approx = x_q × scale
  
Backward pass:
  Straight-through estimator (STE) for round() and clamp()
  ∂L/∂x ≈ ∂L/∂x_approx (gradients pass through as if no quantization)
```

### QAT Configuration

| Parameter | Typical Value | Notes |
|-----------|--------------|-------|
| Quantization start epoch | 5-10 | Let model warm up in FP32 |
| Learning rate for QAT | 0.1-1× of original LR | Lower LR often helps |
| Quantization-aware batch norm | Frozen or updated | Depends on sensitivity |
| Calibration data | Same as training data | Must be representative |

### PTQ vs QAT Comparison

| Aspect | PTQ | QAT |
|--------|-----|-----|
| Training required | No | Yes |
| Time to deploy | Minutes-hours | Hours-days |
| Accuracy at INT8 | 99-100% of FP32 | 99.5-100% of FP32 |
| Accuracy at INT4 | 95-98% of FP32 | 98-99.5% of FP32 |
| Implementation complexity | Low | Moderate |
| Recommended bit width | ≥ INT8 | INT4+ possible |

---

## TensorRT Quantization

### TensorRT Pipeline

```
PyTorch/TensorFlow Model
      ↓
ONNX Export
      ↓
TensorRT Parser
      ↓
Layer Fusion + Optimization
      ↓
Calibration (INT8)
      ↓
Quantized Engine (.plan)
      ↓
TensorRT Runtime
```

### TensorRT Optimization Levels

| Level | Optimizations | Quality | Speed |
|-------|--------------|---------|-------|
| FP32 mode | Layer fusion only | Best | Baseline |
| FP16 mode | FP16 kernels | Very good | 2× faster |
| INT8 mode | INT8 quantization + calibration | Good | 3-4× faster |
| INT8 + sparsity | INT8 + structured sparsity | Moderate | 5-6× faster |

### Recommendation Model Considerations

| Component | Quantization Strategy | Rationale |
|-----------|----------------------|-----------|
| Embedding tables | INT8 or INT4 with per-row scale | Large memory; robust to quantization |
| Dense layers | INT8 with per-channel scale | Standard quantization |
| Attention layers | FP16 or INT8 (sensitive) | Computationally critical |
| Output logits | FP32 or FP16 | Precision matters for ranking |

### TensorRT Plugin System

- Custom plugins for unsupported operations (e.g., sparse attention)
- Write plugins in C++ for maximum performance
- Register plugins with TensorRT builder

---

## Performance vs Accuracy Tradeoffs

### Measurement Framework

For each quantization configuration, measure:

| Metric | Description | Acceptable Degradation |
|--------|-------------|----------------------|
| NDCG@10 | Ranking quality | < 0.5% drop |
| HR@20 | Hit rate | < 1% drop |
| Throughput | Requests/sec | 2-4× improvement |
| Latency (P50/P99) | Response time | < same or better |
| Memory usage | GPU/CPU memory | 2-4× reduction |
| Power consumption | Energy per inference | 2-3× reduction |

### Quantization Impact by Model Type

| Model Type | INT8 Impact | INT4 Impact | Notes |
|-----------|------------|------------|-------|
| Matrix Factorization | Minimal | Low | Simple dot products |
| DeepFM | Low | Moderate | Embedding table sensitive |
| Transformer-based | Low-Moderate | Moderate-High | Attention sensitive |
| Wide & Deep | Low | Moderate | Wide part robust |
| Graph Neural Networks | Moderate | High | Message passing sensitive |

### Decision Matrix

```
                         Quality Required
                    Low         Medium        High
                ┌───────────┬───────────┬───────────┐
    Latency     │           │           │           │
    Constraint  │ INT4 PTQ  │ INT8 PTQ  │ INT8 QAT  │
    < 5ms       │           │           │           │
                ├───────────┼───────────┼───────────┤
    Latency     │           │           │           │
    Constraint  │ INT4 QAT  │ INT8 QAT  │ FP16      │
    < 1ms       │           │           │           │
                ├───────────┼───────────┼───────────┤
    Latency     │           │           │           │
    No limit    │ FP16      │ FP16      │ FP32      │
                │           │           │           │
                └───────────┴───────────┴───────────┘
```

---

## Quantization for Specific Components

### Embedding Table Quantization

Embedding tables are often the dominant memory consumer in recommendation models.

#### Techniques

1. **INT8 quantization**: Store embeddings as INT8 + per-row scale/zero_point
   - Memory: 4 bytes → 2 bytes per dimension (2× reduction)
   - Quality: Usually negligible impact

2. **INT4 quantization**: Store embeddings as INT4 + per-row scale
   - Memory: 4 bytes → 1 byte per dimension (4× reduction)
   - Quality: May need fine-tuning to recover quality

3. **Mixed-dimension embeddings**: Use lower precision for less important dimensions
   - PCA-based: Quantize lower-variance dimensions more aggressively

4. **Embedding table pruning**: Remove low-impact embeddings (rare items)
   - Combine with quantization for maximum compression

### Dense Layer Quantization

| Layer Type | INT8 Quality | FP16 Quality | Recommendation |
|-----------|-------------|-------------|----------------|
| Embedding projection | Excellent | Excellent | INT8 |
| Attention QKV | Good | Excellent | INT8 or FP16 |
| Feed-forward | Excellent | Excellent | INT8 |
| Output projection | Good | Excellent | INT8 |
| Batch norm | N/A (fuse) | Excellent | Fuse into adjacent layers |

---

## Deployment Patterns

### Offline Quantization Pipeline

```
Train FP32 model
      ↓
Export to ONNX
      ↓
Run calibration dataset through TensorRT/ONNX Runtime
      ↓
Generate quantized model
      ↓
Validate quality on test set
      ↓
Deploy to serving infrastructure
```

### A/B Testing Quantized Models

```
Traffic Split:
  20% → FP32 model (reference)
  40% → INT8 PTQ model
  40% → INT8 QAT model

Metrics tracked:
  - NDCG@10 (offline proxy)
  - CTR (online)
  - P99 latency
  - GPU memory usage
  - Cost per 1K predictions
```

### Monitoring Post-Quantization

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Quality drop | > 1% NDCG drop | Investigate, consider QAT |
| Latency increase | > 10% increase | Check TensorRT optimization |
| Throughput decrease | > 5% decrease | Review batch size settings |
| Error rate increase | Any increase | Roll back to FP16/FP32 |

---

## Emerging Techniques

### Weight-Only Quantization

- Quantize weights only, keep activations in FP16
- Dequantize weights at runtime before computation
- W4A16 (4-bit weights, 16-bit activations) is a popular configuration
- Libraries: GPTQ, AWQ, bitsandbytes

### Mixture of Precision

- Different layers get different quantization levels
- Sensitive layers stay in FP16/FP32
- Less sensitive layers go to INT8/INT4
- Automated with tools like NVIDIA AMMO

### Sparsity-Aware Quantization

- Combine structured sparsity (2:4 pattern) with quantization
- Remove 50% of weights (set to zero in structured pattern)
- Quantize remaining weights to INT8
- Combined speedup: up to 6× over FP32
