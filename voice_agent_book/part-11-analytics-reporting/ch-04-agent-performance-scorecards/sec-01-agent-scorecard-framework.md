# Section 01: Agent Scorecard Framework

## Overview

The agent scorecard framework provides a structured system for evaluating agent performance across multiple dimensions: productivity metrics (calls handled, AHT, occupancy), quality metrics (QA scores, compliance), customer experience metrics (CSAT, sentiment), and operational metrics (adherence, punctuality). Scorecards are configurable — each tenant can define their own scoring formula, weighting each dimension according to their business priorities. Scores are computed automatically from platform data and updated daily, weekly, and monthly.

The framework supports multiple scorecard templates (e.g., "Inbound Support Agent," "Outbound Sales Agent," "Team Lead"), each with different weightings and target thresholds. Agents can view their own scorecards with detailed breakdowns showing which areas they excel in and which need improvement. Supervisors see their team's scorecards with ranking and benchmark comparisons. Historical scorecard data is used for performance reviews, promotion decisions, and coaching targeting.

## Architecture

```
              Agent Scorecard Framework

   Platform Data Stream → Scorecard Engine
                              |
                    ┌─────────┴──────────┐
                    |                    |
              Score Calculator      Template Config
              (daily/weekly/       (PostgreSQL)
               monthly rollup)
                    |                   
              ClickHouse (scores)
                    |
              Scorecard API / GraphQL
                    |
              Agent Scorecard View
              Team Scoreboard
              Trend Comparison
```

## Design Decisions

- **Configurable templates with weighted dimensions over a fixed scoring formula:** A sales-focused contact center may weight call volume and conversion heavily, while a support center weights CSAT and FCR. Templates allow each tenant to define their own scoring formula: each dimension has a weight (0-100%), and the overall score is the weighted sum of dimension scores (normalized to 0-100). Trade-off: configurability adds complexity to the UI (template editor) and increases the risk of poorly designed scorecards that misrepresent performance.

- **Automated score computation from platform data over manual supervisor input:** Scores for productivity, schedule adherence, and customer sentiment are computed automatically from call events, agent state transitions, and post-call surveys. Only QA scores require manual supervisor input (and even those are partially automated through transcription-based QA scoring). This reduces the administrative burden on supervisors and ensures scorecards are always up to date. Trade-off: automated scores may miss context that a human evaluator would catch (e.g., a long AHT due to a genuinely complex issue).

- **Score normalization with historical baseline over absolute thresholds:** A score of 85/100 means different things in different campaigns or time periods. The system normalizes scores using the tenant's historical performance distribution — a raw metric is converted to a percentile rank against the last 30 days of data. This ensures scorecards remain fair as baseline performance improves. Trade-off: normalized scores can be confusing to agents who see their score change even though their raw performance stayed the same (if the team average improved).

## Implementation Approach

