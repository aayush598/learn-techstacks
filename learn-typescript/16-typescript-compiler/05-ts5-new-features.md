# TypeScript 4.7 through 5.5+ New Features

## Table of Contents

1. [TypeScript 4.7+](#typescript-47)
2. [TypeScript 4.8+](#typescript-48)
3. [TypeScript 4.9+](#typescript-49)
4. [TypeScript 5.0](#typescript-50)
5. [TypeScript 5.1+](#typescript-51)
6. [TypeScript 5.2+](#typescript-52)
7. [TypeScript 5.3+](#typescript-53)
8. [TypeScript 5.4+](#typescript-54)
9. [TypeScript 5.5+](#typescript-55)
10. [Migration Guide](#migration-guide)
11. [Interview Questions](#interview-questions)

---

## TypeScript 4.7+

### Variance Annotations (`in`/`out` on Type Parameters)

TypeScript 4.7 introduced explicit variance annotations. These let you declare whether
a type parameter is covariant (`out`), contravariant (`in`), or invariant (`in out`):

```typescript
// Covariant: T only in output positions
interface Producer<out T> {
  produce(): T;
}

// Contravariant: T only in input positions
interface Consumer<in T> {
  consume(item: T): void;
}

// Invariant: T in both positions
interface Transformer<in out T> {
  transform(input: T): T;
}

// Error if usage violates annotation
interface BadProducer<out T> {
  consume(item: T): void; // ❌ Error: T is contravariant but annotated as covariant
}
```

### `--moduleResolution bundler`

The new `bundler` module resolution strategy is designed for modern bundlers like
Webpack, Vite, esbuild, and others:

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "module": "esnext",
    "target": "es2022"
  }
}
```

**Key differences from `node` resolution:**

```typescript
// With moduleResolution: "node"
import { foo } from './bar'; // Looks for bar.ts, bar.tsx, bar.d.ts, bar/index.ts
import { foo } from './bar.js'; // ❌ Error — .js extension not allowed for .ts files

// With moduleResolution: "bundler"
import { foo } from './bar'; // ✅ Resolves bar.ts, bar.tsx, etc.
import { foo } from './bar.js'; // ✅ Resolves bar.ts (strips .js extension)
import { foo } from './bar.ts'; // ✅ Also works (when allowImportingTsExtensions is set)
```

**When to use `bundler`:**

```typescript
// Use bundler when:
// - You're building a frontend app with Vite, Webpack, esbuild, etc.
// - You use .js extensions in imports (common in ESM)
// - You want TypeScript to match your bundler's resolution

// Use node when:
// - You're building a Node.js app without a bundler
// - You need CommonJS compatibility
// - You're building a library targeting Node.js

// Use node16/nodenext when:
// - You're building a Node.js app with native ESM support
// - You need strict ESM/CJS interop
```

### Instantiation Expressions

Create new types by applying type arguments to existing declarations:

```typescript
function createArray<T>(length: number, fill: T): T[] {
  return Array(length).fill(fill);
}

// Before: You'd need a wrapper type or utility
type StringArray = string[];
type NumberArray = number[];

// With instantiation expressions:
type StringArray = typeof createArray<string>;
// Equivalent to: (length: number, fill: string) => string[]

// More complex examples:
type AnimalFactory = typeof createArray<Animal>;
type NullableMap = typeof Map<string, unknown>;
type EventCallback = typeof addEventListener<MouseEvent>;

// Use in type annotations:
function processStrings(factory: typeof createArray<string>): string[] {
  return factory(10, 'hello');
}

// Combine with other types:
type ReadonlyStringArray = ReadonlyArray<string>;
type MapFactory = typeof Map<string, number>;
```

### `extends` Constraints on `infer`

You can now constrain `infer` types within conditional types:

```typescript
// Before TS 4.7: No way to constrain infer
type Unpack<T> = T extends Promise<infer U> ? U : T;
type Result = Unpack<Promise<string>>; // string

// With TS 4.7: Constrain infer to specific types
type UnpackNumber<T> = T extends Promise<infer U extends number> ? U : never;
type NumResult = UnpackNumber<Promise<number>>; // number
type BadResult = UnpackNumber<Promise<string>>; // never (string doesn't extend number)

// Practical example: Extract array element types only if they extend Animal
type AnimalArray<T> = T extends Array<infer U extends Animal> ? U : never;
type Cats = AnimalArray<Cat[]>; // Cat
type Strings = AnimalArray<string[]>; // never (string doesn't extend Animal)

// Multiple infer constraints
type DeepUnpack<T> = T extends Promise<infer U extends Animal>
  ? U
  : T extends Array<infer V extends Animal>
  ? V
  : never;
```

---

## TypeScript 4.8+

### Inference Narrowing from Constraints

TypeScript 4.8 narrows the inferred type based on the constraint, making the result
more precise:

```typescript
// Before TS 4.8: Inferred type was the constraint itself
function process<T extends string | number>(value: T): T {
  return value;
}

// The return type was T (unconstrained), not narrowed

// With TS 4.8: Better inference from constraints
type ArrayElement<T extends unknown[]> = T extends (infer E)[] ? E : never;

type Numbers = ArrayElement<number[]>; // number (was unknown before)
type Strings = ArrayElement<string[]>; // string (was unknown before)

// Practical example:
function first<T extends unknown[]>(arr: T): T[0] {
  return arr[0];
}

const num = first([1, 2, 3]); // type: number (was number | undefined before)
const str = first(['a', 'b']); // type: string (was string | undefined before)
```

### Unmatched Expression Checks in `--exactOptionalPropertyTypes`

```typescript
// With exactOptionalPropertyTypes
interface Config {
  name?: string;
  age?: number;
}

// Before: These were treated the same
const c1: Config = { name: 'Alice' }; // OK
const c2: Config = { name: undefined }; // ❌ Error with exactOptionalPropertyTypes

// The `?` means "the property can be absent", NOT "the property can be undefined"
// With exactOptionalPropertyTypes:
// - Omitting the property: ✅
// - Setting to the type: ✅
// - Setting to undefined: ❌ (unless explicitly `string | undefined`)
```

### `--noImplicitOverride` (Implicit Override Check)

```typescript
// With noImplicitOverride
class Base {
  greet(): string {
    return 'hello';
  }
}

class Derived extends Base {
  greet(): string { // ❌ Error: This member must have an 'override' modifier
    return 'hi';
  }
}

// Fix: Add 'override' keyword
class Derived extends Base {
  override greet(): string { // ✅ OK
    return 'hi';
  }
}

// This prevents accidental method shadowing and makes override intent explicit
```

---

## TypeScript 4.9+

### `satisfies` Operator (Deep Dive)

The `satisfies` operator validates that an expression matches a type without widening
it. Unlike `as`, it preserves the literal type:

```typescript
// The `as` type assertion WIDENS the type
const config1 = {
  port: 3000,
  host: 'localhost',
} as {
  port: number;
  host: string;
};
// config1.port is `number`, not `3000`

// The `satisfies` operator VALIDATES but preserves the type
const config2 = {
  port: 3000,
  host: 'localhost',
} satisfies {
  port: number;
  host: string;
};
// config2.port is `3000`, not `number` — type is preserved!

// Practical example: Route definitions
type Route = {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  handler: () => void;
};

const routes = [
  { path: '/', method: 'GET', handler: () => {} },
  { path: '/api', method: 'POST', handler: () => {} },
] satisfies Route[];

// routes[0].method is 'GET', not 'string' — preserved!
// But we also get type checking:
routes.push({ path: '/bad', method: 'PATCH', handler: () => {} });
// ❌ Error: 'PATCH' is not assignable to 'GET' | 'POST' | 'PUT' | 'DELETE'

// Another example: Enum-like objects
type Color = 'red' | 'green' | 'blue';

const colors = {
  primary: 'red',
  secondary: 'green',
  accent: 'blue',
} satisfies Record<string, Color>;

// colors.primary is 'red', not Color — preserved!
// But validation ensures all values are Color colors

// Works with nested objects too:
const deepConfig = {
  database: {
    host: 'localhost',
    port: 5432,
  },
  cache: {
    host: 'redis',
    port: 6379,
  },
} satisfies {
  database: { host: string; port: number };
  cache: { host: string; port: number };
};

// Deep config types are preserved with full validation
```

### `--noCheck` Option

Skip type checking for faster builds during development:

```json
{
  "compilerOptions": {
    "noCheck": true // Skips ALL type checking
  }
}
```

**When to use:**
- During development for faster rebuilds
- When you have a separate type-checking step in CI
- With tools like `tsc --noEmit` for quick feedback

**When NOT to use:**
- In production builds
- When you want type safety during development
- When CI doesn't have a separate type-checking step

### Symbol Description in `unique symbol`

```typescript
// Before TS 4.9: unique symbols couldn't have descriptions
const secret = Symbol(); // No way to add description

// With TS 4.9: unique symbols can have descriptions
const secret = Symbol('my-secret-key');
console.log(secret.toString()); // Symbol(my-secret-key)

// Useful for debugging
interface TokenMap {
  [secret]: string;
  [Symbol.iterator]: () => Iterator<string>;
}
```

---

## TypeScript 5.0

### `const` Type Parameters (Deep Dive)

The `const` modifier on type parameters makes TypeScript infer the narrowest possible
type (literal types instead of widening):

```typescript
// Without `const`: TypeScript widens to general types
function processArray<T>(items: T[]): T {
  return items[0];
}

const result1 = processArray([1, 2, 3]);
// result1 type: number (widened)

// With `const`: TypeScript infers literal types
function processArray<const T extends readonly unknown[]>(items: T): T[number] {
  return items[0];
}

const result2 = processArray([1, 2, 3]);
// result2 type: 1 (narrowed!)

// Practical example: Theme definitions
type Theme = 'light' | 'dark' | 'system';

// Without const: Theme[]
function getThemes<const T extends Theme[]>(themes: T): T {
  return themes;
}

const themes = getThemes(['light', 'dark']);
// themes type: readonly ['light', 'dark'] (preserved!)
// themes[0] is 'light', not Theme

// With const: More precise event maps
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string };
};

function createEmitter<const T extends Record<string, unknown>>(events: T): T {
  return events;
}

const emitter = createEmitter({
  click: { x: 0, y: 0 },
  keydown: { key: 'a' },
});

// emitter.click is { x: 0; y: 0 }, not { x: number; y: number }
```

### Decorators (TC39 Stage 3)

TypeScript 5.0 supports TC39 Stage 3 decorators:

```typescript
// Class decorator
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return `Hello, ${this.greeting}`;
  }
}

// Method decorator
function log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    return originalMethod.apply(this, args);
  };
}

class Calculator {
  @log
  add(a: number, b: number): number {
    return a + b;
  }
}

// Property decorator
function validate(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalSet = descriptor.set;
  descriptor.set = function (value: any) {
    if (typeof value !== 'string') {
      throw new Error(`${propertyKey} must be a string`);
    }
    originalSet.call(this, value);
  };
}

class User {
  @validate
  name: string = '';
}
```

### `--verbatimModuleSyntax` (Replaces `importsNotUsedAsValues`)

This flag enforces explicit import/export syntax and makes module transforms predictable:

```typescript
// With verbatimModuleSyntax:
import type { Cat } from './animal'; // ✅ Type-only import (removed in JS)
import { Dog } from './animal'; // ✅ Value import (kept in JS)

// ❌ Error: This import is neither used as a value nor marked as type-only
import { Cat } from './animal';

// Fix: Use `import type` for type-only imports
import type { Cat } from './animal';

// Export also works the same way:
export type { Cat } from './animal'; // Type-only export
export { Dog } from './animal'; // Value export
```

**Benefits over `importsNotUsedAsValues`:**

```typescript
// verbatimModuleSyntax is more predictable:
// - `import type` → always removed in JS
// - `import` → always kept in JS
// - No more "import was removed because it was only used as a type"

// Before (with importsNotUsedAsValues: "error"):
import { Cat } from './animal'; // If Cat is only used as type, this was an error

// After (with verbatimModuleSyntax):
import type { Cat } from './animal'; // Explicit type import
```

### Multiple Config Extensions (`extends` Array)

```typescript
// tsconfig.json
{
  "extends": [
    "@tsconfig/node18/tsconfig.json",
    "@tsconfig/strictest/tsconfig.json"
  ],
  "compilerOptions": {
    "outDir": "./dist"
  }
}

// Config is merged left-to-right, with later configs overriding earlier ones
// Your local compilerOptions override everything
```

### `--target es2022`

```json
{
  "compilerOptions": {
    "target": "es2022"
  }
}
```

Enables:
- Top-level `await`
- `Object.hasOwn()`
- Error cause
- Array.at()
- RegExp match indices
- Class fields and static blocks

### Enum Improvements

```typescript
// Const enums now work with isolatedModules
const enum Color {
  Red,
  Green,
  Blue,
}

// Before: const enums were problematic with isolatedModules
// After: TypeScript can handle them correctly

// Also: enums can now be used as types
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

function move(dir: Direction) {
  // dir is the Direction enum type
}

// Enum as a type is the same as the enum itself
type Dir = Direction; // ✅ Valid
```

---

## TypeScript 5.1+

### `--allowImportingTsExtensions`

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "allowImportingTsExtensions": true,
    "noEmit": true // Required when using this option
  }
}

// Now you can import with .ts extensions
import { foo } from './bar.ts';
import { baz } from './utils/helpers.ts';

// This aligns with how bundlers resolve imports
```

### `--isolatedDeclarations`

Requires explicit return types and exported types for faster declaration generation:

```typescript
// Without isolatedDeclarations (can infer types)
export function add(a: number, b: number) {
  return a + b; // Return type inferred as number
}

// With isolatedDeclarations (must be explicit)
export function add(a: number, b: number): number {
  return a + b; // Return type must be declared
}

// Also affects classes
export class Calculator {
  // Must have explicit types
  value: number;

  constructor(value: number) {
    this.value = value;
  }

  // Must have explicit return type
  add(n: number): this {
    this.value += n;
    return this;
  }
}

// Arrow functions
export const multiply = (a: number, b: number): number => a * b;
```

### `NoInfer` Utility Type

Prevents TypeScript from inferring a type from a specific position:

```typescript
// Problem: TypeScript infers T from the wrong position
function createFSM<T extends string>(start: T, transitions: T[]): T {
  return start;
}

// TypeScript infers T from both start and transitions
// This can lead to unexpected behavior

// With NoInfer: Block inference from a specific position
function createFSM<T extends string>(
  start: T,
  transitions: NoInfer<T>[]
): T {
  return start;
}

const fsm = createFSM('idle', ['running', 'idle']);
// TypeScript now infers T from 'idle' only
// transitions must be type-compatible with the inferred T

// Another example:
function createMap<K extends string, V>(
  defaultKey: NoInfer<K>,
  defaultValue: V
): Map<K, V> {
  return new Map();
}

// K is inferred from usage, not from defaultKey
```

### `Prettify<T>` Type Pattern

While not a built-in utility type, this pattern became popular with TS 5.1:

```typescript
type Prettify<T> = {
  [K in keyof T]: T[K];
} & {};

// Useful for flattening intersection types in tooltips
type A = { name: string } & { age: number };
type PrettyA = Prettify<A>;
// Instead of showing: { name: string } & { age: number }
// Shows: { name: string; age: number }

// Common pattern in component props:
type Props = Prettify<
  HTMLAttributes<HTMLDivElement> & {
    variant: 'primary' | 'secondary';
    size: 'sm' | 'md' | 'lg';
  }
>;
```

### Namespace Improvements

```typescript
// Namespaced imports are now better supported
import * as fs from 'node:fs/promises';

// `exports =` syntax for CJS modules
export = {
  hello: () => 'world',
};

// Named imports from CJS
import pkg from './package.json';
```

---

## TypeScript 5.2+

### `using` Declarations (Explicit Resource Management)

The `using` keyword implements the TC39 Explicit Resource Management proposal:

```typescript
// Define a disposable resource
class DatabaseConnection implements Disposable {
  private connection: any;

  constructor(url: string) {
    this.connection = connect(url);
    console.log('Connected to database');
  }

  query(sql: string): any {
    return this.connection.query(sql);
  }

  // Symbol.dispose is called automatically
  [Symbol.dispose](): void {
    this.connection.close();
    console.log('Database connection closed');
  }
}

// Using `using` keyword
function handleDatabase() {
  using conn = new DatabaseConnection('postgres://localhost/mydb');
  // Use the connection
  const result = conn.query('SELECT * FROM users');
  // conn[Symbol.dispose]() is called automatically when going out of scope
}

// Async disposable resources
class AsyncFile implements AsyncDisposable {
  private fileHandle: any;

  constructor(path: string) {
    this.fileHandle = open(path);
  }

  async read(): Promise<string> {
    return this.fileHandle.read();
  }

  async [Symbol.asyncDispose](): Promise<void> {
    await this.fileHandle.close();
  }
}

// Using async disposable
async function processFile() {
  await using file = new AsyncFile('data.txt');
  const content = await file.read();
  // file[Symbol.asyncDispose]() is called automatically
}
```

### Decorator Metadata (`Symbol.metadata`)

```typescript
// Decorators can now access metadata through Symbol.metadata
function meta(value: string) {
  return (target: any, context: ClassMethodDecoratorContext) => {
    if (!context.metadata) {
      context.metadata = {};
    }
    context.metadata[context.name] = value;
  };
}

class API {
  @meta('GET')
  getUser(): void {}

  @meta('POST')
  createUser(): void {}
}

// Access metadata
console.log(API[Symbol.metadata]);
// { getUser: 'GET', createUser: 'POST' }
```

### Named and Anonymous Tuple Elements

```typescript
// Before: Tuples could have named elements
type Range = [start: number, end: number];

// After TS 5.2: Better support for named tuples
function createRange(start: number, end: number): Range {
  return [start, end];
}

// Named elements improve documentation
type UserRecord = [id: string, name: string, email: string];

function processUser([id, name, email]: UserRecord): void {
  console.log(`${name} (${email})`);
}

// Anonymous tuples (no labels) still work
type Pair = [number, string];
```

---

## TypeScript 5.3+

### Import Attributes

```typescript
// Import attributes (TC39 proposal)
import data from './data.json' with { type: 'json' };
import stylesheet from './styles.css' with { type: 'css' };

// TypeScript validates the attribute syntax
// This helps bundlers and runtimes know how to handle the import
```

### `--isolatedDeclarations` Improvements

```typescript
// Better inference for common patterns
export const PI = 3.14159; // Now OK without explicit type
export const MAX_SIZE = 1024; // Literal types are OK

// Computed values still need explicit types
export const DOUBLE_PI = PI * 2; // ❌ Error with isolatedDeclarations
export const DOUBLE_PI: number = PI * 2; // ✅ Fixed
```

### Type Narrowing Improvements

```typescript
// Better narrowing in complex scenarios
function process(value: string | number | null) {
  if (value !== null && typeof value === 'string') {
    // value is now narrowed to string
    return value.toUpperCase();
  }

  if (typeof value === 'number' && value > 0) {
    // value is narrowed to number
    return value.toFixed(2);
  }
}

// Improved narrowing with template literals
function handleId(id: `user_${number}` | `post_${number}`) {
  if (id.startsWith('user_')) {
    const userId = id.slice(5); // number
    // userId is narrowed to number
  }
}
```

---

## TypeScript 5.4+

### `NoInfer` Utility Type Improvements

```typescript
// Better behavior with union types
function createFSM<T extends string>(
  states: NoInfer<T>[],
  initial: T
): T {
  return initial;
}

const fsm = createFSM(['idle', 'running', 'stopped'], 'idle');
// T is inferred as 'idle' from the second argument
// states must be compatible with 'idle'[]

// Previously, T would be inferred from both positions
// leading to: T = 'idle' | 'running' | 'stopped'
// Now: T = 'idle' (only from the initial state)
```

### `--isolatedDeclarations` Improvements

```typescript
// Better support for common patterns
export const DEFAULT_CONFIG = {
  port: 3000,
  host: 'localhost',
} as const; // ✅ OK with isolatedDeclarations

// Enum values
export enum Status {
  Active = 'active',
  Inactive = 'inactive',
}

// Enum members as types
export type StatusType = `${Status}`; // 'active' | 'inactive'
```

### Narrowing in Closures Improvement

```typescript
// Before: narrowing didn't always work in closures
function processItems(items: (string | number)[]) {
  const filtered = items.filter((item): item is string => typeof item === 'string');

  // Before TS 5.4: This wasn't always narrowed
  filtered.forEach((item) => {
    console.log(item.toUpperCase()); // Now works correctly!
  });
}

// Better narrowing with Array methods
function sumPositiveNumbers(numbers: (number | string)[]): number {
  return numbers
    .filter((n): n is number => typeof n === 'number' && n > 0)
    .reduce((sum, n) => sum + n, 0); // n is correctly narrowed to number
}
```

---

## TypeScript 5.5+

### `--rewriteRelativeImportExtensions`

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "rewriteRelativeImportExtensions": true,
    "noEmit": false,
    "declaration": true
  }
}

// Write imports with .ts extensions (modern ESM style)
import { foo } from './bar.ts';

// When compiling to .js, TypeScript rewrites them
// Output: import { foo } from './bar.js';

// This is the recommended approach for new projects
// Write .ts, compile to .js, imports are rewritten automatically
```

### Regex Syntax Checking in Type Positions

```typescript
// TypeScript now validates regex syntax in type positions
type ExtractNumbers<S extends string> = S extends `${infer _Start}${infer Num extends number}${infer _Rest}`
  ? Num
  : never;

// Better template literal type inference
type ParseRoute<T extends string> =
  T extends `/${infer Segment}/${infer Rest}`
    ? [Segment, ...ParseRoute<`/${Rest}`>]
    : T extends `/${infer Segment}`
    ? [Segment]
    : [];

type Result = ParseRoute<'/users/123/posts'>;
// ['users', '123', 'posts']

// Regex-like patterns in types
type MatchEmail<S extends string> =
  S extends `${infer User}@${infer Domain}.${infer TLD}`
    ? { user: User; domain: `${Domain}.${TLD}` }
    : never;

type Parsed = MatchEmail<'alice@example.com'>;
// { user: 'alice'; domain: 'example.com' }
```

### Type Narrowing Improvements

```typescript
// Improved control flow analysis
function process(value: string | number | null | undefined) {
  if (value == null) {
    // value is null | undefined (both null and undefined)
    return;
  }

  // value is string | number
  if (typeof value === 'string') {
    // value is string
    return value.toUpperCase();
  }

  // value is number
  return value.toFixed(2);
}

// Better narrowing with optional chaining
function getLength(value: string | null | undefined): number {
  return value?.length ?? 0; // Correctly narrowed
}

// Improved narrowing in switch statements
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2; // shape narrowed to circle
    case 'rectangle':
      return shape.width * shape.height; // shape narrowed to rectangle
  }
}
```

### `Promise.resolve` Type Improvement

```typescript
// Before TS 5.5: Promise.resolve<T> was often too loose
const promise1 = Promise.resolve(42);
// Type: Promise<number> (widened from 42)

