# Section 06: Benchmark Comparison Views

## Overview

Benchmark comparison views provide context for agent performance by comparing individual agent metrics against team averages, campaign averages, tenant-wide averages, and industry benchmarks. These views help supervisors identify top performers (for recognition and best-practice sharing) and bottom performers (for coaching interventions). Benchmarks are computed for all scorecard dimensions: AHT, CSAT, QA score, occupancy, adherence, call volume, and sentiment.

The system computes benchmarks at multiple levels: within-team (agent vs team average), within-campaign (agent vs campaign average), within-role (agents with similar roles), and against historical performance (agent's current vs their own past). Benchmarks are displayed as percentile rankings, radar charts comparing the agent to the team average, and "scorecard vs peer" comparison tables. The visualization uses color coding: green (above average), yellow (at average), red (below average).

## Architecture

```
           Benchmark Comparison Pipeline

   Scorecard Engine → Benchmark Calculator
                          |
               ┌──────────┴──────────┐
               |                     |
         Within-Team           Cross-Tenant
         Benchmarks           Benchmarks (optional)
         (avg, p50, p95)      (anonymized)
               |                     |
         ClickHouse            Benchmark API
         (benchmark            (industry data
          snapshots)            provider)
               |
         Dashboard Widgets
         (radar chart, bar chart,
          percentile rank, comparison table)
```

## Design Decisions

- **Dynamic peer groups over fixed comparison groups:** Rather than always comparing an agent to their assigned team, the system allows supervisors to define custom peer groups (e.g., "all agents with tenure < 6 months," "all agents handling sales campaigns," "all agents on the night shift"). This enables more relevant comparisons — a new hire should be benchmarked against other new hires, not against 10-year veterans. Trade-off: dynamic peer groups require additional computation to create and cache; pre-compute the most common peer groups daily.

- **Percentile-based benchmarks over mean-based:** "You are in the 75th percentile for CSAT" is more informative than "your CSAT is 10% above average" because it accounts for the distribution shape. The system computes percentiles for each metric within each peer group and displays the agent's percentile rank. For metrics where higher is better (CSAT, QA), 90th percentile is good; for metrics where lower is better (AHT, ASA), 10th percentile is good. Trade-off: percentile computation requires sorting all peer group members, which is O(n log n) per metric per peer group.

- **Industry benchmark data via licensed data providers over self-reported benchmarks:** Self-reported benchmarks from the tenant's own data are limited — they only show relative performance within the organization. Industry benchmarks (provided by firms like BenchmarkPortal, SQM Group, or DMG Consulting) show how the contact center performs against industry peers. The system integrates with these providers' APIs to overlay industry benchmark lines on charts. Trade-off: industry benchmark data is expensive and must be refreshed periodically; not all tenants choose to license it.

## Implementation Approach

```typescript
interface BenchmarkConfig {
  tenantId: string;
  peerGroupId: string;
  name: string;
  description: string;
  membershipCriteria: {
    byTeam?: string[];
    byCampaign?: string[];
    byRole?: string[];
    byTenure?: { minMonths: number; maxMonths: number };
    byShift?: string[];
  };
  metrics: string[];           // metrics to benchmark
  updateSchedule: 'daily' | 'weekly';
}

interface BenchmarkResult {
  agentId: string;
  peerGroupId: string;
  periodStart: number;
  periodEnd: number;
  metrics: Array<{
    metricKey: string;
    agentValue: number;
    peerGroupAverage: number;
    peerGroupP50: number;
    peerGroupP75: number;
    peerGroupP90: number;
    peerGroupP10: number;
    agentPercentile: number;       // 0-100
    relativePerformance: 'above_average' | 'at_average' | 'below_average' | 'top_performer';
    industryBenchmark?: number;
  }>;
  overallRank: number;
  overallPercentile: number;
}

class BenchmarkEngine {
  private clickhouse: ClickHouseClient;
  private peerGroups: Map<string, BenchmarkConfig> = new Map();

  async computeBenchmarks(
    peerGroupId: string,
    tenantId: string,
    periodStart: number,
    periodEnd: number
  ): Promise<Map<string, BenchmarkResult>> {
    const config = this.peerGroups.get(peerGroupId);
    if (!config) throw new Error(`Peer group ${peerGroupId} not found`);

    // Get members of this peer group
    const members = await this.getPeerGroupMembers(config);
    if (members.length < 3) return new Map(); // Need at least 3 for meaningful benchmarks

    // Get metric values for all members
    const memberMetrics = await this.getMemberMetrics(members, config.metrics, periodStart, periodEnd);
    if (memberMetrics.length === 0) return new Map();

    const results = new Map<string, BenchmarkResult>();

    for (const member of members) {
      const memberData = memberMetrics.filter((m: any) => m.agentId === member);
      if (memberData.length === 0) continue;

      const metrics = config.metrics.map(metricKey => {
        const values = memberMetrics
          .filter((m: any) => m.metricKey === metricKey)
          .map((m: any) => m.value)
          .sort((a: number, b: number) => a - b);

        const agentValue = memberData.find((m: any) => m.metricKey === metricKey)?.value ?? 0;
        const avg = values.reduce((s: number, v: number) => s + v, 0) / values.length;
        const p50 = this.percentile(values, 50);
        const p75 = this.percentile(values, 75);
        const p90 = this.percentile(values, 90);
        const p10 = this.percentile(values, 10);
        const agentPercentile = this.computePercentileRank(values, agentValue);

        // Determine relative performance
        const relativePerformance = agentPercentile >= 90 ? 'top_performer'
          : agentPercentile >= 75 ? 'above_average'
          : agentPercentile >= 25 ? 'at_average'
          : 'below_average';

        return {
          metricKey,
          agentValue,
          peerGroupAverage: avg,
          peerGroupP50: p50,
          peerGroupP75: p75,
          peerGroupP90: p90,
          peerGroupP10: p10,
          agentPercentile,
          relativePerformance,
        };
      });

      // Overall ranking
      const avgPercentile = metrics.reduce((s, m) => {
        const isLowerBetter = ['ahtSeconds', 'holdTimeSeconds', 'asaSeconds'].includes(m.metricKey);
        return s + (isLowerBetter ? 100 - m.agentPercentile : m.agentPercentile);
      }, 0) / metrics.length;

      results.set(member, {
        agentId: member,
        peerGroupId,
        periodStart,
        periodEnd,
        metrics,
        overallRank: 0, // Computed below
        overallPercentile: avgPercentile,
      });
    }

    // Compute ranks
    const sorted = Array.from(results.values())
      .sort((a, b) => b.overallPercentile - a.overallPercentile);
    sorted.forEach((result, idx) => {
      result.overallRank = idx + 1;
    });

    return results;
  }

  private async getPeerGroupMembers(config: BenchmarkConfig): Promise<string[]> {
    let query = 'SELECT DISTINCT agentId FROM agents WHERE tenantId = ?';
    const params: string[] = [config.tenantId];
    const conditions: string[] = [];

    if (config.membershipCriteria.byTeam && config.membershipCriteria.byTeam.length > 0) {
      conditions.push(`teamId IN (${config.membershipCriteria.byTeam.map(() => '?').join(',')})`);
      params.push(...config.membershipCriteria.byTeam);
    }
    if (config.membershipCriteria.byRole && config.membershipCriteria.byRole.length > 0) {
      conditions.push(`role IN (${config.membershipCriteria.byRole.map(() => '?').join(',')})`);
      params.push(...config.membershipCriteria.byRole);
    }

    if (conditions.length > 0) {
      query += ' AND ' + conditions.join(' AND ');
    }

    const result = await this.clickhouse.query(query, params);
    return result.map((r: any) => r.agentId);
  }

  private async getMemberMetrics(
    agentIds: string[],
    metrics: string[],
    start: number,
    end: number
  ): Promise<any[]> {
    const agentIdList = agentIds.map(id => `'${id}'`).join(',');
    const metricList = metrics.map(m => `'${m}'`).join(',');

    return this.clickhouse.query(`
      SELECT agentId, metric as metricKey, avg(value) as value
      FROM daily_metric_rollups
      WHERE agentId IN (${agentIdList})
        AND metric IN (${metricList})
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY agentId, metric
    `);
  }

  private percentile(sortedValues: number[], percentile: number): number {
    if (sortedValues.length === 0) return 0;
    const index = Math.ceil((percentile / 100) * sortedValues.length) - 1;
    return sortedValues[Math.max(0, index)];
  }

  private computePercentileRank(sortedValues: number[], value: number): number {
    if (sortedValues.length === 0) return 50;
    const below = sortedValues.filter(v => v < value).length;
    return (below / sortedValues.length) * 100;
  }
}

// Benchmark radar chart component
const BenchmarkRadarChart: React.FC<{
  agentValue: number[];
  peerAverage: number[];
  metrics: string[];
}> = ({ agentValue, peerAverage, metrics }) => {
  return (
    <div className="benchmark-radar">
      <RadarChart
        data={metrics.map((m, i) => ({
          metric: m,
          agent: agentValue[i],
          peerAvg: peerAverage[i],
        }))}
        xKey="metric"
        series={[
          { dataKey: 'agent', name: 'You', color: '#3498DB' },
          { dataKey: 'peerAvg', name: 'Peer Avg', color: '#95A5A6' },
        ]}
      />
    </div>
  );
};

// Comparison table
const BenchmarkTable: React.FC<{
  results: BenchmarkResult;
}> = ({ results }) => (
  <table className="benchmark-table">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Your Value</th>
        <th>Peer Avg</th>
        <th>Peer p50</th>
        <th>Percentile</th>
        <th>Performance</th>
      </tr>
    </thead>
    <tbody>
      {results.metrics.map(m => (
        <tr key={m.metricKey} className={m.relativePerformance}>
          <td>{m.metricKey}</td>
          <td>{m.agentValue.toFixed(1)}</td>
          <td>{m.peerGroupAverage.toFixed(1)}</td>
          <td>{m.peerGroupP50.toFixed(1)}</td>
          <td>{m.agentPercentile.toFixed(0)}%</td>
          <td><PerformanceBadge type={m.relativePerformance} /></td>
        </tr>
      ))}
    </tbody>
    <tfoot>
      <tr>
        <td colSpan={5}>Overall Rank: {results.overallRank}</td>
        <td>Overall: {results.overallPercentile.toFixed(0)}%</td>
      </tr>
    </tfoot>
  </table>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Benchmark computation |
| Nivo (MIT) | Client | Radar chart visualization |
| React Table (MIT) | Client | Comparison table |
| Apache ECharts (Apache 2.0) | Client | Bar chart comparisons |

## Production Considerations

**Scaling:** Pre-compute benchmarks for the most common peer groups daily (off-peak hours). Cache benchmark results in Redis with a TTL of 12 hours. For ad-hoc peer groups created by supervisors, compute on-demand with a 30-second timeout and cache for 6 hours. The percentile computation is O(n log n) per metric — for 1000 agents x 10 metrics, this completes in < 1 second in ClickHouse.

**Security:** Benchmark visibility is scoped by role: agents see only their own benchmark compared to anonymized peer averages; supervisors see named comparisons for their team members; administrators see all. The peer group definition API requires the `analytics:configure` permission. Industry benchmark data is licensed per-tenant and should not be shared across tenants.

**Monitoring:** Track benchmark computation job duration and success rate. Alert if a computation exceeds the expected duration by 2x. Monitor the number of ad-hoc benchmark queries — if it exceeds 100 per day, consider adding the peer group to the pre-computed schedule. Track the distribution of relativePerformance labels — if most agents are "top_performer" or "below_average," the peer group definition may need adjustment.
