# Section 01: Testing Philosophy & Pyramid Model

## Overview

The testing pyramid, popularized by Mike Cohn, is a foundational concept in software testing that describes the ideal distribution of different test types. For a voice AI SaaS platform, this pyramid must be adapted to account for the unique challenges of real-time audio processing, conversational AI, and multi-tenant architecture. The traditional pyramid (unit > integration > e2e) must be augmented with conversation simulation and voice-specific quality testing.

The trophy-shaped testing strategy, advocated by Kent C. Dodds, argues for more integration tests and fewer unit and e2e tests. For a voice platform, we adopt a hybrid approach: a broad base of unit tests for business logic, a thick middle of integration tests for voice pipeline components, targeted conversation simulation tests for agent behavior, and minimal but critical E2E tests for key user journeys.

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

```
// Test selection strategy based on what's being tested
const testSelection = {
  'business-logic': { type: 'unit', tool: 'vitest', priority: 'high' },
  'api-route': { type: 'integration', tool: 'vitest', priority: 'high' },
  'voice-pipeline': { type: 'integration', tool: 'vitest', priority: 'critical' },
  'agent-conversation': { type: 'simulation', tool: 'custom', priority: 'critical' },
  'ui-journey': { type: 'e2e', tool: 'playwright', priority: 'medium' },
  'visual-regression': { type: 'e2e', tool: 'playwright', priority: 'low' }
}

const getTestType = (component, changeType) => {
  if (changeType === 'hotfix') return ['unit', 'integration', 'simulation'];
  if (changeType === 'feature') return ['unit', 'integration', 'simulation', 'e2e'];
  return ['unit'];
}
```

## Integration Points

- **CI/CD Pipeline**: Test selection feeds into GitHub Actions for targeted test execution based on changed files
- **Coverage Aggregation**: All test layers report to a central coverage dashboard (Codecov/CodeClimate)
- **Test Reporting**: Results aggregated across layers for unified pass/fail status
- **Quality Gates**: Each layer has pass/fail criteria that gate deployments

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Test Reliability**: Flaky tests are the enemy. Invest in test stability before growing the suite.
- **Execution Time**: Unit tests should run in <30s, integration <2min, simulation <5min, E2E <10min.
- **Parallel Execution**: Use test sharding and parallel workers to keep CI fast as the suite grows.
- **Selective Execution**: Only run relevant test layers based on code changes to minimize feedback time.
- **Test Data Isolation**: Each test layer must have its own data isolation strategy to prevent interference.
