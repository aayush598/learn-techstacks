# Advanced TypeScript Types: Interview Questions

40+ interview questions with detailed answers covering all advanced TypeScript type topics. Organized by category for focused preparation.

---

## Table of Contents

1. [Type Narrowing Questions](#type-narrowing)
2. [Discriminated Unions Questions](#discriminated-unions)
3. [Exhaustive Checking Questions](#exhaustive-checking)
4. [Indexed Access & keyof Questions](#indexed-access--keyof)
5. [typeof & infer Questions](#typeof--infer)
6. [Recursive Types Questions](#recursive-types)
7. [Branded Types Questions](#branded-types)
8. [Maybe Types Questions](#maybe-types)
9. [Utility Types Questions](#utility-types)
10. [Type Compatibility Questions](#type-compatibility)
11. [General Advanced Types Questions](#general-advanced-types)

---

## Type Narrowing

### Q1: What is type narrowing in TypeScript?

**Answer:** Type narrowing is the process of transforming a broad type (like a union or `unknown`) into a more specific type within a conditional branch. TypeScript's compiler automatically narrows types through control flow analysis using runtime checks like `typeof`, `instanceof`, `in`, equality comparisons, and user-defined type guards (`is`).

```typescript
function process(value: string | number) {
  if (typeof value === "string") {
    // value is narrowed to string here
    return value.toUpperCase();
  }
  // value is narrowed to number here
  return value.toFixed(2);
}
```

### Q2: What are user-defined type guards and when do you use them?

**Answer:** User-defined type guard functions use the `is` keyword in their return type to narrow types. They're used when built-in narrowing (typeof, instanceof, in) isn't sufficient for complex conditions.

```typescript
interface Cat { meow(): void; }
interface Dog { bark(): void; }

function isCat(animal: Cat | Dog): animal is Cat {
  return "meow" in animal;
}

function handle(animal: Cat | Dog) {
  if (isCat(animal)) {
    animal.meow(); // narrowed to Cat
  } else {
    animal.bark(); // narrowed to Dog
  }
}
```

### Q3: What is the difference between `is` type guards and assertion functions?

**Answer:** Type guards (`is`) return a boolean and narrow the type in the calling scope's conditional branch. Assertion functions (`asserts`) don't return — they throw on failure and narrow the type for the rest of the function scope.

```typescript
// Type guard
function isString(x: unknown): x is string {
  return typeof x === "string";
}

// Assertion function
function assertString(x: unknown): asserts x is string {
  if (typeof x !== "string") throw new Error("Expected string");
}
```

### Q4: Can you narrow `unknown` to a specific type?

**Answer:** Yes. `unknown` is the type-safe counterpart to `any`. You must narrow it before using it. Use `typeof`, `instanceof`, `in`, or type guards to narrow.

```typescript
function process(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase()); // narrowed to string
  } else if (typeof value === "number") {
    console.log(value.toFixed(2)); // narrowed to number
  }
}
```

---

## Discriminated Unions

### Q5: What is a discriminated union?

**Answer:** A discriminated union is a union of types that share a common property (the discriminant) with a unique literal type. TypeScript uses this discriminant to narrow the union to the correct variant in switch/if-else blocks.

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

### Q6: Why are discriminated unions better than interfaces with optional properties?

**Answer:** Discriminated unions eliminate impossible states — each variant is self-contained. Optional properties can combine in nonsensical ways (both `data` and `error` present). Discriminated unions also enable exhaustive checking with `never`.

```typescript
// ❌ Optional properties — allows impossible states
type Result = { data?: string; error?: string }; // both can be present

// ✅ Discriminated union — impossible states eliminated
type Result =
  | { status: "ok"; data: string }
  | { status: "error"; error: string };
```

### Q7: How do discriminated unions work with React?

**Answer:** Discriminated unions model component state, props, and events cleanly. Each state variant has exactly the properties needed, and the discriminant determines which variant is active.

```typescript
type ConnectionState =
  | { status: "disconnected" }
  | { status: "connecting"; attempt: number }
  | { status: "connected"; socketId: string }
  | { status: "error"; error: Error };

function ConnectionStatus({ state }: { state: ConnectionState }) {
  switch (state.status) {
    case "disconnected": return <p>Disconnected</p>;
    case "connecting": return <p>Attempt {state.attempt}...</p>;
    case "connected": return <p>Connected: {state.socketId}</p>;
    case "error": return <p>Error: {state.error.message}</p>;
  }
}
```

---

## Exhaustive Checking

### Q8: What is exhaustive checking and how does it work?

**Answer:** Exhaustive checking uses the `never` type to ensure all cases in a union type are handled. A helper function `exhaustiveCheck(x: never)` is placed in the default case of a switch. If a new union member is added but not handled, TypeScript raises a compile error because the remaining type isn't `never`.

```typescript
function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled: ${x}`);
}

type Status = "active" | "inactive" | "pending";

function handle(status: Status) {
  switch (status) {
    case "active": return "active";
    case "inactive": return "inactive";
    case "pending": return "pending";
    default: return exhaustiveCheck(status);
  }
}
```

### Q9: Why does `never` work for exhaustive checking?

**Answer:** `never` is the bottom type — no value can be assigned to it. When all union members are handled, the remaining type is `never`. If a case is missed, the remaining type is NOT `never`, and assigning it to `never` causes a compile error. This catches missing cases at compile time.

### Q10: Can you use exhaustive checking with if-else?

**Answer:** Yes, though switch is more common. You can assign the narrowed type to a variable typed as `never` in the final else branch.

```typescript
type Shape = { kind: "circle" } | { kind: "square" };

function process(shape: Shape) {
  let result: never;
  if (shape.kind === "circle") {
    // handle circle
  } else {
    result = shape; // error if square is not the only remaining type
  }
}
```

---

## Indexed Access & keyof

### Q11: How does `keyof` work?

**Answer:** `keyof` is a type operator that produces a union of string literal types representing the keys of a given type. For `type User = { id: number; name: string }`, `keyof User` is `"id" | "name"`.

```typescript
type User = { id: number; name: string; email: string };
type UserKeys = keyof User; // "id" | "name" | "email"

// Used with generics for type-safe access
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Q12: What is `T[P]` (indexed access type)?

**Answer:** Indexed access types extract the type of a specific property from an object type using bracket notation. `User["name"]` returns the type of the `name` property. You can use unions as keys: `User["name" | "email"]` returns `string | string = string`.

```typescript
type User = { id: number; name: string; email: string };
type NameType = User["name"]; // string
type IdOrName = User["id" | "name"]; // number | string
type AllValues = User[keyof User]; // number | string
```

### Q13: What is the `keyof typeof` pattern?

**Answer:** `keyof typeof obj` extracts the keys of a runtime object as a union of string literal types. It's used when you have a const object and want to extract its keys as a type without manually defining them.

```typescript
const ROUTES = {
  home: "/",
  about: "/about",
  blog: "/blog",
} as const;

type RouteKey = keyof typeof ROUTES; // "home" | "about" | "blog"
```

### Q14: How do you get all values of an object type?

**Answer:** Use `T[keyof T]`. For `User = { id: number; name: string }`, `User[keyof User]` returns `number | string`.

---

## typeof & infer

### Q15: What is the difference between `typeof` in JavaScript and TypeScript?

**Answer:** JavaScript `typeof` is a runtime operator returning strings like `"string"`, `"number"`, `"object"`. TypeScript `typeof` is a compile-time type query that extracts the type of a variable or expression for use in type positions.

### Q16: What does the `infer` keyword do?

**Answer:** `infer` declares a type variable within a conditional type. It captures and names a type from a specific position in the conditional type's extends clause.

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type A = ReturnType<() => string>; // string
type B = ReturnType<(x: number) => boolean>; // boolean
```

### Q17: Can you use multiple `infer` in one conditional type?

**Answer:** Yes. Each `infer` captures a different type from the expression.

```typescript
type FunctionInfo<T> = T extends (a: infer P, b: infer Q) => infer R
  ? { params: [P, Q]; return: R }
  : never;

type Info = FunctionInfo<(name: string, age: number) => boolean>;
// { params: [string, number]; return: boolean }
```

### Q18: How do you extract a Promise's resolved type?

**Answer:** Use `infer` in a conditional type:

```typescript
type UnwrapPromise<T> = T extends Promise<infer U> ? UnwrapPromise<U> : T;

type A = UnwrapPromise<Promise<string>>; // string
type B = UnwrapPromise<Promise<Promise<number>>>; // number
```

---

## Recursive Types

### Q19: What are recursive types in TypeScript?

**Answer:** Recursive types reference themselves. They're used for naturally recursive data structures (trees, linked lists, nested objects) and for type-level computation (flattening tuples, string manipulation).

```typescript
type LinkedList<T> = {
  value: T;
  next: LinkedList<T> | null;
};

type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };
```

### Q20: How do you implement DeepPartial?

**Answer:** Use a recursive mapped type:

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;
```

This makes all properties optional at every level of nesting.

### Q21: How do you generate type-safe paths for nested objects?

**Answer:** Use recursive template literal types:

```typescript
type Path<T, P extends string = ""> = T extends object
  ? { [K in keyof T & string]: T[K] extends object
      ? Path<T[K], `${P}${K}.`>
      : `${P}${K}`
  }[keyof T & string]
  : never;
```

---

## Branded Types

### Q22: What are branded types?

**Answer:** Branded types add a phantom property to a type so structurally identical types are treated as different. They emulate nominal typing in TypeScript's structural system.

```typescript
declare const __brand: unique symbol;
type Brand<T, B> = T & { readonly [__brand]: B };

type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;
```

### Q23: How do you create branded types with Zod?

**Answer:** Use the `.brand()` method:

```typescript
import { z } from "zod";

const UserId = z.string().brand<"UserId">();
type UserId = z.infer<typeof UserId>;

const userId = UserId.parse("user-123"); // UserId
```

### Q24: When should you use branded types?

**Answer:** Use branded types for domain-specific IDs (UserId vs PostId), money (USD vs EUR), email, URL, and any case where structural equivalence is incorrect and could cause bugs.

### Q25: Do branded types have runtime overhead?

**Answer:** No. The phantom property is erased at compile time. The only runtime cost is in the factory/validation function, which is explicit and intentional.

---

## Maybe Types

### Q26: What is the difference between `null` and `undefined`?

**Answer:** `undefined` means "not assigned" or "missing" (optional parameters, missing properties). `null` means "intentionally empty" or "no value" (cleared references, search results). TypeScript treats both similarly with `??`, but `||` distinguishes them.

### Q27: What is the difference between `??` and `||`?

**Answer:** `??` (nullish coalescing) returns the right operand only for `null` or `undefined`. `||` (logical OR) returns the right operand for any falsy value, including `0`, `""`, and `false`. Use `??` to preserve falsy values like `0` or `""`.

```typescript
const a = 0 || "default";   // "default"
const b = 0 ?? "default";   // 0
const c = "" || "default";  // "default"
const d = "" ?? "default";  // ""
```

### Q28: How does optional chaining work?

**Answer:** Optional chaining (`?.`) short-circuits and returns `undefined` if the left operand is `null` or `undefined`. It works for property access, method calls, and element access.

```typescript
const city = user?.address?.city;
const result = arr?.[0]?.name;
const value = obj?.method?.();
```

---

## Utility Types

### Q29: What is the difference between Partial and Required?

**Answer:** `Partial<T>` makes all properties optional (adds `?`). `Required<T>` makes all properties required (removes `?`). They are inverses.

### Q30: Are Partial, Required, and Readonly shallow or deep?

**Answer:** All three are shallow — they only affect top-level properties. `Readonly<{ a: { b: string } }>` makes `a` readonly but `a.b` is still mutable. You need custom deep versions (DeepPartial, DeepReadonly) for recursive transformations.

### Q31: What is the difference between Pick and Omit?

**Answer:** `Pick<T, K>` selects specific properties from T. `Omit<T, K>` removes specific properties from T. They are inverses: `Omit<T, K>` is equivalent to `Pick<T, Exclude<keyof T, K>>`.

### Q32: When would you use Record?

**Answer:** `Record<K, V>` creates a type with specific keys and a uniform value type. Use it for dictionaries, status maps, configuration objects, and any key-value mapping where you know the keys at compile time.

### Q33: How do you replace a property type in an existing interface?

**Answer:** Use Omit and intersection:
```typescript
type NewType = Omit<OriginalType, "prop"> & { prop: NewType };
```

---

## Type Compatibility

### Q34: What is structural typing?

**Answer:** Structural typing means types are compatible based on their shape (properties and methods), not their names. If two types have the same structure, they're interchangeable, regardless of their names or explicit declarations.

### Q35: What is the difference between `any` and `unknown`?

**Answer:** `any` is compatible with everything — assignable to and from any type. It disables type checking. `unknown` is assignable from everything but requires narrowing before use. Always prefer `unknown` over `any`.

### Q36: What is function parameter bivariance?

**Answer:** Bivariance means function parameters are compatible in both directions — a function with a broader parameter type can be assigned to one with a narrower type and vice versa. TypeScript uses this for pragmatic callback compatibility, but `--strictFunctionTypes` makes parameters contravariant.

### Q37: How does `never` work with assignability?

**Answer:** `never` is assignable to every type (bottom type) but nothing is assignable to `never` (except `never` itself). This makes `never` useful for exhaustive checking — if all cases are handled, the remaining type is `never`.

### Q38: What is the excess property check?

**Answer:** When you assign an object literal directly to a type, TypeScript checks for extra properties. This prevents typos. But if you assign through a variable, extra properties are allowed (fresh object literal checking).

---

## General Advanced Types

### Q39: When would you use a type assertion (`as`) vs a type guard?

**Answer:** Type guards are safer — they verify the type at runtime. Use type assertions only when you have information the compiler doesn't (and you're certain about the type). Type guards should be preferred in most cases.

### Q40: How do you create a type-safe event emitter?

**Answer:** Use a mapped type with keyof for type-safe events:

```typescript
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string };
};

class TypedEmitter<Events extends Record<string, any>> {
  on<K extends keyof Events>(event: K, handler: (payload: Events[K]) => void) { ... }
  emit<K extends keyof Events>(event: K, payload: Events[K]) { ... }
}
```

### Q41: What is the `as const` assertion and when do you use it?

**Answer:** `as const` makes values deeply readonly and narrows literal types. Use it for enum-like constants, route definitions, and any case where you want literal types instead of widened types.

```typescript
const STATUS = { loading: "LOADING", success: "SUCCESS" } as const;
type Status = typeof STATUS[keyof typeof STATUS]; // "LOADING" | "SUCCESS"
```

### Q42: How do you implement a type-safe pipe function?

**Answer:** Use recursive conditional types with infer:

```typescript
type Pipe<T extends any[]> =
  T extends [(x: infer A) => infer B, ...infer Rest]
    ? Rest extends [(x: B) => any, ...any[]]
      ? [T[0], ...Pipe<Rest>]
      : [T[0]]
    : [];

function pipe<T extends ((x: any) => any)[]>(
  ...fns: T
): (x: Parameters<T[0]>[0]) => ReturnType<T[T["length"] - 1]> {
  return (x) => fns.reduce((acc, fn) => fn(acc), x) as any;
}
```

### Q43: What is the difference between `type` and `interface` for advanced types?

**Answer:** `type` supports unions, intersections, mapped types, conditional types, and computed properties. `interface` supports declaration merging, `extends`, and is generally better for object shapes. Use `type` for advanced type manipulation; use `interface` for object contracts.

### Q44: How do you type a Redux reducer with discriminated unions?

**Answer:** Define a discriminated union for actions and use exhaustive checking:

```typescript
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT": return state + action.amount;
    case "DECREMENT": return state - action.amount;
    case "RESET": return 0;
    default: return exhaustiveCheck(action);
  }
}
```

### Q45: How do you type a function that accepts any number of arguments of the same type?

**Answer:** Use rest parameters with a tuple type:

```typescript
function sum(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

// Or with a generic constraint:
function merge<T extends Record<string, any>>(
  ...objects: T[]
): T {
  return Object.assign({}, ...objects);
}
```

### Q46: What is the `satisfies` operator?

**Answer:** The `satisfies` operator (TypeScript 4.9+) validates that an expression matches a type without widening it. It checks the type but preserves the original literal types.

```typescript
const routes = {
  home: "/",
  about: "/about",
} satisfies Record<string, string>;

// Type is { home: "/"; about: "/about" } — literals preserved!
type Keys = keyof typeof routes; // "home" | "about"
```

### Q47: How do you type a generic API response handler?

**Answer:** Use discriminated unions with generics:

```typescript
type ApiResponse<T> =
  | { status: "success"; data: T; statusCode: 200 }
  | { status: "error"; message: string; statusCode: number };

async function fetchApi<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  if (response.ok) {
    return { status: "success", data: await response.json(), statusCode: 200 };
  }
  return { status: "error", message: response.statusText, statusCode: response.status };
}
```

### Q48: How do you create a type-safe builder pattern?

**Answer:** Use chained mapped types with `this` return types:

```typescript
class QueryBuilder<T extends Record<string, any>> {
  private filters: Partial<T> = {};

  where<K extends keyof T>(key: K, value: T[K]): this {
    this.filters[key] = value;
    return this;
  }

  build(): T {
    return this.filters as T;
  }
}
```
