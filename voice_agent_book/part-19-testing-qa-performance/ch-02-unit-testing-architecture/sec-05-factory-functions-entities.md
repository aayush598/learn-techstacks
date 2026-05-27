# Section 05: Factory Functions for Entities

## Overview

Factory functions provide a consistent, maintainable way to create test entities across the test suite. For the voice AI platform, factories exist for all major domain entities: users, organizations, agents, calls, transcripts, billing records, and configurations. Factories use sensible defaults for all fields, allowing tests to specify only the fields relevant to the scenario being tested.

The factory system supports creating single entities, related entity graphs (user with agents and calls), and specific states (e.g., a failed call, a paused agent). Factories are integrated with the Prisma ORM for database persistence and can also create in-memory objects for unit tests that don't need database access.

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
// Agent factory with builder pattern
export class AgentFactory {
  private data: Partial<AgentCreateInput> = {};

  withName(name: string) {
    this.data.name = name;
    return this;
  }

  withLanguage(language: string) {
    this.data.language = language;
    return this;
  }

  withVoice(voice: string) {
    this.data.voice = voice;
    return this;
  }

  withStatus(status: AgentStatus) {
    this.data.status = status;
    return this;
  }

  withCustomConfig(config: Record<string, unknown>) {
    this.data.config = config as any;
    return this;
  }

  async build(db: PrismaClient): Promise<Agent> {
    return db.agent.create({
      data: {
        name: this.data.name ?? faker.company.name() + ' Bot',
        language: this.data.language ?? 'en-US',
        voice: this.data.voice ?? faker.helpers.arrayElement(['male', 'female']),
        status: this.data.status ?? 'active',
        config: this.data.config ?? { greeting: 'Hello!', temperature: 0.7 },
        organization: { connect: { id: this.data.organizationId ?? (await createOrg(db)).id } },
      },
    });
  }

  async buildMany(db: PrismaClient, count: number): Promise<Agent[]> {
    return Promise.all(Array.from({ length: count }, () => this.build(db)));
  }
}

// Usage in tests
const agent = await new AgentFactory()
  .withName('Support Bot')
  .withLanguage('es-ES')
  .withStatus('active')
  .build(db);
```

## Integration Points

- **Test Context**: Factories consume database client from test context
- **Data Cleanup**: Factories integrate with cleanup strategies (transaction rollback)
- **Fixture Loading**: Static fixtures supplement factories for reference data
- **Seeding**: Factories used in seed scripts for development and test databases
- **Mock Data**: In-memory factory variant for unit tests without database

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Factory Maintenance**: Update factories immediately when schema changes
- **Factory Bloat**: Keep factories focused on entity creation; avoid adding test logic
- **Default Values**: Review defaults periodically to ensure they reflect current domain understanding
- **Performance**: Factory entity creation can be slow; use `createMany` for batch operations
- **Relationship Depth**: Avoid deeply nested entity graphs in default factories; use explicit builders
