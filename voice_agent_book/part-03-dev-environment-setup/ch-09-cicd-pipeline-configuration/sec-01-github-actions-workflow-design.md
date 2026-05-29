# Section 01: GitHub Actions Workflow Design

## Overview

GitHub Actions provides the CI/CD backbone for the voice agent platform. Our workflow design emphasizes reusability, matrix builds for cross-package testing, and concurrency controls that prevent wasted compute on stale pushes. This section covers the workflow architecture, reusable action components, and orchestration patterns that keep pipeline execution efficient and maintainable.

## Workflow Architecture

The workflow design follows a hub-and-spoke model: a single orchestrator workflow dispatches to reusable workflows for each pipeline stage.

```text
┌──────────────────────────────────────────────────────────┐
│                    GitHub Actions Flow                     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Pull Request / Push                                      │
│       │                                                   │
│       ▼                                                   │
│  ┌──────────────┐                                         │
│  │  Orchestrator │  (ci.yml / cd.yml)                      │
│  │  Workflow     │                                         │
│  └──┬───────────┘                                         │
│     │                                                     │
│     ├──► Reusable: Install & Cache                         │
│     │       │                                              │
│     ├──► Reusable: Lint                                    │
│     │       │                                              │
│     ├──► Reusable: Type Check                              │
│     │       │                                              │
│     ├──► Reusable: Unit Tests                              │
│     │       │                                              │
│     ├──► Reusable: Build                                   │
│     │       │                                              │
│     ├──► Reusable: Integration Tests                       │
│     │       │                                              │
│     └──► Reusable: E2E Tests                               │
│                                                           │
│  On Success → Deploy Workflow (separate trigger)           │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Reusable Workflow Structure

Each reusable workflow lives in `.github/workflows/` or `.github/actions/`. This separation keeps pipeline logic DRY and allows different entry points (PR checks, staging deploy, production deploy) to compose the same building blocks.

```yaml
# .github/actions/setup/action.yml
name: "Setup Monorepo"
description: "Install dependencies, cache pnpm store, restore Turborepo cache"
inputs:
  node-version:
    description: "Node.js version"
    required: false
    default: "20.11.0"
  pnpm-version:
    description: "pnpm version"
    required: false
    default: "9.1.0"

runs:
  using: "composite"
  steps:
    - uses: pnpm/action-setup@v4
      with:
        version: ${{ inputs.pnpm-version }}
        run_install: false

    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: "pnpm"

    - name: Restore Turborepo Cache
      uses: actions/cache@v4
      id: turbo-cache
      with:
        path: .turbo
        key: turbo-${{ runner.os }}-${{ github.sha }}
        restore-keys: |
          turbo-${{ runner.os }}-

    - name: Install Dependencies
      run: pnpm install --frozen-lockfile
      shell: bash

    - name: Turborepo Login
      run: npx turbo login
      shell: bash
      env:
        TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

One design decision here is using a **composite action** rather than a Docker container action. Composite actions are lighter, run directly on the runner, and compose existing GitHub actions without an extra Docker build step. The trade-off is that composite actions cannot use `services` or run steps in a different shell environment.

## Concurrency Groups

Concurrency controls prevent duplicate workflow runs when a developer pushes multiple commits in rapid succession. Only the latest run in a group executes; earlier ones cancel.

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
```

The `cancel-in-progress: true` flag is critical for team productivity. Without it, a quick typo fix pushes would queue behind a running full CI suite. With cancellation, the stale run stops immediately and the fresh one starts. The trade-off is that cancellation can leave partial caches in an inconsistent state, so the setup action must handle idempotent cache restoration.

## Matrix Builds

Matrix builds test across multiple Node.js versions and package configurations:

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [18, 20, 22]
        package: ["web", "api", "voice", "ai"]
      fail-fast: false

    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
        with:
          node-version: ${{ matrix.node-version }}
      - run: npx turbo test --filter=@voice-agent/${{ matrix.package }}
```

Setting `fail-fast: false` ensures all matrix combinations report results independently. This is important when testing across Node versions — a failure in Node 18 should not prevent discovering issues in Node 22.

## Environment Secret Management

Secrets are injected at the workflow level, not in action definitions, to avoid leaking them into logs:

```yaml
jobs:
  deploy:
    environment: production
    env:
      DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
    steps:
      - run: doppler run --command="npx turbo build"
```

Using `environment: production` scopes the secrets and provides an approval gate. The Doppler CLI fetches secrets at runtime rather than baking them into environment variables, which prevents secret exposure in build logs or cache artifacts.

## Integration Points

- **GitHub Checks API**: Each job reports status to the PR check suite, enabling branch protection rules
- **Slack/Teams Notifications**: On failure workflows, a notification step alerts the team via webhook
- **Vercel**: Preview deployments triggered after successful CI on PRs
- **Docker Registry**: Build images pushed to GitHub Container Registry for deployment stages

## Production Considerations

1. **Cache key granularity**: Use OS + lockfile hash + SHA for cache keys. Too broad causes cache collisions, too narrow defeats caching.
2. **Runner labels**: Self-hosted runners for expensive E2E tests to reduce queue times on shared GitHub runners.
3. **Workflow dispatch triggers**: Allow manual re-runs with `workflow_dispatch` for flaky test retries without force-push.
4. **Step summaries**: Generate Markdown summaries with test results, coverage deltas, and build sizes that appear in the PR comment thread.
5. **OIDC authentication**: Use GitHub OIDC tokens for cloud provider authentication instead of long-lived service principal secrets.
6. **Action pinning**: Pin all third-party actions to full commit SHA (not version tags) to prevent supply chain attacks via tag mutation.
