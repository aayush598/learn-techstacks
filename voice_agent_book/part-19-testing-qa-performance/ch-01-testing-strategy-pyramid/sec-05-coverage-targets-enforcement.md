# Section 05: Coverage Targets & Enforcement

## Overview

Code coverage targets provide quantitative quality gates that prevent untested code from reaching production. For the voice AI platform, we set different coverage targets for different code categories based on criticality. Core voice pipeline code (VAD, STT integration, LLM orchestration, TTS) requires the highest coverage, while UI components and configuration code have lower targets.

Coverage enforcement is automated in CI using Vitest's built-in coverage provider with Istanbul. The coverage report is generated on every test run, and the CI pipeline gates the merge based on predefined thresholds. Coverage data is also trended over time to detect regressions and celebrate improvements.

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
// vitest.config.ts - Coverage Configuration
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary', 'lcov', 'html'],
      include: ['src/**/*.ts'],
      exclude: [
        'src/**/*.generated.ts',
        'src/**/*.types.ts',
        'src/**/*.config.ts',
        'src/**/index.ts',
      ],
      thresholds: {
        // Core voice pipeline: highest coverage
        './src/core/vad/**/*.ts': {
          branches: 95,
          functions: 95,
          lines: 95,
          statements: 95,
        },
        './src/core/stt/**/*.ts': {
          branches: 90,
          functions: 90,
          lines: 90,
          statements: 90,
        },
        // API routes: high coverage
        './src/api/**/*.ts': {
          branches: 85,
          functions: 85,
          lines: 85,
          statements: 85,
        },
        // Services: good coverage
        './src/services/**/*.ts': {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
        // UI components: moderate coverage
        './src/components/**/*.tsx': {
          branches: 60,
          functions: 60,
          lines: 70,
          statements: 70,
        },
        // Default for everything else
        branches: 75,
        functions: 75,
        lines: 80,
        statements: 80,
      },
    },
  },
});
```

## Integration Points

- **CI Pipeline**: Coverage check runs as a separate step after tests
- **GitHub Status Check**: Coverage thresholds appear as a required status check on PRs
- **Codecov/CodeClimate**: Coverage data uploaded for historical tracking and PR comments
- **Dashboard**: Coverage metrics fed into the engineering quality dashboard
- **Slack Alerts**: Coverage drops below threshold trigger Slack notifications

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **False Confidence**: Coverage doesn't measure test quality; encourage meaningful testing over padding
- **Uncovered Code Reviews**: Review uncovered branches during code review to validate intentional exclusion
- **Coverage Trends**: Watch for coverage decline trends rather than fixating on daily numbers
- **Integration Coverage**: Include integration test coverage in overall metrics, not just unit
- **Exclusion Governance**: Exclusions require team lead approval; regular audit of exclusion list
