# SaaS Schema Design Patterns

## The Multi-Tenant Data Challenge

Every SaaS application must handle data from multiple customers (tenants) while ensuring proper isolation. Your schema design affects everything from security to performance to billing. Getting it right early prevents painful migrations later.

This guide covers schema design patterns for SaaS: multi-tenant data isolation, user management, billing data, audit logging, and common anti-patterns.

## Multi-Tenant Data Isolation

### The Three Isolation Models

```markdown
1. Shared Database, Shared Schema (Simplest)
   - All tenants in same tables
   - Tenant identified by tenant_id column
   - Every query filters by tenant_id

2. Shared Database, Separate Schemas
   - Each tenant has their own schema
   - Same table structure, different schema namespace
   - Better isolation, more complex management

3. Separate Databases
   - Each tenant has their own database
   - Maximum isolation
   - Most complex and expensive
```

### Which Model to Choose

```markdown
Isolation Model Decision Matrix:

| Factor | Shared Schema | Separate Schema | Separate DB |
|--------|---------------|-----------------|-------------|
| Complexity | Low | Medium | High |
| Cost | Low | Low-Medium | High |
| Data isolation | Low | Medium | High |
| Cross-tenant queries | Easy | Hard | Impossible |
| Maintenance | Simple | Moderate | Complex |
| Backup/Restore per tenant| Hard | Moderate | Easy |
| Migration difficulty | High | Medium | Low |
| Compliance support | Low | Medium | High |

Solo Founder Recommendation:
  MVP → Shared Schema (simplest)
  Growth → Row-Level Security in Shared Schema (better isolation)
  Scale → Separate Schemas or Databases (for compliance/scale)
```

### Shared Schema with Row-Level Security (PostgreSQL)

For 90% of solo founders, shared schema with RLS is the optimal approach:

```sql
-- Enable RLS
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tenants table
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  plan VARCHAR(50) DEFAULT 'free',
  settings JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (belong to tenants)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'member', -- owner, admin, member
  password_hash VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, email)
);

-- Projects (tenant-scoped)
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on tenant-scoped tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Users can only see users in their tenant
CREATE POLICY tenant_users_isolation ON users
  USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Projects are visible only within the tenant
CREATE POLICY tenant_projects_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Admin can see all (for support purposes)
CREATE POLICY admin_access ON projects
  FOR SELECT
  USING (current_setting('app.user_role') = 'admin');

-- Set tenant context in application
-- app/middleware/tenant.ts
export function setTenantContext(req: Request, res: Response, next: NextFunction) {
  const tenantId = req.headers['x-tenant-id'] || req.user?.tenantId;
  if (tenantId) {
    // Set PostgreSQL session variables for RLS
    pool.query('SELECT set_config($1, $2, true)', [
      'app.tenant_id',
      tenantId,
    ]);
    pool.query('SELECT set_config($1, $2, true)', [
      'app.user_role',
      req.user?.role || 'member',
    ]);
  }
  next();
}
```

### Application-Level Tenant Isolation

If you're not using PostgreSQL RLS, enforce tenant isolation at the application layer:

```typescript
// lib/database/tenant-aware.ts
// Tenant-aware query builder

class TenantAwareQuery {
  constructor(
    private tenantId: string,
    private pool: Pool
  ) {}

  async query(sql: string, params?: any[]) {
    // Ensure all queries include tenant filter
    return this.pool.query(sql, params);
  }

  // Helper that automatically adds tenant_id filter
  async selectFrom(table: string, options: {
    columns?: string[];
    where?: string;
    params?: any[];
    orderBy?: string;
    limit?: number;
    offset?: number;
  }): Promise<any[]> {
    let sql = `SELECT ${options.columns?.join(', ') || '*'} FROM ${table}`;
    sql += ` WHERE tenant_id = $1`;

    if (options.where) {
      sql += ` AND ${options.where}`;
    }

    if (options.orderBy) {
      sql += ` ORDER BY ${options.orderBy}`;
    }

    if (options.limit) {
      sql += ` LIMIT ${options.limit}`;
    }

    if (options.offset) {
      sql += ` OFFSET ${options.offset}`;
    }

    const params = [this.tenantId, ...(options.params || [])];
    const result = await this.pool.query(sql, params);
    return result.rows;
  }

  async insertInto(table: string, data: Record<string, any>) {
    // Automatically add tenant_id
    const insertData = { tenant_id: this.tenantId, ...data };
    const columns = Object.keys(insertData);
    const values = Object.values(insertData);
    const placeholders = values.map((_, i) => `$${i + 1}`);

    const sql = `INSERT INTO ${table} (${columns.join(', ')})
                 VALUES (${placeholders.join(', ')})
                 RETURNING *`;

    const result = await this.pool.query(sql, values);
    return result.rows[0];
  }
}

// Usage
const db = new TenantAwareQuery(req.tenantId, pool);
const projects = await db.selectFrom('projects', {
  where: 'status = $2',
  params: ['active'],
  orderBy: 'created_at DESC',
});
```

