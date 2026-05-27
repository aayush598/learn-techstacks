# Section 03: Mocking Strategies

## Overview

Mocking is essential for isolating the code under test from its dependencies. The voice AI platform uses a multi-layered mocking strategy: MSW (Mock Service Worker) for HTTP-level mocking of external APIs, Vitest's `vi.mock` for module-level mocking, and manual mock implementations for complex dependencies like database clients and AI service wrappers.

The mocking philosophy is "mock at the boundary": mock external dependencies that the system doesn't control, but use real implementations for internal modules whenever practical. This reduces maintenance burden and increases confidence in test outcomes. Mocks are centrally managed in the test setup but can be overridden per test for specific scenarios.

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
// MSW handler setup for external APIs
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.post('https://api.openai.com/v1/chat/completions', ({ request }) => {
    return HttpResponse.json({
      choices: [{ message: { content: 'Mock response', role: 'assistant' } }],
      usage: { total_tokens: 50 },
    });
  }),

  http.post('https://api.twilio.com/2010-04-01/Accounts/*/Calls.json', () => {
    return HttpResponse.json({
      sid: 'CA-mock-sid',
      status: 'queued',
      direction: 'outbound-api',
    });
  }),
);

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Module mocking
vi.mock('@/services/cache-service', () => ({
  CacheService: vi.fn().mockImplementation(() => ({
    get: vi.fn().mockResolvedValue(null),
    set: vi.fn().mockResolvedValue(true),
    del: vi.fn().mockResolvedValue(true),
  })),
}));

// Partial mock with spyOn
const logger = { info: vi.fn(), error: vi.fn(), warn: vi.fn() };
vi.spyOn(logger, 'error').mockImplementation((msg) => {
  // Custom behavior for error logging in tests
  console.error(`[TEST ERROR] ${msg}`);
});
```

## Integration Points

- **Setup Files**: MSW server and module mocks initialized in Vitest setup files
- **Test Factories**: Mock factory functions provided for each major dependency
- **Override Per Test**: Tests can override default mock behavior for specific cases
- **Unhandled Request Warning**: MSW warns on unhandled requests, catching unintended HTTP calls
- **Mock Reset**: All mocks reset between tests to prevent state leakage

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Mock Maintenance**: Update mocks when external API contracts change; monitor for drift
- **Mock Fidelity**: Overly permissive mocks hide integration issues; validate request structure
- **Mock Leakage**: Ensure mocks don't persist across test files; use setup/teardown correctly
- **Mock Performance**: MSW adds minimal overhead; but excessive module mocks slow test startup
- **Mock Documentation**: Document mock behavior and assumptions in mock factory modules
