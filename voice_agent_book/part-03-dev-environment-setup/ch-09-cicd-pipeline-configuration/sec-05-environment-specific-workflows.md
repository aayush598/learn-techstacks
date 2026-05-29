# Section 05: Environment-Specific Workflows

## Overview

Different Git events trigger different pipeline workflows. PRs get a lightweight validation suite. Merges to main trigger full build and staging deployment. Nightly runs perform deep testing and security scanning. Production releases require manual dispatch with version tags. Each workflow is optimized for its trigger context.

## Workflow Trigger Map

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Workflow Dispatch Matrix                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Trigger              │  Workflow         │  Scope                │
│  ─────────────────────┼───────────────────┼──────────────────────│
│  PR opened/synced     │  PR Checks        │  Changed packages     │
│  PR labeled (deploy)  │  Preview Deploy   │  Single app           │
│  Push to main         │  CI + Stage       │  Full monorepo        │
│  Push to main (tag)   │  Production       │  Full + images        │
│  Schedule (nightly)   │  Deep Test        │  Full + security      │
│  Manual (dispatch)    │  Ad-hoc           │  Configurable         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## PR Checks Workflow

The PR workflow uses Turborepo's `--filter` to only run tasks for changed packages:

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main, develop]

concurrency:
  group: pr-${{ github.ref }}
  cancel-in-progress: true

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: filter
        uses: dorny/paths-filter@v3
        with:
          filters: |
            web: apps/web/**
            api: apps/api/**
            db: packages/db/**
            ui: packages/ui/**
            voice: packages/voice/**
            ai: packages/ai/**
            config: packages/config/**

  lint-typecheck:
    needs: [detect-changes]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: |
          PACKAGES="${{ needs.detect-changes.outputs.packages }}"
          if [ "$PACKAGES" != "[]" ]; then
            npx turbo lint typecheck --filter={./*}... --filter=$PACKAGES
          fi
```

The `dorny/paths-filter` action identifies changed packages by diffing against the base branch. This prevents running lint on `packages/db` when only `apps/web` changed. The trade-off is that cross-package changes (e.g., a shared type change) require running workflows for all affected consumers. The `...` suffix in Turborepo's filter handles this automatically by including dependents.

## Preview Deployment Workflow

When a PR is labeled `deploy`, a preview environment spins up:

```yaml
# .github/workflows/preview-deploy.yml
name: Preview Deploy
on:
  pull_request:
    types: [labeled]
    branches: [main, develop]

jobs:
  preview:
    if: ${{ github.event.label.name == 'deploy' }}
    environment:
      name: preview-${{ github.event.number }}
      url: https://pr-${{ github.event.number }}.voiceagent.example.com
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo build --filter=@voice-agent/web

      - name: Deploy to Vercel Preview
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prebuilt --token=${{ secrets.VERCEL_TOKEN }}"
          github-comment: true
          github-token: ${{ secrets.GITHUB_TOKEN }}

  cleanup:
    if: ${{ github.event.action == 'closed' }}
    runs-on: ubuntu-latest
    steps:
      - name: Teardown Preview
        run: |
          curl -X DELETE "https://api.vercel.com/v1/projects/.../aliases?teamId=..."
```

Preview environments are ephemeral — they deploy on label and tear down on PR close. Each preview gets a unique URL (`pr-123.voiceagent.example.com`) with its own database instance (spun up via a cloud PostgreSQL provider with automated teardown).

## Staging Deployment Workflow

The staging workflow triggers automatically after CI passes on main:

```yaml
# .github/workflows/staging.yml
name: Staging Deploy
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  deploy-staging:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - run: npx turbo build
      - name: Deploy
        run: ./scripts/deploy-staging.sh
      - name: Post-Deploy Tests
        run: npx playwright test --config=e2e/staging.config.ts
      - name: Notify
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Staging deployed: ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_STAGING }}
```

## Nightly Deep Test Workflow

A scheduled workflow runs comprehensive tests that are too expensive for every PR:

```yaml
# .github/workflows/nightly.yml
name: Nightly Deep Tests
on:
  schedule:
    - cron: "0 3 * * *"  # 3 AM daily

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - name: Dependency Audit
        run: pnpm audit --audit-level=high
      - name: SAST Scan
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:typescript"
      - name: Secret Detection
        uses: trufflesecurity/trufflehog@v3
        with:
          extra_args: --results=verified,unknown

  performance-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - name: Load Test
        run: |
          docker run --rm -v $PWD/scripts:/scripts grafana/k6 run /scripts/load-test.js

  database-migration-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup
      - name: Test Migrations
        run: |
          npx prisma migrate deploy
          npx prisma migrate resolve --applied "test_migration"
```

The nightly workflow is split into three parallel jobs: security scanning (CodeQL + trufflehog), performance testing (k6), and database migration testing (verifies that migrations apply cleanly against a fresh database).

## Production Deployment Workflow

Production requires a manually triggered workflow with a version tag:

```yaml
# .github/workflows/production.yml
name: Production Deploy
on:
  push:
    tags:
      - "v*.*.*"

jobs:
  validate-tag:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          # Validate tag matches semantic versioning
          if ! [[ $GITHUB_REF_NAME =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Invalid version tag: $GITHUB_REF_NAME"
            exit 1
          fi
          # Validate CHANGELOG has entry for this version
          grep -q "## \[${GITHUB_REF_NAME#v}\]" CHANGELOG.md || {
            echo "Missing CHANGELOG entry for $GITHUB_REF_NAME"
            exit 1
          }

  deploy:
    needs: [validate-tag]
    uses: ./.github/workflows/deploy.yml
    secrets: inherit
```

The production workflow is triggered by pushing a version tag (`v1.2.3`). It validates the tag format and changelog before calling the shared deploy workflow.

## Integration Points

- **GitHub Environments**: Each environment (preview, staging, production) has its own secret set, approval rules, and deployment history
- **Vercel**: Preview deployments use the Vercel API for instant branch-based hosting
- **Slack**: Notifications differentiate by environment — staging gets the team channel, production gets the on-call channel
- **Docker Registry**: Each environment pulls from tagged images, never from `latest`

## Production Considerations

1. **Workflow dispatch triggers**: All workflows support `workflow_dispatch` for manual triggering. This is essential for hotfixes that bypass the normal PR flow.
2. **Branch protection**: Production deploys only from `main`, staging deploys from `main` and `develop`, preview deploys from any PR branch.
3. **Secret scoping**: Each environment has isolated secrets. A preview environment compromise does not expose staging or production credentials.
4. **Cleanup schedules**: Preview environments auto-remove after 24 hours via a cleanup cron. Stale previews accumulate and cost money if not pruned.
5. **Rate limiting**: The Vercel API has rate limits. Batch preview deployments if multiple PRs trigger simultaneously.
6. **Observability tags**: Every deployment tags logs and metrics with the environment name, commit SHA, and deployer identity for traceability.
