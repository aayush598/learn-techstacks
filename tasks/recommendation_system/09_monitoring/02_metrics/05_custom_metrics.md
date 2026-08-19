# Custom Metrics for Recommendation Systems

## 1. Overview

Custom metrics extend standard application and ML metrics with domain-specific measurements tailored to your recommendation system's unique requirements. While RED/USE metrics cover system health and standard ML metrics cover model quality, custom metrics capture the nuances that make your system distinctive — feature pipeline health, A/B test performance, personalization effectiveness, and operational efficiency.

### 1.1 When to Create Custom Metrics

- Existing metrics don't capture a critical system behavior
- You need to track a business-specific concept (e.g., "recommendation freshness")
- You want to combine multiple signals into a composite health indicator
- You need metrics for automated decision-making (auto-scaling, auto-rollback)

### 1.2 Metric Creation Principles

1. **Every metric must have an owner** — someone responsible for its definition and maintenance
2. **Every metric must have an alert** — if it's worth measuring, it's worth alerting on
3. **Every metric must be documented** — include description, formula, and example queries
4. **Every metric must have a lifecycle plan** — when to retire metrics that are no longer useful

---

## 2. Naming Conventions

### 2.1 Standard Naming Pattern

```
<namespace>_<subsystem>_<name>_<unit_suffix>

Examples:
rec_feature_pipeline_latency_seconds
rec_model_serving_queue_depth_count
rec_recommendation_diversity_score_ratio
rec_ab_test_statistical_significance_value
```

### 2.2 Naming Rules

| Rule | Example (Correct) | Example (Incorrect) |
|---|---|---|
| Use snake_case | `rec_request_latency_seconds` | `rec_requestLatencySeconds` |
| Include unit suffix | `rec_data_bytes_processed` | `rec_data_processed` |
| Use `_total` for counters | `rec_requests_total` | `rec_requests_count` |
| Use `_seconds` for duration | `rec_duration_seconds` | `rec_duration_ms` (ambiguous) |
| Use `_ratio` for 0–1 values | `rec_coverage_ratio` | `rec_coverage_percent` |
| Use `_bytes` for sizes | `rec_model_size_bytes` | `rec_model_size` |
| Avoid abbreviations | `rec_recommendation_count` | `rec_rec_cnt` |
| Start with namespace | `rec_feature_freshness_seconds` | `feature_freshness_seconds` |

### 2.3 Reserved Prefixes

| Prefix | Usage | Examples |
|---|---|---|
| `rec_` | Recommendation system metrics | `rec_serving_latency_seconds` |
| `node_` | Infrastructure metrics | `node_cpu_utilization_percent` |
| `process_` | Runtime metrics | `process_resident_memory_bytes` |
| `go_` / `python_` | Language runtime metrics | `go_gc_duration_seconds` |
| `scrape_` | Prometheus scraping metrics | `scrape_duration_seconds` |

---

## 3. Label Design

### 3.1 Label Cardinality Guidelines

| Label Type | Max Unique Values | Examples |
|---|---|---|
| Service name | 50 | `ranking`, `candidate-gen`, `feature-svc` |
| HTTP method | 5 | `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| HTTP status code | 10 | `200`, `400`, `404`, `500`, `502`, `503` |
| Model name | 20 | `ranking-v3`, `candidate-v2` |
| Model version | 50 | `2026.08.15-rc3` |
| Error type | 30 | `timeout`, `model_error`, `feature_missing` |
| Page type | 15 | `homepage`, `search_results`, `product_detail` |
| Content category | 100 | `sports`, `news`, `entertainment`, `cooking` |
| User segment | 20 | `new_user`, `power_user`, `premium`, `free` |
| Region | 20 | `us-east`, `eu-west`, `ap-south` |

### 3.2 Label Naming Best Practices

**Good labels** (low cardinality, meaningful):
```yaml
service: ranking
model: ranking-v3
model_type: deep_ranking
hardware: gpu
status: success
error_type: timeout
page_type: homepage
```

**Bad labels** (high cardinality, meaningless):
```yaml
user_id: "abc123"         # Millions of values
request_id: "req_001"     # Every request is unique
feature_hash: "a1b2c3"    # Unbounded
timestamp: "2026-08-19"    # Changes every second
log_message: "..."         # Unbounded text
```

### 3.3 Multi-Label Strategy

Use multiple labels for different dimensions rather than a single composite label:

```yaml
# BAD: Single composite label
endpoint: "ranking-v3/deep/gpu"

# GOOD: Separate labels
model: ranking-v3
model_type: deep_ranking
hardware: gpu
```

This enables flexible querying:
- All GPU models: `{hardware="gpu"}`
- All deep ranking models: `{model_type="deep_ranking"}`
- Specific model on GPU: `{model="ranking-v3", hardware="gpu"}`

---

## 4. Aggregation Strategies

### 4.1 Rate

**Purpose:** Convert counters to per-second rates.

```promql
# Request rate (requests per second)
rate(rec_requests_total[5m])

