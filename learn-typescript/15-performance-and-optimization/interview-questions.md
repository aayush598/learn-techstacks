# Performance & Optimization Interview Questions

## 20+ Questions and Answers

---

### Q1: What is tree shaking and how does TypeScript enable it?

**Answer**: Tree shaking is a dead code elimination technique that removes unused exports from the final bundle. TypeScript enables it by:

1. Compiling to ES module syntax (statically analyzable imports/exports)
2. Supporting `import type` for type-only imports (completely erased)
3. The `isolatedModules` flag ensuring compatibility with transpilers
4. Libraries declaring `sideEffects: false` in package.json

```typescript
// math.ts
export function add(a: number, b: number) { return a + b; }
export function multiply(a: number, b: number) { return a * b; }

// main.ts
import { add } from './math'; // Only 'add' used
add(1, 2);

// With tree shaking, 'multiply' is removed from the bundle
```

---

### Q2: Explain the `strict` flag and all its sub-flags

**Answer**: `strict: true` enables all strict type-checking options:

| Flag | Purpose |
|------|---------|
| `strictNullChecks` | `null`/`undefined` are distinct types |
| `strictFunctionTypes` | Contravariant parameter checking |
| `strictBindCallApply` | Type-safe `bind`/`call`/`apply` |
| `strictPropertyInitialization` | Class properties must be initialized |
| `noImplicitAny` | No implicit `any` type |
| `noImplicitThis` | `this` must have explicit type |
| `alwaysStrict` | Emit `"use strict"` in output |
| `useUnknownInCatchVariables` | `catch` variable is `unknown` by default |

---

### Q3: What is the difference between `incremental` and `composite` projects?

**Answer**:

```json
// incremental: enables caching for faster rebuilds
{
  "compilerOptions": { "incremental": true }
}

// composite: sets up project for project references
{
  "compilerOptions": {
    "composite": true,
    // Implies: declaration: true, incremental: true
  }
}
```

`incremental` only speeds up builds. `composite` enables building projects independently and tracking dependencies between them.

---

### Q4: When would you use `emitDeclarationOnly`?

**Answer**: When using a separate bundler (webpack, rollup, esbuild) for JavaScript output and only need TypeScript for type checking and declaration generation.

```json
{
  "compilerOptions": {
    "emitDeclarationOnly": true,
    "declaration": true,
    "declarationDir": "./dist/types"
  }
}
```

---

### Q5: What is `isolatedModules` and why is it important?

**Answer**: It ensures each file can be independently transpiled, required by Babel, esbuild, and SWC. It prevents TypeScript features that require cross-file analysis:

```typescript
// ❌ Error with isolatedModules
const enum Direction { Up, Down } // Can't be inlined without full compilation
export { User } from './types';    // Can't re-export types without 'type'

// ✅ Works with isolatedModules
enum Direction { Up, Down }
export type { User } from './types';
```

---

### Q6: How do you optimize TypeScript compilation performance?

**Answer**:

```json
{
  "compilerOptions": {
    "incremental": true,
    "skipLibCheck": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo",
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Node"
  },
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

Key optimizations:
- `incremental: true` — Cache compilation info
- `skipLibCheck: true` — Skip checking `.d.ts` files
- `isolatedModules: true` — Enable parallel transpilation
- Proper `exclude` patterns

---

### Q7: What is the difference between `declarationMap` and `sourceMap`?

**Answer**:

```typescript
// sourceMap: maps compiled .js back to original .ts
// Enables debugging TypeScript in browser dev tools
"sourceMap": true

// declarationMap: maps .d.ts back to original .ts
// Enables "Go to Definition" to jump to source
"declarationMap": true
```

Both are useful: `sourceMap` for debugging, `declarationMap` for IDE navigation.

---

### Q8: Explain `sideEffects` in package.json and its impact on tree shaking

**Answer**:

```json
{
  "sideEffects": false
  // Tells bundlers: no file in this package has side effects
  // Safe to remove unused exports
}

