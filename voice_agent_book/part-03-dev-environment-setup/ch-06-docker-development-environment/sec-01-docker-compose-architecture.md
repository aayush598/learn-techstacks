# Section 01: Docker Compose Architecture

## Overview

Docker Compose provides a reproducible, isolated development environment for the voice agent platform. All external services — PostgreSQL, Redis, Kafka, MinIO, Mailpit, and pgAdmin — run as containers, eliminating the need for developers to install and configure these services on their host machines.

## Service Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Docker Compose Service Architecture              │
│                                                              │
│  Host Machine                                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Docker Network: voice-agent-dev                        │  │
│  │                                                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │ PostgreSQL│  │  Redis    │  │  Kafka    │             │  │
│  │  │ :5432     │  │ :6379     │  │ :9092     │             │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘             │  │
│  │       │              │              │                    │  │
│  │  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐             │  │
│  │  │  MinIO    │  │  Mailpit  │  │  pgAdmin  │             │  │
│  │  │ :9000     │  │ :8025     │  │ :5050     │             │  │
│  │  │ :9001     │  │ :1025     │  └──────────┘             │  │
│  │  └──────────┘  └──────────┘                              │  │
│  │                                                         │  │
│  │  Host Volumes (persistent data):                        │  │
│  │  ./docker/volumes/postgres                              │  │
│  │  ./docker/volumes/redis                                 │  │
│  │  ./docker/volumes/minio                                 │  │
│  │  ./docker/volumes/kafka                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  Application containers (optional, for DevContainers):      │
│  ┌──────────┐  ┌──────────┐                                │  │
│  │  Web App  │  │  API App  │                                │  │
│  │ :3000     │  │ :4000     │                                │  │
│  └──────────┘  └──────────┘                                │  │
└─────────────────────────────────────────────────────────────┘
```

## Docker Compose Configuration

```yaml
# docker/docker-compose.yml
version: "3.9"

name: voice-agent-dev

services:
  # ── PostgreSQL ──────────────────────────────────────────
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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - voice-agent-dev

  # ── Redis ───────────────────────────────────────────────
  redis:
    image: redis/redis-stack-server:7.2.0
    container_name: voice-agent-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - voice-agent-dev

  # ── Kafka ───────────────────────────────────────────────
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: voice-agent-kafka
    restart: unless-stopped
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_LOG_DIRS: /var/lib/kafka/data
      CLUSTER_ID: "voice-agent-dev-cluster"
    volumes:
      - kafka-data:/var/lib/kafka/data
    healthcheck:
      test: ["CMD", "kafka-topics", "--bootstrap-server", "localhost:9092", "--list"]
      interval: 15s
      timeout: 10s
      retries: 10
      start_period: 30s
    networks:
      - voice-agent-dev

  # ── Kafka Init (Topic Creation) ────────────────────────
  kafka-init:
    image: confluentinc/cp-kafka:7.6.0
    container_name: voice-agent-kafka-init
    restart: "no"
    depends_on:
      kafka:
        condition: service_healthy
    entrypoint: ["/bin/bash", "-c"]
    command: |
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic call-events --partitions 3 --replication-factor 1 && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic transcription-results --partitions 2 --replication-factor 1 && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic agent-events --partitions 1 --replication-factor 1 && \
      echo "Topics created successfully"
    networks:
      - voice-agent-dev

  # ── MinIO ──────────────────────────────────────────────
  minio:
    image: minio/minio:latest
    container_name: voice-agent-minio
    restart: unless-stopped
    ports:
      - "9000:9000"   # API
      - "9001:9001"   # Console
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - voice-agent-dev

  # ── MinIO Init (Bucket Creation) ──────────────────────
  minio-init:
    image: minio/mc:latest
    container_name: voice-agent-minio-init
    restart: "no"
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: ["/bin/sh", "-c"]
    command: |
      mc alias set local http://minio:9000 minioadmin minioadmin && \
      mc mb local/dev-recordings --ignore-existing && \
      mc mb local/dev-transcripts --ignore-existing && \
      mc mb local/dev-exports --ignore-existing && \
      mc policy set public local/dev-recordings && \
      echo "Buckets created successfully"
    networks:
      - voice-agent-dev

  # ── Mailpit ───────────────────────────────────────────
  mailpit:
    image: axllent/mailpit:latest
    container_name: voice-agent-mailpit
    restart: unless-stopped
    ports:
      - "1025:1025"   # SMTP
      - "8025:8025"   # Web UI
    networks:
      - voice-agent-dev

  # ── pgAdmin ───────────────────────────────────────────
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: voice-agent-pgadmin
    restart: unless-stopped
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@voiceagent.dev
      PGADMIN_DEFAULT_PASSWORD: admin
    volumes:
      - pgadmin-data:/var/lib/pgadmin
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - voice-agent-dev

