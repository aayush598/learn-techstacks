# TypeScript Fundamentals — Interview Questions

## 30+ Interview Questions with Detailed Answers

---

### 1. What is TypeScript?

**Answer:** TypeScript is a strongly typed, statically typed superset of JavaScript developed by Microsoft. It adds optional static type checking, interfaces, enums, generics, and other features to JavaScript. Every valid JavaScript program is also a valid TypeScript program. TypeScript code is transpiled to plain JavaScript before execution — the type system exists only at development time and has zero runtime cost.

**Key points:**
- Created by Anders Hejlsberg at Microsoft (2012)
- Strict superset of JavaScript (`TypeScript ⊇ JavaScript`)
- Transpiles to JavaScript (types are removed)
- Optional static typing
- Zero runtime overhead
- Rich tooling and IDE support

---

### 2. How does TypeScript differ from JavaScript?

**Answer:**

| Feature | JavaScript | TypeScript |
|---------|-----------|-----------|
| Typing | Dynamic | Static (optional) |
| Compile step | Not required | Required (transpile) |
| Type errors | Runtime | Compile time |
| IDE support | Basic | Advanced (IntelliSense) |
| Learning curve | Lower | Slightly higher |
| Error catching | At runtime | At compile time |
| Code documentation | Comments only | Types serve as docs |
| Refactoring | Risky | Safe |

TypeScript catches type errors before the code runs, provides better tooling through IDE integration, and makes code self-documenting through type annotations. JavaScript is more flexible but less safe.

---

### 3. What is type inference in TypeScript?

**Answer:** Type inference is TypeScript's ability to automatically determine the type of a variable, expression, or return value without explicit type annotations. TypeScript uses several inference mechanisms:

1. **Initializer inference:** `const x = 42` infers `number`
2. **Best common type:** `[1, "hello"]` infers `(string | number)[]`
3. **Contextual typing:** Callback parameters inferred from context
4. **Return type inference:** Return type inferred from function body

```typescript
// All of these use type inference
const name = "Alice";         // string
const numbers = [1, 2, 3];   // number[]
const doubled = numbers.map(x => x * 2); // number[]
```

Inference reduces boilerplate while maintaining type safety. You should let TypeScript infer when the type is obvious and add annotations when it's not.

---

### 4. What is the difference between `let`, `const`, and `var` in TypeScript?

**Answer:**

| Feature | `var` | `let` | `const` |
|---------|-------|-------|---------|
| Scope | Function | Block | Block |
| Redeclaration | Allowed | Not allowed | Not allowed |
| Reassignment | Allowed | Allowed | Not allowed |
| Hoisting | With undefined | TDZ | TDZ |
| Use in modern code | Avoid | When reassignment needed | Default choice |

```typescript
// var — function-scoped, hoisted with undefined
if (true) {
  var x = 10;
}
console.log(x); // 10 (accessible outside block!)

// let — block-scoped, TDZ
if (true) {
  let y = 10;
}
// console.log(y); // Error: y is not defined

// const — block-scoped, cannot reassign
const z = 10;
// z = 20; // Error: Cannot assign to 'z'
```

**Best practice:** Always use `const` by default, `let` only when reassignment is needed, never `var`.

---

### 5. What is the `as const` assertion?

**Answer:** `as const` is a type assertion that makes all properties `readonly` and infers literal types instead of general types. It affects the value deeply — nested objects and arrays also become readonly.

```typescript
// Without as const
const config = { apiUrl: "https://api.example.com", timeout: 5000 };
// type: { apiUrl: string; timeout: number }

// With as const
const config = { apiUrl: "https://api.example.com", timeout: 5000 } as const;
// type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }

// Arrays become readonly tuples
const arr = [1, 2, 3] as const;
// type: readonly [1, 2, 3]
```

Use cases:
- Enum-like objects (alternative to `enum`)
- Configuration objects that shouldn't change
- Tuple-like arrays
- Type-safe event maps

---

### 6. How does TypeScript narrow types?

**Answer:** TypeScript narrows types through control flow analysis using type guards:

