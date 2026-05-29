# Section 03: Deployment Pipeline

## Overview

The deployment pipeline promotes builds through three environments — development, staging, and production — with automated testing gates and manual approval checkpoints. Each environment has distinct configuration, scaling characteristics, and observability requirements. The pipeline is designed for zero-downtime deployments with instant rollback capability.

## Environment Promotion Model

```text
┌──────────────────────────────────────────────────────────────┐
│                  Environment Promotion Flow                    │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Git: main branch merge                                        │
│       │                                                        │
│       ▼                                                        │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Build       │───▶│  Push Image  │───▶│  Deploy Dev  │      │
│  │  + Test      │    │  to GHCR     │    │  (Automatic) │      │
│  └─────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│                                          ┌──────────────┐      │
│                                          │  Smoke Tests  │      │
│                                          │  (Automated)  │      │
│                                          └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│                                          ┌──────────────┐      │
│                                          │  Deploy Stg   │      │
│                                          │  (Automatic)  │      │
│                                          └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│                                          ┌──────────────┐      │
│                                          │  E2E Tests    │      │
│                                          │  + Load Test  │      │
│                                          └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│                                          ┌──────────────┐      │
│                                          │  Approval     │◀─────│── Slack Approval Request
│                                          │  Gate         │      │
│                                          └──────┬───────┘      │
│                                                  │              │
│                                                  ▼              │
│                                          ┌──────────────┐      │
│                                          │  Deploy Prod  │      │
│                                          │  (Canary)    │      │
│                                          └──────────────┘      │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

## Deployment Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_run:
    workflows: ["CI"]
    types:
      - completed
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup

      - name: Build Application
        run: npx turbo build

      - name: Docker Metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=sha-
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-dev:
    needs: [build-and-push]
    environment:
      name: development
      url: https://dev.voiceagent.example.com
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Dev
        run: |
          echo "Deploying ${{ needs.build-and-push.outputs.image-tag }} to dev"
          # kubectl set image or docker compose up
      - name: Smoke Tests
        run: |
          curl --retry 10 --retry-delay 5 https://dev.voiceagent.example.com/api/health

  deploy-staging:
    needs: [deploy-dev]
    environment:
      name: staging
      url: https://staging.voiceagent.example.com
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: ./scripts/deploy-staging.sh
      - name: E2E Tests
        run: npx playwright test --config=e2e/staging.config.ts
      - name: Load Test
        run: |
          k6 run scripts/load-test.js
          # Fail if p95 > 500ms

  deploy-production:
    needs: [deploy-staging]
    environment:
      name: production
      url: https://voiceagent.example.com
    runs-on: ubuntu-latest
    steps:
      - name: Canary Deploy (10%)
        run: ./scripts/deploy-canary.sh --percentage=10
      - name: Wait for Observability
        run: |
          # Monitor error rate for 5 minutes
          ./scripts/watch-error-rate.sh --timeout=300 --threshold=0.01
      - name: Full Rollout
        run: ./scripts/deploy-full.sh
```

## Approval Gates

Staging deploys automatically. Production requires a manual approval via GitHub Environments:

```yaml
# Environment configuration (set in GitHub UI)
# production:
#   Required reviewers: [team-leads]
#   Wait timer: 0 minutes
#   Deployment branches: [main]
```

The design choice of **manual approval for production, automatic for staging** balances speed and safety. Staging gets the latest code immediately for team testing. Production waits for explicit sign-off, preventing Friday-afternoon deployments without review.

## Rollback Strategy

```bash
# scripts/rollback.sh
#!/bin/bash
ENVIRONMENT=$1
PREVIOUS_TAG=$(gh deployment list --environment "$ENVIRONMENT" --json "task,payload" --jq '.[1].payload.tag')

case $ENVIRONMENT in
  production)
    # Rollback canary first, then full
    kubectl rollout undo deployment/voice-agent-api -n production
    kubectl rollout undo deployment/voice-agent-web -n production
    ;;
  staging)
    docker compose -f docker-compose.staging.yml up -d --force-recreate
    ;;
  development)
    kubectl rollout undo deployment/voice-agent-dev -n development
    ;;
esac

# Verify rollback health
./scripts/wait-for-health.sh "$ENVIRONMENT"
```

The rollback uses Kubernetes `rollout undo` for production, which reverts to the previous ReplicaSet. This is nearly instantaneous and preserves the deployment history. For staging, Docker Compose restarts with the previous image tag.

## Blue-Green vs Canary

| Strategy | Downtime | Risk | Complexity | Rollback Time |
|----------|----------|------|------------|---------------|
| Blue-Green | None | High (all-or-nothing) | Medium | Fast (DNS) |
| Canary (10%→100%) | None | Low (gradual) | High | Medium |
| Rolling Update | None | Medium | Low | Fast (undo) |

Our choice: **Canary for production, rolling for staging**. Production gets a 10% traffic canary for 5 minutes of error-rate observation, then a full rollout. Staging uses a rolling update because staging has fewer traffic concerns and the deployment must be fast.

## Integration Points

- **Docker Registry**: Images pushed to GitHub Container Registry with SHA-based tags for immutability
- **Kubernetes**: Deployments managed via kubectl with manifests in a separate `infra/` directory
- **Doppler**: Secrets injected at deploy time, never baked into Docker images
- **Datadog/Grafana**: Deploy annotations mark the timeline for correlation with metrics
- **Slack**: Deploy notifications with links to the release page and commit log

## Production Considerations

1. **Immutable tags**: Never reuse Docker tags. Every deploy gets a unique SHA-based tag. Reusing `latest` makes rollback ambiguous.
2. **Database migrations**: Run migrations as a separate job before the app deployment. Use `prisma migrate deploy` with connection pooling to avoid locking.
3. **Feature flags**: Decouple deploy from release. Use LaunchDarkly or a custom flag system to gate new features even after deployment.
4. **Deploy freeze windows**: Calendar-based blocks (holiday seasons, major events) prevent deployments during high-risk periods.
5. **Audit trail**: Every deployment is logged with commit SHA, deployer identity, timestamp, and promotion path. This is critical for post-incident analysis.
6. **Health check endpoints**: Every service exposes `/api/health` (liveness) and `/api/ready` (readiness) for orchestrator health monitoring.
