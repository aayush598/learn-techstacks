# Request Tracking for Recommendation Systems

## 1. Overview

Request tracking follows a single recommendation request as it traverses multiple services — from the API gateway through feature computation, candidate generation, ranking, and final serving. In a recommendation system, a single request may touch 8–12 microservices, making distributed tracing essential for debugging latency, understanding dependencies, and identifying failures.

### 1.1 Why Request Tracking is Critical

- **Pipeline debugging**: A recommendation request spans feature computation, candidate retrieval, ranking, and post-processing. Without request tracking, identifying which stage failed is guesswork.
- **Latency attribution**: Understanding where time is spent requires per-stage timing.
- **Dependency mapping**: Request tracking reveals which services depend on which.
- **Anomaly detection**: Correlating anomalies across services requires shared request context.

### 1.2 Request Tracking vs. Logging vs. Metrics

| Dimension | Request Tracking | Logging | Metrics |
|---|---|---|---|
| Granularity | Per-request | Per-event | Aggregated |
| Data model | Directed acyclic graph (trace) | Text/structured events | Time-series numbers |
| Storage | Moderate (sampled) | High (all events) | Low |
| Query model | "Show me this request" | "Show me all errors" | "What's the error rate?" |
| Primary use | Debugging, bottleneck ID | Root cause analysis | Trending, alerting |

---

## 2. Correlation ID Propagation

### 2.1 The Correlation Hierarchy

Every recommendation request generates a hierarchy of identifiers:

```
Trace ID (global unique, one per end-to-end request)
  Span: API Gateway to Rec Service (parent span)
    Span: Rec Service to Feature Service (child span)
      Span: Feature Service to Feature Store (leaf span)
      Span: Feature Service to Feature Transform (leaf span)
    Span: Rec Service to Candidate Service (child span)
      Span: Candidate Service to ANN Index (leaf span)
      Span: Candidate Service to Content Filter (leaf span)
    Span: Rec Service to Ranking Service (child span)
      Span: Ranking Service to Model Server (leaf span)
      Span: Ranking Service to Re-ranker (leaf span)
    Span: Rec Service to Response (leaf span)
```

### 2.2 Correlation ID Types

| ID Type | Scope | Lifetime | Format |
|---|---|---|---|
| Trace ID | Entire request | Request lifetime | 128-bit hex (W3C) |
| Span ID | Single operation | Operation lifetime | 64-bit hex (W3C) |
| Request ID | API request | Request lifetime | UUID v4 |
| User ID | User session | User lifetime | Opaque string |
| Session ID | Browsing session | Session lifetime | UUID v4 |
| Idempotency Key | Deduplication | Request lifetime | UUID v4 |

### 2.3 Propagation Mechanisms

**HTTP headers (synchronous calls):**

```
traceparent: 00-abc123def456789-7890123456789012-01
tracestate: rec_user_id=user123,test_group=exp_a
x-request-id: req-uuid-001
x-idempotency-key: idem-uuid-001
```

**gRPC metadata:**

```
grpc-trace-bin: <binary trace context>
x-request-id: req-uuid-001
```

**Kafka message headers (asynchronous):**

```
Headers:
  traceparent: 00-abc123def456789-7890123456789012-01
  x-request-id: req-uuid-001
  x-correlation-id: corr-uuid-001
  x-producer-service: ranking-service
```

**Message queue attributes (SQS/SNS):**

```json
{
  "MessageAttributes": {
    "traceparent": {"DataType": "String", "StringValue": "00-abc123..."},
    "request_id": {"DataType": "String", "StringValue": "req-uuid-001"}
  }
}
```

### 2.4 Propagation Challenges

| Challenge | Solution |
|---|---|
| Service mesh injection (Istio/Linkerd) | Use native trace context propagation |
| Async boundaries (Kafka, SQS) | Manually attach and extract trace context |
| Third-party APIs | Generate new trace, link via request_id |
| Browser to Backend | Inject traceparent via initial API call |
| Lambda/Serverless | Use X-Ray SDK or OpenTelemetry Lambda extension |
| Thread pool handoff | Use context propagation libraries |

---

## 3. W3C Trace Context Standard

### 3.1 Traceparent Header Format

```
traceparent: 00-{trace-id}-{parent-id}-{trace-flags}

Example:
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01

Where:
- 00: Version (always 00)
- 0af7651916cd43dd8448eb211c80319c: 128-bit trace ID
- b7ad6b7169203331: 64-bit parent span ID
- 01: Trace flags (01 = sampled)
```

### 3.2 Tracestate Header

```
tracestate: rojo=00f067aa0ba902b7,congo=t61rcWkgMzE

Where:
- Key-value pairs for vendor-specific data
- Recommendation system can add: rec_user_id, test_group, model_version
```

### 3.3 OpenTelemetry Integration

