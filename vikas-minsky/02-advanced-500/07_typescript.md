## 26. TypeScript Advanced (701–740)

701. Explain distributive conditional types.
   Distributive conditional types automatically distribute over unions. `T extends U ? X : Y` applied to `A | B` becomes `(A extends U ? X : Y) | (B extends U ? X : Y)`, enabling per-member transformation.

702. How do variadic tuple types work?
   Variadic tuple types use `...T` in tuple positions to capture and manipulate variable-length arrays. Pattern matching like `[infer F, ...infer R]` extracts first and rest elements with type inference.

703. Explain recursive generic constraints.
   Recursive constraints use `type DeepReadonly<T> = { readonly [K in keyof T]: DeepReadonly<T[K]> }` to traverse nested structures. They require careful base-case handling to avoid infinite type recursion.

704. What are phantom types?
   Phantom types use a type parameter that doesn't appear in the runtime representation. For example, `type UserId = string & { __brand: 'UserId' }` adds compile-time safety without runtime cost.

705. Explain nominal typing workarounds.
   TypeScript uses structural typing by default. Nominal typing workarounds include branded types (`string & { __brand: 'Email' }`), intersection with unique symbols, and enum-based discrimination.

706. How do mixins work in TypeScript?
   Mixins use constructor-type intersections to compose behaviors. A mixin function takes a base class and returns an extended class, applied as `class MyClass extends MixinA(MixinB(Base))`.

707. Explain declaration emit.
   Declaration emit (`declaration: true` in tsconfig) generates `.d.ts` files from TypeScript source. These declaration files describe type signatures without implementation, enabling library consumption without source access.

708. What are compiler APIs?
   Compiler APIs (`typescript` package) expose the TypeScript compiler for programmatic use. They provide access to AST nodes, type checking, source files, and transformers for custom code analysis or generation.

709. Explain AST transformations.
   AST transformations modify TypeScript's syntax tree during compilation. Custom transformers (using `ts.visitNode()`/`ts.visitEachChild()`) can inject code, remove dead code, or enforce project-specific linting.

710. How do decorators affect metadata?
   Decorators (legacy/experimental) can attach metadata to class members via `Reflect.metadata`. This enables dependency injection, validation, and serialization by reading decorator-applied metadata at runtime.

711. Explain experimental decorators.
   Experimental decorators (Stage 2 proposal) use `experimentalDecorators: true` and `emitDecoratorMetadata: true`. They work on classes, methods, properties, and parameters, emitting `__decorate` helper code.

712. What are variance annotations?
   Variance annotations (`in` for contravariant, `out` for covariant, `in out` for invariant) in TypeScript 4.7+ define how generic type parameters behave with inheritance. They help with type safety in generic class hierarchies.

713. Explain polymorphic this types.
   `this` as a return type in methods enables fluent chaining from derived classes. When `class A { foo(): this { ... } }` is extended, `B.foo()` returns `B` instead of `A`.

714. How do module augmentations work?
   Module augmentations use `declare module 'module-name' { ... }` to add types to existing modules. They are useful for extending third-party library types or adding global augmentations.

715. Explain keyof with mapped modifiers.
   `keyof` combined with mapped types like `{ [K in keyof T]: ... }` can add/remove `readonly`, `?` (optional), and transform property types. Adding `-readonly` or `+?` modifies variance.

716. What are infer constraints?
   `infer` in conditional types captures a type variable from a pattern. Constraints like `infer U extends SomeType` narrow inference to subtypes of `SomeType`, enabling safer pattern matching.

717. Explain higher-order type inference.
   Higher-order type inference infers types of functions that accept or return other functions. Using `Parameters<T>` and `ReturnType<T>` on generic function types preserves inferred relationships.

718. How does TypeScript handle async iterators?
   Async iterators (`AsyncIterable<T>`, `AsyncIterator<T>`) are supported with `for await...of`. TypeScript tracks yielded types through `AsyncGenerator<T, TReturn, TNext>` with proper completion and error types.

719. Explain exhaustiveness checking.
   Exhaustiveness checking uses the `never` type in union discrimination. A `default` branch in a switch can assign to `never`, causing a compile error if any union member is unhandled.

