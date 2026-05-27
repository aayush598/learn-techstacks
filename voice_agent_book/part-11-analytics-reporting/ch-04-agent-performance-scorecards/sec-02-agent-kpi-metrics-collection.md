# Section 02: Agent KPI Metrics Collection

## Overview

Agent KPI metrics collection is the data acquisition layer that gathers raw performance data from across the voice agent platform and feeds it into the scorecard engine. It collects data from multiple sources: call events (handled calls, talk time, hold time, ACW), agent state transitions (logged-in time, break time, training time), quality assurance scores (from manual QA reviews and automated transcription analysis), customer feedback (post-call surveys, CSAT, NPS), and compliance events (call recording consent, data protection checks).

The collection pipeline runs continuously, processing events from Kafka in real-time and writing aggregated metrics to ClickHouse for scorecard computation. Each metric has a defined collection interval (some are per-call, others are per-shift, others are daily), and the pipeline handles late-arriving data (e.g., QA scores entered hours after the call). Data quality checks validate that metrics are within expected ranges and that no data is missing for active agents.

## Architecture

```
              Agent KPI Metrics Collection

   Kafka Events (call, state, survey, QA)
        |
   KPI Collector (stream processor)
        |
   ┌────┴──────────────┐
   |                   |
   Per-Call Metrics    Per-Shift Metrics    Per-Day Metrics
   (AHT, handle time,  (occupancy,          (CSAT, QA scores,
    hold time)          adherence)           sentiment)
   |                   |                    |
   └────────┬──────────┴────────────────────┘
            |
      ClickHouse tables
      (agent_metrics_hourly,
       agent_metrics_daily)
            |
      Scorecard Engine
```

## Design Decisions

- **Event-sourced metrics over periodic polling:** Rather than polling APIs for agent state, the pipeline consumes agent state transition events from Kafka. This provides near-real-time updates and ensures no data is missed between polls. The Kafka topic has a 7-day retention, allowing replay of any missing data. Trade-off: event-sourced systems depend on reliable event emission; if the agent desktop fails to emit state change events, the metrics will be incomplete.

- **Two-tier aggregation (hourly + daily) over single-tier:** Per-call metrics are first aggregated into hourly buckets, then rolled up into daily buckets. This allows real-time scorecard updates within the current day (showing "today so far" scores) while maintaining efficient historical queries. Trade-off: two-tier aggregation doubles storage requirements, but ClickHouse's columnar compression makes this negligible.

- **Late data handling with reprocessing window over strict cutoffs:** QA scores and survey responses may arrive hours or days after the call. The collector accepts late data within a 72-hour window, updating the relevant hourly/daily aggregates. After 72 hours, late data is stored in a separate table for manual reconciliation. Trade-off: late data updates can cause scorecard values to shift after they've been viewed; the system shows a "last updated" timestamp to manage expectations.

## Implementation Approach

