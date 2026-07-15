# Tree Shaking in TypeScript

## Table of Contents

1. [What is Tree Shaking](#1-what-is-tree-shaking)
2. [How TypeScript Enables Tree Shaking](#2-how-typescript-enables-tree-shaking)
3. [sideEffects in package.json](#3-sideeffects-in-packagejson)
4. [isolatedModules Flag](#4-isolatedmodules-flag)
5. [Type-Only Imports for Tree Shaking](#5-type-only-imports-for-tree-shaking)
6. [ES Modules for Tree Shaking](#6-es-modules-for-tree-shaking)
7. [Bundler Configuration](#7-bundler-configuration)
8. [Practical Examples](#8-practical-examples)
9. [Best Practices](#9-best-practices)

---

## 1. What is Tree Shaking

Tree shaking is a dead code elimination technique that removes unused exports from your final bundle. The term comes from the concept of shaking a tree to remove dead leaves.

```
Without tree shaking:                    With tree shaking:
┌──────────────────┐                    ┌──────────────────┐
│ math.ts          │                    │ math.ts          │
│  ├── add ✓      │                    │  ├── add ✓      │
│  ├── subtract ✓  │                    │  └── subtract ✓  │
│  ├── multiply ✗  │  ──────────────►  │                  │
│  └── divide ✗    │                    │                  │
│                  │                    │                  │
│ index.ts         │                    │ index.ts         │
│  └── uses add,   │                    │  └── uses add,   │
│     subtract     │                    │     subtract     │
└──────────────────┘                    └──────────────────┘
```

### Key Concepts

```typescript
// math.ts — Library with multiple exports
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export function divide(a: number, b: number): number {
  return a / b;
}

// index.ts — Only uses add and subtract
import { add, subtract } from './math';
console.log(add(1, 2));
console.log(subtract(5, 3));

// With tree shaking, multiply and divide are removed from the bundle
// They are exported but never imported/used
```

---

## 2. How TypeScript Enables Tree Shaking

TypeScript compiles to JavaScript with module syntax that bundlers can analyze. The key is **statically analyzable** imports/exports.

### ES Module Syntax (Required for Tree Shaking)

```typescript
// ✅ ES modules — tree-shakeable
import { add } from './math';
export function greet(name: string) {
  return `Hello, ${name}`;
}

// ❌ CommonJS — NOT tree-shakeable
const math = require('./math');
module.exports = { greet };
```

### Why CommonJS Blocks Tree Shaking

```typescript
// CommonJS: requires are dynamic and can have side effects
const utils = require('./utils');

// This could be inside a conditional, loop, or dynamic expression
if (process.env.NODE_ENV === 'development') {
  const debug = require('./debug-tools');
  debug.enable();
}

// Bundlers can't safely remove anything because:
// 1. require() might have side effects
// 2. The entire module is an object, not individual exports
// 3. Module.exports can be reassigned at runtime
```

### TypeScript Compilation and Tree Shaking

```json
{
  "compilerOptions": {
    "module": "ESNext",      // Output ES module syntax
    "target": "ES2020",
    "moduleResolution": "Node"
  }
}
```

```typescript
// Input TypeScript
import { add, subtract } from './math';
export const result = add(1, 2);

// Compiled JavaScript (with module: ESNext)
import { add, subtract } from './math';
export const result = add(1, 2);

// The bundler (webpack/rollup/esbuild) then analyzes this
// and removes unused imports (subtract)
```

---

## 3. sideEffects in package.json

The `sideEffects` field in `package.json` tells bundlers which files are safe to tree-shake.

```json
{
  "name": "my-library",
  "sideEffects": false
}
```

### What Are Side Effects?

```typescript
// ❌ Side effect: modifies global state
console.log('Initializing library');

// ❌ Side effect: modifies prototype
Array.prototype.customMethod = function() { /* ... */ };

// ❌ Side effect: adds global variable
window.MyLibrary = { /* ... */ };

// ❌ Side effect: modifies CSS
import './styles.css'; // CSS imports are side effects

// ❌ Side effect: runs code on import
const db = connectToDatabase(); // Runs immediately

// ✅ No side effects: pure export
export function add(a: number, b: number): number {
  return a + b;
}
```

### sideEffects Configuration

```json
{
  "sideEffects": false
}

// OR specify which files have side effects
{
  "sideEffects": [
    "./src/polyfills.ts",
    "./src/global-styles.css",
    "./src/setup.ts"
  ]
}
```

### How Bundlers Use sideEffects

```typescript
// math.ts (marked as side-effect-free)
export function add(a: number, b: number) { return a + b; }
export function subtract(a: number, b: number) { return a - b; }

// styles.css (NOT side-effect-free — it's in sideEffects list)
// .button { color: blue; }

// main.ts
import { add } from './math'; // Only 'add' used
import './styles.css'; // Side effect — kept

// With sideEffects: false on math.ts:
// Bundler knows it can safely remove subtract
// Bundler knows styles.css import is kept for side effects
```

### Libraries with sideEffects Configuration

```json
// React
{ "sideEffects": false }

// Lodash
{ "sideEffects": ["./**/*.css"] }

// styled-components
{ "sideEffects": ["./dist/stylesheets/*"] }
```

---

## 4. isolatedModules Flag

The `isolatedModules` flag ensures each file can be independently transpiled, which is required for tree-shaking with tools like Babel, esbuild, and SWC.

```json
{
  "compilerOptions": {
    "isolatedModules": true
  }
}
```

### Why isolatedModules Matters

```typescript
// ❌ Problem: Re-exporting from a script file
// types.ts
type User = { name: string; age: number };

// utils.ts
export { User } from './types'; // Error with isolatedModules!
// TypeScript can't re-export types in isolatedModules mode

// ✅ Fix: Use 'type' keyword
export type { User } from './types';

// ❌ Problem: const enum (inlined by TS, can't be isolated)
const enum Direction {
  Up = 'UP',
  Down = 'DOWN',
}

// ✅ Fix: Use regular enum or string union
enum Direction {
  Up = 'UP',
  Down = 'DOWN',
}

// OR
type Direction = 'UP' | 'DOWN';

// ❌ Problem: Class used as both value and type in re-export
// models.ts
export class User {
  name: string;
  age: number;
}

// ❌ Problem: namespace merging
namespace Utils {
  export function add(a: number, b: number) { return a + b; }
}
export = Utils;
```

### Files That Work with isolatedModules

```typescript
// ✅ Files with only type exports/imports
export type { User, Product, Order } from './types';
import type { Config } from './config';

// ✅ Files with only value exports
export function add(a: number, b: number) { return a + b; }
export const PI = 3.14159;

// ✅ Files with mixed exports (using 'type' keyword)
export type { User } from './types';
export { createUser } from './factory';
```

---

## 5. Type-Only Imports for Tree Shaking

TypeScript provides `import type` and `export type` to explicitly mark imports/exports as type-only. These are completely erased at compile time.

```typescript
// Regular imports — may be treated as value imports
import { User } from './types';

// Type-only imports — guaranteed to be erased
import type { User } from './types';
import type { Product, Order } from './types';

// Inline type-only import
import { type User, createUser } from './factory';
// ↑ User is type-only, createUser is a value import
```

### Why Type-Only Imports Help Tree Shaking

```typescript
// types.ts
export interface User {
  name: string;
  email: string;
}

export class UserBuilder {
  // ... implementation
}

export function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'name' in value;
}

// Without 'import type':
import { User } from './types';
// Compiled to: import { User } from './types';
// Bundler might keep the entire module (or UserBuilder, isUser)

// With 'import type':
import type { User } from './types';
// Compiled to: nothing (completely erased)
// Bundler knows there's nothing to import at runtime
```

### export type Usage

```typescript
// ✅ Export interface as type-only
export type { User, Product, Order } from './types';

// ✅ Re-export type
export type { User } from './types';

// ✅ Mixed exports
export { createUser, UserBuilder } from './factory';
export type { User, Product } from './types';
```

### Performance Impact

```typescript
// Before: Importing a class as type removes the class from bundle
import type { UserService } from './services';
// This import is completely erased — no runtime cost

// After: Importing a class as value keeps it in bundle
import { UserService } from './services';
// This import keeps UserService in the bundle even if only used as type
```

---

## 6. ES Modules for Tree Shaking

ES modules are the foundation of tree shaking. They provide static structure that bundlers can analyze.

### Static vs Dynamic Imports

```typescript
// ✅ Static import — analyzable, tree-shakeable
import { add } from './math';
console.log(add(1, 2));

// ❌ Dynamic import — not tree-shakeable (but useful for code splitting)
const math = await import('./math');
console.log(math.add(1, 2));

// ✅ Dynamic import for code splitting (not tree shaking)
const module = await import('./heavy-module');
// The entire heavy-module is loaded as a chunk
```

### Barrel Files and Tree Shaking

```typescript
// index.ts (barrel file)
export { add, subtract, multiply, divide } from './math';
export { User, Product } from './models';

// If only 'add' is used from importing this barrel:
import { add } from './math';
// A good bundler can still tree-shake the barrel file

// However, barrel files can hurt tree shaking:
// ❌ Large barrel file
export * from './utils';       // Re-exports everything
export * from './models';      // No tree shaking possible
export * from './services';    // Bundler may not be able to remove unused

// ✅ Better: Explicit named exports
export { add, subtract } from './utils';
export { User, Product } from './models';
```

### Barrel File Optimization

```typescript
// ❌ Bad barrel file (prevents tree shaking)
// utils/index.ts
export * from './string-utils';
export * from './number-utils';
export * from './date-utils';
export * from './array-utils';

// ✅ Good barrel file (tree-shakeable)
// utils/index.ts
export { capitalize, lowercase } from './string-utils';
export { add, subtract } from './number-utils';
export { formatDate, parseDate } from './date-utils';
```

---

## 7. Bundler Configuration

### Webpack

```javascript
// webpack.config.js
module.exports = {
  mode: 'production', // Enables tree shaking
  optimization: {
    usedExports: true, // Mark unused exports
    sideEffects: true, // Use sideEffects from package.json
    minimize: true, // Minifier removes dead code
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
};
```

### Rollup

```javascript
// rollup.config.js
export default {
  input: 'src/index.ts',
  output: {
    file: 'dist/bundle.js',
    format: 'es',
  },
  plugins: [typescript()],
  // Rollup tree-shakes by default for ES modules
};
```

### esbuild

```javascript
// esbuild.config.js
require('esbuild').build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/bundle.js',
  format: 'esm',
  treeShaking: true, // Explicitly enable
  minify: true,
});
```

### Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined, // Let Vite optimize
      },
    },
  },
});
```

---

## 8. Practical Examples

### Example: Tree Shaking a Utility Library

```typescript
// utils/math.ts
export function add(a: number, b: number): number { return a + b; }
export function subtract(a: number, b: number): number { return a - b; }
export function multiply(a: number, b: number): number { return a * b; }
export function divide(a: number, b: number): number { return a / b; }

// utils/string.ts
export function capitalize(s: string): string { return s.toUpperCase(); }
export function lowercase(s: string): string { return s.toLowerCase(); }

// utils/index.ts (barrel)
export { add, subtract, multiply, divide } from './math';
export { capitalize, lowercase } from './string';

// main.ts — Only uses add and capitalize
import { add, capitalize } from './utils';

const sum = add(1, 2);
const name = capitalize('hello');

// Before tree shaking: ~2KB (all exports)
// After tree shaking: ~0.5KB (only add and capitalize)
```

### Example: Type-Only Imports in Practice

```typescript
// services/user-service.ts
import type { User, CreateUserDTO } from '../types/user';
import type { Database } from '../database';

export class UserService {
  constructor(private db: Database) {}

  async createUser(dto: CreateUserDTO): Promise<User> {
    return this.db.insert('users', dto);
  }
}

// api/users.ts
import type { UserService } from '../services/user-service';
import type { Request, Response } from 'express';

// These type-only imports are completely erased
// The bundle doesn't include UserService, Request, or Response
```

### Example: Side-Effect-Free Library

```typescript
// package.json
{
  "name": "my-utils",
  "sideEffects": false,
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "types": "./dist/types/index.d.ts"
}

// src/index.ts
export { add, subtract } from './math';
export { capitalize, lowercase } from './string';
export type { MathResult, StringResult } from './types';
```

---

## 9. Best Practices

```typescript
// 1. Always use named exports (not default exports)
// ✅ Named exports — tree-shakeable
export function add(a: number, b: number) { return a + b; }

// ⚠️ Default exports — harder to tree shake (bundler must rename)
export default function add(a: number, b: number) { return a + b; }

// 2. Use 'import type' for type-only imports
import type { User } from './types';

// 3. Keep barrel files explicit
export { add, subtract } from './math';
// NOT export * from './math';

// 4. Mark your package as side-effect-free if applicable
{ "sideEffects": false }

// 5. Use ES module syntax
import { add } from './math';
export { add };

// 6. Avoid side effects in module scope
// ❌
console.log('Initializing');
const globalConfig = loadConfig();

// ✅
export function getConfig() { return loadConfig(); }

// 7. Use --isolatedModules for compatibility with transpilers

// 8. Set correct module target in tsconfig
{
  "module": "ESNext",
  "moduleResolution": "Node"
}
```

---

## Interview Questions

**Q1**: What is tree shaking and how does it differ from dead code elimination?
**A**: Tree shaking specifically targets unused exports in ES modules by analyzing the import/export graph. Dead code elimination (DCE) is broader, removing unreachable code (unused variables, dead branches). Tree shaking is a form of DCE.

**Q2**: Why can't CommonJS modules be tree-shaken?
**A**: CommonJS `require()` is dynamic — it can be called conditionally, in loops, or with dynamic expressions. The entire module is an object, and `module.exports` can be reassigned at runtime. Bundlers can't statically determine which exports are used.

**Q3**: What is the `sideEffects` field in package.json?
**A**: It tells bundlers whether files in the package have side effects (global state changes, prototype modifications, etc.). Setting `sideEffects: false` allows bundlers to safely remove unused exports.

**Q4**: How do `import type` and `export type` help with tree shaking?
**A**: They explicitly mark imports/exports as type-only. TypeScript completely erases these at compile time, so they never appear in the output JavaScript. This guarantees the bundler doesn't need to include the referenced modules.

**Q5**: What is `isolatedModules` and why is it important for tree shaking?
**A**: It ensures each file can be independently transpiled (required by Babel, esbuild, SWC). It prevents TypeScript features that require cross-file analysis (const enums, namespace merging, re-exporting types without `type` keyword).
