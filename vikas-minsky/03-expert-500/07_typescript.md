## 45. TypeScript Expert Topics (1201–1240)

1201. How does control flow analysis work?
   TypeScript's control flow analysis narrows types based on runtime checks like `typeof`, `instanceof`, `in`, and equality comparisons. It tracks assignments and type guards through branches, loops, and early returns to refine union types.

1202. Explain distributive object types.
   Distributive object types use mapped types over a union to apply a transformation to each member individually, producing a union of results. The `[K in keyof T]: X` pattern distributes when T is a union type.

1203. What are mapped tuple types?
   Mapped tuple types apply transformations over tuple elements while preserving length and ordering. TypeScript's `{ [K in keyof T]: Transformation<T[K]> }` maps over both array and tuple types, but as-of typing supports homomorphic mapping variants.

1204. Explain advanced infer usage.
   `infer` within conditional types extracts types from other types, enabling recursive type decomposition. Advanced usage includes inferring function parameters, return types, array element types, and deeply nested generic structures.

1205. How do recursive conditional types terminate?
   Recursive conditional types terminate when TypeScript's type instantiation depth limit (~50 levels) is reached or when the recursion reaches a base case that doesn't produce the conditional type. Tail-recursive reductions mitigate depth issues.

1206. Explain literal type widening.
   Literal type widening occurs when `const` declarations are reassigned to `let`, or when literal types pass through generic functions, expanding from `"hello"` to `string`. Using `as const` or explicit literal annotations prevents widening.

1207. What are contextual typing rules?
   Contextual typing infers the types of expressions from their expected usage context. For example, callback parameters in `array.map(x => x + 1)` are typed from the expected callback signature of `.map()`, without explicit annotations.

1208. Explain excess property checks.
   Excess property checks only apply to fresh object literals, warning about unknown properties that aren't defined in the expected type. This catches typos and incorrect API usage while allowing spreading and destructuring to bypass the check.

1209. How do TypeScript emit targets affect output?
   The `target` option determines ECMAScript version of emitted JavaScript, affecting polyfills (async/await, generator, class fields) and module syntax. Targeting older versions produces larger output with helper functions.

1210. Explain declaration merging conflicts.
   Declaration merging allows multiple declarations of the same named interface, namespace, or function to coalesce. Conflicts arise when merged declarations have incompatible properties or generic signatures, causing type errors.

1211. What are symbol-based types?
   Symbol-based types use unique symbols (`declare const sym: unique symbol`) to create nominal-like types that are structurally incompatible even if they share the same shape. This prevents accidental assignment between semantically distinct values.

1212. Explain readonly variance.
   Readonly properties produce covariance in both read and write positions when variance is considered. Arrays marked readonly become covariant (safely assignable to a wider type), while mutable arrays are invariant.

1213. How do compiler transforms work?
   Compiler transforms (custom transformers) intercept the TypeScript AST after parsing or before emit, modifying declarations, adding runtime type information, or generating code. They're passed via the `transformers` option in programmatic API.

1214. Explain transpilation pipelines.
   Transpilation pipelines chain TypeScript compilation with downstream transforms (Babel, SWC) that add polyfills, optimize imports, or apply experimental syntax transforms. SWC is preferred for speed, while Babel offers more plugin extensibility.

1215. What are hybrid callable types?
   Hybrid callable types satisfy both a function signature and property access, created by assigning properties to a function. TypeScript expresses this with intersecting `{ (): T; prop: V }`, useful for factory functions with metadata.

1216. Explain polymorphic generic APIs.
   Polymorphic generic APIs accept generic types that flow through multiple methods, enabling type-safe builder patterns, fluent APIs, and typed reducers. The `this` type in method returns ensures chained calls preserve the concrete type.

1217. How do type predicates work?
   Type predicates (`x is T`) let user-defined type guards narrow types beyond what control flow analysis can infer. The function returns a boolean, and TypeScript uses the predicate to narrow the argument type in the true branch.

1218. Explain strongly typed reducers.
   Strongly typed reducers model state transitions as discriminated unions on action types, with each action carrying typed payloads. TypeScript infers the resulting state type from the reducer's switch cases, ensuring exhaustive handling.

1219. What are immutable type strategies?
   Immutable type strategies use `Readonly<T>`, `ReadonlyArray<T>`, and `as const` to prevent mutations at compile time. Libraries like Immer provide mutable drafts while preserving immutability in persisted state.

1220. Explain advanced utility type design.
   Advanced utility types compose conditional types, mapped types, and template literal types to transform complex type structures. Examples include `DeepPartial`, `PickByValue`, and `UnionToIntersection` for type-level programming.

