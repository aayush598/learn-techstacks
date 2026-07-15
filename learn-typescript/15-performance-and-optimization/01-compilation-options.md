# TypeScript Compilation Options: Performance & Optimization

## Table of Contents

1. [The `strict` Flag Overview](#1-the-strict-flag-overview)
2. [strictNullChecks](#2-strictnullchecks)
3. [strictFunctionTypes](#3-strictfunctiontypes)
4. [strictBindCallApply](#4-strictbindcallapply)
5. [strictPropertyInitialization](#5-strictpropertyinitialization)
6. [noImplicitAny](#6-noimplicitany)
7. [noImplicitThis](#7-noimplicithis)
8. [alwaysStrict](#8-alwaysstrict)
9. [Incremental Compilation](#9-incremental-compilation)
10. [Declaration Emit](#10-declaration-emit)
11. [Source Map Options](#11-source-map-options)
12. [OutFile Bundling](#12-outfile-bundling)
13. [Best Practices](#13-best-practices)

---

## 1. The `strict` Flag Overview

The `strict` flag in `tsconfig.json` is a meta-flag that enables a suite of type-checking options that help catch bugs at compile time. Enabling `strict` is the recommended starting point for any TypeScript project.

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

When you set `"strict": true`, it enables **all** of the following flags:

| Flag | Default without `strict` | With `strict` |
|------|--------------------------|---------------|
| `strictNullChecks` | `false` | `true` |
| `strictFunctionTypes` | `false` | `true` |
| `strictBindCallApply` | `false` | `true` |
| `strictPropertyInitialization` | `false` | `true` |
| `noImplicitAny` | `false` | `true` |
| `noImplicitThis` | `false` | `true` |
| `alwaysStrict` | `false` | `true` |
| `useUnknownInCatchVariables` | `false` | `true` (TS 4.4+) |
| `exactOptionalPropertyTypes` | `false` | `false` (opt-in) |
| `noImplicitReturns` | `false` | `false` (opt-in) |
| `noFallthroughCasesInSwitch` | `false` | `false` (opt-in) |
| `noUncheckedIndexedAccess` | `false` | `false` (opt-in) |

You can enable `strict` and then selectively disable individual flags:

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": false
  }
}
```

> **Best Practice**: Always start with `strict: true` for new projects. For legacy codebases, enable flags incrementally.

---

## 2. strictNullChecks

With `strictNullChecks`, `null` and `undefined` are treated as distinct types. Without it, `null` and `undefined` are assignable to every type.

### Without strictNullChecks

```typescript
// No error — dangerous!
const name: string = null;
const age: number = undefined;

function getLength(s: string): number {
  return s.length; // No error, but s could be null at runtime
}

getLength(null); // No compile error, but throws at runtime
```

### With strictNullChecks

```typescript
// Compile errors
const name: string = null; // Error: Type 'null' is not assignable to type 'string'
const age: number = undefined; // Error: Type 'undefined' is not assignable to type 'number'

function getLength(s: string): number {
  return s.length; // OK — s is guaranteed to be a string
}

getLength(null); // Error: Argument of type 'null' is not assignable to type 'string'
```

### Working with Nullable Types

```typescript
// Use union types to explicitly allow null/undefined
function getLength(s: string | null): number {
  if (s === null) {
    return 0;
  }
  return s.length; // TypeScript knows s is string here (narrowing)
}

// Optional properties
interface User {
  name: string;
  email?: string | null; // Can be string, undefined, or null
}

function sendEmail(user: User) {
  if (user.email) {
    console.log(`Sending to ${user.email}`);
  }
}

// Non-null assertion operator (!)
function processValue(value: string | null) {
  const length = value!.length; // Tells TS "trust me, it's not null"
}

// Optional chaining
interface Company {
  ceo?: {
    name?: string;
  };
}

function getCEOName(company: Company): string {
  return company.ceo?.name ?? 'Unknown'; // Safe navigation
}

// Nullish coalescing
function getDisplayName(name: string | null | undefined): string {
  return name ?? 'Anonymous'; // Only checks null/undefined, not falsy values
}

// Note: '' and 0 are NOT nullish
getDisplayName(''); // Returns '' (not 'Anonymous')
```

### Strict Null Checks and Array Methods

```typescript
const items = [1, 2, 3, undefined, 5];

// find() returns T | undefined with strictNullChecks
const found = items.find(x => x === 3); // type: number | undefined
found.toFixed(); // Error: 'found' is possibly 'undefined'

// Must handle the undefined case
if (found !== undefined) {
  found.toFixed(); // OK
}

// Practical pattern with filter + type predicate
const numbers: (number | undefined)[] = [1, undefined, 3];
const defined: number[] = numbers.filter((n): n is number => n !== undefined);
// defined is number[]
```

---

## 3. strictFunctionTypes

This flag enables **contravariant** parameter type checking for function types. Without it, function parameters are checked **bivariantly** (which is unsound).

```typescript
// Without strictFunctionTypes, this compiles (unsound)
type Animal = { name: string };
type Dog = { name: string; breed: string };

// Bivariant: allows both widening and narrowing of parameter types
let processAnimal: (a: Animal) => void = (a) => console.log(a.name);

// Without strictFunctionTypes, this is allowed (unsound!)
let processDog: (d: Dog) => void = processDog;
processDog = processAnimal; // Error with strictFunctionTypes!
```

### Why Contravariance Matters

```typescript
// Contravariant means: you can assign a function with a BROADER parameter type
// to a variable expecting a function with a NARROWER parameter type.

type Handler<T> = (value: T) => void;

// This is safe:
let animalHandler: Handler<Animal> = (a) => console.log(a.name);
let dogHandler: Handler<Dog> = animalHandler; // OK — Animal is broader than Dog

// This is UNSOUND without strictFunctionTypes:
let stringHandler: Handler<string> = (s) => console.log(s.length);
let anyHandler: Handler<any> = stringHandler; // Error with strictFunctionTypes!
// Because anyHandler might pass a non-string value

// Real-world example: Event Emitters
interface EventEmitter<T> {
  on(event: string, handler: (data: T) => void): void;
  emit(event: string, data: T): void;
}

declare const emitter: EventEmitter<Dog>;

// With strictFunctionTypes:
// Error: handler expects Dog but emitter will pass Dog (broader Animal not allowed)
// This catches bugs where handler expects more specific types
```

---

## 4. strictBindCallApply

Ensures that `bind`, `call`, and `apply` methods have correct type checking for their arguments.

```typescript
// Without strictBindCallApply
function greet(name: string, age: number): string {
  return `Hello ${name}, age ${age}`;
}

// Without the flag, these errors are NOT caught:
greet.call(null, 42, 'world'); // Wrong order — no error without flag
greet.apply(null, [42, 'world']); // Wrong order — no error without flag

// With strictBindCallApply:
greet.call(null, 42, 'world'); // Error: Argument of type 'number' not assignable to 'string'
greet.apply(null, [42, 'world']); // Error: same

// Correct usage:
greet.call(null, 'Alice', 30); // OK
greet.apply(null, ['Alice', 30]); // OK

// bind also gets proper types
const bound = greet.bind(null, 'Bob');
bound(25); // OK — returns string
bound(); // Error: Expected 1 arguments, but got 0
bound('extra'); // Error: Argument of type 'string' not assignable to type 'number'
```

---

## 5. strictPropertyInitialization

Ensures class properties are properly initialized in the constructor or declared with default values.

```typescript
// Without strictPropertyInitialization — compiles but fails at runtime
class User {
  name: string; // May not be initialized!
  email: string;

  constructor(name: string) {
    this.name = name;
    // email is never initialized
  }
}

// With strictPropertyInitialization:
class StrictUser {
  name: string; // Error: Property 'name' has no initializer
  email: string; // Error: Property 'email' has no initializer

  constructor(name: string) {
    this.name = name; // OK — initialized in constructor
  }
}

// Solutions:

// 1. Initialize in constructor
class User1 {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

// 2. Use definite assignment assertion (!)
class User2 {
  name!: string; // Tells TS "I'll initialize this myself"
  constructor(name: string) {
    this.name = name;
  }
}

// 3. Use default values
class User3 {
  name = 'Unknown'; // Initialized with default
  email: string = '';
}

// 4. Use optional properties
class User4 {
  name?: string; // Can be undefined
}

// 5. Use parameter properties (shorthand)
class User5 {
  constructor(public name: string, public email: string) {
    // Automatically creates and initializes properties
  }
}

// 6. Use the --strictPropertyInitialization with --strictNullChecks
// Properties must be initialized in constructor ONLY IF they don't include
// undefined in their type
class User6 {
  name: string | undefined; // OK — undefined is in the type
  constructor() {
    // No need to initialize name
  }
}
```

---

## 6. noImplicitAny

Raises an error when TypeScript infers the `any` type. Forces explicit type annotations.

```typescript
// Without noImplicitAny
function add(a, b) { // Parameters implicitly typed as 'any'
  return a + b;
}
add(1, 2); // Works but no type safety

// With noImplicitAny
function add(a, b) { // Error: Parameter 'a' implicitly has an 'any' type
  return a + b;
}

// Fix by adding types
function add(a: number, b: number): number {
  return a + b;
}

// Edge cases:
// Callback parameters in forEach, map, etc. need explicit types
[1, 2, 3].forEach(x => console.log(x)); // TS infers x: number — OK
[1, 2, 3].map(x => x * 2); // TS infers x: number — OK

// But object arrays may need explicit types
const users = [{ name: 'Alice', age: 30 }];
users.filter(u => u.age > 18); // TS infers u correctly — OK

// When 'any' is truly needed, use it explicitly
function processAny(value: any): any {
  return JSON.parse(value);
}
// Use @ts-ignore or @ts-expect-error as last resort
```

---

## 7. noImplicitThis

Raises an error when `this` has an implicit `any` type.

```typescript
// Without noImplicitThis
function logName() {
  console.log(this.name); // No error, but 'this' is 'any'
}

// With noImplicitThis
function logName() {
  console.log(this.name); // Error: 'this' implicitly has type 'any'
}

// Fix with 'this' parameter
interface HasName {
  name: string;
}

function logName(this: HasName) {
  console.log(this.name); // OK — 'this' is typed as HasName
}

// Usage with call/apply/bind
const obj = { name: 'Alice', log: logName };
obj.log(); // OK

// Arrow functions capture 'this' from enclosing scope
class Counter {
  count = 0;

  increment() {
    // Arrow function captures 'this' from increment method
    setInterval(() => {
      this.count++; // OK — 'this' refers to Counter instance
    }, 1000);
  }
}

// Callback context typing
interface Button {
  onClick: (this: void, event: Event) => void;
}
```

---

## 8. alwaysStrict

Parses in strict mode and emits `"use strict"` at the top of each output file.

```json
{
  "compilerOptions": {
    "alwaysStrict": true
  }
}
```

```typescript
// Output will have "use strict" at the top:
// "use strict";
// Object.defineProperty(exports, "__esModule", { value: true });
// function greet(name) {
//     return `Hello, ${name}`;
// }

// In strict mode:
// - 'with' statements are forbidden
// - Silent errors become thrown errors
// - eval doesn't create variables in surrounding scope
// - 'this' in functions is undefined (not global object)
// - Duplicate parameter names are errors
// - Octal literals are forbidden
```

---

## 9. Incremental Compilation

Incremental compilation reuses previously compiled project information to speed up subsequent builds.

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  }
}
```

### How It Works

```typescript
// After the first build, TypeScript writes a .tsbuildinfo file
// containing:
// - Semantic diagnostics (type errors)
// - Declaration file hashes
// - Affected file lists

// On subsequent builds:
// 1. TypeScript reads the .tsbuildinfo file
// 2. Checks which source files have changed
// 3. Only re-checks types for changed files + their dependents
// 4. Updates the .tsbuildinfo file

// Example tsBuildInfoFile output structure (conceptual):
// {
//   "version": "4.9.5",
//   "root": ["src/index.ts", "src/utils.ts"],
//   "inputs": {
//     "src/index.ts": { "version": 1234, "signature": "..." },
//     "src/utils.ts": { "version": 5678, "signature": "..." }
//   },
//   "errors": []
// }
```

### Incremental Build Performance

```bash
# First build: full compilation
tsc --incremental
# Output: ~2.5 seconds

# Second build (no changes): near-instant
tsc --incremental
# Output: ~0.1 seconds

# Third build (one file changed): partial
tsc --incremental
# Output: ~0.3 seconds
```

### composite and incremental Together

```json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "declaration": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  }
}
```

> **Note**: `composite: true` implies `declaration: true` and `incremental: true`.

---

## 10. Declaration Emit

Control how `.d.ts` declaration files are generated.

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "declarationDir": "./types",
    "emitDeclarationOnly": false
  }
}
```

### declaration: true

```typescript
// src/utils.ts
export function add(a: number, b: number): number {
  return a + b;
}

export interface Config {
  debug: boolean;
  version: string;
}

// Generated declaration file (utils.d.ts):
// export declare function add(a: number, b: number): number;
// export interface Config {
//     debug: boolean;
//     version: string;
// }
```

### declarationMap: true

```typescript
// Generates .d.ts.map files that map declaration files back to source
// Useful for "Go to Definition" in IDEs to jump to source instead of declaration

// Generated utils.d.ts.map:
// {
//   "version": 3,
//   "file": "utils.js",
//   "sourceRoot": "",
//   "sources": ["../src/utils.ts"],
//   "names": [],
//   "mappings": "..."
// }
```

### declarationDir

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationDir": "./dist/types"
  }
}
```

```bash
# Source: src/utils.ts
# Output: dist/utils.js + dist/types/utils.d.ts
```

### emitDeclarationOnly

```json
{
  "compilerOptions": {
    "emitDeclarationOnly": true
  }
}
```

```bash
# Only generates .d.ts files, no .js output
# Useful when bundling with another tool (webpack, esbuild, rollup)
```

---

## 11. Source Map Options

Source maps allow debugging original TypeScript in the browser/dev tools.

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "declarationMap": true,
    "sourceRoot": "./src",
    "mapRoot": "./dist",
    "inlineSourceMap": false,
    "inlineSources": false
  }
}
```

### Source Map Types

```bash
# Standard source map (.js + .js.map)
# dist/
#   utils.js
#   utils.js.map

# Inline source map (embedded in .js file)
# dist/
#   utils.js  (contains base64-encoded source map at the end)
```

### Source Map Options Explained

```typescript
// sourceMap: true — generates external .map files
// dist/utils.js.map

// inlineSourceMap: true — embeds source map in .js file
// Useful for single-file bundles or environments that don't support
// separate .map files

// inlineSources: true — includes original TypeScript source in the map
// Allows debugging original .ts files even if .ts sources aren't available

// sourceRoot: "./src" — specifies the root path for debugger to find sources
// Used in the .map file: "sourceRoot": "./src"

// mapRoot: "./dist" — specifies where .map files should be output
```

### Practical Configuration for Debugging

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "declaration": true,
    "declarationMap": true,
    "sourceRoot": "./src",
    "inlineSources": true,
    "removeComments": false
  }
}
```

---

## 12. OutFile Bundling

Bundles all output into a single file (only for `--module amd` or `--module system`).

```json
{
  "compilerOptions": {
    "module": "amd",
    "outFile": "./dist/bundle.js"
  }
}
```

```typescript
// src/utils.ts
export function add(a: number, b: number) {
  return a + b;
}

// src/index.ts
import { add } from './utils';
console.log(add(1, 2));

// Output bundle (dist/bundle.js):
// var Utils;
// (function (Utils) {
//     function add(a, b) { return a + b; }
//     Utils.add = add;
// })(Utils || (Utils = {}));
//
// var Utils_1 = Utils;
// console.log(Utils_1.add(1, 2));
```

### outFile vs Bundler Tools

```bash
# outFile limitations:
# - Only works with --module amd or --module system
# - Doesn't support tree-shaking well
# - Limited control over bundle structure
# - No code splitting

# Better alternatives:
# - esbuild: extremely fast bundler
# - rollup: tree-shaking optimized
# - webpack: full-featured bundler
# - Vite: dev server + build tool

# Use outFile only for:
# - Simple projects
# - Libraries that need a single-file UMD bundle
# - Legacy projects using AMD modules
```

---

## 13. Best Practices

### Recommended tsconfig for New Projects

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": false,
    "noUncheckedIndexedAccess": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Recommended tsconfig for Libraries

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2018",
    "module": "ESNext",
    "moduleResolution": "Node",
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationDir": "./dist/types",
    "declarationMap": true,
    "sourceMap": true,
    "composite": true,
    "incremental": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Quick Reference: Common Flags

```bash
# Strict mode
--strict                          # Enable all strict checks

# Incremental builds
--incremental                     # Enable incremental compilation
--tsBuildInfoFile <path>          # Path for build info file

# Declaration files
--declaration                     # Generate .d.ts files
--declarationDir <path>           # Output directory for .d.ts files
--declarationMap                  # Generate .d.ts.map files
--emitDeclarationOnly             # Only emit .d.ts files

# Source maps
--sourceMap                       # Generate .js.map files
--inlineSourceMap                 # Embed source map in .js file
--inlineSources                   # Include original source in map
--sourceRoot <path>               # Root path for source files
--mapRoot <path>                  # Output path for .map files

# Bundling
--outFile <path>                  # Bundle all output into one file
```

---

## Interview Questions

**Q1**: What is the difference between `strictNullChecks` and `strictFunctionTypes`?
**A**: `strictNullChecks` makes `null` and `undefined` distinct types that aren't assignable to other types. `strictFunctionTypes` enables contravariant parameter type checking for functions.

**Q2**: Why should you use `strict: true` in new projects?
**A**: It enables all strict type-checking options, catching bugs at compile time. It's the recommended starting point because it's easier to write strict code from scratch than to add strictness later.

**Q3**: What does `incremental` compilation do and when should you use it?
**A**: It caches compilation information in a `.tsbuildinfo` file, allowing TypeScript to only re-check types for changed files on subsequent builds. Use it for large projects where full compilation takes significant time.

**Q4**: When would you use `outFile` vs a bundler like webpack?
**A**: `outFile` is only useful for AMD/System module projects that need a single bundle. For most modern projects, use webpack/rollup/esbuild as they support tree-shaking, code splitting, and multiple module formats.

**Q5**: What is the difference between `declarationMap` and `sourceMap`?
**A**: `sourceMap` maps compiled JS back to original TS source for debugging. `declarationMap` maps `.d.ts` files back to TS source, enabling "Go to Definition" to jump to the actual source code.
