# Type-Checking Performance

## Table of Contents

1. [How the Type Checker Works](#how-the-type-checker-works)
2. [What Makes Type Checking Slow](#what-makes-type-checking-slow)
3. [Tracing and Profiling](#tracing-and-profiling)
4. [Performance Anti-Patterns](#performance-anti-patterns)
5. [Optimization Strategies](#optimization-strategies)
6. [Build Tool Comparison](#build-tool-comparison)
7. [TypeScript in Frameworks](#typescript-in-frameworks)
8. [Real-World Benchmarks](#real-world-benchmarks)
9. [Interview Questions](#interview-questions)

---

## How the Type Checker Works

TypeScript's compiler (`tsc`) has two main phases: **transformation** (stripping types, emitting JS) and **type checking**. The type checker is a separate pass that validates your code against the type system without producing output.

### Internal Architecture

The type checker operates on the **Abstract Syntax Tree (AST)** produced by the parser. It walks the AST nodes and resolves types by consulting the **Type Stores** — internal maps that track declared types, symbols, and their relationships.

```typescript
// Under the hood, TypeScript maintains several key data structures:

// 1. Symbol Table - Maps identifiers to their declarations
// Each file gets a SourceFile symbol, which contains child symbols
// for every declaration in that file.

// 2. Type Stores - Maps type nodes to resolved Type objects
// A Type object carries all metadata: properties, type arguments,
// base types, etc.

// 3. Inference Sites - Tracks locations where type inference happens
// Generic parameter inference creates inference sites that the
// checker resolves through constraint satisfaction.

// Simplified view of the checking pipeline:
// Parse source -> Bind (create symbols) -> Check (resolve types) -> Emit

// The checker resolves types lazily in many cases — it only fully
// resolves a type when it needs to compare it against another type
// or when diagnostics are requested.
```

### Type Instantiation

When TypeScript encounters a generic type with type arguments, it creates a **type instantiation** — a new Type object parameterized with the given arguments.

```typescript
// A simple generic creates an instantiation site
type Box<T> = { value: T; tag: string };

// Each usage creates a new instantiation:
type StringBox = Box<string>;  // Instantiation 1
type NumberBox = Box<number>;  // Instantiation 2

// With nested generics, instantiation count multiplies
type DeepBox<T> = {
  outer: Box<T>;
  inner: Box<Box<T>>;
};

// DeepBox<string> triggers:
//   1. DeepBox instantiation
//   2. Box<string> instantiation (for outer)
//   3. Box<Box<string>> instantiation (for inner outer)
//   4. Box<string> instantiation (for inner inner)
// = 4 total instantiations for ONE usage

// The instantiation counter has a limit (default: 50)
// TypeScript will error if exceeded:
type Infinite<T> = Infinite<T & { depth: 1 }>;
// error: Type instantiation is excessively deep and possibly infinite.
```

### Checker Performance Characteristics

```typescript
// The type checker's performance is NOT linear with code size.
// It depends on:

// 1. Number of type-checkable expressions
// 2. Depth and complexity of type instantiations
// 3. Width of union types being checked
// 4. Number of conditional type evaluations
// 5. Structural compatibility checks (comparing object types)

// A small file with complex generics can be SLOWER to check
// than a large file with simple types:

// Fast (1000 lines of simple code):
const users = Array.from({ length: 100 }, (_, i) => ({
  id: i,
  name: `User ${i}`,
  email: `user${i}@example.com`
}));

// Slow (50 lines of complex generics):
type Slow<T extends [unknown, ...unknown[]]> =
  T extends [infer First, ...infer Rest extends [unknown, ...unknown[]]]
    ? [First, ...Slow<Rest>]
    : [];

type Result = Slow<[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]>;
```

---

## What Makes Type Checking Slow

### 1. Type Instantiation Depth

Recursive or deeply nested generic types cause the checker to create exponentially many type instances.

```typescript
// ANTI-PATTERN: Unbounded recursive type
type NestedObject<T> = {
  [K in keyof T]: T[K] extends object
    ? NestedObject<T[K]>
    : T[K];
};

// For a deeply nested object, this creates instantiations
// proportional to the depth:
type Deep = {
  a: {
    b: {
      c: {
        d: {
          e: {
            f: string;
          };
        };
      };
    };
  };
};

// NestedObject<Deep> requires 6 levels of recursion = 6 instantiations
// Each level also evaluates the conditional type

// ANTI-PATTERN: Recursive type with no base case narrowing
type UnboundedUnion<T> = T extends [infer Head, ...infer Tail]
  ? Head | UnboundedUnion<Tail>
  : never;

// For a union of N elements, this creates N instantiations
type BadUnion = UnboundedUnion<[1, 2, 3, 4, 5]>;
// Instantiations: 5 + 4 + 3 + 2 + 1 = 15
```

### 2. Union Distribution

Large unions force the type checker to evaluate conditional types against each member individually.

```typescript
// Conditional types over unions "distribute" by default
type ToArray<T> = T extends any ? T[] : never;

// For a union of 100 types, this evaluates the conditional
// 100 times, creating 100 result types that are then unified
type BigUnion = 1 | 2 | 3 | 4 | 5 /* ... up to 100 */;

// ToArray<BigUnion> creates 100 instantiations
// The result is a union of 100 array types:
// (1 | 2 | 3 | ... | 100)[]

// The REAL cost comes when the conditional is complex:
type HeavyDistribution<T> = T extends {
  type: infer U;
  payload: infer P;
}
  ? {
      type: U;
      payload: P;
      timestamp: number;
      metadata: Record<string, unknown>;
    }
  : never;

// Applied to a large union of event types:
type Events =
  | { type: 'click'; payload: MouseEvent }
  | { type: 'key'; payload: KeyboardEvent }
  | { type: 'scroll'; payload: WheelEvent }
  | { type: 'focus'; payload: FocusEvent }
  | /* ... 50 more */ { type: 'custom'; payload: unknown };

// HeavyDistribution<Events> evaluates 50+ times
type Distributed = HeavyDistribution<Events>;
```

### 3. Conditional Type Evaluation

```typescript
// ANTI-PATTERN: Complex conditional chain
type InferRoute<T extends string> =
  T extends `${infer _Start}/users/${infer Id}/${infer Rest}`
    ? { userId: Id; rest: InferRoute<Rest> }
    : T extends `${infer _Start}/posts/${infer Id}/${infer Rest}`
    ? { postId: Id; rest: InferRoute<Rest> }
    : T extends `${infer _Start}/comments/${infer Id}`
    ? { commentId: Id }
    : {};

// Each pattern match involves template literal inference,
// which is inherently expensive. The checker must:
// 1. Parse the string literal type
// 2. Try to match against each pattern
// 3. Bind the inferred type variables
// 4. Recurse on the remaining string

// For a path like "/users/123/posts/456/comments/789",
// this triggers 6+ conditional evaluations with template
// literal inference at each step
```

### 4. Large Object Types and Structural Comparisons

```typescript
// ANTI-PATTERN: Comparing massive object types
interface MassiveType {
  field1: string;
  field2: number;
  field3: boolean;
  field4: string[];
  field5: Record<string, unknown>;
  field6: () => void;
  field7: Promise<void>;
  field8: [string, number, boolean];
  field9: Map<string, Set<number>>;
  field10: WeakMap<object, WeakRef<object>>;
  // ... 200+ more fields
}

// Every structural comparison between two types that extend
// or intersect with MassiveType requires the checker to
// compare ALL fields pairwise:

type IsSubtype<A, B> = A extends B ? true : false;

// This check requires comparing every field in MassiveType
// against the target type — O(n) where n = number of fields
type Check = IsSubtype<MassiveType, Partial<MassiveType>>; // fast: true
type Check2 = IsSubtype<MassiveType, { field1: string }>;  // fast: false
// But intermediate computations involving MassiveType are slow
```

---

## Tracing and Profiling

### The `--generateTrace` Flag

TypeScript 4.1+ supports generating V8-compatible trace files for deep performance analysis.

```bash
# Generate a trace of the type-checking process
npx tsc --generateTrace ./trace-output --declaration false

# This creates:
# trace-output/
#   types.json          - All type information
#   trace.json          - Event trace for Chrome DevTools
```

### Reading Trace Files with Chrome DevTools

```bash
# 1. Open Chrome DevTools (chrome://devtools)
# 2. Go to the Performance tab
# 3. Click the "Load" button (upload icon) in the top-left
# 4. Select the trace.json file
# 5. The trace shows:
#    - Check expressions: time spent type-checking each expression
#    - Check type: time resolving each type reference
#    - Instantiate type: time creating type instantiations
#    - Resolve type: time resolving type aliases

# The flame chart shows:
# - Top-level events: "CheckSourceFile" per file
# - Sub-events: "CheckExpression", "CheckType", etc.
# - Duration: each bar's width = time spent

# Useful for identifying:
# - Which files take longest to check
# - Which specific expressions are expensive
# - Where type instantiations accumulate
```

### Programmatic Profiling

```typescript
// You can also use the TypeScript API to profile:
import * as ts from 'typescript';

const configPath = ts.findConfigFile(
  './',
  ts.sys.fileExists,
  'tsconfig.json'
);

const configFile = ts.readConfigFile(configPath, ts.sys.readFile);
const parsed = ts.parseJsonConfigFileContent(
  configFile.config,
  ts.sys,
  './'
);

const program = ts.createProgram(parsed.fileNames, parsed.options);

// Before type checking
const start = performance.now();

// Force full type checking (not just emit)
const diagnostics = ts.getPreEmitDiagnostics(program);

const elapsed = performance.now() - start;

console.log(`Type checking took ${elapsed.toFixed(2)}ms`);
console.log(`Found ${diagnostics.length} diagnostics`);

// Break down by file
const fileTimes = new Map<string, number>();

// Custom checker wrapper for profiling
const checker = program.getTypeChecker();
const signature = checker.getSignatureAtLocation;

// Use --generateTrace for detailed breakdowns
```

---

## Performance Anti-Patterns

### 1. Deeply Nested Conditional Types

```typescript
// BAD: Deep conditional nesting — exponential evaluation
type TransformDeep<T> =
  T extends { a: { b: { c: { d: { e: unknown } } } } }
    ? { result: 'deep'; value: T['a']['b']['c']['d']['e'] }
    : T extends { a: { b: { c: { d: unknown } } } }
    ? { result: 'medium'; value: T['a']['b']['c']['d'] }
    : T extends { a: { b: { c: unknown } } }
    ? { result: 'shallow'; value: T['a']['b']['c'] }
    : T extends { a: { b: unknown } }
    ? { result: 'shallower'; value: T['a']['b'] }
    : T extends { a: unknown }
    ? { result: 'shallowest'; value: T['a'] }
    : { result: 'none'; value: never };

// BETTER: Use indexed access with fallback
type GetNested<T, Path extends string[]> =
  Path extends [infer First extends keyof T, ...infer Rest extends string[]]
    ? Rest extends []
      ? T[First]
      : GetNested<T[First], Rest>
    : T;

type Result1 = GetNested<{ a: { b: { c: string } } }, ['a', 'b', 'c']>;
// Result1 = string
```

### 2. Large Unions

```typescript
// BAD: Massive union that bloats type checking
type Color =
  | '#FF0000' | '#FF4400' | '#FF8800' | '#FFCC00'
  | '#FFFF00' | '#CCFF00' | '#88FF00' | '#44FF00'
  | '#00FF00' | '#00FF44' | '#00FF88' | '#00FFCC'
  | '#00FFFF' | '#00CCFF' | '#0088FF' | '#0044FF'
  | '#0000FF' | '#4400FF' | '#8800FF' | '#CC00FF'
  | '#FF00FF' | '#FF00CC' | '#FF0088' | '#FF0044'
  // ... 1000+ color values
  ;

// BETTER: Use template literal types or branded types
type HexColor = `#${string}`;

// Or use a finite set with a runtime validator
type PrimaryColor = 'red' | 'green' | 'blue';
type ColorShade = 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;
type TailwindColor = `${PrimaryColor}-${ColorShade}`;
// 3 * 9 = 27 members — much more manageable

// Or use a function with runtime validation
function isValidColor(color: string): color is HexColor {
  return /^#[0-9A-Fa-f]{6}$/.test(color);
}
```

### 3. Recursive Types Without Tail Recursion

```typescript
// BAD: Recursive type that blows up
type Sum<T extends number[], Result extends number = 0> =
  T extends [infer Head extends number, ...infer Tail extends number[]]
    ? Sum<Tail, [...TupleOf<Result>, ...TupleOf<Head>]['length']>
    : Result;

// This is not tail-recursive because it uses
// [...TupleOf<Result>, ...TupleOf<Head>] as an intermediate step

// BETTER: Use tail-recursive conditional types (TypeScript 4.5+)
type SumTR<T extends number[], Result extends number = 0> =
  T extends [infer Head extends number, ...infer Tail extends number[]]
    ? SumTR<Tail, [...TupleOf<Result>, ...TupleOf<Head>]['length']>
    : Result;

// TypeScript 4.5+ optimizes tail-recursive conditional types
// by reusing the same instantiation stack frame.
// The key: the recursive call must be in the "true" branch
// with the accumulator as the only state carried forward.

// Helper type for building tuples
type BuildTuple<N extends number, T extends unknown[] = []> =
  T['length'] extends N ? T : BuildTuple<N, [...T, unknown]>;

type TupleOf<N extends number> = BuildTuple<N>;

// Type-level arithmetic with tail recursion
type Add<A extends number, B extends number> =
  [...TupleOf<A>, ...TupleOf<B>]['length'] as number;

type Multiply<A extends number, B extends number, Acc extends unknown[] = []> =
  Acc['length'] extends B
    ? Acc['length']
    : Multiply<A, B, [...Acc, ...TupleOf<A>]>;

// Works up to ~1000 in TypeScript 4.5+ with tail call optimization
type BigSum = SumTR<[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]>; // 55
```

### 4. Barrel File Re-Exports

```typescript
// BAD: Barrel file that re-exports everything
// src/types/index.ts
export * from './user';
export * from './post';
export * from './comment';
export * from './category';
export * from './tag';
export * from './permission';
export * from './role';
export * from './organization';
export * from './settings';
export * from './audit';
// 50+ more re-exports

// The problem: importing from the barrel file forces TypeScript
// to resolve ALL re-exported modules, even if you only use one:

// src/app.ts
import { User } from './types'; // Forces resolution of ALL 50+ modules!

// BETTER: Direct imports
import { User } from './types/user';

// Or use path aliases with careful barrel management:
// tsconfig.json
// {
//   "compilerOptions": {
//     "paths": {
//       "@types/user": ["./src/types/user"],
//       "@types/post": ["./src/types/post"]
//     }
//   }
// }
```

### 5. Using `type` Where `interface` Suffices

```typescript
// `type` aliases create new types that must be resolved each time.
// `interface` declarations are "open" and cached differently by the checker.

// Slightly slower: type alias creates a new type on each reference
type User = {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  preferences: {
    theme: 'light' | 'dark';
    language: string;
    notifications: boolean;
  };
};

// Slightly faster: interfaces are cached and support declaration merging
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  preferences: {
    theme: 'light' | 'dark';
    language: string;
    notifications: boolean;
  };
}

// The performance difference is negligible for small types,
// but for types referenced thousands of times in a large codebase,
// interfaces can measurably reduce check time.
//
// Key distinction:
// - interface: creates a named type symbol, cached by name
// - type: creates a type alias, resolved on each use
```

---

## Optimization Strategies

### 1. Breaking Up Large Types

```typescript
// BAD: Monolithic type
interface FullUser {
  id: string;
  name: string;
  email: string;
  password: string;
  avatar: string;
  bio: string;
  settings: {
    theme: 'light' | 'dark';
    language: string;
    timezone: string;
    notifications: {
      email: boolean;
      push: boolean;
      sms: boolean;
      frequency: 'realtime' | 'daily' | 'weekly';
    };
    privacy: {
      profileVisibility: 'public' | 'private' | 'friends';
      showEmail: boolean;
      showPhone: boolean;
    };
  };
  permissions: string[];
  metadata: Record<string, unknown>;
}

// BETTER: Composable type pieces
interface UserBase {
  id: string;
  name: string;
  email: string;
}

interface UserPreferences {
  theme: 'light' | 'dark';
  language: string;
  timezone: string;
}

interface UserNotifications {
  email: boolean;
  push: boolean;
  sms: boolean;
  frequency: 'realtime' | 'daily' | 'weekly';
}

// Compose from smaller pieces
type FullUser = UserBase & {
  settings: {
    preferences: UserPreferences;
    notifications: UserNotifications;
  };
};
```

### 2. Limiting Union Size with Discriminated Unions

```typescript
// BAD: Flat union with no discrimination
type EventPayload =
  | { type: 'click'; x: number; y: number }
  | { type: 'key'; key: string; ctrl: boolean }
  | { type: 'scroll'; delta: number }
  | { type: 'resize'; width: number; height: number }
  | { type: 'focus'; target: HTMLElement }
  | { type: 'blur'; target: HTMLElement }
  | { type: 'load'; url: string; duration: number }
  | { type: 'error'; message: string; stack: string };

// When checking types against this union, TypeScript must try
// each variant until it finds a match — O(n) structural check.

// BETTER: Group related events into separate discriminated unions
type UIEvent =
  | { type: 'click'; x: number; y: number }
  | { type: 'key'; key: string; ctrl: boolean }
  | { type: 'scroll'; delta: number }
  | { type: 'resize'; width: number; height: number };

type FocusEvent =
  | { type: 'focus'; target: HTMLElement }
  | { type: 'blur'; target: HTMLElement };

type LifecycleEvent =
  | { type: 'load'; url: string; duration: number }
  | { type: 'error'; message: string; stack: string };

// Process smaller unions separately for better performance
function handleUIEvent(event: UIEvent) {
  switch (event.type) {
    case 'click': /* ... */ break;
    case 'key': /* ... */ break;
    case 'scroll': /* ... */ break;
    case 'resize': /* ... */ break;
  }
}
```

### 3. Using `--skipLibCheck`

```json
// tsconfig.json
{
  "compilerOptions": {
    // Skip type checking of declaration files (.d.ts)
    // This is VERY common and generally safe — it skips
    // checking of .d.ts files, not your source code.
    // Improves build time by 20-40% in large projects.
    "skipLibCheck": true,

    // Other performance-relevant options:
    "incremental": true,
    "tsBuildInfoFile": "./.tsbuildinfo",
    "moduleResolution": "bundler",
    "target": "ES2022",
    "module": "ES2022"
  }
}
```

### 4. Incremental Compilation

```json
// tsconfig.json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./.tsbuildinfo"
  }
}
```

```typescript
// With incremental builds, TypeScript:
// 1. Saves type information to .tsbuildinfo file
// 2. On next build, only re-checks files that changed
//    (and files that depend on changed files)
// 3. Uses the cached type information from previous builds

// For large projects, this reduces rebuild time from
// 30+ seconds to under 5 seconds.

// The .tsbuildinfo file tracks:
// - Which files were compiled
// - Their version hashes
// - Dependency graph between files
// - Cached type information
```

### 5. Project References

```json
// Root tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "declaration": true,
    "declarationMap": true
  },
  "references": [
    { "path": "./packages/shared" },
    { "path": "./packages/core" },
    { "path": "./packages/api" },
    { "path": "./packages/web" }
  ]
}

// packages/shared/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"]
}

// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "references": [
    { "path": "../shared" }
  ],
  "include": ["src"]
}
```

```typescript
// With project references, TypeScript builds packages in dependency order:
// shared -> core -> api -> web
//
// Each package only re-checks when its dependencies change.
// This gives near-instant incremental builds even for huge codebases.

// Build the full project:
// npx tsc --build

// Build only changed packages:
// npx tsc --build --force  (force rebuild all)
// npx tsc --build          (incremental — only changed)
```

---

## Build Tool Comparison

### tsc vs esbuild vs swc vs babel

```typescript
// ============= tsc =============
// Full type checking + emit
// Slowest but most complete
// Supports all TS features including enums, const enums, namespaces

// Build time (1000 files, complex generics): ~15-30s
// Supports: decorators, const enums, namespaces, declaration files
// Does NOT support: tree-shaking, bundling

// ============= esbuild =============
// Extremely fast transpilation, no type checking
// Written in Go, uses parallel processing
// Build time (1000 files): ~0.5-2s

// Supports: most TS features including decorators
// Does NOT support: const enums across files, namespaces, declaration emit
// Does NOT do: type checking (use tsc separately)

// Example esbuild config
const esbuild = require('esbuild');

esbuild.buildSync({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/index.js',
  format: 'esm',
  target: 'es2022',
  sourcemap: true,
  // esbuild strips types automatically
  // It handles most TS syntax but doesn't type-check
});

// ============= swc =============
// Rust-based transpiler, very fast
// Build time (1000 files): ~1-3s
// Better compatibility with TS features than esbuild
// Used by Next.js, Vite (optionally)

// Supports: decorators, enum (with limitations), JSX, TSX
// Does NOT support: const enums, namespaces
// Does NOT do: type checking

// .swcrc configuration
const swcConfig = {
  jsc: {
    parser: {
      syntax: 'typescript',
      decorators: true,
    },
    transform: {
      legacyDecorator: true,
      decoratorMetadata: true,
    },
  },
  module: {
    type: 'es6',
  },
};

// ============= Babel =============
// Most flexible, supports all TS features via plugins
// Build time (1000 files): ~2-5s
// Best for gradual migration or non-standard syntax
// Used by create-react-app (historically)

// Does NOT do: type checking
// Requires @babel/preset-typescript

// babel.config.js
module.exports = {
  presets: [
    '@babel/preset-env',
    '@babel/preset-typescript',
    '@babel/preset-react',
  ],
};

// ============= Summary Table =============
// | Tool   | Speed   | Type Check | Decorators | Namespaces | const enum |
// |--------|---------|------------|------------|------------|------------|
// | tsc    | Slow    | Yes        | Yes        | Yes        | Yes        |
// | esbuild| Fast    | No         | Yes*       | No         | Partial    |
// | swc    | Fast    | No         | Yes        | No         | No         |
// | babel  | Medium  | No         | Yes        | Yes        | No         |
//
// * esbuild supports decorators but with limitations
```

---

## TypeScript in Frameworks

### Vite

```typescript
// Vite uses esbuild for dev and Rollup for production.
// TypeScript is transpiled (not type-checked) during dev.

// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  // esbuild handles TS transpilation in Vite
  esbuild: {
    // Enable decorator support
    tsconfigRaw: {
      compilerOptions: {
        experimentalDecorators: true,
        emitDecoratorMetadata: true,
      },
    },
  },

  // For type checking, use a separate process:
  // Add to package.json scripts:
  // "typecheck": "tsc --noEmit",
  // "dev": "vite",
  // "dev:typecheck": "tsc --noEmit --watch & vite"
});

