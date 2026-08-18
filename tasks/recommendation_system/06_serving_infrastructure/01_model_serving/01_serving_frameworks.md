# Model Serving Framework Comparison

## Overview

Model serving is the infrastructure layer that loads trained models and serves predictions in response to real-time or batch requests. For recommendation systems, serving frameworks must handle high throughput (millions of QPS), low latency (single-digit milliseconds), diverse model architectures, and complex pre/post-processing pipelines. This document compares the major serving frameworks and provides guidance for selection.

---

## Framework Overview

### Triton Inference Server (NVIDIA)

#### Architecture

```
Client Request → HTTP/gRPC Endpoint → Scheduler → Model Instance(s)
                                                  ↓
                                        ┌─────────┼─────────┐
                                        │         │         │
                                   Model A   Model B   Model C
                                   (GPU 0)   (GPU 0)   (GPU 1)
```

#### Key Features

- **Multi-framework support**: PyTorch, TensorFlow, TensorRT, ONNX, Python, OpenVINO
- **Dynamic batching**: Automatically groups requests for GPU efficiency
- **Concurrent model execution**: Multiple models on the same GPU
- **Model pipeline (ensemble)**: Chain models (preprocess → model → postprocess)
- **Metrics and monitoring**: Prometheus metrics, detailed profiling
- **Model versioning**: Hot-swapping between model versions
- **GPU sharing**: MPS (Multi-Process Service) for model co-location

#### Configuration

```protobuf
# config.pbtxt
name: "ranking_model"
platform: "pytorch_libtorch"
max_batch_size: 64
input [
  {
    name: "user_ids"
    data_type: TYPE_INT32
    dims: [50]
  },
  {
    name: "item_features"
    data_type: TYPE_FP32
    dims: [128]
  }
]
output [
  {
    name: "scores"
    data_type: TYPE_FP32
    dims: [1]
  }
]
instance_group [
  {
    count: 4
    kind: KIND_GPU
    gpus: [0, 1]
  }
]
dynamic_batching {
  preferred_batch_size: [16, 32, 64]
  max_queue_delay_microseconds: 100
}
```

#### Best For

- Large-scale production serving with GPU acceleration
- Multi-model serving with complex pipelines
- TensorRT-optimized inference for maximum performance

---

### TorchServe (PyTorch)

#### Architecture

```
Client Request → Frontend (HTTP/gRPC) → Dispatcher → Model Worker(s)
                                                ↓
                                          ┌─────┼─────┐
                                          │     │     │
                                        W1    W2    W3
```

#### Key Features

- **Native PyTorch**: First-class PyTorch model support
- **Model archive**: Package model + handler into `.mar` file
- **Custom handlers**: Pre-processing, inference, and post-processing in Python
- **Snapshot**: Model state snapshot for recovery
- **Metrics**: Built-in metrics endpoint (Prometheus compatible)
- **A/B testing**: Traffic splitting between model versions

#### Custom Handler

```python
class MyHandler:
    def preprocess(self, data):
        # Convert request to tensor
        ...
    
    def inference(self, model, inputs):
        # Run model forward pass
        with torch.no_grad():
            return model(inputs)
    
    def postprocess(self, output):
        # Format predictions
        ...
```

#### Best For

- PyTorch-native environments
- Teams already invested in PyTorch ecosystem
- Moderate scale serving (< 100K QPS)

---

### TensorFlow Serving

#### Architecture

```
Client Request → gRPC/REST Server → Model Manager → Model Loader
                                              ↓
                                     Model Repository
                                     (file system or GCS)
```

#### Key Features

- **Seamless TensorFlow integration**: Load SavedModel directly
- **Model versioning**: Automatic version management from directory structure
- **Batching**: Built-in batching with configurable parameters
- **GPU support**: CUDA acceleration for TF models
- **Extended runtime**: Support for TensorFlow Lite models
- **Model warmup**: Pre-load models for fast serving

#### Best For

- TensorFlow-native environments
- Legacy TF model serving
- Kubernetes-based deployments (via TF Serving Docker image)

