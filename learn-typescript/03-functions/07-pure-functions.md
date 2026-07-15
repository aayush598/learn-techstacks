# Pure Functions in TypeScript

## Table of Contents

1. [What Are Pure Functions](#what-are-pure-functions)
2. [Referential Transparency](#referential-transparency)
3. [Side Effects](#side-effects)
4. [Immutability](#immutability)
5. [Testing Pure Functions](#testing-pure-functions)
6. [Functional Programming in TypeScript](#functional-programming-in-typescript)
7. [Pipe/Compose with Pure Functions](#pipecompose-with-pure-functions)
8. [Performance Implications](#performance-implications)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## What Are Pure Functions

A pure function satisfies two conditions: (1) always returns the same output for the same input, and (2) has no side effects.

```typescript
// PURE: Deterministic, no side effects
function add(a: number, b: number): number {
  return a + b;
}

// IMPURE: Modifies external state
let total = 0;
function addToTotal(value: number): number {
  total += value;
  return total;
}

// PURE: No external state dependency
function calculateArea(radius: number): number {
  return Math.PI * radius ** 2;
}

// IMPURE: Depends on external variable
let taxRate = 0.1;
function calculateTax(amount: number): number {
  return amount * taxRate;
}

// PURE: Creates new data instead of modifying
function addUser(users: User[], newUser: User): User[] {
  return [...users, newUser];
}

// IMPURE: Modifies input
function addUserImpure(users: User[], newUser: User): void {
  users.push(newUser);
}
```

### More Pure Function Examples

```typescript
// String manipulation
function toUpperCase(str: string): string {
  return str.toUpperCase();
}

// Array operations
function head<T>(arr: T[]): T | undefined {
  return arr[0];
}

function tail<T>(arr: T[]): T[] {
  return arr.slice(1);
}

function flatten<T>(arr: T[][]): T[] {
  return arr.reduce((acc, val) => acc.concat(val), []);
}

// Object operations
function mergeObjects<A, B>(a: A, b: B): A & B {
  return { ...a, ...b };
}

function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  return keys.reduce((result, key) => {
    result[key] = obj[key];
    return result;
  }, {} as Pick<T, K>);
}

// Math operations
function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function lerp(start: number, end: number, t: number): number {
  return start + (end - start) * clamp(t, 0, 1);
}
```

---

## Referential Transparency

A function is referentially transparent if it can be replaced with its output value without changing program behavior.

```typescript
// Referentially transparent
function square(x: number): number {
  return x * x;
}

// These are equivalent:
const a = square(5) + square(3);
const b = 25 + 9; // a === b (both are 34)

// NOT referentially transparent
let counter = 0;
function increment(): number {
  return ++counter;
}

// increment() !== increment() (different values each call)

// Memoized function (still referentially transparent)
function memoizedFibonacci(n: number): number {
  const cache = new Map<number, number>();

  function fib(n: number): number {
    if (n <= 1) return n;
    if (cache.has(n)) return cache.get(n)!;
    const result = fib(n - 1) + fib(n - 2);
    cache.set(n, result);
    return result;
  }

  return fib(n);
}

// Can be replaced with its value anywhere
const fib10 = memoizedFibonacci(10); // 55
// Anywhere we use memoizedFibonacci(10), we could use 55
```

---

## Side Effects

Side effects occur when a function modifies external state or interacts with the outside world.

```typescript
// Common side effects:
// 1. Modifying global variables
// 2. Modifying function parameters
// 3. Console output / logging
// 4. Network requests
// 5. DOM manipulation
// 6. Database operations
// 7. Writing files
// 8. Generating random numbers
// 9. Getting current time

// Containing side effects at the boundary
// Keep pure functions in the core, push side effects to edges

// PURE core
function validateUser(data: unknown): UserData {
  return validatedData;
}

function prepareUserForStorage(validated: UserData): UserRecord {
  return { ...validated, createdAt: new Date() };
}

// IMPURE boundary
async function createUserHandler(data: unknown): Promise<User> {
  const validated = validateUser(data);
  const record = prepareUserForStorage(validated);
  await saveUser(record);
  return record;
}
```

### Managing Side Effects

```typescript
// Pattern: Return side effects instead of executing them
type SideEffect = () => void;

function processOrder(
  order: Order
): { result: OrderResult; effects: SideEffect[] } {
  const effects: SideEffect[] = [];
  const validated = validateOrder(order);
  const calculated = calculateTotals(validated);

  effects.push(() => sendConfirmationEmail(calculated));
  effects.push(() => updateInventory(calculated.items));
  effects.push(() => logTransaction(calculated));

  return { result: calculated, effects };
}

// Execute effects at the boundary
const { result, effects } = processOrder(order);
effects.forEach((effect) => effect());
```

---

## Immutability

Working with immutable data structures and operations.

```typescript
// Immutable object operations
function updateUser(user: User, updates: Partial<User>): User {
  return { ...user, ...updates };
}

// Immutable array operations
function append<T>(arr: T[], item: T): T[] {
  return [...arr, item];
}

function remove<T>(arr: T[], predicate: (item: T) => boolean): T[] {
  return arr.filter((item) => !predicate(item));
}

function replace<T>(
  arr: T[],
  predicate: (item: T) => boolean,
  updater: (item: T) => T
): T[] {
  return arr.map((item) => (predicate(item) ? updater(item) : item));
}

// Readonly types for immutability
interface ImmutableUser {
  readonly id: string;
  readonly name: string;
  readonly email: string;
  readonly settings: Readonly<{
    theme: "light" | "dark";
    notifications: boolean;
  }>;
}

// Deep readonly utility type
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Immutable state management with reducer pattern
interface State {
  readonly users: readonly User[];
  readonly selectedUserId: string | null;
  readonly loading: boolean;
}

type Action =
  | { type: "ADD_USER"; payload: User }
  | { type: "SELECT_USER"; payload: string }
  | { type: "SET_LOADING"; payload: boolean };

function stateReducer(state: State, action: Action): State {
  switch (action.type) {
    case "ADD_USER":
      return { ...state, users: [...state.users, action.payload] };
    case "SELECT_USER":
      return { ...state, selectedUserId: action.payload };
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}
```

---

## Testing Pure Functions

Pure functions are easy to test because they have no dependencies.

```typescript
function calculateDiscount(price: number, discountPercent: number): number {
  return price * (1 - discountPercent / 100);
}

describe("calculateDiscount", () => {
  it("should calculate 10% discount correctly", () => {
    expect(calculateDiscount(100, 10)).toBe(90);
  });

  it("should handle 0% discount", () => {
    expect(calculateDiscount(100, 0)).toBe(100);
  });

  it("should handle 100% discount", () => {
    expect(calculateDiscount(100, 100)).toBe(0);
  });
});

// Testing pure functions with complex inputs
function processItems(
  items: Array<{ name: string; price: number; quantity: number }>
): { total: number; itemCount: number; averagePrice: number } {
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);
  return { total, itemCount, averagePrice: itemCount > 0 ? total / itemCount : 0 };
}

describe("processItems", () => {
  it("should calculate totals correctly", () => {
    const items = [
      { name: "A", price: 10, quantity: 2 },
      { name: "B", price: 20, quantity: 1 },
    ];
    expect(processItems(items)).toEqual({ total: 40, itemCount: 3, averagePrice: 40 / 3 });
  });

  it("should handle empty array", () => {
    expect(processItems([])).toEqual({ total: 0, itemCount: 0, averagePrice: 0 });
  });
});
```

---

## Functional Programming in TypeScript

Using TypeScript's type system to support functional programming patterns.

```typescript
// Type aliases for common function signatures
type Predicate<T> = (item: T) => boolean;
type Transformer<T, U> = (item: T) => U;
type Reducer<T, U> = (acc: U, item: T) => U;

// Function composition
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
  return (a) => f(g(a));
}

// Map, filter, reduce as standalone functions
function map<T, U>(arr: T[], fn: Transformer<T, U>): U[] {
  return arr.map(fn);
}

function filter<T>(arr: T[], predicate: Predicate<T>): T[] {
  return arr.filter(predicate);
}

function reduce<T, U>(arr: T[], reducer: Reducer<T, U>, initial: U): U {
  return arr.reduce(reducer, initial);
}

// Option type for null safety
type Option<T> = { type: "some"; value: T } | { type: "none" };

function some<T>(value: T): Option<T> {
  return { type: "some", value };
}

function none<T>(): Option<T> {
  return { type: "none" };
}

function mapOption<T, U>(opt: Option<T>, fn: (value: T) => U): Option<U> {
  return opt.type === "some" ? some(fn(opt.value)) : none();
}

function flatMapOption<T, U>(opt: Option<T>, fn: (value: T) => Option<U>): Option<U> {
  return opt.type === "some" ? fn(opt.value) : none();
}

// Either type for error handling
type Either<L, R> = { type: "left"; left: L } | { type: "right"; right: R };

function left<L, R>(l: L): Either<L, R> {
  return { type: "left", left: l };
}

function right<L, R>(r: R): Either<L, R> {
  return { type: "right", right: r };
}

function mapEither<L, R, U>(either: Either<L, R>, fn: (r: R) => U): Either<L, U> {
  return either.type === "right" ? right(fn(either.right)) : either;
}
```

---

## Pipe/Compose with Pure Functions

```typescript
// Pipe (left to right)
function pipe<A, B>(f1: (a: A) => B): (a: A) => B;
function pipe<A, B, C>(f1: (a: A) => B, f2: (b: B) => C): (a: A) => C;
function pipe<A, B, C, D>(f1: (a: A) => B, f2: (b: B) => C, f3: (c: C) => D): (a: A) => D;
function pipe(...fns: Array<(arg: any) => any>): (arg: any) => any {
  return (arg) => fns.reduce((result, fn) => fn(result), arg);
}

// Compose (right to left)
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
  return (a) => f(g(a));
}

// Practical pipeline with pure functions
const trim = (s: string) => s.trim();
const toLowerCase = (s: string) => s.toLowerCase();
const replaceSpaces = (s: string) => s.replace(/\s+/g, "_");
const wrap = (s: string) => `[${s}]`;

const processString = pipe(trim, toLowerCase, replaceSpaces, wrap);
console.log(processString("  Hello World  ")); // "[hello_world]"

// Data transformation pipeline
const users = [
  { name: "  Alice  ", age: 30, active: true },
  { name: "  Bob  ", age: 25, active: false },
  { name: "  Charlie  ", age: 35, active: true },
];

const getActiveNames = pipe(
  (users: typeof users) => users.filter((u) => u.active),
  (active) => active.map((u) => u.name.trim()),
  (names) => names.join(", ")
);
```

---

## Performance Implications

```typescript
// Pure functions enable memoization
function expensiveCalculation(n: number): number {
  console.log("Computing...");
  return n ** 2 + Math.sqrt(n);
}

// Memoize pure functions for performance
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();
  return ((...args: any[]) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

const memoizedCalc = memoize(expensiveCalculation);

// Immutable operations can be slower due to copying
// But they enable safe concurrent access and easier debugging

// Structured sharing: only copy what changed
function updateNested(state: State, path: string[], value: unknown): State {
  if (path.length === 0) return value as State;
  const [head, ...rest] = path;
  return {
    ...state,
    [head]: updateNested((state as any)[head] ?? {}, rest, value),
  };
}

// Performance tips:
// 1. Memoize expensive pure functions
// 2. Use readonly arrays for small datasets
// 3. Consider Immer for complex immutable updates
// 4. Profile before optimizing - purity benefits often outweigh costs
```

---

## Best Practices

```typescript
// 1. Keep core logic pure, push side effects to boundaries
function processOrder(order: Order): OrderResult {
  // Pure logic
  const validated = validateOrder(order);
  const totals = calculateTotals(validated);
  return totals;
}

// 2. Use readonly types to enforce immutability
function sort(items: readonly number[]): number[] {
  return [...items].sort((a, b) => a - b);
}

// 3. Return new objects instead of mutating
function updateSettings(
  settings: Settings,
  updates: Partial<Settings>
): Settings {
  return { ...settings, ...updates };
}

// 4. Avoid Date.now(), Math.random(), new Date() in pure functions
// Pass them as parameters instead
function createEntry(
  data: EntryData,
  now: Date = new Date()
): Entry {
  return { ...data, createdAt: now };
}

// 5. Use function composition for complex transformations
const processUser = pipe(
  validateInput,
  normalizeData,
  enrichWithDefaults,
  formatOutput
);
```

---

## Interview Questions

### Q1: What makes a function "pure"?

**Answer:** A function is pure if (1) it always returns the same output for the same input (deterministic), and (2) it produces no side effects (no modifying external state, no I/O).

### Q2: What is referential transparency?

**Answer:** Referential transparency means a function call can be replaced with its return value without changing program behavior. All pure functions are referentially transparent.

### Q3: Why are pure functions easier to test?

**Answer:** Pure functions require no mocking, no setup, no teardown. You simply provide inputs and assert outputs. No need to reset state between tests.

### Q4: What are the performance tradeoffs of pure functions?

**Answer:** Pure functions may create more objects (memory pressure) but enable memoization, parallel execution, and easier debugging. For most applications, the benefits outweigh the costs.
