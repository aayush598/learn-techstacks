# Section 06: Drill-Down Analysis View

## Overview

The drill-down analysis view for intent and topic analytics enables users to start from an aggregate overview and progressively narrow to specific calls and transcription segments that exemplify a particular intent or topic. The drill path flows: All Intents → Intent Category → Specific Intent → Calls with this Intent → Transcription segments expressing this intent. Each level provides aggregated statistics and the ability to filter, sort, and search.

The drill-down view integrates intent data, sentiment data, and transcription snippets in a single workflow. When viewing calls with a specific intent, the user sees the call's sentiment, duration, agent, and a highlighted snippet of the transcription where the intent was detected. This enables rapid root cause analysis: "Why is the 'Billing Dispute' intent trending up?" → "These 5 agents handled the most billing dispute calls" → "Here's what customers are saying about pricing."

## Architecture

```
           Drill-Down Analysis Flow

   Dashboard (Aggregate View)
        |
   Click on intent → Intent Detail Page
        |
   ┌────┴────────────┐
   |                 |
   Time Series       Dimension Breakdown
   (trend chart)     (by campaign, agent,
   |                 queue, sentiment)
   |
   Click on data point
        |
   Call List (filtered by intent + time)
        |
   Click on call
        |
   Call Detail (transcription with
   highlighted intent segments)
```

## Design Decisions

- **Server-side pagination and filtering over client-side:** The call list under a drill-down view can contain thousands of calls. Server-side pagination (50 per page) with server-side sorting and filtering keeps the UI responsive. ClickHouse supports efficient pagination with `LIMIT/OFFSET` and compound indexes on (tenantId, intentId, timestamp). Trade-off: server-side pagination adds a round-trip per page but ensures the dashboard never freezes.

- **Highlighted intent segments in transcription over full transcription display:** When viewing a call that was classified with a specific intent, the transcription segments that triggered the intent classification are highlighted (yellow background). This focuses attention on the relevant parts of the conversation without requiring the user to read the entire transcript. The full transcription is available via an expandable panel. Trade-off: highlighting only works for rule-based or ML-based classifications where the specific segment can be identified; clustering-based topics may not have segment-level annotations.

- **Breadcrumb navigation with query parameters over client-side state:** The drill-down path is encoded in the URL as query parameters (e.g., `/analytics/intents?category=billing&intent=invoice&campaign=support&page=3`). This enables deep linking (share a drill-down view with a colleague), browser back/forward navigation, and bookmarking. The breadcrumb component parses the URL parameters to render the navigation trail. Trade-off: URL-based state can become long and complex for deep drill paths; paths beyond 4 levels are collapsed in the UI.

## Implementation Approach

