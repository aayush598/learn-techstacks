# Module Resolution in TypeScript

## Table of Contents

- [Overview](#overview)
- [Module Resolution Algorithms](#module-resolution-algorithms)
- [Node Module Resolution](#node-module-resolution)
- [Classic Resolution](#classic-resolution)
- [Node16 / Nodenext Resolution](#node16--nodenext-resolution)
- [Bundler Resolution](#bundler-resolution)
- [baseUrl and paths](#baseurl-and-paths)
- [The moduleResolution Option](#the-moduleresolution-option)
- [Extension Resolution](#extension-resolution)
- [package.json "types" Field](#packagejson-types-field)
- [Resolution Cache](#resolution-cache)
- [Debugging Module Resolution](#debugging-module-resolution)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Module resolution is the process TypeScript uses to determine the actual file or module that an import specifier refers to. The resolution algorithm depends on your `moduleResolution` setting and can vary significantly between options. Incorrect resolution is one of the most common sources of TypeScript errors.

```typescript
// TypeScript must resolve these specifiers to actual files:
import { helper } from './utils';       // relative
import express from 'express';          // bare specifier
import type { Config } from '@app/types'; // path mapping
```

---

## Module Resolution Algorithms

### Resolution Strategy Overview

```
Import Specifier
      │
      ├── Starts with "./" or "../" → Relative import
      │         │
      │         └── Resolve relative to importing file's directory
      │
      ├── Starts with "/" → Absolute path
      │
      ├── Starts with "@/" or "~/" → Path mapping (if configured)
      │
      └── Bare specifier ("express", "lodash")
                │
                ├── package.json "exports" (node16/nodenext)
                ├── node_modules resolution
                └── Type roots fallback
```

---

## Node Module Resolution

The `node` moduleResolution emulates Node.js's classic CommonJS resolution algorithm.

### How It Works

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "node"
  }
}
```

### Resolution Steps for Relative Imports

Given `import { helper } from './utils'` in file `/app/services/user.ts`:

1. Try `/app/services/utils.ts`
2. Try `/app/services/utils.tsx`
3. Try `/app/services/utils.d.ts`
4. Try `/app/services/utils/index.ts`
5. Try `/app/services/utils/index.tsx`
6. Try `/app/services/utils/index.d.ts`

```typescript
// Example file structure:
// app/
//   services/
//     user.ts      ← importing file
//     utils.ts     ← resolved here

// user.ts
import { helper } from './utils';
```

### Resolution Steps for Bare Specifiers

Given `import express from 'express'`:

1. Check `node_modules/express/package.json` → `types` / `typings` field
2. Check `node_modules/@types/express/index.d.ts`
3. Check `node_modules/express/index.ts`
4. Check `node_modules/express/index.d.ts`

```
app/
  node_modules/
    express/
      package.json    → { "types": "./index.d.ts" }
      index.d.ts
    @types/
      express/
        index.d.ts
```

### Limitations of "node" Resolution

- Does NOT check `package.json` `exports` field (ESM feature)
- Does NOT require `.js` extensions on relative imports
- Treats all `.ts` files as CJS
- May resolve to different files than Node.js actually resolves

---

## Classic Resolution

The `classic` resolution is TypeScript's original algorithm, rarely used today.

```typescript
{
  "compilerOptions": {
    "moduleResolution": "classic"
  }
}
```

### How It Differs

- For relative imports: same as Node resolution (tries `.ts`, `.d.ts`, then `index.*`)
- For bare specifiers: looks up the directory tree for `node_modules` containing the package
- Does NOT check `@types` packages
- Does NOT use `package.json` `types` field

> **Warning**: `classic` resolution is deprecated for new projects. Use `node`, `node16`, or `bundler` instead.

---

## Node16 / Nodenext Resolution

`node16` and `nodenext` provide ESM-aware resolution that matches Node.js 16+'s actual behavior.

```typescript
{
  "compilerOptions": {
    "module": "node16",
    "moduleResolution": "node16"
  }
}
```

### Key Differences from "node"

1. **Requires `.js` extensions** on relative imports (even for `.ts` source files)
2. **Checks `package.json` `exports`** field
3. **Distinguishes ESM from CJS** based on file extension and package.json `type`
4. **Enforces strict package boundary rules**

### Extension Requirement

```typescript
// WRONG: Missing extension
import { helper } from './utils';
// Error: Relative import paths need explicit file extensions in ECMAScript imports

// CORRECT: Include .js extension (even though source is .ts)
import { helper } from './utils.js';
```

### Package.json Exports Support

```json
// node_modules/some-lib/package.json
{
  "name": "some-lib",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    },
    "./utils": {
      "import": "./dist/utils.mjs",
      "types": "./dist/utils.d.ts"
    }
  }
}
```

```typescript
// TypeScript resolves based on exports map
import { helper } from 'some-lib/utils';  // resolves via exports."./utils"
import something from 'some-lib';         // resolves via exports."."
```

### ESM vs CJS Detection

```
.mts files → always ESM
.cts files → always CJS
.ts files  → depends on package.json "type"
              "type": "module" → ESM
              "type": "commonjs" or omitted → CJS
```

---

## Bundler Resolution

The `bundler` moduleResolution is designed for use with bundlers (webpack, Vite, esbuild, Rollup).

```typescript
{
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler"
  }
}
```

### How It Differs

- Does NOT require `.js` extensions on relative imports (bundlers resolve without them)
- Checks `package.json` `exports` field (like node16)
- Does NOT enforce ESM vs CJS distinction (bundlers handle this)
- More lenient than node16 — designed for development-time checking

### When to Use "bundler"

- Building with **Vite**, **webpack**, **esbuild**, or **Rollup**
- **Not** targeting Node.js directly (e.g., browser apps)
- You want ESM-style imports without the strictness of node16

```typescript
// With bundler resolution, this is fine:
import { helper } from './utils';  // No .js extension needed

// And exports are respected:
import { something } from 'some-lib/subpath';
```

---

## baseUrl and paths

### baseUrl

`baseUrl` sets the base directory for non-relative module resolution.

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "./src"
  }
}
```

```typescript
// With baseUrl = "./src" and src/
//   components/
//     Button.ts
//   utils/
//     helpers.ts

// Without baseUrl, you'd need relative paths:
import { Button } from '../../../components/Button';

// With baseUrl, you can import from src root:
import { Button } from 'components/Button';
```

### paths (Detailed in 05-path-mapping.md)

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@app/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```typescript
// Now you can use path aliases:
import { Button } from '@components/Button';
import { formatDate } from '@utils/date';
import { User } from '@app/models/User';
```

---

## The moduleResolution Option

### Comparison Table

| Feature | classic | node | node16 | nodenext | bundler |
|---|---|---|---|---|---|
| `.js` extensions required | No | No | Yes | Yes | No |
| `package.json` exports | No | No | Yes | Yes | Yes |
| `@types` support | No | Yes | Yes | Yes | Yes |
| ESM/CJS distinction | No | No | Yes | Yes | No |
| `paths` support | Yes | Yes | Yes | Yes | Yes |
| `baseUrl` support | Yes | Yes | Yes | Yes | Yes |
| Intended use | Legacy | Node.js CJS | Node.js ESM | Node.js ESM | Bundlers |

### Recommended Configurations

```typescript
// For a Node.js project using CJS:
{
  "module": "commonjs",
  "moduleResolution": "node"
}

// For a modern Node.js project using ESM:
{
  "module": "node16",
  "moduleResolution": "node16"
}

// For a Vite/React/Vue project:
{
  "module": "esnext",
  "moduleResolution": "bundler"
}

// For maximum future compatibility in Node.js:
{
  "module": "nodenext",
  "moduleResolution": "nodenext"
}
```

---

## Extension Resolution

TypeScript tries several extensions when resolving a module specifier.

### Resolution Order (node resolution)

```
import './foo'

1. ./foo.ts
2. ./foo.tsx
3. ./foo.d.ts
4. ./foo/package.json (reads "types" or "main" field)
5. ./foo/index.ts
6. ./foo/index.tsx
7. ./foo/index.d.ts
```

### Explicit Extensions in Node16

```typescript
// TypeScript only recognizes these extensions for resolution:
import './file.ts'    // ← compiles to ./file.js
import './file.tsx'   // ← compiles to ./file.jsx
import './file.js'    // ← resolves to ./file.ts (type only, not at runtime)
import './file.mts'   // ← resolves to ./file.mts
import './file.cts'   // ← resolves to ./file.cts
import './file.json'  // ← resolves to ./file.json (with resolveJsonModule)

// These are NOT recognized:
import './file.jsx'   // Error (won't resolve to .tsx source)
import './file.mjs'   // Error (won't resolve to .mts source)
```

---

## package.json "types" Field

The `types` field in `package.json` tells TypeScript where to find type definitions.

```json
{
  "name": "my-lib",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

### Resolution Order for Types

```
1. "exports"."."."types"     (node16/nodenext only)
2. "types" / "typings"       (top-level)
3. "main" + .d.ts variant    (e.g., index.js → index.d.ts)
4. index.d.ts in package root
5. @types/package-name       (DefinitelyTyped)
```

### TypesVersions

```json
{
  "name": "my-lib",
  "typesVersions": {
    "*": {
      "v3": ["./dist/v3/index.d.ts"],
      "v2": ["./dist/v2/index.d.ts"]
    }
  }
}
```

```typescript
// TypeScript selects types based on the consuming project's TypeScript version
// or configured paths
```

---

## Resolution Cache

TypeScript caches module resolution results for performance. In watch mode, the cache can sometimes cause stale results.

### Clearing Resolution Cache

```bash
# Delete TypeScript build cache
rm -rf node_modules/.cache
rm -rf dist

# Restart TypeScript server in VS Code
# Cmd+Shift+P → "TypeScript: Restart TS Server"

# Nuclear option: delete all output
rm -rf out/ dist/ *.tsbuildinfo
tsc --build --clean
```

### Resolution Cache in Watch Mode

```typescript
// In watch mode, TypeScript caches resolution results
// If you change module structure, restart the TS server
// to avoid phantom errors from stale cache

// Known issues:
// - Adding new files that should be picked up by globs
// - Changing package.json types/exports fields
// - Installing new @types packages
```

---

## Debugging Module Resolution

### TypeScript's --traceResolution Flag

```bash
# See exactly how TypeScript resolves each import
tsc --traceResolution

# Output shows each step:
// Resolving module './utils' from '/app/services/user.ts'.
//   '/app/services/utils.ts' exists
//   Resolved to: '/app/services/utils.ts'
```

### Common Resolution Errors

```typescript
// Error: Cannot find module './utils' or its corresponding type declarations
// Cause: File doesn't exist or wrong extension

// Error: Module has no default export
// Cause: Using `import x from 'module'` when module only has named exports

// Error: Cannot find module 'express' because it is not declared in 'dependencies'
// Cause: Missing @types/express or package not installed

// Error: Relative import paths need explicit file extensions in ECMAScript imports
// Cause: Using node16/nodenext without .js extensions
```

---

## Best Practices

1. **Use `moduleResolution: "bundler"`** for frontend projects with Vite/webpack.

2. **Use `moduleResolution: "node16"` or `"nodenext"`** for Node.js projects.

3. **Always include `@types` packages** for third-party libraries.

4. **Use `paths` for import aliases** — it provides IDE support without runtime configuration.

5. **Set `types` in `package.json`** when publishing libraries.

6. **Use `--traceResolution`** to debug module resolution issues.

7. **Keep `baseUrl` at the project root** and use `paths` for specific aliases.

8. **Don't mix `moduleResolution: "node"` with ESM packages** — it can't resolve `exports` fields.

9. **When publishing, test that types resolve** in both CJS and ESM consumers.

10. **Use `typeRoots`** if you have custom type definitions outside `node_modules/@types`.

---

## Interview Questions

### Q1: What is the difference between `moduleResolution: "node"` and `"node16"`?

**Answer**: `node` uses Node.js's classic CJS resolution (no extensions required, no `exports` field). `node16` adds ESM awareness: requires `.js` extensions on relative imports, checks `package.json` `exports` field, and distinguishes ESM from CJS files. `node16` matches Node.js 16+'s actual behavior more closely.

### Q2: Why does `moduleResolution: "node16"` require `.js` extensions?

**Answer**: Node.js ESM requires explicit file extensions for resolution. TypeScript compiles `.ts` → `.js`, so the runtime file is `.js`. TypeScript enforces `.js` extensions at type-checking time to ensure the resolution matches what Node.js will do at runtime.

### Q3: What is `moduleResolution: "bundler"` and when should you use it?

**Answer**: It's designed for projects using bundlers (Vite, webpack, esbuild). It supports `exports` field resolution (like node16) but doesn't require `.js` extensions and doesn't enforce ESM/CJS distinction, since bundlers handle these concerns. Use it for frontend projects.

### Q4: How does TypeScript resolve `import 'express'` to find types?

**Answer**: For bare specifiers, TypeScript looks in `node_modules/express/` → checks `package.json` `types` field → falls back to `index.d.ts`. If not found, it checks `node_modules/@types/express/index.d.ts`. The `types` field in `package.json` takes precedence over `@types`.

### Q5: What does the `--traceResolution` flag do?

**Answer**: It outputs detailed logs showing every step TypeScript takes when resolving module imports. For each import, it shows what paths were tried, which ones succeeded or failed, and why. This is invaluable for debugging "Cannot find module" errors.

### Q6: What is the `types` field in `package.json`?

**Answer**: It tells TypeScript where the type definitions for the package are located. For example, `"types": "./dist/index.d.ts"` points TypeScript to the declaration file. Without it, TypeScript looks for `index.d.ts` at the package root or falls back to `@types/package-name`.

### Q7: Can you explain the `exports` field in `package.json` and how TypeScript handles it?

**Answer**: The `exports` field defines entry points for a package, supporting subpath exports. TypeScript (with node16/nodenext) checks this field first for resolution. It supports conditional exports like `"import"` vs `"require"` and `"types"` conditions. This replaces the older `main` and `types` top-level fields for modern packages.