```python
# Pseudocode for OpenTelemetry propagation
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

# Inject trace context into outgoing request headers
headers = {}
inject(headers)

# Extract trace context from incoming request headers
context = extract(request.headers)

# Create child span within extracted context
with tracer.start_as_current_span("ranking_service", context=context) as span:
    span.set_attribute("model", "ranking-v3")
    span.set_attribute("num_candidates", len(candidates))
```

### 3.4 Trace Context in Service Mesh

Service meshes (Istio, Linkerd) automatically inject trace context:

- **Istio**: Uses Envoy filter to inject/extract traceparent header
- **Linkerd**: Uses linkerd-proxy sidecar for automatic propagation
- **No code changes required** for HTTP/gRPC calls within the mesh
- **Manual propagation needed** for Kafka, SQS, and external APIs

---

## 4. Request Flow Visualization

### 4.1 Trace Visualization

A single recommendation request trace displayed as a waterfall:

```
Service           0ms    20ms    40ms    60ms    80ms   100ms   120ms   140ms   160ms
api-gateway       |========================================================|
rec-service            |=====|
feature-service             |=======|
  feature-store-query       |=====|
  feature-transform               |===|
candidate-service                         |=====================|
  ann-index-search                         |===============|
  content-filter                                |=========|
ranking-service                                                      |================|
  model-inference                                                      |==========|
  re-ranker                                                                |====|
serialization                                                                    |==|
```

### 4.2 Span Attributes for Recommendation Systems

Every span should carry domain-specific attributes:

```
rec.trace.service: "ranking-service"
rec.trace.model.name: "ranking-v3"
rec.trace.model.version: "2026.08.15-rc3"
rec.trace.num_candidates: 5000
rec.trace.num_served: 50
rec.trace.page_type: "homepage"
rec.trace.user.segment: "power_user"
rec.trace.ab.test.group: "rec_v3_shuffled"
rec.trace.feature.completeness: 0.98
rec.trace.cache.hit: true
```

### 4.3 Request Flow for Recommendation Pipeline

Standard flow for a homepage recommendation request:

```
1. Client sends GET /api/recommendations to API Gateway
2. API Gateway creates root span, forwards to Rec Service
3. Rec Service creates child spans for each stage:
   a. Feature Service: Fetch user features + context features
   b. Candidate Service: Retrieve candidate items from multiple sources
   c. Ranking Service: Score candidates with ML model
   d. Post-processing: Apply business rules, diversity, dedup
4. Rec Service returns response, API Gateway forwards to client
5. Each service records timing, attributes, and status
```

---

## 5. Sampling Strategies

### 5.1 Head-Based Sampling

Decision made at trace creation (first service in the chain):

| Strategy | Rate | Use Case |
|---|---|---|
| Fixed rate | 1% of all traces | Baseline sampling |
| Error Always | 100% of error traces | Never miss failures |
| Slow Always | 100% of traces > 500ms | Latency debugging |
| High-value user | 100% for premium users | Business-critical debugging |
| New model | 100% for first hour after deploy | Deploy monitoring |

**Advantages:** Simple, predictable storage requirements.
**Disadvantages:** Cannot retroactively capture interesting events that were not sampled.

### 5.2 Tail-Based Sampling

Decision made after the full trace is collected at a central collector:

**Key criteria for tail-based sampling:**
- **Error presence**: Always retain traces with errors or exceptions
- **Latency threshold**: Retain traces exceeding P99 latency
- **Anomaly detection**: Use statistical methods to identify unusual traces
- **Business rules**: Retain traces for specific user segments or request types

**Architecture:**

```
Services -> Head sampling (10%) -> Collector -> Tail sampling -> Storage
                                       |
                                  Full trace buffer
                                  (100% for 30s)
                                       |
                                  Decision engine
                                  (error? slow? anomalous?)
```

**Tradeoff:** Requires buffering full traces at the collector, increasing memory usage.

### 5.3 Adaptive Sampling

Adjust sampling rates based on traffic volume:

```
if current_rps > 10000:
    sample_rate = 0.01  # 1%
elif current_rps > 1000:
    sample_rate = 0.05  # 5%
elif current_rps > 100:
    sample_rate = 0.10  # 10%
else:
    sample_rate = 1.00  # 100%
```

This ensures consistent trace volume regardless of traffic patterns.

### 5.4 Sampling for Recommendation Systems

| Request Type | Sampling Rate | Rationale |
|---|---|---|
| Homepage recommendations | 1–5% | High volume, stable latency |
| Search recommendations | 5–10% | Moderate volume, variable latency |
| Product detail recommendations | 10–20% | Lower volume, important for debugging |
| Cold-start requests | 100% | Critical for model quality analysis |
| A/B test requests | 50–100% | Statistical validity |
| Error responses | 100% | Always capture failures |
| Slow responses (> 500ms) | 100% | Latency debugging |

