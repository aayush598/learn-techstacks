# Section 04: Local Service Configuration

## Overview

Each Docker Compose service requires specific configuration for our voice agent platform's needs — PostgreSQL with pgvector for embeddings, Redis with modules for caching and pub/sub, Kafka with KRaft for event streaming, and MinIO for S3-compatible storage. This section covers the detailed configuration of each service.

## PostgreSQL Configuration

```sql
-- docker/init/postgres/01-extensions.sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- docker/init/postgres/02-config.sql
-- Performance tuning for development
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '768MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET work_mem = '8MB';
ALTER SYSTEM SET min_wal_size = '1GB';
ALTER SYSTEM SET max_wal_size = '4GB';
```

### pgvector Usage

```sql
-- docker/init/postgres/03-vector-setup.sql
-- Create vector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table for knowledge base embeddings
CREATE TABLE IF NOT EXISTS knowledge_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL,
  agent_id UUID,
  content TEXT NOT NULL,
  embedding vector(1536),  -- OpenAI ada-002 dimension
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create IVFFlat index for approximate nearest neighbor search
CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_vector
  ON knowledge_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Create index for organization lookups
CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_org
  ON knowledge_embeddings (organization_id);
```

## Redis Configuration

```conf
# docker/redis/redis.conf
# Redis configuration for development

# Memory management
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Security
requirepass ""  # No password in development

# Performance tuning
tcp-keepalive 300
timeout 0
lfu-log-factor 10
lfu-decay-time 1

# Modules (Redis Stack)
loadmodule /opt/redis-stack/lib/redisearch.so
loadmodule /opt/redis-stack/lib/redisjson.so
loadmodule /opt/redis-stack/lib/redistimeseries.so
```

### Redis Data Structures

```typescript
// packages/voice/src/cache/redis-schema.ts
// Redis key naming conventions
export const REDIS_KEYS = {
  // Session data
  session: (callId: string) => `session:${callId}`,

  // Rate limiting
  rateLimit: (orgId: string, endpoint: string) =>
    `ratelimit:${orgId}:${endpoint}`,

  // Voice agent state
  agentState: (callId: string) => `agent:state:${callId}`,
  conversationHistory: (callId: string) => `agent:conversation:${callId}`,

  // Cache
  agentConfig: (agentId: string) => `cache:agent:${agentId}`,
  llmResponse: (hash: string) => `cache:llm:${hash}`,

  // Pub/Sub channels
  callEvents: "pubsub:call-events",
  agentCommands: "pubsub:agent-commands",

  // Rate limiting
  callRateLimit: (orgId: string) => `ratelimit:calls:${orgId}`,

  // Locks
  callLock: (callId: string) => `lock:call:${callId}`,
} as const;
```

## Kafka Configuration (KRaft Mode)

```properties
# docker/kafka/server.properties
# Kafka broker configuration (KRaft mode)

# Required for KRaft mode
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093

# Listeners
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
advertised.listeners=PLAINTEXT://localhost:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER

# Topic configuration
num.partitions=3
default.replication.factor=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

# Log configuration
log.dirs=/var/lib/kafka/data
log.retention.hours=168
log.retention.bytes=1073741824
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Performance tuning
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Group coordinator
group.initial.rebalance.delay.ms=0
```

### Topic Naming Convention

```yaml
# docker/kafka/topics.yml
topics:
  - name: call-events
    partitions: 3
    replication-factor: 1
    config:
      cleanup.policy: delete
      retention.ms: 604800000  # 7 days

  - name: transcription-results
    partitions: 2
    replication-factor: 1
    config:
      cleanup.policy: delete
      retention.ms: 2592000000  # 30 days

  - name: agent-events
    partitions: 1
    replication-factor: 1
    config:
      cleanup.policy: compact  # Keep latest value per key

  - name: analytics-events
    partitions: 3
    replication-factor: 1
    config:
      cleanup.policy: delete
      retention.ms: 86400000  # 1 day
```

## MinIO Configuration

```yaml
# docker/minio/buckets.json
{
  "buckets": [
    {
      "name": "dev-recordings",
      "policy": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::dev-recordings/*"
          }
        ]
      },
      "lifecycle": {
        "rules": [
          {
            "id": "expire-old-recordings",
            "status": "Enabled",
            "expiration": {
              "days": 90
            }
          }
        ]
      }
    },
    {
      "name": "dev-transcripts",
      "policy": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::dev-transcripts/*"
          }
        ]
      }
    },
    {
      "name": "dev-exports",
      "policy": null  # Private bucket
    }
  ]
}
```

### Access Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::dev-recordings",
        "arn:aws:s3:::dev-recordings/*",
        "arn:aws:s3:::dev-transcripts",
        "arn:aws:s3:::dev-transcripts/*"
      ]
    }
  ]
}
```

## Service Health Check Configuration

```yaml
# docker/docker-compose.yml (health check definitions)
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  kafka:
    healthcheck:
      test: ["CMD", "kafka-topics", "--bootstrap-server", "localhost:9092", "--list"]
      interval: 15s
      timeout: 10s
      retries: 10
      start_period: 30s

  minio:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Design Decisions

### pgvector dimension choice (1536)

OpenAI's `text-embedding-ada-002` produces 1536-dimensional vectors. While other models use different dimensions (768 for `text-embedding-3-small`, 3072 for `text-embedding-3-large`), 1536 provides a good balance of accuracy and performance for our knowledge base RAG pipeline.

### IVFFlat vs. HNSW index

IVFFlat is faster to build and uses less memory, making it suitable for development. HNSW provides better recall but requires more memory and build time. For production with millions of embeddings, use HNSW.

### Kafka retention policies

- Call events: 7 days (transient)
- Transcription results: 30 days (needed for analytics)
- Agent events: Compacted (keep latest state per agent)
- Analytics: 1 day (aggregated into database)

## Integration Points

- **Prisma**: Connects to PostgreSQL via `DATABASE_URL`
- **ioredis**: Connects to Redis via `REDIS_URL`
- **kafkajs**: Connects to Kafka via `KAFKA_BROKERS`
- **@aws-sdk/client-s3**: Connects to MinIO via `MINIO_ENDPOINT`

## Production Considerations

1. **Resource allocation**: PostgreSQL with pgvector requires significant memory for vector indexes. In production, allocate at least 2GB shared_buffers
2. **Persistence**: Docker volumes provide persistence. For production, use managed services (RDS, ElastiCache, MSK, S3) instead of containerized storage
3. **Kafka replication**: Development uses replication factor 1. Production requires at least 3 brokers with replication factor 3
4. **MinIO TLS**: In production, MinIO must be configured with TLS certificates. The development setup uses plain HTTP
5. **Backup**: Containerized databases in development should be backed up to local storage or S3. Script the backup process
