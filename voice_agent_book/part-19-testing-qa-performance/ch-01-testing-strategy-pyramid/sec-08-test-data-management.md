# Section 08: Test Data Management

## Overview

Test data management encompasses the creation, isolation, and cleanup of data used during testing. For a multi-tenant voice AI platform, test data must be carefully managed to prevent cross-test contamination, ensure reproducibility, and maintain test suite reliability. The approach uses factory functions for entity creation, seeded baseline data for integration tests, and automated cleanup strategies for database state.

Test data factories generate realistic entities (agents, calls, users, transcripts) using Faker.js for random data and builder patterns for complex object graphs. Factories can create single entities or related entity graphs (e.g., a user with agents, calls, and billing records). The factory system supports overriding default values and generating specific states for edge case testing.

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
// Factory system for test data
import { faker } from '@faker-js/faker';

interface AgentConfig {
  name?: string;
  language?: string;
  voice?: string;
  status?: 'draft' | 'active' | 'paused';
  userId?: string;
  orgId?: string;
}

export function createAgentFactory(db: PrismaClient) {
  return {
    async create(overrides: AgentConfig = {}) {
      const config: AgentConfig = {
        name: faker.company.name() + ' Support Bot',
        language: 'en-US',
        voice: faker.helpers.arrayElement(['natural-female', 'natural-male', 'animated']),
        status: 'active',
        ...overrides,
      };

      return db.agent.create({
        data: {
          name: config.name,
          language: config.language,
          voice: config.voice,
          status: config.status,
          userId: config.userId || (await createUser(db)).id,
          orgId: config.orgId || (await createOrg(db)).id,
          config: {
            greeting: faker.helpers.arrayElement([
              'Hello, how can I help you?',
              'Welcome! What can I do for you today?',
            ]),
            temperature: 0.7,
            maxDuration: 300,
          },
        },
      });
    },

    async createWithCalls(count: number, overrides = {}) {
      const agent = await this.create(overrides);
      const calls = await Promise.all(
        Array.from({ length: count }, () => createCallFactory(db).create({ agentId: agent.id }))
      );
      return { agent, calls };
    },
  };
}
```

## Integration Points

- **Database Cleanup**: `afterEach` hooks delete created data or roll back transactions
- **Factory Registry**: Central registry of all factories for discoverability
- **Test Isolation**: Tests use `test.concurrent` only when guaranteed no shared state
- **Data Generators**: Specialized generators for audio fixtures, transcript content, phone numbers
- **Snapshot Data**: Factories support generating data for snapshot testing

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Data Volume**: Integration tests should not create excessive data; limit per-test entity creation
- **Factory Complexity**: Overly complex factories create brittle tests; keep them simple by default
- **Data Cleanup Failures**: Monitor for tests that leave behind data; enforce cleanup in CI
- **Seeded Randomness**: Reproducible failures require deterministic seeds; log the seed on failure
- **Factory Versioning**: When schema changes, update factories immediately to prevent test failures
