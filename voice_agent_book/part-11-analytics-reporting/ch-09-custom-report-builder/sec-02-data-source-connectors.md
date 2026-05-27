# Section 02: Data Source Connectors

## Overview

Data source connectors bridge the report builder to the underlying analytics data stores, providing a unified query interface that abstracts away differences between SQL databases, Elasticsearch indices, time-series databases, and REST API endpoints. Each connector implements a common `DataSourceConnector` interface that exposes schema discovery, query execution, pagination, and caching. Analysts building reports select a data source and pick metrics and dimensions from the connector's discovered schema rather than writing raw queries.

The connector architecture supports multiple storage backends: TimescaleDB for time-series analytics data, Elasticsearch for text and log analytics, Redis for real-time metrics, and ClickHouse for large-scale aggregation queries. Each connector handles backend-specific query syntax, connection pooling, and error handling while presenting a consistent GraphQL-like query interface to the report builder UI. The schema discovery process introspects the backend and caches the results, refreshing every 15 minutes or on demand.

## Architecture

```
                   Data Source Connector Architecture

   Report Builder → Data Source Manager
                          |
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
       PostgreSQL    Elasticsearch   ClickHouse
       Connector     Connector       Connector
            |             |             |
            ▼             ▼             ▼
       Connection    Connection     Connection
       Pool          Pool           Pool
            |             |             |
       ┌────┴─────────────┴─────────────┴────┐
       ▼                                     ▼
   Schema Cache                          Query Cache
   (Redis)                              (Redis)
```

## Design Decisions

- **GraphQL-style query interface over raw SQL injection:** The connector accepts a structured query object (metrics, dimensions, filters, groupBy, orderBy, limit) rather than raw SQL strings. This prevents SQL injection, enables cross-backend compatibility, and allows the UI to auto-complete field names. Trade-off: the structured query format cannot express all SQL features (window functions, subqueries, CTEs), limiting advanced users; a "raw query" escape hatch with strict validation addresses this.

- **Schema discovery with TTL caching over static schema definition:** Each connector exposes a `discoverSchema()` method that introspects the backend's tables, columns, and types. The schema is cached in Redis with a 15-minute TTL. When a new data source is added or schema changes are detected, an invalidation event refreshes the cache. Trade-off: schema caching can serve stale field lists if a database migration adds columns between cache refreshes; a manual "refresh schema" button in the UI mitigates this.

