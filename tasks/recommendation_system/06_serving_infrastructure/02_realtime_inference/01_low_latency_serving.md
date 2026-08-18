# Low-Latency Model Serving

## Overview

Low-latency serving is critical for recommendation systems where predictions must be generated within strict time budgets (typically 1-50ms) to maintain user experience. This document covers batching strategies, model optimization, GPU memory management, request scheduling, and cold start mitigation techniques for achieving sub-50ms recommendation serving at scale.

---

## Latency Budgets

### End-to-End Request Flow

```
User Action (click/scroll)
      ↓ [1-5ms]  Network (client → API gateway)
API Gateway + Auth
      ↓ [1-2ms]  Request processing
Feature Extraction
      ↓ [2-5ms]  Feature store lookup
Model Inference
      ↓ [1-10ms] Model prediction
Post-processing + Filtering
      ↓ [1-3ms]  Business rules, dedup, diversity
Response (API gateway → client)
      ↓ [1-5ms]  Network
Total: 7-30ms
```

### Latency Targets by Use Case

| Use Case | P50 Target | P99 Target | Throughput |
|----------|-----------|-----------|------------|
| Homepage recommendations | < 50ms | < 100ms | 100K QPS |
| Search results ranking | < 20ms | < 50ms | 50K QPS |
| "Next item" prediction | < 10ms | < 20ms | 200K QPS |
| Notification trigger | < 100ms | < 500ms | 10K QPS |
| Email batch generation | Minutes | Hours | Batch |

---

## Batching Strategies

### Dynamic Batching

Group incoming requests into batches for efficient GPU execution:

```
Time →
Request 1: ─────────────────────────────────────
Request 2:    ──────────────────────────────────
Request 3:       ───────────────────────────────
Request 4:          ────────────────────────────
          ↑ wait    ↑ batch executes
          (2ms)     (1ms on GPU)
```

#### Configuration Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| Preferred batch size | Optimal batch size for throughput | 16, 32, 64 |
| Maximum batch size | Hard limit on batch size | 64, 128, 256 |
| Maximum queue delay | Max wait time before executing incomplete batch | 1-5ms |
| Batch timeout | Force batch execution after timeout | 2-10ms |

#### Latency-Throughput Tradeoff

```
Latency
  ↑
  │    *
  │      *
  │        *  ← Sweet spot (batch=32)
  │          *
  │            *
  │              *
  └──────────────────→ Throughput

Increasing batch size:
  ↑ Throughput (better GPU utilization)
  ↑ Latency (longer wait + compute time)
```

### Request Batching Patterns

| Pattern | Description | Latency Impact | Throughput Gain |
|---------|-------------|---------------|-----------------|
| Time-based batching | Collect requests for N ms | +N ms latency | 3-5× |
| Size-based batching | Collect until N requests | Variable latency | 4-8× |
| Adaptive batching | Dynamic based on load | Minimal | 3-6× |
| Prefetch batching | Pre-compute popular items | Near zero | 2-3× (cache hit) |

### Batching for Embedding-Heavy Models

Recommendation models often have large embedding tables that don't benefit from batching in the same way as dense models:

- **Embedding lookup**: Not batch-efficient (random memory access)
- **Dense layers**: Highly batch-efficient (matrix multiplication)
- **Solution**: Batch embedding lookups, then batch dense computation

```
Step 1: Collect all user_ids and item_ids from batch
Step 2: Batch embedding lookup (coalesce for cache efficiency)
Step 3: Batch dense forward pass
Step 4: Split results back to individual requests
```

---

## Model Optimization for Latency

### Architecture-Level Optimizations

| Technique | Latency Reduction | Quality Impact | Implementation |
|-----------|------------------|----------------|----------------|
| Knowledge distillation | 2-5× (smaller model) | 1-3% quality drop | Train student model |
| Embedding pruning | 10-30% | < 1% | Remove low-impact embeddings |
| Early exit | 20-50% (easy cases) | < 0.5% | Confidence-based early return |
| Feature selection | 10-30% | < 1% | Remove non-informative features |
| Model architecture search | Variable | None | NAS for latency constraints |

### Knowledge Distillation for Latency

