# GPU Training for Recommendation Systems

## Overview

Modern recommendation models—deep collaborative filtering, transformer-based sequential models, and multi-modal architectures—demand massive computational resources. GPUs are the backbone of recommendation model training, providing orders-of-magnitude speedup over CPUs for the matrix-heavy operations that define these models. This document covers GPU selection, optimization strategies, and production-grade training practices.

---

## GPU Hardware Landscape

### NVIDIA Data Center GPUs

| GPU | Architecture | VRAM | FP16 TFLOPS | TF32 TFLOPS | NVLink BW | Best For |
|-----|-------------|------|-------------|-------------|-----------|----------|
| A100 40GB | Ampere | 40 GB HBM2e | 312 | 156 | 600 GB/s | Standard training |
| A100 80GB | Ampere | 80 GB HBM2e | 312 | 156 | 600 GB/s | Large embedding tables |
| H100 SXM | Hopper | 80 GB HBM3 | 989 | 494 | 900 GB/s | Next-gen training |
| H100 PCIe | Hopper | 80 GB HBM3 | 756 | 442 | 600 GB/s | Cost-effective Hopper |
| H200 | Hopper | 141 GB HBM3e | 989 | 494 | 900 GB/s | Massive models |

### Key Architectural Differences

- **Ampere (A100)**: Third-generation Tensor Cores, TF32 format for easy FP32 compatibility, MIG support for GPU partitioning, asynchronous memory copy for overlapping compute and data movement
- **Hopper (H100)**: Fourth-generation Tensor Cores, FP8 support (1979 TFLOPS), Transformer Engine for automatic FP8/FP16 mixed precision, thread block clusters, distributed shared memory
- **Recommendation-specific considerations**: Embedding lookups are memory-bandwidth bound, not compute-bound; thus VRAM capacity and HBM bandwidth often matter more than raw TFLOPS

### Why GPUs Dominate Recommendation Training

- Embedding table operations: large gather/scatter operations parallelize well across GPU threads
- Dense component forward/backward passes: matrix multiplications are GPU-native
- Batch processing: millions of training examples per second across large batch sizes
- Multi-head attention in sequential models: parallel attention computation
- Feature interaction networks: cross-network and attention-based interactions benefit from GPU parallelism

---

## CUDA Optimization Fundamentals

### Kernel-Level Optimizations

- **Memory coalescing**: Ensure adjacent threads access adjacent memory addresses for global memory loads/stores; uncoalesced access can cause 10x slowdown
- **Shared memory usage**: Cache frequently accessed data (e.g., small embedding tables, user/item features) in shared memory to reduce global memory latency
- **Warp-level primitives**: Use `__shfl_xor_sync` for reductions and broadcasts within warps without shared memory
- **Instruction-level parallelism (ILP)**: Unroll loops and issue independent instructions concurrently to keep CUDA cores busy

### Memory Hierarchy Awareness

| Level | Size | Latency | Bandwidth |
|-------|------|---------|-----------|
| Registers | 64KB/SM | 0 cycles | Infinite |
| Shared Memory | 48-164KB/SM | ~20-30 cycles | ~19 TB/s (on A100) |
| L1 Cache | 128KB/SM | ~30 cycles | ~19 TB/s |
| L2 Cache | 40 MB total | ~200 cycles | ~5 TB/s |
| HBM2e | 40-80 GB | ~400 cycles | ~2 TB/s |

### CUDA Streams and Concurrency

- Use multiple CUDA streams to overlap data transfer with kernel execution
- Separate compute-bound and memory-bound kernels onto different streams
- Use `cudaMemcpyAsync` with pinned host memory for non-blocking transfers
- On Hopper, leverage Async TMA (Tensor Memory Accelerator) for bulk tensor copies

---

## Mixed Precision Training

### FP16 (Half Precision)

- 16-bit floating point: 1 sign bit, 5 exponent bits, 10 mantissa bits
- Range: ±65,504; smallest normal: 6.1×10⁻⁵
- Risk: gradient underflow in small-valued tensors; loss scaling is mandatory
- Use PyTorch's `GradScaler` to dynamically adjust loss scaling factor

### BF16 (Brain Float 16)

- 16-bit format with FP32 range: 1 sign bit, 8 exponent bits, 7 mantissa bits
- Range: ±3.39×10³⁸ (same as FP32); precision lower than FP16
- Key advantage: no loss scaling needed; numerically stable for most training
- Supported natively on A100+; default choice for training on H100

