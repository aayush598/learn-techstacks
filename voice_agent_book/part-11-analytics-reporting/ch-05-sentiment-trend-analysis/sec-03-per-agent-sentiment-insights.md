# Section 03: Per-Agent Sentiment Insights

## Overview

Per-agent sentiment insights analyze the sentiment of customer interactions handled by each agent, identifying patterns in how individual agents affect customer emotional states. The system computes each agent's average customer sentiment across their handled calls, tracks sentiment trends over time, and compares agent sentiment performance against team and campaign benchmarks. These insights help supervisors identify top-performing agents (those who consistently leave customers with positive sentiment) and agents who may need coaching (those with declining or below-average sentiment scores).

The analysis includes: per-agent sentiment distribution (histogram of call sentiments), sentiment trend over the agent's tenure, sentiment by time of day (does the agent's sentiment performance vary by shift?), sentiment after specific events (training, coaching sessions), and correlation with other agent metrics (AHT, QA scores, CSAT). The system also highlights "sentiment swings" — calls where the customer sentiment changed dramatically from negative to positive (agent successfully de-escalated) or positive to negative (agent escalated a situation).

## Architecture

```
           Per-Agent Sentiment Insights Pipeline

   ClickHouse (sentiment + agent data)
        |
   Per-Agent Aggregator
        |
   ┌────┴────────────┐
   |                 |
   Metrics           Events
   (avg sentiment,   (training, coaching,
    distribution,     campaign changes)
    trend)
   |                 |
   Agent Sentiment API
        |
   Agent Scorecard Integration
   Sentiment De-escalation Highlights
   Coaching Recommendations
```

## Design Decisions

- **Rolling 30-day sentiment window over all-time average for agent comparison:** An agent's sentiment performance from 6 months ago may not reflect their current skill level. The system uses a rolling 30-day window for agent-to-agent comparisons and agent-to-benchmark comparisons. The all-time average is available in a separate "trend" view. Trade-off: agents with less than 30 days of tenure have insufficient data for comparison — they are grouped into a "new hire" benchmark group.

- **De-escalation identification using sentiment delta over absolute sentiment change:** A de-escalation event is identified when the customer sentiment in the last 25% of the call is at least 0.5 points higher than the minimum sentiment during the call. This captures calls where the agent turned a negative interaction into a positive one, even if the overall call sentiment is neutral. The delta-based approach is more robust than absolute thresholds (which vary by baseline sentiment). Trade-off: delta-based detection may flag calls where sentiment improved due to external factors (issue resolved by another system) rather than agent skill.

- **Coaching recommendation engine using correlation analysis over rule-based triggers:** Rather than using fixed rules ("sentiment < 0.2 for 2 consecutive weeks → coaching needed"), the system analyzes correlations between agent behaviors and sentiment outcomes. For example, if an agent's sentiment drops significantly when call duration exceeds 5 minutes, the recommendation might be "this agent may struggle with lengthy calls — consider time management coaching." Trade-off: correlation-based recommendations require sufficient data per agent (minimum 50 calls in the analysis window) and may suggest spurious correlations.

## Implementation Approach

