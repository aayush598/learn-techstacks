# Section 03: Pagination & Filtering

## Overview

The Voice Agent API uses cursor-based pagination for all list endpoints. Cursor pagination provides consistent results even when data changes between requests — unlike offset pagination which can skip or duplicate items when rows are inserted or deleted. Filtering uses query parameters with a consistent syntax across all resources, supporting equality, range, and text search operators.

## Architecture

```
Pagination Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Offset Pagination (not used):
  GET /v1/agents?offset=40&limit=20
  Problem: New agent inserted at position 0 shifts all rows
           → Items skipped or duplicated

Cursor Pagination (used):
  GET /v1/agents?cursor=ag_abc_123&limit=20
  Response: { "data": [...], "pagination": { "cursor": "ag_xyz_789", "hasMore": true } }
  Next: GET /v1/agents?cursor=ag_xyz_789&limit=20

Filtering Syntax:
  GET /v1/agents?status=active                        → Exact match
  GET /v1/agents?createdAt[gte]=2025-06-01&createdAt[lte]=2025-06-30  → Range
  GET /v1/agents?query=customer+support               → Text search
  GET /v1/agents?fields=id,name,status                 → Field selection
  GET /v1/agents?sort=createdAt:desc                   → Sorting
```

## Design Decisions

- **Cursor Over Offset**: Cursors are opaque base64-encoded tokens pointing to the last item; they handle concurrent writes correctly and perform consistently on large datasets
- **Composite Sort Cursors**: For sorted lists, cursors encode sort values + primary key for unambiguous positioning
- **Query Parameter Filtering**: Filters use query parameters only — never in the request body for GET requests
- **Field Selection**: Clients can request specific fields to reduce response size and latency

## Implementation Approach

```typescript
// Pagination types
interface PaginationParams {
  cursor?: string;
  limit: number;
}

interface PaginationMeta {
  cursor: string | null;
  hasMore: boolean;
  total?: number;
}

interface FilterParams {
  status?: string;
  query?: string;
  createdAt?: RangeFilter<Date>;
  updatedAt?: RangeFilter<Date>;
  tags?: string[];
  [key: string]: unknown;
}

interface RangeFilter<T> {
  gte?: T;
  lte?: T;
  gt?: T;
  lt?: T;
}

// Cursor encoding
class CursorCodec {
  encode(sortValue: string, primaryKey: string): string {
    const payload = JSON.stringify({ s: sortValue, pk: primaryKey });
    return Buffer.from(payload).toString('base64url');
  }

  decode(cursor: string): { sortValue: string; primaryKey: string } {
    const payload = Buffer.from(cursor, 'base64url').toString();
    return JSON.parse(payload);
  }
}

// Paginated query service
class AgentQueryService {
  async list(filters: FilterParams, pagination: PaginationParams): Promise<ListResponse<Agent>> {
    const limit = Math.min(pagination.limit, 100);
    const query = this.buildQuery(filters);

    if (pagination.cursor) {
      const { sortValue, primaryKey } = this.cursorCodec.decode(pagination.cursor);
      query.where('createdAt').lte(new Date(sortValue));
      query.where('id').lt(primaryKey);
    }

    query.orderBy('createdAt', 'desc');
    query.limit(limit + 1); // Fetch one extra to detect hasMore

    const items = await query.execute();
    const hasMore = items.length > limit;
    const results = hasMore ? items.slice(0, limit) : items;

    const nextCursor = hasMore
      ? this.cursorCodec.encode(
          results[results.length - 1].createdAt.toISOString(),
          results[results.length - 1].id
        )
      : null;

    return {
      data: results,
      pagination: { cursor: nextCursor, hasMore },
    };
  }

  private buildQuery(filters: FilterParams): QueryBuilder {
    const query = this.db.queryBuilder('agents');

    if (filters.status) {
      query.where('status', filters.status);
    }
    if (filters.createdAt) {
      if (filters.createdAt.gte) query.where('createdAt', '>=', filters.createdAt.gte);
      if (filters.createdAt.lte) query.where('createdAt', '<=', filters.createdAt.lte);
    }
    if (filters.query) {
      query.whereRaw('search_vector @@ plainto_tsquery(?)', [filters.query]);
    }
    return query;
  }
}
```

## Integration Points

- **SDK Integration**: Cursor handling is abstracted in the client — SDK users call `client.agents.list()` and iterate with `for await`
- **API Gateway**: Pagination limits are enforced at the gateway level before reaching services
- **Search Engine**: Full-text search queries can be routed to Meilisearch/Algolia for complex queries

## Production Considerations

- **Default Limits**: Default limit of 20, maximum of 100 to prevent abuse
- **Cursor Expiry**: Cursors are valid for 24 hours; expired cursors return an error
- **Performance Indexing**: Cursor queries require composite indexes on (sort_field, id); without them, queries degrade to table scans
- **Total Count Cost**: The `total` field is opt-in and expensive — it requires COUNT queries on large tables; omitted by default

## Open-Source Tools

- **Zod**: Schema validation for pagination parameters and filter types
- **PostgreSQL / CockroachDB**: Native support for cursor-based pagination with composite indexes
- **Meilisearch**: Full-text search engine for query filtering
