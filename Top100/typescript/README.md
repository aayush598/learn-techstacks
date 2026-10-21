# TypeScript Interview Questions and Answers

## Q1: What is TypeScript and how is it different from JavaScript?
**A:** TypeScript is a typed superset of JavaScript developed by Microsoft that compiles to plain JavaScript. It adds static typing, interfaces, generics, enums, and other features to JavaScript. TypeScript provides compile-time type checking, better IDE support, and catches errors early while maintaining JavaScript runtime behavior.

## Q2: What are the benefits of using TypeScript?
**A:** Benefits include: early error detection via static typing, improved IDE support (autocomplete, refactoring, navigation), self-documenting code through types, easier refactoring at scale, support for modern ES features, better team collaboration through explicit interfaces, and gradual adoption capability.

## Q3: What are the primitive types in TypeScript?
**A:** TypeScript's primitive types: `boolean`, `number`, `string`, `null`, `undefined`, `symbol`, `bigint`, and `void`. These match JavaScript primitives. Additionally, TypeScript adds `never`, `unknown`, and `any`. All types are checked at compile time but erased during compilation.

## Q4: What is the difference between `any` and `unknown`?
**A:** `any` disables type checking entirely—you can assign anything to it and access any property. `unknown` is the type-safe counterpart—you can assign anything to it but must narrow the type before using it (via type guards, assertions, etc.). Prefer `unknown` over `any` for better type safety.

## Q5: What is `never` type?
**A:** `never` represents values that never occur (unreachable code). Used for: functions that always throw, infinite loops, exhaustive type checking in discriminated unions. `never` is assignable to all types but nothing is assignable to `never`. Essential for exhaustiveness checking in switch/if-else chains.

## Q6: Explain TypeScript interfaces.
**A:** Interfaces define the shape of an object with optional, readonly, and method properties. They're open (declaration merging) and can extend other interfaces. Syntax: `interface User { readonly id: number; name?: string; greet(): void }`. Interfaces are primarily for object shapes and are preferred over types for public APIs.

## Q7: What is the difference between `interface` and `type`?
**A:** `interface` can be extended (declaration merging) and only describes objects/functions. `type` creates aliases for any type (primitives, unions, tuples, intersections). Interfaces are typically preferred for object shapes; types for unions, intersections, and complex type compositions. Both are similar for most use cases.

## Q8: What are union types in TypeScript?
**A:** Union types allow a value to be one of several types, denoted by `|`. Example: `string | number`. Use type narrowing (typeof, instanceof, discriminated unions) to determine the specific type. Unions at type level correspond to "either/or" at runtime.

## Q9: What are intersection types?
**A:** Intersection types combine multiple types into one, requiring all properties from each type, denoted by `&`. Example: `A & B` has all properties of A and B. Used for combining interfaces, mixins, and extending types. Conflicts between same-named properties result in `never` if incompatible.

## Q10: What are generics in TypeScript?
**A:** Generics allow creating reusable components that work with multiple types while maintaining type safety. Syntax: `function identity<T>(arg: T): T { return arg }`. Type parameters are specified with angle brackets. Constraints limit what types are allowed: `<T extends Lengthwise>`. Used in functions, classes, interfaces, and types.

## Q11: What are type guards?
**A:** Type guards narrow types within conditional blocks. Built-in: `typeof` (primitives), `instanceof` (classes), `in` operator. Custom: type predicate functions (`x is Type`). Discriminated unions use a literal property (`type` or `kind`) to narrow. Type guards help TypeScript understand type narrowing at compile time.

## Q12: What is the `in` operator type guard?
**A:** The `in` operator checks if a property exists in an object. In TypeScript, `'prop' in obj` narrows the type to those containing the property. Useful for narrowing union types with different property sets. Example: `if ('type' in event) { event.type }`.

## Q13: What are discriminated unions?
**A:** Discriminated unions (tagged unions) have a common literal property (discriminant) that distinguishes each member. TypeScript narrows the type based on the discriminant. Example: `type Shape = { kind: 'circle'; radius: number } | { kind: 'square'; side: number }`. The `kind` property discriminates the union.