1. **Truthiness narrowing:** `if (value)` eliminates `null`, `undefined`, `0`, `""`, `false`
2. **Equality narrowing:** `if (x === "hello")` narrows to the literal type
3. **typeof narrowing:** `if (typeof x === "string")` narrows to `string`
4. **instanceof narrowing:** `if (e instanceof Error)` narrows to `Error`
5. **in narrowing:** `if ("name" in obj)` checks for property existence
6. **Type predicates:** Custom functions with `is` keyword
7. **Assert functions:** Functions with `asserts` keyword
8. **Assignment narrowing:** Variable type changes after assignment

```typescript
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // value narrowed to string
  }
  return value.toFixed(2); // value narrowed to number
}
```

---

### 7. What are the primitive types in TypeScript?

**Answer:** TypeScript has the following primitive types:

| Type | Example | Description |
|------|---------|-------------|
| `string` | `"hello"` | Textual data |
| `number` | `42`, `3.14` | All numeric values (no int/float distinction) |
| `boolean` | `true`, `false` | Logical values |
| `null` | `null` | Intentional absence of value |
| `undefined` | `undefined` | Uninitialized value |
| `symbol` | `Symbol("id")` | Unique identifier |
| `bigint` | `42n` | Arbitrary-precision integers |

Additionally, `void` is a TypeScript-specific type representing the absence of a return value, used primarily for function return types.

With `"strict": true`, `null` and `undefined` are separate types and must be explicitly included in union types.

---

### 8. What is the difference between `null` and `undefined`?

**Answer:**

| Aspect | `null` | `undefined` |
|--------|--------|------------|
| Meaning | Intentionally empty | Not yet assigned |
| typeof | `"object"` (historical bug) | `"undefined"` |
| Assignment | Explicit: `let x = null` | Implicit: `let x` (no assignment) |
| JSON.stringify | Removed from JSON | Removed from JSON |
| `===` comparison | `null === undefined` is `false` | `null === undefined` is `false` |
| `==` comparison | `null == undefined` is `true` | `null == undefined` is `true` |

In TypeScript with `strictNullChecks`, both require explicit union types:

```typescript
let a: string = null;    // Error without strictNullChecks
let b: string | null = null;  // OK

let c: string = undefined;    // Error without strictNullChecks
let d: string | undefined = undefined;  // OK
```

Use `== null` to check for both `null` and `undefined` simultaneously, or use `??` (nullish coalescing) for default values.

---

### 9. What is the `never` type?

**Answer:** The `never` type represents values that never occur. It's used in two main scenarios:

1. **Functions that never return:**
```typescript
function throwError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {}
}
```

2. **Exhaustive checking in switch statements:**
```typescript
type Shape = { kind: "circle"; radius: number } | { kind: "rect"; w: number; h: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rect": return shape.w * shape.h;
    default:
      const _exhaustive: never = shape; // Compile error if not all cases handled
      return _exhaustive;
  }
}
```

`never` is the bottom type — it's assignable to every type, but no type is assignable to it (except `never` itself).

---

### 10. What are interfaces and type aliases? When would you use each?

**Answer:**

Both define object shapes, but have key differences:

**Interface:**
```typescript
interface User {
  name: string;
  age: number;
  email?: string;     // Optional
}

// Declaration merging
interface User {
  phone: string;      // Added to existing interface
}
```

**Type Alias:**
```typescript
type User = {
  name: string;
  age: number;
  email?: string;
};

// No declaration merging
type ID = string | number;  // Union types
type Point = [number, number]; // Tuples
```

**When to use:**
- **Interface:** For object shapes, class contracts, when you need declaration merging
- **Type alias:** For unions, intersections, tuples, computed types, mapped types

**Best practice:** Use `interface` for public API contracts (classes, object shapes), use `type` for everything else (unions, utilities, complex types).

---

### 11. What is the difference between `type` and `interface`?

**Answer:**

| Feature | `interface` | `type` |
|---------|-------------|--------|
| Declaration merging | Yes | No |
| Union types | No | Yes (`A \| B`) |
| Intersection types | Yes (`extends`) | Yes (`A & B`) |
| Tuple types | No | Yes |
| Primitive aliases | No | Yes (`type ID = string`) |
| Implements in classes | Yes | Yes |
| Computed properties | No | Yes |

