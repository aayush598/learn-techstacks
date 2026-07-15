# 08 - Operators

## Table of Contents

- [Arithmetic Operators](#arithmetic-operators)
- [Comparison Operators](#comparison-operators)
- [Logical Operators](#logical-operators)
- [Bitwise Operators](#bitwise-operators)
- [Ternary Operator](#ternary-operator)
- [Nullish Coalescing (??)](#nullish-coalescing-)
- [Optional Chaining (?.)](#optional-chaining-)
- [typeof Operator](#typeof-operator)
- [instanceof Operator](#instanceof-operator)
- [keyof Operator](#keyof-operator)
- [in Operator](#in-operator)
- [Operator Limitations in TypeScript](#operator-limitations-in-typescript)
- [Summary](#summary)

---

## Arithmetic Operators

Arithmetic operators perform mathematical calculations. TypeScript ensures type safety with these operators.

### Basic Arithmetic

```typescript
const a: number = 10;
const b: number = 3;

a + b;   // 13  (addition)
a - b;   // 7   (subtraction)
a * b;   // 30  (multiplication)
a / b;   // 3.3333... (division)
a % b;   // 1   (modulo/remainder)
a ** b;  // 1000 (exponentiation)
```

### Unary Operators

```typescript
const x: number = 5;

// Unary plus — converts to number
const positive: number = +x;
const fromString: number = +"42"; // 42

// Unary negation
const negative: number = -x;    // -5

// Increment
let count: number = 0;
count++;   // count is now 1 (post-increment)
++count;   // count is now 2 (pre-increment)

// Decrement
count--;   // count is now 1 (post-decrement)
--count;   // count is now 0 (pre-decrement)
```

### Type Safety with Arithmetic

```typescript
// TypeScript prevents arithmetic on non-numeric types
const str: string = "hello";
// str - 1;  // Error: Operator '-' cannot be applied to types 'string' and 'number'

// But + is overloaded for string concatenation
"hello" + " world"; // "hello world" (string concatenation)
"5" + 3;            // "53" (string concatenation, not addition!)

// Number conversion
const numStr: string = "42";
const num: number = Number(numStr);  // 42
const parsed: number = parseInt(numStr); // 42
const float: number = parseFloat("3.14"); // 3.14
```

---

## Comparison Operators

Comparison operators compare values and return boolean results.

### Equality Operators

```typescript
const a: number = 5;
const b: number = 5;
const c: string = "5";

// Strict equality (===) — value AND type must match
a === b;   // true
a === c;   // false (different types)

// Strict inequality (!==)
a !== c;   // true

// Loose equality (==) — performs type coercion
a == b;    // true
a == c;    // true (string "5" coerced to number 5)
// WARNING: Avoid loose equality — it leads to subtle bugs
```

### Relational Operators

```typescript
const x: number = 10;
const y: number = 20;

x > y;    // false
x < y;    // true
x >= y;   // false
x <= y;   // true

// String comparison (lexicographic)
"apple" < "banana";  // true
"abc" === "abc";     // true
```

### Comparing Objects

```typescript
// Reference comparison
const obj1 = { name: "Alice" };
const obj2 = { name: "Alice" };
const obj3 = obj1;

obj1 === obj2;  // false (different references)
obj1 === obj3;  // true  (same reference)

// Array comparison
[1, 2, 3] === [1, 2, 3]; // false
const arr = [1, 2, 3];
arr === arr;               // true
```

---

## Logical Operators

Logical operators work with boolean values and support short-circuit evaluation.

### Basic Logical Operators

```typescript
const a: boolean = true;
const b: boolean = false;

a && b;   // false (AND)
a || b;   // true  (OR)
!a;       // false (NOT)
```

### Short-Circuit Evaluation

```typescript
// && returns the first falsy value, or the last value
const result1 = "hello" && 42;     // 42
const result2 = "" && 42;          // ""
const result3 = null && 42;        // null

// || returns the first truthy value, or the last value
const result4 = "hello" || 42;     // "hello"
const result5 = "" || 42;          // 42
const result6 = null || "default"; // "default"
```

### Logical AND for Default Values

```typescript
// Pattern: default values with &&
const name = userInput && userInput.name;

// Better: use nullish coalescing
const name = userInput?.name ?? "Unknown";
```

### Logical OR for Default Values

```typescript
// Pattern: default values with ||
const port = config.port || 3000;

// Subtle issue with falsy values:
const port = 0 || 3000;  // 3000 (0 is falsy!)

// Better: use nullish coalescing
const port = config.port ?? 3000; // 0 (only null/undefined trigger default)
```

### Logical Operators with Non-Boolean Types

```typescript
// TypeScript allows logical operators with non-boolean types
const x: number = 5;
const y: number = 0;

x && console.log("x is truthy"); // Logs: "x is truthy"
y && console.log("y is truthy"); // Does not log (0 is falsy)

// The result type depends on the operand types
const result = "hello" && 42; // type: number
const result2 = "" && 42;     // type: "" (string literal)
```

---

## Bitwise Operators

Bitwise operators work on individual bits of numbers.

### Basic Bitwise Operators

```typescript
const a: number = 5;  // binary: 0101
const b: number = 3;  // binary: 0011

a & b;   // 1  (AND: 0001)
a | b;   // 7  (OR:  0111)
a ^ b;   // 6  (XOR: 0110)
~a;       // -6 (NOT: bitwise complement)
a << 1;  // 10 (left shift: 1010)
a >> 1;  // 2  (right shift: 0010)
a >>> 1; // 2  (unsigned right shift)
```

### Practical Uses

```typescript
// Permission flags
const READ = 0b001;     // 1
const WRITE = 0b010;    // 2
const EXECUTE = 0b100;  // 4

// Combine permissions
let permissions = READ | WRITE; // 011 (3)
permissions |= EXECUTE;          // 111 (7)

// Check permissions
const canRead = (permissions & READ) !== 0;     // true
const canDelete = (permissions & 0b1000) !== 0; // false

// Bit shifting for powers of 2
const powerOf2 = 1 << 10; // 1024
```

---

## Ternary Operator

The ternary operator is a compact if-else expression.

### Basic Syntax

```typescript
// condition ? valueIfTrue : valueIfFalse
const age = 20;
const status = age >= 18 ? "adult" : "minor";
// status: "adult"
```

### Nested Ternaries

```typescript
// Nested ternaries (use sparingly for readability)
const grade = score >= 90 ? "A" :
              score >= 80 ? "B" :
              score >= 70 ? "C" :
              score >= 60 ? "D" : "F";
```

### Ternary with Type Narrowing

```typescript
// TypeScript narrows types in ternary branches
function format(value: string | number): string {
  return typeof value === "string"
    ? value.toUpperCase()     // value is string here
    : value.toFixed(2);       // value is number here
}
```

### Ternary in JSX/Template Literals

```typescript
// Common in React components
const element = <div>{isActive ? "Active" : "Inactive"}</div>;

// In template literals
const message = `Status: ${isActive ? "Active" : "Inactive"}`;
```

---

## Nullish Coalescing (??)

The nullish coalescing operator provides a default value only when the left operand is `null` or `undefined`.

### Basic Usage

```typescript
const value: string | null = null;
const result = value ?? "default";
// result: "default"

const value2: string | null = "hello";
const result2 = value2 ?? "default";
// result2: "hello"
```

### ?? vs ||

```typescript
// The key difference: ?? only checks null/undefined
// || checks all falsy values (including 0, "", false, NaN)

// Example 1: Zero
const port = 0 ?? 3000;  // 0 (?? does NOT trigger on 0)
const port2 = 0 || 3000; // 3000 (|| triggers on 0)

// Example 2: Empty string
const name = "" ?? "Unknown";  // "" (?? does NOT trigger on "")
const name2 = "" || "Unknown"; // "Unknown" (|| triggers on "")

// Example 3: false
const flag = false ?? true;  // false (?? does NOT trigger on false)
const flag2 = false || true; // true (|| triggers on false)
```

### Chaining ??

```typescript
// Chain multiple defaults
const config = {
  apiUrl: null,
  timeout: undefined,
  retries: 0,
};

const url = config.apiUrl ?? "https://default.api.com";
// "https://default.api.com"

const timeout = config.timeout ?? 5000;
// 5000

const retries = config.retries ?? 3;
// 0 (retries is 0, not null/undefined)
```

### ?? with Type Narrowing

```typescript
// TypeScript narrows the type after ??
function processName(name: string | null): string {
  const displayName = name ?? "Anonymous";
  // displayName is string (null has been eliminated)
  return displayName.toUpperCase();
}
```

---

## Optional Chaining (?.)

Optional chaining safely accesses nested properties without throwing an error if an intermediate value is null or undefined.

### Basic Usage

```typescript
interface User {
  name: string;
  address?: {
    street?: string;
    city: string;
  };
}

const user: User = { name: "Alice" };

// Without optional chaining
const street = user.address && user.address.street;
// undefined

// With optional chaining
const street = user.address?.street;
// undefined (no error!)

// Deeply nested
const zipCode = user.address?.street?.match(/\d+/)?.[0];
// undefined (no error!)
```

### Optional Method Calls

```typescript
interface UserService {
  getUser?(id: string): User;
}

const service: UserService = {};

// Without optional chaining
if (service.getUser) {
  const user = service.getUser("123");
}

// With optional chaining
const user = service.getUser?.("123");
// undefined (no error!)
```

### Optional Element Access

```typescript
const arr: number[] = [1, 2, 3];

const first = arr?.[0]; // 1
const tenth = arr?.[9]; // undefined (no error!)
```

### ?. vs &&

```typescript
// && returns the last truthy value or first falsy value
const result1 = user.address && user.address.street;
// Could return false, 0, "", etc. if street is falsy

// ?. returns undefined if any part is null/undefined
const result2 = user.address?.street;
// Returns undefined or the street string

// Key difference with falsy values
const obj = { value: 0 };
const r1 = obj?.value && "default"; // 0 (falsy but not null/undefined)
const r2 = obj?.value ?? "default"; // 0 (not null/undefined)
```

### Combining ?. with ??

```typescript
// Common pattern: optional chaining + nullish coalescing
const street = user.address?.street ?? "No street provided";
const city = user.address?.city ?? "Unknown city";
```

---

## typeof Operator

The `typeof` operator works both at runtime (JavaScript) and compile time (TypeScript).

### Runtime typeof

```typescript
typeof "hello";     // "string"
typeof 42;          // "number"
typeof true;        // "boolean"
typeof null;        // "object" (historical bug)
typeof undefined;   // "undefined"
typeof Symbol("id"); // "symbol"
typeof 42n;         // "bigint"
typeof {};          // "object"
typeof [];          // "object"
typeof function(){}; // "function"
```

### typeof as Type Guard

```typescript
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // value narrowed to string
  }
  return value.toFixed(2); // value narrowed to number
}

function handle(value: string | number | boolean): string {
  switch (typeof value) {
    case "string":
      return value.toUpperCase();
    case "number":
      return value.toFixed(2);
    case "boolean":
      return value ? "Yes" : "No";
  }
}
```

### typeof in Type Position

```typescript
// Extract the type of a variable
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};

type Config = typeof config;
// type Config = { apiUrl: string; timeout: number }

// Use the extracted type
const devConfig: Config = {
  apiUrl: "http://localhost:3000",
  timeout: 1000,
};

// typeof with function return types
function createUser() {
  return { name: "Alice", age: 30 };
}

type User = ReturnType<typeof createUser>;
// type User = { name: string; age: number }
```

---

## instanceof Operator

The `instanceof` operator checks if an object is an instance of a class or constructor.

### Basic Usage

```typescript
class Animal {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

class Dog extends Animal {
  breed: string;
  constructor(name: string, breed: string) {
    super(name);
    this.breed = breed;
  }
}

const dog = new Dog("Rex", "Labrador");

dog instanceof Animal; // true
dog instanceof Dog;    // true
```

### instanceof as Type Guard

```typescript
function processError(error: Error | string): string {
  if (error instanceof Error) {
    return error.message; // error narrowed to Error
  }
  return error; // error narrowed to string
}

class HttpError extends Error {
  statusCode: number;
  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
  }
}

function handleError(error: Error | HttpError): string {
  if (error instanceof HttpError) {
    return `HTTP ${error.statusCode}: ${error.message}`;
  }
  return error.message;
}
```

### instanceof with Built-in Types

```typescript
function formatDate(value: Date | string | number): string {
  if (value instanceof Date) {
    return value.toISOString();
  }
  if (typeof value === "string") {
    return value;
  }
  return new Date(value).toISOString();
}
```

### Limitations of instanceof

```typescript
// instanceof doesn't work across different realms (iframes, Node.js vm)
// It checks the prototype chain, so it fails for cross-frame objects

// instanceof doesn't work with primitive types
const str = "hello";
// str instanceof String; // false (primitives don't have prototype chain)

// Use typeof for primitives, instanceof for objects
```

---

## keyof Operator

The `keyof` operator creates a union type of an object type's keys.

### Basic Usage

```typescript
interface User {
  name: string;
  age: number;
  email: string;
}

type UserKeys = keyof User;
// type UserKeys = "name" | "age" | "email"

// Using keyof with type safety
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { name: "Alice", age: 30, email: "alice@example.com" };

getProperty(user, "name");  // string
getProperty(user, "age");   // number
// getProperty(user, "password"); // Error: "password" is not in keyof User
```

### keyof with Type Assertions

```typescript
// Safe property access
function getPropertyOrDefault<T, K extends keyof T>(
  obj: T,
  key: K,
  defaultValue: T[K]
): T[K] {
  return obj[key] ?? defaultValue;
}

const name = getPropertyOrDefault(user, "name", "Unknown"); // string
const age = getPropertyOrDefault(user, "age", 0);          // number
```

### keyof with Maps and Records

```typescript
// Mapping over object keys
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const userSnippet = pick(user, ["name", "email"]);
// type: { name: string; email: string }

// Using keyof with Record
type UserField = keyof User;
type UserValues = Record<UserField, unknown>;
```

---

## in Operator

The `in` operator checks if a property exists on an object. In TypeScript, it's also used as a type guard.

### Basic Usage

```typescript
const user = { name: "Alice", age: 30 };

"name" in user;  // true
"email" in user; // false
```

### in as Type Guard

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

### in with Discriminated Unions

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  if ("radius" in shape) {
    return Math.PI * shape.radius ** 2;
  }
  return shape.width * shape.height;
}
```

### in for Optional Property Checking

```typescript
interface User {
  name: string;
  age: number;
  email?: string;
}

function processUser(user: User): string {
  if ("email" in user && user.email) {
    return `Email: ${user.email}`;
  }
  return `Name: ${user.name}`;
}
```

---

## Operator Limitations in TypeScript

### No Operator Overloading

TypeScript does not support traditional operator overloading like C++ or C#. However, there are workarounds:

```typescript
// Cannot overload operators directly
class Vector {
  constructor(public x: number, public y: number) {}

  // Cannot do: operator +(other: Vector): Vector

  // Instead, use named methods
  add(other: Vector): Vector {
    return new Vector(this.x + other.x, this.y + other.y);
  }

  equals(other: Vector): boolean {
    return this.x === other.x && this.y === other.y;
  }
}
```

### Symbol.toPrimitive for Custom Coercion

```typescript
class Temperature {
  constructor(private celsius: number) {}

  [Symbol.toPrimitive](hint: string): number | string {
    if (hint === "number") {
      return this.celsius;
    }
    return `${this.celsius}°C`;
  }
}

const temp = new Temperature(25);
+temp;         // 25 (numeric coercion)
`${temp}`;     // "25°C" (string coercion)
temp + 5;      // 30 (numeric)
```

### Limited Type Operations

```typescript
// TypeScript cannot use arbitrary types with operators
const a: string = "hello";
const b: string = "world";

// a - b; // Error: Operator '-' cannot be applied to types 'string' and 'string'
// a * b; // Error: Operator '*' cannot be applied to types 'string' and 'string'
```

---

## Summary

| Operator | Category | Example | Result |
|----------|----------|---------|--------|
| `+` | Arithmetic | `5 + 3` | `8` |
| `-` | Arithmetic | `5 - 3` | `2` |
| `*` | Arithmetic | `5 * 3` | `15` |
| `/` | Arithmetic | `6 / 3` | `2` |
| `%` | Arithmetic | `5 % 3` | `2` |
| `**` | Arithmetic | `2 ** 3` | `8` |
| `===` | Comparison | `5 === 5` | `true` |
| `!==` | Comparison | `5 !== "5"` | `true` |
| `&&` | Logical | `true && false` | `false` |
| `||` | Logical | `true \|\| false` | `true` |
| `??` | Nullish | `null ?? "default"` | `"default"` |
| `?.` | Optional | `null?.prop` | `undefined` |
| `typeof` | Type | `typeof "hello"` | `"string"` |
| `instanceof` | Type | `dog instanceof Dog` | `true` |
| `keyof` | Type | `keyof User` | Union of keys |
| `in` | Type | `"name" in obj` | `boolean` |
| `?:` | Ternary | `x ? "yes" : "no"` | Conditional |

> **Key Takeaways:**
> - Always use `===` instead of `==` for comparisons
> - Use `??` instead of `||` when you only want to default on `null`/`undefined`
> - Use `?.` to safely access nested properties
> - `typeof` is both a runtime check and a compile-time type operator
> - `keyof` and `in` are powerful for type-safe object manipulation
