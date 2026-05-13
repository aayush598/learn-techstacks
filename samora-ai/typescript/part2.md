# TypeScript Interview Questions and Answers - Part 2

## Q1: How does TypeScript's `module resolution` work?
**A:** TypeScript supports two module resolution strategies: `node` (classic Node.js resolution looking for `node_modules`, `package.json` `types`/`typings` fields, and extensionless imports) and `node16`/`nodenext` (modern Node.js ESM-aware resolution respecting `exports` maps in `package.json`, `type: "module"`, and `.mjs`/`.cjs` extensions). The `paths` and `baseUrl` options in `tsconfig.json` allow custom module resolution. `rootDirs` creates virtual directories. TypeScript also supports `self-referencing` (package importing itself via its own name) with `node16` resolution. The `exports` field in `package.json` controls which subpaths are publicly accessible, enabling deep import maps and conditional exports (different files for different environments).

## Q2: Explain TypeScript's `declaration merging` and its practical uses.
**A:** Declaration merging allows TypeScript to combine multiple declarations with the same name into a single definition. Types that support merging: interfaces (merge by adding properties), namespaces (merge by combining members), enums (merge by adding values), and namespace+class/function/enum merges. Interface merging enables extending third-party types (e.g., augmenting Express Request with custom properties: `declare global { namespace Express { interface Request { user?: User } } }`). Namespace merging with classes enables adding static members. Practical uses: augmenting library types, adding global augmentations for polyfills, extending Window/global types, and implementing module augmentation patterns.

## Q3: What are TypeScript's `branded types` and when should you use them?
**A:** Branded types (also called nominal types or opaque types) simulate nominal typing in TypeScript's structural type system by adding a unique brand property:

```typescript
type UserId = string & { readonly __brand: 'UserId' };
type ProductId = string & { readonly __brand: 'ProductId' };
```

Functions create branded values: `function createUserId(id: string): UserId { return id as UserId; }`. This prevents accidentally passing a `ProductId` where a `UserId` is expected, even though both are strings at runtime. Use cases: (1) preventing type confusion (mixing IDs, currencies, units), (2) entity identification in DDD, (3) opaque types for security (sanitized vs unsanitized strings), (4) units of measurement. Brands are compile-time only (no runtime overhead).

## Q4: How does TypeScript's `--strict` mode work and what flags does it enable?
**A:** `--strict` enables a set of type-checking flags for maximum safety: `strictNullChecks` (distinguish `null`/`undefined` from other types), `strictFunctionTypes` (contravariant function parameter checking), `strictBindCallApply` (proper `bind`/`call`/`apply` typing), `strictPropertyInitialization` (ensure class properties are initialized), `noImplicitAny` (error on inferred `any`), `noImplicitThis` (error on `this` with implicit `any`), `alwaysStrict` (emit `'use strict'`), `useUnknownInCatchVariables` (catch variables default to `unknown`). Each flag can be individually disabled. `--strict` is the recommended baseline for all projects. Many additional strictness flags exist outside `--strict`: `noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes`.

## Q5: Explain TypeScript's `infer` keyword in conditional types.
**A:** `infer` declares a type variable within a conditional type's extends clause to capture a type for later use:

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type Unpack<T> = T extends (infer U)[] ? U : T;
type PromiseValue<T> = T extends Promise<infer U> ? U : T;
```

`infer` can infer multiple types and has restrictions: (1) can only be used in conditional types, (2) must appear after `extends`, (3) can be used with `infer` in different positions (parameter types, return types, nested generics). Advanced uses: `infer` with `[infer First, ...infer Rest]` for tuple manipulation, inference from function arguments, and variadic tuple types (TypeScript 4.0+). Multiple `infer` positions can be used simultaneously for complex pattern matching.

## Q6: What are TypeScript's `variadic tuple types`?
**A:** Variadic tuple types (TypeScript 4.0+) use spread of generic type variables in tuples for flexible tuple operations:

```typescript
type Concatenate<T extends any[], U extends any[]> = [...T, ...U];
type Push<T extends any[], V> = [...T, V];
type Shift<T extends any[]> = T extends [infer First, ...infer Rest] ? Rest : [];
```

They enable: typed `Promise.all`, `pipe` functions with inferred argument types, curry with proper types, and dynamic tuple construction. Variadic tuples can use `rest` elements in any position (`[string, ...T[], number]`). TypeScript 4.7+ supports `...T` (spreading a generic) in tuple types. This enables full type-safe manipulation of function parameters and tuple structures.

## Q7: How does TypeScript's `module augmentation` work?
**A:** Module augmentation extends existing modules with additional declarations. Syntax uses `declare module 'module-name'`:

```typescript
import 'some-library'; // Import for side effects / module augmentation

declare module 'some-library' {
  interface ExistingInterface {
    newProperty: string;
  }
  function newFunction(): void;
}
```

Augmentations are merged with the original declarations. Requirements: (1) the augmenting file must be a module (has import/export), (2) the augmented module must be importable, (3) cannot add new top-level declarations that conflict with existing ones. Common uses: adding methods to Express Request/Response, extending Jest matchers, adding properties to React components, and patching third-party library types. Global augmentation (`declare global { ... }`) adds to the global scope across all modules.

## Q8: Explain TypeScript's `satisfies` operator.
**A:** The `satisfies` operator (TypeScript 4.9+) checks that a value's type matches a type without changing the inferred type. Unlike type annotation (`: Type`) which widens the type, `satisfies` retains the most specific inferred type for autocomplete and validation:

```typescript
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
} satisfies Record<string, string | RGB>;
// palette.red inferred as [255, 0, 0] (tuple), not string | RGB
```

Use cases: validating object shapes while preserving literal types, ensuring an expression meets a type constraint without type widening, validating that a value conforms to a union type while keeping the specific member type for discrimination. Unlike assertions (`as Type`), `satisfies` provides full type checking.

## Q9: What are TypeScript's `template literal types` and how do they enhance string typing?
**A:** Template literal types (TypeScript 4.1+) create new string literal types by concatenating:

```typescript
type EventName = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize<EventName>}`; // 'onClick' | 'onFocus' | 'onBlur'
type CSSProperty = 'background' | 'color' | 'margin';
type CSSValue = string | number;
type CSSDeclaration = `${CSSProperty}: ${CSSValue};`;
```

