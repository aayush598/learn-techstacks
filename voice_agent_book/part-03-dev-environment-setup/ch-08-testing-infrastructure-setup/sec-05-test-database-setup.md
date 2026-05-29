# Section 05: Test Database Setup

## Overview

Integration tests require a real database to verify query behavior, constraints, and transactions. Testcontainers provides lightweight, disposable database instances that are automatically created and destroyed for each test run, ensuring test isolation and reproducibility.

## Testcontainers Setup

```typescript
// packages/db/vitest.global-setup.ts
import { PostgreSqlContainer } from "@testcontainers/postgresql";
import type { StartedPostgreSqlContainer } from "@testcontainers/postgresql";
import { execSync } from "child_process";

let container: StartedPostgreSqlContainer;

export async function setup() {
  console.log("Starting PostgreSQL test container...");

  container = await new PostgreSqlContainer("pgvector/pgvector:pg16")
    .withDatabase("voice_agent_test")
    .withUsername("postgres")
    .withPassword("postgres")
    .withExposedPorts(5432)
    .withReuse(true) // Reuse container for faster test startup
    .start();

  const connectionString = `postgresql://postgres:postgres@${container.getHost()}:${container.getMappedPort(5432)}/voice_agent_test`;

  // Set environment variable for tests
  process.env.DATABASE_URL = connectionString;

  // Run migrations
  console.log("Running database migrations...");
  execSync("pnpm --filter @voice-agent/db run db:migrate:prod", {
    env: { ...process.env, DATABASE_URL: connectionString },
    stdio: "inherit",
  });

  console.log(`Test database ready at ${connectionString}`);
}

export async function teardown() {
  if (container) {
    console.log("Stopping PostgreSQL test container...");
    await container.stop();
  }
}
```

## Per-Test Database Cleanup

```typescript
// packages/db/src/test-setup.ts
import { PrismaClient } from "@prisma/client";
import { execSync } from "child_process";

const prisma = new PrismaClient();

export async function resetDatabase(): Promise<void> {
  // Method 1: Truncate all tables (fast)
  const tablenames = await prisma.$queryRaw<
    Array<{ tablename: string }>
  >`SELECT tablename FROM pg_tables WHERE schemaname='public'`;

  const tables = tablenames
    .map(({ tablename }) => `"public"."${tablename}"`)
    .join(", ");

  try {
    await prisma.$executeRawUnsafe(`TRUNCATE TABLE ${tables} CASCADE;`);
  } catch (error) {
    // Fallback: reset via migration
    execSync("pnpm db:reset --force", {
      env: { ...process.env },
      stdio: "inherit",
    });
  }
}

export async function createTestOrganization() {
  return prisma.organization.create({
    data: {
      name: "Test Corp",
      slug: `test-${Date.now()}`,
      plan: "professional",
    },
  });
}

export async function createTestAgent(organizationId: string) {
  return prisma.agent.create({
    data: {
      organizationId,
      name: "Test Agent",
      voiceProvider: "elevenlabs",
      voiceId: "test-voice-id",
      greetingMessage: "Hello!",
      llmProvider: "openai",
      llmModel: "gpt-4",
      status: "active",
    },
  });
}
```

## Transaction Rollback Strategy

```typescript
// packages/db/src/test-transaction.ts
import { PrismaClient } from "@prisma/client";

// Use a test transaction that can be rolled back
export function createTestTransaction() {
  const prisma = new PrismaClient();

  return {
    async begin<T>(fn: (tx: typeof prisma) => Promise<T>): Promise<T> {
      // Prisma doesn't support nested transactions easily,
      // so we use a simple wrapper
      return prisma.$transaction(async (tx) => {
        return fn(tx as unknown as typeof prisma);
      });
    },
    async disconnect() {
      await prisma.$disconnect();
    },
  };
}
```

## Using Testcontainers in Tests

```typescript
// packages/db/src/repositories/__tests__/agent.repo.integration.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { PostgreSqlContainer } from "@testcontainers/postgresql";
import type { StartedPostgreSqlContainer } from "@testcontainers/postgresql";
import { PrismaClient } from "@prisma/client";
import { AgentRepository } from "../agent.repo";
import { execSync } from "child_process";

