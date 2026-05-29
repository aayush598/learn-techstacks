# Section 07: Indexing Strategy

## Index Architecture

A well-designed indexing strategy is critical for query performance at scale. PostgreSQL offers multiple index types — B-tree, GiST, GIN, HNSW (via pgvector) — each suited to different query patterns in the AI Voice Agent platform.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATABASE INDEX STRATEGY MAP                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    INDEX TYPES BY USE CASE                      │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  B-TREE (Default)                                        │   │    │
│  │  │  • Primary keys, unique constraints                      │   │    │
│  │  │  • Equality lookups (WHERE id = '...')                   │   │    │
│  │  │  • Range queries (WHERE created_at > '2025-01-01')      │   │    │
│  │  │  • Sorting (ORDER BY created_at DESC)                     │   │    │
│  │  │  • Composite: (tenant_id, created_at)                    │   │    │
│  │  │  • Foreign key columns (agent_id, campaign_id)           │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  GiST (Generalized Search Tree)                           │   │    │
│  │  │  • Full-text search (tsvector)                            │   │    │
│  │  │  • Range exclusion constraints                            │   │    │
│  │  │  • Geometry/spatial data                                  │   │    │
│  │  │  • Example: transcript full-text search                   │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  GIN (Generalized Inverted Index)                         │   │    │
│  │  │  • JSONB path queries (config->>'key')                    │   │    │
│  │  │  • Array containment (WHERE tags @> ['premium'])          │   │    │
│  │  │  • Full-text search (alternative to GiST)                 │   │    │
│  │  │  • Example: metadata field search                         │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  HNSW (Hierarchical Navigable Small World) via pgvector   │   │    │
│  │  │  • Vector similarity search (embedding)                    │   │    │
│  │  │  • Cosine similarity, L2 distance, inner product          │   │    │
│  │  │  • Example: RAG knowledge base retrieval                  │   │    │
│  │  │  • Example: semantic search across transcripts            │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              COMPOSITE INDEX DESIGN PATTERNS                    │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Pattern 1: Tenant + Time                                  │   │    │
│  │  │  ┌────────────────────────────────────────────────────┐   │   │    │
│  │  │  │ CREATE INDEX idx_calls_tenant_time                   │   │    │    │
│  │  │  │ ON calls (tenant_id, created_at DESC);               │   │   │    │
│  │  │  │                                                        │   │   │    │
│  │  │  │  -- Queries that benefit:                              │   │   │    │
│  │  │  │  SELECT * FROM calls                                   │   │   │    │
│  │  │  │  WHERE tenant_id = 'abc'                               │   │   │    │
│  │  │  │  ORDER BY created_at DESC                              │   │   │    │
│  │  │  │  LIMIT 20;                                             │   │   │    │
│  │  │  └────────────────────────────────────────────────────┘   │   │    │
│  │  │                                                              │   │    │
│  │  │  Pattern 2: Tenant + Status + Time                          │   │    │
│  │  │  ┌────────────────────────────────────────────────────┐   │   │    │
│  │  │  │ CREATE INDEX idx_calls_tenant_status_time            │   │   │    │
│  │  │  │ ON calls (tenant_id, status, created_at DESC);      │   │   │    │
│  │  │  │                                                        │   │   │    │
│  │  │  │  -- Active calls monitoring                           │   │   │    │
│  │  │  │  SELECT * FROM calls                                   │   │   │    │
│  │  │  │  WHERE tenant_id = 'abc'                               │   │   │    │
│  │  │  │  AND status IN ('in_progress', 'ringing')              │   │   │    │
│  │  │  │  ORDER BY created_at;                                  │   │   │    │
│  │  │  └────────────────────────────────────────────────────┘   │   │    │
│  │  │                                                              │   │    │
│  │  │  Pattern 3: Lookup + Sorting                                │   │    │
│  │  │  ┌────────────────────────────────────────────────────┐   │   │    │
│  │  │  │ CREATE INDEX idx_calls_agent_time                    │   │   │    │
│  │  │  │ ON calls (agent_id, created_at DESC);               │   │   │    │
│  │  │  │                                                        │   │   │    │
│  │  │  │  SELECT * FROM calls                                   │   │   │    │
│  │  │  │  WHERE agent_id = 'xyz'                                │   │   │    │
│  │  │  │  ORDER BY created_at DESC;                             │   │   │    │
│  │  │  └────────────────────────────────────────────────────┘   │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Index Definitions

```prisma
// prisma/schema.prisma — Index declarations

model Call {
  // ... fields ...

  // Core tenant-time index (most common query pattern)
  @@index([tenantId, createdAt(sort: Desc)])

  // Status filtering for active calls
  @@index([tenantId, status, createdAt(sort: Desc)])

  // Agent-specific queries
  @@index([agentId, createdAt(sort: Desc)])

  // Caller number lookup (compliance, callback)
  @@index([callerNumber])

  // Campaign analytics
  @@index([campaignId])

  // Full-text search on transcript (via PostgreSQL tsvector)
  // Handled via raw SQL migration (see below)
}

model ConversationEvent {
  // ... fields ...

  // Primary access pattern: all events for a call
  @@index([callId, timestamp(sort: Asc)])

  // Sentiment analysis queries
  @@index([callId, type])
}

model Agent {
  // ... fields ...

  // Tenant-wide agent listing
  @@index([tenantId, status])

  @@index([tenantId, createdAt(sort: Desc)])
}

model Campaign {
  // ... fields ...

  @@index([tenantId, status])
  @@index([agentId])
}

model Contact {
  // ... fields ...

  @@index([contactListId, status])

  // Phone number lookup for DNC
  @@index([phone])
}

model ContactList {
  // ... fields ...

  @@index([campaignId])
  @@index([tenantId])
}

model CallAttempt {
  // ... fields ...

  @@index([contactId, attemptNumber])
  @@index([campaignId, status])
  @@index([scheduledAt])
}
```

