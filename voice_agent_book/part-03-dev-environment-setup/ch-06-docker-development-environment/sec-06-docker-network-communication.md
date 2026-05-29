# Section 06: Docker Network & Communication

## Overview

Docker networking enables containers to communicate with each other and with the host machine. Proper network configuration ensures that the voice agent platform's services can discover and connect to each other reliably, regardless of whether the application runs inside a container or directly on the host.

## Network Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Docker Network Architecture                      │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Network: voice-agent-dev (bridge)                    │    │
│  │                                                       │    │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐       │    │
│  │  │ postgres  │    │  redis   │    │  kafka   │       │    │
│  │  │ :5432     │    │ :6379    │    │ :9092    │       │    │
│  │  └──────────┘    └──────────┘    └──────────┘       │    │
│  │       │               │               │              │    │
│  │  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐         │    │
│  │  │  minio   │    │ mailpit │    │ pgadmin │         │    │
│  │  │ :9000    │    │ :8025   │    │ :5050   │         │    │
│  │  │ :9001    │    │ :1025   │    │          │         │    │
│  │  └──────────┘    └──────────┘    └──────────┘       │    │
│  │                                                       │    │
│  │  Application containers (when running in Docker):     │    │
│  │  ┌──────────┐    ┌──────────┐                        │    │
│  │  │   web     │    │   api    │                        │    │
│  │  │ :3000     │    │ :4000    │                        │    │
│  │  └──────────┘    └──────────┘                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Host machine access:                                        │
│  localhost:3000  → web:3000                                  │
│  localhost:4000  → api:4000                                  │
│  localhost:5432  → postgres:5432                             │
│  localhost:6379  → redis:6379                                │
└─────────────────────────────────────────────────────────────┘
```

## Network Configuration

```yaml
# docker/docker-compose.yml
networks:
  voice-agent-dev:
    name: voice-agent-dev
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

All services join this network implicitly via `networks: - voice-agent-dev`. They can reach each other using the service name as the hostname.

## Service Discovery

Docker Compose provides built-in DNS resolution using service names:

```bash
# Inside the web container, connect to PostgreSQL:
ping postgres          # Resolves to 172.20.x.x
curl http://minio:9000 # Resolves to MinIO container
```

### Connection Strings for Docker Networking

```yaml
# docker/.env (used when app runs inside Docker)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/voice_agent_dev
REDIS_URL=redis://redis:6379
KAFKA_BROKERS=kafka:9092
MINIO_ENDPOINT=minio
MINIO_PORT=9000
```

### Connection Strings for Host Networking

```yaml
# .env.development (used when app runs on host)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/voice_agent_dev
REDIS_URL=redis://localhost:6379
KAFKA_BROKERS=localhost:9092
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
```

## Port Mapping

```yaml
services:
  postgres:
    ports:
      - "5432:5432"   # Host:Container
  redis:
    ports:
      - "6379:6379"
  kafka:
    ports:
      - "9092:9092"
  minio:
    ports:
      - "9000:9000"   # API
      - "9001:9001"   # Console
```

Port mappings are only needed for host access. Containers on the same network communicate directly without port mapping.

## Health Checks for Startup Order

Proper service startup ordering prevents race conditions where an application tries to connect before its dependencies are ready:

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_healthy
```

### Init Containers for Setup

```yaml
services:
  kafka-init:
    image: confluentinc/cp-kafka:7.6.0
    depends_on:
      kafka:
        condition: service_healthy
    restart: "no"
    entrypoint: ["/bin/bash", "-c"]
    command: |
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic call-events --partitions 3 --replication-factor 1 && \
      echo "Topics created"
    networks:
      - voice-agent-dev
```

## Application-Level Retry Logic

Even with health checks, the application should implement retry logic for service connections:

```typescript
// packages/db/src/connect.ts
import { prisma } from "./client";

const MAX_RETRIES = 10;
const RETRY_DELAY_MS = 2000;

export async function connectWithRetry(): Promise<void> {
  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      await prisma.$connect();
      console.log("Connected to PostgreSQL");
      return;
    } catch (error) {
      if (attempt === MAX_RETRIES) {
        throw new Error(
          `Failed to connect to PostgreSQL after ${MAX_RETRIES} attempts`
        );
      }
      console.log(
        `PostgreSQL connection attempt ${attempt}/${MAX_RETRIES} failed, retrying...`
      );
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS));
    }
  }
}
```

## Network Security

```yaml
services:
  # Internal services (no host access)
  postgres:
    expose:
      - "5432"
    # No ports: mapping — only accessible within the Docker network
    networks:
      - voice-agent-dev

  # External services (host access needed)
  pgadmin:
    ports:
      - "5050:80"
    networks:
      - voice-agent-dev
```

For internal services that don't need host access (in production-like setups), omit the `ports` mapping entirely.

## Multi-Network Setup

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
  database:
    driver: bridge

services:
  web:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend
      - database

  postgres:
    networks:
      - database
```

This isolates network access — the web app can't directly access the database, only the API can.

## Troubleshooting Network Issues

```bash
# Check container network
docker inspect voice-agent-web | jq '.[].NetworkSettings.Networks'

# Ping a service from within a container
docker exec voice-agent-web ping postgres

# Check DNS resolution
docker exec voice-agent-web nslookup redis

# Follow network traffic
docker exec voice-agent-web tcpdump -i eth0

# Check open connections
docker exec voice-agent-web ss -tln

# Verify port mapping
docker port voice-agent-postgres 5432
```

## Design Decisions

### Bridge network vs. host network

**Decision**: Use bridge networks (the default).

**Rationale**: Bridge networks provide automatic DNS resolution, container isolation, and port mapping. Host networking would expose all container ports on the host, increasing the attack surface and potentially causing port conflicts.

### Why a single shared network vs. per-service networks?

For development simplicity, a single network is sufficient. In production with Docker Swarm or Kubernetes, network isolation between services provides better security.

## Integration Points

- **Application config**: Service hostnames are configured via environment variables
- **Docker DNS**: Built-in service discovery
- **Health checks**: Ensure ordered startup
- **Retry logic**: Application-level resilience

## Production Considerations

1. **DNS caching**: Docker DNS doesn't cache aggressively. In Kubernetes, use headless services or a service mesh for DNS-based discovery
2. **Network latency**: Bridge networks add minimal latency. For high-throughput services (Kafka), use host networking or dedicated network interfaces
3. **Network policies**: In orchestrated environments (Kubernetes), define NetworkPolicy resources to restrict inter-service communication
4. **Encryption**: For production, all inter-service communication should be encrypted. Use TLS for PostgreSQL, Redis (with TLS mode), and Kafka (with SSL)
5. **Service mesh**: For microservice architectures, consider a service mesh (Istio, Linkerd) for advanced traffic management, observability, and mTLS