### FP8 Training (Hopper)

- Two formats: E4M3 (training forward), E5M2 (training backward)
- Transformer Engine automatically selects format per layer
- Requires calibration pass for dynamic scaling factors
- 2x throughput improvement over BF16 for supported architectures

### Mixed Precision Implementation Checklist

1. Wrap model in `torch.amp.autocast` context manager
2. Use appropriate `torch.amp.GradScaler` for FP16; skip for BF16
3. Keep loss computation and softmax in FP32 for numerical stability
4. Monitor gradient norms for underflow/overflow
5. Verify convergence matches full-precision baseline within tolerance

---

## Gradient Accumulation

### Purpose

Gradient accumulation simulates large batch sizes when GPU memory cannot hold the full batch. Instead of updating weights after each micro-batch, gradients are accumulated over multiple forward-backward passes.

### Effective Batch Size Calculation

```
effective_batch_size = micro_batch_size × accumulation_steps × num_GPUs
```

Example: `micro_batch=256 × accumulation=8 × GPUs=4 = 8,192 samples per update`

### Best Practices

- Set accumulation steps as a power of 2 for optimal GPU utilization
- Ensure batch normalization or layer normalization receives correct batch statistics by using `SyncBatchNorm`
- Track effective batch size in experiment metadata for reproducibility
- Monitor gradient norms at each accumulation boundary to detect instability
- Adjust learning rate linearly when changing effective batch size (linear scaling rule)

### Interaction with Learning Rate Scaling

- Linear scaling: multiply base LR by `effective_batch_size / reference_batch_size`
- Square root scaling for large batches (more stable but slower convergence)
- Warmup period of 5-10 epochs critical when using large effective batch sizes
- LARS/LAMB optimizers enable stable training with batch sizes up to 65,536

---

## Multi-GPU Training Strategies

### Data Parallelism (DDP)

- Each GPU holds a full model replica; data is partitioned across GPUs
- AllReduce communication for gradient synchronization after each step
- PyTorch DDP uses bucketed AllReduce for overlapping communication and computation
- Best when model fits in single GPU memory and communication cost is low

### Model Parallelism

- **Tensor parallelism**: Split individual weight matrices across GPUs (e.g., Megatron-LM style)
  - Row-parallel and column-parallel linear layers
  - Requires AllReduce or ReduceScatter after each partitioned operation
  - Effective for models with very large dense layers
- **Pipeline parallelism**: Split model into stages across GPUs (GPipe, PipeDream)
  - Micro-batching to maintain pipeline utilization
  - Bubble overhead: `(p-1)/(m+p-1)` where p=pipeline stages, m=micro-batches
  - Interleaved schedules reduce bubble to `(p-1)/(m×s+p-1)` with s virtual stages

### Hybrid Parallelism for Recommendation Models

- Embedding tables: table-parallel (row-parallel) across GPUs, since tables are often too large for one GPU
- Dense components: tensor-parallel within nodes, pipeline-parallel across nodes
- Feature interaction layers: often replicated due to small size
- Output scoring: data-parallel since each GPU computes scores independently

### Communication Backends

| Backend | Latency | Bandwidth | Use Case |
|---------|---------|-----------|----------|
| NVLink/NVSwitch | ~1 μs | 600-900 GB/s | Intra-node multi-GPU |
| InfiniBand HDR | ~1 μs | 200 Gbps | Inter-node communication |
| RoCE v2 | ~2 μs | 100-400 Gbps | Cost-effective inter-node |
| PCIe Gen4/5 | ~2 μs | 64 GB/s | CPU-GPU, limited GPU-GPU |

---

## GPU Memory Management

### Memory Composition

- **Model parameters**: embedding tables (often 80%+ of memory), dense weights
- **Optimizer states**: Adam stores m and v (2x model size), total 3x model size
- **Gradients**: Same size as parameters (FP32 or mixed precision)
- **Activations**: Stored for backward pass; proportional to batch size and sequence length
- **CUDA context**: ~500 MB-1 GB per GPU for driver/runtime overhead

### Memory Optimization Techniques

