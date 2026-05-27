# Section 03: Test Containers for Dependencies

## Overview

Testcontainers provides lightweight, disposable instances of infrastructure dependencies for integration tests. For the voice AI platform, Testcontainers manages PostgreSQL databases, Redis caches, and other service dependencies in Docker containers that are started before tests and torn down afterward. This approach ensures tests run against real versions of infrastructure, not mocked or in-memory substitutes.

Each test worker gets its own set of containers, ensuring complete isolation. Containers are configured to match production infrastructure versions as closely as possible. The Testcontainers lifecycle is managed through Vitest's global setup and teardown hooks, with health checks ensuring containers are ready before tests begin.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Simulator|--->| Utterance|--->| Flow     |--->| Debug    |--->| Report   |
| (in-     |    | Player   |    | Executor |    | Panel    |    | (pass/   |
|  browser)|    | (text/   |    | (step    |    | (log,    |    |  fail    |
|          |    |  audio)  |    |  thru)   |    |  state)  |    |  + trace)|
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **In-Browser Simulator**: Full conversation simulation with WASM runtime. No backend needed.
- **Utterance Testing**: Pre-defined test utterances with assertions on path and response.
- **Flow Validation**: Graph analysis for unreachable nodes, infinite loops, missing required fields.
## Implementation Approach

```typescript
// Testcontainers setup
import { PostgreSqlContainer, RedisContainer } from '@testcontainers/postgresql';
import { StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { StartedRedisContainer } from '@testcontainers/redis';

export interface TestContainers {
  postgres: StartedPostgreSqlContainer;
  redis: StartedRedisContainer;
  connectionString: string;
  redisUrl: string;
}

export async function startContainers(): Promise<TestContainers> {
  // Start PostgreSQL container
  const postgres = await new PostgreSqlContainer('postgres:15-alpine')
    .withDatabase('voice_agent_test')
    .withUsername('test')
    .withPassword('test')
    .withExposedPorts(5432)
    .start();

  // Start Redis container
  const redis = await new RedisContainer('redis:7-alpine')
    .withExposedPorts(6379)
    .start();

  // Run migrations
  const connectionString = postgres.getConnectionUri();
  await runMigrations(connectionString);

  return {
    postgres,
    redis,
    connectionString,
    redisUrl: `redis://${redis.getHost()}:${redis.getPort()}`,
  };
}

export async function stopContainers(containers: TestContainers): Promise<void> {
  await containers.redis.stop();
  await containers.postgres.stop();
}

// Vitest global setup
export async function setup() {
  const containers = await startContainers();
  process.env.DATABASE_URL = containers.connectionString;
  process.env.REDIS_URL = containers.redisUrl;
  process.env.TEST_CONTAINERS = 'true';
  (global as any).__CONTAINERS__ = containers;
}

export async function teardown() {
  await stopContainers((global as any).__CONTAINERS__);
}
```

## Integration Points

- **Global Setup**: Containers started in Vitest globalSetup hook
- **Environment Variables**: Connection details passed via environment variables
- **Migration Integration**: Database migrations run automatically after container starts
- **Worker Isolation**: If using multiple workers, each worker gets unique container
- **CI Integration**: Docker must be available in CI environment

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Docker Requirement**: CI environment must have Docker; consider Docker-in-Docker for containerized CI
- **Resource Limits**: Testcontainers consume memory/CPU; set resource limits on containers
- **Startup Time**: Container startup adds 10-30s to test initialization; reuse across suites
- **Image Caching**: Pre-pull container images in CI to speed up test execution
- **Port Conflicts**: Use random port mapping to avoid port conflicts between workers