Built-in intrinsic types: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`. Template literals distribute over union constituents, creating all possible combinations. They're used for: typed event handlers, CSS property typing, route parameter inference (parsing `:id` from `/user/:id`), API endpoint typing, and Redux action type generation. Complex patterns use `infer` with template literals for compile-time string parsing.

## Q10: How does TypeScript's `--noUncheckedIndexedAccess` affect code?
**A:** `--noUncheckedIndexedAccess` (TypeScript 4.1+) adds `| undefined` to all indexed access operations (bracket notation). Without it: `obj[key]` preserves the value type. With it: `obj[key]` becomes `ValueType | undefined`. This forces null checking for all dictionary/array accesses, catching potential runtime errors. Arrays: `arr[0]` becomes `T | undefined`. Objects: `dict['key']` becomes `ValueType | undefined`. Mitigations: use `for...of` instead of indexed iteration, use `Map.get()` which already returns `| undefined`, use `Array.at()` for optional returns, use destructuring with defaults. This flag is recommended for strict null safety but can be verbose.

## Q11: Explain TypeScript's `decorators` and their type-safe usage.
**A:** TypeScript decorators are functions that modify classes, methods, accessors, properties, or parameters (experimental via `experimentalDecorators`). TypeScript 5.0+ implements the TC39 Stage 3 decorators proposal (standard ECMAScript decorators). Key differences: stage 3 decorators receive the decorated value and context object; experimental decorators receive different signatures. Type-safe decorators use generics:

```typescript
function log<This, Args extends any[], Return>(
  target: (this: This, ...args: Args) => Return,
  context: ClassMethodDecoratorContext<This, (this: This, ...args: Args) => Return>
) {
  return function(this: This, ...args: Args): Return {
    console.log(`Called ${context.name}`, args);
    return target.call(this, ...args);
  };
}
```

Stage 3 decorators provide better typing and don't require experimental flags.

## Q12: What are TypeScript's `intrinsic string manipulation types`?
**A:** Intrinsic string types (TypeScript 4.1+) are built-in compiler-level types that transform string literal types: `Uppercase<S>` converts to uppercase, `Lowercase<S>` to lowercase, `Capitalize<S>` capitalizes first character, `Uncapitalize<S>` lowercases first character. They operate at compile-time on literal string types and unions. Examples: `Uppercase<'hello'>` → `'HELLO'`, `Capitalize<'hello'>` → `'Hello'`. When used with union types, the transformation distributes: `Uppercase<'a' | 'b'>` → `'A' | 'B'`. These are implemented as compiler intrinsics (not expressible in TypeScript's type system) because they require character-level operations not possible with conditional types.

## Q13: How does TypeScript's `const type parameters` work?
**A:** `const` type parameters (TypeScript 5.0+) instruct the type system to infer the most specific type (literal type) rather than widening:

```typescript
function getConfig<const T extends readonly string[]>(items: T): T { return items; }
const config = getConfig(['a', 'b']); // Type: readonly ['a', 'b'], not string[]
```

Without `const`, array literals are inferred as `string[]`. With `const`, they're inferred as tuple types with literal elements. This is similar to `as const` on the argument but built into the type parameter. Use cases: configuration objects, event emitters with literal event names, typed routes, and any API where preserving the exact literal value matters. `const` type parameters can be used with objects, arrays, and primitive types.

## Q14: Explain TypeScript's `--exactOptionalPropertyTypes` flag.
**A:** `--exactOptionalPropertyTypes` (TypeScript 4.4+) changes how optional properties work. Without it: `interface Foo { bar?: string }` allows `bar` to be missing (`undefined`). With the flag: the property can be missing but cannot be explicitly set to `undefined` unless the type includes `undefined`: `interface Foo { bar?: string }` means `bar` can be `string` or absent, but NOT `undefined`. To allow `undefined`, use `bar?: string | undefined`. This catches bugs where `undefined` is accidentally assigned to optional properties. The flag is not included in `--strict` and must be explicitly enabled. It requires careful refactoring for existing codebases.

## Q15: What are TypeScript's `assertion functions`?
**A:** Assertion functions (TypeScript 3.7+) narrow types by asserting conditions:

```typescript
function assertString(value: unknown): asserts value is string {
  if (typeof value !== 'string') throw new Error('Not a string');
}
function assert(condition: any, msg?: string): asserts condition {
  if (!condition) throw new Error(msg);
}
```

The return type `asserts value is Type` tells TypeScript that after the function returns, the value is narrowed to that type. `asserts condition` asserts any condition. Assertion functions differ from type guards (which return `boolean` with `value is Type` return type) — they throw on failure instead of returning false. They're useful for: validation functions, API response checking, and defensive programming patterns that prefer throwing over returning booleans.

## Q16: How does TypeScript's `--isolatedModules` affect compilation?
**A:** `--isolatedModules` ensures each file can be transpiled independently (without cross-file type information). Required when using transpilers that process files individually (Babel, esbuild, SWC). Restrictions: (1) re-exports of types must use `export type`, (2) `const enum` members are inlined (not supported by isolated transpilers), (3) some re-export patterns are disallowed. With `--isolatedModules`, TypeScript treats each file as a separate module, not relying on the full program context. This enables faster builds with non-TSC transpilers. TypeScript 5.0+ made `--isolatedModules` compatible with more patterns and improved error messages.

## Q17: Explain TypeScript's ``--verbatimModuleSyntax``
**A:** `--verbatimModuleSyntax` (TypeScript 5.0+) controls how module syntax is emitted. When enabled: (1) `import type` and `export type` are preserved in the output, (2) regular `import`/`export` are not elided even if only used as types, (3) the flag enforces that all type-only imports/exports use `type` modifiers. This is required when using bundlers that rely on explicit type imports for tree-shaking (like with `verbatimModuleSyntax` in TypeScript's own docs). Without this flag, TypeScript might drop imports it determines are type-only. The flag makes type-only imports explicit, improving clarity and bundler compatibility.

## Q18: What are TypeScript's `enum` types and their runtime behavior?
**A:** TypeScript enums generate runtime JavaScript objects (except `const enum`). Numeric enums auto-increment values, string enums require explicit values. Enums support reverse mapping (numeric only — string enums don't). Heterogeneous enums (mix of string and numeric) are allowed but discouraged. `const enum` is completely inlined at compile time (no runtime object), but doesn't work with `--isolatedModules` or `--verbatimModuleSyntax`. Ambient enums (`declare enum`) exist only in type space. Enums are both types and values. Modern alternatives: union types of string literals (`type Status = 'active' | 'inactive'`) or `as const` objects. Enums should be used thoughtfully — they're a TypeScript-specific construct, not standard JavaScript.

## Q19: How does TypeScript's `--noPropertyAccessFromIndexSignature` work?
**A:** `--noPropertyAccessFromIndexSignature` (TypeScript 5.0+) disallows dot notation access on types with index signatures, forcing bracket notation:

```typescript
interface Dict {
  [key: string]: unknown;
}
const d: Dict = {};
d.foo; // Error: Property 'foo' comes from an index signature, use ['foo']
d['foo']; // OK
```

This prevents accidental property access where the property name is not known to exist. It's useful for dictionary types (`Record<string, T>`) where dot access might mask typos or unsafe access. With bracket notation, the developer consciously accesses through the index signature. Not included in `--strict`. Combined with `noUncheckedIndexedAccess`, it provides comprehensive index access safety.

## Q20: Explain TypeScript's `this parameter` in functions.
**A:** TypeScript allows declaring `this` as the first parameter of a function to specify the expected `this` type:

```typescript
function onClick(this: HTMLElement, event: MouseEvent) {
  this; // Type: HTMLElement
}
interface MyObj {
  data: string;
  method(this: MyObj, value: string): void;
}
```

The `this` parameter is removed at runtime (it's compile-time only). It's checked when called as a method — calling `onClick.call(div, event)` is fine; `onClick()` without proper `this` is an error. `this: void` means the function doesn't use `this`. `this: unknown` means any `this` is allowed. Class methods can use `this` parameter for polymorphic `this` typing (`method(this: this, ...)`). Arrow functions can't have `this` parameters (they capture `this` lexically).

## Q21: What are TypeScript's `import type` and `export type`?
**A:** `import type` (TypeScript 3.8+) imports only the type of a module, ensuring it's completely erased at runtime:

```typescript
import type { SomeInterface } from './module';
import { type SomeType, SomeClass } from './module';
```

`export type` does the same for exports: `export type { MyType }`. Benefits: faster compilation (isolated module support), explicit type-only dependencies, avoids circular dependency issues with runtime code, and helps bundlers tree-shake type-only imports. With `--verbatimModuleSyntax`, TypeScript enforces using `import type` for all type-only imports. The inline `import { type A, B }` syntax (TypeScript 4.5+) mixes type and value imports in one statement.

## Q22: How does TypeScript's `exhaustiveness checking` work?
**A:** Exhaustiveness checking ensures all cases of a union type are handled. The `never` type is used for this:

```typescript
type Shape = Circle | Square | Triangle;
function area(shape: Shape): number {
  if (shape.kind === 'circle') return Math.PI * shape.radius ** 2;
  if (shape.kind === 'square') return shape.side ** 2;
  return _exhaustiveCheck(shape);
}
function _exhaustiveCheck(x: never): never {
  throw new Error(`Unexpected: ${x}`);
}
```

If `Triangle` is added to the union but `area` isn't updated, a compile-time error occurs because `shape` (still `Triangle`) can't be assigned to `never`. This pattern catches missing cases at compile time. TypeScript 5.3+ can use `switch(true)` patterns for complex exhaustiveness checks.

## Q23: Explain TypeScript's `--preserveValueImports` option.
**A:** `--preserveValueImports` (TypeScript 4.0+) prevents TypeScript from eliding imports that appear unused in the source but are used in value positions. Normally, TypeScript removes unused imports. However, TypeScript might incorrectly determine an import is unused when it's actually used for side effects or values at runtime (e.g., importing a module that augments global types, or importing a class used only as a type but needed at runtime for `instanceof` checks). `--preserveValueImports` keeps all imports regardless of apparent usage. In TypeScript 5.0+, this is superseded by `--verbatimModuleSyntax` which also handles exports.

## Q24: What are TypeScript's `--strictNullChecks` and its impact on code?
**A:** `--strictNullChecks` makes `null` and `undefined` distinct types that are only assignable to themselves and `any`. Without it, `null` and `undefined` are assignable to any type, causing frequent runtime errors. With it: `string | null` must be handled explicitly via type guards, optional chaining, nullish coalescing, or assertions. This flag fundamentally changes how code is written: (1) forced null checks reduce NPEs significantly, (2) APIs must explicitly declare nullable returns, (3) refactoring is safer (new nullable returns are visible at compile time), (4) `?.`, `??`, `!` operators become essential tools. It's the single most impactful TypeScript configuration for code quality.

## Q25: How does TypeScript's `--paths` and `--baseUrl` work?
**A:** `baseUrl` sets the base directory for resolving non-relative module names. `paths` defines custom module resolution mappings relative to `baseUrl`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

This enables clean imports like `import { Button } from '@components/Button'`. Paths support wildcard patterns. Note: path aliases only affect TypeScript compilation — bundler (webpack, Vite, esbuild) or runtime (ts-node, tsx) needs equivalent configuration. The `rootDir` option controls output structure. Paths are useful for monorepos, clean import paths, and abstracting directory structure.

## Q26: What are TypeScript's `--outDir` and `--declarationDir` options?
**A:** `--outDir` specifies the output directory for compiled JavaScript files. `--declarationDir` separately controls where `.d.ts` declaration files are emitted (when `--declaration` or `--declarationMap` is enabled). Separating declaration output is useful for: (1) libraries that ship separate declaration files, (2) monorepo setups where declarations go to a different package, (3) organizing build output. When only `--outDir` is set, declarations are placed in corresponding subdirectories under `outDir`. With `--declarationDir`, declarations are in a parallel directory structure. `--declarationMap` generates `.d.ts.map` source maps for declaration files, enabling "Go to Definition" that points back to `.ts` source.

## Q27: Explain TypeScript's `--esModuleInterop` and its effects.
**A:** `--esModuleInterop` (TypeScript 2.7+) enables better interoperability between CommonJS and ES modules. It adds `__importDefault` and `__importStar` helpers that handle default imports from CommonJS modules. Without it: `import React from 'react'` might fail because CommonJS modules don't have a `default` export. With it: TypeScript adds `esModuleInterop: true` to wrap CommonJS modules to appear as ES modules with `default` exports. This allows `import React from 'react'` (instead of `import * as React from 'react'`). It also enables `--allowSyntheticDefaultImports`. Best practice: enable `esModuleInterop` for all projects to use standard ES module import syntax.

## Q28: How does TypeScript's `--strictFunctionTypes` affect function compatibility?
**A:** `--strictFunctionTypes` (TypeScript 2.6+) enables stricter checking of function parameter types (contravariance). Without it, function types are bivariant (parameters can be either wider or narrower). With it, function parameters are checked contravariantly — a function can only accept wider parameter types, not narrower. Example: `(x: Animal) => void` is assignable to `(x: Dog) => void` without strict mode, but not with it (because a function expecting `Animal` might not handle specific `Dog` behavior). This catches unsound patterns where callback functions could receive unexpected types. Method parameters are exempt (always bivariant) to preserve class hierarchy compatibility. Not included in `--strict` until TypeScript 2.6.

## Q29: What are TypeScript's `symbol types` and unique symbols?
**A:** `symbol` is a primitive type. TypeScript differentiates between `symbol` and `unique symbol` — the latter requires `const` declarations and `declare`:

```typescript
declare const FOO: unique symbol;
const BAR: unique symbol = Symbol('bar');
```

Unique symbols are nominal-like — each declaration creates a unique type that can't be assigned to another unique symbol type. They're used for: (1) well-known protocol keys (avoiding collisions), (2) branded types, (3) discriminated unions with symbols, (4) singletons and metadata keys. Unique symbols can't be created with `let` (must be `const` or `readonly`). `typeof symbolValue` preserves the unique symbol type. The `SymbolConstructor` type includes methods like `Symbol()` returning `symbol`.

## Q30: Explain TypeScript's `--isolatedDeclarations` and `--declaration`.
**A:** `--declaration` generates `.d.ts` files from `.ts` source. `--isolatedDeclarations` (TypeScript 5.5+) ensures declaration files can be generated without cross-file type information — each file's declaration is self-contained. This enables parallel declaration generation and supports tools like `ts-api-utils`. With `--isolatedDeclarations`, TypeScript requires explicit type annotations on exports (can't always infer types from runtime code alone). Benefits: (1) faster declaration generation, (2) enables new tools, (3) cleaner API contracts, (4) works well with bundlers that process files individually. It's designed for library authors who want fast, reliable `.d.ts` generation.

## Q31: How does TypeScript's `--noUnusedLocals` and `--noUnusedParameters` work?
**A:** `--noUnusedLocals` reports errors for local variables that are declared but never read. `--noUnusedParameters` does the same for function parameters. These flags catch dead code and improve code quality. Exceptions: (1) variables starting with `_` are exempt (common convention), (2) parameters in overridden methods, (3) destructured variables starting with `_`, (4) variables used only in type positions. The `_` prefix exemption follows the JavaScript convention for intentionally unused parameters. These flags are separate from `--strict` but highly recommended. `--noUnusedLocals` can add friction during development — some teams enable them only in CI.

## Q32: What are TypeScript's `--module` and `--moduleResolution` options?
**A:** `--module` specifies the module output format: `commonjs`, `es2015`/`es2020`/`es2022`/`esnext` (ES modules), `amd`, `umd`, `system`, `node16`/`nodenext` (aligns with Node.js module system). `--moduleResolution` determines how modules are resolved: `classic` (deprecated), `node` (Node.js-like resolution), `node16`/`nodenext` (modern Node.js ESM-aware resolution). The recommended modern approach: use `module: "node16"` or `module: "nodenext"` for Node.js projects, which automatically sets `moduleResolution` accordingly and respects `package.json` exports maps and `type: "module"`. For bundler targets: `module: "esnext"` with `moduleResolution: "bundler"` (TypeScript 5.0+).

## Q33: Explain TypeScript's `--resolveJsonModule`.
**A:** `--resolveJsonModule` (TypeScript 2.9+) allows importing `.json` files as modules:

```typescript
import config from './config.json';
// config is typed based on JSON content
```

With `resolveJsonModule`, TypeScript infers types from JSON structure (string → `string`, number → `number`, nested objects → nested types). For `"resolveJsonModule": true` to work, `--module` must be `commonjs`, `es2015`+, `node16`, or `nodenext`. `--esModuleInterop` affects whether default imports work cleanly. For enhanced JSON typing, combine with `--strictNullChecks`. JSON imports are read-only (the type is `as const`-like). This is particularly useful for configuration files, localization data, and static assets.

## Q34: How does TypeScript handle `circular dependencies` between types?
**A:** TypeScript handles circular type references gracefully at the type level but has limitations: (1) recursive types like `type TreeNode = { value: number; children: TreeNode[] }` work fine, (2) indirectly recursive conditional types might hit instantiation depth limits (`--noStrictGenericChecks`), (3) circular type aliases without object wrapping cause errors (`type X = X` — use `type X = { x: X }` instead). At the module level, circular imports between files can cause issues with type-only imports — use `import type` or inline imports to avoid runtime circular dependencies. TypeScript 5.0+ improved circular reference handling in conditional types.

## Q35: What are TypeScript's `readonly` and `Readonly<T>`?
**A:** `readonly` modifier prevents property reassignment after construction. `Readonly<T>` utility type makes all properties of `T` readonly. `readonly` affects the property, not the value — `readonly arr: number[]` prevents reassigning `arr` but not `arr.push(1)`. For deep immutability, combine with `as const` or use `DeepReadonly<T>` (custom or from libraries). `ReadonlyArray<T>` and `ReadonlyMap<K,V>` / `ReadonlySet<T>` provide read-only collection types. `readonly` in constructor parameter shorthand (`constructor(readonly name: string)`) creates and initializes a readonly property. TypeScript 4.0+ introduced variadic tuple types with `readonly [...T]`.

## Q36: Explain TypeScript's `--strictBindCallApply`.
**A:** `--strictBindCallApply` (TypeScript 3.2+) enables proper type checking of `Function.prototype.bind`, `call`, and `apply`:

```typescript
function add(a: number, b: number): number { return a + b; }
const add5 = add.bind(null, 5); // Type: (b: number) => number
add5(3); // OK: 8
add5('x'); // Error: Argument of type 'string' is not assignable to 'number'
```

Without this flag, `bind`/`call`/`apply` return `any`. With it, they correctly infer parameter and return types based on partial application. TypeScript also checks that `this` context is compatible. For functions with overloads, `bind`/`call`/`apply` preserve the overload signatures after partial application.

## Q37: What are TypeScript's `asserts` and `this is` return types?
**A:** These narrow types in specific ways: `asserts value is Type` (assertion functions — throw if wrong, narrow after return), `this is Type` (return type in class methods — narrows `this`):

```typescript
class Shape {
  constructor(public type: string) {}
  isCircle(): this is Circle {
    return this instanceof Circle;
  }
}
class Circle extends Shape {
  radius!: number;
}
declare const shape: Shape;
if (shape.isCircle()) {
  shape.radius; // OK: narrowed to Circle
}
```

`this is Type` works with `this` parameter for polymorphic narrowing, enabling discriminated unions without separate discriminant properties. The method must return a boolean. After the call, TypeScript narrows the instance type.

## Q38: How does TypeScript's `--emitDeclarationOnly` work?
**A:** `--emitDeclarationOnly` generates only `.d.ts` declaration files without JavaScript output. Useful when: (1) using a non-TSC transpiler (Babel, esbuild, SWC) for JS output, (2) publishing type declarations separately, (3) dual-package building (separate JS and type outputs), (4) monorepo setups where other packages need types during development. Combine with `--declaration` and `--declarationMap` for complete type generation. The `--outDir` option controls output location. When using this flag with `--declarationDir`, declarations can be directed to a specific output directory. Most library authors use this pattern with `tsc --emitDeclarationOnly` plus a bundler for JS.

## Q39: Explain TypeScript's `overloads` for functions and methods.
**A:** Function overloads provide multiple call signatures for a single implementation:

```typescript
function double(value: string): string;
function double(value: number): number;
function double(value: string | number): string | number {
  if (typeof value === 'string') return value + value;
  return value * 2;
}
double(5); // number
double('x'); // string
```

The implementation signature is not callable — only the overload signatures are. Overloads can differ by: parameter count, parameter types, return type, and type parameter constraints. Method overloads in classes work similarly. Overloads enhance API ergonomics for: functions accepting different input types, default parameter variations, and discriminated parameter patterns. Order overloads from most specific to least specific.

## Q40: What are TypeScript's `--downlevelIteration`?
**A:** `--downlevelIteration` (TypeScript 2.3+) enables proper iteration protocol support when targeting older ECMAScript versions (ES5/ES3). Without it, `for...of` on arrays is compiled to a simple `for` loop (works only for arrays and array-likes). With it, TypeScript emits code that checks for `Symbol.iterator`, enabling iteration over Map, Set, generators, and custom iterables when targeting older runtimes. The emitted code is larger and slower (calls `Symbol.iterator`, `.next()`, wrapping in try/finally). For modern targets (ES2015+), `downlevelIteration` is unnecessary. Use when supporting IE11 or similar while using `for...of` with non-array iterables.

## Q41: How does TypeScript's `--useDefineForClassFields` work?
**A:** `--useDefineForClassFields` (TypeScript 3.7+) controls how class fields are emitted. Without it (default for older targets): class fields use `this.field = value` assignment in the constructor. With it: class fields use `Object.defineProperty`, matching the ECMAScript class field semantics. This difference matters for subclasses — with `defineProperty`, the parent class field initialization runs before child class fields, and `defineProperty` creates non-enumerable properties (matching the spec). Issues arise when libraries expect specific behavior. TypeScript 5.0+ changed the default to align with the ECMAScript spec when targeting ES2022+. Key difference: overriding accessors in subclasses works correctly with `defineProperty`.

## Q42: Explain TypeScript's `--skipLibCheck`.
**A:** `--skipLibCheck` skips type checking of all `.d.ts` declaration files (both bundled with dependencies and project declarations). Benefits: (1) dramatically faster compilation (often 2-5x faster), (2) avoids errors from third-party type definitions with issues, (3) reduces memory usage. Drawbacks: (1) hidden type errors from library types, (2) type errors may surface at unexpected points due to unchecked library types. Best practice: use `skipLibCheck: true` for application projects (where third-party types are trusted), `skipLibCheck: false` for library projects (where type checking your own declarations is important). TypeScript 5.5+ improved the flag's behavior for better error localization.

## Q43: What are TypeScript's `--sourceMap` and `--inlineSourceMap`?
**A:** `--sourceMap` generates `.js.map` files alongside `.js` output, enabling browser/debugger mapping from compiled JS back to TS source. `--inlineSourceMap` embeds the source map as a base64 data URL in the `.js` file (no separate `.map` file). `--inlineSources` includes the original TypeScript source in the map file (used with `--sourceMap` or `--inlineSourceMap`). Source maps support: (1) debugging with breakpoints in `.ts` files, (2) error stack traces pointing to `.ts` locations, (3) code coverage tools. For production: consider `--sourceMap` for error reporting tools (Sentry, DataDog) but consider hiding source maps (server-side only) to protect source code. Source map files are typically served only in development.

## Q44: How does TypeScript's `--noEmit` and `--noEmitOnError` work?
**A:** `--noEmit` runs type checking only without generating output files. Used by: (1) IDEs and editors for type checking, (2) CI pipelines (with a separate build step), (3) ESLint with `@typescript-eslint` parser. `--noEmitOnError` suppresses output if there are type errors (default behavior in TypeScript 2.0+). Combining both (`--noEmit --noEmitOnError`) is unnecessary. `--noEmit` is common in test/check scripts: `"typecheck": "tsc --noEmit"`. This separates type checking from building. Some build tools run `tsc --noEmit` then a bundler, ensuring type safety before emitting optimized builds.

## Q45: Explain TypeScript's `declaration maps` (`--declarationMap`).
**A:** `--declarationMap` generates `.d.ts.map` source map files alongside `.d.ts` files. These map declaration file locations back to original `.ts` source locations. Benefits: (1) "Go to Definition" in editors navigates to the `.ts` source instead of `.d.ts`, (2) better debugging experience when using libraries, (3) documentation tooling can link to source code. Without declaration maps, users of your library see only the `.d.ts` interface — with them, they can jump directly to your implementation source. Publishing `.d.ts.map` with your library is recommended for public packages. Requires `--declaration` to be enabled.

## Q46: What are TypeScript's `--target` options and how do they affect output?
**A:** `--target` specifies the ECMAScript target version for output JavaScript. Options: `ES3`, `ES5`, `ES2015`/`ES6`, `ES2016`, ..., `ES2022`, `ESNext`. Higher targets: (1) produce cleaner, more idiomatic output (preserves `async/await`, generators, `class` syntax), (2) support more modern features natively, (3) are larger (don't include polyfills for missing features). Lower targets: (1) ensure compatibility with older runtimes, (2) require more transpilation code (async-to-generator, class transforms), (3) produce more verbose output. Modern projects targeting Node.js 18+ use `ES2022`. Browser projects use `ES2015`/`ES2016` for good coverage. `ESNext` uses the latest spec proposals (subject to change).

## Q47: How does TypeScript's `--jsx` option affect React development?
**A:** `--jsx` controls JSX output: `react` (legacy, calls `React.createElement`), `react-native` (preserves JSX for React Native), `react-jsx` (TypeScript 4.1+, uses `_jsx` runtime from `react/jsx-runtime` — automatic import, no need to import React in scope), `react-jsxdev` (development version with extra debugging), `preserve` (keeps JSX for another transpiler). `react-jsx` is the modern default (React 17+). `jsxFactory` and `jsxFragmentFactory` customize element creation (for Preact, Inferno). `jsxImportSource` (TypeScript 4.1+) specifies the JSX runtime package (e.g., `"jsxImportSource": "preact"`). `--module` must be compatible with the chosen JSX mode.

## Q48: Explain TypeScript's `--listFiles` and `--listEmittedFiles`.
**A:** `--listFiles` prints the list of all files TypeScript reads during compilation (source files, library declarations, `@types` packages). Useful for: debugging why certain files are included, understanding project resolution, and verifying `tsconfig.json` includes/excludes. `--listEmittedFiles` prints files that TypeScript writes (`.js`, `.d.ts`, `.js.map`). Useful for: verifying output structure, debugging directive trimming, and confirming declaration generation. Both are diagnostic tools, not typically used in production builds. Combine with `--explainFiles` (TypeScript 4.5+) for verbose file inclusion explanations showing why each file was loaded.

## Q49: What are TypeScript's `--traceResolution` and `--explainFiles`?
**A:** `--traceResolution` logs detailed module resolution steps for every import: search paths tried, resolved files, and resolution result. `--explainFiles` (TypeScript 4.5+) provides a cleaner explanation of why each file is included in the program. Both are debugging tools for understanding module and file inclusion. Use when: (1) imports resolve to unexpected files, (2) phantom type errors occur, (3) too many files are included, (4) type declarations conflict. `--explainFiles` output is more concise and readable than `--traceResolution`. Redirect output to a file: `tsc --explainFiles > explanation.txt`.

## Q50: How does TypeScript's `--diagnostics` and `--extendedDiagnostics` work?
**A:** `--diagnostics` prints compile-time performance diagnostics: total time, parse time, bind time, check time, emit time, and program memory usage. `--extendedDiagnostics` adds more granular performance statistics. Useful for: (1) optimizing compilation speed, (2) identifying slow files or types, (3) comparing `--skipLibCheck` vs full check performance, (4) tracking incremental compilation improvements with `--incremental`. Performance issues can often be traced to: complex conditional types, deep generic recursion, large union types, and excessive type instantiation. These flags help identify bottlenecks for optimization.

## Q51: Explain TypeScript's `composite projects` and project references.
**A:** Project references (TypeScript 3.0+) split a large codebase into smaller, independently buildable projects. Each project has a `composite: true` tsconfig. Root project references sub-projects:

```json
{
  "references": [
    { "path": "./shared" },
    { "path": "./server" },
    { "path": "./client" }
  ]
}
```

Benefits: (1) faster incremental builds (only rebuild changed projects), (2) clear dependency boundaries, (3) smaller compilation units, (4) good monorepo support. `--build` flag builds projects and their dependencies. `--dry` shows what would be built. `--clean` cleans output. Each referenced project must have `composite: true`, which enables `declaration` and `declarationMap` by default. Project references work best with module-based code organization.

## Q52: What are TypeScript's `--incremental` and `--tsBuildInfoFile`?
**A:** `--incremental` (TypeScript 3.4+) enables incremental compilation, saving information about the previous compilation in a `.tsbuildinfo` file. On subsequent builds, TypeScript reuses this information to skip re-checking and re-emitting unchanged files. `--tsBuildInfoFile` specifies the output path for the build info file (default: `.tsbuildinfo` in the output directory). Incremental compilation significantly reduces build times in development. The build info file tracks: file hashes, emit status, and dependency graph. Deleting the build info file triggers a full rebuild. Not compatible with all projects (especially those using `--isolatedModules` with non-TSC transpilers).

## Q53: How does TypeScript handle `--outFile` for concatenated output?
**A:** `--outFile` concatenates all output into a single JavaScript file. Only works with `module: "system"`, `module: "amd"`, or `module: "none"`. Used for browser applications without a module loader. Cannot be used with `module: "commonjs"`, `module: "es2015"`+, or `moduleResolution: "node16"`. `--outFile` with `--declaration` creates a single `.d.ts` file. This is legacy functionality — modern projects use bundlers (webpack, Rollup, esbuild) instead. `--outFile` doesn't perform tree-shaking or dead code elimination. For library development, separate files per module is preferred. With ES module bundlers, `outFile` is essentially obsolete.

## Q54: Explain TypeScript's `--lib` option.
**A:** `--lib` specifies which built-in type definitions to include (DOM, ES features, etc.). Without it, TypeScript includes default libraries based on `--target`. Common libraries: `es5`, `es2015`, `es2015.promise`, `es2015.iterable`, `es2016.array.include`, `es2017.object`, `es2017.string`, `es2017.typedarrays`, `es2018.asynciterable`, `es2019.array`, `es2020.bigint`, `es2020.promise`, `es2020.string`, `es2020.symbol.wellknown`, `es2021.promise`, `es2021.string`, `es2021.weakref`, `es2022.array`, `es2022.error`, `es2022.object`, `es2022.sharedmemory`, `es2022.string`, `esnext`, `dom`, `dom.iterable`, `webworker.importscripts`, `scripthost`. Use `"lib": ["es2022", "dom", "dom.iterable"]` for a full modern setup. Excluding the `dom` lib is useful for non-browser environments (Node.js, Workers).

## Q55: What are TypeScript's `--charset` and `--pretty` options?
**A:** `--charset` (deprecated) specified input file encoding. Modern TypeScript (4.x+) assumes UTF-8 for all files. `--pretty` (default: true in most setups) formats error messages with color and context:

```
src/index.ts:5:3 - error TS2322: Type 'string' is not assignable to type 'number'.

