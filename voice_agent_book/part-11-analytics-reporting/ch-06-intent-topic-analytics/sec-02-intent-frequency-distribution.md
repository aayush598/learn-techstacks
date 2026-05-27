# Section 02: Intent Frequency Distribution

## Overview

Intent frequency distribution analysis reveals how caller needs are distributed across the defined intent taxonomy. It answers questions like: "What percentage of calls are about billing vs technical support?," "Which sub-intents are most common?," "How does intent distribution vary by campaign, queue, or time of day?" The system computes frequency counts and percentages for each intent at every level of the hierarchy, along with trends and comparisons.

The distribution is visualized as a treemap (area proportional to call volume, color-coded by intent category), a sunburst chart (hierarchical drill-down), a horizontal bar chart (sorted by frequency), and a data table with counts. Users can filter by date range, campaign, queue, agent team, and customer segment. The system also flags significant changes in intent distribution compared to the previous period — a sudden spike in "Password Reset" intents may indicate a system issue.

## Architecture

```
           Intent Frequency Pipeline

   ClickHouse (call_intents table)
        |
   Intent Frequency Aggregator
   (hourly, daily rollups)
        |
   ┌────┴────────────┐
   |                 |
   ClickHouse        Redis Cache
   (pre-aggregated   (top-N intents,
    tables)           frequency summary)
   |                 |
   Intent Distribution API
        |
   Treemap / Sunburst / Bar Chart / Table
   Filter Controls (date, campaign, queue)
```

## Design Decisions

- **Pre-aggregated frequency tables at multiple granularities over query-time aggregation:** Intent frequency queries are among the most common dashboard queries. Pre-aggregating by hour, day, and week in ClickHouse materialized views makes these queries sub-second. The pre-aggregated tables store counts per (intentId, dimension, period), enabling drill-down without querying raw data. Trade-off: pre-aggregation adds a 1-hour delay for the latest data; real-time counters (last 60 minutes) use a Redis hash that is updated as intents are classified.

- **Normalized frequency (percentage) over raw counts for comparison:** Raw call volume varies by seasonality (Mondays are busier than Sundays), making raw intent count comparisons misleading. The system computes both raw counts and normalized percentages (intent count / total calls with any intent in the period). Percentages enable fair comparison across different time periods and segments. Trade-off: percentages can be unstable for small sample sizes (e.g., 3 calls on Sunday, 2 are billing = 67% billing); the system shows a "low sample" warning when total calls < 50.

- **Change detection with confidence intervals over simple delta:** A change in intent frequency from 10% to 15% may be noise or a real shift. The system applies a two-proportion z-test to determine whether the change is statistically significant, with a confidence level of 95%. Significant increases are highlighted in red, significant decreases in green, and non-significant changes are shown in gray. Trade-off: statistical significance requires a minimum sample size (50 calls per period) and may not detect small but operationally important shifts.

## Implementation Approach

