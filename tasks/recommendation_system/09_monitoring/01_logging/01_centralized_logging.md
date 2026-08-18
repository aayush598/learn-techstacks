# Centralized Logging Architecture for Recommendation Systems

## Overview

Centralized logging aggregates logs from all recommendation system components — API servers,
model serving endpoints, feature pipelines, event processors, and infrastructure — into a
unified platform for search, analysis, and alerting. This covers ELK Stack vs. Loki+Grafana
trade-offs, structured logging standards, log retention policies, and correlation-based
distributed tracing through logs.

## Why Centralized Logging Matters for Recommendation Systems

Recommendation systems are distributed by nature. A single recommendation request traverses
multiple services:

```
User Request → API Gateway → Recommendation Service → Feature Store
                                    │                       │
                                    ├── Model Server         │
                                    │       │               │
                                    │       ├── Cache        │
                                    │       └── Model Store  │
                                    │                       │
                                    └── Response ←──────────┘

Each component generates logs that must be correlated for debugging:
- API Gateway: request metadata, latency, status
- Recommendation Service: algorithm selection, scoring logic
- Feature Store: feature retrieval, cache hits/misses
- Model Server: inference time, model version, confidence scores
```

Without centralized logging, diagnosing a slow or incorrect recommendation requires manually
inspecting logs across dozens of pods and services.

## ELK Stack vs. Loki + Grafana

### ELK Stack (Elasticsearch, Logstash, Kibana)

**Architecture**:
```
Applications → Logstash (parse/transform) → Elasticsearch (index/store) → Kibana (query/visualize)
```

**Strengths**:
- Full-text search with powerful query DSL
- Structured and unstructured log analysis
- Rich aggregation capabilities for metrics derived from logs
- Mature ecosystem with extensive plugin support
- Production-proven at massive scale

**Weaknesses**:
- High resource consumption (Elasticsearch is memory-intensive)
- Complex operational overhead (cluster management, shard strategy)
- Expensive at scale (requires dedicated Elasticsearch cluster)
- Logstash pipeline adds latency to log ingestion

**When to Choose ELK**:
- Need full-text search across log content
- Complex log analysis and aggregation queries
- Compliance requirements for log search and audit
- Team has Elasticsearch operational expertise

### Loki + Grafana

**Architecture**:
```
Applications → Promtail/Alloy (label/ship) → Loki (index labels only) → Grafana (query/visualize)
```

**Strengths**:
- Significantly lower storage costs (indexes labels, not content)
- Lightweight — uses 10x less memory than Elasticsearch
- Native integration with Prometheus and Grafana ecosystem
- Simple operational model
- LogQL is intuitive for Prometheus users

**Weaknesses**:
- No full-text indexing (content search is regex-based, slower)
- Limited aggregation capabilities compared to Elasticsearch
- Dependent on Grafana for visualization
- Less mature for complex log analysis use cases

**When to Choose Loki**:
- Already using Prometheus + Grafana for metrics
- Cost optimization is a priority
- Logs are primarily used for debugging, not complex analytics
- Team prefers simpler operational footprint

### Comparison Matrix

| Feature                  | ELK Stack                        | Loki + Grafana                   |
|--------------------------|----------------------------------|----------------------------------|
| Storage cost             | High (full-text index)           | Low (label index only)           |
| Query performance        | Fast (inverted index)            | Medium (regex on chunks)         |
| Full-text search         | Excellent                        | Limited                          |
| Operational complexity   | High                             | Low                              |
| Metric extraction        | Excellent (aggregations)         | Basic (via LogQL)                |
| Dashboard integration    | Kibana (separate)                | Native Grafana                   |
| Alerting                 | ElastAlert /Watcher              | Grafana alerting (native)        |
| Scalability              | Proven at petabyte scale         | Proven at terabyte scale         |
| Setup time               | Days to weeks                    | Hours to days                    |

## Structured Logging Standards

### Log Event Schema

