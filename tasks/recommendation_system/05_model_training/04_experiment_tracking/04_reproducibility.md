# Reproducibility in Recommendation Model Training

## Overview

Reproducibility ensures that experiments can be reliably repeated with identical results, which is critical for debugging, validation, and building on previous work. In recommendation systems, reproducibility is complicated by stochastic training processes, large-scale distributed computing, and evolving data. This document covers seed management, dependency pinning, data versioning, environment containers, and deterministic training practices.

---

## Seed Management

### Sources of Randomness

| Source | Example | Control Method |
|--------|---------|---------------|
| Python random | Data shuffling, augmentation | `random.seed()` |
| NumPy random | Feature sampling, noise | `np.random.seed()` |
| PyTorch CPU | Weight initialization | `torch.manual_seed()` |
| PyTorch GPU | CUDA operations | `torch.cuda.manual_seed()` |
| cuDNN | Algorithm selection | `torch.backends.cudnn.deterministic = True` |
| Multi-GPU | Non-deterministic AllReduce | `torch.use_deterministic_algorithms(True)` |
| DataLoader workers | Parallel data loading | `worker_init_fn` per worker |

### Comprehensive Seed Setting

```python
import os, random, numpy as np, torch

def set_global_seed(seed=42):
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    torch.use_deterministic_algorithms(True)
```

### Determinism vs Performance Trade-offs

| Setting | Deterministic | Performance Impact |
|---------|--------------|-------------------|
| `cudnn.deterministic=True` | Yes | 10-20% slower |
| `cudnn.benchmark=False` | Yes | 5-15% slower (loses auto-tuning) |
| `use_deterministic_algorithms` | Yes | 15-30% slower |
| `CUBLAS_WORKSPACE_CONFIG` | Yes | Minimal |

**Recommendation**: Use full determinism for final experiments and ablation studies. Use non-deterministic settings during exploration and hyperparameter search for speed.

---

## Dependency Pinning

### Requirements Management

**Exact Pinning** (recommended for reproducibility):
```
torch==2.1.0+cu118
transformers==4.35.0
numpy==1.24.3
pandas==2.1.1
```

**Compatible Pinning** (for flexibility):
```
torch>=2.1.0,<2.2.0
transformers>=4.35.0,<5.0.0
```

### Dependency Pinning Tools

| Tool | Approach | Best For |
|------|----------|----------|
| pip-tools | Compile requirements.in → requirements.txt | Python-only projects |
| Poetry | Lock file with exact versions | Full Python project |
| conda-lock | Cross-platform lock files | Conda environments |
| Docker | Full OS + dependency pinning | Complete environment |
| Nix | Fully reproducible builds | Maximum determinism |

### Common Pitfalls

- Implicit dependencies: library A depends on library B version X
- CUDA version mismatches: torch compiled for CUDA 11.8 vs CUDA 12.0
- Platform differences: Linux vs macOS, different CPU architectures
- Transitive dependency updates: pip resolves different sub-dependency versions

### Dependency Audit

- Regularly review and update pinned versions for security patches
- Test updates in a branch before merging to main training pipeline
- Document which version updates have been tested and validated
- Maintain a compatibility matrix for critical dependencies

---

## Data Versioning with DVC

### Why Data Versioning Matters

- Training data evolves: new items, updated features, changed labeling
- Model results depend on specific data version
- Reproducibility requires exact data reconstruction
- Regulatory compliance may require data provenance tracking

### DVC (Data Version Control) Workflow

```
git init
dvc init
dvc remote add -d storage s3://my-bucket/dvc-storage
dvc add data/train.parquet
git add data/train.parquet.dvc .gitignore
git commit -m "Add training data v1"
```

### DVC Best Practices

- Store raw data in versioned storage (S3/GCS)
- Use DVC to track data file hashes (not the data itself in git)
- Version data processing pipelines alongside code
- Tag data versions alongside model versions
- Store feature engineering code with data pipeline definitions

### Data Lineage with DVC

```
raw_data (S3) → preprocessing_pipeline.py → features_v1 (S3) → train.py → model_v1
```

- Track input → output relationships for each pipeline stage
- Reproduce entire pipeline from raw data to trained model
- Compare model performance across different data versions
- Audit which data was used for any production model

---

## Environment Containers