- **Query result pagination with cursor-based keyset over offset-based:** All connectors implement cursor-based pagination using a sort-key cursor (typically the row's timestamp or ID). This ensures stable pagination results even when new data is inserted between pages. Trade-off: cursor-based pagination requires the connector to know the sort field and cannot jump to arbitrary pages (page 5 of 20), requiring the UI to implement "load more" or infinite scroll instead of traditional pagination controls.

## Implementation Approach

```typescript
interface DataSourceConnector {
  type: string;
  connect(config: DataSourceConfig): Promise<void>;
  disconnect(): Promise<void>;
  discoverSchema(): Promise<DataSourceSchema>;
  query(params: QueryParams): Promise<QueryResult>;
  queryOne(params: QueryParams): Promise<Record<string, unknown>>;
  estimateRowCount(params: QueryParams): Promise<number>;
}

interface DataSourceConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string; // never stored, injected at runtime
  sslMode: 'require' | 'prefer' | 'disable';
  poolSize: number;
  timeoutMs: number;
}

interface DataSourceSchema {
  tables: TableSchema[];
  lastRefreshed: number;
}

interface TableSchema {
  name: string;
  columns: ColumnSchema[];
  estimatedRowCount: number;
  description?: string;
}

interface ColumnSchema {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'date' | 'timestamp' | 'array' | 'json';
  nullable: boolean;
  isMetric: boolean;
  isDimension: boolean;
  enumValues?: string[];
  description?: string;
}

interface QueryParams {
  table: string;
  metrics: MetricField[];
  dimensions: string[];
  filters: QueryFilter[];
  groupBy: string[];
  orderBy: { field: string; direction: 'asc' | 'desc' }[];
  limit: number;
  cursor?: string;
  timeRange?: { start: number; end: number; granularity: string };
}

interface MetricField {
  field: string;
  aggregation: 'sum' | 'avg' | 'count' | 'min' | 'max' | 'distinct' | 'percentile';
  alias: string;
}

interface QueryFilter {
  field: string;
  operator: 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'in' | 'between' | 'contains' | 'regex';
  value: unknown;
}

interface QueryResult {
  columns: string[];
  rows: Record<string, unknown>[];
  totalRows: number;
  cursor?: string;
  hasMore: boolean;
  executionTimeMs: number;
}

class PostgreSQLConnector implements DataSourceConnector {
  private pool: pg.Pool;
  private schemaCache: DataSourceSchema | null = null;

  type = 'postgresql';

  async connect(config: DataSourceConfig): Promise<void> {
    this.pool = new pg.Pool({
      host: config.host,
      port: config.port,
      database: config.database,
      user: config.username,
      password: config.password,
      ssl: config.sslMode === 'require' ? { rejectUnauthorized: true } : false,
      max: config.poolSize,
      connectionTimeoutMillis: config.timeoutMs,
    });
  }

  async disconnect(): Promise<void> {
    await this.pool.end();
  }

  async discoverSchema(): Promise<DataSourceSchema> {
    if (this.schemaCache) return this.schemaCache;

    const tables = await this.pool.query(`
      SELECT table_name, (SELECT COUNT(*) FROM information_schema.tables
       WHERE table_schema = 'public') as all_tables
    `);

    const schema: DataSourceSchema = {
      tables: [],
      lastRefreshed: Date.now(),
    };

    for (const row of tables.rows) {
      const columns = await this.pool.query(`
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = $1
      `, [row.table_name]);

      schema.tables.push({
        name: row.table_name,
        columns: columns.rows.map(col => ({
          name: col.column_name,
          type: this.mapPgType(col.data_type),
          nullable: col.is_nullable === 'YES',
          isMetric: this.isMetricType(col.data_type),
          isDimension: this.isDimensionType(col.data_type),
        })),
        estimatedRowCount: 0,
      });
    }

    this.schemaCache = schema;
    return schema;
  }

  async query(params: QueryParams): Promise<QueryResult> {
    const { sql, values } = this.buildQuery(params);
    const start = Date.now();
    const result = await this.pool.query(sql, values);
    const executionTimeMs = Date.now() - start;

    return {
      columns: params.metrics.map(m => m.alias),
      rows: result.rows,
      totalRows: result.rows.length,
      hasMore: result.rows.length >= params.limit,
      executionTimeMs,
    };
  }

  private buildQuery(params: QueryParams): { sql: string; values: unknown[] } {
    const selectFields = [
      ...params.dimensions,
      ...params.metrics.map(m => `${m.aggregation}("${m.field}") AS "${m.alias}"`),
    ];

    const whereClauses: string[] = [];
    const values: unknown[] = [];
    let paramIndex = 1;

    if (params.timeRange) {
      whereClauses.push(`"timestamp" >= $${paramIndex++} AND "timestamp" < $${paramIndex++}`);
      values.push(new Date(params.timeRange.start), new Date(params.timeRange.end));
    }

    for (const filter of params.filters) {
      whereClauses.push(`"${filter.field}" ${this.filterOperator(filter, paramIndex)}`);
      values.push(filter.value);
      paramIndex++;
    }

    const sql = `
      SELECT ${selectFields.join(', ')}
      FROM "${params.table}"
      ${whereClauses.length > 0 ? 'WHERE ' + whereClauses.join(' AND ') : ''}
      ${params.groupBy.length > 0 ? 'GROUP BY ' + params.groupBy.map(g => `"${g}"`).join(', ') : ''}
      ${params.orderBy.length > 0 ? 'ORDER BY ' + params.orderBy.map(o => `"${o.field}" ${o.direction}`).join(', ') : ''}
      LIMIT ${params.limit}
    `;

    return { sql, values };
  }

  private filterOperator(filter: QueryFilter, paramIndex: number): string {
    switch (filter.operator) {
      case 'eq': return `= $${paramIndex}`;
      case 'neq': return `!= $${paramIndex}`;
      case 'gt': return `> $${paramIndex}`;
      case 'gte': return `>= $${paramIndex}`;
      case 'lt': return `< $${paramIndex}`;
      case 'lte': return `<= $${paramIndex}`;
      case 'in': return `= ANY($${paramIndex}::text[])`;
      case 'contains': return `LIKE '%' || $${paramIndex} || '%'`;
      case 'between': return `BETWEEN $${paramIndex} AND $${paramIndex + 1}`;
      default: return `= $${paramIndex}`;
    }
  }

  private mapPgType(pgType: string): ColumnSchema['type'] {
    if (pgType.startsWith('int') || pgType.startsWith('float') || pgType === 'numeric' || pgType === 'double precision') return 'number';
    if (pgType === 'boolean') return 'boolean';
    if (pgType === 'date') return 'date';
    if (pgType.startsWith('timestamp')) return 'timestamp';
    if (pgType === 'json' || pgType === 'jsonb') return 'json';
    return 'string';
  }

  private isMetricType(pgType: string): boolean {
    return ['int', 'float', 'numeric', 'double', 'bigint', 'real'].some(t => pgType.startsWith(t));
  }

  private isDimensionType(pgType: string): boolean {
    return ['timestamp', 'date', 'varchar', 'text', 'boolean'].some(t => pgType.startsWith(t));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| node-postgres (MIT) | Server | PostgreSQL connector |
| @elastic/elasticsearch (Apache 2.0) | Server | Elasticsearch connector |
| ClickHouse JDBC (Apache 2.0) | Server | ClickHouse connector |
| Redis (RSAL) | Server | Schema and query cache |

## Production Considerations

**Scaling:** Each connector maintains a configurable connection pool. For PostgreSQL, pool size defaults to 10 per connector instance and scales with the number of concurrent report queries. Query results are cached in Redis with a TTL based on the data source type (real-time sources: 30 seconds; batch sources: 5 minutes). Long-running queries (> 30 seconds) are executed asynchronously with a callback token. Schema discovery runs on a cron schedule per data source, staggered to avoid all connectors refreshing simultaneously.

**Security:** Database credentials are stored in a secrets manager (AWS Secrets Manager or HashiCorp Vault) and injected into connector config at connection time — never persisted in the report definition or schema cache. Each connector uses a read-only database role with `SELECT`-only permissions and no access to system tables beyond schema introspection. Queries are parameterized to prevent injection; the structured query format is validated against the discovered schema before execution.

**Monitoring:** Track per-connector query latency (p50, p95, p99), connection pool utilization, schema cache hit ratio, error rate by error type (connection, timeout, syntax, permission), and query result size distribution. Alert if any connector's p99 query latency exceeds 10 seconds, if connection pool utilization exceeds 80%, or if schema discovery fails for more than 5 minutes.
