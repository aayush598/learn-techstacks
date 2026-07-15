# Literal Types in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [String Literal Types](#string-literal-types)
3. [Number Literal Types](#number-literal-types)
4. [Boolean Literal Types](#boolean-literal-types)
5. [Template Literal Types](#template-literal-types)
6. [Union of Literals](#union-of-literals)
7. [Literal Inference](#literal-inference)
8. [as const for Literals](#as-const-for-literals)
9. [Literal Type Narrowing](#literal-type-narrowing)
10. [Using Literals for API Keys and Event Names](#using-literals-for-api-keys-and-event-names)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

Literal types allow you to narrow a type to exactly one value. Instead of `string`, you can specify `"hello"` as a type. This provides much stronger type safety.

---

## String Literal Types

```typescript
// Basic string literal type
type Direction = "up" | "down" | "left" | "right";

const dir1: Direction = "up";    // OK
const dir2: Direction = "down";  // OK
// const dir3: Direction = "forward"; // Error

// Using in function parameters
function move(direction: Direction): void {
  console.log(`Moving ${direction}`);
}

move("up");     // OK
move("left");   // OK
// move("north"); // Error

// String literal in objects
interface Config {
  mode: "development" | "production" | "test";
  logLevel: "debug" | "info" | "warn" | "error";
}

const config: Config = {
  mode: "production",
  logLevel: "info",
};

// String literal in class properties
class Logger {
  private level: "debug" | "info" | "warn" | "error";

  constructor(level: "debug" | "info" | "warn" | "error") {
    this.level = level;
  }

  log(message: string): void {
    if (this.level === "debug" || this.level === "info") {
      console.log(`[${this.level.toUpperCase()}] ${message}`);
    }
  }
}

// String literal in API design
type HTTPStatus = "ok" | "error" | "loading";
type UserRole = "admin" | "user" | "guest";
type Theme = "light" | "dark" | "system";
type SortOrder = "asc" | "desc";

// Deriving literals from existing values
const METHODS = ["GET", "POST", "PUT", "DELETE"] as const;
type HTTPMethod = (typeof METHODS)[number]; // "GET" | "POST" | "PUT" | "DELETE"
```

---

## Number Literal Types

```typescript
// Number literal types
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
type Month = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
type Percentage = 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100;

// Using number literals
function rollDice(): DiceRoll {
  return Math.floor(Math.random() * 6) + 1 as DiceRoll;
}

function setMonth(month: Month): void {
  console.log(`Setting month to ${month}`);
}

setMonth(1);   // OK
setMonth(13);  // Error

// Number literals in objects
interface HTTPConfig {
  port: 3000 | 8080 | 8443;
  timeout: 5000 | 10000 | 30000;
}

const serverConfig: HTTPConfig = {
  port: 3000,
  timeout: 10000,
};

// Number literals in generic constraints
function createArray<T extends 1 | 2 | 3>(length: T): T[] {
  return new Array(length);
}

const arr1 = createArray(3); // number[]
const arr2 = createArray(2); // number[]
// const arr3 = createArray(4); // Error: 4 is not assignable to 1 | 2 | 3

// Number literals with const enums
const enum Direction4 {
  Up = 0,
  Down = 1,
  Left = 2,
  Right = 3,
}

// Number literals in type guards
function isDiceRoll(value: number): value is DiceRoll {
  return value >= 1 && value <= 6 && Number.isInteger(value);
}
```

---

## Boolean Literal Types

```typescript
// Boolean literal types (used in discriminated unions)
type Success = {
  success: true;
  data: string;
};

type Failure = {
  success: false;
  error: string;
};

type Result = Success | Failure;

function handle(result: Result): void {
  if (result.success) {
    // result is Success
    console.log(result.data);
  } else {
    // result is Failure
    console.error(result.error);
  }
}

// Boolean literal in configuration
interface FeatureFlags {
  enableDarkMode: true;
  enableNotifications: false;
  enableBetaFeatures: boolean; // Regular boolean (both true and false)
}

const flags: FeatureFlags = {
  enableDarkMode: true,
  enableNotifications: false,
  enableBetaFeatures: Math.random() > 0.5,
};

// Boolean literal in function overloads
function process(value: string, shouldLog: true): string[];
function process(value: string, shouldLog: false): string;
function process(value: string, shouldLog: boolean): string | string[] {
  const result = value.split(" ");
  return shouldLog ? result.map((s) => `[${s}]`) : result;
}

const withLog = process("hello world", true);  // string[]
const withoutLog = process("hello world", false); // string
```

---

## Template Literal Types

```typescript
// Basic template literal types
type Greeting = `Hello, ${string}`;
const g1: Greeting = "Hello, World"; // OK
// const g2: Greeting = "Hi, World"; // Error

// Combining with unions
type Color = "red" | "blue" | "green";
type ColorClass = `color-${Color}`;
// "color-red" | "color-blue" | "color-green"

const c1: ColorClass = "color-red";   // OK
// const c2: ColorClass = "color-yellow"; // Error

// Combining with multiple unions
type Size = "small" | "medium" | "large";
type CSSProperty = `size-${Size}`;
// "size-small" | "size-medium" | "size-large"

// Complex template literals
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIEndpoint = `/${string}`;
type Route = `${HTTPMethod} ${APIEndpoint}`;
// "GET /..." | "POST /..." | "PUT /..." | "DELETE /..."

const route: Route = "GET /api/users"; // OK

// Template literal with number
type EventName = `event-${number}`;
const e1: EventName = "event-42"; // OK
// const e2: EventName = "event-abc"; // Error

// Nested template literals
type CSSValue = `${number}${"px" | "em" | "rem" | "%"}`;
const width: CSSValue = "100px";
const fontSize: CSSValue = "1.5em";

// Intrinsic string manipulation types
type Upper = Uppercase<"hello">;        // "HELLO"
type Lower = Lowercase<"HELLO">;        // "hello"
type Cap = Capitalize<"hello">;         // "Hello"
type UnCap = Uncapitalize<"Hello">;     // "hello"

// Combining intrinsic with unions
type Status = "active" | "inactive";
type StatusMethod = `on${Capitalize<Status>}`;
// "onActive" | "onInactive"

// Template literal types in mapped types
type PropNames = "name" | "age" | "email";
type Getters = {
  [K in PropNames as `get${Capitalize<K>}`]: () => string;
};
// {
//   getName: () => string;
//   getAge: () => string;
//   getEmail: () => string;
}

// Template literal types for event handlers
type EventName2 = "click" | "focus" | "blur";
type HandlerMap = {
  [K in EventName2 as `on${Capitalize<K>}`]: (event: Event) => void;
};
// {
//   onClick: (event: Event) => void;
//   onFocus: (event: Event) => void;
//   onBlur: (event: Event) => void;
}
```

---

## Union of Literals

```typescript
// Union of string literals
type Status = "active" | "inactive" | "pending";
type Direction = "up" | "down" | "left" | "right";
type Theme = "light" | "dark" | "system";

// Union of number literals
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
type Month = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

// Mixed literal unions
type Primitive = "hello" | 42 | true | null;

// Literals from objects (as const)
const HttpStatus = {
  OK: 200,
  NotFound: 404,
  ServerError: 500,
} as const;

type HTTPStatusCode = (typeof HttpStatus)[keyof typeof HttpStatus];
// 200 | 404 | 500

// Literals from arrays (as const)
const ROLES = ["admin", "user", "guest"] as const;
type UserRole = (typeof ROLES)[number]; // "admin" | "user" | "guest"

// Literals from enums
enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE",
}

type ColorValue = `${Color}`; // "RED" | "GREEN" | "BLUE"

// Exhaustive literal union
type DayOfWeek =
  | "monday"
  | "tuesday"
  | "wednesday"
  | "thursday"
  | "friday"
  | "saturday"
  | "sunday";

type Weekend = Extract<DayOfWeek, "saturday" | "sunday">;
type Weekday = Exclude<DayOfWeek, Weekend>;

// Literals in generic constraints
function getStatus<T extends Status>(status: T): T {
  return status;
}

const active = getStatus("active"); // "active" (literal type!)
```

---

## Literal Inference

TypeScript infers types from values. By default, it widens literal types.

```typescript
// Default inference: widens to base type
const direction = "up"; // inferred as string (not "up")
const count = 42;       // inferred as number (not 42)
const flag = true;      // inferred as boolean (not true)

// To keep literal types, use:
// 1. as const
const dir = "up" as const; // "up"
const num = 42 as const;   // 42

// 2. Explicit type annotation
const dir2: "up" = "up"; // "up"
const num2: 42 = 42;     // 42

// 3. Satisfies (preserves narrow type while checking against a type)
const config = {
  mode: "production",
} satisfies Record<string, string>;
// config.mode is "production" (literal), not string

// Inference in objects (widens by default)
const obj = { x: 1, y: 2 }; // { x: number; y: number }
const objConst = { x: 1, y: 2 } as const;
// { readonly x: 1; readonly y: 2 } (literal types!)

// Inference in arrays
const arr = [1, 2, 3];         // number[]
const arrConst = [1, 2, 3] as const; // readonly [1, 2, 3]

// Inference in function return values
function getStatus() {
  return "active" as const; // "active" (not string)
}

const status = getStatus(); // "active"

// Inference in const variables (narrower)
const X = 42;          // number (widened)
const Y = 42 as const; // 42 (literal)

// Contextual typing affects inference
const arr2: ("a" | "b" | "c")[] = ["a", "b", "c"]; // ("a" | "b" | "c")[]
// Without annotation: string[]
```

---

## as const for Literals

```typescript
// as const is the primary way to get literal types from values

// On values
const x = "hello" as const; // "hello"
const y = 42 as const;      // 42
const z = true as const;    // true

// On objects (deep readonly with literal types)
const config = {
  host: "localhost",
  port: 3000,
  debug: true,
} as const;
// { readonly host: "localhost"; readonly port: 3000; readonly debug: true }

// On arrays (readonly tuple with literal types)
const colors = ["red", "green", "blue"] as const;
// readonly ["red", "green", "blue"]
type Color = (typeof colors)[number]; // "red" | "green" | "blue"

// On nested objects (deep readonly)
const api = {
  baseUrl: "https://api.example.com",
  endpoints: {
    users: "/users",
    posts: "/posts",
  },
} as const;
// Fully readonly with literal types

// as const in function parameters
function log(message: string, level: "info" | "warn" | "error"): void {
  console.log(`[${level.toUpperCase()}] ${message}`);
}

// as const with assertions
const direction = "up" as const;
log("Moving", direction); // OK — "up" is assignable to "info" | "warn" | "error"

// as const for enum-like patterns
const HttpMethod = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  DELETE: "DELETE",
} as const;

type HttpMethod = (typeof HttpMethod)[keyof typeof HttpMethod];
// "GET" | "POST" | "PUT" | "DELETE"

// Usage
function request(method: HttpMethod, url: string): void {
  console.log(`${method} ${url}`);
}

request("GET", "/api/users"); // OK
request(HttpMethod.POST, "/api/posts"); // OK (runtime value)
```

---

## Literal Type Narrowing

```typescript
// Narrowing from wider to literal types
function getStatus(code: number): "success" | "error" | "loading" {
  if (code === 200) return "success";
  if (code === 500) return "error";
  return "loading";
}

// Narrowing with switch
type Action = "increment" | "decrement" | "reset";

function handleAction(state: number, action: Action): number {
  switch (action) {
    case "increment":
      return state + 1;
    case "decrement":
      return state - 1;
    case "reset":
      return 0;
  }
}

// Narrowing with if
function process(value: string | number): string {
  if (typeof value === "string") {
    // narrowed to string
    return value.toUpperCase();
  }
  // narrowed to number
  return value.toFixed(2);
}

// Narrowing with type guard
function isStatus(value: string): value is "active" | "inactive" {
  return value === "active" || value === "inactive";
}

function setStatus(value: string): void {
  if (isStatus(value)) {
    // narrowed to "active" | "inactive"
    document.body.dataset.status = value;
  }
}

// Narrowing with discriminated union
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

// Exhaustive narrowing
function assertNever(value: never): never {
  throw new Error(`Unexpected: ${value}`);
}

function describe(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return `Circle (r=${shape.radius})`;
    case "square":
      return `Square (s=${shape.side})`;
    default:
      return assertNever(shape);
  }
}
```

---

## Using Literals for API Keys and Event Names

```typescript
// API keys as literal types
type APIKey = `sk_live_${string}` | `pk_test_${string}`;

function initStripe(key: APIKey): void {
  console.log(`Initializing with key: ${key}`);
}

initStripe("sk_live_abc123"); // OK
// initStripe("invalid_key"); // Error

// Event names as literal types
type AppEvent =
  | "user.created"
  | "user.updated"
  | "user.deleted"
  | "order.placed"
  | "order.shipped"
  | "order.delivered";

function onEvent(event: AppEvent, handler: () => void): void {
  // Register handler
}

onEvent("user.created", () => {}); // OK
// onEvent("user.created", () => {}); // OK
// onEvent("invalid.event", () => {}); // Error

// CSS class names as literal types
type CSSClass =
  | "container"
  | "header"
  | "footer"
  | "button-primary"
  | "button-secondary";

function addClass(element: HTMLElement, className: CSSClass): void {
  element.classList.add(className);
}

// Route parameters as literal types
type RouteParam = `:${string}`;
type Route = `/${string}${RouteParam}${string}`;

function defineRoute(path: Route): void {
  console.log(`Route: ${path}`);
}

defineRoute("/users/:id");    // OK
defineRoute("/posts/:postId/comments/:commentId"); // OK
// defineRoute("/users"); // Error: no route parameter

// SQL column names as literal types
type Column = "id" | "name" | "email" | "created_at";

function select(columns: Column[]): string {
  return `SELECT ${columns.join(", ")} FROM users`;
}

select(["id", "name"]); // OK
// select(["id", "invalid"]); // Error

// GraphQL field names
type GraphQLField = "user" | "post" | "comment" | "like";

function query(field: GraphQLField, args?: Record<string, unknown>): string {
  return args
    ? `${field}(${JSON.stringify(args)})`
    : field;
}
```

---

## Best Practices

1. **Use `as const`** to get literal types from arrays, objects, and values
2. **Use literal unions** over enums for simple value sets (better tree-shaking)
3. **Use template literal types** for string pattern matching at the type level
4. **Use `satisfies`** to preserve narrow types while validating against a type
5. **Use literal types for API boundaries** to constrain allowed values
6. **Use discriminant properties** with literal types for discriminated unions
7. **Don't over-narrow** — literal types are most useful at API boundaries
8. **Use `typeof` + `as const`** to derive literal types from runtime values
9. **Use literal types in function parameters** to constrain allowed inputs
10. **Document literal type meaning** — the values alone may not be self-explanatory

---

## Interview Questions

### Q1: What is a literal type in TypeScript?

**Answer:** A literal type represents exactly one specific value. For example, `"hello"` is a literal string type, `42` is a literal number type. Literal types let you constrain values to specific allowed strings, numbers, or booleans.

### Q2: How do you preserve literal types from runtime values?

**Answer:** Use `as const`: `const x = "hello" as const;`. Without it, TypeScript widens `"hello"` to `string`. You can also use explicit type annotations or `satisfies`.

### Q3: What are template literal types?

**Answer:** Types created by combining string literals and types using backtick syntax. They enable type-level string manipulation: `` `on${Capitalize<string>}` `` creates types like `"onHello"`, `"onWorld"`, etc.

### Q4: When would you use literal types?

**Answer:** For API parameters that accept specific values (`"GET" | "POST"`), discriminated unions, configuration objects, event names, CSS classes, route patterns, and any domain where only specific string/number values are valid.

### Q5: What is `as const` and how does it affect literal types?

**Answer:** `as const` is a type assertion that tells TypeScript to infer the narrowest possible type. It makes values literal types, objects deeply readonly, and arrays readonly tuples. It's the primary way to get literal types from runtime values.
