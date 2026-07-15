# Rest Parameters in TypeScript

## Table of Contents

1. [Rest Parameter Syntax](#rest-parameter-syntax)
2. [Typed Rest Parameters](#typed-rest-parameters)
3. [Rest vs Arguments Object](#rest-vs-arguments-object)
4. [Rest with Other Parameters](#rest-with-other-parameters)
5. [Converting Arguments to Array](#converting-arguments-to-array)
6. [Rest with Generics](#rest-with-generics)
7. [Tuple Rest Parameters](#tuple-rest-parameters)
8. [Spread Syntax vs Rest Parameters](#spread-syntax-vs-rest-parameters)
9. [Advanced Patterns](#advanced-patterns)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Rest Parameter Syntax

Rest parameters allow a function to accept an indefinite number of arguments as an array.

```typescript
// Basic rest parameter
function sum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}

console.log(sum(1, 2, 3));       // 6
console.log(sum(1, 2, 3, 4, 5)); // 15
console.log(sum());               // 0

// Rest parameter with strings
function concatenate(...strings: string[]): string {
  return strings.join(" ");
}

console.log(concatenate("Hello", "World"));           // "Hello World"
console.log(concatenate("TypeScript", "is", "great")); // "TypeScript is great"
```

### Basic Examples

```typescript
// Logging with rest parameters
function log(level: string, ...messages: unknown[]): void {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level.toUpperCase()}]`, ...messages);
}

log("info", "Server started", "on port 3000");
log("error", "Connection failed", { retries: 3 }, new Error("Timeout"));

// Finding maximum
function max(...numbers: number[]): number {
  return Math.max(...numbers);
}

console.log(max(1, 5, 3, 9, 2)); // 9

// Creating arrays
function range(start: number, end: number, ...additional: number[]): number[] {
  const result: number[] = [];
  for (let i = start; i <= end; i++) {
    result.push(i);
  }
  return [...result, ...additional];
}

console.log(range(1, 5));         // [1, 2, 3, 4, 5]
console.log(range(1, 3, 10, 20)); // [1, 2, 3, 10, 20]
```

---

## Typed Rest Parameters

Rest parameters can have any type annotation.

```typescript
// Rest with primitive types
function logNumbers(...nums: number[]): void { /* ... */ }
function logStrings(...strs: string[]): void { /* ... */ }
function logBools(...bools: boolean[]): void { /* ... */ }

// Rest with object types
interface User {
  id: number;
  name: string;
  email: string;
}

function createUsers(...userData: Omit<User, "id">[]): User[] {
  return userData.map((data, index) => ({
    id: index + 1,
    ...data,
  }));
}

const users = createUsers(
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob", email: "bob@example.com" }
);

// Rest with union types
function log(...values: (string | number | boolean)[]): void {
  values.forEach((value) => {
    console.log(typeof value, value);
  });
}

log("hello", 42, true); // string hello, number 42, boolean true
```

### Rest with Complex Types

```typescript
// Rest with arrays
function mergeArrays<T>(...arrays: T[][]): T[] {
  return arrays.reduce((merged, arr) => [...merged, ...arr], []);
}

const merged = mergeArrays([1, 2], [3, 4], [5, 6]);
console.log(merged); // [1, 2, 3, 4, 5, 6]

// Rest with promise types
async function fetchAll<T>(...urls: string[]): Promise<T[]> {
  const responses = await Promise.all(urls.map((url) => fetch(url)));
  return Promise.all(responses.map((r) => r.json()));
}

// Rest with function types
function compose<T>(...fns: Array<(arg: T) => T>): (arg: T) => T {
  return (arg: T) => fns.reduce((result, fn) => fn(result), arg);
}

const process = compose(
  (x: number) => x * 2,
  (x: number) => x + 1,
  (x: number) => x * x
);

console.log(process(3)); // ((3 * 2) + 1)^2 = 49
```

---

## Rest vs Arguments Object

The `arguments` object is the older way to access function arguments. Rest parameters are preferred.

```typescript
// OLD: Using arguments object (not recommended)
function oldSum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}

// PROBLEMS with arguments:
// 1. It's not an array (no .map, .filter, etc.)
// 2. It doesn't work with arrow functions
// 3. It includes all arguments, not just the ones you want
// 4. TypeScript has limited type inference for it

// NEW: Using rest parameters (recommended)
function newSum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}

// Arrow functions with rest (arguments object doesn't work in arrow functions)
const arrowSum = (...numbers: number[]): number => {
  return numbers.reduce((total, n) => total + n, 0);
};

// Comparison table:
// Feature              | arguments object | rest parameters
// -------------------- | ---------------- | ----------------
// Works in arrow funcs | No               | Yes
// Is an array          | No               | Yes
// TypeScript support   | Limited          | Full
// Can be typed         | No               | Yes
// Named parameters     | No               | Yes
```

### Converting Arguments to Array (When Needed)

```typescript
// If you must use arguments (legacy code), convert to array
function legacyFunction() {
  // Method 1: Array.from
  const argsArray = Array.from(arguments);

  // Method 2: Slice
  const argsSlice = [].slice.call(arguments);

  // Method 3: Spread (ES6+)
  const argsSpread = [...arguments];

  // All produce real arrays with full array methods
  return argsArray.filter((arg) => typeof arg === "string");
}

// Modern equivalent with rest
function modernFunction(...args: (string | number)[]): string[] {
  return args.filter((arg): arg is string => typeof arg === "string");
}
```

---

## Rest with Other Parameters

Rest parameters can be combined with regular and optional parameters.

```typescript
// Rest must be the last parameter
function logWithPrefix(
  prefix: string,
  ...messages: unknown[]
): void {
  console.log(`[${prefix}]`, ...messages);
}

logWithPrefix("INFO", "Server started");
logWithPrefix("ERROR", "Connection failed", { code: 500 });

// Multiple parameters before rest
function createUser(
  name: string,
  email: string,
  ...roles: string[]
): User {
  return {
    id: Date.now(),
    name,
    email,
    roles: roles.length > 0 ? roles : ["user"],
  };
}

createUser("Alice", "alice@example.com");                    // roles: ["user"]
createUser("Bob", "bob@example.com", "admin", "editor");    // roles: ["admin", "editor"]

// Optional parameter before rest
function formatMessage(
  level: string,
  timestamp?: boolean,
  ...parts: string[]
): string {
  const prefix = timestamp ? `[${new Date().toISOString()}]` : "";
  return `${prefix}[${level.toUpperCase()}] ${parts.join(" ")}`;
}

formatMessage("info", true, "Hello", "World");
// "[2024-01-15T...] [INFO] Hello World"

formatMessage("error", undefined, "Something", "went", "wrong");
// "[ERROR] Something went wrong"
```

### Rest After Optional

```typescript
// This is NOT valid - rest after optional is not allowed
// function broken(optional?: string, ...rest: string[]): void {}

// Workaround 1: Use an options object
function valid(
  options?: { optional?: string },
  ...rest: string[]
): void { /* ... */ }

// Workaround 2: Make the optional required with a default
function alsoValid(
  optional: string = "",
  ...rest: string[]
): void { /* ... */ }
```

---

## Converting Arguments to Array

```typescript
// When you receive arguments as rest, you already have an array
function processItems(...items: string[]): void {
  // items is already an array - use array methods directly
  const uppercased = items.map((item) => item.toUpperCase());
  const filtered = items.filter((item) => item.length > 3);
  const sorted = [...items].sort();
  console.log({ uppercased, filtered, sorted });
}

// Rest with destructuring
function sum(...[first, second, ...rest]: number[]): number {
  console.log(`First: ${first}, Second: ${second}, Rest: [${rest}]`);
  return first + second + rest.reduce((a, b) => a + b, 0);
}

sum(1, 2, 3, 4, 5);
// First: 1, Second: 2, Rest: [3, 4, 5]
// Returns 15

// Advanced destructuring with rest
function process(first: string, second: string, ...remaining: string[]): void {
  console.log(`Required: ${first}, ${second}`);
  console.log(`Optional rest: ${remaining.join(", ")}`);
}

process("a", "b", "c", "d", "e");
// Required: a, b
// Optional rest: c, d, e
```

---

## Rest with Generics

Rest parameters work beautifully with generics.

```typescript
// Generic rest parameters
function first<T>(...items: T[]): T | undefined {
  return items[0];
}

console.log(first(1, 2, 3));       // 1
console.log(first("a", "b", "c")); // "a"
console.log(first<string>());       // undefined

// Generic tuple with rest
function zip<T, U>(...pairs: [T, U][]): [T[], U[]] {
  const firsts: T[] = [];
  const seconds: U[] = [];
  for (const [a, b] of pairs) {
    firsts.push(a);
    seconds.push(b);
  }
  return [firsts, seconds];
}

const [names, ages] = zip(
  ["Alice", "Bob", "Charlie"],
  [25, 30, 35]
);

// Generic variadic functions
function curry<A extends unknown[], R>(
  fn: (...args: A) => R
): (...args: A) => R {
  return fn;
}

// Generic function composition
function pipe<A, B>(f1: (a: A) => B): (a: A) => B;
function pipe<A, B, C>(f1: (a: A) => B, f2: (b: B) => C): (a: A) => C;
function pipe<A, B, C, D>(
  f1: (a: A) => B,
  f2: (b: B) => C,
  f3: (c: C) => D
): (a: A) => D;
function pipe(...fns: Array<(arg: any) => any>) {
  return (arg: any) => fns.reduce((result, fn) => fn(result), arg);
}

const processString = pipe(
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/\s+/g, "_")
);

console.log(processString("  Hello World  ")); // "hello_world"
```

---

## Tuple Rest Parameters

Rest parameters can be typed as tuples for fixed-length, heterogeneous arrays.

```typescript
// Tuple rest parameter
function logWithLevel(
  ...args: [level: string, message: string, ...optional: unknown[]]
): void {
  const [level, message, ...optional] = args;
  console.log(`[${level}] ${message}`, ...optional);
}

logWithLevel("info", "User logged in");
logWithLevel("error", "Failed to save", { retries: 3 });
logWithLevel("debug", "State", { count: 42 }, "extra data");

// Named tuple elements
function move(
  ...args: [x: number, y: number, z?: number]
): void {
  const [x, y, z = 0] = args;
  console.log(`Moving to (${x}, ${y}, ${z})`);
}

move(10, 20);      // Moving to (10, 20, 0)
move(10, 20, 30);  // Moving to (10, 20, 30)

// Heterogeneous tuple rest
function dispatch<T extends unknown[]>(
  action: string,
  ...payload: T
): void {
  console.log(`Dispatching: ${action}`, ...payload);
}

dispatch("USER_LOGIN", { id: 1, name: "Alice" });
dispatch("PAGE_VIEW", "/home", { referrer: "google.com" });

// Tuple rest with constraints
function createRoute<T extends [string, ...string[]]>(
  ...segments: T
): string {
  return segments.join("/");
}

createRoute("api", "users", "123");       // "api/users/123"
createRoute("home");                       // "home"
```

---

## Spread Syntax vs Rest Parameters

Understanding the difference between spread (`...`) and rest (`...`).

```typescript
// REST: Gathers multiple arguments into an array
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3); // ... in function signature = REST

// SPREAD: Expands an array into individual arguments
const nums = [1, 2, 3];
sum(...nums); // ... in function call = SPREAD

// They work together
function logAll(...messages: (string | number)[]): void {
  console.log(messages.join(" "));
}

const parts = ["Hello", "World"];
logAll(...parts, 42, ...[true, false]);
// "Hello World 42 true false"

// Spread with objects (not rest, but related)
function mergeOptions(
  defaults: Options,
  ...overrides: Partial<Options>[]
): Options {
  return Object.assign({}, defaults, ...overrides);
}

// Rest gathers, spread distributes
// Rest: f(...args)       => args is [1, 2, 3]
// Spread: f(...[1, 2, 3]) => f(1, 2, 3)
```

### Practical Examples

```typescript
// Combining rest and spread
function bindAll<T extends object>(
  obj: T,
  ...methodNames: Array<keyof T>
): T {
  const result = { ...obj };
  for (const name of methodNames) {
    if (typeof result[name] === "function") {
      (result[name] as Function) = (result[name] as Function).bind(obj);
    }
  }
  return result;
}

class Calculator {
  value = 0;

  add(n: number): Calculator {
    this.value += n;
    return this;
  }

  subtract(n: number): Calculator {
    this.value -= n;
    return this;
  }

  multiply(n: number): Calculator {
    this.value *= n;
    return this;
  }
}

const calc = new Calculator();
const boundCalc = bindAll(calc, "add", "subtract", "multiply");

// Rest in generics
function curry<Args extends unknown[], R>(
  fn: (...args: Args) => R
): Curried<Args, R> {
  // Implementation...
}

// Spread in function calls
function greetAll(...names: string[]): void {
  names.forEach((name) => console.log(`Hello, ${name}!`));
}

const friends = ["Alice", "Bob", "Charlie"];
greetAll(...friends); // Calls greetAll("Alice", "Bob", "Charlie")
```

---

## Advanced Patterns

```typescript
// Function decorator with rest
function log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const original = descriptor.value;
  descriptor.value = function (...args: unknown[]) {
    console.log(`Calling ${propertyKey} with`, args);
    const result = original.apply(this, args);
    console.log(`${propertyKey} returned`, result);
    return result;
  };
}

class MathService {
  @log
  add(a: number, b: number): number {
    return a + b;
  }
}

// Variadic function builder
function createValidator<T>(
  ...validators: Array<(value: T) => boolean>
): (value: T) => string[] {
  return (value: T) => {
    return validators
      .map((validator, index) => (validator(value) ? null : `Validator ${index} failed`))
      .filter((msg): msg is string => msg !== null);
  };
}

const isPositive = (n: number) => n > 0;
const isEven = (n: number) => n % 2 === 0;
const isLessThan100 = (n: number) => n < 100;

const validateNumber = createValidator(isPositive, isEven, isLessThan100);
console.log(validateNumber(50));   // []
console.log(validateNumber(-1));   // ["Validator 0 failed"]
console.log(validateNumber(150));  // ["Validator 2 failed"]

// Event emitter with typed events
type EventMap = {
  login: [userId: string, timestamp: Date];
  logout: [userId: string];
  purchase: [userId: string, amount: number, items: string[]];
};

class TypedEventEmitter<Events extends Record<string, unknown[]>> {
  private listeners = new Map<string, Function[]>();

  on<K extends keyof Events>(
    event: K,
    listener: (...args: Events[K]) => void
  ): void {
    const existing = this.listeners.get(event as string) ?? [];
    existing.push(listener);
    this.listeners.set(event as string, existing);
  }

  emit<K extends keyof Events>(event: K, ...args: Events[K]): void {
    const listeners = this.listeners.get(event as string) ?? [];
    listeners.forEach((listener) => listener(...args));
  }
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on("login", (userId, timestamp) => {
  console.log(`${userId} logged in at ${timestamp}`);
});
emitter.emit("login", "user123", new Date());
```

---

## Best Practices

```typescript
// 1. Use rest parameters instead of arguments object
// BAD
function oldLog() {
  console.log.apply(console, arguments);
}

// GOOD
function newLog(...args: unknown[]): void {
  console.log(...args);
}

// 2. Type rest parameters explicitly
// BAD
function process(...args) { /* ... */ }

// GOOD
function process(...args: string[]): void { /* ... */ }

// 3. Use tuple rest for fixed-length, heterogeneous arrays
function move3D(...coords: [number, number, number]): void {
  const [x, y, z] = coords;
  console.log(`Moving to (${x}, ${y}, ${z})`);
}

// 4. Use rest sparingly - don't use it to avoid defining parameters
// BAD
function getUser(...args: unknown[]) {
  const id = args[0];
  const name = args[1];
}

// GOOD
function getUser(id: number, name: string): User { /* ... */ }

// 5. Combine rest with spread for flexible APIs
function createElement(
  tag: string,
  props: Record<string, unknown>,
  ...children: (string | HTMLElement)[]
): HTMLElement {
  const el = document.createElement(tag);
  Object.entries(props).forEach(([key, value]) => {
    el.setAttribute(key, String(value));
  });
  el.append(...children);
  return el;
}
```

---

## Interview Questions

### Q1: What is the difference between rest parameters and the `arguments` object?

**Answer:** Rest parameters are real arrays with full type support, work in arrow functions, and only capture remaining parameters. The `arguments` object is array-like, lacks type safety, doesn't work in arrow functions, and captures all parameters regardless.

### Q2: Can a rest parameter be used as the first parameter?

**Answer:** Yes, rest parameters can be at any position, but they must be the last parameter in the signature. You can have required parameters before the rest parameter.

### Q3: How do rest parameters work with generics?

**Answer:** Rest parameters can be typed as generic arrays (`...args: T[]`) or generic tuples (`...args: [T, U]`). This enables type-safe variadic functions that preserve type information across arguments.

### Q4: What is the difference between rest parameters and spread syntax?

**Answer:** Rest parameters gather multiple arguments into an array in a function signature. Spread syntax expands an array into individual arguments at a call site. They use the same `...` syntax but in opposite directions.