// Vite does NOT type-check during dev — this is intentional.
// The HMR (Hot Module Replacement) must be fast, so Vite
// only transpiles the file you're editing.
//
// For type checking in your editor, use the TypeScript
// language service (VS Code, WebStorm handle this natively).
```

### webpack with ts-loader

```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: {
          loader: 'ts-loader',
          options: {
            // Option 1: Transpile only (fast)
            transpileOnly: true,

            // Option 2: Type checking (slow)
            // transpileOnly: false,

            // Option 3: Fork type checking (fast)
            // Use fork-ts-checker-webpack-plugin
          },
        },
        exclude: /node_modules/,
      },
    ],
  },
};

// Recommended: fork-ts-checker-webpack-plugin
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');

module.exports.plugins = [
  new ForkTsCheckerWebpackPlugin({
    typescript: {
      diagnosticOptions: {
        semantic: true,
        syntactic: true,
      },
    },
    // Type checking happens in a separate process
    // Main webpack build is not blocked
  }),
];
```

### Rspack

```javascript
// Rspack (Rust-based webpack alternative) with TS support
// rspack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: {
          loader: 'builtin:swc-loader',
          options: {
            jsc: {
              parser: {
                syntax: 'typescript',
              },
            },
          },
        },
      },
    ],
  },
};

