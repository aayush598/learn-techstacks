# Distributed Training for Recommendation Models

## Overview

Modern recommendation models at scale require distributed training to handle billions of training examples, terabytes of feature data, and model parameters that may exceed single-GPU memory. This document covers distributed training strategies, parallelism paradigms, and practical infrastructure for training production recommendation systems.

---

## Why Distributed Training?

### Scale Requirements

| Factor | Typical Scale | Single Machine Limit |
|--------|--------------|---------------------|
| Training examples | 10B–100B+ interaction events | ~10M–100M in memory |
| Feature vocabulary | 100M–1B sparse features | ~10M embeddings in GPU memory |
| Model parameters | 1B–100B (including embeddings) | ~10B on high-end GPU |
| Training time | Days to weeks (single GPU) | Hours (target) |
| Feature dimensionality | 1000s of dense features | Memory-bound |

### Cost Efficiency

- **Time-to-model**: Distribute computation to meet latency SLAs for model updates
- **Hardware utilization**: Maximize GPU/TPU utilization across a cluster
- **Cost-performance**: Multiple smaller GPUs can be cheaper than fewer larger ones

---

## Parallelism Paradigms

### Data Parallelism

#### Concept

Each worker holds a complete copy of the model. Training data is partitioned across workers. Each worker computes gradients on its data partition, then gradients are synchronized.

```
Worker 1: Model Copy + Data Partition 1 → Gradients 1
Worker 2: Model Copy + Data Partition 2 → Gradients 2
Worker 3: Model Copy + Data Partition 3 → Gradients 3
Worker 4: Model Copy + Data Partition 4 → Gradients 4
                          ↓
              Gradient Synchronization (AllReduce)
                          ↓
              All Workers Update Model Identically
```

#### Synchronous Data Parallelism

- All workers compute gradients simultaneously
- Gradients are aggregated (mean) before model update
- Guarantees consistent model updates
- **Problem**: Slowest worker determines step time (straggler problem)

#### Asynchronous Data Parallelism

- Workers compute and update independently
- Workers read the latest model parameters before each step
- No synchronization barrier
- **Problem**: Gradient staleness (parameters may be outdated by the time update is applied)

#### Comparison

| Aspect | Synchronous | Asynchronous |
|--------|------------|-------------|
| Consistency | Perfect | Stale gradients |
| Straggler sensitivity | High | None |
| Implementation complexity | Moderate | Higher |
| Convergence guarantee | Strong | Weaker |
| Throughput | Limited by slowest worker | Maximum utilization |
| Production usage | Most common | Rare (older systems) |

### Model Parallelism

#### Concept

The model is split across workers. Each worker holds a subset of parameters and computes a portion of the forward/backward pass.

```
Worker 1: Layers 1-6    → Hidden states →
Worker 2: Layers 7-12   → Hidden states →
Worker 3: Layers 13-18  → Hidden states →
Worker 4: Layers 19-24  → Final output
```

#### When Model Parallelism is Necessary

- Model parameters exceed single GPU memory (e.g., 100B parameter model)
- Very large embedding tables (billions of rows × 128+ dimensions)
- Model architecture inherently parallel (e.g., mixture of experts)

#### Types

| Type | Description | Use Case |
|------|-------------|----------|
| Pipeline parallelism | Split model by layers across workers | Deep models |
| Tensor parallelism | Split individual operations (matmul) across workers | Very wide layers |
| Expert parallelism | Different experts on different workers | Mixture of Experts models |

### Pipeline Parallelism

#### Concept

Divide the model into stages, each assigned to a different device. Micro-batches flow through the pipeline.

```
Stage 1 (GPU 0): Embedding → Layer 1-4 → Micro-batch output
Stage 2 (GPU 1): Layer 5-8 → Micro-batch output
Stage 3 (GPU 2): Layer 9-12 → Micro-batch output
Stage 4 (GPU 3): Layer 13-16 → Final output → Loss → Backward pass
```

#### Scheduling Strategies

| Strategy | Description | Bubble Rate | Memory |
|----------|-------------|-------------|--------|
| GPipe | Forward pass all micro-batches, then backward | High (1/(P×M)) | High |
| PipeDream | 1F1B (one forward, one backward interleaved) | Lower | Moderate |
| PipeDream-2BW | Two backward passes per forward | Lower | Moderate |
| Interleaved | Virtual stages per device | Lowest | Moderate |

Where P = pipeline stages, M = micro-batches.

#### Micro-batch Size Selection

```
Total batch size = micro_batch_size × num_micro_batches × num_workers
```

- Larger micro-batches: Better GPU utilization, more memory
- More micro-batches: Lower pipeline bubble rate, more communication
- Sweet spot: 4–16 micro-batches per pipeline stage

---

