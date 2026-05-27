# Section: Document Metadata Extraction

Document Metadata Extraction is a core component of the document ingestion system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|                   Document Ingestion Pipeline                    |
+------------------------------------------------------------------+
|                                                                   |
|  Upload ---> Queue ---> Parser ---> Processor ---> Store        |
|   |                    |          |              |               |
|  ++--------+     +-----+----+  +--+------+   +--+--------+      |
|  |  Web UI |     |  Rabbit  |  | OCR     |   |  Vector   |      |
|  |  API    |     |  /SQS    |  | Markdown|   |  Store    |      |
|  |  S3     |     |  Pub/Sub |  | HTML    |   |  Object   |      |
|  +---------+     +----------+  | JSON    |   |  Store    |      |
|                                +---------+   +-----------+      |
+------------------------------------------------------------------+
```

## Design Decisions

**Scalable architecture.** The system is designed with horizontal scalability in mind. Each component can be independently scaled based on load, and data partitioning follows the organization ID to maintain tenant isolation.

**Latency versus accuracy trade-off.** Real-time processing paths favor low latency with approximate results, while post-call batch processing delivers higher accuracy. The system supports both modes with configurable thresholds.

**Failure isolation.** Components communicate through asynchronous message queues with dead-letter handling. If any downstream service fails, the pipeline buffers data and retries with exponential backoff, ensuring no data loss.

**Provider abstraction.** External dependencies (STT, LLM, embedding models, translation services) are accessed through provider abstraction layers. This allows swapping providers without affecting the core pipeline logic and enables multi-provider fallback chains.

## Pseudo-code

```typescript
interface HighlightCriteria {
  id: string;
  name: string;
  type: 'SENTIMENT_SHIFT' | 'ACTION_ITEM' | 'OBJECTION' | 'KEYWORD_TRIGGER' | 'TRANSCRIPTION_CONFIDENCE';
  config: Record<string, unknown>;
  priority: number;
}

interface CallHighlight {
  id: string;
  callId: string;
  type: HighlightCriteria['type'];
  startTime: number;
  endTime: number;
  text: string;
  score: number;
  metadata: HighlightMetadata;
  createdAt: Date;
}

interface HighlightSummary {
  callId: string;
  highlights: CallHighlight[];
  summary: string;
  actionItems: ActionItem[];
  sentiment: SentimentAnalysis;
  timeline: TimelineEntry[];
}

interface HighlightExtractor {
  analyze(call: CallTranscript): Promise<CallHighlight[]>;
  generateSummary(highlights: CallHighlight[]): Promise<string>;
  formatExport(highlights: CallHighlight[], format: ExportFormat): Promise<Buffer>;
}
```

## Open-Source Tools

- **HuggingFace Transformers** (Apache 2.0) — Sentiment analysis and text classification
- **spaCy TextCategorizer** (MIT) — Custom text classifier for action item detection
- **Sumy** (MIT) — Text summarization library for highlight generation
- **vaderSentiment** (MIT) — Rule-based sentiment analysis engine

## Integration Points

The ingestion system integrates with the document upload interface (web UI and API), the file storage (S3/MinIO for raw files), the chunking service (splits documents), the embedding service (generates vectors), and the monitoring system (tracks ingestion metrics). It exposes a REST API for document management and hooks for post-processing pipelines.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- Dead letter queue for failed documents with manual reprocessing UI
- Ingestion pipeline backpressure with configurable concurrency limits
- Document size limits with pre-processing validation