## User Management Schema

### Complete User Schema Pattern

```sql
-- Extended user management for SaaS

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Core users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),

  -- Authentication
  email VARCHAR(255) NOT NULL,
  email_verified_at TIMESTAMPTZ,
  password_hash VARCHAR(255),
  auth_provider VARCHAR(50), -- 'email', 'google', 'github', 'sso'
  auth_provider_id VARCHAR(255), -- External provider's user ID

  -- Profile
  name VARCHAR(255) NOT NULL,
  display_name VARCHAR(255),
  avatar_url TEXT,
  timezone VARCHAR(50) DEFAULT 'UTC',
  locale VARCHAR(10) DEFAULT 'en',

  -- Status
  role VARCHAR(50) DEFAULT 'member',
  is_active BOOLEAN DEFAULT true,
  is_onboarded BOOLEAN DEFAULT false,

  -- Metadata
  metadata JSONB DEFAULT '{}',
  last_login_at TIMESTAMPTZ,
  last_login_ip INET,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(tenant_id, email)
);

-- Indexes for common queries
CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(tenant_id, role);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- User sessions
CREATE TABLE user_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL,
  ip_address INET,
  user_agent TEXT,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);

-- User invitations (for team invites)
CREATE TABLE invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  token VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(50) DEFAULT 'member',
  invited_by UUID REFERENCES users(id),
  expires_at TIMESTAMPTZ NOT NULL,
  accepted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_invitations_tenant ON invitations(tenant_id);
CREATE INDEX idx_invitations_email ON invitations(email);
CREATE INDEX idx_invitations_token ON invitations(token);
```

## Billing Schema

### Subscription and Billing Schema

```sql
-- Plans (product catalog)
CREATE TABLE plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  price_cents INTEGER NOT NULL,
  currency VARCHAR(3) DEFAULT 'usd',
  interval VARCHAR(20) DEFAULT 'month', -- month, year
  trial_days INTEGER DEFAULT 0,
  features JSONB DEFAULT '{}', -- { "max_projects": 10, "max_users": 5 }
  is_active BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  plan_id UUID NOT NULL REFERENCES plans(id),

  -- Stripe/LemonSqueezy integration
  provider VARCHAR(50) DEFAULT 'stripe',
  provider_subscription_id VARCHAR(255),
  provider_customer_id VARCHAR(255),

  -- Status
  status VARCHAR(50) NOT NULL DEFAULT 'trialing',
  -- active, trialing, past_due, canceled, incomplete, incomplete_expired

  -- Period
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  trial_start TIMESTAMPTZ,
  trial_end TIMESTAMPTZ,

  -- Cancellation
  cancel_at_period_end BOOLEAN DEFAULT false,
  canceled_at TIMESTAMPTZ,
  cancellation_reason TEXT,

  -- Metadata
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_provider ON subscriptions(provider, provider_subscription_id);
CREATE INDEX idx_subscriptions_period ON subscriptions(current_period_end);

-- Invoices
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  subscription_id UUID REFERENCES subscriptions(id),

  -- Provider reference
  provider VARCHAR(50) DEFAULT 'stripe',
  provider_invoice_id VARCHAR(255),
  provider_payment_intent_id VARCHAR(255),

  -- Amount
  amount_cents INTEGER NOT NULL,
  currency VARCHAR(3) DEFAULT 'usd',
  tax_cents INTEGER DEFAULT 0,
  total_cents INTEGER NOT NULL,

  -- Status
  status VARCHAR(50) NOT NULL DEFAULT 'open',
  -- open, paid, void, uncollectible

  -- Dates
  paid_at TIMESTAMPTZ,
  due_date TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(provider, provider_invoice_id)
);

CREATE INDEX idx_invoices_tenant ON invoices(tenant_id);
CREATE INDEX idx_invoices_subscription ON invoices(subscription_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_created ON invoices(created_at);

-- Usage records (for usage-based billing)
CREATE TABLE usage_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  metric VARCHAR(100) NOT NULL, -- 'api_calls', 'storage_gb', 'seats'
  quantity DECIMAL(12,4) NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_usage_tenant ON usage_records(tenant_id, metric, recorded_at);

-- Helper: Get current subscription for tenant
CREATE OR REPLACE VIEW current_subscriptions AS
  SELECT DISTINCT ON (s.tenant_id)
    s.*, p.name as plan_name, p.slug as plan_slug,
    p.features as plan_features, p.price_cents as plan_price
  FROM subscriptions s
  JOIN plans p ON s.plan_id = p.id
  WHERE s.status IN ('active', 'trialing', 'past_due')
  ORDER BY s.tenant_id, s.created_at DESC;
```

