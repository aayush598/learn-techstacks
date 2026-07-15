# Union Types in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Union Type Syntax](#union-type-syntax)
3. [Union of Primitives](#union-of-primitives)
4. [Union of Objects](#union-of-objects)
5. [Union with Type Narrowing](#union-with-type-narrowing)
6. [Discriminated Unions](#discriminated-unions)
7. [Union Type Checking](#union-type-checking)
8. [Assignability with Unions](#assignability-with-unions)
9. [Union of Functions](#union-of-functions)
10. [Union of Enums](#union-of-enums)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

A union type represents a value that can be one of several types. Use the `|` (pipe) operator to create unions.

```typescript
// A variable that can be string OR number
let id: string | number;
id = "abc-123"; // OK
id = 42;        // OK
// id = true;   // Error: boolean not in union

// Union of object types
type Success = { status: "ok"; data: string };
type Failure = { status: "error"; message: string };
type Result = Success | Failure;
```

---

## Union Type Syntax

```typescript
// Basic union
type StringOrNumber = string | number;

// Union with more types
type Primitive = string | number | boolean | null | undefined;

// Union of object types
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

// Union with existing types
type ID = string | number;
type NullableString = string | null;
type OptionalNumber = number | undefined;

// Nested unions
type A = string | number;
type B = boolean | null;
type C = A | B; // string | number | boolean | null

// Union in function parameters
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

// Union in return types
function getLength(value: string | any[]): number {
  return value.length;
}

// Union in type positions
type Container = { value: string | number };
const a: Container = { value: "hello" };
const b: Container = { value: 42 };
```

---

## Union of Primitives

```typescript
// Common primitive unions
type ID = string | number;
type Status = "active" | "inactive" | "pending";
type ErrorCode = 400 | 401 | 403 | 404 | 500;
type Switch = true | false;

// Using primitive unions in APIs
function fetchUser(id: string | number): Promise<User> {
  return fetch(`/api/users/${id}`);
}

function setStatus(status: "active" | "inactive"): void {
  document.body.dataset.status = status;
}

// Narrowing primitive unions
function formatValue(value: string | number | boolean): string {
  switch (typeof value) {
    case "string":
      return value.toUpperCase();
    case "number":
      return value.toFixed(2);
    case "boolean":
      return value ? "Yes" : "No";
  }
}

// Union with literal types
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type CSSUnit = "px" | "em" | "rem" | "%";
type Theme = "light" | "dark" | "system";

// Discriminated union with primitives
type Result =
  | { type: "success"; data: unknown }
  | { type: "error"; message: string };
```

---

## Union of Objects

```typescript
// Union of different object shapes
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  side: number;
}

interface Triangle {
  kind: "triangle";
  base: number;
  height: number;
}

type Shape = Circle | Square | Triangle;

// Accessing properties
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}

// Common properties are accessible directly
function getKind(shape: Shape): string {
  return shape.kind; // All shapes have 'kind'
}

// Different properties require narrowing
function describe(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return `Circle with radius ${shape.radius}`;
    case "square":
      return `Square with side ${shape.side}`;
    case "triangle":
      return `Triangle with base ${shape.base} and height ${shape.height}`;
  }
}

// Union of similar objects
type User = {
  id: number;
  name: string;
  email: string;
};

type Admin = {
  id: number;
  name: string;
  email: string;
  role: "admin";
  permissions: string[];
};

type Person = User | Admin;

// Common properties accessible
function greet(person: Person): string {
  return `Hello, ${person.name}`; // name exists on both
}

// Specific properties require narrowing
function getPermissions(person: Person): string[] {
  if ("role" in person && person.role === "admin") {
    return person.permissions;
  }
  return [];
}
```

---

## Union with Type Narrowing

```typescript
// typeof narrowing
function process(value: string | number | boolean): string {
  if (typeof value === "string") {
    // value is string here
    return value.toUpperCase();
  }
  if (typeof value === "number") {
    // value is number here
    return value.toFixed(2);
  }
  // value is boolean here
  return value.toString();
}

// instanceof narrowing
function handleError(error: Error | string): string {
  if (error instanceof Error) {
    return error.message;
  }
  return error;
}

// in operator narrowing
type Fish = { swim: () => void; name: string };
type Bird = { fly: () => void; name: string };

function move(animal: Fish | Bird): void {
  if ("swim" in animal) {
    animal.swim(); // narrowed to Fish
  } else {
    animal.fly(); // narrowed to Bird
  }
}

// Equality narrowing
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // Both are string (only common type)
    console.log(x.toUpperCase(), y.toUpperCase());
  }
}

// Custom type guard
function isFish(animal: Fish | Bird): animal is Fish {
  return "swim" in animal;
}

function handleAnimal(animal: Fish | Bird): void {
  if (isFish(animal)) {
    animal.swim();
  } else {
    animal.fly();
  }
}

// Truthiness narrowing
function processValue(value: string | null | undefined): number {
  if (value) {
    // narrowed to string (null/undefined are falsy)
    return value.length;
  }
  return 0;
}

// Assertion functions
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Expected string");
  }
}

function useString(value: string | number): string {
  assertIsString(value);
  // value is narrowed to string here
  return value.toUpperCase();
}
```

---

## Discriminated Unions

Discriminated unions use a common literal property (discriminant) to narrow the union.

```typescript
// Basic discriminated union
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}

// Real-world: API response
type ApiResponse<T> =
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function handleResponse(response: ApiResponse<User>): void {
  switch (response.status) {
    case "loading":
      console.log("Loading...");
      break;
    case "success":
      console.log(response.data.name); // narrowed to data
      break;
    case "error":
      console.error(response.error.message); // narrowed to error
      break;
  }
}

// Real-world: Redux actions
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "SET"; value: number }
  | { type: "RESET" };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT":
      return state + action.amount;
    case "DECREMENT":
      return state - action.amount;
    case "SET":
      return action.value;
    case "RESET":
      return 0;
  }
}

// Exhaustive checking with never
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

function processAction(action: Action): void {
  switch (action.type) {
    case "INCREMENT":
      break;
    case "DECREMENT":
      break;
    case "SET":
      break;
    case "RESET":
      break;
    default:
      assertNever(action); // Compile error if a case is missing
  }
}

// Nested discriminated unions
type Event =
  | { kind: "click"; x: number; y: number }
  | { kind: "keypress"; key: string }
  | { kind: "focus"; target: HTMLElement }
  | { kind: "blur"; target: HTMLElement };

function handleEvent(event: Event): void {
  switch (event.kind) {
    case "click":
      console.log(`Click at (${event.x}, ${event.y})`);
      break;
    case "keypress":
      console.log(`Key: ${event.key}`);
      break;
    case "focus":
    case "blur":
      console.log(`Target: ${event.target.tagName}`);
      break;
  }
}
```

---

## Union Type Checking

```typescript
// Assignability
let value: string | number;
value = "hello"; // OK
value = 42;      // OK
// value = true; // Error

// Union of wider type accepts narrower types
let wider: string | number | boolean;
let narrow: string = "hello";
wider = narrow; // OK — string is in the union

// Narrowing narrows the union
function narrow(value: string | number | boolean): void {
  if (typeof value === "string") {
    // value: string
    let s: string = value; // OK
    // let n: number = value; // Error
  }
}

// Union in generic constraints
function first<T extends string | number>(arr: T[]): T | undefined {
  return arr[0];
}

const n = first([1, 2, 3]);     // number | undefined
const s = first(["a", "b"]);    // string | undefined

// Union of union types (flattened)
type A = "a" | "b";
type B = "b" | "c";
type C = A | B; // "a" | "b" | "c" (flattened, no duplicates)

// Union distribution over conditional types
type ToArray<T> = T extends any ? T[] : never;

type StrArr = ToArray<string | number>; // string[] | number[] (distributed)

// Prevent distribution with brackets
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;

type StrArr2 = ToArrayNonDist<string | number>; // (string | number)[] (not distributed)
```

---

## Assignability with Unions

```typescript
// A union type accepts values that match ANY member
type StringOrNumber = string | number;

const a: StringOrNumber = "hello"; // OK
const b: StringOrNumber = 42;      // OK

// Specific literal types are assignable to unions containing them
type Status = "active" | "inactive" | "pending";
const active: Status = "active"; // OK
const specific: "active" = "active"; // OK

// Object assignability with unions
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

const circle: Shape = { kind: "circle", radius: 10 }; // OK
const square: Shape = { kind: "square", side: 5 };    // OK

// Excess property checking still applies to unions
// const bad: Shape = { kind: "circle", radius: 10, color: "red" }; // Error!

// Workaround: assign to variable first
const circleObj = { kind: "circle", radius: 10, color: "red" };
const good: Shape = circleObj; // OK (no excess checking on variables)

// Union assignability with function types
type Callback = ((x: number) => string) | ((x: string) => number);

// A function that handles both cases is assignable
const fn: Callback = (x: any) => x.toString(); // OK

// Union of arrays
const arr: (string | number)[] = [1, "two", 3];
const arr2: string[] | number[] = [1, 2, 3]; // Different! Must be all strings or all numbers
```

---

## Union of Functions

```typescript
// Union of function types
type Formatter = ((x: number) => string) | ((x: Date) => string);

// Calling union functions requires narrowing
function format(value: string | number, formatter: Formatter): string {
  if (typeof value === "number") {
    return (formatter as (x: number) => string)(value);
  }
  return "unknown";
}

// Function overload-like behavior with unions
type Handler = {
  (event: "click"): void;
  (event: "keypress"): void;
};

// Union of function signatures
type Factory = {
  new (name: string): { name: string };
  (name: string): string;
};

// Common pattern: optional callback
type OnComplete = ((result: string) => void) | null;

function fetchData(onComplete: OnComplete): void {
  const result = "done";
  if (onComplete) {
    onComplete(result);
  }
}

// Union in generic function types
type Middleware<T> = (next: T) => T | Promise<T>;
type SyncMiddleware = (next: number) => number;
type AsyncMiddleware = (next: number) => Promise<number>;
```

---

## Union of Enums

```typescript
enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE",
}

enum Size {
  Small = "SMALL",
  Medium = "MEDIUM",
  Large = "LARGE",
}

// Union of enum values
type ColorOrSize = Color | Size;
const a: ColorOrSize = Color.Red;   // OK
const b: ColorOrSize = Size.Small;  // OK

// Narrowing union of enums
function process(value: ColorOrSize): string {
  if (Object.values(Color).includes(value as Color)) {
    return `Color: ${value}`;
  }
  return `Size: ${value}`;
}

// Union of enum and literal
type Theme = Color | "system" | "auto";
const t: Theme = "system";    // OK
const t2: Theme = Color.Red;  // OK

// Discriminated union with enums
type Event2 =
  | { type: Color.Red; data: string }
  | { type: Color.Green; data: number }
  | { type: Color.Blue; data: boolean };

// Enum values in switch
function handle(value: Color): string {
  switch (value) {
    case Color.Red:   return "Red";
    case Color.Green: return "Green";
    case Color.Blue:  return "Blue";
  }
}
```

---

## Best Practices

1. **Use discriminated unions** for objects with different shapes — they enable exhaustive checking
2. **Always include a `default` case** with `never` for exhaustive narrowing
3. **Use literal unions** (`"active" | "inactive"`) over enums when you don't need runtime values
4. **Prefer `unknown` + narrowing** over `any` + union for API boundaries
5. **Use type guards** for complex narrowing logic
6. **Don't overuse unions** — if you have 10+ members, consider an object or enum
7. **Use `as const`** for literal unions from arrays/objects
8. **Narrow early** — check types at the beginning of functions
9. **Use exhaustive checking** to catch missing cases when new union members are added
10. **Document union members** — add comments explaining when each member is used

---

## Interview Questions

### Q1: What is a union type?

**Answer:** A union type represents a value that can be one of several types, created with the `|` operator. For example, `string | number` means the value can be either a string or a number.

### Q2: What is a discriminated union?

**Answer:** A union of object types sharing a common discriminant property (a literal type field). TypeScript uses the discriminant to narrow the union:
```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };
```

### Q3: How do you narrow a union type?

**Answer:** Using `typeof`, `instanceof`, `in` operator, equality checks, custom type guards (`is` keyword), assertion functions, and discriminated union switches.

### Q4: What is exhaustive checking?

**Answer:** Using `never` in a default switch case to ensure all union members are handled. If a new member is added to the union, the compiler will produce an error if it's not handled.

### Q5: Can a union type have both object and primitive types?

**Answer:** Yes. `string | { name: string }` is valid. However, accessing properties on the object requires narrowing since primitives don't have those properties.