5   const x: number = 'hello';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
```

With `--pretty false`, errors are single-line without formatting. Pretty errors are more readable in terminal output. For CI or machine parsing, `--pretty false` produces cleaner output. The `--noErrorTruncation` option (not in `--pretty`) prevents TypeScript from truncating long error messages, useful for deeply nested generic types.

## Q56: How does TypeScript's `--strictPropertyInitialization` work?
**A:** `--strictPropertyInitialization` ensures all class properties are initialized in the constructor or with a field initializer:

```typescript
class User {
  name: string; // Error if not initialized
  age!: number; // Assertion: initialized externally
  email?: string; // Optional: undefined is fine
  role = 'user'; // Initialized inline
}
```

The definite assignment assertion (`!`) tells TypeScript the property will be initialized elsewhere (e.g., by a framework or dependency injection). The `_` prefix convention doesn't apply here — use `!` for external initialization. Common patterns: `constructor(private readonly injected: SomeService)` (parameter property shorthand), `@inject decorator` (Angular/nestjs), `declare` modifier for properties initialized externally. This flag catches common bugs where properties are accessed before initialization.

## Q57: Explain TypeScript's `--noImplicitReturns`.
**A:** `--noImplicitReturns` (TypeScript 2.0+) requires all code paths in a function to explicitly return a value if the return type is not `void`:

```typescript
function getValue(n: number): string {
  if (n > 0) return 'positive';
  if (n < 0) return 'negative';
  // Error: Not all code paths return a value
}
```

This catches subtle bugs where a conditional branch falls through without returning. It applies to all functions with explicit or inferred return types. The flag doesn't require `return undefined` explicitly — `return;` with `undefined` return type is fine. Not included in `--strict` but highly recommended. Combined with `--noImplicitReturns`, you get exhaustiveness checking for conditional logic.

## Q58: What are TypeScript's `--noFallthroughCasesInSwitch`?
**A:** `--noFallthroughCasesInSwitch` (TypeScript 2.0+) reports errors for fall-through cases in `switch` statements (cases that don't end with `break`, `return`, `throw`, or `continue`):

```typescript
switch (x) {
  case 1:
    console.log('one');
    // Error: Fallthrough case in switch
  case 2:
    console.log('two');
    break; // OK
}
```

Intentional fall-through requires a comment or explicit `// falls through` to suppress the error. This catches one of the most common JavaScript bugs. TypeScript also flags cases that fall through to a `default` case. The flag is not included in `--strict`. When combined with exhaustiveness checking, switch statements become very robust.

