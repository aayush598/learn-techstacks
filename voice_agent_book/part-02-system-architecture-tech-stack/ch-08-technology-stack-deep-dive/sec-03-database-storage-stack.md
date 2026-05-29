# Section 03: Database & Storage Stack

## Technology Overview

The data layer uses **PostgreSQL 16** as the primary relational database with **pgvector** for embeddings, **Redis 7** for caching and real-time data, **MinIO** for S3-compatible object storage, **ClickHouse** for analytics, and **Apache Kafka** for event streaming.

```
┌─────────────────────────────────────────────────────────────────────┐
│                  DATABASE & STORAGE STACK                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL 16 (Primary Database)                           │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Relational   │ │  pgvector    │ │   Row-Level      │    │   │
│  │  │  Data (Users, │ │  (Embeddings)│ │   Security (RLS) │    │   │
│  │  │  Agents,      │ │             │ │   per tenant     │    │   │
│  │  │  Calls, etc)  │ │             │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Native JSONB │ │  Full-Text   │ │   Logical        │    │   │
│  │  │  (Flexible    │ │  Search      │ │   Replication    │    │   │
│  │  │   Schemas)    │ │  (tsvector)  │ │   (pglogical)    │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Redis 7 (Cache & Real-Time)                                │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Session     │ │  Rate Limit  │ │   WebSocket      │    │   │
│  │  │  Cache       │ │  Counters    │ │   Pub/Sub        │    │   │
│  │  │  (TTL-based) │ │  (Token      │ │   (Multi-cast)   │    │   │
│  │  │              │ │   Bucket)    │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  BullMQ      │ │  Geo-        │ │   Leaderboard    │    │   │
│  │  │  Queue       │ │  Spatial     │ │   (Sorted Sets)  │    │   │
│  │  │  Backend     │ │  (Geo Sets)  │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MinIO (Object Storage)    │  ClickHouse (Analytics)       │   │
│  │  ┌──────────────────┐      │  ┌──────────────────────┐    │   │
│  │  │  Call Recordings  │      │  │  Call Metrics       │    │   │
│  │  │  Transcriptions   │      │  │  Usage Data         │    │   │
│  │  │  Exports          │      │  │  Billing Records    │    │   │
│  │  │  Tenant Assets    │      │  │  Time-Series Events │    │   │
│  │  └──────────────────┘      │  └──────────────────────┘    │   │
│  │  (S3-compatible API)       │  (Column-oriented OLAP)     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Apache Kafka (Event Streaming)                             │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Agent Events │ │  Call Events │ │   Billing        │    │   │
│  │  │  (created,    │ │  (initiated, │ │   Events         │    │   │
│  │  │  updated)     │ │  completed)  │ │   (usage meter)  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## PostgreSQL Configuration

```sql
-- PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS vector;       -- pgvector for embeddings
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;  -- Query monitoring
CREATE EXTENSION IF NOT EXISTS pgcrypto;     -- UUID generation
CREATE EXTENSION IF NOT EXISTS pg_trgm;      -- Fuzzy text search

-- Connection pool configuration
-- max_connections = 200 (via PgBouncer)
-- shared_buffers = 4GB
-- effective_cache_size = 12GB
-- work_mem = 64MB
-- maintenance_work_mem = 1GB

-- Row-Level Security example
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  name VARCHAR(100) NOT NULL,
  config JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON agents
  USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

## Redis Data Structures

```typescript
// Redis key conventions
const REDIS_KEYS = {
  session: (token: string) => `session:${token}`,
  rateLimit: (key: string) => `rate_limit:${key}`,
  cache: (key: string) => `cache:${key}`,
  pubsub: (channel: string) => `pubsub:${channel}`,
  queue: (name: string) => `bull:${name}`,
  geo: (key: string) => `geo:${key}`,
  leaderboard: (period: string) => `leaderboard:${period}`,
};

// Session cache TTL
const SESSION_TTL = 60 * 60 * 24; // 24 hours
const RATE_LIMIT_TTL = 60;        // 1 minute
const QUERY_CACHE_TTL = 30;       // 30 seconds
```

## MinIO Buckets

```typescript
const MINIO_BUCKETS = {
  callRecordings: {
    name: 'call-recordings',
    policy: 'private',
    versioning: true,
    lifecycle: { expiration: 365 }, // 1 year retention
  },
  transcriptions: {
    name: 'transcriptions',
    policy: 'private',
    versioning: true,
  },
  exports: {
    name: 'exports',
    policy: 'private',
    lifecycle: { expiration: 7 }, // Auto-clean after 7 days
  },
  tenantAssets: {
    name: 'tenant-assets',
    policy: 'public-read-only', // Logos, favicons, etc.
  },
};
```

## ClickHouse Tables

```sql
-- Call metrics table
CREATE TABLE call_metrics (
  tenant_id UUID,
  call_id UUID,
  agent_id UUID,
  status LowCardinality(String),
  duration_seconds UInt32,
  cost_micro_usd UInt64,
  stt_latency_ms UInt16,
  llm_latency_ms UInt16,
  tts_latency_ms UInt16,
  timestamp DateTime DEFAULT now(),
  date Date DEFAULT toDate(timestamp)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (tenant_id, date);

-- Aggregating materialized view
CREATE MATERIALIZED VIEW call_metrics_daily
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (tenant_id, date, agent_id)
AS SELECT
  tenant_id,
  date,
  agent_id,
  count() AS total_calls,
  sum(duration_seconds) AS total_duration,
  sum(cost_micro_usd) AS total_cost
FROM call_metrics
GROUP BY tenant_id, date, agent_id;
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary database | PostgreSQL 16 | Reliability, pgvector, JSONB, mature ecosystem |
| Vector extension | pgvector | No separate vector DB needed, transactional consistency |
| Object storage | MinIO (S3-compatible) | Self-hosted, no vendor lock-in, S3 API |
| Analytics DB | ClickHouse | Column-oriented, 100x faster for time-series aggregates |
| Event streaming | Apache Kafka | Durable, replayable, exactly-once semantics |
| Cache layer | Redis 7 | Multi-purpose (cache, queue, pub/sub, rate limit) |

## Integration Points

- **Ch 03 (Database)** — Detailed schema design and indexing strategy
- **Ch 05 (Microservices)** — Database-per-service pattern with shared Kafka
- **Ch 09 (Data Flow)** — CQRS with ClickHouse for read models and PostgreSQL for writes

## Production Considerations

- **PostgreSQL**: Streaming replication with 2 standby replicas; PgBouncer for connection pooling
- **Redis**: Redis Cluster with 3 masters + replicas; RDB + AOF persistence for queues
- **MinIO**: Distributed mode with erasure coding (EC:4), behind CDN for public assets
- **ClickHouse**: Single large node for MVP, sharded cluster for scale (1TB+)
- **Kafka**: 3-broker cluster with replication factor 3; topics auto-created with 6 partitions
- **Backup**: PostgreSQL WAL streaming to S3 (15-minute RPO); daily full backups (1-hour RTO)
