# Section: Objection Detection

Objection Detection is a core component of the call highlight extraction system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|                   Call Highlight Extraction                       |
+------------------------------------------------------------------+
|                                                                   |
|  Transcript ---> Analysis ---> Highlight ---> Export             |
|    Stream        Pipeline       Generator     Formatter          |
|                    |                               |              |
|  +----+----+  +----+----+                  +------+------+      |
|  |Sentiment|  | Action  |                  |  Summary   |      |
|  |Analysis |  | Item    |                  |  Timeline  |      |
|  +----------+  | Detect  |                  +------------+      |
|                +---------+                                       |
|  Criteria: Sentiment Shift | Action Phrase | Objection Pattern   |
+------------------------------------------------------------------+
```

## Design Decisions

**Scalable architecture.** The system is designed with horizontal scalability in mind. Each component can be independently scaled based on load, and data partitioning follows the organization ID to maintain tenant isolation.

**Latency versus accuracy trade-off.** Real-time processing paths favor low latency with approximate results, while post-call batch processing delivers higher accuracy. The system supports both modes with configurable thresholds.

**Failure isolation.** Components communicate through asynchronous message queues with dead-letter handling. If any downstream service fails, the pipeline buffers data and retries with exponential backoff, ensuring no data loss.

**Provider abstraction.** External dependencies (STT, LLM, embedding models, translation services) are accessed through provider abstraction layers. This allows swapping providers without affecting the core pipeline logic and enables multi-provider fallback chains.


**Composite highlight scoring.** Highlights are scored using a weighted combination of multiple signals: sentiment intensity (magnitude of positive/negative shift), keyword density (presence of action or objection trigger words), transcription confidence (model certainty), and duration (length of the highlighted segment). The composite score normalizes these signals into a 0-1 range, with configurable weights per customer vertical.
## 
## Pseudo-code

```typescript
interface ServiceConfig {
  id: string;
  name: string;
  enabled: boolean;
  options: Record<string, unknown>;
}

interface ProcessResult {
  id: string;
  status: 'SUCCESS' | 'FAILURE' | 'PARTIAL';
  data: Record<string, unknown>;
  errors: string[];
  processingTimeMs: number;
}

interface ServiceProvider {
  initialize(config: ServiceConfig): Promise<void>;
  process(input: unknown): Promise<ProcessResult>;
  healthCheck(): Promise<HealthStatus>;
}
```



**Real-time objection alerting.** When an objection is detected with high confidence, the system can trigger real-time alerts to supervisors or sales managers, enabling live coaching interventions. The alert includes the objection type, the surrounding context, and suggested response scripts from the knowledge base.

## Open-Source Tools

- **Prometheus** (Apache 2.0) — Metrics collection and monitoring
- **Grafana** (AGPL 3.0) — Dashboard and visualization
- **OpenTelemetry** (Apache 2.0) — Distributed tracing and observability
- **Docker** (Apache 2.0) — Containerization and deployment

## Integration Points

This component integrates with upstream data sources, downstream processing pipelines, and external services through well-defined API contracts. Integration points are secured with API keys, rate-limited, and monitored for latency and error rates.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- Timeout and retry configuration for external service calls
- Resource limit enforcement with per-tenant quotas
