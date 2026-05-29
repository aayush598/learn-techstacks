# Section 02: Dependency Versioning Strategy

## Overview

A consistent dependency versioning strategy prevents the "it works on my machine" problem, ensures reproducible builds, and simplifies security updates. This section covers the decision between exact versions and ranges, major version pinning, and automated updates via Renovate.

## Versioning Philosophy

```text
┌─────────────────────────────────────────────────────────────┐
│                 Dependency Versioning Strategy                │
│                                                              │
│  ┌───────────────────┐          ┌───────────────────────┐   │
│  │ Production deps    │          │ Dev dependencies       │   │
│  │                    │          │                        │   │
│  │  Exact versions    │          │  Caret ranges (^)      │   │
│  │  (e.g., 5.12.3)    │          │  (e.g., ^5.12.0)      │   │
│  │                    │          │                        │   │
│  │  Predictable       │          │  Flexible updates      │   │
│  │  Reproducible      │          │  Latest tooling        │   │
│  └───────────────────┘          └───────────────────────┘   │
│                                                              │
│  Lockfile (pnpm-lock.yaml) pins transitive deps             │
│  Renovate automates major/minor updates                     │
│  Major versions require manual review                       │
└─────────────────────────────────────────────────────────────┘
```

## Exact Versions for Production Dependencies

```jsonc
{
  "dependencies": {
    // Production deps use exact versions
    "next": "14.2.3",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "zod": "3.23.8",
    "@prisma/client": "5.14.0",
    "@radix-ui/react-dialog": "1.0.5"
  },
  "devDependencies": {
    // Dev deps use caret ranges
    "typescript": "^5.4.5",
    "vitest": "^1.6.0",
    "eslint": "^8.57.0",
    "prettier": "^3.2.5",
    "@types/react": "^18.3.3",
    "@types/node": "^20.14.0"
  }
}
```

### Rationale

**Production deps (exact versions)**: A patch update to Next.js (14.2.3 → 14.2.4) could theoretically change behavior. Exact versions ensure that `pnpm install` always produces byte-identical `node_modules`, guaranteeing reproducible builds. The lockfile pins transitive deps, but exact versions for direct deps add an extra layer of predictability.

**Dev deps (caret ranges)**: Dev dependencies don't affect production runtime. Allowing minor/patch updates keeps tooling current without manual intervention. The lockfile still ensures consistency within a given install.

## pnpm Catalog for Shared Versions

```yaml
# pnpm-workspace.yaml
catalog:
  # Production deps (exact)
  next: 14.2.3
  react: 18.3.1
  react-dom: 18.3.1
  zod: 3.23.8
  "@prisma/client": 5.14.0

  # Dev deps (ranges)
  typescript: ^5.4.5
  vitest: ^1.6.0
  eslint: ^8.57.0
  prettier: ^3.2.5
  "@types/node": ^20.14.0

  # Shared across workspaces
  "@voice-agent/config-typescript": workspace:*
  "@voice-agent/config-eslint": workspace:*
```

With catalogs, changing a version once in `pnpm-workspace.yaml` updates it across all workspaces:

```bash
# Update Next.js in all workspaces
# Edit pnpm-workspace.yaml: next: 14.2.4
pnpm install
```

## Renovate Configuration

Renovate automates dependency updates with intelligent grouping and scheduling:

