# Log Search & Filtering

## Overview

Log search and filtering provides full-text search across activity logs with structured query filters, date range filtering, and Elasticsearch integration for high-performance querying at scale.

## Search Implementation

```typescript
interface LogSearchQuery {
  query?: string;                          // Full-text search
  filters: {
    actions?: string[];
    actorIds?: string[];
    targetType?: string;
    targetId?: string;
    severity?: string[];
    source?: string[];
  };
  dateRange: {
    start: Date;
    end: Date;
  };
  sort: 'timestamp_desc' | 'timestamp_asc';
  limit: number;
  offset: number;
}

interface LogSearchResult {
  total: number;
  hits: ActivityEvent[];
  aggregations: {
    actions: TermAggregation[];
    actors: TermAggregation[];
    targets: TermAggregation[];
    severity: TermAggregation[];
    timeline: TimeSeriesPoint[];
  };
}

class LogSearchService {
  private es: ElasticsearchClient;

  async search(query: LogSearchQuery): Promise<LogSearchResult> {
    const must: any[] = [];
    const filter: any[] = [];

    // Full-text search
    if (query.query) {
      must.push({
        multi_match: {
          query: query.query,
          fields: ['action', 'actor.email', 'target.name', 'target.id', 'metadata.*'],
        },
      });
    }

    // Filters
    if (query.filters.actions?.length) {
      filter.push({ terms: { action: query.filters.actions } });
    }
    if (query.filters.severity?.length) {
      filter.push({ terms: { severity: query.filters.severity } });
    }
    if (query.filters.source?.length) {
      filter.push({ terms: { 'context.source': query.filters.source } });
    }

    // Date range
    filter.push({
      range: { timestamp: { gte: query.dateRange.start, lte: query.dateRange.end } },
    });

    const response = await this.es.search({
      index: 'activity_logs',
      body: {
        query: { bool: { must, filter } },
        sort: [{ timestamp: { order: query.sort === 'timestamp_desc' ? 'desc' : 'asc' } }],
        from: query.offset,
        size: query.limit,
        aggs: {
          actions: { terms: { field: 'action', size: 20 } },
          actors: { terms: { field: 'actor.id', size: 10 } },
          severity: { terms: { field: 'severity' } },
          timeline: {
            date_histogram: { field: 'timestamp', calendar_interval: 'hour' },
          },
        },
      },
    });

    return this.formatResponse(response, query);
  }
}
```

## Filter UI

```
Search: [🔍 Delete agent "test-123"    ] [Search]
Filters:
  Action: [campaign.created ▼] [+ Add]
  Actor: [user_id] [___________]
  Severity: [✓ info] [✓ warning] [✓ error] [✓ critical]
  Date: [2025-06-01] to [2025-06-15]
  Source: [✓ app] [✓ api] [✓ admin] [✓ system]

Results: 2,345 matches  [Export CSV ▼]
```

## Open-Source Tools

- **Elasticsearch** (Apache 2.0 / Elastic License) — Full-text search engine
- **Meilisearch** (MIT) — Lightweight search alternative
- **Kibana** — Log visualization dashboards

## Production Considerations

- Use Elasticsearch for logs exceeding 10M records
- Set index template with appropriate mappings and analyzers
- Implement query timeout (max 10 seconds)
- Cache frequent searches (last 1 hour)
- Limit search results to 10,000 max
- Provide field suggestions for filter values
- Export search results as CSV/JSON for offline analysis
- Restrict search to user's tenant only