# Error rate (errors per second)
rate(rec_errors_total[5m])

# Error ratio (errors / total requests)
rate(rec_errors_total[5m]) / rate(rec_requests_total[5m])
```

**Recommendation-specific rates:**
```promql
# Fallback usage rate
rate(rec_model_fallback_triggered_total[5m]) / rate(rec_requests_total[5m])

# Feature cache hit rate
rate(rec_feature_cache_hits_total[5m]) / rate(rec_feature_cache_requests_total[5m])

# Model version change rate
rate(rec_model_version_changes_total[1h])
```

### 4.2 Histogram Percentiles

**Purpose:** Understand latency and score distributions.

```promql
# P50, P95, P99 latency
histogram_quantile(0.50, rate(rec_request_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(rec_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[5m]))

# P99/P50 ratio (latency variance indicator)
histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[5m]))
/
histogram_quantile(0.50, rate(rec_request_duration_seconds_bucket[5m]))
```

### 4.3 Moving Averages

**Purpose:** Smooth out noise for trend detection.

```promql
# 5-minute moving average of CTR
avg_over_time(rec_ctr_ratio[5m])

# 1-hour moving average of prediction confidence
avg_over_time(rec_prediction_confidence_mean[1h])

# Compare current vs. 1-day-ago
rec_ctr_ratio / rec_ctr_ratio offset 1d
```

### 4.4 Aggregation by Label

```promql
# CTR by page type
sum(rate(rec_clicks_total[5m])) by (page_type)
/
sum(rate(rec_impressions_total[5m])) by (page_type)

# Latency by model
histogram_quantile(0.99, rate(rec_model_inference_latency_seconds_bucket[5m])) by (model)

# Error rate by service
sum(rate(rec_errors_total[5m])) by (service, error_type)
```

---

## 5. Metric-Based Alerting

### 5.1 Alert Design Patterns

**Absolute threshold:**
```yaml
# Simple threshold alert
- alert: HighLatency
  expr: histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[5m])) > 0.5
  for: 5m
  labels:
    severity: warning
```

**Relative threshold:**
```yaml
# Compare against baseline
- alert: CTRDrop
  expr: rec_ctr_ratio < rec_ctr_ratio offset 7d * 0.8
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "CTR dropped more than 20% vs. 7-day baseline"
```

**Composite score:**
```yaml
# Health score alert
- alert: ModelHealthDegraded
  expr: rec_model_health_score < 0.7
  for: 10m
  labels:
    severity: critical
```

### 5.2 Alert Severity Levels

| Severity | Response Time | Examples |
|---|---|---|
| P0 (Critical) | Immediate | Model serving down, error rate >10% |
| P1 (High) | <15 minutes | P99 latency >2s, error rate >5% |
| P2 (Medium) | <1 hour | CTR drop >20%, feature staleness >5 min |
| P3 (Low) | <4 hours | Coverage drop, minor latency increase |
| P4 (Info) | Next business day | Training run completed, model promoted |

### 5.3 Alert Fatigue Prevention

- **Require multi-condition alerts**: Don't alert on single metric spikes
- **Use `for` duration**: Require condition sustained for 2–5 minutes
- **Implement alert grouping**: Related alerts should fire together
- **Set maintenance windows**: Suppress alerts during known maintenance
- **Review alert monthly**: Remove or tune alerts that are always firing or never firing

---

## 6. Dashboard Design Patterns

### 6.1 Dashboard Hierarchy

```
Executive Dashboard (weekly/monthly)
├── Business KPIs (CTR, conversion, revenue)
├── OKR progress
└── Cost per recommendation

Operational Dashboard (daily/on-call)
├── Request rate and error rate
├── Latency percentiles
├── Model health scores
└── Feature freshness

