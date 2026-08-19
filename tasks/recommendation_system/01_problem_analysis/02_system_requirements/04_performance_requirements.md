# Performance Requirements — Recommendation System

## 1. Latency Budget Breakdown

### 1.1 End-to-End Latency Decomposition

A recommendation request travels through multiple stages, each consuming a portion of the total latency budget. For a target end-to-end P95 latency of 200ms, the budget is allocated as follows:

| Stage | P50 Budget | P95 Budget | P99 Budget | Description |
|-------|-----------|-----------|-----------|-------------|
| API Gateway / Auth | 2 ms | 5 ms | 10 ms | Request parsing, authentication, rate limiting |
| Feature Retrieval | 5 ms | 10 ms | 25 ms | Fetch user/item features from feature store |
| Candidate Generation | 10 ms | 20 ms | 40 ms | Retrieve candidate item set (ANN search, rules) |
| Scoring / Ranking | 5 ms | 15 ms | 30 ms | Score candidates with ML model |
| Re-Ranking | 3 ms | 8 ms | 15 ms | Business rules, diversity, freshness, dedup |
| Serialization / Response | 1 ms | 2 ms | 5 ms | Response serialization, compression |
| **Total** | **26 ms** | **60 ms** | **125 ms** | |
| **Network Overhead (2 hops)** | **~10 ms** | **~30 ms** | **~60 ms** | Inter-service network RTT |
| **Grand Total** | **~36 ms** | **~90 ms** | **~185 ms** | |

**Key Principle**: Every millisecond matters. At scale, a 10ms latency reduction across 50M daily requests translates to 500,000 user-hours saved per year.

### 1.2 Latency vs Accuracy Trade-Off

- **Aggressive Truncation**: Candidate generation can use approximate nearest neighbor (ANN) search with configurable recall/latency trade-off — e.g., 95% recall at 5ms vs 99% recall at 20ms.
- **Model Complexity Budget**: Ranking model inference must complete within the scoring budget; if a more accurate model exceeds the budget, use knowledge distillation to create a faster student model.
- **Early Exit**: The re-ranking stage should support early exit — if the first K candidates already meet quality thresholds, skip processing the full candidate set.

---

## 2. Latency Percentile Targets

### 2.1 Why Percentiles Matter

- **P50 (Median)**: Represents the typical user experience. Must be fast to ensure most users feel the system is responsive.
- **P95**: Represents the worst-case experience for 1 in 20 users. Must still be acceptable to prevent user frustration.
- **P99**: Represents the extreme tail. Even at 1%, with millions of daily requests, this affects tens of thousands of users.
- **P99.9**: Represents system boundary conditions. Useful for identifying cascading failure modes.

### 2.2 Target Percentiles by Endpoint

| Endpoint | P50 | P95 | P99 | P99.9 | Timeout |
|----------|-----|-----|-----|-------|---------|
| `/recommendations/home` | 50 ms | 150 ms | 300 ms | 500 ms | 1000 ms |
| `/recommendations/similar/{item_id}` | 30 ms | 100 ms | 200 ms | 400 ms | 800 ms |
| `/recommendations/for-you` | 60 ms | 180 ms | 350 ms | 600 ms | 1200 ms |
| `/recommendations/search-rerank` | 40 ms | 120 ms | 250 ms | 450 ms | 900 ms |
| `/recommendations/email-batch` | N/A | N/A | N/A | N/A | 30 min (batch) |
| `/feedback/event` | 10 ms | 30 ms | 50 ms | 100 ms | 200 ms |

### 2.3 Latency Regression Detection

- **Continuous Latency Monitoring**: P50, P95, P99 must be computed over 1-minute rolling windows and alerted when thresholds are breached.
- **Latency Regression Budget**: Each new feature or model deployment is allowed a maximum of 5ms P95 regression; anything beyond requires explicit approval.
- **A/B Test Latency Guardrails**: Experiments must be automatically paused if the treatment group's P95 latency exceeds the control group's by more than 10%.

---

## 3. Queries Per Second (QPS) Estimation

### 3.1 QPS Calculation Methodology

```
Average QPS = DAU × Average Requests per User per Day / 86,400
Peak QPS = Average QPS × Peak-to-Average Ratio
Peak-to-Average Ratio = Typically 3–5× for consumer applications
```

### 3.2 QPS by Traffic Profile

| Traffic Profile | DAU | Requests/User/Day | Avg QPS | Peak QPS (4×) |
|----------------|-----|-------------------|---------|----------------|
| Early Stage | 1M | 10 | 116 | 464 |
| Growth Stage | 10M | 15 | 1,736 | 6,944 |
| Scale Stage | 50M | 20 | 11,574 | 46,296 |
| Global Scale | 200M | 25 | 57,870 | 231,481 |

### 3.3 QPS by Recommendation Type

| Recommendation Type | % of Total QPS | Peak QPS (at 50M DAU) | Scaling Consideration |
|-------------------|---------------|----------------------|----------------------|
| Home Page Recs | 35% | 16,204 | Cacheable, high reuse |
| For-You Feed | 25% | 11,574 | Requires real-time features |
| Similar Items | 20% | 9,259 | Item-based, highly cacheable |
| Search Re-Ranking | 15% | 6,944 | Query-dependent, less cacheable |
| Email/Notification Recs | 5% | 2,315 | Batch-generated, low real-time load |

---

## 4. Concurrent User Handling

### 4.1 Concurrency Modeling

