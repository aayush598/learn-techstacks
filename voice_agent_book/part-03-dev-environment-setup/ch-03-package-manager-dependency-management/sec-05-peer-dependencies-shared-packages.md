# Section 05: Peer Dependencies & Shared Packages

## Overview

Peer dependencies are critical in a monorepo where multiple packages share common frameworks like React, Next.js, and TypeScript. They ensure that a single copy of these shared dependencies is used across the entire application, preventing bundle duplication, "invalid hook call" errors, and type conflicts.

## The Problem Peer Dependencies Solve

```text
Without peer dependencies:
┌─────────────────────────────────────────────────────────────┐
│  node_modules/                                               │
│  ├── apps/web/                                               │
│  │   └── node_modules/react@18.3.1    ← One copy            │
│  ├── packages/ui/                                            │
│  │   └── node_modules/react@18.3.1    ← Duplicate!          │
│  └── packages/widget/                                        │
│      └── node_modules/react@18.3.1    ← Duplicate!          │
│                                                              │
│  Problem: React context from web can't reach UI components   │
│  Error: "Invalid hook call" or context undefined             │
└─────────────────────────────────────────────────────────────┘

With peer dependencies:
┌─────────────────────────────────────────────────────────────┐
│  node_modules/                                               │
│  ├── react@18.3.1                          ← Single copy     │
│  ├── apps/web/                                               │
│  │   └── (react resolved to root)                            │
│  ├── packages/ui/                                            │
│  │   └── (react resolved to root via peer)                   │
│  └── packages/widget/                                        │
│      └── (react resolved to root via peer)                   │
│                                                              │
│  Result: Single React instance, shared context               │
└─────────────────────────────────────────────────────────────┘
```

## Peer Dependency Declaration

### UI Package

```jsonc
{
  "name": "@voice-agent/ui",
  "version": "0.0.1",
  "peerDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0"
  }
}
```

The key pattern: peer dependencies are also listed as devDependencies. This allows the package to be developed independently (tests, Storybook) while ensuring consumers provide the actual runtime dependency.

### Configuration Package

```jsonc
{
  "name": "@voice-agent/config-eslint",
  "peerDependencies": {
    "eslint": "^8.57.0"
  },
  "devDependencies": {
    "eslint": "^8.57.0"
  }
}
```

### Database Package (no peer deps)

```jsonc
{
  "name": "@voice-agent/db",
  "dependencies": {
    "@prisma/client": "5.14.0"
  },
  "devDependencies": {
    "prisma": "5.14.0"
  }
}
```

The DB package uses regular dependencies for `@prisma/client` since it doesn't share a runtime context with the consumer. Prisma is an implementation detail.

## When to Use Peer Dependencies

```typescript
// Decision matrix for dependency type
interface DepDecision {
  type: "dependency" | "peerDependency" | "devDependency";
  criteria: string[];
}

const decisions: Record<string, DepDecision> = {
  // React — always a peer dependency in shareable packages
  react: {
    type: "peerDependency",
    criteria: [
      "Multiple packages need the SAME instance",
      "Runtime context sharing required",
      "Package exposes React components",
    ],
  },

  // Prisma — always a regular dependency
  "@prisma/client": {
    type: "dependency",
    criteria: [
      "No runtime context shared",
      "Package is an implementation detail",
      "Version is specific to the package",
    ],
  },

  // TypeScript — peer dependency for config packages
  typescript: {
    type: "peerDependency",
    criteria: [
      "Config package extends TypeScript",
      "Consumer must have TypeScript installed",
      "Version compatibility is critical",
    ],
  },

  // Lodash — regular dependency (or avoid entirely)
  lodash: {
    type: "dependency",
    criteria: [
      "Utility functions, no shared state",
      "Multiple versions can coexist",
      "Easier to manage as direct dependency",
    ],
  },
};
```

## Hoisting Strategy with pnpm

pnpm handles peer dependencies differently from npm/Yarn:

```yaml
# .npmrc — peer dependency settings
strict-peer-dependencies=true
auto-install-peers=true
```

With `strict-peer-dependencies=true`, pnpm will fail the install if any peer dependency is missing. This is stricter than npm and surfaces issues earlier.

