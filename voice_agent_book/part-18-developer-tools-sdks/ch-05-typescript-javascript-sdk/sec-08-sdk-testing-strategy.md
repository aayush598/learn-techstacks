# Section 08: SDK Testing Strategy

## Overview

The SDK testing strategy covers unit tests (module-level), integration tests (against sandbox API), end-to-end tests (real API flows), and snapshot tests (type and response consistency). Tests run in both browser and Node.js environments, and the CI pipeline gates releases on all test suites passing.

## Architecture

```
Testing Pyramid
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

         ┌──────────────────────────────────────┐
         │     E2E Tests (few)                  │
         │  Real API → Real response            │
         │  Critical user flows                 │
         │  Cost: slow, external dep            │
         ├──────────────────────────────────────┤
         │  Integration Tests (some)            │
         │  Mock HTTP → Integration             │
         │  Resource client behavior            │
         │  Cost: moderate                      │
         ├──────────────────────────────────────┤
         │  Unit Tests (many)                   │
         │  Pure functions → Fast               │
         │  Error handling, parsing, utils      │
         │  Cost: very fast                     │
         └──────────────────────────────────────┘

Test Types:
  Unit Tests:
    - Error class construction and methods
    - Backoff calculator math
    - URL construction
    - Response parsing
    - Type guard functions

  Integration Tests:
    - Resource client (mock HTTP)
    - Retry logic (mock failures)
    - Authentication flow
    - Pagination iteration

  E2E Tests:
    - Full create → read → update → delete flow
    - File upload → download
    - WebSocket connect → subscribe → receive
    - Webhook sign → verify

  Snapshot Tests:
    - Generated types match expected shape
    - Error responses match expected format
```

## Design Decisions

- **Mock HTTP Responses**: Integration tests mock the HTTP layer with MSW (Mock Service Worker) — fast, deterministic
- **Sandbox E2E**: E2E tests run against sandbox environment with dedicated test API keys
- **CI Test Splitting**: Unit + integration run on every PR; E2E runs on merge to main
- **Snapshot Testing for Types**: Ensure generated types don't break accidentally

## Implementation Approach

```typescript
// Unit test example — Vitest
import { describe, it, expect } from 'vitest';
import { BackoffCalculator, RetryHandler } from '../src/utils/retry';

describe('BackoffCalculator', () => {
  const calculator = new BackoffCalculator({
    baseDelayMs: 1000,
    maxDelayMs: 30_000,
    jitterMs: 0, // Disable jitter for deterministic tests
  });

  it('should calculate exponential backoff', () => {
    expect(calculator.getDelay(1)).toBe(1000);
    expect(calculator.getDelay(2)).toBe(2000);
    expect(calculator.getDelay(3)).toBe(4000);
    expect(calculator.getDelay(4)).toBe(8000);
  });

  it('should cap delay at maxDelayMs', () => {
    // 1000 * 2^6 = 64000 > 30000
    expect(calculator.getDelay(7)).toBe(30_000);
  });

  it('should respect Retry-After header', () => {
    const delay = calculator.getDelay(1, 60); // 60 seconds
    expect(delay).toBe(30_000); // Capped at maxDelayMs
  });
});

// Integration test example — Mock HTTP
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { VoiceAgent } from '../src';

const server = setupServer();

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('AgentsResource', () => {
  const client = new VoiceAgent({
    apiKey: 'va_test_abc',
    baseUrl: 'http://localhost:3000',
  });

  it('should list agents with cursor pagination', async () => {
    server.use(
      http.get('http://localhost:3000/v1/agents', ({ request }) => {
        const url = new URL(request.url);
        expect(url.searchParams.get('limit')).toBe('20');

        return HttpResponse.json({
          data: [
            { id: 'ag_1', name: 'Agent 1', status: 'active', createdAt: '2025-01-01T00:00:00Z' },
          ],
          pagination: { cursor: 'cursor_abc', hasMore: true },
        });
      }),
    );

    const result = await client.agents.list({ limit: 20 });
    expect(result.data).toHaveLength(1);
    expect(result.pagination.hasMore).toBe(true);
  });

  it('should handle 429 rate limit with retry', async () => {
    let attempts = 0;

    server.use(
      http.get('http://localhost:3000/v1/agents', () => {
        attempts++;
        if (attempts < 2) {
          return HttpResponse.json(
            { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
            { status: 429, headers: { 'Retry-After': '1' } },
          );
        }
        return HttpResponse.json({
          data: [],
          pagination: { cursor: null, hasMore: false },
        });
      }),
    );

    const result = await client.agents.list({});
    expect(attempts).toBe(2);
    expect(result.data).toEqual([]);
  });

  it('should throw NotFoundError for 404', async () => {
    server.use(
      http.get('http://localhost:3000/v1/agents/nonexistent', () => {
        return HttpResponse.json(
          { error: { code: 'NOT_FOUND', message: 'Agent nonexistent not found' } },
          { status: 404 },
        );
      }),
    );

    await expect(client.agents.get('nonexistent')).rejects.toThrowNotFoundError();
  });
});

// E2E test example
describe('E2E: Agent CRUD', () => {
  const client = new VoiceAgent({
    apiKey: process.env.VOICE_AGENT_TEST_API_KEY!,
    environment: 'sandbox',
  });

  it('should create, read, update, and delete an agent', async () => {
    // Create
    const created = await client.agents.create({
      name: 'E2E Test Agent',
      voice: { provider: 'elevenlabs', voiceId: 'test_voice' },
      model: { provider: 'openai', model: 'gpt-4o' },
    });
    expect(created.id).toBeDefined();

    // Read
    const fetched = await client.agents.get(created.id);
    expect(fetched.name).toBe('E2E Test Agent');

    // Update
    const updated = await client.agents.update(created.id, { name: 'Updated E2E Agent' });
    expect(updated.name).toBe('Updated E2E Agent');

    // Delete
    await client.agents.delete(created.id);
    await expect(client.agents.get(created.id)).rejects.toThrowNotFoundError();
  }, 30_000);
});
```

## Integration Points

- **CI Pipeline**: Unit + integration tests run on every PR; E2E runs nightly and on merge to main
- **Code Coverage**: Minimum 90% coverage for unit tests; 80% for integration
- **Test Reporting**: Test results reported to GitHub Checks API
- **Sandbox Environment**: Dedicated test tenant for E2E tests with rate limit exemptions

## Production Considerations

- **Test Data Cleanup**: E2E tests clean up created resources; CI failure doesn't leave orphaned resources
- **Flaky Test Detection**: Tests that fail intermittently are quarantined and investigated
- **API Version Lock**: E2E tests pin a specific API version; test failures trigger version compatibility review
- **Mock vs Real Balance**: Unit tests are fast and reliable; E2E tests catch real integration issues

## Open-Source Tools

- **Vitest**: Fast unit test runner with TypeScript support
- **MSW (Mock Service Worker)**: HTTP request mocking for integration tests
- **Playwright**: Browser E2E testing for browser-specific SDK features
