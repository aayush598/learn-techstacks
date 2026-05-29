# Section 02: Path Aliases & Module Resolution

## Overview

Path aliases provide clean, maintainable import paths throughout the codebase. By configuring `@/` for source files and `@voice-agent/` for internal packages, we eliminate deeply nested relative imports and make code easier to refactor.

## The Problem with Relative Imports

```typescript
// Without path aliases — hard to read and refactor
import { AgentService } from "../../../services/agent.service";
import { prisma } from "../../../../../packages/db/src/client";
import { Button } from "../../../components/ui/button";
import type { Agent } from "../../../types/agent";

// With path aliases — clean and unambiguous
import { AgentService } from "@/services/agent.service";
import { prisma } from "@voice-agent/db/client";
import { Button } from "@voice-agent/ui";
import type { Agent } from "@/types/agent";
```

## Path Alias Configuration

### Root TypeScript Configuration

```jsonc
// packages/config/typescript/base.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@voice-agent/ui": ["../../packages/ui/src"],
      "@voice-agent/ui/*": ["../../packages/ui/src/*"],
      "@voice-agent/db": ["../../packages/db/src"],
      "@voice-agent/db/*": ["../../packages/db/src/*"],
      "@voice-agent/voice": ["../../packages/voice/src"],
      "@voice-agent/voice/*": ["../../packages/voice/src/*"],
      "@voice-agent/ai": ["../../packages/ai/src"],
      "@voice-agent/ai/*": ["../../packages/ai/src/*"],
      "@voice-agent/types": ["../../packages/types/src"],
      "@voice-agent/types/*": ["../../packages/types/src/*"]
    }
  }
}
```

### Per-Application Config

Each application extends the root and adds its own `@/` alias:

```jsonc
// apps/web/tsconfig.json
{
  "extends": "@voice-agent/config-typescript/nextjs.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@voice-agent/db": ["../../packages/db/src"],
      "@voice-agent/ui": ["../../packages/ui/src"],
      "@voice-agent/types": ["../../packages/types/src"]
    }
  }
}
```

```text
┌─────────────────────────────────────────────────────────────┐
│                  Path Alias Resolution Order                 │
│                                                              │
│  Import: @voice-agent/db/client                              │
│                                                              │
│  ┌──────────────────────┐                                    │
│  │ 1. Check paths in     │                                    │
│  │    local tsconfig     │                                    │
│  └──────────┬───────────┘                                    │
│             │                                                 │
│             ▼                                                 │
│  ┌──────────────────────┐                                    │
│  │ 2. Match @voice-agent │                                    │
│  │    /db/* → ../../     │                                    │
│  │    packages/db/src/*  │                                    │
│  └──────────┬───────────┘                                    │
│             │                                                 │
│             ▼                                                 │
│  ┌──────────────────────┐                                    │
│  │ 3. Resolve to:        │                                    │
│  │    ../../packages/    │                                    │
│  │    db/src/client.ts   │                                    │
│  └──────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

## Bundle Resolver Configuration

Path aliases in tsconfig only help TypeScript. We need to configure bundlers to understand the same aliases.

### Next.js Configuration

```typescript
// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: [
    "@voice-agent/ui",
    "@voice-agent/db",
    "@voice-agent/types",
  ],
};

module.exports = nextConfig;
```

Next.js automatically reads `compilerOptions.paths` from `tsconfig.json` and configures Webpack/Turbopack accordingly.

### Jest / Vitest Configuration

```typescript
// apps/web/vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@voice-agent/db": path.resolve(__dirname, "../../packages/db/src"),
      "@voice-agent/types": path.resolve(__dirname, "../../packages/types/src"),
    },
  },
  test: {
    // ...
  },
});
```

### ESLint Configuration

ESLint needs the `import/resolver` plugin to resolve aliases:

```typescript
// packages/config/eslint/base.ts
export const baseConfig = [
  {
    settings: {
      "import/resolver": {
        typescript: {
          alwaysTryTypes: true,
          project: [
            "apps/*/tsconfig.json",
            "packages/*/tsconfig.json",
          ],
        },
      },
    },
  },
];
```

## Barrel Exports

Barrel files (re-exporting index files) create clean public APIs for each package:

```typescript
// packages/ui/src/index.ts — barrel exports
export { Button } from "./components/ui/button";
export type { ButtonProps } from "./components/ui/button";
export { Input } from "./components/ui/input";
export type { InputProps } from "./components/ui/input";
export { Card, CardHeader, CardContent } from "./components/ui/card";
export { Sidebar } from "./components/layout/sidebar";
export { DataTable } from "./components/layout/data-table";
export { PhoneInput } from "./components/forms/phone-input";
export { cn } from "./utils/cn";
export { colors } from "./tokens/colors";
```

```typescript
// packages/db/src/index.ts — barrel exports
export { prisma } from "./client";
export { AgentRepository, agentRepository } from "./repositories/agent.repo";
export { CallRepository, callRepository } from "./repositories/call.repo";
export type { AgentWithRelations } from "./types";
```

### Barrel Export Best Practices

```typescript
// ✅ Good: Named exports from barrel
import { Button, Card } from "@voice-agent/ui";

// ✅ Good: Specific sub-path import for tree-shaking
import { colors } from "@voice-agent/ui/tokens";

// ❌ Avoid: Namespace imports that defeat tree-shaking
import * as UI from "@voice-agent/ui";
```

## Module Resolution Strategy

```typescript
// packages/db/src/client.ts
import { PrismaClient } from "@prisma/client";

// packages/db/src/repositories/agent.repo.ts
import { prisma } from "../client"; // Relative import within package

// apps/api/src/services/agent.service.ts
import { agentRepository } from "@voice-agent/db"; // Workspace import
import type { CreateAgentRequest } from "@/schemas/agent.schema"; // Source alias
```

### Resolution Order

```
1. Relative imports (./ or ../) — resolved relative to importing file
2. Workspace packages (@voice-agent/*) — resolved via paths in tsconfig
3. Source aliases (@/*) — resolved to ./src/*
4. Node modules (react, zod) — resolved from node_modules
```

## Design Decisions

### @/ vs ~/ or @app/

We chose `@/` because it's the convention established by Next.js and Vue.js, making it familiar to most frontend developers. The `@voice-agent/` namespace clearly distinguishes internal packages from application code.

### Why not use relative imports within packages?

Within a single package, relative imports are acceptable. The alias pattern is primarily for cross-package imports and for application code that would otherwise use deeply nested relatives like `../../../components/button`.

## Integration Points

- **VS Code**: Automatically resolves aliases when jumping to definitions
- **Next.js**: Built-in support via tsconfig paths
- **Vitest**: Must be configured with `resolve.alias`
- **Storybook**: Uses the same tsconfig as the main app
- **ESLint**: Plugin ensures imports respect type-only syntax

## Production Considerations

1. **Path collisions**: If a package name starts with `@/`, aliases will conflict. Use distinct prefixes: `@voice-agent/` for packages, `@/` for source
2. **Build tools**: Every build tool (esbuild, Webpack, Turbopack, tsc) must be configured with the same aliases. Missing one causes cryptic resolution errors
3. **Monorepo path drift**: When packages are extracted from the monorepo, their path aliases break. Use build-time substitution or a build step that rewrites paths
4. **Circular barrels**: Two barrel files that import each other create circular dependencies. Use direct file imports between packages that depend on each other
5. **TypeScript path resolution in CI**: Ensure `tsconfig.json` paths are available during CI type checking. The `tsc` CLI should be run from the workspace root or with explicit project references
