# 06 - Type Inference

## Table of Contents

- [What is Type Inference?](#what-is-type-inference)
- [How TypeScript Infers Types](#how-typescript-infers-types)
- [Return Type Inference](#return-type-inference)
- [Parameter Inference](#parameter-inference)
- [Best Practices: When to Annotate vs Infer](#best-practices-when-to-annotate-vs-infer)
- [Contextual Typing](#contextual-typing)
- [Const Assertions](#const-assertions)
- [as const](#as-const)
- [Widening vs Narrowing](#widening-vs-narrowing)
- [Inference in Complex Scenarios](#inference-in-complex-scenarios)
- [Summary](#summary)

---

## What is Type Inference?

Type inference is TypeScript's ability to **automatically determine the type** of a variable, expression, or return value without explicit type annotations. This is one of the most powerful features of TypeScript — it provides the safety of static typing without the verbosity of annotating everything.

```typescript
// TypeScript infers these types automatically
let name = "Alice";        // inferred as string
let age = 30;              // inferred as number
let isActive = true;       // inferred as boolean
let items = [1, 2, 3];    // inferred as number[]
let user = { name: "Bob" } // inferred as { name: string }

// You don't need to write:
let name: string = "Alice";
let age: number = 30;
let isActive: boolean = true;
let items: number[] = [1, 2, 3];
let user: { name: string } = { name: "Bob" };
```

---

## How TypeScript Infers Types

TypeScript uses several mechanisms to infer types:

### 1. Initializer Inference

The most common form — TypeScript infers the type from the assigned value:

```typescript
// String literal → string
let message = "Hello";

// Number literal → number
let count = 42;

// Boolean literal → boolean
let flag = true;

// Null literal → null
let empty = null; // inferred as null (with strictNullChecks, this is just null)

// Undefined literal → undefined
let notAssigned = undefined; // inferred as undefined

// Array literal → array type
let numbers = [1, 2, 3]; // inferred as number[]
let mixed = [1, "hello"]; // inferred as (string | number)[]

// Object literal → object type with properties
let config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};
// inferred as { apiUrl: string; timeout: number }
```

### 2. Best Common Type (Array Inference)

When inferring array types from multiple elements:

```typescript
// All same type
let nums = [1, 2, 3]; // number[]

// Different types — TypeScript finds the best common type
let mixed = [1, "hello"]; // (string | number)[]

// With null/undefined
let nullable = [1, null]; // (number | null)[]

// With objects
let items = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];
// inferred as { name: string; age: number }[]
```

### 3. Contextual Type Inference

TypeScript infers types from the **context** in which a value is used:

```typescript
// Context from function parameter type
const numbers = [1, 2, 3];
numbers.map((x) => x * 2);
// TypeScript knows 'x' is number because map expects (value: number) => number

// Context from event handler
document.addEventListener("click", (event) => {
  // event is inferred as MouseEvent
  console.log(event.clientX, event.clientY);
});

// Context from typed variable
let callback: (x: number) => string;
callback = (x) => x.toString(); // x is inferred as number
```

### 4. Return Type Inference

TypeScript infers the return type of functions:

```typescript
function add(a: number, b: number) {
  return a + b; // inferred return type: number
}

function getUser() {
  return {
    name: "Alice",
    age: 30,
    email: "alice@example.com",
  };
}
// inferred return type: { name: string; age: number; email: string }

// Arrow functions
const multiply = (a: number, b: number) => a * b;
// inferred return type: number
```

---

## Return Type Inference

TypeScript can infer function return types, but sometimes explicit annotation is better.

### Automatic Inference

```typescript
// TypeScript infers return type from the function body
function greet(name: string) {
  return `Hello, ${name}!`; // inferred return: string
}

function divide(a: number, b: number) {
  if (b === 0) throw new Error("Division by zero");
  return a / b; // inferred return: number
}

function processData(items: number[]) {
  return items
    .filter((x) => x > 0)
    .map((x) => x * 2)
    .reduce((sum, x) => sum + x, 0);
}
// inferred return: number
```

### When Inference Works Well

```typescript
// Simple functions — inference is reliable
const double = (x: number) => x * 2; // number

// Chained methods — TypeScript follows the chain
const result = [1, 2, 3, 4, 5]
  .filter((x) => x > 2)
  .map((x) => x.toString()); // string[]
```

### When to Explicitly Annotate Return Types

```typescript
// 1. Public API functions — document the contract
function getUser(id: string): Promise<User | null> {
  return db.users.findById(id);
}

// 2. Recursive functions — TypeScript may fail to infer
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// 3. Complex conditional returns
function formatValue(value: unknown): string {
  if (typeof value === "string") return value.toUpperCase();
  if (typeof value === "number") return value.toFixed(2);
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return String(value);
}

// 4. Functions with multiple return paths
function process(status: "success" | "error"): { message: string; code: number } {
  if (status === "success") {
    return { message: "OK", code: 200 };
  } else {
    return { message: "Error", code: 500 };
  }
}
```

---

## Parameter Inference

TypeScript can infer parameter types from the context in which the function is used.

### From Context

```typescript
// TypeScript knows 'x' is number because of the array type
const numbers = [1, 2, 3];
numbers.map((x) => x * 2); // x: number

// From event listeners
document.addEventListener("click", (event) => {
  // event: MouseEvent (inferred from addEventListener's type)
  console.log(event.clientX);
});

// From setTimeout
setTimeout((timer) => {
  // timer: number (inferred from setTimeout's type)
  console.log(timer);
}, 1000);
```

### From Typed Variables

```typescript
// Callback parameter types inferred from the function signature
type Transformer<T, U> = (input: T) => U;

const transform: Transformer<string, number> = (input) => {
  return input.length; // input: string (inferred from Transformer<string, number>)
};
```

### From Generics

```typescript
// Generic type parameter inference
function identity<T>(x: T): T {
  return x;
}

const result = identity("hello"); // T is inferred as string
const num = identity(42);        // T is inferred as number
```

---

## Best Practices: When to Annotate vs Infer

### When to Let TypeScript Infer

```typescript
// 1. Simple variable declarations
const name = "Alice";         // string (inferred)
const count = 42;            // number (inferred)
const items = [1, 2, 3];    // number[] (inferred)

// 2. Function return types (simple functions)
const add = (a: number, b: number) => a + b; // number (inferred)

// 3. Callback parameters (when context is clear)
[1, 2, 3].map((x) => x * 2); // x: number (inferred)

// 4. Chained method calls
const result = users
  .filter((u) => u.isActive)
  .map((u) => u.name); // string[] (inferred)
```

### When to Add Explicit Annotations

```typescript
// 1. Function parameters (usually good practice)
function greet(name: string): string {
  return `Hello, ${name}`;
}

// 2. Variables declared without initialization
let result: string | null = null;
result = fetchData();

// 3. Object literals passed to functions
interface Config {
  apiUrl: string;
  timeout: number;
}

const config: Config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};

// 4. Public API surface (library/framework code)
export function processUser(user: User): ProcessedUser {
  // ...
}

// 5. Complex types that benefit from documentation
type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

// 6. When inference gives 'any' or 'unknown'
const data = JSON.parse(rawJson); // any — annotate this!
const data: User = JSON.parse(rawJson); // User

// 7. When you want to narrow or widen the type
let status: "pending" | "active" | "deleted" = "pending";
```

### The Spectrum

```
Too Little Annotation                              Too Much Annotation
│                                                                      │
│  const x = 42;    const x: number = 42;    const x: number = 42;   │
│                                                                      │
│  ← Good                    OK                          Verbose →    │
│                                                                      │
│  sweet spot ──────────────────────────────                            │
```

---

## Contextual Typing

Contextual typing is when TypeScript infers types based on **where** a value is used.

### Event Handlers

```typescript
// HTML element events
const button = document.querySelector("button");

button?.addEventListener("click", (event) => {
  // event: MouseEvent (inferred from addEventListener)
  console.log(event.clientX, event.clientY);
});

const input = document.querySelector("input");
input?.addEventListener("input", (event) => {
  // event: InputEvent (inferred from input element)
  console.log(event.target.value);
});
```

### Promises

```typescript
// Promise callbacks
const promise = new Promise<string>((resolve) => {
  resolve("hello"); // resolve parameter inferred as string
});

promise.then((value) => {
  // value: string (inferred from Promise<string>)
  console.log(value.toUpperCase());
});

promise.catch((error) => {
  // error: any (default catch type)
});
```

### Array Methods

```typescript
const numbers = [1, 2, 3, 4, 5];

// All parameter types are inferred from the array type
numbers.filter((x) => x > 3);        // x: number
numbers.map((x) => x.toString());    // x: number
numbers.reduce((acc, x) => acc + x, 0); // acc: number, x: number
numbers.find((x) => x === 3);        // x: number
numbers.some((x) => x > 4);          // x: number
numbers.every((x) => x > 0);         // x: number
```

### Object.entries and Object.keys

```typescript
const user = { name: "Alice", age: 30, email: "alice@example.com" };

Object.entries(user).forEach(([key, value]) => {
  // key: string, value: string | number (inferred from user type)
  console.log(`${key}: ${value}`);
});

Object.keys(user).forEach((key) => {
  // key: string
});
```

---

## Const Assertions

The `as const` assertion tells TypeScript to infer the **narrowest possible type** — literals instead of general types, and readonly instead of mutable.

### Without as const

```typescript
// TypeScript infers wide types
let x = 42;           // type: number
let s = "hello";      // type: string
let arr = [1, 2, 3]; // type: number[]

// Mutable — can be reassigned and modified
arr.push(4);     // OK
arr[0] = 10;     // OK
```

### With as const

```typescript
// as const infers narrow, literal types
let x = 42 as const;       // type: 42
let s = "hello" as const;  // type: "hello"
let arr = [1, 2, 3] as const; // type: readonly [1, 2, 3]

// Immutable — cannot be modified
// arr.push(4);    // Error
// arr[0] = 10;    // Error
```

### Object as const

```typescript
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
} as const;
// type: {
//   readonly apiUrl: "https://api.example.com";
//   readonly timeout: 5000;
//   readonly retries: 3;
// }

// Without as const
const config2 = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
};
// type: {
//   apiUrl: string;
//   timeout: number;
//   retries: number;
// }
```

### Nested as const

```typescript
const state = {
  user: {
    name: "Alice",
    preferences: {
      theme: "dark",
      language: "en",
    },
  },
  isLoading: false,
} as const;
// Every property at every level is readonly and a literal type

// state.user.name = "Bob"; // Error: readonly
// state.isLoading = true;  // Error: readonly
```

### Use Cases for as const

```typescript
// 1. Enum-like objects (alternative to enum)
const ROUTES = {
  HOME: "/",
  ABOUT: "/about",
  CONTACT: "/contact",
  DASHBOARD: "/dashboard",
} as const;

type Route = (typeof ROUTES)[keyof typeof ROUTES];
// type Route = "/" | "/about" | "/contact" | "/dashboard"

// 2. Color palettes
const COLORS = {
  PRIMARY: "#007bff',
  SECONDARY: "#6c757d",
  SUCCESS: "#28a745",
  DANGER: "#dc3545",
} as const;

// 3. Configuration objects that shouldn't change
const API_CONFIG = {
  baseUrl: "https://api.example.com",
  version: "v1",
  endpoints: {
    users: "/users",
    posts: "/posts",
  },
} as const;

// 4. Tuple-like arrays
const coordinates = [10, 20] as const;
// type: readonly [10, 20]
// Can be used as a tuple type
function move(point: readonly [number, number]): void {
  console.log(`Moving to (${point[0]}, ${point[1]})`);
}
move(coordinates); // OK
```

---

## Widening vs Narrowing

TypeScript's type inference involves both widening and narrowing types.

### Widening

TypeScript **widens** types in certain contexts:

```typescript
// Variable declaration — widens to base type
let x = 42;           // type: number (not 42)
let s = "hello";      // type: string (not "hello")

// But const keeps the literal type
const y = 42;         // type: 42
const t = "hello";    // type: "hello"

// let with string union
let direction = "north"; // type: string (widened)
```

### Narrowing

TypeScript **narrows** types in certain contexts:

```typescript
// Type guards narrow the type
function process(value: string | number) {
  if (typeof value === "string") {
    // value is narrowed to string
    return value.toUpperCase();
  }
  // value is narrowed to number
  return value.toFixed(2);
}

// instanceof narrowing
function handleError(error: Error | string) {
  if (error instanceof Error) {
    // error is narrowed to Error
    console.log(error.message);
  } else {
    // error is narrowed to string
    console.log(error);
  }
}

// Equality narrowing
function check(value: string | null) {
  if (value === null) {
    // value is narrowed to null
    return "no value";
  }
  // value is narrowed to string
  return value.toUpperCase();
}
```

---

## Inference in Complex Scenarios

### Generics

```typescript
// TypeScript infers generic type parameters
function first<T>(array: T[]): T | undefined {
  return array[0];
}

const num = first([1, 2, 3]);       // T inferred as number
const str = first(["a", "b"]);      // T inferred as string
const mixed = first([1, "a"]);      // T inferred as string | number

// Multiple type parameters
function pair<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

const p = pair("hello", 42); // [string, number]
```

### Conditional Types

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false
type C = IsString<string>;  // true
```

### Mapped Types

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

interface User {
  name: string;
  age: number;
}

type ReadonlyUser = Readonly<User>;
// type: { readonly name: string; readonly age: number }
```

### Infer Keyword in Conditional Types

```typescript
// Extract return type of a function
type ReturnOf<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { name: "Alice", age: 30 };
}

type UserType = ReturnOf<typeof getUser>;
// type: { name: string; age: number }

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;

type Num = ElementOf<number[]>;   // number
type Str = ElementOf<string[]>;   // string
```

### Template Literal Types

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">;    // "onClick"
type FocusEvent = EventName<"focus">;    // "onFocus"
type BlurEvent = EventName<"blur">;      // "onBlur"
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| **Inference** | TypeScript determines types automatically |
| **Initializer** | Types inferred from assigned values |
| **Contextual** | Types inferred from usage context |
| **Return type** | Inferred from function body |
| **const vs let** | const keeps literal types, let widens |
| **as const** | Makes everything readonly and literal |
| **Best practice** | Infer when clear, annotate when ambiguous |

> **Golden Rule:** Let TypeScript infer when the type is obvious. Annotate when the type is not clear, when you want to document the API contract, or when inference gives an undesired type (like `any`).
