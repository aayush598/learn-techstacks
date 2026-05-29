# Section 06: Data & Storage Layer

## Multi-Engine Storage Architecture

The platform uses a **polyglot persistence** approach — different data stores optimized for different access patterns. Rather than forcing all data into a single database, we select the best storage engine for each workload.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA & STORAGE LAYER                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                     APPLICATION DATA                             │     │
│  │                                                                  │     │
│  │  ┌─────────────────────┐  ┌─────────────────────┐               │     │
│  │  │      PostgreSQL     │  │        Redis        │               │     │
│  │  │  ┌─────────────────┐│  │  ┌─────────────────┐│               │     │
│  │  │  │  Tenants        ││  │  │  Sessions       ││               │     │
│  │  │  │  Users/RBAC     ││  │  │  Cache          ││               │     │
│  │  │  │  Agents         ││  │  │  Rate Limiting  ││               │     │
│  │  │  │  Calls          ││  │  │  Pub/Sub        ││               │     │
│  │  │  │  Conversations  ││  │  │  Job Queue      ││               │     │
│  │  │  │  Recordings     ││  │  │  (BullMQ)       ││               │     │
│  │  │  │  Campaigns      ││  │  │  API Keys Cache ││               │     │
│  │  │  │  Billing        ││  │  └─────────────────┘│               │     │
│  │  │  │  Embeddings     ││  │                     │               │     │
│  │  │  │  (pgvector)     ││  │                     │               │     │
│  │  │  └─────────────────┘│  │                     │               │     │
│  │  └─────────────────────┘  └─────────────────────┘               │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                     MEDIA & FILES                              │     │
│  │                                                                  │     │
│  │  ┌─────────────────────┐  ┌─────────────────────┐               │     │
│  │  │    MinIO (S3 API)   │  │      CDN (Edge)     │               │     │
│  │  │  ┌─────────────────┐│  │  ┌─────────────────┐│               │     │
│  │  │  │ Call Recordings  ││  │  │ Static Assets   ││               │     │
│  │  │  │ Transcripts      ││  │  │ Recorded Audio  ││               │     │
│  │  │  │ Exported Reports ││  │  │ SDK Files       ││               │     │
│  │  │  │ Agent Audio      ││  │  └─────────────────┘│               │     │
│  │  │  │ Knowledge Base   ││  │                     │               │     │
│  │  │  └─────────────────┘│  │                     │               │     │
│  │  └─────────────────────┘  └─────────────────────┘               │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                      ANALYTICS & EVENTS                         │     │
│  │                                                                  │     │
│  │  ┌─────────────────────┐  ┌─────────────────────┐               │     │
│  │  │     ClickHouse      │  │    Apache Kafka     │               │     │
│  │  │  ┌─────────────────┐│  │  ┌─────────────────┐│               │     │
│  │  │  │ Usage Metrics   ││  │  │ Call Events     ││               │     │
│  │  │  │ Call Analytics  ││  │  │ Billing Events  ││               │     │
│  │  │  │ Performance     ││  │  │ Audit Events    ││               │     │
│  │  │  │ Aggregations    ││  │  │ System Events   ││               │     │
│  │  │  │ Time-series     ││  │  └─────────────────┘│               │     │
│  │  │  └─────────────────┘│  │                     │               │     │
│  │  └─────────────────────┘  └─────────────────────┘               │     │
│  └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## PostgreSQL (Primary Database)

PostgreSQL 16 serves as the primary operational database, extended with:
- **pgvector** for embedding storage and similarity search
- **pg_partman** for automatic table partitioning
- **pg_cron** for scheduled maintenance tasks
- **Row-Level Security (RLS)** for multi-tenant isolation

```typescript
// Prisma schema — core tenant isolation pattern
model Tenant {
  id        String   @id @default(uuid())
  slug      String   @unique
  name      String
  config    Json     @default("{}")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  users     User[]
  agents    Agent[]
  calls     Call[]
  campaigns Campaign[]

  @@map("tenants")
}

// RLS policy via Prisma middleware
// Every query automatically filters by tenant_id
// This is enforced at the database level, not just the application level
```

**Data Distribution by Service:**

| Service | Tables | PostgreSQL | Redis |
|---------|--------|-----------|-------|
| Agent Service | agents, agent_versions, prompts, voices, knowledge_bases | ✓ | Config cache |
| Call Service | calls, conversations, transcript_chunks, events | ✓ | Active calls |
| Voice Service | — (stateless) | — | Stream state |
| AI Service | embeddings, memory, rag_logs | ✓ (pgvector) | Model cache |
| Campaign Service | campaigns, contacts, contact_lists, call_attempts, dnc_numbers | ✓ | Queue state |
| Billing Service | subscriptions, usage_records, invoices, payments, plans | ✓ | Rate limit counters |
| Notification Service | notifications, webhook_endpoints, webhook_deliveries | ✓ | Pending queue |

## Redis (Cache & Real-Time)

Redis 7 handles four distinct workloads:

```typescript
interface RedisNamespaces {
  // 1. Cache — TTL-based, evictable
  cache: {
    'cache:agent:{id}': AgentConfig       // TTL: 5min
    'cache:tenant:{id}:config': TenantConfig // TTL: 1min
    'cache:api-key:{hash}': ApiKey         // TTL: 10min
    'cache:did:{number}': DIDConfig        // TTL: 10min
  }

  // 2. Session & State — Ephemeral, key-based
  session: {
    'session:user:{id}': UserSession       // TTL: 24h
    'session:call:{id}': CallState         // TTL: call duration + 1h
    'session:stream:{id}': StreamState     // TTL: stream duration
  }

  // 3. Pub/Sub — Real-time messaging
  pubsub: {
    'ps:call:{id}:events'       // Call event channel
    'ps:agent:{id}:state'       // Agent state changes
    'ps:tenant:{id}:broadcast'  // Tenant-wide broadcasts
    'ps:ws:rooms:{room}'        // WebSocket room events
  }

  // 4. Rate Limiting & Counters
  counter: {
    'ratelimit:{key}:{window}'      // Sliding window counter
    'usage:{tenant}:{metric}:{day}' // Daily usage counter
    'concurrent:{service}'          // Active connection count
  }

  // 5. Job Queue (BullMQ)
  queue: {
    'bull:call-processing:{id}'
    'bull:transcription:{id}'
    'bull:analytics-export:{id}'
    'bull:webhook-delivery:{id}'
  }
}
```

## MinIO (Object Storage)

MinIO provides S3-compatible object storage for media files:

```typescript
interface StorageLayout {
  buckets: {
    'call-recordings': {
      prefix: '{tenant_id}/{date}/{call_id}/'
      files: {
        'audio/recording.{format}'       // Raw call audio
        'audio/mono-agent.{format}'      // Agent-only track
        'audio/mono-caller.{format}'     // Caller-only track
        'transcript/transcript.json'     // Full transcript
        'transcript/utterances.json'     // Per-utterance data
        'analysis/sentiment.json'        // Sentiment analysis
        'analysis/summary.json'          // Call summary
      }
    }
    'knowledge-base': {
      prefix: '{tenant_id}/{kb_id}/'
      files: {
        'documents/{doc_id}.{format}'    // Uploaded documents
        'chunks/{chunk_id}.json'         // Processed chunks
        'embeddings/{chunk_id}.npy'      // Stored as pgvector
      }
    }
    'exports': {
      prefix: '{tenant_id}/{export_id}/'
      files: {
        'report.{format}'                // Exported reports
        'analytics-{date}.csv'           // Data exports
      }
    }
    'static-assets': {
      prefix: 'global/'
      files: {
        'audio/hold-music.{format}'      // Default hold music
        'ivr-prompts/{language}/'         // IVR audio prompts
        'branding/{tenant_id}/'           // Custom branding
      }
    }
  }
}
```

## ClickHouse (Analytics)

ClickHouse handles analytics queries that would be too expensive on PostgreSQL:

```typescript
// Example ClickHouse table for call analytics
// CREATE TABLE call_analytics (
//   tenant_id String,
//   call_id String,
//   agent_id String,
//   campaign_id Nullable(String),
//   caller_number String,
//   start_time DateTime,
//   end_time Nullable(DateTime),
//   duration_seconds UInt32,
//   status Enum('completed', 'failed', 'no_answer', 'busy', 'transferred'),
//   stt_latency_ms UInt16,
//   ai_latency_ms UInt16,
//   tts_latency_ms UInt16,
//   total_cost_micro_us UInt64,
//   sentiment_score Float32,
//   transcript_word_count UInt32,
//   turn_count UInt16
// ) ENGINE = MergeTree()
// PARTITION BY toYYYYMM(start_time)
// ORDER BY (tenant_id, start_time)
```

## Data Flow Between Stores

```
Write Path:
  API Call → PostgreSQL (transactional) → Kafka (event) → ClickHouse (analytics)

Cache Invalidation:
  API Call → PostgreSQL → Event → Redis Cache Invalidation → Next Read refills cache

File Upload:
  Client → MinIO (presigned URL) → Database (metadata reference)

Event Pipeline:
  Service → Kafka → Stream Processor → ClickHouse + Redis + WebSocket
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary DB | PostgreSQL 16 | Mature, extensible, pgvector support |
| Object Storage | MinIO (not S3) | Self-hosted, S3-compatible, cost-effective |
| Analytics | ClickHouse (separate) | Avoids analytics load on operational DB |
| Cache | Redis (multi-purpose) | Single technology for cache, pub/sub, queues |
| Event Bus | Kafka (not RabbitMQ) | Durability, replay, partitioning for scale |

## Integration Points

- **Part 03 (Database Architecture)** — Deep dive into schema design
- **Part 11 (Analytics)** — ClickHouse powers all reporting
- **Part 12 (Recording)** — MinIO stores call recordings
- **Part 17 (Billing)** — Usage records flow through ClickHouse

## Production Considerations

- **Backup Strategy**: PostgreSQL WAL streaming + daily snapshots, Redis RDB + AOF, MinIO erasure coding
- **Disaster Recovery**: Cross-region replication for PostgreSQL, Kafka mirroring
- **Scaling**: Read replicas for PostgreSQL, cluster mode for Redis, ClickHouse sharding
- **Data Retention**: Hot data in PostgreSQL (30 days), warm in ClickHouse (12 months), cold in MinIO (7 years)
- **Cost Monitoring**: Track storage costs per tenant, set per-tenant limits