```typescript
interface AgentKpiEvent {
  type: 'call_completed' | 'state_transition' | 'qa_score' | 'survey_response';
  agentId: string;
  tenantId: string;
  timestamp: number;
  data: Record<string, unknown>;
}

interface AgentHourlyMetrics {
  agentId: string;
  tenantId: string;
  date: string;
  hour: number;
  callsHandled: number;
  talkTimeSeconds: number;
  holdTimeSeconds: number;
  acwTimeSeconds: number;
  loggedInSeconds: number;
  breakSeconds: number;
  trainingSeconds: number;
  averageSentiment: number;
  csatCount: number;
  csatSum: number;
  qaScoreCount: number;
  qaScoreSum: number;
  // Computed
  ahtSeconds: number;
  occupancy: number;
  adherence: number;
}

class KpiCollector {
  private clickhouse: ClickHouseClient;
  private kafka: KafkaConsumer;
  private pendingUpdates: Map<string, AgentHourlyMetrics> = new Map();

  async start(): Promise<void> {
    await this.kafka.subscribe({
      topics: ['agent.call.completed', 'agent.state.transition', 'agent.qa.scored', 'agent.survey.response'],
      groupId: 'kpi-collector',
      eachMessage: async ({ topic, message }) => {
        const event: AgentKpiEvent = JSON.parse(message.value.toString());
        await this.processEvent(event);
      },
    });
  }

  async processEvent(event: AgentKpiEvent): Promise<void> {
    switch (event.type) {
      case 'call_completed':
        await this.processCallCompleted(event);
        break;
      case 'state_transition':
        await this.processStateTransition(event);
        break;
      case 'qa_score':
        await this.processQaScore(event);
        break;
      case 'survey_response':
        await this.processSurveyResponse(event);
        break;
    }
  }

  private async processCallCompleted(event: AgentKpiEvent): Promise<void> {
    const { agentId, tenantId, timestamp, data } = event;
    const hour = this.getHourBucket(timestamp);
    const date = this.getDateString(timestamp);
    const key = `${agentId}:${date}:${hour}`;

    const callData = data as {
      talkTimeSeconds: number;
      holdTimeSeconds: number;
      acwTimeSeconds: number;
      sentimentScore?: number;
    };

    // Upsert hourly metrics
    await this.clickhouse.insert(`INSERT INTO agent_metrics_hourly
      (agentId, tenantId, date, hour, callsHandled, talkTimeSeconds,
       holdTimeSeconds, acwTimeSeconds, loggedInSeconds, breakSeconds,
       trainingSeconds, averageSentiment, csatCount, csatSum,
       qaScoreCount, qaScoreSum)
      VALUES
      ('${agentId}', '${tenantId}', '${date}', ${hour},
       1, ${callData.talkTimeSeconds}, ${callData.holdTimeSeconds},
       ${callData.acwTimeSeconds}, 0, 0, 0,
       ${callData.sentimentScore ?? 0}, 0, 0, 0, 0)
      ON CONFLICT (agentId, date, hour)
      DO UPDATE SET
        callsHandled = agent_metrics_hourly.callsHandled + 1,
        talkTimeSeconds = agent_metrics_hourly.talkTimeSeconds + ${callData.talkTimeSeconds},
        holdTimeSeconds = agent_metrics_hourly.holdTimeSeconds + ${callData.holdTimeSeconds},
        acwTimeSeconds = agent_metrics_hourly.acwTimeSeconds + ${callData.acwTimeSeconds},
        averageSentiment = (agent_metrics_hourly.averageSentiment * (agent_metrics_hourly.callsHandled) + ${callData.sentimentScore ?? 0}) / (agent_metrics_hourly.callsHandled + 1)
    `);
  }

  private async processStateTransition(event: AgentKpiEvent): Promise<void> {
    const { agentId, tenantId, timestamp, data } = event;
    const stateData = data as { fromState: string; toState: string; durationSeconds: number };

    const hour = this.getHourBucket(timestamp);
    const date = this.getDateString(timestamp);

    const columnMap: Record<string, string> = {
      'available': 'loggedInSeconds',
      'on_call': 'loggedInSeconds',
      'acw': 'loggedInSeconds',
      'break': 'breakSeconds',
      'training': 'trainingSeconds',
    };

    const column = columnMap[stateData.toState];
    if (!column) return;

    await this.clickhouse.query(`
      INSERT INTO agent_metrics_hourly
      (agentId, tenantId, date, hour, ${column})
      VALUES
      ('${agentId}', '${tenantId}', '${date}', ${hour}, ${stateData.durationSeconds})
      ON CONFLICT (agentId, date, hour)
      DO UPDATE SET
        ${column} = agent_metrics_hourly.${column} + ${stateData.durationSeconds}
    `);
  }

  private async processQaScore(event: AgentKpiEvent): Promise<void> {
    const { agentId, tenantId, timestamp, data } = event;
    const qaData = data as { score: number; maxScore: number };
    const hour = this.getHourBucket(timestamp);
    const date = this.getDateString(timestamp);

    const normalizedScore = (qaData.score / qaData.maxScore) * 100;

    await this.clickhouse.query(`
      INSERT INTO agent_metrics_hourly
      (agentId, tenantId, date, hour, qaScoreCount, qaScoreSum)
      VALUES
      ('${agentId}', '${tenantId}', '${date}', ${hour}, 1, ${normalizedScore})
      ON CONFLICT (agentId, date, hour)
      DO UPDATE SET
        qaScoreCount = agent_metrics_hourly.qaScoreCount + 1,
        qaScoreSum = agent_metrics_hourly.qaScoreSum + ${normalizedScore}
    `);
  }

  private async processSurveyResponse(event: AgentKpiEvent): Promise<void> {
    const { agentId, tenantId, timestamp, data } = event;
    const surveyData = data as { csatScore?: number; npsScore?: number };
    const hour = this.getHourBucket(timestamp);
    const date = this.getDateString(timestamp);

    if (surveyData.csatScore != null) {
      await this.clickhouse.query(`
        INSERT INTO agent_metrics_hourly
        (agentId, tenantId, date, hour, csatCount, csatSum)
        VALUES
        ('${agentId}', '${tenantId}', '${date}', ${hour}, 1, ${surveyData.csatScore})
        ON CONFLICT (agentId, date, hour)
        DO UPDATE SET
          csatCount = agent_metrics_hourly.csatCount + 1,
          csatSum = agent_metrics_hourly.csatSum + ${surveyData.csatScore}
      `);
    }
  }

  // Daily rollup job (runs hourly, after the hour ends)
  async runDailyRollup(date: string): Promise<void> {
    await this.clickhouse.query(`
      INSERT INTO agent_metrics_daily
      (agentId, tenantId, date,
       callsHandled, talkTimeSeconds, holdTimeSeconds, acwTimeSeconds,
       loggedInSeconds, breakSeconds, trainingSeconds,
       averageSentiment, averageCsat, averageQaScore)
      SELECT
        agentId, tenantId, '${date}' as date,
        sum(callsHandled), sum(talkTimeSeconds), sum(holdTimeSeconds), sum(acwTimeSeconds),
        sum(loggedInSeconds), sum(breakSeconds), sum(trainingSeconds),
        avg(averageSentiment), avg(csatSum / nullif(csatCount, 0)), avg(qaScoreSum / nullif(qaScoreCount, 0))
      FROM agent_metrics_hourly
      WHERE date = '${date}'
      GROUP BY agentId, tenantId
    `);
  }

  private getHourBucket(timestamp: number): number {
    return new Date(timestamp).getHours();
  }

  private getDateString(timestamp: number): string {
    return new Date(timestamp).toISOString().split('T')[0];
  }
}

// Data quality check
async function validateAgentMetrics(agentId: string, date: string): Promise<string[]> {
  const issues: string[] = [];
  const daily = await clickhouse.query(`
    SELECT * FROM agent_metrics_daily
    WHERE agentId = '${agentId}' AND date = '${date}'
  `);

  if (daily.length === 0) {
    issues.push(`No metrics found for ${agentId} on ${date}`);
    return issues;
  }

  const m = daily[0];
  if (m.callsHandled === 0 && m.loggedInSeconds > 1800) {
    issues.push('Agent logged in but handled 0 calls');
  }
  if (m.averageSentiment === 0 && m.callsHandled > 10) {
    issues.push('No sentiment data for handled calls');
  }
  if (m.occupancy > 100) {
    issues.push('Occupancy exceeds 100% — possible state tracking error');
  }

  return issues;
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache Kafka (Apache 2.0) | Server | Agent event ingestion |
| ClickHouse (Apache 2.0) | Server | Metrics storage (hourly+daily) |
| Apache Flink (Apache 2.0) | Server | Stream processing for KPI collection |
| kafkajs (MIT) | Server | Kafka consumer client |

## Production Considerations

**Scaling:** The KPI collector is a Kafka consumer group with configurable parallelism (one consumer per partition). For high-volume tenants (1000+ agents x 200 calls/agent/day = 200K events/day), start with 6 partitions per topic. ClickHouse `INSERT ON CONFLICT` updates hourly metrics efficiently with the MergeTree engine. The daily rollup job processes all agents in a single query and completes in under 10 seconds for 500 agents.

**Security:** The collector processes events that contain agent IDs and tenant IDs. No PII is processed in the KPI collector (caller identities are not included in agent metric events). The ClickHouse tables are access-controlled — only the collector and the scorecard engine have write access; the dashboard API has read-only access.

**Monitoring:** Track event processing rate (events/second), event processing lag (time from event creation to metric insertion), and late data rate (events arriving > 1 hour late). Alert if processing lag exceeds 5 minutes or if the late data rate exceeds 5% of total events. Monitor the daily rollup job completion time and alert if it fails. Track the number of agents with missing metrics for the current day (potential data pipeline issue).
