# ONNX Conversion for Recommendation Models

## Overview

ONNX (Open Neural Network Exchange) provides a standardized model format for deploying trained models across different inference runtimes. Converting recommendation models to ONNX enables hardware-agnostic optimization, cross-platform deployment, and access to ONNX Runtime's graph optimization passes. This covers PyTorch export, opset compatibility, custom operators, and ONNX Runtime optimization.

---

## PyTorch to ONNX Export

### Basic Export

```python
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    opset_version=17,
    input_names=["user_features", "item_features"],
    output_names=["scores"],
    dynamic_axes={
        "user_features": {0: "batch_size"},
        "item_features": {0: "batch_size"},
        "scores": {0: "batch_size"}
    }
)
```

### Export Considerations for Recommendation Models

**Dynamic Shapes**:
- Batch size must be dynamic for variable-size inference
- Sequence length may vary for sequential models
- Candidate item count varies per request
- Use `dynamic_axes` to specify variable dimensions

**Embedding Table Handling**:
- Large embedding tables must be embedded in the ONNX graph
- Consider quantizing embeddings before export (reduces ONNX file size)
- For very large tables, external data format stores tensors separately

**Control Flow**:
- `torch.onnx.export` traces the model; dynamic control flow requires special handling
- Use `torch.jit.script` for models with complex conditional logic
- ORT can handle `If` and `Loop` ops from torch.jit.export

### Common Export Failures

| Error | Cause | Solution |
|-------|-------|---------|
| Unsupported op | PyTorch op not in ONNX opset | Custom operator or rewrite |
| Dynamic shape error | Undefined dynamic dimensions | Explicit dynamic_axes |
| Tracing failure | Side effects in forward pass | Refactor to pure computation |
| Export too slow | Large model with many ops | Export subgraphs separately |

---

## Opset Version Compatibility

### Opset Evolution

| Opset Version | Key Additions | Recommendation |
|--------------|---------------|----------------|
| 11 | Basic ops, Attention | Legacy support only |
| 13 | Improved GatherElements | Minimum for most models |
| 14 | ReduceSum, GroupNormalization | Stable for production |
| 17 | Latest stable opset | Recommended for new models |
| 18 | Attention extensions | Cutting-edge features |

### Opset Selection Guidelines

- Use opset 17 for new models (best compatibility + features)
- Match opset to ONNX Runtime version (newer ORT supports newer opsets)
- Test with target inference runtime before finalizing opset
- Lower opset for wider compatibility (edge devices, older runtimes)

### Version Migration

- When upgrading opset, re-export and validate metrics
- Some ops change behavior between versions (e.g., ReduceSum axis handling)
- Test dynamic shapes at multiple sizes after opset upgrade
- Maintain a validation suite for ONNX export correctness

---

## Custom Operators

### When Custom Operators Are Needed

- Recommendation-specific operations (e.g., custom feature interaction)
- Novel attention patterns not in standard ONNX ops
- Custom loss functions (not needed for inference export)
- Domain-specific preprocessing embedded in the model

### Custom Operator Registration

1. Implement the operator in C++ or use a custom op library
2. Register with ONNX Runtime as a custom op domain
3. Provide forward and optionally backward implementations
4. Bundle with the ONNX model or as a shared library

### Alternatives to Custom Operators

- Rewrite using standard ONNX ops (preferred for portability)
- Decompose complex operations into equivalent sequences
- Move custom logic to preprocessing (outside the model graph)
- Use ONNX Runtime contrib ops when available

---

## ONNX Runtime Optimization

### Graph Optimization Passes

| Pass | Description | Impact |
|------|-------------|--------|
| Constant folding | Pre-compute constant subgraphs | Reduces runtime computation |
| Dead code elimination | Remove unused nodes | Smaller graph, faster loading |
| Layout optimization | Optimize tensor memory layout | Better hardware utilization |
| Node fusion | Merge consecutive ops into single kernel | Reduces kernel launch overhead |
| Arithmetic simplification | Simplify mathematical expressions | Fewer operations |
| Cast elimination | Remove unnecessary type conversions | Reduces overhead |

