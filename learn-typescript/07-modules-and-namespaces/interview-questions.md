# Modules & Namespaces — Interview Questions

## Overview

This document contains 25+ interview questions covering ES modules, CommonJS, namespaces, module resolution, path mapping, and barrel files in TypeScript. Each question includes a detailed answer.

---

## Questions

### Q1: What is the difference between ES Modules and CommonJS?

**Answer**: ES Modules (ESM) use static `import`/`export` syntax, support asynchronous loading, enable tree-shaking, and are the JavaScript standard. CommonJS (CJS) uses `require()`/`module.exports`, loads synchronously, and was Node.js's original module system. ESM performs static analysis at parse time; CJS evaluates at runtime, allowing dynamic `require()`.

---

### Q2: Why does TypeScript have both `import` and `import type`?

**Answer**: `import type` guarantees the import is completely erased at compile time — no JavaScript runtime code is emitted. This prevents accidentally importing runtime values, avoids triggering side effects in imported modules, eliminates circular dependency issues for type-only imports, and results in smaller bundles.

```typescript
// This might accidentally import a runtime value
import { User } from './models';

// This is GUARANTEED to be erased
import type { User } from './models';
```

---

### Q3: What is `esModuleInterop` and why should you always enable it?

**Answer**: `esModuleInterop` makes TypeScript generate `__importDefault` and `__importStar` helper functions that properly wrap CommonJS modules when imported using ESM syntax. Without it, `import x from 'cjs-module'` produces incorrect runtime behavior because CJS modules don't have a `.default` property. It implies `allowSyntheticDefaultImports` and should always be `true`.

---

### Q4: Explain the `moduleResolution` options and when to use each.

**Answer**:
- **`node`**: Classic Node.js CJS resolution. Use for legacy CJS-only projects.
- **`node16`/`nodenext`**: ESM-aware resolution for Node.js 16+. Requires `.js` extensions, checks `exports` field. Use for modern Node.js projects.
- **`bundler`**: Like node16 but lenient (no extension requirement). Use for Vite/webpack projects.
- **`classic`**: TypeScript's legacy resolution. Deprecated, don't use.

---

### Q5: Why does `moduleResolution: "node16"` require `.js` extensions on imports?

**Answer**: Node.js ESM requires explicit file extensions for module resolution. TypeScript compiles `.ts` → `.js`, so the runtime file is `.js`. To ensure type-checking matches runtime behavior, TypeScript enforces `.js` extensions. This catches resolution bugs at compile time rather than runtime.

```typescript
// CORRECT for node16:
import { helper } from './utils.js';
// TypeScript resolves this to ./utils.ts at compile time
// and Node.js resolves to ./utils.js at runtime
```

---

### Q6: What is a barrel file and what are its trade-offs?

**Answer**: A barrel file (`index.ts`) re-exports from sub-modules to provide a single import point. Benefits: cleaner imports, single entry point for feature modules. Drawbacks: slower TypeScript compilation (must resolve all re-exported modules), reduced incremental compilation efficiency, potential tree-shaking issues, and circular dependency amplification.

---

### Q7: When would you use namespaces instead of modules?

**Answer**: Namespaces are useful for: (1) declaration merging to augment third-party types, (2) ambient type definitions in `.d.ts` files for untyped JavaScript libraries, (3) organizing global type declarations. They should NOT be used for application code organization — modules are superior for that due to tree-shaking, standard compliance, and bundler support.

---

### Q8: What is module augmentation?

**Answer**: Module augmentation lets you add new type declarations to existing modules without modifying their source. You use `declare module 'module-name'` to extend types. Common use case: adding custom properties to Express's `Request` interface.

```typescript
declare module 'express' {
  interface Request {
    userId?: string;
  }
}
```

---

### Q9: What is the `exports` field in `package.json` and how does TypeScript use it?

**Answer**: The `exports` field defines entry points for a package, supporting subpath exports and conditional exports (different code for ESM vs CJS vs types). TypeScript with `node16`/`nodenext` resolution checks this field first, supporting the `"types"` condition for type definitions and `"import"`/`"require"` for different module formats.

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

---

### Q10: How do path aliases work in TypeScript and what's required at runtime?

**Answer**: `paths` in `tsconfig.json` maps import patterns to file paths for type checking. TypeScript resolves `@components/Button` to `src/components/Button.ts` during compilation. However, this only affects type checking — the compiled JavaScript still has the literal import string. You must configure your bundler (Vite, webpack) or use `tsc-alias` to resolve aliases at runtime.

---

### Q11: Can you use `require()` in ESM or `import` in CommonJS?

**Answer**: You cannot use `require()` in ESM — Node.js throws `ReferenceError: require is not defined`. You cannot use static `import` in CJS. However, CJS can use dynamic `import()` (returns a Promise), and ESM can use dynamic `import()` to load any module format.

---

### Q12: What is global augmentation and why must the file be a module?

**Answer**: Global augmentation adds types to the global scope using `declare global { ... }`. The file must be a module (contain at least one `import` or `export`) because TypeScript treats non-module files as scripts with global scope already. Without `export {}`, TypeScript ignores `declare global` in script files.

```typescript
// global.d.ts
declare global {
  interface Window {
    __APP_VERSION__: string;
  }
}
export {}; // makes this a module, enabling global augmentation
```

---

### Q13: What is the difference between `rootDir` and `baseUrl`?

**Answer**: `rootDir` controls the output directory structure — it tells TypeScript where source files start so `outDir` mirrors the structure. `baseUrl` affects module resolution — it sets the base for non-relative imports. `rootDir` is about output; `baseUrl` is about input resolution.

