# Prometheus Metrics for FastAPI

## Table of Contents
1. [Prometheus Overview](#overview)
2. [prometheus_client with FastAPI](#fastapi)
3. [Counter](#counter)
4. [Histogram](#histogram)
5. [Gauge](#gauge)
6. [Custom Metrics](#custom)
7. [Metrics Endpoint](#endpoint)
8. [Metric Labels](#labels)
9. [Alerting Rules](#alerting)
10. [Prometheus Setup](#setup)

---

## Prometheus Overview <a name="overview"></a>

Prometheus is an open-source monitoring system that collects metrics via HTTP endpoints. It scrapes `/metrics` endpoints, stores time-series data, and supports PromQL for queries and alerting.

### Metric Types

| Type | Description | Example |
|------|-------------|---------|
| Counter | Monotonically increasing value | Total requests, total errors |
| Histogram | Value distribution with buckets | Request duration, response size |
| Gauge | Value that can go up and down | Active connections, queue depth |
| Summary | Similar to histogram, client-side | Quantiles (less flexible) |

---

## prometheus_client with FastAPI <a name="fastapi"></a>

### Installation

```bash
pip install prometheus-client
```

### Basic Setup

```python
# app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
import time

# Define metrics
REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_REQUESTS = Gauge(
    "fastapi_active_requests",
    "Number of active requests"
)

APP_INFO = Info(
    "fastapi_app",
    "Application information"
)

APP_INFO.info({
    "version": "1.0.0",
    "environment": "production",
})

# Middleware to collect metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    ACTIVE_REQUESTS.dec()

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

---

## Counter <a name="counter"></a>

Counters only increase. Use for cumulative metrics like total requests, total errors.

```python
from prometheus_client import Counter

# Request counter
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# Usage
http_requests_total.labels(method="GET", endpoint="/api/users", status="200").inc()
http_requests_total.labels(method="POST", endpoint="/api/users", status="201").inc(5)  # Increment by 5

# Business metric
orders_created_total = Counter(
    "orders_created_total",
    "Total orders created",
    ["payment_method", "user_tier"]
)

orders_created_total.labels(payment_method="credit_card", user_tier="premium").inc()

# Error counter
errors_total = Counter(
    "errors_total",
    "Total errors",
    ["error_type", "severity"]
)

errors_total.labels(error_type="database", severity="critical").inc()
```

---

## Histogram <a name="histogram"></a>

Histograms track value distributions. Perfect for latency and request sizes.

```python
from prometheus_client import Histogram

# Request latency histogram
request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf"))
)

# Usage
import time

start = time.time()
# ... process request
duration = time.time() - start
request_duration_seconds.labels(method="GET", endpoint="/api/users").observe(duration)

# Database query latency
db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Database query duration",
    ["operation", "table"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0)
)

# Response size histogram
response_size_bytes = Histogram(
    "http_response_size_bytes",
    "HTTP response size",
    ["method", "endpoint"],
    buckets=(100, 500, 1000, 5000, 10000, 50000, 100000)
)
```

### Histogram Quantiles

```promql
# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Average latency
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

---

## Gauge <a name="gauge"></a>

Gauges can increase and decrease. Use for current state metrics.

```python
from prometheus_client import Gauge

# Active connections
active_connections = Gauge(
    "active_connections",
    "Number of active connections"
)

active_connections.inc()  # +1
active_connections.dec()  # -1

# Database pool size
db_pool_size = Gauge(
    "db_pool_connections",
    "Database connection pool size",
    ["state"]  # active, idle
)

db_pool_size.labels(state="active").set(5)
db_pool_size.labels(state="idle").set(15)

# Queue depth
queue_depth = Gauge(
    "task_queue_depth",
    "Number of pending tasks in queue"
)

# CPU/Memory (if monitoring your own process)
import psutil

process_cpu_percent = Gauge(
    "process_cpu_percent",
    "Process CPU usage"
)

process_memory_bytes = Gauge(
    "process_memory_bytes",
    "Process memory usage"
)

# Background task to update gauges
async def update_system_metrics():
    while True:
        process_cpu_percent.set(psutil.Process().cpu_percent())
        process_memory_bytes.set(psutil.Process().memory_info().rss)
        await asyncio.sleep(10)
```

---

## Custom Metrics <a name="custom"></a>

```python
# Business metrics
active_users = Gauge("active_users", "Currently active users")
daily_orders = Counter("daily_orders_total", "Orders placed today")
revenue_total = Counter("revenue_total", "Total revenue", ["currency"])

# Cache metrics
cache_hits = Counter("cache_hits_total", "Cache hits", ["cache_name"])
cache_misses = Counter("cache_misses_total", "Cache misses", ["cache_name"])

cache_hit_ratio = Gauge(
    "cache_hit_ratio",
    "Cache hit ratio",
    ["cache_name"]
)

# External service metrics
external_service_calls = Counter(
    "external_service_calls_total",
    "External service calls",
    ["service", "method", "status"]
)

external_service_duration = Histogram(
    "external_service_duration_seconds",
    "External service call duration",
    ["service", "method"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

# Background task metrics
background_tasks_total = Counter(
    "background_tasks_total",
    "Background tasks executed",
    ["task_name", "status"]
)

background_task_duration = Histogram(
    "background_task_duration_seconds",
    "Background task duration",
    ["task_name"],
    buckets=(0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0)
)
```

---

## Metrics Endpoint <a name="endpoint"></a>

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import prometheus_client

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST,
    )

# Custom metrics endpoint with filtering
@app.get("/metrics/custom")
async def custom_metrics():
    from prometheus_client import CollectorRegistry

    registry = CollectorRegistry()

    # Only include specific metrics
    registry.register(REQUEST_COUNT)
    registry.register(REQUEST_LATENCY)

    return Response(
        content=generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST,
    )
```

---

## Metric Labels <a name="labels"></a>

Labels add dimensions to metrics for filtering and grouping.

```python
# Good: Low cardinality labels
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total requests",
    ["method", "status_code"]  # method: GET/POST/PUT/DELETE, status: 200/400/500
)

# Bad: High cardinality labels (can cause memory issues)
# Don't use user_id, request_id, or timestamps as labels

# Label best practices:
# - Use enums/categorical values
# - Keep label values low cardinality (< 1000 unique values)
# - Use method (GET, POST) not full URL
# - Use status code class (2xx, 4xx, 5xx) not exact codes

# Using label patterns
REQUEST_STATUS = Counter(
    "http_requests_total",
    "Total requests",
    ["method", "endpoint", "status_class"]
)

def get_status_class(status_code: int) -> str:
    return f"{status_code // 100}xx"

# Usage
REQUEST_STATUS.labels(
    method="GET",
    endpoint="/api/users",
    status_class=get_status_class(200)
).inc()
```

---

## Alerting Rules <a name="alerting"></a>

```yaml
# prometheus/alert_rules.yml
groups:
  - name: fastapi_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status_class=~"5xx"}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High P95 latency"
          description: "P95 latency is {{ $value }}s"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          process_memory_bytes / 1024 / 1024 > 512
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}MB"

      # No traffic
      - alert: NoTraffic
        expr: |
          rate(http_requests_total[5m]) == 0
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "No traffic detected"
          description: "No requests received in 10 minutes"

      # Pod restart
      - alert: PodRestarting
        expr: |
          increase(kube_pod_container_status_restarts_total[1h]) > 3
        labels:
          severity: critical
        annotations:
          summary: "Pod is restarting frequently"
```

---

## Prometheus Setup <a name="setup"></a>

### docker-compose.yml

```yaml
version: "3.9"

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.retention.time=30d"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  app:
    build: .
    ports:
      - "8000:8000"
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=8000"
      - "prometheus.io/path=/metrics"

volumes:
  prometheus_data:
  grafana_data:
```

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

scrape_configs:
  - job_name: "fastapi-app"
    static_configs:
      - targets: ["app:8000"]
    metrics_path: "/metrics"
    scrape_interval: 10s

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

### PromQL Queries

```promql
# Request rate (per second)
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status_class="5xx"}[5m]) / rate(http_requests_total[5m])

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Active requests
fastapi_active_requests

# Top endpoints by request count
topk(10, sum by (endpoint) (rate(http_requests_total[5m])))

# 5xx errors in the last hour
sum(increase(http_requests_total{status_class="5xx"}[1h]))
```

---

## Interview Questions

1. **What is the difference between Counter, Histogram, and Gauge?**
Counter: monotonically increasing (total requests, errors). Histogram: value distribution with buckets (latency, response size). Gauge: value that goes up and down (active connections, queue depth). Use Counter for rates, Histogram for percentiles, Gauge for current state.

2. **Why are labels important in Prometheus metrics?**
Labels add dimensions for filtering and grouping. You can query by method, endpoint, status code, etc. Keep label cardinality low to avoid memory issues. Never use high-cardinality values like user IDs or timestamps as labels.

3. **How do you calculate error rate with Prometheus?**
`rate(http_requests_total{status_class="5xx"}[5m]) / rate(http_requests_total[5m])`. This gives the 5xx error ratio over 5 minutes. Alert when this exceeds a threshold (e.g., 5%).

4. **What are the best practices for defining Prometheus metrics?**
Use appropriate metric types (Counter vs Gauge). Keep label cardinality low. Name metrics with `_total` suffix for counters, `_seconds` for duration metrics. Define buckets that match your expected value ranges. Use prefixes consistently (e.g., `http_`, `db_`, `app_`).

5. **How do you collect metrics from a FastAPI application?**
Add `prometheus-client` middleware that instruments every request. Expose a `/metrics` endpoint using `generate_latest()`. Configure Prometheus to scrape this endpoint. Use labels for method, endpoint, and status code. Add custom metrics for business logic.
