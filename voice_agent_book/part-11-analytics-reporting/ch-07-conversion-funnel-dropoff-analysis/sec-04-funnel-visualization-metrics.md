# Section 04: Funnel Visualization and Metrics

## Overview

Funnel visualization and metrics present the conversion funnel as intuitive, interactive visualizations that communicate caller progression, drop-off points, and conversion rates at a glance. The primary visualization is a funnel chart (also called a "sankey" or "waterfall" chart) showing the progressive narrowing of caller volume from stage to stage. Supporting visualizations include cumulative conversion curves, stage-by-stage bar charts, and comparison funnels (current period vs previous period side by side).

Each visualization is interactive: hovering over a stage shows detailed metrics (entries, exits, drop-offs, conversion rate, average duration); clicking a stage opens the drill-down view; toggles switch between absolute counts and percentages. The funnel can be segmented by campaign, queue, customer segment, or time of day, overlaying multiple funnel lines on the same chart for comparison. The visualization engine uses ECharts for the sankey/funnel chart and Recharts for supporting charts.

## Architecture

```
            Funnel Visualization Pipeline

   ClickHouse (funnel event aggregations)
        |
   Funnel Data API (query & transform)
        |
   ┌────┴────────────┐
   |                 |
   Funnel Chart      Supporting Charts
   (sankey /         (bar chart, line chart,
    waterfall)        comparison funnel)
   |                 |
   ECharts           Recharts
   (Canvas)          (SVG)
   |                 |
   Interactive Dashboard
   (hover, click, filter, toggle)
```

## Design Decisions

- **Sankey diagram for main funnel over pyramid funnel chart:** The traditional pyramid funnel chart (inverted triangle) only shows the narrowing of the funnel but doesn't show the flow paths (splits, rejoins, loops). A sankey diagram shows the flow volume between stages, with the width of each flow proportional to the number of callers. It naturally handles branching funnels (IVR → Queue or Self-Service) and can show re-entry paths (caller returns to a previous stage). Trade-off: sankey diagrams are more complex to read than pyramid funnels; a simplified "waterfall" view is available as an alternative for users who prefer the classic funnel shape.

- **Comparison mode with overlay and side-by-side options over single-mode display:** Users need to compare funnels across time periods (this week vs last week), segments (campaign A vs campaign B), or configurations (before vs after IVR redesign). The comparison mode supports both overlay (two funnels drawn on the same chart with different colors) and side-by-side (two separate funnel charts arranged horizontally). The overlay mode highlights stage-by-stage differences with deltas. Trade-off: overlay mode can become visually cluttered with more than 2 comparisons; limit to 4 concurrent overlays.

- **Configurable metric display (absolute vs percentage, cumulative vs stage-level) over fixed metric:** Different stakeholders need different views: operations managers want absolute counts, executives want percentages, and analysts want both. Toggle controls allow switching between: absolute counts (showing actual caller numbers at each stage), percentages (showing % of initial callers remaining), stage-level conversion (showing % who progress from each stage to the next), and cumulative conversion (showing % who reached each stage from the start). Trade-off: multiple display modes increase frontend complexity and testing requirements.

## Implementation Approach

