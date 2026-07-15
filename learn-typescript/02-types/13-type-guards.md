# Type Guards in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [typeof Guards](#typeof-guards)
3. [instanceof Guards](#instanceof-guards)
4. [in Guards](#in-guards)
5. [User-Defined Type Guards](#user-defined-type-guards)
6. [Assertion Function Type Guards](#assertion-function-type-guards)
7. [Discriminated Union Guards](#discriminated-union-guards)
8. [Null Guards](#null-guards)
9. [Truthiness Guards](#truthiness-guards)
10. [Custom Type Guard Functions](#custom-type-guard-functions)
11. [Exhaustiveness Checking](#exhaustiveness-checking)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## Overview

Type guards are expressions that perform runtime checks and narrow the type within a control flow block. They are essential for working with union types and `unknown`.

---

## typeof Guards

The `typeof` operator checks the type of a value at runtime.

```typescript
// Basic typeof narrowing
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

// typeof with null/undefined
function format(value: string | null | undefined): string {
  if (typeof value === "string") {
    return value;
  }
  return "N/A";
}

// typeof in switch statements
function describe(value: string | number | boolean | null): string {
  switch (typeof value) {
    case "string":
      return `String: ${value}`;
    case "number":
      return `Number: ${value}`;
    case "boolean":
      return `Boolean: ${value}`;
    case "undefined":
      return "undefined";
    default:
      return "null"; // typeof null === "object"
  }
}

// ⚠️ typeof null === "object" (a JavaScript quirk)
function isNull(value: unknown): boolean {
  return typeof value === "object" && value === null;
}

// typeof with typeof expressions
function getType(value: unknown): string {
  if (typeof value === "string") return "string";
  if (typeof value === "number") return "number";
  if (typeof value === "boolean") return "boolean";
  if (typeof value === "function") return "function";
  if (typeof value === "object") return "object";
  return "unknown";
}

// typeof in conditional types (compile-time)
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<42>;      // false
```

---

## instanceof Guards

The `instanceof` operator checks if an object is an instance of a class.

```typescript
// Basic instanceof
function handleError(error: Error | string): string {
  if (error instanceof Error) {
    return error.message; // narrowed to Error
  }
  return error; // narrowed to string
}

// instanceof with custom classes
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string,
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

class NetworkError extends Error {
  constructor(
    message: string,
    public statusCode: number,
  ) {
    super(message);
    this.name = "NetworkError";
  }
}

function handleAppError(error: ValidationError | NetworkError | string): string {
  if (error instanceof ValidationError) {
    return `Validation error on field "${error.field}": ${error.message}`;
  }
  if (error instanceof NetworkError) {
    return `Network error ${error.statusCode}: ${error.message}`;
  }
  return error;
}

// instanceof with built-in classes
function processInput(input: string | RegExp | Date): string {
  if (input instanceof RegExp) {
    return input.source;
  }
  if (input instanceof Date) {
    return input.toISOString();
  }
  return input;
}

// instanceof with Promise
async function handleResult(result: Promise<string> | string): Promise<string> {
  if (result instanceof Promise) {
    return await result;
  }
  return result;
}

// ⚠️ instanceof doesn't work across different globals (iframes, etc.)
// Use duck typing or type guards instead
```

---

## in Guards

The `in` operator checks if a property exists on an object.

```typescript
// Basic in narrowing
interface Fish {
  swim: () => void;
  name: string;
}

interface Bird {
  fly: () => void;
  name: string;
}

function move(animal: Fish | Bird): string {
  if ("swim" in animal) {
    animal.swim(); // narrowed to Fish
    return `${animal.name} is swimming`;
  }
  animal.fly(); // narrowed to Bird
  return `${animal.name} is flying`;
}

// in with optional properties
interface User {
  name: string;
  email: string;
  address?: {
    street: string;
    city: string;
  };
}

function getCity(user: User): string {
  if ("address" in user && user.address) {
    return user.address.city;
  }
  return "Unknown";
}

// in with discriminated unions
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function describe(shape: Shape): string {
  if ("radius" in shape) {
    return `Circle with radius ${shape.radius}`;
  }
  return `Square with side ${shape.side}`;
}

// in vs optional chaining
interface Config {
  db?: {
    host: string;
    port: number;
  };
}

function getPort(config: Config): number {
  // Using in guard
  if ("db" in config && config.db) {
    return config.db.port;
  }

  // Using optional chaining (often cleaner)
  return config.db?.port ?? 5432;
}

// in with hasOwnProperty
function hasProperty<T, K extends string>(
  obj: T,
  key: K,
): obj is T & Record<K, unknown> {
  return typeof obj === "object" && obj !== null && key in obj;
}
```

---

## User-Defined Type Guards

Type guards that return a boolean with a type predicate using the `is` keyword.

```typescript
// Basic type guard with 'is'
interface Cat {
  type: "cat";
  meow(): void;
  purr(): void;
}

interface Dog {
  type: "dog";
  bark(): void;
  fetch(): void;
}

type Pet = Cat | Dog;

function isCat(pet: Pet): pet is Cat {
  return pet.type === "cat";
}

function isDog(pet: Pet): pet is Dog {
  return pet.type === "dog";
}

function handlePet(pet: Pet): void {
  if (isCat(pet)) {
    pet.meow();  // narrowed to Cat
    pet.purr();  // narrowed to Cat
  } else {
    pet.bark();  // narrowed to Dog
    pet.fetch(); // narrowed to Dog
  }
}

// Type guard for primitive unions
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isNumber(value: unknown): value is number {
  return typeof value === "number";
}

function process(value: string | number | boolean): string {
  if (isString(value)) {
    return value.toUpperCase();
  }
  if (isNumber(value)) {
    return value.toFixed(2);
  }
  return value.toString();
}

// Type guard for objects
interface User {
  id: number;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as User).id === "number" &&
    typeof (value as User).name === "string" &&
    typeof (value as User).email === "string"
  );
}

function processUser(data: unknown): string {
  if (isUser(data)) {
    return `User: ${data.name} (${data.email})`;
  }
  return "Invalid user";
}

// Type guard with arrays
function isStringArray(value: unknown): value is string[] {
  return (
    Array.isArray(value) &&
    value.every((item) => typeof item === "string")
  );
}

// Type guard for nullable types
function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const items = [1, null, 2, undefined, 3];
const definedItems = items.filter(isDefined); // number[]
```

---

## Assertion Function Type Guards

Assertion functions throw an error if the condition is false, narrowing the type.

```typescript
// Basic assertion function
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`Expected string, got ${typeof value}`);
  }
}

function process(value: string | number): string {
  assertIsString(value); // narrows 'value' to string after this line
  return value.toUpperCase(); // OK
}

// Assertion function for objects
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

function handleData(data: unknown): string {
  assertIsUser(data);
  // data is narrowed to User
  return `${data.name} (${data.email})`;
}

// Assertion function for arrays
function assertNonEmptyArray<T>(value: T[]): asserts value is [T, ...T[]] {
  if (value.length === 0) {
    throw new Error("Array is empty");
  }
}

function first<T>(arr: T[]): T {
  assertNonEmptyArray(arr);
  return arr[0]; // narrowed to T (not T | undefined)
}

// Assertion function for null/undefined
function assertDefined<T>(
  value: T | null | undefined,
  message: string,
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}

function getLength(value: string | null | undefined): number {
  assertDefined(value, "Value must be defined");
  return value.length; // narrowed to string
}

// Assertion function in class methods
class Validator {
  assertValidAge(value: unknown): asserts value is number {
    if (typeof value !== "number" || value < 0 || value > 150) {
      throw new Error("Invalid age");
    }
  }
}
```

---

## Discriminated Union Guards

Using the discriminant property to narrow discriminated unions.

```typescript
// Basic discriminated union guard
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
  }
}

// Real-world: API response guard
type ApiResponse<T> =
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function handleResponse(response: ApiResponse<User>): string {
  switch (response.status) {
    case "loading":
      return "Loading...";
    case "success":
      return `User: ${response.data.name}`;
    case "error":
      return `Error: ${response.error.message}`;
  }
}

// Discriminated union guard function
function isSuccess<T>(
  response: ApiResponse<T>,
): response is { status: "success"; data: T } {
  return response.status === "success";
}

function isError(
  response: ApiResponse<unknown>,
): response is { status: "error"; error: Error } {
  return response.status === "error";
}

// Using guards
function processData(response: ApiResponse<User>): void {
  if (isSuccess(response)) {
    console.log(response.data.name); // narrowed to success
  } else if (isError(response)) {
    console.error(response.error.message); // narrowed to error
  }
  // loading case falls through
}

// Discriminated union with multiple discriminants
type Event =
  | { type: "click"; x: number; y: number }
  | { type: "keypress"; key: string }
  | { type: "focus"; target: HTMLElement };

function handleEvent(event: Event): string {
  switch (event.type) {
    case "click":
      return `Click at (${event.x}, ${event.y})`;
    case "keypress":
      return `Key: ${event.key}`;
    case "focus":
      return `Focus on ${event.target.tagName}`;
  }
}
```

---

## Null Guards

Checking for null and undefined values.

```typescript
// Strict null checks (recommended)
function getLength(value: string | null | undefined): number {
  if (value === null || value === undefined) {
    return 0;
  }
  return value.length; // narrowed to string
}

// Optional chaining (shorthand for null/undefined checks)
function getCity(user: { address?: { city: string } }): string {
  return user.address?.city ?? "Unknown";
}

// Nullish coalescing
function processValue(value: string | null | undefined): string {
  return value ?? "default"; // Returns "default" for null/undefined
}

// Type guard for nullable
function isNotNull<T>(value: T | null): value is T {
  return value !== null;
}

function isDefined2<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

// Filtering nullable values
const items = [1, null, 2, undefined, 3, null];
const defined = items.filter(isDefined2); // number[]

// Non-null assertion (use sparingly!)
function processElement(element: HTMLElement | null): void {
  // element!.className; // Non-null assertion — risky
  if (element) {
    element.className; // Safer — type narrowed
  }
}

// Assertion function for null
function assertNonNull<T>(
  value: T | null | undefined,
  message?: string,
): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error(message ?? "Value is null or undefined");
  }
}

// Null check in optional chaining
interface Config {
  database?: {
    connection?: {
      host: string;
      port: number;
    };
  };
}

function getHost(config: Config): string {
  return config.database?.connection?.host ?? "localhost";
}
```

---

## Truthiness Guards

Using truthiness/falsy values to narrow types.

```typescript
// Truthiness narrowing
function processValue(value: string | null | undefined): string {
  if (value) {
    // value is string (null and undefined are falsy)
    return value.toUpperCase();
  }
  return "N/A";
}

// Truthiness in filter callbacks
const items = [1, 0, 2, null, 3, undefined, 4, false, 5];
const truthyItems = items.filter(Boolean); // [1, 2, 3, 4, 5]

// ⚠️ Boolean filter loses type information
// Use a type guard for proper typing
function isTruthy<T>(value: T): value is T & truthy {
  return Boolean(value);
}
// (Note: 'truthy' is not a built-in type — this is conceptual)

// Truthiness in loop conditions
function processArray(arr: (string | null | undefined)[]): string {
  let result = "";
  for (const item of arr) {
    if (item) {
      result += item; // narrowed to string
    }
  }
  return result;
}

// Truthiness with default values
function greet(name: string | null | undefined): string {
  const displayName = name || "Guest"; // Fallback for null/undefined/empty string
  return `Hello, ${displayName}!`;
}

// ⚠️ || vs ?? — important distinction
function getPort(value: number | null | undefined): number {
  return value || 3000; // Falls back for 0 too!
  return value ?? 3000; // Only falls back for null/undefined
}
```

---

## Custom Type Guard Functions

Building reusable type guard functions.

```typescript
// Comprehensive type guard for objects
function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// Type guard for arrays
function isArray<T>(value: unknown): value is T[] {
  return Array.isArray(value);
}

// Type guard with specific structure
interface Point {
  x: number;
  y: number;
}

function isPoint(value: unknown): value is Point {
  return (
    isObject(value) &&
    "x" in value &&
    "y" in value &&
    typeof value.x === "number" &&
    typeof value.y === "number"
  );
}

// Composable type guards
function hasProperty<T extends object, K extends string>(
  obj: T,
  key: K,
): obj is T & Record<K, unknown> {
  return key in obj;
}

function isUserWithAge(value: unknown): value is User & { age: number } {
  return isUser(value) && hasProperty(value, "age") && typeof value.age === "number";
}

// Type guard factory
function createIsInstanceOf<T>(
  constructor: new (...args: any[]) => T,
): (value: unknown) => value is T {
  return (value: unknown): value is T => value instanceof constructor;
}

const isDate = createIsInstanceOf(Date);
const isRegExp = createIsInstanceOf(RegExp);

// Type guard for nested structures
interface TreeNode {
  value: number;
  left?: TreeNode;
  right?: TreeNode;
}

function isTreeNode(value: unknown): value is TreeNode {
  return (
    isObject(value) &&
    "value" in value &&
    typeof value.value === "number" &&
    (!("left" in value) || isTreeNode(value.left)) &&
    (!("right" in value) || isTreeNode(value.right))
  );
}

// Type guard with async validation
async function is ValidUser(data: unknown): Promise<data is User> {
  if (!isObject(data)) return false;
  if (!("id" in data) || typeof data.id !== "number") return false;
  if (!("name" in data) || typeof data.name !== "string") return false;
  if (!("email" in data) || typeof data.email !== "string") return false;
  // Could also make API call to validate
  return true;
}
```

---

## Exhaustiveness Checking

Using `never` to ensure all cases are handled.

```typescript
// Basic exhaustive check
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      return assertNever(shape); // Compile error if missing a case
  }
}

// Exhaustive check in if-else
function handleStatus(status: "active" | "inactive" | "pending"): string {
  if (status === "active") return "Active";
  if (status === "inactive") return "Inactive";
  if (status === "pending") return "Pending";
  return assertNever(status);
}

// Exhaustive check with never in conditional types
type ExhaustiveCheck<T extends never> = T;

// Real-world: action handler
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
    default:
      return assertNever(action);
  }
  // If you add a new action type and forget to handle it,
  // TypeScript will produce a compile error
}
```

---

## Best Practices

1. **Always prefer type guards over type assertions** — they're safer
2. **Use discriminated unions** for objects with different shapes — enables exhaustive checking
3. **Use `typeof` for primitive type narrowing** — it's the simplest and fastest
4. **Use `instanceof` for class instance checks** — it's reliable for custom classes
5. **Use `in` for property existence checks** — especially for duck typing
6. **Use `is` keyword** for user-defined type guards — enables narrowing in callbacks
7. **Use assertion functions** for preconditions — they narrow and throw
8. **Always include exhaustive checking** with `never` in switch statements
9. **Prefer optional chaining** (`?.`) over explicit null checks when possible
10. **Use `Array.filter(Boolean)`** for filtering falsy values (but lose type info)

---

## Interview Questions

### Q1: What are type guards in TypeScript?

**Answer:** Type guards are runtime checks that narrow the type of a value within a control flow block. They include `typeof`, `instanceof`, `in`, custom type guards with `is`, and assertion functions.

### Q2: What is the difference between a type guard and a type assertion?

**Answer:** A type guard (`if (typeof x === "string")`) is a runtime check that safely narrows the type. A type assertion (`x as string`) is a compile-time hint that tells TypeScript to treat a value as a specific type without runtime verification.

### Q3: What is an assertion function?

**Answer:** A function that returns `void` and uses `asserts` to narrow a parameter's type. If the assertion fails, it throws an error. If it succeeds, the parameter is narrowed: `function assertString(v: unknown): asserts v is string`.

### Q4: What is exhaustive checking?

**Answer:** Using `never` in a default switch case to ensure all union members are handled. If a new member is added to the union and not handled in the switch, TypeScript produces a compile error.

### Q5: When would you use `in` over `typeof`?

**Answer:** Use `in` when checking for the existence of a property on an object (duck typing). Use `typeof` when checking the primitive type of a value. `in` is useful for narrowing union types of objects with different property shapes.
