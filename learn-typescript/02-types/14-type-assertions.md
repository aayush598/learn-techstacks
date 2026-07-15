# Type Assertions in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [as Syntax](#as-syntax)
3. [Angle Bracket Syntax](#angle-bracket-syntax)
4. [Type Assertions vs Type Guards](#type-assertions-vs-type-guards)
5. [When to Use Assertions](#when-to-use-assertions)
6. [as const](#as-const)
7. [satisfies Operator](#satisfies-operator)
8. [Double Assertions](#double-assertions)
9. [Non-Null Assertion (!)](#non-null-assertion)
10. [Assertion Functions](#assertion-functions)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

Type assertions tell TypeScript to treat a value as a specific type. They are compile-time hints that don't affect runtime behavior.

```typescript
// Without assertion: error
const input = document.getElementById("name");
// input is HTMLElement | null
// input.value; // Error: 'value' does not exist on 'HTMLElement | null'

// With assertion: no error
const input2 = document.getElementById("name") as HTMLInputElement;
input2.value; // OK — treated as HTMLInputElement
```

**Type assertions are NOT type checks — they are promises to the compiler.**

---

## as Syntax

The `as` keyword is the modern, preferred way to assert types.

```typescript
// Basic as assertion
const value = "hello" as string;
const num = 42 as number;

// Asserting to a more specific type
const element = document.getElementById("app") as HTMLDivElement;
const input = document.querySelector("input") as HTMLInputElement;
const canvas = document.querySelector("canvas") as HTMLCanvasElement;

// Asserting unknown to a specific type
const data: unknown = JSON.parse('{"name": "Alice"}');
const user = data as { name: string; age: number };
console.log(user.name);

// Asserting union to a specific member
type StringOrNumber = string | number;
const value2: StringOrNumber = "hello";
const str = value2 as string; // OK

// Asserting in function return
function fetchData(): { name: string; age: number } {
  const response = JSON.parse('{"name": "Alice", "age": 30}');
  return response as { name: string; age: number };
}

// Asserting with as const
const direction = "up" as const; // type: "up" (not string)
const numbers = [1, 2, 3] as const; // type: readonly [1, 2, 3]

// Asserting in type positions
const config = {
  host: "localhost",
  port: 3000,
} as { host: string; port: number; debug: boolean };
// ⚠️ This doesn't add the debug property — it just changes the type
// config.debug; // Type says it exists, but runtime says it doesn't!

// Asserting with multiple types
const value3 = "hello" as string | number; // OK
const value4 = 42 as string | number;      // OK
```

---

## Angle Bracket Syntax

The legacy syntax using angle brackets. Only works in `.tsx` files with `as`.

```typescript
// Angle bracket syntax (legacy)
const value = <string>"hello";
const num = <number>42;

// ⚠️ Cannot use in .tsx files (conflicts with JSX syntax)
// In React components, <string> would be interpreted as a JSX element

// Modern code should always use `as` syntax
// The angle bracket syntax is considered deprecated

// Comparison
const a = <string>"hello"; // Angle bracket
const b = "hello" as string; // as syntax (preferred)

// Angle bracket with complex types
const user = <{ name: string; age: number }>{
  name: "Alice",
  age: 30,
};

// The `as` syntax is equivalent and preferred
const user2 = {
  name: "Alice",
  age: 30,
} as { name: string; age: number };
```

---

## Type Assertions vs Type Guards

```typescript
// Type assertion: compile-time only (NO runtime check)
const value: unknown = "hello";
const str = value as string;
// If value is actually a number, this will crash at runtime!

// Type guard: runtime check + compile-time narrowing
function isString(value: unknown): value is string {
  return typeof value === "string";
}

if (isString(value)) {
  // Safe! Runtime check verified the type
  console.log(value.toUpperCase());
}

// Comparison
function processValue(value: unknown): string {
  // ❌ Assertion (unsafe)
  // const str = value as string;
  // return str.toUpperCase(); // Might crash!

  // ✅ Type guard (safe)
  if (typeof value === "string") {
    return value.toUpperCase(); // Verified at runtime
  }
  return "N/A";
}

// When assertions are OK:
// 1. You know the type from context (DOM queries, JSON parsing)
// 2. You've verified the type elsewhere
// 3. The value is from a well-known source

// When to use type guards:
// 1. Processing unknown data (API responses, user input)
// 2. Working with union types
// 3. When you can't guarantee the type
```

---

## When to Use Assertions

```typescript
// 1. DOM queries (most common)
const element = document.getElementById("app") as HTMLDivElement;
const input = document.querySelector("input[type='text']") as HTMLInputElement;

// Better alternative: use the assertion function pattern
function getElement<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Element #${id} not found`);
  return element as T;
}

const app = getElement<HTMLDivElement>("app");

// 2. JSON parsing
const data = JSON.parse('{"name": "Alice"}') as { name: string; age: number };

// Better alternative: use a validation library (zod, io-ts)
import { z } from "zod";

const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
});

type User = z.infer<typeof UserSchema>;

// 3. Third-party library results
const result = someLibrary.doSomething() as MyType;

// 4. Testing (mock data)
const mockUser = {
  id: 1,
  name: "Test User",
  email: "test@example.com",
} as User;

// 5. Working with any
const legacyData: any = getLegacyData();
const typedData = legacyData as SpecificType;

// 6. Assertion in return type
function createState() {
  return {
    count: 0,
    increment: () => {},
    decrement: () => {},
  } as State; // Asserting to a well-defined interface
}
```

---

## as const

The `as const` assertion makes values as narrow and immutable as possible.

```typescript
// Basic as const
const x = "hello" as const; // type: "hello" (not string)
const y = 42 as const;      // type: 42 (not number)
const z = true as const;    // type: true (not boolean)

// Object as const (deep readonly with literal types)
const config = {
  host: "localhost",
  port: 3000,
} as const;
// type: { readonly host: "localhost"; readonly port: 3000 }

// Array as const (readonly tuple with literal types)
const colors = ["red", "green", "blue"] as const;
// type: readonly ["red", "green", "blue"]
type Color = (typeof colors)[number]; // "red" | "green" | "blue"

// Nested as const
const api = {
  baseUrl: "https://api.example.com",
  endpoints: {
    users: "/users",
    posts: "/posts",
  },
} as const;
// Fully readonly with literal types

// as const in function parameters
function move(direction: "up" | "down" | "left" | "right"): void {
  console.log(`Moving ${direction}`);
}

const dir = "up" as const;
move(dir); // OK — "up" is assignable to the union

// as const with enum-like patterns
const HttpStatus = {
  OK: 200,
  NotFound: 404,
  ServerError: 500,
} as const;

type HTTPStatus = (typeof HttpStatus)[keyof typeof HttpStatus]; // 200 | 404 | 500

// as const with arrays
const ROUTES = ["/users", "/posts", "/comments"] as const;
type Route = (typeof ROUTES)[number]; // "/users" | "/posts" | "/comments"

// as const with functions
const createLogger = () => ({
  log: (msg: string) => console.log(msg),
  error: (msg: string) => console.error(msg),
} as const);

// as const vs regular assertion
const a = [1, 2, 3];         // number[]
const b = [1, 2, 3] as const; // readonly [1, 2, 3]

const c = { x: 1 };         // { x: number }
const d = { x: 1 } as const; // { readonly x: 1 }
```

---

## satisfies Operator

TypeScript 4.9+ — validates that a value matches a type while preserving the narrow type.

```typescript
// satisfies validates without widening
const config = {
  host: "localhost",
  port: 3000,
} satisfies Record<string, string | number>;
// config.host is "localhost" (literal), not string
// config.port is 3000 (literal), not number

// Without satisfies (type annotation widens)
const config2: Record<string, string | number> = {
  host: "localhost",
  port: 3000,
};
// config2.host is string (widened!)
// config2.port is number (widened!)

// satisfies with union types
type Color = "red" | "green" | "blue";

const color = "red" satisfies Color;
// color is "red" (not Color)

// satisfies with complex types
type Theme = {
  colors: {
    primary: string;
    secondary: string;
  };
  fonts: string[];
};

const theme = {
  colors: {
    primary: "#000",
    secondary: "#fff",
  },
  fonts: ["Arial", "sans-serif"],
} satisfies Theme;
// theme.colors.primary is "#000" (literal)
// Without satisfies, it would be string

// satisfies with readonly
const readOnlyArray = [1, 2, 3] satisfies readonly number[];
// preserved as number[] (not widened)

// satisfies for enum-like objects
const HttpStatus = {
  OK: 200,
  NotFound: 404,
} satisfies Record<string, number>;

// HttpStatus.OK is 200 (literal)

// satisfies vs as
const a2 = "hello" as string;    // "hello" → string (widened)
const b2 = "hello" satisfies string; // "hello" stays "hello" (narrow)

// satisfies vs type annotation
type Status = "active" | "inactive";
const s1: Status = "active";     // "active" → Status (widened)
const s2 = "active" satisfies Status; // "active" stays "active" (narrow)
```

---

## Double Assertions

Going through `unknown` to assert between incompatible types.

```typescript
// Direct assertion between incompatible types (error)
// const str = "hello" as number; // Error: Conversion may be a mistake

// Double assertion through unknown (works but unsafe)
const str = "hello" as unknown as number; // OK
// This is almost always a bug — avoid it!

// When double assertions might be OK:
// 1. Migrating between incompatible types
// 2. Working with external APIs that return unexpected types
// 3. Testing edge cases

// Better alternatives:
// 1. Use type guards
// 2. Use unknown + narrowing
// 3. Use a validation library

// Example of when double assertion is dangerous
const value = "hello" as unknown as number;
// value.toFixed(2); // Runtime error! "hello" is not a number
```

---

## Non-Null Assertion (!)

The `!` operator tells TypeScript that a value is not null or undefined.

```typescript
// Basic non-null assertion
function processElement(element: HTMLElement | null): void {
  element!.className; // Asserts element is not null
  // But might crash at runtime if element IS null!
}

// Better: use a guard
function processElement2(element: HTMLElement | null): void {
  if (element) {
    element.className; // Safe — type narrowed
  }
}

// Non-null assertion in property access
interface Config {
  db?: {
    host?: string;
    port?: number;
  };
}

function getHost(config: Config): string {
  return config.db!.host!; // Multiple non-null assertions
  // Dangerous! Multiple potential null points
}

// Better: optional chaining
function getHost2(config: Config): string {
  return config.db?.host ?? "localhost";
}

// Non-null assertion after a check
function process(value: string | null): void {
  if (value !== null) {
    value.toUpperCase(); // Safe — narrowed
  }
  // value!.toUpperCase(); // Also works after the check, but redundant
}

// Non-null assertion in assertions
function assertDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Value is null or undefined");
  }
}

function processValue(value: string | null): void {
  assertDefined(value);
  value.toUpperCase(); // Safe after assertion
}

// Non-null assertion in for loops
const items: (string | null)[] = ["a", null, "b", null, "c"];
for (const item of items) {
  if (item !== null) {
    console.log(item.toUpperCase()); // Safe
  }
}

// Non-null assertion in map/filter
const strings: (string | null)[] = ["a", null, "b"];
const uppercased = strings
  .filter((s): s is string => s !== null)
  .map((s) => s.toUpperCase()); // Safe
```

---

## Assertion Functions

Functions that narrow types by throwing if the assertion fails.

```typescript
// Basic assertion function
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`Expected string, got ${typeof value}`);
  }
}

