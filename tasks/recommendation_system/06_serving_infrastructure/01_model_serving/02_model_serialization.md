# Model Serialization for Recommendation Systems

## Overview

Model serialization converts trained models into formats suitable for deployment, serving, and long-term storage. For recommendation systems, serialization must preserve complex architectures (embedding tables, attention layers, feature interactions), support efficient inference, and enable version management across training and serving environments.

---

## PyTorch State Dict

### Standard Serialization

The most common PyTorch serialization method: saves model parameters as a dictionary of tensors.

```python
# Save
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch,
    'loss': loss,
}, 'checkpoint.pt')

# Load
checkpoint = torch.load('checkpoint.pt')
model.load_state_dict(checkpoint['model_state_dict'])
```

### State Dict Characteristics

| Property | Description |
|----------|-------------|
| Format | Python dict mapping string keys to tensor values |
| Size | Proportional to model parameter count |
| Portability | PyTorch-only; not cross-framework |
| Embedding tables | Stored as full dense tensors (even if sparse) |
| Optimizer states | Can be large (Adam: 3x model size) |

### State Dict for Recommendation Models

**Embedding Tables**:
- Large embedding tables dominate state dict size
- Store as sparse tensors if most embeddings are unused
- Consider sharding across multiple files for very large tables
- Include feature-to-index mapping for reconstruction

**Dense Layers**:
- Standard tensor storage
- Include weight, bias, and any normalization parameters
- Batch norm running statistics stored separately

### Chunked Serialization

For models exceeding available disk memory:
- Split state dict into multiple chunks
- Save embedding tables separately from dense layers
- Use `torch.save` with file-like objects for streaming
- Parallel save/load across chunks

---

## TorchScript

### Concept

TorchScript is a statically-typed subset of Python that can be compiled and optimized for production inference. It creates a serialized representation of the model graph that doesn't require Python runtime.

### Scripting vs Tracing

| Method | Approach | Pros | Cons |
|--------|----------|------|------|
| `torch.jit.script` | Compiles Python to TorchScript IR | Handles control flow | Requires type annotations |
| `torch.jit.trace` | Records operations from example input | Simple, handles any model | No dynamic control flow |
| `torch.jit.script_module` | Scripts a full module | Complete module graph | More verbose |

### TorchScript for Recommendation Models

**Challenges**:
- Dynamic dictionary lookups for embedding tables
- Conditional logic in feature processing
- Dynamic vocabulary sizes
- Custom loss functions

**Solutions**:
- Use `torch.jit.script` for models with control flow
- Pre-compute embedding indices in Python, pass tensors to TorchScript
- Use `@torch.jit.export` for specific methods
- Test scripted model output matches eager mode output

### TorchScript Optimization

- Operator fusion (conv+bn, linear+relu)
- Constant propagation
- Dead code elimination
- Common subexpression elimination
- Memory planning for tensor allocation

---

## ONNX Format

### Benefits for Recommendation Systems

| Benefit | Description |
|---------|-------------|
| Framework agnostic | Train in PyTorch, serve in ONNX Runtime |
| Hardware optimization | TensorRT, OpenVINO, CoreML support |
| Graph optimization | Built-in optimization passes |
| Quantization | Native INT8/INT4 support |
| Dynamic shapes | Variable batch sizes at inference |

### Export Challenges

- **Embedding tables**: Large static tensors embedded in graph
- **Sparse operations**: Limited ONNX support for sparse tensors
- **Custom operators**: Must register with ONNX runtime
- **Dynamic control flow**: Requires scripting or custom op implementation

### ONNX Export Best Practices

1. Export with dynamic axes for variable batch sizes
2. Validate numerical equivalence with PyTorch output
3. Test on target hardware before production deployment
4. Use opset version compatible with target ONNX Runtime
5. Store ONNX model with metadata (export config, validation results)

---

## PMML (Predictive Model Markup Language)

### When PMML Is Appropriate

- Linear models, tree-based models, and simple neural networks
- Interchange between Java-based ML platforms (Spark MLlib, H2O)
- Regulatory environments requiring model explainability
- Cross-organization model sharing

### PMML Limitations

- Limited support for deep learning architectures
- Cannot represent complex embedding tables or attention mechanisms
- XML-based: verbose, large file sizes
- Not suitable for large-scale recommendation models

---

## SavedModel (TensorFlow)

### TensorFlow Serving Integration

- Native format for TensorFlow Serving
- Includes computation graph and weights
- Supports TensorFlow Lite for mobile/edge
- Versioned directory structure for multiple model versions

### Relevance to Recommendation Systems

- TensorFlow Serving is mature and battle-tested at scale
- Good for models trained in TensorFlow/Keras
- TFX pipeline integration for end-to-end ML workflows
- Less common for PyTorch-based recommendation systems

---

## Pickle vs Safe Alternatives

### Security Concerns with Pickle

- `pickle.loads()` can execute arbitrary code during deserialization
- Loading untrusted pickle files is a security vulnerability
- Model files from external sources should never be loaded with pickle

### Safe Alternatives

| Method | Safety | Speed | Compatibility |
|--------|--------|-------|--------------|
| `torch.save` (uses pickle) | Unsafe with untrusted sources | Fast | PyTorch |
| `safetensors` | Safe (no code execution) | Fast | PyTorch, HF |
| ONNX | Safe | Fast | Cross-framework |
| `torch.load` with `weights_only=True` | Safer | Fast | PyTorch 2.0+ |
| msgpack/binary | Safe | Fast | Custom |

### safetensors for Recommendation Models

- Stores tensors in a flat binary format with metadata
- No code execution during loading
- Memory-mapped loading for large models
- Supported by Hugging Face ecosystem
- Recommended for storing model weights shared across teams

---

## Versioned Model Storage

### Storage Architecture

```
s3://model-registry/
├── homefeed_model/
│   ├── v1.0.0/
│   │   ├── model.onnx
│   │   ├── metadata.json
│   │   ├── config.yaml
│   │   └── validation_report.json
│   ├── v1.1.0/
│   │   ├── model.onnx
│   │   └── ...
│   └── v1.1.0-staging/
│       └── ...
└── search_model/
    └── ...
```

### Metadata Schema

```json
{
  "model_name": "homefeed_ranking",
  "version": "1.3.0",
  "format": "onnx",
  "created_at": "2026-08-15T10:30:00Z",
  "author": "ml-team",
  "git_commit": "abc123def",
  "training_experiment": "exp_20260815_0042",
  "dataset_version": "v2.1",
  "metrics": {
    "ndcg@10": 0.452,
    "auc": 0.789,
    "latency_p99_ms": 15
  },
  "artifacts": {
    "model_path": "s3://model-registry/homefeed_model/v1.3.0/model.onnx",
    "config_path": "s3://model-registry/homefeed_model/v1.3.0/config.yaml",
    "features_path": "s3://model-registry/homefeed_model/v1.3.0/features.json"
  }
}
```

### Storage Best Practices

- Use immutable object storage (S3, GCS) for model artifacts
- Store metadata in a queryable database (not just file system)
- Compress model files if storage cost is a concern
- Implement access control: production models require approval to modify
- Set retention policies: keep N versions per model lineage
- Replicate across regions for disaster recovery
