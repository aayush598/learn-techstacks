# Chapter 01: Multi-Tenancy Models & Strategy

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Tenancy Model Comparison Framework](sec-01-tenancy-model-comparison.md) | Database-per-tenant vs schema-per-tenant vs shared, hybrid approaches, decision matrix |
| 02 | [Database-per-Tenant Strategy](sec-02-database-per-tenant.md) | Full isolation, connection pooling, migration overhead, backup strategies, when to use |
| 03 | [Schema-per-Tenant Strategy](sec-03-schema-per-tenant.md) | Shared database with isolated schemas, schema management, connection routing |
| 04 | [Shared Tenant + RLS Strategy](sec-04-shared-tenant-rls.md) | Single schema with tenant ID column, PostgreSQL RLS policies, performance implications |
| 05 | [Hybrid Multi-Tenancy Approaches](sec-05-hybrid-approaches.md) | Tier-based isolation mixing, gradual isolation upgrade path, enterprise vs SMB segmentation |
| 06 | [Tenant Isolation Level Selection Guide](sec-06-isolation-level-selection.md) | Decision tree for choosing isolation level, cost vs compliance trade-off analysis |
| 07 | [Cross-Tenant Data Sharing Patterns](sec-07-cross-tenant-sharing.md) | Controlled data sharing between tenants, global reference data, shared pool resources |
| 08 | [Migration Between Tenancy Models](sec-08-migration-between-models.md) | Live migration strategies, downtime minimization, data consistency validation, rollback plans |

---

## Key Tenancy Models

| Model | Isolation | Complexity | Cost | Typical Use |
|-------|-----------|------------|------|-------------|
| Database-per-Tenant | Highest | High | High | Enterprise, Healthcare |
| Schema-per-Tenant | High | Medium | Medium | Mid-Market, Compliance |
| Shared + RLS | Medium | Low | Low | SMB, Starter Tiers |
| Hybrid | Custom | High | Variable | Mixed Customer Base |

---

## Learning Objectives

- Compare multi-tenancy models across isolation, cost, complexity, and compliance dimensions
- Implement database-per-tenant isolation with automated provisioning
- Design schema-per-tenant patterns with PostgreSQL schemas
- Architect shared-tenant solutions with row-level security
- Build hybrid approaches that mix isolation levels by customer tier
- Create a tenant isolation decision framework for your SaaS
- Implement cross-tenant data sharing with proper guardrails
- Execute live migrations between tenancy models with zero downtime
