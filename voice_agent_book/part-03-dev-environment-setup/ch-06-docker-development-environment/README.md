# Chapter 06: Docker Development Environment

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Docker Compose Architecture](sec-01-docker-compose-architecture.md) | Service definitions for PostgreSQL, Redis, Kafka, MinIO, Mailpit, pgAdmin |
| 02 | [Development Dockerfile](sec-02-development-dockerfile.md) | Hot reload configuration, volume mounts, node_modules handling, multi-stage for dev |
| 03 | [Production Dockerfile](sec-03-production-dockerfile.md) | Multi-stage builds (deps → build → production), image size optimization, security scanning |
| 04 | [Local Service Configuration](sec-04-local-service-configuration.md) | PostgreSQL with pgvector, Redis with modules, Kafka with KRaft, MinIO console |
| 05 | [DevContainers Setup](sec-05-devcontainers-setup.md) | VS Code DevContainers, consistent dev environment, extension installation, post-create commands |
| 06 | [Docker Network & Communication](sec-06-docker-network-communication.md) | Internal network, service discovery (service names), port mapping, health checks |

---

## Docker Compose Services

```yaml
services:
  postgres:   # PostgreSQL 16 + pgvector
  redis:      # Redis 7
  kafka:      # Apache Kafka (KRaft mode)
  minio:      # S3-compatible object storage
  mailpit:    # Email testing
  pgadmin:    # Database management UI
```

---

## Key Takeaways

- Docker Compose for reproducible local development environment
- All external services (DB, cache, queue, storage) containerized
- Hot reload via volume mounts and Turborepo watch mode
- Production multi-stage builds for minimal image size
- DevContainers for consistent team development environments
- Health checks for all services to ensure proper startup order
