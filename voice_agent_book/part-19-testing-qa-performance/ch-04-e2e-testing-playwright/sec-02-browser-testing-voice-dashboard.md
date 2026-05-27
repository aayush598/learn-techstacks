# Section 02: Browser Testing for Voice Dashboard

## Overview

Browser testing for the voice dashboard validates the primary user interface where customers configure agents, monitor calls, review transcripts, and analyze performance. The dashboard is a complex single-page application with real-time updates via WebSocket, dynamic forms for agent configuration, data visualization for analytics, and interactive call controls.

Tests cover critical user journeys: logging in, creating and configuring agents, viewing call logs and recordings, monitoring live calls, reviewing analytics dashboards, managing billing settings, and administering team members. Each journey is tested across desktop and mobile viewports to ensure responsive design correctness.

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
// Dashboard E2E test
import { test, expect } from './fixtures/dashboard';

test.describe('Agent Management', () => {
  test('create and configure a new voice agent', async ({ page, user }) => {
    // Navigate to agent creation
    await page.goto('/dashboard/agents/new');
    await expect(page.locator('h1')).toContainText('Create Agent');

    // Fill agent configuration form
    await page.fill('[data-testid="agent-name"]', 'Support Agent');
    await page.fill('[data-testid="agent-description"]', 'Handles customer support');
    
    // Select language and voice
    await page.selectOption('[data-testid="language-select"]', 'en-US');
    await page.click('[data-testid="voice-select"]');
    await page.click('text=Natural Female Voice');
    
    // Configure greeting
    await page.fill('[data-testid="greeting-input"]', 'Hello, welcome to support!');
    
    // Save agent
    await page.click('[data-testid="save-agent"]');
    
    // Verify agent created
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page).toHaveURL(/\/dashboard\/agents\/[a-f0-9-]+/);
    
    // Verify agent appears in list
    await page.goto('/dashboard/agents');
    await expect(page.locator('text=Support Agent')).toBeVisible();
  });

  test('dashboard shows real-time call metrics', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Wait for metrics to load
    await expect(page.locator('[data-testid="active-calls"]')).toBeVisible();
    
    // Verify metric values
    const activeCalls = await page.locator('[data-testid="active-calls"]').textContent();
    expect(Number(activeCalls)).toBeGreaterThanOrEqual(0);
    
    // Real-time updates should appear
    await page.waitForFunction(() => {
      const el = document.querySelector('[data-testid="last-update"]');
      return el?.textContent?.includes('seconds ago') ?? false;
    }, { timeout: 10000 });
  });
});
```

## Integration Points

- **API Layer**: Tests create/read data via the same API used by the frontend
- **WebSocket**: Real-time dashboard tests verify WebSocket event handling
- **Authentication**: Login flow tested with actual credentials; subsequent tests reuse session
- **Component Library**: UI component interactions use data-testid attributes
- **Error Tracking**: Dashboard error boundaries tested via API error simulation

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Data Sensitivity**: Dashboard tests should not use production-like PII in test data
- **Performance Budgets**: Dashboard load time should not exceed 3 seconds; enforce via tests
- **Error Boundaries**: Test that React error boundaries catch and display errors gracefully
- **Network Conditions**: Test dashboard behavior under slow network (Playwright network throttling)
- **Browser Extensions**: Tests should not assume absence of browser extensions