## Q14: What is `keyof` operator?
**A:** `keyof T` returns a union of all property keys of type T as string literals. Example: `keyof { name: string; age: number }` is `"name" | "age"`. Used for type-safe object property access, mapping, and generic constraints. Combined with generics for type-safe `getProperty` functions.

## Q15: What is `typeof` type operator?
**A:** In TypeScript, `typeof` in type context captures the type of a value: `type T = typeof obj`. Used for reusing types from existing values, combining with `keyof` for type-safe property access, and `ReturnType<typeof func>`. Not to be confused with JavaScript's runtime `typeof` operator.

## Q16: What is `satisfies` operator?
**A:** `satisfies` (TypeScript 4.9+) checks that a value matches a type without changing the inferred type. Example: `const palette = { red: [255,0,0] } satisfies Record<string, number[]>`. The value must satisfy the type, but the inferred type retains its literal structure for precise autocomplete.

## Q17: What are mapped types?
**A:** Mapped types create new object types by transforming properties of an existing type. Syntax: `{ [P in K]: T }`. Examples: `Partial<T>`, `Readonly<T>`, `Record<K,V>`. Custom: `type Nullable<T> = { [P in keyof T]: T[P] | null }`. Combined with key remapping (`as`) for advanced transformations.

## Q18: What are conditional types?
**A:** Conditional types select a type based on a condition: `T extends U ? X : Y`. Distributive over unions. Examples: `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`. Use `infer` keyword to extract types within conditions: `ReturnType<T> = T extends (...args: any[]) => infer R ? R : never`.

## Q19: How does `infer` work in conditional types?
**A:** `infer` declares a type variable inside a conditional type's extends clause. It captures a type from the structure being tested. Example: `type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never`. Only works in conditional types. Useful for extracting element types, promise values, etc.

## Q20: What is `typeof` vs `instanceof` in TypeScript?
**A:** `typeof x` (runtime) returns a string ("string", "number", "object", etc.). TypeScript uses `typeof` in type guards. `instanceof` checks if an object is an instance of a class. In type context, `typeof value` captures the TypeScript type of a value. They serve different purposes.

## Q21: What is `as const` in TypeScript?
**A:** `as const` (const assertion) marks an expression's type as deeply read-only and narrows literals to their exact values (not widened types). Example: `const colors = ['red', 'blue'] as const` gives type `readonly ["red", "blue"]` instead of `string[]`. Creates literal types from mutable values.

## Q22: Explain TypeScript enums.
**A:** Enums define a set of named constants. Numeric enums (default) auto-increment: `enum Color { Red = 1, Green, Blue }`. String enums: `enum Direction { Up = "UP" }`. Const enums (`const enum`) are inlined at compile time (no runtime object). Enums support reverse mapping for numeric values.

## Q23: What are the differences between `const enum` and regular `enum`?
**A:** Regular enums generate a runtime object with both forward (name to value) and reverse (value to name) mappings. `const enum` is completely inlined at compile time—no runtime code generated. `const enum` values are substituted directly. `const enum` cannot have computed members.

## Q24: What is module augmentation in TypeScript?
**A:** Module augmentation extends existing modules with new declarations. Useful for adding properties to third-party types. Syntax: `declare module 'express' { interface Request { user?: User } }`. Declaration merging adds to existing interfaces. Must be in a module file (with import/export).

## Q25: What are declaration files (`.d.ts`)?
**A:** Declaration files (`.d.ts`) describe the shape of JavaScript modules to TypeScript. They contain only type information, no implementation. `declare module`, `declare function`, `declare class`, etc. Used for consuming JS libraries with types. Can be bundled with packages or in `@types/*` on npm.

## Q26: What is `declare` keyword in TypeScript?
**A:** `declare` tells TypeScript that a value exists at runtime without providing implementation. Used in `.d.ts` files for describing existing JavaScript code. Examples: `declare var`, `declare function`, `declare class`, `declare module`, `declare global`. Important for ambient declarations.

