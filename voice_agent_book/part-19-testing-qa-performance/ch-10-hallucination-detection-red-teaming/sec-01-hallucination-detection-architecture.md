# Section 01: Hallucination Detection Architecture

## Overview

Hallucination detection identifies when LLM-generated responses contain incorrect, fabricated, or misleading information. The detection system combines multiple approaches: factuality checking against knowledge bases, self-consistency verification, natural language inference (NLI) for contradiction detection, and confidence scoring from the LLM itself. Detection runs both in real-time (blocking hallucinations before they reach users) and asynchronously (for monitoring and analysis).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Hallucination Detection                       │
├─────────────────────────────────────────────────────────────┤
│  Input: LLM Response + Context + Knowledge Base              │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Factuality   │  │ Self-        │  │ NLI                 │  │
│  │ Check        │  │ Consistency  │  │ Contradiction       │  │
│  │              │  │ Check        │  │ Detection           │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│  ┌──────▼────────────────▼─────────────────────▼──────────┐ │
│  │              Aggregator                                  │ │
│  │  Weighted scoring → Confidence → Decision               │ │
│  └──────────────────────┬──────────────────────────────────┘ │
│                         │                                     │
│                         ▼                                     │
│              Pass / Flag / Block                              │
└───────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Multi-Method Approach**: Combine techniques for robust detection
- **Real-Time vs Async**: Light checks in real-time, heavy checks async
- **Configurable Strictness**: Per-agent detection thresholds
- **Human-in-the-Loop**: Flagged responses reviewed by humans

## Implementation Approach

```typescript
interface HallucinationCheckResult {
  detected: boolean;
  confidence: number;
  method: string;
  details: string;
}

class HallucinationDetector {
  async check(response: string, context: CallContext): Promise<DetectionResult> {
    const checks: HallucinationCheckResult[] = await Promise.all([
      this.factualityCheck(response, context.knowledgeBase),
      this.selfConsistencyCheck(response, context.conversationHistory),
      this.nliContradictionCheck(response, context),
      this.confidenceScoring(response),
    ]);

    const aggregated = this.aggregateChecks(checks);
    return {
      hallucinationDetected: aggregated.score > this.getThreshold(context.agentId),
      confidence: aggregated.confidence,
      checks,
      decision: aggregated.score > this.getThreshold(context.agentId) ? 'block' : 'pass',
    };
  }

  private async factualityCheck(response: string, kb: KnowledgeBase): Promise<HallucinationCheckResult> {
    const claims = this.extractClaims(response);
    const facts = await kb.query(claims);
    const unsupported = claims.filter(c => !this.isSupported(c, facts));
    return {
      detected: unsupported.length > 0,
      confidence: unsupported.length / claims.length,
      method: 'factuality',
      details: `Found ${unsupported.length} unsupported claims`,
    };
  }
}
```

## Integration Points

- **LLM Response Pipeline**: Detection runs after LLM generates response
- **Guardrails**: Blocked responses fall back to safe default
- **Monitoring**: Detection rates tracked in dashboards

## Open-Source Tools

- **Guardrails AI** (MIT): LLM guardrail framework
- **NLI Models** (Hugging Face): Contradiction detection
- **LangChain** (MIT): LLM application framework
- **spaCy** (MIT): NLP for claim extraction

## Production Considerations

- **Latency Impact**: Detection adds 100-500ms to response time
- **False Positives**: Overly strict detection blocks valid responses
- **Model Updates**: Detection models need updating as LLM behavior changes