---

### Q14: How does TypeScript handle circular module dependencies?

**Answer**: TypeScript allows circular imports but warns. At runtime with ESM, circular dependencies result in partially initialized module namespace objects — imports may be `undefined` if the exporting module hasn't completed initialization. CJS handles this differently by returning whatever has been assigned to `module.exports` at that point. Both can cause subtle runtime bugs.

---

### Q15: What are the rules for namespace merging?

**Answer**: Namespaces with the same name are automatically merged. Multiple declarations of the same interface within a namespace are also merged (declaration merging). Namespaces can merge with classes (adding static members), functions (adding overload signatures), and enums (adding members). Each combination follows specific rules.

---

### Q16: What is the `--traceResolution` flag?

**Answer**: `tsc --traceResolution` outputs detailed logs showing every step TypeScript takes when resolving module imports. It shows what file paths were tried, which succeeded or failed, and the reason. Essential for debugging "Cannot find module" errors and understanding why TypeScript resolves to unexpected files.

---

### Q17: How do you share TypeScript config in a monorepo?

**Answer**: Use TypeScript project references with `composite: true`. Create a base `tsconfig.base.json` with shared settings, then each project extends it with `extends: "../../tsconfig.base.json"` and adds project-specific config. Use `references` to declare dependencies between projects, and `tsc --build` to build in dependency order.

---

### Q18: What is the "dual package hazard"?

**Answer**: When a package publishes both CJS and ESM versions, there's a risk that both versions are loaded simultaneously in the same process (e.g., one package requires CJS while another imports ESM). This creates two separate instances of the module with independent state, leading to `instanceof` checks failing and inconsistent behavior.

---

### Q19: How do you prevent name collisions in named exports?

**Answer**: Use import aliasing (`import { Button as UIButton } from './ui'`), avoid `export * from` in public APIs, keep barrel files explicit with named re-exports, and use namespaces when organizing re-exports. Also, prefix internal exports to avoid accidental re-export collisions.

---

### Q20: What is `sideEffects` in `package.json` and how does it relate to barrel files?

**Answer**: `sideEffects: false` tells bundlers that all modules in the package are pure (no side effects when imported), enabling aggressive tree-shaking. Barrel files with `export * from` are less tree-shakable without this annotation because bundlers conservatively assume re-exports might have side effects. Always set `sideEffects: false` if your modules are pure.

---

### Q21: How does `moduleResolution: "bundler"` differ from `"node16"`?

**Answer**: Both support `exports` field resolution, but `bundler` doesn't require `.js` extensions (bundlers resolve without them), doesn't enforce ESM/CJS distinction (bundlers handle this), and is more lenient overall. `bundler` is for projects using Vite/webpack/esbuild; `node16` is for running TypeScript directly with Node.js.

---

### Q22: What is `typeRoots` and when would you use it?

**Answer**: `typeRoots` specifies directories where TypeScript looks for type definitions (default: `node_modules/@types`). Use it when you have custom type definitions in a non-standard location, or when you want to restrict which `@types` packages are included. For example, `"typeRoots": ["./types", "./node_modules/@types"]`.

---

### Q23: How do you properly type a CommonJS module in TypeScript?

**Answer**: Use `declare module` in a `.d.ts` file to describe the module's shape, or use the `module.exports` / `exports` assignment patterns in TypeScript compiled with `module: "commonjs"`. For third-party CJS modules without types, use `@types` packages or write your own ambient declarations.

```typescript
// types/legacy-lib.d.ts
declare module 'legacy-lib' {
  export function doStuff(input: string): number;
  export interface Options {
    verbose: boolean;
  }
}
```

---

### Q24: What is `resolveJsonModule` and why is it needed?

**Answer**: By default, TypeScript doesn't allow importing `.json` files. Setting `resolveJsonModule: true` enables type-safe JSON imports with inferred types. TypeScript generates types from the JSON structure, so `config.apiUrl` is typed as `string` if the value is a string.

```typescript
// tsconfig.json: resolveJsonModule = true
import config from './config.json';
// config is typed based on the JSON structure
console.log(config.apiUrl); // string
```

---

### Q25: Explain the difference between `export =` and `export default`.

**Answer**: `export =` is TypeScript's CommonJS interop syntax — it exports a single value as the entire module, designed for CJS `module.exports =` patterns. `export default` is ESM's default export syntax. With `esModuleInterop`, you can import either using `import x from 'module'`. Without it, `export =` requires `import x = require('module')`.

```typescript
// CJS-style (module.exports = something)
export = MyClass;

// ESM-style (exports.default = something)
export default MyClass;
```

---

### Q26: What happens when you use `import * as x` on a CommonJS module?

**Answer**: Without `esModuleInterop`, it gives you the raw `module.exports` object. With `esModuleInterop`, TypeScript wraps it using `__importStar` — if the module has `__esModule: true`, you get the module namespace as-is; otherwise, you get a synthetic namespace with a `.default` property pointing to the module's exports.

---

### Q27: How do you test if your library works with both CJS and ESM consumers?

**Answer**: Create test projects that consume your library in both ways:
1. A CJS project with `require()` calls
2. An ESM project with `import` statements
3. A TypeScript project with type-checking
4. Verify the `exports` field in package.json works correctly
5. Use `publint` or `arethetypeswrong` to validate your package exports
6. Test in both Node.js CJS mode (`"type": "commonjs"`) and ESM mode (`"type": "module"`)
