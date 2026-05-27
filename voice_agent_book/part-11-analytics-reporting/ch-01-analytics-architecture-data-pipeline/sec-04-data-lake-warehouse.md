# Section 04: Data Lake and Warehouse

## Overview

The data lake and warehouse layer provides durable, queryable storage for all analytics data. The data lake (object storage with Parquet files) serves as the system of record — an immutable, cost-effective archive of all raw events. The data warehouse (ClickHouse) provides fast analytical queries on aggregated and materialized data, serving dashboards, reports, and ad-hoc analytics queries. Data flows from Kafka to the data lake via a sink connector and into the data warehouse through stream and batch processing.

The data lake stores raw events partitioned by date and tenant ID for efficient query pruning. Parquet format with Snappy compression achieves 5-10x storage reduction compared to JSON. Schema evolution is handled through Parquet's native schema merge capability — new columns are added with default values for older data. The warehouse contains both pre-computed aggregations (daily metrics, hourly call volumes) and materialized views that combine real-time and batch data for consistent query results.

## Architecture

```
   Kafka → S3 Sink Connector → Data Lake (Parquet)
     |                              |
     v                              v
  Stream Proc ──────────────→ ClickHouse (Warehouse)
     |                              |
     v                              v
  Batch Proc → Data Lake         Dashboards
    (Hourly)    (Backfill)
```

## Design Decisions

- **Data lake as system of record over warehouse-first:** All raw event data is written to the data lake (S3/Parquet) before any processing. The warehouse is rebuilt from the data lake in case of corruption or schema migration. This provides an immutable audit trail and enables reprocessing with updated logic. The data lake is write-once, read-many — data is never modified in place. Trade-off: dual storage doubles storage cost (though Parquet is cheap) but provides an irreplaceable durability and reprocessing capability.

- **Hive-style partitioning for query efficiency over flat storage:** Data is partitioned by `dt=YYYY-MM-DD/tenant_id=XXXXX/hour=HH` in the data lake. This enables partition pruning — queries that filter by date and tenant only scan the relevant directories. Partition columns are also used as ClickHouse sharding keys. Hourly partitions balance granularity (fast queries for daily ranges) and partition count (8760 partitions per year per tenant). Trade-off: fine-grained partitioning increases the number of files (small file problem) but dramatically reduces query scan size.

- **Materialized views in ClickHouse for hybrid real-time/batch consistency over separate tables:** ClickHouse materialized views continuously ingest data from Kafka and maintain real-time aggregates. Batch jobs run hourly to recalculate the same aggregates from the data lake and replace the materialized view data if there are discrepancies (late-arriving data corrections). Queries read from the materialized views, which automatically include both real-time and corrected batch data. Trade-off: materialized view maintenance adds CPU overhead during data ingestion but provides a single query endpoint with consistent, corrected data.

## Implementation Approach