Every log line from the recommendation system must be structured JSON:

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "service": "recommendation-api",
  "version": "2.3.1",
  "environment": "production",
  "region": "us-east-1",
  "host": "rec-api-7b4d8f-xk2mn",
  "trace_id": "abc123def456",
  "span_id": "789ghi012jkl",
  "user_id": "usr_a1b2c3d4",
  "session_id": "sess_x1y2z3",
  "request_id": "req_m1n2o3",
  "message": "Recommendation generated successfully",
  "context": {
    "algorithm": "collaborative_filtering",
    "model_version": "v2.3.1",
    "num_candidates": 500,
    "num_final": 10,
    "latency_ms": 45,
    "cache_hit": true
  }
}
```

### Required Fields

| Field          | Type   | Description                                    |
|---------------|--------|------------------------------------------------|
| timestamp     | ISO8601| When the event occurred                        |
| level         | Enum   | DEBUG, INFO, WARN, ERROR, FATAL                |
| service       | String | Name of the service emitting the log           |
| trace_id      | String | Distributed trace ID (OpenTelemetry format)    |
| span_id       | String | Current span within the trace                  |
| request_id    | String | Unique identifier for the current request      |
| message       | String | Human-readable description of the event        |

### Recommended Additional Fields

| Field          | When to Include                                  |
|---------------|--------------------------------------------------|
| user_id       | When processing a user request (pseudonymized)   |
| session_id    | When tracking user sessions                       |
| model_version | When model inference is involved                  |
| algorithm     | When multiple algorithms are available            |
| latency_ms    | For performance-sensitive operations              |
| error_code    | For error and warning level logs                  |
| context       | Any additional structured metadata               |

## Log Levels and Their Usage

| Level   | Usage                                                     | Example                                        |
|---------|----------------------------------------------------------|-------------------------------------------------|
| DEBUG   | Development troubleshooting, verbose output               | Feature vector dimensions, intermediate scores  |
| INFO    | Normal operational events, request lifecycle              | Request received, recommendation generated      |
| WARN    | Degraded but functional, needs attention                  | Cache miss, fallback to default features        |
| ERROR   | Operation failed, requires investigation                  | Model inference timeout, feature store down     |
| FATAL   | Critical system failure, immediate action required        | Cannot load model, database unreachable          |

### Level Configuration by Component

| Component          | Default Level | Debug Trigger                    |
|-------------------|---------------|----------------------------------|
| API Gateway        | INFO          | Per-request tracing              |
| Recommendation API | INFO          | Algorithm debugging              |
| Feature Pipeline   | INFO          | Feature computation tracing      |
| Model Server       | INFO          | Inference details                |
| Event Processor    | WARN          | Event schema validation          |
| Batch Jobs         | INFO          | Job progress details             |

## Log Retention Policies

### Tiered Retention Strategy

```
Hot Storage (SSD, fast query):
├── Duration: 7 days
├── Use: Active debugging, real-time alerting
├── Query speed: < 1 second
└── Storage cost: $$$

Warm Storage (HDD, bulk):
├── Duration: 30 days
├── Use: Investigation, pattern analysis
├── Query speed: < 10 seconds
└── Storage cost: $$

Cold Storage (Object storage, archive):
├── Duration: 90 days (or per compliance)
├── Use: Compliance, historical analysis
├── Query speed: Minutes to hours
└── Storage cost: $

Delete:
├── Duration: After cold storage retention
├── Exception: Audit logs retained per compliance
└── Method: Automated lifecycle policy
```

### Retention by Log Category

| Log Category          | Hot    | Warm   | Cold    | Archive |
|----------------------|--------|--------|---------|---------|
| Application logs     | 7 days | 30 days| 90 days | Delete  |
| Access/API logs      | 7 days | 30 days| 90 days | 1 year  |
| Audit logs           | 30 days| 90 days| 1 year  | 7 years |
| Security events      | 30 days| 90 days| 1 year  | 7 years |
| Recommendation logs  | 7 days | 30 days| 90 days | Delete  |
| Model inference logs | 7 days | 14 days| 30 days | Delete  |

## Log-Based Alerting

### Alert Rules for Recommendation Systems

| Alert                        | Condition                                    | Severity |
|------------------------------|----------------------------------------------|----------|
| High error rate              | > 1% ERROR logs in 5-minute window           | Critical |
| Model inference failures     | > 10 ERROR logs from model server in 1 min   | Critical |
| Feature store timeouts       | > 5 WARN logs for feature timeout in 1 min   | Warning  |
| Cold-start spike             | > 20% increase in cold-start logs            | Warning  |
| Anomalous recommendation     | Zero recommendations generated in 5 minutes  | Critical |
| Latency spike                | P99 latency > 500ms derived from logs        | Warning  |

### Alert Fatigue Prevention

- Aggregate similar alerts (e.g., "feature store errors" not per-request alerts)
- Use rate-based conditions, not absolute counts
- Set appropriate evaluation windows (5-minute minimum)
- Implement alert grouping and deduplication
- Review and tune alert thresholds monthly based on false positive rates

## Correlation IDs for Distributed Tracing

### Trace Propagation Through Services

```
Request arrives at API Gateway:
  trace_id = generate-or-extract-from-header()
  span_id = generate()

Pass to Recommendation Service:
  Headers: traceparent: 00-{trace_id}-{span_id}-01

Pass to Feature Store:
  Headers: traceparent: 00-{trace_id}-{new_span_id}-01

Pass to Model Server:
  Headers: traceparent: 00-{trace_id}-{newer_span_id}-01

All logs from all services share the same trace_id.
Filter logs by trace_id to reconstruct the full request journey.
```

### Correlation ID Best Practices

1. Generate trace ID at the edge (API gateway) for external requests
2. Propagate trace ID in HTTP headers (W3C Trace Context format)
3. Include trace ID in every log line automatically (middleware/interceptor)
4. Store trace ID in Kafka message headers for async processing
5. Use trace ID as the primary debugging tool for customer-reported issues

## Log Analysis for Debugging

### Common Debugging Workflows

**Slow Recommendation Request**:
1. Filter logs by request_id
2. Find the slowest span in the trace
3. Examine that span's context (which service, what operation)
4. Check for errors or warnings within the slow span
5. Compare latency breakdown against baseline

**Incorrect Recommendation**:
1. Filter logs by user_id and timestamp
2. Examine feature values used for the request
3. Check model version and inference output
4. Compare with expected behavior based on user history
5. Trace the scoring and ranking pipeline

**Intermittent Failures**:
1. Filter logs by error level in affected time window
2. Identify common pattern (same user, same item, same service)
3. Check dependent service health during failure window
4. Examine infrastructure metrics (CPU, memory, network) during failures
5. Look for correlation with deployments or configuration changes
