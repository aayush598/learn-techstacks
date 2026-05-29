# Section 01: pnpm Workspace Configuration

## Overview

pnpm provides the foundation for dependency management in our monorepo. Unlike npm or Yarn, pnpm uses a content-addressable store and strict dependency isolation, which prevents phantom dependencies and reduces disk usage. Combined with pnpm workspaces, it provides efficient, reliable package management for the voice agent platform.

## Why pnpm Over npm or Yarn

```text
┌─────────────────────────────────────────────────────────────┐
│              Package Manager Comparison                      │
│                                                              │
│  Feature              npm         Yarn        pnpm           │
│  ─────────────────────────────────────────────────────       │
│  Disk efficiency      ❌         ❌          ✅ (store)      │
│  Strict isolation     ❌         ❌          ✅              │
│  Workspace support    ✅         ✅          ✅              │
│  Speed (install)      Slow       Fast        Fast            │
│  Monorepo-native      ❌         ❌          ✅ (catalog)    │
│  Phantom dep prevent  ❌         ❌          ✅              │
│  Plug'n'Play          ❌         ✅          ❌              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**pnpm store**: All package versions are stored once in a flat content-addressable store (~/.local/share/pnpm/store). Projects use hard links to the store, consuming negligible additional disk space. For our monorepo with 10+ workspaces sharing React, Next.js, and TypeScript, this saves gigabytes.

**Strict isolation**: pnpm creates node_modules with nested structure where packages can only access their declared dependencies. This prevents the "it works on my machine" problem caused by hoisted phantom dependencies.

## Workspace Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

This tells pnpm that any directory matching these patterns is a workspace package. Each package's `package.json` `name` field is used for cross-referencing.

### Catalog Support (pnpm 9+)

Catalogs allow centralizing shared dependency versions:

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"

catalog:
  typescript: ^5.4.0
  react: ^18.3.0
  react-dom: ^18.3.0
  next: ^14.2.0
  zod: ^3.22.0
  "@prisma/client": ^5.12.0
  prisma: ^5.12.0
  vitest: ^1.6.0
  "@types/node": ^20.12.0
  "@types/react": ^18.3.0
  "@types/react-dom": ^18.3.0
```

Workspace packages can then reference catalog entries:

```jsonc
{
  "dependencies": {
    "react": "catalog:",
    "zod": "catalog:"
  },
  "devDependencies": {
    "typescript": "catalog:",
    "vitest": "catalog:"
  }
}
```

Catalogs ensure every workspace uses the same version of shared dependencies, preventing version drift and duplicated packages in the store.

## Package Filters

pnpm provides powerful filtering for workspace operations:

```bash
# Install only web app dependencies
pnpm --filter @voice-agent/web install

# Add a dependency to a specific package
pnpm --filter @voice-agent/db add zod

# Add a dev dependency to all packages
pnpm -r --filter ./packages/* add -D vitest

# Run a script in a specific package
pnpm --filter @voice-agent/api run dev

# Run in packages changed since last commit
pnpm --filter ".[HEAD^1]" test

# Run in a package and its dependencies
pnpm --filter "@voice-agent/api..." build

# Run in a package and its dependents
pnpm --filter "...@voice-agent/db" test
```

## Hoisting Strategy

pnpm's node_modules structure is different from npm/Yarn:

```text
npm/Yarn (flat hoisting):
node_modules/
├── react/              # Hoisted to root
├── next/               # Hoisted to root
├── zod/                # Hoisted to root
└── @voice-agent/
    ├── web/
    │   └── node_modules/  # Never used
    └── db/
        └── node_modules/

pnpm (strict nesting):
node_modules/
├── .pnpm/              # Virtual store
│   ├── react@18.3.0/   # Single copy
│   ├── next@14.2.0/
│   └── zod@3.22.0/
├── react -> .pnpm/react@18.3.0  # Symlink
├── next -> .pnpm/next@14.2.0
└── @voice-agent/
    ├── web -> ../../packages/web  # Workspace symlink
    └── db -> ../../packages/db
```

This structure means packages can only import from their declared dependencies. If `@voice-agent/web` forgets to declare `zod` in its `package.json`, importing it will fail — even if another package depends on it.

### Public Hoist Pattern

Some tools (like TypeScript's `types` in tsconfig) expect packages at the root. Configure public hoisting:

```yaml
# .npmrc
shamefully-hoist=true
# Or selectively:
public-hoist-pattern[]=*types*
public-hoist-pattern[]=*vite*
```

## .npmrc Configuration

```ini
# .npmrc
# Use pnpm's strict mode
strict-peer-dependencies=true
auto-install-peers=true

# Workspace settings
link-workspace-packages=true
prefer-workspace-packages=true
shared-workspace-lockfile=true

# Store location
store-dir=/home/user/.local/share/pnpm/store

# Registry
registry=https://registry.npmjs.org/

# Save exact versions by default
save-exact=true

# Engine checks
engine-strict=true

# Resolution
resolution-mode=highest
```

## Workspace Scripts

Root-level scripts orchestrate workspace operations through pnpm:

```jsonc
{
  "scripts": {
    "install:clean": "pnpm install --frozen-lockfile",
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "typecheck": "turbo typecheck",
    "clean": "turbo clean",
    "reset": "turbo clean && rm -rf node_modules && pnpm install",
    "outdated": "pnpm outdated -r",
    "update": "pnpm update -r --latest",
    "audit": "pnpm audit",
    "why": "pnpm why"
  }
}
```

## Lockfile Considerations

```bash
# Generate lockfile
pnpm install --frozen-lockfile

# Check lockfile is up to date (CI)
pnpm install --frozen-lockfile --fail-if-lockfile-changed

# Update lockfile after dependency changes
pnpm install --lockfile-only
```

## Design Decisions

### Why not npm workspaces?

npm workspaces lack strict isolation, meaning packages can access undeclared dependencies that happen to be hoisted. This leads to "works on my machine" bugs that surface in CI or production.

### Why not Yarn Berry (Plug'n'Play)?

Yarn Berry's PnP mode requires a `.pnp.cjs` loader and has compatibility issues with many tools (TypeScript, ESLint, Jest). pnpm provides similar disk efficiency without the compatibility burden.

## Integration Points

- **pnpm-workspace.yaml**: Defines the monorepo structure
- **.npmrc**: Controls hoisting, dependency resolution, and strictness
- **package.json**: Each workspace declares its own dependencies
- **Turborepo**: Uses pnpm's workspace topology for build ordering
- **CI pipeline**: Uses `--frozen-lockfile` for reproducible installs

## Production Considerations

1. **Store location**: Configure a shared pnpm store in CI to avoid re-downloading packages. GitHub Actions cache can persist the store across runs
2. **Lockfile conflicts**: In a monorepo with many contributors, lockfile merge conflicts are common. pnpm's shared lockfile reduces conflicts compared to per-package lockfiles
3. **Node.js version**: Pin the required Node.js version in `package.json` `engines` field and enforce with `engine-strict=true` in `.npmrc`
4. **Registry security**: Use `npm config set @voice-agent:registry https://npm.pkg.github.com` for private packages, and configure `//npm.pkg.github.com/:_authToken` via environment variables
5. **Patch packages**: Use `pnpm patch` to apply fixes to dependencies without forking. Track patches in version control under `patches/`