1221. How do you model finite-state machines?
   Finite-state machines are modeled using discriminated unions for states and a transition function that maps `(state, event) => nextState`. TypeScript ensures exhaustive matching and type-safe event payloads per state.

1222. Explain recursive discriminated unions.
   Recursive discriminated unions model trees, linked lists, and nested structures where a union member references itself. TypeScript requires explicit `type` or `interface` definitions with optional recursion via indirection.

1223. What are compile-time validation strategies?
   Compile-time validation uses branded types, template literal types for format constraints, and type-level arithmetic for numeric bounds. These enforce invariants at compile time without runtime overhead.

1224. Explain schema-derived types.
   Schema-derived types automatically generate TypeScript interfaces from runtime validation schemas (Zod, Yup) using `z.infer<typeof schema>` or `yup.Schema`. This ensures type definitions stay synchronized with validation logic.

1225. How does TypeScript impact build speed?
   TypeScript compilation time scales with project size, third-party `.d.ts` resolution, and complex generics. Strategies to improve speed include project references, incremental builds, `skipLibCheck`, and delegating transpilation to SWC or esbuild.

1226. Explain AST-driven tooling.
   AST-driven tooling (TypeScript Compiler API, ts-morph, tsquery) enables automated refactoring, linting rules, and code generation by analyzing and transforming the Abstract Syntax Tree. These tools power large-scale migrations.

1227. What are custom transformers?
   Custom transformers are functions that modify the TypeScript AST during compilation, enabling features like decorator-to-HoC conversion, automatic dependency injection, or compile-time internationalization.

1228. Explain type-safe backend contracts.
   Type-safe backend contracts share types between frontend and backend using monorepo packages, generating client SDKs that mirror server procedures. tRPC and GraphQL Codegen exemplify this approach.

1229. How do advanced generics improve libraries?
   Advanced generics enable library authors to provide flexible, type-inferred APIs that adapt to user types. Patterns like conditional overloads, variadic tuple types, and template literal types power tools like Zod and Prisma.

1230. Explain typed event architecture.
   Typed event architecture maps event names to payload types using a record type, then constrains emit and listen methods to match. This ensures that `emit("user:created", payload)` is type-checked against the event's payload type.

1231. What are pitfalls of excessive typing?
   Excessive typing increases cognitive load, slows compilation, and can make code harder to refactor. Over-engineered generics, deeply nested conditional types, and unnecessary brand types reduce readability without proportional safety.

1232. Explain maintainable type design.
   Maintainable type design patterns include starting with simple types and adding complexity only when needed, extracting reusable type utilities, documenting type constraints with JSDoc, and preferring union types over inheritance.

1233. How do SDKs leverage TypeScript?
   SDKs leverage TypeScript for auto-complete, documentation via types, and compile-time validation of API usage. Generated SDKs from OpenAPI specs ensure the client types always match the backend contract.

1234. Explain interoperability with JavaScript packages.
   Interoperability requires `allowJs`, `checkJs`, or declaration files (DefinitelyTyped). Poorly typed JS libraries need manual `.d.ts` files, and `skipLibCheck` is often enabled to avoid errors from low-quality third-party types.

1235. What are runtime metadata limitations?
   `emitDecoratorMetadata` emits basic type info (`String`, `Number`, `Object`) but cannot capture complex generics, union types, or type aliases at runtime. This limits dependency injection and serialization frameworks.

1236. Explain compile-time API generation.
   Compile-time API generation uses code generators that read TypeScript type definitions and produce client code, server stubs, or documentation. Tools like `openapi-typescript` and `graphql-codegen` automate this.

1237. What are advanced monorepo typing patterns?
   Advanced monorepo typing uses project references for faster builds, composite projects for declaration maps, and barrel file management to prevent circular imports. Path aliases in `tsconfig.json` simplify cross-package imports.

1238. Explain dependency graph typing.
   Dependency graph typing uses TypeScript's module resolution to enforce dependency direction through `references` in project references. This prevents lower-level packages from importing higher-level ones, maintaining proper layering.

1239. What are frontend type synchronization challenges?
   Frontend/backend type synchronization requires keeping API client types aligned with server responses. Schema-first tools (GraphQL, tRPC, OpenAPI Codegen) automate this, while manual approaches risk drift and runtime errors.

1240. How do elite teams structure TypeScript systems?
   Elite teams structure TypeScript systems with strict mode enabled, exhaustive lint rules, dependency injection for testability, domain-driven module organization, and automated type generation from schemas. They treat types as documentation.
