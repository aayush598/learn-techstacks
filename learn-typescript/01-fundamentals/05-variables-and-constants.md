# 05 - Variables and Constants

## Table of Contents

- [Overview](#overview)
- [var — The Legacy Way](#var--the-legacy-way)
- [let — Block-Scoped Variables](#let--block-scoped-variables)
- [const — Block-Scoped Constants](#const--block-scoped-constants)
- [Block Scoping](#block-scoping)
- [Hoisting](#hoisting)
- [Naming Conventions](#naming-conventions)
- [When to Use const](#when-to-use-const)
- [readonly vs const](#readonly-vs-const)
- [Variable Declaration Best Practices](#variable-declaration-best-practices)
- [TypeScript-Specific Considerations](#typescript-specific-considerations)
- [Summary](#summary)

---

## Overview

TypeScript inherits JavaScript's three variable declaration keywords: `var`, `let`, and `const`. While they may seem similar, they have critical differences in scoping, hoisting, and mutability that affect how your code behaves.

```
┌─────────────────────────────────────────────┐
│              var                              │
│  - Function-scoped                           │
│  - Hoisted with initialization as undefined  │
│  - Can be redeclared                         │
│  - Avoid in modern code                      │
├─────────────────────────────────────────────┤
│              let                              │
│  - Block-scoped                              │
│  - Hoisted but not initialized (TDZ)         │
│  - Cannot be redeclared in same scope        │
│  - Mutable                                   │
├─────────────────────────────────────────────┤
│              const                            │
│  - Block-scoped                              │
│  - Hoisted but not initialized (TDZ)         │
│  - Cannot be redeclared in same scope        │
│  - Immutable binding (not deep immutable)    │
└─────────────────────────────────────────────┘
```

---

## var — The Legacy Way

`var` is the original variable declaration in JavaScript. It has several problematic behaviors that `let` and `const` fix.

### Function Scoping (Not Block Scoping)

```typescript
function doSomething(): void {
  if (true) {
    var x: number = 10;
  }
  console.log(x); // 10 — x is accessible outside the if block!
}

// This is because var is FUNCTION-scoped, not BLOCK-scoped
```

### Redeclaration

```typescript
var x: number = 10;
var x: number = 20; // No error — var allows redeclaration

console.log(x); // 20
```

### Hoisting

```typescript
// var declarations are hoisted to the top of the function
console.log(name); // undefined (not an error!)
var name: string = "Alice";

// JavaScript interprets this as:
// var name;
// console.log(name); // undefined
// name = "Alice";
```

### Loop Problem

```typescript
// Classic var in loop problem
for (var i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i); // All three print 3 (not 0, 1, 2!)
  }, 100);
}

// All callbacks share the same 'i' variable
// By the time they execute, i is already 3
```

### When to Use var

**Almost never.** Use `let` or `const` instead. The only legitimate use case is when you need **function-scoped** variables in very specific patterns, which is rare.

---

## let — Block-Scoped Variables

`let` is the modern replacement for `var` when you need a mutable variable.

### Block Scoping

```typescript
function doSomething(): void {
  if (true) {
    let x: number = 10;
    console.log(x); // 10
  }
  // console.log(x); // Error: x is not defined
}

// let is BLOCK-scoped — it only exists within the nearest { }
```

### No Redeclaration

```typescript
let x: number = 10;
// let x: number = 20; // Error: Cannot redeclare block-scoped variable 'x'

x = 20; // OK — reassignment is allowed, redeclaration is not
```

### Temporal Dead Zone (TDZ)

```typescript
// let variables are in the "temporal dead zone" until declared
// console.log(x); // Error: Cannot access 'x' before initialization
let x: number = 10;

// This is different from var:
// console.log(y); // undefined (var is hoisted with undefined)
var y: number = 10;
```

### Loop Fix

```typescript
// let in for loop — each iteration gets its own 'i'
for (let i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(i); // Prints 0, 1, 2
  }, 100);
}

// Each callback captures its own copy of 'i'
```

### let in TypeScript

```typescript
// let with type annotation
let count: number = 0;
let name: string = "Alice";
let isActive: boolean = true;

// let with type inference (equivalent)
let count = 0;         // inferred as number
let name = "Alice";    // inferred as string
let isActive = true;   // inferred as boolean

// let with union types (common use case)
let result: string | null = null;
result = "success";
result = null;

// let with no type annotation — inferred as 'any' if not initialized
// let x; // Type is 'any' (avoid this)
let x: string; // Explicit annotation required in strict mode
```

---

## const — Block-Scoped Constants

`const` creates a **read-only binding** — the variable cannot be reassigned after initialization.

### Basic Usage

```typescript
const PI: number = 3.14159;
const APP_NAME: string = "MyApp";
const IS_DEV: boolean = true;

// PI = 3.14; // Error: Cannot assign to 'PI' because it is a read-only property
```

### const Does NOT Mean Immutable

This is the most common misconception. `const` prevents **reassignment** of the binding, but the **value itself can still be mutated** if it's an object or array:

```typescript
// Primitive values — truly immutable with const
const count: number = 42;
// count = 43; // Error

// Objects — can be mutated!
const user: { name: string; age: number } = {
  name: "Alice",
  age: 30,
};

user.age = 31; // OK — modifying a property
user.name = "Bob"; // OK — modifying a property
// user = { name: "Charlie", age: 25 }; // Error — cannot reassign

// Arrays — can be mutated!
const numbers: number[] = [1, 2, 3];
numbers.push(4);    // OK — modifying the array
numbers[0] = 10;    // OK — modifying an element
// numbers = [4, 5, 6]; // Error — cannot reassign
```

### const with Type Inference

```typescript
// TypeScript infers a narrower type with const
const x = 42;      // type: 42 (literal type, not just number)
const s = "hello";  // type: "hello" (literal type, not just string)
const b = true;     // type: true (literal type, not just boolean)

// With let, TypeScript infers the wider type
let x = 42;         // type: number
let s = "hello";    // type: string
let b = true;       // type: boolean

// This difference is important for type narrowing
function handle(value: "success" | "error"): void {
  // ...
}

const status = "success"; // type: "success"
handle(status);           // OK — "success" is a valid argument

let status2 = "success"; // type: string
// handle(status2);      // Error: string is not assignable to "success" | "error"
```

### const Assertions (Preview)

```typescript
// as const — makes everything deeply readonly and literal
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
} as const;
// type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }

// const arrays become readonly tuples
const colors = ["red", "green", "blue"] as const;
// type: readonly ["red", "green", "blue"]
```

---

## Block Scoping

Understanding block scoping is crucial for writing correct TypeScript.

### Basic Block Scoping

```typescript
{
  // Block scope starts here
  let x: number = 10;
  const y: string = "hello";
  console.log(x, y); // 10 "hello"
}
// console.log(x); // Error: x is not defined
// console.log(y); // Error: y is not defined
```

### Nested Blocks

```typescript
let outer: number = 1;

{
  let outer: number = 2; // Shadows the outer 'outer'
  let inner: number = 10;
  console.log(outer); // 2
  console.log(inner); // 10

  {
    let outer: number = 3; // Shadows again
    let inner2: number = 20;
    console.log(outer); // 3
    console.log(inner); // 10 (from parent block)
    console.log(inner2); // 20
  }

  console.log(outer); // 2 (back to this block's 'outer')
  // console.log(inner2); // Error: inner2 is not defined
}

console.log(outer); // 1 (back to original 'outer')
```

### Block Scoping in Control Structures

```typescript
// if/else blocks
if (true) {
  let x: number = 10;
}
// x is not accessible here

// for loop blocks
for (let i = 0; i < 3; i++) {
  let temp: number = i * 2;
}
// i and temp are not accessible here

// try/catch blocks
try {
  let error: string = "oops";
} catch (e) {
  let message: string = (e as Error).message;
}
// error and message are not accessible here
```

### Destructuring with Block Scoping

```typescript
const user = { name: "Alice", age: 30, email: "alice@example.com" };

// Destructure with const — each variable is block-scoped
const { name, age } = user;
console.log(name, age); // "Alice" 30

// Destructure in a block
if (age > 18) {
  const { email } = user;
  console.log(email); // "alice@example.com"
}
// email is not accessible here
```

---

## Hoisting

Hoisting is JavaScript's behavior of moving declarations to the top of their scope during compilation.

### var Hoisting

```typescript
// var declarations are hoisted AND initialized to undefined
console.log(x); // undefined (not an error!)
var x: number = 10;

// What JavaScript actually executes:
// var x;           // Declaration hoisted
// console.log(x);  // undefined
// x = 10;          // Assignment stays in place
```

### let Hoisting

```typescript
// let declarations are hoisted but NOT initialized
// console.log(x); // ReferenceError: Cannot access 'x' before initialization
let x: number = 10;

// What JavaScript actually executes:
// x is hoisted but enters the "temporal dead zone"
// console.log(x);  // TDZ — ReferenceError
// x = 10;          // Assignment happens here
```

### const Hoisting

```typescript
// const declarations are hoisted but NOT initialized
// console.log(PI); // ReferenceError: Cannot access 'PI' before initialization
const PI: number = 3.14;

// Same temporal dead zone behavior as let
```

### Hoisting Comparison

```
┌─────────┬──────────────────┬───────────────────┬──────────────────┐
│         │ Declaration      │ Initialization    │ TDZ              │
├─────────┼──────────────────┼───────────────────┼──────────────────┤
│ var     │ Hoisted to top   │ Initialized to   │ No TDZ           │
│         │ of function      │ undefined        │                  │
├─────────┼──────────────────┼───────────────────┼──────────────────┤
│ let     │ Hoisted to top   │ NOT initialized  │ Yes — until      │
│         │ of block         │                  │ declaration      │
├─────────┼──────────────────┼───────────────────┼──────────────────┤
│ const   │ Hoisted to top   │ NOT initialized  │ Yes — until      │
│         │ of block         │                  │ declaration      │
└─────────┴──────────────────┴───────────────────┴──────────────────┘
```

---

## Naming Conventions

TypeScript follows established naming conventions that improve code readability.

### camelCase

Used for **variables, functions, parameters, and methods**:

```typescript
// Variables
const firstName: string = "Alice";
const userAge: number = 30;
let isLoggedIn: boolean = true;

// Functions
function getUserData(): UserData { /* ... */ }
const calculateTotal = (items: Item[]): number => { /* ... */ };

// Parameters
function greet(firstName: string, lastName: string): string {
  return `Hello, ${firstName} ${lastName}`;
}

// Methods
class UserService {
  getUserById(id: string): User { /* ... */ }
  createUser(data: CreateUserDto): User { /* ... */ }
}
```

### PascalCase

Used for **classes, interfaces, types, enums, and constructors**:

```typescript
// Classes
class UserService { /* ... */ }
class HttpRequestHandler { /* ... */ }

// Interfaces
interface UserData { /* ... */ }
interface ApiResponse { /* ... */ }

// Type aliases
type Coordinate = [number, number];
type Status = "pending" | "active" | "deleted";

// Enums
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

// Constructors (in React and similar)
function MyComponent() { /* ... */ }
```

### UPPER_SNAKE_CASE

Used for **constants that are truly constant** (never change):

```typescript
// Global constants
const API_BASE_URL: string = "https://api.example.com";
const MAX_RETRY_COUNT: number = 3;
const DEFAULT_TIMEOUT: number = 5000;

// Environment variables
const NODE_ENV: string = process.env.NODE_ENV ?? "development";

// Enum-like constants (alternative to enum)
const STATUS = {
  PENDING: "PENDING",
  ACTIVE: "ACTIVE",
  DELETED: "DELETED",
} as const;
```

### Private Members

TypeScript uses the `#` prefix (JavaScript private fields) or the `private` keyword:

```typescript
class User {
  // TypeScript private (compile-time only)
  private _password: string;

  // JavaScript private field (runtime enforced)
  #secretKey: string;

  constructor(password: string, secretKey: string) {
    this._password = password;
    this.#secretKey = secretKey;
  }

  // Convention: underscore prefix for "private" properties
  get password(): string {
    return this._password;
  }
}
```

---

## When to Use const

### Default to const

The best practice is to **always use `const` by default** and only switch to `let` when reassignment is necessary.

```typescript
// GOOD: Use const for values that don't change
const API_URL = "https://api.example.com";
const MAX_ITEMS = 100;
const user = { name: "Alice" };

// GOOD: Use let only when reassignment is needed
let count = 0;
count++; // Reassignment needed

let result: string | null = null;
result = fetchData(); // Reassignment needed

// BAD: Using let when const would work
let name = "Alice"; // Never reassigned — should be const
let age = 30;       // Never reassigned — should be const
```

### Decision Flowchart

```
Does the variable need to be reassigned?
│
├── YES → use let
│   ├── Loop counter
│   ├── Accumulator
│   ├── Flag that changes
│   └── Nullable variable
│
└── NO → use const
    ├── Function results
    ├── Configuration values
    ├── DOM elements
    ├── Imported modules
    └── Destructured values
```

---

## readonly vs const

TypeScript provides two ways to make things immutable: `const` (for variables) and `readonly` (for properties).

### const (Variable Level)

```typescript
const x: number = 42;
// x = 43; // Error: cannot reassign

// const only prevents reassignment of the binding
const arr: number[] = [1, 2, 3];
arr.push(4); // OK — array is mutable
```

### readonly (Property Level)

```typescript
interface User {
  readonly id: string;
  readonly name: string;
  email: string;
  age: number;
}

const user: User = {
  id: "123",
  name: "Alice",
  email: "alice@example.com",
  age: 30,
};

// user.id = "456";   // Error: id is readonly
// user.name = "Bob"; // Error: name is readonly
user.email = "bob@example.com"; // OK — email is not readonly
user.age = 31;                   // OK — age is not readonly
```

### readonly Arrays

```typescript
// Readonly arrays
const numbers: readonly number[] = [1, 2, 3];
// numbers.push(4);    // Error: Property 'push' does not exist on type 'readonly number[]'
// numbers[0] = 10;    // Error: Index signature in type 'readonly number[]' only permits reading

// ReadonlyArray type (same as readonly T[])
const names: ReadonlyArray<string> = ["Alice", "Bob"];

// Tuple types with readonly
const point: readonly [number, number] = [10, 20];
```

### readonly Maps and Sets

```typescript
// Readonly Map
const map: ReadonlyMap<string, number> = new Map([
  ["a", 1],
  ["b", 2],
]);
// map.set("c", 3); // Error: Map is readonly

// Readonly Set
const set: ReadonlySet<number> = new Set([1, 2, 3]);
// set.add(4); // Error: Set is readonly
```

### Deep Readonly

```typescript
// Type for deeply readonly objects
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

interface Config {
  database: {
    host: string;
    port: number;
    credentials: {
      username: string;
      password: string;
    };
  };
}

const config: DeepReadonly<Config> = {
  database: {
    host: "localhost",
    port: 5432,
    credentials: {
      username: "admin",
      password: "secret",
    },
  },
};

// config.database.port = 5433; // Error
// config.database.credentials.password = "new"; // Error
```

---

## Variable Declaration Best Practices

### 1. Always Use const by Default

```typescript
// BAD
let name = "Alice";

// GOOD
const name = "Alice";
```

### 2. Use let Only When Necessary

```typescript
// GOOD: Reassignment needed
let total = 0;
for (const item of items) {
  total += item.price;
}

// GOOD: Updating state
let isLoading = false;
isLoading = true;
```

### 3. Declare Variables Close to Usage

```typescript
// BAD
let result: string;
// ... 50 lines of code ...
result = fetchData();

// GOOD
// ... 50 lines of code ...
const result = fetchData();
```

### 4. One Declaration Per Variable

```typescript
// BAD
let x: number, y: number, z: number;

// GOOD
const x: number = 1;
const y: number = 2;
const z: number = 3;
```

### 5. Avoid Unused Variables

```typescript
// BAD — unused variable
const unused = 42;

// GOOD — prefix with underscore if intentionally unused
const _unused = 42;

// BETTER — remove it entirely
```

### 6. Use Descriptive Names

```typescript
// BAD
const d = new Date();
const x = user.name;

// GOOD
const currentDate = new Date();
const userName = user.name;
```

### 7. Avoid Magic Numbers and Strings

```typescript
// BAD
if (user.age >= 18) { /* ... */ }
setTimeout(() => { /* ... */ }, 3000);

// GOOD
const MINIMUM_AGE = 18;
const TOAST_DURATION_MS = 3000;

if (user.age >= MINIMUM_AGE) { /* ... */ }
setTimeout(() => { /* ... */ }, TOAST_DURATION_MS);
```

---

## TypeScript-Specific Considerations

### Type Annotations with Variables

```typescript
// Explicit annotation
const name: string = "Alice";

// Type inference (usually preferred)
const name = "Alice"; // inferred as string

// When to annotate explicitly:
// 1. When the type is not obvious
const data = JSON.parse(rawJson); // type: any (annotate this!)
const data: User = JSON.parse(rawJson); // type: User

// 2. When you want a wider type
let status: "pending" | "active" | "deleted" = "pending";

// 3. When initializing later
let result: string;
result = computeExpensiveValue();
```

### const and Type Narrowing

```typescript
// const provides narrower types than let
const x = "hello"; // type: "hello" (literal)
let y = "hello";   // type: string

// This matters for discriminated unions
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number };

function handle(action: Action): void {
  const type = action.type; // type: "INCREMENT" | "DECREMENT"

  // With const, the switch works with literal types
  switch (type) {
    case "INCREMENT":
      // action is narrowed to { type: "INCREMENT"; amount: number }
      break;
    case "DECREMENT":
      // action is narrowed to { type: "DECREMENT"; amount: number }
      break;
  }
}
```

### Destructuring with const/let

```typescript
// Object destructuring
const { name, age, email } = user;
let { x, y, z } = coordinate;

// Array destructuring
const [first, second, ...rest] = numbers;
let [a, b] = [1, 2];

// Default values
const { name = "Unknown", age = 0 } = user ?? {};

// Renaming
const { name: userName, age: userAge } = user;

// Nested destructuring
const { address: { city, country } } = user;
```

---

## Summary

| Keyword | Scoping | Redeclaration | Reassignment | Hoisting | Best For |
|---------|---------|---------------|--------------|----------|----------|
| `var` | Function | Allowed | Allowed | With undefined | Avoid |
| `let` | Block | Not allowed | Allowed | TDZ | Mutable variables |
| `const` | Block | Not allowed | Not allowed | TDZ | Immutable bindings |

> **Golden Rules:**
> 1. **Always** use `const` by default
> 2. Use `let` only when reassignment is needed
> 3. **Never** use `var` in modern TypeScript
> 4. Use `readonly` for object properties that shouldn't change
> 5. Follow naming conventions: camelCase for variables, PascalCase for types
