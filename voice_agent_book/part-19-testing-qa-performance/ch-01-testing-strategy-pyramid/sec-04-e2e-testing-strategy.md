# Section 04: E2E Testing Strategy

## Overview

End-to-end (E2E) testing validates complete user journeys across the entire stack, from browser interactions through API calls to database operations. For the voice AI platform, E2E tests cover critical business flows: user signup, agent creation and configuration, dashboard interaction, call log review, and billing management. E2E tests run against a full deployment including the frontend, API, database, and integrated services.

Given the cost and fragility of E2E tests, we employ a "critical path only" strategy: E2E tests cover the top 20% of user journeys that handle 80% of user value. Less critical paths are covered by integration or unit tests. Each E2E test focuses on a single user goal, not multiple scenarios per test.

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
// E2E test for agent creation flow
import { test, expect } from './fixtures/authenticated-user';

test('user can create and configure a new voice agent', async ({ page, user }) => {
  // Navigate to agent creation
  await page.goto('/agents/new');
  await expect(page.locator('h1')).toContainText('Create Agent');

  // Fill agent details
  await page.fill('[name="agentName"]', 'Customer Support Bot');
  await page.fill('[name="description"]', 'Handles customer inquiries');
  
  // Select voice
  await page.click('[data-testid="voice-select"]');
  await page.click('text=Natural Female Voice');
  
  // Configure knowledge base
  await page.click('[data-testid="add-knowledge-source"]');
  await page.fill('[name="knowledgeUrl"]', 'https://docs.example.com/faq');
  
  // Save and deploy
  await page.click('button:has-text("Create Agent")');
  
  // Verify agent created
  await expect(page.locator('[data-testid="agent-status"]')).toContainText('Active');
  await expect(page).toHaveURL(/\/agents\/[a-f0-9-]+/);
  
  // Verify in database via API
  const response = await page.request.get(`/api/agents/${user.agentId}`);
  expect(response.ok()).toBeTruthy();
});
```

## Integration Points

- **CI Pipeline**: E2E tests run on PR merge to main and before production deployments
- **Test Environment**: Deployed via Helm to a dedicated E2E Kubernetes namespace
- **Data Seeding**: Test data seeded via API calls before test execution
- **Cleanup**: Test data cleanup runs after suite completion
- **Reporting**: Results published to Allure TestOps for trend analysis

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Test Data Management**: Never use production data; always seed fresh test data
- **Environment Cleanup**: Automated cleanup of test resources after runs
- **Parallel Execution**: Use Playwright sharding across multiple machines in CI
- **Flaky Test Quarantine**: Automatically quarantine tests that fail >3 consecutive runs
- **Execution Budget**: E2E suite must complete within 15 minutes for CI viability
