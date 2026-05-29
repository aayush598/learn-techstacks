# Section 06: CI/CD Environment Injection

## Overview

CI/CD pipelines need access to environment variables to build, test, and deploy applications. This section covers how secrets and configuration are injected into GitHub Actions workflows, how environment protection rules prevent accidental production deployments, and how PR preview environments get isolated secrets.

## Secrets Injection Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              CI/CD Secret Injection Flow                      │
│                                                              │
│  ┌──────────────┐                                           │
│  │ GitHub        │                                           │
│  │ Actions       │                                           │
│  │ Secrets Store │                                           │
│  └──────┬───────┘                                           │
│         │                                                     │
│         ▼                                                     │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │ Environment:      │    │ Environment:      │               │
│  │ Development       │    │ Production        │               │
│  │                   │    │                   │               │
│  │ TURBO_TOKEN       │    │ DOPPLER_TOKEN     │               │
│  │ DOPPLER_TOKEN_DEV │    │ PROD              │               │
│  │ VAULT_ROLE_ID     │    │ VAULT_ROLE_ID     │               │
│  │ VAULT_SECRET_ID   │    │ VAULT_SECRET_ID   │               │
│  │                   │    │                   │               │
│  │ PR Checks:        │    │ Approvals:        │               │
│  │   Lint ✓          │    │   Tech Lead ✓     │               │
│  │   Test ✓          │    │   QA Lead ✓       │               │
│  └──────────────────┘    └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## GitHub Actions Environment Setup

```yaml
# .github/environments/production.yml
name: production
environment:
  deployment_branch: main
  required_reviewers:
    - tech-lead
    - qa-lead
  required_deployments:
    - staging
  secrets:
    - DOPPLER_TOKEN_PROD
    - VAULT_ROLE_ID
    - VAULT_SECRET_ID
    - DOCKER_REGISTRY_PASSWORD
  vars:
    NODE_ENV: production
    LOG_LEVEL: info
```

## Workflow Environment Injection

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ── Non-production jobs ──────────────────────────────────
  lint-and-test:
    runs-on: ubuntu-latest
    environment: development
    env:
      NODE_ENV: test
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint
        env:
          NODE_ENV: development

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test
        env:
          # Test-specific env vars
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379

  # ── Staging deploy ───────────────────────────────────────
  deploy-staging:
    needs: [lint-and-test]
    runs-on: ubuntu-latest
    environment: staging
    concurrency: staging
    env:
      NODE_ENV: production
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4

      - name: Inject Doppler secrets
        uses: dopplerhq/cli-action@v3
        with:
          setup: |
            echo "DOPPLER_TOKEN=${{ secrets.DOPPLER_TOKEN_STAGING }}" >> $GITHUB_ENV

      - name: Build
        run: doppler run -- pnpm build

      - name: Deploy to staging
        run: |
          doppler run -- \
            ./scripts/deploy.sh staging

  # ── Production deploy ────────────────────────────────────
  deploy-production:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.voiceagent.example.com
    concurrency: production
    env:
      NODE_ENV: production
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4

      - name: Inject production secrets
        uses: dopplerhq/cli-action@v3
        with:
          setup: |
            echo "DOPPLER_TOKEN=${{ secrets.DOPPLER_TOKEN_PROD }}" >> $GITHUB_ENV

      - name: Build
        run: doppler run -- pnpm build

      - name: Deploy to production
        run: |
          doppler run -- \
            ./scripts/deploy.sh production
```

## Environment Protection Rules

```yaml
# .github/environments/development.yml
name: development
environment:
  deployment_branch: '*'
  # No approval required for dev

# .github/environments/staging.yml
name: staging
environment:
  deployment_branch: main
  required_reviewers:
    - tech-lead
  # Automatic deploy on main merge

# .github/environments/production.yml
name: production
environment:
  deployment_branch: main
  required_reviewers:
    - tech-lead
    - qa-lead
  wait_timer: 300  # 5-minute cooldown after staging deploy
  required_deployments:
    - staging
  prevent_self_review: true
```

## PR Preview Environments

Preview environments provide isolated deployments for each PR with their own secrets:

```yaml
# .github/workflows/preview.yml
name: Preview Deploy
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    environment:
      name: preview
      url: https://pr-${{ github.event.number }}.voiceagent.preview.example.com

    env:
      NODE_ENV: preview
      PR_NUMBER: ${{ github.event.number }}

    steps:
      - uses: actions/checkout@v4

      - name: Generate preview secrets
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_PREVIEW }}
        run: |
          # Create isolated preview environment
          doppler setup --project voice-agent --config pr-${{ env.PR_NUMBER }}
          doppler secrets set \
            APP_URL=https://pr-${{ env.PR_NUMBER }}.voiceagent.preview.example.com \
            API_URL=https://api-pr-${{ env.PR_NUMBER }}.voiceagent.preview.example.com

      - name: Deploy preview
        run: |
          doppler run --config pr-${{ env.PR_NUMBER }} -- \
            ./scripts/deploy-preview.sh ${{ env.PR_NUMBER }}

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview environment deployed: https://pr-${process.env.PR_NUMBER}.voiceagent.preview.example.com`
            })
