# TypeScript Functions - Interview Questions

## Table of Contents

1. [Function Basics](#function-basics)
2. [Optional and Default Parameters](#optional-and-default-parameters)
3. [Rest Parameters](#rest-parameters)
4. [Function Overloading](#function-overloading)
5. [Arrow Functions](#arrow-functions)
6. [Higher-Order Functions](#higher-order-functions)
7. [Pure Functions](#pure-functions)
8. [Function Types](#function-types)
9. [Closures](#closures)
10. [Recursion](#recursion)
11. [Advanced Questions](#advanced-questions)

---

## Function Basics

### Q1: What is the difference between a function declaration and a function expression?

**Answer:**
- **Function declaration** defines a named function and is hoisted (can be called before the line where it's defined).
- **Function expression** assigns a function to a variable and is not hoisted.

```typescript
// Declaration - hoisted
console.log(add(2, 3)); // 5
function add(a: number, b: number): number {
  return a + b;
}

// Expression - NOT hoisted
// console.log(multiply(2, 3)); // Error!
const multiply = (a: number, b: number): number => a * b;
```

### Q2: When should you use explicit return types?

**Answer:**
- **Exported/public API functions:** Establishes a contract that won't break consumers if implementation changes.
- **Complex return types:** Helps documentation and IDE autocomplete.
- **Recursive functions:** TypeScript sometimes struggles to infer recursive return types.
- **When you want the compiler to catch unintended return type changes.**

```typescript
// GOOD: Explicit return type for exported function
export function processData(input: string): ProcessedResult {
  // If implementation accidentally returns wrong type, compiler catches it
}

// FINE: Let TypeScript infer for simple internal functions
const double = (x: number) => x * 2;
```

### Q3: What is the `void` return type and when to use it?

**Answer:** `void` means the function doesn't return a meaningful value. Use it for functions that perform side effects (logging, modifying state, etc.). A `void` function can technically return a value, but it's ignored.

```typescript
function logMessage(msg: string): void {
  console.log(msg);
}

// void callbacks can return values (return is ignored)
[1, 2, 3].forEach((n) => n * 2); // No error, return is ignored
```

### Q4: Can a function return both a value and void?

**Answer:** A `void`-typed function can technically return a value, but the caller shouldn't rely on it. This is because `void` means "the return value will be ignored."

```typescript
type VoidFn = () => void;

const fn: VoidFn = () => 42; // Allowed! But the return value is ignored
```

---

## Optional and Default Parameters

### Q5: What is the difference between optional parameters and default parameters?

**Answer:**
- **Optional (`?`):** The parameter can be omitted; its value is `undefined` if not provided.
- **Default (`= value`):** The parameter has a fallback value used when omitted or when `undefined` is explicitly passed.

```typescript
// Optional - value is undefined if not provided
function greet(name?: string): string {
  return `Hello, ${name ?? "World"}`;
}

// Default - has a fallback value
function greet2(name: string = "World"): string {
  return `Hello, ${name}`;
}
```

### Q6: Why must optional parameters come after required parameters?

**Answer:** TypeScript has no way to distinguish between "missing argument" and "undefined argument" in positional parameters. If optional parameters came first, the compiler couldn't determine which arguments were intended for which parameters.

```typescript
// VALID
function create(name: string, age?: number): User { /* ... */ }

// INVALID
// function create(name?: string, age: number): User { /* ... */ }

// WORKAROUND: Use options object
function create(config: { name: string; age?: number }): User { /* ... */ }
```

### Q7: How do you handle 4+ optional parameters in a function?

**Answer:** Use an options object pattern for self-documenting, order-independent parameters.

```typescript
// BAD: Hard to remember parameter order
function connect(host, port, secure, timeout, retries) {}

// GOOD: Self-documenting
interface ConnectOptions {
  host: string;
  port?: number;
  secure?: boolean;
  timeout?: number;
  retries?: number;
}

function connect(options: ConnectOptions): Connection { /* ... */ }
```

---

## Rest Parameters

### Q8: What is the difference between rest parameters and the `arguments` object?

**Answer:**
- **Rest parameters** are real arrays with full type support, work in arrow functions, and only capture remaining parameters.
- **`arguments`** is array-like, lacks type safety, doesn't work in arrow functions, and captures all parameters.

```typescript
// Rest (recommended)
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}

// Arrow functions can use rest but not arguments
const sumArrow = (...numbers: number[]): number =>
  numbers.reduce((a, b) => a + b, 0);
```

### Q9: Can a rest parameter be used as the first parameter?

**Answer:** Yes, but it must be the last parameter in the signature. You can have required parameters before the rest parameter.

```typescript
function log(level: string, ...messages: unknown[]): void {
  console.log(`[${level}]`, ...messages);
}

log("info", "Server started", "on port 3000");
```

### Q10: What is the difference between rest parameters and spread syntax?

**Answer:**
- **Rest parameters** gather multiple arguments into an array in a function signature.
- **Spread syntax** expands an array into individual arguments at a call site.

```typescript
// REST: Gathers into array
function sum(...numbers: number[]): number { /* ... */ }

// SPREAD: Expands array into arguments
const nums = [1, 2, 3];
sum(...nums); // sum(1, 2, 3)
```

---

## Function Overloading

### Q11: What is function overloading in TypeScript?

**Answer:** Function overloading allows a single function to have multiple signatures with different parameter types and return types. TypeScript resolves which signature to use based on the arguments.

```typescript
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;
function format(value: string | number | Date): string {
  if (typeof value === "string") return value.toUpperCase();
  if (typeof value === "number") return value.toFixed(2);
  return value.toISOString();
}

format("hello");   // string
format(3.14);      // string
format(new Date()); // string
```

### Q12: What is the difference between overload signatures and the implementation signature?

**Answer:**
- **Overload signatures** define the public API that callers see.
- **Implementation signature** is hidden from callers and must be compatible with all overloads.

```typescript
// These are overload signatures (public API)
function process(input: string): string;
function process(input: number): number;
// This is the implementation signature (hidden)
function process(input: string | number): string | number {
  if (typeof input === "string") return input.trim();
  return input * 2;
}
```

### Q13: When should you use overloads vs union types vs generics?

**Answer:**
- **Union types:** Simple cases where return type doesn't depend on input type.
- **Overloads:** Different inputs produce different output types.
- **Generics:** The relationship between input and output types is consistent.

```typescript
// Union: Same return type regardless
function format(input: string | number): string {
  return String(input);
}

// Overloads: Different input → different output
function parseJson(input: string): unknown;
function parseJson<T>(input: string, schema: Schema<T>): T;

// Generics: Consistent relationship
function wrap<T>(value: T): { value: T; timestamp: Date } {
  return { value, timestamp: new Date() };
}
```

---

## Arrow Functions

### Q14: What is the difference between arrow functions and regular functions in TypeScript?

**Answer:**
- Arrow functions don't have their own `this` binding (lexically inherited).
- Arrow functions can't be used as constructors.
- Arrow functions don't have `arguments` object.
- Arrow functions can't be generators.
- Arrow functions have concise syntax.

```typescript
class Timer {
  seconds = 0;

  // Regular function: 'this' depends on call context
  startRegular() {
    setInterval(function () {
      this.seconds++; // 'this' is undefined/global
    }, 1000);
  }

  // Arrow function: 'this' is lexically bound
  startArrow() {
    setInterval(() => {
      this.seconds++; // 'this' is Timer instance
    }, 1000);
  }
}
```

### Q15: When should you use arrow functions vs regular functions?

**Answer:**
- **Arrow functions:** Callbacks, array methods, when you need lexical `this`.
- **Regular functions:** Object methods, constructors, when you need `this` to depend on call context.

### Q16: Why can't arrow functions be used as constructors?

**Answer:** Arrow functions lack a `prototype` property and don't have their own `this` binding. The `new` keyword requires these to create and initialize objects properly.

### Q17: What is lexical `this` in arrow functions?

**Answer:** Arrow functions inherit `this` from the enclosing lexical scope (the surrounding non-arrow function or global scope). This makes them ideal for callbacks where you need access to the outer context.

---

## Higher-Order Functions

### Q18: What are higher-order functions?

**Answer:** Higher-order functions are functions that either take other functions as arguments, return functions, or both. Examples include `map`, `filter`, `reduce`, `compose`, and `pipe`.

```typescript
// Takes a function as argument
function applyToAll<T>(items: T[], fn: (item: T) => T): T[] {
  return items.map(fn);
}

// Returns a function
function createMultiplier(factor: number): (value: number) => number {
  return (value) => value * factor;
}
```

### Q19: What is currying and why is it useful?

**Answer:** Currying transforms a function with multiple arguments into a sequence of functions each taking a single argument. It's useful for creating specialized functions, partial application, and functional composition.

```typescript
// Before currying
function add(a: number, b: number): number {
  return a + b;
}

// After currying
function curriedAdd(a: number): (b: number) => number {
  return (b) => a + b;
}

const add5 = curriedAdd(5);
add5(3); // 8
```

### Q20: What is the difference between compose and pipe?

**Answer:** Compose applies functions right to left (mathematical composition). Pipe applies functions left to right (readable flow). They're functionally equivalent but pipe is more readable.

```typescript
// Compose (right to left)
const result = compose(format, validate, parse)(input);

// Pipe (left to right) - same operations, more readable
const result2 = pipe(parse, validate, format)(input);
```

### Q21: How do you type a function that returns a function?

**Answer:** Use nested arrow syntax or type aliases.

```typescript
// Type alias
type FnReturningFn = (x: number) => (y: string) => boolean;

// Inline
function createFormatter(prefix: string): (value: string) => string {
  return (value) => `${prefix}${value}`;
}

// Generic version
function curry<A extends unknown[], R>(
  fn: (...args: A) => R
): CurriedFn<A, R> {
  // ...
}
```

---

## Pure Functions

### Q22: What makes a function "pure"?

**Answer:** A function is pure if:
1. It always returns the same output for the same input (deterministic).
2. It produces no side effects (no modifying external state, no I/O).

```typescript
// Pure
function add(a: number, b: number): number {
  return a + b;
}

// Impure (side effect)
let count = 0;
function increment(): number {
  return ++count;
}
```

### Q23: What is referential transparency?

**Answer:** Referentially transparent means a function call can be replaced with its return value without changing program behavior. All pure functions are referentially transparent.

```typescript
// Referentially transparent
function square(x: number): number {
  return x * x;
}

// These are equivalent:
const a = square(5) + square(3); // 25 + 9 = 34
const b = 25 + 9;                // 34
```

### Q24: Why are pure functions easier to test?

**Answer:** Pure functions require no mocking, no setup, no teardown. You provide inputs and assert outputs. No state to reset between tests.

```typescript
// Simple, deterministic tests
it("should calculate discount", () => {
  expect(calculateDiscount(100, 10)).toBe(90);
});

it("should handle edge cases", () => {
  expect(calculateDiscount(100, 0)).toBe(100);
  expect(calculateDiscount(100, 100)).toBe(0);
});
```

---

## Function Types

### Q25: What is the difference between `type Func = () => void` and `type Func = () => undefined`?

**Answer:**
- **`void`:** The return value is ignored. The function can return anything.
- **`undefined`:** The function must explicitly return `undefined`.

```typescript
type VoidFn = () => void;
type UndefinedFn = () => undefined;

const a: VoidFn = () => 42;     // Allowed
const b: UndefinedFn = () => 42; // Error
```

### Q26: What are call signatures and when would you use them?

**Answer:** Call signatures define callable types using interface syntax. Useful when you need to add properties to a function type or create overloaded, extensible function types.

```typescript
interface Counter {
  (start: number): void;
  interval: number;
  reset(): void;
}

const counter: Counter = (start) => { /* ... */ };
counter.interval = 1000;
counter.reset();
```

### Q27: What is the `this` parameter in TypeScript?

**Answer:** The `this` parameter is a TypeScript-only parameter that defines the type of `this` inside the function. It's erased at runtime and only used for compile-time checking.

```typescript
interface Logger {
  log(this: Logger, message: string): void;
}

function setupLogger(logger: Logger): void {
  logger.log("test"); // TypeScript checks 'this' type
}
```

---

## Closures

### Q28: What is a closure in TypeScript?

**Answer:** A closure is a function that captures and remembers variables from its enclosing lexical scope, even after the outer function has returned. Closures enable private state, function factories, and many FP patterns.

```typescript
function createCounter(): () => number {
  let count = 0;
  return function (): number {
    return ++count;
  };
}

const counter = createCounter();
counter(); // 1
counter(); // 2 (count is remembered)
```

### Q29: How do closures handle the `var` vs `let` problem in loops?

**Answer:** `var` is function-scoped, so all closures share the same variable. `let` is block-scoped, creating a new binding per iteration.

```typescript
// BAD: var
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // 5, 5, 5, 5, 5
}

// GOOD: let
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // 0, 1, 2, 3, 4
}
```

### Q30: What are common uses of closures?

**Answer:** Private state, function factories, memoization, event handlers, partial application, module patterns, callbacks with context, debounce/throttle.

---

## Recursion

### Q31: What is tail recursion and why is it important?

**Answer:** Tail recursion is when the recursive call is the last operation. It allows engines to optimize by reusing the stack frame, preventing overflow. Not all JS engines support this optimization.

```typescript
// NOT tail-recursive
function factorial(n: number): number {
  if (n <= 1) return 1;
  return n * factorial(n - 1); // Multiplication after recursive call
}

// Tail-recursive
function factorialTail(n: number, acc: number = 1): number {
  if (n <= 1) return acc;
  return factorialTail(n - 1, n * acc); // Recursive call is last
}
```

### Q32: How do you prevent stack overflow in recursive functions?

**Answer:** (1) Convert to iteration, (2) Tail recursion with TCO, (3) Trampolining, (4) Async chunking, (5) Explicit stack.

```typescript
// Trampolining
function trampoline<A extends unknown[], R>(
  fn: (...args: A) => R | (() => R)
): (...args: A) => R {
  return (...args: A): R => {
    let result = fn(...args);
    while (typeof result === "function") {
      result = result();
    }
    return result as R;
  };
}
```

### Q33: When should you use recursion vs iteration?

**Answer:**
- **Recursion:** Tree/graph traversal, divide-and-conquer, recursive data structures.
- **Iteration:** Simple loops, performance-critical code, very deep recursion.

---

## Advanced Questions

### Q34: How do you type a function that accepts any function as a callback?

**Answer:**
```typescript
// Using generics
function withRetry<T extends (...args: any[]) => any>(
  fn: T,
  retries: number
): T {
  return ((...args: any[]) => {
    for (let i = 0; i <= retries; i++) {
      try {
        return fn(...args);
      } catch (e) {
        if (i === retries) throw e;
      }
    }
  }) as T;
}
```

### Q35: How do you create a type-safe event emitter?

**Answer:**
```typescript
type EventMap = {
  login: [userId: string, timestamp: Date];
  logout: [userId: string];
  purchase: [userId: string, amount: number];
};

class TypedEmitter<Events extends Record<string, unknown[]>> {
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
    listeners.forEach((fn) => fn(...args));
  }
}

const emitter = new TypedEmitter<EventMap>();
emitter.on("login", (userId, timestamp) => { /* fully typed */ });
```

### Q36: What is the difference between `never` and `void` return types?

**Answer:**
- **`void`:** Function returns but the value is meaningless (side-effect functions).
- **`never`:** Function never returns (throws error, infinite loop, or exhaustive check).

```typescript
function log(msg: string): void {
  console.log(msg); // Returns but value is ignored
}

function throwError(msg: string): never {
  throw new Error(msg); // Never returns
}

// Exhaustive check
function process(x: string | number): string {
  if (typeof x === "string") return x;
  if (typeof x === "number") return x.toString();
  const exhaustive: never = x; // Compiler ensures all cases handled
  return exhaustive;
}
```

### Q37: How do you implement a type-safe pipe function?

**Answer:**
```typescript
function pipe<A, B>(f1: (a: A) => B): (a: A) => B;
function pipe<A, B, C>(f1: (a: A) => B, f2: (b: B) => C): (a: A) => C;
function pipe<A, B, C, D>(
  f1: (a: A) => B,
  f2: (b: B) => C,
  f3: (c: C) => D
): (a: A) => D;
function pipe(...fns: Array<(arg: any) => any>): (arg: any) => any {
  return (arg) => fns.reduce((result, fn) => fn(result), arg);
}

// Usage
const process = pipe(
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/\s+/g, "_")
);

process("  Hello World  "); // "hello_world"
```

### Q38: How do you implement a type-safe curry function?

**Answer:**
```typescript
type Curried<A extends unknown[], R> =
  A extends [infer First, ...infer Rest]
    ? Rest extends [never]
      ? (arg: First) => R
      : (arg: First) => Curried<Rest, R>
    : R;

function curry<A extends unknown[], R>(
  fn: (...args: A) => R
): Curried<A, R> {
  const arity = fn.length;

  function curried(args: unknown[]): unknown {
    if (args.length >= arity) {
      return fn(...(args as A));
    }
    return (arg: unknown) => curried([...args, arg]);
  }

  return curried([]) as Curried<A, R>;
}

const add = curry((a: number, b: number, c: number) => a + b + c);
add(1)(2)(3);   // 6
add(1, 2)(3);   // 6
add(1)(2, 3);   // 6
```

### Q39: What are discriminated unions and how do they relate to function overloads?

**Answer:** Discriminated unions use a common literal property (discriminant) to distinguish between types. They can often replace function overloads with pattern matching.

```typescript
// Discriminated union (preferred over overloads for this case)
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

### Q40: How do you type a function that accepts either a value or an array of values?

**Answer:**
```typescript
// Using overloads
function toArray<T>(value: T): T[];
function toArray<T>(value: T[]): T[];
function toArray<T>(value: T | T[]): T[] {
  return Array.isArray(value) ? value : [value];
}

// Using union with Array.isArray check
function ensureArray<T>(value: T | T[]): T[] {
  return Array.isArray(value) ? value : [value];
}

// Using generic constraint
function wrap<T>(value: T): T[] {
  return Array.isArray(value) ? value : [value];
}
```