### Docker for Reproducible Training

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
RUN apt-get update && apt-get install -y python3.10 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /workspace
WORKDIR /workspace
ENV PYTHONHASHSEED=42
ENV CUDNN_DETERMINISTIC=1
```

### Container Versioning Strategy

| Component | Versioning Approach | Tag Example |
|-----------|-------------------|-------------|
| Base CUDA image | CUDA version + cuDNN version | `cuda11.8-cudnn8` |
| Python packages | Exact versions in requirements | `torch2.1-transformers4.35` |
| Application code | Git commit hash | `abc123def` |
| Full image | Semantic version | `rec-train:v1.3.0` |

### Container Registry Management

- Store training containers in a private registry (ECR, GCR, Harbor)
- Tag images with both semantic version and git commit
- Retain images for all production model versions
- Scan images for security vulnerabilities
- Maintain base image update schedule (monthly security patches)

---

## Experiment Snapshots

### What to Snapshot

| Component | Storage | Retention |
|-----------|---------|-----------|
| Model checkpoint | Object storage | Last N checkpoints |
| Training config | Git + registry | Permanent |
| Code version | Git commit | Permanent |
| Data version | DVC + object storage | Permanent |
| Environment | Docker image | Permanent |
| Metrics | Experiment DB | Permanent |
| Hyperparameters | Experiment DB | Permanent |

### Snapshot Workflow

1. Before training: record all inputs (code commit, data version, config, environment)
2. During training: save periodic checkpoints with timestamps
3. After training: save final model, metrics, and analysis artifacts
4. Register: push all artifacts to model registry with full metadata
5. Validate: verify snapshot can be loaded and produces identical predictions

### Snapshot Validation

- Load model from snapshot and run inference on fixed input
- Compare output to original (bit-exact for deterministic, within tolerance otherwise)
- Verify all metrics match within floating-point precision
- Test on multiple machines to rule out hardware-specific effects

---

## Deterministic Training Practices

### PyTorch Determinism Controls

| Setting | Effect | When to Use |
|---------|--------|-------------|
| `torch.use_deterministic_algorithms(True)` | Enforce deterministic ops | Final experiments |
| `torch.backends.cudnn.deterministic = True` | Deterministic convolutions | Always |
| `torch.backends.cudnn.benchmark = False` | Disable auto-tuner | Reproducibility runs |
| `CUBLAS_WORKSPACE_CONFIG=:4096:8` | Deterministic cuBLAS | When using deterministic algos |

### Non-Determinism Sources to Watch

- **Atomic operations in CUDA**: Use `torch.use_deterministic_algorithms` with `warn_only=True` for ops without deterministic alternatives
- **DataLoader num_workers > 0**: Set `worker_init_fn` for each worker's random state
- **Multi-GPU training**: Order of gradient accumulation may vary; use `torch.distributed.barrier` for synchronization
- **Floating-point associativity**: FP32 addition is not associative; reduction order affects results
- **CPU parallelism**: `torch.set_num_threads(1)` eliminates thread-level non-determinism

### When Full Determinism Is Not Possible

- Use metric tolerance bands instead of exact equality
- Run 3-5 seeds and report mean ± standard deviation
- Statistical comparison (t-test) accounts for run-to-run variance
- Document known sources of non-determinism and their expected impact

---

## Reproducibility Checklist

### Before Training

- [ ] Set all random seeds
- [ ] Pin all dependency versions
- [ ] Record git commit hash
- [ ] Record data version (DVC hash or dataset version)
- [ ] Record hardware configuration (GPU type, count, driver version)
- [ ] Save complete training configuration as YAML/JSON
- [ ] Use deterministic Docker image

### During Training

- [ ] Log hyperparameters at start
- [ ] Save checkpoints at regular intervals
- [ ] Monitor for NaN/Inf (non-deterministic divergence)
- [ ] Record wall-clock time per epoch for timing reproducibility

### After Training

- [ ] Save final model with complete metadata
- [ ] Run reproducibility validation (reload + inference comparison)
- [ ] Store all artifacts in versioned storage
- [ ] Register in model registry with lineage information
- [ ] Document any deviations from expected deterministic behavior

### Periodic Verification

- [ ] Monthly: reproduce a historical experiment from snapshots
- [ ] Quarterly: verify Docker image builds and runs correctly
- [ ] Annually: update base images and re-validate pipeline