## Q59: How does TypeScript's `--forceConsistentCasingInFileNames` work?
**A:** `--forceConsistentCasingInFileNames` ensures that import paths match the actual file casing on disk. On case-insensitive file systems (macOS, Windows), imports with wrong casing work but break on case-sensitive systems (Linux, CI). This flag catches discrepancies during development, preventing CI failures. Example: `import { User } from './User'` when the file is `./user.ts` would be flagged. The check applies to all module resolutions — relative imports, `@types` packages, and `node_modules`. Enabled by default in `--strict` setups. In monorepos or cross-platform teams, this flag is essential for preventing case-sensitivity bugs.

## Q60: Explain TypeScript's `--keyofStringsOnly` and `--keyofStringsOnly` (deprecated).
**A:** `--keyofStringsOnly` (deprecated in TypeScript 2.9+, removed in 5.0+) restricted `keyof` to return only string keys, excluding symbol keys. Before TypeScript 2.9, `keyof T` returned `string` for index signatures. TypeScript 2.9+ added symbol key support to `keyof`. This flag allowed opting out of symbol key support for backward compatibility. Modern TypeScript always includes symbol keys in `keyof`. Code depending solely on string-key typing should use `Extract<keyof T, string>` for explicit string-only key constraints. The symbol key inclusion in `keyof` affects mapped types, conditional types, and generic constraints.

