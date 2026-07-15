# The any, unknown, and never Types

## Table of Contents

1. [Overview](#overview)
2. [The any Type](#the-any-type)
3. [The unknown Type](#the-unknown-type)
4. [The never Type](#the-never-type)
5. [The void Type](#the-void-type)
6. [Comparison Table](#comparison-table)
7. [Best Practices](#best-practices)
8. [Interview Questions](#interview-questions)

---

## Overview

TypeScript provides four special types that represent different levels of type safety and control flow:

| Type      | Safe to use? | Description                                        |
|-----------|-------------|----------------------------------------------------|
| `any`     | ❌ Avoid    | Escapes the type system — no type checking         |
| `unknown` | ✅ Use      | Type-safe alternative to `any` — must narrow first |
| `never`   | ✅ Use      | Represents values that never occur (bottom type)   |
| `void`    | ✅ Use      | Represents absence of return value                  |

---

## The any Type

`any` is TypeScript's escape hatch from the type system. When a value is typed as `any`, all type checking is disabled.

### When any is Assigned

```typescript
// Explicit any
let anything: any = "hello";
anything = 42;       // OK
anything = true;     // OK
anything = [1, 2];   // OK
anything = {};       // OK

// Implicit any (when TypeScript can't infer the type)
function processData(data) { // Parameter 'data' implicitly has 'any' type
  return data.foo; // No error — but runtime crash if data doesn't have .foo
}

// Callbacks without type annotations
[1, 2, 3].forEach(item => {
  console.log(item.toFixed()); // 'item' is implicitly 'any'
});

// JSON.parse returns any
const parsed: any = JSON.parse('{"name": "Alice"}');
parsed.name;     // OK (no type checking)
parsed.nonexist; // OK (no type checking — even for wrong properties)
```

### Dangers of any

```typescript
// any disables ALL type checking — it's contagious
let value: any = "hello";
let num: number = value; // No error — any is assignable to anything
let str: string = value; // No error
let bool: boolean = value; // No error

// any propagates through operations
const result = value.toUpperCase(); // No error (but would crash if value is a number)
const array: number[] = value; // No error

// any defeats the purpose of TypeScript
function add(a: any, b: any): any {
  return a + b; // No type checking on parameters or return value
}

// You lose autocomplete, refactoring support, and compile-time safety
const obj: any = { name: "Alice", age: 30 };
obj.name;      // No autocomplete
obj.age;       // No autocomplete
obj.nonexist;  // No error, no autocomplete
```

### noImplicitAny

The `noImplicitAny` compiler option prevents implicit `any` types:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true // Includes noImplicitAny
    // or specifically:
    // "noImplicitAny": true
  }
}
```

```typescript
// With noImplicitAny: true

// ❌ Error: Parameter 'x' implicitly has an 'any' type
function double(x) {
  return x * 2;
}

// ✅ Fix: Add explicit type annotation
function doubleFixed(x: number): number {
  return x * 2;
}

// ❌ Error: Variable 'data' implicitly has an 'any' type
let data;
data = "hello";
data = 42;

// ✅ Fix: Declare with type
let dataFixed: string | number;
dataFixed = "hello";
dataFixed = 42;

// ❌ Error in callback
[1, 2, 3].forEach(x => x.toFixed()); // 'x' implicitly has 'any' type

// ✅ Fix: Add type annotation
[1, 2, 3].forEach((x: number) => x.toFixed());
// Or let TypeScript infer (it usually can for simple cases):
[1, 2, 3].forEach(x => x.toFixed()); // Actually, TS infers this correctly
```

### When any Might Be Acceptable

```typescript
// 1. During migration from JavaScript
// @ts-ignore or any can be used temporarily
const legacyModule: any = require("old-module");

// 2. When working with truly dynamic data
function processDynamic(input: any): any {
  // At API boundaries, you might use any temporarily
}

// 3. Third-party libraries without type definitions (prefer @types first)
// npm install @types/some-library

// 4. Test files (less critical to have strict types)
// jest.mock returns any in some configurations
```

---

## The unknown Type

`unknown` is the type-safe counterpart to `any`. You can assign anything to `unknown`, but you must narrow it before using it.

### Basic Usage

```typescript
// unknown accepts any value
let value: unknown = "hello";
value = 42;       // OK
value = true;     // OK
value = [1, 2];   // OK
value = {};       // OK

// ❌ Cannot use unknown directly
let num: number = value;    // Error: 'value' is of type 'unknown'
let str: string = value;    // Error
value.toUpperCase();         // Error: 'value' is of type 'unknown'
value.foo;                   // Error

// ✅ Must narrow first
if (typeof value === "string") {
  console.log(value.toUpperCase()); // OK — narrowed to string
}

if (typeof value === "number") {
  console.log(value.toFixed(2)); // OK — narrowed to number
}
```

### Type Narrowing unknown

```typescript
// typeof narrowing
function processUnknown(value: unknown): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // narrowed to string
  }
  if (typeof value === "number") {
    return value.toFixed(2); // narrowed to number
  }
  if (typeof value === "boolean") {
    return value ? "true" : "false"; // narrowed to boolean
  }
  if (value === null) {
    return "null"; // narrowed to null
  }
  if (value === undefined) {
    return "undefined"; // narrowed to undefined
  }
  return "unknown type";
}

// instanceof narrowing
function handleError(value: unknown): string {
  if (value instanceof Error) {
    return value.message; // narrowed to Error
  }
  return String(value);
}

// Custom type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "name" in value &&
    "age" in value &&
    typeof (value as User).name === "string" &&
    typeof (value as User).age === "number"
  );
}

interface User {
  name: string;
  age: number;
}

function processUser(data: unknown): User {
  if (isUser(data)) {
    return data; // narrowed to User
  }
  throw new Error("Invalid user data");
}

// Assertion function
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Expected a string");
  }
}