```jsonc
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "group:allNonMajor",
    "schedule:weekly",
    ":separateMajorMinor",
    ":combinePatchMinorUpdates"
  ],
  "labels": ["dependencies"],
  "prConcurrentLimit": 5,
  "packageRules": [
    {
      // Production deps — manual review, weekly grouping
      "matchDepTypes": ["dependencies"],
      "matchUpdateTypes": ["major"],
      "labels": ["dependency-major"],
      "assignees": ["@tech-lead"],
      "reviewers": ["@tech-lead"],
      "automerge": false
    },
    {
      // Production deps — minor/patch can auto-merge
      "matchDepTypes": ["dependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      // Dev deps — auto-merge all non-major
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      // Major dev deps — schedule monthly
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["major"],
      "schedule": ["before 9am on the first day of the month"],
      "labels": ["dev-dependency-major"]
    },
    {
      // Framework packages — manual review always
      "matchPackageNames": [
        "next",
        "react",
        "react-dom",
        "typescript"
      ],
      "automerge": false,
      "reviewers": ["@tech-lead", "@senior-dev"]
    },
    {
      // Security updates — fast-track
      "matchUpdateTypes": ["pin", "digest", "patch"],
      "matchCategories": ["security"],
      "automerge": true,
      "automergeType": "pr",
      "schedule": ["at any time"],
      "prPriority": 10
    },
    {
      // Monorepo internal packages — separate group
      "matchPackagePrefixes": ["@voice-agent/"],
      "enabled": false
    }
  ],
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "schedule": ["at any time"]
  },
  "lockFileMaintenance": {
    "enabled": true,
    "schedule": ["before 9am on Monday"]
  }
}
```

## Major Version Upgrade Process

```text
┌─────────────────────────────────────────────────────────────┐
│              Major Version Upgrade Process                    │
│                                                              │
│  1. Renovate creates PR with major update                   │
│  2. Automated CI runs: lint → typecheck → test → build      │
│  3. Manual code review required                             │
│  4. Check changelog for breaking changes                    │
│  5. Update all affected code paths                          │
│  6. Run full test suite                                     │
│  7. Deploy to staging for validation                        │
│  8. Monitor in staging for 24 hours                         │
│  9. Approve and merge                                       │
│  10. Monitor production after deploy                        │
│                                                              │
│  Typical timeline: 1-3 days for framework packages          │
│                    < 1 day for library packages              │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Update Automation

```bash
# Commands for manual dependency management

# Check which dependencies are outdated
pnpm outdated -r

# Update all dependencies to latest within ranges
pnpm update -r --latest

# Update a specific dependency across all workspaces
pnpm update -r zod

# Check why a specific version is installed
pnpm why zod

# List all installed packages with versions
pnpm ls -r --depth=0
```

## Version Locking Strategy

```bash
# Force exact versions (if save-exact is set in .npmrc)
pnpm config set save-exact true

# Alternatively, set in root .npmrc
# save-exact=true
```

For yarn/npm users migrating to pnpm, the `save-exact` setting ensures `pnpm add` always writes exact versions to `package.json`.

## Design Decisions

### Why exact versions for production deps?

1. **Reproducibility**: `pnpm install --frozen-lockfile` + exact versions = deterministic builds
2. **Auditability**: Every production dependency is pinned to a specific version. When auditing, you know exactly what's running
3. **Rollback**: If a patch update introduces a bug, exact versions make it trivial to revert

### Why ranges for dev deps?

Dev tools like TypeScript, ESLint, and Vitest improve frequently. Minor updates often bring performance improvements and bug fixes. Ranges allow these benefits without manual PRs for every patch.

## Integration Points

- **Renovate**: Automated PR creation for dependency updates
- **GitHub Dependabot**: Alternative or complement to Renovate for security alerts
- **CI pipeline**: `pnpm install --frozen-lockfile` ensures lockfile consistency
- **Vulnerability scanning**: `pnpm audit` in CI fails on critical vulnerabilities

## Production Considerations

1. **Lockfile freshness**: CI should fail if the lockfile is out of date. Use `pnpm install --frozen-lockfile` or `--fail-if-lockfile-changed`
2. **Breaking changes**: Major version updates of Next.js or React require comprehensive testing. Keep a staging environment that mirrors production for validation
3. **Deprecation notices**: Monitor `pnpm audit` output for deprecated packages. Renovate's `vulnerabilityAlerts` surfaces CVEs automatically
4. **Peer dependency conflicts**: With strict peer deps enabled, any mismatch causes install failures. Catalogs help by ensuring consistent versions
5. **Bundle size**: Use `pnpm why <package>` to investigate why a large dependency is included. Tools like `bundlesize` or `size-limit` can prevent bundle bloat
