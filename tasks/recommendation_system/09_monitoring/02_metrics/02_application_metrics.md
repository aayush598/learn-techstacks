# Application Metrics for Recommendation Systems

## 1. Overview

Application metrics quantify the behavior and health of recommendation system components. Unlike logs (which describe individual events), metrics provide aggregated, time-series views that enable dashboards, alerting, and trend analysis. A well-instrumented recommendation system emits metrics at every pipeline stage — from feature computation through model inference to serving and post-ranking.

### 1.1 Metrics vs. Logs vs. Traces

| Dimension | Metrics | Logs | Traces |
|---|---|---|---|
| Nature | Numeric time-series | Structured text events | Request flow paths |
| Cardinality | Low (thousands of series) | Unbounded | Per-request |
| Storage cost | Low | High | Medium |
| Query model | Aggregation (avg, p99) | Search/filter | Graph traversal |
| Primary use | Dashboards, alerting | Debugging, auditing | Bottleneck identification |

### 1.2 The Three Pillars Plus Metrics

Metrics are often called the "fourth pillar" of observability. In recommendation systems, they are the primary tool for:

- **SLI measurement** (Service Level Indicators)
- **Capacity planning** (resource utilization trends)
- **Anomaly detection** (deviation from baseline patterns)
- **Business KPI tracking** (CTR, conversion, revenue)

---

## 2. RED Method (Rate, Errors, Duration)

### 2.1 The RED Method

The RED method focuses on request-oriented metrics for microservices:

| Metric | Description | Example |
|---|---|---|
| **Rate** | Number of requests per second | 5,000 req/s for ranking service |
| **Errors** | Number of failed requests per second | 25 errors/s (0.5% error rate) |
| **Duration** | Distribution of request latency | P50=15ms, P99=120ms |

### 2.2 RED Metrics for Recommendation Pipeline

Each pipeline stage has its own RED metrics:

**Candidate Generation:**
```
rec_candidate_generation_requests_total{service="candidate-gen"} counter
rec_candidate_generation_errors_total{service="candidate-gen", error_type="timeout|index_error|empty_results"} counter
rec_candidate_generation_duration_seconds{service="candidate-gen"} histogram
```

**Ranking:**
```
rec_ranking_requests_total{service="ranking"} counter
rec_ranking_errors_total{service="ranking", error_type="model_error|feature_error|fallback_used"} counter
rec_ranking_duration_seconds{service="ranking"} histogram
```

**Serving:**
```
rec_serving_requests_total{service="serving"} counter
rec_serving_errors_total{service="serving", error_type="cache_miss|serialization_error|downstream_timeout"} counter
rec_serving_duration_seconds{service="serving"} histogram
```

### 2.3 RED-Based Alerting

| Alert | Condition | Severity |
|---|---|---|
| High error rate | error_rate > 1% for 5 min | Warning |
| Critical error rate | error_rate > 5% for 2 min | Critical |
| High latency | P99 > 500ms for 5 min | Warning |
| Latency spike | P99 > 2s for 2 min | Critical |
| Traffic drop | rate < 50% of baseline for 10 min | Warning |

---

## 3. USE Method (Utilization, Saturation, Errors)

### 3.1 The USE Method

The USE method focuses on resource-oriented metrics:

| Metric | Description | Example |
|---|---|---|
| **Utilization** | Percentage of resource in use | 75% CPU utilization |
| **Saturation** | Degree of queued work | 200 items in request queue |
| **Errors** | Count of resource errors | 3 GPU memory errors/hour |

### 3.2 USE Metrics for Recommendation Infrastructure

**CPU Resources:**
```
node_cpu_utilization_percent{instance="ranking-gpu-01"} gauge
node_cpu_saturation_load_average_1m{instance="ranking-gpu-01"} gauge
node_cpu_errors_total{instance="ranking-gpu-01"} counter
```

**Memory Resources:**
```
node_memory_utilization_percent{instance="ranking-gpu-01"} gauge
node_memory_saturation_swap_usage_bytes{instance="ranking-gpu-01"} gauge
node_memory_errors_total{instance="ranking-gpu-01"} counter
```

**GPU Resources (critical for model serving):**
```
nvidia_gpu_utilization_percent{gpu="0", instance="ranking-gpu-01"} gauge
nvidia_gpu_memory_utilization_percent{gpu="0", instance="ranking-gpu-01"} gauge
nvidia_gpu_saturation_pending_operations{gpu="0", instance="ranking-gpu-01"} gauge
nvidia_gpu_errors_total{gpu="0", instance="ranking-gpu-01"} counter
```