function greet(name: unknown): string {
  assertIsString(name); // narrows 'name' to string after this line
  return `Hello, ${name.toUpperCase()}`;
}
```

### unknown in Function Signatures

```typescript
// unknown as parameter type (safer than any)
function process(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number") return String(value);
  return JSON.stringify(value);
}

// unknown as return type
function fetchData(): unknown {
  // The caller must narrow the result before using it
  return JSON.parse('{"name": "Alice"}');
}

// Generic constraints with unknown
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// unknown is useful for library code that works with any value
function safeClone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value));
}

// unknown in union types
type ApiResponse = {
  data: unknown;
  status: number;
};

function handleResponse(response: ApiResponse): void {
  if (response.status === 200) {
    // Still need to narrow response.data
    if (typeof response.data === "object" && response.data !== null) {
      console.log(response.data);
    }
  }
}
```

### any vs unknown — Key Differences

```typescript
// any: skips type checking entirely
const anyValue: any = "hello";
anyValue.nonexist.property; // No error at compile time, crashes at runtime

// unknown: forces type checking
const unknownValue: unknown = "hello";
unknownValue.nonexist.property; // Compile error!

// any: assignable to anything
const a: any = "hello";
const b: number = a;   // OK
const c: string = a;   // OK
const d: boolean = a;  // OK

// unknown: NOT assignable to anything (except unknown and any)
const u: unknown = "hello";
// const b: number = u;   // Error
// const c: string = u;   // Error
// const d: boolean = u;  // Error
const e: unknown = u;   // OK (unknown is assignable to unknown)

// any: can call methods directly
const a2: any = "hello";
a2.toUpperCase();  // OK
a2.foo.bar.baz();  // OK (no error, but runtime crash)

// unknown: cannot call methods without narrowing
const u2: unknown = "hello";
// u2.toUpperCase(); // Error
if (typeof u2 === "string") {
  u2.toUpperCase(); // OK
}
```

---

## The never Type

`never` is the **bottom type** in TypeScript — it represents values that never occur. A function that never returns (throws or has infinite loop) has return type `never`.

### Functions That Never Return

```typescript
// Function that always throws
function throwError(message: string): never {
  throw new Error(message);
}

// Function with infinite loop
function infiniteLoop(): never {
  while (true) {
    // This function never returns
  }
}

// Function that never completes
function neverResolves(): never {
  return new Promise(() => {}); // Promise that never resolves
}

// Type narrowing to never through exhaustive checking
function getArea(shape: "circle" | "square"): number {
  switch (shape) {
    case "circle":
      return Math.PI * 10 * 10;
    case "square":
      return 10 * 10;
    default:
      const _exhaustive: never = shape; // OK — all cases handled
      return _exhaustive;
  }
}

