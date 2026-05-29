# Section 03: Build Pipeline Configuration

## Overview

Turborepo's pipeline configuration defines how tasks are scheduled, cached, and executed across the monorepo. A well-tuned pipeline is the difference between a 30-second CI and a 3-minute CI. This section covers task dependencies, output caching, remote caching, parallel execution, and input/output contracts.

## Pipeline Architecture

```text
         ┌─────────────────────────────────────────────┐
         │              Turborepo Pipeline              │
         │                                              │
         │  ┌──────────┐    ┌──────────┐               │
         │  │  lint     │    │ typecheck │               │
         │  │ (parallel)│    │ (parallel)│               │
         │  └─────┬─────┘    └─────┬─────┘               │
         │        │                 │                     │
         │  ┌─────┴─────────────────┴─────┐              │
         │  │         build                │              │
         │  │   (depends on ^build)        │              │
         │  └─────┬─────────────────┬─────┘              │
         │        │                 │                     │
         │  ┌─────┴─────┐    ┌──────┴──────┐             │
         │  │   test     │    │ integration │             │
         │  │ (unit)     │    │    test     │             │
         │  └─────┬─────┘    └──────┬──────┘             │
         │        │                 │                     │
         │  ┌─────┴─────────────────┴─────┐              │
         │  │         deploy               │              │
         │  │   (manual gate in CI/CD)     │              │
         │  └──────────────────────────────┘              │
         └─────────────────────────────────────────────┘
```

## Task Dependency Configuration

### dependsOn Semantics

The `dependsOn` field uses a prefix convention:

```jsonc
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"]
      // ^build = build all topological dependencies first
    },
    "test": {
      "dependsOn": ["build"]
      // build (no ^) = build this package (if not cached), but not deps
    }
  }
}
```

| Pattern | Meaning | Example |
|---------|---------|---------|
| `^build` | Build all upstream dependencies first | Before building `apps/api`, build `packages/db`, `packages/voice`, `packages/ai` |
| `build` | Build this package first (no dependency propagation) | Before testing `apps/api`, build `apps/api` itself |
| `["^build", "lint"]` | Both must complete before this task starts | |
| `[]` (empty) | No dependencies — can run immediately | `lint`, `clean` |

### Topological Sort Example

Given our workspace dependency graph:

```
packages/db → packages/voice → packages/ai → apps/api
                                             → apps/web
packages/ui → apps/web
```

Running `turbo build` produces this execution order:

```
Phase 1: packages/config   (no deps)
Phase 2: packages/db       (no workspace deps)
         packages/ui        (peer dep on React only)
Phase 3: packages/voice    (depends on db)
Phase 4: packages/ai       (depends on db, voice)
Phase 5: apps/api          (depends on db, voice, ai)
         apps/web           (depends on db, ui)
```

Each phase runs packages in parallel.

## Caching Strategy

### Cache Key Computation

```text
Input Files
    │
    ▼
Content Hash (SHA-256)
    │
    ├── File contents (all input globs matched)
    ├── Dependencies (all ^dependency outputs hash)
    ├── Environment variables (declared in pipeline.env)
    └── Global dependencies (root configs)
    │
    ▼
    ┌──────────┐
    │ Cache Hit │◄──── Local (.turbo/cache) + Remote
    └─────┬────┘
          │
    ┌─────▼──────┐     ┌──────────────┐
    │ Restore     │     │ Execute Task  │
    │ Outputs     │     │ (cache miss)  │
    └─────┬──────┘     └──────┬────────┘
          │                   │
          │             ┌─────▼──────┐
          │             │ Store       │
          └─────────────► Outputs     │
                        │ (local +    │
                        │  remote)    │
                        └─────────────┘
```

### Input Configuration

```jsonc
{
  "build": {
    "inputs": [
      "src/**/*.ts",
      "src/**/*.tsx",
      "src/**/*.json",
      "tsconfig.json",
      "tsconfig.base.json",
      "!src/**/*.test.ts",    // Exclude test files
      "!src/**/*.spec.ts"     // They don't affect build output
    ]
  }
}
```

**Why narrow inputs matter**: Each input file is hashed to compute the cache key. Including `node_modules` or `dist` in inputs would make cache keys unstable. Excluding test files means changing a test doesn't invalidate the build cache.

### Output Configuration

