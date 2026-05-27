# Section 08: Accessibility & Performance Testing

## Overview

Accessibility and performance testing embedded in E2E tests ensure the voice AI platform meets WCAG 2.1 AA standards and performance budgets. Accessibility checks run automatically during E2E tests using axe-core integration, catching violations like missing ARIA labels, insufficient color contrast, keyboard navigation issues, and focus management problems.

Performance testing uses Lighthouse CI integration to measure Core Web Vitals (LCP, FID, CLS), time-to-interactive, and bundle size. Performance budgets are enforced in CI, preventing regressions from reaching production. Both accessibility and performance tests generate reports that track trends over time.

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
// Accessibility testing
import AxeBuilder from '@axe-core/playwright';

test('dashboard page has no critical accessibility violations', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');
  
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .disableRules(['color-contrast']) // Handled separately
    .analyze();

  // Check for critical/serious violations
  const violations = results.violations.filter(
    v => v.impact === 'critical' || v.impact === 'serious'
  );

  expect(violations).toEqual([]);
});

// Performance testing with Lighthouse
test('dashboard meets performance budgets', async ({ page }) => {
  const lighthouseResult = await runLighthouse(page, {
    thresholds: {
      performance: 85,
      accessibility: 90,
      'best-practices': 85,
      seo: 85,
    },
    reportsDir: 'lighthouse-reports',
  });

  expect(lighthouseResult.scores.performance).toBeGreaterThanOrEqual(85);
  expect(lighthouseResult.scores.accessibility).toBeGreaterThanOrEqual(90);
});

// Custom performance assertions
test('agent list loads within budget', async ({ page }) => {
  const startTime = Date.now();
  
  await page.goto('/dashboard/agents');
  await page.waitForSelector('[data-testid="agent-table"]');
  
  const loadTime = Date.now() - startTime;
  expect(loadTime).toBeLessThan(3000); // 3 second budget
});
```

## Integration Points

- **CI Pipeline**: A11y and perf tests run as part of E2E suite
- **Reporting**: Violations and scores reported in CI output and PR comments
- **Dashboard**: Accessibility score trend displayed on engineering dashboard
- **Issue Tracking**: New a11y violations auto-create tickets
- **Component Library**: Design system components tested for accessibility individually

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **False Positives**: Some a11y rules need manual review; maintain exclusion list
- **Performance Variance**: Test environment performance varies; use percentile-based budgets
- **Continuous Monitoring**: Accessibility regressions can appear anytime; monitor daily
- **User Research**: Automated a11y checks don't replace testing with real users with disabilities
- **Budget Reviews**: Performance budgets should be reviewed quarterly and adjusted based on user data
