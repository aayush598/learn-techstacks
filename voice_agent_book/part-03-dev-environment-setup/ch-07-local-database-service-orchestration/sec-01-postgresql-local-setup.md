# Section 01: PostgreSQL Local Setup

## Overview

PostgreSQL serves as the primary data store for the voice agent platform. With the pgvector extension for embedding similarity search, it supports both transactional data and AI-powered RAG queries. This section covers local configuration, extension setup, database creation, and user/permissions management.

## Container Configuration

```yaml
# docker/docker-compose.yml (PostgreSQL service)
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: voice-agent-postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: voice_agent_dev
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init/postgres:/docker-entrypoint-initdb.d
    command:
      - "postgres"
      - "-c"
      - "shared_preload_libraries=pg_stat_statements"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - voice-agent-dev
```

## PostgreSQL Configuration

```conf
# docker/postgres/postgresql.conf
# PostgreSQL configuration for development

# Connection settings
max_connections = 200
listen_addresses = '*'

# Memory settings
shared_buffers = 256MB
effective_cache_size = 768MB
maintenance_work_mem = 64MB
work_mem = 8MB

# Write-ahead log
wal_level = logical
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB
checkpoint_completion_target = 0.9

# Planner settings
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d.log'
log_statement = 'ddl'
log_min_duration_statement = 1000  # Log queries > 1 second

# Extensions
shared_preload_libraries = 'pg_stat_statements'
track_io_timing = on
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

## Initialization Scripts

```sql
-- docker/init/postgres/00-create-databases.sql
-- Create databases for different environments
SELECT 'CREATE DATABASE voice_agent_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'voice_agent_dev')\gexec

SELECT 'CREATE DATABASE voice_agent_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'voice_agent_test')\gexec

-- docker/init/postgres/01-extensions.sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- docker/init/postgres/02-schemas.sql
-- Create application schemas
CREATE SCHEMA IF NOT EXISTS voice;
CREATE SCHEMA IF NOT EXISTS analytics;

-- docker/init/postgres/03-users.sql
-- Create application users with minimal privileges
DO $$
BEGIN
  -- Application user (read/write on voice and public schemas)
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'voice_app') THEN
    CREATE ROLE voice_app WITH LOGIN PASSWORD 'voice_app_password';
  END IF;

  -- Read-only user (for analytics/reporting)
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'voice_readonly') THEN
    CREATE ROLE voice_readonly WITH LOGIN PASSWORD 'voice_readonly_password';
  END IF;
END
$$;

-- Grant permissions
GRANT CONNECT ON DATABASE voice_agent_dev TO voice_app, voice_readonly;
GRANT USAGE ON SCHEMA public, voice TO voice_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public, voice TO voice_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public, voice TO voice_app;
GRANT SELECT ON ALL TABLES IN SCHEMA public, voice TO voice_readonly;
```

## pgvector Configuration for RAG

```sql
-- docker/init/postgres/04-vector-setup.sql
-- Setup pgvector for embedding storage and search

-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the knowledge base embeddings table
CREATE TABLE IF NOT EXISTS knowledge_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL,
  agent_id UUID,
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for vector search
-- IVFFlat index (faster build, suitable for up to ~1M vectors)
CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_ivfflat
  ON knowledge_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Create indexes for filtering
CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_org
  ON knowledge_embeddings (organization_id);

CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_agent
  ON knowledge_embeddings (agent_id);

CREATE INDEX IF NOT EXISTS idx_knowledge_embeddings_metadata
  ON knowledge_embeddings USING gin (metadata);

