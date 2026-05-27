# Chapter 02: Tenant Schema Design & Row-Level Security

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Tenant ID Column Pattern](sec-01-tenant-id-column-pattern.md) | Universal tenant_id column, composite keys, indexing strategy, foreign key considerations |
| 02 | [PostgreSQL Row-Level Security Policies](sec-02-postgresql-rls-policies.md) | RLS policy syntax, enable row level security, policy types, USING vs WITH CHECK expressions |
| 03 | [Tenant Context Middleware Pattern](sec-03-tenant-context-middleware.md) | Request-scoped tenant context, middleware architecture, thread-local storage in Node.js |
| 04 | [RLS Performance Optimization](sec-04-rls-performance.md) | Indexing for RLS, policy complexity impact, query planning with RLS, benchmarking |
| 05 | [Cross-Tenant Query Safeguards](sec-05-cross-tenant-safeguards.md) | Forced tenant filtering, query interceptors, SQL injection prevention, audit detection |
| 06 | [Tenant-Aware Database Migrations](sec-06-tenant-aware-migrations.md) | Migration strategies per tenancy model, running migrations across tenants, rollback isolation |
| 07 | [Read-Replica Tenant Routing](sec-07-read-replica-routing.md) | Tenant-consistent read replica routing, stale read tolerance per tenant, replica lag monitoring |
| 08 | [Tenant Data Backup Isolation](sec-08-tenant-backup-isolation.md) | Per-tenant backup strategies, point-in-time recovery with tenant context, backup encryption |

---

## RLS Policy Example

```sql
-- Enable RLS on a table
ALTER TABLE calls ENABLE ROW LEVEL SECURITY;

-- Create tenant isolation policy
CREATE POLICY tenant_isolation ON calls
  USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Create admin override policy
CREATE POLICY admin_access ON calls
  USING (current_setting('app.current_role') = 'admin');
```

---

## Learning Objectives

- Implement tenant_id column pattern across all tables
- Write PostgreSQL row-level security policies for tenant isolation
- Build tenant context middleware for web request pipelines
- Optimize RLS query performance with proper indexing
- Implement cross-tenant query safeguards and detection
- Design tenant-aware database migration strategies
- Route read replicas consistently per tenant
- Create isolated backup and recovery procedures per tenant