### Billing Service Pattern

```typescript
// lib/billing/subscription.ts

class SubscriptionService {
  async getPlanFeatures(tenantId: string): Promise<Record<string, any>> {
    const result = await pool.query(
      `SELECT p.features FROM current_subscriptions cs
       JOIN plans p ON cs.plan_id = p.id
       WHERE cs.tenant_id = $1`,
      [tenantId]
    );

    // Default plan features if no subscription
    return result.rows[0]?.features || {
      max_projects: 3,
      max_users: 1,
      max_storage_mb: 100,
    };
  }

  async checkFeatureAccess(
    tenantId: string,
    feature: string,
    currentValue: number
  ): Promise<{ allowed: boolean; limit: number }> {
    const features = await this.getPlanFeatures(tenantId);
    const limit = features[feature] || 0;

    return {
      allowed: limit === -1 || currentValue < limit, // -1 = unlimited
      limit,
    };
  }
}
```

## Audit Logging Schema

### Complete Audit Trail

```sql
-- Audit log for tracking all important changes
CREATE TYPE audit_action AS ENUM (
  'created', 'updated', 'deleted', 'viewed',
  'exported', 'imported', 'shared',
  'login', 'logout', 'password_changed',
  'invitation_sent', 'invitation_accepted',
  'subscription_changed', 'payment_received',
  'role_changed', 'settings_changed'
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),

  -- Who
  actor_id UUID REFERENCES users(id),
  actor_email VARCHAR(255),
  actor_ip INET,

  -- What
  action audit_action NOT NULL,
  entity_type VARCHAR(100) NOT NULL, -- 'project', 'user', 'subscription'
  entity_id UUID,
  changes JSONB, -- { "field": { "old": "...", "new": "..." } }

  -- Context
  metadata JSONB DEFAULT '{}',
  user_agent TEXT,
  request_id VARCHAR(255),

  -- When
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for querying audit logs
CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id, created_at);
CREATE INDEX idx_audit_actor ON audit_logs(actor_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_metadata ON audit_logs USING GIN (metadata);

-- Partition by month for large audit tables
CREATE TABLE audit_logs_y2024m01 PARTITION OF audit_logs
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE audit_logs_y2024m02 PARTITION OF audit_logs
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

### Audit Log Helper

```typescript
// lib/audit/index.ts

interface AuditEntry {
  tenantId: string;
  actorId?: string;
  actorEmail?: string;
  actorIp?: string;
  action: string;
  entityType: string;
  entityId?: string;
  changes?: Record<string, { old: any; new: any }>;
  metadata?: Record<string, any>;
  userAgent?: string;
  requestId?: string;
}

