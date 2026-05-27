# Section 02: Unit Testing Strategy

## Overview

Unit testing forms the foundation of the testing pyramid for our voice AI platform. Each unit test validates a single function, utility, or module in isolation with all external dependencies mocked. The primary focus is on business logic, data transformation, state management, and algorithmic correctness. For the voice pipeline specifically, we unit test components like VAD classifiers, audio buffer manipulation, text sanitization, intent parsing, and response generation helpers.

Pure functions are prioritized for unit testing as they have no side effects and produce deterministic results. Services with dependency injection are tested by mocking their dependencies, allowing verification of interaction patterns and edge cases. The unit testing strategy enforces that every public function has at least one positive and one negative test case.

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
// Example: Testing a voice pipeline utility function
// Pure function - no mocking needed
function calculateVadThreshold(audioLevels: number[], sensitivity: number): number {
  const mean = audioLevels.reduce((a, b) => a + b, 0) / audioLevels.length;
  const stdDev = Math.sqrt(
    audioLevels.reduce((sq, n) => sq + Math.pow(n - mean, 2), 0) / audioLevels.length
  );
  return mean + (sensitivity * stdDev);
}

describe('calculateVadThreshold', () => {
  it('returns correct threshold for normal audio levels', () => {
    const levels = [0.1, 0.2, 0.15, 0.3, 0.25, 0.1, 0.2];
    expect(calculateVadThreshold(levels, 2.0)).toBeCloseTo(0.35, 2);
  });

  it('handles silence (all zeros)', () => {
    expect(calculateVadThreshold([0, 0, 0, 0], 2.0)).toBe(0);
  });

  it('throws on empty array', () => {
    expect(() => calculateVadThreshold([], 1.0)).toThrow();
  });
});
```

## Integration Points

- **Service Layer Testing**: Services tested with mocked repositories and external clients
- **Coverage Enforcement**: 80% line coverage minimum, 90% for critical business logic
- **CI Integration**: Unit tests run on every push, blocking merge on failure
- **Pre-commit Hooks**: Changed files run their related unit tests via lint-staged

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Test Speed**: Unit tests must complete in under 30 seconds total
- **Determinism**: No random or time-dependent values without seeding
- **Isolation**: Each test file must be independently runnable
- **File Organization**: Tests co-located with source files (*.test.ts alongside *.ts)
- **Naming Convention**: Describe what's under test, the scenario, and expected outcome
