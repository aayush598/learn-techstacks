# Section 05: Anomaly Scoring & Prioritization

## Overview

Anomaly scoring quantifies the severity and impact of detected anomalies to prevent alert fatigue. Each anomaly receives a score based on deviation magnitude, affected metric criticality, business impact, and historical false positive rate. High-scoring anomalies are promoted to alerts; low-scoring ones are suppressed or logged.

## Architecture

```
Scoring Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Anomaly Detected] → [Scoring Engine] → [Priority] → [Action]
         │                   │                │            │
    Raw detection       Score = f(         Critical →   Immediate
    with deviation      deviation,         High     →   Alert (5min)
    and features        impact,            Medium   →   Digest
                        confidence,        Low      →   Log only
                        false_pos_rate)    Info     →   Suppress

Score Components:
  ┌──────────────────────────────────────────────┐
  │  AnomalyScore =                              │
  │    w1 * deviationScore +                       │
  │    w2 * impactScore +                          │
  │    w3 * confidenceScore -                      │
  │    w4 * falsePositivePenalty                   │
  │                                                │
  │  Where w1 + w2 + w3 + w4 = 1.0                │
  │  (default: 0.4, 0.3, 0.2, 0.1)                │
  └──────────────────────────────────────────────┘

Priority Mapping:
  Score ≥ 0.9  → Critical → Notify on-call immediately
  Score ≥ 0.7  → High     → Notify team channel
  Score ≥ 0.4  → Medium   → Add to next digest
  Score ≥ 0.1  → Low      → Log for review
  Score < 0.1  → Info     → Suppress
```

## Design Decisions

- **Weighted Scoring**: Configurable weights for different score components
- **False Positive Feedback Loop**: User feedback reduces future score of similar anomalies
- **Impact Estimation**: Combines metric criticality with user count affected
- **Dynamic Thresholds**: Thresholds adjust based on current alert volume

## Implementation Approach

```typescript
interface ScoringConfig {
  weights: {
    deviation: number;
    impact: number;
    confidence: number;
    falsePositivePenalty: number;
  };
  thresholds: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  metricCriticality: Record<string, number>; // 0.0 - 1.0
}

interface AnomalyEvent {
  id: string;
  metric: string;
  value: number;
  baseline: number;
  deviation: number; // z-score or percentage
  method: string;
  featureImportance: Array<{ feature: string; importance: number }>;
  timestamp: Date;
}

interface ScoredAnomaly extends AnomalyEvent {
  score: number;
  priority: 'critical' | 'high' | 'medium' | 'low' | 'info';
  scoreBreakdown: {
    deviationScore: number;
    impactScore: number;
    confidenceScore: number;
    falsePositivePenalty: number;
  };
  affectedUsers?: number;
}

class AnomalyScorer {
  private falsePositiveHistory: Map<string, number> = new Map();

  constructor(private config: ScoringConfig) {}

  async score(anomaly: AnomalyEvent): Promise<ScoredAnomaly> {
    const deviationScore = this.computeDeviationScore(anomaly);
    const impactScore = this.computeImpactScore(anomaly);
    const confidenceScore = this.computeConfidenceScore(anomaly);
    const falsePositivePenalty = this.computeFalsePositivePenalty(anomaly);

    const score =
      this.config.weights.deviation * deviationScore +
      this.config.weights.impact * impactScore +
      this.config.weights.confidence * confidenceScore -
      this.config.weights.falsePositivePenalty * falsePositivePenalty;

    const clampedScore = Math.max(0, Math.min(1, score));

    return {
      ...anomaly,
      score: clampedScore,
      priority: this.mapPriority(clampedScore),
      scoreBreakdown: { deviationScore, impactScore, confidenceScore, falsePositivePenalty },
    };
  }

  private computeDeviationScore(anomaly: AnomalyEvent): number {
    // Normalize deviation to 0-1 range
    const deviation = Math.abs(anomaly.deviation);
    if (deviation >= 10) return 1.0;
    if (deviation >= 5) return 0.9;
    if (deviation >= 3) return 0.7;
    if (deviation >= 2) return 0.5;
    return deviation / 2 * 0.5;
  }

  private computeImpactScore(anomaly: AnomalyEvent): number {
    const criticality = this.config.metricCriticality[anomaly.metric] || 0.3;

    // Estimate affected users based on metric
    const estimatedUsers = this.estimateAffectedUsers(anomaly);
    const userImpact = Math.min(1, estimatedUsers / 10000); // 10k+ users = max impact

    return criticality * 0.6 + userImpact * 0.4;
  }

  private estimateAffectedUsers(anomaly: AnomalyEvent): number {
    // In production, query real-time user count from monitoring
    switch (anomaly.metric) {
      case 'call_error_rate': return 5000;
      case 'api_latency_p99': return 8000;
      case 'stt_failure_rate': return 3000;
      case 'agent_response_timeout': return 2000;
      default: return 100;
    }
  }

  private computeConfidenceScore(anomaly: AnomalyEvent): number {
    // Higher confidence for methods with more data points
    const methodConfidence: Record<string, number> = {
      'zscore': 0.7,
      'moving_average': 0.6,
      'isolation_forest': 0.8,
      'autoencoder': 0.75,
      'ensemble': 0.9,
    };

    return methodConfidence[anomaly.method] || 0.5;
  }

  private computeFalsePositivePenalty(anomaly: AnomalyEvent): number {
    const metricHistory = this.falsePositiveHistory.get(anomaly.metric) || 0;
    // If metric has high false positive rate, reduce score
    return Math.min(1, metricHistory / 100 * 0.5);
  }

  recordFeedback(anomalyId: string, isFalsePositive: boolean): void {
    if (isFalsePositive) {
      // Store metric-level false positive count
      // (simplified — in production, use feature-based similarity)
    }
  }

  private mapPriority(score: number): ScoredAnomaly['priority'] {
    const t = this.config.thresholds;
    if (score >= t.critical) return 'critical';
    if (score >= t.high) return 'high';
    if (score >= t.medium) return 'medium';
    if (score >= t.low) return 'low';
    return 'info';
  }
}
```

## Integration Points

- **Alert Router**: Scored anomalies routed to appropriate channels based on priority
- **Feedback API**: Users can mark alerts as false positives
- **Dashboard**: Score breakdown visualization for each anomaly

## Production Considerations

- **Weight Tuning**: Scoring weights tuned based on historical alert outcomes
- **Alert Fatigue Monitoring**: Track alerts per user and adjust thresholds
- **Seasonal Score Adjustment**: Reduce scores during known high-traffic periods

## Open-Source Tools

- **Lodash**: Statistical utilities for score computation
- **BullMQ**: Priority-based job queue for alert processing
