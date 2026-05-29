# Section 04: Caching Strategy

## Overview

Caching is the single most impactful optimization for CI/CD pipeline speed. Our strategy combines four caching layers — pnpm store, Turborepo remote cache, Docker layer caching, and GitHub Actions cache — to achieve sub-5-minute CI runs for a monorepo with 20+ packages. Each layer targets a different bottleneck in the pipeline.

## Cache Layer Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    CI Cache Stack                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Layer 1: pnpm Store Cache                             │    │
│  │  Path: ~/.local/share/pnpm/store                      │    │
│  │  Key: hashFiles('pnpm-lock.yaml')                     │    │
│  │  Hit Rate: 95%+ (only invalidated on dependency       │    │
│  │             changes)                                   │    │
│  └──────────────────────────────────────────────────────┘    │
│                               │                                │
│                               ▼                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Layer 2: Turborepo Remote Cache                       │    │
│  │  Provider: Vercel Remote Cache                        │    │
│  │  Key: Content hash of inputs + env + deps             │    │
│  │  Hit Rate: 80-90% (per-package granularity)           │    │
│  └──────────────────────────────────────────────────────┘    │
│                               │                                │
│                               ▼                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Layer 3: Docker Layer Cache                           │    │
│  │  Provider: GitHub Actions Cache (gha driver)          │    │
│  │  Scope: Per-branch, with max() mode for full layers   │    │
│  │  Purpose: docker buildx --cache-from/--cache-to      │    │
│  └──────────────────────────────────────────────────────┘    │
│                               │                                │
│                               ▼                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Layer 4: GitHub Actions Cache                         │    │
│  │  Targets: .turbo/ directory, node_modules (fallback)  │    │
│  │  Strategy: Save on post-setup, restore on pre-setup   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Layer 1: pnpm Store Cache

pnpm's content-addressable store stores every version of every package exactly once. When shared across CI runs, installs drop from 90 seconds to under 10 seconds:

```yaml
- name: Cache pnpm store
  uses: actions/cache@v4
  with:
    path: |
      ~/.local/share/pnpm/store
      node_modules/.pnpm
    key: pnpm-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-
```

The key design choice is using `hashFiles('pnpm-lock.yaml')` rather than `hashFiles('pnpm-lock.yaml', 'package.json')`. The lockfile already encodes all transitive dependency resolution, so the package.json hash is redundant. This reduces cache misses when only metadata (not dependencies) changes.

```text
Lockfile unchanged:  pnpm install --frozen-lockfile → 8 seconds (cache hit)
Lockfile changed:    pnpm install --frozen-lockfile → 85 seconds (cache miss)
```

## Layer 2: Turborepo Remote Cache

Turborepo's cache operates at the task level. Each task's inputs are hashed (source files, env vars, dependencies), and if the hash matches a previous run, outputs are restored from the remote cache:

```jsonc
// turbo.json (cache-relevant excerpt)
{
  "pipeline": {
    "build": {
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "tsconfig.json"],
      "outputs": ["dist/**", ".next/**"],
      "env": ["DATABASE_URL", "NEXT_PUBLIC_*"],
      "dependsOn": ["^build"]
    }
  }
}
```

The cache granularity is per-package. A change to `packages/ui` only invalidates the cache for `packages/ui` and its consumers (`apps/web`), leaving `packages/db` and `apps/api` hits.

```yaml
- name: Turborepo Remote Cache
  env:
    TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
    TURBO_TEAM: ${{ vars.TURBO_TEAM }}
    TURBO_REMOTE_ONLY: true
  run: npx turbo build
```

`TURBO_REMOTE_ONLY: true` disables the local cache in CI (which would be ephemeral anyway) and forces all cache operations through Vercel's remote cache.

## Layer 3: Docker Layer Caching

Docker builds are notoriously slow without caching. Our Dockerfile is structured to maximize layer reuse, and the GitHub Actions cache driver persists those layers:

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and Push
  uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

The `mode=max` flag caches all layers (not just the exported ones), which allows the cache to be used across different build targets. The trade-off is increased cache storage — each build can add hundreds of megabytes to the cache.

Dockerfile layer ordering for maximum cache hits:

```dockerfile
# Layer 1: OS packages (rarely changes)
FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat

# Layer 2: Global tools (rarely changes)
FROM base AS deps
RUN npm install -g pnpm@9.1.0

# Layer 3: Dependencies (changes only on lockfile update)
COPY pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm fetch

# Layer 4: Source (changes on every commit)
COPY . .
RUN pnpm install --offline

# Layer 5: Build output (changes on every commit)
RUN pnpm build
```

By keeping `pnpm fetch` before `COPY .`, we avoid reinstalling dependencies when only source code changes.

## Cache Key Strategies

| Cache Type | Key | Scope | Invalidation |
|---|---|---|---|
| pnpm store | `pnpm-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}` | Global across branches | Only on lockfile change |
| Turborepo | Content hash of task inputs per package | Per-package | Source file changes |
| Docker layers | `type=gha` (automatic layer SHA) | Per-branch | Dockerfile or dependency changes |
| Build artifacts | `turbo-${{ runner.os }}-${{ github.sha }}` | Per-commit | Every commit (fresh) |

## Cache Size Management

GitHub Actions cache has a 10 GB limit per repository. Without management, we can hit this limit quickly:

```bash
# Monthly cache cleanup script
gh actions-cache list --limit 100 --order-by created-at --asc |
  jq -r '.[] | .id + " " + .created_at' |
  while read id created; do
    age_days=$(( ( $(date +%s) - $(date -d "$created" +%s) ) / 86400 ))
    if [ $age_days -gt 30 ]; then
      gh actions-cache delete "$id" --confirm
    fi
  done
```

This script keeps only the last 30 days of cache entries. Turborepo cache entries are typically small (compiled JS + source maps), so 30 days of history stays well under the 10 GB limit.

## Integration Points

- **Turbo remote cache** integrates with Vercel out of the box, but also supports S3-compatible backends for self-hosted setups
- **Docker cache (gha)** only works within GitHub Actions; for other CI providers, use `type=registry` and push cache layers to a container registry
- **pnpm store cache** works on any runner, but the store location varies by OS (`~/.local/share/pnpm/store` on Linux, `~/Library/pnpm/store` on macOS)

## Production Considerations

1. **Cache poisoning**: Validate cache integrity with checksums. A corrupted Turborepo cache produces broken builds. Use `TURBO_REMOTE_ONLY=true` to force remote verification.
2. **Cache miss fallback**: Always have a fallback for missing caches. The pipeline must work from scratch on a fresh runner.
3. **Concurrent cache writes**: GitHub Actions cache writes from concurrent jobs can conflict. Use `restore-keys` with partial matching rather than exact key matching.
4. **Cache isolation per branch**: Feature branch caches don't interfere with main branch caches. This is automatic with Turborepo's content-based hashing.
5. **Cost monitoring**: Vercel Remote Cache bills by storage and bandwidth. Monitor usage and set budget alerts. For high-volume teams, self-hosting the cache on S3 may be cheaper.
6. **Eviction policy**: Turborepo automatically evicts least-recently-used cache entries based on the storage backend's policy. For GitHub Actions cache, manual cleanup is required via scheduled workflows.