## PyTorch Distributed Data Parallel (DDP)

### Architecture

```
torch.distributed.init_process_group()
  ↓
model = DDP(model, device_ids=[local_rank])
  ↓
DistributedSampler ensures each GPU sees different data
  ↓
Forward + Backward pass (automatic gradient bucketing)
  ↓
AllReduce gradients across all GPUs
  ↓
Optimizer step (all GPUs have same parameters)
```

### Key Configuration

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| NCCL backend | GPU communication library | NCCL for NVIDIA GPUs |
| World size | Total number of GPUs | 8–128 |
| Batch size per GPU | Local batch size | 256–4096 |
| Gradient accumulation | Steps before synchronization | 1–16 |
| Mixed precision | FP16/BF16 training | Enabled |

### Gradient Accumulation

When the desired effective batch size exceeds GPU memory:

```
effective_batch = batch_per_gpu × accumulation_steps × num_gpus

Example: 256 × 4 × 8 = 8192 effective batch size
```

Implementation:
```
for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### Communication Overhead

- AllReduce cost: O(model_parameters × log(world_size))
- For a 1B parameter model: ~4 GB of gradient data per synchronization
- Overlap computation and communication using DDP's gradient bucketing

### Best Practices

1. **Use DDP, not DataParallel**: DDP uses separate processes (no GIL limitation)
2. **Pin memory**: `pin_memory=True` in DataLoader for faster CPU→GPU transfer
3. **Non-blocking transfers**: Overlap data loading with computation
4. **Find unused parameters**: Set `find_unused_parameters=False` if possible (faster)
5. **Gradient compression**: For large-scale, use gradient compression (PowerSGD)

---

## DeepSpeed ZeRO

### Motivation

Standard DDP replicates the entire model on each GPU. For models with billions of parameters, this wastes memory. ZeRO (Zero Redundancy Optimizer) partitions optimizer states, gradients, and parameters across GPUs.

### ZeRO Stages

| Stage | Partitions | Memory Savings | Communication |
|-------|-----------|---------------|---------------|
| ZeRO-1 | Optimizer states | 4× | Same as DDP |
| ZeRO-2 | Optimizer states + gradients | 8× | Same as DDP |
| ZeRO-3 | Optimizer states + gradients + parameters | N× (N = num GPUs) | 1.5× DDP |

Where N = number of GPUs. For 64 GPUs: 64× memory savings with ZeRO-3.

### ZeRO-1 Detail

```
GPU 0: Model copy + Optimizer states for params 0-25%
GPU 1: Model copy + Optimizer states for params 25-50%
GPU 2: Model copy + Optimizer states for params 50-75%
GPU 3: Model copy + Optimizer states for params 75-100%

During training:
1. All GPUs compute full forward/backward pass
2. All GPUs compute gradients for all parameters
3. Each GPU updates only its partition of optimizer states
4. AllReduce to synchronize updated parameters
```

### ZeRO-3 with Offloading

Offload optimizer states and parameters to CPU memory:

```
GPU: Active parameters only (~1-2 copies)
CPU: Optimizer states + parameter partitions
SSD: Optionally offload to NVMe for extreme scale
```

### DeepSpeed Configuration

```json
{
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": 5e8,
    "stage3_prefetch_bucket_size": 5e8,
    "stage3_param_persistence_threshold": 1e6
  }
}
```

### When to Use Each ZeRO Stage

| Model Size | GPUs Available | Recommended Stage |
|-----------|---------------|-------------------|
| < 1B params | 1-2 GPUs | No ZeRO (standard DDP) |
| 1-10B params | 8 GPUs | ZeRO-2 |
| 10-50B params | 8-64 GPUs | ZeRO-3 |
| 50-200B params | 64-256 GPUs | ZeRO-3 + Offloading |
| > 200B params | 256+ GPUs | ZeRO-3 + NVMe offloading |

---

## Parameter Servers

### Architecture

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Worker 1    │  │  Worker 2    │  │  Worker 3    │
│  (data partition 1) │  (data partition 2) │  (data partition 3) │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                ┌────────┴────────┐
                │ Parameter Server │
                │ (stores global   │
                │  model params)   │
                └─────────────────┘
```

### Asynchronous Parameter Server

- Workers pull latest parameters from server
- Workers compute gradients locally
- Workers push gradients to server
- Server updates parameters immediately (asynchronous)
- No waiting for other workers

### Synchronous Parameter Server

- Workers pull parameters, compute gradients
- Server collects gradients from all workers
- Server applies aggregated gradient
- Workers wait for updated parameters before next step

### Comparison with AllReduce