```typescript
// Interface — extensible via declaration merging
interface Logger {
  log(message: string): void;
}

interface Logger {
  error(message: string): void;
}
// Logger has both log and error

// Type — cannot be merged, but supports unions
type Result = Success | Error;
type ID = string | number;
type Point = [number, number];
```

**Rule of thumb:** Start with `interface` for object shapes. Switch to `type` when you need unions, tuples, or computed types.

---

### 12. What is a discriminated union?

**Answer:** A discriminated union (tagged union) is a union type where each member has a common literal property (the discriminant) that TypeScript uses to narrow the type.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}
```

The `kind` property is the discriminant. TypeScript uses it in `switch`/`if` statements to narrow the union to a specific variant. This pattern is one of the most powerful features of TypeScript's type system.

---

### 13. What are generics in TypeScript?

**Answer:** Generics allow you to write reusable, type-safe code that works with multiple types while preserving type information.

```typescript
// Generic function
function identity<T>(value: T): T {
  return value;
}

const str = identity("hello");  // T is string, returns string
const num = identity(42);       // T is number, returns number

// Generic interface
interface ApiResponse<T> {
  data: T;
  status: number;
}

// Generic class
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }
}

const numberStack = new Stack<number>();
numberStack.push(42);
// numberStack.push("hello"); // Error: string not assignable to number
```

**Key concepts:**
- Type parameter `<T>` is determined at call site
- Generics preserve type information through operations
- Constraints: `<T extends HasLength>` limits what T can be
- Default types: `<T = unknown>` provides fallback

---

### 14. What is the difference between `unknown` and `any`?

**Answer:**

| Feature | `any` | `unknown` |
|---------|-------|-----------|
| Type checking | Disabled | Enabled |
| Can access properties | Yes (no errors) | No (must narrow first) |
| Can call methods | Yes (no errors) | No (must narrow first) |
| Can assign to other types | Yes | No (must assert/narrow) |
| Safe | No | Yes |

```typescript
// any — disables type checking
const data: any = "hello";
data.foo.bar.baz; // No error at compile time, crashes at runtime
const num: number = data; // No error

// unknown — enforces type checking
const data: unknown = "hello";
// data.foo.bar.baz; // Error: 'data' is of type 'unknown'
const num: number = data; // Error: 'unknown' not assignable to 'number'

// Must narrow unknown
if (typeof data === "string") {
  console.log(data.toUpperCase()); // OK — data is string
}
```

**Best practice:** Always use `unknown` instead of `any`. Use `any` only as a last resort when migrating legacy code.

---

### 15. What are utility types in TypeScript?

**Answer:** TypeScript provides built-in utility types for common type transformations:

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Partial — all properties optional
type PartialUser = Partial<User>;
// { id?: string; name?: string; email?: string; age?: number }

// Required — all properties required
type RequiredUser = Required<PartialUser>;

// Pick — select specific properties
type UserBasic = Pick<User, "id" | "name">;
// { id: string; name: string }

// Omit — exclude specific properties
type UserWithoutEmail = Omit<User, "email">;
// { id: string; name: string; age: number }

// Record — create object type
type UserMap = Record<string, User>;

// Readonly
type ReadonlyUser = Readonly<User>;

// ReturnType — extract function return type
function getUser(): User { /* ... */ }
type UserReturn = ReturnType<typeof getUser>;

// Parameters — extract function parameter types
type GetUserParams = Parameters<typeof getUser>;
```

---

### 16. What is the `satisfies` operator?

**Answer:** The `satisfies` operator (TypeScript 4.9+) validates that a value matches a type without widening it. Unlike type annotations, it preserves the literal types of the value.

```typescript
// Type annotation — widens the type
const colors1: Record<string, [number, number, number]> = {
  red: [255, 0, 0],
  green: [0, 255, 0],
};
// type: Record<string, [number, number, number]>
// colors1.red is [number, number, number] (widened)

// satisfies — validates without widening
const colors2 = {
  red: [255, 0, 0],
  green: [0, 255, 0],
} satisfies Record<string, [number, number, number]>;
// type: { red: number[]; green: number[] } (preserved!)
// colors2.red is number[] (not widened to the constraint type)
```