- **Gradient checkpointing (activation recomputation)**: Trade compute for memory by recomputing activations during backward pass; reduces activation memory by O(√n) for n layers
- **Embedding table sharding**: Distribute large embedding tables across GPUs and CPU memory using hybrid embedding (e.g., TorchRec's `ShardedEmbeddingBagCollection`)
- **CPU offloading**: Move optimizer states and inactive embeddings to CPU; overlaps CPU computation with GPU via CUDA unified memory or explicit transfers
- **Memory-efficient attention**: FlashAttention-2 computes attention without materializing full N×N attention matrix; reduces from O(N²) to O(N) memory
- **Dynamic batching**: Adjust batch size based on sequence length to maximize GPU utilization without OOM

### OOM Prevention Strategies

1. Pre-allocate maximum memory pool with `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128`
2. Use `torch.cuda.memory_stats()` to monitor fragmentation
3. Set `CUDNN_DETERMINISTIC=False` and `torch.backends.cudnn.benchmark=True` for reduced memory fragmentation
4. Profile memory usage with `torch.cuda.memory_snapshot()` before scaling batch size

---

## Profiling with PyTorch Profiler

### Basic Profiling Setup

```python
with torch.profiler.profile(
    activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA],
    schedule=torch.profiler.schedule(wait=1, warmup=3, active=5, repeat=2),
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/profiler'),
    record_shapes=True,
    profile_memory=True,
    with_stack=True
) as prof:
    for step, batch in enumerate(dataloader):
        if step >= (1 + 3 + 5) * 2:
            break
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        prof.step()
```

### Key Metrics to Extract

- **GPU utilization**: Target >80% for compute-bound workloads; <50% indicates data loading bottleneck
- **Kernel time breakdown**: Identify dominant kernels (embedding lookup, attention, MLP layers)
- **Memory bandwidth utilization**: Compare achieved vs. peak bandwidth for memory-bound kernels
- **Communication time**: AllReduce, AllGather as percentage of total step time
- **CPU-GPU overlap**: Ensure data preprocessing overlaps with GPU computation
- **Operator fusion opportunities**: Identify consecutive small operators that could be fused

### Common Bottlenecks and Solutions

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Low GPU util (<40%) | Data loading bottleneck | Increase num_workers, use pinned memory, pre-fetch |
| High CPU time | Data preprocessing on CPU | Move transforms to GPU, use DALI/NTK |
| Memory spike during loss | Large activation tensors | Gradient checkpointing, reduce batch size |
| Long AllReduce time | Slow inter-GPU communication | Use NVLink topology, bucket gradients |
| Frequent CUDA sync | CPU-GPU synchronization points | Remove .item(), .cpu() calls in training loop |

### Torch Profiler with TensorBoard

- Export trace to TensorBoard for visual analysis of GPU/CPU timeline
- Use trace viewer to identify idle GPU gaps and overlapping opportunities
- Plugin shows memory timeline, allowing identification of peak memory events
- Compare profiling results across hardware configurations (A100 vs H100)

---

## Production GPU Training Pipeline

### Pre-Training Checklist

1. Verify data pipeline throughput exceeds GPU consumption rate
2. Profile single-GPU performance before scaling to multi-GPU
3. Establish baseline metrics (loss curve, throughput, memory usage)
4. Set up checkpointing interval based on GPU-hour cost
5. Configure automatic failure recovery (restart from last checkpoint)

### Training Monitoring

- **Throughput**: Samples/second per GPU; target 10K-100K for typical rec models
- **GPU memory utilization**: Should be stable; spikes indicate potential OOM
- **Loss curve**: Monitor for divergence, plateaus, or oscillations
- **Gradient norms**: Track for exploding/vanishing gradients
- **Learning rate schedule**: Verify warmup and decay as designed

### Checkpointing Strategy

- Full model checkpoint every N steps (based on time to checkpoint vs. recovery cost)
- EMA (Exponential Moving Average) model state for evaluation
- Include optimizer state for exact training continuation
- Store checkpoints in distributed storage (S3, GCS) with metadata
- Maintain at least 3 recent checkpoints for rollback capability

### Cost Optimization

- Use spot/preemptible instances for training (60-70% cost reduction)
- Implement automatic checkpointing on preemption signals
- Right-size GPU selection: A100 40GB for most models, H100 only when justified
- Profile and eliminate idle GPU time through pipeline optimization
- Consider mixed precision for 1.5-2x throughput improvement with minimal accuracy loss