## Q61: What are TypeScript's `--preserveConstEnums` and `--removeComments`?
**A:** `--preserveConstEnums` prevents `const enum` inlining, keeping the runtime enum object. Without it, `const enum` members are inlined at usage sites. With it, the enum object is emitted even though TypeScript can inline values. Useful when: (1) runtime reflection on the enum is needed, (2) debugging in environments that can't inline, (3) the enum is consumed by non-TypeScript code via the enum object. `--removeComments` strips comments from output. By default, TypeScript preserves comments (except those on JSX expressions and some internal comments). For production builds, `--removeComments` reduces file size. For library development, consider keeping comments for consumers.

## Q62: How does TypeScript's `--noImplicitUseStrict` work?
**A:** `--noImplicitUseStrict` (deprecated in modern versions) prevents TypeScript from emitting `"use strict"` at the top of output files. Without this flag, TypeScript always emits `"use strict"` when targeting ES modules or with `alwaysStrict: true`. Useful when: (1) the output is consumed by systems that handle strict mode themselves, (2) concatenating scripts where `"use strict"` at file level affects following code, (3) targeting CommonJS modules that don't want strict mode. Modern TypeScript has `alwaysStrict` (set by `--strict`) which overrides `noImplicitUseStrict`. In practice, always emitting strict mode is recommended for new projects.

