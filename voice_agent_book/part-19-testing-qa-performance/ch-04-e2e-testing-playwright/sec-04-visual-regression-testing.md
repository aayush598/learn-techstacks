# Section 04: Visual Regression Testing

## Overview

Visual regression testing captures screenshots of UI components and pages, comparing them against baseline images to detect unintended visual changes. For the voice AI platform, visual regression tests cover the dashboard layout, agent configuration screens, analytics visualizations, call transcript rendering, and mobile responsive views. Changes to CSS, component structure, or content are caught before they reach production.

Playwright's built-in screenshot capabilities, combined with pixel matching assertions, provide reliable visual regression testing. The strategy focuses on critical visual elements rather than entire pages, using component-level screenshots for targeted coverage.

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
// Visual regression test
import { test, expect } from '@playwright/test';

test.describe('Dashboard Visual Regression', () => {
  test('agent list page matches baseline', async ({ page }) => {
    await page.goto('/dashboard/agents');
    await page.waitForLoadState('networkidle');
    
    // Mask dynamic content
    await expect(page).toHaveScreenshot('agent-list.png', {
      mask: [
        page.locator('[data-testid="live-call-count"]'),
        page.locator('[data-testid="user-avatar"]'),
      ],
      threshold: 0.001, // 0.1% pixel tolerance
    });
  });

  test('analytics chart renders correctly', async ({ page }) => {
    await page.goto('/dashboard/analytics');
    await page.waitForLoadState('networkidle');
    
    // Wait for chart to render
    await page.waitForSelector('[data-testid="chart-container"] svg');
    
    await expect(page.locator('[data-testid="chart-container"]'))
      .toHaveScreenshot('analytics-chart.png', {
        threshold: 0.002,
      });
  });

  test('mobile viewport agent form', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/dashboard/agents/new');
    await page.waitForLoadState('networkidle');
    
    await expect(page).toHaveScreenshot('agent-form-mobile.png', {
      fullPage: true,
      threshold: 0.01, // 1% tolerance for full page
    });
  });
});
```

## Integration Points

- **CI Pipeline**: Visual regression tests run as part of E2E suite
- **Baseline Storage**: Screenshot baselines stored in git (in `__snapshots__` directories)
- **PR Reviews**: Visual diffs visible in Playwright report attached to PR
- **Component Library**: Design system changes caught by visual regression
- **Theme Support**: Dark/light theme screenshots for both variants

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Baseline Drift**: Review and update baselines periodically as UI evolves
- **False Positives**: Anti-aliasing, font rendering, and OS differences cause false diffs
- **Storage Growth**: Screenshot baselines grow over time; prune unused baselines
- **Test Flakiness**: Animations, loading states, and timers cause flaky visual tests
- **CI Performance**: Visual tests are slower; run as a separate CI job