```typescript
interface IntentFrequencyResult {
  intentId: string;
  intentName: string;
  level: number;
  parentId?: string;
  parentName?: string;
  callCount: number;
  frequency: number;            // percentage of total calls with intent
  previousFrequency?: number;   // previous period percentage
  change?: number;              // percentage point change
  significant?: boolean;        // statistically significant change
  children?: IntentFrequencyResult[];
  trend: 'increasing' | 'decreasing' | 'stable';
}

interface FrequencyQuery {
  tenantId: string;
  start: number;
  end: number;
  granularity: 'hour' | 'day' | 'week';
  level: number;                // 1, 2, or 3
  filters?: {
    campaignId?: string;
    queueId?: string;
    agentTeamId?: string;
  };
  includeChange?: boolean;
}

class IntentFrequencyService {
  private clickhouse: ClickHouseClient;
  private redis: Redis;

  async getIntentFrequency(query: FrequencyQuery): Promise<IntentFrequencyResult[]> {
    const cacheKey = `intent:freq:${JSON.stringify(query)}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Get total calls with intents in the period
    const totalResult = await this.getTotalCalls(query);
    const totalCalls = totalResult[0]?.total ?? 1;

    // Get frequency for each intent at the requested level
    const conditions = this.buildConditions(query);
    const results = await this.clickhouse.query(`
      SELECT
        ci.intentId,
        id.name as intentName,
        id.parentId,
        ip.name as parentName,
        count(DISTINCT ci.callSid) as callCount
      FROM call_intents ci
      JOIN intent_definitions id ON ci.intentId = id.id
      LEFT JOIN intent_definitions ip ON id.parentId = ip.id
      WHERE ${conditions.join(' AND ')}
        AND id.level = ${query.level}
      GROUP BY ci.intentId, id.name, id.parentId, ip.name
      ORDER BY callCount DESC
    `);

    let frequencies: IntentFrequencyResult[] = results.map((r: any) => ({
      intentId: r.intentId,
      intentName: r.intentName,
      level: query.level,
      parentId: r.parentId,
      parentName: r.parentName,
      callCount: r.callCount,
      frequency: (r.callCount / totalCalls) * 100,
      trend: 'stable',
    }));

    // Get previous period data for change detection
    if (query.includeChange) {
      const periodDuration = query.end - query.start;
      const previousQuery = { ...query, start: query.start - periodDuration, end: query.start };
      const previousTotal = await this.getTotalCalls(previousQuery);
      const previousTotalCalls = previousTotal[0]?.total ?? 1;

      const previousResults = await this.clickhouse.query(`
        SELECT intentId, count(DISTINCT callSid) as callCount
        FROM call_intents
        WHERE ${this.buildConditions(previousQuery).join(' AND ')}
        GROUP BY intentId
      `);
      const prevMap = new Map(previousResults.map((r: any) => [r.intentId, r.callCount]));

      frequencies = frequencies.map(f => {
        const prevCount = prevMap.get(f.intentId) ?? 0;
        const prevFreq = (prevCount / previousTotalCalls) * 100;
        const change = f.frequency - prevFreq;
        const significant = this.isChangeSignificant(f.callCount, totalCalls, prevCount, previousTotalCalls);

        return {
          ...f,
          previousFrequency: prevFreq,
          change,
          significant,
          trend: Math.abs(change) < 1 ? 'stable'
            : change > 0 ? 'increasing' : 'decreasing',
        };
      });
    }

    // Get children for level 1 (sub-intent breakdown)
    if (query.level === 1) {
      for (const freq of frequencies) {
        const childQuery = { ...query, level: query.level + 1, filters: { ...query.filters } };
        // Add parent intent filter
        freq.children = await this.getIntentFrequency({
          ...childQuery,
          filters: { ...childQuery.filters },
        });
        // Filter children belonging to this parent
        freq.children = freq.children.filter(c => c.parentId === freq.intentId);
      }
    }

    await this.redis.setex(cacheKey, 600, JSON.stringify(frequencies));
    return frequencies;
  }

  private async getTotalCalls(query: FrequencyQuery): Promise<any[]> {
    const conditions = this.buildConditions(query);
    return this.clickhouse.query(`
      SELECT count(DISTINCT callSid) as total
      FROM call_intents
      WHERE ${conditions.join(' AND ')}
    `);
  }

  private buildConditions(query: FrequencyQuery): string[] {
    const conditions = [
      `tenantId = '${query.tenantId}'`,
      `timestamp >= ${query.start}`,
      `timestamp <= ${query.end}`,
    ];

    if (query.filters?.campaignId) conditions.push(`campaignId = '${query.filters.campaignId}'`);
    if (query.filters?.queueId) conditions.push(`queueId = '${query.filters.queueId}'`);
    if (query.filters?.agentTeamId) conditions.push(`agentTeamId = '${query.filters.agentTeamId}'`);

    return conditions;
  }

  private isChangeSignificant(
    currentCount: number,
    currentTotal: number,
    previousCount: number,
    previousTotal: number,
    alpha: number = 0.05
  ): boolean {
    if (currentTotal < 50 || previousTotal < 50) return false;

    const p1 = currentCount / currentTotal;
    const p2 = previousCount / previousTotal;
    const p = (currentCount + previousCount) / (currentTotal + previousTotal);

    const se = Math.sqrt(p * (1 - p) * (1 / currentTotal + 1 / previousTotal));
    if (se === 0) return false;

    const z = Math.abs(p1 - p2) / se;
    return z > 1.96; // z-score for alpha=0.05 (two-tailed)
  }
}

// Intent treemap component
const IntentTreemap: React.FC<{
  data: IntentFrequencyResult[];
  onDrill: (intentId: string) => void;
}> = ({ data, onDrill }) => (
  <div className="intent-treemap">
    <TreemapChart
      data={data.map(d => ({
        name: d.intentName,
        value: d.callCount,
        color: d.change != null
          ? d.change > 2 ? '#E74C3C' : d.change < -2 ? '#2ECC71' : '#3498DB'
          : '#3498DB',
        onClick: () => d.children && onDrill(d.intentId),
      }))}
    />
    {data.length === 0 && <EmptyState message="No intent data for the selected period." />}
  </div>
);

// Frequency bar chart
const IntentFrequencyBarChart: React.FC<{
  data: IntentFrequencyResult[];
}> = ({ data }) => (
  <HorizontalBarChart
    data={data.slice(0, 15).map(d => ({
      label: d.intentName,
      value: d.frequency,
      change: d.change,
      significant: d.significant,
    }))}
    xLabel="% of Calls"
  />
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Frequency aggregation |
| Redis (RSAL) | Server | Query result cache |
| Apache ECharts (Apache 2.0) | Client | Treemap and sunburst charts |
| Recharts (MIT) | Client | Bar chart visualization |

## Production Considerations

**Scaling:** Pre-aggregated frequency tables are small — one row per (intentId, date, dimension). For 100 intents × 365 days × 50 dimensions = 1.8M rows/year, easily handled by ClickHouse. Real-time counters for the last 60 minutes use Redis hashes with 1-hour TTL. The two-proportion z-test is computed server-side in Node.js (not SQL) because it involves intermediate calculations not easily expressed in ClickHouse.

**Security:** Intent frequency data is aggregated and shows percentages across all calls. It does not expose individual call or caller data. However, filtering to a single queue or campaign with low call volume could allow inferring specific call patterns — access requires `analytics:view` permission. Intent definitions are tenant-scoped.

**Monitoring:** Track intent frequency query performance (p95 < 100 ms for pre-aggregated queries). Alert if the intent frequency aggregation job fails. Monitor the percentage of calls with no intent classified — if it exceeds 20%, trigger an alert for the ML engineering team.
