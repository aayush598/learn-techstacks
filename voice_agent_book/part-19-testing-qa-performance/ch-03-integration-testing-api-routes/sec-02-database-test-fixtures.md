# Section 02: Database Test Fixtures

## Overview

Database test fixtures provide reliable, repeatable data for integration tests. The voice AI platform uses a combination of static seed data (reference information like roles, plans, and templates) and dynamic factory-generated data (test-specific entities like users, agents, calls). Fixtures are loaded before test suites and cleaned up afterward, ensuring each test starts with known database state.

The fixture system supports loading specific data sets per test suite, creating entities on-the-fly for test-specific scenarios, and managing complex entity relationships. Fixtures are designed to be composable: a test suite for agent management loads agent-related fixtures, while a billing test suite loads customer and subscription fixtures.

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
// Fixture management system
export class DatabaseFixture {
  private loaded: Set<string> = new Set();

  constructor(private db: PrismaClient) {}

  async loadReferenceData() {
    if (this.loaded.has('reference')) return;
    
    await this.db.role.createMany({
      data: referenceData.roles,
      skipDuplicates: true,
    });
    await this.db.plan.createMany({
      data: referenceData.plans,
      skipDuplicates: true,
    });
    this.loaded.add('reference');
  }

  async loadAgentsFixtures() {
    await this.loadReferenceData();
    
    // Create test organization with owner
    const org = await this.db.organization.create({
      data: {
        name: 'Test Org',
        slug: 'test-org',
        owner: {
          create: { email: 'owner@test.com', name: 'Test Owner' },
        },
      },
      include: { owner: true },
    });
    
    // Create sample agents
    const agents = await Promise.all([
      this.db.agent.create({
        data: {
          name: 'Sales Agent',
          language: 'en-US',
          voice: 'natural-female',
          status: 'active',
          organizationId: org.id,
        },
      }),
      this.db.agent.create({
        data: {
          name: 'Support Agent',
          language: 'en-US',
          voice: 'natural-male',
          status: 'draft',
          organizationId: org.id,
        },
      }),
    ]);

    return { org, agents };
  }

  async cleanup() {
    // Delete in reverse dependency order
    await this.db.transcript.deleteMany();
    await this.db.call.deleteMany();
    await this.db.agent.deleteMany();
    await this.db.organization.deleteMany();
    this.loaded.clear();
  }
}
```

## Integration Points

- **Factory Integration**: Factories use the same database client for entity creation
- **Migration System**: Fixtures are loaded after migrations are applied
- **Seed Data Versioning**: Static fixtures version-controlled alongside schema changes
- **Test Context**: Fixtures accessible through test context object
- **Parallel Safety**: Fixture loading uses advisory locks for parallel test safety

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Fixture Data Volume**: Keep fixture data minimal; large fixtures slow tests
- **Fixture Maintenance**: Update fixtures when schema changes; out-of-date fixtures cause confusing failures
- **Data Consistency**: Ensure fixture data respects referential integrity constraints
- **Fixture Drift**: Regularly review fixtures against production data patterns
- **Loading Time**: Cache fixture data where possible; avoid reloading reference data between suites
