# Section 07: Service Health & Monitoring

## Overview

Service health monitoring ensures that all local development services are running correctly and provides visibility into their status. Health check endpoints, a status dashboard, restart policies, and log aggregation help developers quickly identify and resolve service issues.

## Health Check Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Service Health Monitoring                        │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ PostgreSQL│    │  Redis    │    │  Kafka    │              │
│  │ Health: ✓  │    │ Health: ✓  │    │ Health: ✓  │              │
│  │ Queries:   │    │ Memory:   │    │ Lag: 0    │              │
│  │  12/s     │    │  45%     │    │ Topics: 4 │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  MinIO    │    │ Mailpit   │    │  pgAdmin  │              │
│  │ Health: ✓  │    │ Health: ✓  │    │ Health: ✓  │              │
│  │ Objects:   │    │ Emails:   │    │ Uptime:   │              │
│  │  42       │    │  0        │    │  5h       │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Health API: /api/health                              │   │
│  │  Returns JSON with all service statuses               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Docker Compose Health Checks

```yaml
# docker/docker-compose.yml (health checks for all services)
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 5s

  kafka:
    healthcheck:
      test: ["CMD", "kafka-topics", "--bootstrap-server", "localhost:9092", "--list"]
      interval: 15s
      timeout: 10s
      retries: 10
      start_period: 30s

  minio:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  mailpit:
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8025/health"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Application Health Endpoint

```typescript
// apps/api/src/app/api/health/route.ts
import { NextResponse } from "next/server";
import { prisma } from "@voice-agent/db/client";
import { redis } from "@voice-agent/voice/cache/redis-client";
import { getKafka } from "@voice-agent/voice/events/kafka-client";
import { getS3Client } from "@voice-agent/voice/storage/s3-client";
import { ListBucketsCommand } from "@aws-sdk/client-s3";

interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy";
  version: string;
  uptime: number;
  timestamp: string;
  services: {
    database: ServiceHealth;
    redis: ServiceHealth;
    kafka: ServiceHealth;
    storage: ServiceHealth;
  };
}

interface ServiceHealth {
  status: "healthy" | "degraded" | "unhealthy";
  latency: number;
  error?: string;
}

export async function GET() {
  const health: HealthStatus = {
    status: "healthy",
    version: process.env.NEXT_PUBLIC_APP_VERSION ?? "dev",
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    services: {
      database: await checkDatabase(),
      redis: await checkRedis(),
      kafka: await checkKafka(),
      storage: await checkStorage(),
    },
  };

  // Overall status is degraded if any service is degraded
  const serviceStatuses = Object.values(health.services);
  if (serviceStatuses.some((s) => s.status === "unhealthy")) {
    health.status = "unhealthy";
  } else if (serviceStatuses.some((s) => s.status === "degraded")) {
    health.status = "degraded";
  }

  const statusCode = health.status === "healthy" ? 200 : health.status === "degraded" ? 200 : 503;

  return NextResponse.json(health, { status: statusCode });
}

async function checkDatabase(): Promise<ServiceHealth> {
  const start = Date.now();
  try {
    await prisma.$queryRaw`SELECT 1`;
    return { status: "healthy", latency: Date.now() - start };
  } catch (error) {
    return {
      status: "unhealthy",
      latency: Date.now() - start,
      error: (error as Error).message,
    };
  }
}

async function checkRedis(): Promise<ServiceHealth> {
  const start = Date.now();
  try {
    const pong = await redis.ping();
    if (pong !== "PONG") {
      return { status: "degraded", latency: Date.now() - start };
    }
    return { status: "healthy", latency: Date.now() - start };
  } catch (error) {
    return {
      status: "unhealthy",
      latency: Date.now() - start,
      error: (error as Error).message,
    };
  }
}

async function checkKafka(): Promise<ServiceHealth> {
  const start = Date.now();
  try {
    const kafka = getKafka();
    const admin = kafka.admin();
    await admin.connect();
    const topics = await admin.listTopics();
    await admin.disconnect();

    if (topics.length === 0) {
      return { status: "degraded", latency: Date.now() - start };
    }
    return { status: "healthy", latency: Date.now() - start };
  } catch (error) {
    return {
      status: "unhealthy",
      latency: Date.now() - start,
      error: (error as Error).message,
    };
  }
}

async function checkStorage(): Promise<ServiceHealth> {
  const start = Date.now();
  try {
    const s3 = getS3Client();
    await s3.send(new ListBucketsCommand({}));
    return { status: "healthy", latency: Date.now() - start };
  } catch (error) {
    return {
      status: "unhealthy",
      latency: Date.now() - start,
      error: (error as Error).message,
    };
  }
}
```

## Status Dashboard

```typescript
// apps/web/src/app/status/page.tsx
"use client";