**Network Resources:**
```
node_network_utilization_bandwidth_percent{interface="eth0"} gauge
node_network_saturation_queue_depth{interface="eth0"} gauge
node_network_errors_total{interface="eth0"} counter
```

### 3.3 Resource Sizing Targets

| Resource | Target Utilization | Action Threshold |
|---|---|---|
| CPU | 60–70% average | >80% sustained |
| Memory | 70–80% average | >85% sustained |
| GPU | 70–85% average | >90% sustained |
| Network | <50% bandwidth | >70% sustained |
| Disk I/O | <60% IOPS capacity | >80% sustained |
| Disk Space | <70% capacity | >80% capacity |

---

## 4. Prometheus Metric Types

### 4.1 Counter

**Definition:** Monotonically increasing value. Only goes up (or resets to zero on process restart).

**Use cases:**
- Total request count
- Total error count
- Total bytes processed
- Total model inferences

**Example:**
```
rec_model_inference_total{
  service="ranking",
  model="xgboost-v3",
  status="success"
} 1234567
```

**Important:** Always use `_total` suffix. Always use `rate()` or `increase()` when querying.

### 4.2 Gauge

**Definition:** Value that can go up or down freely.

**Use cases:**
- Current queue depth
- Active connections
- Model accuracy (rolling window)
- Cache size
- Feature store staleness

**Example:**
```
rec_active_connections{service="serving"} 42
rec_feature_store_staleness_seconds{feature_group="user_embedding"} 3.5
rec_model_accuracy_rolling{model="xgboost-v3"} 0.847
```

### 4.3 Histogram

**Definition:** Samples observations and counts them in configurable buckets. Also calculates configurable quantiles.

**Use cases:**
- Request duration distribution
- Prediction latency distribution
- Feature computation time
- Response size distribution

**Example:**
```
rec_request_duration_seconds_bucket{service="serving", le="0.01"} 1234
rec_request_duration_seconds_bucket{service="serving", le="0.05"} 5678
rec_request_duration_seconds_bucket{service="serving", le="0.1"} 8901
rec_request_duration_seconds_bucket{service="serving", le="0.5"} 9876
rec_request_duration_seconds_bucket{service="serving", le="1"} 9950
rec_request_duration_seconds_bucket{service="serving", le="+Inf"} 10000
rec_request_duration_seconds_sum{service="serving"} 456.78
rec_request_duration_seconds_count{service="serving"} 10000
```

**Bucket strategy:**
- Use logarithmic buckets for latency (0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10 seconds)
- This gives good resolution across 3 orders of magnitude

### 4.4 Summary

**Definition:** Similar to histogram but calculates quantiles on the client side.

**When to use histograms over summaries:**
- Histograms: When you need server-side aggregation across instances
- Summaries: When you need exact quantiles and don't aggregate across instances

**Recommendation:** Prefer histograms for most use cases due to aggregation flexibility.

---

## 5. Custom Histograms for Recommendation Systems

### 5.1 Prediction Score Distribution

Track the distribution of model output scores over time:

```
rec_prediction_score_distribution_bucket{model="ranking-v3", le="0.1"} 100
rec_prediction_score_distribution_bucket{model="ranking-v3", le="0.3"} 500
rec_prediction_score_distribution_bucket{model="ranking-v3", le="0.5"} 2000
rec_prediction_score_distribution_bucket{model="ranking-v3", le="0.7"} 4500
rec_prediction_score_distribution_bucket{model="ranking-v3", le="0.9"} 4900
rec_prediction_score_distribution_bucket{model="ranking-v3", le="1.0"} 5000
```

**Why this matters:**
- Score distribution shift can indicate data drift
- Bimodal distributions may suggest model confusion
- Score collapse (all predictions near 0.5) indicates model degradation

### 5.2 Feature Completeness Distribution

```
rec_feature_completeness_bucket{feature_group="user_profile", le="0.5"} 10
rec_feature_completeness_bucket{feature_group="user_profile", le="0.8"} 50
rec_feature_completeness_bucket{feature_group="user_profile", le="0.95"} 500
rec_feature_completeness_bucket{feature_group="user_profile", le="1.0"} 1000
```

### 5.3 Candidate Count Distribution

