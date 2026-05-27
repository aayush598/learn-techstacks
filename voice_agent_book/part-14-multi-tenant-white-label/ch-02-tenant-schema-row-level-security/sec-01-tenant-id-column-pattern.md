# Section 01: Tenant ID Column Pattern

## Overview

The tenant ID column is the foundational building block of multi-tenant data isolation. Every table containing tenant-specific data must include a `tenant_id` column that associates each row with its owning tenant. This column serves as the discriminator for RLS policies, the partition key for tenant-aware sharding, the filter for cross-tenant query safeguards, and the basis for per-tenant backup and export operations. Getting the tenant ID column design right is critical—retrofitting it after production data exists is painful and risky.

The tenant ID should be a UUID (v4 or v7) stored as `UUID` type in PostgreSQL. UUIDs provide global uniqueness without coordination, prevent enumeration attacks (sequential integers expose tenant count and enable guessing), and support sharding and partitioning strategies. A `tenant_id` column must be `NOT NULL` with a foreign key constraint to the `tenants` table, ensuring referential integrity at the database level. Every `INSERT` must include the tenant ID, and every `SELECT`, `UPDATE`, and `DELETE` should filter by tenant ID (or rely on RLS to do so).

Beyond the basic column, the tenant ID pattern includes composite indexes for performance, default value functions for safety, and audit triggers for compliance. A `set_tenant_id()` default function using `current_setting('app.tenant_id')` ensures that application code that forgets to set tenant_id still gets the correct value from the session context.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```sql
-- PostgreSQL implementation
-- 1. Create helper function for tenant context
CREATE SCHEMA IF NOT EXISTS app;

CREATE OR REPLACE FUNCTION app.tenant_id()
RETURNS UUID
LANGUAGE SQL
STABLE
AS $$
  SELECT COALESCE(
    current_setting('app.tenant_id', true)::UUID,
    NULL
  );
$$;

CREATE OR REPLACE FUNCTION app.require_tenant_id()
RETURNS UUID
LANGUAGE SQL
STABLE
AS $$
  SELECT current_setting('app.tenant_id')::UUID;
$$;

-- 2. Create tenants table
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  tier TEXT NOT NULL DEFAULT 'starter',
  isolation_tier TEXT NOT NULL DEFAULT 'shared',
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Create tenant-scoped tables
CREATE TABLE calls (
  tenant_id UUID NOT NULL DEFAULT app.require_tenant_id()
              REFERENCES tenants(id) ON DELETE CASCADE,
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  caller_phone TEXT NOT NULL,
  callee_phone TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  duration_seconds INT,
  direction TEXT NOT NULL DEFAULT 'outbound',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  PRIMARY KEY (tenant_id, id)
);

-- 4. Create tenant-aware indexes
CREATE INDEX idx_calls_tenant_created 
  ON calls (tenant_id, created_at DESC);

CREATE INDEX idx_calls_tenant_status 
  ON calls (tenant_id, status) 
  WHERE status IN ('in_progress', 'queued');

CREATE INDEX idx_calls_tenant_caller 
  ON calls (tenant_id, caller_phone);

-- 5. Create function to enforce tenant_id on all queries
CREATE OR REPLACE FUNCTION app.enforce_tenant_id()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS $$
BEGIN
  IF NEW.tenant_id IS NULL THEN
    NEW.tenant_id := app.require_tenant_id();
  END IF;
  RETURN NEW;
END;
$$;

-- Apply trigger to all tenant-scoped tables
CREATE TRIGGER enforce_tenant_id_calls
  BEFORE INSERT ON calls
  FOR EACH ROW EXECUTE FUNCTION app.enforce_tenant_id();
```

## Integration Points

- **RLS Policies (Ch 02, Sec 02):** Tenant ID column is the foundation for all RLS policies
- **Migration Pipeline:** Migrations must include tenant_id in new tables
- **Export/Import (Ch 10):** Tenant ID is the filter key for data portability
- **Analytics (Part 11):** Aggregated queries GROUP BY tenant_id for cross-tenant reporting
- **Row-Level Security:** Every RLS policy references the tenant_id column

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Missing Tenant ID Detection:** Run periodic queries to find rows with NULL tenant_id. Set up alerts. Any NULL tenant_id is a bug that must be fixed immediately.
- **Tenant ID in Indexes:** Always include tenant_id as the leading column in indexes for tenant-scoped queries. PostgreSQL can efficiently skip non-matching partitions.
- **Foreign Key Cost:** `REFERENCES tenants(id) ON DELETE CASCADE` adds a small cost to every INSERT but provides critical referential integrity. Monitor `pg_stat_user_tables` for sequential scans on the tenants table.
- **Application Layer Validation:** Never rely solely on database-level tenant_id enforcement. Validate tenant_id at the API layer before passing to the database. RLS is a defense-in-depth measure, not the primary control.
- **Migration Safety:** When adding tenant_id to an existing table, use `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT (app.require_tenant_id())` only after ensuring all existing rows have valid tenant_id values. Consider a multi-step migration: add nullable, backfill, set NOT NULL.
- **Partitioning Strategy:** For very large tables, partition BY tenant_id ranges. PostgreSQL 11+ supports partition pruning that can dramatically improve query performance when filtering by tenant_id.
- **ORM Compatibility:** Most ORMs (Prisma, TypeORM, Sequelize) support composite keys and default values. Ensure your ORM configuration includes tenant_id in every model and every query.
- **Audit Logging:** Log any attempt to query without tenant context. This may indicate a bug or a security issue.
