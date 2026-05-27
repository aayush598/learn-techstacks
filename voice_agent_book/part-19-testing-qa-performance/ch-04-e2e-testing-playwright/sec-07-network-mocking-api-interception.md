# Section 07: Network Mocking & API Interception

## Overview

Network mocking in E2E tests intercepts and controls HTTP requests made by the browser, enabling tests to simulate various backend responses without a real server. For the voice AI platform, network mocking covers API responses, WebSocket messages, third-party service integrations (payment providers, AI services), and error scenarios (network failures, slow responses, server errors).

Playwright's `page.route()` API intercepts network requests at the browser level, allowing tests to return mock responses, modify request/response data, or block requests entirely. This enables testing of loading states, error handling, offline behavior, and edge cases that are difficult to reproduce with a real backend.

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
// Network mocking setup
import { test, expect, type Page } from '@playwright/test';

async function setupApiMocks(page: Page) {
  // Mock external AI service
  await page.route('https://api.openai.com/**', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        choices: [{ message: { content: 'Mock response' } }],
      }),
    });
  });

  // Mock payment provider
  await page.route('https://api.stripe.com/**', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        id: 'pi_mock',
        status: 'succeeded',
      }),
    });
  });

  // Simulate slow API for loading state testing
  await page.route('**/api/analytics/**', async (route) => {
    await new Promise(r => setTimeout(r, 2000)); // 2s delay
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ data: [] }),
    });
  });
}

test('displays loading state while analytics load', async ({ page }) => {
  await setupApiMocks(page);
  await page.goto('/dashboard/analytics');
  
  // Loading state should be visible
  await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible();
  
  // After delay, data should appear
  await expect(page.locator('[data-testid="loading-spinner"]')).not.toBeVisible();
});

test('handles API error gracefully', async ({ page }) => {
  await page.route('**/api/agents**', async (route) => {
    await route.fulfill({
      status: 500,
      body: JSON.stringify({ error: { code: 'INTERNAL_ERROR' } }),
    });
  });
  
  await page.goto('/dashboard/agents');
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="retry-button"]')).toBeVisible();
});
```

## Integration Points

- **API Contract**: Mock responses should match actual API contracts
- **Error Boundaries**: Test that React error boundaries catch network failures
- **Offline Support**: Test PWA offline behavior by blocking all network requests
- **Retry Logic**: Verify retry UI after transient failures
- **Optimistic Updates**: Test optimistic UI updates with delayed mock responses

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Mock Fidelity**: Mock responses must match real API shapes; update when API changes
- **Over-Mocking**: Over-mocking hides integration issues; use selective mocking
- **WebSocket Mocking**: WebSocket interception is complex; consider test-specific WebSocket server
- **Mock Leakage**: Clean up mocks between tests; Playwright context isolation helps
- **Flaky Mocks**: Race conditions between mock setup and page navigation cause flakiness
