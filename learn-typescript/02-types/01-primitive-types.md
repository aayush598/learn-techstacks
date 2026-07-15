# Primitive Types in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [String](#string)
3. [Number](#number)
4. [Boolean](#boolean)
5. [Null and Undefined](#null-and-undefined)
6. [Symbol](#symbol)
7. [BigInt](#bigint)
8. [Void](#void)
9. [Template Literal Types with Primitives](#template-literal-types-with-primitives)
10. [Type Narrowing with Primitives](#type-narrowing-with-primitives)
11. [Primitive Comparison](#primitive-comparison)
12. [Boxing Behavior](#boxing-behavior-string-vs-string)
13. [Literal Primitive Types](#literal-primitive-types)
14. [Best Practices](#best-practices)
15. [Interview Questions](#interview-questions)

---

## Overview

TypeScript has **7 primitive types** that map directly to JavaScript primitives:

| Type      | JavaScript Equivalent | Description                        |
|-----------|-----------------------|------------------------------------|
| `string`  | `String`              | Textual data                       |
| `number`  | `Number`              | Numeric data (integers and floats) |
| `boolean` | `Boolean`             | `true` or `false`                  |
| `null`    | `null`                | Intentional absence of value       |
| `undefined` | `undefined`         | Uninitialized value                |
| `symbol`  | `Symbol`              | Unique identifier                  |
| `bigint`  | `BigInt`              | Arbitrary-precision integers       |

Primitives are **immutable** — operations on them return new values rather than modifying the original.

---

## String

The `string` type represents textual data enclosed in single quotes, double quotes, or backticks.

```typescript
// All three are valid string literals
const single: string = 'hello';
const double: string = "hello";
const backtick: string = `hello`;

// String methods return new strings (primitives are immutable)
const upper: string = single.toUpperCase(); // "HELLO"
const sliced: string = single.slice(1, 3);  // "el"

// Template literals (backtick strings) allow expressions
const name: string = "Alice";
const greeting: string = `Hello, ${name}!`; // "Hello, Alice!"

// Unicode and escape sequences
const heart: string = "\u2764";       // ❤
const newline: string = "line1\nline2";

// Multiline strings with backticks
const multiline: string = `
  This is
  a multiline
  string
`;
```

**Key point:** TypeScript `string` maps to JavaScript's `String` primitive, NOT the `String` object wrapper.

```typescript
function greet(name: string): string {
  return `Hello, ${name}!`;
}

greet("World");      // OK
greet(42);           // Error: Type 'number' is not assignable to type 'string'
greet(true);         // Error
greet(null);         // Error (with strictNullChecks)
```

---

## Number

The `number` type represents **all** numeric values: integers, floats, infinity, and NaN.

```typescript
// Integers
const age: number = 30;
const negative: number = -100;

// Floating-point
const pi: number = 3.14159;
const price: number = 9.99;

// Hexadecimal
const hex: number = 0xff; // 255

// Binary
const binary: number = 0b1010; // 10

// Octal
const octal: number = 0o744; // 484

// Special numeric values
const infinity: number = Infinity;
const notANumber: number = NaN;

// BigInt vs Number
const big: number = 9007199254740991; // MAX_SAFE_INTEGER
const tooBig: number = 9007199254740993; // Loses precision!

// Use BigInt for truly large integers
const huge: bigint = 9007199254740993n; // Exact
```

**Important:** There is no separate `integer` or `float` type in TypeScript — all numbers are `number`.

```typescript
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

divide(10, 3);   // 3.3333...
divide(10, 0);   // Throws Error
divide("10", 3); // Error: Argument of type 'string' is not assignable
```

---

## Boolean

The `boolean` type has two values: `true` and `false`.

```typescript
const isActive: boolean = true;
const isDeleted: boolean = false;

// Boolean expressions
const x: number = 10;
const isPositive: boolean = x > 0;    // true
const isZero: boolean = x === 0;      // false
const isTruthy: boolean = !!x;        // true

// Functions returning booleans
function isEven(n: number): boolean {
  return n % 2 === 0;
}

function isEmpty(value: string | null): boolean {
  return value === null || value.length === 0;
}

// Boolean objects (avoid these)
const boolObj: Boolean = new Boolean(1); // Wrapper object — avoid!
const boolPrim: boolean = Boolean(1);    // Primitive — OK
```

**Best Practice:** Always annotate with lowercase `boolean`, not uppercase `Boolean`:

```typescript
// ✅ Correct — primitive boolean
const flag: boolean = true;

// ❌ Wrong — wrapper object Boolean
const flagObj: Boolean = true;
// The wrapper object has different behavior in comparisons:
// new Boolean(false) == true  — because it's an object!
// new Boolean(false) === true — false, but for wrong reason
```

---

## Null and Undefined

These two types represent the absence of a value, but with different semantics:

```typescript
// undefined: variable declared but not assigned, missing function argument, etc.
let notAssigned: undefined;
notAssigned = undefined; // OK
notAssigned = null;      // Error

// null: intentional absence of value
let emptyValue: null;
emptyValue = null;      // OK
emptyValue = undefined; // Error

// With strictNullChecks (recommended in tsconfig.json)
// null and undefined are separate types and cannot be assigned to other types
const name: string = null;      // Error without strictNullChecks
const count: number = undefined; // Error without strictNullChecks

// Use union types to allow null/undefined
const maybeName: string | null = null;      // OK
const maybeCount: number | undefined = undefined; // OK

// Function that might return null
function findUser(id: number): User | null {
  const user = database.get(id);
  return user ?? null;
}

// Function with optional parameter (undefined)
function greet(name?: string): string {
  return `Hello, ${name ?? "stranger"}!`;
}
```

**`strictNullChecks` is one of the most important TypeScript compiler flags:**

```json
// tsconfig.json
{
  "compilerOptions": {
    "strictNullChecks": true
  }
}
```

With `strictNullChecks: true`:
- `null` and `undefined` are their own types
- You must explicitly handle nullability
- Prevents the "billion-dollar mistake" at compile time

Without `strictNullChecks`:
- `null` and `undefined` are assignable to any type
- Leads to runtime errors
- Essentially disables a huge portion of TypeScript's value

---

## Symbol

Symbols are unique, immutable primitive values. Each call to `Symbol()` creates a new, unique symbol.

```typescript
// Creating symbols
const sym1: symbol = Symbol("description");
const sym2: symbol = Symbol("description");
console.log(sym1 === sym2); // false — every Symbol is unique

// Symbol as object keys
const ID: symbol = Symbol("id");
const NAME: symbol = Symbol("name");

interface Entity {
  [ID]: number;
  [NAME]: string;
  // Can also use regular properties
  age: number;
}

const entity: Entity = {
  [ID]: 123,
  [NAME]: "Alice",
  age: 30,
};

// Well-known symbols
const iterator: symbol = Symbol.iterator;
const species: symbol = Symbol.species;

// Symbols as unique object property keys (prevents property name collisions)
const PRIVATE_KEY: unique symbol = Symbol("private");
class MyClass {
  private [PRIVATE_KEY]: string = "secret";

  public getSecret(): string {
    return this[PRIVATE_KEY];
  }
}

// Global symbol registry
const globalSym1: symbol = Symbol.for("shared-symbol");
const globalSym2: symbol = Symbol.for("shared-symbol");
console.log(globalSym1 === globalSym2); // true — same symbol from registry
```

**`unique symbol` type:**

```typescript
// The unique symbol type represents a specific symbol instance
const mySymbol: unique symbol = Symbol("my");
const sameSymbol: typeof mySymbol = mySymbol; // OK — same type
const otherSymbol: typeof mySymbol = Symbol("other"); // Error — different type

// unique symbol can only be const or read-only
declare const readonlySymbol: unique symbol;
```

---

## BigInt

BigInt represents arbitrary-precision integers, useful when `Number` is too small.

```typescript
// Creating BigInt values
const big1: bigint = 9007199254740993n;
const big2: bigint = BigInt(9007199254740993);

// BigInt arithmetic
const sum: bigint = 100n + 200n;    // 300n
const product: bigint = 100n * 2n;  // 200n
const power: bigint = 2n ** 53n;    // Huge number

// Comparison
console.log(1n < 2n);  // true
console.log(1n === 1n); // true (strict equality)
console.log(1n == 1);   // false — BigInt and Number are not equal!

// ⚠️ Cannot mix BigInt and Number
const mixed = 1n + 2; // Error: Cannot mix BigInt and other types

// Must explicitly convert
const result: bigint = 1n + BigInt(2);   // 3n
const num: number = Number(1n) + 2;      // 3

// Division truncates (no decimal)
console.log(7n / 2n); // 3n (not 3.5)
console.log(7n % 2n); // 1n (remainder)

// TypeScript type guard for BigInt
function processValue(value: number | bigint): string {
  if (typeof value === "bigint") {
    return `BigInt: ${value.toString()}n`;
  }
  return `Number: ${value.toFixed(2)}`;
}
```

---

## Void

The `void` type represents the absence of a return value. It is used for functions that don't return anything.

```typescript
// void as a return type
function logMessage(message: string): void {
  console.log(message);
  // No return statement (or return; with no value)
}

function sideEffect(): void {
  document.title = "Updated";
  // No return value
}

// void in a type position (rare)
type VoidCallback = () => void;

const callback: VoidCallback = () => {
  return 42; // OK — return value is ignored
};

// This is why () => void is useful: it accepts functions with ANY return type
const array = [1, 2, 3];
const doubled: number[] = array.map((n) => n * 2); // map expects () => void | something
// Actually, map expects (value: number) => U, so void would be U
// But in callback positions, () => void means "we don't care about the return value"
```

**Important distinction:** `void` vs `undefined` as return types:

```typescript
// void: function doesn't return a meaningful value
function doSomething(): void {
  console.log("done");
}

// undefined: function explicitly returns undefined
function doSomethingElse(): undefined {
  console.log("done");
  return undefined; // Must explicitly return
}

// With --noImplicitReturns, the above is required to have a return statement
```

---

## Template Literal Types with Primitives

Template literal types let you create new string types by combining existing types.

```typescript
// Basic template literal types
type Greeting = `Hello, ${string}`;
const g1: Greeting = "Hello, World"; // OK
const g2: Greeting = "Hi, World";    // Error

// Combining with other primitive types
type Color = "red" | "blue" | "green";
type ColorPrefix = `color-${Color}`;
// Result: "color-red" | "color-blue" | "color-green"

const c1: ColorPrefix = "color-red";   // OK
const c2: ColorPrefix = "color-yellow"; // Error

// Numeric literal types in template literals
type EventName = `event-${number}`;
const e1: EventName = "event-42";   // OK
const e2: EventName = "event-abc";  // Error

// Complex template literal types
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIEndpoint = `/${string}`;
type Route = `${HTTPMethod} ${APIEndpoint}`;

const route: Route = "GET /api/users";    // OK
const route2: Route = "PATCH /api/users"; // Error

// Template literals with boolean
type DebugMode = `debug-${boolean}`;
const d1: DebugMode = "debug-true";  // OK
const d2: DebugMode = "debug-false"; // OK
const d3: DebugMode = "debug-yes";   // Error

// Intrinsic string manipulation types
type Upper = Uppercase<"hello">;     // "HELLO"
type Lower = Lowercase<"HELLO">;     // "hello"
type Capitalized = Capitalize<"hello">; // "Hello"
type Uncap = Uncapitalize<"Hello">;  // "hello"

// Combining intrinsic types with unions
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;
const width: CSSValue = "100px";
const fontSize: CSSValue = "1.5em";
```

---

## Type Narrowing with Primitives

TypeScript can automatically narrow primitive types in control flow.

```typescript
// typeof narrowing
function processValue(value: string | number | boolean): string {
  if (typeof value === "string") {
    // Here, value is narrowed to string
    return value.toUpperCase();
  }
  if (typeof value === "number") {
    // Here, value is narrowed to number
    return value.toFixed(2);
  }
  // Here, value is narrowed to boolean
  return value ? "truthy" : "falsy";
}

// Equality narrowing
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // x and y are both narrowed to string
    console.log(x.toUpperCase(), y.toUpperCase());
  }
}

// Truthiness narrowing
function printLength(value: string | null | undefined): number {
  if (value) {
    // value is narrowed to string (null and undefined are falsy)
    return value.length;
  }
  return 0;
}

// Switch narrowing
function getColorCode(color: "red" | "green" | "blue"): number {
  switch (color) {
    case "red":
      return 0xff0000;
    case "green":
      return 0x00ff00;
    case "blue":
      return 0x0000ff;
    default:
      // Exhaustiveness check — compile error if a case is missing
      const _exhaustive: never = color;
      return _exhaustive;
  }
}

// `in` operator narrowing
interface Fish { swim: () => void; }
interface Bird { fly: () => void; }

function move(animal: Fish | Bird): void {
  if ("swim" in animal) {
    animal.swim(); // narrowed to Fish
  } else {
    animal.fly(); // narrowed to Bird
  }
}

// Literal type narrowing with const
const status = "active" as const; // type: "active"
function setStatus(s: "active" | "inactive"): void { /* ... */ }
setStatus(status); // OK — "active" is assignable to "active" | "inactive"
```

---

## Primitive Comparison

Understanding how primitives compare is important for avoiding subtle bugs.

```typescript
// String comparison (lexicographic)
console.log("abc" === "abc"); // true
console.log("abc" == "ABC");  // false (case-sensitive)
console.log("abc" < "abd");   // true (alphabetical)
console.log("9" > "10");      // true! ("9" > "1" lexicographically)

// Number comparison
console.log(1 === 1.0);        // true (no distinction)
console.log(0.1 + 0.2 === 0.3); // false! (floating-point precision)
console.log(Math.abs(0.1 + 0.2 - 0.3) < 1e-10); // true (safe comparison)

// Special number comparisons
console.log(NaN === NaN);       // false (NaN is not equal to anything)
console.log(Object.is(NaN, NaN)); // true (use Object.is for NaN comparison)
console.log(+0 === -0);         // true
console.log(Object.is(+0, -0)); // false

// BigInt comparison
console.log(1n === 1);   // false (different types)
console.log(1n == 1);    // false
console.log(1n < 2n);    // true
console.log(BigInt(1) === 1n); // true

// Symbol comparison
console.log(Symbol("a") === Symbol("a")); // false (unique)
console.log(Symbol.for("a") === Symbol.for("a")); // true (same registry)

// Boolean comparison
console.log(true === 1);  // false (strict equality)
console.log(true == 1);   // true (loose equality)
console.log(false === 0); // false
console.log(false == 0);  // true

// null and undefined
console.log(null === undefined); // false
console.log(null == undefined);  // true (loose equality treats them the same)
console.log(null == false);      // false
console.log(null == 0);          // false
console.log(undefined == false); // false
```

**Critical floating-point issue:**

```typescript
// ❌ Don't compare floats with ===
0.1 + 0.2 === 0.3; // false

// ✅ Use a tolerance
function floatsEqual(a: number, b: number, epsilon = 1e-10): boolean {
  return Math.abs(a - b) < epsilon;
}

floatsEqual(0.1 + 0.2, 0.3); // true
```

---

## Boxing Behavior (String vs string)

TypeScript distinguishes between primitive types and their wrapper object types.

```typescript
// Primitive types (lowercase) — use these
const primString: string = "hello";
const primNumber: number = 42;
const primBoolean: boolean = true;

// Wrapper object types (uppercase) — avoid these
const objString: String = new String("hello");
const objNumber: Number = new Number(42);
const objBoolean: Boolean = new Boolean(true);

// The difference matters in comparisons
console.log(primString == objString);  // true  (auto-boxing)
console.log(primString === objString); // false (different types!)
console.log(typeof primString);        // "string"
console.log(typeof objString);         // "object"

// ⚠️ The Boolean wrapper trap
const falseObj: Boolean = new Boolean(false);
if (falseObj) {
  console.log("This runs! Object is truthy, even if wrapped value is false");
}

// TypeScript catches this:
if (primBoolean) { /* OK */ }
if (objBoolean) { /* OK but misleading */ }

// String methods auto-box primitives (temporary wrapper, then unwrap)
const len: number = "hello".length; // Auto-boxed to access .length, then unwrapped
const upper: string = "hello".toUpperCase();

// You cannot assign wrapper objects where primitives are expected
function needsString(s: string): void { /* ... */ }
needsString(primString);       // OK
needsString(objString);        // Error: String is not assignable to string
needsString(new String("hi")); // Error
```

**Rule:** Always use lowercase `string`, `number`, `boolean`. Never use `String`, `Number`, `Boolean`.

---

## Literal Primitive Types

TypeScript can narrow primitives down to specific values using literal types.

```typescript
// String literal types
type Direction = "up" | "down" | "left" | "right";
const dir: Direction = "up";   // OK
const dir2: Direction = "west"; // Error

// Number literal types
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
const roll: DiceRoll = 3;   // OK
const roll2: DiceRoll = 7;  // Error

// Boolean literal types (rarely used alone, but useful in unions)
type Success = { success: true; data: string };
type Failure = { success: false; error: string };
type Result = Success | Failure;

function handleResult(result: Result): void {
  if (result.success) {
    console.log(result.data);  // narrowed to Success
  } else {
    console.log(result.error); // narrowed to Failure
  }
}

// `const` assertions create literal types automatically
const directions = ["up", "down", "left", "right"] as const;
type DirArray = typeof directions; // readonly ["up", "down", "left", "right"]
type Dir = (typeof directions)[number]; // "up" | "down" | "left" | "right"

// Satisfies with literal types
const config = {
  env: "production",
  port: 3000,
} satisfies Record<string, string | number>;
// env is inferred as "production" (literal type), not string

// Literal types in function overloads
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div = createElement("div");   // HTMLDivElement
const span = createElement("span"); // HTMLSpanElement
const p = createElement("p");       // HTMLElement
```

**Why literal types matter:**

```typescript
// Without literal types — any string is allowed
type ConfigBad = {
  mode: string;
};
const configBad: ConfigBad = { mode: "anything goes" }; // No safety

// With literal types — only valid values
type ConfigGood = {
  mode: "development" | "staging" | "production";
};
const configGood: ConfigGood = { mode: "production" }; // Safe
// const configBad2: ConfigGood = { mode: "test" };    // Error!
```

---

## Best Practices

1. **Always use `strictNullChecks: true`** in tsconfig.json
2. **Use lowercase primitives** (`string`, `number`, `boolean`) — never uppercase wrappers
3. **Use `typeof` checks** for runtime type narrowing
4. **Use `Object.is()`** when comparing `NaN` or `+0/-0`
5. **Prefer literal types** over general primitives for API boundaries
6. **Use `as const`** for arrays and objects where you want literal types
7. **Avoid floating-point equality** — use tolerance-based comparison
8. **Handle `null`/`undefined` explicitly** with union types, not assertions
9. **Use `unique symbol`** for globally unique identifiers
10. **Use `BigInt`** when you need integer precision beyond `Number.MAX_SAFE_INTEGER`

---

## Interview Questions

### Q1: What is the difference between `string` and `String` in TypeScript?

**Answer:** `string` (lowercase) is the primitive type, while `String` (uppercase) is the wrapper object type. Always use `string`. The wrapper type can lead to unexpected behavior in comparisons (`"hello" === new String("hello")` is `false`) and memory overhead.

### Q2: Can you assign `null` to a `string` type?

**Answer:** Only if `strictNullChecks` is disabled. With `strictNullChecks: true` (recommended), you must use `string | null` to allow null values. This is one of the most important compiler flags for type safety.

### Q3: What is the difference between `null` and `undefined`?

**Answer:** `undefined` represents an uninitialized or missing value (default for variables, function return values, missing object properties). `null` represents an intentional absence of value. They are not equal with `===` but are equal with `==`.

### Q4: Why does `0.1 + 0.2 !== 0.3`?

**Answer:** This is a floating-point precision issue in JavaScript (IEEE 754). Use `Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON` for safe comparison. TypeScript inherits this behavior from JavaScript.

### Q5: What is a literal type in TypeScript?

**Answer:** A literal type is a type that represents exactly one specific value. For example, `"hello"` is a literal string type, `42` is a literal number type. Literal types are useful for constraining values to specific allowed strings, numbers, or booleans.
