# Section: Alert Routing for Keyword Hits

Alert Routing for Keyword Hits is a core component of the keyword and phrase spotting system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|                   Keyword & Phrase Spotting                       |
+------------------------------------------------------------------+
|                                                                   |
|  Transcript ---> Keyword Matcher ---> Hit Handler ---> Alert     |
|    Stream        Engine               Router          System    |
|                    |                    |                        |
|  +----+----+  +----+----+        +------+------+                |
|  | Catalog  |  |  Aho-   |        |  Webhook  |                |
|  | Manager  |  | Corasick|        |  /Slack   |                |
|  +----------+  +---------+        +------------+                |
|                                                                   |
|  Features: Exact | Fuzzy | Regex | Proximity | Negation          |
+------------------------------------------------------------------+
```

## Design Decisions

**Scalable architecture.** The system is designed with horizontal scalability in mind. Each component can be independently scaled based on load, and data partitioning follows the organization ID to maintain tenant isolation.

**Latency versus accuracy trade-off.** Real-time processing paths favor low latency with approximate results, while post-call batch processing delivers higher accuracy. The system supports both modes with configurable thresholds.

**Failure isolation.** Components communicate through asynchronous message queues with dead-letter handling. If any downstream service fails, the pipeline buffers data and retries with exponential backoff, ensuring no data loss.

**Provider abstraction.** External dependencies (STT, LLM, embedding models, translation services) are accessed through provider abstraction layers. This allows swapping providers without affecting the core pipeline logic and enables multi-provider fallback chains.

## Pseudo-code

```typescript
interface KeywordEntry {
  id: string;
  phrase: string;
  matchType: 'EXACT' | 'FUZZY' | 'REGEX' | 'PROXIMITY';
  caseSensitive: boolean;
  proximityWords?: number;
  threshold: number;
  category: string;
  alertWebhook?: string;
  enabled: boolean;
}

interface KeywordMatch {
  keywordId: string;
  phrase: string;
  transcriptId: string;
  callId: string;
  matchPosition: { start: number; end: number };
  matchTimestamp: number;
  confidence: number;
  context: string;
}

interface KeywordCatalog {
  id: string;
  name: string;
  description: string;
  keywords: KeywordEntry[];
  version: number;
  updatedAt: Date;
}

interface KeywordSpotterService {
  loadCatalog(catalog: KeywordCatalog): Promise<void>;
  processChunk(text: string, callContext: CallContext): Promise<KeywordMatch[]>;
  handleAlert(match: KeywordMatch): Promise<void>;
}
```

## Open-Source Tools

- **Aho-Corasick Automaton** (MIT) — Multi-pattern string matching algorithm
- **Flask/Express webhook** (MIT) — Webhook receiver for keyword alerts
- **Redis** (MIT) — In-memory cache for keyword catalog
- **Hyperscan** (BSD 3-Clause) — High-performance regex matching library

## Integration Points

The keyword spotter integrates with the real-time transcription engine (receives streaming text chunks), the alerting system (Slack/PagerDuty webhooks), the catalog management API (CRUD operations), and the post-call analytics pipeline (batch processing). It exposes a WebSocket stream for live keyword hits and a REST API for catalog management.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- Keyword catalog size limits with performance degradation monitoring
- Deduplication of repeated keyword matches within a single call
- Alert throttling with configurable cooldown periods
