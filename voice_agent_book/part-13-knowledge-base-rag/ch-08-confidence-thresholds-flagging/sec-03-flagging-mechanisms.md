# Section: Flagging Mechanisms

Flagging Mechanisms is a core component of the confidence thresholds and flagging system. This section examines its architecture, implementation, and operational considerations.

## System Architecture

```
+------------------------------------------------------------------+
|              Confidence Thresholds & Flagging                    |
+------------------------------------------------------------------+
|                                                                   |
|  Answer ---> Confidence ---> Threshold ---> Flag/Pass            |
|               Scorer        Check          |                     |
|                               |      +-----+-----+               |
|                          +----+----+ |   Human    |              |
|                          |  High   | |   Review   |              |
|                          |  Pass   | |   Queue    |              |
|                          +---------+ +-----------+               |
|                                                                   |
|  Thresholds: 0.0-0.3: Reject | 0.3-0.7: Flag | 0.7-1.0: Pass    |
+------------------------------------------------------------------+
```

## Design Decisions

**Scalable architecture.** The system is designed with horizontal scalability in mind. Each component can be independently scaled based on load, and data partitioning follows the organization ID to maintain tenant isolation.

**Latency versus accuracy trade-off.** Real-time processing paths favor low latency with approximate results, while post-call batch processing delivers higher accuracy. The system supports both modes with configurable thresholds.

**Failure isolation.** Components communicate through asynchronous message queues with dead-letter handling. If any downstream service fails, the pipeline buffers data and retries with exponential backoff, ensuring no data loss.

**Provider abstraction.** External dependencies (STT, LLM, embedding models, translation services) are accessed through provider abstraction layers. This allows swapping providers without affecting the core pipeline logic and enables multi-provider fallback chains.

## Pseudo-code

```typescript
interface ConfidenceScore {
  overall: number;
  components: {
    retrievalRelevance: number;
    answerCoherence: number;
    factualConsistency: number;
    sourceFreshness: number;
  };
  modelConfidence: number;
}

interface ThresholdConfig {
  id: string;
  name: string;
  domain: string;
  passThreshold: number;
  flagThreshold: number;
  rejectThreshold: number;
  autoPassEnabled: boolean;
  requireHumanReview: boolean;
  notifyOnFlag: boolean;
}

interface FlaggedItem {
  id: string;
  query: string;
  answer: string;
  confidence: ConfidenceScore;
  thresholdConfig: ThresholdConfig;
  flagReason: FlagReason[];
  status: 'OPEN' | 'IN_REVIEW' | 'RESOLVED' | 'DISMISSED';
  assignedTo?: string;
  createdAt: Date;
}

interface FlaggingService {
  evaluate(query: string, answer: string): Promise<FlaggedItem | null>;
  review(itemId: string, decision: ReviewDecision): Promise<void>;
  updateThreshold(config: ThresholdConfig): Promise<void>;
  getFlaggedItems(filter: FlagFilter): Promise<FlaggedItem[]>;
}
```

## Open-Source Tools

- **OpenAI Evals** (MIT) — LLM output evaluation and confidence measurement
- **Ragas** (Apache 2.0) — RAG evaluation framework for confidence scoring
- **Trulens** (Apache 2.0) — LLM app evaluation and tracking
- **LangSmith** (Proprietary) — LLM observability and evaluation platform

## Integration Points

The flagging system integrates with the RAG pipeline (receives query-answer pairs), the human review dashboard (displays flagged items), the feedback loop (incorporates reviewer corrections), and the notification service (alerts on critical flags). It exposes a configuration API for threshold management and a review API for workflow handling.

## Production Considerations

- Prometheus metrics for all pipeline stages with latency histograms
- Graceful degradation under load with circuit breaker pattern
- Comprehensive structured logging with correlation IDs
- Health check endpoints for Kubernetes liveness and readiness probes
- Rate limiting and request throttling for API endpoints
- Backpressure handling with configurable watermarks
- Connection pooling for database and external service connections
- Distributed tracing with OpenTelemetry for end-to-end visibility
- Feedback incorporation with active learning for threshold auto-tuning
- Review queue prioritization based on confidence score descending
- SLA tracking for human review turnaround time