## Q63: Explain TypeScript's `--suppressExcessPropertyErrors` and `--suppressImplicitAnyIndexErrors`.
**A:** Both are legacy options (deprecated) from older TypeScript versions. `--suppressExcessPropertyErrors` disabled errors for "excess properties" in object literals (e.g., passing `{a: 1, b: 2}` to a function expecting `{a: number}`). This is now always checked. `--suppressImplicitAnyIndexErrors` suppressed errors when accessing properties via index on types without index signatures. Superseded by `--noImplicitAny`. These options existed before TypeScript reached full maturity. Modern TypeScript doesn't support them. Code previously relying on these flags should add explicit type annotations.

## Q64: What are TypeScript's `--allowUmdGlobalAccess`?
**A:** `--allowUmdGlobalAccess` (TypeScript 3.5+) allows accessing UMD module exports as globals from module files. Without it, UMD modules can only be imported (can't be used as globals from within modules). With it, variables exported by UMD modules (like `React`, `jQuery`) can be referenced globally even from module files. This is useful for: (1) migrating legacy code from script to module format, (2) hybrid projects with both scripts and modules, (3) quick prototyping. For new projects, prefer explicit imports over global access. The flag doesn't affect non-module files (where global access is always allowed). TypeScript's global augmentation (`declare global`) is the recommended alternative.

## Q65: How does TypeScript's `--allowUmdGlobalAccess` relate to ambient declarations?
**A:** `--allowUmdGlobalAccess` works alongside `declare` statements. UMD library type definitions typically use `export as namespace` to declare the global name. When the flag is enabled, TypeScript allows module code to reference these global names directly without imports. Without the flag, module code must use `import` statements even though the UMD library is also available globally. The flag is a convenience for working with mixed globals-and-modules codebases. For proper modern code, import everything explicitly. This flag is most useful during incremental migration from script-style (global references) to module-style code.

## Q66: Explain TypeScript's `--charset` output handling (deprecated).
**A:** Previously, `--charset` controlled the encoding of output files (default: `utf8`). Modern TypeScript always outputs UTF-8 (standard for JavaScript). Other encodings (like `ascii` or `iso-8859-1`) were sometimes needed for legacy systems. The option was removed because: (1) modern ecosystems handle UTF-8 natively, (2) JavaScript engines require UTF-16 internally, (3) source maps require UTF-8, (4) the option caused confusion. Source files are expected to be UTF-8. BOM (Byte Order Mark) is not processed — files should be UTF-8 without BOM. For consuming non-UTF-8 sources, convert files before TypeScript processing.

## Q67: What are TypeScript's `--emitBOM` and `--newLine`?
**A:** `--emitBOM` adds a UTF-8 Byte Order Mark (BOM) at the beginning of output files. Rarely needed — some legacy tools require BOM for UTF-8 detection. `--newLine` specifies line ending in output: `CRLF` (Windows: `\r\n`) or `LF` (Unix: `\n`). The default is platform-specific. For cross-platform consistency: (1) library authors often set `"newLine": "LF"` for consistent file hashes, (2) Windows projects might use `"CRLF"`, (3) `git` configuration (`core.autocrlf`) affects how line endings are stored. Consistent `--newLine` prevents false-positive change detection in version control. Modern editors and tools handle both line ending styles transparently.

## Q68: How does TypeScript's `--stripInternal` work?
**A:** `--stripInternal` removes declarations marked with `/** @internal */` JSDoc from the generated `.d.ts` files. This allows hiding internal API surface from public type declarations. When combined with `--declaration`, TypeScript excludes `@internal`-annotated exports from the output declarations. Limitations: (1) only works with `--declaration`, (2) the symbol must have a `/** @internal */` JSDoc tag, (3) doesn't prevent runtime access (JS consumers can still use the API), (4) not enforced at type-check time within the project. Modern alternatives: use `@internal` with API extractor tools (Microsoft's `api-extractor`), or restructure code to physically separate internal and public modules.

## Q69: Explain TypeScript's `--showConfig` and `--generateCpuProfile`.
**A:** `--showConfig` (TypeScript 4.1+) prints the effective `tsconfig.json` after resolution (combining CLI options, config file, and extends). Useful for debugging configuration inheritance and verifying options. `--generateCpuProfile` (TypeScript 4.1+) generates a CPU profile during compilation, saved as `tsc.cpuprofile` (or custom path). Analyze with Chrome DevTools or VS Code. Helps identify performance bottlenecks in TypeScript's compilation. Usage: `tsc --generateCpuProfile profile.cpuprofile`. Both are diagnostic tools. Profile size grows with project size. The `--generateTrace` option generates Chrome trace files for analyzing compilation dependency graphs.

## Q70: What are TypeScript's `--strictBuiltinIteratorReturn`?
**A:** `--strictBuiltinIteratorReturn` (TypeScript 5.5+) improves typing of `Iterator` return values. Built-in iterators (like `Array` iterator) have `return(value)` method that may be called. This flag enables proper typing of these return values in `Iterator` protocol types. It ensures that `IteratorResult<T, TReturn>` accurately reflects the `return` method's behavior. This affects: (1) `for...of` with `break`/`return`, (2) generator functions with `return(value)`, (3) custom iterators implementing `return()`. The flag is part of TypeScript's ongoing work to improve iterator type safety.

## Q71: How does TypeScript's `--watch` mode work?
**A:** `--watch` runs TypeScript in file-watching mode, recompiling when files change. TypeScript uses efficient file watching (fsevents on macOS, inotify on Linux, polling for some CI environments). `--watchDirectory` controls directory watching strategy. `--preserveWatchOutput` prevents clearing the terminal between compilations. Watcher triggers on: file saves, file creation, file deletion, and config file changes. TypeScript's watcher is smart — it knows about project references and rebuilds the minimal set. Performance: initial compilation is full; subsequent compilations use `--incremental` (if enabled). For large projects, `tsc --noEmit --watch` provides fast type-checking-only feedback without emitting files.

## Q72: Explain TypeScript's `--assumeChangesOnlyAffectDirectDependencies`.
**A:** `--assumeChangesOnlyAffectDirectDependencies` (TypeScript 3.8+) is a performance optimization for `--watch` mode. When enabled, TypeScript skips type-checking files beyond those directly affected by a change. This can significantly speed up watch-mode compilation in large projects when a change only affects immediate consumers. Risk: this flag can result in incomplete error detection — a change might indirectly affect types in distant files. Best used in: (1) large projects with many files, (2) development workflows where quick feedback matters more than exhaustive checking, (3) CI runs with full checking. Combine with `--incremental` for maximum watch-mode performance.

## Q73: What are TypeScript's `--typeRoots` and `--types`?
**A:** `--typeRoots` specifies directories where TypeScript looks for type definitions (default: `node_modules/@types`). `--types` restricts which `@types` packages are auto-included — only listed packages are loaded. Without `--types`, all visible `@types` packages are included. `--typeRoots` is useful for: (1) monorepos with custom type locations, (2) strict control over type definition sources, (3) isolating type definitions from global `@types`. `--types` prevents type pollution from unnecessary `@types` packages. Both options are commonly used in library projects. Application projects often rely on defaults. If you set `typeRoots`, always include `node_modules/@types` if you need any third-party types.

## Q74: How does TypeScript's `--noResolve` work?
**A:** `--noResolve` (rarely used) instructs TypeScript not to automatically resolve referenced files beyond those explicitly listed in the command line input. Without it, TypeScript resolves all `/// <reference>` directives and imports. With it, only explicitly provided files are included. This is a legacy option useful for: (1) debugging file inclusion, (2) integration with specific build systems that manage file lists, (3) restricting compilation to a specific set of files. Modern TypeScript projects don't use `--noResolve` — let TypeScript resolve dependencies automatically. The flag doesn't affect module resolution — only file resolution (`/// <reference>` and `--files`).

## Q75: Explain TypeScript's `--emitDecoratorMetadata`.
**A:** `--emitDecoratorMetadata` (TypeScript 2.5+) generates type metadata for decorators, used by dependency injection frameworks (Angular, NestJS, Inversify). When enabled, TypeScript emits `design:type`, `design:paramtypes`, and `design:returntype` metadata for decorated members. This metadata allows frameworks to determine types at runtime. Requires `experimentalDecorators: true`. Limitations: (1) doesn't work with TypeScript's stage 3 decorators, (2) relies on experimental decorators, (3) can't handle complex generic types, (4) increases bundle size. Frameworks like Angular require this flag. For NestJS, `emitDecoratorMetadata` is optional — many teams prefer explicit `@Inject()` decorators.

