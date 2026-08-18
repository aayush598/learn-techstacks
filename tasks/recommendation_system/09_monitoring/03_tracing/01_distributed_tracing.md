# Distributed Tracing with OpenTelemetry for Recommendation Systems

## Overview

Distributed tracing tracks requests as they flow through multiple services in the recommendation
system, providing end-to-end visibility into latency, errors, and data flow. OpenTelemetry is
the CNCF standard for collecting traces (along with metrics and logs), providing a vendor-neutral
instrumentation framework. This covers trace/span propagation, sampling strategies, trace
analysis for latency optimization, and integration with the broader observability stack.

## Why Distributed Tracing Is Critical for Recommendation Systems

A single recommendation request touches many services:

```
Trace for one recommendation request:

[API Gateway] 2ms
  └── [Auth Service] 1ms
  └── [Recommendation Service] 42ms
        └── [Feature Store] 8ms
        │     └── [Redis] 2ms
        └── [Model Server] 25ms
        │     └── [Model Store] 3ms
        └── [Catalog Service] 5ms
        │     └── [PostgreSQL] 2ms
        └── [Post-processing] 4ms
  └── [Response Serialization] 1ms

Total: 46ms

Without tracing, finding the 25ms model inference bottleneck
requires manually correlating logs across 5 services.
With tracing, the critical path is immediately visible.
```

## OpenTelemetry Architecture

### Component Overview

```
Application Code
    │
    ├── OpenTelemetry SDK (auto-instrumentation + custom spans)
    │
    ├── OTLP Exporter (gRPC or HTTP)
    │
    ▼
OpenTelemetry Collector
    │
    ├── Receivers (OTLP, Prometheus, Jaeger, Zipkin)
    ├── Processors (batch, sampling, filtering, attributes)
    ├── Exporters (Jaeger, Tempo, Prometheus, logging)
    │
    ▼
Backend Storage
    ├── Jaeger / Grafana Tempo (trace storage)
    ├── Prometheus (metrics)
    └── Loki (logs)

Visualization
    └── Grafana (unified dashboards with traces, metrics, logs)
```

### OpenTelemetry SDK Setup

Initialize the SDK at application startup:

1. Configure the OTLP exporter to send to the collector
2. Set the service name and version
3. Configure resource attributes (environment, region, pod)
4. Enable auto-instrumentation for HTTP/gRPC clients and servers
5. Add custom spans for recommendation-specific operations

### Auto-Instrumentation Libraries

| Language        | Libraries Auto-Instrumented                        |
|----------------|---------------------------------------------------|
| Python         | Flask, Django, FastAPI, requests, urllib3, gRPC    |
| Java           | Spring, Servlet, JDBC, Kafka, gRPC                 |
| Go             | net/http, gRPC, database/sql                       |
| Node.js        | Express, Fastify, http, grpc, pg                   |
| Rust           | actix-web, hyper, tonic (manual instrumentation)   |

## Trace and Span Propagation

### Span Structure for Recommendation Requests

```
TraceID: abc123def456789012345678
│
├── Span: API Gateway (2ms)
│   ├── SpanID: 001
│   ├── ParentSpanID: null (root span)
│   ├── Attributes: http.method=GET, http.url=/api/v1/recommendations
│   └── Status: OK
│
├── Span: Recommendation Service (42ms)
│   ├── SpanID: 002
│   ├── ParentSpanID: 001
│   ├── Attributes: algorithm=hybrid, model_version=v2.3
│   ├── Event: cache_miss (feature store)
│   └── Status: OK
│
├── Span: Feature Store Query (8ms)
│   ├── SpanID: 003
│   ├── ParentSpanID: 002
│   ├── Attributes: store=redis, feature_set=user_profile
│   └── Status: OK
│
├── Span: Model Inference (25ms)
│   ├── SpanID: 004
│   ├── ParentSpanID: 002
│   ├── Attributes: model=cf_v2, device=GPU, batch_size=1
│   └── Status: OK
│
└── Span: Catalog Lookup (5ms)
    ├── SpanID: 005
    ├── ParentSpanID: 002
    ├── Attributes: items_count=10, source=cache
    └── Status: OK
```

### HTTP Header Propagation

W3C Trace Context format (recommended):

```
Request header:
  traceparent: 00-abc123def456789012345678-0011223344556677-01
               ── ──────────────────────── ──────────────── ──
               v1  Trace ID (16 bytes)     Span ID (8 bytes)  Flags

Optional tracestate header:
  tracestate: rec=algorithm=hybrid,model=v2.3
```

### Kafka Context Propagation

Kafka does not natively support trace context propagation. Solutions:

1. **Message headers**: Embed traceparent in Kafka message headers
2. **Producer interceptor**: Auto-inject trace context on produce
3. **Consumer interceptor**: Auto-extract trace context on consume
4. **Custom propagation**: Include trace_id in message payload (legacy)

```
Kafka Producer Side:
  Headers: {
    "traceparent": "00-abc123-001-01",
    "tracestate": "rec=source=recommendation-service"
  }
  Key: user_pseudonymous_id
  Value: {"event": "item_viewed", "item_id": "item_123"}

Kafka Consumer Side:
  Extract traceparent from headers
  Create child span for consumer processing
  Link span to original producer trace
```

## Sampling Strategies

### Why Sampling Matters

At scale, tracing every request generates enormous data volumes:

- 10,000 requests/second × 5 spans/request = 50,000 spans/second
- At 1KB per span = 50MB/second = 4.3TB/day
- Storage and processing costs are significant

### Sampling Strategies