volumes:
  postgres-data:
  redis-data:
  kafka-data:
  minio-data:
  pgadmin-data:

networks:
  voice-agent-dev:
    name: voice-agent-dev
    driver: bridge
```

## Environment Variable References

```yaml
# docker/.env (automatically loaded by Docker Compose)
COMPOSE_PROJECT_NAME=voice-agent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=voice_agent_dev
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

## Initialization Scripts

```sql
-- docker/init/postgres/01-extensions.sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create application database if not exists
SELECT 'CREATE DATABASE voice_agent_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'voice_agent_dev')\gexec

-- Create test database
SELECT 'CREATE DATABASE voice_agent_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'voice_agent_test')\gexec
```

## Usage

```bash
# Start all services
pnpm docker:up

# Start specific services
docker compose -f docker/docker-compose.yml up -d postgres redis

# View logs
pnpm docker:logs

# Stop all services
pnpm docker:down

# Rebuild and start
pnpm docker:rebuild

# Reset all data (destroys volumes)
docker compose -f docker/docker-compose.yml down -v
pnpm docker:up
```

## Service Ports Summary

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Caching, sessions, pub/sub |
| Kafka | 9092 | Event streaming |
| MinIO API | 9000 | S3-compatible storage |
| MinIO Console | 9001 | Storage management UI |
| Mailpit SMTP | 1025 | Email testing SMTP |
| Mailpit UI | 8025 | Email testing web UI |
| pgAdmin | 5050 | Database management UI |

## Design Decisions

### Why Docker Compose instead of installing services natively?

1. **Reproducibility**: Every developer gets identical service versions
2. **Isolation**: No conflicts with host-installed services
3. **Cleanup**: `docker compose down -v` completely resets the environment
4. **Documentation**: The Compose file serves as living documentation of required services
5. **CI integration**: Same Compose file can be used in CI for integration tests

### Why pgvector/pgvector image?

The standard PostgreSQL image doesn't include the `pgvector` extension needed for RAG embeddings. The `pgvector/pgvector` image bundles the extension.

### Kafka with KRaft (no Zookeeper)

The Confluent 7.6+ images support KRaft mode, eliminating the Zookeeper dependency. This simplifies the Compose file from 3 services (Zookeeper + Kafka + init) to 2 (Kafka + init).

## Integration Points

- **Application**: Apps connect via service names (Docker DNS) when running in containers, or via `localhost` when running on the host
- **Prisma**: Reads `DATABASE_URL` from environment
- **Voice/LLM clients**: Connect to provider APIs over the internet
- **MinIO client**: Uses S3-compatible SDK with local endpoint

## Production Considerations

1. **Resource allocation**: Docker Compose dev setup can use significant resources (2GB+ RAM). Configure resource limits in Docker Desktop settings
2. **Volume performance**: On macOS, Docker volumes mounted from the host filesystem can be slow. Use Docker volumes (managed by Docker) instead of bind mounts for database data
3. **Startup order**: The `depends_on` with `condition: service_healthy` ensures proper startup ordering. Without health checks, dependent services may fail because prerequisites aren't ready
4. **Port conflicts**: If host ports 5432, 6379, etc. are occupied, change the host port mapping: `"5433:5432"` maps host port 5433 to container port 5432
5. **Cleanup**: Running `docker compose down -v` destroys all data volumes. Educate developers about this destructive command
