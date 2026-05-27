# Chapter 07: Local Database & Service Orchestration

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [PostgreSQL Local Setup](sec-01-postgresql-local-setup.md) | Configuration, pgvector extension, database creation, user/permissions |
| 02 | [Prisma Schema & Migrations](sec-02-prisma-schema-migrations.md) | Schema definition, migration generation, apply/reset, seed scripts, migration naming |
| 03 | [Redis Configuration](sec-03-redis-configuration.md) | Redis Stack (JSON, Search, Timeseries), persistence config, maxmemory policy |
| 04 | [Kafka Local Setup](sec-04-kafka-local-setup.md) | KRaft mode (no Zookeeper), topic creation, partition configuration, consumer groups |
| 05 | [MinIO Storage Setup](sec-05-minio-storage-setup.md) | Bucket creation (recordings, transcripts, exports), access policies, lifecycle rules |
| 06 | [Seed Data Strategy](sec-06-seed-data-strategy.md) | Development seed data, demo tenant, sample agents, test contacts, fake call records |
| 07 | [Service Health & Monitoring](sec-07-service-health-monitoring.md) | Health check endpoints, service status dashboard, restart policies, log aggregation |

---

## Key Takeaways

- PostgreSQL with pgvector is the primary data store
- Prisma handles schema migrations with type-safe client
- Redis for caching, sessions, rate limiting, and pub/sub
- Kafka in KRaft mode (no Zookeeper dependency) for event streaming
- MinIO replaces S3 for local development of recording storage
- Seed data creates a realistic demo environment out of the box
- All services have health checks and auto-restart policies
