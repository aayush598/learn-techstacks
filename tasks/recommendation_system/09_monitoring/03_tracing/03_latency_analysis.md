# Latency Analysis for Recommendation Systems

## 1. Overview

Latency analysis decomposes end-to-end request latency into per-stage contributions to identify bottlenecks, detect regressions, and track SLO compliance. In recommendation systems, latency directly impacts user experience — a 100ms increase in response time can reduce engagement by 1–3%. Understanding where latency comes from is essential for targeted optimization.

### 1.1 Latency Budget

Every recommendation system should have a latency budget that allocates maximum time per pipeline stage:

```
Total latency budget: 200ms (P99)

  API Gateway + Network:           10ms (5%)
  Feature Computation:             30ms (15%)
  Candidate Generation:            50ms (25%)
  Ranking (Model Inference):       60ms (30%)
  Post-processing:                 20ms (10%)
  Serialization + Response:        10ms (5%)
  Buffer (safety margin):          20ms (10%)
```

### 1.2 Why Average Latency is Misleading

Average latency hides the tail:

| Metric | Value | User Impact |
|---|---|---|
| Average latency | 80ms | Feels fast |
| P50 latency | 60ms | Half of users get 60ms |
| P95 latency | 150ms | 5% of users get 150ms+ |
| P99 latency | 450ms | 1% of users get 450ms+ |
| Max latency | 3200ms | 0.1% of users get 3.2s |

**Always track percentiles, not averages.**

---

## 2. Percentile Decomposition

### 2.1 What Percentile Decomposition Does

Breaks down P50/P95/P99 latency by pipeline stage:

```
End-to-end P99: 450ms

Decomposition:
  Feature Computation P99:    45ms  (10%)
  Candidate Retrieval P99:   180ms  (40%)  <-- BOTTLENECK
  Ranking P99:               120ms  (27%)
  Post-processing P99:        35ms   (8%)
  Network/Serialization P99:  70ms  (15%)
```

### 2.2 Percentile Metrics

```promql
# P50 latency per stage
histogram_quantile(0.50, rate(rec_stage_latency_seconds_bucket{stage="feature"}[5m]))
histogram_quantile(0.50, rate(rec_stage_latency_seconds_bucket{stage="candidate"}[5m]))
histogram_quantile(0.50, rate(rec_stage_latency_seconds_bucket{stage="ranking"}[5m]))

# P99 latency per stage
histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket{stage="feature"}[5m]))
histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket{stage="candidate"}[5m]))
histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket{stage="ranking"}[5m]))

# P99 contribution ratio (which stage dominates P99)
histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket[5m])) by (stage)
/
sum(histogram_quantile(0.99, rate(rec_stage_latency_seconds_bucket[5m])))
```

### 2.3 Latency Distribution by Percentile

Track how each percentile behaves independently:

| Stage | P50 | P75 | P90 | P95 | P99 |
|---|---|---|---|---|---|
| Feature computation | 8ms | 12ms | 18ms | 25ms | 45ms |
| Candidate retrieval | 20ms | 35ms | 60ms | 95ms | 180ms |
| Ranking | 15ms | 25ms | 40ms | 55ms | 120ms |
| Post-processing | 5ms | 8ms | 12ms | 18ms | 35ms |
| Network overhead | 3ms | 5ms | 8ms | 12ms | 25ms |
| **End-to-end** | **51ms** | **85ms** | **138ms** | **205ms** | **405ms** |

### 2.4 Latent Percentile Analysis

Compare P99/P50 ratio to detect tail latency issues:

```
P99/P50 ratio by stage:
  Feature computation: 45/8 = 5.6x   (healthy: <5x)
  Candidate retrieval: 180/20 = 9.0x (CONCERN: >7x)
  Ranking: 120/15 = 8.0x (CONCERN: >7x)
  Post-processing: 35/5 = 7.0x (monitoring)
```