class AuditLogger {
  async log(entry: AuditEntry) {
    await pool.query(
      `INSERT INTO audit_logs
       (tenant_id, actor_id, actor_email, actor_ip,
        action, entity_type, entity_id, changes,
        metadata, user_agent, request_id)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)`,
      [
        entry.tenantId, entry.actorId, entry.actorEmail, entry.actorIp,
        entry.action, entry.entityType, entry.entityId,
        JSON.stringify(entry.changes || {}),
        JSON.stringify(entry.metadata || {}),
        entry.userAgent, entry.requestId,
      ]
    );
  }

  async getEntityHistory(
    entityType: string,
    entityId: string,
    tenantId: string,
    limit = 50
  ) {
    const result = await pool.query(
      `SELECT * FROM audit_logs
       WHERE tenant_id = $1
         AND entity_type = $2
         AND entity_id = $3
       ORDER BY created_at DESC
       LIMIT $4`,
      [tenantId, entityType, entityId, limit]
    );
    return result.rows;
  }

  diff<T extends Record<string, any>>(
    before: T,
    after: T
  ): Record<string, { old: any; new: any }> {
    const changes: Record<string, { old: any; new: any }> = {};
    for (const key of Object.keys(after)) {
      if (JSON.stringify(before[key]) !== JSON.stringify(after[key])) {
        changes[key] = { old: before[key], new: after[key] };
      }
    }
    return changes;
  }
}

export const auditLogger = new AuditLogger();
```

## Feature Flags Schema

```sql
-- Feature flags for gradual rollouts
CREATE TABLE feature_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  is_enabled BOOLEAN DEFAULT false,
  rollout_percentage INTEGER DEFAULT 0, -- 0-100
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenant-specific overrides
CREATE TABLE tenant_feature_flags (
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  feature_flag_id UUID NOT NULL REFERENCES feature_flags(id),
  is_enabled BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (tenant_id, feature_flag_id)
);

-- Plan-based feature access (from plans.features JSON)
-- Already handled in the plans table
```

## API Keys Schema

```sql
-- API Keys for programmatic access
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  name VARCHAR(255) NOT NULL,
  key_prefix VARCHAR(10) NOT NULL, -- First 10 chars of key (for identification)
  key_hash VARCHAR(255) NOT NULL, -- Hashed full key
  permissions JSONB DEFAULT '[]', -- ["read", "write", "admin"]
  ip_restrictions INET[], -- Optional: restrict to specific IPs
  last_used_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_api_keys_tenant ON api_keys(tenant_id);
CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
```

## Webhook Events Schema

```sql
-- Webhook event delivery tracking
CREATE TABLE webhook_endpoints (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  url VARCHAR(2048) NOT NULL,
  secret VARCHAR(255) NOT NULL,
  events VARCHAR(100)[] NOT NULL, -- Which events to deliver
  is_active BOOLEAN DEFAULT true,
  last_success_at TIMESTAMPTZ,
  last_failure_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE webhook_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  endpoint_id UUID NOT NULL REFERENCES webhook_endpoints(id),
  event_type VARCHAR(100) NOT NULL,
  payload JSONB NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  -- pending, delivered, failed, retrying
  response_status INTEGER,
  response_body TEXT,
  attempt_count INTEGER DEFAULT 0,
  max_attempts INTEGER DEFAULT 5,
  last_attempt_at TIMESTAMPTZ,
  next_attempt_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_webhook_deliveries_endpoint ON webhook_deliveries(endpoint_id);
CREATE INDEX idx_webhook_deliveries_next ON webhook_deliveries(next_attempt_at)
  WHERE status = 'pending' OR status = 'retrying';
```

## Common SaaS Schema Anti-Patterns

### Anti-Pattern 1: The God Table

```sql
-- BAD: One table for everything
CREATE TABLE entities (
  id UUID PRIMARY KEY,
  type VARCHAR(50) NOT NULL, -- 'user', 'project', 'task', 'comment'
  tenant_id UUID,
  data JSONB NOT NULL -- Everything in one JSONB column
);

-- GOOD: Separate tables for each entity
CREATE TABLE users (...);
CREATE TABLE projects (...);
CREATE TABLE tasks (...);
CREATE TABLE comments (...);
```

### Anti-Pattern 2: Missing Indexes

```sql
-- BAD: No indexes on frequently queried columns
SELECT * FROM projects WHERE tenant_id = 'abc' AND status = 'active';

-- GOOD: Indexes on filter and join columns
CREATE INDEX idx_projects_tenant_status ON projects(tenant_id, status);
```

### Anti-Pattern 3: Soft Deletes Without Plans

```sql
-- BAD: Soft deletes without cleanup or query guidance
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Every query must remember to filter: WHERE deleted_at IS NULL
-- Over time, deleted records outnumber active records

-- GOOD: Separate archive table for soft deletes
CREATE TABLE deleted_users (LIKE users INCLUDING ALL);
-- Move deleted records here, not flag them in the main table
```

### Anti-Pattern 4: Over-Normalization

```sql
-- BAD: Normalized to the extreme
CREATE TABLE addresses (
  id UUID PRIMARY KEY,
  street VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  zip VARCHAR(20),
  country VARCHAR(100)
);

CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255),
  billing_address_id UUID REFERENCES addresses(id),
  shipping_address_id UUID REFERENCES addresses(id)
);

