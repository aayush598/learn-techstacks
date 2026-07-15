# Triple-Slash Directives in TypeScript

## Table of Contents

1. [What Are Triple-Slash Directives](#1-what-are-triple-slash-directives)
2. [reference path](#2-reference-path)
3. [reference types](#3-reference-types)
4. [reference lib](#4-reference-lib)
5. [reference no-default-lib](#5-reference-no-default-lib)
6. [When to Use Each](#6-when-to-use-each)
7. [Triple-Slash vs Imports](#7-triple-slash-vs-imports)
8. [History and Modern Usage](#8-history-and-modern-usage)
9. [Best Practices](#9-best-practices)

---

## 1. What Are Triple-Slash Directives

Triple-slash directives are single-line comments containing XML-like tags that instruct the TypeScript compiler about dependencies between files. They are parsed before imports and exports.

```typescript
// Triple-slash directives MUST be at the top of the file
// (before any code, only preceded by comments and other directives)

/// <reference path="./types/global.d.ts" />
/// <reference types="node" />
/// <reference lib="es2020" />

// Code starts after directives
import { add } from './math';
console.log(add(1, 2));
```

### Directive Types Summary

| Directive | Purpose | Example |
|-----------|---------|---------|
| `reference path` | Reference a local `.d.ts` file | `/// <reference path="./types/global.d.ts" />` |
| `reference types` | Include an `@types` package | `/// <reference types="node" />` |
| `reference lib` | Include a specific TypeScript lib | `/// <reference lib="es2020" />` |
| `reference no-default-lib` | Exclude default lib | `/// <reference no-default-lib="true" />` |

---

## 2. reference path

The `reference path` directive includes a specific file in the compilation.

```typescript
/// <reference path="./types/custom.d.ts" />

// This tells the compiler:
// "Include this file in the compilation process"
```

### When to Use

```typescript
// Project structure:
// project/
//   src/
//     index.ts
//     utils.ts
//   types/
//     global.d.ts       ← Contains global declarations
//     custom-modules.d.ts ← Contains module declarations

// src/index.ts
/// <reference path="../types/global.d.ts" />
/// <reference path="../types/custom-modules.d.ts" />

// Now types from those .d.ts files are available:
console.log(API_URL); // From global.d.ts
import { doSomething } from 'untyped-lib'; // From custom-modules.d.ts
```

### Modern Alternative

```json
// tsconfig.json — better than reference path
{
  "include": [
    "src/**/*",
    "types/**/*"
  ]
}
```

```typescript
// The tsconfig.json "include" glob pattern includes
// all .d.ts files in the types/ directory
// No need for triple-slash reference path directives
```

### reference path vs tsconfig include

```typescript
// ✅ Modern approach (tsconfig include)
// tsconfig.json
{
  "include": ["src/**/*", "types/**/*"]
}
// All .d.ts files in types/ are automatically included

// ⚠️ Legacy approach (triple-slash)
// src/index.ts
/// <reference path="../types/global.d.ts" />
// Must manually reference each file

// Use tsconfig include for new projects
// Use reference path only when you can't modify tsconfig
```

---

## 3. reference types

The `reference types` directive includes type declarations from `@types` packages.

```typescript
/// <reference types="node" />
/// <reference types="jest" />
/// <reference types="react" />
/// <reference types="express" />

// These are equivalent to adding packages to the "types" array in tsconfig.json
```

### How It Works

```typescript
/// <reference types="node" />

// Equivalent to:
// tsconfig.json
// {
//   "compilerOptions": {
//     "types": ["node"]
//   }
// }

// Now Node.js types are available:
import * as fs from 'fs';
import * as path from 'path';

// Without reference types "node":
// Error: Cannot find module 'fs'
// Error: Cannot find module 'path'
```

### When to Use reference types

```typescript
// ✅ Use when you need types but can't modify tsconfig.json
// Useful in library code that needs specific types

// Example: A utility library that works with Node.js
/// <reference types="node" />

export function readFileContent(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// ❌ Don't use if you can modify tsconfig.json
// Prefer adding "types" array in tsconfig.json instead
```

---

## 4. reference lib

The `reference lib` directive includes specific TypeScript standard library declarations.

```typescript
/// <reference lib="es2020" />
/// <reference lib="dom" />
/// <reference lib="dom.iterable" />
/// <reference lib="webworker" />
/// <reference lib="esnext" />
```

### Available Lib Options

```typescript
// ECMAScript features
/// <reference lib="es5" />
/// <reference lib="es6" />      // = es2015
/// <reference lib="es2016" />
/// <reference lib="es2017" />
/// <reference lib="es2018" />
/// <reference lib="es2019" />
/// <reference lib="es2020" />
/// <reference lib="es2021" />
/// <reference lib="es2022" />
/// <reference lib="esnext" />

// DOM APIs
/// <reference lib="dom" />
/// <reference lib="dom.iterable" />
/// <reference lib="dom.asynciterable" />
/// <reference lib="webworker" />
/// <reference lib="webworker.iterable" />

// JavaScript features
/// <reference lib="scripthost" />
/// <reference lib="safari" />
```

### When to Use reference lib

```typescript
// Use reference lib when you need specific library features
// but don't want to include everything

// Example: Only ES2020 features (no DOM)
/// <reference lib="es2020" />

// Now Promise.allSettled, globalThis, etc. are available
// But DOM types (document, window) are NOT

// Useful for:
// - Node.js projects (no DOM needed)
// - Browser projects that need specific DOM features
// - Library projects targeting specific environments
```

### lib vs reference lib

```json
// tsconfig.json — better for most projects
{
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  }
}
```

```typescript
// reference lib in source files
/// <reference lib="es2020" />
/// <reference lib="dom" />

// Both approaches include the same libraries
// tsconfig.json "lib" is the modern, recommended approach
// reference lib is for edge cases where you can't modify tsconfig
```

---

## 5. reference no-default-lib

The `reference no-default-lib` directive prevents the compiler from including the default TypeScript library (`lib.d.ts`).

```typescript
/// <reference no-default-lib="true" />

// This removes all built-in TypeScript types:
// - No Array, Object, String, Number
// - No Promise, Map, Set
// - No Error, RegExp
// - No console, setTimeout, etc.
```

### Why It Exists

```typescript
// Used by custom TypeScript implementations
// Example: A custom TypeScript runtime that provides its own standard library

/// <reference no-default-lib="true" />
/// <reference path="./custom-lib.d.ts" />

// Custom lib provides:
declare function customPrint(message: string): void;
// Instead of console.log
```

### Practical Use

```typescript
// Almost never needed in normal projects
// Only use when:
// 1. You're building a custom TypeScript runtime
// 2. You need complete control over available types
// 3. You're working in a constrained environment

// For normal projects, use tsconfig.json:
{
  "compilerOptions": {
    "lib": []  // Include no libs
  }
}
```

---

## 6. When to Use Each

```typescript
// Decision tree:

// Do you need to reference a local .d.ts file?
// → Use reference path (or better: tsconfig include)
/// <reference path="./types/global.d.ts" />

// Do you need types from an @types package?
// → Use reference types (or better: tsconfig types)
/// <reference types="node" />

// Do you need specific standard library features?
// → Use reference lib (or better: tsconfig lib)
/// <reference lib="es2020" />

// Do you need to remove all default types?
// → Use reference no-default-lib (or better: tsconfig lib: [])
/// <reference no-default-lib="true" />

// Modern preference: Use tsconfig.json for all of these
// Use triple-slash directives only when tsconfig isn't available
```

### Practical Examples

```typescript
// Example 1: Node.js project
// src/index.ts
/// <reference types="node" />
import * as http from 'http';

// Example 2: Browser project with specific DOM features
/// <reference lib="dom" />
/// <reference lib="es2020" />

// Example 3: Library with its own type declarations
/// <reference path="../types/custom.d.ts" />

// Example 4: Custom standard library
/// <reference no-default-lib="true" />
/// <reference path="./custom-lib.d.ts" />
```

---

## 7. Triple-Slash vs Imports

```typescript
// TRIPLE-SLASH DIRECTIVES
/// <reference types="node" />
// - Tells compiler to include @types/node in compilation
// - No actual module import
// - Types are available globally

// ES MODULE IMPORTS
import * as fs from 'fs';
// - Actually imports the module at runtime
// - Creates a module dependency
// - Types are scoped to the module

// Key difference:
// reference types: "Include these types in compilation"
// import: "Import this module at runtime and include its types"
```

### When to Use Which

```typescript
// ✅ Use imports for actual dependencies
import { readFileSync } from 'fs';
import express from 'express';

// ✅ Use reference types when you need global types
/// <reference types="node" />
// Now process.env, Buffer, etc. are available globally

// ✅ Use reference path for local .d.ts files
/// <reference path="./types/global.d.ts" />

// ❌ Don't use reference types for modules you import
// Instead of:
/// <reference types="express" />
import express from 'express';

// Just import the module — TypeScript will find the types
import express from 'express';
```

---

## 8. History and Modern Usage

### History

```typescript
// Triple-slash directives were the ORIGINAL way to manage types
// Before @types packages and tsconfig.json improvements

// Early TypeScript (pre-2016):
// - No @types packages
// - No tsconfig.json "include" glob
// - Triple-slash directives were the ONLY way to share types

/// <reference path="./my-types.d.ts" />
/// <reference types="some-old-lib" />

// Modern TypeScript (2016+):
// - @types packages for third-party types
// - tsconfig.json "include" for file inclusion
// - tsconfig.json "types" and "typeRoots" for @types control
// - esModuleInterop for better import syntax
```

### Modern Usage

```typescript
// ✅ Modern projects: Rarely need triple-slash directives
// Use tsconfig.json instead:

// tsconfig.json
{
  "compilerOptions": {
    "types": ["node", "jest", "react"],
    "lib": ["ES2020", "DOM"],
    "moduleResolution": "Node"
  },
  "include": ["src/**/*", "types/**/*"]
}

// ⚠️ Still useful for:
// 1. Single-file scripts without tsconfig
// 2. Libraries that need specific type inclusions
// 3. Legacy projects
// 4. Custom TypeScript environments
```

### Migration from Triple-Slash to Modern

```typescript
// BEFORE (triple-slash):
/// <reference path="./types/global.d.ts" />
/// <reference types="node" />
/// <reference lib="es2020" />

// AFTER (tsconfig.json):
{
  "compilerOptions": {
    "lib": ["ES2020"],
    "types": ["node"]
  },
  "include": ["src/**/*", "types/**/*"]
}
```

---

## 9. Best Practices

```typescript
// 1. Prefer tsconfig.json over triple-slash directives
// Use tsconfig.json for:
// - types array (replaces reference types)
// - lib array (replaces reference lib)
// - include/exclude (replaces reference path)

// 2. Only use reference path for legacy projects
/// <reference path="./types/global.d.ts" />

// 3. Use reference types when you can't modify tsconfig
/// <reference types="node" />

// 4. Never mix triple-slash with imports for the same types
// ❌
/// <reference types="node" />
import * as fs from 'fs'; // Redundant — types already included

// ✅ Just use import (TypeScript finds types automatically)
import * as fs from 'fs';

// 5. Place directives at the very top of the file
/// <reference types="node" />
/// <reference path="./types/custom.d.ts" />

// Code starts here
import { readFileSync } from 'fs';

// 6. One directive per line
// ❌
/// <reference types="node" /> /// <reference lib="es2020" />

// ✅
/// <reference types="node" />
/// <reference lib="es2020" />

// 7. Use self-closing tags
// ❌
/// <reference path="./types/global.d.ts">

// ✅
/// <reference path="./types/global.d.ts" />
```

---

## Interview Questions

**Q1**: What is the difference between `reference path` and `reference types`?
**A**: `reference path` includes a specific local `.d.ts` file. `reference types` includes an `@types` package from node_modules. Both tell the compiler to include type information.

**Q2**: When would you use `reference lib` instead of the tsconfig `lib` option?
**A**: You'd use `reference lib` only when you can't modify tsconfig.json (e.g., in a single-file script or a library that needs to include specific lib types without requiring users to configure their tsconfig).

**Q3**: What does `reference no-default-lib` do?
**A**: It prevents the compiler from including the default TypeScript library (lib.d.ts), removing all built-in types. Almost never needed in normal projects — only used by custom TypeScript runtimes.

**Q4**: How have triple-slash directives evolved with modern TypeScript?
**A**: They were originally the only way to manage type dependencies. Now, tsconfig.json options (`types`, `lib`, `include`) and `@types` packages have largely replaced them. Triple-slash directives are mainly used in legacy projects or specific edge cases.

**Q5**: When should you use `import` instead of `reference types`?
**A**: Always use `import` when you're actually importing a module at runtime. Use `reference types` only when you need global type declarations without importing anything.