High P99/P50 ratios indicate:
- Resource contention (CPU, memory, network)
- Cold path issues (cache misses, model cold start)
- Tail latency drivers (specific query patterns, large feature vectors)

---

## 3. Latency Heatmaps

### 3.1 What Latency Heatmaps Show

Heatmaps visualize latency distributions over time:

```
Latency (ms)   Time
0-10ms         ████████████████████████████████████████
10-25ms        ██████████████████████████████████████████████████
25-50ms        ██████████████████████████████████████
50-100ms       ████████████████████
100-250ms      ██████████
250-500ms      ████
500ms-1s       ██
1s+            █
```

### 3.2 Heatmap Metrics

```promql
# Latency heatmap for ranking service
rate(rec_model_inference_latency_seconds_bucket[5m])
# Use Grafana heatmap panel with:
# - Y-axis: latency buckets (log scale)
# - X-axis: time
# - Color intensity: count of requests in bucket
```

### 3.3 Interpreting Heatmaps

| Pattern | Interpretation | Action |
|---|---|---|
| Tight band at low latency | Healthy, consistent performance | Monitor |
| Spread across low-mid range | Normal variance | Monitor |
| Bimodal distribution | Two distinct latency populations | Investigate fast vs. slow paths |
| Drift upward over time | Gradual degradation | Profile and optimize |
| Sudden spike to high latency | Incident or deployment | Investigate immediately |
| Periodic spikes | Batch jobs, garbage collection | Tune or reschedule |

### 3.4 Latence Heatmap by Request Type

Different request types have different latency profiles:

```
Homepage recs (simple):
  Most requests: 20-50ms
  Tail: 50-100ms

Search recs (complex):
  Most requests: 50-150ms
  Tail: 150-500ms

Cold-start recs (new user):
  Most requests: 100-300ms
  Tail: 300-1000ms
```

---

## 4. Bottleneck Identification

### 4.1 Systematic Bottleneck Analysis

```
Step 1: Identify the slowest stage (highest P99 contribution)
Step 2: Check if the stage is CPU-bound, memory-bound, or I/O-bound
Step 3: Profile the stage under load
Step 4: Identify the specific operation within the stage
Step 5: Apply targeted optimization
Step 6: Verify improvement with A/B test
```

### 4.2 Common Bottlenecks in Recommendation Systems

| Bottleneck | Symptoms | Diagnosis | Solution |
|---|---|---|---|
| Feature store latency | High feature computation P99 | Trace shows long DB calls | Add caching, read replicas |
| Model inference | High ranking P99 | GPU utilization > 90% | Batch inference, model optimization |
| Candidate retrieval | High candidate P99 | ANN index search slow | Increase index shards, tune HNSW params |
| Network | High serialization overhead | Large payloads | Compress, use protobuf |
| Cache miss | Bimodal latency distribution | Cache hit rate dropping | Increase cache size, tune TTL |
| Garbage collection | Periodic latency spikes | JVM GC pauses | Tune GC, use off-heap memory |

### 4.3 Latency Attribution Table

For each request, compute the percentage of total latency per stage:

```
Request ID: req-abc123
Total latency: 342ms

Stage                    Duration    Percentage
feature_computation      45ms        13.2%
candidate_generation     156ms       45.6%  <-- BOTTLENECK
ranking                  82ms        24.0%
post_processing          31ms         9.1%
serialization            28ms         8.2%
```

### 4.4 Automated Bottleneck Detection

Define rules for automated bottleneck detection:

```yaml
bottleneck_rules:
  - name: "Feature store slow"
    condition: "rec_stage_p99_latency{stage='feature'} > 50ms for 10m"
    action: "Page on-call, check feature store health"

  - name: "Model inference slow"
    condition: "rec_stage_p99_latency{stage='ranking'} > 100ms for 5m"
    action: "Check GPU utilization, model version, batch size"

  - name: "Candidate retrieval slow"
    condition: "rec_stage_p99_latency{stage='candidate'} > 150ms for 5m"
    action: "Check ANN index health, shard distribution"
```

