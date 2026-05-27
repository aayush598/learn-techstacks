# Section 06: Test Categorization & Tagging

## Overview

Test categorization enables selective test execution based on context, reducing feedback time and resource consumption. The voice AI platform uses a multi-dimensional tagging system that categorizes tests by type (unit/integration/e2e/simulation), category (smoke/regression/acceptance), criticality (critical/high/medium/low), and owner (team/module). This tag system allows developers to run only relevant tests when making changes, and CI to execute targeted test suites based on code change scope.

Tags are defined using Vitest's built-in `test.tags` and custom markers. Tag inheritance allows tests to inherit tags from their parent describe block. Tag-based filtering is supported in both local development (via CLI) and CI (via environment variables).

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
// Tag usage examples
describe('Voice Pipeline', { tags: ['@unit', '@critical', '@core'] }, () => {
  it('processes audio buffer within time limits', 
    { tags: ['@performance'] }, 
    async () => {
      const result = await processAudio(testBuffer);
      expect(result.duration).toBeLessThan(100);
    }
  );

  it('handles empty audio gracefully', 
    { tags: ['@edge-case'] }, 
    async () => {
      const result = await processAudio(new Float32Array(0));
      expect(result.error).toBe('EMPTY_BUFFER');
    }
  );
});

// Selective execution in CI
// Run only smoke tests on quick checks
// vitest run --tags '@smoke'

// Run critical tests for deployment gate
// vitest run --tags '@critical'

// Exclude slow E2E tests during development
// vitest run --tags '-@e2e'

// Complex tag queries
// vitest run --tags '@critical,@core' --tags '@regression'
```

## Integration Points

- **CI Pipeline**: Commit-stage runs `@unit,@smoke`; PR-stage runs `@integration,@regression`; Deploy-stage runs `@critical`
- **GitHub Actions**: Tag-based test matrix that splits tests across parallel runners
- **Local Development**: `npm run test:changed` runs only tests tagged for changed modules
- **Pre-commit**: Lint-staged runs only tests relevant to staged files via owner tags
- **Flaky Test Detection**: Tests tagged `@flaky` are quarantined and tracked separately

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Tag Drift**: Audits ensure tags remain accurate as code evolves
- **Tag Proliferation**: Avoid too many unique tags; keep taxonomy manageable (8-12 tag values per dimension)
- **CI Performance**: Tag-based filtering significantly reduces CI times for targeted changes
- **Documentation**: Maintain a tag reference document for the team
- **Automated Tagging**: Consider automated tag inference based on file path patterns
