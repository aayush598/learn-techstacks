# Enums in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Numeric Enums](#numeric-enums)
3. [String Enums](#string-enums)
4. [Heterogeneous Enums](#heterogeneous-enums)
5. [Computed vs Constant Members](#computed-vs-constant-members)
6. [Reverse Mappings](#reverse-mappings)
7. [Enum as Union Types](#enum-as-union-types)
8. [Const Enums](#const-enums)
9. [Enums vs Unions vs Objects](#enums-vs-unions-vs-objects)
10. [When to Use Enums](#when-to-use-enums)
11. [String Literal Unions as Alternatives](#string-literal-unions-as-alternatives)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## Overview

Enums provide a way to define a set of named constants. TypeScript supports both numeric and string enums, with optional reverse mapping for numeric enums.

---

## Numeric Enums

By default, enums are numeric, starting at 0 and auto-incrementing.

```typescript
// Basic numeric enum (starts at 0)
enum Direction {
  Up,      // 0
  Down,    // 1
  Left,    // 2
  Right,   // 3
}

const dir: Direction = Direction.Up;
console.log(dir); // 0

// Using enum values
function move(direction: Direction): void {
  switch (direction) {
    case Direction.Up:    console.log("Moving up"); break;
    case Direction.Down:  console.log("Moving down"); break;
    case Direction.Left:  console.log("Moving left"); break;
    case Direction.Right: console.log("Moving right"); break;
  }
}

move(Direction.Up); // "Moving up"
move(0);            // Also works (numeric value)
move(Direction.Up as number); // Also works

// Custom starting value
enum HttpStatus {
  OK = 200,
  NotFound = 404,
  InternalServerError = 500,
}
// 201, 405, etc. are NOT auto-generated (only starts from the first member)

// Partial custom values
enum Status {
  Active = 1,
  Inactive,  // 2 (auto-increments from 1)
  Pending,   // 3
  Banned = 10,
  Suspended, // 11 (auto-increments from 10)
}

// All numeric
enum Color {
  Red,     // 0
  Green,   // 1
  Blue,    // 2
}

// Numeric enums are assignable to number
const num: number = Color.Red; // OK
const color: Color = 0; // OK — numeric enums accept numbers!
```

**Important:** Numeric enums accept any number value — this is a known weakness:

```typescript
enum Status {
  Active = 1,
  Inactive = 2,
}

const s: Status = 42; // OK! No compile error
// This is because TypeScript allows numeric enums to be used as flags
```

---

## String Enums

Each member must be initialized with a string value.

```typescript
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

const dir: Direction = Direction.Up;
console.log(dir); // "UP"

// String enums don't accept arbitrary strings
// const d: Direction = "FORWARD"; // Error!

// String enums in switch statements
function move(direction: Direction): string {
  switch (direction) {
    case Direction.Up:    return "Moving up";
    case Direction.Down:  return "Moving down";
    case Direction.Left:  return "Moving left";
    case Direction.Right: return "Moving right";
  }
}

// String enums in objects
const keyBindings: Record<Direction, string> = {
  [Direction.Up]: "W",
  [Direction.Down]: "S",
  [Direction.Left]: "A",
  [Direction.Right]: "D",
};

// String enums with API responses
enum Environment {
  Development = "development",
  Staging = "staging",
  Production = "production",
}

function getApiUrl(env: Environment): string {
  switch (env) {
    case Environment.Development: return "http://localhost:3000";
    case Environment.Staging: return "https://staging.example.com";
    case Environment.Production: return "https://api.example.com";
  }
}
```

---

## Heterogeneous Enums

Mix string and numeric members (generally discouraged):

```typescript
enum Mixed {
  Number = 0,
  String = "hello",
  Boolean = true, // Error: not string or number!
}

// Boolean is not allowed in enums
// Valid enum members are string or number values

// Technically possible but not recommended
enum Weird {
  A = 0,
  B = "string",
  C = 100,
}
```

**Recommendation:** Avoid heterogeneous enums — they make the type harder to reason about.

---

## Computed vs Constant Members

Enum members are either **constant** or **computed**:

```typescript
// Constant members (evaluated at compile time)
enum Constants {
  A,          // constant (auto-incremented)
  B,          // constant
  C = "c",    // constant (string literal)
  D = 100,    // constant (numeric literal)
  E = "e",    // constant
}

// Computed members (evaluated at runtime)
enum Computed {
  A = Math.random(),              // computed
  B = "hello".length,            // computed
  C = 1 + 2,                     // computed (constant expression)
  D = someFunction(),            // computed (function call)
  E = A + 1,                     // computed (depends on another member)
}

function someFunction(): number {
  return 42;
}

// Constant expressions are still constant
enum ConstantExpressions {
  A = 1 + 2,           // constant (3)
  B = "hello" + "world", // constant ("helloworld")
  C = A * 2,           // constant (6)
}

// Computed members can break reverse mapping
enum WithComputed {
  A,              // 0
  B = "string",   // "string"
  C,              // 1 (auto-increments from A=0, not B!)
}
// The auto-increment continues from the last numeric constant
// B is computed (string), so C becomes 1 (0 + 1)
```

**Rule:** A member is constant if its value is a literal, a constant enum member reference, or a constant expression. Everything else is computed.

---

## Reverse Mappings

Numeric enums support reverse mapping (value to name):

```typescript
enum Color {
  Red,   // 0
  Green, // 1
  Blue,  // 2
}

// Forward mapping (name to value)
console.log(Color.Red); // 0

// Reverse mapping (value to name)
console.log(Color[0]); // "Red"
console.log(Color[1]); // "Green"
console.log(Color[2]); // "Blue"

// Reverse mapping in iteration
for (const key in Color) {
  console.log(`${key}: ${Color[key as keyof typeof Color]}`);
}
// Output:
// 0: Red
// 1: Green
// 2: Blue
// Red: 0
// Green: 1
// Blue: 2

// ⚠️ Reverse mapping works for numeric enums only!
enum StringEnum {
  A = "a",
  B = "b",
}
// StringEnum["a"]; // Error: Element implicitly has 'any' type

// Reverse mapping with computed members
enum Mixed {
  A = 0,
  B = "hello",
  C = 10,
}
console.log(Mixed[0]); // "A"
console.log(Mixed[10]); // "C"
// Mixed["hello"] is undefined — no reverse for string members

// Using Object.entries with enums
const colorEntries = Object.entries(Color);
// [["0", "Red"], ["1", "Green"], ["2", "Blue"], ["Red", 0], ["Green", 1], ["Blue", 2]]

// Using Object.keys with enums
const colorKeys = Object.keys(Color);
// ["0", "1", "2", "Red", "Green", "Blue"]
```

---

## Enum as Union Types

TypeScript provides utility types to convert enums to unions.

```typescript
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Pending = "PENDING",
}

// Get enum values as a union
type StatusValues = `${Status}`; // "ACTIVE" | "INACTIVE" | "PENDING"
const s: StatusValues = "ACTIVE"; // OK

// Get enum keys as a union
type StatusKeys = keyof typeof Status; // "Active" | "Inactive" | "Pending"

// Enum values as array
const statusValues: Status[] = Object.values(Status) as Status[];
// ["ACTIVE", "INACTIVE", "PENDING"]

// Enum keys as array
const statusKeys: StatusKeys[] = Object.keys(Status) as StatusKeys[];
// ["Active", "Inactive", "Pending"]

// Iterating over enum values
function getAllStatuses(): Status[] {
  return Object.values(Status) as Status[];
}

// Type-safe enum checking
function isValidStatus(value: string): value is Status {
  return Object.values(Status).includes(value as Status);
}

// Using enums with Record
type StatusConfig = Record<Status, { label: string; color: string }>;
const configs: StatusConfig = {
  [Status.Active]: { label: "Active", color: "green" },
  [Status.Inactive]: { label: "Inactive", color: "gray" },
  [Status.Pending]: { label: "Pending", color: "yellow" },
};
```

---

## Const Enums

Const enums are fully erased at compile time — no JavaScript object is generated.

```typescript
// Regular enum generates JavaScript code
enum RegularEnum {
  A,
  B,
  C,
}
// Compiles to:
// var RegularEnum;
// (function (RegularEnum) {
//   RegularEnum[RegularEnum["A"] = 0] = "A";
//   RegularEnum[RegularEnum["B"] = 1] = "B";
//   RegularEnum[RegularEnum["C"] = 2] = "C";
// })(RegularEnum || (RegularEnum = {}));

// Const enum — no JavaScript output
const enum ConstEnum {
  A,
  B,
  C,
}

// Usage (inlined at compile time)
const x = ConstEnum.A; // Compiles to: const x = 0;
const y = ConstEnum.B; // Compiles to: const y = 1;

// ⚠️ Limitations of const enums
// 1. Cannot use reverse mapping
// const name = ConstEnum[0]; // Error: not allowed

// 2. Cannot be used in computed expressions
// const obj = { [ConstEnum.A]: "value" }; // Error

// 3. Cannot iterate
// for (const key in ConstEnum) { } // Error

// 4. Isolated modules issues
// const enums don't work well with --isolatedModules
// They need the entire enum definition available at compile time

// 5. Cannot be used as type in declaration files
// const enum Foo { A, B }
// declare function bar(x: Foo): void; // Problematic in .d.ts files

// ⚠️ Const enums with string values (TypeScript 5.0+)
const enum StringConstEnum {
  A = "A",
  B = "B",
  C = "C",
}
// These are inlined as string literals
```

**Recommendation:** Avoid `const enum` unless you have a specific performance reason. They cause issues with `--isolatedModules`, bundlers, and declaration file generation.

---

## Enums vs Unions vs Objects

| Feature | Enum | Union of Literals | Object |
|---------|------|-------------------|--------|
| Runtime value | ✅ Yes | ❌ No (type only) | ✅ Yes |
| Tree-shakeable | ❌ No (regular) | N/A | ✅ Yes |
| Reverse lookup | ✅ Numeric only | ❌ No | ❌ No |
| Auto-complete | ✅ Yes | ✅ Yes | ✅ Yes |
| Can use as value | ✅ Yes | ❌ No | ✅ Yes |
| Bundle size | Larger | Zero | Smaller |
| Runtime overhead | Yes | None | Minimal |
| Type safety | Good | Good | Good |

```typescript
// Option 1: Enum
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

// Option 2: Union type
type Direction2 = "UP" | "DOWN" | "LEFT" | "RIGHT";

// Option 3: Object (as const)
const Direction3 = {
  Up: "UP",
  Down: "DOWN",
  Left: "LEFT",
  Right: "RIGHT",
} as const;
type Direction3 = (typeof Direction3)[keyof typeof Direction3];

// Option 4: Object with separate type
const Direction4 = {
  Up: "UP",
  Down: "DOWN",
  Left: "LEFT",
  Right: "RIGHT",
} as const;
type Direction4Value = "UP" | "DOWN" | "LEFT" | "RIGHT";
```

---

## When to Use Enums

```typescript
// ✅ GOOD: Enums for API integration (server sends numeric codes)
enum HttpStatusCode {
  OK = 200,
  BadRequest = 400,
  Unauthorized = 401,
  NotFound = 404,
  ServerError = 500,
}

function handleResponse(status: HttpStatusCode): void {
  if (status === HttpStatusCode.OK) {
    console.log("Success");
  }
}

// ✅ GOOD: Enums for configuration constants
enum LogLevel {
  Debug = "debug",
  Info = "info",
  Warn = "warn",
  Error = "error",
}

// ❌ AVOID: Simple enums that could be unions
enum SimpleStatus {
  Active = "active",
  Inactive = "inactive",
}
// Better:
type SimpleStatus = "active" | "inactive";

// ❌ AVOID: Numeric enums without reverse mapping needs
enum Size {
  Small = 0,
  Medium = 1,
  Large = 2,
}
// Better:
type Size = "small" | "medium" | "large";
```

---

## String Literal Unions as Enums

```typescript
// Define the union type
type Status = "active" | "inactive" | "pending";
type Method = "GET" | "POST" | "PUT" | "DELETE";
type Direction = "up" | "down" | "left" | "right";

// Use in function signatures
function setStatus(status: Status): void { /* ... */ }
function makeRequest(method: Method, url: string): Promise<Response> {
  return fetch(url, { method });
}

// Use in objects
type StatusConfig = Record<Status, { color: string; icon: string }>;
const configs: StatusConfig = {
  active: { color: "green", icon: "check" },
  inactive: { color: "gray", icon: "x" },
  pending: { color: "yellow", icon: "clock" },
};

// Derive from a const object (similar to enums but lighter)
const HttpMethod = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  DELETE: "DELETE",
} as const;

type HttpMethod = (typeof HttpMethod)[keyof typeof HttpMethod];

function request(method: HttpMethod): void { /* ... */ }
request("GET");    // OK
request("POST");   // OK
// request("PATCH"); // Error

// This pattern gives you:
// 1. Runtime values (the const object)
// 2. Type safety (the union type)
// 3. Tree-shakeability (the object can be tree-shaken)
// 4. No reverse mapping overhead
```

---

## Best Practices

1. **Prefer string literal unions** over enums for simple value sets
2. **Use `as const` objects** when you need both runtime values and types
3. **Use numeric enums** only when you need reverse mapping or interoperability with numeric codes
4. **Avoid `const enum`** unless you have a specific performance reason
5. **Avoid heterogeneous enums** — they make the type harder to reason about
6. **Use `as const` on enum-like objects** for tree-shakeability
7. **Document enum values** — the meaning of numeric values isn't self-documenting

---

## Interview Questions

### Q1: What is a TypeScript enum?

**Answer:** An enum is a way to define a set of named constants. TypeScript supports numeric (auto-incremented) and string enums. Numeric enums support reverse mapping (value to name).

### Q2: What is the difference between a regular enum and a const enum?

**Answer:** A regular enum generates a JavaScript object at runtime. A const enum is fully erased at compile time and values are inlined. Const enums have limitations: no reverse mapping, no iteration, and issues with `--isolatedModules`.

### Q3: Why might you prefer string literal unions over enums?

**Answer:** String literal unions have zero runtime overhead, are tree-shakeable, and provide the same type safety. Enums generate JavaScript objects and are not tree-shakeable. The `as const` object + union type pattern gives you both runtime values and types.

### Q4: Can a numeric enum accept any number value?

**Answer:** Yes! This is a known weakness. `enum Status { Active = 1, Inactive = 2 }` allows `const s: Status = 42` without a compile error. String enums don't have this issue.

### Q5: What is reverse mapping in enums?

**Answer:** Reverse mapping allows looking up an enum name from its numeric value: `Color[0]` returns `"Red"`. It only works with numeric enums, not string enums.
