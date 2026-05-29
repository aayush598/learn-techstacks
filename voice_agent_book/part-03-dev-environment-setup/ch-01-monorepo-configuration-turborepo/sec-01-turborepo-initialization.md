# Section 01: Turborepo Initialization

## Overview

Turborepo provides the build orchestration foundation for our voice agent platform monorepo. It delivers incremental builds, parallel task execution, and both local and remote caching that dramatically reduce CI times. This section covers project scaffolding, workspace configuration with pnpm, and the turbo.json pipeline definition.

## Why Turborepo

Before adopting Turborepo, teams typically use one of three approaches: a single giant package with no separation of concerns, Lerna with npm/yarn workspaces, or Nx with its more opinionated structure. Turborepo wins for our use case because:

- **Incremental builds**: Only rebuild what changed, using content-aware hashing
- **Parallel execution**: Run tasks across packages in topological order with maximum parallelism
- **Remote caching**: Share build artifacts across team members and CI (Vercel Remote Cache)
- **Zero configuration overhead**: Sensible defaults that work with existing package managers
- **Humble design philosophy**: No code generation, no custom package manager — just a task runner

```text
┌─────────────────────────────────────────────────────┐
│                  Turborepo Pipeline                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Input Files → Content Hash → Cache Lookup          │
│                      │                               │
│              ┌───────┴───────┐                      │
│              │               │                       │
│           Cache Hit     Cache Miss                   │
│              │               │                       │
│         Restore           Execute                    │
│         Artifacts         Task                       │
│              │               │                       │
│              └───────┬───────┘                      │
│                      │                               │
│                  Store Output                        │
│                  (Local + Remote)                    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Project Scaffolding

The initialization begins with creating the root project structure and configuring pnpm workspaces alongside Turborepo.

```bash
# Create monorepo root
mkdir voice-agent-platform && cd voice-agent-platform
pnpm init

# Install Turborepo
pnpm add -D turbo@latest --workspace-root

# Create workspace structure
mkdir -p apps/web apps/api
mkdir -p packages/ui packages/db packages/voice packages/ai packages/config
```

### Root package.json

```jsonc
{
  "name": "voice-agent-platform",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "test": "turbo test",
    "typecheck": "turbo typecheck",
    "clean": "turbo clean",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\""
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "prettier": "^3.2.0"
  },
  "packageManager": "pnpm@9.1.0",
  "engines": {
    "node": ">=20.11.0",
    "pnpm": ">=9.1.0"
  }
}
```

## turbo.json Pipeline Definition

The pipeline defines how tasks relate to each other, their caching behavior, and execution order. This is the heart of Turborepo configuration.

```jsonc
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    "**/.env.*local",
    "tsconfig.json",
    "tsconfig.base.json"
  ],
  "globalDotEnv": [
    ".env",
    ".env.local"
  ],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "src/**/*.json",
        "tsconfig.json"
      ],
      "outputs": [
        ".next/**",
        "dist/**",
        "build/**"
      ],
      "env": [
        "NEXT_PUBLIC_*",
        "DATABASE_URL",
        "REDIS_URL",
        "KAFKA_BROKERS"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        ".eslintrc*"
      ]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "tsconfig.json"
      ]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "src/**/*.test.ts",
        "src/**/*.spec.ts"
      ],
      "outputs": []
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Pipeline Design Decisions

**dependsOn with ^ prefix**: The `^build` syntax means "wait for all upstream dependencies to build first." This ensures topological ordering — `packages/db` builds before `apps/api` that depends on it.

**inputs**: Narrow input globs prevent unnecessary cache invalidations. If we used `src/**/*` it would include images, SVGs, and other files that don't affect the TypeScript build output. By listing only compilation-relevant files we maximize cache hits.

**outputs**: Explicit output directories tell Turborepo what to cache. For Next.js apps, we cache `.next` and `dist`. For packages, `dist` or `build`. Missing output declarations means nothing gets cached.

**env**: Declaring environment variables as dependencies ensures that changing `DATABASE_URL` invalidates the build cache. This prevents stale build artifacts when configuration changes.

## Workspace Configuration (pnpm)

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

The pnpm workspace file tells pnpm where to find workspace packages. Combined with Turborepo, it provides:

- **Hoisting control**: pnpm's node_modules structure prevents phantom dependencies
- **Filtered operations**: `pnpm --filter @voice-agent/web add some-package`
- **Catalog support**: Shared version pins across the monorepo

## Remote Caching Setup

Remote caching is configured via the `turbo` CLI or `turbo.json`:

```bash
# Link remote cache (Vercel)
npx turbo link

# Or configure via environment
export TURBO_TOKEN=your_token
export TURBO_TEAM=your_team
export TURBO_REMOTE_ONLY=true
```

```jsonc
// .gitignore additions
.turbo
node_modules
dist
.next
```

## Integration Points

Turborepo integrates with:

- **pnpm workspaces**: Uses the same workspace topology for dependency resolution
- **Git**: Uses git timestamps and content hashes for cache invalidation
- **CI/CD**: GitHub Actions, CircleCI, and others — cache is shared across runs
- **Vercel**: Native integration for deployments and remote caching
- **VS Code**: The Turborepo extension provides pipeline visualization

## Production Considerations

1. **Cache poisoning prevention**: Use `TURBO_REMOTE_ONLY=false` in development and `TURBO_REMOTE_ONLY=true` in CI to ensure cache consistency
2. **Cache size limits**: Remote caches can grow large. Set up TTL policies on your Vercel dashboard
3. **Pipeline strictness**: Use `"inputs"` and `"outputs"` aggressively to avoid false cache misses
4. **Global hash**: Add `tsconfig.base.json` and root `.eslintrc` to `globalDependencies` to trigger full rebuilds when shared config changes
5. **Environment variables**: Always declare env vars in pipeline tasks — forgetting one can produce subtly broken builds from cache
