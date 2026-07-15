# 09 - Control Flow

## Table of Contents

- [if/else](#ifelse)
- [switch/case](#switchcase)
- [Type Narrowing](#type-narrowing)
  - [Truthiness Narrowing](#truthiness-narrowing)
  - [Equality Narrowing](#equality-narrowing)
  - [instanceof Narrowing](#instanceof-narrowing)
  - [in Narrowing](#in-narrowing)
  - [Assignment Narrowing](#assignment-narrowing)
- [Control Flow Analysis](#control-flow-analysis)
- [Exhaustive Checking with never](#exhaustive-checking-with-never)
- [Type Predicates](#type-predicates)
- [Assert Functions](#assert-functions)
- [Summary](#summary)

---

## if/else

The `if/else` statement is the most basic control flow mechanism. In TypeScript, it also serves as a **type narrowing** tool.

### Basic Usage

```typescript
const age: number = 25;

if (age >= 18) {
  console.log("Adult");
} else if (age >= 13) {
  console.log("Teenager");
} else {
  console.log("Child");
}
```

### if/else as Type Guard

```typescript
function process(value: string | number): string {
  if (typeof value === "string") {
    // TypeScript KNOWS value is string here
    return value.toUpperCase();
  } else {
    // TypeScript KNOWS value is number here
    return value.toFixed(2);
  }
}
```

### Truthiness Checks

```typescript
function greet(name: string | null): string {
  if (name) {
    // name is narrowed to string (null is falsy)
    return `Hello, ${name}!`;
  }
  return "Hello, World!";
}

function processItems(items: string[] | null): string {
  if (items && items.length > 0) {
    // items is string[] and is not empty
    return items.join(", ");
  }
  return "No items";
}
```

### Nested Type Guards

```typescript
type Result =
  | { status: "success"; data: string }
  | { status: "error"; message: string }
  | { status: "loading" };

function handleResult(result: Result): string {
  if (result.status === "success") {
    // result narrowed to { status: "success"; data: string }
    return result.data;
  } else if (result.status === "error") {
    // result narrowed to { status: "error"; message: string }
    return result.message;
  } else {
    // result narrowed to { status: "loading" }
    return "Loading...";
  }
}
```

---

## switch/case

The `switch` statement provides multi-branch control flow. In TypeScript, it's especially powerful for narrowing discriminated unions.

### Basic Switch

```typescript
type Direction = "north" | "south" | "east" | "west";

function move(direction: Direction): string {
  switch (direction) {
    case "north":
      return "Moving north";
    case "south":
      return "Moving south";
    case "east":
      return "Moving east";
    case "west":
      return "Moving west";
    default:
      // TypeScript ensures all cases are handled
      const _exhaustive: never = direction;
      return _exhaustive;
  }
}
```

### Switch with Type Narrowing

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      // shape is narrowed to { kind: "circle"; radius: number }
      return Math.PI * shape.radius ** 2;

    case "rectangle":
      // shape is narrowed to { kind: "rectangle"; width: number; height: number }
      return shape.width * shape.height;

    case "triangle":
      // shape is narrowed to { kind: "triangle"; base: number; height: number }
      return (shape.base * shape.height) / 2;
  }
}
```

### Fallthrough Warning

```typescript
// switch/case falls through by default — be careful!
function handleStatus(status: number): string {
  switch (status) {
    case 200:
      console.log("OK");
      // Missing break! Falls through to next case
    case 201:
      console.log("Created");
      break;
    case 404:
      console.log("Not Found");
      break;
    default:
      console.log("Unknown");
  }
  return "done";
}

// handleStatus(200) logs both "OK" AND "Created"
// Always use break, return, or throw
```

### Switch vs if/else Chain

```typescript
// Use switch when comparing a single value against constants
if (status === 200) {
  // ...
} else if (status === 404) {
  // ...
} else if (status === 500) {
  // ...
}

// switch is cleaner for this pattern
switch (status) {
  case 200: /* ... */ break;
  case 404: /* ... */ break;
  case 500: /* ... */ break;
}

// Use if/else when conditions are complex
if (user.isAdmin && user.isActive) {
  // ...
} else if (user.isModerator || user.hasPermission("edit")) {
  // ...
}
```

---

## Type Narrowing

Type narrowing is TypeScript's ability to **refine types** based on control flow analysis. When you check a type, TypeScript automatically narrows the type in that branch.

### Truthiness Narrowing

Any value that is falsy (`null`, `undefined`, `0`, `""`, `false`, `NaN`) can be eliminated through truthiness checks:

```typescript
function process(value: string | null | undefined): string {
  if (value) {
    // value is narrowed to string
    return value.toUpperCase();
  }
  // value is narrowed to null | undefined
  return "No value";
}

// Array filtering
const items: (string | null)[] = ["hello", null, "world", null];
const filtered: string[] = items.filter((item): item is string => item !== null);
// filtered: ["hello", "world"]
```

### Equality Narrowing

Comparing with `===`, `!==`, `==`, or `!=` narrows types:

```typescript
function process(a: string | number, b: string | boolean): string {
  if (a === b) {
    // Both a and b are narrowed to string
    return a.toUpperCase(); // OK — both are string
  }
  // a is string | number, b is string | boolean
  return "different";
}

// null/undefined equality
function greet(name: string | null | undefined): string {
  if (name == null) {
    // name is narrowed to null | undefined
    return "Hello, stranger!";
  }
  // name is narrowed to string
  return `Hello, ${name}!`;
}
```

### typeof Narrowing

Using `typeof` to narrow primitive types:

```typescript
function format(value: string | number | boolean): string {
  switch (typeof value) {
    case "string":
      return value.toUpperCase();       // string
    case "number":
      return value.toFixed(2);          // number
    case "boolean":
      return value ? "Yes" : "No";      // boolean
  }
}

// typeof with guard clauses
function process(value: string | number): void {
  if (typeof value !== "string") {
    // value narrowed to number
    console.log(value.toFixed(2));
    return;
  }
  // value narrowed to string
  console.log(value.toUpperCase());
}
```

### instanceof Narrowing

Using `instanceof` to narrow class instances:

```typescript
class HttpError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
  }
}

class ValidationError extends Error {
  constructor(public fields: Record<string, string>) {
    super("Validation failed");
  }
}

function handleError(error: Error): string {
  if (error instanceof HttpError) {
    // error narrowed to HttpError
    return `HTTP ${error.statusCode}: ${error.message}`;
  }
  if (error instanceof ValidationError) {
    // error narrowed to ValidationError
    const fields = Object.entries(error.fields)
      .map(([k, v]) => `${k}: ${v}`)
      .join(", ");
    return `Validation: ${fields}`;
  }
  // error narrowed to Error
  return error.message;
}
```

### in Narrowing

Using `in` to check for property existence:

```typescript
interface Bird {
  fly(): void;
  layEggs(): void;
}

interface Fish {
  swim(): void;
  layEggs(): void;
}

function move(animal: Bird | Fish): void {
  if ("fly" in animal) {
    animal.fly();   // animal narrowed to Bird
  } else {
    animal.swim();  // animal narrowed to Fish
  }
}
```

### Assignment Narrowing

Variables can be narrowed through assignment:

```typescript
let value: string | number = "hello"; // value is string | number

if (typeof value === "string") {
  value = value.toUpperCase(); // OK — value is string
}

// After the if block, value is back to string | number
// because assignment may have changed it
```

---

## Control Flow Analysis

TypeScript performs **control flow analysis** to determine the type of a variable at any point in the code. This analysis considers:

1. Variable declarations and assignments
2. Conditional checks (type guards)
3. Return statements
4. Throw statements

### Basic Control Flow

```typescript
function process(value: string | number): string {
  // value: string | number

  if (typeof value === "string") {
    // value: string
    return value.toUpperCase();
  }

  // value: number (TypeScript knows the string case returned)
  return value.toFixed(2);
}
```

### Complex Control Flow

```typescript
function process(
  input: string | number | null,
  mode: "strict" | "loose"
): string {
  // input: string | number | null

  if (input === null) {
    // input: null
    return "No input";
  }

  // input: string | number

  if (mode === "strict") {
    if (typeof input === "string") {
      // input: string
      return input.toUpperCase();
    }
    // input: number
    return input.toFixed(2);
  }

  // mode: "loose"
  // input: string | number
  return String(input);
}
```

### Definite Assignment Analysis

```typescript
let name: string;

// TypeScript knows 'name' is definitely assigned here
if (condition) {
  name = "Alice";
} else {
  name = "Bob";
}

// 'name' is definitely assigned — safe to use
console.log(name.toUpperCase());
```

### Unreachable Code Detection

```typescript
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }

  return value.toFixed(2);

  // This code is unreachable — TypeScript warns about it
  // console.log("This never runs");
}

function throwError(): never {
  throw new Error("Always throws");
}

function processValue(value: string | number): string {
  if (typeof value === "string") {
    return value;
  }

  throwError(); // TypeScript knows this never returns

  // TypeScript knows this is unreachable
  return value.toFixed(2);
}
```

---

## Exhaustive Checking with never

The `never` type represents values that never occur. It's used to ensure all cases in a union type are handled.

### Basic Exhaustive Check

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
    default:
      // shape is narrowed to 'never'
      // If you add a new case to Shape but forget to handle it here,
      // TypeScript will error: Type '...' is not assignable to type 'never'
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```

### Why This Works

```typescript
// If we add a new case to Shape:
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number }; // NEW!

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default:
      // ERROR! Type '{ kind: "triangle"; base: number; height: number }'
      // is not assignable to type 'never'
      const _exhaustive: never = shape;
      // This forces you to handle the new case
      return 0;
  }
}
```

### Exhaustive Check with if/else

```typescript
type Status = "pending" | "active" | "deleted";

function handleStatus(status: Status): string {
  if (status === "pending") return "Waiting...";
  if (status === "active") return "Running";
  if (status === "deleted") return "Removed";

  // Exhaustive check
  const _exhaustive: never = status;
  return _exhaustive;
}
```

### Exhaustive Check with Object Lookup

```typescript
type EventName = "click" | "focus" | "blur";

const handlers: Record<EventName, () => void> = {
  click: () => console.log("clicked"),
  focus: () => console.log("focused"),
  blur: () => console.log("blurred"),
  // If you add a new EventName but forget to add a handler,
  // TypeScript will error here
};

function handleEvent(event: EventName): void {
  handlers[event]();
}
```

---

## Type Predicates

Type predicates are functions that return a boolean and narrow the type through the `is` keyword.

### Basic Type Predicate

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

function handle(animal: Cat | Dog): void {
  if (isCat(animal)) {
    animal.meow();   // TypeScript knows it's a Cat
    animal.purr();
  } else {
    animal.bark();   // TypeScript knows it's a Dog
    animal.fetch();
  }
}
```

### Type Predicate for Null Checks

```typescript
function isNotNull<T>(value: T | null): value is T {
  return value !== null;
}

const items: (string | null)[] = ["hello", null, "world", null];
const filtered: string[] = items.filter(isNotNull);
// filtered: ["hello", "world"]
```

### Type Predicate for Array Filtering

```typescript
interface User {
  name: string;
  email?: string;
}

function hasEmail(user: User): user is User & { email: string } {
  return user.email !== undefined;
}

const users: User[] = [
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob" },
  { name: "Charlie", email: "charlie@example.com" },
];

const usersWithEmail: (User & { email: string })[] = users.filter(hasEmail);
// usersWithEmail: Alice and Charlie (with guaranteed email string)
```

### Built-in Type Guards

TypeScript provides several built-in type guard functions:

```typescript
// Array.isArray
function process(value: string | string[]): string {
  if (Array.isArray(value)) {
    return value.join(", "); // value narrowed to string[]
  }
  return value; // value narrowed to string
}

// Number.isNaN, Number.isFinite, etc.
function processNumber(value: number): string {
  if (Number.isNaN(value)) {
    return "NaN";
  }
  return value.toFixed(2);
}
```

---

## Assert Functions

Assert functions are functions that throw an error if a condition is not met, narrowing the type to the asserted type.

### Basic Assert Function

```typescript
function assertDefined<T>(value: T | null | undefined, name: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(`${name} is required`);
  }
}

function processUser(user: User | null): string {
  assertDefined(user, "user");
  // user is narrowed to User (not null anymore)
  return user.name;
}
```

### Assert with Custom Conditions

```typescript
function assertPositive(value: number): asserts value is number {
  if (value <= 0) {
    throw new Error(`Expected positive number, got ${value}`);
  }
}

function assertString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`Expected string, got ${typeof value}`);
  }
}

// Usage
function process(value: unknown): string {
  assertString(value);
  // value is narrowed to string
  return value.toUpperCase();
}
```

### Non-null Assertion Operator (!)

The `!` operator asserts that a value is not null or undefined. Use it sparingly:

```typescript
const element = document.getElementById("myElement");
// element: HTMLElement | null

// Non-null assertion (risky — no runtime check)
element!.addEventListener("click", () => {
  console.log("clicked");
});

// Better approach: null check
if (element) {
  element.addEventListener("click", () => {
    console.log("clicked");
  });
}

// Or optional chaining
element?.addEventListener("click", () => {
  console.log("clicked");
});
```

---

## Summary

| Concept | Purpose | Example |
|---------|---------|---------|
| **if/else** | Branching logic | `if (typeof x === "string")` |
| **switch/case** | Multi-branch on single value | `switch (shape.kind)` |
| **Truthiness narrowing** | Eliminate falsy values | `if (value)` |
| **Equality narrowing** | Narrow by comparison | `if (a === b)` |
| **typeof narrowing** | Narrow primitives | `if (typeof x === "string")` |
| **instanceof narrowing** | Narrow class instances | `if (e instanceof Error)` |
| **in narrowing** | Check property existence | `if ("meow" in animal)` |
| **never** | Exhaustive checking | `const _: never = shape` |
| **Type predicates** | Custom type guards | `animal is Cat` |
| **Assert functions** | Runtime assertions | `asserts value is T` |

> **Key Takeaways:**
> - TypeScript's control flow analysis is one of its most powerful features
> - Use type guards (`typeof`, `instanceof`, `in`) to narrow types
> - Use `never` for exhaustive checking in switch statements
> - Type predicates and assert functions let you create custom type guards
> - Always handle all cases in discriminated unions