// Rspack transpiles TS using SWC under the hood
// Build times are 5-10x faster than webpack
// No type checking during build — use tsc separately
```

---

## Real-World Benchmarks

```typescript
// Benchmark: Medium-sized project (500 files, 50k LOC)

// Full build (tsc --noEmit):
// - Fresh build: 18.3 seconds
// - Incremental: 2.1 seconds (90% reduction)
// - With project references: 0.8 seconds (per package)

// Transpilation only:
// - esbuild: 0.4 seconds
// - swc: 0.9 seconds
// - babel: 2.3 seconds
// - tsc (transpileOnly): 8.2 seconds

// CI/CD optimization strategy:
// 1. Run esbuild/swc for build artifacts (fast)
// 2. Run tsc --noEmit for type checking (separate step)
// 3. Use incremental/project references for caching
// 4. Cache node_modules and .tsbuildinfo in CI

// Example GitHub Actions config:
// - name: Cache TypeScript build info
//   uses: actions/cache@v3
//   with:
//     path: |
//       **/.tsbuildinfo
//       node_modules/.cache
//     key: tsbuild-${{ runner.os }}-${{ hashFiles('**/tsconfig.json') }}

// - name: Type check
//   run: npx tsc --noEmit --incremental

// - name: Build
//   run: npx esbuild src --outdir=dist --bundle

