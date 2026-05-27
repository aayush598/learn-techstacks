# Section 01: Analytics Pipeline Architecture

## Overview

The analytics pipeline architecture defines the end-to-end data flow for collecting, processing, storing, and analyzing voice agent platform data. The pipeline ingests raw telephony events (call start, end, DTMF input, transcription segments), enriches them with contextual data (customer profiles, agent assignments, campaign metadata), processes them through real-time and batch computation layers, and stores the results in an analytics data store for querying and dashboarding.

The pipeline is designed for high throughput (thousands of concurrent calls generating events at sub-second intervals) and low latency (real-time dashboards require sub-5-second event-to-display latency). It follows the Lambda architecture pattern with both a speed layer (real-time stream processing) and a batch layer (hourly/daily aggregations for accuracy and historical analysis). The pipeline uses Apache Kafka as the central event bus, with stream processing via Apache Flink or similar, and storage in a columnar data warehouse (ClickHouse, Snowflake, or DuckDB for self-hosted).

## Architecture

```
               Analytics Pipeline Architecture

   Call Events → Event Bus → Stream Proc → Real-time DB → Dashboard
                    |              |
                    |              v
                    |         Batch Proc → Data Lake → Warehouse
                    v
               Event Archive (S3)
```

## Design Decisions

- **Lambda architecture with stream and batch convergence over pure streaming:** The stream processing layer provides sub-second aggregations for real-time dashboards using approximate algorithms (HyperLogLog for unique counts, t-digest for percentiles). The batch layer reprocesses the same data every hour with exact computations to correct any approximations or late-arriving data. The results from both layers are combined in the serving layer. Trade-off: dual processing doubles infrastructure cost but provides both real-time responsiveness and data accuracy.

- **Schema-on-read data lake with schema registry over strict schema-on-write:** Raw events are stored in Parquet format in S3 (or equivalent object storage) with a schema registry that tracks field definitions. The stream processing layer uses a strict schema for performance, but the data lake allows schema evolution (new fields added without backfilling). Analytics queries access the data lake through a query engine that applies schemas at read time. Trade-off: schema-on-read may cause compatibility issues with older data but enables agile schema evolution without downtime.

- **Columnar storage (ClickHouse) over row-oriented (PostgreSQL) for analytics:** Analytics queries typically aggregate millions of events across a subset of columns. Columnar storage compresses data by column (10x compression ratios), scans only relevant columns, and supports vectorized query execution. PostgreSQL is used for operational data (user accounts, configurations), while ClickHouse is the analytics store. Trade-off: columnar storage is slower for single-record lookups and does not support full ACID transactions but provides 100-1000x faster analytical queries.

## Implementation Approach

```
interface CallEvent {
  eventType: 'call.started' | 'call.ended' | 'call.transcription' | 'call.sentiment';
  callSid: string;
  timestamp: number;        // Unix ms
  tenantId: string;
  campaignId?: string;
  agentId?: string;
  customerPhone?: string;
  duration?: number;
  status?: string;
  transcription?: string;
  sentiment?: { score: number; label: string };
  metadata?: Record<string, string>;
}

class AnalyticsPipeline {
  private producer: KafkaProducer;
  private streamProcessor: StreamProcessor;
  private batchProcessor: BatchProcessor;
  private schemaRegistry: SchemaRegistry;

  async ingestEvent(event: CallEvent): Promise<void> {
    // Validate against schema registry
    const schema = this.schemaRegistry.getSchema(event.eventType);
    const valid = schema.validate(event);
    if (!valid) {
      logger.error('Event validation failed', { eventType: event.eventType, errors: schema.errors });
      return; // or send to DLQ
    }

    // Publish to Kafka
    await this.producer.send({
      topic: `events.${event.eventType}`,
      key: event.callSid,
      value: JSON.stringify(event),
      headers: { tenantId: event.tenantId, eventType: event.eventType },
    });
  }

  async start(): Promise<void> {
    // Start stream processing
    await this.streamProcessor.start({
      inputTopics: ['events.call.*'],
      outputTopic: 'aggregates.realtime',
      windowSizeMs: 60000, // 1-minute tumbling windows
      aggregations: [
        { field: 'callSid', function: 'count', as: 'callCount' },
        { field: 'duration', function: 'avg', as: 'avgDuration' },
        { field: 'duration', function: 'p95', as: 'p95Duration' },
        { field: 'sentiment.score', function: 'avg', as: 'avgSentiment' },
        { field: 'customerPhone', function: 'count_distinct', as: 'uniqueCallers' },
      ],
    });

    // Start batch processor (hourly)
    await this.batchProcessor.start({
      schedule: '0 * * * *',
      sourceTopic: 'events.*',
      outputTable: 'analytics.daily_aggregations',
      queries: [
        `INSERT INTO analytics.daily_aggregations
         SELECT tenantId, toDate(timestamp) as date, campaignId,
                count(*) as totalCalls,
                countDistinct(customerPhone) as uniqueCallers,
                avg(duration) as avgDuration,
                quantile(0.95)(duration) as p95Duration
         FROM events.call_ended
         WHERE timestamp >= now() - INTERVAL 2 HOUR
         GROUP BY tenantId, date, campaignId`,
      ],
    });
  }
}

// Kafka topic naming convention
const TOPIC_PATTERNS = {
  raw: 'events.{eventType}',            // Raw events
  enriched: 'enriched.{eventType}',      // Enriched with context
  aggregates: 'agg.{granularity}.{metric}', // Pre-computed aggregates
  alerts: 'alerts.{severity}',           // Alert events
};

// Schema registry entry example
const callEndedSchema = {
  eventType: 'call.ended',
  version: '1.0.0',
  fields: [
    { name: 'callSid', type: 'string', required: true },
    { name: 'timestamp', type: 'int64', required: true },
    { name: 'tenantId', type: 'string', required: true },
    { name: 'duration', type: 'int32', required: true },
    { name: 'status', type: 'string', required: true, enum: ['completed', 'failed', 'busy', 'no_answer', 'canceled'] },
    { name: 'campaignId', type: 'string', required: false },
    { name: 'agentId', type: 'string', required: false },
    { name: 'customerPhone', type: 'string', required: false },
    { name: 'metadata', type: 'map<string,string>', required: false },
  ],
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache Kafka (Apache 2.0) | Server | Event bus |
| Apache Flink (Apache 2.0) | Server | Stream processing |
| ClickHouse (Apache 2.0) | Server | Columnar analytics store |
| Redpanda (BSL) | Server | Kafka-compatible event streaming |

## Production Considerations

**Scaling:** Kafka partitioning strategy must align with query patterns. Partition by tenant ID for tenant-level aggregation isolation and by call SID for call-level event ordering. Set log retention to 7 days on raw topics (events are archived to S3 in Parquet format). Stream processor parallelism should match Kafka partition count. ClickHouse uses distributed tables with sharding across nodes — choose shard key (typically tenant ID) to balance data evenly.

**Security:** Events may contain PII (phone numbers, transcription text). Implement field-level encryption for sensitive fields before publishing to Kafka. Use Kafka ACLs to restrict topic access. The analytics pipeline should mask or hash PII fields in the batch layer before writing to the data lake. Tenants must never access other tenants' data — enforce row-level security in ClickHouse using tenant ID as the shard key and query filter.

**Monitoring:** Track events ingested per second, processing lag (event timestamp to stream processor output), ClickHouse query performance (p50/p95/p99), data lake storage growth, and batch job success/failure rates. Alert on pipeline lag exceeding 30 seconds, event schema validation failures exceeding 1% of events, and batch job failures. Monitor Kafka consumer group lag and partition imbalance.