---

## 5. Distributed Latency Breakdown

### 5.1 Network Latency Components

```
Total network latency = DNS resolution + TCP handshake + TLS negotiation + Request transfer + Response transfer

Typical values:
  DNS resolution:        1-5ms (first call), 0ms (cached)
  TCP handshake:         1-2ms (same region), 20-50ms (cross-region)
  TLS negotiation:       1-3ms (session resumption), 20-40ms (full handshake)
  Request transfer:      0.1-1ms (small payload)
  Response transfer:     1-10ms (depends on payload size)
```

### 5.2 Latency Breakdown by Call Type

| Call Type | Typical Latency | Variance | Optimization |
|---|---|---|---|
| In-process function call | <0.01ms | Minimal | N/A |
| Local gRPC (same pod) | 0.1-1ms | Low | Connection pooling |
| gRPC (same AZ) | 1-5ms | Low | Keep-alive, load balancing |
| gRPC (cross-AZ) | 5-20ms | Medium | Avoid cross-AZ for hot path |
| gRPC (cross-region) | 50-200ms | High | Cache, regional routing |
| HTTP external API | 100-1000ms | Very high | Timeout, circuit breaker |
| Database query | 1-50ms | Medium | Connection pooling, indexing |
| Cache lookup (Redis) | 0.1-2ms | Low | Pipeline, local cache |

### 5.3 Cascading Latency Analysis

When multiple services are involved, latency cascades:

```
Service A (total: 200ms)
  - Local processing: 10ms
  - Call to Service B: 80ms
    - Service B local: 15ms
    - Call to Service C: 50ms
      - Service C local: 10ms
      - Call to DB: 30ms
    - Service B post-call: 15ms
  - Call to Service D: 100ms
    - Service D local: 20ms
    - Call to Model Server: 70ms
    - Service D post-call: 10ms
```

### 5.4 Latency Regression Detection

Monitor for latency regressions using comparison methods:

```promql
# Compare current P99 with 1 week ago (same time of day)
histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[1h]))
/
histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[1h] offset 7d))

# Alert if ratio > 1.5 (50% slower than 1 week ago)
```

---

## 6. Latency SLO Tracking

### 6.1 Latency SLO Definitions

| Service | SLO Metric | Target | Measurement |
|---|---|---|---|
| End-to-end | P99 latency | < 200ms | 30-day rolling window |
| Feature service | P99 latency | < 50ms | 30-day rolling window |
| Candidate service | P99 latency | < 100ms | 30-day rolling window |
| Ranking service | P99 latency | < 80ms | 30-day rolling window |
| Serving layer | P99 latency | < 150ms | 30-day rolling window |

### 6.2 Latency SLO Compliance

```
latency_slo_compliance{service="ranking", percentile="p99", target_ms="80"} gauge

# Calculate compliance over 30-day window
# = (number of requests within SLO) / (total requests)
# Target: 99.9% of requests within SLO
```

### 6.3 Latency Error Budget

```
latency_error_budget_total{service="ranking"} = total_requests * (1 - slo_target)
latency_error_budget_remaining{service="ranking"} = budget - (requests_exceeding_slo)

# Alert when error budget is consumed
alert: LatencyErrorBudgetBurnRate
expr: rate(rec_latency_slo_breach_total[1h]) > (1 - 0.999) * 1.44 / 1h
# 1.44x burn rate = consuming budget 44% faster than allowed
```

### 6.4 Latency SLO Dashboard

Key panels:
- **Current compliance**: Percentage of requests within latency SLO
- **Error budget remaining**: How much budget remains for the month
- **Burn rate**: How fast is the budget being consumed
- **Latency trend**: P50/P95/P99 over time with SLO threshold line
- **Breach analysis**: Which stages contribute most to SLO breaches