Debugging Dashboard (per-incident)
├── Request trace visualization
├── Feature values for specific request
├── Model prediction details
└── Downstream dependency status
```

### 6.2 Dashboard Panel Patterns

**Single stat panel** — Key metric at a glance:
```
┌─────────────────┐
│   Current CTR   │
│     4.2%        │
│  ▲ +0.3% vs 7d │
└─────────────────┘
```

**Time series panel** — Trend over time:
```
┌─────────────────────────────┐
│  CTR Trend (7 days)         │
│  ╱╲  ╱╲  ╱╲  ╱╲           │
│ ╱  ╲╱  ╲╱  ╲╱  ╲╱╲       │
│──────────────────────────── │
│ 4.0% ─────── baseline       │
└─────────────────────────────┘
```

**Heatmap panel** — Distribution over time:
```
┌─────────────────────────────┐
│  Latency Distribution       │
│  ■■■■■■■■■■■■■■■■■■■■■■■  │
│  ■■■■■■■■■■■■■■■■■■■■■■■  │
│  ■■■■■■■■■■■■■■■■■■■■■■■  │
│  ■■■■■■■■■■■■■■■■■■■■■■■  │
│  ← time →                   │
└─────────────────────────────┘
```

### 6.3 Dashboard as Code (Grafana JSON)

```json
{
  "dashboard": {
    "title": "Recommendation System Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(rec_requests_total[5m]))",
            "legendFormat": "{{service}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "thresholds": {
              "steps": [
                {"value": 0, "color": "green"},
                {"value": 1000, "color": "yellow"},
                {"value": 5000, "color": "red"}
              ]
            }
          }
        }
      }
    ],
    "templating": {
      "list": [
        {
          "name": "service",
          "query": "label_values(rec_requests_total, service)",
          "type": "query"
        }
      ]
    }
  }
}
```

### 6.4 Template Patterns

Use Grafana template variables for reusable dashboards:

```json
{
  "templating": {
    "list": [
      {"name": "datasource", "type": "datasource", "query": "prometheus"},
      {"name": "environment", "type": "query", "query": "label_values(rec_requests_total, environment)"},
      {"name": "service", "type": "query", "query": "label_values(rec_requests_total{environment=\"$environment\"}, service)"},
      {"name": "model", "type": "query", "query": "label_values(rec_model_inference_total{service=\"$service\"}, model)"}
    ]
  }
}
```

---

## 7. Metric Cost Management

### 7.1 Cost Drivers

| Factor | Impact | Optimization |
|---|---|---|
| Series cardinality | Directly proportional to storage | Reduce label cardinality |
| Scrape interval | 15s = 4x storage of 60s | Use 15s for critical, 60s for infrequent |
| Retention period | 30 days vs. 90 days = 3x storage | Differentiate by metric importance |
| Remote write | Network and storage at destination | Filter before remote write |
| Query complexity | Compute cost for dashboards | Pre-aggregate, use recording rules |

### 7.2 Recording Rules for Expensive Queries

```yaml
groups:
  - name: rec_recording_rules
    interval: 15s
    rules:
      # Pre-compute 5-minute error rate
      - record: rec:error_rate_5m
        expr: sum(rate(rec_errors_total[5m])) by (service)

      # Pre-compute P99 latency
      - record: rec:p99_latency_5m
        expr: histogram_quantile(0.99, rate(rec_request_duration_seconds_bucket[5m]))

      # Pre-compute CTR
      - record: rec:ctr_5m
        expr: sum(rate(rec_clicks_total[5m])) by (page_type) / sum(rate(rec_impressions_total[5m])) by (page_type)
```

### 7.3 Metric Lifecycle Management

```
New metric proposal → Review (cardinality, cost) → Approved → Implemented → Active → Deprecated → Removed

Review checklist:
- [ ] Cardinality estimate < budget
- [ ] Owner assigned
- [ ] Alert defined
- [ ] Dashboard panel created
- [ ] Documentation complete
- [ ] Cost estimate within budget

Deprecation criteria:
- Metric not queried in 90 days
- Metric replaced by better alternative
- Alert on metric never fires
- Cardinality exceeds budget
```

---

## 8. Recommendation System Custom Metrics Catalog

### 8.1 Feature Pipeline Metrics

```
rec_feature_pipeline_latency_seconds{feature_group, stage}
rec_feature_pipeline_errors_total{feature_group, error_type}
rec_feature_freshness_seconds{feature_group, feature_type}
rec_feature_completeness_ratio{feature_group, model}
rec_feature_cache_hit_ratio{feature_group, cache_type}
rec_feature_default_value_rate{feature_group, feature_name}
```

### 8.2 Candidate Generation Metrics

```
rec_candidate_retrieval_latency_seconds{method, index_type}
rec_candidate_count{stage, source}
rec_candidate_diversity_score{method}
rec_candidate_coverage_ratio{source, category}
rec_candidate_fallback_rate{method}
```

### 8.3 Ranking Metrics

```
rec_model_inference_latency_seconds{model, model_type, hardware}
rec_model_prediction_confidence_distribution_bucket{model, le}
rec_model_feature_importance_top_features{model, feature}
rec_model_score_distribution_bucket{model, le}
rec_model_calibration_error{model}
```

### 8.4 Serving Metrics

```
rec_serving_latency_seconds{page_type, slot_id}
rec_serving_cache_hit_ratio{cache_type}
rec_serving_fallback_rate{reason}
rec_serving_recommendation_diversity{page_type}
rec_serving_recommendation_novelty{page_type}
```

---

## 9. Key Takeaways

1. **Follow naming conventions** strictly — consistency enables cross-service metric correlation
2. **Control label cardinality** — set budgets per metric and monitor compliance
3. **Use recording rules** for expensive queries to reduce dashboard latency
4. **Design alerts with multi-condition logic** and sustained duration requirements
5. **Implement metric lifecycle management** — review, deprecate, and remove unused metrics
6. **Create domain-specific custom metrics** for feature pipelines, candidate generation, and serving
7. **Dashboard as code** enables version control and reproducible dashboard configurations
8. **Monitor metric cost** as aggressively as you monitor application cost