// With TS 5.5: Better type preservation
const promise2 = Promise.resolve(42 as const);
// Type: Promise<42> (preserved as literal!)

// Practical example:
async function fetchData() {
  const response = await Promise.resolve({ status: 200, data: [] });
  // response is { status: 200; data: never[] }
  // More precise than before
}
```

---

## Migration Guide

### Breaking Changes Per Version

```typescript
// TS 4.7 → 4.8:
// - Inference from constraints changed (may affect generics)
// - `--exactOptionalPropertyTypes` stricter

// TS 4.8 → 4.9:
// - `satisfies` is a reserved keyword
// - Some union type narrowing changes

// TS 4.9 → 5.0:
// - Decorators changed to TC39 Stage 3 syntax
// - `--importsNotUsedAsValues` deprecated
// - `--suppressImplicitAnyIndexErrors` removed
// - Enum exhaustiveness checks

// TS 5.0 → 5.1:
// - `isolatedDeclarations` may require type annotations
// - `allowImportingTsExtensions` requires `noEmit`

// TS 5.1 → 5.2:
// - `using` keyword reserved
// - `Symbol.dispose` and `Symbol.asyncDispose` required

// TS 5.2 → 5.3:
// - Import attributes may affect build

// TS 5.3 → 5.4:
// - Narrowing behavior changes in closures

