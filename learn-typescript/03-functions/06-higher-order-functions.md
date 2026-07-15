# Higher-Order Functions in TypeScript

## Table of Contents

1. [Functions That Return Functions](#functions-that-return-functions)
2. [Currying with Types](#currying-with-types)
3. [Partial Application](#partial-application)
4. [Function Composition](#function-composition)
5. [Memoization with Types](#memoization-with-types)
6. [Decorator Pattern with Functions](#decorator-pattern-with-functions)
7. [Pipe Function with Types](#pipe-function-with-types)
8. [Flow Function](#flow-function)
9. [Lodash/Ramda Typed Examples](#lodashramda-typed-examples)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Functions That Return Functions

A higher-order function is a function that takes one or more functions as arguments or returns a function.

```typescript
// Basic: function that returns a function
function multiply(factor: number): (value: number) => number {
  return (value: number) => value * factor;
}

const double = multiply(2);
const triple = multiply(3);

console.log(double(5));   // 10
console.log(triple(5));   // 15

// Function returning a function with different type
function createGreeter(greeting: string): (name: string) => string {
  return (name: string) => `${greeting}, ${name}!`;
}

const hello = createGreeter("Hello");
const howdy = createGreeter("Howdy");

console.log(hello("Alice"));  // "Hello, Alice!"
console.log(howdy("Bob"));    // "Howdy, Bob!"

// Function returning a function with complex types
interface Logger {
  (message: string): void;
}

function createLogger(prefix: string, level: string): Logger {
  return (message: string): void => {
    console.log(`[${prefix}] [${level}] ${message}`);
  };
}

const appLogger = createLogger("APP", "INFO");
const errorLogger = createLogger("APP", "ERROR");

appLogger("Server started");
errorLogger("Connection failed");
```

### Practical Examples

```typescript
// Validation factory
function createValidator(
  validate: (value: string) => boolean,
  errorMessage: string
): (value: string) => string | null {
  return (value: string): string | null => {
    return validate(value) ? null : errorMessage;
  };
}

const emailValidator = createValidator(
  (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),
  "Invalid email address"
);

const minLength = (min: number) =>
  createValidator(
    (value) => value.length >= min,
    `Must be at least ${min} characters`
  );

const passwordValidator = minLength(8);

console.log(emailValidator("test@example.com")); // null
console.log(emailValidator("invalid"));           // "Invalid email address"
console.log(passwordValidator("short"));          // "Must be at least 8 characters"

// Event handler factory
function createEventHandler<T>(
  handler: (event: T) => void,
  errorHandler: (error: Error) => void
): (event: T) => void {
  return (event: T): void => {
    try {
      handler(event);
    } catch (error) {
      errorHandler(error as Error);
    }
  };
}

const safeClickHandler = createEventHandler<MouseEvent>(
  (event) => console.log("Clicked at", event.clientX, event.clientY),
  (error) => console.error("Click handler error:", error)
);
```

---

## Currying with Types

Currying transforms a function that takes multiple arguments into a sequence of functions that each take a single argument.

```typescript
// Manual currying
function add(a: number): (b: number) => number {
  return (b: number) => a + b;
}

const add5 = add(5);
console.log(add5(3)); // 8

// Generic curry function
function curry<A extends unknown[], R>(
  fn: (...args: A) => R
): CurriedFunction<A, R> {
  const arity = fn.length;

  function curried(args: unknown[]): unknown {
    if (args.length >= arity) {
      return fn(...(args as A));
    }
    return (moreArgs: unknown[]) => curried([...args, ...moreArgs]);
  }

  return curried([]) as CurriedFunction<A, R>;
}

// Curried functions for common operations
const curriedAdd = curry((a: number, b: number) => a + b);
const add10 = curriedAdd(10);
console.log(add10(5)); // 15

const curriedMap = curry(<T, U>(fn: (item: T) => U, items: T[]) =>
  items.map(fn)
);

const doubleAll = curriedMap((n: number) => n * 2);
console.log(doubleAll([1, 2, 3])); // [2, 4, 6]

// Practical currying examples
const curriedFetch = curry(
  async (url: string, options: RequestInit): Promise<Response> => {
    return fetch(url, options);
  }
);

const fetchGet = curriedFetch("", { method: "GET" });
const fetchPost = curriedFetch("", { method: "POST" });

// Curried logging
const curriedLog = curry(
  (level: string, message: string, data?: unknown): void => {
    console.log(`[${level}] ${message}`, data);
  }
);

const infoLog = curriedLog("info");
const errorLog = curriedLog("error");

infoLog("User logged in", { userId: 123 });
errorLog("Connection failed");
```

### Auto-Curry Implementation

```typescript
type Curried<T> = T extends (...args: infer A) => infer R
  ? A extends [infer First, ...infer Rest]
    ? Rest extends [never]
      ? (arg: First) => R
      : (arg: First) => Curried<(...args: Rest) => R>
    : R
  : never;

function autoCurry<A extends unknown[], R>(
  fn: (...args: A) => R
): Curried<(...args: A) => R> {
  const arity = fn.length;

  function curried(args: unknown[]): unknown {
    if (args.length >= arity) {
      return fn(...(args as A));
    }
    return (arg: unknown) => curried([...args, arg]);
  }

  return curried([]) as Curried<(...args: A) => R>;
}

// Usage
const divide = autoCurry((a: number, b: number) => a / b);
const divideBy2 = divide(2);
console.log(divideBy2(10)); // 5
```

---

## Partial Application

Partial application fixes a few arguments of a function, producing another function with smaller arity.

```typescript
// Manual partial application
function partial<A, B, R>(
  fn: (a: A, b: B) => R,
  fixedA: A
): (b: B) => R {
  return (b: B) => fn(fixedA, b);
}

const add = (a: number, b: number) => a + b;
const add10 = partial(add, 10);
console.log(add10(5)); // 15

// Generic partial application
function partialRight<A extends unknown[], R>(
  fn: (...args: A) => R,
  ...fixedArgs: Partial<A>
): (...remainingArgs: any[]) => R {
  return (...remainingArgs: any[]) => {
    return fn(...remainingArgs, ...fixedArgs) as R;
  };
}

// Partial application with placeholders
function partialFill<A extends unknown[], R>(
  fn: (...args: A) => R,
  ...fixedArgs: any[]
): (...remainingArgs: any[]) => R {
  return (...remainingArgs: any[]) => {
    const args = [...fixedArgs];
    let remainingIndex = 0;
    for (let i = 0; i < args.length; i++) {
      if (args[i] === undefined) {
        args[i] = remainingArgs[remainingIndex++];
      }
    }
    return fn(...args, ...remainingArgs.slice(remainingIndex)) as R;
  };
}

// Practical partial application
const createEndpoint = partialRight(
  (baseUrl: string, path: string, params: Record<string, string>) =>
    `${baseUrl}${path}?${new URLSearchParams(params)}`,
  { format: "json" }
);

const apiEndpoint = createEndpoint("https://api.com", "/users");

// Partial application in event handling
function handleEvent(
  eventType: string,
  handler: (event: Event) => void,
  element: HTMLElement
): void {
  element.addEventListener(eventType, handler);
}

const handleClick = partialRight(handleEvent, "click");
// Can now use: handleClick(handler, element)
```

---

## Function Composition

Combining multiple functions into a single function.

```typescript
// Simple composition (right to left, mathematical notation)
function compose<A, B, C>(
  f: (b: B) => C,
  g: (a: A) => B
): (a: A) => C {
  return (a) => f(g(a));
}

const add1 = (x: number) => x + 1;
const double = (x: number) => x * 2;
const square = (x: number) => x * x;

const add1ThenDouble = compose(double, add1);
console.log(add1ThenDouble(3)); // (3 + 1) * 2 = 8

// Multi-function composition
function composeMany<A>(
  ...fns: Array<(arg: A) => A>
): (arg: A) => A {
  return (arg) => fns.reduce((result, fn) => fn(result), arg);
}

const process = composeMany(
  (x: number) => x + 1,
  (x: number) => x * 2,
  (x: number) => x - 3
);

console.log(process(5)); // ((5 + 1) * 2) - 3 = 9

// Compose with different types
function composeChain<A, B, C, D>(
  f: (c: C) => D,
  g: (b: B) => C,
  h: (a: A) => B
): (a: A) => D {
  return (a) => f(g(h(a)));
}

const transform = composeChain(
  (s: string) => s.toUpperCase(),
  (n: number) => n.toString(),
  (x: number) => x * 2
);

console.log(transform(5)); // "10"
```

### Practical Composition

```typescript
// Data transformation pipeline
interface User {
  name: string;
  age: number;
  email: string;
  active: boolean;
}

const filterActive = (users: User[]) => users.filter((u) => u.active);
const sortByAge = (users: User[]) => [...users].sort((a, b) => a.age - b.age);
const extractNames = (users: User[]) => users.map((u) => u.name);
const formatList = (names: string[]) => names.join(", ");

const getActiveUserNames = composeMany(
  filterActive,
  sortByAge,
  extractNames,
  formatList as any
) as (users: User[]) => string;

// Compose with validation
const validateEmail = (email: string) => email.includes("@");
const validateLength = (s: string) => s.length > 0;
const sanitize = (s: string) => s.trim().toLowerCase();

const processEmail = composeMany(sanitize, (s: string) => {
  if (!validateEmail(s)) throw new Error("Invalid email");
  return s;
});
```

---

## Memoization with Types

Caching function results for performance optimization.

```typescript
// Basic memoization
function memoize<Args extends unknown[], R>(
  fn: (...args: Args) => R
): (...args: Args) => R {
  const cache = new Map<string, R>();

  return (...args: Args): R => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Memoized expensive computation
const fibonacci = memoize((n: number): number => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

console.log(fibonacci(50)); // Fast! Uses cached values

// Memoize with custom key generator
function memoizeWithKey<Args extends unknown[], R>(
  fn: (...args: Args) => R,
  keyFn: (...args: Args) => string
): (...args: Args) => R {
  const cache = new Map<string, R>();

  return (...args: Args): R => {
    const key = keyFn(...args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Memoize async functions
function memoizeAsync<Args extends unknown[], R>(
  fn: (...args: Args) => Promise<R>
): (...args: Args) => Promise<R> {
  const cache = new Map<string, Promise<R>>();

  return (...args: Args): Promise<R> => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Memoize with TTL (time-to-live)
function memoizeWithTTL<Args extends unknown[], R>(
  fn: (...args: Args) => R,
  ttlMs: number
): (...args: Args) => R {
  const cache = new Map<string, { value: R; timestamp: number }>();

  return (...args: Args): R => {
    const key = JSON.stringify(args);
    const cached = cache.get(key);

    if (cached && Date.now() - cached.timestamp < ttlMs) {
      return cached.value;
    }

    const result = fn(...args);
    cache.set(key, { value: result, timestamp: Date.now() });
    return result;
  };
}

// LRU Cache memoization
function memoizeWithLRU<Args extends unknown[], R>(
  fn: (...args: Args) => R,
  maxSize: number
): (...args: Args) => R {
  const cache = new Map<string, R>();

  return (...args: Args): R => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      const value = cache.get(key)!;
      // Move to end (most recently used)
      cache.delete(key);
      cache.set(key, value);
      return value;
    }

    const result = fn(...args);

    // Evict oldest if at capacity
    if (cache.size >= maxSize) {
      const firstKey = cache.keys().next().value!;
      cache.delete(firstKey);
    }

    cache.set(key, result);
    return result;
  };
}
```

---

## Decorator Pattern with Functions

Wrapping functions to add behavior without modifying the original.

```typescript
// Basic function decorator
function withLogging<A extends unknown[], R>(
  fn: (...args: A) => R
): (...args: A) => R {
  return (...args: A): R => {
    console.log(`Calling ${fn.name} with`, args);
    const result = fn(...args);
    console.log(`${fn.name} returned`, result);
    return result;
  };
}

const add = withLogging((a: number, b: number) => a + b);
add(2, 3); // Logs: Calling anonymous with [2, 3], anonymous returned 5

// Timing decorator
function withTiming<A extends unknown[], R>(
  fn: (...args: A) => R
): (...args: A) => R {
  return (...args: A): R => {
    const start = performance.now();
    const result = fn(...args);
    const end = performance.now();
    console.log(`${fn.name} took ${end - start}ms`);
    return result;
  };
}

// Retry decorator
function withRetry<A extends unknown[], R>(
  fn: (...args: A) => R,
  maxRetries: number = 3
): (...args: A) => R {
  return (...args: A): R => {
    let lastError: Error | undefined;
    for (let i = 0; i <= maxRetries; i++) {
      try {
        return fn(...args);
      } catch (error) {
        lastError = error as Error;
        console.log(`Attempt ${i + 1} failed, retrying...`);
      }
    }
    throw lastError;
  };
}

// Validation decorator
function withValidation<A extends unknown[], R>(
  fn: (...args: A) => R,
  validators: Array<(args: A) => boolean>
): (...args: A) => R {
  return (...args: A): R => {
    for (const validator of validators) {
      if (!validator(args)) {
        throw new Error(`Validation failed for ${fn.name}`);
      }
    }
    return fn(...args);
  };
}

// Cache decorator
function withCache<A extends unknown[], R>(
  fn: (...args: A) => R
): (...args: A) => R {
  const cache = new Map<string, R>();

  return (...args: A): R => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Composing decorators
const heavyComputation = withLogging(
  withTiming(
    withCache((n: number) => {
      // Expensive computation
      return Array.from({ length: n }, (_, i) => i ** 2);
    })
  )
);
```

---

## Pipe Function with Types

Left-to-right function composition using pipe.

```typescript
// Basic pipe function
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

// Usage (left to right, more readable than compose)
const processString = pipe(
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/\s+/g, "_"),
  (s: string) => s.padStart(10, "0")
);

console.log(processString("  Hello World  ")); // "0hello_world"

// Pipe with async functions
async function pipeAsync<A, B>(f1: (a: A) => Promise<B>): (a: A) => Promise<B>;
async function pipeAsync<A, B, C>(
  f1: (a: A) => Promise<B>,
  f2: (b: B) => Promise<C>
): (a: A) => Promise<C>;
async function pipeAsync(
  ...fns: Array<(arg: any) => Promise<any>>
): (arg: any) => Promise<any> {
  return async (arg) => {
    let result = arg;
    for (const fn of fns) {
      result = await fn(result);
    }
    return result;
  };
}

// Practical pipe usage
const processUser = pipe(
  (input: { name: string; email: string }) => ({
    ...input,
    name: input.name.trim(),
    email: input.email.toLowerCase(),
  }),
  (user) => ({
    ...user,
    isValid: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email),
  }),
  (user) => ({
    ...user,
    displayName: user.isValid ? user.name : "Unknown User",
  })
);

console.log(processUser({ name: "  Alice  ", email: "ALICE@EXAMPLE.COM" }));
// { name: "Alice", email: "alice@example.com", isValid: true, displayName: "Alice" }
```

---

## Flow Function

Alias for compose (left-to-right composition).

```typescript
// flow is the same as pipe
function flow<A, B>(f1: (a: A) => B): (a: A) => B;
function flow<A, B, C>(f1: (a: A) => B, f2: (b: B) => C): (a: A) => C;
function flow<A, B, C, D>(
  f1: (a: A) => B,
  f2: (b: B) => C,
  f3: (c: C) => D
): (a: A) => D;
function flow(...fns: Array<(arg: any) => any>): (arg: any) => any {
  return (arg) => fns.reduce((result, fn) => fn(result), arg);
}

// Usage
const truncate = (s: string) => (s.length > 10 ? s.slice(0, 10) : s);
const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
const addEllipsis = (s: string) => s + "...";

const formatTitle = flow(truncate, capitalize, addEllipsis);
console.log(formatTitle("hello world foo")); // "Hello worl..."
```

---

## Lodash/Ramda Typed Examples

```typescript
// Lodash-style typed helpers
import _ from "lodash";

// Typed map
function typedMap<T, U>(array: T[], fn: (item: T, index: number) => U): U[] {
  return array.map(fn);
}

// Typed filter
function typedFilter<T>(
  array: T[],
  predicate: (item: T, index: number) => boolean
): T[] {
  return array.filter(predicate);
}

// Typed reduce
function typedReduce<T, U>(
  array: T[],
  reducer: (acc: U, item: T, index: number) => U,
  initial: U
): U {
  return array.reduce(reducer, initial);
}

// Lodash-style debounce with types
function debounce<A extends unknown[], R>(
  fn: (...args: A) => R,
  delay: number
): (...args: A) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: A): void => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Lodash-style throttle with types
function throttle<A extends unknown[], R>(
  fn: (...args: A) => R,
  limit: number
): (...args: A) => void {
  let inThrottle = false;
  return (...args: A): void => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

// Ramda-style curry
function ramdaCurry(fn: Function): Function {
  const arity = fn.length;
  function curried(args: unknown[]): Function {
    if (args.length >= arity) {
      return fn(...args);
    }
    return (...moreArgs: unknown[]) => curried([...args, ...moreArgs]);
  }
  return curried([]);
}

// Ramda-style compose (right to left)
function ramdaCompose<A>(
  ...fns: Array<(arg: A) => A>
): (arg: A) => A {
  return (arg) => fns.reduceRight((result, fn) => fn(result), arg);
}
```

---

## Best Practices

```typescript
// 1. Keep functions pure when using composition
const pure = (x: number) => x + 1; // GOOD
const impure = (x: number) => { console.log(x); return x + 1; }; // BAD

// 2. Use pipe for readability (left to right)
const result = pipe(
  fetchData,        // First
  processData,      // Second
  formatOutput      // Third
)(input);

// 3. Type your higher-order functions properly
function typedHigherOrder<T, U>(
  fn: (item: T) => U
): (items: T[]) => U[] {
  return (items) => items.map(fn);
}

// 4. Memoize expensive computations
const expensiveCalc = memoize((n: number) => {
  // Long computation
  return n ** 2;
});

// 5. Use decorators for cross-cutting concerns
const logged = withLogging(myFunction);
const timed = withTiming(myFunction);
const cached = withCache(myFunction);

// 6. Document the function type in comments
/** @type {(a: number) => (b: number) => number} */
const curriedAdd = curry((a: number, b: number) => a + b);
```

---

## Interview Questions

### Q1: What are higher-order functions?

**Answer:** Higher-order functions are functions that either take other functions as arguments, return functions, or both. Examples include `map`, `filter`, `reduce`, `compose`, and `pipe`.

### Q2: What is currying and why is it useful?

**Answer:** Currying transforms a function with multiple arguments into a sequence of functions each taking a single argument. It's useful for creating specialized functions, partial application, and functional composition.

### Q3: What is the difference between compose and pipe?

**Answer:** Compose applies functions right to left (mathematical composition). Pipe applies functions left to right (readable flow). They're functionally equivalent but pipe is more readable for sequential transformations.

### Q4: When should you memoize a function?

**Answer:** Memoize when: (1) the function is pure, (2) it's called frequently with the same arguments, (3) computation is expensive, (4) memory is available for caching.
