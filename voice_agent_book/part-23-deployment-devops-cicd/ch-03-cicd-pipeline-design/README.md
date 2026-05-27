# Chapter 03: CI/CD Pipeline Design

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [GitHub Actions Pipeline Architecture](sec-01-github-actions-pipeline-architecture.md) | Workflow structure, job dependencies, matrix builds, reusable workflows, environment secrets |
| 02 | [Build Caching Strategy](sec-02-build-caching-strategy.md) | Dependency caching, Docker layer caching, Next.js build caching, Turbo repo caching |
| 03 | [Parallel Job Execution](sec-03-parallel-job-execution.md) | Job concurrency, dependency graph, artifact sharing, test sharding |
| 04 | [Environment Promotion](sec-04-environment-promotion.md) | Dev → Staging → Production promotion, approval gates, environment parity, promotion automation |
| 05 | [Approval Gates & Manual Interventions](sec-05-approval-gates-manual-interventions.md) | Required reviewers, environment approval, deployment freeze, emergency bypass |
| 06 | [Testing in CI Pipeline](sec-06-testing-ci-pipeline.md) | Unit/integration/E2E test stages, parallel test execution, test reporting, flaky test management |
| 07 | [Artifact Management](sec-07-artifact-management.md) | Build artifacts, Docker image registry, npm package publishing, version tagging |
| 08 | [Pipeline Monitoring & Metrics](sec-08-pipeline-monitoring-metrics.md) | Pipeline duration tracking, pass/fail rates, flaky test detection, deployment frequency |