// If you add a new shape to the union but forget to handle it:
// type Shape = "circle" | "square" | "triangle";
// default: const _exhaustive: never = shape;
// Error: Type '"triangle"' is not assignable to type 'never'
// This catches missing cases at compile time!
```

### never in Conditional Types

```typescript
// never in conditional types removes members from unions
type Exclude<T, U> = T extends U ? never : T;

type Result = Exclude<"a" | "b" | "c", "a">;
// "b" | "c"

// never in mapped types
type NonNullable2<T> = T extends null | undefined ? never : T;

type Clean = NonNullable2<string | null | undefined | number>;
// string | number

// never as the result of a conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false
type C = IsString<string>;  // true (string includes all string literals)

// Distributive conditional types with never
type ToArray<T> = T extends any ? T[] : never;

type StrArr = ToArray<string | number>; // string[] | number[]
// (distributes over the union)

// Using never to filter types
type FilterByType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

interface User {
  name: string;
  age: number;
  email: string;
  isActive: boolean;
}

type StringKeys = FilterByType<User, string>;
// "name" | "email"

type NumberKeys = FilterByType<User, number>;
// "age"
```

### never vs void

```typescript
// never: function NEVER returns (throws, infinite loop, or terminates the process)
function throwError(msg: string): never {
  throw new Error(msg);
}

function processForever(): never {
  while (true) {}
}

// void: function returns undefined (or nothing)
function logMessage(msg: string): void {
  console.log(msg);
  // implicit return of undefined
}

function explicitVoid(): void {
  return undefined; // OK — explicit undefined
  // return 42;     // Error: Type 'number' is not assignable to type 'void'
}

// A function typed as () => void CAN return a value, but it's ignored
const fn: () => void = () => 42; // OK — return value is discarded
// A function typed as () => never CANNOT return at all
// const neverFn: () => never = () => 42; // Error: never cannot return
```

### never in Type Utilities

```typescript
// never is used extensively in built-in utility types

// Readonly — never in the value mapping
type Readonly<T> = { readonly [P in keyof T]: T[P] };

// Pick — never for keys not in the pick list
type Pick<T, K extends keyof T> = { [P in K]: T[P] };

// Omit — uses Exclude with never
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;

// Record — the value type can be never to create empty objects
type Empty = Record<string, never>;
const empty: Empty = {}; // Only empty object is allowed
// empty.foo = "bar";    // Error: Property 'foo' does not exist

// Extract — returns never for non-matching types
type Extract<T, U> = T extends U ? T : never;

type Numbers = Extract<string | number | boolean, number>;
// number

type Nothing = Extract<string, number>;
// never
```

### never in Union and Intersection

```typescript
// never is the identity element for unions (like 0 for addition)
type A = string | never;        // string (never disappears from unions)
type B = number | never | boolean; // number | boolean

// never is the annihilator for intersections (like 0 for multiplication)
type C = string & never;        // never
type D = { a: string } & never; // never

// This makes never useful as a "filter" in conditional types
type Without<T, U> = T extends U ? never : T;
type Result = Without<"a" | "b" | "c", "a" | "b">;
// "c"
```

---

## The void Type

`void` represents the absence of a return value. It's the return type of functions that don't return anything.

### Basic Usage

```typescript
// void as return type
function logMessage(message: string): void {
  console.log(message);
  // No return statement needed
}

function setConfig(key: string, value: string): void {
  document.title = value;
}

// void in type positions
type Callback = () => void;
type Processor = (input: string) => void;

// void in generics
const numbers: Array<void> = []; // Not useful, but valid

// void vs undefined
function returnsVoid(): void {
  console.log("hello");
  // No return — implicit undefined, but type is void
}

function returnsUndefined(): undefined {
  console.log("hello");
  return undefined; // Must explicitly return undefined
}
```

### void in Callback Position

```typescript
// () => void means "we don't care about the return value"
// This is different from () => undefined

// When used as a callback type, the return value is ignored
const numbers = [1, 2, 3];

// map expects (value: number, index: number) => U
// If we use () => void, the return type is void
const voidMapped = numbers.map((n): void => {
  console.log(n);
  // return 42; // Error: void functions shouldn't return a value
});

// But if we use () => any, we can return anything
const anyMapped = numbers.map((n) => {
  console.log(n);
  return n * 2; // OK — but the return type is inferred as number
});

