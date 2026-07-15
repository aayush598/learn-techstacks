# Type Narrowing in TypeScript

Type narrowing is the process of transforming a broad type into a more specific type within a conditional branch. TypeScript's compiler automatically narrows types through **control flow analysis**, making your code safer and more expressive without explicit casts.

---

## Table of Contents

1. [What is Type Narrowing?](#what-is-type-narrowing)
2. [Control Flow Analysis](#control-flow-analysis)
3. [Truthiness Narrowing](#truthiness-narrowing)
4. [Equality Narrowing](#equality-narrowing)
5. [typeof Narrowing](#typeof-narrowing)
6. [instanceof Narrowing](#instanceof-narrowing)
7. [in Narrowing](#in-narrowing)
8. [Assignment Narrowing](#assignment-narrowing)
9. [User-Defined Type Guards (`is`)](#user-defined-type-guards)
10. [Assertion Functions](#assertion-functions)
11. [Exhaustive Narrowing with `never`](#exhaustive-narrowing-with-never)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## What is Type Narrowing?

Type narrowing is when TypeScript **automatically infers** a more specific type within a code branch. Instead of manually asserting types, you write conditional checks that the compiler understands.

```typescript
function processValue(value: string | number | boolean) {
  // `value` is string | number | boolean here

  if (typeof value === "string") {
    // `value` is narrowed to `string`
    console.log(value.toUpperCase());
  } else if (typeof value === "number") {
    // `value` is narrowed to `number`
    console.log(value.toFixed(2));
  } else {
    // `value` is narrowed to `boolean`
    console.log(value ? "truthy" : "falsy");
  }
}
```

Without narrowing, you would need type assertions everywhere:

```typescript
// Without narrowing — verbose and unsafe
function processValue(value: string | number | boolean) {
  console.log((value as string).toUpperCase()); // runtime error if not string!
}
```

Narrowing eliminates unsafe casts and lets the compiler verify type safety for you.

---

## Control Flow Analysis

TypeScript performs **control flow analysis** — it tracks the type of each variable at every point in the code by following branches, assignments, and checks.

```typescript
function example(x: string | number | boolean) {
  // x: string | number | boolean

  if (typeof x === "string") {
    // x: string
    x; // string
  } else {
    // x: number | boolean
    if (typeof x === "number") {
      // x: number
    } else {
      // x: boolean
    }
  }

  // After the if/else, back to the original union
  // x: string | number | boolean
}
```

TypeScript tracks narrowing through:
- **Assignment**: assigning a narrower type
- **Return/throw**: control flow exits
- **Type predicates**: functions returning `boolean` with `is`
- **Equality checks**: `===`, `!==`, `==`, `!=`
- **Truthiness checks**: `if (value)`, `!value`
- **`instanceof` and `in` operators**

### Narrowing with Truthiness Guards Early Return

```typescript
function getLength(value: string | null): number {
  if (value === null) {
    return 0; // early return narrows `value` to string after this line
  }
  // value: string (narrowed!)
  return value.length;
}
```

---

## Truthiness Narrowing

JavaScript values can be truthy or falsy. TypeScript uses this to narrow types. The falsy values in JS are: `false`, `0`, `""`, `null`, `undefined`, `NaN`.

```typescript
function process(input: string | null | undefined | 0 | "") {
  // input: string | null | undefined | 0 | ""

  if (input) {
    // input is narrowed to string (0 and "" are falsy, null and undefined are falsy)
    console.log(input.length);
  } else {
    // input: null | undefined | 0 | ""
    // (string with length 0 is excluded)
  }
}
```

### Narrowing out null/undefined with early return

```typescript
interface User {
  name: string;
  email: string;
}

function greet(user: User | null) {
  if (!user) {
    console.log("No user found");
    return;
  }
  // user: User (narrowed from User | null)
  console.log(`Hello, ${user.name}`);
}
```

### Truthiness Narrowing Pitfalls

```typescript
function greet(name: string | undefined) {
  if (name) {
    console.log(`Hello, ${name}`);
  }
  // ⚠️ name is still `string | undefined` here
  // Because `name` could have been reassigned in another scope
}
```

### Boolean coercion is NOT narrowing

```typescript
function check(value: string | number) {
  // Boolean(value) does NOT narrow
  if (Boolean(value)) {
    // value: string | number — NOT narrowed!
  }
}
```

Use `!!` or direct truthiness checks instead.

---

## Equality Narrowing

TypeScript narrows types when you compare variables using equality operators (`===`, `!==`, `==`, `!=`).

```typescript
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // Both x and y must be `string` (only common type)
    console.log(x.toUpperCase()); // OK
    console.log(y.toUpperCase()); // OK
  }
}
```

### Strict equality with null/undefined

```typescript
function process(x: string | number | null) {
  if (x !== null) {
    // x: string | number
    if (typeof x === "string") {
      // x: string
    }
  }
}
```

### Using equality with specific values

```typescript
type Status = "loading" | "success" | "error";

function handleStatus(status: Status) {
  if (status === "loading") {
    // status: "loading"
    console.log("Loading...");
  } else if (status === "success") {
    // status: "success"
    console.log("Done!");
  } else {
    // status: "error"
    console.error("Failed");
  }
}
```

### Equality narrowing with switch

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
  }
}
```

---

## typeof Narrowing

The `typeof` operator checks the JavaScript runtime type and TypeScript uses it for narrowing.

```typescript
function format(value: string | number | boolean): string {
  switch (typeof value) {
    case "string":
      return value.toUpperCase();
    case "number":
      return value.toFixed(2);
    case "boolean":
      return value.toString();
  }
}
```

### typeof with type guards in if statements

```typescript
function padLeft(value: string | number, padding: string | number) {
  if (typeof padding === "number") {
    // padding: number
    return " ".repeat(padding) + value;
  }
  // padding: string
  return padding + value;
}
```

### typeof is a compile-time AND runtime check

```typescript
// TypeScript knows the runtime typeof and narrows accordingly
function example(x: unknown) {
  if (typeof x === "string") {
    // x: string — both at compile time and runtime
    console.log(x.toUpperCase());
  }
}
```

### typeof does NOT work on classes/instances

```typescript
class Dog {
  bark() {}
}
class Cat {
  meow() {}

  // typeof dogInstance === "object", typeof catInstance === "object"
  // So typeof cannot distinguish between classes!
}
```

Use `instanceof` for class instances.

---

## instanceof Narrowing

The `instanceof` operator checks if a value is an instance of a class. TypeScript uses this for narrowing.

```typescript
class HttpError {
  statusCode: number;
  message: string;
  constructor(statusCode: number, message: string) {
    this.statusCode = statusCode;
    this.message = message;
  }
}

class ValidationError {
  field: string;
  message: string;
  constructor(field: string, message: string) {
    this.field = field;
    this.message = message;
  }
}

function handleError(error: HttpError | ValidationError) {
  if (error instanceof HttpError) {
    // error: HttpError
    console.log(`HTTP ${error.statusCode}: ${error.message}`);
  } else {
    // error: ValidationError
    console.log(`Field "${error.field}": ${error.message}`);
  }
}
```

### instanceof with built-in types

```typescript
function processDate(input: Date | string) {
  if (input instanceof Date) {
    // input: Date
    console.log(input.getFullYear());
  } else {
    // input: string
    console.log(new Date(input));
  }
}
```

### instanceof does NOT work across different realms (iframes)

```typescript
// ⚠️ instanceof fails across frames/realms
// instanceof checks the prototype chain, which differs across iframes
```

---

## in Narrowing

The `in` operator checks if an object has a specific property. TypeScript uses it for narrowing union types.

```typescript
interface Bird {
  fly(): void;
  layEggs(): void;
}

interface Fish {
  swim(): void;
  layEggs(): void;
}

function move(animal: Bird | Fish) {
  if ("fly" in animal) {
    // animal: Bird
    animal.fly();
  } else {
    // animal: Fish
    animal.swim();
  }
}
```

### in narrowing with discriminated unions

```typescript
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

function calculateArea(shape: Circle | Square) {
  if ("radius" in shape) {
    // shape: Circle
    return Math.PI * shape.radius ** 2;
  }
  // shape: Square
  return shape.sideLength ** 2;
}
```

### in narrowing with optional properties

```typescript
interface A {
  a: number;
}

interface AB {
  a: number;
  b: number;
}

function process(obj: A | AB) {
  if ("b" in obj) {
    // obj: AB
    console.log(obj.b);
  }
  // obj: A | AB (since A doesn't have `b`, it could still be A here if checked differently)
}
```

---

## Assignment Narrowing

When you assign a value to a variable, TypeScript narrows the type if the assignment is more specific.

```typescript
let value: string | number | boolean = "hello";
// value: string | number | boolean

value = 42;
// value: string | number | boolean (type is still the declared type)

// But in a conditional branch:
function example(x: string | number) {
  let result: string | number = x;
  if (typeof x === "string") {
    result = x; // x is string, result is string
  }
  // result: string | number (type widens back)
}
```

### const assertions narrow types

```typescript
const direction = "up"; // type is "up", not string
let direction2 = "up"; // type is string

// Use `as const` for literal types
const config = {
  host: "localhost",
  port: 3000,
} as const;
// config: { readonly host: "localhost"; readonly port: 3000 }
```

### Narrowing in catch blocks

```typescript
try {
  throw new Error("something went wrong");
} catch (error) {
  // error: unknown (in TypeScript 4.4+ with useUnknownInCatchVariables)
  if (error instanceof Error) {
    console.log(error.message); // narrowed to Error
  }
}
```

---

## User-Defined Type Guards

When built-in narrowing isn't enough, you can write **type guard functions** that return a `boolean` with a type predicate.

### The `is` keyword

```typescript
interface Cat {
  meow(): void;
  purr(): void;
}

interface Dog {
  bark(): void;
  fetch(): void;
}

function isCat(animal: Cat | Dog): animal is Cat {
  return "meow" in animal;
}

function handleAnimal(animal: Cat | Dog) {
  if (isCat(animal)) {
    // animal: Cat
    animal.meow();
    animal.purr();
  } else {
    // animal: Dog
    animal.bark();
    animal.fetch();
  }
}
```

### Type guard for primitives

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isNumber(value: unknown): value is number {
  return typeof value === "number" && !isNaN(value);
}

function process(value: string | number) {
  if (isString(value)) {
    console.log(value.toUpperCase()); // string
  } else {
    console.log(value.toFixed(2)); // number
  }
}
```

### Type guard for arrays

```typescript
interface Success {
  type: "success";
  data: string[];
}

interface Error {
  type: "error";
  message: string;
}

function isSuccess(result: Success | Error): result is Success {
  return result.type === "success";
}

function handleResult(result: Success | Error) {
  if (isSuccess(result)) {
    // result: Success
    console.log(result.data.join(", "));
  } else {
    // result: Error
    console.error(result.message);
  }
}
```

### Type guard with in operator

```typescript
interface Admin {
  role: "admin";
  permissions: string[];
}

interface User {
  role: "user";
  name: string;
}

function isAdmin(person: Admin | User): person is Admin {
  return person.role === "admin";
}
```

---

## Assertion Functions

Assertion functions throw an error if the condition is false. They narrow the type by eliminating invalid types.

```typescript
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`Expected string, got ${typeof value}`);
  }
}

function assertIsDefined<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Expected value to be defined");
  }
}

function process(input: unknown) {
  assertIsString(input);
  // input: string (narrowed!)
  console.log(input.toUpperCase());
}

function getLength(value: string | null): number {
  assertIsDefined(value);
  // value: string (narrowed!)
  return value.length;
}
```

### Assertion function pattern for validation

```typescript
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

function assertIsArray<T>(value: unknown): asserts value is T[] {
  if (!Array.isArray(value)) {
    throw new Error("Expected array");
  }
}
```

---

## Exhaustive Narrowing with `never`

When you've handled all cases in a union type, the remaining type should be `never`. If it's not, you've missed a case.

```typescript
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
```

### Why `never` works

- `never` is the bottom type — it has no values
- If all union members are handled, the remaining type is `never`
- Assigning a non-`never` type to `never` causes a compile error
- This catches missing cases at compile time

### Adding a new union member breaks the switch

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number }; // NEW

// The switch now has a compile error because `rectangle` is not handled!
// TypeScript will say: Type '{ kind: "rectangle"; width: number; height: number }' is not assignable to type 'never'
```

### exhaustiveCheck helper

```typescript
function exhaustiveCheck(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
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
      exhaustiveCheck(shape); // Compile error if a case is missing
      throw new Error("unreachable");
  }
}
```

---

## Never-Throwing Patterns

The `never` type is useful for patterns where you want to enforce exhaustive handling.

### Pattern: Exhaustive discriminated union handler

```typescript
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" }
  | { type: "SET"; value: number };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT":
      return state + action.amount;
    case "DECREMENT":
      return state - action.amount;
    case "RESET":
      return 0;
    case "SET":
      return action.value;
    default:
      exhaustiveCheck(action);
      return state;
  }
}

function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled action: ${JSON.stringify(x)}`);
}
```

### Pattern: Unreachable code

```typescript
function throwError(message: string): never {
  throw new Error(message);
}

function loopForever(): never {
  while (true) {
    // never returns
  }
}
```

---

## Best Practices

1. **Use built-in narrowing first** — `typeof`, `instanceof`, `in`, and equality checks cover most cases
2. **Use type guards for complex conditions** — when the narrowing logic isn't expressible with built-in operators
3. **Use assertion functions for preconditions** — when a function should fail fast if the type is wrong
4. **Always use exhaustive checks with `never`** — prevents missed cases when adding new union members
5. **Avoid type assertions (`as`)** — they bypass narrowing and can hide bugs
6. **Use `unknown` over `any`** — forces you to narrow before using the value
7. **Name your type guards clearly** — use `is` prefix: `isString`, `isUser`, `isHttpError`

---

## Interview Questions

### Q1: What is type narrowing in TypeScript?

**Answer:** Type narrowing is the process of transforming a union type or `unknown`/`any` into a more specific type within a conditional branch. TypeScript uses control flow analysis to automatically narrow types based on runtime checks like `typeof`, `instanceof`, `in`, equality comparisons, and user-defined type guards.

### Q2: How does TypeScript narrow types in a switch statement?

**Answer:** TypeScript narrows using literal type checking in switch cases. When you switch on a string union type like `"a" | "b" | "c"`, each case narrows the type to the specific literal. For discriminated unions, TypeScript narrows the entire union to the matching variant based on the discriminant property.

### Q3: What is the difference between a type guard (`is`) and an assertion function (`asserts`)?

**Answer:** A type guard (`is`) returns a boolean and narrows the type in the calling scope — it tells TypeScript "if this returns true, the value is of this type." An assertion function (`asserts`) never returns (or throws) — it narrows the type by asserting the type is valid, and throws an error if it's not. Type guards work in `if` conditions; assertion functions work as standalone statements.

### Q4: Why does `never` work for exhaustive checking?

**Answer:** `never` is the bottom type — no value can be assigned to it. When all union members have been handled in a switch/if-else, the remaining type is `never`. If you assign a non-`never` type to `never`, TypeScript raises a compile error. This means if a new member is added to the union, the compiler catches the missing case automatically.

### Q5: Can `typeof` narrow class instances?

**Answer:** No. `typeof` returns `"object"` for all class instances (unless the class has a `typeof` method that returns a string literal, which is rare and not useful). Use `instanceof` instead, which checks the prototype chain and can distinguish between different classes.

### Q6: What is the difference between `any` and `unknown` with narrowing?

**Answer:** `any` disables type checking — you can do anything with it and TypeScript won't warn you. `unknown` forces you to narrow the type before using it. With `unknown`, you must use a type guard or assertion before accessing properties or calling methods. `unknown` is type-safe; `any` is not.
