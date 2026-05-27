# Section 05: Test Isolation & State Management

## Overview

E2E test isolation ensures each test runs in a clean environment without side effects from previous tests. For the voice AI platform, isolation spans browser state (localStorage, cookies, sessionStorage), application state (Redux/Zustand stores), database state (test data), and authentication state (active sessions). Proper isolation prevents flaky tests and enables reliable parallel execution.

State management in E2E tests involves setting up known state before tests (seeding), verifying state during tests (assertions), and cleaning up after tests (teardown). Playwright's browser context isolation provides natural separation between test files, while within-file tests manage shared state through fixtures.

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
// Authentication fixture setup
// playwright/fixtures/auth.ts
import { test as base } from '@playwright/test';
import { createUser, createAuthToken } from './helpers';

export const test = base.extend({
  // Authenticated context with saved storage state
  storageState: async ({}, use) => {
    const state = await setupAuthState();
    await use(state);
  },

  // User fixture with seeded data
  user: async ({ request }, use) => {
    const user = await createUser(request);
    const token = createAuthToken(user);
    await use({ user, token });
    
    // Cleanup
    await request.delete(`/api/test/users/${user.id}`);
  },

  // Authenticated page
  authPage: async ({ browser, user }, use) => {
    const context = await browser.newContext({
      storageState: {
        cookies: [],
        origins: [{
          origin: BASE_URL,
          localStorage: [
            { name: 'auth_token', value: user.token },
          ],
        }],
      },
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});

// Usage
test('agent creation with auth fixture', async ({ authPage, user }) => {
  await authPage.goto('/dashboard/agents/new');
  // Page is already authenticated
  await authPage.fill('[name="name"]', 'Test Agent');
  // ...
});
```

## Integration Points

- **API Layer**: Test data seed/cleanup via internal API endpoints
- **Authentication**: Auth state managed through JWT tokens and storage state
- **Database**: Test data isolation via unique identifiers per test
- **Cookie Management**: Session cookies set via storageState
- **Local Storage**: App state initialized via localStorage before navigation

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Storage State Expiry**: Auth tokens expire; refresh storage state periodically
- **Cleanup Failures**: Test data cleanup failures should be monitored but not block CI
- **Parallel Safety**: Test data identifiers must be unique across parallel runs
- **Context Limits**: Browser contexts consume memory; limit parallel contexts per machine
- **State Leakage Investigation**: Use `--replay` flag for debugging state leakage issues