function process(value: string | number): string {
  assertIsString(value);
  return value.toUpperCase(); // narrowed to string
}

// Assertion for objects
interface User {
  id: number;
  name: string;
  email: string;
}

function assertIsUser(value: unknown): asserts value is User {
  if (
    typeof value !== "object" ||
    value === null ||
    !("id" in value) ||
    !("name" in value) ||
    !("email" in value)
  ) {
    throw new Error("Invalid user data");
  }
}

// Assertion for arrays
function assertNonEmpty<T>(arr: T[]): asserts arr is [T, ...T[]] {
  if (arr.length === 0) {
    throw new Error("Array is empty");
  }
}

// Assertion for class instances
function assertIsError(value: unknown): asserts value is Error {
  if (!(value instanceof Error)) {
    throw new Error("Expected Error instance");
  }
}

// Assertion for specific values
function assertIsDefined<T>(
  value: T | null | undefined,
  name: string,
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(`${name} is required`);
  }
}

// Usage
function getLength(value: string | null): number {
  assertIsDefined(value, "value");
  return value.length;
}

// Assertion in test code
function expectToBeDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Expected value to be defined");
  }
}

// Assertion in class
class Validator {
  static assertIsNumber(value: unknown): asserts value is number {
    if (typeof value !== "number") {
      throw new Error(`Expected number, got ${typeof value}`);
    }
  }