720. What are opaque types?
   Opaque types hide internal structure from external consumers. In TypeScript, they're simulated with intersection types and private brand members, enforcing encapsulation at the type level.

721. Explain utility type composition.
   Utility types like `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Exclude<T, U>`, and `Extract<T, U>` can be composed. For example, `Partial<Pick<T, 'a' | 'b'>>` creates optional sub-objects.

722. How do conditional mapped types work?
   Conditional mapped types apply differently per property based on its type. `{ [K in keyof T]: T[K] extends string ? null : T[K] }` transforms only string properties to `null`.

723. Explain indexed signatures.
   Indexed signatures define types for unknown keys: `{ [key: string]: unknown }` or `{ [key: number]: string }`. They describe dictionaries but sacrifice per-key type checking.

724. What are readonly tuples?
   Readonly tuples (e.g., `readonly [number, string]`) prevent mutation of tuple elements. `as const` infers tuples as readonly with literal element types for stricter immutability.

725. Explain exact optional property types.
   Exact optional property types (via `exactOptionalPropertyTypes: true`) prevent assigning `undefined` to optional properties directly, enforcing that only the type itself or omission are valid.

726. What are project references?
   Project references (`references` in tsconfig) split a codebase into multiple TypeScript projects with dependency order. They enable incremental builds, faster compilation, and better editor performance.

727. Explain incremental compilation.
   Incremental compilation (`incremental: true`) caches previous compilation results in `.tsbuildinfo` files. Subsequent builds only recompile changed files and their dependencies, significantly reducing build times.

728. How do declaration maps work?
   Declaration maps (`.d.ts.map`) map declaration file positions back to source `.ts` positions. They enable "Go to Definition" in editors to navigate from `.d.ts` to original TypeScript source.

729. Explain type-level programming.
   Type-level programming uses conditional types, mapped types, recursive constraints, and template literal types to perform computations at compile time. Examples include implementing arithmetic, string manipulation, and state machines with types.

730. What are recursive mapped types?
   Recursive mapped types traverse nested objects by applying themselves to nested values: `type DeepPartial<T> = { [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K] }`.

731. Explain strongly typed event emitters.
   Strongly typed event emitters map event names to payload types: `type MyEmitter = { on<K extends keyof Events>(event: K, cb: (data: Events[K]) => void): void }`. This provides autocomplete and type safety for event handlers.

732. How do generics improve APIs?
   Generics reuse logic across types with compile-time enforcement. APIs like `Array<T>`, `Promise<T>`, and generic functions preserve type relationships between inputs and outputs without sacrificing type safety.

733. Explain compile-time performance bottlenecks.
   Bottlenecks include complex conditional types, deeply recursive types, large union types, and excessive type instantiation. Mitigation includes simplifying types, using interface over type, and incremental compilation.

734. What are deep partial types?
   Deep partial types make all nested properties optional. They are useful for partial updates and test fixtures, implemented as recursive mapped types.

735. Explain typed state machines.
   Typed state machines define states, transitions, and guards as types. Each state has an associated value type, and transitions are validated at compile time to prevent illegal state changes.

736. How do schema validators complement TypeScript?
   Schema validators (Zod, Yup) provide runtime type checking beyond TypeScript's compile-time only guarantees. They validate external data (API responses, user input) and can infer static types from schemas.

737. Explain runtime type safety gaps.
   TypeScript types vanish at runtime, so external data (API calls, JSON parse, user input) bypasses compile-time guarantees. Runtime validators or type guards fill this gap.

738. What are advanced tsconfig optimizations?
   Optimizations include `skipLibCheck: true`, `isolatedModules: true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`, and enabling `composite` + `incremental` for monorepo performance.

739. Explain enterprise TypeScript conventions.
   Conventions include strict mode, consistent file naming (kebab-case), explicit return types on public APIs, organized imports, no `any` usage, JSDoc for complex types, and modular type exports.

740. How do you design scalable type systems?
   Design scalable types with separation of domain types (entities, value objects), DTOs (API contracts), and infrastructure types (DB schemas). Use generics, avoid deep nesting, and leverage project references for large codebases.
