# Chapter 02: Database Scaling & Sharding

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Connection Pooling (PgBouncer)](sec-01-connection-pooling-pgbouncer.md) | PgBouncer configuration, pool modes, connection limits, transaction pooling vs session pooling |
| 02 | [Read Replicas](sec-02-read-replicas.md) | Read replica setup, replication lag, query routing, failover handling |
| 03 | [Table Partitioning](sec-03-table-partitioning.md) | Range/list/hash partitioning, partition pruning, partition management, indexing |
| 04 | [Database Sharding](sec-04-database-sharding.md) | Application-level sharding, proxy-based sharding (Vitess/Citus), shard rebalancing |
| 05 | [NoSQL for Analytics](sec-05-nosql-for-analytics.md) | Time-series data (TimescaleDB), analytics (ClickHouse), caching (Redis), document store (MongoDB) |
| 06 | [Query Routing & Middleware](sec-06-query-routing-middleware.md) | Read/write splitting, query routing middleware, connection pooling, failover |
| 07 | [Backup at Scale](sec-07-backup-at-scale.md) | Parallel backup, incremental backup, WAL archiving, backup consistency across shards |
| 08 | [Database Monitoring at Scale](sec-08-database-monitoring-scale.md) | Slow query monitoring, connection monitoring, replication monitoring, storage monitoring |
