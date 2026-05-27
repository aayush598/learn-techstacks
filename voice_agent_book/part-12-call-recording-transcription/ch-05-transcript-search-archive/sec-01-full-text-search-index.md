# Section: Full-Text Search Index

Full-Text Search Index is a core component of the transcript search and archive system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|                   Transcript Search & Archive                     |
+------------------------------------------------------------------+
|                                                                   |
|  Transcript ---> Indexing ---> Search Engine ---> Results        |
|    Stream        Pipeline      (Elasticsearch)    Ranking       |
|                    |                                |            |
|               +----+----+                    +------+------+    |
|               |  Inverted |                  |  BM25 +    |    |
|               |  Index    |                  |  Vector    |    |
|               +-----------+                  +------------+    |
|                                                                   |
|  +----------------------------------------------------------------+
|  |  Filters: Date Range | Speaker | Duration | Keyword | Tags
+------------------------------------------------------------------+
```

## Design Decisions

**Scalable architecture.** The system is designed with horizontal scalability in mind. Each component can be independently scaled based on load, and data partitioning follows the organization ID to maintain tenant isolation.

**Latency versus accuracy trade-off.** Real-time processing paths favor low latency with approximate results, while post-call batch processing delivers higher accuracy. The system supports both modes with configurable thresholds.

**Failure isolation.** Components communicate through asynchronous message queues with dead-letter handling. If any downstream service fails, the pipeline buffers data and retries with exponential backoff, ensuring no data loss.

**Provider abstraction.** External dependencies (STT, LLM, embedding models, translation services) are accessed through provider abstraction layers. This allows swapping providers without affecting the core pipeline logic and enables multi-provider fallback chains.


**Index type selection guide.** HNSW (Hierarchical Navigable Small World) provides faster query performance and higher recall at the cost of slower index builds and higher memory usage. IVFFlat (Inverted File with Flat Compression) builds faster and uses less memory but requires careful tuning of the `lists` and `probes` parameters. The system automatically recommends the optimal index type based on dataset size, query latency requirements, and update frequency. For datasets under 100K vectors, IVFFlat is usually sufficient; above 1M, HNSW is preferred.
## 
## Pseudo-code

```typescript
interface SearchIndex {
  id: string;
  callId: string;
  organizationId: string;
  transcript: string;
  speakers: SpeakerSegment[];
  metadata: TranscriptMetadata;
  embeddings: number[];
  createdAt: Date;
}

interface SearchQuery {
  text: string;
  filters?: SearchFilters;
  sort?: SearchSort;
  pagination: PaginationParams;
}

interface SearchResult {
  transcript: SearchIndex;
  score: number;
  highlights: HighlightRange[];
}

interface SearchService {
  index(transcript: ProcessedTranscript): Promise<void>;
  search(query: SearchQuery): Promise<PaginatedResults<SearchResult>>;
  delete(callId: string): Promise<void>;
}
```

## Open-Source Tools

- **Elasticsearch** (Apache 2.0) — Full-text search and analytics engine
- **Meilisearch** (MIT) — Lightweight search engine with typo tolerance
- **Tantivy** (MIT) — Full-text search engine library written in Rust
- **Typesense** (GPL 3.0) — Typo-tolerant search engine

## Integration Points

The search service integrates with the transcription engine (receives completed transcripts), the archive storage (reads stored transcripts), the web application (serves search results), and the analytics system (tracks query patterns). It exposes a RESTful search API with faceted filtering and pagination.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- Index sharding strategy based on organization ID for tenant isolation
- Search index refresh interval tuning for near-real-time vs. batch trade-offs
- Query timeout and result window limits to prevent resource exhaustion
