# Section: Speaker Embedding Extraction

Speaker Embedding Extraction is a core component of the speaker diarization system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|                   Speaker Diarization Pipeline                    |
+------------------------------------------------------------------+
|                                                                   |
|  Audio In ---> VAD ---> Embedding ---> Clustering ---> Speaker   |
|                  |         Extractor        |            Labels   |
|             +----+----+            +--------+--------+            |
|             |  Voice  |            |   Spectral    |            |
|             | Active  |            |  Clustering   |            |
|             | Detect  |            |  (AHC/SC)     |            |
|             +---------+            +---------------+            |
|                                                                   |
|  +----------------------------------------------------------------+
|  |  Speaker Turn Timeline
|  +---> Speaker A: 0:00-1:23  "Hello, this is Alice..."
|       Speaker B: 1:23-3:45  "Hi Alice, this is Bob..."
|       Speaker A: 3:45-5:10  "Let me explain our product..."
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

- **pyannote-audio** (MIT) — Speaker diarization pipeline
- **SpeechBrain** (Apache 2.0) — Speaker recognition and embedding
- **WeSpeaker** (Apache 2.0) — Speaker diarization toolkit
- **ECAPA-TDNN** (MIT) — Speaker embedding extraction model

## Integration Points

The diarization system integrates with the transcription engine (receives recognized text segments), the audio recording pipeline (access to raw audio), the speaker profile database (registration and lookup), and the transcript archive (annotated diarized transcripts). It exposes a gRPC API for real-time speaker tracking and a REST API for batch processing.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- GPU memory management for embedding models with dynamic batching
- Fallback to channel-based diarization when clustering confidence is low
- Periodic model reloading to capture updated speaker profiles