**Key difference:** `satisfies` checks that the value conforms to the type while keeping the original (narrower) type. Type annotations widen to the declared type.

---

### 17. What are mapped types?

**Answer:** Mapped types create new types by transforming properties of an existing type using a mapping clause.

```typescript
// Basic mapped type
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Nullable mapped type
type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};

// Getters mapped type
type Getters<T> = {
  [P in keyof T as `get${Capitalize<string & P>}`]: () => T[P];
};

interface User {
  name: string;
  age: number;
}

type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }

// Conditional mapped type
type OptionalExcept<T, K extends keyof T> = {
  [P in keyof T]: P extends K ? T[P] : T[P] | undefined;
};
```

**Key modifiers in mapped types:**
- `readonly` — makes properties readonly
- `?` — makes properties optional
- `-readonly` — removes readonly
- `-?` — removes optional

---

### 18. What are conditional types?

**Answer:** Conditional types create types based on conditions, similar to ternary expressions:

```typescript
// Basic conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Extract return type
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

// Exclude from union
type Exclude<T, U> = T extends U ? never : T;

type Result = Exclude<"a" | "b" | "c", "a">;
// "b" | "c"

// Extract from union
type Extract<T, U> = T extends U ? T : never;

// Non-nullable
type NonNullable<T> = T extends null | undefined ? never : T;
```

**Key concepts:**
- `extends` checks type relationship
- `infer` captures a type within the conditional
- Distributes over unions automatically
- `never` in conditional types removes members from unions

---

### 19. What is the difference between `class` and `interface` in TypeScript?

**Answer:**

| Feature | `class` | `interface` |
|---------|---------|-------------|
| Runtime code | Yes (generates JS) | No (type-only) |
| Methods | Implemented | Declared only |
| Constructor | Yes | No |
| Access modifiers | public, private, protected | readonly |
| Instantiation | Yes (`new Class()`) | No |
| Declaration merging | No | Yes |
| Extends | Single class | Multiple interfaces |

```typescript
// Interface — contract only
interface Serializable {
  serialize(): string;
}

// Class — implementation
class User implements Serializable {
  constructor(public name: string) {}

  serialize(): string {
    return JSON.stringify({ name: this.name });
  }
}

// Classes also create types
const user: User = new User("Alice"); // User type from class
```

**Rule of use:** Use interfaces for contracts/ABIs. Use classes when you need implementation and runtime behavior.

---

### 20. What is declaration merging?

**Answer:** Declaration merging is TypeScript's ability to combine multiple declarations with the same name into a single definition. This works with interfaces:

```typescript
// Interface merging
interface Window {
  myCustomProperty: string;
}

// Now Window has myCustomProperty in addition to all built-in properties

// Namespace merging
namespace Validation {
  export interface StringValidator {
    isAcceptable(s: string): boolean;
  }
}

namespace Validation {
  export class EmailValidator implements StringValidator {
    isAcceptable(s: string): boolean {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
    }
  }
}

// Both Validation interfaces are merged
```

**Only interfaces and namespaces merge.** Type aliases, classes, functions, and variables do not merge — they produce errors if redeclared.

---

### 21. What are type assertions and when should you use them?

**Answer:** Type assertions tell TypeScript to treat a value as a specific type, overriding inference:

```typescript
// Two syntaxes
const el1 = document.getElementById("name") as HTMLInputElement;
const el2 = <HTMLInputElement>document.getElementById("name");

// Type assertion doesn't change runtime behavior
const str: string = "hello";
const num: number = str as unknown as number; // Unsafe but compiles
```

**When to use:**
1. DOM element access: `document.getElementById("x") as HTMLInputElement`
2. JSON parsing: `JSON.parse(data) as User`
3. Third-party library typing gaps
4. Working with `unknown` or `any` during migration

