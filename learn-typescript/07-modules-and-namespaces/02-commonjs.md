# CommonJS in TypeScript

## Table of Contents

- [Overview](#overview)
- [CommonJS Syntax](#commonjs-syntax)
- [TypeScript CommonJS Output](#typescript-commonjs-output)
- [Interop Between ESM and CommonJS](#interop-between-esm-and-commonjs)
- [esModuleInterop Flag](#esmoduleinterop-flag)
- [allowSyntheticDefaultImports Flag](#allowsyntheticdefaultimports-flag)
- [When to Use CommonJS vs ESM](#when-to-use-commonjs-vs-esm)
- [CJS in Node.js](#cjs-in-nodejs)
- [Practical Examples](#practical-examples)
- [Migration Strategies](#migration-strategies)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

CommonJS (CJS) is the original module system for Node.js, using `require()` for imports and `module.exports` for exports. While ESM is the modern standard, CommonJS remains widely used in the Node.js ecosystem. TypeScript can compile to both CJS and ESM, and understanding the interop between them is critical.

### Key Differences: CJS vs ESM

| Feature | CommonJS | ESM |
|---|---|---|
| Syntax | `require()` / `module.exports` | `import` / `export` |
| Loading | Synchronous | Asynchronous |
| Resolution | Runtime dynamic | Static (compile-time) |
| Top-level `this` | `module.exports` | `undefined` |
| Node.js file extension | `.cjs` | `.mjs` |
| `package.json` field | `main` | `type: "module"` + `exports` |

---

## CommonJS Syntax

### Exports

```typescript
// math.ts (compiled with module: "commonjs")

// Method 1: Assign to module.exports (the entire export)
function add(a: number, b: number): number {
  return a + b;
}

function multiply(a: number, b: number): number {
  return a * b;
}

module.exports = { add, multiply };

// Method 2: Assign to exports object (named-style)
exports.add = add;
exports.multiply = multiply;

// Method 3: One-shot export
module.exports = function subtract(a: number, b: number): number {
  return a - b;
};
```

### Imports

```typescript
// CommonJS require — dynamic, runtime resolution
const math = require('./math');

console.log(math.add(2, 3));       // 5
console.log(math.multiply(2, 3));  // 6

// Destructuring from require
const { add, multiply } = require('./math');
```

### Module.exports vs Exports

```typescript
// exports is a reference to module.exports
// Reassigning module.exports breaks this reference!
exports.foo = 'bar';       // OK: adds foo to module.exports
exports = { foo: 'bar' };  // WRONG: breaks the reference, exports nothing

module.exports = { foo: 'bar' }; // OK: replaces entire exports
```

---

## TypeScript CommonJS Output

### Configuration

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "module": "commonjs",  // Compile to CJS
    "target": "es2020",
    "outDir": "./dist",
    "declaration": true
  }
}
```

### What TypeScript Generates

```typescript
// Source: src/utils.ts
export function greet(name: string): string {
  return `Hello, ${name}!`;
}

export interface Config {
  apiUrl: string;
  timeout: number;
}
```

```javascript
// Compiled: dist/utils.js (CommonJS output)
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.greet = greet;

function greet(name) {
  return `Hello, ${name}!`;
}
```

### Default Export Handling in CJS

```typescript
// Source
export default class Logger {
  log(msg: string) { console.log(msg); }
}
```

```javascript
// Compiled CJS output
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = Logger;

class Logger {
  log(msg) { console.log(msg); }
}
```

Note: TypeScript wraps default exports in `exports.default` and sets `__esModule: true`. This is why naive `require()` of a TypeScript-compiled default export gives you an object with `.default` instead of the class itself.

### Requiring a Module with Default Export

```typescript
// Compiled CJS module with default export
const loggerModule = require('./logger');
console.log(loggerModule.default); // the Logger class

// You can't destructure default imports from CJS directly:
// const Logger = require('./logger');  // gives you { default: Logger, __esModule: true }
// You need .default:
const Logger = require('./logger').default;
```

---

## Interop Between ESM and CommonJS

### ESM Importing a CommonJS Module

```typescript
// ESM file: app.mts
// CJS module: legacy-lib.cjs (or compiled from TypeScript with module: "commonjs")

// Default import — works with esModuleInterop
import LegacyLib from './legacy-lib.cjs';

// Named imports from CJS — works in most cases
import { helper } from './legacy-lib.cjs';
```

### CommonJS Importing an ESM Module

```typescript
// CJS file: legacy.cjs

// You CANNOT use require() to import ESM
// const something = require('./esm-module.mjs'); // ERROR in Node.js

// You must use dynamic import
async function loadESM() {
  const { default: ESMModule } = await import('./esm-module.mjs');
  const { helper } = await import('./esm-module.mjs');
  return { ESMModule, helper };
}
```

### The __esModule Marker

```typescript
// TypeScript and Babel add this to compiled ESM output:
Object.defineProperty(exports, "__esModule", { value: true });

// This marker helps interop layers detect whether a module
// was originally written as ESM or CJS.
// Tools like ts-node, babel, and webpack check for this flag.
```

---

## esModuleInterop Flag

This is one of the most important TypeScript compiler flags for module interop.

### Without esModuleInterop

```typescript
// tsconfig.json: esModuleInterop = false (default in older TS)

// CJS module compiled by TypeScript:
// module.exports = "hello"
// module.exports.default = "hello"  (for default exports)

// You MUST do this:
import * as myModule from './my-module';
console.log(myModule.default);  // awkward

// OR:
const myModule = require('./my-module');
```

### With esModuleInterop

```typescript
// tsconfig.json: esModuleInterop = true

// TypeScript generates a helper function that wraps modules:
// - CJS modules get a synthetic default export
// - Namespace imports are wrapped correctly

// Now you can do:
import myModule from './my-module';
console.log(myModule);  // works naturally

// Named imports also work:
import { helper } from './my-module';
```

### Generated Helper Code

```javascript
// When esModuleInterop = true, TypeScript emits:
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};

// Usage in compiled output:
const myModule = __importDefault(require("./my-module"));
```

### esModuleInterop Impact Summary

| Scenario | Without | With |
|---|---|---|
| `import x from 'cjs-module'` | Error or wrong behavior | Correct |
| `import * as x from 'cjs-module'` | Gets raw exports | Gets wrapped namespace |
| `import { named } from 'esm-module'` | Works | Works |
| `require('esm-module')` | Gets raw module | Raw module (require is always raw) |

---

## allowSyntheticDefaultImports Flag

This flag only affects type-checking — it does NOT emit any helper code.

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "allowSyntheticDefaultImports": true
  }
}

// This lets you write:
import React from 'react';  // React doesn't have a default export,
                             // but this is allowed type-wise
```

### esModuleInterop vs allowSyntheticDefaultImports

| Flag | Type Checking | Runtime Code |
|---|---|---|
| `allowSyntheticDefaultImports` | Allows `import x from 'cjs'` | No change |
| `esModuleInterop` | Same as above | Adds `__importDefault` helper |

> **Best Practice**: Always set `esModuleInterop: true`. It automatically implies `allowSyntheticDefaultImports: true`.

---

## When to Use CommonJS vs ESM

### Use CommonJS When

- Building a **library that must support older Node.js** versions (< 14)
- Working in a **legacy codebase** that uses `require()` throughout
- The package needs to be consumed by both Node.js and bundlers without dual packaging
- You're writing a **CLI tool** that needs synchronous module loading
- You're in an environment where ESM is not yet supported

### Use ESM When

- Building a **new Node.js project** (Node.js 14+)
- You want **tree-shaking** support
- You're building a **browser-compatible** library
- You want **static analysis** and better tooling support
- You're writing **modern TypeScript** and want to follow standards

### Decision Matrix

```
New project? ─── Yes ───> Use ESM
     │
     No
     │
     └── Legacy Node.js support needed? ── Yes ──> Use CJS
                                                   │
                                              No ──┘
                                                   │
                                              Use ESM
```

---

## CJS in Node.js

### File Extensions

```
.mjs  → Always treated as ESM by Node.js
.cjs  → Always treated as CJS by Node.js
.js   → Determined by "type" field in package.json
```

### package.json for CJS

```json
{
  "name": "my-cjs-package",
  "type": "commonjs",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts"
}
```

Or simply omit `"type"` — `"commonjs"` is the default.

### Dynamic Requires in Node.js

```typescript
// CJS allows dynamic requires — ESM does not
function loadPlugin(pluginName: string): any {
  try {
    return require(`./plugins/${pluginName}`);
  } catch (err) {
    console.error(`Plugin "${pluginName}" not found`);
    return null;
  }
}

// In ESM, you'd use dynamic import instead:
async function loadPluginESM(pluginName: string): Promise<any> {
  return import(`./plugins/${pluginName}.mjs`);
}
```

### Module Caching in CJS

```typescript
// require() caches modules — the same module returns the same object
const a = require('./singleton');
const b = require('./singleton');
console.log(a === b); // true

// To clear the cache (e.g., for testing):
delete require.cache[require.resolve('./singleton')];
```

### __dirname and __filename in CJS

```typescript
// These are available in CommonJS modules
const __filename = __filename; // file path
const __dirname = __dirname;   // directory path

// In ESM, you must use:
import { fileURLToPath } from 'url';
import path from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

---

## Practical Examples

### Publishing a CJS Library

```typescript
// src/index.ts
export { default as Logger } from './logger';
export { formatDate, parseDate } from './date-utils';
export type { LoggerOptions, DateFormat } from './types';
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "es2020",
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src"]
}
```

### Using a CJS Library with ESM Consumer

```typescript
// Consumer (ESM): consuming a CJS library
import legacyLib from 'legacy-cjs-lib';        // default import
import { helper } from 'legacy-cjs-lib';        // named import

// The esModuleInterop flag makes this seamless.
// Without it, you might need:
// const { default: legacyLib } = await import('legacy-cjs-lib');
```

### Conditional Module Loading

```typescript
// CJS: load different implementations based on environment
function getDatabaseDriver() {
  if (process.env.DB_DRIVER === 'postgres') {
    return require('./drivers/postgres');
  } else if (process.env.DB_DRIVER === 'mysql') {
    return require('./drivers/mysql');
  } else {
    return require('./drivers/sqlite');
  }
}

// ESM equivalent:
async function getDatabaseDriverESM() {
  switch (process.env.DB_DRIVER) {
    case 'postgres':
      return import('./drivers/postgres.mjs');
    case 'mysql':
      return import('./drivers/mysql.mjs');
    default:
      return import('./drivers/sqlite.mjs');
  }
}
```

---

## Migration Strategies

### CJS to ESM Migration Steps

1. **Add `"type": "module"` to package.json**
2. **Replace `require()` with `import`**
3. **Replace `module.exports` / `exports` with `export`**
4. **Add `.js` extensions to all relative imports**
5. **Replace `__dirname` / `__filename`** with `import.meta` equivalents
6. **Update `tsconfig.json`** to `"module": "node16"` or `"nodenext"`
7. **Run tests and fix any circular dependency issues**

### Gradual Migration

```typescript
// Use .mjs for ESM files, .cjs for CJS files during migration
// Node.js determines module type by extension regardless of package.json "type"

// ESM file
import { helper } from './helper.mjs';  // import ESM

// CJS file
const { legacy } = require('./legacy.cjs');  // require CJS
```

---

## Best Practices

1. **Always enable `esModuleInterop: true`** — it makes interop seamless and is considered best practice.

2. **Use `module: "commonjs"` only when necessary** — prefer ESM for new projects.

3. **Use `.cjs` extension** to explicitly mark files as CommonJS in ESM packages.

4. **Never mix `module.exports` and ES `export` in the same file** — it leads to confusion.

5. **Test your library's types/exports** in both CJS and ESM consumers if publishing.

6. **Avoid dynamic `require()` in ESM code** — use dynamic `import()` instead.

7. **Use the `exports` field in package.json** instead of just `main` for proper dual-package support.

8. **Check `__esModule` flag** when building interop utilities to detect the source module format.

9. **Document your package's module format** clearly in README and package.json.

10. **Consider using `tsup` or `unbuild`** for dual CJS/ESM package builds.

---

## Interview Questions

### Q1: What is the difference between `require()` and `import`?

**Answer**: `require()` is CommonJS's synchronous module loading mechanism — it runs at runtime and can be called conditionally. `import` is ESM's static declaration — it's parsed at compile time, enabling tree-shaking and static analysis. ESM `import` statements are hoisted and cannot be used conditionally (though dynamic `import()` can).

### Q2: What does `esModuleInterop` actually do?

**Answer**: It enables TypeScript to generate `__importDefault` and `__importStar` helper functions that properly wrap CommonJS modules when they're imported using ESM syntax. Without it, `import x from 'cjs-module'` fails or produces incorrect results because CJS modules don't have a `.default` property naturally.

### Q3: Why can't you `require()` an ESM module?

**Answer**: ESM modules are loaded asynchronously and their exports are live bindings, while `require()` is synchronous. Node.js disallows `require()` of ESM to prevent race conditions and maintain the ESM specification's integrity. You must use dynamic `import()` which returns a Promise.

### Q4: What is the `__esModule` flag?

**Answer**: It's a boolean property set on `module.exports` by TypeScript (and Babel) when compiling ESM source to CJS output. It signals to interop layers that the module was originally written as ESM, allowing tools to handle default exports and namespace imports correctly.

### Q5: When would you use `.cjs` vs `.mjs` file extensions?

**Answer**: `.mjs` forces Node.js to treat a file as ESM regardless of `package.json`'s `type` field. `.cjs` forces CJS treatment. Use them to explicitly control module format in a mixed codebase, during CJS-to-ESM migration, or when you need specific module format for certain files in an ESM package.

### Q6: What is the difference between `esModuleInterop` and `allowSyntheticDefaultImports`?

**Answer**: `allowSyntheticDefaultImports` only affects type-checking — it allows `import x from 'cjs'` to pass type-checking without emitting any code. `esModuleInterop` does the same thing for type-checking AND emits runtime helper code (`__importDefault`) that makes it work at runtime. Always prefer `esModuleInterop: true`.

### Q7: Can you use `__dirname` and `__filename` in ESM?

**Answer**: No, these globals only exist in CommonJS. In ESM, you derive them using:
```typescript
import { fileURLToPath } from 'url';
import path from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

### Q8: What are the challenges of dual CJS/ESM package publishing?

**Answer**: You need separate build outputs, separate `package.json` exports conditions, handle the fact that CJS can't import ESM synchronously, ensure TypeScript types resolve correctly in both environments, and avoid the "dual package hazard" where the same module is loaded twice with different state.