// TS 5.4 → 5.5:
// - `rewriteRelativeImportExtensions` may change output
```

### How to Upgrade Safely

```bash
# Step 1: Update TypeScript
npm install typescript@latest --save-dev

# Step 2: Check for errors
npx tsc --noEmit

# Step 3: Update tsconfig.json
# - Replace importsNotUsedAsValues with verbatimModuleSyntax
# - Update target if needed
# - Add new strict flags if desired

# Step 4: Fix any new errors
# - Add explicit return types if using isolatedDeclarations
# - Update decorator syntax if using decorators
# - Add `override` keyword if using noImplicitOverride

# Step 5: Test your application
npm test

# Step 6: Update CI/CD
# - Ensure CI uses the same TypeScript version
# - Update any TypeScript-related tools (ts-node, tsx, etc.)
```

### Deprecation Timeline

```typescript
// Deprecated in TS 4.9:
// - importsNotUsedAsValues → use verbatimModuleSyntax

// Deprecated in TS 5.0:
// - suppressImplicitAnyIndexErrors → use @ts-ignore or proper types
// - noImplicitUseStrict → removed
// - keyofStringsOnly → use keydown event type

// Deprecated in TS 5.2:
// - Old decorator syntax → use TC39 Stage 3 decorators

// Deprecated in TS 5.4:
// - Some type narrowing patterns → use improved narrowing

