# Section 03: Quality Assurance Score Integration

## Overview

Quality Assurance (QA) score integration connects the agent scorecard system with manual and automated quality evaluation processes. QA scores measure how well agents adhere to quality standards — script adherence, compliance with regulations, greeting and closing procedures, problem resolution, and soft skills. Scores are entered by QA evaluators through a dedicated review interface (or automatically via transcription analysis) and flow into the scorecard system as a weighted dimension.

The integration supports multiple QA evaluation methods: full evaluation (every call scored), random sampling (random percentage of each agent's calls), targeted evaluation (calls flagged by sentiment, long duration, or customer complaint), and automated evaluation (NLP-based scoring of transcription against quality criteria). QA scores are normalized to 0-100 and can be weighted to reflect the importance of different evaluation criteria. Historical QA scores are tracked to identify improvement or decline trends.

## Architecture

```
            QA Score Integration Pipeline

   Call Recordings/Transcriptions
        |
   ┌────┴────┐
   | QA UI   | ← QA Evaluators (Manual)
   | (Review |
   |  Queue) |
   └────┬────┘
        |
   ┌────┴────┐
   | Auto QA | ← NLP Engine (Automated)
   | (NLP)   |
   └────┬────┘
        |
   Kafka Topic (agent.qa.scored)
        |
   KPI Collector → Scorecard Engine
        |
   ClickHouse (QA scores)
        |
   QA Score Widget
   Agent Scorecard (QA dimension)
```

## Design Decisions

- **Automated QA as a complement to manual QA, not a replacement:** Automated NLP-based QA scoring can evaluate 100% of calls for basic criteria (greeting, compliance statement, positive closing), but misses nuanced soft skills (empathy, tone, rapport building). The system uses automated QA for baseline quality screening and routes only borderline or failed calls to human evaluators for detailed review. Trade-off: automated QA requires NLP model training and may have lower accuracy for complex criteria (e.g., "Did the agent upsell effectively?").

- **Queue-based review assignment over individual call selection:** QA evaluators work from a queue of calls assigned by the QA distribution algorithm. The algorithm prioritizes calls that need review (flagged by sentiment, long duration, customer complaint), ensures random sampling coverage, and avoids assigning too many calls to the same evaluator. Each call is scored independently by two evaluators, and the scores are averaged (or flagged for arbitration if they differ by more than 20 points). Trade-off: double evaluation increases QA workload by 100% but improves scoring reliability.

- **Scoring criteria with weighted sub-scores over a single holistic score:** A QA score is composed of multiple criteria (e.g., Greeting: 10%, Problem Understanding: 25%, Resolution: 30%, Compliance: 20%, Closing: 15%). Each criterion is scored 1-5 (or 0-100) and weighted to compute the total. This provides agents with actionable feedback on specific areas for improvement. Trade-off: detailed criteria increase the time required per evaluation (2-3 minutes per call) compared to a holistic score (30 seconds).

## Implementation Approach

```typescript
interface QaCriteria {
  id: string;
  name: string;
  description: string;
  weight: number;           // percentage, must sum to 100 across all criteria
  scoreMin: number;
  scoreMax: number;
  scoreStep: number;        // 1 for 1-5 scale, 10 for 0-100 scale
  automated: boolean;       // can this be scored by NLP?
  rubric: Array<{           // scoring rubric for evaluators
    score: number;
    description: string;
  }>;
}

interface QaEvaluation {
  id: string;
  callSid: string;
  agentId: string;
  tenantId: string;
  evaluatorId: string;
  evaluationMethod: 'manual' | 'automated' | 'hybrid';
  criteria: Array<{
    criterionId: string;
    score: number;
    weight: number;
    comment?: string;
  }>;
  totalScore: number;       // weighted sum
  maxScore: number;
  normalizedScore: number;  // 0-100
  status: 'pending' | 'completed' | 'flagged' | 'arbitrated';
  createdAt: number;
  completedAt?: number;
}

interface QaReviewQueue {
  queueId: string;
  tenantId: string;
  calls: Array<{
    callSid: string;
    agentId: string;
    agentName: string;
    duration: number;
    reason: string;           // 'random' | 'sentiment' | 'complaint' | 'long_duration'
    priority: number;         // 1-5, higher = more urgent
    transcription: string;
    recordingUrl: string;
  }>;
}

class QaScoreIntegration {
  private kafka: KafkaProducer;
  private clickhouse: ClickHouseClient;

  async submitEvaluation(evaluation: QaEvaluation): Promise<void> {
    // Store evaluation
    await this.clickhouse.insert('qa_evaluations', evaluation);

    // Publish to Kafka for scorecard update
    await this.kafka.send({
      topic: 'agent.qa.scored',
      key: evaluation.agentId,
      value: JSON.stringify({
        type: 'qa_score',
        agentId: evaluation.agentId,
        tenantId: evaluation.tenantId,
        timestamp: Date.now(),
        data: {
          score: evaluation.normalizedScore,
          maxScore: 100,
        },
      }),
    });

    // Update review queue
    await this.removeFromQueue(evaluation.callSid);
  }

  async getEvaluationQueue(
    tenantId: string,
    evaluatorId: string,
    limit: number = 20
  ): Promise<QaReviewQueue> {
    // Get calls that need QA review, prioritized
    const calls = await this.clickhouse.query(`
      SELECT
        c.callSid, c.agentId, a.name as agentName,
        c.duration, c.sentimentScore,
        c.transcription, c.recordingUrl,
        CASE
          WHEN c.sentimentScore < -0.5 THEN 5
          WHEN c.duration > 1800 THEN 4
          WHEN c.complaintFlag = 1 THEN 5
          ELSE 2
        END as priority,
        CASE
          WHEN c.sentimentScore < -0.5 THEN 'sentiment'
          WHEN c.duration > 1800 THEN 'long_duration'
          WHEN c.complaintFlag = 1 THEN 'complaint'
          ELSE 'random'
        END as reason
      FROM call_records c
      JOIN agents a ON c.agentId = a.id
      WHERE c.tenantId = '${tenantId}'
        AND c.callSid NOT IN (SELECT callSid FROM qa_evaluations WHERE tenantId = '${tenantId}')
        AND c.timestamp >= now() - INTERVAL 7 DAY
      ORDER BY priority DESC, c.timestamp ASC
      LIMIT ${limit}
    `);

    return {
      queueId: `qa:${tenantId}:${evaluatorId}`,
      tenantId,
      calls: calls.map((c: any) => ({
        callSid: c.callSid,
        agentId: c.agentId,
        agentName: c.agentName,
        duration: c.duration,
        reason: c.reason,
        priority: c.priority,
        transcription: c.transcription,
        recordingUrl: c.recordingUrl,
      })),
    };
  }

  async getAgentQaStats(
    agentId: string,
    start: number,
    end: number
  ): Promise<{
    totalEvaluations: number;
    averageScore: number;
    byCriteria: Array<{ criterionId: string; averageScore: number; count: number }>;
    trend: 'improving' | 'declining' | 'stable';
  }> {
    const result = await this.clickhouse.query(`
      SELECT
        count() as totalEvals,
        avg(normalizedScore) as avgScore
      FROM qa_evaluations
      WHERE agentId = '${agentId}'
        AND completedAt >= ${start}
        AND completedAt <= ${end}
    `);

    const byCriteria = await this.clickhouse.query(`
      SELECT criterionId, avg(score) as avgScore, count() as count
      FROM qa_evaluations
      ARRAY JOIN criteria
      WHERE agentId = '${agentId}'
        AND completedAt >= ${start}
        AND completedAt <= ${end}
      GROUP BY criterionId
    `);

    // Trend: compare last 30 days to previous 30 days
    const midPoint = (start + end) / 2;
    const recent = await this.getAverageScore(agentId, midPoint, end);
    const previous = await this.getAverageScore(agentId, start, midPoint);

    const trend = recent > previous ? 'improving'
      : recent < previous ? 'declining' : 'stable';

    return {
      totalEvaluations: result[0].totalEvals,
      averageScore: result[0].avgScore,
      byCriteria: byCriteria.map((c: any) => ({
        criterionId: c.criterionId,
        averageScore: c.avgScore,
        count: c.count,
      })),
      trend,
    };
  }

  private async getAverageScore(agentId: string, start: number, end: number): Promise<number> {
    const result = await this.clickhouse.query(`
      SELECT avg(normalizedScore) as score
      FROM qa_evaluations
      WHERE agentId = '${agentId}'
        AND completedAt >= ${start}
        AND completedAt <= ${end}
    `);
    return result[0]?.score ?? 0;
  }

  // Automated QA scoring via NLP
  async autoScore(callSid: string, transcription: string): Promise<Partial<QaEvaluation>> {
    // This would call an NLP model service
    // For illustration, simplified criteria evaluation
    const autoCriteria = [
      { criterionId: 'greeting', score: this.checkGreeting(transcription) ? 5 : 1 },
      { criterionId: 'compliance', score: this.checkCompliance(transcription) ? 5 : 1 },
      { criterionId: 'closing', score: this.checkClosing(transcription) ? 5 : 1 },
    ];

    const totalScore = autoCriteria.reduce((s, c) => s + c.score, 0);
    const maxScore = autoCriteria.length * 5;
    const normalized = (totalScore / maxScore) * 100;

    return {
      callSid,
      evaluationMethod: 'automated',
      criteria: autoCriteria.map(c => ({ ...c, weight: 100 / autoCriteria.length })),
      totalScore,
      maxScore,
      normalizedScore: normalized,
    };
  }

  private checkGreeting(transcription: string): boolean {
    const greetings = ['hello', 'hi', 'good morning', 'good afternoon', 'welcome', 'thank you for calling'];
    return greetings.some(g => transcription.toLowerCase().includes(g));
  }

  private checkCompliance(transcription: string): boolean {
    const compliancePhrases = ['this call may be recorded', 'for quality assurance', 'your call will be monitored'];
    return compliancePhrases.some(p => transcription.toLowerCase().includes(p));
  }

  private checkClosing(transcription: string): boolean {
    const closings = ['thank you', 'have a great day', 'goodbye', 'anything else', 'pleasure helping you'];
    return closings.some(c => transcription.toLowerCase().includes(c));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| spaCy (MIT) | Server | NLP for automated QA scoring |
| Hugging Face Transformers (Apache 2.0) | Server | Transformer models for QA |
| Apache Kafka (Apache 2.0) | Server | QA event bus |
| ClickHouse (Apache 2.0) | Server | QA score storage and analytics |

## Production Considerations

**Scaling:** The QA review queue query prioritizes calls using a weighted formula based on sentiment, duration, and complaint flags. For tenants with 10,000+ calls/day, add an index on `(tenantId, timestamp, sentimentScore)`. Automated QA scoring via NLP processes calls asynchronously — new transcriptions are published to a Kafka topic, consumed by NLP workers, and results are inserted back into ClickHouse. Scale NLP workers horizontally behind a Kafka consumer group.

**Security:** QA evaluators access call recordings and transcriptions through the review interface, which requires the `qa:evaluate` permission. Evaluators can only see calls for their assigned campaigns/queues. QA scores are visible to the agent (who can see their own scores with detailed criteria feedback), their supervisor, and administrators. Agents cannot see other agents' QA scores. Score arbitration (when two evaluators disagree) is limited to QA managers.

**Monitoring:** Track QA evaluation rate (calls evaluated per day per evaluator), average evaluation time, inter-rater reliability (correlation between two evaluators' scores), and automated QA coverage rate. Alert if the QA queue grows beyond 500 calls (indicating insufficient evaluator capacity) or if the automated QA accuracy drops below 80% (compared to manual evaluations).