- **Concurrent Users Estimation**: Concurrent users ≈ DAU × (Average Session Duration / 86,400). For 50M DAU with 20-minute average sessions: 50M × (20 × 60) / 86,400 ≈ 694,444 concurrent users.
- **Request Fan-Out**: Each page load may trigger 3–5 concurrent recommendation requests (home page + trending + personalized carousel + ad slots), multiplying effective concurrency.
- **Connection Pool Sizing**: Each service must maintain connection pools sized for peak concurrent requests with 20% headroom.

### 4.2 Concurrency Control

- **Rate Limiting**: Per-user rate limits (e.g., 100 requests/minute) to prevent abuse and ensure fair resource allocation.
- **Request Queuing**: When the system is at capacity, low-priority requests (email recommendations, analytics events) must be queued; high-priority requests (home page, search) must be served immediately.
- **Load Shedding**: Under extreme load, the system must shed non-critical requests (e.g., "similar items" carousel) to preserve capacity for core recommendation endpoints.

---

## 5. Time-to-First-Recommendation (TTFR)

### 5.1 Cold-Start TTFR

- **New User**: First recommendation must be served within 500ms of account creation, using popularity-based or content-based fallback.
- **New Item**: An item must appear in recommendation candidates within 5 minutes of catalog ingestion, using content-based features (no collaborative signal yet).
- **New Feature**: When a new feature is added to the model, the feature must be available in the feature store within 1 hour of deployment.

### 5.2 Session TTFR

- **First Request in Session**: The very first recommendation request in a session may have slightly higher latency (10–20ms) due to cold cache misses; subsequent requests should be faster.
- **Return User**: A returning user should receive personalized recommendations (not generic) on their first request of the session, leveraging persisted user embeddings.

### 5.3 Model TTFR

- **Training to Serving**: The time from model training completion to serving live traffic must be ≤ 30 minutes, including evaluation, validation, deployment, and traffic ramp-up.
- **Experiment TTFR**: New A/B test variants must be launchable within 5 minutes of configuration approval, without requiring model retraining.

---

## 6. Model Inference Constraints

### 6.1 Inference Latency Budgets

| Model Component | Latency Budget | Optimization Strategy |
|----------------|---------------|----------------------|
| Embedding Lookup | ≤ 2 ms | Pre-computed embeddings, in-memory cache |
| Feature Transform | ≤ 3 ms | Vectorized operations, pre-computed features |
| Forward Pass (Ranking) | ≤ 10 ms | TensorRT optimization, quantization, batching |
| Score Post-Processing | ≤ 2 ms | Simple arithmetic, GPU-accelerated |
| **Total Inference** | **≤ 17 ms** | |

### 6.2 Throughput Requirements

- **Batch Inference**: The ranking model must support batch inference with batch sizes up to 256 candidates, achieving ≥ 10,000 inferences/second on a single GPU.
- **Streaming Inference**: For real-time use cases, the model must support single-request inference with ≤ 15ms latency.
- **Model Scaling**: Inference throughput must scale linearly with GPU count up to 8 GPUs per serving node, with < 10% overhead from inter-GPU communication.

### 6.3 Model Optimization Techniques

| Technique | Latency Reduction | Accuracy Impact | Implementation Effort |
|-----------|-------------------|-----------------|----------------------|
| FP16 Quantization | 30–50% | Negligible (<0.1% metric drop) | Low |
| INT8 Quantization | 50–70% | Small (0.1–0.5% metric drop) | Medium |
| Knowledge Distillation | 40–60% | Small (0.2–1% metric drop) | High |
| TensorRT Compilation | 20–40% | None (numerically equivalent) | Medium |
| Feature Pruning | 10–30% | Depends on features removed | Low |
| ONNX Runtime | 15–30% | None | Low |

---

## 7. End-to-End Optimization Strategy

### 7.1 Pipeline Parallelism

- **Parallel Feature Retrieval**: User features and item features must be fetched in parallel, not sequentially, reducing feature retrieval latency by ~40%.
- **Speculative Candidate Generation**: While the first batch of candidates is being scored, the next batch can be retrieved, overlapping I/O with compute.
- **Asynchronous Logging**: Request logging and metric emission must be non-blocking (fire-and-forget) to avoid adding latency to the serving path.

### 7.2 Caching at Every Layer

| Cache Layer | Hit Rate Target | Invalidation Strategy | Latency Savings |
|------------|----------------|----------------------|-----------------|
| CDN Edge Cache | 60–80% | TTL-based (15 min) | 80–90% |
| Application-Level Cache | 40–60% | Event-driven (user action) | 70–85% |
| Feature Store Cache | 80–95% | Write-through | 60–80% |
| Embedding Cache | 90–99% | TTL-based (1 hour) | 90–95% |
| Model Prediction Cache | 20–40% | TTL-based (5 min) | 95–99% |

### 7.3 Resource Efficiency

- **P99 Budget Awareness**: Design for P99, not P50. A system optimized only for median latency will have unacceptable tail latency under load.
- **Noisy Neighbor Prevention**: Each service must have dedicated resource pools (CPU, memory, network) to prevent one component from starving another.
- **Garbage Collection Tuning**: JVM-based services must use low-latency GC (ZGC, Shenandoah) with target < 10ms pause times to avoid latency spikes.
- **Zero-Copy Serialization**: Use efficient serialization formats (Protobuf, FlatBuffers, Arrow IPC) to minimize serialization/deserialization overhead.
