# Latency Testing

## 1. Overview

Latency is the most user-visible performance metric for recommendation systems. Users
expect personalized recommendations to appear within milliseconds of opening an app or
page. This document covers end-to-end latency measurement, component-level profiling,
percentile distribution analysis, latency regression detection, and network latency
simulation for production-grade recommendation systems.

### 1.1 Latency Requirements by Interface

| Interface | P50 Target | P99 Target | P999 Target | Hard Timeout |
|---|---|---|---|---|
| Home page recommendations | < 50ms | < 100ms | < 200ms | 500ms |
| Related items | < 30ms | < 80ms | < 150ms | 300ms |
| Search results | < 100ms | < 200ms | < 400ms | 1000ms |
| Push notification recs | < 500ms | < 1000ms | < 2000ms | 5000ms |
| Batch prediction | < 5000ms | < 15000ms | < 30000ms | 60000ms |
| Model training (per epoch) | - | - | - | 3600s |

### 1.2 Latency Components

```
Total Latency = Network + API Gateway + Auth + Feature Fetch + Model Inference + Post-processing + Serialization
                  ↓         ↓          ↓        ↓              ↓                  ↓                 ↓
               DNS+TLS   Routing   JWT      Redis/Hive    GPU/CPU            Business         JSON/
               +TCP      +LB      verify    read          inference         logic             Protobuf
```

---

## 2. End-to-End Latency Measurement

### 2.1 Measurement Points

Instrument every significant boundary in the request path:

```
Client Request
    ↓ [T0] Client timestamp
DNS Resolution
    ↓ [T1]
TCP + TLS Handshake
    ↓ [T2]
API Gateway Receives Request
    ↓ [T3]
Authentication Middleware
    ↓ [T4]
Request Parsing
    ↓ [T5]
Feature Store Read (start)
    ↓ [T6] Feature Store Read (end)
Model Inference (start)
    ↓ [T7] Model Inference (end)
Post-processing
    ↓ [T8]
Response Serialization
    ↓ [T9]
API Gateway Sends Response
    ↓ [T10]
Client Receives Response
```

**Key latency segments:**

| Segment | Calculation | Typical Value |
|---|---|---|
| Network round-trip | T1 - T0 | 5-50ms |
| API processing | T9 - T3 | 20-100ms |
| Feature fetch | T6 - T5 | 1-10ms |
| Model inference | T7 - T6 | 5-50ms |
| Post-processing | T8 - T7 | 1-5ms |
| Serialization | T9 - T8 | 1-3ms |

### 2.2 Distributed Tracing Integration

Use distributed tracing (Jaeger, Zipkin, AWS X-Ray) for automatic latency measurement:

- **Trace propagation**: Inject trace context into all service-to-service calls
- **Span creation**: Each service creates spans with timing information
- **Sampling strategy**: Adaptive sampling (100% for slow requests, 1% for normal)
- **Trace analysis**: Automated identification of latency bottlenecks

### 2.3 Client-Side Latency Measurement

Don't forget client-side latency in end-to-end measurements:

| Client Component | Measurement | Target |
|---|---|---|
| DNS resolution | Time to resolve API hostname | < 20ms (cached) |
| TLS handshake | Time to establish secure connection | < 50ms |
| Request serialization | Time to encode request | < 5ms |
| Response deserialization | Time to decode response | < 10ms |
| UI rendering | Time to display recommendations | < 100ms |

### 2.4 Latency Measurement Infrastructure

- **High-resolution timers**: Use monotonic clocks (nanosecond precision)
- **Clock synchronization**: NTP-synchronized clocks across all services
- **Histogram-based collection**: Store latency distributions, not just averages
- **Percentile computation**: Compute P50, P90, P95, P99, P99.9 in real-time
- **Aggregation**: Aggregate latencies across services, regions, and endpoints

---

## 3. Component-Level Latency Profiling

### 3.1 Feature Store Latency

| Operation | Target | Measurement Method |
|---|---|---|
| Single feature read | < 2ms p99 | Direct Redis/DB read timing |
| Batch feature read (100 features) | < 10ms p99 | Multi-key read timing |
| Feature computation (real-time) | < 5ms p99 | Streaming pipeline latency |
| Feature store write | < 5ms p99 | Write operation timing |
| Feature store connection | < 1ms | Connection pool timing |

**Feature store latency optimization:**

- **Connection pooling**: Maintain persistent connections to avoid TCP overhead
- **Pipeline reads**: Batch multiple feature reads into single round-trip
- **Local caching**: Cache frequently accessed features in application memory
- **Pre-fetching**: Pre-fetch features based on user context before explicit request

### 3.2 Model Inference Latency