-- Create function for similarity search
CREATE OR REPLACE FUNCTION search_knowledge(
  query_embedding vector(1536),
  match_threshold FLOAT,
  match_count INT,
  org_id UUID DEFAULT NULL
)
RETURNS TABLE(
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    ke.id,
    ke.content,
    ke.metadata,
    1 - (ke.embedding <=> query_embedding) AS similarity
  FROM knowledge_embeddings ke
  WHERE
    (org_id IS NULL OR ke.organization_id = org_id)
    AND 1 - (ke.embedding <=> query_embedding) > match_threshold
  ORDER BY ke.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

## Performance Testing

```sql
-- Test vector search performance
EXPLAIN ANALYZE
SELECT * FROM search_knowledge(
  (SELECT embedding FROM knowledge_embeddings LIMIT 1),
  0.7,
  10,
  'some-org-uuid'
);
```

## Connection Pool Configuration

```typescript
// packages/db/src/pool.ts
import { PrismaClient } from "@prisma/client";

export function createPooledClient(): PrismaClient {
  const url = new URL(process.env.DATABASE_URL!);

  // Add PgBouncer-compatible connection string
  if (process.env.NODE_ENV === "production") {
    url.searchParams.set("pgbouncer", "true");
    url.searchParams.set("statement_cache_size", "0");
    url.searchParams.set("connection_limit", "10");
    url.searchParams.set("pool_timeout", "30");
  }

  return new PrismaClient({
    datasources: {
      db: { url: url.toString() },
    },
    log: process.env.NODE_ENV === "development"
      ? ["query", "error", "warn"]
      : ["error"],
  });
}
```

## Backup and Restore

```bash
#!/bin/bash
# scripts/db-backup.sh
# Backup local development database

BACKUP_DIR="./docker/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="voice_agent_dev"

mkdir -p "$BACKUP_DIR"

echo "Backing up $DB_NAME..."
docker exec voice-agent-postgres pg_dump \
  -U postgres \
  -d "$DB_NAME" \
  --format=custom \
  --compress=9 \
  --verbose \
  -f "/tmp/${DB_NAME}_${TIMESTAMP}.dump"

docker cp \
  "voice-agent-postgres:/tmp/${DB_NAME}_${TIMESTAMP}.dump" \
  "${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.dump"

echo "Backup saved to ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.dump"
```

```bash
#!/bin/bash
# scripts/db-restore.sh
# Restore local development database

BACKUP_FILE=$1
if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: ./db-restore.sh <backup-file>"
  exit 1
fi

echo "Restoring from $BACKUP_FILE..."
docker cp "$BACKUP_FILE" "voice-agent-postgres:/tmp/restore.dump"

docker exec voice-agent-postgres pg_restore \
  -U postgres \
  -d voice_agent_dev \
  --clean \
  --if-exists \
  --verbose \
  /tmp/restore.dump

echo "Restore complete."
```

## Design Decisions

### pgvector vs. dedicated vector database

| Feature | pgvector | Pinecone | Weaviate | Qdrant |
|---------|----------|----------|----------|--------|
| Operational simplicity | High (in-DB) | Low (external) | Medium | Medium |
| Consistency with data | Strong (same transaction) | Eventual | Configurable | Configurable |
| Query language | SQL | REST/gRPC | GraphQL | REST/gRPC |
| Scale limit | ~50M vectors | Unlimited | Unlimited | Unlimited |
| Cost | Free | Usage-based | Self-host | Self-host |

**Decision**: Use pgvector for development and initial production. The operational simplicity of keeping embeddings in the same database outweighs the scaling advantages of dedicated vector databases at our expected scale (< 10M embeddings). If we exceed pgvector's limits, we can migrate to Pinecone with the same embedding interface.

### Why UUID primary keys?

UUIDs (ULID) prevent ID collision during distributed operations and make database merging possible. They're slightly slower than auto-increment integers (especially for B-tree indexes) but the difference is negligible at our scale.

## Integration Points

- **Prisma**: Schema migrations and client generation
- **pgvector**: Embedding storage and similarity search
- **pg_stat_statements**: Query performance monitoring
- **PgBouncer**: Connection pooling in production

## Production Considerations

1. **Connection pooling**: Prisma's connection management is adequate for development. In production, use PgBouncer for connection pooling. Configure PgBouncer with `transaction` mode and set `?pgbouncer=true` in the DATABASE_URL
2. **Index maintenance**: IVFFlat indexes require periodic rebuilding as data changes. Schedule `REINDEX` during maintenance windows. Consider using HNSW indexes (available in pgvector 0.6+) for better query performance with dynamic data
3. **Monitoring**: Use pg_stat_statements to identify slow queries. Log queries that exceed 100ms in production
4. **Backup strategy**: Development databases should be backed up daily to local storage. Production databases require continuous WAL archiving and point-in-time recovery
5. **Extension updates**: When upgrading PostgreSQL, verify all extensions (especially pgvector) are compatible. Extension version mismatches are a common cause of migration failures
