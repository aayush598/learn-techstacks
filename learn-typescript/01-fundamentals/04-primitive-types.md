# 04 - Primitive Types

## Table of Contents

- [Overview](#overview)
- [string](#string)
- [number](#number)
- [boolean](#boolean)
- [null](#null)
- [undefined](#undefined)
- [symbol](#symbol)
- [bigint](#bigint)
- [void](#void)
- [typeof Checks](#typeof-checks)
- [Type Compatibility Between Primitives](#type-compatibility-between-primitives)
- [Edge Cases](#edge-cases)
- [Summary](#summary)

---

## Overview

JavaScript (and therefore TypeScript) has the following **primitive types**:

| Type | Example | Description |
|------|---------|-------------|
| `string` | `"hello"` | Textual data |
| `number` | `42`, `3.14`, `Infinity`, `NaN` | Numeric data (all numbers are floating-point) |
| `boolean` | `true`, `false` | Logical values |
| `null` | `null` | Intentional absence of value |
| `undefined` | `undefined` | Uninitialized value |
| `symbol` | `Symbol("id")` | Unique identifier |
| `bigint` | `9007199254740991n` | Arbitrary-precision integers |
| `void` | — | Absence of a return value (TypeScript-specific) |

> **Note:** `void` is not a true primitive in JavaScript — it's a TypeScript concept used to indicate that a function does not return a value.

---

## string

The `string` type represents textual data — a sequence of characters.

### Basic Usage

```typescript
// String literals
const name: string = "Alice";
const greeting: string = 'Hello, World!';
const template: string = `My name is ${name}`;

// All three are valid string syntax
```

### Template Literals

Template literals (backtick strings) allow embedded expressions:

```typescript
const firstName: string = "Alice";
const lastName: string = "Smith";
const age: number = 30;

const bio: string = `${firstName} ${lastName} is ${age} years old`;
// "Alice Smith is 30 years old"

// Multi-line strings
const multiLine: string = `
  This is line 1
  This is line 2
  This is line 3
`;
```

### String Methods

TypeScript provides full type information for all string methods:

```typescript
const str: string = "Hello, TypeScript!";

str.length;              // number — 18
str.toUpperCase();       // string — "HELLO, TYPESCRIPT!"
str.toLowerCase();       // string — "hello, typescript!"
str.charAt(0);           // string — "H"
str.indexOf("Type");     // number — 7
str.slice(0, 5);         // string — "Hello"
str.replace("TypeScript", "World"); // string — "Hello, World!"
str.includes("Script");  // boolean — true
str.startsWith("Hello"); // boolean — true
str.split(", ");         // string[] — ["Hello", "TypeScript!"]
str.trim();              // string — "Hello, TypeScript!"
str.repeat(2);           // string — "Hello, TypeScript!Hello, TypeScript!"
```

### Unicode and Escapes

```typescript
const unicode: string = "\u0048\u0065\u006C\u006C\u006F"; // "Hello"
const emoji: string = "👋 Hello 🌍"; // Valid string with emoji
const escape: string = "Line 1\nLine 2\tTabbed";
```

### String Union Types

```typescript
type Direction = "north" | "south" | "east" | "west";

const heading: Direction = "north";  // Valid
const wrong: Direction = "up";       // Error: not a valid Direction
```

---

## number

The `number` type represents **all numeric values** — integers and floating-point numbers. JavaScript uses IEEE 754 double-precision floating-point, so there is no distinction between `int` and `float`.

### Basic Usage

```typescript
// Integers
const count: number = 42;
const negative: number = -100;
const zero: number = 0;

// Floating-point
const pi: number = 3.14159;
const temperature: number = -40.0;

// Different number systems
const hex: number = 0xff;       // 255
const binary: number = 0b1010;  // 10
const octal: number = 0o777;    // 511
```

### Special Values

```typescript
const infinity: number = Infinity;
const negInfinity: number = -Infinity;
const notANumber: number = NaN;

// These are all valid numbers in TypeScript
console.log(typeof Infinity);  // "number"
console.log(typeof NaN);       // "number"
```

### Number Methods

```typescript
const num: number = 42.567;

num.toFixed(2);          // string — "42.57" (rounded)
num.parseInt("42");      // number — 42
Number.parseInt("42");   // number — 42
Number.isFinite(42);     // boolean — true
Number.isNaN(NaN);       // boolean — true
Number.isInteger(42);    // boolean — true
Number.isInteger(42.5);  // boolean — false

Math.floor(42.9);       // number — 42
Math.ceil(42.1);        // number — 43
Math.round(42.5);       // number — 43
Math.abs(-42);          // number — 42
Math.max(1, 2, 3);      // number — 3
Math.min(1, 2, 3);      // number — 1
Math.random();           // number — 0 to 1
```

### BigInt Literals

BigInt literals are a separate type but related to numbers:

```typescript
const big: bigint = 9007199254740991n; // bigint type
const regular: number = 9007199254740991; // number type (loses precision)
```

### Infinity and NaN

```typescript
const result: number = 10 / 0;   // Infinity
const notNumber: number = "abc" as unknown as number; // NaN

// TypeScript treats these as valid numbers
// Always validate user input when expecting numbers
```

---

## boolean

The `boolean` type has exactly two values: `true` and `false`.

### Basic Usage

```typescript
const isActive: boolean = true;
const isDeleted: boolean = false;

// Comparison operators return booleans
const isEqual: boolean = 5 === 5;       // true
const isGreater: boolean = 10 > 5;      // true
const isString: boolean = typeof "hi" === "string"; // true
```

### Boolean Methods

```typescript
const str: string = "hello";
const num: number = 42;

// These are not really "boolean methods" but expressions
const isTruthy: boolean = Boolean(str);      // true
const isFalsy: boolean = Boolean(0);         // false

// Boolean objects (avoid these)
const boolObj: Boolean = new Boolean(true);  // Don't use this
```

### Falsy Values

These values are all treated as `false` in boolean contexts:

```typescript
Boolean(false);      // false
Boolean(0);          // false
Boolean(-0);         // false
Boolean(0n);         // false (BigInt zero)
Boolean("");         // false (empty string)
Boolean(null);       // false
Boolean(undefined);  // false
Boolean(NaN);        // false
```

### Truthy Values

Everything else is truthy:

```typescript
Boolean(true);           // true
Boolean(1);              // true
Boolean(-1);             // true
Boolean(42);             // true
Boolean("hello");        // true
Boolean("false");        // true (string "false" is truthy!)
Boolean([]);             // true (empty array is truthy!)
Boolean({});             // true (empty object is truthy!)
Boolean(() => {});       // true (functions are truthy)
Boolean(Symbol("id"));   // true
```

### Boolean in Conditionals

```typescript
const name: string = "";

// Truthiness check
if (name) {
  console.log("Name exists");    // Won't execute — "" is falsy
}

// Explicit check (preferred for clarity)
if (name.length > 0) {
  console.log("Name exists");
}
```

---

## null

`null` represents an **intentional absence** of any object value.

### Basic Usage

```typescript
// Explicitly set to null
const user: User | null = null;
const data: string | null = null;
const count: number | null = null;

// Null check required before accessing properties
if (user !== null) {
  console.log(user.name);
}
```

### Null vs Undefined

| Aspect | `null` | `undefined` |
|--------|--------|------------|
| Meaning | Intentionally empty | Not yet assigned |
| typeof | `"object"` (historical bug) | `"undefined"` |
| JSON.stringify | Removed from JSON | Removed from JSON |
| Comparison | `null === null` is `true` | `undefined === undefined` is `true` |
| Equality | `null == undefined` is `true` | `null == undefined` is `true` |
| Equality | `null === undefined` is `false` | `null === undefined` is `false` |

### Null in TypeScript

```typescript
// Without strict null checks (old behavior)
const maybeNull: string = null; // Allowed — dangerous

// With strict null checks (strict: true)
const maybeNull: string = null; // Error: Type 'null' is not assignable to type 'string'

// Must use union type to allow null
const maybeNull: string | null = null; // OK
```

### Null Checking Patterns

```typescript
function processName(name: string | null): string {
  // Pattern 1: Explicit check
  if (name !== null) {
    return name.toUpperCase();
  }

  // Pattern 2: Nullish coalescing
  return (name ?? "Unknown").toUpperCase();

  // Pattern 3: Optional chaining
  return name?.toUpperCase() ?? "UNKNOWN";
}
```

---

## undefined

`undefined` represents a variable that has been **declared but not assigned** a value.

### Basic Usage

```typescript
// Declared but not assigned
let x: undefined;
console.log(x); // undefined

// Object property that doesn't exist
const obj: { name: string; age?: number } = { name: "Alice" };
console.log(obj.age); // undefined

// Function return without explicit return
function doNothing(): undefined {
  // No return statement
  // Returns undefined implicitly
}

// Array element access beyond bounds
const arr: number[] = [1, 2, 3];
console.log(arr[10]); // undefined
```

### Undefined in TypeScript

```typescript
// Without strict null checks
const x: string = undefined; // Allowed

// With strict null checks
const x: string = undefined; // Error: Type 'undefined' is not assignable to type 'string'

// Must use union type
const x: string | undefined = undefined; // OK
```

### Undefined Checking Patterns

```typescript
function greet(name: string | undefined): string {
  // Pattern 1: Explicit check
  if (name !== undefined) {
    return `Hello, ${name}!`;
  }

  // Pattern 2: Optional parameter with default
  return "Hello, World!";
}

// Pattern 3: Default parameter
function greet(name: string = "World"): string {
  return `Hello, ${name}!`;
}

// Pattern 4: Nullish coalescing
function greet(name?: string): string {
  return `Hello, ${name ?? "World"}!`;
}
```

---

## symbol

`symbol` is a **unique and immutable** primitive value that can be used as an identifier for object properties.

### Basic Usage

```typescript
// Creating symbols
const sym1: symbol = Symbol("description");
const sym2: symbol = Symbol("description");

// Each symbol is unique, even with the same description
console.log(sym1 === sym2); // false

// Symbols are unique identifiers
const id1: symbol = Symbol("id");
const id2: symbol = Symbol("id");
console.log(id1 === id2); // false
```

### Well-Known Symbols

TypeScript recognizes JavaScript's built-in well-known symbols:

```typescript
// Symbol.iterator — makes an object iterable
class NumberRange {
  constructor(private start: number, private end: number) {}

  [Symbol.iterator](): Iterator<number> {
    let current = this.start;
    const end = this.end;
    return {
      next(): IteratorResult<number> {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { done: true, value: undefined };
      },
    };
  }
}

const range = new NumberRange(1, 5);
for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}
```

### Symbols as Object Keys

```typescript
const secretKey: symbol = Symbol("secret");

const obj: { [secretKey]: string; name: string } = {
  [secretKey]: "hidden value",
  name: "Alice",
};

// Accessing symbol properties
console.log(obj[secretKey]); // "hidden value"

// Symbol properties are not included in...
Object.keys(obj);              // ["name"] — not included
JSON.stringify(obj);           // {"name":"Alice"} — not included
for (const key in obj) {}     // Only iterates "name"
```

### Symbol.for() — Global Symbol Registry

```typescript
// Shared symbols across different parts of an application
const sym1: symbol = Symbol.for("shared");
const sym2: symbol = Symbol.for("shared");
console.log(sym1 === sym2); // true — same symbol from registry

// Get key from symbol
const key: string | undefined = Symbol.keyFor(sym1); // "shared"
```

### Use Cases

```typescript
// 1. Private-like properties (convention-based)
const _privateField = Symbol("privateField");

class MyClass {
  [_privateField]: string = "hidden";

  get publicInfo(): string {
    return this[_privateField];
  }
}

// 2. Unique constants
const EVENT_CLICK = Symbol("CLICK");
const EVENT_SUBMIT = Symbol("SUBMIT");

function handleEvent(event: symbol): void {
  if (event === EVENT_CLICK) {
    console.log("Clicked!");
  } else if (event === EVENT_SUBMIT) {
    console.log("Submitted!");
  }
}
```

---

## bigint

`bigint` represents **arbitrary-precision integers** — integers larger than `Number.MAX_SAFE_INTEGER` (2^53 - 1).

### Basic Usage

```typescript
// BigInt literals (append 'n')
const big: bigint = 9007199254740991n;
const small: bigint = 42n;
const negative: bigint = -100n;

// Using BigInt() constructor
const fromNumber: bigint = BigInt(42);
const fromString: bigint = BigInt("9007199254740991");

// Comparison with regular numbers
const regularMax: number = Number.MAX_SAFE_INTEGER; // 9007199254740991
const bigMax: bigint = 9007199254740991n;

// Beyond safe integer range
const beyondSafe: bigint = 9007199254740992n; // 9007199254740992 (exact)
const beyondSafeNum: number = 9007199254740992; // 9007199254740992 (may lose precision)
```

### BigInt Operations

```typescript
const a: bigint = 100n;
const b: bigint = 300n;

a + b;   // 400n
a - b;   // -200n
a * b;   // 30000n
b / a;   // 3n (integer division)
b % a;   // 0n (remainder)
-a;      // -100n (negation)

// Comparison
a < b;   // true
a > b;   // false
a === b; // false

// Bitwise operations
a & b;   // 0n
a | b;   // 400n
a ^ b;   // 400n
~a;      // -101n
a << 2n; // 400n
a >> 2n; // 25n
```

### BigInt Limitations

```typescript
// Cannot mix BigInt and Number
const big: bigint = 100n;
const num: number = 42;

// big + num; // Error: Cannot mix BigInt and other types
// Use explicit conversion:
big + BigInt(num);   // 142n
Number(big) + num;   // 142 (may lose precision for large values)

// Cannot use with Math
// Math.max(100n, 200n); // Error

// JSON.stringify doesn't support BigInt by default
// JSON.stringify({ value: 100n }); // Error: Do not know how to serialize a BigInt
// Use a replacer:
JSON.stringify({ value: 100n }, (_, v) =>
  typeof v === "bigint" ? v.toString() : v
); // '{"value":"100"}'
```

---

## void

`void` represents the **absence of a return value**. It's a TypeScript-specific type, not a true JavaScript primitive.

### Basic Usage

```typescript
// Function that returns nothing
function logMessage(message: string): void {
  console.log(message);
  // No return statement (or return; or return undefined;)
}

// Arrow function with void
const log = (msg: string): void => {
  console.log(msg);
};

// void callback
function doSomething(callback: () => void): void {
  callback();
}
```

### Void vs undefined

```typescript
// void means the return value should not be used
// undefined means the return value is exactly undefined

function returnsVoid(): void {
  console.log("no return");
}

function returnsUndefined(): undefined {
  return undefined;
}

// The void operator
const result: void = void 0; // Evaluates expression, returns undefined

// void can be used to ignore a promise
function fireAndForget(): void {
  fetch("/api/data"); // Promise<void> — we don't care about the result
}
```

### Void in Type Positions

```typescript
// As a return type — function should not return a value
function process(callback: () => void): void {
  callback();
}

// void callback can still return a value (it's just ignored)
function process2(callback: () => void): void {
  const result = callback(); // Return value is ignored
}

// In Promise types
async function fetchData(): Promise<void> {
  await fetch("/api/data");
  // No return value
}
```

### void Callbacks

```typescript
// Common pattern: void callbacks
const numbers: number[] = [1, 2, 3, 4, 5];

// forEach returns void
numbers.forEach((num): void => {
  console.log(num);
});

// map returns a value (not void)
const doubled: number[] = numbers.map((num): number => num * 2);
```

---

## typeof Checks

TypeScript provides a `typeof` type operator for getting the type of a variable at compile time.

### typeof in JavaScript (Runtime)

```typescript
// Runtime type checking
const x = 42;
typeof x; // "number"

const s = "hello";
typeof s; // "string"

const b = true;
typeof b; // "boolean"

const n = null;
typeof n; // "object" (historical bug in JS)

const u = undefined;
typeof u; // "undefined"

const sy = Symbol("id");
typeof sy; // "symbol"

const bi = 42n;
typeof bi; // "bigint"

const fn = () => {};
typeof fn; // "function"

const obj = { name: "Alice" };
typeof obj; // "object"

const arr = [1, 2, 3];
typeof arr; // "object" (arrays are objects!)
```

### typeof in TypeScript (Compile Time)

```typescript
// typeof in type position — extracts the type of a variable
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
};

type Config = typeof config;
// type Config = {
//   apiUrl: string;
//   timeout: number;
//   retries: number;
// }

// Using the extracted type
const devConfig: Config = {
  apiUrl: "http://localhost:3000",
  timeout: 1000,
  retries: 1,
};
```

### typeof for Type Guarding

```typescript
function process(value: string | number): string {
  if (typeof value === "string") {
    // TypeScript narrows 'value' to 'string'
    return value.toUpperCase();
  } else {
    // TypeScript narrows 'value' to 'number'
    return value.toFixed(2);
  }
}
```

---

## Type Compatibility Between Primitives

### Direct Assignment

```typescript
// Same types — compatible
let a: string = "hello";
let b: string = a; // OK

let x: number = 42;
let y: number = x; // OK

// Different types — incompatible
let s: string = "hello";
let n: number = s; // Error: Type 'string' is not assignable to type 'number'
```

### Type Assertions

```typescript
// Explicit type assertions (use carefully)
const num: number = 42 as unknown as number; // Valid
const str: string = "hello" as string; // Valid

// Dangerous assertion (will cause runtime error)
// const bad: number = "hello" as unknown as number;
```

### Union Types

```typescript
// Union types allow multiple primitive types
let flexible: string | number = 42;  // OK
flexible = "hello";                   // OK

// Type narrowing with typeof
function handle(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // value is string here
  }
  return value.toFixed(2);     // value is number here
}
```

### Special Equality Rules

```typescript
// null and undefined are special
null === undefined; // false (strict equality)
null == undefined;  // true (loose equality)

// In TypeScript with strictNullChecks:
let x: string | null | undefined = null;
x = undefined; // OK — both are allowed in the union

// Type guards
function check(value: string | null | undefined): string {
  if (value == null) {
    // Handles both null and undefined
    return "no value";
  }
  return value.toUpperCase(); // value is string here
}
```

---

## Edge Cases

### Number Precision

```typescript
const a: number = 0.1 + 0.2;
console.log(a === 0.3); // false — floating point precision issue
console.log(a);          // 0.30000000000000004

// Use Math.round or epsilon comparison
console.log(Math.abs(a - 0.3) < Number.EPSILON); // true
```

### String to Number Conversion

```typescript
// These are NOT type-safe (TypeScript doesn't catch them):
const num: number = Number("42");      // 42
const bad: number = Number("hello");   // NaN

const parsed: number = parseInt("42px");  // 42 (ignores trailing non-numeric)
const parsed2: number = parseInt("abc");  // NaN

// Always validate
function toNumber(value: string): number | null {
  const result = Number(value);
  return Number.isNaN(result) ? null : result;
}
```

### Symbol as Object Key

```typescript
// Symbol keys don't show up in iteration
const sym: symbol = Symbol("hidden");
const obj: Record<string, unknown> = { [sym]: "secret", visible: true };

Object.keys(obj);          // ["visible"]
Object.getOwnPropertySymbols(obj); // [Symbol(hidden)]
Reflect.ownKeys(obj);      // ["visible", Symbol(hidden)]
```

### Void Function Assignment

```typescript
// void function can be assigned to () => undefined
const fn1: () => void = () => {};
const fn2: () => undefined = () => undefined;

// But void function CANNOT be assigned to () => undefined
const fn3: () => void = fn2; // OK
// const fn4: () => undefined = fn1; // Error if strict
```

---

## Summary

| Type | typeof Result | Example | Null? | Undefined? |
|------|--------------|---------|-------|-----------|
| `string` | `"string"` | `"hello"` | No | No |
| `number` | `"number"` | `42` | No | No |
| `boolean` | `"boolean"` | `true` | No | No |
| `null` | `"object"` | `null` | Yes | No |
| `undefined` | `"undefined"` | `undefined` | No | Yes |
| `symbol` | `"symbol"` | `Symbol()` | No | No |
| `bigint` | `"bigint"` | `42n` | No | No |
| `void` | N/A | N/A | N/A | N/A |

> **Key Takeaways:**
> - All numbers in TypeScript are floating-point (there's no separate `int` type)
> - `null` and `undefined` require explicit union types with `"strict": true`
> - `symbol` provides unique identifiers for object properties
> - `bigint` handles integers beyond the safe range
> - `void` is TypeScript-specific for functions that don't return values
> - Always validate user input — TypeScript types don't exist at runtime
