# Section 06: Product Quality Metrics

## Quality Framework

Product quality metrics measure technical performance, reliability, and accuracy of the voice AI platform. These are leading indicators of customer satisfaction and retention.

```
Product Quality Pillars
┌─────────────────────────────────────────────────────────────────────────┐
│ Reliability (40%)         Performance (30%)         Accuracy (30%)     │
│ ┌────────────────────┐   ┌──────────────────┐   ┌────────────────┐    │
│ • Uptime (99.9%)     │   • E2E latency      │   • Transcription │    │
│ • Call success rate  │   • STT real-time    │     accuracy      │    │
│ • Error rate         │     factor           │   • Intent recog. │    │
│ • API error rate     │   • TTS generation   │   • Sentiment     │    │
│ • Infrastructure     │     speed            │     accuracy      │    │
│   health             │   • Response start   │   • FCR rate      │    │
│                      │     time             │                   │    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Quality Metrics

### Reliability Metrics
- **Uptime (SLA):** Service availability (target: 99.9%+, enterprise: 99.99%)
- **Call success rate:** % of calls that complete without error (target: >98%)
- **Error rate:** % of calls with technical failure (target: <2%)
- **API error rate:** % of API requests returning errors (target: <0.5%)
- **Transcription failure rate:** % of calls failing STT (target: <0.1%)

### Performance Metrics
- **End-to-end latency (p50):** 1,500ms target (caller speaks → hears response)
- **End-to-end latency (p95):** 3,000ms target
- **STT real-time factor:** <0.5x (audio processed faster than real-time)
- **TTS generation speed:** <500ms for first audio chunk
- **Response start time:** <1,500ms from end of caller speech

### Accuracy Metrics
- **Word Error Rate (WER):** <5% for clear audio, <10% for noisy audio
- **Intent recognition accuracy:** >95%
- **Entity extraction accuracy:** >90%
- **Sentiment classification accuracy:** >85%
- **First Call Resolution (FCR):** >75%

## Quality Data Model

```typescript
interface ProductQualityMetrics {
  reliability: {
    uptime: number;
    callSuccessRate: number;
    errorRate: number;
    apiErrorRate: number;
    transcriptionFailureRate: number;
    infrastructureHealth: 'healthy' | 'degraded' | 'critical';
  };
  
  performance: {
    e2eLatencyP50: number;
    e2eLatencyP95: number;
    sttRealTimeFactor: number;
    ttsGenerationSpeed: number;
    responseStartTime: number;
  };
  
  accuracy: {
    wordErrorRate: number;
    intentAccuracy: number;
    entityAccuracy: number;
    sentimentAccuracy: number;
    fcrRate: number;
  };
  
  healthScore: number; // composite (0-100)
}

function calculateQualityScore(metrics: ProductQualityMetrics): QualityGrade {
  const reliability = (
    (metrics.reliability.uptime / 99.9) * 40 +
    metrics.reliability.callSuccessRate * 0.4 * 100 +
    (1 - metrics.reliability.errorRate) * 0.2 * 100
  );
  
  const performance = (
    Math.max(0, 100 - (metrics.performance.e2eLatencyP50 / 1500) * 100) * 0.5 +
    Math.max(0, 100 - (metrics.performance.e2eLatencyP95 / 3000) * 100) * 0.5
  );
  
  const accuracy = (
    (1 - metrics.accuracy.wordErrorRate) * 0.4 +
    metrics.accuracy.intentAccuracy * 0.3 +
    metrics.accuracy.entityAccuracy * 0.3
  ) * 100;
  
  const healthScore = (reliability * 0.4 + performance * 0.3 + accuracy * 0.3);
  
  return {
    healthScore,
    grade: healthScore > 90 ? 'A' : healthScore > 80 ? 'B' : healthScore > 70 ? 'C' : 'D',
    reliability,
    performance,
    accuracy,
    actionableAlerts: generateAlerts(metrics),
  };
}
```

## SLA Tiers

| Tier | Uptime | Response (Critical) | Response (Normal) | Credits |
|------|--------|---------------------|-------------------|---------|
| Free | 99.5% | Best effort | 24 hours | None |
| Starter | 99.5% | 4 hours | 8 hours | 5% per 0.5% below |
| Pro | 99.9% | 1 hour | 4 hours | 10% per 0.1% below |
| Business | 99.95% | 30 minutes | 2 hours | 15% per 0.05% below |
| Enterprise | 99.99% | 15 minutes | 1 hour | 25% per 0.01% below |

## Monitoring & Alerting

```typescript
interface QualityAlert {
  metric: string;
  currentValue: number;
  threshold: number;
  severity: 'critical' | 'warning' | 'info';
  duration: number; // how long threshold exceeded
  impactedCustomers: string[];
  autoRemediation: string;
}

class QualityMonitor {
  private thresholds = {
    callSuccessRate: { critical: 0.95, warning: 0.98 },
    e2eLatencyP95: { critical: 5000, warning: 3000 },
    errorRate: { critical: 0.05, warning: 0.02 },
  };
  
  async checkQuality(): Promise<QualityAlert[]> {
    const metrics = await this.collectMetrics();
    const alerts: QualityAlert[] = [];
    
    if (metrics.callSuccessRate < this.thresholds.callSuccessRate.critical) {
      alerts.push({
        metric: 'Call Success Rate',
        currentValue: metrics.callSuccessRate,
        threshold: this.thresholds.callSuccessRate.critical,
        severity: 'critical',
        duration: 300, // 5 minutes
        impactedCustomers: await this.getImpactedCustomers(),
        autoRemediation: 'Scale GPU pool, restart failed pods',
      });
    }
    
    // Additional checks...
    return alerts;
  }
}
```

## Quality Dashboard

```
Quality Dashboard (Last 24 Hours)
┌─────────────────────────────────────────────────────────────────────────┐
│ Health Score: 93.7 (A)   Uptime: 99.97%   Calls: 12,847              │
│                                                                         │
│ Reliability                  Performance              Accuracy         │
│ ┌────────────────────────┐  ┌────────────────────┐  ┌──────────────┐  │
│ │ Success Rate: 97.8%    │  │ E2E Latency P50:   │  │ WER: 3.2%    │  │
│ │ ▼ 0.3% from baseline  │  │   1,423ms          │  │ Intent: 96.7%│  │
│ │ Error Rate: 0.8%      │  │ E2E Latency P95:   │  │ Entity: 91.2%│  │
│ │ API Errors: 0.3%      │  │   2,847ms          │  │ Sentiment:   │  │
│ │ Infra: ✅ Healthy     │  │ Response Start:    │  │   88.5%      │  │
│ └────────────────────────┘  │   1,215ms          │  └──────────────┘  │
│                              └────────────────────┘                    │
│ Alerts: None                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Open Source Tools

| Tool | Purpose | Alternative |
|------|---------|-------------|
| Prometheus | Metrics collection | Datadog |
| Grafana | Dashboard visualization | Datadog |
| Loki | Log aggregation | Datadog, ELK |
| Tempo | Distributed tracing | Datadog APM |
| Sentry | Error tracking | Rollbar |
| Checkly | Synthetic monitoring | Datadog Synthetics |
| K6 | Load testing | Locust, Artillery |

## Production Considerations

- Monitor E2E latency on every call (not sampled)
- Track quality per model version (canary new models)
- Automated rollback if quality drops below thresholds
- Quality regression test suite runs before every deployment
- P1 quality issues trigger automated incident response
- Weekly quality review with engineering team
- Monthly quality report shared with customers (transparency)