{
  "sideEffects": ["./src/polyfills.ts", "*.css"]
  // Only these files have side effects
}
```

Without `sideEffects`, bundlers conservatively keep all imports because they might have side effects.

---

### Q9: What are the best tsconfig settings for a library?

**Answer**:

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2018",
    "module": "ESNext",
    "moduleResolution": "Node",
    "declaration": true,
    "declarationDir": "./dist/types",
    "declarationMap": true,
    "sourceMap": true,
    "composite": true,
    "incremental": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

---

### Q10: How do project references work in a monorepo?

**Answer**:

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

Build with `tsc --build` or `tsc -b`.

---

### Q11: What is the difference between `--outFile` and a bundler?

**Answer**: `outFile` bundles all output into one file but only works with AMD/System modules. Bundlers (webpack, rollup, esbuild) support ES modules, tree shaking, code splitting, and more.

```json
// outFile (limited)
{ "compilerOptions": { "module": "amd", "outFile": "./dist/bundle.js" } }

// Bundler (recommended)
// webpack.config.js / rollup.config.js
```

---

### Q12: How do you reduce the size of TypeScript type declarations?

**Answer**:

1. Use `import type` for type-only imports
2. Avoid re-exporting entire modules (`export *`)
3. Use `emitDeclarationOnly` with a minifier
4. Use `dts-bundle-generator` to bundle declarations
5. Remove unused type declarations
6. Use `skipLibCheck: true` in consumer projects

---

### Q13: What is `noUncheckedIndexedAccess` and when should you use it?

**Answer**:

```typescript
// Without noUncheckedIndexedAccess
const arr = [1, 2, 3];
const num = arr[5]; // type: number (but undefined at runtime!)

// With noUncheckedIndexedAccess
const num = arr[5]; // type: number | undefined (correct!)

// You must handle the undefined case:
if (num !== undefined) {
  console.log(num.toFixed()); // Safe
}
```

Use it for safer array/object access. It's not included in `strict` because it adds verbosity.

---

### Q14: Explain the impact of `strictNullChecks` on performance

**Answer**: `strictNullChecks` doesn't affect runtime performance (types are erased). However, it:

1. Increases compile time slightly (more type checking)
2. Requires more null checks in code (slightly more code)
3. Catches bugs that would cause runtime errors
4. Results in more reliable, production-ready code

The compile-time cost is negligible compared to the bug prevention benefits.

---

### Q15: What is `exactOptionalPropertyTypes` and when should you use it?

**Answer**:

```typescript
// Without exactOptionalPropertyTypes
interface Config {
  debug?: boolean;
}

const config: Config = { debug: undefined }; // Allowed (but may be a bug)
const config2: Config = {}; // Allowed

// With exactOptionalPropertyTypes
const config: Config = { debug: undefined }; // Error!
// 'debug' is optional — don't pass undefined, just omit it
const config2: Config = {}; // OK
```

Use it when you want to distinguish between "not provided" and "explicitly undefined".

---

### Q16: How do you handle large TypeScript projects efficiently?

**Answer**:

```json
// 1. Use project references
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/api" },
    { "path": "./packages/web" }
  ]
}

// 2. Enable incremental builds
{ "compilerOptions": { "incremental": true } }

// 3. Use --build mode
// tsc --build

// 4. Parallel compilation
// Each project compiles independently

// 5. Skip library checking
{ "compilerOptions": { "skipLibCheck": true } }
```

---

### Q17: What is the difference between `module: ESNext` and `module: NodeNext`?

**Answer**:

```json
// ESNext: Modern ES modules (import/export)
{ "module": "ESNext" }
// Output: import { add } from './math.js';

