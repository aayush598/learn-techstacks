# Function Overloading in TypeScript

## Table of Contents

1. [Function Overload Syntax](#function-overload-syntax)
2. [Overload Signatures vs Implementation Signature](#overload-signatures-vs-implementation-signature)
3. [Overload Resolution](#overload-resolution)
4. [Overloads with Different Parameter Counts](#overloads-with-different-parameter-counts)
5. [Overloads with Type Predicates](#overloads-with-type-predicates)
6. [Overloads vs Union Types vs Generics](#overloads-vs-union-types-vs-generics)
7. [When to Use Overloading](#when-to-use-overloading)
8. [Overload Best Practices](#overload-best-practices)
9. [Advanced Overloading Patterns](#advanced-overloading-patterns)
10. [Interview Questions](#interview-questions)

---

## Function Overload Syntax

TypeScript function overloads allow a function to accept different types and numbers of arguments, returning different types based on the input.

```typescript
// Overload signatures (the public API)
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;
function format(value: string | number | Date): string {
  // Implementation signature (not visible to callers)
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  return value.toISOString();
}

console.log(format("hello"));        // "HELLO"
console.log(format(3.14159));        // "3.14"
console.log(format(new Date()));     // "2024-01-15T..."
```

### Basic Overload Examples

```typescript
// String or number conversion
function toNumber(value: string): number;
function toNumber(value: string, radix: number): number;
function toNumber(value: string, radix?: number): number {
  return Number(value, radix);
}

console.log(toNumber("42"));           // 42
console.log(toNumber("ff", 16));       // 255

// Array or single value
function toArray<T>(value: T): T[];
function toArray<T>(value: T[]): T[];
function toArray<T>(value: T | T[]): T[] {
  return Array.isArray(value) ? value : [value];
}

console.log(toArray("hello"));          // ["hello"]
console.log(toArray([1, 2, 3]));        // [1, 2, 3]

// Class constructor pattern
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: "input"): HTMLInputElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div = createElement("div");       // HTMLDivElement
const span = createElement("span");     // HTMLSpanElement
const input = createElement("input");   // HTMLInputElement
```

---

## Overload Signatures vs Implementation Signature

Understanding the distinction between overload signatures and the implementation.

```typescript
// These are OVERLOAD SIGNATURES (visible to callers)
function process(input: string): string;
function process(input: number): number;
function process(input: boolean): string;
// This is the IMPLEMENTATION SIGNATURE (hidden from callers)
function process(input: string | number | boolean): string | number {
  if (typeof input === "string") {
    return input.trim();
  }
  if (typeof input === "number") {
    return input * 2;
  }
  return input ? "yes" : "no";
}

// This works - matches overload signature
const result1 = process("hello");   // string
const result2 = process(42);        // number
const result3 = process(true);      // string

// This would NOT work if trying to call the implementation directly
// process({ key: "value" }); // Error: No matching overload

// Key rules:
// 1. Overload signatures are what callers see
// 2. Implementation signature is what TypeScript checks internally
// 3. Implementation signature must be compatible with ALL overloads
// 4. Callers cannot call the implementation signature directly
```

### Multiple Overload Signatures

```typescript
// Multiple overloads for different use cases
function createElement(
  tag: "div",
  attrs?: Record<string, string>
): HTMLDivElement;
function createElement(
  tag: "input",
  attrs?: { type?: string; value?: string }
): HTMLInputElement;
function createElement(
  tag: string,
  attrs?: Record<string, string>
): HTMLElement;
function createElement(
  tag: string,
  attrs?: Record<string, string>
): HTMLElement {
  const el = document.createElement(tag);
  if (attrs) {
    Object.entries(attrs).forEach(([key, value]) => {
      el.setAttribute(key, value);
    });
  }
  return el;
}

// TypeScript knows the exact return type
const div = createElement("div", { class: "container" });   // HTMLDivElement
const input = createElement("input", { type: "text" });     // HTMLInputElement
const unknown = createElement("p", { id: "para" });          // HTMLElement
```

---

## Overload Resolution

TypeScript resolves overloads from top to bottom, using the first matching signature.

```typescript
// Resolution order matters
function resolve(value: string): string;       // First overload
function resolve(value: number): number;       // Second overload
function resolve(value: unknown): unknown;     // Third overload (catch-all)
function resolve(value: unknown): unknown {
  return value;
}

// TypeScript tries overloads in order
const a = resolve("hello");  // string (matches first)
const b = resolve(42);       // number (matches second)
const c = resolve(true);     // unknown (matches third)

// Resolution with complex types
function search(query: string): string[];
function search(query: string, limit: number): string[];
function search(query: string, limit: number, offset: number): string[];
function search(
  query: string,
  limit?: number,
  offset?: number
): string[] {
  // Implementation
  return [];
}

// Resolution by argument count
search("hello");                  // string[] (1 arg)
search("hello", 10);              // string[] (2 args)
search("hello", 10, 20);          // string[] (3 args)

// Resolution by argument type
function getData(id: string): UserData;
function getData(id: number): UserData;
function getData(ids: string[]): UserData[];
function getData(ids: number[]): UserData[];
function getData(
  idOrIds: string | number | string[] | number[]
): UserData | UserData[] {
  // Implementation
  return {} as UserData;
}

const user1 = getData("abc");          // UserData
const user2 = getData(123);            // UserData
const users1 = getData(["a", "b"]);    // UserData[]
const users2 = getData([1, 2]);         // UserData[]
```

---

## Overloads with Different Parameter Counts

Handling functions that behave differently based on argument count.

```typescript
// Function with optional arguments via overloads
function createUrl(baseUrl: string): string;
function createUrl(baseUrl: string, path: string): string;
function createUrl(baseUrl: string, path: string, params: Record<string, string>): string;
function createUrl(
  baseUrl: string,
  path?: string,
  params?: Record<string, string>
): string {
  let url = baseUrl;
  if (path) {
    url += path.startsWith("/") ? path : `/${path}`;
  }
  if (params) {
    const queryString = Object.entries(params)
      .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
      .join("&");
    url += `?${queryString}`;
  }
  return url;
}

console.log(createUrl("https://api.com"));                           // "https://api.com"
console.log(createUrl("https://api.com", "/users"));                 // "https://api.com/users"
console.log(createUrl("https://api.com", "/users", { page: "1" })); // "https://api.com/users?page=1"

// Function that returns different types based on argument count
function parse(input: string): ParsedResult;
function parse(input: string, strict: boolean): StrictParsedResult;
function parse(input: string, strict?: boolean): ParsedResult | StrictParsedResult {
  if (strict) {
    return { valid: true, data: input, strict: true } as StrictParsedResult;
  }
  return { valid: true, data: input } as ParsedResult;
}

interface ParsedResult {
  valid: boolean;
  data: string;
}

interface StrictParsedResult extends ParsedResult {
  strict: boolean;
}

const result1 = parse("hello");          // ParsedResult
const result2 = parse("hello", true);   // StrictParsedResult
```

### Overloads with Rest Parameters

```typescript
// Overloads with rest parameters
function sum(...values: number[]): number;
function sum(...values: string[]): number;
function sum(...values: (number | string)[]): number {
  return values.reduce((total, value) => {
    if (typeof value === "string") {
      return total + parseFloat(value);
    }
    return total + value;
  }, 0);
}

console.log(sum(1, 2, 3));           // 6
console.log(sum("1.5", "2.5"));     // 4
console.log(sum(1, "2.5", 3));      // 6.5
```

---

## Overloads with Type Predicates

Using type predicates in overloads for better type narrowing.

```typescript
// Type predicate overloads
function filter(items: (string | number)[], predicate: (item: string) => boolean): string[];
function filter(items: (string | number)[], predicate: (item: number) => boolean): number[];
function filter<T>(
  items: T[],
  predicate: (item: T) => boolean
): T[] {
  return items.filter(predicate);
}

const numbers = filter([1, "hello", 2, "world", 3], (item) => item > 1);
// numbers: number[]

const strings = filter([1, "hello", 2, "world", 3], (item) => item.startsWith("h"));
// strings: string[]

// Discriminated union overloads
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: { kind: "circle"; radius: number }): number;
function area(shape: { kind: "rectangle"; width: number; height: number }): number;
function area(shape: { kind: "triangle"; base: number; height: number }): number;
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

console.log(area({ kind: "circle", radius: 5 }));         // 78.54
console.log(area({ kind: "rectangle", width: 4, height: 6 })); // 24
console.log(area({ kind: "triangle", base: 4, height: 6 }));   // 12
```

---

## Overloads vs Union Types vs Generics

Understanding when to use each approach.

```typescript
// APPROACH 1: Union types (simple, less type-safe)
function processUnion(input: string | number): string | number {
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  return input.toFixed(2);
}

// Problem: return type is always string | number
const result1 = processUnion("hello"); // string | number (not narrowed)

// APPROACH 2: Overloads (more type-safe, more verbose)
function processOverload(input: string): string;
function processOverload(input: number): number;
function processOverload(input: string | number): string | number {
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  return input.toFixed(2);
}

// Better: return type is narrowed
const result2 = processOverload("hello"); // string (not string | number)
const result3 = processOverload(42);      // number (not string | number)

// APPROACH 3: Generics (most flexible, sometimes complex)
function processGeneric<T extends string | number>(input: T): T {
  if (typeof input === "string") {
    return input.toUpperCase() as T;
  }
  return input.toFixed(2) as T;
}

// Also narrowed, but may need type assertions
const result4 = processGeneric("hello"); // string
const result5 = processGeneric(42);      // number

// When to use which:
// - Union types: Simple cases where return type doesn't depend on input type
// - Overloads: Complex cases where different inputs produce different outputs
// - Generics: When the relationship between input and output types is consistent
```

### Decision Matrix

```typescript
// Use UNION TYPES when:
// - Simple parameter types
// - Return type is the same regardless of input
function format(input: string | number): string {
  return String(input);
}

// Use OVERLOADS when:
// - Different parameter types produce different return types
// - Different parameter counts produce different return types
// - You need type-safe discriminated behavior
function parseJson(input: string): unknown;
function parseJson<T>(input: string, schema: Schema<T>): T;
function parseJson(input: string, schema?: Schema<unknown>): unknown {
  // Implementation
}

// Use GENERICS when:
// - Input and output types are related
// - You want to preserve type information through transformations
function wrap<T>(value: T): { value: T; timestamp: Date } {
  return { value, timestamp: new Date() };
}

// Use TYPE PREDICATES when:
// - You need to narrow union types based on runtime checks
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

---

## When to Use Overloading

```typescript
// USE OVERLOADS: Different return types based on input
function createRoute(path: string): Route;
function createRoute(path: string, options: RouteOptions): RouteWithMiddleware;
function createRoute(
  path: string,
  options?: RouteOptions
): Route | RouteWithMiddleware {
  if (options) {
    return { path, ...options, hasMiddleware: true } as RouteWithMiddleware;
  }
  return { path } as Route;
}

// USE OVERLOADS: API design for convenience
function fetch(url: string): Promise<Response>;
function fetch(url: string, init: RequestInit): Promise<Response>;
function fetch(url: string, init?: RequestInit): Promise<Response> {
  return window.fetch(url, init);
}

// USE OVERLOADS: When you want compile-time type safety
function divide(a: number, b: number): number;
function divide(a: number, b: number, precision: number): number;
function divide(a: number, b: number, precision?: number): number {
  const result = a / b;
  if (precision !== undefined) {
    return parseFloat(result.toFixed(precision));
  }
  return result;
}

// DON'T use overloads: When generics work fine
// BAD
function identityString(input: string): string;
function identityNumber(input: number): number;
function identity(input: string | number): string | number {
  return input;
}

// GOOD
function identity<T>(input: T): T {
  return input;
}
```

---

## Overload Best Practices

```typescript
// 1. Order overloads from most specific to least specific
function process(value: string): string;           // Most specific
function process(value: number): number;           // Less specific
function process(value: unknown): unknown;         // Least specific
function process(value: unknown): unknown {
  return value;
}

// 2. Keep overloads related - don't mix unrelated functionality
// BAD
function doSomething(input: string): string;
function doSomething(input: number): number;
function doSomething(input: boolean): void;  // Different behavior!
function doSomething(input: string | number | boolean) { /* ... */ }

// GOOD - consistent behavior
function format(input: string): string;
function format(input: number): string;
function format(input: Date): string;
function format(input: string | number | Date): string {
  return String(input);
}

// 3. Document overload behavior
/**
 * Parses a JSON string.
 * @param input - The JSON string to parse
 * @returns The parsed value
 */
function parseJson(input: string): unknown;
/**
 * Parses a JSON string with a schema validator.
 * @param input - The JSON string to parse
 * @param schema - The schema to validate against
 * @returns The validated, typed value
 */
function parseJson<T>(input: string, schema: Schema<T>): T;
function parseJson(input: string, schema?: Schema<unknown>): unknown {
  const parsed = JSON.parse(input);
  if (schema) {
    return schema.validate(parsed);
  }
  return parsed;
}

// 4. Use overloads sparingly - consider alternatives first
// 5. Make sure the implementation covers all overload signatures
// 6. Test all overload paths
```

---

## Advanced Overloading Patterns

```typescript
// Curried function overloads
function curry<A, R>(fn: (a: A) => R): (a: A) => R;
function curry<A, B, R>(fn: (a: A, b: B) => R): (a: A) => (b: B) => R;
function curry<A, B, C, R>(
  fn: (a: A, b: B, c: C) => R
): (a: A) => (b: B) => (c: C) => R;
function curry(fn: Function) {
  const arity = fn.length;
  return function curried(...args: unknown[]) {
    if (args.length >= arity) {
      return fn(...args);
    }
    return (...moreArgs: unknown[]) => curried(...args, ...moreArgs);
  };
}

// Builder pattern with overloads
class QueryBuilder {
  select(...columns: string[]): this;
  select<T>(columns: T[]): this;
  select(...columns: string[] | string[][]): this {
    // Implementation
    return this;
  }

  where(condition: string): this;
  where(condition: string, value: unknown): this;
  where(condition: string, value?: unknown): this {
    // Implementation
    return this;
  }
}

// Method overloads in classes
class DataStore {
  get(key: string): unknown;
  get<T>(key: string, type: new (...args: unknown[]) => T): T;
  get<T>(key: string, type?: new (...args: unknown[]) => T): unknown | T {
    const value = this._retrieve(key);
    if (type) {
      return new type(value);
    }
    return value;
  }

  private _retrieve(key: string): unknown {
    // Implementation
    return null;
  }
}

// Conditional overloads
function processArray<T>(arr: T[]): T[];
function processArray<T, U>(arr: T[], mapper: (item: T) => U): U[];
function processArray<T, U>(
  arr: T[],
  mapper?: (item: T) => U
): T[] | U[] {
  if (mapper) {
    return arr.map(mapper);
  }
  return arr;
}

const nums = processArray([1, 2, 3]);                    // number[]
const strs = processArray([1, 2, 3], (n) => n.toString()); // string[]
```

---

## Interview Questions

### Q1: What is function overloading in TypeScript?

**Answer:** Function overloading allows a single function to have multiple signatures with different parameter types and return types. TypeScript resolves which signature to use based on the arguments passed at the call site.

### Q2: What is the difference between overload signatures and the implementation signature?

**Answer:** Overload signatures define the public API that callers see. The implementation signature is hidden from callers and must be compatible with all overload signatures. Callers can only use the overload signatures.

### Q3: When should you use overloads vs union types vs generics?

**Answer:** Use union types for simple cases with the same return type. Use overloads when different inputs produce different output types. Use generics when the relationship between input and output types is consistent and predictable.

### Q4: Can you overload arrow functions?

**Answer:** No, you cannot directly overload arrow functions. You must use function declarations or function expressions. However, you can type a variable with overloaded function types.

```typescript
type Formatter = {
  (input: string): string;
  (input: number): string;
};

const format: Formatter = (input: string | number): string => {
  return String(input);
};
```
