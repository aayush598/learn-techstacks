# tsconfig.json Deep Dive

## Table of Contents

1. [Target](#1-target)
2. [Module](#2-module)
3. [Lib](#3-lib)
4. [OutDir and RootDir](#4-outdir-and-rootdir)
5. [Include, Exclude, Files](#5-include-exclude-files)
6. [Extends](#6-extends)
7. [Compiler Options Groups](#7-compiler-options-groups)
8. [Composite Projects](#8-composite-projects)
9. [Complete Reference](#9-complete-reference)

---

## 1. Target

Controls which JavaScript version TypeScript compiles to.

```json
{
  "compilerOptions": {
    "target": "ES2022"
  }
}
```

### Available Targets

| Target | Features Downleveled | Output Size |
|--------|---------------------|-------------|
| `ES3` | Everything | Largest |
| `ES5` | async/await, arrow functions, classes, template literals | Large |
| `ES2015` | async/await, generators | Medium |
| `ES2016` | `**` operator | Medium |
| `ES2017` | async/await | Medium |
| `ES2018` | async iteration, rest/spread | Small |
| `ES2019` | optional catch binding | Small |
| `ES2020` | dynamic import, nullish coalescing, optional chaining | Smaller |
| `ES2021` | `replaceAll`, logical assignment | Smaller |
| `ES2022` | class fields, top-level await, `at()` | Smallest |
| `ESNext` | Latest features | Smallest |

### Target Impact

```typescript
// Source
async function fetchData() {
  const response = await fetch('/api');
  return response.json();
}

// Target: ES5 — Downleveled to generator/awaiter
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
  // ... polyfill code
};
function fetchData() {
  return __awaiter(this, void 0, void 0, function* () {
    const response = yield fetch('/api');
    return response.json();
  });
}

// Target: ES2017 — async/await preserved
async function fetchData() {
  const response = await fetch('/api');
  return response.json();
}
```

---

## 2. Module

Controls the module system in the output.

```json
{
  "compilerOptions": {
    "module": "ESNext"
  }
}
```

### Available Module Systems

| Module | Output Syntax | Use Case |
|--------|--------------|----------|
| `CommonJS` | `require()` / `module.exports` | Node.js (legacy) |
| `AMD` | `define()` / `require()` | RequireJS |
| `UMD` | Universal Module Definition | Libraries |
| `System` | `System.import()` | SystemJS |
| `ES6` / `ES2015` | `import` / `export` | ES modules |
| `ES2020` | Dynamic `import()` | Modern bundlers |
| `ES2022` | Top-level `await` | Modern runtimes |
| `ESNext` | Latest module syntax | Latest features |
| `Node16` | Node.js ESM/CJS | Node.js 16+ |
| `NodeNext` | Node.js latest | Node.js latest |

### Module Examples

```typescript
// Source
import { add } from './math';
export const result = add(1, 2);

// module: CommonJS
const math_1 = require('./math');
exports.result = math_1.add(1, 2);

// module: ESNext
import { add } from './math';
export const result = add(1, 2);

// module: NodeNext (with .js extension)
import { add } from './math.js';
export const result = add(1, 2);
```

---

## 3. Lib

Controls which standard library declarations are included.

```json
{
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  }
}
```

### Common Lib Combinations

```json
// Node.js project
{ "lib": ["ES2020"] }

// Browser project
{ "lib": ["ES2020", "DOM", "DOM.Iterable"] }

// Web Worker
{ "lib": ["ES2020", "WebWorker"] }

// Full features
{ "lib": ["ESNext", "DOM", "DOM.Iterable"] }
```

### What Each Lib Provides

```typescript
// ES2020: Promise.allSettled, globalThis, BigInt, etc.
// DOM: document, window, HTMLElement, fetch, etc.
// DOM.Iterable: Array, Map, Set iteration methods
// WebWorker: Worker, postMessage, etc.
// ESNext: Latest features (may change)
```

---

## 4. OutDir and RootDir

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### How They Work

```bash
# Source structure:
src/
  index.ts
  utils.ts
  models/
    user.ts

# With rootDir: "./src" and outDir: "./dist":
dist/
  index.js
  utils.js
  models/
    user.js

# Without rootDir:
dist/
  src/
    index.js
    utils.js
    models/
      user.js
```

### rootDir Inference

```typescript
// TypeScript infers rootDir from the source files
// If all source files are in src/, rootDir is src/

// To override:
{
  "rootDir": "./src",
  "rootDir": "./lib" // Explicit root directory
}

// rootDir must be a parent of all source files
// Otherwise: error TS6059: Root file is not under rootDir
```

---

## 5. Include, Exclude, Files

```json
{
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"],
  "files": ["src/index.ts"]
}
```

### Pattern Syntax

```json
// Glob patterns
"include": [
  "src/**/*",           // All files in src/ recursively
  "src/**/*.ts",        // All .ts files in src/ recursively
  "src/**/*.{ts,tsx}",  // All .ts and .tsx files
  "types/**/*.d.ts",    // All .d.ts files in types/
  "*.ts"                // All .ts files in root
]
```

### Include vs Files

```json
// include: glob patterns (recursive)
{
  "include": ["src/**/*"] // Finds all files recursively
}

// files: specific files (non-recursive)
{
  "files": [
    "src/index.ts",
    "src/types.d.ts"
  ]
}
```

### Exclude Patterns

```json
{
  "exclude": [
    "node_modules",
    "dist",
    "**/*.test.ts",
    "**/*.spec.ts",
    "**/test/**",
    "**/tests/**",
    "**/__tests__/**"
  ]
}
```

---

## 6. Extends

Inherit configuration from a base tsconfig.

```json
// tsconfig.base.json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}

// tsconfig.json (inherits from base)
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"]
}
```

### Extends Patterns

```json
// Single base config
{ "extends": "./tsconfig.base.json" }

// From node_modules
{ "extends": "@tsconfig/node16/tsconfig.json" }

// Multiple levels
// tsconfig.base.json → tsconfig.build.json → tsconfig.json
{
  "extends": "./tsconfig.build.json",
  "compilerOptions": {
    "outDir": "./dist"
  }
}
```

---

## 7. Compiler Options Groups

### Type Checking

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "alwaysStrict": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true
  }
}
```

### Module Resolution

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@utils/*": ["utils/*"]
    },
    "rootDirs": ["./src", "./generated"],
    "typeRoots": ["./types", "./node_modules/@types"],
    "types": ["node", "jest"],
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "isolatedModules": true
  }
}
```

### Emit

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationDir": "./dist/types",
    "declarationMap": true,
    "sourceMap": true,
    "inlineSourceMap": false,
    "inlineSources": false,
    "removeComments": false,
    "noEmit": false,
    "noEmitOnError": true,
    "emitDeclarationOnly": false,
    "importHelpers": false,
    "downlevelIteration": false,
    "isolatedModules": true
  }
}
```

### Interoperability

```json
{
  "compilerOptions": {
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "allowJs": true,
    "checkJs": true,
    "resolveJsonModule": true
  }
}
```

---

## 8. Composite Projects

```json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "declaration": true,
    "declarationMap": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  }
}
```

### Project References

```json
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist"
  }
}

// packages/app/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist"
  },
  "references": [
    { "path": "../core" }
  ]
}

