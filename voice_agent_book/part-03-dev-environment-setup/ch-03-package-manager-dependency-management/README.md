# Chapter 03: Package Manager & Dependency Management

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [pnpm Workspace Configuration](sec-01-pnpm-workspace-configuration.md) | pnpm-workspace.yaml, catalog for shared versions, package filters, hoisting |
| 02 | [Dependency Versioning Strategy](sec-02-dependency-versioning-strategy.md) | Exact versions vs ranges, major version pinning, automated updates via Renovate |
| 03 | [Dependency Audit & Security](sec-03-dependency-audit-security.md) | pnpm audit, Snyk/Trivy scanning, dependency review in CI, CVE monitoring |
| 04 | [Lockfile Management](sec-04-lockfile-management.md) | pnpm-lock.yaml, lockfile validation in CI, merge conflicts resolution |
| 05 | [Peer Dependencies & Shared Packages](sec-05-peer-dependencies-shared-packages.md) | React, Next.js, TypeScript as peer deps, hoisting strategy |
| 06 | [Monorepo Scripts & Task Running](sec-06-monorepo-scripts-task-running.md) | Root package.json scripts, filtering (--filter), parallel execution, --continue |

---

## Key Takeaways

- pnpm for disk-efficient, fast package management with strict dependency isolation
- Renovate for automated dependency updates with grouping and scheduling
- pnpm audit in CI to fail builds on critical vulnerabilities
- Exact versions for production deps, ranges for dev deps
- Peer dependencies for shared framework packages (React, Next.js)
- Lockfile must be committed and validated in CI
