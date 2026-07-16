# Monitoring and Logging — Interview Questions

## Table of Contents
1. [Basics](#basics)
2. [Structured Logging](#structured-logging)
3. [Prometheus Metrics](#prometheus-metrics)
4. [Grafana Dashboards](#grafana-dashboards)
5. [Distributed Tracing](#distributed-tracing)
6. [OpenTelemetry](#opentelemetry)
7. [Health Checks](#health-checks)
8. [Alerting](#alerting)
9. [SLO/SLI](#slosli)
10. [Log Aggregation](#log-aggregation)
11. [Production Observability](#production-observability)

---

## Basics

### Q1: What are the three pillars of observability?
**Answer:** The three pillars are **logs**, **metrics**, and **traces**. Logs provide discrete event records. Metrics provide aggregated numerical measurements over time. Traces provide request-level execution paths through distributed systems. Together they give full visibility into system behavior.

| Pillar | What | Example | Tool |
|--------|------|---------|------|
| Logs | Discrete events | "User login failed" | ELK, Loki |
| Metrics | Aggregated numbers | Request rate, latency | Prometheus |
| Traces | Request paths | DB→Service→Service | Jaeger, Tempo |

### Q2: What is structured logging and why use it?
**Answer:** Structured logging outputs logs as JSON objects with consistent field names instead of unstructured text strings. Benefits: machine-parseable, filterable in log aggregators, supports correlation IDs, and enables programmatic analysis.

```python
# ❌ Unstructured (bad)
logger.info(f"User {user_id} logged in from {ip}")

# ✅ Structured (good)
logger.info("User logged in", extra={
    "user_id": user_id,
    "ip": ip,
    "action": "login",
    "timestamp": datetime.utcnow().isoformat(),
})
```

### Q3: What is the difference between logging and monitoring?
**Answer:** Logging records discrete events for debugging and auditing. Monitoring collects metrics and alerts on thresholds. Logging tells you *what happened*. Monitoring tells you *how the system is performing*. Both are essential for production observability.

### Q4: What are log levels and when to use each?
**Answer:**
- **DEBUG**: Detailed diagnostic info (dev only)
- **INFO**: Normal operations (requests, user actions)
- **WARNING**: Unexpected but handled (retrying, degraded service)
- **ERROR**: Operation failed (exception, 5xx response)
- **CRITICAL**: System is unusable (database down, disk full)

### Q5: How do you implement logging in FastAPI?
**Answer:** Use Python's `logging` module with a structured formatter. Inject a request-scoped logger via middleware. Include correlation IDs for distributed tracing.

```python
import logging
import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger

# Usage in endpoint
@app.get("/users")
async def get_users():
    logger = get_logger("users")
    logger.info("Fetching users", extra={"request_id": request_id_var.get()})
    ...
```

---

## Structured Logging

### Q6: How do you structure log entries for microservices?
**Answer:** Each log entry should include: timestamp (ISO 8601), level, service name, request ID, user ID, action, duration, status, and error details if applicable. This structure enables filtering, correlation, and debugging across services.

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

logger.info(
    "api_request",
    method="GET",
    path="/api/users",
    status_code=200,
    duration_ms=45.2,
    user_id="u_123",
    request_id="req_abc",
)
# Output: {"event": "api_request", "level": "info", "timestamp": "2024-01-15T10:30:00Z", "method": "GET", ...}
```

### Q7: How do you handle sensitive data in logs?
**Answer:** Never log passwords, tokens, credit card numbers, or PII. Use log filtering/redaction middleware. Mask sensitive fields with partial values (e.g., `****1234`). Implement a redaction layer that runs on all log output.

```python
import re

class SensitiveDataFilter(logging.Filter):
    PATTERNS = [
        (re.compile(r'password["\s:=]+\S+', re.I), 'password=****'),
        (re.compile(r'token["\s:=]+\S+', re.I), 'token=****'),
        (re.compile(r'\b\d{16}\b'), '****-****-****-****'),
    ]

    def filter(self, record):
        msg = record.getMessage()
        for pattern, replacement in self.PATTERNS:
            msg = pattern.sub(replacement, msg)
        record.msg = msg
        record.args = ()
        return True
```

### Q8: What is the ELK stack?
**Answer:** **Elasticsearch** (search/indexing), **Logstash** (processing/parsing), **Kibana** (visualization). It's a log aggregation pipeline. Filebeat ships logs to Logstash, which parses and enriches them, then sends to Elasticsearch for indexing and search. Kibana provides dashboards and query UI.

### Q9: What is the difference between ELK and Loki?
**Answer:** ELK stores the full log content and indexes every field. Loki stores only labels (like Prometheus) and the raw log text, indexing only labels. Loki is cheaper to run, integrates natively with Grafana, but supports less powerful search. ELK is better for full-text search across log content.

---

## Prometheus Metrics

### Q10: What are the four types of Prometheus metrics?
**Answer:**
- **Counter**: Monotonically increasing value (total requests, errors)
- **Gauge**: Value that can go up or down (memory usage, queue size)
- **Histogram**: Distribution of values with buckets (request duration)
- **Summary**: Like histogram but calculated client-side (less common now)

```python
from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Number of active connections"
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "path"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)
```

### Q11: How do you instrument a FastAPI app with Prometheus?
**Answer:** Use `prometheus-fastapi-instrumentator` for automatic metrics, or write custom middleware for control.

```python
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

# Automatic instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Custom metrics
ERROR_COUNT = Counter("app_errors_total", "Total errors", ["error_type"])

@app.get("/process")
async def process_data():
    try:
        result = await process()
        return result
    except ValueError as e:
        ERROR_COUNT.labels(error_type="value_error").inc()
        raise
```

### Q12: What are cardinality issues in Prometheus?
**Answer:** Cardinality explosion happens when label values are unbounded (user IDs, request IDs, UUIDs). Each unique label combination creates a time series. Too many time series consume memory and slow queries. Always use bounded labels. Use logarithmic bucketing for high-cardinality data.

```python
# ❌ High cardinality (BAD)
REQUEST_LATENCY.labels(user_id="u_123", request_id="req_abc").observe(duration)

# ✅ Low cardinality (GOOD)
REQUEST_LATENCY.labels(endpoint="/api/users", method="GET").observe(duration)
```

### Q13: How do you write effective Prometheus queries (PromQL)?
**Answer:**

```promql
# Request rate (per second, over 5m)
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Apdex score
(rate(http_requests_total{status=~"2.."}[5m]) + rate(http_requests_total{status=~"2..", duration<0.3}[5m]) / 2) / rate(http_requests_total[5m])

# Top 10 slowest endpoints
topk(10, histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])))

# Memory usage trend
process_resident_memory_bytes / 1024 / 1024
```

---

## Grafana Dashboards

### Q14: What should a production FastAPI dashboard include?
**Answer:**
- Request rate (total and per endpoint)
- Error rate (5xx, 4xx)
- Latency percentiles (P50, P95, P99)
- Active connections
- CPU/memory usage
- Database connection pool stats
- Queue depth
- Cache hit/miss ratio

### Q15: How do you create Grafana alerts?
**Answer:** Use Grafana alerting rules with conditions on PromQL queries. Define thresholds, evaluation intervals, and notification channels (Slack, PagerDuty, email).

```yaml
# grafana/alerting.yaml
groups:
  - name: fastapi-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency above 2 seconds"
```

### Q16: How do you visualize distributed tracing data in Grafana?
**Answer:** Use Grafana Tempo as the trace backend. Configure OpenTelemetry to send traces to Tempo. In Grafana, use the TraceQL query language to search and filter traces. Link logs to traces using trace IDs.

---

## Distributed Tracing

### Q17: What is distributed tracing?
**Answer:** Distributed tracing tracks a request as it flows through multiple services. Each service creates a **span** (unit of work) with timing and metadata. Spans are connected via **trace IDs** to form a **trace** (complete request path). This helps identify bottlenecks, failures, and latency in distributed systems.

### Q18: What are spans and how do they work?
**Answer:** A span represents a single operation within a trace. It has: operation name, start/end time, parent span ID, and attributes (tags). Spans form a tree - the root span covers the entire request, child spans cover sub-operations (DB query, HTTP call).

```python
from opentelemetry import trace

tracer = trace.get_tracer("my-service")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)

        with tracer.start_as_current_span("db_query") as child_span:
            user = await db.get(User, user_id)
            child_span.set_attribute("db.statement", "SELECT * FROM users WHERE id = ?")

        span.set_attribute("user.found", user is not None)
        return user
```

### Q19: How do you propagate trace context across services?
**Answer:** Use W3C Trace Context headers (`traceparent`, `tracestate`). When Service A calls Service B, it injects the trace ID into the HTTP headers. Service B extracts the headers and continues the trace. OpenTelemetry handles this automatically.

```python
import httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# Auto-instrument httpx client
HTTPXClientInstrumentor().instrument()

@app.get("/aggregate")
async def aggregate_data():
    # Trace context automatically propagated
    async with httpx.AsyncClient() as client:
        users = await client.get("http://users-service/api/users")
        orders = await client.get("http://orders-service/api/orders")
    return {"users": users.json(), "orders": orders.json()}
```

---

## OpenTelemetry

### Q20: What is OpenTelemetry?
**Answer:** OpenTelemetry (OTel) is an open-source observability framework providing vendor-neutral APIs for collecting traces, metrics, and logs. It includes SDKs, exporters, and instrumentation libraries. It standardizes observability across languages and backends.

### Q21: How do you configure OpenTelemetry for FastAPI?
**Answer:**

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, OTLPExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure provider
provider = TracerProvider()
exporter = OTLPExporter(endpoint="http://otel-collector:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLAlchemy
SQLAlchemyInstrumentor().instrument(engine=engine)
```

### Q22: What is an OpenTelemetry Collector?
**Answer:** A vendor-agnostic proxy that receives telemetry data, processes it (batching, filtering, enrichment), and exports it to multiple backends (Jaeger, Prometheus, Grafana Tempo, Datadog). It decouples your app from the observability backend, making backend switches transparent.

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 5s
    send_batch_size: 1000

exporters:
  otlp:
    endpoint: jaeger:4317
  prometheus:
    endpoint: 0.0.0.0:8889

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

### Q23: How do you correlate logs, metrics, and traces?
**Answer:** Use the trace ID as the correlation key. Include trace IDs in log entries. Link metrics to traces using exemplars. Grafana provides cross-linking between dashboards, logs, and traces using these IDs.

```python
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        return True

# Log format includes trace_id
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", '
    '"trace_id": "%(trace_id)s", "message": "%(message)s"}'
)
```

---

## Health Checks

### Q24: How do you implement health checks in FastAPI?
**Answer:** Implement `/health/live` (liveness) and `/health/ready` (readiness) endpoints. Liveness confirms the process is running. Readiness confirms the service can handle requests (DB connected, dependencies available).

```python
from fastapi import Response

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness(response: Response):
    checks = {}
    all_ok = True

    # Check database
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        all_ok = False

    # Check Redis
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
        all_ok = False

    status_code = 200 if all_ok else 503
    response.status_code = status_code
    return {"status": "healthy" if all_ok else "degraded", "checks": checks}
```

### Q25: How do Kubernetes health checks work with FastAPI?
**Answer:** Kubernetes uses liveness probes to restart unhealthy pods and readiness probes to route traffic. Configure in deployment YAML. Liveness should detect deadlocks (process running but not responding). Readiness should check external dependencies.

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    spec:
      containers:
        - name: fastapi
          image: fastapi-app:latest
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

---

## Alerting

### Q26: What are alert fatigue and how do you prevent it?
**Answer:** Alert fatigue happens when too many low-priority alerts desensitize engineers. Prevent it by: grouping related alerts, setting appropriate thresholds (not too sensitive), using severity levels (critical vs warning), implementing alert deduplication, and regularly reviewing and pruning alerts.

### Q27: How do you design an effective alerting strategy?
**Answer:** Alert on symptoms, not causes (error rate, not CPU usage). Use multi-window multi-burn-rate alerts for SLOs. Define runbooks for each alert. Escalate based on severity. Test alerts regularly.

```yaml
# Burn rate alert example
groups:
  - name: slo-alerts
    rules:
      - alert: HighErrorBurnRate
        expr: |
          (
            rate(http_requests_total{status=~"5.."}[1h])
            / rate(http_requests_total[1h])
          ) > (14.4 * 0.001)
          and
          (
            rate(http_requests_total{status=~"5.."}[5m])
            / rate(http_requests_total[5m])
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error budget burning too fast"
          runbook_url: "https://runbooks.example.com/slo-burn-rate"
```

### Q28: How do you route alerts to the right teams?
**Answer:** Use alert labels to determine routing. Route by service, severity, and team ownership. Integrate with PagerDuty for on-call scheduling, Slack for non-urgent notifications, and email for informational alerts.

```yaml
# Alertmanager routing
route:
  receiver: default
  group_by: ['alertname', 'service']
  routes:
    - match:
        severity: critical
      receiver: pagerduty-oncall
    - match:
        severity: warning
      receiver: slack-alerts
    - match:
        severity: info
      receiver: email-team
```

---

## SLO/SLI

### Q29: What are SLOs and SLIs?
**Answer:** **SLI** (Service Level Indicator) is a quantitative measure: error rate, latency, throughput. **SLO** (Service Level Objective) is the target value for an SLI: 99.9% availability, P99 latency < 500ms. **SLA** (Service Level Agreement) is the contractual commitment with consequences for missing targets.

```python
# Example SLO definitions
SLOS = {
    "availability": {
        "sli": "successful_requests / total_requests",
        "target": 0.999,  # 99.9%
        "window": "30d",
        "error_budget": 0.001 * 30 * 24 * 60,  # 43.2 minutes/month
    },
    "latency": {
        "sli": "requests_under_500ms / total_requests",
        "target": 0.99,  # 99% under 500ms
        "window": "30d",
    },
}
```

### Q30: How do you calculate and monitor error budgets?
**Answer:** Error budget = 1 - SLO target. For 99.9% availability over 30 days, the budget is 0.1% of requests or ~43.2 minutes of downtime. Track consumption rate. When the budget is depleted, freeze feature releases and focus on reliability. Alert when the burn rate exceeds sustainable levels.

```promql
# Error budget remaining (30-day window)
1 - (
  (1 - 0.999) * 30 * 24 * 60  # total budget in minutes
  - (sum_over_time((1 - (rate(http_requests_total{status!~"5.."}[5m]) / rate(http_requests_total[5m]))) * 60)[30d:5m])
)
# If result < 0, error budget is exhausted

# Burn rate (1h window vs 30-day budget)
(rate(http_requests_total{status=~"5.."}[1h]) / rate(http_requests_total[1h])) / (1 - 0.999)
```

---

## Log Aggregation

### Q31: How do you ship logs from containers to a central system?
**Answer:** Use a log shipper (Filebeat, Fluentd, Promtail) as a sidecar or daemonset. It reads container stdout/stderr, parses and enriches logs, and forwards to the aggregation backend (ELK, Loki).

```yaml
# Fluentd ConfigMap for Kubernetes
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      <parse>
        @type json
      </parse>
    </source>

    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>

    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name ${tag}
    </match>
```

### Q32: What is the difference between centralized and edge logging?
**Answer:** Centralized logging ships all logs to a central system for indexing and search. Edge logging processes and filters logs locally before shipping, reducing bandwidth and storage costs. Use edge logging for high-volume applications; centralize for complete audit trails.

### Q33: How do you implement log-based alerting?
**Answer:** Define alerts on log patterns using LogQL (Loki), Lucene (Elasticsearch), or metric filters (CloudWatch). Alert when a log pattern appears more than a threshold rate. Useful for detecting application errors that don't surface as HTTP errors.

```promql
# Loki alert: too many OOM errors
sum(rate({app="fastapi"} |~ "OOM|OutOfMemory"[5m])) > 0.1

# Elasticsearch alert: exception spike
{
  "query": {
    "bool": {
      "filter": [
        { "match": { "message": "Exception" } },
        { "range": { "@timestamp": { "gte": "now-5m" } } }
      ]
    }
  },
  "aggs": {
    "exception_rate": {
      "rate": { "field": "message" }
    }
  }
}
```

---

## Production Observability

### Q34: How do you debug a slow request in production?
**Answer:** Use distributed tracing to identify which span is slow. Check the trace in Jaeger/Tempo. Look at the span's duration, database queries, and downstream calls. Correlate with logs using the trace ID. Check if the slowness is in the app, database, or a downstream service.

### Q35: What metrics should you track for database performance?
**Answer:**
- Query latency (P50, P95, P99)
- Query throughput (queries per second)
- Connection pool utilization
- Active/idle connections
- Cache hit ratio
- Lock wait time
- Replication lag
- Deadlock count

```python
# SQLAlchemy instrumentation
from prometheus_client import Histogram, Gauge

DB_QUERY_DURATION = Histogram(
    "db_query_duration_seconds",
    "Database query duration",
    ["query_type"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

DB_POOL_SIZE = Gauge("db_pool_size", "Database pool size")
DB_POOL_CHECKED_OUT = Gauge("db_pool_checked_out", "Checked out connections")
DB_POOL_OVERFLOW = Gauge("db_pool_overflow", "Pool overflow count")
```

### Q36: How do you handle log retention and rotation?
**Answer:** Use time-based rotation (daily/weekly) and size-based rotation (100MB files). Implement retention policies (30 days for app logs, 90 days for audit logs, 1 year for compliance). Compress old logs. Use object storage (S3) for archival. Configure in the log shipper, not the application.

```python
# logging.conf
[handler_file]
class=logging.handlers.RotatingFileHandler
maxBytes=104857600  # 100MB
backupCount=30
formatter=json
```

### Q37: What is the RED method for monitoring?
**Answer:** **Rate** (requests per second), **Errors** (error rate), **Duration** (latency). It's a methodology for monitoring user-facing services. Track these three metrics per service/endpoint. It covers the most important aspects of service health.

### Q38: What is the USE method for monitoring?
**Answer:** **Utilization** (percentage of resource in use), **Saturation** (work queued), **Errors** (error events). It's for monitoring infrastructure resources (CPU, memory, disk, network). Apply to every resource in the system. It helps identify capacity constraints.

| Resource | Utilization | Saturation | Errors |
|----------|-------------|------------|--------|
| CPU | % busy | Run queue length | Machine checks |
| Memory | % used | Swap usage | OOM kills |
| Disk | % utilized | I/O queue | I/O errors |
| Network | % bandwidth | Queue length | Drops/retransmits |

### Q39: How do you implement request tracing headers in FastAPI?
**Answer:**

```python
import uuid
from contextvars import ContextVar

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")
span_id_var: ContextVar[str] = ContextVar("span_id", default="")

@app.middleware("http")
async def tracing_middleware(request: Request, call_next):
    # Extract or generate trace context
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    parent_span_id = request.headers.get("X-Span-ID")

    trace_id_var.set(trace_id)
    span_id_var.set(str(uuid.uuid4()))

    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    # Add tracing headers to response
    response.headers["X-Trace-ID"] = trace_id_var.get()
    response.headers["X-Span-ID"] = span_id_var.get()
    response.headers["X-Response-Time"] = f"{duration:.4f}s"

    # Log request with trace context
    logger.info("request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2),
        trace_id=trace_id,
    )

    return response
```

### Q40: How do you set up a complete observability stack for FastAPI?
**Answer:** Combine all components:
- **FastAPI** with OpenTelemetry instrumentation
- **Prometheus** for metrics collection
- **Grafana** for dashboards and visualization
- **Loki** (or ELK) for log aggregation
- **Tempo** (or Jaeger) for distributed tracing
- **Alertmanager** for alert routing

```yaml
# docker-compose.yml
version: "3.8"
services:
  fastapi:
    build: .
    environment:
      OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector:4317
      OTEL_SERVICE_NAME: fastapi-app

  otel-collector:
    image: otel/opentelemetry-collector:latest
    volumes:
      - ./otel-config.yaml:/etc/otelcol/config.yaml

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"

  loki:
    image: grafana/loki:latest

  tempo:
    image: grafana/tempo:latest

  alertmanager:
    image: prom/alertmanager:latest
```

### Q41: How do you measure API performance in production?
**Answer:** Track these KPIs:
- **Apdex score**: User satisfaction (satisfied + tolerating / total)
- **P50 latency**: Median response time
- **P95/P99 latency**: Tail latency
- **Throughput**: Requests per second
- **Error rate**: 5xx / total requests
- **Saturation**: CPU, memory, connection pool usage

```promql
# Apdex (0.5s tolerance)
(rate(http_requests_total{status=~"2.."}[5m])
 + (rate(http_requests_total{status=~"2..", duration<0.5}[5m]) / 2))
/ rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Throughput
sum(rate(http_requests_total[5m])) by (service)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

### Q42: How do you handle observability in serverless/lambda environments?
**Answer:** Use structured JSON logging (stdout). Send metrics to CloudWatch/Prometheus Pushgateway. Enable X-Ray or OpenTelemetry for tracing. Cold start metrics are critical. Use Powertools for AWS Lambda to simplify instrumentation.

```python
# AWS Lambda with Powertools
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics()

@tracer.capture_lambda_handler
@logger.inject_lambda_context
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event, context):
    logger.info("Processing request", request_id=event["requestId"])

    with tracer.provider.in_subsegment("external_api_call") as subsegment:
        result = call_external_api(event["data"])

    metrics.add_metric(name="ProcessingTime", unit=MetricUnit.Milliseconds, value=duration)
    metrics.add_metric(name="SuccessCount", unit=MetricUnit.Count, value=1)

    return result
```
