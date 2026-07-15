# 07 - Type Annotations

## Table of Contents

- [What are Type Annotations?](#what-are-type-annotations)
- [Annotation Syntax](#annotation-syntax)
- [Variable Annotations](#variable-annotations)
- [Function Annotations](#function-annotations)
- [Object Annotations](#object-annotations)
- [Array Annotations](#array-annotations)
- [Tuple Annotations](#tuple-annotations)
- [Annotation Best Practices](#annotation-best-practices)
- [Common Patterns](#common-patterns)
- [Summary](#summary)

---

## What are Type Annotations?

Type annotations are **explicit type declarations** that you add to variables, function parameters, return values, and other code elements. They tell TypeScript what type a value should be, overriding or supplementing inference.

```typescript
// Type annotation syntax: variable: Type
const name: string = "Alice";
const age: number = 30;
const isActive: boolean = true;

// Without annotations — TypeScript infers these
const name = "Alice";     // string (inferred)
const age = 30;           // number (inferred)
const isActive = true;    // boolean (inferred)
```

---

## Annotation Syntax

The general syntax is:

```
identifier: Type = value;
```

### Basic Syntax Examples

```typescript
// Variable annotation
let x: number = 42;

// Function parameter annotation
function add(a: number, b: number): number {
  return a + b;
}

// Object property annotation
interface User {
  name: string;
  age: number;
}

// Array annotation
const items: string[] = ["a", "b", "c"];

// Tuple annotation
const point: [number, number] = [10, 20];

// Union type annotation
let status: "active" | "inactive" = "active";

// Intersection type annotation
type PersonWithAge = { name: string } & { age: number };

// Generic annotation
const list: Array<number> = [1, 2, 3];
```

---

## Variable Annotations

### Primitives

```typescript
const name: string = "Alice";
const age: number = 30;
const isStudent: boolean = false;
const nothing: null = null;
const notDefined: undefined = undefined;
const uniqueId: symbol = Symbol("id");
const bigNumber: bigint = 9007199254740991n;
```

### Union Types

```typescript
// A value can be one of several types
let id: string | number;
id = "abc-123";
id = 42;

// Nullable types (with strictNullChecks)
let name: string | null = null;
name = "Alice";

// Multiple nullable types
let value: string | number | null | undefined;
```

### Literal Types

```typescript
// Specific string values
type Direction = "north" | "south" | "east" | "west";
const heading: Direction = "north";

// Specific number values
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
const roll: DiceRoll = 3;

// Specific boolean values
type Enabled = true;
const feature: Enabled = true;
```

### Type Aliases

```typescript
// Create reusable type names
type ID = string | number;
type Name = string;
type Age = number;

const userId: ID = "abc-123";
const userName: Name = "Alice";
const userAge: Age = 30;

// Complex type aliases
type Point = {
  x: number;
  y: number;
};

type Callback = (data: string) => void;
```

---

## Function Annotations

### Parameter Annotations

```typescript
// Explicit parameter types
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Multiple parameters
function createUser(name: string, age: number, email: string): User {
  return { name, age, email };
}

// Optional parameters (with ?)
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}!`;
}

// Default parameters
function greet(name: string, greeting: string = "Hello"): string {
  return `${greeting}, ${name}!`;
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}
```

### Return Type Annotations

```typescript
// Explicit return type
function add(a: number, b: number): number {
  return a + b;
}

// Void return type
function logMessage(message: string): void {
  console.log(message);
}

// Never return type (function never returns)
function throwError(message: string): never {
  throw new Error(message);
}

// Promise return types
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Complex return types
function processItems(items: Item[]): { processed: Item[]; count: number } {
  return {
    processed: items.map(processItem),
    count: items.length,
  };
}
```

### Function Type Aliases

```typescript
// Define function types explicitly
type MathOperation = (a: number, b: number) => number;

const add: MathOperation = (a, b) => a + b;
const subtract: MathOperation = (a, b) => a - b;
const multiply: MathOperation = (a, b) => a * b;

// With descriptive parameter names in the type
type EventHandler = (event: MouseEvent) => void;

// Generic function types
type Mapper<T, U> = (input: T) => U;

const stringToNumber: Mapper<string, number> = (s) => s.length;
const numberToString: Mapper<number, string> = (n) => n.toString();
```

### Function Overloads

```typescript
// Function overloads — multiple call signatures
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;
function format(value: string | number | Date): string {
  if (typeof value === "string") return value.toUpperCase();
  if (typeof value === "number") return value.toFixed(2);
  return value.toISOString();
}

format("hello");    // "HELLO"
format(3.14159);    // "3.14"
format(new Date()); // "2024-01-15T12:00:00.000Z"
```

---

## Object Annotations

### Inline Object Types

```typescript
// Inline object type annotation
const user: { name: string; age: number; email: string } = {
  name: "Alice",
  age: 30,
  email: "alice@example.com",
};

// Function with inline object parameter
function createUser(user: { name: string; age: number }): User {
  return {
    id: generateId(),
    ...user,
  };
}
```

### Interface Annotations

```typescript
// Interface declaration
interface User {
  name: string;
  age: number;
  email: string;
  isActive: boolean;
}

// Using the interface
const user: User = {
  name: "Alice",
  age: 30,
  email: "alice@example.com",
  isActive: true,
};

// Function with interface parameter
function processUser(user: User): string {
  return `${user.name} (${user.email})`;
}
```

### Optional Properties

```typescript
interface Config {
  apiUrl: string;
  timeout: number;
  retries?: number;        // Optional
  debug?: boolean;          // Optional
}

const config: Config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  // retries and debug are optional
};

// Accessing optional properties
const retries = config.retries ?? 3; // Default value if undefined
```

### Readonly Properties

```typescript
interface User {
  readonly id: string;
  readonly createdAt: Date;
  name: string;
  email: string;
}

const user: User = {
  id: "123",
  createdAt: new Date(),
  name: "Alice",
  email: "alice@example.com",
};

// user.id = "456"; // Error: readonly
user.name = "Bob"; // OK — not readonly
```

### Index Signatures

```typescript
// Object with dynamic keys
interface StringMap {
  [key: string]: string;
}

const translations: StringMap = {
  hello: "Hello",
  goodbye: "Goodbye",
  thanks: "Thank you",
};

// Typed dictionary
interface NumberDict {
  [key: string]: number;
}

const scores: NumberDict = {
  alice: 95,
  bob: 87,
  charlie: 92,
};
```

### Nested Object Types

```typescript
interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

interface User {
  name: string;
  age: number;
  address: Address;
  contacts: {
    email: string;
    phone?: string;
  };
}

const user: User = {
  name: "Alice",
  age: 30,
  address: {
    street: "123 Main St",
    city: "Springfield",
    state: "IL",
    zipCode: "62701",
    country: "US",
  },
  contacts: {
    email: "alice@example.com",
  },
};
```

---

## Array Annotations

### Basic Array Types

```typescript
// Method 1: Type[]
const numbers: number[] = [1, 2, 3];
const names: string[] = ["Alice", "Bob"];
const flags: boolean[] = [true, false, true];

// Method 2: Array<Type> (generic syntax)
const numbers: Array<number> = [1, 2, 3];
const names: Array<string> = ["Alice", "Bob"];

// Both methods are equivalent
```

### Arrays of Objects

```typescript
interface User {
  name: string;
  age: number;
}

const users: User[] = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

// Or using Array<User>
const users: Array<User> = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];
```

### Multidimensional Arrays

```typescript
// 2D array
const matrix: number[][] = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];

// 3D array
const cube: number[][][] = [
  [[1, 2], [3, 4]],
  [[5, 6], [7, 8]],
];

// Array of arrays of objects
const grid: User[][] = [
  [user1, user2],
  [user3, user4],
];
```

### Readonly Arrays

```typescript
// Readonly array — cannot be modified
const numbers: readonly number[] = [1, 2, 3];
// numbers.push(4);    // Error
// numbers[0] = 10;    // Error

// ReadonlyArray type (same as readonly T[])
const names: ReadonlyArray<string> = ["Alice", "Bob"];
// names.push("Charlie"); // Error

// Readonly tuple
const point: readonly [number, number] = [10, 20];
```

### Sparse Arrays

```typescript
// Arrays with holes
const sparse: (number | undefined)[] = [1, , 3];
// TypeScript treats this as (number | undefined)[]

// Safer approach
const sparse: Array<number | undefined> = [1, undefined, 3];
```

---

## Tuple Annotations

Tuples are **fixed-length arrays** where each element has a specific type.

### Basic Tuples

```typescript
// Tuple: [type1, type2, ...]
const point: [number, number] = [10, 20];
const person: [string, number] = ["Alice", 30];
const triple: [string, number, boolean] = ["hello", 42, true];

// Accessing tuple elements
const x = point[0]; // number
const y = point[1]; // number

// Destructuring
const [name, age] = person; // name: string, age: number
```

### Named Tuples (Documentation Only)

```typescript
// Named elements for documentation (type names are not enforced)
type Range = [start: number, end: number];
type Color = [red: number, green: number, blue: number];

const range: Range = [0, 100];
const color: Color = [255, 128, 0];
```

### Optional Tuple Elements

```typescript
// Optional elements at the end
type Response = [status: number, data: string, timestamp?: Date];

const success: Response = [200, "OK", new Date()];
const error: Response = [404, "Not Found"]; // timestamp is optional

// Accessing optional elements
const ts = success[2]; // Date | undefined
```

### Rest Elements in Tuples

```typescript
// Tuples with rest elements
type StringAndNumbers = [string, ...number[]];

const mixed: StringAndNumbers = ["hello", 1, 2, 3];
const single: StringAndNumbers = ["hello"];

// Leading rest element
type NumbersAndString = [...number[], string];
const nums: NumbersAndString = [1, 2, 3, "end"];

// Multiple rest elements (not allowed)
// type Invalid = [...number[], ...string[]]; // Error
```

### Readonly Tuples

```typescript
// Readonly tuples — cannot be modified
const point: readonly [number, number] = [10, 20];
// point[0] = 30; // Error: readonly

// Useful as function parameters
function move(point: readonly [number, number], dx: number, dy: number): [number, number] {
  return [point[0] + dx, point[1] + dy];
}
```

### Tuple vs Array

```typescript
// Tuple — fixed length and types
const person: [string, number] = ["Alice", 30];
// person.push(true); // Error — tuple has fixed length

// Array — variable length, same type
const numbers: number[] = [1, 2, 3];
numbers.push(4); // OK — array can grow

// Tuple access — exact type
const name = person[0]; // string (exact type)
const age = person[1];  // number (exact type)

// Array access — element type or undefined
const first = numbers[0];    // number
const big = numbers[100];    // number (but actually undefined at runtime!)
```

---

## Annotation Best Practices

### 1. Annotate Function Parameters

```typescript
// GOOD — parameters are annotated
function processUser(user: User): string {
  return user.name;
}

// BAD — parameter has implicit 'any' type
function processUser(user) { // Error in strict mode
  return user.name;
}
```

### 2. Let TypeScript Infer Return Types (Simple Functions)

```typescript
// GOOD — return type is inferred for simple functions
const add = (a: number, b: number) => a + b; // number (inferred)

// GOOD — return type is annotated for complex functions
function fetchData(url: string): Promise<Response> {
  return fetch(url);
}
```

### 3. Annotate Public API Surface

```typescript
// Library code — annotate everything public
export function processOrder(order: Order): ProcessedOrder {
  // ...
}

// Internal code — can rely on inference
const items = order.items.filter((item) => item.active);
```

### 4. Use Type Aliases for Repeated Types

```typescript
// BAD — repeating the same type
function createUser(name: string, age: number, email: string): { name: string; age: number; email: string } {
  // ...
}

function updateUser(user: { name: string; age: number; email: string }): void {
  // ...
}

// GOOD — using a type alias
interface User {
  name: string;
  age: number;
  email: string;
}

function createUser(name: string, age: number, email: string): User {
  // ...
}

function updateUser(user: User): void {
  // ...
}
```

### 5. Avoid Redundant Annotations

```typescript
// BAD — redundant annotation
const name: string = "Alice"; // TypeScript already knows this is a string

// GOOD — let TypeScript infer
const name = "Alice";

// When annotation IS helpful
let name: string | null = null; // Annotation clarifies the type
```

### 6. Use readonly for Immutable Data

```typescript
// GOOD — readonly for data that shouldn't change
function processItems(items: readonly Item[]): Result {
  // ...
}

// GOOD — readonly arrays as return types
function getStaticData(): readonly Config[] {
  return Object.freeze([...configs]);
}
```

### 7. Annotate Complex Object Types

```typescript
// GOOD — clear object type
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: Date;
}

// BAD — inline type is hard to read
function fetchData(): { data: User; status: number; message: string; timestamp: Date } {
  // ...
}
```

---

## Common Patterns

### Discriminated Unions

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

### Type Assertions

```typescript
// When you know more than TypeScript
const input = document.getElementById("name") as HTMLInputElement;
input.value = "Alice";

// const assertions
const config = {
  apiUrl: "https://api.example.com",
} as const;
```

### Satisfies Operator

```typescript
// Satisfies — validates type without widening
type Colors = Record<string, [number, number, number]>;

const palette = {
  red: [255, 0, 0],
  green: [0, 255, 0],
  blue: [0, 0, 255],
} satisfies Colors;

// palette.red is [number, number, number] (not just number[])
palette.red.map((c) => c.toString()); // OK
```

---

## Summary

| Annotation Type | Syntax | Example |
|----------------|--------|---------|
| Variable | `x: Type` | `const x: number = 42` |
| Function parameter | `(x: Type)` | `(name: string)` |
| Function return | `(): Type` | `(): string` |
| Array | `Type[]` or `Array<Type>` | `number[]` |
| Tuple | `[Type, Type]` | `[string, number]` |
| Object | `{ key: Type }` | `{ name: string; age: number }` |
| Union | `Type \| Type` | `string \| number` |
| Intersection | `Type & Type` | `Named & Aged` |
| Optional | `key?: Type` | `name?: string` |
| Readonly | `readonly prop: Type` | `readonly id: string` |

> **Golden Rules:**
> 1. Always annotate function parameters
> 2. Let TypeScript infer simple variable types
> 3. Annotate return types for complex functions
> 4. Use interfaces/types for repeated object shapes
> 5. Avoid redundant annotations
> 6. Use `readonly` for immutable data