```typescript
interface ScorecardTemplate {
  id: string;
  name: string;
  tenantId: string;
  description: string;
  dimensions: ScorecardDimension[];
  overallScoreFormula: 'weighted_sum' | 'average' | 'min_dimension';
  targets: {
    overall: { warning: number; critical: number };
    perDimension: Record<string, { warning: number; critical: number }>;
  };
  schedule: 'daily' | 'weekly' | 'monthly';
  createdAt: number;
  updatedAt: number;
}

interface ScorecardDimension {
  name: string;
  weight: number;                // 0-100, all weights must sum to 100
  metricKey: string;             // e.g., 'aht', 'csat', 'occupancy'
  aggregation: 'avg' | 'p95' | 'count';
  normalization: 'percentile' | 'z_score' | 'raw' | 'inverse_percentile';
  direction: 'higher_is_better' | 'lower_is_better';
  targetValue: number;
}

interface AgentScore {
  agentId: string;
  tenantId: string;
  templateId: string;
  periodStart: number;
  periodEnd: number;
  overallScore: number;          // 0-100
  dimensions: Array<{
    name: string;
    rawValue: number;
    normalizedScore: number;     // 0-100
    weight: number;
    contribution: number;        // weight * normalizedScore / 100
  }>;
  trend: 'improving' | 'declining' | 'stable';
  rank?: number;                 // within team or tenant
  percentile?: number;
}

class ScorecardEngine {
  private clickhouse: ClickHouseClient;
  private templates: Map<string, ScorecardTemplate> = new Map();

  async computeScores(
    templateId: string,
    tenantId: string,
    periodStart: number,
    periodEnd: number
  ): Promise<Map<string, AgentScore>> {
    const template = this.templates.get(templateId);
    if (!template) throw new Error(`Template ${templateId} not found`);

    const agents = await this.getAgents(tenantId);
    const scores = new Map<string, AgentScore>();

    for (const agentId of agents) {
      const score = await this.computeAgentScore(
        agentId,
        tenantId,
        template,
        periodStart,
        periodEnd
      );
      scores.set(agentId, score);
    }

    // Compute ranks and percentiles
    const sortedScores = Array.from(scores.values())
      .sort((a, b) => b.overallScore - a.overallScore);

    sortedScores.forEach((score, idx) => {
      score.rank = idx + 1;
      score.percentile = ((sortedScores.length - idx - 1) / sortedScores.length) * 100;
    });

    return scores;
  }

  private async computeAgentScore(
    agentId: string,
    tenantId: string,
    template: ScorecardTemplate,
    periodStart: number,
    periodEnd: number
  ): Promise<AgentScore> {
    const dimensionScores: AgentScore['dimensions'] = [];
    let overallScore = 0;

    for (const dim of template.dimensions) {
      const rawValue = await this.queryMetric(
        agentId,
        tenantId,
        dim.metricKey,
        dim.aggregation,
        periodStart,
        periodEnd
      );

      const normalizedScore = await this.normalizeScore(
        rawValue,
        dim,
        tenantId,
        periodStart
      );

      const contribution = (dim.weight * normalizedScore) / 100;
      overallScore += contribution;

      dimensionScores.push({
        name: dim.name,
        rawValue,
        normalizedScore,
        weight: dim.weight,
        contribution,
      });
    }

    // Determine trend
    const previousScore = await this.getPreviousScore(agentId, template.id, periodStart);
    const trend = previousScore != null
      ? overallScore > previousScore ? 'improving'
        : overallScore < previousScore ? 'declining' : 'stable'
      : 'stable';

    return {
      agentId,
      tenantId,
      templateId: template.id,
      periodStart,
      periodEnd,
      overallScore: Math.round(overallScore * 100) / 100,
      dimensions: dimensionScores,
      trend,
    };
  }

  private async normalizeScore(
    rawValue: number,
    dim: ScorecardDimension,
    tenantId: string,
    periodStart: number
  ): Promise<number> {
    const thirtyDaysAgo = periodStart - 30 * 24 * 3600 * 1000;

    switch (dim.normalization) {
      case 'percentile': {
        // Get historical distribution
        const histResult = await this.clickhouse.query(`
          SELECT count() as total,
                 countIf(value < ${rawValue}) as belowCount
          FROM daily_metric_rollups
          WHERE tenantId = '${tenantId}'
            AND metric = '${dim.metricKey}'
            AND timestamp >= ${thirtyDaysAgo}
            AND timestamp < ${periodStart}
        `);

        const total = histResult[0]?.total ?? 0;
        const belowCount = histResult[0]?.belowCount ?? 0;
        const percentile = total > 0 ? (belowCount / total) * 100 : 50;

        if (dim.direction === 'lower_is_better') {
          return 100 - percentile;
        }
        return percentile;
      }

      case 'inverse_percentile': {
        // Same as percentile but inverted
        const result = await this.clickhouse.query(`
          SELECT count() as total,
                 countIf(value > ${rawValue}) as aboveCount
          FROM daily_metric_rollups
          WHERE tenantId = '${tenantId}'
            AND metric = '${dim.metricKey}'
            AND timestamp >= ${thirtyDaysAgo}
            AND timestamp < ${periodStart}
        `);
        const total = result[0]?.total ?? 0;
        const aboveCount = result[0]?.aboveCount ?? 0;
        return total > 0 ? (aboveCount / total) * 100 : 50;
      }

      case 'raw': {
        // Direct percentage of target
        if (dim.direction === 'higher_is_better') {
          return Math.min(100, (rawValue / dim.targetValue) * 100);
        }
        return Math.min(100, (dim.targetValue / Math.max(rawValue, 0.01)) * 100);
      }

      default:
        return 50;
    }
  }

  private async queryMetric(
    agentId: string,
    tenantId: string,
    metricKey: string,
    aggregation: string,
    start: number,
    end: number
  ): Promise<number> {
    const aggFn = aggregation === 'p95' ? 'quantile(0.95)' : aggregation;

    const result = await this.clickhouse.query(`
      SELECT ${aggFn}(value) as val
      FROM daily_metric_rollups
      WHERE agentId = '${agentId}'
        AND tenantId = '${tenantId}'
        AND metric = '${metricKey}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    return result[0]?.val ?? 0;
  }

  private async getPreviousScore(
    agentId: string,
    templateId: string,
    currentPeriodStart: number
  ): Promise<number | null> {
    // Find the previous scorecard period
    const result = await this.clickhouse.query(`
      SELECT overallScore
      FROM agent_scorecards
      WHERE agentId = '${agentId}'
        AND templateId = '${templateId}'
        AND periodEnd <= ${currentPeriodStart}
      ORDER BY periodEnd DESC
      LIMIT 1
    `);
    return result[0]?.overallScore ?? null;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Scorecard computation |
| PostgreSQL (PostgreSQL) | Server | Template configuration storage |
| React Table (MIT) | Client | Scoreboard table rendering |
| Recharts (MIT) | Client | Score trend visualization |

## Production Considerations

**Scaling:** Scorecard computation runs as a scheduled job (daily, weekly, monthly) and processes all agents in a tenant. For tenants with 500+ agents, the computation is parallelized across worker processes (one per 100 agents). Results are written to ClickHouse and cached in Redis for dashboard queries. Historical scorecards are retained indefinitely for annual review purposes.

**Security:** Scorecard access follows the agent-supervisor hierarchy: agents see only their own scorecards, supervisors see their team's scorecards, administrators see all. The API enforces this through a team membership query before returning results. Scorecard templates are tenant-scoped and cannot be shared across tenants. Raw dimension values for sensitive metrics (AHT, occupancy) require the same permissions as the underlying metric.

**Monitoring:** Track scorecard computation job duration and success/failure rate. Alert if the daily scorecard computation fails to complete within the expected window (typically <10 minutes for 500 agents). Monitor score distribution — if all agents score above 90 or below 50, the normalization or weighting may need adjustment. Track the number of agents without scorecards (potential data quality issue if events are missing for an agent).
