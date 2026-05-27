# Section 02: CSAT Collection & Scoring

## Overview

The CSAT (Customer Satisfaction Score) collection and scoring system captures customer ratings on a 1-5 scale immediately after a call interaction. Customers are prompted with a question such as "How satisfied were you with today's call?" and provide their rating via voice IVR (keypad or voice response), SMS reply, or in-app widget. The system aggregates individual responses into per-agent, per-campaign, and per-tenant CSAT scores that feed into analytics dashboards and agent performance scorecards.

CSAT scores are computed as the average of all ratings received within a configurable rolling window (default: 7 days). The system also computes CSAT distribution (percentage of 4-5 ratings vs. 1-3 ratings), trend lines over time, and breakdowns by call reason, agent, and time of day. The collector handles partial responses, survey abandonment, and channel-specific constraints (e.g., SMS limits to single-question surveys while voice IVR supports multi-question flows).

## Architecture

```
                  CSAT Collection Pipeline

   Survey Delivery → Customer Responds → Response Handler
                                              |
                                    ┌─────────┴──────────┐
                                    ▼                    ▼
                              CSAT Validator        Channel Parser
                              (1-5 range)      (DTMF / SMS / API)
                                    |                    |
                                    ▼                    ▼
                              CSAT Enricher ←─ Kafka ←──┘
                                    |
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              Score Aggregator  Trend Analyzer   Agent Mapper
                    |               |               |
                    ▼               ▼               ▼
              Time-Series DB   Elasticsearch   Agent Store
```

## Design Decisions

- **Rolling window aggregation over cumulative scoring:** CSAT scores use a configurable rolling time window (7, 14, or 30 days) rather than a cumulative all-time average. This ensures recent performance changes are reflected promptly. Trade-off: short windows (7 days) can be noisy for low-volume agents with fewer than 10 surveys per week, requiring a minimum-response threshold before displaying a score.

- **Weighted recency decay over equal-weight averaging:** Recent ratings within the window receive higher weight than older ones using an exponential decay function. A rating from 1 hour ago has ~5x the weight of a rating from 6 days ago in a 7-day window. Trade-off: recency weighting adds computational complexity and requires explaining the scoring methodology transparently to agents who might not understand why their score changed despite good ratings.

- **Channel-specific validation over uniform parsing:** Each delivery channel applies its own validation rules. Voice IVR responses must be DTMF digits 1-5 or spoken numbers captured via speech-to-text. SMS responses must match a numeric pattern. This prevents channel-specific garbage data from polluting scores. Trade-off: maintaining per-channel parsers increases code surface and testing burden.

## Implementation Approach

```typescript
interface CSATResponse {
  id: string;
  surveyId: string;
  callSid: string;
  tenantId: string;
  agentId: string;
  campaignId: string;
  rating: number; // 1-5
  channel: 'voice_dtmf' | 'voice_stt' | 'sms' | 'email' | 'in_app';
  timestamp: number;
  abandoned: boolean;
  partialResponses?: Record<string, unknown>;
}

interface CSATAggregation {
  tenantId: string;
  agentId?: string;
  campaignId?: string;
  windowStart: number;
  windowEnd: number;
  averageScore: number;
  totalResponses: number;
  distribution: { 1: number; 2: number; 3: number; 4: number; 5: number };
  trend: TrendPoint[];
}

class CSATCollector {
  private decayFactor = 0.3; // configurable

  async recordResponse(raw: RawSurveyResponse): Promise<CSATResponse> {
    const validated = this.validateRating(raw);
    const enriched = await this.enrichWithCallData(validated);

    await this.publishToKafka(enriched);
    await this.updateLiveAggregation(enriched);

    return enriched;
  }

  private validateRating(raw: RawSurveyResponse): CSATResponse {
    let rating: number;

    switch (raw.channel) {
      case 'voice_dtmf': {
        const digit = parseInt(raw.rawResponse, 10);
        if (isNaN(digit) || digit < 1 || digit > 5) {
          throw new ValidationError('Invalid DTMF CSAT rating');
        }
        rating = digit;
        break;
      }
      case 'voice_stt': {
        const parsed = this.parseSpokenNumber(raw.rawResponse);
        if (!parsed || parsed < 1 || parsed > 5) {
          throw new ValidationError('Invalid speech CSAT rating');
        }
        rating = parsed;
        break;
      }
      case 'sms': {
        const trimmed = raw.rawResponse.trim();
        if (!/^[1-5]$/.test(trimmed)) {
          throw new ValidationError('Invalid SMS CSAT rating');
        }
        rating = parseInt(trimmed, 10);
        break;
      }
      default:
        rating = parseInt(raw.rawResponse, 10);
    }

    return { ...raw, rating };
  }

  private async enrichWithCallData(response: CSATResponse): Promise<CSATResponse> {
    const callData = await this.callStore.getCallBySid(response.callSid);
    return {
      ...response,
      agentId: callData.agentId,
      campaignId: callData.campaignId,
    };
  }

  computeWeightedScore(responses: CSATResponse[], windowMs: number): number {
    const now = Date.now();
    const weighted = responses
      .filter(r => (now - r.timestamp) < windowMs && !r.abandoned)
      .reduce((acc, r) => {
        const age = (now - r.timestamp) / windowMs;
        const weight = Math.exp(-this.decayFactor * age);
        return {
          sum: acc.sum + r.rating * weight,
          totalWeight: acc.totalWeight + weight,
        };
      }, { sum: 0, totalWeight: 0 });

    return weighted.totalWeight > 0
      ? Math.round((weighted.sum / weighted.totalWeight) * 100) / 100
      : 0;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache Kafka (Apache 2.0) | Server | Response event stream |
| TimescaleDB (Apache 2.0) | Server | Time-series score storage |
| Elasticsearch (ELASTIC) | Server | Aggregation query engine |
| Redis (RSAL) | Server | Live aggregation cache |

## Production Considerations

**Scaling:** CSAT aggregation is computed in two tiers. A lightweight stream processor maintains 15-minute window aggregations in Redis for real-time dashboard display. A batch job recomputes precise scores hourly using the time-series database for reporting accuracy. For high-volume tenants (50,000+ surveys/day), pre-aggregate by hour and materialize the rolling window from hourly buckets rather than recomputing from raw responses.

**Security:** CSAT responses are associated with call SIDs and must never expose PII in analytics outputs. Aggregate scores displayed on dashboards hide agent-level CSAT when fewer than 5 responses exist in the window (privacy threshold). API endpoints that serve CSAT data enforce tenant isolation and require the `analytics:csat-read` permission.

**Monitoring:** Track CSAT response rate (responses / surveys delivered), average score per tenant, CSAT distribution over time (monitor for sudden drops), and validation failure rate. Alert if CSAT drops more than 0.5 points in 24 hours, if response rate falls below 5%, or if validation failure exceeds 10% for any channel.
