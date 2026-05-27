# Section 01: Playwright Configuration & Setup

## Overview

Playwright provides cross-browser E2E testing capabilities for the voice AI platform's web dashboard, agent configuration interface, and real-time call monitoring views. Configuration is centralized in `playwright.config.ts` with environment-specific overrides. The setup includes browser selection (Chromium, Firefox, WebKit), device emulation profiles, authentication state management, and reporting configuration.

Playwright's test runner integrates with the existing Vitest patterns while providing browser-specific capabilities. The configuration supports parallel execution across browsers, retry logic for flaky tests, video recording for failure analysis, and trace viewer integration for debugging complex scenarios.

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
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : 1,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['github'],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    viewport: { width: 1280, height: 720 },
    actionTimeout: 10000,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
});
```

## Integration Points

- **Test Environment**: E2E tests run against a dedicated staging deployment
- **Authentication**: Auth state stored as `storageState.json` for reuse
- **Data Seeding**: Test data seeded via API before test execution
- **Reporting**: HTML reports published to CI artifacts, JSON for custom dashboards
- **WebSocket**: Playwright's page.route for WebSocket interception

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Browser Versions**: Keep browser binaries updated; CI should auto-download new versions
- **Test Data Cleanup**: E2E tests create real data; ensure automated cleanup
- **CI Resource Usage**: Browser tests are resource-intensive; provision adequate CI runners
- **Test Flakiness**: WebKit tests are most flaky; consider reducing WebKit coverage if unstable
- **Local Development**: Use `npx playwright install` to manage local browser binaries