```
Teacher Model (complex, slow, high quality)
      ↓ soft targets
Student Model (simple, fast, near-teacher quality)

Teacher: Transformer with 12 layers, 768 hidden → 50ms
Student: 2-layer MLP, 256 hidden → 3ms (16× faster)
Quality: 98% of teacher NDCG
```

### Embedding Optimization

| Technique | Speedup | Memory Savings | Quality Impact |
|-----------|---------|---------------|----------------|
| Embedding quantization (INT8) | 1.5× lookup | 2× | Negligible |
| Hash-based embeddings | 2× lookup | Configurable | Small table collision |
| Embedding clustering | 3-5× lookup | 5-10× | Moderate |
| Locality-sensitive hashing | Sub-linear lookup | Moderate | Approximate only |

### Operator Fusion

Combine multiple operations into a single kernel:

| Fusion Pattern | Operations Fused | Speedup |
|---------------|-----------------|---------|
| Embedding + Linear | Look up → matmul | 1.2-1.5× |
| Linear + ReLU + Dropout | Three kernels → one | 1.3-1.8× |
| Attention fusion | QK^T → softmax → ×V | 1.5-2× |
| LayerNorm fusion | Mean, variance, normalize | 1.2-1.5× |

---

## GPU Memory Management

### Memory Layout for Recommendation Models

```
GPU Memory (80 GB A100)
├── Model Parameters (~2-10 GB)
│   ├── Embedding tables (~1-8 GB) ← largest component
│   ├── Dense layer weights (~0.1-1 GB)
│   └── Bias terms (~0.01 GB)
├── KV Cache (for transformers, ~0.5-4 GB)
├── Activation Memory (during forward pass, ~0.1-1 GB)
├── CUDA Overhead (~0.5-1 GB)
└── Available for batching (~60-75 GB)
```

### Embedding Table Management

Embedding tables often don't fit in GPU memory. Strategies:

| Strategy | Description | Latency | Memory |
|----------|-------------|---------|--------|
| GPU-resident | Entire table on GPU | Lowest | High |
| CPU-offload + cache | Table on CPU, cache hot entries | Moderate | Low GPU |
| SSD-offload | Table on NVMe SSD | Higher | Minimal GPU |
| Sharded | Table split across GPUs | Low | Distributed |

### KV-Cache Management (Transformers)

For autoregressive models serving multiple users:

```
Total KV cache = 2 × num_layers × num_heads × head_dim × seq_len × batch_size × dtype_size

Example: 12 layers × 8 heads × 64 dim × 100 seq × 32 batch × FP16
       = 2 × 12 × 8 × 64 × 100 × 32 × 2 bytes = 75 MB
```

#### Paged KV Cache

Inspired by virtual memory:
- Allocate KV cache in fixed-size pages
- Pages don't need to be contiguous in memory
- Share pages across requests with common prefixes
- Reclaim pages when requests complete

### Memory Fragmentation

