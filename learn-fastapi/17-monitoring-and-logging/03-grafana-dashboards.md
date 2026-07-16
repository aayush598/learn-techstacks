# Grafana Dashboards for FastAPI

## Table of Contents
1. [Dashboard Design](#design)
2. [FastAPI Metrics Dashboard](#fastapi-dashboard)
3. [RED Metrics](#red)
4. [USE Metrics](#use)
5. [SLO/SLI Tracking](#slo-sli)
6. [Alerting](#alerting)

---

## Dashboard Design <a name="design"></a>

### Dashboard Hierarchy

```
Level 1: Overview Dashboard
  - Service health (green/yellow/red)
  - Request rate, error rate, latency
  - Key business metrics

Level 2: Service Dashboard
  - Detailed per-endpoint metrics
  - Database performance
  - Cache hit rates
  - External service calls

Level 3: Infrastructure Dashboard
  - CPU, memory, disk, network
  - Container/pod metrics
  - Database connections
  - Queue depths
```

### Dashboard Layout Principles

```
Row 1: Overview panels (health status, key rates)
Row 2: Request metrics (rate, errors, latency)
Row 3: Resource metrics (CPU, memory, connections)
Row 4: Business metrics (orders, revenue, users)
Row 5: Dependencies (database, cache, external services)
```

---

## FastAPI Metrics Dashboard <a name="fastapi-dashboard"></a>

### Key Panels

```json
{
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(rate(http_requests_total[5m])) by (endpoint)",
        "legendFormat": "{{method}} {{endpoint}}"
      }]
    },
    {
      "title": "Error Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(rate(http_requests_total{status_class=\"5xx\"}[5m])) / sum(rate(http_requests_total[5m])) * 100",
        "legendFormat": "5xx Error Rate %"
      }]
    },
    {
      "title": "P50/P95/P99 Latency",
      "type": "timeseries",
      "targets": [
        {"expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "P50"},
        {"expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "P95"},
        {"expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "P99"}
      ]
    },
    {
      "title": "Active Requests",
      "type": "stat",
      "targets": [{
        "expr": "fastapi_active_requests"
      }]
    },
    {
      "title": "Top Endpoints by Latency",
      "type": "table",
      "targets": [{
        "expr": "topk(10, histogram_quantile(0.95, sum by (endpoint, le) (rate(http_request_duration_seconds_bucket[5m]))))",
        "format": "table"
      }]
    },
    {
      "title": "Database Query Duration",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))",
        "legendFormat": "{{operation}} on {{table}}"
      }]
    },
    {
      "title": "Cache Hit Ratio",
      "type": "gauge",
      "targets": [{
        "expr": "rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) * 100",
        "legendFormat": "{{cache_name}}"
      }]
    }
  ]
}
```

### Dashboard JSON (Simplified)

```json
{
  "dashboard": {
    "title": "FastAPI Application",
    "panels": [
      {
        "title": "Request Rate (req/s)",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m]))",
            "legendFormat": "Total Requests"
          }
        ]
      },
      {
        "title": "Error Rate (%)",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status_class=~\"4xx|5xx\"}[5m])) / sum(rate(http_requests_total[5m])) * 100",
            "legendFormat": "Error Rate"
          }
        ],
        "thresholds": [
          {"value": 1, "color": "yellow"},
          {"value": 5, "color": "red"}
        ]
      }
    ]
  }
}
```

---

## RED Metrics <a name="red"></a>

RED = Rate, Errors, Duration. The three most important metrics for any service.

### Rate

```promql
# Total request rate
sum(rate(http_requests_total[5m]))

# Request rate by endpoint
sum by (endpoint) (rate(http_requests_total[5m]))

# Request rate by method
sum by (method) (rate(http_requests_total[5m]))
```

### Errors

```promql
# Error rate (5xx)
sum(rate(http_requests_total{status_class="5xx"}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Error count by endpoint
sum by (endpoint) (rate(http_requests_total{status_class="5xx"}[5m]))

# Client error rate (4xx)
sum(rate(http_requests_total{status_class="4xx"}[5m])) / sum(rate(http_requests_total[5m])) * 100
```

### Duration

```promql
# P50 latency
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Average latency
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# P95 by endpoint
histogram_quantile(0.95, sum by (endpoint, le) (rate(http_request_duration_seconds_bucket[5m])))
```

### RED Dashboard

```json
{
  "title": "RED Metrics",
  "panels": [
    {
      "title": "Rate (requests/sec)",
      "type": "stat",
      "targets": [{"expr": "sum(rate(http_requests_total[5m]))"}]
    },
    {
      "title": "Errors (%)",
      "type": "stat",
      "targets": [{"expr": "sum(rate(http_requests_total{status_class=\"5xx\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"}],
      "thresholds": [
        {"value": 0, "color": "green"},
        {"value": 1, "color": "yellow"},
        {"value": 5, "color": "red"}
      ]
    },
    {
      "title": "Duration P95 (ms)",
      "type": "stat",
      "targets": [{"expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) * 1000"}],
      "thresholds": [
        {"value": 0, "color": "green"},
        {"value": 200, "color": "yellow"},
        {"value": 1000, "color": "red"}
      ]
    }
  ]
}
```

---

## USE Metrics <a name="use"></a>

USE = Utilization, Saturation, Errors. For infrastructure resources.

### CPU

```promql
# Utilization
rate(process_cpu_seconds_total[5m]) * 100

# Saturation (load average)
node_load1

# Errors (none typically)
```

### Memory

```promql
# Utilization
process_resident_memory_bytes / 1024 / 1024

# Saturation (swap usage)
node_memory_SwapTotal_bytes - node_memory_SwapFree_bytes

# Errors (OOM kills)
kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}
```

### Database Connections

```promql
# Utilization
db_pool_connections{state="active"} / (db_pool_connections{state="active"} + db_pool_connections{state="idle"})

# Saturation
db_pool_connections{state="active"}

# Errors
db_connection_errors_total
```

---

## SLO/SLI Tracking <a name="slo-sli"></a>

### Service Level Indicators (SLIs)

```promql
# Availability SLI: % of non-5xx requests
1 - (sum(rate(http_requests_total{status_class="5xx"}[30d])) / sum(rate(http_requests_total[30d])))

# Latency SLI: % of requests under 200ms
1 - (sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d])) / sum(rate(http_request_duration_seconds_count[30d])))

# Correctness SLI: % of successful mutations
sum(rate(http_requests_total{method=~"POST|PUT|DELETE", status_class="2xx"}[30d])) / sum(rate(http_requests_total{method=~"POST|PUT|DELETE"}[30d]))
```

### SLO Error Budget

```promql
# SLO: 99.9% availability = 0.1% error budget
# Error budget remaining (30-day window)
1 - (
  sum(increase(http_requests_total{status_class="5xx"}[30d]))
  /
  sum(increase(http_requests_total[30d]))
) - 0.999

# Error budget burn rate (how fast are we consuming budget)
# If > 1, we're consuming budget too fast
(increase(http_requests_total{status_class="5xx"}[1h]) / increase(http_requests_total[1h])) / 0.001
```

### SLO Dashboard

```json
{
  "title": "SLO Dashboard",
  "panels": [
    {
      "title": "Availability (30d)",
      "type": "gauge",
      "targets": [{"expr": "1 - (sum(rate(http_requests_total{status_class=\"5xx\"}[30d])) / sum(rate(http_requests_total[30d])))"}],
      "min": 0.99, "max": 1.0,
      "thresholds": [
        {"value": 0.999, "color": "green"},
        {"value": 0.99, "color": "yellow"},
        {"value": 0.98, "color": "red"}
      ]
    },
    {
      "title": "Error Budget Remaining",
      "type": "stat",
      "targets": [{"expr": "(1 - (sum(increase(http_requests_total{status_class=\"5xx\"}[30d])) / sum(increase(http_requests_total[30d])))) - 0.999) / 0.001 * 100"}],
      "format": "percent"
    },
    {
      "title": "Latency SLO (P95 < 200ms)",
      "type": "gauge",
      "targets": [{"expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[30d]))"}]
    }
  ]
}
```

---

## Alerting <a name="alerting"></a>

### Grafana Alert Rules

```yaml
# Alert: High error rate
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status_class="5xx"}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate: {{ $value | humanizePercentage }}"

# Alert: High latency
- alert: HighLatencyP95
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "P95 latency is {{ $value }}s"

# Alert: SLO burn rate
- alert: SLOBurnRateHigh
  expr: (sum(rate(http_requests_total{status_class="5xx"}[1h])) / sum(rate(http_requests_total[1h]))) / 0.001 > 14.4
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "SLO error budget burning too fast"

# Alert: No traffic
- alert: NoTraffic
  expr: sum(rate(http_requests_total[5m])) == 0
  for: 10m
  labels:
    severity: info
  annotations:
    summary: "No traffic for 10 minutes"
```

### Notification Channels

```yaml
# Grafana alerting notification channels
contact_points:
  - name: slack
    type: slack
    settings:
      url: https://hooks.slack.com/services/xxx
      channel: "#alerts"

  - name: pagerduty
    type: pagerduty
    settings:
      integrationKey: xxx

  - name: email
    type: email
    settings:
      addresses: oncall@example.com
```

---

## Interview Questions

1. **What are RED metrics and why are they important?**
RED = Rate (requests/sec), Errors (error rate), Duration (latency). They're the three most important metrics for any service. They tell you: how much traffic you're getting, how many requests are failing, and how long requests take. Start with RED for any new service.

2. **What are USE metrics and when do you use them?**
USE = Utilization, Saturation, Errors. Used for infrastructure resources (CPU, memory, disk, network). Utilization = % of resource used. Saturation = queue depth/waiting. Errors = resource-level errors. Use USE for infrastructure, RED for services.

3. **What is an SLO and how do you track it in Grafana?**
A Service Level Objective is a target for a Service Level Indicator (e.g., 99.9% availability). Track SLIs (actual metrics) against SLOs (targets). Calculate error budget remaining. Alert when budget burns too fast. Grafana dashboards show SLO compliance.

4. **How do you design a Grafana dashboard for a FastAPI application?**
Start with an overview row (request rate, error rate, P95 latency). Add per-endpoint breakdown. Include database metrics (query duration, connections). Add cache metrics. Include infrastructure metrics. Use stat panels for key numbers, time series for trends, tables for top-N.

5. **What are the most important Prometheus metrics for a FastAPI app?**
- `http_requests_total` (Counter) — total requests by method, endpoint, status
- `http_request_duration_seconds` (Histogram) — request latency
- `fastapi_active_requests` (Gauge) — current concurrent requests
- `db_query_duration_seconds` (Histogram) — database query latency
- `cache_hits_total` / `cache_misses_total` (Counters) — cache performance
