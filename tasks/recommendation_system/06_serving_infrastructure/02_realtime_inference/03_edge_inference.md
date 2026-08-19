# Edge Inference for Recommendation Systems

## Overview

Edge inference brings recommendation computation to the user's device, eliminating network latency, enabling offline recommendations, and improving privacy. As mobile and IoT devices become more powerful, on-device recommendation models are increasingly feasible. This covers model compression for edge, federated inference, offline recommendations, and edge caching.

---

## On-Device Recommendation Models

### Device Hardware Profiles

| Device Class | CPU | RAM | GPU/NPU | Example |
|-------------|-----|-----|---------|---------|
| Flagship phone | 8 cores, 3+ GHz | 8-16 GB | Adreno/Mali + NPU | iPhone 15, Pixel 8 |
| Mid-range phone | 8 cores, 2 GHz | 4-8 GB | Basic GPU + NPU | Samsung A-series |
| Smart TV | 4 cores, 1.5 GB | 2-4 GB | Basic GPU | Android TV |
| Smart speaker | 4 cores, 1 GHz | 1-2 GB | None | Echo, Google Home |
| Wearable | 2 cores, 500 MHz | 256-512 MB | None | Apple Watch |

### On-Device Model Requirements

| Constraint | Target | Rationale |
|-----------|--------|-----------|
| Model size | < 50 MB | App store limits, memory constraints |
| Inference latency | < 10 ms | Real-time user experience |
| RAM usage | < 100 MB | Co-exist with other app features |
| Battery impact | < 5% per session | User experience preservation |
| Startup time | < 500 ms | Fast recommendation availability |

### Model Architectures for Edge

**Lightweight Collaborative Filtering**:
- Small embedding tables (feature hashing, quantized)
- Shallow MLP (1-2 layers, 64-128 hidden units)
- Quantized to INT8 for inference

**Content-Based Models**:
- TF-IDF or BM25 for text features
- Lightweight CNN for image features
- Simple similarity computation

**Rule-Based with ML Hybrid**:
- Rules for most common cases (fast path)
- ML model for complex/ambiguous cases
- Graceful degradation to rules if ML unavailable

---

## Model Compression for Edge

### Quantization

| Precision | Size Reduction | Speedup | Quality Impact |
|-----------|---------------|---------|---------------|
| FP32 → FP16 | 2x | 1.5x | Negligible |
| FP32 → INT8 | 4x | 2-3x | < 0.5% |
| FP32 → INT4 | 8x | 3-5x | 0.5-1.5% |
| FP32 → Binary | 32x | 10x+ | 1-3% |

### Pruning for Edge

- Target 70-90% sparsity for embedding tables
- Structured pruning for hardware acceleration
- Remove entire embedding dimensions for rare features
- Use sparse matrix operations supported by mobile frameworks

### Knowledge Distillation for Edge

- Train large teacher model server-side
- Distill to small student model for edge deployment
- Use soft targets for richer knowledge transfer
- Consider multi-teacher distillation from ensemble

### Framework Support

| Framework | Quantization | Pruning | Hardware Support |
|-----------|-------------|---------|-----------------|
| TensorFlow Lite | INT8, FP16 | Structured | CPU, GPU, NNAPI, EdgeTPU |
| Core ML | INT8, INT4 | Auto | Apple Neural Engine |
| ONNX Runtime Mobile | INT8 | Basic | CPU, GPU |
| PyTorch Mobile | INT8, FP16 | Basic | CPU, GPU |
| MNN (Alibaba) | INT8, INT4 | Advanced | CPU, GPU, NPU |

---

## Federated Inference

### Concept

Keep user data on-device; only share model updates (not raw data) with the server. Combines privacy with collective learning.

### Federated Learning Pipeline

```
Server sends global model → Device trains on local data → 
Device sends model updates → Server aggregates updates → 
Updated global model → Repeat
```

### Federated Recommendation

1. Each user's device trains on their local interaction history
2. Model updates (gradients) are sent to server
3. Server aggregates updates from many users (Federated Averaging)
4. Updated model pushed to all devices
5. Users benefit from collective patterns without sharing data

### Privacy Considerations

- **Differential privacy**: Add calibrated noise to model updates
- **Secure aggregation**: Encrypt updates so server sees only aggregate
- **On-device inference**: No raw data leaves the device
- **Gradient clipping**: Bound individual contribution to prevent information leakage

### Challenges for Recommendation Systems

- **Data heterogeneity**: User preferences are highly non-IID
- **Communication cost**: Large embedding tables are expensive to transmit
- **Model convergence**: Federated training converges slower than centralized
- **Free riders**: Some users contribute little data but benefit from others

---

## Offline Recommendations

### When Offline Mode Is Needed

- No network connectivity (airplane, underground)
- Privacy-sensitive contexts
- Battery conservation mode
- Initial app startup before network connection

### Offline Recommendation Strategies

**Pre-Cached Recommendations**:
- Store top-N recommendations computed during last online session
- Refresh periodically when connectivity is available
- Prioritize caching high-quality recommendations

**On-Device Computation**:
- Run lightweight model on cached features
- Use only local interaction history
- Quality degrades with time since last sync

**Hybrid Offline**:
- Combine cached recommendations with on-device computation
- Use popularity-based fallback for unknown items
- Serve cached recommendations first, augment with on-device scoring

### Offline Cache Management

| Strategy | Cache Size | Freshness | Quality |
|----------|-----------|-----------|---------|
| Top-N per category | Small (100 items) | High | High |
| Full catalog scores | Large (10K+ items) | Medium | Medium |
| Hybrid | Medium (500 items) | High | High |
| Adaptive | Variable | Based on usage | Best |

---

## Edge Caching

### Cache Architecture

```
App → Local Cache (SQLite/Realm) → On-Device Model → Network (fallback)
```

### Cache Layers

| Layer | Storage | Latency | Capacity |
|-------|---------|---------|----------|
| L1: Memory | RAM | < 1 ms | 10-50 MB |
| L2: Disk | SQLite/Realm | 1-5 ms | 100 MB - 1 GB |
| L3: Network | Server cache | 10-50 ms | Unlimited |

### Cache Invalidation

- **Time-based**: Expire after configurable TTL
- **Event-based**: Invalidate on user action (purchase, hide)
- **Model-based**: Invalidate when model updates
- **User-triggered**: Manual refresh by user

### Cache Warming

- Pre-load popular recommendations at app startup
- Warm cache during background sync
- Prioritize warming for high-traffic categories
- Use prediction to pre-fetch likely-needed recommendations

---

## Deployment and Updates

### Model Update Strategy

- **OTA updates**: Push new models via app update mechanism
- **Background download**: Download model updates when on WiFi
- **Delta updates**: Send only model weight changes (smaller downloads)
- **A/B testing**: Serve different model versions to different users

### Rollback on Device

- Keep previous model version as fallback
- If new model causes errors or poor metrics, revert locally
- Server can trigger rollback for specific model versions
- User can manually revert if experiencing issues

### Monitoring Edge Models

- Report inference latency distribution from device telemetry
- Track model performance metrics (click-through, engagement)
- Monitor device resource usage (battery, memory, CPU)
- Aggregate metrics server-side for model quality assessment
