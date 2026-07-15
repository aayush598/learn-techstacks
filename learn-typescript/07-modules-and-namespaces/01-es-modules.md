# ES Modules in TypeScript

## Table of Contents

- [Overview](#overview)
- [Named Exports](#named-exports)
- [Default Exports](#default-exports)
- [Re-exports](#re-exports)
- [Type-Only Imports](#type-only-imports)
- [Dynamic Imports](#dynamic-imports)
- [Barrel Files](#barrel-files)
- [Module Augmentation](#module-augmentation)
- [Global Augmentation](#global-augmentation)
- [ESM in Node.js with TypeScript](#esm-in-nodejs-with-typescript)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

ES Modules (ESM) are the official standard module system for JavaScript, introduced in ES2015. TypeScript fully supports ES module syntax and compiles it to various module formats. Every TypeScript file is treated as a module by default if it contains any `import` or `export` statement.

```typescript
// math.ts — this file is a module because it has exports
export function add(a: number, b: number): number {
  return a + b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}
```

```typescript
// main.ts
import { add, multiply } from './math';

console.log(add(2, 3));       // 5
console.log(multiply(2, 3));  // 6
```

### Key Concepts

- **Module scope**: Top-level variables, functions, classes, and interfaces are scoped to the module — they are NOT global.
- **Strict mode**: ESM is always in strict mode.
- **Static analysis**: The import/export structure is determined at parse time, enabling tree-shaking and static analysis.
- **Circular dependency handling**: ESM handles circular dependencies differently from CommonJS (see module resolution notes).

---

## Named Exports

Named exports allow you to export multiple values from a single module by name.

```typescript
// types.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Post {
  id: number;
  title: string;
  body: string;
  authorId: number;
}

export type UserRole = 'admin' | 'editor' | 'viewer';

export const MAX_POSTS_PER_PAGE = 20;
```

### Importing Named Exports

```typescript
// Method 1: Inline imports
import { User, Post, UserRole, MAX_POSTS_PER_PAGE } from './types';

// Method 2: Import with renaming (aliasing)
import { User as UserType, Post as PostType } from './types';

// Method 3: Namespace import — all exports under one namespace
import * as Types from './types';

function createUser(name: string, email: string): Types.User {
  return { id: 1, name, email };
}
```

### Exporting Individual Declarations

```typescript
// You can export declarations directly
export const API_URL = 'https://api.example.com';

export class ApiClient {
  async get<T>(path: string): Promise<T> {
    const response = await fetch(`${API_URL}${path}`);
    return response.json();
  }
}

export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}
```

### Export List

```typescript
// utils.ts
function internalHelper(): void {
  console.log('internal');
}

export function publicMethodA(): void {
  internalHelper();
}

export function publicMethodB(): void {
  internalHelper();
}

// Re-export only specific items
export { publicMethodA, publicMethodB };
```

---

## Default Exports

Each module can have exactly one default export. The importing side can choose any name for it.

```typescript
// logger.ts
export default class Logger {
  private context: string;

  constructor(context: string) {
    this.context = context;
  }

  log(message: string): void {
    console.log(`[${this.context}] ${message}`);
  }

  error(message: string): void {
    console.error(`[${this.context}] ERROR: ${message}`);
  }
}
```

```typescript
// Importing default exports — you can name it anything
import Logger from './logger';
import MyLogger from './logger';
import L from './logger'; // even a single letter

const log = new Logger('App');
log.log('Application started');
```

### Default Export of Functions and Expressions

```typescript
// config.ts
export default {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
  retries: 3,
};

// middleware.ts
export default function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
}
```

### Combining Default and Named Exports

```typescript
// types.ts
export interface Config {
  apiUrl: string;
  timeout: number;
}

export interface Logger {
  log(message: string): void;
  error(message: string): void;
}

export default function createApp(config: Config): void {
  console.log(`App created with API: ${config.apiUrl}`);
}
```

### Named vs Default Exports — When to Use Which

| Scenario | Use |
|---|---|
| Module exports a single primary thing | Default export |
| Module exports multiple utilities/types | Named exports |
| You want refactoring-friendly imports | Named exports |
| You want the consumer to decide the name | Default export |
| React components (convention) | Default export |
| Utility libraries (e.g., lodash) | Named exports |

> **Best Practice**: Prefer named exports in library code because they provide better auto-import support in IDEs, are more explicit, and make refactoring easier.

---

## Re-exports

Re-exports allow you to aggregate and forward exports from other modules without importing them locally.

```typescript
// types/index.ts — aggregates all type definitions

// Re-export everything from sub-modules
export * from './user-types';
export * from './post-types';
export * from './common-types';

// Re-export specific items
export { type AdminRole, type ViewerRole } from './user-roles';

// Re-export with renaming
export { type UserDTO as UserResponse } from './user-types';
```

### Re-export Patterns

```typescript
// Pattern 1: Selective re-exports
export { createLogger, Logger } from './logger';
export { formatDate, formatTime } from './formatters';
export type { LoggerOptions } from './logger';

// Pattern 2: Namespace re-export
export * as validation from './validation';
export * as auth from './auth';

// Pattern 3: Default re-export
export { default as Express } from 'express';
export { default as createApp } from './app';
```

---

## Type-Only Imports

Type-only imports are erased entirely at compile time. They ensure you are not accidentally pulling in runtime code.

```typescript
// interfaces.ts
export interface User {
  id: number;
  name: string;
}

export const USER_ROLES = ['admin', 'editor', 'viewer'] as const;
```

```typescript
// BAD: imports the entire module including the runtime value USER_ROLES
import { User, USER_ROLES } from './interfaces';

// GOOD: type-only import — no runtime code is emitted
import type { User } from './interfaces';
import { USER_ROLES } from './interfaces';

// Combined type-only and value imports in a single statement
import { USER_ROLES, type User } from './interfaces';
```

### Type-Only Exports

```typescript
// You can also export types explicitly
export type { User } from './interfaces';
export type { Post, Comment } from './models';

// In TypeScript 4.5+, inline type modifiers
export { type User, type Post, createPost } from './models';
```

### Why Type-Only Imports Matter

```typescript
// Without "type", TypeScript might emit a require() for User
// even though it's only used as a type annotation.
// This can cause circular dependency issues and bundle bloat.

// BEFORE (potentially problematic):
import { User } from './heavy-module'; // might emit runtime import

// AFTER (explicitly erased):
import type { User } from './heavy-module'; // guaranteed erased
```

---

## Dynamic Imports

Dynamic imports allow you to lazily load modules at runtime, enabling code splitting and conditional loading.

```typescript
// Basic dynamic import
async function loadChartLibrary() {
  const { Chart } = await import('./chart-library');
  return new Chart();
}

// Dynamic import with type annotation
const module = await import('./my-module');
module.default(); // for default export
module.someFunction(); // for named export
```

### Conditional Dynamic Imports

```typescript
async function getAnalyticsService() {
  if (process.env.NODE_ENV === 'production') {
    const { ProductionAnalytics } = await import('./analytics/production');
    return new ProductionAnalytics();
  } else {
    const { DevelopmentAnalytics } = await import('./analytics/development');
    return new DevelopmentAnalytics();
  }
}
```

### Dynamic Import in React

```typescript
import React, { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Type Assertions for Dynamic Imports

```typescript
// Force the type of a dynamic import
const { default: Chart } = await import(
  /* webpackChunkName: "chart" */
  /* webpackMode: "lazy" */
  './chart-library'
) as { default: typeof Chart };
```

---

## Barrel Files

Barrel files (typically `index.ts`) re-export everything from a directory to provide a single import point.

```typescript
// models/user.ts
export class User { /* ... */ }

// models/post.ts
export class Post { /* ... */ }

// models/comment.ts
export class Comment { /* ... */ }

// models/index.ts — barrel file
export { User } from './user';
export { Post } from './post';
export { Comment } from './comment';

// Consumer can now import from the directory
import { User, Post, Comment } from './models';
```

### Barrel File Best Practices

```typescript
// Prefer explicit re-exports over wildcard re-exports for better control
// AVOID:
export * from './user';
export * from './post';

// PREFER:
export { User, type UserType } from './user';
export { Post, type PostType } from './post';
```

---

## Module Augmentation

Module augmentation lets you extend existing modules with new declarations.

```typescript
// Extend the Express Request type
// types/express.d.ts
import 'express';

declare module 'express' {
  interface Request {
    userId?: string;
    userRole?: 'admin' | 'editor' | 'viewer';
  }
}

// Now in your middleware:
app.use((req, res, next) => {
  req.userId = '123';       // TypeScript knows about this property
  req.userRole = 'admin';   // No type error!
  next();
});
```

### Augmenting Third-Party Modules

```typescript
// augmenting the 'lodash' module
declare module 'lodash' {
  export function shuffle<T>(array: T[]): T[];
  export function uniqueId(prefix?: string): string;

  // You can add entire new namespaces
  namespace helpers {
    function deepClone<T>(obj: T): T;
  }
}
```

### Conditional Module Augmentation

```typescript
// Only augment if the module exists
declare module 'optional-dep' {
  export function doSomething(): void;
}

// Augment a module's types without modifying its runtime behavior
declare module 'my-app-config' {
  interface AppConfig {
    apiUrl: string;
    debug: boolean;
  }
}
```

---

## Global Augmentation

Global augmentation adds types to the global scope, making them available everywhere without imports.

```typescript
// global.d.ts
declare global {
  interface Window {
    __APP_VERSION__: string;
    __CONFIG__: {
      apiUrl: string;
      environment: string;
    };
  }

  // Add global types
  type Nullable<T> = T | null;
  type Optional<T> = T | undefined;

  // Add global functions
  function assertNever(value: never): never;

  // Add global constants
  const IS_DEV: boolean;
}

export {}; // this file must be a module for global augmentation to work
```

```typescript
// Now usable everywhere without import:
function initApp() {
  console.log(window.__APP_VERSION__);
  const config = window.__CONFIG__;
  const name: Nullable<string> = null;
}
```

---

## ESM in Node.js with TypeScript

### Configuration

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "module": "node16",          // or "nodenext"
    "moduleResolution": "node16", // matches module
    "target": "es2022",
    "outDir": "./dist",
    "declaration": true
  }
}
```

### package.json Setup

```json
{
  "name": "my-esm-package",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./utils": {
      "import": "./dist/utils.js",
      "types": "./dist/utils.d.ts"
    }
  }
}
```

### Writing ESM-Compatible TypeScript for Node.js

```typescript
// IMPORTANT: In ESM with Node16 module resolution, you MUST include file extensions
import { readFile } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// For relative imports, use .js extension (even though source is .ts)
import { helper } from './utils.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

### Common Pitfalls in Node ESM + TypeScript

```typescript
// WRONG: Missing file extension in ESM
import { helper } from './utils'; // Error in Node16 module resolution

// CORRECT:
import { helper } from './utils.js';

// WRONG: Using require() in ESM
const utils = require('./utils'); // Error: require is not defined

// CORRECT: Use dynamic import
const utils = await import('./utils.js');
```

### Dual Package Pattern (ESM + CJS)

```typescript
// src/index.ts — the source file
export function greet(name: string): string {
  return `Hello, ${name}!`;
}
```

```json
// tsconfig.esm.json
{
  "compilerOptions": {
    "module": "node16",
    "outDir": "./dist/esm",
    "declaration": true
  }
}

// tsconfig.cjs.json
{
  "compilerOptions": {
    "module": "commonjs",
    "outDir": "./dist/cjs",
    "declaration": true
  }
}
```

---

## Best Practices

1. **Use named exports by default** — they provide better tree-shaking, IDE support, and refactoring safety.

2. **Always use `import type`** when importing only types — it prevents runtime module loading and circular dependencies.

3. **Keep barrel files small and focused** — don't create one mega barrel for an entire application.

4. **Avoid circular dependencies** — they cause initialization bugs that are hard to debug.

5. **Use file extensions in ESM Node.js** — Node16/Nodenext resolution requires `.js` extensions on relative imports.

6. **Prefer `node16` or `nodenext` over `node`** — the older `node` resolution doesn't handle ESM correctly.

7. **Explicitly declare re-exports** — avoid `export * from` in public APIs to prevent accidentally exposing internals.

8. **Use dynamic imports for code splitting** — lazily load heavy modules that aren't needed immediately.

9. **Leverage module augmentation** to extend third-party types rather than monkey-patching.

10. **Keep `.d.ts` files for global augmentation** in a dedicated file (e.g., `global.d.ts`) with `export {}` at the bottom.

---

## Interview Questions

### Q1: What is the difference between `export default` and named exports?

**Answer**: Default exports allow one exported value per module, imported without braces using any name the consumer chooses. Named exports export multiple values by name, imported with braces and can be aliased. Named exports are better for tree-shaking, auto-imports, and explicitness.

### Q2: What does `import type` do differently from `import`?

**Answer**: `import type` is completely erased at compile time — no JavaScript runtime code is emitted for it. This prevents accidentally importing runtime values, avoids circular dependency issues, and ensures zero runtime cost for type-only imports.

### Q3: Why do you need `.js` extensions in ESM TypeScript for Node.js?

**Answer**: Node.js ESM requires explicit file extensions for resolution. TypeScript compiles `.ts` to `.js`, so the runtime file is `.js`. TypeScript's `node16`/`nodenext` resolution enforces this at type-checking time to match Node.js runtime behavior.

### Q4: What is a barrel file and what are its downsides?

**Answer**: A barrel file (`index.ts`) re-exports from sub-modules to provide a single import point. Downsides: increased compilation time (TypeScript must resolve the entire barrel chain), potential circular dependency issues, reduced tree-shaking effectiveness, and larger bundle sizes when wildcard re-exports are used.

### Q5: What is module augmentation?

**Answer**: Module augmentation allows you to add new declarations to existing modules without modifying the original source. You use `declare module 'module-name'` to extend its types. Common use: adding custom properties to Express's `Request` or extending library types.

### Q6: Explain the difference between `export *` and explicit named re-exports.

**Answer**: `export * from './module'` re-exports all named exports (except default). Explicit re-exports (`export { foo, bar } from './module'`) only re-export specified items. Explicit re-exports are preferred in public APIs because they prevent accidentally exposing internal types or functions.

### Q7: How does TypeScript handle circular module dependencies?

**Answer**: TypeScript allows circular imports but warns about them. At runtime, ESM handles cycles by providing partially initialized module namespaces — imports may reference undefined values if the exporting module hasn't finished executing yet. This can cause subtle runtime bugs, so circular dependencies should be avoided.

### Q8: What is `moduleResolution` and why does it matter?

**Answer**: `moduleResolution` controls how TypeScript resolves module specifiers to actual files. Options include `node` (classic Node.js resolution), `node16` (ESM-aware), `bundler` (for bundler environments), and `classic` (legacy). Wrong setting causes incorrect path resolution, missing types, or runtime errors.

### Q9: What is global augmentation and when would you use it?

**Answer**: Global augmentation adds types to the global scope without any import needed. You use `declare global { ... }` inside a `.d.ts` file (that must be a module via `export {}`). Use case: adding global utility types, extending `Window`, or declaring global constants.
