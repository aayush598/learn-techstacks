# Section 02: Conversion Rate Tracking

## Overview

Conversion rate tracking measures the percentage of callers who successfully progress from one funnel stage to the next, and ultimately reach the final "success" or "resolution" stage. It answers critical questions: "What percentage of callers who reach an agent actually resolve their issue?," "How does conversion vary by campaign, queue, time of day, or customer segment?" The system tracks conversion rates at each funnel stage, providing both stage-level and overall conversion metrics.

Conversion rates are computed for configurable time windows (real-time 30-minute rolling, hourly, daily, weekly) and segmented by relevant dimensions. The system distinguishes between different types of stage exits: successful progression (caller moves to the next stage), drop-off (caller leaves the funnel without resolution), and abandonment (caller hangs up). Each exit type is tracked separately to provide a complete picture of caller behavior. Statistical significance tests highlight meaningful changes in conversion rates.

## Architecture

```
           Conversion Rate Tracking Pipeline

   Platform Events → Event Processor → Funnel Engine
                                             |
                                   ClickHouse (funnel_events)
                                             |
                                   Conversion Calculator
                                   (stage-level, overall, segmented)
                                             |
                                   Redis (real-time counters)
                                             |
                                   Dashboard Widgets
                                   (conversion gauge, funnel bar chart,
                                    stage-by-stage table, trend chart)
```

## Design Decisions

- **Event-sourced conversion tracking over periodic snapshots:** Each stage transition (entry, exit, drop-off, abandonment) generates an event that is consumed by the funnel engine. The engine updates conversion counters in Redis in real-time and writes the event to ClickHouse for historical queries. This provides sub-second conversion rate updates for the dashboard. Trade-off: event-sourced systems depend on reliable event emission; missing or duplicate events require deduplication and reconciliation logic.

- **Multi-stage conversion rate (end-to-end) over per-stage only:** Per-stage conversion rates (e.g., IVR → Queue: 85%) are useful but don't tell the full story. The overall conversion rate (caller reaches "Resolved" stage from "Contact") is the most important business metric. The system computes both: stage-by-stage conversion (stage N → stage N+1) and cumulative conversion (stage 1 → stage N). The "funnel bar chart" shows the cumulative drop at each stage, highlighting where the biggest losses occur. Trade-off: cumulative conversion rates compound errors from earlier stages — a data quality issue in stage 2 affects all downstream conversion calculations.

- **Conversion with time limits (slaTime) over unlimited wait:** A caller who takes 2 hours to reach resolution may have technically "converted" but the experience was poor. Each stage can have a time limit (default: 10 minutes per stage). If the caller spends longer than the limit in a stage, it's marked as "converted but exceeded SLA" — tracked separately from on-time conversions. The dashboard shows both "conversion rate" and "on-time conversion rate." Trade-off: time limits add complexity to the configuration and may not apply equally to all call types (complex technical issues naturally take longer).

## Implementation Approach

