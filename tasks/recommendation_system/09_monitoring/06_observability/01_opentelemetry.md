# OpenTelemetry for Recommendation Systems

## Overview

OpenTelemetry (OTel) is the CNCD-standard, vendor-neutral observability framework that unifies
metrics, traces, and logs into a single instrumentation system. For recommendation systems,
OTel provides end-to-end visibility across the entire request lifecycle — from API gateway
through feature retrieval, model inference, and response delivery — while remaining agnostic
to the backend storage (Prometheus, Jaeger, Grafana Tempo, Loki). This covers the OTel
architecture, auto-instrumentation, custom metrics, trace context propagation, and integration
with the Grafana observability stack.

## Why OpenTelemetry for Recommendation Systems

### Observability Challenges

Recommendation systems present unique observability challenges:

- **Multi-service architecture**: 5-10+ microservices per recommendation request
- **Heterogeneous workloads**: CPU-bound API serving, GPU-bound model inference, I/O-bound feature reads
- **Real-time and batch**: Online serving requires sub-100ms latency; batch pipelines process millions of records
- **ML-specific metrics**: Model accuracy, feature drift, and prediction quality need custom instrumentation
- **Vendor lock-in risk**: Proprietary agent dependencies limit flexibility

### OpenTelemetry Advantages

| Advantage                     | Description                                          |
|------------------------------|------------------------------------------------------|
| Vendor-neutral               | Switch backends without re-instrumenting              |
| Unified SDK                  | Single API for metrics, traces, and logs              |
| Auto-instrumentation         | Zero-code instrumentation for common frameworks       |
| Rich ecosystem               | 500+ integrations (libraries, databases, services)   |
| CNCF graduated               | Long-term support and community investment            |
| Future-proof                 | Adding new backends requires only configuration       |

## Metrics, Traces, Logs Integration

### The Three Pillars in OpenTelemetry

```
                    OpenTelemetry API
                    ┌────────────────┐
                    │                │
    ┌───────────────┤   Traces       ├───────────────┐
    │               │   (Spans)      │               │
    │               └────────────────┘               │
    │                                                │
┌───▼──────────┐                        ┌────────────▼───┐
│   Metrics    │                        │     Logs       │
│   (Counters, │                        │   (Structured  │
│   Histograms,│                        │    Events)     │
│   Gauges)    │                        │                │
└──────────────┘                        └────────────────┘
    │                    │                   │
    └────────────────────┼───────────────────┘
                         │
              OpenTelemetry Collector
                         │
              ┌──────────▼──────────┐
              │   Processed,        │
              │   Batched,          │
              │   Exported          │
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
    │Prometheus│    │   Tempo   │   │  Loki   │
    │(Metrics) │    │ (Traces)  │   │ (Logs)  │
    └─────────┘    └───────────┘   └─────────┘
```

### Correlation Between Pillars

OpenTelemetry enables correlation across all three pillars:

1. **Metrics → Traces**: Exemplars link high-latency metrics to specific traces
2. **Traces → Logs**: Trace ID and span ID appear in structured logs
3. **Logs → Traces**: Log queries can navigate to the associated trace
4. **Metrics → Logs**: Log-based metrics derive counters from log events

This correlation enables debugging workflows like:
- See high latency in metrics dashboard
- Click exemplar to view the specific trace
- From trace, navigate to logs for that request
- From logs, see the error details and stack trace

## Auto-Instrumentation

### Python Auto-Instrumentation

OpenTelemetry provides zero-code instrumentation for Python web frameworks:

```python
# No code changes needed — use the OTel agent
# Command: opentelemetry-instrument \
#   --service_name recommendation-api \
#   --exporter_otlp_endpoint http://otel-collector:4317 \
#   python -m uvicorn main:app

# Automatically instruments:
# - FastAPI / Flask / Django request handling
# - HTTP client calls (requests, urllib3)
# - Database queries (SQLAlchemy, psycopg2)
# - Redis operations (redis-py)
# - Kafka produce/consume (confluent-kafka)
# - gRPC client/server calls
```

### Framework-Specific Instrumentation