-- GOOD: Denormalize when appropriate
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255),
  billing_address JSONB, -- Denormalized address
  shipping_address JSONB
);
```

### Anti-Pattern 5: Missing Audit Trail

```sql
-- BAD: No record of who changed what
UPDATE users SET role = 'admin' WHERE id = '123';
-- Now you don't know who made this change or when

-- GOOD: Use audit logging (see audit_logs table above)
-- Or use generated columns for tracking
ALTER TABLE users ADD COLUMN updated_by UUID REFERENCES users(id);
ALTER TABLE users ADD COLUMN updated_at TIMESTAMPTZ DEFAULT NOW();
```

## Schema Migration Patterns

### Adding a New Table

```sql
-- Always use migrations, not direct SQL changes

-- migration_001_create_projects.sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_tenant ON projects(tenant_id);
```

### Adding a Column

```sql
-- migration_002_add_projects_description.sql
ALTER TABLE projects ADD COLUMN description TEXT;
ALTER TABLE projects ADD COLUMN status VARCHAR(50) DEFAULT 'active';

-- For nullable columns with defaults, this is instant.
-- For columns with NOT NULL, add as nullable first, then fill, then add constraint.
```

### Adding a JSONB Index

```sql
-- migration_003_add_projects_metadata_index.sql
ALTER TABLE projects ADD COLUMN metadata JSONB DEFAULT '{}';
CREATE INDEX idx_projects_metadata ON projects USING GIN (metadata);
```

## Complete SaaS Schema Template

```sql
-- Complete MVP schema for a typical SaaS

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tenants (organizations)
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  plan VARCHAR(50) DEFAULT 'free',
  settings JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'member',
  password_hash VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, email)
);

-- 3. Plans
CREATE TABLE plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  price_cents INTEGER NOT NULL,
  interval VARCHAR(20) DEFAULT 'month',
  features JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0
);

-- 4. Subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  plan_id UUID NOT NULL REFERENCES plans(id),
  provider VARCHAR(50) DEFAULT 'stripe',
  provider_subscription_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'trialing',
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Your core entities (example: projects)
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Audit logs
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  actor_id UUID,
  action VARCHAR(50) NOT NULL,
  entity_type VARCHAR(100) NOT NULL,
  entity_id UUID,
  changes JSONB,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_tenant ON projects(tenant_id, status);
CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id, created_at);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
```

## Summary

Good SaaS schema design follows these principles:

1. **Multi-tenant isolation from day one** — Shared schema with `tenant_id` column, RLS for security
2. **Single source of truth for user identity** — Users table is canonical, reference by UUID
3. **Billing is separate from core data** — Subscriptions and plans are their own bounded context
4. **Audit everything** — Audit logs from day one (you'll need them for support and compliance)
5. **Feature flags in the schema** — Plan-based feature control in JSONB
6. **Indexes on tenant_id and status** — Most common query filters
7. **JSONB for flexible metadata** — Avoid schema changes for non-critical fields
8. **UUIDs as primary keys** — Never use auto-increment integers (security and migration reasons)
9. **Timestamps on every table** — `created_at` and `updated_at` are non-negotiable
10. **Soft deletes are a trap** — Use audit logs and archive tables instead
