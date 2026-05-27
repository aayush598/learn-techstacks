# Section 06: Coverage Reporting & Analysis

## Overview

Coverage reporting provides visibility into which code paths are exercised by tests and identifies untested areas that could harbor defects. The voice AI platform uses Istanbul/V8 coverage instrumentation integrated with Vitest, generating reports in multiple formats for different audiences: terminal output for developers, HTML reports for detailed browsing, LCOV for IDE integration, and JSON for CI tooling.

Coverage analysis goes beyond simple percentage tracking. The team reviews coverage on a per-module basis, identifying uncovered branches and functions. Diff coverage (coverage of newly added lines) is enforced in CI to prevent coverage erosion. Coverage data is trended over time to detect quality regressions and guide testing investment.

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
// Coverage configuration in vitest.config.ts
coverage: {
  provider: 'v8',
  reporter: ['text', 'json', 'lcov', 'html', 'clover'],
  reportsDirectory: './coverage',
  include: [
    'src/**/*.ts',
    'src/**/*.tsx',
    '!src/**/*.generated.ts',
    '!src/**/*.types.ts',
    '!src/**/*.d.ts',
  ],
  thresholds: {
    // Per-directory thresholds
    'src/core/voice': { branches: 95, functions: 95, lines: 95 },
    'src/api': { branches: 85, functions: 85, lines: 85 },
    'src/services': { branches: 80, functions: 80, lines: 80 },
    'src/components': { branches: 60, functions: 60, lines: 70 },
    // Global defaults
    branches: 75,
    functions: 75,
    lines: 80,
    statements: 80,
  },
}

// CI integration for diff coverage
// Uses Codecov's --diff flag to report coverage of changed lines
// github action step:
// - name: Upload coverage
//   uses: codecov/codecov-action@v3
//   with:
//     directory: ./coverage
//     flags: unittests
//     diff: true
```

## Integration Points

- **CI Pipeline**: Coverage checks run as a separate job after tests
- **Codecov**: Coverage data uploaded for historical tracking and PR comments
- **IDE Integration**: LCOV files enable inline coverage highlighting (VS Code Coverage Gutters)
- **Team Dashboard**: Coverage trends displayed on engineering dashboard (Grafana)
- **Pulse Checks**: Weekly reports on coverage changes, uncovered areas, and improvement suggestions

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Coverage Theater**: High coverage doesn't mean good tests; review test quality alongside metrics
- **False Security**: 100% coverage of a function that's never tested with real data is misleading
- **Coverage Debt**: Track intentional coverage gaps with TODO comments and tickets
- **Performance Impact**: Coverage instrumentation slows test execution; use separate CI job
- **Granular Targets**: Different coverage targets for different code categories prevent false negatives
