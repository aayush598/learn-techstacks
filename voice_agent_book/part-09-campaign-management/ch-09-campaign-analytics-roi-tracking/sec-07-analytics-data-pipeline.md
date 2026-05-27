# Section 07: Analytics Data Pipeline

## Overview

The analytics data pipeline is the backbone of all campaign reporting and ROI calculations, responsible for collecting raw events from the voice platform, transforming them into analytics-ready datasets, and serving them to dashboards and APIs. The pipeline must handle high-throughput event ingestion (thousands of events per second during peak dialing), provide sub-second latency for real-time dashboards, support complex analytical queries over billions of events for historical analysis, and maintain data quality and consistency across all downstream consumers.

The pipeline architecture follows a Lambda architecture pattern with both real-time (speed layer) and batch (batch layer) processing paths. The speed layer uses Redis streams for real-time aggregation and WebSocket delivery to dashboards. The batch layer uses ClickHouse for columnar storage and analytical querying, with materialized views pre-computing common aggregation patterns. A change data capture (CDC) mechanism ensures the batch layer catches up with the speed layer during normal operations and provides data recovery in case of speed layer failures.

## Architecture

```
                   Analytics Data Pipeline Architecture

   Event Sources (Call Events, Agent Events, Conversion Events, System Events)
        |
        v
   +----------------------+
   | Event Ingestion      |  Kafka / Redpanda
   | (Unified event bus)  |  Partitioned by tenant_id + event_type
   +----------------------+
        |                     |
        v                     v
   +------------------+  +------------------+
   | Speed Layer      |  | Batch Layer      |
   | (Redis Streams)  |  | (ClickHouse)     |
   | • Real-time      |  | • Columnar       |
   |   counters       |  | • Materialized   |
   | • Sliding window |  |   views          |
   |   aggregations   |  | • TTL-based      |
   | • Alert checks   |  |   retention      |
   +------------------+  +------------------+
        |                     |
        +---------+-----------+
                  |
                  v
   +----------------------+
   | Materialized Views   |  ClickHouse AggregatingMergeTree
   | (Pre-computed)       |  Hourly, daily, weekly granularity
   |                      |  Common query patterns pre-aggregated
   +----------------------+
                  |
                  v
   +----------------------+
   | Serving Layer        |  REST API / GraphQL / WebSocket
   | (API Gateway)        |  Query routing, caching, auth
   +----------------------+
                  |
                  v
         Dashboards and Reports
```

## Design Decisions

- **Lambda architecture over pure streaming (Kappa) architecture:** The batch layer provides data completeness guarantees that streaming systems struggle to achieve — exactly-once processing, late-arriving event handling, and full data recovery after system failures. The speed layer provides the low-latency view for dashboards. Trade-off: maintaining two processing paths doubles operational complexity and requires careful reconciliation between speed and batch layers.

- **ClickHouse as the single analytics database over multiple specialized stores:** ClickHouse handles both high-ingestion-throughput event storage and sub-second analytical queries over billions of rows. Its materialized views pre-compute common aggregates without maintaining a separate ETL pipeline. Its columnar storage compresses event data 5-10x, reducing storage costs. Trade-off: ClickHouse has limited join performance compared to PostgreSQL, requiring denormalized event tables for analytics workloads.

- **Schema-on-read with schema registry for event evolution:** Events are ingested as semi-structured data (JSON) with schema validation against a central schema registry. The schema registry enforces backward compatibility — old queries must work with new events. This enables adding new event fields without breaking existing dashboards. Trade-off: schema-on-read requires more runtime validation than schema-on-write and can mask data quality issues.

## Implementation Approach

```
interface AnalyticsEvent {
  tenantId: string;
  eventType: string;
  eventId: string;
  timestamp: number;
  source: string;
  payload: Record<string, any>;
  metadata: {
    schemaVersion: number;
    environment: string;
    correlationId: string;
  };
}

class AnalyticsPipeline {
  constructor(kafka, clickhouse, redis) {
    this.eventBus = kafka;
    this.warehouse = clickhouse;
    this.realtime = redis;
    this.schemaRegistry = new SchemaRegistry();
  }

  async ingestEvent(event: AnalyticsEvent) {
    // Validate against schema registry
    await this.schemaRegistry.validate(event.eventType, event);

    // Write to Kafka for durability
    await this.eventBus.produce('analytics_events', event);

    // Update real-time counters
    await this.updateRealtimeCounters(event);

    // Async: batch consumer will write to ClickHouse
  }

  async updateRealtimeCounters(event: AnalyticsEvent) {
    const windowKey = this.getSlidingWindowKey(event.timestamp, 60);
    await this.realtime
      .pipeline()
      .hIncrBy(`realtime:${event.tenantId}:${windowKey}`, event.eventType, 1)
      .hIncrBy(`realtime:${event.tenantId}:${windowKey}:${event.payload.campaignId}`, event.eventType, 1)
      .expire(`realtime:${event.tenantId}:${windowKey}`, 120)
      .exec();
  }

  async queryAnalytics(sql: string, params: Record<string, any>) {
    // Route to appropriate layer based on query time requirement
    if (this.requiresRealTime(sql)) {
      return this.queryRealtime(sql, params);
    }
    return this.warehouse.query(sql, params);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **ClickHouse** (Apache 2.0) | Analytics | Columnar analytics database |
| **Apache Kafka** (Apache 2.0) | Streaming | Event ingestion and processing |
| **Redis** (BSD) | Cache | Real-time counters and caching |
| **dbt** (Apache 2.0) | Transformation | Analytics transformations |
| **Schema Registry** (Confluent) | Governance | Event schema management |
| **Grafana** (AGPLv3) | Monitoring | Pipeline monitoring dashboards |

## Production Considerations

**Scaling:** Kafka partitioning strategy must match query patterns — partition by tenant_id for natural isolation and by event_type for balanced consumer load. ClickHouse uses `Distributed` tables across shards for horizontal scaling. Materialized views are created with `AggregatingMergeTree` engine for incremental aggregation. Monitor Kafka consumer lag as the primary pipeline health metric.

**Security:** The pipeline handles potentially sensitive call metadata. Encrypt events at rest in ClickHouse using encryption-at-rest. Mask or exclude PII fields from analytics events. Implement column-level access control in ClickHouse for sensitive metrics (cost data, agent performance). Use Kafka ACLs to restrict topic access.

**Monitoring:** Track events per second (peak and sustained), Kafka consumer lag (alert if > 10 minutes), ClickHouse insertion throughput (rows/sec), query latency by pattern (p50, p95, p99), materialized view freshness, and storage utilization by retention tier. Build a pipeline health dashboard with SLO indicators: ingestion latency < 5 seconds p99, query latency < 500ms p95, data completeness > 99.9%.