// The key insight: () => void accepts functions that return ANYTHING
function invokeCallback(callback: () => void): void {
  callback();
}

invokeCallback(() => 42);            // OK — return value is ignored
invokeCallback(() => "hello");       // OK
invokeCallback(() => { return {}; }); // OK

// This is why array methods work with void-typed callbacks
const arr = [1, 2, 3];
arr.forEach((item): void => {
  console.log(item * 2); // forEach callback type expects () => void
});
```

---

## Comparison Table

| Feature                    | `any`              | `unknown`          | `never`                 | `void`              |
|----------------------------|--------------------|--------------------|-------------------------|---------------------|
| Can assign anything to it? | ✅ Yes             | ✅ Yes             | ❌ No (bottom type)     | ❌ No               |
| Can assign it to anything? | ✅ Yes             | ❌ No (must narrow) | ✅ Yes (bottom type)    | ❌ No (only void)   |
| Can use methods?           | ✅ Yes (no check)  | ❌ No (must narrow) | N/A (no values)         | ❌ No               |
| Type safety                | ❌ None            | ✅ Full            | ✅ Full                 | ✅ Full             |
| Runtime values             | Any value          | Any value          | No values               | `undefined`         |
| Common use case            | Migration/FFI      | API boundaries     | Exhaustive checking     | No return value     |
| Compile-time errors?       | ❌ No              | ✅ Yes             | ✅ Yes                  | ✅ Yes              |
| Acceptable in production?  | ❌ Rarely          | ✅ Yes             | ✅ Yes                  | ✅ Yes              |

---

## Best Practices

1. **Enable `noImplicitAny`** and `strictNullChecks` in every project
2. **Use `unknown` instead of `any`** when you don't know the type — it forces narrowing
3. **Use `any` only** during JavaScript-to-TypeScript migration or with untyped third-party code
4. **Use `never`** for exhaustive checking in switch statements and conditional types
5. **Use `void`** for function return types where the return value is intentionally unused
6. **Don't use `void` as a variable type** — use `undefined` or `null` instead
7. **Prefer `unknown` + type guards** over `any` + type assertions
8. **Use `never` as a filter** in conditional types to remove members from unions
9. **Remember:** `never` is assignable to every type, but no type (except `never`) is assignable to `never`
10. **Use `void` in callback types** when you don't care about the return value

---

## Interview Questions

### Q1: What is the difference between `any` and `unknown`?

**Answer:** `any` disables all type checking — you can assign it to anything and call any methods on it without errors. `unknown` accepts any value but requires type narrowing before use. `unknown` is the type-safe alternative to `any`.

```typescript
const a: any = "hello";
a.toUpperCase(); // OK
a.foo.bar();      // OK (runtime crash)

const u: unknown = "hello";
// u.toUpperCase(); // Error — must narrow first
if (typeof u === "string") {
  u.toUpperCase(); // OK
}
```

### Q2: When would you use `never`?

**Answer:** `never` is used for:
- Functions that never return (always throw or have infinite loops)
- Exhaustive checking in switch statements (compile error if a case is missing)
- Conditional types that filter out types (e.g., `Exclude<T, U>` uses `never` to remove matching types)
- Representing impossible states in type systems

### Q3: What is a discriminated union?

**Answer:** A discriminated union is a union of object types that share a common discriminant property (a literal type field). TypeScript uses the discriminant to narrow the union:

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
  }
}
```

### Q4: What is the bottom type in TypeScript?

**Answer:** `never` is the bottom type — it represents values that never exist. Every type is assignable to `never` (vacuously true), but `never` is not assignable to any type (except `never` and `any`). It's useful for exhaustive checking and type-level computation.

### Q5: Can `void` and `undefined` be used interchangeably?

**Answer:** No. `void` is the return type of functions that don't return a value. `undefined` is a specific value. A function typed as `() => void` can return any value (it's ignored), but `() => undefined` must explicitly return `undefined`. Use `void` for callback return types where the value is intentionally unused.

### Q6: What is `noImplicitAny`?

**Answer:** A TypeScript compiler option that prevents variables, parameters, and return types from being implicitly typed as `any`. When enabled, every declaration must have an explicit type annotation or be inferrable. This catches bugs where TypeScript would silently allow any operation on untyped values.
