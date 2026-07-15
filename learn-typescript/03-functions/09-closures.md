# Closures in TypeScript

## Table of Contents

1. [Closures in TypeScript](#closures-in-typescript)
2. [Lexical Scope](#lexical-scope)
3. [Closure with Type Inference](#closure-with-type-inference)
4. [Closure in Loops](#closure-in-loops)
5. [Closure Patterns](#closure-patterns)
6. [Factory Functions](#factory-functions)
7. [Module Pattern with Closures](#module-pattern-with-closures)
8. [Performance Considerations](#performance-considerations)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Closures in TypeScript

A closure is a function that captures and remembers the variables from its enclosing lexical scope, even after the outer function has finished executing.

```typescript
// Basic closure
function createCounter(): () => number {
  let count = 0; // This variable is "captured" by the closure

  return function (): number {
    count++; // Accesses 'count' from the outer scope
    return count;
  };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
// 'count' is still accessible via the closure, but not directly

// Closure with parameter
function createMultiplier(factor: number): (value: number) => number {
  return function (value: number): number {
    return value * factor; // 'factor' is captured
  };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15

// Closure capturing multiple variables
function createLogger(prefix: string, level: string): (message: string) => string {
  const timestamp = new Date().toISOString(); // Captured

  return function (message: string): string {
    return `[${timestamp}] [${prefix}] [${level}] ${message}`;
  };
}

const logger = createLogger("APP", "INFO");
console.log(logger("Server started"));
// "[2024-01-15T...] [APP] [INFO] Server started"
```

### Closures in Action

```typescript
// Private state via closure
function createBankAccount(initialBalance: number): {
  deposit: (amount: number) => void;
  withdraw: (amount: number) => boolean;
  getBalance: () => number;
} {
  let balance = initialBalance;

  return {
    deposit(amount: number): void {
      if (amount > 0) {
        balance += amount;
      }
    },
    withdraw(amount: number): boolean {
      if (amount > 0 && amount <= balance) {
        balance -= amount;
        return true;
      }
      return false;
    },
    getBalance(): number {
      return balance;
    },
  };
}

const account = createBankAccount(1000);
account.deposit(500);
console.log(account.getBalance()); // 1500
account.withdraw(200);
console.log(account.getBalance()); // 1300
// balance is not directly accessible from outside

// Closure for memoization
function createMemoizedFn<A extends unknown[], R>(
  fn: (...args: A) => R
): (...args: A) => R {
  const cache = new Map<string, R>(); // Captured cache

  return function (...args: A): R {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const expensiveCalc = createMemoizedFn((n: number) => {
  console.log("Computing...");
  return n ** 2;
});

expensiveCalc(5); // "Computing..." → 25
expensiveCalc(5); // 25 (from cache, no "Computing...")
```

---

## Lexical Scope

Understanding how closures capture variables from their lexical scope.

```typescript
// Lexical scope determines what variables a closure can access
let globalVar = "global";

function outer(): void {
  let outerVar = "outer";

  function middle(): void {
    let middleVar = "middle";

    function inner(): void {
      let innerVar = "inner";

      // inner can access all outer scopes
      console.log(innerVar);   // inner (own scope)
      console.log(middleVar);  // middle (middle scope)
      console.log(outerVar);   // outer (outer scope)
      console.log(globalVar);  // global (global scope)
    }

    inner();
  }

  middle();
}

outer();

// Lexical scope chain
function createChain(): () => number {
  let a = 1;

  return function (): number {
    let b = 2;

    return function (): number {
      let c = 3;
      return a + b + c; // Captures a and b from outer scopes
    }();
  }();
}

// Variable shadowing in closures
function shadowing(): void {
  let x = 10;

  const fn1 = () => x; // Captures x = 10

  x = 20;

  const fn2 = () => x; // Captures x = 20 (same variable, different time)

  console.log(fn1()); // 20 (not 10! Closure captures reference, not value)
  console.log(fn2()); // 20
}

// Closures capture references, not values
function referenceVsValue(): void {
  let counter = 0;

  const increment = () => {
    counter++;
    return counter;
  };

  const getCounter = () => counter;

  console.log(increment()); // 1
  console.log(increment()); // 2
  console.log(getCounter()); // 2 (both closures share the same 'counter')
}
```

---

## Closure with Type Inference

TypeScript infers types in closures from their enclosing scope.

```typescript
// Type inference in closures
function createProcessor<T>(items: T[]): {
  getNext: () => T | undefined;
  reset: () => void;
  getAll: () => T[];
} {
  let index = 0; // Inferred as number

  return {
    getNext(): T | undefined {
      return items[index++]; // 'items' is T[], 'index' is number
    },
    reset(): void {
      index = 0;
    },
    getAll(): T[] {
      return [...items];
    },
  };
}

const processor = createProcessor([1, 2, 3]);
console.log(processor.getNext()); // 1
console.log(processor.getNext()); // 2

// Generic closure
function createSorter<T>(compareFn: (a: T, b: T) => number): (items: T[]) => T[] {
  return function (items: T[]): T[] {
    return [...items].sort(compareFn); // compareFn is captured with correct types
  };
}

const numberSort = createSorter<number>((a, b) => a - b);
const stringSort = createSorter<string>((a, b) => a.localeCompare(b));

// Closure with complex type inference
function createStateMachine<S extends string, E extends string>(
  initial: S,
  transitions: Record<S, Partial<Record<E, S>>>
): {
  getState: () => S;
  send: (event: E) => S;
  reset: () => S;
} {
  let current = initial;

  return {
    getState: () => current,
    send(event: E): S {
      const next = transitions[current]?.[event];
      if (next) {
        current = next;
      }
      return current;
    },
    reset(): S {
      current = initial;
      return current;
    },
  };
}

const trafficLight = createStateMachine("green", {
  green: { next: "yellow" },
  yellow: { next: "red" },
  red: { next: "green" },
});

console.log(trafficLight.getState()); // "green"
console.log(trafficLight.send("next")); // "yellow"
console.log(trafficLight.send("next")); // "red"
```

---

## Closure in Loops

Handling closures in loops correctly.

```typescript
// Classic problem: closures in for loops
// All functions share the same 'i' variable
const functions: Array<() => void> = [];

for (var i = 0; i < 5; i++) {
  functions.push(() => console.log(i));
}

// All log 5! (not 0, 1, 2, 3, 4)
functions.forEach((fn) => fn()); // 5, 5, 5, 5, 5

// Solution 1: Use let (block scoping)
const functions2: Array<() => void> = [];

for (let i = 0; i < 5; i++) {
  functions2.push(() => console.log(i));
}

// Each closure captures a different 'i'
functions2.forEach((fn) => fn()); // 0, 1, 2, 3, 4

// Solution 2: Use IIFE to create new scope
const functions3: Array<() => void> = [];

for (var i = 0; i < 5; i++) {
  (function (j: number) {
    functions3.push(() => console.log(j));
  })(i);
}

functions3.forEach((fn) => fn()); // 0, 1, 2, 3, 4

// Solution 3: Use bind
const functions4: Array<() => void> = [];

for (var i = 0; i < 5; i++) {
  functions4.push(
    ((j: number) => () => console.log(j)).bind(null, i)
  );
}

functions4.forEach((fn) => fn()); // 0, 1, 2, 3, 4

// Practical example: Event handlers in loops
function setupButtons(): void {
  const buttons = document.querySelectorAll("button");

  // WRONG: All handlers reference the same 'i'
  buttons.forEach(function (button, i) {
    button.addEventListener("click", function () {
      console.log(`Button ${i} clicked`); // Always logs the last 'i'
    });
  });

  // CORRECT: Each handler gets its own 'i'
  buttons.forEach((button, i) => {
    button.addEventListener("click", () => {
      console.log(`Button ${i} clicked`); // Correct index
    });
  });
}

// Closure in async loops
async function fetchDataForAll(urls: string[]): Promise<unknown[]> {
  const results: unknown[] = [];

  // CORRECT: Using for...of with await
  for (const url of urls) {
    const data = await fetch(url).then((r) => r.json());
    results.push(data);
  }

  return results;
}

// Closure with setTimeout
function scheduleTasks(): void {
  // WRONG with var
  for (var i = 0; i < 5; i++) {
    setTimeout(function () {
      console.log(i); // Logs 5 five times
    }, i * 1000);
  }

  // CORRECT with let
  for (let i = 0; i < 5; i++) {
    setTimeout(function () {
      console.log(i); // Logs 0, 1, 2, 3, 4
    }, i * 1000);
  }
}
```

---

## Closure Patterns

Common closure patterns in TypeScript.

```typescript
// 1. Function Factory
function createFormatter(
  prefix: string,
  suffix: string
): (value: string) => string {
  return (value: string) => `${prefix}${value}${suffix}`;
}

const bold = createFormatter("**", "**");
const italic = createFormatter("_", "_");
const code = createFormatter("`", "`");

// 2. Once (execute function only once)
function once<T extends (...args: any[]) => any>(
  fn: T
): (...args: Parameters<T>) => ReturnType<T> | undefined {
  let called = false;
  let result: ReturnType<T>;

  return function (this: any, ...args: Parameters<T>): ReturnType<T> | undefined {
    if (!called) {
      called = true;
      result = fn.apply(this, args);
      return result;
    }
    return result;
  };
}

const initialize = once(() => {
  console.log("Initializing...");
  return { ready: true };
});

initialize(); // "Initializing..." → { ready: true }
initialize(); // { ready: true } (no log)

// 3. Throttle
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  let lastArgs: Parameters<T> | null = null;

  return function (this: any, ...args: Parameters<T>): void {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
        if (lastArgs) {
          fn.apply(this, lastArgs);
          lastArgs = null;
        }
      }, limit);
    } else {
      lastArgs = args;
    }
  };
}

// 4. Debounce
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;

  return function (this: any, ...args: Parameters<T>): void {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// 5. Lazy evaluation
function lazy<T>(fn: () => T): () => T {
  let computed = false;
  let value: T;

  return function (): T {
    if (!computed) {
      value = fn();
      computed = true;
    }
    return value;
  };
}

const expensiveResult = lazy(() => {
  console.log("Computing...");
  return 42;
});

expensiveResult(); // "Computing..." → 42
expensiveResult(); // 42 (no computation)

// 6. Predicate builder
function createPredicate<T>(
  ...predicates: Array<(item: T) => boolean>
): (item: T) => boolean {
  return (item: T) => predicates.every((p) => p(item));
}

const isAdultAndActive = createPredicate(
  (user: User) => user.age >= 18,
  (user: User) => user.active === true
);
```

---

## Factory Functions

Creating objects with closures for private state.

```typescript
// Basic factory function
function createUser(name: string, email: string): {
  getName: () => string;
  getEmail: () => string;
  setEmail: (email: string) => void;
  toJSON: () => { name: string; email: string };
} {
  // Private state
  let _name = name;
  let _email = email;
  const _createdAt = new Date();

  return {
    getName: () => _name,
    getEmail: () => _email,
    setEmail: (newEmail: string) => {
      if (!newEmail.includes("@")) {
        throw new Error("Invalid email");
      }
      _email = newEmail;
    },
    toJSON: () => ({ name: _name, email: _email }),
  };
}

// Factory with validation
function createEmail(value: string): {
  get: () => string;
  toString: () => string;
  equals: (other: { get: () => string }) => boolean;
} {
  // Validate on creation
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    throw new Error(`Invalid email: ${value}`);
  }

  const normalized = value.toLowerCase();

  return {
    get: () => normalized,
    toString: () => normalized,
    equals: (other) => normalized === other.get(),
  };
}

// Factory with inheritance
function createAnimal(type: string, name: string): {
  getType: () => string;
  getName: () => string;
  speak: () => string;
} {
  const sounds: Record<string, string> = {
    dog: "Woof!",
    cat: "Meow!",
    bird: "Tweet!",
  };

  return {
    getType: () => type,
    getName: () => name,
    speak: () => sounds[type] ?? "...",
  };
}

// Generic factory
function createRepository<T extends { id: string }>(
  tableName: string
): {
  findById: (id: string) => T | undefined;
  findAll: () => T[];
  save: (entity: T) => T;
  delete: (id: string) => boolean;
} {
  let items: T[] = [];

  return {
    findById: (id) => items.find((item) => item.id === id),
    findAll: () => [...items],
    save: (entity) => {
      const index = items.findIndex((item) => item.id === entity.id);
      if (index >= 0) {
        items[index] = entity;
      } else {
        items.push(entity);
      }
      return entity;
    },
    delete: (id) => {
      const index = items.findIndex((item) => item.id === id);
      if (index >= 0) {
        items.splice(index, 1);
        return true;
      }
      return false;
    },
  };
}
```

---

## Module Pattern with Closures

Implementing the module pattern using closures.

```typescript
// Classic module pattern
const CalculatorModule = (function () {
  // Private state
  let result = 0;
  const history: string[] = [];

  // Private function
  function log(operation: string): void {
    history.push(`${operation} = ${result}`);
  }

  // Public API
  return {
    add(n: number): typeof CalculatorModule {
      result += n;
      log(`add(${n})`);
      return this;
    },
    subtract(n: number): typeof CalculatorModule {
      result -= n;
      log(`subtract(${n})`);
      return this;
    },
    getResult(): number {
      return result;
    },
    getHistory(): string[] {
      return [...history];
    },
    reset(): typeof CalculatorModule {
      result = 0;
      log("reset");
      return this;
    },
  };
})();

// Modern module pattern with closures
function createApp() {
  // Private state
  let state: AppState = {
    users: [],
    settings: {},
    currentPage: "home",
  };

  const listeners: Array<(state: AppState) => void> = [];

  // Private functions
  function notify(): void {
    listeners.forEach((listener) => listener(state));
  }

  function setState(updater: (prev: AppState) => AppState): void {
    state = updater(state);
    notify();
  }

  // Public API
  return {
    getState: () => ({ ...state }),

    subscribe(listener: (state: AppState) => void): () => void {
      listeners.push(listener);
      return () => {
        const index = listeners.indexOf(listener);
        if (index >= 0) listeners.splice(index, 1);
      };
    },

    navigate(page: string): void {
      setState((prev) => ({ ...prev, currentPage: page }));
    },

    addUser(user: User): void {
      setState((prev) => ({
        ...prev,
        users: [...prev.users, user],
      }));
    },
  };
}

// Revealing module pattern
const DataStore = (function () {
  // Private
  const data = new Map<string, unknown>();
  const indexes = new Map<string, Map<unknown, string[]>>();

  function addToIndex(collection: string, field: string, value: unknown, id: string): void {
    if (!indexes.has(collection)) {
      indexes.set(collection, new Map());
    }
    const collectionIndex = indexes.get(collection)!;
    if (!collectionIndex.has(value)) {
      collectionIndex.set(value, []);
    }
    collectionIndex.get(value)!.push(id);
  }

  // Public (revealed)
  return {
    put<T extends { id: string }>(collection: string, item: T): void {
      data.set(`${collection}:${item.id}`, item);
    },

    get<T>(collection: string, id: string): T | undefined {
      return data.get(`${collection}:${id}`) as T;
    },

    query<T>(collection: string, predicate: (item: T) => boolean): T[] {
      const results: T[] = [];
      data.forEach((value, key) => {
        if (key.startsWith(`${collection}:`) && predicate(value as T)) {
          results.push(value as T);
        }
      });
      return results;
    },
  };
})();
```

---

## Performance Considerations

```typescript
// Memory: Closures keep references to outer variables
function createHeavyClosure(): () => number {
  const largeArray = new Array(1000000).fill(0).map((_, i) => i);
  let index = 0;

  // This closure keeps 'largeArray' in memory
  return function (): number {
    return largeArray[index++ % largeArray.length];
  };
}

// Fix: Only capture what you need
function createLightClosure(): () => number {
  const length = 1000000;
  let index = 0;

  // Only 'length' and 'index' are captured, not the array
  return function (): number {
    return index++ % length;
  };
}

// Garbage collection: Closures prevent garbage collection
function problematic(): () => void {
  const hugeData = new Array(10000000).fill("data");

  return function (): void {
    // This function references hugeData, keeping it alive
    console.log(hugeData.length);
  };
}

// Fix: Release references
function improved(): () => void {
  let hugeData: string[] | null = new Array(10000000).fill("data");

  const fn = function (): void {
    console.log(hugeData?.length ?? 0);
  };

  hugeData = null; // Release reference

  return fn;
}

// Closure in hot paths
// BAD: Creating closures in tight loops
function processItems(items: Item[]): void {
  items.forEach((item) => {
    const processor = createProcessor(); // New closure each iteration
    processor(item);
  });
}

// GOOD: Reuse closures
function processItemsOptimized(items: Item[]): void {
  const processor = createProcessor(); // Created once
  items.forEach(processor);
}

// Memory leak with event listeners
function setupListeners(): () => void {
  const handler = () => console.log("clicked");

  document.addEventListener("click", handler);

  // Return cleanup function
  return () => {
    document.removeEventListener("click", handler);
  };
}

const cleanup = setupListeners();
// Later: cleanup(); // Prevents memory leak
```

---

## Best Practices

```typescript
// 1. Capture only what you need
// BAD
function createFn(): () => void {
  const hugeObject = getHugeObject();
  const smallValue = 42;

  return () => console.log(smallValue); // hugeObject is also captured!
}

// GOOD
function createFn(): () => void {
  const smallValue = 42;
  return () => console.log(smallValue);
}

// 2. Be careful with closures in loops
// BAD
const fns = [];
for (var i = 0; i < 10; i++) {
  fns.push(() => console.log(i)); // All log 10
}

// GOOD
const fns2 = [];
for (let i = 0; i < 10; i++) {
  fns2.push(() => console.log(i)); // Each logs correct value
}

// 3. Use WeakRef for large objects in closures
function createCache(): {
  get: (key: string) => unknown;
  set: (key: string, value: unknown) => void;
} {
  const cache = new Map<string, WeakRef<object>>();

  return {
    get: (key) => cache.get(key)?.deref() ?? null,
    set: (key, value) => {
      if (typeof value === "object" && value !== null) {
        cache.set(key, new WeakRef(value));
      }
    },
  };
}

// 4. Document closure behavior
/** Creates a counter that persists across calls.
 *  The returned function maintains its own private count. */
function createCounter(start: number = 0): () => number {
  let count = start;
  return () => ++count;
}

// 5. Clean up closures to prevent memory leaks
function createObservable<T>(): {
  subscribe: (fn: (value: T) => void) => () => void;
  emit: (value: T) => void;
} {
  const subscribers = new Set<(value: T) => void>();

  return {
    subscribe: (fn) => {
      subscribers.add(fn);
      return () => subscribers.delete(fn); // Cleanup function
    },
    emit: (value) => {
      subscribers.forEach((fn) => fn(value));
    },
  };
}
```

---

## Interview Questions

### Q1: What is a closure in TypeScript?

**Answer:** A closure is a function that captures and remembers variables from its enclosing lexical scope, even after the outer function has returned. Closures enable private state, function factories, and many functional programming patterns.

### Q2: How do closures handle the `var` vs `let` problem in loops?

**Answer:** `var` is function-scoped, so all closures in a loop share the same variable. `let` is block-scoped, creating a new binding for each iteration. Use `let` in loops to give each closure its own copy.

### Q3: What are common uses of closures?

**Answer:** Closures are used for: (1) private state encapsulation, (2) function factories, (3) memoization, (4) event handlers, (5) partial application, (6) module patterns, (7) callbacks with context.

### Q4: What are the performance implications of closures?

**Answer:** Closures keep references to captured variables, preventing garbage collection. Large objects captured by closures remain in memory as long as the closure exists. Only capture what you need and clean up when done.
