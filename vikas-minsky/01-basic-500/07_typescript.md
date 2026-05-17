## 7. TypeScript (201–240)

201. Why use TypeScript?
     TypeScript adds static typing to JavaScript, catching errors at compile time rather than runtime. It provides better IDE support with autocompletion and refactoring, improves code documentation through type annotations, and scales well for large codebases.

202. Difference between interface and type?
     Interfaces are primarily for object shapes and can be extended via `extends` or merged (declaration merging). Types are more flexible, supporting unions, intersections, primitives, and mapped types. Both are largely interchangeable for object types in modern TypeScript.

203. Explain generics.
     Generics create reusable components that work with any type by using type parameters (`<T>`). They preserve type information across functions, classes, and interfaces, enabling type-safe data structures like `Array<T>` and utility functions with inferred return types.

204. What are utility types?
     Utility types are built-in generic types for common transformations: `Partial<T>` (all optional), `Required<T>` (all required), `Pick<T, K>` (select keys), `Omit<T, K>` (exclude keys), `Record<K, V>` (key-value map), `Exclude<T, U>` (union subtraction), and `ReturnType<T>`.

205. Explain mapped types.
     Mapped types transform existing types by iterating over keys using `in keyof`. They create new types based on old ones, like making all properties readonly or nullable. Example: `{ [K in keyof T]: T[K] | null }` makes all values nullable.

206. What are conditional types?
     Conditional types use `extends` for type-level conditionals: `T extends U ? X : Y`. They enable type transformations based on type relationships, like extracting return types (`infer R`) or filtering union members based on constraints.

207. Explain union and intersection types.
     Union types (`A | B`) mean the value can be either type A or B. Intersection types (`A & B`) combine both types, requiring all properties from both. Unions represent alternatives, intersections represent combinations.

208. What is type narrowing?
     Type narrowing is TypeScript's process of refining a broad type to a more specific one based on runtime checks. It works through `typeof` guards, `instanceof` checks, discriminated unions, `in` operator, and type predicates.

209. Explain type inference.
     Type inference means TypeScript automatically deduces types based on values and usage. Variables get their type from initialization, function return types from return statements, and generic types from arguments — reducing explicit annotations while maintaining safety.

210. Difference between any, unknown, and never?
     `any` disables type checking entirely — use sparingly. `unknown` is type-safe `any` — requires type narrowing before use. `never` represents values that never occur, like the return type of functions that always throw or infinite loops.

211. Explain enums.
     Enums define a set of named constants. Numeric enums auto-increment values, string enums have explicit values, and const enums are inlined at compile time with no runtime overhead. Enums improve readability but some avoid them due to runtime cost.

212. What are discriminated unions?
     Discriminated unions combine union types with a common literal property (discriminant) that TypeScript uses for type narrowing. Each member has a unique discriminant value, enabling exhaustive switch statements and type-safe pattern matching.

213. Explain declaration merging.
     Declaration merging is TypeScript's ability to combine multiple declarations with the same name into one. Interfaces with the same name merge their members, which is useful for extending third-party types. Types cannot be merged.

214. What are decorators?
     Decorators are functions prefixed with `@` that modify classes, methods, properties, or parameters. They're used in frameworks like Angular and NestJS for metadata injection, logging, and dependency injection. TypeScript enables them with `experimentalDecorators`.

215. Explain namespaces vs modules.
     Namespaces (internal modules) organize code within a single global scope using `namespace` keyword. Modules (external modules) use ES module syntax (`import`/`export`) and are file-based. Modules are preferred for modern code, namespaces are legacy.

216. What are ambient declarations?
     Ambient declarations (`declare module 'x'`) tell TypeScript about types from external JavaScript libraries without implementation. `.d.ts` files provide type information for plain JS modules, enabling type checking without rewriting in TypeScript.

217. Explain tsconfig options.
     Key options: `strict` enables all strict checks, `target` determines JS output version, `module` sets module system, `outDir` is output directory, `rootDir` is source root, `paths` maps module aliases, `include`/`exclude` controls file scope.

