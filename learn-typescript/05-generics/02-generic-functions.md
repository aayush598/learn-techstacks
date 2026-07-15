# 02 — Generic Functions

## Table of Contents

1. [Generic Function Syntax](#generic-function-syntax)
2. [Type Inference in Generic Functions](#type-inference)
3. [Generic Constraints in Functions](#generic-constraints-in-functions)
4. [Default Type Parameters in Functions](#default-type-parameters)
5. [Generic Arrow Functions](#generic-arrow-functions)
6. [Generic Async Functions](#generic-async-functions)
7. [Generic Overloaded Functions](#generic-overloaded-functions)
8. [Real-World Generic Function Examples](#real-world-examples)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Generic Function Syntax

Generic functions declare type parameters **before** the parameter list, enclosed in
angle brackets `< >`.

### Function Declaration

```typescript
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const num = first([10, 20, 30]);     // number
const str = first(["a", "b"]);       // string
const empty = first([]);              // undefined
```

### Function Expression

```typescript
const first = function <T>(items: T[]): T | undefined {
  return items[0];
};
```

### Type Argument Required

Sometimes TypeScript cannot infer the type. Provide it explicitly:

```typescript
function create<T>(): T {
  // Implementation depends on runtime logic
  return JSON.parse("{}") as T;
}

// TypeScript cannot infer T — you must provide it
const obj = create<User>();
// Without <User>, T would be inferred as {}
```

---

## Type Inference

TypeScript infers `T` from the **argument types** at the call site. This is called
**type argument inference**.

### Inference from Arguments

```typescript
function wrap<T>(value: T): { value: T } {
  return { value };
}

// T inferred as number
const a = wrap(42);           // { value: number }

// T inferred as string
const b = wrap("hello");     // { value: string }

// T inferred as boolean[]
const c = wrap([true, false]); // { value: boolean[] }
```

### Inference from Multiple Arguments

When multiple arguments use `T`, TypeScript finds the **best common type**:

```typescript
function pair<T>(a: T, b: T): [T, T] {
  return [a, b];
}

// T = string (both are strings)
const p1 = pair("hello", "world");

// T = string | number (best common type)
const p2 = pair("hello", 42);
```

### Inference from Return Type Context

```typescript
function createArray<T>(item: T, count: number): T[] {
  return Array(count).fill(item);
}

// TypeScript infers T from the expected return type context
const arr: string[] = createArray("x", 5); // T = string
```

### Inference from Callbacks

```typescript
function transform<T, R>(items: T[], fn: (item: T) => R): R[] {
  return items.map(fn);
}

// T inferred from array, R inferred from callback return
const lengths = transform(["hello", "world"], (s) => s.length);
// T = string, R = number
```

### When Inference Produces a Union

```typescript
function concatenate<T>(a: T, b: T): T[] {
  return [a, b];
}

// T = string | number (union, not what you might want)
const result = concatenate("hello", 42);
// result: (string | number)[]

// Fix: use two type parameters for independent types
function concatenate2<T, U>(a: T, b: U): [T, U] {
  return [a, b];
}
const result2 = concatenate2("hello", 42);
// result2: [string, number]
```

---

## Generic Constraints in Functions

Constraints restrict what types `T` can be using the `extends` keyword.

### Basic Constraint

```typescript
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(value: T): void {
  console.log(`Length: ${value.length}`);
}

logLength("hello");       // ✅ string has .length
logLength([1, 2, 3]);     // ✅ array has .length
logLength({ length: 10 }); // ✅ matches HasLength
// logLength(42);          // ❌ number has no .length
```

### keyof Constraint

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };

getProperty(user, "name");  // ✅ string
getProperty(user, "age");   // ✅ number
// getProperty(user, "email"); // ❌ "email" not in keyof User
```

### Constraint to Specific Types

```typescript
function processArray<T extends number[]>(items: T): number {
  return items.reduce((sum, n) => sum + n, 0);
}

processArray([1, 2, 3]);     // ✅ 6
// processArray(["a", "b"]); // ❌ string[] not assignable to number[]
```

---

## Default Type Parameters

Default type parameters provide a fallback when no type argument is given and inference
fails.

```typescript
function createState<T = string>(initial?: T): T {
  return (initial ?? "default") as T;
}

const a = createState();           // T = string (default)
const b = createState(42);        // T = number (inferred)
const c = createState<boolean>();  // T = boolean (explicit)
```

### Defaults with Constraints

```typescript
function fetchData<T extends object = Record<string, unknown>>(
  url: string
): Promise<T> {
  return fetch(url).then((r) => r.json()) as Promise<T>;
}

// Uses default Record<string, unknown>
const data1 = await fetchData("/api/data");

// Uses specific type
const data2 = await fetchData<User[]>("/api/users");
```

---

## Generic Arrow Functions

Arrow functions support generics but require special syntax in `.tsx` files.

### Basic Syntax

```typescript
const identity = <T>(value: T): T => value;

const first = <T>(items: T[]): T | undefined => items[0];
```

### The `.tsx` Problem

In `.tsx` files, `<T>` is parsed as a JSX tag:

```typescript
// ❌ Parse error in .tsx files
const identity = <T>(value: T): T => value;

// ✅ Fix 1: trailing comma
const identity = <T,>(value: T): T => value;

// ✅ Fix 2: explicit constraint
const identity = <T extends unknown>(value: T): T => value;
```

### Arrow with Multiple Type Parameters

```typescript
const map = <TInput, TOutput>(
  items: TInput[],
  fn: (item: TInput) => TOutput
): TOutput[] => items.map(fn);

const lengths = map(["a", "bb"], (s) => s.length);
// lengths: number[]
```

---

## Generic Async Functions

Generics work seamlessly with `async` functions and Promises.

```typescript
async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
}

const user = await fetchJson<User>("/api/users/1");
// user.id: number, user.name: string

const users = await fetchJson<User[]>("/api/users");
// users: User[]
```

### Generic with Error Handling

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeFetch<T>(
  url: string
): Promise<Result<T>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return { ok: false, error: new Error(`HTTP ${response.status}`) };
    }
    const data = await response.json();
    return { ok: true, value: data as T };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}

const result = await safeFetch<User>("/api/users/1");
if (result.ok) {
  console.log(result.value.name);  // TypeScript knows value exists
} else {
  console.error(result.error.message); // TypeScript knows error exists
}
```

### Generic with Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e as Error;
      if (attempt < maxRetries) {
        await new Promise((resolve) => setTimeout(resolve, delay * (attempt + 1)));
      }
    }
  }

  throw lastError;
}

const data = await withRetry(() => fetchJson<User>("/api/users/1"), 3, 500);
```

---

## Generic Overloaded Functions

Overloads allow a function to have **multiple generic signatures** with different type
constraints and return types.

### Basic Overload

```typescript
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: "input"): HTMLInputElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div = createElement("div");    // HTMLDivElement
const span = createElement("span");  // HTMLSpanElement
```

### Generic Overloads

```typescript
function parse<T extends "json" | "text">(
  format: T,
  data: string
): T extends "json" ? unknown : string;
function parse(format: "json" | "text", data: string): unknown | string {
  if (format === "json") {
    return JSON.parse(data);
  }
  return data;
}

const obj = parse("json", '{"key": "value"}');  // unknown
const text = parse("text", "hello");            // string
```

### Overloads vs Union Parameters

```typescript
// ❌ Overly broad return type
function process(value: string | number): string | number {
  if (typeof value === "string") return value.toUpperCase();
  return value * 2;
}

// ✅ Overloaded: precise return type
function process(value: string): string;
function process(value: number): number;
function process(value: string | number): string | number {
  if (typeof value === "string") return value.toUpperCase();
  return value * 2;
}

const a = process("hello");  // string (not string | number)
const b = process(42);       // number (not string | number)
```

---

## Real-World Examples

### Debounce Function

```typescript
function debounce<TArgs extends unknown[]>(
  fn: (...args: TArgs) => void,
  delay: number
): (...args: TArgs) => void {
  let timeoutId: ReturnType<typeof setTimeout> | undefined;

  return (...args: TArgs) => {
    if (timeoutId !== undefined) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const debouncedSearch = debounce((query: string, page: number) => {
  console.log(`Searching: ${query}, page ${page}`);
}, 300);

debouncedSearch("hello", 1);  // ✅ types enforced
// debouncedSearch(42, "1");  // ❌ wrong types
```

### Deep Partial

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

function deepMerge<T extends object>(
  target: T,
  source: DeepPartial<T>
): T {
  const result = { ...target };
  for (const key in source) {
    if (
      source[key] !== undefined &&
      typeof source[key] === "object" &&
      source[key] !== null
    ) {
      (result as any)[key] = deepMerge(
        (target as any)[key] ?? {},
        (source as any)[key]
      );
    } else {
      (result as any)[key] = source[key];
    }
  }
  return result;
}
```

### Type-Safe Event Emitter

```typescript
type EventMap = {
  connect: { userId: string };
  disconnect: { userId: string; reason: string };
  message: { from: string; text: string };
};

function createEmitter<TEvents extends Record<string, unknown>>() {
  const listeners = new Map<string, Set<Function>>();

  return {
    on<K extends keyof TEvents>(
      event: K,
      listener: (payload: TEvents[K]) => void
    ): void {
      if (!listeners.has(event as string)) {
        listeners.set(event as string, new Set());
      }
      listeners.get(event as string)!.add(listener);
    },

    emit<K extends keyof TEvents>(event: K, payload: TEvents[K]): void {
      listeners.get(event as string)?.forEach((fn) => fn(payload));
    },
  };
}

const emitter = createEmitter<EventMap>();

emitter.on("message", (payload) => {
  console.log(payload.from, payload.text); // ✅ typed
});

emitter.emit("connect", { userId: "123" });       // ✅ typed
// emitter.emit("connect", { userId: 123 });       // ❌ userId must be string
// emitter.emit("unknown", {});                     // ❌ "unknown" not in EventMap
```

### Paginated API Fetcher

```typescript
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

async function fetchPaginated<T>(
  url: string,
  page: number = 1,
  pageSize: number = 20
): Promise<PaginatedResponse<T>> {
  const params = new URLSearchParams({
    page: String(page),
    pageSize: String(pageSize),
  });

  const response = await fetch(`${url}?${params}`);
  return response.json() as Promise<PaginatedResponse<T>>;
}

interface Product {
  id: string;
  name: string;
  price: number;
}

const products = await fetchPaginated<Product>("/api/products", 1, 10);
console.log(products.data[0].name); // ✅ string
console.log(products.hasMore);      // ✅ boolean
```

---

## Best Practices

1. **Let TypeScript infer** — only provide type arguments when inference fails or is
   wrong.
2. **Constrain generics** — if the function only works with certain shapes, add
   `extends`.
3. **Prefer overloads for narrow cases** — when you need different return types per
   input type.
4. **Use callbacks for type flow** — generic callbacks help TypeScript infer the right
   types.
5. **Keep type parameter count low** — 1-2 is ideal; 3 is the maximum before refactoring.
6. **Document complex signatures** — generic signatures can produce confusing error
   messages; JSDoc helps.

---

## Interview Questions

**Q1: How does TypeScript infer generic types in functions?**

TypeScript infers type parameters from the types of arguments passed at the call site.
It uses contextual typing from callbacks, expected return types, and multiple argument
types to determine the best type.

**Q2: What happens when two arguments use the same type parameter?**

TypeScript finds the **best common type** — typically a union. If you want independent
types, use separate type parameters.

**Q3: How do generic constraints work?**

The `extends` keyword restricts `T` to types that satisfy a given interface or shape.
For example, `<T extends { length: number }>` ensures `T` has a `length` property.

**Q4: Can you use generics in arrow functions?**

Yes, but in `.tsx` files the `<T>` syntax conflicts with JSX. Use a trailing comma
(`<T,>`) or explicit constraint (`<T extends unknown>`) as a workaround.

**Q5: When should you use overloads vs generics?**

Use generics when the function is **type-polymorphic** — it works with any type that
meets a constraint. Use overloads when different input types produce **different return
types** and you need precise control.