```
class DataLakeManager {
  private s3: S3Client;
  private parquetWriter: ParquetWriter;

  constructor(private config: { bucket: string; prefix: string }) {
    this.s3 = new S3Client({});
  }

  async writeEventBatch(events: Record<string, any>[], eventType: string, partitionDate: Date): Promise<void> {
    const partitionPath = this.buildPartitionPath(partitionDate, events[0]?._metadata?.tenantId);
    const fileKey = `${this.config.prefix}/${eventType}/${partitionPath}/${uuidv4()}.snappy.parquet`;

    // Convert to Parquet
    const schema = this.inferSchema(events);
    const rows = events.map(e => this.flattenEvent(e));

    const buffer = await this.parquetWriter.writeBuffer(schema, rows, { compression: 'SNAPPY' });

    // Upload to S3
    await this.s3.send(new PutObjectCommand({
      Bucket: this.config.bucket,
      Key: fileKey,
      Body: buffer,
      ContentType: 'application/octet-stream',
    }));

    logger.debug('Events written to data lake', { eventType, count: events.length, fileKey });
  }

  private buildPartitionPath(date: Date, tenantId: string): string {
    const dt = date.toISOString().split('T')[0];
    const hour = date.getUTCHours().toString().padStart(2, '0');
    return `dt=${dt}/tenant_id=${tenantId}/hour=${hour}`;
  }

  private flattenEvent(event: Record<string, any>): Record<string, any> {
    const flat: Record<string, any> = {};
    for (const [key, value] of Object.entries(event)) {
      if (typeof value !== 'object' || value === null || Array.isArray(value)) {
        flat[key] = value;
      } else if (value instanceof Date) {
        flat[key] = value.toISOString();
      } else {
        for (const [subKey, subValue] of Object.entries(value)) {
          flat[`${key}_${subKey}`] = subValue;
        }
      }
    }
    return flat;
  }

  async batchWriteFromKafka(topic: string, partition: number, offset: number): Promise<void> {
    // Read batch from Kafka, write to data lake, commit offset
  }
}

class ClickHouseWarehouse {
  private client: ClickHouseClient;

  constructor(config: { host: string; port: number; database: string; user: string; password: string }) {
    this.client = createClient(config);
  }

  async initializeSchema(): Promise<void> {
    await this.client.exec({
      query: `
        CREATE TABLE IF NOT EXISTS call_events (
          callSid String,
          tenantId String,
          campaignId Nullable(String),
          agentId Nullable(String),
          duration Nullable(Int32),
          status String,
          customerPhone Nullable(String),
          timestamp DateTime64(3),
          ingestedAt DateTime64(3),
          metadata Map(String, String)
        ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/call_events', '{replica}')
          PARTITION BY toYYYYMM(timestamp)
          ORDER BY (tenantId, toDate(timestamp), callSid)
          SAMPLE BY callSid
          SETTINGS index_granularity = 8192
      `,
    });

    // Materialized view for real-time aggregations
    await this.client.exec({
      query: `
        CREATE MATERIALIZED VIEW IF NOT EXISTS call_metrics_hourly
        ENGINE = SummingMergeTree()
          PARTITION BY toYYYYMM(hour)
          ORDER BY (tenantId, hour, campaignId)
        AS SELECT
          tenantId,
          toStartOfHour(timestamp) AS hour,
          campaignId,
          count() AS totalCalls,
          countIf(status = 'completed') AS answeredCalls,
          avg(duration) AS avgDuration,
          quantile(0.95)(duration) AS p95Duration,
          uniq(customerPhone) AS uniqueCallers
        FROM call_events
        GROUP BY tenantId, hour, campaignId
      `,
    });

    logger.info('ClickHouse schema initialized');
  }

  async insertEvents(events: Record<string, any>[]): Promise<void> {
    await this.client.insert({
      table: 'call_events',
      values: events.map(e => ({
        callSid: e.callSid,
        tenantId: e._metadata?.tenantId,
        campaignId: e.campaignId,
        agentId: e.agentId,
        duration: e.duration,
        status: e.status,
        customerPhone: e.customerPhone,
        timestamp: new Date(e.timestamp),
        ingestedAt: new Date(e._metadata?.ingestedAt),
        metadata: e.metadata || {},
      })),
      format: 'JSONEachRow',
    });
  }

  async queryCallMetrics(params: {
    tenantId: string;
    startDate: Date;
    endDate: Date;
    granularity: 'hour' | 'day' | 'week';
    campaignId?: string;
  }): Promise<CallMetricsRow[]> {
    const granularityMap = { hour: 'toStartOfHour', day: 'toStartOfDay', week: 'toStartOfWeek' };
    const granularityFn = granularityMap[params.granularity];

    const result = await this.client.query({
      query: `
        SELECT
          tenantId,
          ${granularityFn}(timestamp) AS period,
          campaignId,
          sum(totalCalls) AS totalCalls,
          sum(answeredCalls) AS answeredCalls,
          avg(avgDuration) AS avgDuration,
          max(p95Duration) AS p95Duration,
          sum(uniqueCallers) AS uniqueCallers
        FROM call_metrics_hourly
        WHERE tenantId = {tenantId:String}
          AND hour >= {startDate:DateTime}
          AND hour <= {endDate:DateTime}
          ${params.campaignId ? 'AND campaignId = {campaignId:String}' : ''}
        GROUP BY tenantId, period, campaignId
        ORDER BY period ASC
      `,
      params: {
        tenantId: params.tenantId,
        startDate: params.startDate.toISOString(),
        endDate: params.endDate.toISOString(),
        campaignId: params.campaignId,
      },
      format: 'JSONEachRow',
    });

    return result as CallMetricsRow[];
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Columnar data warehouse |
| ParquetJS (MIT) | Node.js | Parquet file writing |
| AWS SDK (Apache 2.0) | Node.js | S3 data lake storage |
| MinIO (AGPL 3.0) | Server | Self-hosted S3 alternative |

## Production Considerations

**Scaling:** Data lake storage grows linearly with call volume. Estimate 1KB per call event in Parquet (compressed). For 1 million calls/day with 5 events each: ~5GB/day uncompressed, ~500MB/day in Parquet. Partition by date prevents any single directory from growing unbounded. ClickHouse uses distributed tables across multiple shards — choose shard key (tenant ID) to balance data. Use ReplicatedMergeTree for high availability.

**Security:** Data lake files contain raw event data including PII — enable S3 encryption at rest (SSE-S3 or SSE-KMS) and enforce bucket policies that prevent public access. ClickHouse supports role-based access control at the row level — enforce tenant isolation via ClickHouse row policies that filter by tenant ID. Never grant direct ClickHouse access to end users; expose only through the API layer.

**Monitoring:** Track data lake write throughput (MB/s), partition file count (too many small files degrades query performance — use 64MB target file size), ClickHouse query performance by query pattern, merge tree optimization status, and partition storage size. Alert on data lake write failures, ClickHouse query timeouts, and partition imbalance across ClickHouse shards.