| Strategy                 | Description                                          | Use Case                      |
|-------------------------|------------------------------------------------------|-------------------------------|
| Always sample           | 100% of traces collected                             | Low-traffic services          |
| Never sample            | 0% of traces collected                               | High-throughput, low-value    |
| Head-based sampling     | Decision made at trace root, propagated to children  | Most common approach          |
| Tail-based sampling     | Decision made after trace completes                  | Error and slow trace capture  |
| Rate limiting           | Sample N traces per second                           | High-traffic services         |
| Adaptive sampling       | Dynamic rate based on traffic volume                 | Variable-traffic services     |

### Recommended Sampling Configuration

| Service              | Strategy              | Rate     | Rationale                              |
|---------------------|----------------------|----------|----------------------------------------|
| API Gateway          | Head-based, probabilistic | 10%  | High traffic, all paths similar        |
| Recommendation API   | Tail-based (errors+slow) | 100% errors, 5% normal | Capture failures always     |
| Model Server         | Head-based, rate-limited | 100/sec | Fixed budget, uniform coverage        |
| Feature Pipeline     | Head-based, probabilistic | 5%   | Batch processing, less critical       |
| Event Processor      | Head-based, probabilistic | 1%    | Very high volume, low per-event value |

### Tail-Based Sampling Configuration

The OpenTelemetry Collector can make sampling decisions after the trace completes:

```
Tail Sampling Processor Rules:
1. Always sample traces with errors (status=ERROR)
2. Always sample traces with latency > 500ms
3. Always sample traces for premium users (attribute: user.tier=premium)
4. Sample 10% of traces with latency > 200ms
5. Sample 5% of all other traces
6. Drop traces with only health-check spans
```

## Trace Analysis for Latency Optimization

### Critical Path Analysis

Use traces to identify the critical path of recommendation requests:

```
Critical Path Analysis (P95 latency):
1. Feature retrieval:     12ms  (24% of total) ← OPTIMIZATION TARGET
2. Model inference:       28ms  (56% of total) ← PRIMARY TARGET
3. Post-processing:        5ms  (10% of total)
4. Network overhead:       5ms  (10% of total)
                          ────
Total P95:               50ms
```

### Latency Breakdown by Component

| Component              | P50    | P95    | P99    | Optimization Strategy                  |
|-----------------------|--------|--------|--------|----------------------------------------|
| API Gateway           | 1ms    | 2ms    | 5ms    | Already optimal                        |
| Auth validation       | 1ms    | 2ms    | 3ms    | Token caching                          |
| Feature retrieval     | 3ms    | 12ms   | 30ms   | Cache warming, pipeline optimization   |
| Model inference       | 15ms   | 28ms   | 60ms   | Model optimization, GPU utilization    |
| Post-processing       | 2ms    | 5ms    | 10ms   | Filter optimization                    |
| Response serialization| 1ms    | 3ms    | 8ms    | Lazy loading, compact format           |

### Span-Based Latency Alerting

Create alerts based on span attributes:
- Alert when model inference span duration > 100ms (P99)
- Alert when feature retrieval span duration > 50ms (P99)
- Alert when total request span duration > 500ms (P99)
- Alert on span error rate > 1% per service

## Jaeger / Grafana Tempo Setup

### Jaeger Architecture

```
Agent (per node)
├── Receives spans from applications (UDP)
├── Batches and forwards to collector
└── Minimal resource footprint

Collector
├── Validates and processes spans
├── Applies sampling policies
├── Writes to storage backend
└── Horizontal scaling supported

Query + UI
├── Trace search and retrieval
├── Dependency graph visualization
└── Latency analysis tools

Storage
├── Elasticsearch (production recommended)
├── Cassandra (alternative)
└── Kafka (buffer for high-throughput)
```

### Grafana Tempo Architecture

Tempo is a lightweight, high-scale trace storage backend:

```
Application → OTLP → Tempo → Grafana
                              ├── TraceQL queries
                              ├── Service graph visualization
                              ├── Exemplar linking (metrics → traces)
                              └── Trace-to-logs correlation
```

**Tempo Advantages**:
- Object storage backend (S3/GCS/minio) — very low cost
- No indexing of trace content — label-based queries only
- Native integration with Grafana
- TraceQL query language similar to PromQL

## Trace-Based Debugging

### Debugging Workflow

1. **Identify the problem**: Alert fires on high latency or error rate
2. **Find representative traces**: Query traces matching the problem pattern
3. **Locate the bottleneck**: Examine span durations along the critical path
4. **Root cause**: Look at span events, attributes, and linked logs
5. **Verify fix**: Confirm new traces show improvement

### Common Debugging Queries

```
Find slow recommendation requests:
  service="recommendation-api" AND duration>500ms AND status!=ERROR

Find failed model inferences:
  service="model-server" AND status=ERROR AND span.name="inference"

Find cold-start requests:
  service="recommendation-api" AND attribute.cache_hit=false

Find requests with feature store timeouts:
  service="feature-store" AND duration>100ms AND status=ERROR
```

## Trace-Context Propagation in Async Processing

### Recommended Message Flow Tracing

```
Synchronous path (API request):
  API Gateway → Recommendation Service → Feature Store → Model Server
  (all spans connected via traceparent header)

Asynchronous path (event processing):
  Recommendation Service → Kafka (traceparent in header)
    → Event Consumer (new span, linked to original trace)
    → Feature Update (new span)
    → Model Retraining Trigger (new span)

Linking strategy:
  - Use trace_id from Kafka header to link consumer span to producer
  - Create a new parent span for the consumer's processing chain
  - Store original trace_id as attribute on consumer span
```