| Framework          | What Is Auto-Instrumented                           |
|-------------------|-----------------------------------------------------|
| FastAPI/Flask      | HTTP request duration, status codes, route patterns  |
| SQLAlchemy         | Query duration, rows affected, connection pool stats |
| Redis              | Command duration, pipeline operations, connection    |
| Kafka producer     | Produce duration, batch size, acknowledgments       |
| Kafka consumer     | Consume duration, batch processing time              |
| gRPC               | Call duration, status codes, message sizes           |
| HTTP client        | Outbound request duration, status, target service    |

### Custom Instrumentation

For recommendation-specific operations, add custom spans and metrics:

```python
# Custom span for recommendation pipeline
with tracer.start_as_current_span("recommendation.pipeline") as span:
    span.set_attribute("user_id", user_id)
    span.set_attribute("algorithm", "hybrid")

    with tracer.start_as_current_span("feature.retrieval") as feature_span:
        features = feature_store.get_features(user_id)
        feature_span.set_attribute("feature_count", len(features))
        feature_span.set_attribute("cache_hit", was_cached)

    with tracer.start_as_current_span("model.inference") as model_span:
        scores = model.predict(features, candidates)
        model_span.set_attribute("model_version", model.version)
        model_span.set_attribute("candidate_count", len(candidates))

    with tracer.start_as_current_span("ranking.postprocess") as rank_span:
        final = rank_and_filter(scores, constraints)
        rank_span.set_attribute("output_count", len(final))
```

### Custom Metrics

```python
# Recommendation-specific metrics
recommendation_counter = meter.create_counter(
    name="recommendations.generated.total",
    description="Total recommendations generated",
    unit="1"
)

recommendation_histogram = meter.create_histogram(
    name="recommendation.score.distribution",
    description="Distribution of recommendation scores",
    unit="1",
    boundaries=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

cold_start_counter = meter.create_counter(
    name="recommendations.cold_start.total",
    description="Total cold-start recommendation requests"
)

model_accuracy_gauge = meter.create_gauge(
    name="model.accuracy.current",
    description="Current model accuracy score",
    unit="1"
)

# Usage
recommendation_counter.add(1, {
    "algorithm": "hybrid",
    "model_version": "v2.3",
    "user_segment": "active"
})

recommendation_histogram.record(score, {
    "algorithm": "collaborative_filtering"
})

cold_start_counter.add(1, {"reason": "new_user"})
```

## Trace Context Propagation

### W3C Trace Context Standard

OpenTelemetry uses W3C Trace Context as the default propagation format:

```
Header: traceparent: 00-{trace-id}-{span-id}-{trace-flags}
Example: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

Components:
  00       — version
  4bf92f   — trace ID (128-bit, globally unique)
  00f067   — span ID (64-bit, unique within trace)
  01       — trace flags (01 = sampled)
```

### Propagation Across Recommendation Services

```
External Request:
  Client → API Gateway
  Headers: (no trace context)

API Gateway creates root span:
  trace_id: abc123...
  span_id: 001
  Headers: traceparent: 00-abc123...-001-01

API Gateway → Recommendation Service:
  Headers: traceparent: 00-abc123...-001-01 (forwarded)

Recommendation Service creates child span:
  span_id: 002
  Parent: 001

Recommendation Service → Feature Store:
  Headers: traceparent: 00-abc123...-002-01

Recommendation Service → Model Server:
  Headers: traceparent: 00-abc123...-002-01
  All child spans share the same trace_id

Model Server creates child span:
  span_id: 003
  Parent: 002
```

### Context Propagation in Kafka

Kafka does not natively propagate HTTP headers. Solutions:

1. **OTel Kafka interceptor**: Auto-inject/extract trace context in Kafka headers
2. **Manual propagation**: Include traceparent in message headers explicitly
3. **Messaging attributes**: Use OTel messaging semantic conventions

```
Producer:
  Kafka Headers: {
    "traceparent": "00-abc123...-002-01"
  }
  OTel Attributes: {
    messaging.system: "kafka"
    messaging.destination: "user-events"
    messaging.operation: "publish"
  }

Consumer:
  Extract traceparent from Kafka headers
  Create consumer span linked to producer trace
  OTel Attributes: {
    messaging.system: "kafka"
    messaging.destination: "user-events"
    messaging.operation: "receive"
  }
```