```typescript
interface AgentSentimentMetrics {
  agentId: string;
  tenantId: string;
  periodStart: number;
  periodEnd: number;
  totalCalls: number;
  averageCustomerSentiment: number;
  averageAgentSentiment: number;
  sentimentDistribution: {
    positive: number;
    neutral: number;
    negative: number;
  };
  trend: 'improving' | 'declining' | 'stable';
  teamPercentile: number;
  deEscalationCount: number;
  deEscalationRate: number;    // percentage of calls with de-escalation
  sentimentSwings: Array<{
    callSid: string;
    customerName?: string;
    minSentiment: number;
    maxSentiment: number;
    delta: number;
    duration: number;
    date: string;
  }>;
  recommendations: string[];
}

class PerAgentSentimentService {
  private clickhouse: ClickHouseClient;

  async getAgentSentiment(
    agentId: string,
    tenantId: string,
    start: number,
    end: number
  ): Promise<AgentSentimentMetrics> {
    // Get call-level sentiment for this agent
    const calls = await this.clickhouse.query(`
      SELECT
        callSid,
        customerSentiment,
        agentSentiment,
        overallLabel,
        duration,
        timestamp
      FROM call_sentiment_analysis
      WHERE agentId = '${agentId}'
        AND tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      ORDER BY timestamp DESC
    `);

    if (calls.length === 0) {
      return this.emptyMetrics(agentId, tenantId, start, end);
    }

    // Compute metrics
    const totalCalls = calls.length;
    const avgCustomerSentiment = calls.reduce((s: number, c: any) => s + c.customerSentiment, 0) / totalCalls;
    const positiveCalls = calls.filter((c: any) => c.overallLabel === 'positive').length;
    const negativeCalls = calls.filter((c: any) => c.overallLabel === 'negative').length;
    const neutralCalls = totalCalls - positiveCalls - negativeCalls;

    // Identify de-escalations
    const deEscalations = await this.identifyDeEscalations(agentId, tenantId, start, end);

    // Compute team percentile
    const teamStats = await this.getTeamComparisons(agentId, tenantId, start, end);
    const percentile = this.computePercentile(avgCustomerSentiment, teamStats);

    // Generate recommendations
    const recommendations = await this.generateRecommendations(agentId, tenantId, calls, deEscalations);

    // Determine trend
    const trend = await this.computeTrend(agentId, tenantId);

    return {
      agentId,
      tenantId,
      periodStart: start,
      periodEnd: end,
      totalCalls,
      averageCustomerSentiment: avgCustomerSentiment,
      averageAgentSentiment: calls.reduce((s: number, c: any) => s + c.agentSentiment, 0) / totalCalls,
      sentimentDistribution: {
        positive: (positiveCalls / totalCalls) * 100,
        neutral: (neutralCalls / totalCalls) * 100,
        negative: (negativeCalls / totalCalls) * 100,
      },
      trend,
      teamPercentile: percentile,
      deEscalationCount: deEscalations.length,
      deEscalationRate: (deEscalations.length / totalCalls) * 100,
      sentimentSwings: deEscalations.slice(0, 10),
      recommendations,
    };
  }

  private async identifyDeEscalations(
    agentId: string,
    tenantId: string,
    start: number,
    end: number
  ): Promise<AgentSentimentMetrics['sentimentSwings']> {
    // Get calls with sentiment timeline data
    const timelineData = await this.clickhouse.query(`
      SELECT
        callSid,
        sentimentTimeline,
        duration
      FROM call_sentiment_analysis
      WHERE agentId = '${agentId}'
        AND tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
        AND sentimentTimeline != []
    `);

    const deEscalations: AgentSentimentMetrics['sentimentSwings'] = [];

    for (const call of timelineData) {
      const timeline = call.sentimentTimeline as Array<{ timeOffset: number; score: number; speaker: string }>;
      if (!timeline || timeline.length < 3) continue;

      const customerTimeline = timeline.filter(t => t.speaker === 'customer');
      if (customerTimeline.length < 3) continue;

      const minSentiment = Math.min(...customerTimeline.map(t => t.score));
      const maxSentiment = Math.max(...customerTimeline.map(t => t.score));
      const delta = maxSentiment - minSentiment;

      // De-escalation: sentiment in last 25% is >= 0.5 above minimum
      const lastQuarter = customerTimeline.slice(Math.floor(customerTimeline.length * 0.75));
      const lastQuarterAvg = lastQuarter.reduce((s, t) => s + t.score, 0) / lastQuarter.length;

      if (lastQuarterAvg - minSentiment >= 0.5) {
        deEscalations.push({
          callSid: call.callSid,
          minSentiment,
          maxSentiment,
          delta,
          duration: call.duration,
          date: new Date(call.timestamp).toISOString().split('T')[0],
        });
      }
    }

    return deEscalations.sort((a, b) => b.delta - a.delta);
  }

  private async getTeamComparisons(
    agentId: string,
    tenantId: string,
    start: number,
    end: number
  ): Promise<number[]> {
    // Get agent's team
    const agentInfo = await this.clickhouse.query(`
      SELECT teamId FROM agents WHERE agentId = '${agentId}'
    `);
    const teamId = agentInfo[0]?.teamId;
    if (!teamId) return [];

    // Get sentiment averages for all team members
    const teamData = await this.clickhouse.query(`
      SELECT agentId, avg(customerSentiment) as avgSentiment
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}'
        AND agentId IN (SELECT agentId FROM agents WHERE teamId = '${teamId}')
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY agentId
    `);

    return teamData.map((t: any) => t.avgSentiment);
  }

  private computePercentile(value: number, distribution: number[]): number {
    if (distribution.length === 0) return 50;
    const sorted = [...distribution].sort((a, b) => a - b);
    const below = sorted.filter(v => v < value).length;
    return (below / sorted.length) * 100;
  }

  private async computeTrend(agentId: string, tenantId: string): Promise<'improving' | 'declining' | 'stable'> {
    const monthlyData = await this.clickhouse.query(`
      SELECT toStartOfMonth(timestamp) as month, avg(customerSentiment) as avgSentiment
      FROM call_sentiment_analysis
      WHERE agentId = '${agentId}' AND tenantId = '${tenantId}'
        AND timestamp >= now() - INTERVAL 3 MONTH
      GROUP BY month
      ORDER BY month
    `);

    if (monthlyData.length < 2) return 'stable';
    const first = monthlyData[0].avgSentiment;
    const last = monthlyData[monthlyData.length - 1].avgSentiment;
    const diff = last - first;

    if (diff > 0.1) return 'improving';
    if (diff < -0.1) return 'declining';
    return 'stable';
  }

  private async generateRecommendations(
    agentId: string,
    tenantId: string,
    calls: any[],
    deEscalations: any[]
  ): Promise<string[]> {
    const recs: string[] = [];

    // Low sentiment
    const avg = calls.reduce((s: number, c: any) => s + c.customerSentiment, 0) / calls.length;
    if (avg < 0) {
      recs.push('Customer sentiment is below neutral. Consider empathy and active listening training.');
    }

    // No de-escalations
    if (deEscalations.length === 0 && calls.length >= 20) {
      recs.push('No de-escalation events detected. Review techniques for turning around negative interactions.');
    }

    // Sentiment drops on long calls
    const longCalls = calls.filter((c: any) => c.duration > 300); // > 5 min
    if (longCalls.length >= 10) {
      const longAvg = longCalls.reduce((s: number, c: any) => s + c.customerSentiment, 0) / longCalls.length;
      if (longAvg < avg - 0.15) {
        recs.push('Sentiment drops on calls longer than 5 minutes. Consider time management or de-escalation training for complex calls.');
      }
    }

    return recs;
  }

  private emptyMetrics(agentId: string, tenantId: string, start: number, end: number): AgentSentimentMetrics {
    return { agentId, tenantId, periodStart: start, periodEnd: end, totalCalls: 0,
      averageCustomerSentiment: 0, averageAgentSentiment: 0,
      sentimentDistribution: { positive: 0, neutral: 0, negative: 0 },
      trend: 'stable', teamPercentile: 50, deEscalationCount: 0, deEscalationRate: 0,
      sentimentSwings: [], recommendations: ['Insufficient call data for sentiment analysis.'] };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Agent-level sentiment queries |
| Apache ECharts (Apache 2.0) | Client | Sentiment distribution charts |
| Apache Kafka (Apache 2.0) | Server | Sentiment timeline event ingestion |
| Recharts (MIT) | Client | Sentiment comparison bar charts |

## Production Considerations

**Scaling:** Per-agent sentiment queries scan the `call_sentiment_analysis` table filtered by `agentId`. With an index on `(agentId, tenantId, timestamp)`, queries complete in under 50 ms for 1 year of data. The de-escalation detection queries the `sentimentTimeline` column (an array) — ClickHouse handles array operations efficiently for up to 200 segments per call.

**Security:** Per-agent sentiment insights are agent performance data — agents can view their own, supervisors can view their team's, and administrators can view all. De-escalation highlights include call SIDs and optionally customer names — access requires `calls:view-details`. Coaching recommendations are generated from data and marked as "AI-generated — review before acting."

**Monitoring:** Track per-agent sentiment query performance and de-escalation detection latency. Alert if an agent's sentiment drops by more than 0.3 in a single week — this may indicate a personal issue or training gap. Monitor the de-escalation rate per team — teams with de-escalation rates below 5% may need training on conflict resolution.
