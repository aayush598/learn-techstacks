# TypeScript Monorepo Tooling

## Table of Contents

1. [Monorepo vs Polyrepo](#monorepo-vs-polyrepo)
2. [pnpm Workspaces + TypeScript](#pnpm-workspaces--typescript)
3. [Turborepo + TypeScript](#turborepo--typescript)
4. [Nx + TypeScript](#nx--typescript)
5. [Project References in Monorepos](#project-references-in-monorepos)
6. [Shared TypeScript Configuration](#shared-typescript-configuration)
7. [Package Boundary Enforcement](#package-boundary-enforcement)
8. [Type-Safe Imports Between Packages](#type-safe-imports-between-packages)
9. [CI/CD for Monorepos](#cicd-for-monorepos)
10. [Interview Questions](#interview-questions)

---

## Monorepo vs Polyrepo

```typescript
// MONOREPO: All packages in one repository
// my-project/
//   packages/
//     shared/         (shared utilities, types)
//     api/            (backend API server)
//     web/            (frontend web app)
//     mobile/         (React Native app)
//     docs/           (documentation site)
//   package.json      (root)
//   pnpm-workspace.yaml
//   tsconfig.json     (base config)

// POLYREPO: Each package in separate repository
// shared-repo/      (separate git repo)
// api-repo/         (separate git repo)
// web-repo/         (separate git repo)

// Advantages of monorepos for TypeScript:
// 1. Shared types are atomic — breaking change in shared/ fails api/ immediately
// 2. Refactoring across packages is one commit
// 3. Single version of dependencies (no version conflicts)
// 4. CI can build/test only affected packages
// 5. Code review sees full impact of type changes

// Disadvantages:
// 1. Git history grows fast
// 2. Build tooling is more complex
// 3. All team members clone the full repo
// 4. Requires careful workspace configuration
```

---

## pnpm Workspaces + TypeScript

### Setup

```bash
# Initialize a pnpm workspace monorepo
mkdir my-monorepo && cd my-monorepo
pnpm init

# Create workspace config
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'packages/*'
  - 'apps/*'
EOF
```

```typescript
// Root package.json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "pnpm -r build",
    "typecheck": "pnpm -r typecheck",
    "dev": "pnpm -r --parallel dev",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint"
  },
  "devDependencies": {
    "typescript": "^5.4.0"
  }
}
```

### Package Structure

```typescript
// packages/shared/package.json
{
  "name": "@myorg/shared",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc --build",
    "typecheck": "tsc --noEmit",
    "dev": "tsc --build --watch"
  },
  "devDependencies": {
    "typescript": "workspace:*"
  }
}

// packages/shared/src/index.ts
export { formatDate, parseDate } from './date';
export { type User, type UserRole, createUser } from './user';
export { generateId, slugify } from './utils';

// packages/shared/src/user.ts
export type UserRole = 'admin' | 'editor' | 'viewer';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  createdAt: Date;
}

export function createUser(
  name: string,
  email: string,
  role: UserRole = 'viewer'
): User {
  return {
    id: crypto.randomUUID(),
    name,
    email,
    role,
    createdAt: new Date(),
  };
}
```

```typescript
// packages/api/package.json
{
  "name": "@myorg/api",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "scripts": {
    "build": "tsc --build",
    "typecheck": "tsc --noEmit",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "@myorg/shared": "workspace:*"
  },
  "devDependencies": {
    "typescript": "workspace:*",
    "tsx": "^4.7.0"
  }
}

// packages/api/src/index.ts
import { createUser, type User, type UserRole } from '@myorg/shared';

const admin = createUser('Admin', 'admin@example.com', 'admin');
console.log(admin);
```

### Installing Dependencies

```bash
# Install all dependencies across all workspaces
pnpm install

# Add a dependency to a specific workspace
pnpm --filter @myorg/api add express
pnpm --filter @myorg/api add -D @types/express

# Add a shared dependency to all workspaces
pnpm -r add lodash

# Link local packages (automatic with workspace: protocol)
# pnpm automatically symlinks @myorg/shared in node_modules
# when api declares it as a dependency with "workspace:*"
```

---

## Turborepo + TypeScript

### Setup

```bash
# Add Turborepo to an existing pnpm workspace
pnpm add -Dw turbo

# Or use the template
npx create-turbo@latest my-turborepo
```

```json
// turbo.json — the heart of Turborepo configuration
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "inputs": ["src/**", "tsconfig.json"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "lint": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "dev": {
      "dependsOn": ["^build"],
      "cache": false,
      "persistent": true
    }
  }
}
```

```typescript
// How Turborepo pipelines work for TypeScript:
//
// Given this dependency graph:
//   shared -> api
//   shared -> web
//
// `turbo run build` executes:
// 1. Build shared (no dependencies)
// 2. Build api AND web in parallel (both depend on shared)
//
// `turbo run typecheck` executes:
// 1. typecheck shared (no dependencies)
// 2. typecheck api AND web in parallel
//
// The "^" prefix means "depend on the task in dependencies"
// Without "^", it means "depend on the task in the same package"
//
// Caching:
// - Turborepo caches task outputs based on input hashes
// - If shared/src hasn't changed, shared's build is restored from cache
// - If shared hasn't changed, api and web typechecks use cached shared output

// Root package.json scripts
{
  "scripts": {
    "build": "turbo run build",
    "typecheck": "turbo run typecheck",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "clean": "turbo run clean && rm -rf node_modules/.cache"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  }
}
```

### Turborepo Caching for TypeScript

```typescript
// Turborepo uses content hashing to determine cache validity:
// - Input: files matching the "inputs" pattern
// - Output: files matching the "outputs" pattern
// - If inputs haven't changed -> restore from cache (instant)

// For TypeScript specifically:
// - "outputs": [] for typecheck means no files are produced
//   (cache is based on successful exit code + input hashes)
// - "outputs": ["dist/**"] for build means the dist folder is cached

// Turbo run with verbose output shows caching decisions:
// $ turbo run typecheck
//
// • Packages in scope: @myorg/shared, @myorg/api, @myorg/web
// @myorg/shared:typecheck: cache hit, replaying output
// @myorg/api:typecheck: cache miss, executing
// @myorg/web:typecheck: cache miss, executing
//
// Tasks:    3 successful, 3 total
// Cached:   1 cached, 3 total
// Time:     1.2s >>> local cache

// Force rebuild (skip cache):
// turbo run build --force

// Cache configuration in turbo.json
{
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "tsconfig.json"],
      "env": ["NODE_ENV"]
    }
  }
}
```

---

## Nx + TypeScript

### Setup

```bash
# Create a new Nx workspace with TypeScript
npx create-nx-workspace@latest my-nx-workspace \
  --preset=ts \
  --packageManager=pnpm

# Add packages to the workspace
nx g @nx/js:library shared
nx g @nx/js:library api
nx g @nx/js:application web
```

```typescript
// Nx workspace structure
// my-nx-workspace/
//   nx.json              (Nx configuration)
//   package.json
//   pnpm-workspace.yaml
//   tsconfig.base.json   (shared base config)
//   packages/
//     shared/
//       src/
//         index.ts
//       tsconfig.json
//       package.json
//     api/
//       src/
//         index.ts
//       tsconfig.json
//       package.json
//     web/
//       src/
//         main.ts
//       tsconfig.json
//       package.json
```

```json
// nx.json
{
  "namedInputs": {
    "default": ["{projectRoot}/src/**/*"],
    "production": ["default", "!{projectRoot}/**/*.spec.ts"]
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production"],
      "outputs": ["{projectRoot}/dist"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": ["default"]
    },
    "lint": {
      "inputs": ["default"]
    },
    "test": {
      "inputs": ["default"]
    }
  },
  "defaultBase": "main"
}
```

### Nx Affected Commands

```bash
# Nx tracks which files changed and only runs targets on
# packages that are affected by those changes.

# Check which packages are affected by your changes
nx affected --target=typecheck --dry-run

# This will show:
# - @myorg/shared (changed)
# - @myorg/api (depends on @myorg/shared)
# - @myorg/web (depends on @myorg/shared)

# Run type checking on affected packages only
nx affected --target=typecheck

# Build only affected packages
nx affected --target=build

# Run tests on affected packages
nx affected --target=test

# Compare against main branch (default)
nx affected --target=typecheck --base=main

# The power of affected:
// In a monorepo with 50 packages, if you change one package,
// nx affected might only need to check 3-5 packages instead of 50.
// This can reduce CI time from 30 minutes to 2 minutes.
```

### Nx Dependency Graph

```bash
# Visualize the dependency graph
nx graph

# Shows a visual representation of:
# - All packages in the workspace
# - Their dependencies (including implicit ones)
# - Which packages are affected by changes

// Example graph:
//   shared
//   ├── api
//   └── web
//
// If shared has a TypeScript error, both api and web will fail.

# The graph also identifies circular dependencies:
// api -> shared -> api  (CIRCULAR!)
// Nx will warn about circular dependencies and refuse to build.
```

### Nx TypeScript Configuration

```typescript
// tsconfig.base.json (root)
{
  "compileOnSave": false,
  "compilerOptions": {
    "rootDir": ".",
    "sourceMap": true,
    "declaration": true,
    "moduleResolution": "bundler",
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "skipLibCheck": true,
    "skipDefaultLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@myorg/shared": ["packages/shared/src/index.ts"],
      "@myorg/api": ["packages/api/src/index.ts"]
    }
  },
  "exclude": ["node_modules", "tmp"]
}

// packages/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "references": [
    { "path": "../shared" }
  ]
}
```

---

## Project References in Monorepos

### Setup

```typescript
// Project references allow TypeScript to understand
// the dependency graph between packages.
//
// Benefits:
// 1. Each package only rebuilds when dependencies change
// 2. Type checking respects package boundaries
// 3. Declaration files (.d.ts) flow between packages
// 4. Near-incremental builds across the monorepo

// Root tsconfig.json
{
  "files": [],
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/api" },
    { "path": "packages/web" }
  ]
}

// packages/shared/tsconfig.json
{
  "compilerOptions": {
    "composite": true,        // Required for project references
    "incremental": true,      // Cache build output
    "declaration": true,      // Emit .d.ts for consumers
    "declarationMap": true,   // Source map for .d.ts
    "outDir": "./dist",
    "rootDir": "./src",
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "skipLibCheck": true
  },
  "include": ["src"]
}

// packages/api/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "skipLibCheck": true
  },
  "include": ["src"],
  "references": [
    { "path": "../shared" }  // Depends on shared
  ]
}
```

### Building with Project References

```bash
# Build all packages in dependency order
npx tsc --build

# Build only changed packages (incremental)
npx tsc --build --incremental

# Force rebuild all packages
npx tsc --build --force

# Verbose output shows build order
npx tsc --build --verbose
# [1] projects/shared/tsconfig.json
# [2] projects/api/tsconfig.json  (depends on shared)
# [3] projects/web/tsconfig.json  (depends on shared)
```

```typescript
// How project references work internally:
//
// When shared is built with "composite: true":
// 1. shared/dist/index.js     (compiled JS)
// 2. shared/dist/index.d.ts   (declaration file)
// 3. shared/dist/tsconfig.tsbuildinfo (cached build info)
//
// When api depends on shared:
// 1. api reads shared's tsconfig.tsbuildinfo
// 2. If shared hasn't changed, api skips rebuilding shared
// 3. api uses shared's .d.ts for type checking
// 4. api only re-checks files that import from shared
//
// The .tsbuildinfo file tracks:
// - File hashes (detect changes)
// - Dependency graph (which files import what)
// - Type information cache (skip re-checking unchanged types)
```

---

## Shared TypeScript Configuration

### Base Configuration Pattern

```typescript
// configs/tsconfig.base.json — shared base configuration
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "moduleResolution": "bundler",
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}

// configs/tsconfig.node.json — for Node.js packages
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "module": "ES2022",
    "target": "ES2022",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "types": ["node"]
  }
}

// configs/tsconfig.react.json — for React packages
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "outDir": "./dist",
    "types": ["react", "react-dom"]
  }
}

// packages/shared/tsconfig.json
{
  "extends": "../../configs/tsconfig.node.json",
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"]
}

// packages/web/tsconfig.json
{
  "extends": "../../configs/tsconfig.react.json",
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

### Environment-Specific Configs

```typescript
// configs/tsconfig.build.json — for production builds
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": false,
    "declaration": true,
    "incremental": true
  }
}

// configs/tsconfig.check.json — for type checking only
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true,
    "incremental": true,
    "tsBuildInfoFile": "./.tsbuildinfo"
  }
}

// Package.json scripts using different configs:
{
  "scripts": {
    "typecheck": "tsc --project tsconfig.check.json",
    "build": "tsc --project tsconfig.build.json"
  }
}
```

---

## Package Boundary Enforcement

```typescript
// Prevent packages from importing from unauthorized dependencies
// using ESLint with import rules.

// .eslintrc.js (root)
module.exports = {
  plugins: ['import'],
  rules: {
    'import/no-restricted-paths': ['error', {
      zones: [
        // api cannot import from web
        {
          target: './packages/api',
          from: './packages/web',
          message: 'API packages cannot import from web packages',
        },
        // web cannot import from api (except shared types)
        {
          target: './packages/web',
          from: './packages/api',
          except: ['./packages/api/src/types'],
          message: 'Web packages cannot import from api implementations',
        },
        // shared cannot import from api or web
        {
          target: './packages/shared',
          from: './packages/api',
          message: 'Shared packages cannot import from api',
        },
        {
          target: './packages/shared',
          from: './packages/web',
          message: 'Shared packages cannot import from web',
        },
      ],
    }],
  },
};

// Circular dependency detection with madge
// package.json
{
  "scripts": {
    "circular": "npx madge --circular --extensions ts ./packages"
  }
}

// Example circular dependency detection:
// $ npm run circular
// ─────────────────────────────────────────
// Circular dependency detected
//
// packages/shared/src/user.ts
//   -> packages/api/src/user-service.ts
//     -> packages/shared/src/user.ts
//
// This breaks TypeScript incremental builds and causes
// confusing type errors. Always fix circular dependencies.
```

---

## Type-Safe Imports Between Packages

```typescript
// packages/shared/src/index.ts
// Public API surface — only export what other packages need
export { createUser, type User, type UserRole } from './user';
export { formatDate, type DateFormatOptions } from './date';
export { generateId, slugify } from './utils';

// packages/shared/src/internal.ts
// Internal implementation details — NOT re-exported from index.ts
export function hashPassword(password: string): string {
  // Internal implementation
  return password; // placeholder
}

export interface InternalConfig {
  saltRounds: number;
  pepper: string;
}

// By NOT exporting from index.ts, other packages cannot import
// internal functions. This enodes the public API boundary.

// packages/shared/package.json
{
  "name": "@myorg/shared",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./types": {
      "types": "./dist/types.d.ts",
      "import": "./dist/types.js"
    }
  }
}

// This limits what can be imported:
// import { createUser } from '@myorg/shared';        ✅ works
// import { hashPassword } from '@myorg/shared';       ❌ not exported
// import { hashPassword } from '@myorg/shared/internal'; // ❌ not in exports
```

### Shared Types Package

```typescript
// For types shared across multiple packages, create a dedicated types package:

// packages/types/src/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Post {
  id: string;
  authorId: string;
  title: string;
  content: string;
  publishedAt: Date | null;
}

export interface ApiResponse<T> {
  data: T;
  meta: {
    page: number;
    pageSize: number;
    total: number;
  };
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

// packages/types/package.json
{
  "name": "@myorg/types",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsc --build"
  }
}

// packages/types/tsconfig.json
{
  "extends": "../../configs/tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"]
}

// Now both api and web can depend on types:
// packages/api/package.json
{
  "dependencies": {
    "@myorg/types": "workspace:*"
  }
}

// packages/web/package.json
{
  "dependencies": {
    "@myorg/types": "workspace:*"
  }
}

// packages/api/src/users.ts
import type { User, ApiResponse, ApiError } from '@myorg/types';

async function getUser(id: string): Promise<ApiResponse<User> | ApiError> {
  // Type-safe return value
  return { data: { id, name: 'Test', email: 'test@test.com' }, meta: { page: 1, pageSize: 10, total: 1 } };
}
```

---

## CI/CD for Monorepos

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for nx affected

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Turborepo approach
      - name: Typecheck
        run: pnpm turbo typecheck

      - name: Build
        run: pnpm turbo build

      - name: Test
        run: pnpm turbo test

      # Nx approach (alternative)
      # - name: Affected typecheck
      #   run: npx nx affected --target=typecheck --base=origin/main
      #
      # - name: Affected build
      #   run: npx nx affected --target=build --base=origin/main
      #
      # - name: Affected test
      #   run: npx nx affected --target=test --base=origin/main
```

```typescript
// CI optimization strategies for TypeScript monorepos:

// 1. CACHE EVERYTHING
// - pnpm store cache
// - Turborepo/Nx task cache
// - .tsbuildinfo files
// - dist/ folders for unchanged packages

// 2. PARALLELIZE
// - Turborepo/Nx automatically parallelize independent packages
// - For 10 packages with no interdependencies, all 10 run simultaneously

// 3. AFFECTED-ONLY
// - Only typecheck/build/test packages affected by changes
// - In a 50-package monorepo, a typical PR affects 3-5 packages
// - CI time: 50 packages -> 5 packages = 10x faster

// 4. SEPARATE TYPE CHECKING FROM BUILDING
// - Type checking (tsc --noEmit) can be a fast-fail gate
// - If types are wrong, don't waste time on build/test
//
// Example pipeline:
// 1. Lint (10s) — parallel
// 2. Typecheck (30s) — parallel, depends on lint
// 3. Build (20s) — depends on typecheck
// 4. Test (60s) — depends on build, parallel across packages
// 5. E2E test (120s) — depends on build, sequential
//
// Total with affected: ~3-5 minutes
// Total without optimization: ~20-30 minutes
```

---

## Interview Questions

### Q1: What are the key differences between Turborepo and Nx?

**Answer:** Both are task runners for monorepos. Turborepo is simpler — configuration lives in turbo.json, focuses on task orchestration and caching. Nx is more feature-rich — provides generators, affected commands, dependency graph visualization, and plugins for frameworks. Turborepo uses pnpm/yarn workspaces; Nx has its own workspace structure. Choose Turborepo for simplicity, Nx for larger teams needing code generation and enforcement.

### Q2: How do TypeScript project references work in a monorepo?

**Answer:** Project references tell TypeScript about the dependency graph between packages. Each package uses `composite: true` and emits `.d.ts` files. When building, TypeScript compiles in dependency order and caches type information in `.tsbuildinfo` files. On subsequent builds, only packages with changed dependencies are re-checked. This reduces a full monorepo build from minutes to seconds.

### Q3: What is the `workspace:*` protocol in pnpm?

**Answer:** `workspace:*` tells pnpm to link a local package from the workspace instead of installing from the registry. In `package.json`: `"@myorg/shared": "workspace:*"` means "use the local packages/shared directory." pnpm automatically creates symlinks in node_modules. This ensures type changes in shared are immediately visible to dependent packages.

### Q4: How would you prevent circular dependencies in a TypeScript monorepo?

**Answer:**
1. Use ESLint `import/no-restricted-paths` to define allowed import zones
2. Use `madge --circular` in CI to detect circular dependencies
3. Enforce a layered architecture (shared <- api <- web)
4. Use Nx's dependency graph (`nx graph`) to visualize dependencies
5. Create dedicated types packages for shared type definitions

### Q5: How do you share TypeScript configurations across packages?

**Answer:** Create a base `tsconfig.base.json` in the root with shared compiler options. Each package extends it: `"extends": "../../tsconfig.base.json"`. Package-specific overrides (jsx, types, outDir) go in the package's tsconfig.json. For different environments (node, browser), create specialized base configs (`tsconfig.node.json`, `tsconfig.browser.json`).

### Q6: Explain the Turborepo pipeline configuration.

**Answer:** turbo.json defines tasks and their dependencies. `"dependsOn": ["^build"]` means "build all upstream dependencies first." `"outputs": ["dist/**"]` defines what to cache. `"inputs": ["src/**"]` defines what triggers a rebuild. When a package changes, Turborepo re-runs tasks for that package and all downstream consumers.

### Q7: When would you use `nx affected` over `turbo run`?

**Answer:** `nx affected` compares against a base branch to determine exactly which packages changed, running only those. Turborepo's caching achieves similar results but relies on input hashing rather than git diff analysis. `nx affected` is better for CI pipelines in large monorepos where git-awareness reduces unnecessary work. Turborepo is simpler to set up and sufficient for most cases.

### Q8: How do you handle version publishing in a TypeScript monorepo?

**Answer:** Use tools like `changesets` or `lerna` alongside your workspace manager. Changesets tracks changes per package, creates version bumps, and updates cross-package dependencies. Each package has its own version number. When shared is updated, dependent packages (api, web) get updated dependency versions. TypeScript ensures type compatibility across version boundaries.
