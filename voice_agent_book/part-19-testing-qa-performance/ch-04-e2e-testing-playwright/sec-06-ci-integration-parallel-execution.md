# Section 06: CI Integration & Parallel Execution

## Overview

CI integration for Playwright E2E tests requires careful configuration to balance coverage, execution time, and resource utilization. The voice AI platform uses GitHub Actions with a matrix strategy to shard tests across multiple runners, each running multiple browser projects in parallel. Artifact management preserves test reports, videos, and traces for debugging.

The CI pipeline stages E2E tests to run after unit and integration tests pass, ensuring faster feedback for simple failures. Playwright's retry logic handles flaky tests, while reporting provides visibility into test health trends and failure patterns.

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

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      
      - run: npm ci
      
      - run: npx playwright install --with-deps chromium firefox
      
      - name: Build application
        run: npm run build
      
      - name: Start test server
        run: npm run start:e2e &
      
      - name: Wait for server
        run: npx wait-on http://localhost:3000
      
      - name: Run Playwright tests
        run: npx playwright test --shard=${{ matrix.shard }}/${{ strategy.job-total }}
        env:
          BASE_URL: http://localhost:3000
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.shard }}
          path: |
            playwright-report/
            test-results/
          retention-days: 7
      
      - name: Upload failed test videos
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-videos-${{ matrix.shard }}
          path: test-results/*/video.*
          retention-days: 3
```

## Integration Points

- **Status Checks**: E2E test results posted as GitHub status checks
- **PR Comments**: Test summary posted as PR comment with failure links
- **Slack Notifications**: E2E pipeline failures notified to team Slack channel
- **Dashboard**: Test health dashboard updated with results
- **Flaky Test Tracking**: Flaky tests tracked in test analytics system

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **CI Runner Resources**: E2E tests require significant CPU/memory; use larger runners
- **Browser Binary Caching**: Cache Playwright browser binaries in CI for faster setup
- **Environment Flakiness**: CI environment differences can cause flakiness; pin image versions
- **Cost Optimization**: Run full E2E suite on main branch; subset on PRs for faster feedback
- **Test Selection**: Run only changed test files on PRs using `--last-failed` or file matching
