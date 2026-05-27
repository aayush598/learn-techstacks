# Section 03: Drop-Off Point Identification

## Overview

Drop-off point identification pinpoints exactly where in the funnel callers abandon their journey, enabling targeted interventions to reduce abandonment. The system analyzes stage-level events to identify not just which stage has the highest drop-off rate, but also the specific causes: excessive wait time (caller hangs up in queue), IVR complexity (caller exits IVR without reaching a queue), agent transfer (caller drops during or after transfer), or unresolved issues (caller reaches agent but doesn't get a resolution).

Drop-off analysis goes beyond simple abandonment rates. It segments drop-offs by reason (abandoned during IVR, abandoned in queue, abandoned after transfer), by duration bucket (how long did the caller wait before abandoning), and by caller attributes (new vs returning customer, high-value vs standard). The system also tracks "bounces" — callers who hang up within the first 5 seconds and never re-enter the funnel. Each drop-off category has different operational implications and remediation strategies.

## Architecture

```
            Drop-Off Point Identification Pipeline

   Funnel Events → Drop-Off Analyzer
                        |
            ┌───────────┴───────────┐
            |                       |
      Stage-Level Drop      Root Cause
      (which stage?)        (why?)
            |                       |
      ClickHouse            Event Correlation
      (drop_off_records)    (wait time, IVR path,
                            transfer count, agent)
            |
      Drop-Off Dashboard
      (drop-off heatmap,
       reason breakdown,
       cost of abandonment)
```

## Design Decisions

- **Multi-dimensional drop-off classification over single-reason attribution:** A caller may abandon because of a combination of factors: they waited 5 minutes (long wait), they were transferred twice (multiple transfers), and the IVR had 4 menu levels (complex IVR). The system classifies each drop-off with multiple contributing factors rather than a single "primary reason." The dashboard shows a Venn diagram or stacked bar of overlapping factors. Trade-off: multi-dimensional classification is more complex to compute and visualize but provides richer insights than single-reason analysis.

- **Cost of abandonment estimation over raw count reporting:** Every dropped call has a business cost: lost sales opportunity, customer dissatisfaction, potential churn, and wasted agent capacity. The system estimates abandonment cost using configurable parameters: average revenue per call (for sales funnels), customer lifetime value impact (for support funnels), and agent idle cost (when agents wait for callers who never arrive). These costs are displayed alongside drop-off counts to communicate business impact. Trade-off: cost estimates are approximations and require tenant-specific configuration; displayed as "estimated cost" with a methodology note.

- **Real-time drop-off alerts over daily digest:** Supervisors need to know immediately when a drop-off spike occurs, not the next morning. The system evaluates drop-off rates every 5 minutes and triggers alerts when the rate exceeds configurable thresholds (e.g., "IVR abandonment > 15% in the last 5 minutes"). Alerts include the estimated cost of the current spike and links to the drill-down view for root cause analysis. Trade-off: real-time alerting increases system load (evaluation every 5 minutes per stage) and may cause alert fatigue if thresholds are too sensitive.

## Implementation Approach

```typescript
interface DropOffRecord {
  callSid: string;
  tenantId: string;
  funnelId: string;
  stageId: string;
  stageName: string;
  dropOffType: 'ivr_abandon' | 'queue_abandon' | 'transfer_drop' | 'unresolved' | 'bounce';
  dropOffReason: string;
  contributingFactors: Array<{
    factor: 'long_wait' | 'complex_ivr' | 'multiple_transfers' | 'agent_unavailable' | 'long_duration';
    value: number;
    threshold: number;
    severity: 'low' | 'medium' | 'high';
  }>;
  waitTimeSeconds: number;
  ivrSteps: number;
  transferCount: number;
  agentCount: number;
  durationSeconds: number;
  estimatedCost: number;
  timestamp: number;
}

interface DropOffSummary {
  stageId: string;
  stageName: string;
  totalEntries: number;
  totalDropOffs: number;
  dropOffRate: number;
  byType: Record<string, number>;
  byFactor: Array<{ factor: string; count: number; percentage: number }>;
  averageWaitBeforeDrop: number;
  estimatedTotalCost: number;
  trend: 'increasing' | 'decreasing' | 'stable';
}

class DropOffAnalyzer {
  private clickhouse: ClickHouseClient;
  private redis: Redis;

  async identifyDropOffs(
    tenantId: string,
    funnelId: string,
    start: number,
    end: number
  ): Promise<DropOffSummary[]> {
    // Get all funnel stages
    const funnelDef = await this.getFunnelDefinition(funnelId, tenantId);
    if (!funnelDef) return [];

    const summaries: DropOffSummary[] = [];

    for (const stage of funnelDef.stages) {
      // Query drop-off events for this stage
      const dropOffs = await this.clickhouse.query(`
        SELECT
          eventType,
          count() as count,
          avg(durationMs) as avgDuration
        FROM funnel_events
        WHERE tenantId = '${tenantId}'
          AND funnelId = '${funnelId}'
          AND stageId = '${stage.id}'
          AND eventType IN ('stage_dropoff', 'stage_abandon')
          AND timestamp >= ${start}
          AND timestamp <= ${end}
        GROUP BY eventType
      `);

      const totalDropOffs = dropOffs.reduce((s: number, r: any) => s + r.count, 0);

      // Get entries for this stage
      const entries = await this.clickhouse.query(`
        SELECT count() as count
        FROM funnel_events
        WHERE tenantId = '${tenantId}'
          AND funnelId = '${funnelId}'
          AND stageId = '${stage.id}'
          AND eventType = 'stage_entry'
          AND timestamp >= ${start}
          AND timestamp <= ${end}
      `);

      const totalEntries = entries[0]?.count ?? 0;

      // Get detailed contributing factors from recent drop-offs
      const factorAnalysis = await this.clickhouse.query(`
        SELECT
          countIf(waitTimeSeconds > 120) as longWait,
          countIf(ivrSteps > 4) as complexIvr,
          countIf(transferCount > 1) as multipleTransfers,
          countIf(durationSeconds > 600) as longDuration,
          count() as total
        FROM funnel_drop_off_details
        WHERE tenantId = '${tenantId}'
          AND funnelId = '${funnelId}'
          AND stageId = '${stage.id}'
          AND timestamp >= ${start}
          AND timestamp <= ${end}
      `);

      const factors = factorAnalysis[0];
      const factorList = [
        { factor: 'long_wait', count: factors?.longWait ?? 0 },
        { factor: 'complex_ivr', count: factors?.complexIvr ?? 0 },
        { factor: 'multiple_transfers', count: factors?.multipleTransfers ?? 0 },
        { factor: 'long_duration', count: factors?.longDuration ?? 0 },
      ].filter(f => f.count > 0);

      // Estimate cost
      const estimatedCost = await this.estimateDropOffCost(tenantId, totalDropOffs, stage);

      summaries.push({
        stageId: stage.id,
        stageName: stage.name,
        totalEntries,
        totalDropOffs,
        dropOffRate: totalEntries > 0 ? (totalDropOffs / totalEntries) * 100 : 0,
        byType: Object.fromEntries(
          dropOffs.map((r: any) => [r.eventType, r.count])
        ),
        byFactor: factorList.map(f => ({
          ...f,
          percentage: totalDropOffs > 0 ? (f.count / totalDropOffs) * 100 : 0,
        })),
        averageWaitBeforeDrop: dropOffs[0]?.avgDuration ?? 0,
        estimatedTotalCost: estimatedCost,
        trend: 'stable', // Computed by comparing to previous period
      });
    }

    return summaries;
  }

  async getRealtimeDropOffRate(
    tenantId: string,
    funnelId: string,
    stageId: string
  ): Promise<{ rate: number; count: number; entries: number }> {
    const now = Date.now();
    const fiveMinutesAgo = now - 5 * 60 * 1000;

    const dropOffs = await this.clickhouse.query(`
      SELECT count() as dropOffs
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND stageId = '${stageId}'
        AND eventType IN ('stage_dropoff', 'stage_abandon')
        AND timestamp >= ${fiveMinutesAgo}
    `);

    const entries = await this.clickhouse.query(`
      SELECT count() as entries
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND stageId = '${stageId}'
        AND eventType = 'stage_entry'
        AND timestamp >= ${fiveMinutesAgo}
    `);

    const dropCount = dropOffs[0]?.dropOffs ?? 0;
    const entryCount = entries[0]?.entries ?? 0;

    return {
      rate: entryCount > 0 ? (dropCount / entryCount) * 100 : 0,
      count: dropCount,
      entries: entryCount,
    };
  }

  async analyzeDropOffCall(callSid: string): Promise<DropOffRecord | null> {
    const result = await this.clickhouse.query(`
      SELECT * FROM funnel_drop_off_details
      WHERE callSid = '${callSid}'
      LIMIT 1
    `);

    if (result.length === 0) return null;
    return result[0];
  }

  private async estimateDropOffCost(
    tenantId: string,
    dropOffCount: number,
    stage: any
  ): Promise<number> {
    // Get configured cost parameters
    const config = await this.redis.hgetall(`funnel:cost:${tenantId}`);
    const averageRevenuePerCall = parseFloat(config.averageRevenuePerCall ?? '0');
    const agentCostPerMinute = parseFloat(config.agentCostPerMinute ?? '0.50');

    // Estimate: lost revenue + wasted agent time
    const lostRevenue = dropOffCount * averageRevenuePerCall;
    const wastedAgentTime = dropOffCount * (stage.averageDurationMs / 60000) * agentCostPerMinute;

    return lostRevenue + wastedAgentTime;
  }

  private async getFunnelDefinition(funnelId: string, tenantId: string): Promise<any> {
    // Injected dependency
    return null;
  }
}

// Drop-off analysis dashboard component
const DropOffDashboard: React.FC<{
  summaries: DropOffSummary[];
  onStageClick: (stageId: string) => void;
}> = ({ summaries, onStageClick }) => (
  <div className="dropoff-dashboard">
    <div className="dropoff-heatmap">
      <StageDropOffHeatmap
        stages={summaries.map(s => ({
          name: s.stageName,
          dropOffRate: s.dropOffRate,
          cost: s.estimatedTotalCost,
        }))}
        onStageClick={onStageClick}
      />
    </div>
    <div className="dropoff-details">
      {summaries.map(s => (
        <StageDropOffCard key={s.stageId} summary={s} onClick={() => onStageClick(s.stageId)} />
      ))}
    </div>
    <div className="dropoff-cost-summary">
      <MetricLabel label="Total Estimated Cost" value={`$${summaries.reduce((sum, s) => sum + s.estimatedTotalCost, 0).toLocaleString()}`} />
      <MetricLabel label="Period" value="Last 7 days" />
    </div>
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Drop-off analytics queries |
| Redis (RSAL) | Server | Real-time drop-off counters & cost config |
| Apache Kafka (Apache 2.0) | Server | Drop-off event ingestion |
| Apache ECharts (Apache 2.0) | Client | Drop-off heatmap visualization |

## Production Considerations

**Scaling:** Drop-off analysis queries group by stageId and eventType — ensure compound index on (tenantId, funnelId, stageId, eventType, timestamp). The contributing factors analysis queries a separate `funnel_drop_off_details` table that is populated asynchronously by a worker process. For real-time drop-off rate (5-minute window), use Redis counters rather than querying ClickHouse, which would be slower. Cost estimation parameters are tenant-scoped and loaded from Redis.

**Security:** Drop-off data is tenant-scoped. The `funnel_drop_off_details` table contains call SIDs and associated metadata — access requires `calls:view` permission for raw call details. Aggregate drop-off summaries are accessible with `analytics:view`. Cost estimation parameters (average revenue per call) are business-sensitive and require `analytics:configure` permission to modify.

**Monitoring:** Track drop-off rate per stage per hour, real-time drop-off alert firing rate, and cost estimation accuracy. Alert if any stage's drop-off rate exceeds 20% in a rolling 30-minute window. Monitor the drop-off alert false positive rate — if > 30% of alerts are dismissed without action, the threshold may be too sensitive.
