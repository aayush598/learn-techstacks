# Chapter 03: Database Architecture & Data Modeling

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Entity Relationship Overview](sec-01-entity-relationship-overview.md) | Core entities: Tenant, User, Agent, Conversation, Call, Campaign, Recording, KnowledgeBase |
| 02 | [User & Tenant Schema](sec-02-user-tenant-schema.md) | Users with RLS, tenant isolation, user-role relationships, invite/team models |
| 03 | [Agent Configuration Schema](sec-03-agent-configuration-schema.md) | Agent, AgentVersion, AgentNode, AgentEdge, Prompt, Voice, Language models |
| 04 | [Call & Conversation Schema](sec-04-call-conversation-schema.md) | Call records, conversation events, transcript chunks, sentiment snapshots, escalation records |
| 05 | [Campaign & Contact Schema](sec-05-campaign-contact-schema.md) | Campaigns, ContactLists, Contacts, CallAttempts, DNC lists, CampaignResults |
| 06 | [Billing & Usage Schema](sec-06-billing-usage-schema.md) | Subscriptions, UsageRecords, Invoices, Payments, Credits, PlanDefinitions |
| 07 | [Indexing Strategy](sec-07-indexing-strategy.md) | B-tree for lookups, GiST for full-text search, HNSW for vectors, composite indexes for queries |
| 08 | [Migrations & Schema Evolution](sec-08-migrations-schema-evolution.md) | Prisma migrations, naming conventions, rollback strategy, migration testing, seed data |
| 09 | [Data Archival & Cleanup](sec-09-data-archival-cleanup.md) | Partitioning by date, archival policies, soft-delete, TTL-based cleanup, data retention |

---

## Key Takeaways

- Prisma ORM with PostgreSQL for type-safe database access
- RLS (Row-Level Security) for multi-tenant data isolation
- Composite indexes on (tenant_id, created_at) for all queries
- Partitioned tables for calls, conversations, and usage records
- pgvector extension for embedding storage and similarity search
- Migration pipeline with automated validation in CI/CD