---

## 7. Regression Detection

### 7.1 Types of Latency Regressions

| Type | Pattern | Example | Detection |
|---|---|---|---|
| Step change | Sudden increase after deploy | New model is slower | Compare before/after deploy |
| Gradual drift | Slow increase over days/weeks | Index growing, query slowing | Trend analysis |
| Periodic spike | Regular intervals | GC, batch jobs, cron | Periodic pattern detection |
| Bimodal shift | New population of slow requests | Feature store cold path | Distribution analysis |

### 7.2 Automated Regression Detection

**CUSUM (Cumulative Sum) method:**

```
For each latency measurement:
  deviation = measured_latency - baseline_mean
  CUSUM = max(0, CUSUM_prev + deviation - allowance)

If CUSUM > decision_threshold:
  Flag regression
```

**Alert rules:**

```yaml
# Step change detection (comparing against 7-day baseline)
- alert: LatencyStepRegression
  expr: |
    histogram_quantile(0.99, rate(rec_latency_bucket[5m]))
    > histogram_quantile(0.99, rate(rec_latency_bucket[5m] offset 7d)) * 1.3
  for: 15m
  labels:
    severity: warning

# Gradual drift detection (comparing against 30-day baseline)
- alert: LatencyDriftRegression
  expr: |
    histogram_quantile(0.99, rate(rec_latency_bucket[1h]))
    > histogram_quantile(0.99, rate(rec_latency_bucket[1h] offset 30d)) * 1.5
  for: 1h
  labels:
    severity: critical
```

### 7.3 Regression Root Cause Analysis

When a latency regression is detected:

1. **Check recent deployments** — new model version, config change, feature change
2. **Compare traces** — find slow traces and compare against fast traces
3. **Check resource utilization** — CPU, memory, GPU saturation changes
4. **Check dependency health** — feature store, model server, cache hit rates
5. **Check traffic patterns** — new user segment, different request distribution
6. **Profile the slow path** — CPU profile, memory profile, network trace

---

## 8. Latency Optimization Strategies

### 8.1 Pipeline-Level Optimizations

| Optimization | Expected Improvement | Complexity |
|---|---|---|
| Parallel stage execution | 30–50% reduction | Medium |
| Feature caching | 20–40% reduction | Low |
| Candidate pre-fetching | 15–30% reduction | Medium |
| Model batching | 20–40% reduction | Medium |
| Response compression | 5–15% reduction | Low |
| Connection pooling | 5–20% reduction | Low |

### 8.2 Model-Level Optimizations

| Optimization | Expected Improvement | Complexity |
|---|---|---|
| Model quantization (FP32 to INT8) | 2–4x speedup | Medium |
| Model pruning | 1.5–3x speedup | High |
| Knowledge distillation | 2–5x speedup | High |
| TensorRT optimization | 2–3x speedup | Medium |
| Model caching (keep in GPU memory) | Eliminates load time | Low |

### 8.3 Infrastructure Optimizations

| Optimization | Expected Improvement | Complexity |
|---|---|---|
| GPU instance upgrade | 2–5x speedup | Low |
| Increase parallelism | Linear speedup (up to limit) | Low |
| Local SSD for model storage | Reduces load time | Low |
| Network optimization (placement) | 10–30% reduction | Medium |

---

## 9. Key Takeaways

1. **Always track percentiles** (P50, P95, P99) — averages hide tail latency issues
2. **Decompose latency by stage** to identify bottlenecks systematically
3. **Use latency heatmaps** for visual distribution analysis over time
4. **Set latency SLOs per service** with error budget tracking
5. **Detect regressions automatically** using comparison against baselines
6. **Profile the slow path** — focus optimization on the highest-latency stage
7. **Track P99/P50 ratio** as a measure of tail latency health
8. **Budget latency explicitly** — every millisecond should be accounted for
