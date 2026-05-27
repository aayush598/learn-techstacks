# Section 03: Component Testing with Playwright

## Overview

Component testing with Playwright validates individual UI components in isolation, providing faster feedback than full E2E tests while exercising real browser rendering. For the voice AI platform, component tests cover the voice visualizer, call transcript viewer, agent configuration form fields, analytics chart components, and notification panels.

Component tests mount components without requiring a full application deployment. They interact with the component's rendered output, verify state changes, test accessibility, and validate responsive behavior. Component testing bridges the gap between unit tests (logic only) and E2E tests (full application).

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

```tsx
// Component test using Playwright's component testing
import { test, expect } from '@playwright/experimental-ct-react';
import { AgentConfigForm } from '@/components/AgentConfigForm';
import { createMockAgent } from '@test/factories/agent';

test('AgentConfigForm validates required fields', async ({ mount }) => {
  const onSave = jest.fn();
  
  const component = await mount(
    <AgentConfigForm onSave={onSave} />
  );

  // Try saving without filling required fields
  await component.locator('[data-testid="save"]').click();
  
  // Validation errors should appear
  await expect(component.locator('[data-testid="field-error-name"]')).toBeVisible();
  await expect(component.locator('[data-testid="field-error-language"]')).toBeVisible();
  
  // Fill required fields
  await component.locator('[name="name"]').fill('Test Agent');
  await component.locator('[data-testid="language-select"]').click();
  await component.locator('text=en-US').click();
  
  // Now save should work
  await component.locator('[data-testid="save"]').click();
  expect(onSave).toHaveBeenCalledWith(
    expect.objectContaining({ name: 'Test Agent' })
  );
});

test('AgentConfigForm displays existing configuration', async ({ mount }) => {
  const agent = createMockAgent({
    name: 'Existing Agent',
    language: 'es-ES',
    voice: 'spanish-female',
  });

  const component = await mount(
    <AgentConfigForm agent={agent} onSave={jest.fn()} />
  );

  await expect(component.locator('[name="name"]')).toHaveValue('Existing Agent');
  await expect(component.locator('[data-testid="selected-language"]')).toContainText('es-ES');
});
```

## Integration Points

- **Design System**: Component tests validate design system components usage
- **State Management**: Components tested with mock store/provider context
- **API Integration**: Components that fetch data are tested with mock API responses
- **Accessibility**: Automated a11y checks integrated into component tests
- **Visual Regression**: Component screenshots compared on each test run

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Component Complexity**: Test component behavior, not implementation details
- **Mock Fidelity**: Mock data should resemble production data shapes
- **Style Loading**: Ensure component styles load correctly in test environment
- **Animation Handling**: Disable animations in tests to avoid timing issues
- **Browser Compatibility**: Test components across Chromium/Firefox/WebKit for CSS differences