218. What is strict mode?
     Strict mode (`strict: true`) enables all type-checking options including `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, and `alwaysStrict` for maximum type safety.

219. Explain module resolution.
     Module resolution determines how TypeScript locates files for imports. Classic is the legacy strategy. Node mimics Node.js resolution (looking for `index.ts`, package.json `types` field). `bundler` and `Node16`/`NodeNext` are modern strategies for ESM support.

220. Difference between compile-time and runtime?
     Compile-time is when TypeScript checks types and transpiles to JavaScript — errors caught here prevent compilation. Runtime is when the compiled JavaScript executes in the browser or Node.js — type information is erased, only runtime checks catch errors.

221. Explain readonly types.
     `readonly` prevents property reassignment after initialization. `Readonly<T>` utility type makes all properties readonly. `readonly` arrays (`readonly T[]`) prevent mutation methods like `push` and `pop`, ensuring immutability at the type level.

222. What are indexed access types?
     Indexed access types look up a property type using bracket syntax: `type T = User['name']` gets the type of the `name` property. They support nesting (`User['address']['city']`) and union indices (`User['name' | 'email']`).

223. Explain keyof operator.
     `keyof T` returns a union of all property keys of type T as string literals. It's used with mapped types, generic constraints, and type-safe functions for accessing object properties, enabling compile-time property name validation.

224. What are template literal types?
     Template literal types use string literal types with template syntax to create new string types: `` type EventName = `on${Capitalize<string>}` ``. They enable type-safe string manipulation for event handlers, CSS properties, and API endpoint patterns.

225. Explain overloads.
     Overloads define multiple function signatures for different argument types or counts, providing type-safe variations of the same function. Only the implementation signature exists at runtime — overload signatures are purely for compile-time type checking.

226. What are assertion functions?
     Assertion functions narrow types by throwing if a condition fails. They are annotated with `asserts` keyword: `function assertIsString(val: unknown): asserts val is string`. After a successful call, TypeScript narrows the type within the scope.

227. Explain covariance and contravariance.
     Covariance means a type preserves its subtype relationship (if `A extends B`, then `Array<A> extends Array<B>`). Contravariance reverses it (function parameters are contravariant — if `A extends B`, then `(b: B) => void` extends `(a: A) => void`).

228. What is structural typing?
     Structural typing (duck typing) means type compatibility is determined by structure, not explicit declarations. If two types have the same shape, they are compatible — unlike nominal typing where types must be explicitly related by name or inheritance.

229. Explain async typing.
     Async typing handles types for asynchronous operations: `Promise<T>` wraps future values, `async` functions return `Promise<T>`, and `await` unwraps the promise type. TypeScript tracks Promise states through generics for type-safe async code.

230. How does TypeScript improve DX?
     TypeScript improves developer experience through intelligent autocompletion, inline documentation on hover, refactoring tools (rename symbol, extract method), instant error feedback in editors, and type-based navigation like "Go to Definition."

231. Explain source maps.
     Source maps map compiled JavaScript back to original TypeScript source, enabling debugging with original file names and line numbers in browser DevTools. They're generated with `sourceMap: true` in tsconfig and are crucial for production debugging.

232. What are declaration files?
     Declaration files (`.d.ts`) contain type information without implementation. They describe the shape of JavaScript libraries for TypeScript consumers, enable type checking without source code access, and are generated with `declaration: true` in tsconfig.

233. Explain infer keyword.
     `infer` is used in conditional types to extract a type from another type within an `extends` clause. It's used in utility types like `ReturnType<T>` (infers return type) and `Parameters<T>` (infers parameter types) to capture and reuse type information.

234. What are recursive types?
     Recursive types reference themselves, enabling type-safe representation of nested data like JSON, trees, or linked lists. TypeScript supports recursive type aliases with property-level recursion and recursive conditional types for complex transformations.

235. Explain branded types.
     Branded types (nominal typing simulation) add a unique property to distinguish structurally identical types: `type Email = string & { __brand: 'Email' }`. They prevent mixing up values of the same base type, like UserId vs OrderId.

236. Difference between extends and implements?
     `extends` creates class inheritance where the child inherits methods and properties from the parent. `implements` enforces that a class adheres to an interface contract without inheriting implementation — multiple interfaces can be implemented.

237. Explain optional chaining.
     Optional chaining (`?.`) safely accesses deeply nested properties without throwing on null/undefined. `user?.profile?.name` returns `undefined` if any intermediate value is nullish, replacing verbose null checks with concise syntax.

238. What are const assertions?
     Const assertions (`as const`) make TypeScript infer literal types instead of widening them. An array becomes `readonly` tuple, object properties become `readonly` with literal value types, enabling precise type inference for constants.

239. Explain TypeScript performance issues.
     Performance issues arise from large projects with complex types, deep generics, excessive type inference, and large declaration files. Solutions include project references for incremental builds, `skipLibCheck`, type-only imports, and avoiding extreme conditional types.

240. How do you scale TypeScript projects?
     Scale using project references (monorepo with incremental builds), strict mode for consistency, shared type packages, barrels carefully (avoid circular deps), ESLint with `@typescript-eslint`, consistent tsconfig across packages, and path aliases for clean imports.
