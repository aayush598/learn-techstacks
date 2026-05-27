# Chapter 09: CI/CD Pipeline Configuration

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [GitHub Actions Workflow Design](sec-01-github-actions-workflow-design.md) | Workflow organization, reusable workflows, matrix builds, concurrency groups |
| 02 | [Build & Test Pipeline](sec-02-build-test-pipeline.md) | Install → Lint → Type Check → Unit Test → Build → Integration Test → E2E Test |
| 03 | [Deployment Pipeline](sec-03-deployment-pipeline.md) | Environment promotion (dev → staging → prod), approval gates, rollback capability |
| 04 | [Caching Strategy](sec-04-caching-strategy.md) | pnpm store cache, Turborepo remote cache, Docker layer caching, dependency caching |
| 05 | [Environment-Specific Workflows](sec-05-environment-specific-workflows.md) | PR checks, staging deploy, production deploy, nightly tests, security scans |
| 06 | [Quality Gates & Artifacts](sec-06-quality-gates-artifacts.md) | Coverage thresholds, lint errors, type errors, bundle size, build artifacts |

---

## Pipeline Stages

```
PR Opened → Lint → TypeCheck → Unit Tests → Build → Integration Tests → Preview Deploy
PR Merged → Build → Test → Staging Deploy → E2E Tests → Approval → Production Deploy
```

---

## Key Takeaways

- CI runs on every PR: lint, type check, test, build
- CD: Automatic staging deploy with E2E tests, manual approval for production
- Turborepo remote caching for 80%+ cache hit rates in CI
- pnpm store cached between runs for fast installs
- Quality gates block builds that fail coverage or lint thresholds
- Preview deployments for every PR via Vercel/VPS