## OpenTelemetry Collector

### Collector Architecture

```
Receivers          Processors           Exporters
──────────        ────────────         ──────────
OTLP gRPC    →    Batch          →     Prometheus
OTLP HTTP    →    Attributes     →     Jaeger
Prometheus   →    Tail Sampling  →     Grafana Tempo
Jaeger       →    Filter         →     Loki
Zipkin       →    Memory Limiter →     OTLP

Additional Components:
  Connectors: Bridge between metrics and traces
  Extensions: Health check, pprof, zpages
```

### Collector Deployment for Recommendation Systems

```yaml
# DaemonSet (per-node) + Deployment (central) pattern

DaemonSet (per-node agent):
  Receivers: OTLP (from local pods)
  Processors: Batch (small batches, fast export)
  Exporters: Forward to central collector

Deployment (central collector):
  Receivers: OTLP (from agents) + Prometheus (scrape)
  Processors: Batch (large batches) + Tail Sampling + Attributes
  Exporters: Backend storage (Prometheus, Tempo, Loki)
```

### Tail Sampling Configuration

```yaml
processors:
  tail_sampling:
    decision_wait: 10s        # Wait 10s for spans to arrive
    num_traces: 100000        # Max traces in memory
    policies:
      - name: errors
        type: status_code
        status_code:
          status_codes: [ERROR]

      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 500

      - name: probabilistic
        type: probabilistic
        probabilistic:
          sampling_percentage: 5

      - name: service-specific
        type: string_attribute
        string_attribute:
          key: service.name
          values: [recommendation-api, model-server]
```

## Grafana Stack Integration

### Unified Observability Dashboard

```
Grafana Dashboard Layout:
├── Row 1: System Overview
│   ├── Request rate (Prometheus metrics)
│   ├── Error rate (Prometheus metrics)
│   ├── P95 latency (Prometheus metrics)
│   └── Active traces count (Tempo)
│
├── Row 2: Service Details
│   ├── Per-service latency (Prometheus metrics)
│   ├── Trace breakdown (Tempo traces)
│   ├── Service dependency graph (Tempo service graph)
│   └── Error logs (Loki logs)
│
├── Row 3: ML Model Monitoring
│   ├── Model inference latency (custom metrics)
│   ├── Prediction score distribution (custom metrics)
│   ├── Feature drift indicators (custom metrics)
│   └── Model accuracy trend (custom metrics)
│
└── Row 4: Infrastructure
    ├── CPU/Memory utilization (node_exporter)
    ├── Pod status and restarts (kube-state-metrics)
    ├── Network traffic (node_exporter)
    └── Disk I/O (node_exporter)
```

### Exemplar Configuration

Exemplars link metrics to traces:

```
Prometheus metric with exemplar:
  http_request_duration_seconds_bucket{le="0.1"} 9542
  # Exemplar: trace_id="abc123" timestamp=1704067200000

In Grafana:
  1. View latency histogram in metrics panel
  2. Click on a data point with exemplar
  3. Navigate directly to the trace in Tempo
  4. Investigate the specific slow request
```

## Observability-Driven Development

### Development Workflow

1. **Design**: Define what needs to be observable before coding
2. **Instrument**: Add spans and metrics during development
3. **Test**: Verify observability in staging (logs appear, traces are complete)
4. **Review**: Code review includes observability check (are spans meaningful?)
5. **Deploy**: Verify dashboards and alerts work in production
6. **Operate**: Use observability data for debugging and optimization

### Observability Checklist for New Features

- [ ] Custom metrics defined for the feature
- [ ] Traces cover all critical code paths
- [ ] Structured logs include relevant context
- [ ] Dashboard panels created for new metrics
- [ ] Alert rules configured for error conditions
- [ ] Runbook updated with new observability data points
- [ ] Exemplars configured for key metrics

### SLO Definitions in OpenTelemetry

Define SLOs as part of the instrumentation:

- Availability SLO: 99.9% successful requests
- Latency SLO: 99% of requests < 200ms
- Freshness SLO: 99% of features < 1 hour old
- Correctness SLO: 99.99% of recommendations are valid items

These SLOs drive both dashboard design and alerting strategy, creating a unified
observability approach from development through production operations.