---

### ONNX Runtime

#### Architecture

```
Model (PyTorch/TF/Sklearn) → ONNX Export → ONNX Runtime → Inference
```

#### Key Features

- **Framework agnostic**: Export from any framework, serve with one runtime
- **Graph optimization**: Constant folding, layer fusion, redundant node elimination
- **Quantization**: INT8 quantization with calibration
- **Hardware execution providers**: CUDA, TensorRT, OpenVINO, CoreML
- **Memory optimization**: Memory pattern optimization, memory planning

#### Optimization Levels

| Level | Optimizations | Typical Speedup |
|-------|--------------|-----------------|
| ORT_DISABLE_ALL | No optimization | 1× |
| ORT_ENABLE_BASIC | Constant folding, dead code elimination | 1.2-1.5× |
| ORT_ENABLE_EXTENDED | + Layer fusion, attention fusion | 1.5-2× |
| ORT_ENABLE_ALL | + TensorRT, all optimizations | 2-4× |

#### Best For

- Cross-framework serving
- Edge deployment
- CPU-optimized inference

---

### vLLM

#### Architecture

```
Client Request → API Server → Scheduler → KV Cache Manager → Model Execution
                                        ↓
                                  PagedAttention
                                  (virtual memory for KV cache)
```

#### Key Features

- **PagedAttention**: Efficient memory management for transformer KV cache
- **Continuous batching**: Dynamic request scheduling
- **Tensor parallelism**: Multi-GPU serving for large models
- **Quantization**: GPTQ, AWQ, INT4/INT8 support
- **Prefix caching**: Reuse KV cache for common prefixes

#### Best For

- Large language model serving
- Autoregressive transformer models
- High-throughput text generation

---

### BentoML

#### Architecture

```
BentoML Service
├── Preprocessing (Python)
├── Model Runner(s)
│   ├── ONNX Runtime
│   ├── PyTorch
│   ├── TensorFlow
│   └── Triton (remote)
├── Postprocessing (Python)
└── API Endpoints (HTTP/gRPC)
```

#### Key Features

- **Unified framework**: Wrap any model in a standardized service
- **Bento creation**: Package code, models, and dependencies into a Bento
- **Adaptive batching**: Automatic request batching
- **Traffic management**: A/B testing, canary deployment
- **Multi-model serving**: Serve multiple models in one service
- **YAML configuration**: Declarative service definition

#### Best For

- Multi-framework environments
- Rapid prototyping and deployment
- Teams needing flexibility in serving infrastructure

---

### Seldon Core

#### Architecture

```
Client → Seldon API Gateway → Predictor (Kubernetes Pod)
                              ├── Model A (Docker container)
                              ├── Transformer
                              └── Combiner
```

#### Key Features

- **Kubernetes-native**: Custom Resource Definitions (CRDs) for model deployment
- **Microservice-based**: Each component is a separate container
- **Multi-language**: Python, Java, Go model wrappers
- **A/B testing and MAB**: Built-in experiment routing
- **Explainability**: Integrated SHAP and Alibi for model explanations
- **Drift detection**: Built-in data drift detection

#### Best For

- Kubernetes-native ML platforms
- Complex deployment topologies (A/B, MAB)
- Enterprise environments with strict operational requirements

---

## Performance Benchmarks

### Throughput Comparison (Recurrent Recommendation Model, A100 GPU)

| Framework | Batch=1 (QPS) | Batch=32 (QPS) | Batch=256 (QPS) | Latency P99 (ms) |
|-----------|--------------|----------------|-----------------|-------------------|
| Triton + TensorRT | 8,500 | 42,000 | 85,000 | 1.2 |
| Triton + PyTorch | 6,200 | 35,000 | 72,000 | 1.8 |
| TorchServe | 5,800 | 32,000 | 65,000 | 2.1 |
| ONNX Runtime | 7,100 | 38,000 | 78,000 | 1.5 |
| BentoML + ONNX | 6,800 | 36,000 | 74,000 | 1.7 |
| TF Serving | 5,500 | 30,000 | 62,000 | 2.3 |