// Root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/app" }
  ],
  "files": []
}
```

---

## 9. Complete Reference

```json
{
  "compilerOptions": {
    // Type Checking
    "strict": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "alwaysStrict": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,

    // Module
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] },
    "rootDirs": ["./src", "./generated"],
    "typeRoots": ["./types"],
    "types": ["node"],
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "isolatedModules": true,
    "allowJs": true,
    "checkJs": true,

    // Emit
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationDir": "./dist/types",
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,
    "noEmit": false,
    "noEmitOnError": true,
    "emitDeclarationOnly": false,
    "importHelpers": false,
    "downlevelIteration": false,

    // Interoperability
    "forceConsistentCasingInFileNames": true,

    // Composite
    "composite": true,
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo",

    // Experimental
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,

    // JSX
    "jsx": "react-jsx"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"],
  "files": [],
  "extends": "./tsconfig.base.json",
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/app" }
  ]
}
```

---

## Interview Questions

**Q1**: What is the difference between `target` and `module` in tsconfig?
**A**: `target` controls JavaScript version (ES5, ES2020, etc.) and determines which syntax is downleveled. `module` controls the module system (CommonJS, ESNext, etc.) and determines import/export syntax.

**Q2**: What does `esModuleInterop` do?
**A**: It allows default imports from CommonJS modules that don't have a default export. Without it, you need `import * as express from 'express'`. With it, you can use `import express from 'express'`.

**Q3**: What is the difference between `include` and `files` in tsconfig?
**A**: `include` uses glob patterns and is recursive. `files` lists specific files and is not recursive. Use `include` for most projects; use `files` when you need precise control.

**Q4**: How do project references work?
**A**: Project references allow you to split a project into multiple sub-projects. Each sub-project has its own tsconfig with `composite: true`. The root tsconfig lists all sub-projects in `references`. Build with `tsc --build`.

**Q5**: What is `composite: true` and when should you use it?
**A**: `composite: true` sets up a project for project references. It implies `declaration: true` and `incremental: true`. Use it when building a monorepo or multi-package project.