```

## CI-Specific Environment Configuration

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}
      # CI-specific optimization
      NEXT_TELEMETRY_DISABLED: 1
      CI: true
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test
        env:
          NODE_ENV: test
          # Test containers spin up their own services
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
          TESTCONTAINERS: true

      - name: Build
        run: pnpm build
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          NEXT_PUBLIC_SENTRY_DSN: ${{ secrets.SENTRY_DSN }}
```

## Secret Rotation in CI

```yaml
# .github/workflows/rotate-ci-secrets.yml
name: Rotate CI Secrets
on:
  schedule:
    - cron: '0 0 1 */3 *'   # Quarterly
  workflow_dispatch:

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Rotate secrets
        run: |
          # Generate new secrets
          NEW_TURBO_TOKEN=$(openssl rand -hex 32)
          NEW_DOPPLER_TOKEN=$(doppler tokens create --config prod)

          # Update GitHub secrets
          gh secret set TURBO_TOKEN --body "$NEW_TURBO_TOKEN" --app actions
          gh secret set DOPPLER_TOKEN_PROD --body "$NEW_DOPPLER_TOKEN" --app actions

          # Update environment-specific secrets
          gh secret set TURBO_TOKEN --env production --body "$NEW_TURBO_TOKEN"
```

## Environment Variable Precedence in CI

```text
GitHub Actions Variable Resolution:
1. Repository secrets (lowest priority)
2. Environment secrets (medium priority)
3. Organization secrets (high priority)
4. Step-level env (highest)

Example:
┌────────────────────────────────────────────┐
│  Organization Secrets:                      │
│    NODE_AUTH_TOKEN (org-wide)              │
├────────────────────────────────────────────┤
│  Repository Secrets:                        │
│    DOPPLER_TOKEN_DEV                       │
│    DOPPLER_TOKEN_STAGING                   │
│    DOPPLER_TOKEN_PROD                      │
├────────────────────────────────────────────┤
│  Environment: development                   │
│    TURBO_TOKEN                              │
│    NEXT_PUBLIC_API_URL                      │
├────────────────────────────────────────────┤
│  Environment: production                    │
│    TURBO_TOKEN (overrides repo default)    │
│    VAULT_ROLE_ID                            │
│    VAULT_SECRET_ID                          │
└────────────────────────────────────────────┘
```

## Design Decisions

### Doppler/Vault vs. GitHub Secrets Only

**Decision**: Use GitHub Actions secrets for CI-specific tokens (TURBO_TOKEN, DOPPLER_TOKEN), and inject actual application secrets via Doppler/Vault.

**Rationale**: GitHub secrets are awkward to manage at scale — they can't be grouped by environment easily, lack audit trails, and have size limits. Doppler provides a better UX for managing hundreds of secrets across multiple environments.

### Environment protection vs. branch protection

**Decision**: Use GitHub Environments with required reviewers for production deployments, combined with branch protection rules requiring PRs to main.

**Rationale**: Branch protection prevents unauthorized merges. Environment protection prevents unauthorized deployments. Together they provide defense in depth. A malicious actor would need to bypass both code review AND deployment approval.

## Integration Points

- **GitHub Actions**: Secrets injected via `${{ secrets.* }}` and `${{ vars.* }}`
- **Doppler**: CLI injects secrets into workflow steps
- **Vault**: GitHub Action `hashicorp/vault-action` authenticates and fetches secrets
- **PR comments**: Preview URLs posted to PRs for review

## Production Considerations

1. **Secret storage at rest**: GitHub encrypts secrets with AES-256. Doppler/Vault use additional encryption layers. Ensure compliance requirements (SOC2, HIPAA) are met
2. **Audit logging**: GitHub Audit Log tracks who modified secrets. Set up alerts for secret modifications
3. **Secret size limits**: GitHub secrets are limited to 64KB. For larger configurations, use Doppler/Vault references
4. **Fallback strategy**: If Doppler/Vault is unreachable during deployment, fail the build. Never deploy with default or fallback secrets
5. **Cleanup**: Preview environment secrets should be cleaned up when the PR is closed. Use a workflow triggered on `pull_request: closed` to delete secrets
