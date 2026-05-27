# Section 08: Test Isolation & Parallel Execution

## Overview

Test isolation ensures that tests can run in any order, in parallel, without interfering with each other. For the voice AI platform, test isolation spans database state, cache state, authentication contexts, file system artifacts, and environment variables. Parallel execution maximizes CI efficiency by distributing tests across multiple workers, reducing feedback time.

The isolation strategy enforces that no test depends on state created by another test. Each test setup creates required data from scratch and teardown removes it. Database transactions provide automatic rollback, Redis databases are isolated, and file system operations use temporary directories.

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
// Test isolation configuration
// vitest.config.ts
export default defineConfig({
  test: {
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: false,
        isolate: true,
      },
    },
    sequence: {
      // Ensure tests don't depend on order
      shuffle: true,
      seed: Date.now(),
    },
  },
});

// Database isolation using transaction rollback
describe('Database Isolation', () => {
  let db: PrismaClient;
  
  beforeEach(async () => {
    db = await getTestDatabase();
    // Start transaction that will be rolled back
    await db.$executeRawUnsafe('BEGIN');
  });

  afterEach(async () => {
    // Rollback all changes made during test
    await db.$executeRawUnsafe('ROLLBACK');
  });

  it('creates data visible only within this test', async () => {
    await db.agent.create({ data: { name: 'Isolated Agent', /* ... */ } });
    const count = await db.agent.count();
    expect(count).toBe(1); // Other tests see 0
  });
});

// Parallel execution helper
// CI: vitest run --shard=${{ matrix.shard }}/${{ strategy.matrix.total-shards }}
// Matrix strategy:
// jobs:
//   test:
//     strategy:
//       matrix:
//         shard: [1, 2, 3, 4]
//     steps:
//       - run: npx vitest run --shard=${{ matrix.shard }}/4
```

## Integration Points

- **CI Matrix Strategy**: GitHub Actions matrix for parallel shard execution
- **Test Splitting**: Tests distributed across shards by file path
- **Container Reuse**: Testcontainers reused within a worker across test files
- **Shared Reference Data**: Reference data loaded once, not per test
- **Result Aggregation**: Coverage merged from parallel shards

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Worker Memory**: Each worker runs a database container; ensure CI has sufficient memory
- **Test Database Connections**: Each worker needs a database connection; tune connection pool
- **Flaky Tests in Parallel**: Some tests only fail in parallel; use --reporter=verbose for diagnosis
- **Resource Limits**: Set container CPU/memory limits to prevent resource starvation
- **Shard Balance**: Ensure even test distribution across shards for optimal parallelization
