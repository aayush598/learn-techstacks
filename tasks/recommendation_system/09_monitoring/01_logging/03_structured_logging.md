# Structured Logging for Recommendation Systems

## 1. Why Structured Logging

### 1.1 Benefits Over Unstructured Logs
- **Machine Readable**: JSON format enables automated parsing and querying
- **Consistent Schema**: Standardized fields across all services
- **Queryable**: Filter by any field (user_id, model_version, latency)
- **Correlatable**: Trace requests across services via correlation IDs
- **Analyzable**: Aggregate metrics directly from logs

### 1.2 Standard Log Format
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "service": "ranking-service",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user_123",
  "message": "Ranking completed",
  "metadata": {
    "model_version": "v4.2.1",
    "candidates_scored": 500,
    "latency_ms": 85,
    "experiment_id": "exp_456"
  }
}
```

---

## 2. Standardized Fields

### 2.1 Required Fields
- **timestamp**: ISO 8601 format with timezone
- **level**: ERROR, WARN, INFO, DEBUG, TRACE
- **service**: Service name (ranking-service, feature-store, etc.)
- **message**: Human-readable description

### 2.2 Context Fields
- **trace_id**: Distributed trace identifier (W3C format)
- **span_id**: Current span identifier
- **user_id**: User identifier (if applicable)
- **request_id**: Unique request identifier
- **session_id**: User session identifier

### 2.3 ML-Specific Fields
- **model_version**: Active model version
- **model_name**: Model identifier
- **inference_latency_ms**: Model inference time
- **prediction_confidence**: Model confidence score
- **feature_freshness_ms**: Age of features used

### 2.4 Recommendation-Specific Fields
- **recommendation_id**: Unique recommendation identifier
- **item_ids**: List of recommended items
- **scores**: Prediction scores
- **experiment_id**: A/B test identifier
- **variant**: Experiment variant assignment

---

## 3. Log Levels

### 3.1 Level Usage Guidelines
| Level | Usage | Example |
|---|---|---|
| ERROR | System errors requiring attention | Model serving failure, feature store timeout |
| WARN | Potential issues to monitor | High latency, fallback triggered, feature staleness |
| INFO | Normal operational events | Request served, model loaded, feature updated |
| DEBUG | Detailed diagnostic information | Feature values, model inputs, intermediate scores |
| TRACE | Very detailed tracing | Full request/response payload, all intermediate steps |

### 3.2 Dynamic Log Levels
- Increase log level temporarily for debugging specific issues
- Per-service log level configuration
- Log level overrides via API for production debugging
- Automatic level adjustment based on error rate

---

## 4. Correlation IDs

### 4.1 Propagation
- Generate correlation ID at API gateway
- Propagate via HTTP headers (X-Request-ID, X-Correlation-ID)
- Propagate via Kafka message headers
- Include in all log entries for the request

### 4.2 Usage
- **Request Tracing**: Follow a single request through all services
- **Debugging**: Find all logs related to a problematic request
- **Performance Analysis**: Trace latency across service boundaries
- **Audit Trail**: Complete record of request processing

---

## 5. Log Enrichment

### 5.1 Enrichment Pipeline
```
Raw Log → Enrichment Agent → Enriched Log
  - Add Kubernetes metadata (pod, node, namespace)
  - Add service version
  - Add environment (production, staging)
  - Add geographic location (from IP)
  - Add business context (user tier, subscription)
```

### 5.2 Enrichment Tools
- **Fluentd**: Filter plugins for enrichment
- **Logstash**: Mutate/filter plugins
- **OpenTelemetry Collector**: Resource detection, attribute enrichment

---

## 6. Best Practices for ML Services

### 6.1 What to Log
- Model inference requests (input features summary, not full vectors)
- Prediction results (scores, rankings)
- Model loading and unloading events
- Feature computation timing
- Training metrics during online learning
- A/B test assignment decisions

### 6.2 What NOT to Log
- Full user data (PII concerns)
- Full model parameters (security concerns)
- Complete feature vectors (too large)
- Every prediction score (too verbose)
- Secrets or credentials

### 6.3 Performance Considerations
- Async logging to avoid blocking request processing
- Buffer logs and batch ship
- Use structured logging over string formatting
- Log sampling for high-volume endpoints
