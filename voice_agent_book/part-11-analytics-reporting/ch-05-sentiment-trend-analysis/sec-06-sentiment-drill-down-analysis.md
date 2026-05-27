# Section 06: Sentiment Drill-Down Analysis

## Overview

Sentiment drill-down analysis enables users to start from a high-level sentiment trend and progressively narrow down to specific calls, segments, and phrases that contributed to the overall score. This investigative workflow helps identify root causes of sentiment shifts: "Why did sentiment drop yesterday?" → "It dropped in the Technical Support queue" → "Agent Smith had 3 calls with sentiment < -0.5" → "These calls all involved the same billing error." The drill-down path is fully navigable via interactive charts and filters.

The drill-down interface supports slicing by: time (drill from yearly to monthly to daily to hourly), dimension (tenant → campaign → queue → agent → call), metric (overall sentiment → customer sentiment → specific emotion), and topic (all topics → billing → invoice questions). Each drill level shows aggregated metrics with the ability to expand to the next level. The interface uses breadcrumb navigation showing the current drill path with the ability to step back.

## Architecture

```
            Sentiment Drill-Down System

   User Click on Trend Point / Chart Segment
        |
   Drill-Down API
        |
   ┌────┴────────────┐
   |                 |
   Dimension         Time
   Resolver          Resolver
   (campaign→agent)  (year→month→day→hour)
   |                 |
   ClickHouse (pre-aggregated + raw)
        |
   Breadcrumb State
   Interactive Charts
   Call List with Highlights
```

## Design Decisions

- **Pre-computed drill-down paths over real-time aggregation:** Each drill level is pre-computed hourly and stored in ClickHouse as a materialized view. For example, the path "tenant → campaign → queue → agent → call" is stored as a nested aggregation table where each row contains the parent dimension, child dimension, sentiment average, and call count. This makes drill-down queries sub-second — the user clicks and sees results immediately. Trade-off: pre-computed paths add storage overhead (a 5-level hierarchy with 100,000 calls generates ~500,000 rows) and have a 1-hour update delay.

- **Call-level detail with highlighted low-sentiment segments over full transcription display:** When drilling to the call level, the system displays a sentiment timeline (score over time) with the lowest-sentiment segments highlighted in red. The user can click a highlighted segment to see the transcription text. This focuses attention on the moments that drove negative sentiment without overwhelming the user with the full transcription. Trade-off: highlighting only low segments may miss context — a segment that appears neutral but follows a positive escalation may be relevant; the full timeline is always available as an expandable panel.

- **Breadcrumb-based navigation over modal/dialog drill-down:** Each drill action pushes a new level onto a breadcrumb bar at the top of the page (e.g., "All Calls > Technical Support > Agent Smith > Call #12345"). Users can click any breadcrumb to return to that level. This provides spatial awareness of where the user is in the drill path and enables quick back/forward navigation. Trade-off: breadcrumbs consume vertical space and may overflow for very deep drill paths; collapse breadcrumbs beyond 5 levels into a dropdown.

## Implementation Approach