**When NOT to use:**
1. When a type guard is safer
2. When you can fix the types properly
3. To silence TypeScript errors (indicates a real problem)

**Best practice:** Prefer type guards (`typeof`, `instanceof`, `in`) over assertions. Use `as` only when you genuinely know more than TypeScript.

---

### 22. What are template literal types?

**Answer:** Template literal types create new string types from string literal types using template literal syntax:

```typescript
// Basic template literal type
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">;    // "onClick"
type FocusEvent = EventName<"focus">;    // "onFocus"

// Combined template literal types
type Color = "red" | "blue" | "green";
type Size = "small" | "medium" | "large";

type ColorSize = `${Color}-${Size}`;
// "red-small" | "red-medium" | "red-large" |
// "blue-small" | "blue-medium" | "blue-large" |
// "green-small" | "green-medium" | "green-large"

// With constraints
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIPath = `/api/${string}`;
type Endpoint = `${HTTPMethod} ${APIPath}`;
// "GET /api/..." | "POST /api/..." | etc.
```

---

### 23. What is the difference between `==` and `===` in TypeScript?

**Answer:** TypeScript enforces the use of strict equality:

- `===` (strict equality): Compares value AND type. `5 === "5"` is `false`
- `==` (loose equality): Compares after type coercion. `5 == "5"` is `true`

```typescript
// TypeScript allows both but strongly recommends ===
0 == "";      // true (coerced)
0 == false;   // true (coerced)
"" == false;  // true (coerced)
null == undefined; // true (special rule)

// With ===
0 === "";      // false
0 === false;   // false
"" === false;  // false
null === undefined; // false
```

**Best practice:** Always use `===` and `!==`. The only exception is `value == null` which is an idiomatic way to check for both `null` and `undefined`.

---

### 24. What is a type guard?

**Answer:** A type guard is an expression that TypeScript uses to narrow the type of a variable within a conditional block:

```typescript
// Built-in type guards
typeof x === "string"      // narrows to string
x instanceof Error         // narrows to Error
"name" in obj              // narrows to object with "name" property
Array.isArray(x)           // narrows to array

// Custom type guard (type predicate)
function isString(x: unknown): x is string {
  return typeof x === "string";
}

function process(value: unknown) {
  if (isString(value)) {
    console.log(value.toUpperCase()); // value narrowed to string
  }
}

// Assert function
function assertDefined<T>(x: T | null | undefined): asserts x is T {
  if (x == null) throw new Error("Value is null or undefined");
}
```

Type guards enable safe type narrowing in complex scenarios where built-in checks are insufficient.

---

### 25. What is the difference between `readonly` and `const`?

**Answer:**

| Feature | `const` | `readonly` |
|---------|---------|-----------|
| Applies to | Variables | Properties |
| Scope | Block-scoped variable | Object property |
| Prevents reassignment | Yes (the binding) | Yes (the property) |
| Prevents mutation | No (objects/arrays can mutate) | No (unless deeply readonly) |
| TypeScript-specific | No (JavaScript feature) | Yes (compile-time only) |

```typescript
// const — cannot reassign the variable
const arr = [1, 2, 3];
arr.push(4); // OK — array is mutable
// arr = [4, 5, 6]; // Error — cannot reassign

// readonly — cannot reassign the property
interface Config {
  readonly apiUrl: string;
  timeout: number;
}

const config: Config = { apiUrl: "https://api.example.com", timeout: 5000 };
// config.apiUrl = "other"; // Error — readonly
config.timeout = 3000; // OK — not readonly

// Deep readonly with utility type
type DeepReadonly<T> = { readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P] };
```

---

### 26. What is the `keyof` operator?

**Answer:** `keyof` creates a union type of all keys of an object type:

```typescript
interface User {
  name: string;
  age: number;
  email: string;
}

type UserKeys = keyof User;
// "name" | "age" | "email"

// Used with generics for type-safe property access
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { name: "Alice", age: 30, email: "alice@example.com" };
const name = getProperty(user, "name"); // string
const age = getProperty(user, "age");   // number
// getProperty(user, "password"); // Error: "password" not in keyof User

// Used with Record
type UserValues = Record<UserKeys, unknown>;
// { name: unknown; age: unknown; email: unknown }

// Used with Pick/Omit
type UserName = Pick<User, "name">; // { name: string }
```

