# Path Mapping in TypeScript

## Table of Contents

- [Overview](#overview)
- [paths in tsconfig](#paths-in-tsconfig)
- [baseUrl with paths](#baseurl-with-paths)
- [Wildcard Patterns](#wildcard-patterns)
- [Path Mapping for Aliases](#path-mapping-for-aliases)
- [Path Mapping with Bundlers](#path-mapping-with-bundlers)
- [Non-Relative Module Paths](#non-relative-module-paths)
- [rootDir and outDir](#rootdir-and-outdir)
- [Project References for Path Mapping](#project-references-for-path-mapping)
- [Troubleshooting Path Mapping](#troubleshooting-path-mapping)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Path mapping in TypeScript lets you define custom module resolution paths using the `paths` field in `tsconfig.json`. This enables import aliases, clean directory-relative imports, and better project organization without relying on bundler-specific configurations.

```typescript
// Without path mapping (ugly relative paths):
import { Button } from '../../../components/Button';
import { formatDate } from '../../../utils/date';
import { User } from '../../../models/User';

// With path mapping (clean aliases):
import { Button } from '@components/Button';
import { formatDate } from '@utils/date';
import { User } from '@models/User';
```

---

## paths in tsconfig

### Basic Configuration

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@app/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"],
      "@models/*": ["src/models/*"]
    }
  }
}
```

### How paths Work

The `paths` field maps a pattern (key) to one or more resolution paths (value array).

```jsonc
{
  "paths": {
    // Map @components/Button to src/components/Button
    "@components/Button": ["src/components/Button"],
    // The file extension is NOT needed — TypeScript handles it
  }
}
```

```typescript
// Usage
import { Button } from '@components/Button';
// TypeScript resolves this to: src/components/Button.ts (or .tsx, .d.ts)
```

### Multiple Resolution Paths

```jsonc
{
  "paths": {
    // Try src first, then lib, then types
    "@shared/*": ["src/shared/*", "lib/shared/*", "types/shared/*"]
  }
}
```

TypeScript tries each path in order and uses the first one that resolves successfully.

---

## baseUrl with paths

`baseUrl` sets the root directory for all non-relative imports. It's often used alongside `paths`.

### Without baseUrl

```jsonc
{
  "compilerOptions": {
    "paths": {
      "@components/*": ["./src/components/*"]
    }
    // paths without baseUrl requires "./" prefix in values
  }
}
```

### With baseUrl

```jsonc
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@components/*": ["components/*"],
      "@utils/*": ["utils/*"]
    }
    // baseUrl = "./src" means values are relative to src/
  }
}
```

### Without Paths

```jsonc
{
  "compilerOptions": {
    "baseUrl": "./src"
    // No paths configured
  }
}
```

```typescript
// With baseUrl only (no paths), TypeScript resolves non-relative imports
// by looking in the baseUrl directory:
import { Button } from 'components/Button';
// resolves to: src/components/Button.ts
```

> **Warning**: Using `baseUrl` without `paths` can cause unexpected resolution. It's generally recommended to use `paths` explicitly rather than relying on `baseUrl` alone.

### Recommended Pattern

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
    // baseUrl at project root, paths define all aliases explicitly
  }
}
```

---

## Wildcard Patterns

Path mapping supports wildcard characters (`*`) for flexible resolution.

### Single Wildcard

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@shared/*": ["src/shared/*"]
    }
  }
}
```

```typescript
// The * captures the rest of the import path
import { Button } from '@components/Button';
// * = "Button" → resolves to src/components/Button

import { Badge } from '@components/Badge/Icon';
// * = "Badge/Icon" → resolves to src/components/Badge/Icon
```

### Multiple Wildcards

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@store/*/actions": ["src/store/*/actions"],
      "@store/*/reducers": ["src/store/*/reducers"]
    }
  }
}
```

```typescript
import { fetchUsers } from '@store/users/actions';
// resolves to: src/store/users/actions.ts

import { usersReducer } from '@store/users/reducers';
// resolves to: src/store/users/reducers.ts
```

### Wildcard with Fixed Suffix

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@models/*": ["src/models/*"],
      "@models": ["src/models/index"]
    }
  }
}
```

```typescript
import { User } from '@models/User';   // matches @models/*
import { User } from '@models';         // matches @models (exact) → src/models/index
```

---

## Path Mapping for Aliases

### Full Path Alias Setup

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"],
      "@services/*": ["src/services/*"],
      "@types/*": ["src/types/*"],
      "@assets/*": ["src/assets/*"],
      "@styles/*": ["src/styles/*"]
    },
    "strict": true,
    "target": "es2020",
    "module": "esnext",
    "moduleResolution": "bundler"
  },
  "include": ["src"]
}
```

### Usage

```typescript
// Clean, scannable imports
import { Button, Card, Modal } from '@components';
import { useAuth, useTheme } from '@hooks';
import { formatDate, capitalize } from '@utils';
import { UserService } from '@services/UserService';
import type { User, Post } from '@types';
```

### Absolute Import Without Aliases

```typescript
// With baseUrl = "./src" and no paths:
import { Button } from 'components/Button';
import { formatDate } from 'utils/date';

// This works but makes imports ambiguous (is "utils" a library or local?)
// Path aliases solve this: @utils/date is clearly local
```

---

## Path Mapping with Bundlers

TypeScript's `paths` only affects type checking — you must configure your bundler separately for runtime resolution.

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils'),
      '@hooks': path.resolve(__dirname, 'src/hooks'),
      '@services': path.resolve(__dirname, 'src/services'),
    },
  },
});
```

### Webpack Configuration

```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils'),
    },
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
};
```

### ESLint Import Resolution

```json
// .eslintrc.json
{
  "settings": {
    "import/resolver": {
      "typescript": {
        "project": "./tsconfig.json"
      }
    }
  }
}
```

### Keeping tsconfig and Bundler in Sync

```typescript
// Use a shared config file to avoid duplication:
// path-config.ts
export const aliases = {
  '@': 'src',
  '@components': 'src/components',
  '@utils': 'src/utils',
  '@hooks': 'src/hooks',
  '@services': 'src/services',
} as const;
```

```typescript
// vite.config.ts
import { aliases } from './path-config';
// Convert aliases to Vite format...
```

---

## Non-Relative Module Paths

### Relative vs Non-Relative Imports

```typescript
// Relative: starts with ./ or ../
import { helper } from './utils';
import { Button } from '../components/Button';

// Non-relative (bare specifier): does NOT start with . or ..
import express from 'express';
import { helper } from 'utils';           // with baseUrl
import { Button } from '@components/Button'; // with paths
```

### Resolution Difference

```
Relative imports:
  - Resolved relative to the importing file's directory
  - Always file-system based

Non-relative imports:
  - Resolved by module resolution algorithm
  - Checks node_modules, @types, paths, typeRoots
  - More flexible but less predictable
```

### When to Use Non-Relative

```typescript
// GOOD: Use path aliases for internal modules
import { UserService } from '@services/UserService';
import { useAuth } from '@hooks/useAuth';

// AVOID: Bare specifiers without paths (ambiguous)
import { UserService } from 'services/UserService'; // is this internal or npm?
```

---

## rootDir and outDir

### rootDir

`rootDir` specifies the root directory of input files. It controls the output directory structure.

```jsonc
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist"
  }
}
```

```typescript
// Input: src/components/Button.ts
// Output: dist/components/Button.js

// rootDir ensures the output mirrors the src structure
// Without rootDir, output might include parent directories
```

### rootDir vs baseUrl

```
rootDir:
  - Controls the output directory structure
  - Affects where TypeScript expects source files
  - Does NOT affect import resolution

baseUrl:
  - Controls where non-relative imports resolve from
  - Affects module resolution
  - Does NOT affect output structure

paths:
  - Defines import aliases
  - Works with baseUrl for resolution
  - Requires bundler config for runtime
```

### outDir

```jsonc
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist",
    "declaration": true,
    "declarationDir": "./dist/types"
  }
}
```

### Multiple rootDirs

```jsonc
{
  "compilerOptions": {
    "rootDirs": ["./src", "./generated"],
    "outDir": "./dist"
  }
}
```

```typescript
// rootDirs lets TypeScript treat multiple directories as one
// Useful for generated code alongside hand-written code

// src/services/UserService.ts
import { GeneratedUser } from './generated-types';  // from ./generated/
```

---

## Project References for Path Mapping

For monorepos or large projects, project references provide clean path resolution between projects.

### tsconfig.json (Root)

```jsonc
{
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/app" },
    { "path": "packages/api" }
  ],
  "files": []
}
```

### packages/shared/tsconfig.json

```jsonc
{
  "compilerOptions": {
    "outDir": "./dist",
    "declaration": true,
    "composite": true,  // Required for project references
    "declarationMap": true
  },
  "include": ["src"]
}
```

### packages/app/tsconfig.json

```jsonc
{
  "compilerOptions": {
    "outDir": "./dist",
    "composite": true
  },
  "references": [
    { "path": "../shared" }
  ],
  "include": ["src"]
}
```

```typescript
// In packages/app/src/index.ts:
// TypeScript resolves @myorg/shared via project references
import { SharedUtil } from '@myorg/shared';
```

---

## Troubleshooting Path Mapping

### Common Issues

```typescript
// Issue 1: Path works in editor but not at runtime
// Fix: Configure bundler aliases to match tsconfig paths

// Issue 2: "Cannot find module" with path alias
// Fix: Ensure baseUrl is set and paths pattern matches the import

// Issue 3: Path mapping works for .ts but not .d.ts
// Fix: Ensure declaration files are generated and included

// Issue 4: Circular path mapping
// Fix: Avoid patterns that resolve to the same directory
```

### Debugging Steps

```bash
# 1. Check what TypeScript resolves:
tsc --traceResolution

# 2. Verify the file exists at the resolved path
ls -la src/components/Button.ts

# 3. Check tsconfig is being used correctly
tsc --showConfig

# 4. Restart IDE TypeScript server
# VS Code: Cmd+Shift+P → "TypeScript: Restart TS Server"

# 5. Verify bundler aliases match tsconfig paths
# Check vite.config.ts, webpack.config.js, etc.
```

---

## Best Practices

1. **Use `@/` as the primary alias** — maps to `src/` for all internal imports.

2. **Keep `baseUrl` at `"."` (project root)** — use `paths` for all resolution.

3. **Always configure both TypeScript AND bundler** — `paths` alone only affects type checking.

4. **Use a consistent alias naming convention** — `@components`, `@utils`, `@hooks`, etc.

5. **Don't over-alias** — too many aliases make imports harder to grep and navigate.

6. **Use `paths` with `moduleResolution: "bundler"`** for frontend projects.

7. **Keep `rootDir` and `outDir` configured** to maintain clean output structure.

8. **Use `traceResolution`** when debugging module resolution issues.

9. **Consider `tsc-alias`** to rewrite path aliases in compiled output (for Node.js without bundler).

10. **Document your path aliases** in README or a shared config file for team consistency.

---

## Interview Questions

### Q1: What is the difference between `baseUrl` and `paths`?

**Answer**: `baseUrl` sets the root directory for all non-relative module resolution — any bare specifier is resolved relative to it. `paths` defines specific pattern-to-path mappings that override default resolution. `baseUrl` is like a default path prefix; `paths` gives explicit, fine-grained control.

### Q2: Do TypeScript `paths` work at runtime?

**Answer**: No. `paths` only affects TypeScript's type-checking resolution. At runtime, the JavaScript has no knowledge of path aliases. You must configure your bundler (Vite, webpack, etc.) to resolve these aliases, or use a tool like `tsc-alias` to rewrite them in compiled output.

### Q3: Why do you need to configure path aliases in multiple places?

**Answer**: TypeScript's `paths` is for the compiler/type-checker, webpack/Vite aliases are for the bundler, and ESLint's `import/resolver` is for linting. Each tool has its own resolution system, so they all need to be configured independently to ensure consistency.

### Q4: What is the purpose of `rootDir`?

**Answer**: `rootDir` controls the output directory structure. It tells TypeScript where the root of your source files is, so the output in `outDir` mirrors the source structure. For example, with `rootDir: "./src"` and `outDir: "./dist"`, `src/foo.ts` compiles to `dist/foo.js`.

### Q5: Can you have multiple path patterns that resolve to different directories?

**Answer**: Yes. TypeScript tries each path in the array in order and uses the first successful resolution. You can also have completely different patterns mapped to different directories, like `"@components/*": ["src/components/*"]` and `"@shared/*": ["lib/shared/*"]`.

### Q6: What happens if tsconfig paths and bundler aliases are mismatched?

**Answer**: TypeScript type-checking may pass (if tsconfig resolves correctly), but the bundler fails to find the module at runtime, causing build errors or runtime crashes. Alternatively, the bundler might resolve to a different file, causing type mismatches. Always keep them in sync.

### Q7: What is `tsc-alias` and when would you use it?

**Answer**: `tsc-alias` is a tool that rewrites TypeScript path aliases in compiled JavaScript output. Use it when you're running TypeScript directly (via `ts-node` or Node.js) without a bundler, and you need the aliases to work at runtime.