// Always check release notes for the latest deprecations
```

---

## Interview Questions

### Q1: What is the `satisfies` operator and how does it differ from `as`?

**A:** `satisfies` validates that an expression matches a type while preserving the
literal type. `as` type-asserts (and widens) the type:

```typescript
const config = { port: 3000 } as { port: number };
// config.port is `number`

const config2 = { port: 3000 } satisfies { port: number };
// config2.port is `3000` (preserved!)
```

### Q2: What are const type parameters?

**A:** The `const` modifier on type parameters makes TypeScript infer the narrowest
possible type (literal types instead of widening):

```typescript
function createArray<const T extends readonly unknown[]>(items: T): T {
  return items;
}

const arr = createArray([1, 2, 3]);
// arr type: readonly [1, 2, 3] (not number[])
```

### Q3: What is `verbatimModuleSyntax`?

**A:** A flag that enforces explicit import/export syntax. `import type` is always removed
in JS output, `import` is always kept. It replaces the deprecated `importsNotUsedAsValues`
and provides more predictable module transforms.

### Q4: What are decorators in TypeScript 5.0?

**A:** TC39 Stage 3 decorators that replace the legacy decorator syntax. They use a
different API (`context` parameter with `metadata`, `name`, `static` properties) and
are compatible with the JavaScript decorator proposal.

### Q5: What is `NoInfer` utility type?

**A:** `NoInfer<T>` prevents TypeScript from inferring `T` from a specific position.
This is useful when you want type inference to come from one argument but not another:

```typescript
function createFSM<T extends string>(
  initial: T,
  transitions: NoInfer<T>[]
): T { ... }
```

### Q6: What is `using` declaration?

**A:** The `using` keyword implements TC39 Explicit Resource Management. It ensures
`Symbol.dispose()` (or `Symbol.asyncDispose()`) is called automatically when the
variable goes out of scope, similar to C#'s `using` or Python's `with`:

```typescript
using conn = new DatabaseConnection();
// conn[Symbol.dispose]() called automatically
```

### Q7: How does `--moduleResolution bundler` differ from `node`?

**A:** `bundler` is designed for modern bundlers (Vite, Webpack, esbuild). Key differences:
- Allows `.js` extensions in imports for `.ts` files
- Allows extensionless imports
- More lenient about file existence
- Better matches how bundlers actually resolve modules

### Q8: What is `--isolatedDeclarations`?

**A:** A flag that requires explicit return types and exported type annotations. This
enables faster declaration file generation because TypeScript doesn't need to infer types
across module boundaries. Useful for large codebases where declaration generation is slow.

### Q9: What are import attributes?

**A:** A TC39 proposal (Stage 3) that lets you specify how imports should be handled:
```typescript
import data from './data.json' with { type: 'json' };
```
TypeScript validates the syntax, and runtimes/bundlers use the attributes to process
the import correctly.

### Q10: Explain the difference between `as` and `satisfies` with an example.

**A:** `as` is a type assertion that widens the type to the asserted type. `satisfies`
is a type validation that preserves the original type while checking compatibility:

```typescript
type Point = { x: number; y: number };

// `as`: Widens to Point, loses literal types
const p1 = { x: 0, y: 0 } as Point;
// p1.x is `number`

// `satisfies`: Validates as Point, preserves literals
const p2 = { x: 0, y: 0 } satisfies Point;
// p2.x is `0` (literal preserved)
// But p2 is still type-checked against Point
```

### Q11: What is `--rewriteRelativeImportExtensions`?

**A:** A TypeScript 5.5 flag that automatically rewrites `.ts` extensions to `.js` in
compiled output. This lets you write modern ESM-style imports with `.ts` extensions
while producing valid JavaScript output.

### Q12: How do variance annotations work in TypeScript 4.7+?

**A:** `out T` marks a type parameter as covariant (output-only), `in T` marks it as
contravariant (input-only), and `in out T` marks it as invariant. TypeScript enforces
that the actual usage matches the annotation, providing both documentation and compile-time
safety.
