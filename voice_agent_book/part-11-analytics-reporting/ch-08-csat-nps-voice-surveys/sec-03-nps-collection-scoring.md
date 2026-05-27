# Section 03: NPS Collection & Scoring

## Overview

The NPS (Net Promoter Score) collection and scoring system measures customer loyalty by asking "How likely are you to recommend our service to a friend or colleague?" on an 11-point scale (0-10). Respondents are categorized as Promoters (9-10), Passives (7-8), or Detractors (0-6), and the NPS is computed as %Promoters − %Detractors. The system manages the entire lifecycle from survey delivery through scoring, trend analysis, and feedback collection.

Unlike CSAT which measures satisfaction with a specific interaction, NPS measures overall brand perception. The system typically sends NPS surveys on a periodic cadence (weekly, monthly, or after a customer's Nth call) rather than after every interaction. It supports open-ended follow-up questions for Detractors and Promoters to capture qualitative feedback. The NPS engine tracks score history per customer to detect Promoter-to-Detractor migration patterns and integrates with retention workflows.

## Architecture

```
                   NPS Collection Pipeline

   NPS Trigger → Kafka → NPS Survey Delivery
                             |
                   ┌─────────┴────────┐
                   ▼                  ▼
             Voice IVR            SMS/Email
           (0-10 scale)      (link/text reply)
                   |                  |
                   ▼                  ▼
             Response Parser → Kafka → NPS Processor
                                         |
                              ┌──────────┼──────────┐
                              ▼          ▼          ▼
                         Categorizer  Computator  Feedback
                         (Promoter/   (NPS score)  Collector
                          Passive/                   |
                          Detractor)                 ▼
                              |               Feedback Store
                              ▼
                     Time-Series NPS Store
```

## Design Decisions

- **Periodic cadence over post-call delivery for NPS:** NPS surveys are delivered on a configurable schedule (e.g., once per month per customer, or after every 5th call) rather than after every call. This matches the methodology's intent of measuring overall relationship rather than transaction satisfaction. Trade-off: periodic delivery requires a customer identity resolution system that may not exist in pure call-centric platforms, adding integration complexity with CRM systems.

- **Open-ended follow-up for Promoters and Detractors over single-question NPS:** When a respondent selects 9-10 (Promoter) or 0-6 (Detractor), the survey automatically prompts for a follow-up explanation: "What do you most appreciate?" for Promoters and "What can we improve?" for Detractors. This qualitative data is critical for root cause analysis. Trade-off: follow-up questions increase survey duration by 30-60 seconds, reducing completion rates by approximately 8%.

- **Customer-level NPS tracking over call-level NPS:** NPS scores are attributed to the customer profile, not individual calls. The system maintains an NPS history per customer and computes trend lines. This requires merging survey responses with customer identity data from the CRM or contact center platform. Trade-off: customer identity resolution can fail for anonymous callers, requiring a fallback to call-level attribution.

## Implementation Approach

```typescript
interface NPSResponse {
  id: string;
  surveyId: string;
  tenantId: string;
  customerId: string;
  customerPhone: string;
  score: number; // 0-10
  category: 'promoter' | 'passive' | 'detractor';
  followUpFeedback?: string;
  channel: 'voice_dtmf' | 'voice_stt' | 'sms' | 'email' | 'in_app';
  timestamp: number;
}

interface NPSCalculation {
  tenantId: string;
  periodStart: number;
  periodEnd: number;
  totalResponses: number;
  promoters: number;
  passives: number;
  detractors: number;
  promoterPercent: number;
  detractorPercent: number;
  npsScore: number; // -100 to +100
  customerSegments?: Record<string, NPSCalculation>;
}

function categorizeScore(score: number): 'promoter' | 'passive' | 'detractor' {
  if (score >= 9) return 'promoter';
  if (score >= 7) return 'passive';
  return 'detractor';
}

class NPSProcessor {
  async processResponse(raw: RawNPSResponse): Promise<NPSResponse> {
    const score = this.parseScore(raw.rawResponse, raw.channel);
    if (score < 0 || score > 10) {
      throw new ValidationError(`Invalid NPS score: ${score}`);
    }

    const category = categorizeScore(score);
    const customerId = await this.resolveCustomerId(raw.customerPhone);

    const response: NPSResponse = {
      id: generateId(),
      surveyId: raw.surveyId,
      tenantId: raw.tenantId,
      customerId,
      customerPhone: maskPhone(raw.customerPhone),
      score,
      category,
      followUpFeedback: raw.followUpResponse,
      channel: raw.channel,
      timestamp: Date.now(),
    };

    await this.storeResponse(response);
    await this.updateNPSCalculation(response);

    if (category === 'detractor') {
      await this.triggerRetentionWorkflow(response);
    }

    return response;
  }

  private parseScore(rawResponse: string, channel: string): number {
    switch (channel) {
      case 'voice_dtmf': {
        const digits = rawResponse.replace(/[^0-9]/g, '');
        if (digits.length === 1) return parseInt(digits, 10);
        if (digits.length === 2 && digits.startsWith('1') && '0'.includes(digits[1])) return 10;
        throw new ValidationError('Invalid DTMF length for NPS');
      }
      case 'voice_stt': {
        const spoken = rawResponse.toLowerCase().trim();
        const numberMap: Record<string, number> = {
          zero: 0, one: 1, two: 2, three: 3, four: 4,
          five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
        };
        if (numberMap[spoken] !== undefined) return numberMap[spoken];
        const parsed = parseInt(spoken, 10);
        if (!isNaN(parsed) && parsed >= 0 && parsed <= 10) return parsed;
        throw new ValidationError('Could not parse speech NPS');
      }
      default:
        return parseInt(rawResponse.trim(), 10);
    }
  }

  async computeNPS(params: {
    tenantId: string;
    startTime: number;
    endTime: number;
  }): Promise<NPSCalculation> {
    const responses = await this.queryResponses(params);
    const total = responses.length;

    if (total === 0) {
      return { ...params, totalResponses: 0, promoters: 0, passives: 0,
               detractors: 0, promoterPercent: 0, detractorPercent: 0, npsScore: 0 };
    }

    const promoters = responses.filter(r => r.category === 'promoter').length;
    const detractors = responses.filter(r => r.category === 'detractor').length;

    const promoterPercent = (promoters / total) * 100;
    const detractorPercent = (detractors / total) * 100;
    const npsScore = Math.round(promoterPercent - detractorPercent);

    return {
      ...params,
      totalResponses: total,
      promoters,
      passives: total - promoters - detractors,
      detractors,
      promoterPercent,
      detractorPercent,
      npsScore,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| TimescaleDB (Apache 2.0) | Server | Time-series NPS score storage |
| Apache Kafka (Apache 2.0) | Server | Response event streaming |
| Redis (RSAL) | Server | Customer identity cache |
| Elasticsearch (ELASTIC) | Server | NPS trend and segment queries |

## Production Considerations

**Scaling:** NPS calculations for large tenant bases (100,000+ responses) use pre-aggregated hourly buckets. The `computeNPS` function reads from materialized views rather than scanning raw responses. For customer-level NPS trend tracking, maintain a separate document store (Elasticsearch) indexed by customer ID and timestamp. Periodic NPS survey dispatch runs as a scheduled job with configurable cadence per tenant, respecting per-customer suppression windows.

**Security:** NPS responses are PII-linked and must be stored with encryption at rest. Follow-up feedback text may contain sensitive information; implement automated PII redaction before storing in analytics stores. Customer ID resolution must respect data residency requirements — EU customer data must not be resolved through US-based CRM systems without appropriate safeguards.

**Monitoring:** Track NPS response rate, score distribution (Promoter/Passive/Detractor percentages), NPS trend week-over-week, and Detractor follow-up response rate. Alert if NPS drops by more than 10 points in a week, if response rate falls below 5%, or if Detractor feedback volume spikes by 50% indicating a systemic issue.