*Benchmarks are approximate; actual numbers depend on model, hardware, and configuration.*

### CPU-Only Serving (Intel Xeon)

| Framework | QPS (batch=1) | QPS (batch=32) | Latency P99 |
|-----------|--------------|----------------|-------------|
| ONNX Runtime | 3,200 | 12,000 | 8 ms |
| Triton (OpenVINO) | 3,000 | 11,500 | 9 ms |
| TorchServe | 2,100 | 8,500 | 12 ms |
| BentoML | 2,500 | 9,000 | 11 ms |

### Memory Efficiency

| Framework | Base Memory (MB) | Per-Model (MB) | GPU Utilization |
|-----------|-----------------|----------------|-----------------|
| Triton | 200 | Varies | High (MPS) |
| TorchServe | 150 | Varies | Moderate |
| ONNX Runtime | 50 | Varies | N/A (CPU) |
| TF Serving | 180 | Varies | High |
| BentoML | 100 | Varies | Depends on runner |

---

## GPU vs CPU Serving

### When to Use GPU

- Model has > 100M parameters
- Batch inference with large batches
- Transformer-based models (attention is GPU-friendly)
- Latency budget < 5ms
- Serving volume justifies GPU cost

### When to Use CPU

- Model has < 10M parameters
- Sparse models with embedding lookups dominate
- Budget constraints
- Latency budget > 10ms
- Serving volume doesn't justify GPU cost

### Hybrid Approach (Common in Production)

```
Candidate Generation: CPU (sparse models, ANN search)
      ↓
Ranking: GPU (deep models, transformer)
      ↓
Re-ranking: CPU (business rules, diversity)
```

---

## Selection Guide

| Requirement | Recommended Framework |
|------------|----------------------|
| Maximum GPU throughput | Triton + TensorRT |
| PyTorch-native | TorchServe or Triton |
| Cross-framework | ONNX Runtime or BentoML |
| Kubernetes-native | Seldon Core |
| LLM serving | vLLM |
| Quick prototyping | BentoML |
| Multi-model pipeline | Triton (ensemble) |
| Enterprise with MLOps | Seldon Core |
| Edge deployment | ONNX Runtime |

### Decision Matrix

| Factor | Weight | Triton | TorchServe | TF Serving | ONNX RT | BentoML | Seldon |
|--------|--------|--------|-----------|-----------|---------|---------|--------|
| Performance | 30% | ★★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★ |
| Ease of use | 20% | ★★★ | ★★★★ | ★★★ | ★★★★ | ★★★★★ | ★★★ |
| Flexibility | 15% | ★★★★★ | ★★★★ | ★★★ | ★★★★ | ★★★★★ | ★★★★★ |
| Ecosystem | 15% | ★★★★ | ★★★★ | ★★★★ | ★★★ | ★★★★ | ★★★★ |
| Operational maturity | 10% | ★★★★★ | ★★★ | ★★★★ | ★★★ | ★★★ | ★★★★★ |
| Community | 10% | ★★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★ |

---

## Production Deployment Patterns

### Triton Deployment (Kubernetes)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ranking-model
spec:
  replicas: 4
  template:
    spec:
      containers:
      - name: triton
        image: nvcr.io/nvidia/tritonserver:23.10-py3
        args: ["--model-repository=s3://models/ranking/"]
        resources:
          limits:
            nvidia.com/gpu: 1
        ports:
        - containerPort: 8000  # HTTP
        - containerPort: 8001  # gRPC
        - containerPort: 8002  # Metrics
```

### Health Checks

```bash
# Triton health check
curl http://localhost:8000/v2/health/ready

# Model ready check
curl http://localhost:8000/v2/repository/models/ranking_model/ready

# Get model metadata
curl http://localhost:8000/v2/models/ranking_model
```

### Monitoring Integration

- Export Triton metrics to Prometheus (port 8002)
- Grafana dashboards for throughput, latency, GPU utilization
- Alerting on latency P99 > threshold
- Track model inference count and error rate