### ONNX Runtime Execution Providers

| Provider | Hardware | Use Case |
|----------|---------|----------|
| CUDAExecutionProvider | NVIDIA GPU | Server inference |
| TensorrtExecutionProvider | NVIDIA GPU (TensorRT) | Max GPU performance |
| CPUExecutionProvider | CPU | Fallback, CPU serving |
| OpenVINOExecutionProvider | Intel CPU/GPU | Intel hardware |
| CoreMLExecutionProvider | Apple Silicon | Edge/Mac deployment |

### Optimization Level Configuration

```
SessionOptions:
  graph_optimization_level: ORT_ENABLE_ALL
  optimization_level: 99  # Maximum optimization
  enable_mem_pattern: true
  enable_cpu_mem_arena: true
  execution_mode: ORT_PARALLEL
  intra_op_num_threads: 4
  inter_op_num_threads: 4
```

---

## Graph Optimization for Recommendation Models

### Embedding-Specific Optimizations

- **Constant embedding**: If embeddings don't change, fold them into constants
- **Sparse embedding**: Use sparse tensor format for sparse features
- **Quantized embedding**: Convert embeddings to INT8/INT4 before export
- **Embedding lookup fusion**: Merge embedding lookup + concatenation into single op

### Feature Interaction Optimizations

- **Cross-layer fusion**: Fuse consecutive cross layers into single computation
- **Attention fusion**: Merge Q/K/V projection + attention + output projection
- **Batch normalization folding**: Fold BN into preceding linear layer
- **Activation function fusion**: Fuse activations with preceding ops

### Multi-Tower Optimizations

- **Tower parallelization**: Execute independent towers in parallel (inter-op parallelism)
- **Score fusion**: Merge score computation from multiple towers
- **Candidate pruning**: Embed pruning logic in the graph for early candidate elimination

---

## Quantization Within ONNX

### Static Quantization

- Quantize model weights and activations using calibration data
- 8-bit integers for weights and activations
- Requires representative calibration dataset (100-1000 samples)
- Best speedup on hardware with INT8 support

### Dynamic Quantization

- Weights are quantized at export; activations quantized at runtime
- No calibration data needed
- Slightly less optimal than static quantization
- Good for variable-input-size recommendation models

### Quantization-Aware Export

- Export from PyTorch with quantization nodes already inserted
- Ensures quantization is part of the training-aware optimization
- Most accurate approach for quantized models
- Use `torch.quantization` before ONNX export

### INT4 Quantization

- Microsoft's ONNX Runtime supports INT4 weight-only quantization
- 8x memory reduction for embedding-heavy models
- Quality validation essential: check accuracy degradation per layer
- Use AdaRound or GPTQ-style quantization for best results

---

## Deployment Pipeline

### Export Workflow

1. Train model in PyTorch
2. Validate model on test set (record baseline metrics)
3. Export to ONNX with dynamic shapes
4. Run ONNX shape inference and validation
5. Apply ORT graph optimizations
6. Quantize if applicable
7. Benchmark latency on target hardware
8. Validate ONNX model metrics match baseline
9. Version and store ONNX model with metadata
10. Deploy to serving infrastructure

### Validation Checklist

- Output numerical equivalence (FP32 tolerance: 1e-5)
- Dynamic shape correctness at min, typical, and max sizes
- Latency SLA compliance on target hardware
- Memory usage within deployment constraints
- No regression in recommendation quality metrics (NDCG, AUC)
- Correct behavior for edge cases (empty input, single item, max batch)

### Versioning

- Store ONNX model with opset version in filename/metadata
- Track export configuration (PyTorch version, ORT version, quantization settings)
- Maintain mapping: ONNX version ↔ PyTorch checkpoint ↔ training experiment
- Enable rollback to previous ONNX version if quality issues arise
