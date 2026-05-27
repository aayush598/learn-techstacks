# Section 06: Sentiment-Survey Correlation

## Overview

The sentiment-survey correlation system bridges the gap between real-time call sentiment analysis and explicit customer survey responses. By correlating the automated sentiment score computed during the call (based on tone, word choice, and engagement) with the post-call survey rating, operators can validate sentiment accuracy, identify mismatches, and derive deeper insights. For example, a call with negative automated sentiment but a high CSAT rating may indicate the agent successfully recovered the interaction, while a positive sentiment call with a low NPS may reveal an issue the sentiment model cannot detect.

The correlation system joins sentiment time-series data (per-call segment scores) with survey response data using the call SID as the join key. It produces correlation matrices, discrepancy reports, and composite scores that feed into quality assurance workflows. The system processes data in near-real-time, making correlated results available within 1 minute of survey completion for dashboard display.

## Architecture

```
               Sentiment-Survey Correlation Pipeline

   Call Sentiment Stream → Kafka → Sentiment Store
                                         |
   Survey Response Stream → Kafka → Survey Response Store
                                         |
                              ┌─────────┴────────┐
                              ▼                  ▼
                        Correlation Join    Discrepancy
                        (call SID key)      Detector
                              |                  |
                              ▼                  ▼
                        Correlation Matrix   Alert Engine
                              |                  |
                              ▼                  ▼
                        Elasticsearch      Notification
                        (analytics)        (QA team)
```

## Design Decisions

- **Per-segment sentiment correlation over whole-call average:** Rather than comparing the survey score to the overall call sentiment average, the system correlates survey responses with sentiment scores from the last 30 seconds of the call and the highest-emotion segment. Research shows that customers weigh the end of the call and emotional peak moments most heavily in survey ratings. Trade-off: per-segment correlation requires storing granular sentiment data (5-second intervals), increasing storage by approximately 10x compared to per-call averages.

- **Discrepancy detection with severity classification over simple difference:** The system classifies sentiment-survey mismatches into severity levels. A "minor discrepancy" is a 1-point gap between normalized sentiment (mapped to 1-5 scale) and CSAT. A "major discrepancy" is a 2+ point gap, and a "critical discrepancy" is when sentiment is positive but survey is negative (or vice versa). Critical discrepancies trigger QA review workflows. Trade-off: severity classification requires defining and tuning thresholds per tenant, as customer segments may have different baseline sentiment norms.

- **Composite confidence scoring over treating sentiment and survey equally:** Instead of presenting sentiment and survey scores side-by-side, the system computes a "composite confidence score" that weights survey response (60%), call sentiment (30%), and historical customer behavior (10%). This gives a more reliable overall satisfaction measure when survey response rates are low. Trade-off: composite scoring is less transparent to end users who may want raw sentiment and survey scores independently, requiring the UI to expose both raw and composite views.

## Implementation Approach