```typescript
interface DrillDownLevel {
  type: 'category' | 'intent' | 'call_list' | 'call_detail';
  label: string;
  id: string;
  parentId?: string;
}

interface DrillCallItem {
  callSid: string;
  customerName?: string;
  agentName?: string;
  campaignName?: string;
  timestamp: number;
  duration: number;
  sentimentScore: number;
  intentConfidence: number;
  highlightedSegments: Array<{
    text: string;
    offset: number;
    confidence: number;
  }>;
}

interface DrillQuery {
  tenantId: string;
  level: DrillDownLevel['type'];
  intentId?: string;
  categoryId?: string;
  callSid?: string;
  filters?: {
    campaignIds?: string[];
    agentIds?: string[];
    sentimentMin?: number;
    sentimentMax?: number;
    dateRange?: { start: number; end: number };
  };
  sort?: 'timestamp_desc' | 'timestamp_asc' | 'sentiment_asc' | 'sentiment_desc';
  page: number;
  pageSize: number;
}

class IntentDrillService {
  private clickhouse: ClickHouseClient;

  async getDrillData(query: DrillQuery): Promise<{
    levels: DrillDownLevel[];
    items: DrillCallItem[];
    total: number;
    page: number;
    pageSize: number;
  }> {
    switch (query.level) {
      case 'category':
        return this.getCategoryLevel(query);
      case 'intent':
        return this.getIntentLevel(query);
      case 'call_list':
        return this.getCallList(query);
      case 'call_detail':
        return this.getCallDetail(query);
      default:
        throw new Error(`Unknown drill level: ${query.level}`);
    }
  }

  private async getCategoryLevel(query: DrillQuery): Promise<any> {
    const conditions = [ `tenantId = '${query.tenantId}'` ];
    if (query.filters?.dateRange) {
      conditions.push(`timestamp >= ${query.filters.dateRange.start}`);
      conditions.push(`timestamp <= ${query.filters.dateRange.end}`);
    }

    const results = await this.clickhouse.query(`
      SELECT
        id.parentId as categoryId,
        ip.name as categoryName,
        count(DISTINCT ci.callSid) as callCount,
        avg(ci.score) as avgSentiment
      FROM call_intents ci
      JOIN intent_definitions id ON ci.intentId = id.id
      LEFT JOIN intent_definitions ip ON id.parentId = ip.id
      WHERE ${conditions.join(' AND ')}
      GROUP BY categoryId, categoryName
      ORDER BY callCount DESC
    `);

    const items = results.map((r: any) => ({
      callSid: r.categoryId,
      agentName: r.categoryName,
      customerName: r.callCount.toString(),
      duration: 0,
      timestamp: 0,
      sentimentScore: r.avgSentiment,
      intentConfidence: 1,
      highlightedSegments: [],
    }));

    return {
      levels: [{ type: 'category' as const, label: 'All Intents', id: 'root' }],
      items,
      total: items.length,
      page: 1,
      pageSize: items.length,
    };
  }

  private async getIntentLevel(query: DrillQuery): Promise<any> {
    const conditions = [
      `ci.tenantId = '${query.tenantId}'`,
      `id.parentId = '${query.categoryId}'`,
    ];

    if (query.filters?.dateRange) {
      conditions.push(`ci.timestamp >= ${query.filters.dateRange.start}`);
      conditions.push(`ci.timestamp <= ${query.filters.dateRange.end}`);
    }

    const results = await this.clickhouse.query(`
      SELECT
        ci.intentId,
        id.name as intentName,
        count(DISTINCT ci.callSid) as callCount,
        avg(ci.score) as avgSentiment,
        avg(ci.confidence) as avgConfidence
      FROM call_intents ci
      JOIN intent_definitions id ON ci.intentId = id.id
      WHERE ${conditions.join(' AND ')}
      GROUP BY ci.intentId, id.name
      ORDER BY callCount DESC
    `);

    const items = results.map((r: any) => ({
      callSid: r.intentId,
      agentName: r.intentName,
      customerName: r.callCount.toString(),
      sentimentScore: r.avgSentiment,
      intentConfidence: r.avgConfidence,
      highlightedSegments: [],
    }));

    return {
      levels: [
        { type: 'category' as const, label: 'All Intents', id: 'root' },
        { type: 'intent' as const, label: `Category: ${query.categoryId}`, id: query.categoryId },
      ],
      items,
      total: items.length,
      page: 1,
      pageSize: items.length,
    };
  }

  private async getCallList(query: DrillQuery): Promise<{
    levels: DrillDownLevel[];
    items: DrillCallItem[];
    total: number;
    page: number;
    pageSize: number;
  }> {
    const offset = (query.page - 1) * query.pageSize;
    const sortClause = query.sort === 'sentiment_desc' ? 'ci.score DESC'
      : query.sort === 'sentiment_asc' ? 'ci.score ASC'
      : query.sort === 'timestamp_asc' ? 'ci.timestamp ASC'
      : 'ci.timestamp DESC';

    const conditions = [
      `ci.tenantId = '${query.tenantId}'`,
      `ci.intentId = '${query.intentId}'`,
    ];

    if (query.filters?.campaignIds && query.filters.campaignIds.length > 0) {
      conditions.push(`ci.campaignId IN (${query.filters.campaignIds.map(c => `'${c}'`).join(',')})`);
    }
    if (query.filters?.agentIds && query.filters.agentIds.length > 0) {
      conditions.push(`ci.agentId IN (${query.filters.agentIds.map(a => `'${a}'`).join(',')})`);
    }
    if (query.filters?.sentimentMin != null) {
      conditions.push(`ci.score >= ${query.filters.sentimentMin}`);
    }
    if (query.filters?.sentimentMax != null) {
      conditions.push(`ci.score <= ${query.filters.sentimentMax}`);
    }
    if (query.filters?.dateRange) {
      conditions.push(`ci.timestamp >= ${query.filters.dateRange.start}`);
      conditions.push(`ci.timestamp <= ${query.filters.dateRange.end}`);
    }

    // Count total
    const countResult = await this.clickhouse.query(`
      SELECT count(DISTINCT ci.callSid) as total
      FROM call_intents ci
      WHERE ${conditions.join(' AND ')}
    `);
    const total = countResult[0]?.total ?? 0;

    // Get calls
    const results = await this.clickhouse.query(`
      SELECT
        ci.callSid,
        ci.customerName,
        a.name as agentName,
        cmp.name as campaignName,
        ci.timestamp,
        c.duration,
        ci.score as sentimentScore,
        ci.confidence as intentConfidence,
        ci.highlightedSegments
      FROM call_intents ci
      LEFT JOIN call_records c ON ci.callSid = c.callSid
      LEFT JOIN agents a ON ci.agentId = a.id
      LEFT JOIN campaigns cmp ON ci.campaignId = cmp.id
      WHERE ${conditions.join(' AND ')}
      GROUP BY ci.callSid, ci.customerName, a.name, cmp.name, ci.timestamp, c.duration, ci.score, ci.confidence, ci.highlightedSegments
      ORDER BY ${sortClause}
      LIMIT ${query.pageSize} OFFSET ${offset}
    `);

    const items: DrillCallItem[] = results.map((r: any) => ({
      callSid: r.callSid,
      customerName: r.customerName,
      agentName: r.agentName,
      campaignName: r.campaignName,
      timestamp: r.timestamp,
      duration: r.duration,
      sentimentScore: r.sentimentScore,
      intentConfidence: r.intentConfidence,
      highlightedSegments: (r.highlightedSegments ?? []).map((s: any) => ({
        text: s.text,
        offset: s.offset,
        confidence: s.confidence,
      })),
    }));

    return {
      levels: [
        { type: 'category', label: 'All Intents', id: 'root' },
        { type: 'intent', label: `Intent: ${query.intentId}`, id: query.intentId, parentId: query.categoryId },
        { type: 'call_list', label: 'Calls', id: `calls:${query.intentId}` },
      ],
      items,
      total,
      page: query.page,
      pageSize: query.pageSize,
    };
  }

  private async getCallDetail(query: DrillQuery): Promise<any> {
    const callSid = query.callSid!;

    const result = await this.clickhouse.query(`
      SELECT
        c.*,
        ci.intentId,
        id.name as intentName,
        ci.score as sentimentScore,
        ci.highlightedSegments
      FROM call_records c
      JOIN call_intents ci ON c.callSid = ci.callSid
      JOIN intent_definitions id ON ci.intentId = id.id
      WHERE c.callSid = '${callSid}'
        AND ci.intentId = '${query.intentId}'
    `);

    if (result.length === 0) {
      return { levels: [], items: [], total: 0, page: 1, pageSize: 50 };
    }

    const call = result[0];

    return {
      levels: [
        { type: 'category', label: 'All Intents', id: 'root' },
        { type: 'intent', label: `Intent: ${call.intentName}`, id: call.intentId },
        { type: 'call_list', label: 'Calls', id: `calls:${call.intentId}` },
        { type: 'call_detail', label: `Call: ${callSid}`, id: callSid },
      ],
      items: [{
        callSid: call.callSid,
        customerName: call.customerName,
        agentName: call.agentName,
        campaignName: call.campaignName,
        timestamp: call.timestamp,
        duration: call.duration,
        sentimentScore: call.sentimentScore,
        intentConfidence: call.intentConfidence,
        highlightedSegments: call.highlightedSegments ?? [],
      }],
      total: 1,
      page: 1,
      pageSize: 1,
    };
  }
}

// Drill-down call list component
const DrillCallList: React.FC<{
  items: DrillCallItem[];
  total: number;
  page: number;
  onPageChange: (page: number) => void;
  onCallSelect: (callSid: string) => void;
}> = ({ items, total, page, onPageChange, onCallSelect }) => (
  <div className="drill-call-list">
    <table>
      <thead>
        <tr>
          <th>Call ID</th>
          <th>Customer</th>
          <th>Agent</th>
          <th>Sentiment</th>
          <th>Duration</th>
          <th>Intent Confidence</th>
        </tr>
      </thead>
      <tbody>
        {items.map(item => (
          <tr key={item.callSid} onClick={() => onCallSelect(item.callSid)} className="clickable">
            <td>{item.callSid}</td>
            <td>{item.customerName ?? 'Unknown'}</td>
            <td>{item.agentName ?? 'Unknown'}</td>
            <td><SentimentBadge score={item.sentimentScore} /></td>
            <td>{formatDuration(item.duration)}</td>
            <td>{(item.intentConfidence * 100).toFixed(0)}%</td>
          </tr>
        ))}
      </tbody>
    </table>
    <Pagination current={page} total={Math.ceil(total / 50)} onChange={onPageChange} />
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Drill-down queries |
| React Router (MIT) | Client | URL-based drill state |
| React Table (MIT) | Client | Call list table |
| React Virtualized (MIT) | Client | Virtual scrolling for large lists |

## Production Considerations

**Scaling:** The call list query filters by intentId and timestamp — ensure a compound index on (tenantId, intentId, timestamp). For tenants with >100K calls per intent, pagination with large offsets can be slow; use keyset pagination (WHERE timestamp < lastTimestamp) instead of LIMIT/OFFSET. The transcription highlight segments are stored as JSON arrays in ClickHouse — limit to top 5 segments per call to keep response sizes manageable.

**Security:** Drill-down reveals call SIDs, customer names, agent names, and transcription snippets. Access requires escalating permissions: `analytics:view` for the intent overview, `calls:view` for the call list, and `calls:view-transcription` for the highlighted segments. The drill-down component checks permissions at each level and shows a "permission denied" message if the user lacks access.

**Monitoring:** Track drill-down navigation depth (average number of drill steps per session). Alert if any drill query exceeds 2 seconds — review query performance and indexing. Monitor the most common drill paths to optimize pre-computation and caching.