| Component | Target | Optimization |
|---|---|---|
| Input preprocessing | < 1ms | Vectorized operations |
| Embedding lookup | < 2ms | GPU-accelerated, pre-loaded |
| Forward pass | < 20ms | Optimized model (ONNX, TensorRT) |
| Output processing | < 1ms | Batched operations |
| Model loading (cold) | < 30s | Warm standby, pre-loading |

**Model inference profiling tools:**

- **PyTorch Profiler**: Layer-by-layer timing breakdown
- **NVIDIA Nsight**: GPU kernel-level profiling
- **ONNX Runtime Profiler**: Optimized inference path analysis
- **Custom instrumentation**: Function-level timing in inference code

### 3.3 API Gateway Latency

| Component | Target | Factors |
|---|---|---|
| TLS termination | < 5ms | Hardware acceleration |
| Rate limiting check | < 1ms | In-memory counters |
| Request routing | < 1ms | Route table lookup |
| Load balancing | < 1ms | Algorithm complexity |
| Response caching | < 1ms | Cache hit/miss |

### 3.4 Database Latency

| Operation | Target | Notes |
|---|---|---|
| Point query (user profile) | < 5ms | Indexed lookup |
| Range query (item catalog) | < 20ms | Indexed range scan |
| Aggregate query (analytics) | < 100ms | Pre-computed aggregations |
| Write (event logging) | < 10ms | Async write acceptable |
| Connection acquisition | < 2ms | Connection pool warm |

---

## 4. Percentile Distribution Analysis

### 4.1 Why Percentiles Matter

Average latency is misleading for recommendation systems because:

- Most requests are fast (cached, simple)
- A few requests are slow (complex features, cold model)
- Average hides the slow tail
- Users experience the tail, not the average

**Example latency distribution:**

| Percentile | Latency | User Experience |
|---|---|---|
| P50 | 35ms | Excellent |
| P90 | 72ms | Good |
| P95 | 89ms | Acceptable |
| P99 | 145ms | Degraded |
| P99.9 | 280ms | Poor |
| Max | 1200ms | Timeout territory |

### 4.2 Percentile Monitoring

**Real-time percentile computation:**

- **T-digest**: Streaming quantile estimation with bounded memory
- **HDR Histogram**: High Dynamic Range histogram for accurate percentile tracking
- **CKMS quantiles**: Probabilistic quantile estimation
- **Exponential histograms**: Compact representation for high-throughput systems

**Alert thresholds:**

| Percentile | Warning | Critical | Action |
|---|---|---|---|
| P50 | > 50ms | > 80ms | Investigate common path |
| P95 | > 100ms | > 150ms | Profile slow path |
| P99 | > 150ms | > 250ms | Urgent investigation |
| P99.9 | > 300ms | > 500ms | Immediate escalation |

### 4.3 Latency Distribution Shape Analysis

| Distribution Shape | Diagnosis | Common Cause |
|---|---|---|
| Normal (bell curve) | Healthy | Natural variation |
| Bimodal | Two distinct paths | Cache hit vs. miss |
| Long tail | Occasional slow requests | Cold model, GC pauses |
| Heavy tail | Frequent slow requests | Resource contention |
| Multi-modal | Multiple distinct behaviors | A/B test with different models |

### 4.4 Tail Latency Analysis

Deep analysis of the slowest requests:

- **Request classification**: Group slow requests by feature (endpoint, user type, item type)
- **Root cause correlation**: Correlate slow requests with system metrics (CPU, memory, GC)
- **Trace analysis**: Sample and analyze individual slow request traces
- **Temporal patterns**: Identify time-based patterns in tail latency

---

## 5. Latency Regression Detection

### 5.1 Baseline Establishment

Establish latency baselines for every endpoint and operation:

| Baseline | Period | Percentiles | Update Frequency |
|---|---|---|---|
| Daily baseline | Previous 7 days | P50, P95, P99 | Daily |
| Weekly baseline | Previous 4 weeks | P50, P95, P99 | Weekly |
| Release baseline | Previous release | P50, P95, P99 | Per release |
| Feature baseline | Feature introduction | P50, P95, P99 | Per feature |

### 5.2 Regression Detection Methods

**Statistical methods:**

- **Z-score**: Flag when current latency deviates > 3σ from baseline
- **Change point detection**: Detect statistically significant shifts using PELT or BOCPD
- **Hypothesis testing**: Compare current distribution against baseline using KS test
- **Control charts**: SPC (Statistical Process Control) charts for continuous monitoring

**Automated detection pipeline:**

```
Metrics Collection → Baseline Comparison → Statistical Test → Alert Decision
        ↓                    ↓                    ↓                ↓
   Prometheus/         Historical          Z-score,          Alert/
   StatsD              baseline            KS test           No Alert
                                           comparison
```

### 5.3 Regression Root Cause Analysis

When latency regression is detected:

1. **Identify change**: What changed since baseline? (code, config, data, infrastructure)
2. **Narrow scope**: Which endpoint, operation, or component shows regression?
3. **Correlate**: Match regression timing with deployment events
4. **Profile**: Run detailed profiling on affected path
5. **Fix**: Implement fix and validate against baseline
6. **Prevent**: Add latency assertion to CI pipeline

### 5.4 CI/CD Latency Gates

Prevent latency regressions from reaching production:

| Gate | Criteria | Action on Failure |
|---|---|---|
| Unit test latency | Function execution time within budget | Block merge |
| Integration test latency | API endpoint latency within baseline | Block merge |
| Load test latency | P99 latency within 5% of baseline | Block deploy |
| A/B test latency | Treatment latency within 5% of control | Block full rollout |

---

## 6. Network Latency Simulation

### 6.1 Network Conditions to Simulate

| Condition | Latency | Packet Loss | Bandwidth | Use Case |
|---|---|---|---|---|
| Excellent WiFi | 5ms | 0% | 100 Mbps | Best case |
| Good WiFi | 20ms | 0.1% | 50 Mbps | Typical |
| Mobile 4G | 40ms | 0.5% | 20 Mbps | Mobile users |
| Mobile 3G | 100ms | 1% | 2 Mbps | Rural areas |
| Satellite | 600ms | 2% | 1 Mbps | Remote areas |
| Congested | 200ms | 5% | 5 Mbps | Peak hours |
| Degraded | 500ms | 10% | 1 Mbps | Network issues |

### 6.2 Network Simulation Tools

| Tool | Platform | Features |
|---|---|---|
| tc (traffic control) | Linux | Latency, loss, bandwidth simulation |
| Toxiproxy | Docker | Application-level network fault injection |
| Comcast | Cross-platform | User-friendly network simulation |
| Netflix Chaos Monkey | AWS | Automated network partition simulation |
| Charles Proxy | Desktop | Request/response manipulation and delay |

### 6.3 Inter-Service Latency Impact

Recommendation systems have multiple service calls. Network latency compounds:

```
User → API Gateway (5ms) → Auth Service (5ms) → Feature Store (5ms) → Model Serving (5ms) → Response (5ms)
Total network overhead: 25ms × 2 (round trip) = 50ms
```

**Mitigation strategies:**

- **Request coalescing**: Combine multiple service calls into single request
- **Predictive pre-fetching**: Start feature fetch before user request arrives
- **Connection multiplexing**: Reuse connections across requests
- **Service mesh optimization**: Use gRPC with HTTP/2 multiplexing
- **Geographic placement**: Deploy services in same availability zone

### 6.4 Client Network Impact

How network conditions affect user-perceived latency:

| Network | Client Overhead | Total Recommendation Latency |
|---|---|---|
| Excellent WiFi | 10ms | 45ms (35ms server + 10ms network) |
| Mobile 4G | 80ms | 115ms (35ms server + 80ms network) |
| Mobile 3G | 200ms | 235ms (35ms server + 200ms network) |
| Degraded | 1000ms | 1035ms (35ms server + 1000ms network) |

**Client-side optimizations for poor networks:**

- **Response compression**: gzip/brotli for 60-80% size reduction
- **Predictive caching**: Cache recommendations client-side
- **Progressive loading**: Show cached results immediately, update when fresh data arrives
- **Request deduplication**: Don't send duplicate requests while one is in-flight
- **Offline fallback**: Serve cached recommendations when offline

---

## 7. Latency Testing Framework

### 7.1 Latency Test Execution

| Test Type | Duration | Load Level | Frequency |
|---|---|---|---|
| Baseline measurement | 30 minutes | Expected peak | Weekly |
| Regression detection | 15 minutes | Expected peak | Per deploy |
| Tail latency analysis | 60 minutes | 2x peak | Monthly |
| Network simulation | 30 minutes | Expected peak | Monthly |
| Cold start latency | 10 minutes | Low (warm-up) | Per deploy |

### 7.2 Latency Reporting

**Latency dashboard components:**

- **Real-time latency graph**: Live P50, P95, P99 lines
- **Latency heatmap**: Latency distribution by time and endpoint
- **Regression alerts**: Automated alerts for baseline deviations
- **Component breakdown**: Latency contribution by service component
- **Historical trends**: Week-over-week and month-over-month comparison

### 7.3 Latency Optimization Playbook

When latency exceeds targets:

1. **Profile the hot path**: Use distributed tracing to find the slowest segment
2. **Check cache hit rates**: Low cache hits are the most common cause
3. **Check feature store latency**: Feature reads are often the bottleneck
4. **Check model complexity**: Model may be too large for latency budget
5. **Check GC behavior**: JVM garbage collection pauses cause tail latency
6. **Check network topology**: Services may be in different availability zones
7. **Check connection pools**: Pool exhaustion causes queuing delays