| Aspect | Parameter Server | AllReduce |
|--------|-----------------|-----------|
| Communication pattern | Star (workers ↔ server) | Ring or tree |
| Server bottleneck | Yes (centralized) | No (decentralized) |
| Straggler handling | Natural (async) | Requires sync |
| Memory | Server needs large memory | Distributed |
| Network topology | Flexible | Requires high bandwidth |

### Scaling Parameter Servers

- **Sharded PS**: Partition parameters across multiple servers
- **Hierarchical PS**: Local PS per machine, global PS across machines
- **Distributed PS**: Replace central server with distributed hash table

---

## Mixed Precision Training

### Data Types

| Type | Bits | Range | Speed | Use Case |
|------|------|-------|-------|----------|
| FP32 | 32 | ±3.4×10³⁸ | Baseline | Master weights, loss |
| FP16 | 16 | ±65504 | 2-3× faster | Forward/backward |
| BF16 | 16 | ±3.4×10³⁸ | 2-3× faster | Better range than FP16 |
| TF32 | 19 | ±3.4×10³⁸ | 2× faster (A100) | Default on A100+ |
| INT8 | 8 | -128 to 127 | 3-4× faster | Inference |

### FP16 Training

```
Forward pass: FP16 (faster matmul on Tensor Cores)
Loss computation: FP32 (avoid underflow)
Backward pass: FP16
Gradient scaling: Dynamic loss scaling (prevent underflow)
Master weights: FP32 (maintain precision)
Weight update: FP32 → FP16 for next forward pass
```

### BF16 Training

- Same exponent range as FP32 (no underflow/overflow issues)
- No loss scaling needed
- Slightly lower precision than FP16 in mantissa
- Recommended over FP16 for recommendation models

### AMP (Automatic Mixed Precision) in PyTorch

```python
scaler = torch.cuda.amp.GradScaler()

for batch in dataloader:
    with torch.cuda.amp.autocast():
        output = model(batch)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

---

## Gradient Accumulation Strategies

### When to Accumulate

- GPU memory limits batch size
- Large effective batch sizes needed for stability (common in recommendation training)
- Communication bandwidth is the bottleneck (accumulate locally, sync less often)

### Advanced Patterns

#### Gradient Compression

- Quantize gradients before communication (e.g., to INT8)
- Top-K sparsification: Only communicate largest K% of gradients
- PowerSGD: Low-rank approximation of gradient matrices

#### Gradient Checkpointing

- Trade compute for memory
- Don't store activations for all layers
- Recompute activations during backward pass
- Can reduce memory by 50-70% at 20-30% compute overhead

---

## Training Infrastructure

### Cluster Configuration

| Component | Typical Spec | Purpose |
|-----------|-------------|---------|
| GPU nodes | 8× A100 80GB per node | Training compute |
| InfiniBand | 200-400 Gbps | Inter-node communication |
| NVLink | 600 GB/s | Intra-node GPU communication |
| CPU nodes | 128+ cores, 1TB RAM | Data preprocessing, parameter servers |
| Storage | Parallel file system (Lustre, GPFS) | Training data, checkpoints |
| Network | 25-100 Gbps Ethernet | Management, monitoring |

### Data Pipeline

```
Raw Data (S3/GCS/HDFS)
      ↓
Distributed Preprocessing (Spark/Dask)
      ↓
Feature Engineering (Offline)
      ↓
Feature Store (Feast/Tecton)
      ↓
Training Data Writer (Parquet/TFRecord)
      ↓
Distributed Data Loading (All workers read in parallel)
      ↓
Training Loop (DDP/DeepSpeed)
```

### Checkpointing Strategy

| Strategy | Frequency | Storage | Recovery Time |
|----------|----------|---------|--------------|
| Full checkpoint | Every N steps | Full model state | Fast (load and resume) |
| Incremental | Every step (to distributed FS) | Only changed params | Very fast |
| Periodic full + incremental | Both | Tiered | Fast |
| Async checkpointing | Background process | Non-blocking | Very fast |

### Scaling Laws for Recommendations

```
Optimal batch size ∝ learning_rate (linear scaling rule)
When doubling GPUs:
  - Double learning rate (with warm-up)
  - Or double batch size (without LR change)
  
Diminishing returns:
  - Beyond ~128 GPUs, communication overhead dominates
  - Beyond ~1000 batch size, convergence may degrade
```

---

## Common Pitfalls and Solutions

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Dead embeddings | Zero gradients for rare items | Embedding regularization, minimum frequency |
| Gradient explosion | Loss goes to NaN | Gradient clipping (max_norm=1.0) |
| Communication bottleneck | GPU utilization < 80% | Overlap comm with compute, use InfiniBand |
| Straggler workers | Step time = slowest worker | Load balancing, timeout and retry |
| Checkpoint failure | Training crashes during save | Async checkpointing, verify before overwriting |
| Data imbalance | Some workers get more data | Use DistributedSampler with shuffle |
