# Section 02: Build & Test Pipeline

## Overview

The build-and-test pipeline is the heart of CI — it runs on every PR commit and validates that changes compile, pass type checks, satisfy lint rules, and pass all test levels (unit, integration, E2E). The pipeline is organized as a DAG of dependent stages executed via Turborepo, with early failure to conserve runner minutes.

## Pipeline Stages

```text
┌──────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐
│  Install  │───▶│   Lint   │───▶│ TypeCheck │───▶│   Test   │
│  + Cache  │    │          │    │           │    │  (Unit)  │
└──────────┘    └──────────┘    └───────────┘    └────┬─────┘
                                                       │
                                                       ▼
                                                ┌──────────┐
                                                │  Build    │
                                                │          │
                                                └────┬─────┘
                                                       │
                                                       ▼
                                          ┌──────────────┐
                                          │ Integration  │
                                          │ Tests        │
                                          └──────┬───────┘
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │  E2E Tests   │
                                          │ (Playwright)  │
                                          └──────────────┘
```

The ordering maximizes early feedback: lint and typecheck run without starting containers, so a syntax error is caught in under 60 seconds. Only after those pass do we spin up test containers for integration and E2E suites.

## GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
  TURBO_REMOTE_ONLY: true

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      turbo-cache-key: ${{ steps.turbo-key.outputs.key }}
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - id: turbo-key
        run: echo "key=turbo-${{ runner.os }}-${{ github.sha }}" >> $GITHUB_OUTPUT

  lint:
    needs: [setup]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo lint --filter={./*}...
      - run: npx prettier --check "**/*.{ts,tsx,js,json,md}"

  typecheck:
    needs: [setup]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo typecheck --filter={./*}...

  unit-test:
    needs: [setup]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo test -- --reporter=junit --coverage
      - uses: dorny/test-reporter@v1
        if: always()
        with:
          name: "Unit Test Results"
          path: reports/junit-*.xml
          reporter: java-junit
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-reports
          path: packages/*/coverage

  build:
    needs: [lint, typecheck, unit-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo build
      - uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            apps/*/.next
            packages/*/dist

  integration-test:
    needs: [build]
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: voice_agent_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo test --filter=@voice-agent/db
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/voice_agent_test

  e2e-test:
    needs: [build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx playwright install --with-deps chromium
      - run: npx turbo test --filter=@voice-agent/web -- --project=chromium
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-screenshots
          path: apps/web/test-results/
```

## Stage Design Decisions

**Lint and typecheck in parallel**: These have no dependencies on each other and both complete in under two minutes. Running them in parallel reduces total wall-clock time.

**Unit tests before build**: Unit tests run against TypeScript source directly via vitest with `tsx`. We don't need compiled JavaScript to run unit tests. Build only runs after unit tests pass, preventing wasted build minutes when tests fail.

**Integration tests after build**: Integration tests start Docker containers via testcontainers or GitHub Actions `services`. Running them after build ensures the compiled artifacts exist. This is a deliberate trade-off — we could run them in parallel with the build at the cost of more complex caching.

**E2E tests as a separate job**: Playwright tests need a running build and a browser. They are the most resource-intensive stage, so they run last and only if everything else passes.

## Caching for Speed

```yaml
- name: Cache pnpm store
  uses: actions/cache@v4
  with:
    path: ~/.local/share/pnpm/store
    key: pnpm-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: pnpm-
```

Turborepo's remote cache is the primary accelerator. In our testing, a full CI run on a cold cache takes 12 minutes. With cache hits (the common case for PRs touching only a few packages), it drops to 3-4 minutes.

## Integration Points

- **PR status checks**: Each job maps to a required status check in branch protection rules
- **Test reporter**: The `dorny/test-reporter` action parses JUnit XML and annotates the PR with test summaries
- **Coverage artifacts**: Uploaded for later analysis and PR coverage comments
- **Slack notifications**: A final step notifies the channel only on failure (success is silent)

## Production Considerations

1. **Timeout limits**: Each job has an explicit timeout. Lint/typecheck at 5 minutes, tests at 15 minutes, build at 20 minutes. Timeouts prevent hung jobs from blocking the queue.
2. **Resource class**: Use `runs-on: ubuntu-latest-4core` for test jobs and `ubuntu-latest-8core` for builds. The extra cores for builds halve the TypeScript compilation time.
3. **Flaky test retries**: Integration tests automatically retry once on failure. If the retry passes, the test is reported as flaky but the pipeline succeeds. A weekly report tracks flakiness trends.
4. **Dependency caching isolation**: Each matrix combination gets its own cache key. Mixing Node 18 and Node 20 caches causes version conflicts.
5. **Secrets scanning**: Run `trufflehog` or `gitleaks` as a pre-lint step to catch accidentally committed secrets before they reach the test suite.
6. **GitHub Actions usage budget**: Monitor monthly included minutes. For large monorepos, consider self-hosted runners with runner groups to contain costs.