## Raw SQL Index Migrations

Some indexes require raw SQL (full-text search, partial indexes, HNSW):

```sql
-- Full-text search on transcripts
CREATE INDEX idx_transcript_search
  ON conversation_events
  USING GIN (to_tsvector('english', text))
  WHERE type = 'utterance';

-- Partial indexes for common filtered queries
CREATE INDEX idx_calls_active
  ON calls (tenant_id, created_at DESC)
  WHERE status IN ('in_progress', 'ringing', 'connecting');

CREATE INDEX idx_calls_failed
  ON calls (tenant_id, created_at DESC)
  WHERE status = 'failed';

-- HNSW vector index for RAG (via pgvector)
CREATE INDEX idx_kb_chunks_embedding
  ON knowledge_base_chunks
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 200);

-- Hash index on phone number for fast equality lookup
CREATE INDEX idx_contacts_phone_hash
  ON contacts
  USING hash (phone);

-- JSONB GIN index for config queries
CREATE INDEX idx_agents_config
  ON agents
  USING GIN (config jsonb_path_ops);

-- BRIN index for time-series data (cheaper than B-tree for large tables)
CREATE INDEX idx_usage_recorded_at
  ON usage_records
  USING BRIN (recorded_at)
  WITH (pages_per_range = 32);
```

## Composite Index Design

```sql
-- Example: Query that needs a specific composite index
-- Query: Find completed calls for a tenant in the last 7 days
EXPLAIN ANALYZE
SELECT id, caller_number, duration, sentiment_score
FROM calls
WHERE tenant_id = 'abc-123'
  AND status = 'completed'
  AND created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 50;

-- Optimal index:
-- CREATE INDEX idx_calls_tenant_status_time
--   ON calls (tenant_id, status, created_at DESC)
--   WHERE status = 'completed';
--
-- This is a covering index if we INCLUDE the selected columns:
-- CREATE INDEX idx_calls_tenant_status_time_cov
--   ON calls (tenant_id, status, created_at DESC)
--   INCLUDE (caller_number, duration, sentiment_score)
--   WHERE status = 'completed';
```

## Index Maintenance

```sql
-- Rebuild indexes with low concurrency
REINDEX INDEX CONCURRENTLY idx_calls_tenant_time;

-- Analyze table statistics
ANALYZE calls;

-- Check index usage
SELECT
  schemaname || '.' || tablename as table_name,
  indexname,
  indexdef,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;

-- Find unused indexes (scan count near 0)
SELECT
  indexrelid::regclass as index_name,
  relid::regclass as table_name,
  idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan < 10
  AND indexrelid::regclass !~ '^.*_pkey$'
ORDER BY idx_scan ASC;
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary Index | B-tree (default) | Best general-purpose performance |
| Tenant Isolation | Composite prefix on all indexes | Every query starts with tenant_id |
| Full-Text Search | GIN on tsvector | Fast text search on transcripts |
| Vectors | HNSW (pgvector) | Best accuracy-speed tradeoff for RAG |
| Partial Indexes | Common filtered queries | Smaller indexes, faster writes |
| Covering Indexes | INCLUDE clause | Index-only scans for common queries |

## Index Strategy by Table

| Table | Primary Index | Secondary Indexes | Special Index |
|-------|--------------|-------------------|---------------|
| calls | (tenant_id, created_at DESC) | (tenant_id, status, created_at), (agent_id, created_at) | Partial (active), BRIN (time) |
| conversation_events | (call_id, timestamp ASC) | (call_id, type) | GIN tsvector on text |
| agents | (tenant_id, status) | (tenant_id, created_at) | GIN on config JSONB |
| contacts | (contact_list_id, status) | (phone) | Hash on phone |
| usage_records | (tenant_id, metric, recorded_at) | (subscription_id, recorded_at) | BRIN on recorded_at |
| knowledge_base_chunks | (kb_id) | — | HNSW on embedding |

## Integration Points

- **Part 03 (Database Architecture)** — Index design is integral to schema design
- **Part 11 (Analytics)** — Aggregation queries rely on proper indexes
- **Part 24 (Scaling)** — Index strategy affects query performance at scale

## Production Considerations

- **Write Amplification**: Each additional index increases write time by ~10-20%. Keep indexes lean.
- **Index Size**: B-tree indexes ~30% of table size; GIN indexes ~50%; HNSW ~100%+ of vector data.
- **Maintenance Window**: Scheduled REINDEX during low-usage periods (3 AM daily).
- **Monitoring**: Track index scan count, tuple fetch ratio, and index size growth.
- **Query Analysis**: Use `pg_stat_statements` to identify queries missing indexes.
- **Bloat**: Monitor index bloat with `pgstattuple`; rebuild when bloat exceeds 20%.