import { useEffect, useState } from "react";

interface HealthData {
  status: string;
  version: string;
  uptime: number;
  services: Record<string, { status: string; latency: number; error?: string }>;
}

export default function StatusPage() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch("/api/health");
        const data = await response.json();
        setHealth(data);
      } catch (error) {
        setHealth(null);
      } finally {
        setLoading(false);
      }
    }

    fetchHealth();
    const interval = setInterval(fetchHealth, 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading status...</div>;
  if (!health) return <div>Failed to fetch health status</div>;

  const statusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-green-500";
      case "degraded":
        return "bg-yellow-500";
      default:
        return "bg-red-500";
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Service Status</h1>

      <div className={`inline-flex items-center px-3 py-1 rounded-full text-white ${statusColor(health.status)}`}>
        {health.status.toUpperCase()}
      </div>

      <div className="mt-6 grid gap-4">
        {Object.entries(health.services).map(([name, service]) => (
          <div key={name} className="border rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${statusColor(service.status)}`} />
                <span className="font-medium capitalize">{name}</span>
              </div>
              <span className="text-sm text-gray-500">
                {service.latency}ms
              </span>
            </div>
            {service.error && (
              <p className="mt-2 text-sm text-red-600">{service.error}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Restart Policies

```yaml
# docker/docker-compose.yml (restart policies)
services:
  postgres:
    restart: unless-stopped
    # Restart unless explicitly stopped by the user

  redis:
    restart: unless-stopped

  kafka:
    restart: unless-stopped
    # Kafka has start_period: 30s — give it time to initialize

  minio:
    restart: unless-stopped
```

## Log Aggregation

```bash
#!/bin/bash
# scripts/aggregate-logs.sh
# Aggregate logs from all Docker services

SERVICES="postgres redis kafka minio mailpit pgadmin"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="./logs/${TIMESTAMP}"

mkdir -p "$LOG_DIR"

for service in $SERVICES; do
  echo "Fetching logs for $service..."
  docker compose -f docker/docker-compose.yml logs --tail=100 "$service" > "${LOG_DIR}/${service}.log"
done

echo "Logs saved to ${LOG_DIR}"

# Check for errors across all logs
echo ""
echo "=== Error Summary ==="
grep -i "error\|failed\|exception\|timeout" "${LOG_DIR}"/*.log || echo "No errors found"
```

## Monitoring Commands

```bash
# Check all service statuses
docker compose -f docker/docker-compose.yml ps

# View logs for a specific service
docker compose logs -f postgres

# Check container resource usage
docker stats voice-agent-postgres voice-agent-redis voice-agent-kafka

# Check health status explicitly
docker inspect --format='{{json .State.Health}}' voice-agent-postgres | jq

# Follow Kafka consumer lag
docker exec voice-agent-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group call-processor \
  --describe

# Monitor Redis memory
docker exec voice-agent-redis redis-cli INFO memory | grep used_memory_human

# Check PostgreSQL connections
docker exec voice-agent-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Verify MinIO buckets
docker exec voice-agent-minio-init mc ls local/
```

## Design Decisions

### Liveness vs. Readiness probes

**Decision**: Use combined health checks that verify both liveness and readiness.

**Rationale**: For development, a single health check that verifies the process is alive AND ready to serve requests is sufficient. In Kubernetes, separate liveness (is the process alive?) and readiness (is it ready to serve?) probes provide better lifecycle management.

### Why include error messages in health response?

Error messages in the health response help developers quickly diagnose issues without checking container logs. The error is displayed in the status dashboard, reducing debugging time.

## Integration Points

- **Docker health checks**: Container-level health verification
- **Next.js API route**: `/api/health` endpoint
- **Status dashboard**: Web UI for visual health monitoring
- **CI/CD**: Health checks determine deployment readiness
- **Kubernetes**: Liveness and readiness probes (production)

## Production Considerations

1. **Health endpoint security**: In production, the health endpoint should be internal-only or behind authentication
2. **Detailed vs. summary health**: Production health checks should return summary status (healthy/unhealthy) without exposing internal details. A separate `/api/health/detailed` endpoint can provide more information for debugging
3. **Alerting**: In production, health check failures should trigger alerts via PagerDuty, Slack, or email. The health endpoint should be polled by an external monitoring service (Pingdom, Datadog, etc.)
4. **Dependency health cascading**: If the database is unhealthy, dependent services (Kafka consumer that writes to DB) should be reported as degraded, not unhealthy
5. **Performance impact**: Health checks should be lightweight. Avoid expensive queries or operations. Cache results for short periods (e.g., 10 seconds)
