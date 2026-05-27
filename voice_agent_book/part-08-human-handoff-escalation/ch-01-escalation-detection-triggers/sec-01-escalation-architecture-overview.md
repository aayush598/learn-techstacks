# Section 01: Escalation Architecture Overview

## Overview

The escalation system determines when an AI agent should hand off a conversation to a human agent. It uses multi-signal fusion (sentiment analysis, keyword detection, confidence scoring, explicit requests) to make escalation decisions with high precision (low false positives) and high recall (few missed escalations).

The system architecture has three layers: (1) Signal Detection - individual modules detect escalation indicators, (2) Scoring Engine - fuses signals into a composite escalation score, and (3) Action Engine - executes the escalation (warm transfer, cold transfer, queue placement). The system supports configurable thresholds per tenant and per agent.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Conversation │──▶│  Signal      │──▶│  Scoring     │──▶│  Action      │
│ Stream       │   │  Detectors   │   │  Engine      │   │  Engine      │
│ (STT output) │   │              │   │              │   │              │
└──────────────┘   │ - Sentiment  │   │ - Weighted   │   │ - Warm xfer  │
                   │ - Keyphrases │   │   sum        │   │ - Cold xfer  │
                   │ - Confidence │   │ - ML model   │   │ - Queue      │
                   │ - Explicit   │   │ - Threshold  │   │ - Voicemail  │
                   │   requests   │   │   comparison │   └──────────────┘
                   └──────────────┘   └──────────────┘
                           │                  │
                           ▼                  ▼
                    ┌──────────────┐   ┌──────────────┐
                    │  Real-time   │   │  Log &       │
                    │  Dashboard   │   │  Analytics   │
                    │  (supervisor)│   │  (post-call) │
                    └──────────────┘   └──────────────┘
```

## Design Decisions

- **Multi-Signal Fusion**: No single signal is reliable enough for escalation decisions. Sentiment alone can be misleading (angry but solvable by AI). The fusion model weights 4+ signals and escalates only when composite score exceeds threshold.
- **Configurable Thresholds**: Each tenant can set per-agent escalation thresholds. Default: sentiment < -0.7 OR confidence < 0.6 OR keyword match. Enterprise tenants get custom ML model per agent.
- **Real-time Scoring**: The scoring engine runs per utterance (every 300-500ms). Score history maintained for trend analysis (escalating anger detected before single-utterance threshold).
- **Human-in-the-Loop**: Escalation is proposed, not automatic (unless configured). Supervisor dashboard shows pending escalations with 5-second window to cancel before transfer executes.

## Implementation Approach

```typescript
interface EscalationSignal {
  name: string;
  value: number; // 0-1
  weight: number;
  timestamp: number;
}

interface EscalationConfig {
  threshold: number; // composite score triggers escalation
  minSignals: number; // require at least N signals
  cooldownPeriod: number; // ms before re-escalation
  autoEscalate: boolean; // skip supervisor confirmation
}

class EscalationEngine {
  private detectors: SignalDetector[];
  private config: EscalationConfig;
  private lastEscalation: number = 0;

  async evaluate(utterance: Utterance): Promise<EscalationDecision | null> {
    const signals = await Promise.all(
      this.detectors.map(d => d.detect(utterance))
    );

    const score = this.fuseSignals(signals);
    if (score >= this.config.threshold &&
        signals.filter(s => s.value > 0.5).length >= this.config.minSignals &&
        Date.now() - this.lastEscalation > this.config.cooldownPeriod) {
      this.lastEscalation = Date.now();
      return {
        shouldEscalate: true,
        score,
        signals,
        timestamp: Date.now(),
      };
    }
    return null;
  }

  private fuseSignals(signals: EscalationSignal[]): number {
    const weighted = signals.reduce((sum, s) => sum + s.value * s.weight, 0);
    const totalWeight = signals.reduce((sum, s) => sum + s.weight, 0);
    return weighted / totalWeight;
  }
}
```

## Integration Points

- **Transfer System (P8 Ch 02)**: Escalation triggers warm or cold transfer with context serialization.
- **Supervisor Dashboard (P8 Ch 05)**: Pending escalations appear in supervisor UI with 5s cancellation window.
- **Sentiment Analysis (P5 Ch 04)**: Primary signal source for escalation detection.
- **Confidence Scoring (P5 Ch 06)**: Low-confidence AI responses trigger escalation.

## Open-Source Tools

- **Redis** (BSD): Signal history storage and scoring state.
- **BullMQ** (MIT): Escalation action queue with priority.
- **Prometheus**: Escalation metrics (escalation rate, false positive rate, avg response time).

## Production Considerations

- **False Positive Rate**: Target <5% false positive rate (escalations that human judges as unnecessary). Monitor via post-call human review of 10% of escalated calls.
- **Escalation Latency**: Escalation decision within 200ms of utterance end. Transfer execution within 2 seconds.
- **Threshold Tuning**: A/B test threshold variations across tenant cohorts. Track customer satisfaction score (CSAT) for each threshold variant.
- **Cooldown**: 30-second cooldown prevents repeated escalation requests for the same conversation issue.
- **Human Availability**: Check human agent availability before escalating. If no agents available, route to queue with priority boost.
