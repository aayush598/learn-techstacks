# Section 03: Integration Testing Strategy

## Overview

Integration testing validates that multiple components work together correctly. For our voice AI platform, integration tests cover API routes with database interactions, service-to-service communication, voice pipeline stage transitions, and third-party service integrations. Unlike unit tests, integration tests use real (or containerized) dependencies rather than mocks, providing higher confidence that the system works as a whole.

The integration testing strategy follows the "test one boundary at a time" principle: each test crosses exactly one real boundary (e.g., API + database) while mocking others (e.g., external APIs). This keeps tests focused, fast, and reliable while still providing meaningful coverage of integration points.

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
// Integration test for an API route
import { createTestContext, TestContext } from './helpers/test-context';
import { createCallRecord } from './factories/call-record.factory';

describe('POST /api/calls/:id/transcript', () => {
  let ctx: TestContext;

  beforeAll(async () => {
    ctx = await createTestContext();
  });

  afterAll(async () => {
    await ctx.teardown();
  });

  it('returns 200 and stores transcript for existing call', async () => {
    const call = await createCallRecord(ctx.db, { status: 'completed' });
    
    const response = await ctx.request
      .post(`/api/calls/${call.id}/transcript`)
      .send({ segments: [{ text: 'Hello', timestamp: 0 }] })
      .expect(200);

    expect(response.body.transcriptId).toBeDefined();
    
    const stored = await ctx.db.transcript.findUnique({
      where: { id: response.body.transcriptId }
    });
    expect(stored).not.toBeNull();
    expect(stored.segments).toHaveLength(1);
  });

  it('returns 404 for non-existent call', async () => {
    await ctx.request
      .post('/api/calls/00000000-0000-0000-0000-000000000000/transcript')
      .send({ segments: [] })
      .expect(404);
  });
});
```

## Integration Points

- **CI Pipeline**: Integration tests run on every PR, blocking merge on failure
- **Database Migrations**: Tests run against the latest schema via automatic migration
- **Service Dependencies**: External services (Twilio, OpenAI) are mocked; internal services are real
- **Coverage**: Integration tests aim for 70% coverage of API routes and service boundaries

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Test Database Cleanup**: Implement thorough cleanup between tests to prevent data leakage
- **Parallel Execution**: Use Vitest's pool feature to run integration tests in parallel with isolated databases
- **Resource Limits**: Testcontainers can be resource-intensive; set memory and CPU limits for containers
- **CI Optimization**: Cache Docker images for Testcontainers to speed up pipeline execution
- **Flaky Test Detection**: Track and alert on flaky integration tests with automatic re-run and quarantine