```typescript
interface FunnelEvent {
  callSid: string;
  tenantId: string;
  funnelId: string;
  stageId: string;
  eventType: 'stage_entry' | 'stage_exit' | 'stage_dropoff' | 'stage_abandon' | 'stage_timeout';
  timestamp: number;
  previousStageId?: string;
  nextStageId?: string;
  durationMs: number;           // time spent in this stage
  metadata?: Record<string, string>;
}

interface ConversionRate {
  stageId: string;
  stageName: string;
  stageOrder: number;
  entries: number;
  successfulExits: number;
  dropoffs: number;
  abandons: number;
  timeouts: number;
  conversionRate: number;          // successfulExits / entries * 100
  onTimeConversionRate: number;    // successfulExits without timeout / entries * 100
  averageDurationMs: number;
  previousPeriod?: {
    conversionRate: number;
    change: number;                // percentage point change
    significant: boolean;
  };
}

class ConversionTracker {
  private redis: Redis;
  private clickhouse: ClickHouseClient;

  async recordEvent(event: FunnelEvent): Promise<void> {
    // Update Redis real-time counters
    const hour = this.getHourBucket(event.timestamp);
    const counterKey = `funnel:${event.tenantId}:${event.funnelId}:${event.stageId}:${hour}`;

    const field = event.eventType === 'stage_exit' ? 'successfulExits'
      : event.eventType === 'stage_dropoff' ? 'dropoffs'
      : event.eventType === 'stage_abandon' ? 'abandons'
      : event.eventType === 'stage_timeout' ? 'timeouts'
      : null;

    if (field) {
      await this.redis.hincrby(counterKey, field, 1);
      await this.redis.expire(counterKey, 7200); // 2 hour TTL
    }
    if (event.eventType === 'stage_entry' || event.eventType === 'stage_exit') {
      await this.redis.hincrby(counterKey, 'entries', 1);
    }

    // Write to ClickHouse
    await this.clickhouse.insert('funnel_events', event);
  }

  async getConversionRates(
    tenantId: string,
    funnelId: string,
    start: number,
    end: number,
    stageIds?: string[]
  ): Promise<ConversionRate[]> {
    const stageFilter = stageIds && stageIds.length > 0
      ? `AND stageId IN (${stageIds.map(s => `'${s}'`).join(',')})`
      : '';

    const results = await this.clickhouse.query(`
      SELECT
        stageId,
        countIf(eventType = 'stage_entry') as entries,
        countIf(eventType = 'stage_exit') as successfulExits,
        countIf(eventType = 'stage_dropoff') as dropoffs,
        countIf(eventType = 'stage_abandon') as abandons,
        countIf(eventType = 'stage_timeout') as timeouts,
        avgIf(durationMs, eventType IN ('stage_exit', 'stage_dropoff', 'stage_abandon', 'stage_timeout')) as avgDuration
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
        ${stageFilter}
      GROUP BY stageId
    `);

    // Get stage names from definition
    const funnelDef = await this.getFunnelDefinition(funnelId, tenantId);
    const stageNames = new Map(funnelDef?.stages.map(s => [s.id, s.name]) ?? []);

    // Get previous period for comparison
    const periodDuration = end - start;
    const previousStart = start - periodDuration;

    const previousResults = await this.clickhouse.query(`
      SELECT stageId,
        countIf(eventType = 'stage_exit') / nullif(countIf(eventType = 'stage_entry'), 0) * 100 as prevConvRate
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND timestamp >= ${previousStart}
        AND timestamp < ${start}
        ${stageFilter}
      GROUP BY stageId
    `);
    const prevMap = new Map(previousResults.map((r: any) => [r.stageId, r.prevConvRate]));

    return results.map((r: any) => {
      const convRate = r.entries > 0 ? (r.successfulExits / r.entries) * 100 : 0;
      const onTimeConvRate = r.entries > 0
        ? ((r.successfulExits - r.timeouts) / r.entries) * 100
        : 0;
      const prevConvRate = prevMap.get(r.stageId);
      const change = prevConvRate != null ? convRate - prevConvRate : 0;

      return {
        stageId: r.stageId,
        stageName: stageNames.get(r.stageId) ?? r.stageId,
        stageOrder: funnelDef?.stages.find(s => s.id === r.stageId)?.order ?? 0,
        entries: r.entries,
        successfulExits: r.successfulExits,
        dropoffs: r.dropoffs,
        abandons: r.abandons,
        timeouts: r.timeouts,
        conversionRate: convRate,
        onTimeConversionRate: onTimeConvRate,
        averageDurationMs: r.avgDuration ?? 0,
        previousPeriod: prevConvRate != null ? {
          conversionRate: prevConvRate,
          change,
          significant: Math.abs(change) > 5 && r.entries > 50,
        } : undefined,
      };
    }).sort((a, b) => a.stageOrder - b.stageOrder);
  }

  async getOverallConversion(
    tenantId: string,
    funnelId: string,
    start: number,
    end: number
  ): Promise<{ overallRate: number; stageCount: number; startEntries: number; finalExits: number }> {
    const stages = await this.getConversionRates(tenantId, funnelId, start, end);
    if (stages.length === 0) return { overallRate: 0, stageCount: 0, startEntries: 0, finalExits: 0 };

    const firstStage = stages[0];
    const lastStage = stages[stages.length - 1];

    return {
      overallRate: firstStage.entries > 0 ? (lastStage.successfulExits / firstStage.entries) * 100 : 0,
      stageCount: stages.length,
      startEntries: firstStage.entries,
      finalExits: lastStage.successfulExits,
    };
  }

  async getRealtimeConversion(
    tenantId: string,
    funnelId: string,
    stageId: string
  ): Promise<number> {
    const hour = this.getHourBucket(Date.now());
    const counterKey = `funnel:${tenantId}:${funnelId}:${stageId}:${hour}`;

    const counters = await this.redis.hgetall(counterKey);
    const entries = parseInt(counters.entries ?? '0');
    const exits = parseInt(counters.successfulExits ?? '0');

    return entries > 0 ? (exits / entries) * 100 : 0;
  }

  private getHourBucket(timestamp: number): number {
    return Math.floor(timestamp / 3600000);
  }

  private async getFunnelDefinition(funnelId: string, tenantId: string): Promise<any> {
    // Injected — would use the FunnelStageService
    return null;
  }
}

// Funnel conversion bar chart component
const FunnelBarChart: React.FC<{
  stages: ConversionRate[];
  overall: { overallRate: number; startEntries: number; finalExits: number };
}> = ({ stages, overall }) => {
  const cumulativeRates = stages.reduce((acc, stage, idx) => {
    const prev = idx === 0 ? 100 : acc[idx - 1];
    acc.push(prev * (stage.conversionRate / 100));
    return acc;
  }, [] as number[]);

  return (
    <div className="funnel-conversion">
      <div className="overall-gauge">
        <CircularGauge value={overall.overallRate} max={100} label="Overall Conversion" />
        <div className="funnel-summary">
          <span>{overall.startEntries} callers entered</span>
          <span>{overall.finalExits} reached resolution</span>
        </div>
      </div>
      <FunnelChart
        stages={stages.map((s, i) => ({
          name: s.stageName,
          value: cumulativeRates[i],
          previous: s.previousPeriod?.conversionRate,
          detail: `${s.conversionRate.toFixed(1)}% → ${s.successfulExits}/${s.entries}`,
        }))}
      />
      <StageConversionTable stages={stages} />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis (RSAL) | Server | Real-time conversion counters |
| ClickHouse (Apache 2.0) | Server | Historical conversion analytics |
| Apache Kafka (Apache 2.0) | Server | Funnel event ingestion |
| Apache ECharts (Apache 2.0) | Client | Funnel bar chart visualization |

## Production Considerations

**Scaling:** Real-time conversion counters use Redis hashes with 2-hour TTL, one per (tenant, funnel, stage, hour). For 50 funnels × 8 stages × 24 hours = 9,600 keys — each ~200 bytes, negligible. Historical conversion queries aggregate funnel_events table — partition by month and ensure compound index on (tenantId, funnelId, stageId, timestamp). For tenants with >1M funnel events/month, use a materialized view with hourly pre-aggregation.

**Security:** Conversion rate data is tenant-scoped. The funnel ID is prefixed with the tenant ID to enforce isolation. Conversion rates at the aggregate level (overall funnel) are accessible with `analytics:view`. Per-agent conversion rates (how often callers resolve when handled by a specific agent) require `agent-performance:view`.

**Monitoring:** Track funnel event processing rate, conversion rate update latency (event arrival to counter update), and stage abandonment rate. Alert if any stage's abandonment rate exceeds 20% in a 1-hour window (indicates a systemic issue). Alert if overall conversion rate drops by more than 10 percentage points compared to the same period last week.
