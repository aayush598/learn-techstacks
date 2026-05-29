# Section 08: Local Package Development

## Overview

Developing internal packages within a monorepo requires seamless linking, hot reload, versioning, and publishing workflows. This section covers the patterns and tooling for efficient local package development in the voice agent platform.

## Development Loop

```text
┌─────────────────────────────────────────────────────────┐
│                Local Package Development Loop             │
│                                                          │
│  Edit Source ──► Type Check ──► Build ──► Test          │
│       ▲                                       │         │
│       │        ┌─────────────────┐            │         │
│       └────────│ Hot Reload (dev) │◄──────────┘         │
│                │ Watch Mode       │                      │
│                └─────────────────┘                      │
│                                                          │
│  Tools: tsc --watch, turbo dev, nodemon, tsx             │
└─────────────────────────────────────────────────────────┘
```

## Workspace Linking with pnpm

The `pnpm-workspace.yaml` file defines which directories contain workspace packages. The `workspace:*` protocol links them together:

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

When a package declares a dependency using `"workspace:*"`, pnpm creates a symlink to the local package directory rather than downloading from the npm registry:

```bash
# What this does internally:
# node_modules/@voice-agent/db → ../../packages/db

# Install all workspace dependencies
pnpm install
```

## Watch Mode for Packages

### TypeScript Watch Mode

```bash
# In the types package — rebuild on every change
cd packages/types && tsc --watch

# Or use turbo to run all watch modes
turbo dev --parallel
```

### Turborepo dev Pipeline

```jsonc
// turbo.json (dev pipeline)
{
  "dev": {
    "cache": false,
    "persistent": true
  }
}
```

The `dev` task is marked `"persistent": true` to indicate it runs indefinitely (watch mode). Turborepo doesn't cache persistent tasks, and they don't participate in cache key computation.

### Running Development Across Workspaces

```bash
# Run all packages in watch mode
turbo dev --filter="./packages/*"

# Run a specific package and its consumers
turbo dev --filter="@voice-agent/db" --filter="@voice-agent/api"
```

## TypeScript Project References

For faster type checking during development, use TypeScript project references:

```jsonc
// apps/api/tsconfig.json
{
  "extends": "@voice-agent/config-typescript/nextjs.json",
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
  },
  "references": [
    { "path": "../../packages/db" },
    { "path": "../../packages/voice" },
    { "path": "../../packages/ai" },
    { "path": "../../packages/types" }
  ]
}
```

```bash
# Build all referenced projects in dependency order
tsc --build

# Build with watch mode
tsc --build --watch
```

## Hot Reload Integration

### Next.js with Package Changes

Next.js's Turbopack (or Webpack) watches the `node_modules` symlinks and triggers hot reload when workspace packages change:

```javascript
// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: [
    "@voice-agent/ui",
    "@voice-agent/types",
    "@voice-agent/db",
  ],
  webpack: (config) => {
    // Ensure workspace packages are watched
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
      ignored: ["**/node_modules", "**/.next", "**/dist"],
    };
    return config;
  },
};

module.exports = nextConfig;
```

The `transpilePackages` option is critical — it tells Next.js to compile workspace packages through its Babel/ SWC pipeline, enabling features like JSX transformation and CSS modules for packages.

### Node.js Services with Hot Reload

For the API app, use `tsx watch` for hot reload:

```jsonc
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "dev:api": "next dev -p 4000"
  }
}
```

## Versioning Internal Packages

### Manual Version Bumping

```bash
# Bump a specific package
pnpm version patch --filter @voice-agent/db

# Bump all changed packages
pnpm changeset version

# Create changeset
pnpm changeset
```

### Using Changesets for Monorepo Versioning

```bash
# Install Changesets
pnpm add -D @changesets/cli

# Initialize
pnpm changeset init

# Create a changeset (describes what changed)
pnpm changeset

# Version packages based on changesets
pnpm changeset version

# Publish packages (if any are public)
pnpm changeset publish
```