```typescript
interface CallSentimentRecord {
  callSid: string;
  tenantId: string;
  overallScore: number; // -1.0 to 1.0
  segments: SentimentSegment[];
  peakEmotion: { score: number; timestamp: number };
  endSentiment: { score: number; timestamp: number };
  wordCount: number;
  talkRatio: number; // agent vs customer
}

interface SentimentSegment {
  startTime: number;
  endTime: number;
  score: number;
  emotion: 'anger' | 'sadness' | 'joy' | 'fear' | 'neutral';
  confidence: number;
}

interface SurveyResponseRecord {
  callSid: string;
  tenantId: string;
  surveyType: 'CSAT' | 'NPS' | 'CES';
  score: number;
  normalizedScore: number; // 0-5 or 0-10 normalized
  timestamp: number;
}

interface CorrelationResult {
  callSid: string;
  tenantId: string;
  sentimentScore: number; // -1.0 to 1.0
  normalizedSentiment: number; // 1-5 mapped
  surveyScore: number;
  normalizedSurvey: number;
  discrepancy: number;
  severity: 'none' | 'minor' | 'major' | 'critical';
  compositeConfidence: number;
  correlationFactors: CorrelationFactor[];
}

interface CorrelationFactor {
  name: string;
  weight: number;
  contribution: number;
}

class SentimentSurveyCorrelation {
  private sentimentStore: SentimentStore;
  private surveyStore: SurveyStore;

  async correlate(
    callSid: string,
    tenantId: string
  ): Promise<CorrelationResult | null> {
    const sentiment = await this.sentimentStore.getByCallSid(callSid);
    const survey = await this.surveyStore.getByCallSid(callSid);

    if (!sentiment || !survey) return null;

    const normalizedSentiment = this.normalizeSentimentToSurveyScale(
      sentiment,
      survey.surveyType
    );

    const normalizedSurvey = survey.surveyType === 'NPS'
      ? survey.score
      : survey.score;

    const discrepancy = Math.abs(normalizedSurvey - normalizedSentiment);
    const severity = this.classifyDiscrepancy(
      discrepancy,
      sentiment.overallScore,
      survey.score
    );

    const factors: CorrelationFactor[] = [
      { name: 'survey_response', weight: 0.6, contribution: 0 },
      { name: 'call_sentiment', weight: 0.3, contribution: 0 },
      { name: 'customer_history', weight: 0.1, contribution: 0 },
    ];

    const compositeConfidence = this.computeCompositeConfidence(
      survey.score,
      normalizedSentiment,
      factors
    );

    return {
      callSid,
      tenantId,
      sentimentScore: sentiment.overallScore,
      normalizedSentiment,
      surveyScore: survey.score,
      normalizedSurvey,
      discrepancy,
      severity,
      compositeConfidence,
      correlationFactors: factors.map(f => ({
        ...f,
        contribution: this.computeFactorContribution(f, survey, sentiment),
      })),
    };
  }

  private normalizeSentimentToSurveyScale(
    sentiment: CallSentimentRecord,
    surveyType: string
  ): number {
    // Map -1..1 sentiment to 1..5 for CSAT/CES or 0..10 for NPS
    const maxScore = surveyType === 'NPS' ? 10 : 5;
    const normalized = ((sentiment.overallScore + 1) / 2) * maxScore;
    return Math.round(Math.max(0, Math.min(maxScore, normalized)));
  }

  private classifyDiscrepancy(
    discrepancy: number,
    sentimentScore: number,
    surveyScore: number
  ): 'none' | 'minor' | 'major' | 'critical' {
    if (discrepancy < 1) return 'none';
    if (discrepancy < 2) return 'minor';
    if (discrepancy >= 2) {
      // Check if sentiment and survey disagree on polarity
      const sentimentPositive = sentimentScore > 0;
      const surveyPositive = surveyScore > (surveyScore >= 10 ? 5 : 3);
      if (sentimentPositive !== surveyPositive) return 'critical';
      return 'major';
    }
    return 'none';
  }

  private computeCompositeConfidence(
    surveyScore: number,
    normalizedSentiment: number,
    factors: CorrelationFactor[]
  ): number {
    // Weighted average: survey (60%) + sentiment (30%) + history (10%)
    // History component defaults to neutral (0.5) if unavailable
    const surveyComponent = surveyScore / (surveyScore <= 10 ? 10 : 5);
    const sentimentComponent = normalizedSentiment / (normalizedSentiment <= 10 ? 10 : 5);

    // Simple weighted combination
    return Math.round(
      (surveyComponent * 0.6 + sentimentComponent * 0.3 + 0.5 * 0.1) * 100
    ) / 100;
  }

  private computeFactorContribution(
    factor: CorrelationFactor,
    survey: SurveyResponseRecord,
    sentiment: CallSentimentRecord
  ): number {
    switch (factor.name) {
      case 'survey_response':
        return survey.normalizedScore * factor.weight;
      case 'call_sentiment':
        return ((sentiment.overallScore + 1) / 2) * 5 * factor.weight;
      case 'customer_history':
        return 2.5 * factor.weight; // Default neutral
      default:
        return 0;
    }
  }

  async findCriticalDiscrepancies(params: {
    tenantId: string;
    startTime: number;
    endTime: number;
  }): Promise<CorrelationResult[]> {
    const correlations = await this.queryCorrelationRange(params);
    return correlations.filter(c => c.severity === 'critical');
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Elasticsearch (ELASTIC) | Server | Correlation result indexing and search |
| Apache Kafka (Apache 2.0) | Server | Event stream for sentiment and survey data |
| Redis (RSAL) | Server | Fast call-SID lookup cache |
| Python scipy (BSD-3) | Server | Statistical correlation analysis (batch) |

## Production Considerations

**Scaling:** Correlation is computed on-demand for individual calls and in batch for analytics dashboards. Batch correlation runs as a scheduled job every 15 minutes, processing the last 15 minutes of survey responses and their corresponding sentiment records. Materialized correlation views in Elasticsearch serve dashboard queries with sub-second latency. For tenants with 500,000+ calls/month, partition correlation data by week to keep index sizes manageable.

**Security:** Correlation results contain references to call SIDs and customer identifiers. Access to discrepancy reports requires the `qa:discrepancy-read` permission. Critical discrepancy notifications should not include PII in the notification payload — send only the correlation ID and severity, with a link to the full report behind authentication.

**Monitoring:** Track correlation coverage (percentage of survey responses with matching sentiment data), discrepancy rate (percentage of correlations with non-none severity), composite confidence distribution, and critical discrepancy frequency. Alert if correlation coverage drops below 90% (indicating missing sentiment data), if critical discrepancy rate exceeds 5% (possible systemic issue), or if composite confidence drops across all correlations (possible model drift).