## Q27: Explain TypeScript's strict mode.
**A:** `strict: true` in tsconfig enables all strict checks: `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitAny`, `noImplicitReturns`, `noImplicitThis`, `alwaysStrict`. These catch more errors and provide better type safety. Recommended for all projects.

## Q28: What does `strictNullChecks` do?
**A:** `strictNullChecks` distinguishes `null`/`undefined` from other types. `string` does not include `null` or `undefined`. Variables that might be null/undefined must be explicitly typed as `string | null`. This catches null reference errors at compile time. Requires explicit null handling.

## Q29: What is `noImplicitAny`?
**A:** `noImplicitAny` raises an error when TypeScript can't infer a type and defaults to `any`. Forces explicit type annotations where types can't be inferred. Catches accidentally untyped parameters and variables. Part of strict mode. Makes code more predictable and self-documenting.

## Q30: What are utility types in TypeScript?
**A:** Built-in utility types: `Partial<T>`, `Required<T>`, `Readonly<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`, `ReturnType<T>`, `InstanceType<T>`, `Parameters<T>`, `ConstructorParameters<T>`, `Awaited<T>`, `NoInfer<T>`.

## Q31: What is `Record<K, V>` and when is it used?
**A:** `Record<K, V>` creates an object type with keys of type K and values of type V. K must be string, number, or symbol. Example: `Record<'name' | 'age', string>` = `{ name: string; age: string }`. Used for typed dictionaries and mapping patterns where keys are known.

## Q32: What is `Pick<T, K>` and `Omit<T, K>`?
**A:** `Pick<T, K>` creates a type with only the specified keys K from T. `Omit<T, K>` creates a type with all keys except K. Example: `Pick<User, 'name' | 'email'>` includes only those fields. `Omit<User, 'password'>` excludes password. Useful for derived types.

## Q33: What is `Partial<T>` and `Required<T>`?
**A:** `Partial<T>` makes all properties optional (`?`). `Required<T>` makes all properties required (removes `?`). Example: `Partial<User>` allows creating a user with only some fields. `Required<PartialUser>` requires all fields. Often used for update operations and form state.