```typescript
interface DrillLevel {
  dimension: string;          // 'tenant', 'campaign', 'queue', 'agent', 'call'
  id: string;                 // dimension value ID
  label: string;              // display name
  metrics: {
    callCount: number;
    averageSentiment: number;
    positivePct: number;
    negativePct: number;
    sentimentTrend: string;
  };
  children?: DrillLevel[];    // next level items
  hasDetail: boolean;         // whether deeper drill is available
}

interface DrillPath {
  levels: Array<{ dimension: string; id: string; label: string }>;
  currentLevel: DrillLevel;
  breadcrumbs: Array<{ label: string; dimension: string; id: string }>;
}

class SentimentDrillService {
  private clickhouse: ClickHouseClient;

  async getInitialLevel(tenantId: string, start: number, end: number): Promise<DrillLevel> {
    // Top-level tenant overview
    const overview = await this.clickhouse.query(`
      SELECT
        count() as callCount,
        avg(customerSentiment) as avgSentiment,
        countIf(customerSentiment > 0.2) / count() * 100 as positivePct,
        countIf(customerSentiment < -0.2) / count() * 100 as negativePct
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    // Get campaign breakdown (first drill dimension)
    const campaigns = await this.clickhouse.query(`
      SELECT
        campaignId,
        campaignName,
        count() as callCount,
        avg(customerSentiment) as avgSentiment,
        countIf(customerSentiment > 0.2) / count() * 100 as positivePct,
        countIf(customerSentiment < -0.2) / count() * 100 as negativePct
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY campaignId, campaignName
      ORDER BY callCount DESC
    `);

    return {
      dimension: 'tenant',
      id: tenantId,
      label: `All Campaigns`,
      metrics: {
        callCount: overview[0].callCount,
        averageSentiment: overview[0].avgSentiment,
        positivePct: overview[0].positivePct,
        negativePct: overview[0].negativePct,
        sentimentTrend: 'stable',
      },
      children: campaigns.map((c: any) => ({
        dimension: 'campaign',
        id: c.campaignId,
        label: c.campaignName,
        metrics: {
          callCount: c.callCount,
          averageSentiment: c.avgSentiment,
          positivePct: c.positivePct,
          negativePct: c.negativePct,
          sentimentTrend: 'stable',
        },
        hasDetail: true,
      })),
      hasDetail: true,
    };
  }

  async drillDown(
    tenantId: string,
    currentDimension: string,
    currentId: string,
    nextDimension: string,
    start: number,
    end: number
  ): Promise<DrillLevel> {
    let query: string;

    switch (nextDimension) {
      case 'queue': {
        query = `
          SELECT
            queueId, queueName,
            count() as callCount,
            avg(customerSentiment) as avgSentiment,
            countIf(customerSentiment > 0.2) / count() * 100 as positivePct,
            countIf(customerSentiment < -0.2) / count() * 100 as negativePct
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND ${currentDimension}Id = '${currentId}'
            AND timestamp >= ${start}
            AND timestamp <= ${end}
          GROUP BY queueId, queueName
          ORDER BY callCount DESC
        `;
        break;
      }
      case 'agent': {
        query = `
          SELECT
            agentId, agentName,
            count() as callCount,
            avg(customerSentiment) as avgSentiment,
            countIf(customerSentiment > 0.2) / count() * 100 as positivePct,
            countIf(customerSentiment < -0.2) / count() * 100 as negativePct
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND ${currentDimension}Id = '${currentId}'
            AND timestamp >= ${start}
            AND timestamp <= ${end}
          GROUP BY agentId, agentName
          ORDER BY callCount DESC
        `;
        break;
      }
      case 'call': {
        query = `
          SELECT
            callSid,
            customerName,
            customerSentiment,
            overallLabel,
            duration,
            timestamp
          FROM call_sentiment_analysis
          WHERE tenantId = '${tenantId}'
            AND ${currentDimension}Id = '${currentId}'
            AND timestamp >= ${start}
            AND timestamp <= ${end}
          ORDER BY customerSentiment ASC
          LIMIT 50
        `;
        break;
      }
      default:
        throw new Error(`Unknown dimension: ${nextDimension}`);
    }

    const results = await this.clickhouse.query(query);

    return {
      dimension: nextDimension,
      id: currentId,
      label: results[0]?.queueName ?? results[0]?.agentName ?? currentId,
      metrics: this.computeParentMetrics(results),
      children: results.map((r: any) => ({
        dimension: nextDimension,
        id: r.callSid ?? r.agentId ?? r.queueId,
        label: r.customerName ?? r.agentName ?? r.queueName ?? r.callSid,
        metrics: {
          callCount: r.callCount ?? 1,
          averageSentiment: r.customerSentiment ?? r.avgSentiment,
          positivePct: r.positivePct ?? 0,
          negativePct: r.negativePct ?? 0,
          sentimentTrend: 'stable',
        },
        hasDetail: nextDimension !== 'call',
      })),
      hasDetail: nextDimension !== 'call',
    };
  }

  async getCallDetail(callSid: string): Promise<{
    sentimentTimeline: Array<{ timeOffset: number; score: number; speaker: string }>;
    transcriptionSnippets: Array<{ timeOffset: number; text: string; sentiment: number; speaker: string }>;
    lowSentimentSegments: Array<{ timeOffset: number; text: string; score: number }>;
    summary: any;
  }> {
    const analysis = await this.clickhouse.query(`
      SELECT * FROM call_sentiment_analysis WHERE callSid = '${callSid}'
    `);

    if (analysis.length === 0) {
      return { sentimentTimeline: [], transcriptionSnippets: [], lowSentimentSegments: [], summary: null };
    }

    const call = analysis[0];
    const timeline: Array<{ timeOffset: number; score: number; speaker: string }> =
      call.sentimentTimeline ?? [];
    const transcription: Array<{ timeOffset: number; text: string; sentiment: number; speaker: string }> =
      call.transcription ?? [];

    // Find lowest sentiment segments
    const lowSegments = transcription
      .filter(t => t.sentiment < -0.3)
      .sort((a, b) => a.sentiment - b.sentiment)
      .slice(0, 5);

    return {
      sentimentTimeline: timeline,
      transcriptionSnippets: transcription,
      lowSentimentSegments: lowSegments,
      summary: call,
    };
  }

  private computeParentMetrics(children: any[]): DrillLevel['metrics'] {
    const totalCalls = children.reduce((s: number, c: any) => s + (c.callCount ?? 1), 0);
    const totalSentiment = children.reduce(
      (s: number, c: any) => s + (c.avgSentiment ?? c.customerSentiment ?? 0) * (c.callCount ?? 1),
      0
    );
    return {
      callCount: totalCalls,
      averageSentiment: totalCalls > 0 ? totalSentiment / totalCalls : 0,
      positivePct: children.reduce((s: number, c: any) => s + (c.positivePct ?? 0), 0) / children.length,
      negativePct: children.reduce((s: number, c: any) => s + (c.negativePct ?? 0), 0) / children.length,
      sentimentTrend: 'stable',
    };
  }
}