// Real-world CI times (with caching):
// - TypeScript check: ~3s (incremental, cached)
// - esbuild bundle: ~1s
// - Total build pipeline: ~5-8s
// - Without optimization: ~30-45s
```

---

## Interview Questions

### Q1: Why is TypeScript type checking slow?

**Answer:** TypeScript's type checker performs structural analysis, type instantiation, conditional type evaluation, and union distribution. For a generic type `Box<T>` used 1000 times with different type arguments, the checker creates 1000 separate instantiations. Conditional types over large unions distribute across all members. Deeply nested generics multiply instantiation count exponentially.

### Q2: What is the difference between `type` and `interface` from a performance perspective?

**Answer:** `interface` declarations are cached by their symbol name in the type checker's symbol table. `type` aliases create new type references that may need re-resolution. For types referenced thousands of times across a large codebase, interfaces can be marginally faster. However, the difference is negligible for most codebases — choose based on semantics (open vs closed) rather than performance.

### Q3: How does `--skipLibCheck` improve performance?

**Answer:** `--skipLibCheck` skips type checking of `.d.ts` declaration files. Since declaration files are pre-validated and stable, re-checking them every build is redundant. This improves build time by 20-40% in large projects. It does NOT skip checking your own source files.

### Q4: Explain project references and when to use them.

**Answer:** Project references split a codebase into independently compilable packages. Each package has `composite: true` and lists its dependencies via `references`. When building, TypeScript compiles packages in dependency order and only re-checks packages whose dependencies changed. Use them for monorepos or codebases with clear module boundaries (>50k LOC).

### Q5: How would you optimize TypeScript in a CI/CD pipeline?

**Answer:**
1. Use `tsc --incremental` with `.tsbuildinfo` caching
2. Separate type checking (`tsc --noEmit`) from bundling (esbuild/swc)
3. Cache `node_modules` and `.tsbuildinfo` in CI
4. Use `--skipLibCheck` for faster checks
5. Consider project references for monorepos
6. Use `tsc --build --dry` to detect which packages need rebuilding

### Q6: What is the difference between tsc, esbuild, and swc?

**Answer:** `tsc` is the full TypeScript compiler — type checks and emits. `esbuild` (Go) and `swc` (Rust) are transpilers that only strip types and transform syntax — 10-100x faster. esbuild/swc don't do type checking. Use esbuild/swc for building and `tsc --noEmit` separately for checking.

### Q7: How does `--generateTrace` help with performance?

**Answer:** `--generateTrace` outputs V8-compatible trace files (trace.json) that can be loaded into Chrome DevTools' Performance tab. The flame chart shows exactly which types, expressions, and files consume the most checking time. Use this to identify bottlenecks: expensive conditional types, large union distributions, or slow module resolution.

### Q8: What causes "Type instantiation is excessively deep" errors?

**Answer:** Recursive generic types without proper base case narrowing, or types that create infinitely expanding type structures. TypeScript limits instantiation depth to 50 (configurable). Fix by: adding explicit base cases, using tail-recursive conditional types (TypeScript 4.5+), or restructuring the type to avoid recursion.

### Q9: How do barrel files affect type-checking performance?

**Answer:** Barrel files (index.ts re-exporting everything) force TypeScript to resolve all re-exported modules when any single import is used. Importing `{ User }` from a barrel that re-exports 50 modules triggers resolution of all 50. This increases both type-checking time and memory usage. Use direct imports or split barrels by feature.

### Q10: Explain incremental compilation and how it works.

**Answer:** Incremental compilation saves type information to a `.tsbuildinfo` file after each build. On subsequent builds, TypeScript reads this cache and only re-checks files that changed (and their dependents). This reduces rebuild time by 80-90%. The cache tracks file hashes, dependency graphs, and resolved type information.

### Q11: What is the relationship between TypeScript and Vite regarding performance?

**Answer:** Vite uses esbuild for TS transpilation during development (no type checking), which enables sub-second HMR. Type checking is handled by the editor's TypeScript language service. For production builds, Vite uses Rollup (or optionally esbuild). Add `tsc --noEmit --watch` as a separate process for real-time type checking during development.