---

### 27. What is the difference between `void` and `undefined`?

**Answer:**

| Feature | `void` | `undefined` |
|---------|--------|------------|
| Meaning | Function doesn't return | Actual undefined value |
| Usage | Return type annotation | Variable value |
| Runtime | No equivalent | `undefined` exists at runtime |
| Assignable | `undefined` is assignable to `void` | `void` is not assignable to `undefined` |

```typescript
// void — return type (function returns nothing)
function log(message: string): void {
  console.log(message);
}

// undefined — actual value
let x: undefined = undefined;

// void function can return undefined
function doNothing(): void {
  return undefined; // OK
}

// void callback — return value is ignored
const arr = [1, 2, 3];
arr.forEach((x): void => {
  console.log(x);
  // Can return a value, but it's ignored
});

// void in Promise types
async function fetchData(): Promise<void> {
  await fetch("/api/data");
  // No return value
}
```

---

### 28. How do you handle errors in TypeScript?

**Answer:** TypeScript provides several patterns for error handling:

```typescript
// 1. Try-catch (typed catch variable with strict mode)
try {
  const data = JSON.parse(input);
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}

// 2. Result type pattern (functional error handling)
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { ok: false, error: "Division by zero" };
  return { ok: true, value: a / b };
}

const result = divide(10, 0);
if (result.ok) {
  console.log(result.value);
} else {
  console.error(result.error);
}

// 3. Discriminated union for error states
type ApiResponse =
  | { status: "success"; data: User }
  | { status: "error"; message: string }
  | { status: "loading" };

// 4. Custom error classes
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = "ValidationError";
  }
}
```

---

### 29. What is structural typing vs nominal typing?

**Answer:**

- **TypeScript uses structural typing:** Types are compatible if they have the same structure (shape), regardless of their names.
- **Nominal typing** (Java, C#): Types are compatible only if they share the same name/identity.

```typescript
// Structural typing — same shape = compatible
interface Point {
  x: number;
  y: number;
}

interface Coordinate {
  x: number;
  y: number;
}

const point: Point = { x: 1, y: 2 };
const coord: Coordinate = point; // OK! Same structure

// Even without explicit interface
function printPoint(p: { x: number; y: number }) {
  console.log(`${p.x}, ${p.y}`);
}

printPoint({ x: 1, y: 2 }); // OK — object literal matches
printPoint(point);           // OK — Point matches { x: number; y: number }
```

**Implication:** You can't use TypeScript types as unique identifiers. Use `unique symbol` or branded types for nominal-like behavior:

```typescript
// Branded type pattern for nominal typing
type UserId = string & { readonly __brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

function processUser(id: UserId) { /* ... */ }

// processUser("abc"); // Error — string is not UserId
processUser(createUserId("abc")); // OK
```

---

### 30. What are the strictest tsconfig settings for maximum type safety?

**Answer:**

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "forceConsistentCasingInFileNames": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "useUnknownInCatchVariables": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true
  }
}
```

Key additions beyond `strict: true`:
- `noUncheckedIndexedAccess`: Array/object index access returns `T | undefined`
- `exactOptionalPropertyTypes`: Distinguishes between `undefined` and missing
- `verbatimModuleSyntax`: Enforces explicit `type` imports

---

### 31. What is the difference between `export type` and `export`?

**Answer:**

```typescript
// Regular export — exports the runtime value
export const PI = 3.14159;
export function add(a: number, b: number) { return a + b; }

// Type-only export — exports only the type (removed at compile time)
export type User = { name: string; age: number };
export interface Logger { log(msg: string): void; }

// Inline type export
export { type User, type Logger };
// Or
export type { User, Logger };
```

With `verbatimModuleSyntax: true`, you must use `import type` / `export type` for type-only imports/exports:

```typescript
// Correct with verbatimModuleSyntax
import type { User } from "./types";
import { createUser } from "./users";