## Q76: What are TypeScript's `--importHelpers` and `--noEmitHelpers`?
**A:** `--importHelpers` (TypeScript 2.1+) imports helper functions from `tslib` instead of inlining them. Without it, TypeScript inlines helpers like `__extends`, `__assign`, `__awaiter` in every file. With it, TypeScript imports them from `tslib` — reducing output size significantly (especially with many files). Requires `tslib` as a runtime dependency. `--noEmitHelpers` suppresses all helper emission (useful if helpers are provided by another source). `--importHelpers` is recommended for: (1) library authors (smaller bundle), (2) projects targeting multiple modules, (3) production builds. Development builds can skip `importHelpers` for simplicity. `tslib` versions should match TypeScript version.

## Q77: How does TypeScript's `--keyof` and `--noStrictGenerics` work?
**A:** `--keyof` (TypeScript 4.7+) improved how `keyof` works with index signatures. `--noStrictGenericChecks` (removed in TypeScript 5.0) disabled strict generic variance checks. Modern TypeScript doesn't support `--noStrictGenericChecks` — all generics are variance-checked. TypeScript's generic variance is automatically inferred: (1) readonly positions → covariant, (2) regular positions → invariant, (3) method parameters → bivariant (without `--strictFunctionTypes`). The compiler determines if a generic parameter is used in covariant, contravariant, or invariant positions. Variance checking ensures sound generic types. Complex variance scenarios might require explicit annotations.

## Q78: Explain TypeScript's `--reactNamespace` (legacy).
**A:** `--reactNamespace` (deprecated, replaced by `--jsxFactory`) specified the JSX factory function name for the old `react` JSX mode. Default: `React`. Changed when using alternative JSX libraries (Preact: `h`, Inferno: `createElement`). Replaced by `--jsxFactory` in TypeScript 2.2 and completely superseded by `--jsxImportSource` in TypeScript 4.1. Modern code uses `"jsx": "react-jsx"` with `"jsxImportSource": "preact"` instead. The `--reactNamespace` option exists only for backward compatibility with ancient TypeScript configurations. All new projects should use modern JSX transform settings.

## Q79: What are TypeScript's `--noErrorTruncation`?
**A:** `--noErrorTruncation` prevents TypeScript from truncating long error messages. Without it, TypeScript shortens deeply nested type expressions with `...` (especially in generic types, conditional types, and mapped types). With it, the full type expression is displayed. Useful for: (1) debugging complex generic types, (2) understanding detailed type relationships, (3) reporting accurate type information in bug reports. The output can be extremely verbose for deeply nested types. Pipe through `less` or redirect to a file. Combined with `--pretty false` for machine-readable full type information.

## Q80: How does TypeScript's `--traceResolution` help debug imports?
**A:** `--traceResolution` prints every module resolution attempt in detail: (1) the import path, (2) the containing file, (3) each resolution strategy tried (Node, Classic), (4) the paths attempted for each strategy, (5) whether each path resolved or failed, (6) the final resolved path or failure reason. Troubleshooting patterns: (1) wrong module resolution → check `moduleResolution` setting, (2) file not found → check `paths`, `baseUrl`, and directory structure, (3) wrong version selected → check `types`, `typeRoots`, `maxNodeModuleJsDepth`, (4) resolution unexpected → check `node_modules` layout. `--traceResolution` output is verbose — always redirect to a file.

## Q81: Explain TypeScript's `--version` and `--init` flags.
**A:** `--version` prints the TypeScript compiler version. `--init` (TypeScript 2.0+) creates a `tsconfig.json` with default settings. The generated config includes: `target: "es2016"`, `module: "commonjs"`, `strict: true`, `esModuleInterop: true`, `skipLibCheck: true`, `forceConsistentCasingInFileNames: true`. The defaults vary by TypeScript version — modern `--init` generates more complete configs. After `--init`, customize for your project: change `target` (ES2022+ for Node 18+), adjust `module` (`node16` for modern Node ESM), set `outDir`, add `include`/`exclude` patterns, and configure `paths`. `--init` is a quick starter but generated config isn't optimal for all projects.

## Q82: What are TypeScript's `--build` and `--dry` flags?
**A:** `--build` (TypeScript 3.0+) builds a project and its project references, respecting dependency order. Flags: `--clean` deletes all project build outputs, `--dry` shows what would be built without actually building, `--force` rebuilds all projects regardless of changes, `--verbose` provides detailed build output. `--build` is designed for monorepos with project references. Without project references, `--build` behaves like regular compilation. `--dry` is useful for CI pipelines to preview changes. `--clean` must be used carefully — it removes the entire `outDir` for each referenced project. `--build` with `--incremental` is the most efficient way to compile large multi-project repositories.

## Q83: How does TypeScript's `--preserveSymlinks` work?
**A:** `--preserveSymlinks` (TypeScript 2.1+) mirrors Node.js's `--preserve-symlinks` option. Without it, TypeScript resolves symlinks to their real path, leading to: (1) `require.resolve` returning the real path, (2) type resolution using the real path. With it, TypeScript preserves the symlinked path, enabling: (1) correct resolution when packages are linked (pnpm, yarn workspaces, `npm link`), (2) avoiding duplicate module instances from linked packages, (3) working with symlinked monorepo packages. The flag affects both module resolution and source file resolution. Necessary for pnpm users (uses symlinked `node_modules`). Without this flag, pnpm users might get duplicate type definitions.

