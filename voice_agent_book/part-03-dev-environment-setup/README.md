# Part 03: Development Environment & Project Setup

> **Duration:** Setup Phase (Weeks 3-4)  
> **Goal:** Establish a production-ready development environment, monorepo tooling, and engineering conventions.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Monorepo Configuration with Turborepo](ch-01-monorepo-configuration-turborepo/README.md) | Turborepo setup, workspace configuration, shared packages, build caching |
| 02 | [TypeScript Configuration & Strict Mode](ch-02-typescript-configuration-strict-mode/README.md) | Strict TS config, path aliases, shared types, declaration files |
| 03 | [Package Manager & Dependency Management](ch-03-package-manager-dependency-management/README.md) | pnpm workspaces, lockfile strategy, dependency audit, version pinning |
| 04 | [Environment Variables & Secrets Management](ch-04-environment-variables-secrets/README.md) | .env strategy, validation (Zod), secret rotation, Doppler/Vault integration |
| 05 | [Linting, Formatting & Pre-commit Hooks](ch-05-linting-formatting-precommit/README.md) | ESLint, Prettier, Husky, lint-staged, commitlint, editorconfig |
| 06 | [Docker Development Environment](ch-06-docker-development-environment/README.md) | Docker Compose for local services, DevContainers, multi-stage builds |
| 07 | [Local Database & Service Orchestration](ch-07-local-database-service-orchestration/README.md) | PostgreSQL, Redis, Kafka, MinIO setup locally, seed data scripts |
| 08 | [Testing Infrastructure Setup](ch-08-testing-infrastructure-setup/README.md) | Vitest, Playwright, MSW, testing utilities, coverage configuration |
| 09 | [CI/CD Pipeline Configuration](ch-09-cicd-pipeline-configuration/README.md) | GitHub Actions, build/test/deploy stages, caching, conditional workflows |
| 10 | [Project Conventions & Coding Standards](ch-10-project-conventions-coding-standards/README.md) | Naming conventions, folder structure, API design patterns, code review guidelines |

---

## Development Workflow

```
git clone → pnpm install → docker compose up → pnpm dev
     ↓
Write code → lint → test → commit → push → CI passes → deploy
```

---

## Key Open-Source Tools

- **Turborepo** (MIT) — Monorepo build system
- **pnpm** (MIT) — Fast, disk-efficient package manager
- **Zod** (MIT) — Schema validation
- **Husky** (MIT) — Git hooks
- **Vitest** (MIT) — Unit testing
- **Playwright** (Apache 2.0) — E2E testing
- **MSW** (MIT) — API mocking

---

## Learning Objectives

- Set up a performant monorepo with shared packages and build caching
- Configure TypeScript for maximum safety without sacrificing developer experience
- Implement a robust environment variable and secrets management strategy
- Create reproducible local development environments with Docker
- Build a comprehensive CI/CD pipeline that catches issues early
- Establish coding conventions that scale across a large engineering team