---

## 6. Trace Storage Backends

### 6.1 Backend Comparison

| Backend | Query Model | Retention | Cost | Best For |
|---|---|---|---|---|
| Jaeger | Trace search by ID, tags | 7–30 days | Medium | Self-hosted, Kubernetes |
| Zipkin | Trace search by ID, tags | 7–14 days | Low | Lightweight, simple |
| Tempo (Grafana) | TraceQL (LogQL-like) | 30+ days | Low | Grafana ecosystem |
| AWS X-Ray | Service map, trace search | 30 days | Pay-per-trace | AWS-native |
| Honeycomb | BubbleUp, trace search | 60+ days | High | Advanced debugging |
| ClickHouse-based | SQL on trace data | Custom | Low-Medium | Analytics on traces |

### 6.2 Trace Data Model

Standard OpenTelemetry trace data model:

```
Trace:
  trace_id: 128-bit unique identifier
  spans:
    - span_id: 64-bit unique identifier
      parent_span_id: 64-bit (null for root)
      operation_name: "ranking_service"
      service_name: "ranking-service"
      start_time: nanosecond timestamp
      duration: nanoseconds
      status: {code: OK|ERROR|UNSET, message: "..."}
      attributes: {key: value, ...}
      events: [{name, timestamp, attributes}, ...]
      links: [{trace_id, span_id, attributes}, ...]
```

### 6.3 Trace Retention Strategy

| Age | Retention | Access Pattern | Storage |
|---|---|---|---|
| 0–24 hours | 100% of traces | Real-time debugging | Hot (SSD) |
| 1–7 days | 100% of sampled traces | Recent incident investigation | Warm (HDD) |
| 7–30 days | 10% of traces (errors always retained) | Historical analysis | Cold (object storage) |
| 30–365 days | 1% of traces (errors and slow retained) | Compliance, trend analysis | Archive |

---

## 7. Distributed Tracing in Recommendation Systems

### 7.1 Challenge: Cross-Service Correlation

A single recommendation request touches many services. The trace must capture:

1. **Synchronous calls**: HTTP/gRPC between services (automatic propagation)
2. **Asynchronous calls**: Kafka messages, background jobs (manual propagation)
3. **Database queries**: Feature store, model store (add as span attributes)
4. **Cache operations**: Redis, Memcached (record as span events)
5. **External calls**: Third-party APIs, ML model serving (propagate or create linked trace)

### 7.2 Trace Enrichment

Add domain-specific information to spans for richer debugging:

```
Span: ranking-service
  Attributes:
    rec.model.name: "ranking-v3"
    rec.model.version: "2026.08.15-rc3"
    rec.num_candidates: 5000
    rec.num_features: 127
    rec.feature_completeness: 0.98
    rec.prediction_scores: [0.92, 0.87, 0.81, 0.76, 0.71]
    rec.cache.hit: true
    rec.ab.test.group: "rec_v3_shuffled"
    rec.page_type: "homepage"
    rec.user.segment: "power_user"
```

### 7.3 Trace-Based Debugging Workflow

1. **Alert fires**: P99 latency exceeded for ranking service
2. **Find slow traces**: Query traces by service and duration
3. **Analyze trace waterfall**: Identify which span is slow
4. **Compare with baseline**: Compare slow trace against typical trace
5. **Check attributes**: Look for unusual attribute values (cold-start, cache miss, fallback)
6. **Correlate with logs**: Use trace_id to find corresponding log entries
7. **Correlate with metrics**: Check metrics for the time window of the slow trace

---

## 8. Implementation Checklist

- [ ] Adopt OpenTelemetry SDK for all services
- [ ] Implement W3C trace context propagation across all call types
- [ ] Configure sampling strategy (head-based + tail-based)
- [ ] Deploy trace storage backend (Jaeger, Tempo, or X-Ray)
- [ ] Add domain-specific span attributes to all services
- [ ] Create trace-based dashboards (latency waterfall, service map)
- [ ] Set up trace-based alerting (slow traces, error traces)
- [ ] Integrate trace_id with log aggregation (trace-to-log correlation)
- [ ] Document trace propagation for async boundaries
- [ ] Test trace propagation across all service boundaries

---

## 9. Key Takeaways

1. **Propagate trace context** across all service boundaries (sync and async)
2. **Use W3C Trace Context** standard for vendor-neutral propagation
3. **Implement head-based + tail-based sampling** to balance cost and visibility
4. **Enrich spans with domain attributes** (model name, num_candidates, page_type)
5. **Always retain error traces** at 100% sampling rate
6. **Integrate traces with logs** via trace_id correlation
7. **Use service maps** for dependency visualization and impact analysis
8. **Sample cold-start and A/B test requests** at higher rates for debugging