- **Problem**: Frequent allocation/deallocation of varying-size tensors fragments GPU memory
- **Solution**: Pre-allocate memory pools for common tensor sizes
- **PyTorch**: Use `torch.cuda.memory_stats()` to monitor fragmentation
- **CUDA**: Use memory pool allocators (e.g., PyTorch's caching allocator)

---

## Request Scheduling

### Scheduling Algorithms

| Algorithm | Description | Latency | Throughput | Fairness |
|-----------|-------------|---------|-----------|----------|
| FIFO | First in, first out | Variable | Moderate | Fair |
| Round Robin | Rotate through request types | Predictable | Moderate | Fair |
| Priority | Higher priority requests first | Low for high priority | High | Unfair |
| Shortest Job First | Estimate compute, schedule shortest first | Low average | High | Can starve |
| Fair Share | Equal GPU time per user/client | Bounded | Moderate | Fair |

### Priority Levels

```
Priority 1 (Critical):  Real-time predictions (homepage, search)
Priority 2 (High):      Session-based updates, "next item"
Priority 3 (Medium):    Email/notification recommendations
Priority 4 (Low):       Batch re-scoring, model evaluation
```

### Preemption

- Allow high-priority requests to preempt low-priority ones
- Save partial computation state for preempted requests
- Resume preempted requests when GPU is available
- Implement via request cancellation tokens

---

## Pre-warming and Model Loading

### Pre-warming Strategy

```
Service Start →
  Load model weights to CPU memory (10-30s)
  → Load model to GPU (5-15s)
  → Warm-up inference (1-5s)
  → Ready to serve

Total cold start: 15-50s (model dependent)
```

### Pre-loading Techniques

| Technique | Description | Cold Start Reduction |
|-----------|-------------|---------------------|
| Model pre-loading | Load at service startup | Essential |
| Warm-up requests | Send dummy requests to initialize CUDA | 1-3s |
| Snapshot/restore | Save GPU state, restore on start | 2-5s |
| Shared memory | Load model once, share across processes | Eliminates duplicate loading |
| Container image caching | Keep model in container layer | Reduces download time |

### Model Caching

```
Multi-level cache:
├── L1: GPU memory (hot models, < 1ms)
├── L2: CPU memory (warm models, 5-50ms)
├── L3: SSD/NVMe (cold models, 100-500ms)
└── L4: Object storage (archived models, 1-10s)
```

Cache eviction policies:
- **LRU**: Least Recently Used (most common)
- **LFU**: Least Frequently Used
- **TTL**: Time-to-live based expiration
- **Size-aware**: Evict largest models first when memory is full

---

## Cold Start Mitigation

### Types of Cold Start

| Type | Description | Duration | Impact |
|------|-------------|----------|--------|
| Service cold start | Container/pod restart | 15-50s | All requests affected |
| Model cold start | New model deployment | 5-15s | New model requests |
| GPU cold start | GPU not initialized | 2-5s | First GPU request |
| Feature cold start | New user/item features | N/A | Feature pipeline |
| User cold start | New user | N/A | Personalization quality |

### Mitigation Strategies

#### Infrastructure Level

| Strategy | Implementation | Effectiveness |
|----------|---------------|---------------|
| Always-on instances | Keep minimum replicas running | Eliminates cold start |
| Pre-scaling | Scale up before predicted load | Prevents cold start |
| Model warm-up endpoints | Dedicated endpoint to trigger loading | Reduces warm-up time |
| GPU persistence | Keep GPU context alive across requests | Eliminates GPU init |
| Sidecar pre-loading | Load model in sidecar container | Parallel loading |

#### Application Level

| Strategy | Implementation | Effectiveness |
|----------|---------------|---------------|
| Fallback model | Use simpler model during cold start | Maintains availability |
| Cached predictions | Return cached results for common requests | Hides latency |
| Progressive loading | Load critical layers first, serve partial model | Reduces TTFB |
| Async initialization | Accept requests while model loads | Reduces perceived latency |

---

## Monitoring and Alerting

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|----------------|
| P50 latency | Median response time | > target × 1.5 |
| P99 latency | 99th percentile response time | > target × 2 |
| P999 latency | 99.9th percentile response time | > target × 3 |
| Throughput | Requests per second | < 80% of capacity |
| GPU utilization | Percentage of GPU compute used | < 30% or > 95% |
| GPU memory | Percentage of GPU memory used | > 90% |
| Batch size | Average batch size | Monitor trends |
| Queue depth | Requests waiting in queue | > 100 |
| Error rate | Failed requests percentage | > 0.1% |
| Cold start count | Number of cold starts per hour | > expected |

### Dashboard Design

```
Row 1: Throughput (QPS) | Latency Distribution | Error Rate
Row 2: GPU Utilization | GPU Memory | Batch Size
Row 3: Model Load Time | Queue Depth | Active Instances
Row 4: Feature Lookup Latency | Model Inference Latency | E2E Latency
```

---

## Performance Engineering Checklist

1. **Profile first**: Identify actual bottlenecks (embedding lookup, dense compute, network)
2. **Batch effectively**: Find the optimal batch size for your latency budget
3. **Quantize models**: INT8 quantization with < 1% quality loss
4. **Optimize embeddings**: Quantize, prune, or hash-embed large tables
5. **Pre-warm everything**: Models, GPU contexts, feature caches
6. **Use mixed precision**: FP16/BF16 for computation, FP32 for critical operations
7. **Cache aggressively**: Popular recommendations, feature values, embedding lookups
8. **Monitor continuously**: Track latency percentiles, not just averages
9. **Load test regularly**: Verify performance at 2× expected peak load
10. **Plan for failure**: Graceful degradation, fallback models, circuit breakers