```markdown
---
"@voice-agent/db": patch
"@voice-agent/api": minor
---

Add cursor-based pagination to agent repository
```

## Linking Pattern for Development

Instead of publishing to npm, use pnpm's workspace protocol:

```jsonc
// In the consumer's package.json
{
  "dependencies": {
    "@voice-agent/db": "workspace:*",
    "@voice-agent/voice": "workspace:^0.2.0"
  }
}
```

- `workspace:*` always links to the local version
- `workspace:^0.2.0` links to the local version but also expresses the semver range (useful when publishing externally)

## Testing Package Changes

### Running Tests for a Package and Its Consumers

```bash
# Test only the changed package
turbo test --filter @voice-agent/db

# Test the package and all downstream consumers
turbo test --filter "@voice-agent/db..."

# Test everything affected by changes
turbo test --filter "[HEAD^1]"
```

The `...` suffix tells Turborepo to include downstream dependents. The `[HEAD^1]` filter detects packages changed since the given commit.

## Package Publishing Workflow

### For Private Packages (Default)

Private packages are never published. They're consumed locally via workspace links:

```jsonc
{
  "name": "@voice-agent/db",
  "private": true,
  "publishConfig": {
    "access": "restricted"
  }
}
```

### For Public Packages

If a package needs to be published to npm:

```jsonc
{
  "name": "@voice-agent/ui",
  "private": false,
  "publishConfig": {
    "access": "public"
  },
  "files": ["dist"],
  "main": "dist/index.js",
  "types": "dist/index.d.ts"
}
```

## Development Scripts

```jsonc
// package.json (root)
{
  "scripts": {
    "dev": "turbo dev",
    "dev:web": "turbo dev --filter @voice-agent/web",
    "dev:api": "turbo dev --filter @voice-agent/api",
    "dev:packages": "turbo dev --filter='./packages/*'",
    "build": "turbo build",
    "build:packages": "turbo build --filter='./packages/*'",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck",
    "test": "turbo test",
    "clean": "turbo clean",
    "reset": "turbo clean && rm -rf node_modules && pnpm install"
  }
}
```

## Design Decisions

### workspace:* vs. npm link

| Feature | workspace:* | npm link |
|---------|-------------|----------|
| Symlink creation | Automatic | Manual |
| Dependency resolution | Correct (pnpm hoisting) | Can break hoisting |
| Multiple consumers | Works seamlessly | Must link in each consumer |
| CI support | Built-in | Requires bootstrap script |
| Version constraints | Semver-aware | Always latest |

**Decision**: Always use `workspace:*` over `npm link`. The workspace protocol is faster, more reliable, and integrated with pnpm's dependency resolution.

### Build First vs. TypeScript Paths

Two approaches exist for local package development:

1. **Build first**: Run `tsc` or `turbo build` before consuming changes
2. **TypeScript paths**: Use `compilerOptions.paths` to point directly to source files

```jsonc
{
  "compilerOptions": {
    "paths": {
      "@voice-agent/db": ["../../packages/db/src"],
      "@voice-agent/types": ["../../packages/types/src"]
    }
  }
}
```

**Decision**: Use build-first for deployment (CI) and TypeScript paths for development (local). The paths approach avoids the build step during development but doesn't work with `next build` or production deployments. Configure both and switch based on environment.

## Production Considerations

1. **Build artifacts in version control**: Never commit `dist/` directories. The `files` field in `package.json` controls what gets published
2. **Cache invalidation**: When a package changes, all downstream consumers must rebuild. Turborepo handles this automatically
3. **Circular dependencies**: A package that imports another package which transitively imports the first creates a build loop. Turborepo detects and blocks these
4. **Stale dist folders**: After switching branches, run `turbo clean && turbo build` to purge stale build artifacts
5. **Pre-commit checks**: Use lint-staged to run `turbo typecheck --filter` on changed packages before commit to catch type errors early