```
rec_candidate_count_bucket{stage="retrieval", le="10"} 100
rec_candidate_count_bucket{stage="retrieval", le="50"} 300
rec_candidate_count_bucket{stage="retrieval", le="100"} 500
rec_candidate_count_bucket{stage="retrieval", le="500"} 900
rec_candidate_count_bucket{stage="retrieval", le="1000"} 1000
```

### 5.4 Custom Bucket Configuration

```yaml
# Prometheus histogram bucket configuration for recommendation systems
histogram_buckets:
  latency_seconds: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
  prediction_score: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  feature_completeness: [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
  candidate_count: [10, 50, 100, 200, 500, 1000, 2000, 5000]
```

---

## 6. Metric Cardinality Management

### 6.1 The Cardinality Problem

Cardinality is the number of unique label combinations per metric. High cardinality causes:

- **Memory explosion**: Each unique series consumes ~1–2KB in Prometheus
- **Query slowdown**: Aggregation over millions of series takes seconds
- **Storage bloat**: High-cardinality metrics dominate storage costs
- **Dashboard rendering failures**: Too many series in a single panel

### 6.2 Cardinality Budget

Set explicit cardinality budgets per metric:

| Metric Type | Max Cardinality | Example |
|---|---|---|
| Infrastructure metrics | 1,000 | node_cpu_utilization{instance, cpu} |
| Service RED metrics | 10,000 | rec_requests_total{service, endpoint, method, status} |
| Model metrics | 5,000 | rec_model_accuracy{model, version, dataset} |
| User-level metrics | **Forbidden** | Never use user_id as a label |
| Content-level metrics | 100,000 max | rec_content_ctr{content_category, rec_type} |

### 6.3 High-Cardinality Anti-Patterns

**Never do:**
- `rec_requests{user_id="abc123"}` — millions of unique users
- `rec_predictions{feature_hash="a1b2c3"}` — unbounded feature hashes
- `rec_errors{stack_trace_hash="..."}` — unbounded stack traces
- `rec_requests{request_id="..."}` — every request is unique

**Instead:**
- Aggregate at the application level before emitting metrics
- Use logarithmic or bucketed representations
- Use labels for enumerated values with bounded cardinality
- Use metrics for aggregates, logs for individual events

### 6.4 Cardinality Monitoring

```
# Prometheus metric showing current cardinality per metric name
prometheus_tsdb_head_series{job="prometheus"}
prometheus_tsdb_head_bytes{job="prometheus"}
```

Alert when:
- Total series count exceeds budget (>1M per Prometheus instance)
- Any single metric exceeds its cardinality budget
- Cardinality growth rate exceeds 10% per week

---

## 7. Metric Instrumentation Guidelines

### 7.1 Naming Convention

```
<namespace>_<subsystem>_<name>_<unit>

Where:
- namespace: rec (for recommendation system)
- subsystem: model, feature, candidate, ranking, serving
- name: descriptive snake_case
- unit: _seconds, _bytes, _total, _count

Examples:
- rec_model_inference_duration_seconds
- rec_feature_computation_bytes
- rec_candidate_retrieval_total
- rec_serving_request_duration_seconds
```

### 7.2 Label Guidelines

- Use labels for dimensions you want to filter/group by
- Keep label values low-cardinality (<1000 unique values per label)
- Prefer label names that are semantically meaningful
- Avoid labels that change frequently (leads to series churn)
- Use consistent label names across related metrics

### 7.3 Metric Documentation

Every metric should have:
- **Help text**: One-line description
- **Type**: Counter, Gauge, Histogram, Summary
- **Labels**: List with descriptions and valid values
- **Unit**: Physical unit (seconds, bytes, count)
- **Example queries**: Common PromQL expressions
- **Related metrics**: Metrics that should be viewed together

---

## 8. Key Takeaways

1. **Apply RED method** for request-oriented metrics at every pipeline stage
2. **Apply USE method** for resource-oriented metrics (especially GPU for model serving)
3. **Prefer histograms over summaries** for latency metrics (enables server-side aggregation)
4. **Set cardinality budgets** and monitor compliance
5. **Never use high-cardinality labels** (user_id, request_id, feature_hash)
6. **Standardize metric naming** with namespace, subsystem, name, and unit
7. **Document every metric** with type, labels, unit, and example queries
8. **Use logarithmic histogram buckets** for latency (covers 3+ orders of magnitude)