// Error without type keyword when importing types
// import { User } from "./types"; // Error: User is a type
```

---

### 32. What are index signatures?

**Answer:** Index signatures define the type of properties accessed via dynamic keys:

```typescript
// String index signature
interface StringMap {
  [key: string]: string;
}

const translations: StringMap = {
  hello: "Hello",
  goodbye: "Goodbye",
};

// Number index signature
interface NumberArray {
  [index: number]: string;
}

// Combined with known properties
interface Dictionary {
  [key: string]: string;
  length: number; // Known property
}

// With access control
interface Config {
  readonly [key: string]: unknown;
  apiUrl: string; // This must be string, not unknown
}
```

**Index signature vs Record:**
```typescript
// Index signature
interface Obj { [key: string]: number }

// Record utility type (equivalent)
type Obj2 = Record<string, number>
```

---

### 33. How does TypeScript handle async/await?

**Answer:** TypeScript fully supports async/await with proper typing:

```typescript
// Async functions always return Promise<T>
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data: User = await response.json();
  return data;
}

// Promise chaining
function processUsers(ids: string[]): Promise<User[]> {
  return Promise.all(ids.map(id => fetchUser(id)));
}

// Error handling
async function safeFetch(id: string): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch (error) {
    if (error instanceof Error) {
      console.error(error.message);
    }
    return null;
  }
}

// Typed promises
const promise: Promise<string> = new Promise((resolve) => {
  resolve("hello");
});

const result: string = await promise;

// Promise.all with proper typing
const [users, posts] = await Promise.all([
  fetchUsers(),    // Promise<User[]>
  fetchPosts(),    // Promise<Post[]>
]);
// users: User[], posts: Post[]
```

---

### 34. What is the `infer` keyword?

**Answer:** `infer` is used in conditional types to capture (infer) a type within the conditional expression:

```typescript
// Infer return type of a function
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() { return { name: "Alice", age: 30 }; }
type UserType = ReturnOf<typeof getUser>;
// { name: string; age: number }

// Infer element type of an array
type ElementOf<T> = T extends (infer E)[] ? E : never;
type Num = ElementOf<number[]>; // number

// Infer parameters of a function
type ParamsOf<T> = T extends (...args: infer P) => any ? P : never;
type FnParams = ParamsOf<(a: string, b: number) => void>;
// [a: string, b: number]

// Infer Promise result type
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
type Result = Awaited<Promise<string>>; // string
type Nested = Awaited<Promise<Promise<number>>>; // number
```

---

### 35. What are some common TypeScript anti-patterns?

**Answer:**

1. **Using `any`:** Use `unknown` instead and narrow.
2. **Type assertions to silence errors:** Fix the underlying type issue.
3. **Non-null assertion (`!`) abuse:** Use proper null checks.
4. **Ignoring strictNullChecks:** Always enable `"strict": true`.
5. **Over-annotating:** Let TypeScript infer obvious types.
6. **Using `enum`:** Prefer `as const` objects or union types.
7. **Ignoring `noImplicitAny`:** Always annotate function parameters.
8. **Using `var`:** Always use `const` or `let`.
9. **Catching without typing:** Use `error instanceof Error`.
10. **Mixing `type` and `interface` inconsistently:** Follow a convention.

```typescript
// BAD
const data: any = fetchData();
(data as User).name; // Unsafe

// GOOD
const data: unknown = fetchData();
if (isUser(data)) {
  data.name; // Safe
}
```

---

## Quick Reference: Key Concepts

| Concept | One-Line Answer |
|---------|----------------|
| TypeScript | JavaScript with static types |
| Type inference | Automatic type determination |
| Type narrowing | Refining types through control flow |
| Generics | Reusable, type-safe components |
| Discriminated unions | Tagged unions for exhaustive checking |
| Utility types | Built-in type transformations |
| Structural typing | Shape-based compatibility |
| `never` | Type for values that never occur |
| `unknown` | Type-safe alternative to `any` |
| `as const` | Deep readonly + literal types |
| `satisfies` | Validate type without widening |
| `keyof` | Union of object keys |
| `infer` | Capture type in conditional |
| `void` | Function returns nothing |