describe("AgentRepository (integration)", () => {
  let container: StartedPostgreSqlContainer;
  let prisma: PrismaClient;
  let repo: AgentRepository;
  let orgId: string;

  beforeAll(async () => {
    // Start PostgreSQL container
    container = await new PostgreSqlContainer("pgvector/pgvector:pg16")
      .withDatabase("test")
      .start();

    const url = `postgresql://postgres:postgres@${container.getHost()}:${container.getMappedPort(5432)}/test`;

    // Run migrations
    execSync("pnpm db:migrate:prod", {
      env: { ...process.env, DATABASE_URL: url },
    });

    // Create client
    process.env.DATABASE_URL = url;
    prisma = new PrismaClient({ datasources: { db: { url } } });
    repo = new AgentRepository();
  });

  afterAll(async () => {
    await prisma.$disconnect();
    await container.stop();
  });

  beforeEach(async () => {
    // Clean database
    await prisma.organization.deleteMany();

    // Create test organization
    const org = await prisma.organization.create({
      data: { name: "Test Org", slug: `test-${Date.now()}` },
    });
    orgId = org.id;
  });

  it("should create an agent", async () => {
    const agent = await repo.create(orgId, {
      name: "Test Agent",
      voiceProvider: "elevenlabs",
      voiceId: "test-voice",
      greetingMessage: "Hello!",
      llmProvider: "openai",
      llmModel: "gpt-4",
      status: "draft",
    });

    expect(agent).toBeDefined();
    expect(agent.name).toBe("Test Agent");
    expect(agent.status).toBe("draft");
  });

  it("should find an agent by ID", async () => {
    const created = await repo.create(orgId, {
      name: "Test Agent",
      voiceProvider: "elevenlabs",
      voiceId: "test-voice",
      greetingMessage: "Hello!",
      llmProvider: "openai",
      llmModel: "gpt-4",
      status: "active",
    });

    const found = await repo.findById(created.id, orgId);
    expect(found).toBeDefined();
    expect(found!.id).toBe(created.id);
  });

  it("should return null for non-existent agent", async () => {
    const result = await repo.findById("non-existent", orgId);
    expect(result).toBeNull();
  });

  it("should update an agent", async () => {
    const created = await repo.create(orgId, {
      name: "Test Agent",
      voiceProvider: "elevenlabs",
      voiceId: "test-voice",
      greetingMessage: "Hello!",
      llmProvider: "openai",
      llmModel: "gpt-4",
      status: "draft",
    });

    const updated = await repo.update(created.id, orgId, {
      name: "Updated Agent",
      status: "active",
    });

    expect(updated.name).toBe("Updated Agent");
    expect(updated.status).toBe("active");
  });

  it("should paginate results", async () => {
    // Create multiple agents
    for (let i = 0; i < 15; i++) {
      await repo.create(orgId, {
        name: `Agent ${i}`,
        voiceProvider: "elevenlabs",
        voiceId: "test-voice",
        greetingMessage: "Hello!",
        llmProvider: "openai",
        llmModel: "gpt-4",
        status: "active",
      });
    }

    const page1 = await repo.findMany(orgId, { page: 1, pageSize: 10 });
    expect(page1.agents).toHaveLength(10);
    expect(page1.total).toBe(15);
    expect(page1.totalPages).toBe(2);

    const page2 = await repo.findMany(orgId, { page: 2, pageSize: 10 });
    expect(page2.agents).toHaveLength(5);
  });
});
```

## Redis Testcontainers

```typescript
// packages/voice/src/cache/__tests__/redis-integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { GenericContainer } from "testcontainers";
import type { StartedTestContainer } from "testcontainers";
import Redis from "ioredis";

describe("Redis Integration", () => {
  let container: StartedTestContainer;
  let redis: Redis;

  beforeAll(async () => {
    container = await new GenericContainer("redis/redis-stack-server:7.2.0")
      .withExposedPorts(6379)
      .start();

    redis = new Redis({
      host: container.getHost(),
      port: container.getMappedPort(6379),
    });
  });

  afterAll(async () => {
    await redis.quit();
    await container.stop();
  });

  it("should set and get a value", async () => {
    await redis.set("test-key", "test-value");
    const value = await redis.get("test-key");
    expect(value).toBe("test-value");
  });

  it("should respect TTL", async () => {
    await redis.setex("expiring-key", 1, "value");
    const beforeExpiry = await redis.get("expiring-key");
    expect(beforeExpiry).toBe("value");

    await new Promise((resolve) => setTimeout(resolve, 1500));
    const afterExpiry = await redis.get("expiring-key");
    expect(afterExpiry).toBeNull();
  });
});
```

## Docker Compose Alternative

For CI environments where Testcontainers adds overhead, use the existing Docker Compose services:

```yaml
# docker/docker-compose.test.yml
version: "3.9"
name: voice-agent-test

services:
  postgres-test:
    image: pgvector/pgvector:pg16
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: voice_agent_test
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## Design Decisions

### Testcontainers vs. Docker Compose vs. In-memory SQLite

| Approach | Isolation | Realism | Speed | Setup Complexity |
|----------|-----------|---------|-------|------------------|
| Testcontainers | Full | High | Medium | Low |
| Docker Compose | Shared | High | Fast | Low |
| SQLite in-memory | Full | Low | Fast | None |

**Decision**: Use Testcontainers for integration tests that need a real PostgreSQL with pgvector. Use Docker Compose for CI where container orchestration is simpler. Never use SQLite for testing PostgreSQL-specific features (pgvector, JSONB, array types).

### Why not transaction rollback for isolation?

Prisma doesn't support nested transactions natively (it uses Prisma's own transaction API, not database savepoints). Truncating tables between tests is simple and reliable. For very large test suites, consider database snapshot/restore for faster cleanup.

## Integration Points

- **Vitest global setup**: Starts Testcontainers before all tests
- **Repository tests**: Use real database instances
- **CI**: Testcontainers or Docker Compose for integration test databases
- **Prisma migrations**: Applied automatically during test setup

## Production Considerations

1. **Resource usage**: Testcontainers consume memory. Set `withReuse(true)` to keep the container alive between test runs. Add `container.stop()` in `afterAll` hooks
2. **Parallelism**: Each test worker needs its own database. Use unique database names per worker: `voice_agent_test_${workerId}`
3. **Migration speed**: Running `prisma migrate deploy` on every test run is slow. Consider using `prisma db push` for test setups (no migration history needed)
4. **Cleanup**: Always clean up test data. Use `beforeEach` hooks to reset state. Failing to clean up leads to order-dependent test failures
5. **CI caching**: In CI, cache the Docker image used by Testcontainers to avoid downloading on every run