## Q84: Explain TypeScript's `--maxNodeModuleJsDepth`.
**A:** `--maxNodeModuleJsDepth` (TypeScript 2.4+) controls how deep TypeScript checks JavaScript files (`.js`) inside `node_modules`. Default: 0 (don't check JS in node_modules). Increasing this value enables type checking deeper layers of JavaScript dependencies. Useful when: (1) using JS libraries without type definitions, (2) gradual migration from JS to TS, (3) understanding JS library types for type inference. Risk: can significantly increase compilation time and memory. Alternative: create `.d.ts` files for critical dependencies. For JS libraries, consider using `allowJs` with `checkJs` and `maxNodeModuleJsDepth`.

## Q85: What are TypeScript's `--allowJs` and `--checkJs`?
**A:** `--allowJs` allows JavaScript files to be part of a TypeScript project, enabling: (1) mixed JS/TS projects, (2) gradual migration from JS to TS, (3) importing JS modules with type inference. `--checkJs` adds type checking for `.js` files (requires `--allowJs`). JS files are checked using JSDoc type annotations and type inference. `// @ts-nocheck` disables checking per file. `// @ts-expect-error` suppresses specific errors. JS checking is less strict than TS (no implicit any in `--noImplicitAny` for JS). Combine with `--maxNodeModuleJsDepth` for deeper JS checking. Essential for incremental migration projects.

## Q86: How does TypeScript's `--outDir` and `--rootDir` interact?
**A:** `--rootDir` sets the root directory for input files. TypeScript computes the output structure by stripping `rootDir` from the source path and prepending `--outDir`. Example: `rootDir: "src"`, `outDir: "dist"`, file `src/components/Button.ts` → `dist/components/Button.js`. If `rootDir` is not set, TypeScript computes it as the common root of all input files. Mismatched `rootDir` can cause: (1) unexpected output structure, (2) "all inputs must share a common rootDir" errors. Best practice: explicitly set `rootDir` (often `"."` or `"src"`) and `outDir` (`"dist"`). For libraries, `declarationDir` can be separate from `outDir`.

## Q87: Explain TypeScript's `--declaration` and `--declarationMap` relationship.
**A:** `--declaration` generates `.d.ts` files. `--declarationMap` generates `.d.ts.map` files. Declaration maps work like source maps for declarations, mapping `.d.ts` positions back to original `.ts` source. Benefits: (1) editors can "Go to Definition" to original TS source, (2) error stacks reference original types, (3) documentation tools show source types. Both require `--declaration` for `--declarationMap` to work. `--declarationDir` separates declarations from JS output. For library publishing: always include `--declaration` and `--declarationMap`. Without declaration maps, consumers see only the `.d.ts` interface, not the source. With them, IDE navigation flows naturally to the implementation.

## Q88: What are TypeScript's `--composite` and related options?
**A:** `--composite` (TypeScript 3.0+) enables project references mode: (1) sets `--declaration` and `--declarationMap` automatically, (2) requires `rootDir`, (3) enables incremental compilation, (4) creates a `.tsbuildinfo` file. Composite projects are designed to be referenced by other projects via project references. A composite project must have its outputs in a deterministic location. `--composite` is just for project references — regular TS projects don't need it. The `--build` mode uses composite projects for its dependency graph. For monorepo libraries, each library should be a composite project. Related: `--tsBuildInfoFile` controls build info output location.

## Q89: How does TypeScript's `--disableReferencedProjectLoad` work?
**A:** `--disableReferencedProjectLoad` (TypeScript 4.0+) prevents TypeScript from automatically loading referenced composite projects. When in `--build` mode, TypeScript normally loads all project references. This flag disables that, useful for: (1) reducing startup time when TypeScript is used for editing/checking, not building, (2) avoiding loading unnecessary projects, (3) fixing issues with circular project references. Only affects `--build` mode. For editing, use `--noEmit` with `--disableReferencedProjectLoad` for faster feedback. The flag is a performance optimization for large monorepos.

## Q90: Explain TypeScript's `--disableSizeLimit`.
**A:** `--disableSizeLimit` removes TypeScript's internal source size limit (default: 4MB per file). Large generated files (like database migrations, localization files) can exceed this limit. The flag allows processing such files. Before using this flag: (1) consider breaking the large file into smaller modules, (2) verify the file isn't accidentally duplicated, (3) ensure the file doesn't cause memory issues. The size limit exists to prevent out-of-memory crashes on TypeScript's parser. Disabling it can cause the compiler to use excessive memory. Used primarily by database schema generators and localization file tools.

## Q91: What are TypeScript's `--listFilesOnly` and `--print`?
**A:** `--listFilesOnly` (TypeScript 4.2+) prints the files that would be compiled without actually compiling. Similar to `--listFiles` but doesn't compile. Useful for debugging include/exclude patterns. `--print` (TypeScript 5.3+) prints the output file to stdout instead of writing to disk. Used for: (1) inspecting compilation output, (2) piping output to other tools, (3) debugging transformations. `--print FILE` prints a specific file's output. Both are diagnostic tools for understanding TypeScript's file handling and output generation.

## Q92: How does TypeScript's `--explainFiles` output differ from `--traceResolution`?
**A:** `--explainFiles` (TypeScript 4.5+) provides a tree showing why each file is included in the program: (1) entry points (from tsconfig `include`/`files`), (2) `/// <reference>` directives, (3) import dependencies, (4) `@types` packages, (5) lib references. `--traceResolution` focuses on module resolution (how import paths map to files). `--explainFiles` is broader (why files are in the program), `--traceResolution` is narrower (how specific imports resolve). For most debugging, `--explainFiles` is more useful. Example output format:

```
src/index.ts
  Entry point of module resolution
  src/app.ts
    Imported by src/index.ts
  node_modules/@types/react/index.d.ts
    Lib reference 'dom'
```

## Q93: What are TypeScript's type-only `import()` types and `module` declarations?
**A:** TypeScript supports `import()` type syntax (import types) for inline type references: `type Fn = import('./types').MyFn`. Module declarations (`declare module 'module'`) declare the shape of external modules without actual implementations:

```typescript
declare module '*.svg' {
  const content: string;
  export default content;
}
```

Module declarations can be: (1) ambient module declarations (declare existing modules), (2) wildcard declarations (`'*.svg'`, `'*.css'`), (3) augment existing modules (merging). Path mapping and module declarations together enable typed imports for non-JS assets. Import types are useful for avoiding circular dependencies — import the type inline without importing the module.

## Q94: Explain TypeScript's `--strict` and `--alwaysStrict`.
**A:** `--strict` enables a bundle of strict checking flags (see Q4). `--alwaysStrict` always emits `'use strict'` at the top of output files (regardless of target or module settings). Without `--alwaysStrict`, TypeScript emits `'use strict'` based on target and module settings (e.g., ESM always has strict). `--alwaysStrict` ensures all output files run in strict mode, catching: (1) assignment to undeclared variables, (2) `this` being `undefined` in functions, (3) `with` statement errors, (4) `arguments.callee` errors, (5) duplicate property names. `--alwaysStrict` is included in `--strict`. The flag is set automatically for ESM and when using decorators.

## Q95: How does TypeScript's `--noLib` work?
**A:** `--noLib` disables automatic inclusion of the default lib declaration files (the built-in type definitions for ECMAScript, DOM, etc.). With this flag, `Promise`, `Array`, `Object`, and all other built-ins have no type definitions. Use cases: (1) extremely constrained environments (no ES features), (2) custom runtime with non-standard APIs, (3) library compatibility testing, (4) embedding TypeScript in a unique environment. Without libs, you must provide all type declarations yourself. This is rarely used — most projects include appropriate libs via `--lib`. TypeScript's `--target` sets default libs; `--noLib` overrides this entirely.

## Q96: What are TypeScript's `--moduleDetection` options?
**A:** `--moduleDetection` (TypeScript 5.0+) controls how TypeScript determines if a file is a module: `auto` (default, checks for `import`/`export`), `legacy` (pre-5.0 behavior with some edge cases), `force` (treats all files as modules). Module detection affects: (1) whether variables are in module scope or global scope, (2) whether `declare global` is needed, (3) how `this` at top level is typed. `force` is useful for: (1) ensuring consistent module behavior, (2) preventing accidental global scope pollution, (3) strict codebase conventions. `auto` is best for mixed codebases. Modern TypeScript recommends explicit module handling.

## Q97: How does TypeScript's `--customConditions` work?
**A:** `--customConditions` (TypeScript 4.7+) adds custom conditions to the module resolution algorithm, matching the `exports` field in `package.json`. Example: `"customConditions": ["development"]` allows resolving conditions like:

```json
{
  "exports": {
    ".": {
      "development": "./src/index.dev.js",
      "default": "./dist/index.js"
    }
  }
}
```

Useful for: (1) differentiating dev/prod builds, (2) browser-specific exports, (3) platform-specific code, (4) feature flags. Multiple conditions are tried in order. Conditions are additive — they don't replace the standard conditions. Available in TypeScript 4.7+ with `node16`/`nodenext` module resolution. Works with bundlers that support custom conditions (webpack, Vite, esbuild).

## Q98: Explain TypeScript's `--ignoreDeprecations`.
**A:** `--ignoreDeprecations` (TypeScript 5.0+) suppresses deprecation warnings for specific TypeScript features. Syntax: `"ignoreDeprecations": "5.0"`. Currently only supports `"5.0"`, which suppresses warnings about the deprecated `target: "ES3"` option. TypeScript 5.0 deprecated ES3 target — this flag allows projects still needing ES3 to compile without warnings. This is a temporary measure — ES3 target will be removed in a future major version. For ES3 support, consider using a transpiler like Babel or esbuild instead. The flag should be considered a migration aid, not a permanent solution.

## Q99: How does TypeScript's `--watch` handle file changes in different environments?
**A:** TypeScript's `--watch` uses different file-watching strategies: (1) `UseFsEvents` (fallback to `FixedChunkSizePolling`), (2) `DynamicPriority` (picks the best strategy per directory), (3) `FixedPollingInterval` (always poll), (4) `PriorityPollingInterval` (poll at different rates). Configurable via `watchOptions` in `tsconfig.json`:

```json
{
  "watchOptions": {
    "watchFile": "fixedPollingInterval",
    "watchDirectory": "dynamicPriorityPolling",
    "fallbackPolling": "dynamicPriority",
    "synchronousWatchDirectory": true,
    "excludeDirectories": ["**/node_modules"]
  }
}
```

On Linux, `inotify` watches (limited by `fs.inotify.max_user_watches`). On macOS, `fsevents` for directory watching. On Windows, `FileSystemWatcher`. Network filesystems (NFS, SSHFS) require polling. Adjust `watchOptions` for CI, Docker, and remote development.

## Q100: What are TypeScript's `--diagnostics` and performance optimization strategies?
**A:** TypeScript compilation bottlenecks: (1) `check` phase (type checking) — most expensive, (2) `bind` phase (symbol resolution), (3) `emit` phase (output generation). Optimization strategies: (1) `skipLibCheck: true` — skip `.d.ts` checking, (2) `incremental: true` — reuse previous compilation, (3) project references — parallel build, (4) `isolatedModules: true` — supports faster transpilers (esbuild, SWC), (5) `--noEmit` for type-check-only workflows, (6) reduce `@types` dependencies, (7) prefer `interface` over `type` (faster), (8) avoid complex conditional types with deep recursion, (9) use `const` assertions instead of complex types, (10) avoid large union types (>100 members). Profile with `--diagnostics` and `--generateCpuProfile`