// Drill-down breadcrumb component
const DrillBreadcrumbs: React.FC<{
  path: Array<{ label: string; dimension: string; id: string }>;
  onNavigate: (index: number) => void;
}> = ({ path, onNavigate }) => (
  <nav className="drill-breadcrumbs">
    {path.map((crumb, index) => (
      <span key={crumb.id} className="breadcrumb-item">
        {index > 0 && <span className="separator">›</span>}
        {index < path.length - 1 ? (
          <button onClick={() => onNavigate(index)}>{crumb.label}</button>
        ) : (
          <span className="current">{crumb.label}</span>
        )}
      </span>
    ))}
  </nav>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Drill-down queries |
| Apache ECharts (Apache 2.0) | Client | Interactive drill-down charts |
| React Router (MIT) | Client | Breadcrumb navigation state |
| D3.js (ISC) | Client | Call sentiment timeline rendering |

## Production Considerations

**Scaling:** Pre-computed drill paths are written hourly by a ClickHouse materialized view. The view tree has a maximum depth of 5 levels (tenant → campaign/queue → agent → call). Each level is a ClickHouse table with partitioning by (tenantId, date). Query times for drill operations are consistently under 50 ms. The call detail query accesses the raw call_sentiment_analysis table by callSid — ensure an index on (callSid, tenantId).

**Security:** Drill-down access is gated by the same permissions as the underlying data. An agent drilling into their own calls works; a supervisor drilling into team calls works; an unrestricted user drilling all calls requires `analytics:view-all`. The call detail view (with transcription snippets) requires `calls:view-transcription` permission. Breadcrumb state does not expose data — it only contains labels and IDs.

**Monitoring:** Track drill-down query performance by level — p95 should be under 100 ms. Track the most common drill paths (which dimensions users explore most) to optimize pre-computation order. Alert if the materialized view refresh for drill paths fails. Monitor the call detail view access rate — if it exceeds 1000 views/day, consider caching full call analysis results.
