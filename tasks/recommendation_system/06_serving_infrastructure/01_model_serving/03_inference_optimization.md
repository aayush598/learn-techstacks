# Inference Optimization for Recommendation Systems

## Overview

Inference optimization reduces the latency and cost of serving recommendation models at scale. With millions of requests per second, even microsecond improvements per request translate to significant infrastructure savings and improved user experience. This covers operator fusion, kernel optimization, memory optimization, batch scheduling, and latency profiling.

---

## Operator Fusion

### Types of Fusion

| Fusion Type | Description | Speedup |
|-------------|-------------|---------|
| Layer fusion | Merge consecutive layers into single kernel | 10-30% |
| Activation fusion | Fuse activation with preceding layer | 5-15% |
| Attention fusion | Merge Q/K/V projection + attention | 15-25% |
| Batch norm fusion | Fold BN into preceding linear layer | 10-20% |
| Softmax + loss fusion | Merge softmax and cross-entropy | 5-10% |

### Fusion for Recommendation Models

**Embedding + Linear Fusion**:
- Merge embedding lookup with first linear layer
- Reduces memory traffic (embeddings stay in registers)
- Particularly effective for wide-and-deep models

**Feature Interaction Fusion**:
- Fuse cross layers or attention layers into single kernels
- Avoid intermediate tensor materialization
- Reduces memory bandwidth bottleneck

**Multi-Tower Fusion**:
- Execute independent towers in parallel
- Fuse score computation from multiple towers
- Reduce kernel launch overhead

### Implementation

- ONNX Runtime applies fusion automatically during graph optimization
- TensorRT provides comprehensive fusion for NVIDIA GPUs
- Custom CUDA kernels for model-specific fusion patterns
- XLA (Accelerated Linear Algebra) in TensorFlow/JAX for automatic fusion

---

## Kernel Optimization

### Custom CUDA Kernels

For operations where standard libraries are suboptimal:

**Embedding Lookup Kernel**:
- Fused gather + transformation for embedding lookups
- Coalesced memory access for batch embedding lookups
- Shared memory caching for hot embeddings
- Warp-level reduction for attention computation

**Attention Kernel**:
- FlashAttention-style tiled computation
- Online softmax for memory-efficient attention
- Fuse Q/K/V projection with attention computation
- Optimize for sequence lengths typical in recommendations (20-200)

**Score Computation Kernel**:
- Fuse multiple scoring operations into single kernel
- Optimize for batch matrix multiplication patterns
- Use Tensor Cores for mixed-precision scoring

### Kernel Auto-Tuning

- Use Triton for Python-based kernel development
- Auto-tune kernel parameters for target hardware
- Benchmark multiple kernel implementations and select best
- Cache tuned kernels for consistent performance

---

## Memory Optimization

### Inference Memory Layout

| Component | Memory | Optimization |
|-----------|--------|-------------|
| Model weights | Static | Quantize, compress |
| KV cache (attention) | Grows with sequence length | Limit cache size |
| Intermediate activations | Per-request | Minimize with fusion |
| Batch buffers | Proportional to batch size | Pre-allocate |
| Feature cache | Shared across requests | LRU eviction |

### Memory Efficiency Techniques

**Weight Sharing**:
- Share weights across similar model components
- Reduces total memory footprint
- Enables larger batch sizes

**Activation Memory**:
- Recompute activations instead of storing (inference rarely needs backward pass)
- Use in-place operations where possible
- Minimize tensor copies through graph optimization

**KV Cache Optimization**:
- Pre-allocate KV cache for typical batch sizes
- Reuse cache buffers across requests
- Limit maximum sequence length to bound cache size
- Evict old entries for very long sequences

---

## Batch Scheduling

### Dynamic Batching

Group incoming requests into batches for efficient GPU utilization:

**Static Batching**:
- Fixed batch size, fixed timeout
- Simple but may waste resources (partial batches) or add latency (waiting for full batch)

**Dynamic Batching**:
- Adjust batch size based on request arrival rate
- Time-based batching: collect requests for T ms, then process
- Size-based batching: process when batch reaches N requests
- Whichever comes first

**Continuous Batching**:
- Add/remove requests from batch without waiting for batch completion
- Higher GPU utilization than static batching
- More complex implementation
- Used in vLLM-style serving

### Batch Scheduling Parameters

| Parameter | Typical Value | Impact |
|-----------|--------------|--------|
| Max batch size | 64-256 | Higher = better GPU util, more latency |
| Max wait time | 1-10 ms | Lower = lower latency, less batching |
| Max sequence length | 128-512 | Bounds memory per request |
| Priority levels | 2-3 | High-priority requests skip queue |

---

## GPU Utilization Maximization

### Profiling GPU Usage

- **SM utilization**: Target >80% for compute-bound inference
- **Memory bandwidth**: Measure achieved vs peak bandwidth
- **Kernel occupancy**: Number of active warps per SM
- **Occupancy vs registers**: Balance register usage and occupancy

### Bottleneck Analysis

| Symptom | Bottleneck | Solution |
|---------|-----------|----------|
| Low SM utilization | Memory bandwidth | Use smaller batch, fuse ops |
| Low memory bandwidth | Compute bound | Increase batch size, use Tensor Cores |
| High latency, low GPU util | Small batch + overhead | Increase batch size, reduce preprocessing |
| High latency, high GPU util | Model too large | Quantize, prune, distill |

### Multi-Stream Inference

- Use multiple CUDA streams for concurrent request processing
- Overlap data transfer with computation
- Different streams for different request types (real-time vs batch)
- Stream priority for high-priority requests

---

## Latency Profiling

### End-to-End Latency Breakdown

| Component | Typical % | Optimization Target |
|-----------|-----------|-------------------|
| Feature preprocessing | 10-30% | Move to GPU, vectorize |
| Embedding lookup | 15-30% | Cache, quantize, pre-compute |
| Dense forward pass | 20-40% | Fuse ops, quantize |
| Post-processing | 5-15% | Fuse with output layer |
| Network I/O | 5-20% | Connection pooling, compression |

### Latency Measurement

- **P50 latency**: Median; typical experience
- **P95 latency**: Tail latency; most users within this
- **P99 latency**: Extreme tail; SLA compliance
- **P999 latency**: Worst case; infrastructure planning

### Latency Budget Example

For a 50ms SLA:
```
Feature preprocessing:     8 ms (16%)
Embedding lookup:         10 ms (20%)
Dense forward pass:       15 ms (30%)
Post-processing:           5 ms (10%)
Network overhead:         12 ms (24%)
Total:                    50 ms (100%)
```

### Continuous Latency Monitoring

- Track latency percentiles per model version
- Alert on latency regression (> 10% increase)
- Profile latency by request characteristics (batch size, feature count)
- Compare latency across hardware configurations

---

## Production Optimization Checklist

1. **Model level**: Quantize (INT8), prune (50%+), fuse operations
2. **Graph level**: ONNX Runtime / TensorRT graph optimization
3. **Kernel level**: Custom CUDA kernels for hot paths
4. **System level**: Batch scheduling, memory pooling, multi-stream
5. **Infrastructure level**: GPU selection, model parallelism, caching
6. **Monitoring**: Latency dashboards, utilization alerts, regression detection
