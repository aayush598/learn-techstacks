# Section 02: PostgreSQL Row-Level Security Policies

## Overview

PostgreSQL Row-Level Security (RLS) is the database-level mechanism for enforcing tenant isolation in shared-table multi-tenancy models. When RLS is enabled on a table, PostgreSQL automatically evaluates policy expressions for every query against that table, transparently filtering rows that the current session is not permitted to access. This provides a security layer that operates below the application layer, ensuring that even if application-level tenant filtering fails, the database prevents cross-tenant data access.

RLS policies are defined using PostgreSQL's policy syntax: `CREATE POLICY name ON table FOR operation USING (expression) [WITH CHECK (expression)]`. The `USING` clause determines which rows are visible for SELECT, UPDATE, and DELETE operations. The `WITH CHECK` clause determines which rows can be inserted or modified. Policies can reference session parameters (like `current_setting('app.tenant_id')`), function calls, subqueries, and joins to implement sophisticated access control rules.

For a voice agent platform, RLS policies go beyond simple tenant_id equality. They must handle admin override roles, support reseller hierarchy access, manage soft-delete visibility, and potentially implement time-based or status-based access restrictions. Policy performance is critical—every query against a table with RLS evaluates the policy, so policies must be simple and well-indexed.

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
-- Enable RLS extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Helper functions for tenant context
CREATE OR REPLACE FUNCTION app.current_tenant_id()
RETURNS UUID
LANGUAGE SQL
STABLE
AS $$
  SELECT current_setting('app.tenant_id')::UUID;
$$;

CREATE OR REPLACE FUNCTION app.current_user_role()
RETURNS TEXT
LANGUAGE SQL
STABLE
AS $$
  SELECT current_setting('app.user_role', true);
$$;

CREATE OR REPLACE FUNCTION app.is_admin()
RETURNS BOOLEAN
LANGUAGE SQL
STABLE
AS $$
  SELECT current_setting('app.user_role', true) IN ('admin', 'superadmin');
$$;

-- Enable RLS on tables
ALTER TABLE calls ENABLE ROW LEVEL SECURITY;
ALTER TABLE calls FORCE ROW LEVEL SECURITY;  -- Even table owner must obey

ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents FORCE ROW LEVEL SECURITY;

ALTER TABLE transcripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE transcripts FORCE ROW LEVEL SECURITY;

-- Tenant isolation policies
-- SELECT: Only see rows belonging to your tenant (or admin)
CREATE POLICY tenant_isolation_select ON calls
  FOR SELECT
  USING (
    tenant_id = app.current_tenant_id()
    OR app.is_admin()
  );

-- INSERT: Must belong to your tenant
CREATE POLICY tenant_isolation_insert ON calls
  FOR INSERT
  WITH CHECK (
    tenant_id = app.current_tenant_id()
  );

-- UPDATE: Only update your tenant's rows
CREATE POLICY tenant_isolation_update ON calls
  FOR UPDATE
  USING (tenant_id = app.current_tenant_id())
  WITH CHECK (tenant_id = app.current_tenant_id());  -- Prevent changing tenant_id

-- DELETE: Only delete your tenant's rows
CREATE POLICY tenant_isolation_delete ON calls
  FOR DELETE
  USING (tenant_id = app.current_tenant_id());

-- Admin override: Full access for support
CREATE POLICY admin_full_access ON calls
  FOR ALL
  USING (app.is_admin())
  WITH CHECK (app.is_admin());

-- Read-only role policy (for analytics users)
CREATE POLICY read_only_access ON calls
  FOR SELECT
  USING (
    current_setting('app.user_role', true) = 'analyst'
    AND created_at >= NOW() - INTERVAL '90 days'  -- Time-bound access
  );

-- Reseller hierarchy policy
CREATE POLICY reseller_access ON calls
  FOR SELECT
  USING (
    tenant_id IN (
      SELECT id FROM tenants 
      WHERE parent_tenant_id = app.current_tenant_id()
        OR id = app.current_tenant_id()
    )
    AND current_setting('app.user_role', true) = 'reseller_admin'
  );

-- Soft-delete visibility (hide soft-deleted records from regular users)
CREATE POLICY hide_soft_deleted ON calls
  FOR SELECT
  USING (
    deleted_at IS NULL 
    OR app.is_admin()
    OR current_setting('app.user_role', true) = 'auditor'
  );

-- Create specific database roles
CREATE ROLE voiceagent_app;
CREATE ROLE voiceagent_admin;
CREATE ROLE voiceagent_analyst;
CREATE ROLE voiceagent_reseller;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON calls TO voiceagent_app;
GRANT ALL ON ALL TABLES IN SCHEMA public TO voiceagent_admin;
GRANT SELECT ON calls TO voiceagent_analyst;
GRANT SELECT ON calls TO voiceagent_reseller;

-- Note: RLS policies will further restrict what these roles can see
```

## Integration Points

- **Tenant Context Middleware:** Sets `app.tenant_id` and `app.user_role` before each request
- **Admin Dashboard:** Admin logs in with `voiceagent_admin` role for cross-tenant support
- **Analytics Pipeline:** Uses `voiceagent_analyst` role with time-bound access to recent data
- **Reseller Portal:** Uses `voiceagent_reseller` role for hierarchical tenant access
- **Audit Logging:** `app.current_user_role()` is logged for all access attempts

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Policy Performance:** Each RLS policy is evaluated for every row, so policy expressions must be fast. Avoid subqueries in RLS policies on high-traffic tables. Use indexed columns and simple equality checks.
- **Policy Testing:** Create a comprehensive test suite for RLS policies. Test every role, every operation type, and every edge case. Use `pgtap` for automated RLS testing in CI/CD.
- **Policy Management:** Track RLS policies as code in your migration files. Each deployment should verify that expected policies exist on all tenant-scoped tables.
- **FORCE ROW LEVEL SECURITY:** Always use `FORCE ROW LEVEL SECURITY` to ensure even the table owner (or superuser) respects RLS. This prevents accidental bypass during maintenance.
- **EXPLAIN with RLS:** Use `EXPLAIN (ANALYZE, BUFFERS)` on queries with RLS to verify that the policy is being applied efficiently. Look for sequential scans where indexes should be used.
- **Policy Conflicts:** When multiple policies apply to the same operation, PostgreSQL ORs them together (a row visible if any policy allows it). Design policies carefully to avoid unintended access.
- **RLS and Caching:** RLS policies are evaluated at the database level. ORM-level caches may bypass RLS. Ensure your caching strategy respects tenant isolation.
- **Migration Safety:** When adding or modifying RLS policies in production, test the impact on query performance first. A poorly written policy can cause a full table scan on a high-traffic table.