```typescript
interface FunnelVisualizationData {
  funnelId: string;
  tenantId: string;
  periodStart: number;
  periodEnd: number;
  stages: FunnelStageVisual[];
  flows: Array<{
    source: string;
    target: string;
    value: number;
    conversionRate: number;
  }>;
  totalEntries: number;
  totalConversions: number;
  overallRate: number;
}

interface FunnelStageVisual {
  id: string;
  name: string;
  order: number;
  entries: number;
  exits: number;
  dropOffs: number;
  stageConversion: number;      // % who exit successfully
  cumulativeConversion: number;  // % of initial callers remaining
  averageDuration: number;
  color: string;
}

interface FunnelComparisonData {
  primary: FunnelVisualizationData;
  comparison?: FunnelVisualizationData;
  deltas: Array<{
    stageId: string;
    stageName: string;
    entryDelta: number;
    conversionDelta: number;
    direction: 'up' | 'down' | 'flat';
  }>;
}

class FunnelVisualizationService {
  private clickhouse: ClickHouseClient;

  async getFunnelData(
    tenantId: string,
    funnelId: string,
    start: number,
    end: number,
    segment?: { dimension: string; value: string }
  ): Promise<FunnelVisualizationData> {
    const stageFilter = segment
      ? `AND ${segment.dimension} = '${segment.value}'`
      : '';

    // Get stage entries and exits
    const stageData = await this.clickhouse.query(`
      SELECT
        stageId,
        countIf(eventType = 'stage_entry') as entries,
        countIf(eventType = 'stage_exit') as exits,
        countIf(eventType IN ('stage_dropoff', 'stage_abandon')) as dropOffs,
        avgIf(durationMs, eventType = 'stage_exit') as avgDuration
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
        ${stageFilter}
      GROUP BY stageId
    `);

    // Get flows between stages
    const flowData = await this.clickhouse.query(`
      SELECT
        previousStageId as source,
        stageId as target,
        count() as value
      FROM funnel_events
      WHERE tenantId = '${tenantId}'
        AND funnelId = '${funnelId}'
        AND eventType = 'stage_entry'
        AND previousStageId IS NOT NULL
        AND timestamp >= ${start}
        AND timestamp <= ${end}
        ${stageFilter}
      GROUP BY source, target
    `);

    // Get funnel definition for stage names and ordering
    const funnelDef = await this.getFunnelDefinition(funnelId, tenantId);
    const stages = (funnelDef?.stages ?? [])
      .filter((s: any) => s.isEnabled)
      .sort((a: any, b: any) => a.order - b.order);

    const stageMap = new Map(stages.map((s: any) => [s.id, s]));
    const stageDataMap = new Map(stageData.map((r: any) => [r.stageId, r]));

    // Build stage visuals
    const firstStageEntries = stageDataMap.get(stages[0]?.id)?.entries ?? 0;
    const lastStageExits = stageDataMap.get(stages[stages.length - 1]?.id)?.exits ?? 0;

    const funnelStages: FunnelStageVisual[] = stages.map((stage: any) => {
      const data = stageDataMap.get(stage.id) ?? { entries: 0, exits: 0, dropOffs: 0, avgDuration: 0 };
      return {
        id: stage.id,
        name: stage.name,
        order: stage.order,
        entries: data.entries,
        exits: data.exits,
        dropOffs: data.dropOffs,
        stageConversion: data.entries > 0 ? (data.exits / data.entries) * 100 : 0,
        cumulativeConversion: firstStageEntries > 0 ? (data.exits / firstStageEntries) * 100 : 0,
        averageDuration: data.avgDuration,
        color: this.getStageColor(stage.stageType, data.entries > 0 ? data.exits / data.entries : 0),
      };
    });

    // Build flows
    const flows = flowData
      .filter((r: any) => stageMap.has(r.source) && stageMap.has(r.target))
      .map((r: any) => ({
        source: r.source,
        target: r.target,
        value: r.value,
        conversionRate: 0, // Computed below
      }));

    // Compute flow conversion rates
    for (const flow of flows) {
      const sourceEntries = stageDataMap.get(flow.source)?.entries ?? 1;
      flow.conversionRate = (flow.value / sourceEntries) * 100;
    }

    return {
      funnelId,
      tenantId,
      periodStart: start,
      periodEnd: end,
      stages: funnelStages,
      flows,
      totalEntries: firstStageEntries,
      totalConversions: lastStageExits,
      overallRate: firstStageEntries > 0 ? (lastStageExits / firstStageEntries) * 100 : 0,
    };
  }

  async getComparisonData(
    tenantId: string,
    funnelId: string,
    currentStart: number,
    currentEnd: number,
    comparisonStart: number,
    comparisonEnd: number,
    segment?: { dimension: string; value: string }
  ): Promise<FunnelComparisonData> {
    const primary = await this.getFunnelData(tenantId, funnelId, currentStart, currentEnd, segment);
    const comparison = await this.getFunnelData(tenantId, funnelId, comparisonStart, comparisonEnd, segment);

    // Compute deltas
    const primaryMap = new Map(primary.stages.map(s => [s.id, s]));
    const comparisonMap = new Map(comparison.stages.map(s => [s.id, s]));

    const deltas = Array.from(primaryMap.entries()).map(([stageId, primaryStage]) => {
      const comparisonStage = comparisonMap.get(stageId);
      const entryDelta = comparisonStage ? primaryStage.entries - comparisonStage.entries : 0;
      const conversionDelta = comparisonStage
        ? primaryStage.stageConversion - comparisonStage.stageConversion
        : 0;

      return {
        stageId,
        stageName: primaryStage.name,
        entryDelta,
        conversionDelta,
        direction: conversionDelta > 2 ? 'up' as const : conversionDelta < -2 ? 'down' as const : 'flat' as const,
      };
    });

    return { primary, comparison, deltas };
  }

  private getStageColor(stageType: string, conversionRate: number): string {
    if (stageType === 'exit') return '#2ECC71';
    if (conversionRate > 0.8) return '#3498DB';
    if (conversionRate > 0.5) return '#F39C12';
    return '#E74C3C';
  }

  private async getFunnelDefinition(funnelId: string, tenantId: string): Promise<any> {
    // Injected dependency
    return null;
  }
}

// Funnel visualization React component
const FunnelVisualization: React.FC<{
  data: FunnelVisualizationData | FunnelComparisonData;
  mode: 'single' | 'comparison';
  displayMode: 'absolute' | 'percentage' | 'cumulative';
}> = ({ data, mode, displayMode }) => {
  const isComparison = 'primary' in data && 'comparison' in data;
  const funnelData = isComparison ? (data as FunnelComparisonData).primary : data as FunnelVisualizationData;
  const comparisonData = isComparison ? (data as FunnelComparisonData).comparison : undefined;

  return (
    <div className="funnel-visualization">
      <div className="funnel-controls">
        <ToggleGroup
          options={['absolute', 'percentage', 'cumulative']}
          selected={displayMode}
          onChange={() => {}}
        />
        {mode === 'comparison' && (
          <ComparisonControls>
            <DeltaIndicators deltas={isComparison ? (data as FunnelComparisonData).deltas : []} />
          </ComparisonControls>
        )}
      </div>
      <div className="funnel-charts">
        <SankeyChart
          stages={funnelData.stages.map(s => ({
            name: s.name,
            value: displayMode === 'absolute' ? s.entries
              : displayMode === 'percentage' ? s.cumulativeConversion
              : s.stageConversion,
            color: s.color,
          }))}
          flows={funnelData.flows.map(f => ({
            source: f.source,
            target: f.target,
            value: f.value,
          }))}
          onClick={(stageId) => handleStageClick(stageId)}
        />
        {comparisonData && (
          <OverlayFunnel
            primary={funnelData.stages}
            comparison={comparisonData.stages}
          />
        )}
      </div>
      <FunnelMetricsTable
        stages={funnelData.stages}
        overallRate={funnelData.overallRate}
        totalEntries={funnelData.totalEntries}
        totalConversions={funnelData.totalConversions}
      />
    </div>
  );
};

// Stage metrics table
const FunnelMetricsTable: React.FC<{
  stages: FunnelStageVisual[];
  overallRate: number;
  totalEntries: number;
  totalConversions: number;
}> = ({ stages, overallRate, totalEntries, totalConversions }) => (
  <table className="funnel-metrics-table">
    <thead>
      <tr>
        <th>Stage</th>
        <th>Entries</th>
        <th>Exits</th>
        <th>Drop-offs</th>
        <th>Stage Conv.</th>
        <th>Cumulative</th>
        <th>Avg Duration</th>
      </tr>
    </thead>
    <tbody>
      {stages.map(s => (
        <tr key={s.id}>
          <td>{s.name}</td>
          <td>{s.entries}</td>
          <td>{s.exits}</td>
          <td className="dropoff">{s.dropOffs}</td>
          <td>{s.stageConversion.toFixed(1)}%</td>
          <td>{s.cumulativeConversion.toFixed(1)}%</td>
          <td>{formatDuration(s.averageDuration)}</td>
        </tr>
      ))}
    </tbody>
    <tfoot>
      <tr>
        <td colSpan={7}>
          Overall: {overallRate.toFixed(1)}% ({totalConversions}/{totalEntries})
        </td>
      </tr>
    </tfoot>
  </table>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache ECharts (Apache 2.0) | Client | Sankey/funnel chart rendering |
| Recharts (MIT) | Client | Supporting bar/line charts |
| ClickHouse (Apache 2.0) | Server | Funnel data queries |
| React (MIT) | Client | Visualization component infrastructure |

## Production Considerations

**Scaling:** Funnel visualization queries are cached aggressively — results for common time ranges (last 7 days, last 30 days) are pre-computed hourly and served from Redis with 1-hour TTL. Ad-hoc date ranges or segments query ClickHouse directly but are cached for 5 minutes. The sankey diagram can render up to 50 stages and 500 flows without performance degradation.

**Security:** Funnel data access requires `analytics:view` permission. Segment comparisons (e.g., funnel by agent, by campaign) require the permission level appropriate for the segment dimension. The comparison feature should not allow comparing across tenants.

**Monitoring:** Track funnel visualization load time (p95 < 500 ms), sankey render time (p95 < 200 ms), and comparison query frequency. Alert if funnel data queries exceed 2 seconds. Monitor the most popular segment dimensions to optimize pre-computation. Track comparison mode usage — if > 50% of funnel views use comparison, prioritize pre-computing common comparison pairs.