  static assertIsPositive(value: number): asserts value is number {
    if (value <= 0) {
      throw new Error(`Expected positive number, got ${value}`);
    }
  }
}
```

---

## Best Practices

1. **Prefer type guards over assertions** — they're safer
2. **Use `as` syntax** — avoid angle brackets (they conflict with JSX)
3. **Use `as const`** for literal types from runtime values
4. **Use `satisfies`** to validate types while preserving narrow types
5. **Avoid double assertions** — they're almost always a bug
6. **Avoid non-null assertion (`!`)** — use optional chaining or type guards instead
7. **Use assertion functions** for preconditions in functions
8. **Use `as const`** for enum-like objects instead of actual enums
9. **Document why an assertion is safe** — add a comment explaining the reasoning
10. **Use validation libraries** (zod, io-ts) for external data instead of assertions

---

## Interview Questions

### Q1: What is a type assertion in TypeScript?

**Answer:** A type assertion tells TypeScript to treat a value as a specific type. It's a compile-time hint that doesn't affect runtime behavior. Use `as` syntax: `const str = value as string`. It's unsafe if the value doesn't actually match the asserted type.

### Q2: What is the difference between `as` and angle bracket syntax?

**Answer:** Both do the same thing. `as` is the modern, preferred syntax. Angle brackets (`<string>value`) conflict with JSX in `.tsx` files and are considered deprecated.

### Q3: What is `satisfies` and when would you use it?

**Answer:** `satisfies` (TS 4.9+) validates that a value matches a type while preserving the narrow literal type. Unlike type annotations, it doesn't widen types. Use it when you want type validation without losing literal types.

### Q4: What is `as const`?

**Answer:** A type assertion that makes values as narrow and immutable as possible. Objects become deeply readonly with literal types, arrays become readonly tuples. It's the primary way to get literal types from runtime values.

### Q5: When should you use a type assertion over a type guard?

**Answer:** Use assertions when you have high confidence in the type (DOM queries, JSON parsing from known APIs, testing). Use type guards when processing unknown data, working with unions, or when you can't guarantee the type at runtime.