// NodeNext: Node.js native modules (with .js extensions)
{ "module": "NodeNext" }
// Output: import { add } from './math.js';
// Requires .js extensions in imports
```

`NodeNext` is better for Node.js projects (follows Node.js module resolution). `ESNext` is better for browser/bundler projects.

---

### Q18: How do source maps affect build performance?

**Answer**:

```json
// No source maps — fastest
{ "compilerOptions": { "sourceMap": false } }

// External source maps — moderate
{ "compilerOptions": { "sourceMap": true } }

// Inline source maps — slowest (larger output)
{ "compilerOptions": { "inlineSourceMap": true } }
```

Source maps add build time and disk space. Disable them for production builds if not needed.

---

### Q19: What is `forceConsistentCasingInFileNames` and why does it matter?

**Answer**:

```typescript
// Without this flag:
import { User } from './User';  // Works on macOS (case-insensitive)
import { user } from './user';  // Works on Linux (case-sensitive)

// With this flag:
import { User } from './User';  // Error on Linux if file is 'user.ts'
// Forces consistent casing across platforms
```

Essential for cross-platform development (macOS/Windows are case-insensitive, Linux is case-sensitive).

---

### Q20: How do you optimize a TypeScript project for CI/CD?

**Answer**:

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo",
    "skipLibCheck": true,
    "noEmit": false,
    "declaration": true,
    "declarationMap": false,
    "sourceMap": false
  }
}
```

CI/CD optimizations:
- Cache `.tsbuildinfo` file between builds
- Use `skipLibCheck: true`
- Disable source maps in CI
- Use project references for parallel builds
- Consider using `esbuild` or `SWC` for faster transpilation

---

### Q21: What is the impact of `target` on bundle size?

**Answer**:

```json
// ES5 — largest output (includes polyfills)
{ "target": "ES5" }

// ES2015 — modern output
{ "target": "ES2015" }

// ES2020 — smallest output (native async/await, optional chaining)
{ "target": "ES2020" }

// ESNext — smallest (latest features)
{ "target": "ESNext" }
```

Higher target = smaller output (less transpilation), but requires modern runtimes.

---

### Q22: Explain `noUnusedLocals` and `noUnusedParameters`

**Answer**:

```typescript
// Without these flags:
function add(a: number, b: number): number {
  const unused = 'hello'; // No error
  return a + b;
}

// With noUnusedLocals and noUnusedParameters:
function add(a: number, b: number): number {
  const unused = 'hello'; // Error: 'unused' is declared but never used
  return a + b;
}

// Fix: Remove unused variables or prefix with _
function add(a: number, _b: number): number {
  return a;
}
```

These flags help maintain clean, dead-code-free codebases.

---

### Q23: How do you handle third-party libraries without types?

**Answer**:

```typescript
// Option 1: Check for @types package
npm install --save-dev @types/library-name

// Option 2: Create your own declarations
// types/library-name.d.ts
declare module 'library-name' {
  export function doSomething(value: string): number;
}

// Option 3: Use minimal typing
declare module 'library-name' {
  const value: any;
  export default value;
}

// Option 4: Use @ts-ignore (last resort)
// @ts-ignore
import library from 'library-name';
```

---

### Q24: What is `resolveJsonModule` and when should you use it?

**Answer**:

```typescript
// With resolveJsonModule: true
import config from './config.json';
console.log(config.database.host); // Type-safe JSON access

// tsconfig.json
{ "compilerOptions": { "resolveJsonModule": true } }
```

Use it when you need type-safe access to JSON files. TypeScript infers types from the JSON structure.

---

### Q25: How do you optimize TypeScript for large codebases?

**Answer**:

1. **Project references**: Split into independent projects
2. **Incremental builds**: Cache compilation info
3. **skipLibCheck**: Skip checking declaration files
4. **isolatedModules**: Enable parallel transpilation
5. **ESBuild/SWC**: Use faster transpilers for development
6. **TypeScript ESLint**: Only type-check changed files
7. **Proper exclude patterns**: Don't compile test/vendor files
8. **Composite projects**: Track dependencies between projects