```text
pnpm peer resolution for packages/ui:

1. Consumer (apps/web) has react@18.3.1 declared
2. pnpm resolves the peer dep: react@18.3.1 satisfies ^18.3.0
3. packages/ui gets react from the consumer's node_modules
4. If consumer didn't have react → install fails (strict mode)
```

## Package hoisting with pnpm workspace

```yaml
# .npmrc
# Ensure React is hoisted to the root for shared access
public-hoist-pattern[]=react
public-hoist-pattern[]=react-dom
public-hoist-pattern[]=next
```

## Shared TypeScript Version

TypeScript version conflicts between packages cause confusing type errors:

```yaml
# pnpm-workspace.yaml
catalog:
  typescript: ^5.4.0
  "@types/node": ^20.12.0
  "@types/react": ^18.3.0
  "@types/react-dom": ^18.3.0
```

All packages reference the catalog:

```jsonc
{
  "devDependencies": {
    "typescript": "catalog:"
  }
}
```

## Peer Dependency Validation

```bash
# Check peer dependency issues
pnpm ls --depth=0 -r

# Find duplicate packages that should be shared
pnpm why -r react

# Audit peer dependency mismatches
pnpm audit --audit-level=high

# Check for invalid hook call scenarios
pnpm ls react --depth=0 -r
# Should show only ONE version of react
```

## Runtime Validation

For critical shared dependencies like React, add runtime validation:

```typescript
// packages/ui/src/utils/react-version.ts
import React from "react";

const MIN_REACT_VERSION = 18;
const MAX_REACT_VERSION = 19;

export function validateReactVersion(): void {
  const version = React.version;
  const major = parseInt(version.split(".")[0] ?? "0", 10);

  if (major < MIN_REACT_VERSION || major >= MAX_REACT_VERSION) {
    throw new Error(
      `@voice-agent/ui requires React ${MIN_REACT_VERSION}.x. ` +
      `Found React ${version}. ` +
      `This may happen when multiple React versions are installed.`
    );
  }
}
```

## Design Decisions

### Peer Deps vs. Regular Deps for Shared Libraries

| Aspect | Peer Dependency | Regular Dependency |
|--------|----------------|-------------------|
| Bundle duplication | Prevents | Can cause |
| Context sharing | Enables | Breaks |
| Consumer flexibility | Must provide dep | Transparent |
| Install complexity | Higher | Lower |
| Version conflicts | Catches early | Hidden |

**Decision**: Use peer dependencies for:
- **Framework libraries** (React, React DOM, Next.js)
- **Config tools** (TypeScript, ESLint, Tailwind)
- **Any package that shares runtime state**

Use regular dependencies for:
- **Implementation details** (Prisma, Zod, utility libraries)
- **Build tools** (PostCSS, autoprefixer)
- **Type-only packages** (@types/*)

### Multiple React Versions

The most common monorepo issue is duplicate React versions. Prevention:
1. Use pnpm catalog to pin React version across all workspaces
2. Enable `strict-peer-dependencies=true`
3. Run `pnpm ls react --depth=0 -r` in CI to detect duplicates
4. Add a pre-commit hook that checks for React version consistency

## Integration Points

- **packages/ui**: React is a peer dep — consumer provides it
- **packages/config-eslint**: ESLint is a peer dep — consumer provides it
- **apps/web**: Provides React, Next.js, Tailwind for all peer-dependent packages
- **apps/api**: May not need React — doesn't install it

## Production Considerations

1. **Peer dep warnings**: pnpm's `auto-install-peers=true` automatically installs missing peer deps. In CI, enable `strict-peer-dependencies=true` to fail on any mismatch
2. **Bundle analysis**: Use `webpack-bundle-analyzer` or `vite-bundle-visualizer` to detect duplicate bundled versions
3. **Package upgrades**: When upgrading React, update the peer dep range in ALL packages simultaneously. Catalogs make this a single change
4. **External consumers**: If a package is published externally, its peer deps require consumer coordination. Document peer dep requirements clearly in the package README
5. **Testing**: Test suites should validate that the package works with the minimum declared peer dep version, not just the current version