```jsonc
{
  "build": {
    "outputs": [
      "dist/**",
      ".next/**",
      "!dist/**/*.map"       // Source maps can be large; consider excluding from cache
    ]
  }
}
```

Outputs are the artifacts stored in the cache. If outputs are not declared, Turbo treats the task as having no cacheable outputs.

## Remote Caching

### Setup and Configuration

```bash
# Install Turbo and authenticate
pnpm add -D turbo
npx turbo login
npx turbo link

# CI environment variables
export TURBO_TOKEN=${{ secrets.TURBO_TOKEN }}
export TURBO_TEAM=${{ secrets.TURBO_TEAM }}
export TURBO_REMOTE_ONLY=true  # CI doesn't need local cache
```

### Remote Cache Architecture

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Developer A   │     │ Developer B   │     │     CI       │
│ (local build) │     │ (local build) │     │              │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │                    │                    │
       └────────────┬───────┴────────────────────┘
                    │
          ┌─────────▼─────────┐
          │  Vercel Remote     │
          │  Cache (S3-based)  │
          │                    │
          │  TTL: 7 days       │
          │  Max artifact:     │
          │  200 MB            │
          └────────────────────┘
```

## Parallel Execution

Turborepo maximizes parallelism by respecting the topological dependency graph. You can control parallelism with the `--parallel` flag:

```bash
# Run with default parallelism (CPU count)
turbo build

# Limit parallel tasks
turbo build --concurrency=4

# Run tests across all packages in parallel
turbo test --parallel
```

### Task Execution Flow

```text
Time ──────────────────────────────────────────────►
                                                    
┌────────────┐                                     
│ packages/  │──► build ──► test                   
│  voice     │     │          │                    
└────────────┘     │          │                    
                   │    ┌─────┘                    
                   ▼    ▼                          
┌────────────┐  ┌────────────┐                     
│ packages/  │  │  apps/api  │──► build ──► test   
│  ai        │  └────────────┘                     
└────────────┘                                     
```

## Environment Variable Declarations

```jsonc
{
  "build": {
    "env": [
      "NEXT_PUBLIC_*",          // Wildcard pattern
      "DATABASE_URL",
      "REDIS_URL",
      "KAFKA_BROKERS",
      "NEXT_PUBLIC_APP_URL",
      "NEXT_PUBLIC_API_URL",
      "SENTRY_DSN",
      "VERCEL_URL",
      "VERCEL_ENV"
    ],
    "passThroughEnv": [
      "NODE_ENV",               // Pass through without affecting cache key
      "CI"
    ]
  }
}
```

The `passThroughEnv` array allows environment variables to be available during the build without affecting the cache key. This is useful for `NODE_ENV` or `CI` which don't change the output.

## Design Decisions

### Monorepo Task Runner Comparison

| Feature | Turborepo | Nx | Lerna |
|---------|-----------|-----|-------|
| Content-aware caching | Yes | Yes | No |
| Remote caching | Vercel | Nx Cloud | No |
| Parallel execution | Topological | Topological | Sequential |
| Configuration complexity | Low | Medium | Low |
| Package manager agnostic | Yes | Yes | Yes |

**Decision**: Turborepo provides the best balance of simplicity and performance. Nx offers more features (code generation, project graph visualization) but introduces more complexity than we need for this project.

### Trade-offs

1. **Granularity vs. overhead**: Fine-grained inputs improve cache hit rates but require maintenance as project structure evolves
2. **Cache size vs. speed**: Caching `.next` output is critical for Next.js apps (saves 30-60s per build) but each cache entry is ~50MB
3. **Remote cache dependency**: If Vercel Remote Cache is unavailable, builds fall back to local cache only — still fast but CI benefits are lost

## Production Considerations

1. **Cache eviction**: Remote caches have a 7-day TTL on Vercel's free tier. For teams, artifacts persist longer but consider setting up a custom cache server for compliance requirements
2. **Cache poisoning**: If a build produces incorrect output due to a bug, that corrupted artifact is cached. Use `turbo build --force` to bypass cache when needed
3. **CI cache warm-up**: The first CI run after a long period will be a cache miss. Schedule a nightly "cache warm" build to keep artifacts fresh
4. **Pipeline visibility**: Use `turbo run build --graph` to visualize the pipeline DAG — invaluable for debugging unexpected build orders
5. **Monorepo size limits**: Turborepo works well up to ~100 packages. Beyond that, consider Nx which has better scaling characteristics