## Q34: What is `Readonly<T>` and `ReadonlyArray<T>`?
**A:** `Readonly<T>` makes all properties readonly (can't be reassigned). `ReadonlyArray<T>` (or `readonly T[]`) prevents array mutation (no push, pop, etc.). Mapped arrays: `readonly` in function parameters signals the array won't be modified. Compile-time only; no runtime enforcement.

## Q35: Explain `ReturnType<T>` and `Parameters<T>`.
**A:** `ReturnType<T>` extracts the return type of a function type. `Parameters<T>` extracts parameter types as a tuple. Built on conditional types with `infer`. Example: `ReturnType<typeof fetch>` returns `Promise<Response>`. Useful for propagating types from existing functions.

## Q36: What is `Awaited<T>`?
**A:** `Awaited<T>` (TypeScript 4.5+) unwraps promises recursively. Gets the type that a Promise resolves to. Example: `Awaited<Promise<Promise<string>>>` = `string`. Better than manual `T extends Promise<infer U> ? U : T` for deeply nested promises. Useful with `async` functions.

## Q37: What is `NoInfer<T>`?
**A:** `NoInfer<T>` (TypeScript 5.4+) prevents TypeScript from inferring the type from that position. Forces the caller to explicitly specify the generic or have it inferred from other positions. Useful for preventing overly broad inferences and improving error messages.

## Q38: How do you write a type-safe `Object.keys` in TypeScript?
**A:** `Object.keys` returns `string[]` by default. For typed keys: use a cast: `(Object.keys(obj) as Array<keyof typeof obj>)`. Or create a helper: `function keys<T extends object>(obj: T): (keyof T)[] { return Object.keys(obj) as (keyof T)[] }`.

## Q39: What are assertion functions in TypeScript?
**A:** Assertion functions (TypeScript 3.7+) narrow types by throwing if assertion fails. Return type is `asserts condition` or `asserts x is Type`. Example: `function assertDefined<T>(x: T | undefined): asserts x is T { if (x === undefined) throw new Error() }`. After call, type is narrowed.

## Q40: What is `this` parameter in TypeScript?
**A:** A `this` parameter is a fake parameter at position 0 of a function, specifying the expected type of `this`. Example: `function onClick(this: HTMLButtonElement, e: Event) {}`. Prevents calling the function with wrong `this` context. Used in callbacks, event handlers, and class methods.

## Q41: What are abstract classes in TypeScript?
**A:** Abstract classes cannot be instantiated directly. Marked with `abstract` keyword. They can have implemented methods, abstract methods (no body), and properties. Subclasses must implement all abstract members. Abstract classes provide partial implementation while enforcing a contract.

## Q42: What are access modifiers in TypeScript?
**A:** `public` (default): accessible everywhere. `private`: only within the class (hard private in JS with `#` prefix for true privacy). `protected`: within class and subclasses. `readonly`: can only be assigned during initialization. TypeScript's `private` is compile-time-only; JavaScript's `#` is truly private.

## Q43: What is the difference between `private` and `#private`?
**A:** TypeScript's `private` keyword is enforced at compile time only; at runtime it's just a regular property. JavaScript's `#private` is truly private (ES2021+), enforced at runtime, and can't be accessed even with `Object.keys()` or `in`. TypeScript supports both.

## Q44: Explain parameter properties in TypeScript constructors.
**A:** Parameter properties combine declaration and assignment in one step. Prefix constructor parameter with access modifier: `constructor(public name: string, private age: number)`. Automatically creates and initializes the property. Reduces boilerplate in classes. Supports `public`, `private`, `protected`, `readonly`.

## Q45: What are decorators in TypeScript?
**A:** Decorators are special declarations that modify classes, methods, properties, or parameters. Prefix with `@expression`. Types: class, method, accessor, property, parameter decorators. `experimentalDecorators: true` enables them. TC39 stage 3 decorators differ from experimental ones.

## Q46: What is `declare global` in TypeScript?
**A:** `declare global` adds declarations to the global scope from within a module file. Used for augmenting global types (like adding to `Window`, `String`, `Array`). Syntax: `declare global { interface Window { myProp: string } }`. Only works in files with at least one import/export.

## Q47: Explain template literal types.
**A:** Template literal types (TypeScript 4.1+) create string literal types using template syntax: `type EventName<T extends string> = \`on${T}Changed\``. Combined with unions: `type Color = 'red' | 'blue'; type DarkColor = \`dark-${Color}\``. Used for type-safe event names, CSS properties, and API paths.

## Q48: What are variadic tuple types?
**A:** Variadic tuple types (TypeScript 4.0+) allow generic spread in tuples. Example: `type Concat<A extends any[], B extends any[]> = [...A, ...B]`. Enables type-safe tuple concatenation, function parameter forwarding, and partial argument binding. Powerful for higher-order function typing.

## Q49: What is `readonly` in tuples and arrays?
**A:** `readonly` prevents mutation. `readonly [number, string]` is a readonly tuple. `readonly number[]` prevents array modification. `ReadonlyArray<T>` or `readonly T[]` for arrays. Properties: `as const` makes deeply readonly. Method should accept readonly when they don't mutate.

## Q50: How does TypeScript handle optional chaining?
**A:** Optional chaining (`?.`) is a JavaScript feature that TypeScript types precisely. If `obj?.prop`, TypeScript evaluates `prop` type on `obj`'s type, or `undefined` if `obj` is null/undefined. TypeScript's type system handles the null/undefined propagation through the chain automatically.

## Q51: What is `esModuleInterop`?
**A:** `esModuleInterop` enables better interoperability between CommonJS and ES modules. Allows default imports from CommonJS modules (`import x from 'cjs-module'`) instead of `import * as x from 'cjs-module'`. Enables `__esModule` checks and synthetic default exports. Recommended for modern TS projects.

## Q52: Explain `isolatedModules` in tsconfig.
**A:** `isolatedModules: true` ensures each file can be transpiled independently (without cross-file type information). Required by some transpilers (Babel, esbuild, swc). Disallows features that need cross-file analysis: `const enum` exports, `export * from` re-exporting type conflicts.

## Q53: What is `declarationMap` in tsconfig?
**A:** `declarationMap: true` generates source maps for `.d.ts` declaration files, mapping declarations back to original `.ts` source. Enables "Go to Definition" in IDEs to navigate to `.ts` source instead of `.d.ts`. Improves developer experience for published libraries.

## Q54: How do you type a `fetch` API response?
**A:** `const res = await fetch(url); const data: MyType = await res.json();` — but this doesn't validate the response shape. For proper typing: define a type for the response and optionally use runtime validation (zod, io-ts). TypeScript trusts the JSON parse result.

## Q55: What is `as` type assertion?
**A:** `as` asserts a value's type when TypeScript cannot infer it. Example: `const el = document.getElementById('id') as HTMLInputElement`. Uses: narrowing DOM elements, converting `any` to specific type, JSON.parse results. Prefer over angle bracket syntax in `.tsx`. Use cautiously: bypasses type checking.

## Q56: What is the difference between `as` and `satisfies`?
**A:** `as` is a type assertion (overrides TypeScript's inferred type entirely). `satisfies` checks that a value matches a type while preserving the inferred literal type. `as` can be unsafe (asserting wrong types). `satisfies` is safer as it validates without overriding.

## Q57: What are branded types in TypeScript?
**A:** Branded types create nominal-like typing by adding a unique brand property. Example: `type UserId = string & { __brand: 'UserId' }`. Prevents mixing up IDs of different entities at compile time. No runtime cost (erasable). Uses type assertions for creation: `id as UserId`.

## Q58: What is `unique symbol` in TypeScript?
**A:** `unique symbol` is a subtype of `symbol` where each declaration is unique. Created with `const` and `symbol` type: `const mySymbol: unique symbol = Symbol()`. Used with branded types and for ensuring symbol keys are unique across declarations. Each `declare const` creates distinct type.

## Q59: How does TypeScript handle covariance and contravariance?
**A:** TypeScript function parameters are contravariant (function accepts supertypes), return types are covariant (returns subtypes). In `strictFunctionTypes: true`, parameter types are checked contravariantly (more correct). Arrays are covariant (which is unsound but practical). Method parameters use bivariance.

## Q60: What is type erasure in TypeScript?
**A:** Type erasure means all TypeScript-specific type annotations, interfaces, and generics are removed during compilation. The emitted JavaScript contains no type information. This ensures compatibility with JavaScript runtimes. Type information only exists at compile time for static analysis.

## Q61: What are `const` type parameters?
**A:** `const` type parameters (TypeScript 5.0+) infer types as literals without widening. Example: `function tuple<const T extends any[]>(...args: T): T { return args }`. `tuple('a', 1)` returns `['a', 1]` (literal types) instead of `(string | number)[]`. Similar to `as const` on call site.

## Q62: Explain `@ts-expect-error` vs `@ts-ignore`.
**A:** `@ts-ignore` suppresses errors on the next line regardless of whether there's an actual error. `@ts-expect-error` (TS 3.9+) suppresses the error but flags an error if there's NO error on the next line. `@ts-expect-error` is preferred as it surfaces outdated suppressions.

## Q63: What are declaration merges?
**A:** Declaration merging combines multiple declarations with the same name into one. Interface merging adds properties from later declarations: `interface Box { height: number }` and `interface Box { width: number }` produce one interface with both. Namespace merging also possible. Module augmentation relies on this.

## Q64: How do you type a tuple with rest elements?
**A:** Tuple with rest: `type NamedArgs = [string, ...any[]]`. Labeled: `type Range = [start: number, end: number]`. Variadic: `type Pair<T> = [T, T]`. Rest in middle: `type Params = [number, ...string[], boolean]` (TS 4.2+). Labeled tuples improve readability in function overloads.

## Q65: What are `this`-based type guards?
**A:** `this is Type` return type in class methods narrows the type of the class instance. Example: `class Shape { isCircle(): this is Circle { return this instanceof Circle } }`. After `if (shape.isCircle()) shape` is narrowed to `Circle`. Cleaner than `instanceof` checks.

## Q66: What is `exactOptionalPropertyTypes`?
**A:** `exactOptionalPropertyTypes: true` (TS 4.4+) prevents setting optional properties to `undefined` when reading/writing. With this, `obj.optProp = undefined` is an error for optional `prop?`. The property must either be the specified type or missing. Provides stricter optional handling.

## Q67: How do you use `import type` and `export type`?
**A:** `import type { MyType }` imports only for type checking, not emitted in JS. `export type { MyType }` re-exports only type. Type-only imports/runtime values with the same name: `import { Thing } from './thing'; import type { ThingType } from './thing-type'`. Improves transpilation with isolatedModules.

## Q68: What is `inline type import` in TypeScript?
**A:** Inline type imports (TS 4.5+): `import { type MyType, myFunc } from './module'`. Mixes runtime and type imports in one statement. The `type` keyword marks specific imports as type-only. Cleaner than separate import statements for types and values.

## Q69: Explain `verbatimModuleSyntax`.
**A:** `verbatimModuleSyntax: true` (TS 5.0+) requires that imports/exports not modified by TypeScript. If an import is type-only, must use `import type`. Unused type imports must be explicitly marked. Prevents runtime code from importing purely type values. Strict enforcement of type-only imports.

## Q70: What is `downlevelIteration`?
**A:** `downlevelIteration: true` enables proper iteration support when targeting older ES versions (ES5). Adds helper functions for iterating over iterables (for...of, spread, destructuring). Without it, for...of falls back to simple for loop (may not work with Maps, Sets, etc.). Increases output size.

## Q71: What is the `noUncheckedIndexedAccess` option?
**A:** `noUncheckedIndexedAccess: true` adds `undefined` to all indexed property accesses. Example: `obj[key]` returns `T | undefined` instead of `T`. Catches potential undefined accesses on objects with index signatures or Record types. Requires explicit undefined checks.

## Q72: How does `extends` work in generics?
**A:** `extends` in generics constrains type parameters: `<T extends SomeType>`. T must be assignable to SomeType. Used in conditional types: `T extends U ? X : Y`. Generic constraints can refer to other type parameters: `<T, U extends T>`. Ensures type safety in generic operations.

## Q73: What is the difference between `extends` and `implements`?
**A:** `extends` is for class inheritance (class extends class) or interface extension (interface extends interface). `implements` is for class contract enforcement (class implements interface). A class can extend one class but implement multiple interfaces. Interfaces can extend multiple interfaces.

## Q74: What are mixins in TypeScript?
**A:** Mixins compose behavior from multiple classes into one. Pattern: `type Constructor<T = {}> = new (...args: any[]) => T`; then `function Mixin<TBase extends Constructor>(Base: TBase) { return class extends Base { ... } }`. Combined: `class Final extends Mixin1(Mixin2(Base))`. Alternative to multiple inheritance.

## Q75: How do you create a type-safe event emitter?
**A:** Use generics with mapped types: `interface Events { click: (x: number) => void; change: (val: string) => void }`. Then `class Emitter<T> { on<K extends keyof T>(event: K, handler: T[K]): void {} emit<K extends keyof T>(event: K, ...args: Parameters<T[K]>) {} }`.

## Q76: What is `OmitThisParameter`?
**A:** `OmitThisParameter<T>` removes the `this` parameter from a function type. Example: if `T = (this: Window, x: number) => void`, `OmitThisParameter<T>` gives `(x: number) => void`. Useful when manipulating callback types and removing this-parameter requirements.

## Q77: What are `intrinsic` string manipulation types?
**A:** TypeScript provides intrinsic types for string manipulation: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`. These transform string literal types at compile time. Example: `type Greeting = Capitalize<'hello'>` = `'Hello'`. Used in template literal type patterns.

## Q78: What is `Map` typing in TypeScript?
**A:** `Map<K, V>` is typed with key and value types: `const m = new Map<string, number>()`. Map preserves insertion order. `Map.prototype.get()` returns `V | undefined`. Iteration: `for (const [k, v] of m)`. `Map.keyof()` returns iterable of keys. More type-safe than objects for dynamic keys.

## Q79: How do you type `Object.entries` in TypeScript?
**A:** `Object.entries(obj)` returns `[string, any][]` by default. For typed entries: use `(Object.entries(obj) as [keyof typeof obj, typeof obj[keyof typeof obj]][])`. Or helper: `function entries<T extends Record<string, any>>(obj: T): [keyof T, T[keyof T]][]`.

## Q80: What are `nominal` vs `structural` typing?
**A:** TypeScript uses structural typing (duck typing): types match based on shape, not name. Java/C# use nominal typing: types match based on explicit declarations. Structural typing is more flexible but can accidentally match unrelated types. Branded types add nominal-like behavior.

## Q81: What are `globalThis` and its typing?
**A:** `globalThis` is the standard global object across environments. TypeScript's `lib` includes types for `globalThis`. Extend with `declare global { var myGlobal: string }`. Provides type-safe access to globals. `Window` (browser), `global` (Node), and `self` (Web Worker) are environment-specific.

## Q82: How do you read `.tsconfig.json` paths?
**A:** `tsconfig.json` has `compilerOptions` like `target` (ES version), `module` (module system), `outDir`, `rootDir`, `strict`, `paths` (alias mapping), `baseUrl`, `lib` (included type libraries), `types` (@types packages), `include`/`exclude` (file patterns), `references` (project references).

## Q83: What are project references in TypeScript?
**A:** Project references (TS 3.0+) split a large codebase into smaller projects. `references: [{ path: './shared' }]` in tsconfig. Composite projects (`composite: true`) must produce `.d.ts` files. Enables incremental builds, faster compilation, better organization. Dependencies are built first.

## Q84: What is the `paths` option in tsconfig?
**A:** `paths` maps module imports to file system paths. Example: `"@shared/*": ["./src/shared/*"]`. Requires `baseUrl`. Used for cleaner imports instead of relative paths. Must also configure bundler (Webpack, Vite) or Node module resolution to match paths at runtime.

## Q85: How do you handle circular type dependencies?
**A:** TypeScript generally handles circular type references in interfaces well (trees, linked lists). For circular imports: use `import type` (avoids runtime circular), restructure code, or use interfaces that can reference themselves. TypeScript may error on circular type aliases (use interfaces instead, which can be self-referential).

## Q86: What is the difference between `type` and `interface` for performance?
**A:** Interfaces are generally faster for the type checker, especially with inheritance and intersection. Types with intersections create new computed types each time. For large type compositions, interfaces with `extends` may be faster than types with `&`. Microsoft recommends interfaces for object shapes in public APIs.

## Q87: What is `Promise.all` typing in TypeScript?
**A:** `Promise.all([p1, p2])` infers a tuple of resolved types. Example: `Promise.all([Promise.resolve(1), Promise.resolve('a')])` returns `Promise<[number, string]>`. This works due to variadic tuple types and type inference across array elements. `Promise.allSettled` returns `PromiseSettledResult<T>[]`.

## Q88: How do you type `JSON.parse` and `JSON.stringify` safely?
**A:** `JSON.parse(str)` returns `any`. Use: `JSON.parse(str) as MyType`. For runtime safety: use a schema validator (zod). `JSON.stringify(value)` returns `string | undefined` (undefined if value has toJSON returning undefined). Spreading results: always validate at boundaries.

## Q89: What is `Array.isArray` typing?
**A:** `Array.isArray(value)` narrows `value` to `readonly unknown[]` in TypeScript. Combined with type guard: `if (Array.isArray(value)) { value // readonly unknown[] }`. For specific types: `if (Array.isArray(value)) { const arr = value as MyType[] }`. Better with custom type guards.

## Q90: How do you type event handlers in React with TypeScript?
**A:** React event types: `React.ChangeEvent<HTMLInputElement>` for input changes, `React.FormEvent<HTMLFormElement>` for form submit, `React.MouseEvent<HTMLButtonElement>` for clicks, `React.KeyboardEvent<HTMLInputElement>` for keyboard. `React.EventHandler<React.SyntheticEvent>` for generic handlers.

## Q91: What is `React.FC` and should you use it?
**A:** `React.FC<Props>` (or `React.FunctionComponent<Props>`) is a type for function components. Includes `children` implicitly (now deprecated in React 18 types), `displayName`, `defaultProps`, etc. Currently debated: some prefer `const Component = ({ prop }: Props) => ...` without FC for explicitness.

## Q92: What are `React.ReactNode` vs `React.ReactElement` vs `JSX.Element`?
**A:** `ReactNode` = `ReactElement | string | number | boolean | null | undefined | ReactNode[]` (most broad). `ReactElement` = object with type, props, key (created by JSX). `JSX.Element` = `ReactElement<any, any>` (specific to JSX). `ReactNode` is the return type of components; `ReactElement` for createElement calls.

## Q93: What is the `as` keyword in React?
**A:** Not to be confused with type assertion, the polymorphic `as` prop (e.g., `styled-components`, `MUI`, `Chakra`) lets a component render as a different HTML element or component. Typed with: `type Props<C extends ElementType> = { as?: C } & ComponentPropsWithoutRef<C>`.

## Q94: How do you type a generic React component?
**A:** `function List<T extends { id: string }>({ items, renderItem }: { items: T[]; renderItem: (item: T) => React.ReactNode }) { ... }`. Type inference works at call site: `<List items={users} renderItem={(u) => u.name} />` - T infers from items. Use JSX generics syntax.

## Q95: What is `useRef` typing in TypeScript?
**A:** `useRef<T>(initialValue)` returns `MutableRefObject<T>` if initialValue matches T, or `RefObject<T>` if typing is `null`. For DOM refs: `const ref = useRef<HTMLDivElement>(null)` returns `RefObject<HTMLDivElement | null>` (current is readonly). For mutable values: `const ref = useRef(0)` returns `MutableRefObject<number>`.

## Q96: What is `useReducer` typing in TypeScript?
**A:** Define action type as discriminated union: `type Action = { type: 'increment'; payload: number } | { type: 'decrement' }`. Define reducer: `(state: State, action: Action): State`. TypeScript infers action type in switch cases, narrowing based on `type` discriminant.

## Q97: How do you type a custom hook?
**A:** Custom hooks are regular functions with inferred or explicit return types. Example: `function useLocalStorage<T>(key: string, initial: T): [T, (value: T) => void]`. Generic type parameters propagate call-site types. Return tuples are preferred over objects for hooks returning 2-3 values.

## Q98: What are template literal types used for in practice?
**A:** Practical uses: type-safe event names (`on${Event}`), CSS class composition (`${Size}-${Color}`), API route parameters (`/api/${Resource}/${Id}`), SQL query builders, localization keys (`t\`welcome.${lang}\``), and typed CSS-in-JS property values.

## Q99: What is the `infer` keyword with function types?
**A:** `infer` extracts types from complex structures. Example: extract first argument type: `type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never`. Extract Promise value: `type Unpack<T> = T extends Promise<infer U> ? U : T`. Used heavily in utility type libraries.

## Q100: How do you create a type-safe builder pattern in TypeScript?
**A:** Use mutable generic parameter: `class Builder<T extends Record<string, any> = {}> { with<K extends string, V>(key: K, val: V): Builder<T & Record<K, V>> { ...; return this as any } build(): T { ... } }`. Each `.with()` call adds to the accumulated type. The final `.build()` returns the full union.
