# Nullish Coalescing in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [?? Operator](#-operator)
3. [?? vs ||](#-vs-)
4. [Nullish Coalescing Assignment (??=)](#nullish-coalescing-assignment-)
5. [Interaction with Optional Chaining](#interaction-with-optional-chaining)
6. [Short-Circuit Evaluation](#short-circuit-evaluation)
7. [When to Use ?? vs ||](#when-to-use--vs-)
8. [Common Patterns](#common-patterns)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Overview

The nullish coalescing operator (`??`) is an ECMAScript 2020 feature that provides a default value when the left-hand side is `null` or `undefined`.

```typescript
// Basic usage
const value = null ?? "default"; // "default"
const value2 = undefined ?? "default"; // "default"
const value3 = "hello" ?? "default"; // "hello"
const value4 = "" ?? "default"; // "" (empty string is NOT null/undefined)
const value5 = 0 ?? "default"; // 0 (0 is NOT null/undefined)
const value6 = false ?? "default"; // false (false is NOT null/undefined)
```

---

## ?? Operator

```typescript
// Basic nullish coalescing
function greet(name: string | null | undefined): string {
  return `Hello, ${name ?? "stranger"}!`;
}

greet("Alice");     // "Hello, Alice!"
greet(null);        // "Hello, stranger!"
greet(undefined);   // "Hello, stranger!"

// With function return values
function getPort(): number | null {
  return process.env.PORT ? parseInt(process.env.PORT) : null;
}

const port = getPort() ?? 3000; // 3000 if null, otherwise the actual port

// With optional properties
interface Config {
  host?: string;
  port?: number;
  debug?: boolean;
}

function createServer(config: Config): void {
  const host = config.host ?? "localhost";
  const port = config.port ?? 3000;
  const debug = config.debug ?? false;
  console.log(`${host}:${port} (debug: ${debug})`);
}

// With array methods
const items = [1, 2, 3];
const first = items[0] ?? "empty"; // 1

const empty: number[] = [];
const firstEmpty = empty[0] ?? "empty"; // "empty"

// With type assertion
const value: string | null = null;
const result: string = value ?? "default"; // result is string

// Multiple ?? in sequence
function getConfig(
  host?: string | null,
  port?: number | null,
  debug?: boolean | null,
): { host: string; port: number; debug: boolean } {
  return {
    host: host ?? "localhost",
    port: port ?? 3000,
    debug: debug ?? false,
  };
}

// ?? with template literals
function greetUser(name: string | null | undefined): string {
  return `Hello, ${name ?? "Guest"}!`;
}
```

---

## ?? vs ||

The key difference: `||` treats all falsy values as triggers, while `??` only triggers on `null` and `undefined`.

```typescript
// Falsy values in JavaScript:
// false, 0, "", null, undefined, NaN, 0n (BigInt(0))

// || treats ALL falsy values as triggers
const a = "" || "default";    // "default" (empty string is falsy!)
const b = 0 || "default";     // "default" (0 is falsy!)
const c = false || "default"; // "default" (false is falsy!)
const d = null || "default";  // "default"
const e = undefined || "default"; // "default"

// ?? only triggers on null and undefined
const f = "" ?? "default";    // "" (empty string is preserved!)
const g = 0 ?? "default";     // 0 (zero is preserved!)
const h = false ?? "default"; // false (false is preserved!)
const i = null ?? "default";  // "default"
const j = undefined ?? "default"; // "default"

// Practical difference
function getPort(): number | null {
  return null;
}

// ❌ Wrong: || falls back for 0
const port1 = getPort() || 3000; // 3000
const port2 = 0 || 3000;        // 3000 (0 is falsy!)

// ✅ Correct: ?? only falls back for null/undefined
const port3 = getPort() ?? 3000; // 3000
const port4 = 0 ?? 3000;         // 0 (0 is preserved!)

// With string values
function getDisplayName(name?: string | null): string {
  // ❌ Falls back for empty string
  const display = name || "Anonymous"; // "" becomes "Anonymous"

  // ✅ Only falls back for null/undefined
  const display2 = name ?? "Anonymous"; // "" stays ""
}

// With boolean values
function getFlag(value?: boolean | null): boolean {
  // ❌ Falls back for false
  return value || true; // false becomes true!

  // ✅ Only falls back for null/undefined
  return value ?? true; // false stays false
}

// Summary of differences:
// | Left value    | \|\| result | ?? result   |
// |---------------|-------------|-------------|
// | null          | "default"   | "default"   |
// | undefined     | "default"   | "default"   |
// | ""            | "default"   | ""          |
// | 0             | "default"   | 0           |
// | false         | "default"   | false       |
// | NaN           | "default"   | NaN         |
// | "hello"       | "hello"     | "hello"     |
// | 42            | 42          | 42          |
// | true          | true        | true        |
```

---

## Nullish Coalescing Assignment (??=)

The `??=` operator assigns a value only if the left-hand side is `null` or `undefined`.

```typescript
// Basic ??=
let value: string | null = null;
value ??= "default"; // value = "default"

let value2: string | null = "hello";
value2 ??= "default"; // value2 = "hello" (unchanged)

// ??= with undefined
let value3: string | undefined;
value3 ??= "default"; // value3 = "default"

let value4: string | undefined = "hello";
value4 ??= "default"; // value4 = "hello" (unchanged)

// ??= vs ||= difference
let a = "";
a ||= "default"; // a = "default" (empty string is falsy)
let b = "";
b ??= "default"; // b = "" (empty string is not null/undefined)

let c = 0;
c ||= 100; // c = 100 (0 is falsy)
let d = 0;
d ??= 100; // d = 0 (0 is not null/undefined)

// Practical uses of ??=

// Initialize config values
interface Config {
  host?: string;
  port?: number;
  debug?: boolean;
}

function initConfig(config: Config): Required<Config> {
  // Only set defaults for null/undefined values
  config.host ??= "localhost";
  config.port ??= 3000;
  config.debug ??= false;
  return config as Required<Config>;
}

// Initialize state
let currentUser: User | null = null;
currentUser ??= createDefaultUser(); // Only if null

// Lazy initialization
let cache: Map<string, unknown> | null = null;
function getCache(): Map<string, unknown> {
  cache ??= new Map(); // Only create if null
  return cache;
}

// ??= with objects
interface State {
  count: number;
  name?: string;
}

const state: State = { count: 0 };
state.name ??= "unnamed"; // Sets name because it's undefined
// state.count ??= 10; // Doesn't change count (it's 0, not null/undefined)

// ??= in class properties
class Service {
  private connection: Connection | null = null;

  getConnection(): Connection {
    this.connection ??= createConnection();
    return this.connection;
  }
}

// ??= with function results
let data: string | null = null;
data ??= fetchData(); // Only fetch if null
```

---

## Interaction with Optional Chaining

`?.` and `??` are designed to work together.

```typescript
// Basic combination
interface User {
  name: string;
  address?: {
    city?: string;
    zip?: string;
  };
}

const user: User = { name: "Alice" };

// ?. for safe access, ?? for default
const city = user?.address?.city ?? "Unknown";
const zip = user?.address?.zip ?? "00000";

// vs without ?.
const city2 = (user.address && user.address.city) ?? "Unknown";
// More verbose and error-prone

// Real-world: API response
interface ApiResponse {
  data?: {
    user?: {
      profile?: {
        displayName?: string;
        avatar?: string;
      };
    };
  };
}

function processResponse(response: ApiResponse): string {
  const displayName = response?.data?.user?.profile?.displayName ?? "Anonymous";
  const avatar = response?.data?.user?.profile?.avatar ?? "/default-avatar.png";
  return `${displayName} - ${avatar}`;
}

// Chaining multiple ??
function getConfigValue(settings?: Record<string, unknown>): string {
  return (
    settings?.["theme"] ??
    settings?.["ui"]?.["theme"] ??
    "light"
  );
}

// ?? with function calls
function getPort(): number | null {
  return null;
}

// ?. on the result, then ?? for default
const port = getPort()?.toString() ?? "3000";

// Nested ?? with ?.
interface Config2 {
  database?: {
    primary?: { host?: string };
    replica?: { host?: string };
  };
}

function getDbHost(config: Config2): string {
  return (
    config?.database?.primary?.host ??
    config?.database?.replica?.host ??
    "localhost"
  );
}
```

---

## Short-Circuit Evaluation

`??` short-circuits — the right-hand side is only evaluated if the left-hand side is `null` or `undefined`.

```typescript
// Short-circuit evaluation
let computed = 0;

const a = null ?? (computed++, "default");
// computed is 1 (right side evaluated)

const b = "hello" ?? (computed++, "default");
// computed is still 1 (right side NOT evaluated)

// Side effects in right-hand side
function createExpensiveObject(): { data: string } {
  console.log("Creating object...");
  return { data: "expensive" };
}

const x = "existing" ?? createExpensiveObject();
// "Creating object..." is NOT logged

const y = null ?? createExpensiveObject();
// "Creating object..." IS logged

// Short-circuit in conditional assignments
let counter = 0;
function increment(): number {
  return ++counter;
}

let value: number | null = 5;
value ??= increment(); // counter is still 0 (not incremented)

let value2: number | null = null;
value2 ??= increment(); // counter is now 1

// Short-circuit with complex expressions
interface Factory {
  create(): string;
}

function getOrCreate(factory: Factory | null, existing?: string): string {
  return existing ?? factory?.create() ?? "default";
  // If existing is defined, factory.create() is NOT called
}
```

---

## When to Use ?? vs ||

```typescript
// Use ?? when:
// 1. You only want to default for null/undefined
function getPort(port?: number | null): number {
  return port ?? 3000; // 0 should be preserved
}

// 2. Working with numbers that could be 0
function getOffset(offset?: number | null): number {
  return offset ?? 0; // Don't treat 0 as "no value"
}

// 3. Working with strings that could be empty
function getLabel(label?: string | null): string {
  return label ?? ""; // Empty string is a valid label
}

// 4. Working with booleans
function getFlag(flag?: boolean | null): boolean {
  return flag ?? false; // false should be preserved
}

// Use || when:
// 1. You want to treat all falsy values as "no value"
function getRequiredName(name?: string): string {
  return name || "Anonymous"; // "" should also default
}

// 2. You want to filter out 0, "", false, etc.
function getPositiveValue(value?: number): number {
  return value || 1; // 0 should also default to 1
}

// 3. You're sure you won't have legitimate falsy values
function getNonEmptyArray(arr?: unknown[]): unknown[] {
  return arr || []; // Empty array should also default
}

// Decision guide:
// "Is 0 a valid value for my use case?" → Use ??
// "Is '' a valid value for my use case?" → Use ??
// "Is false a valid value for my use case?" → Use ??
// If yes to any → Use ??
// If no to all → Use || is fine
```

---

## Common Patterns

```typescript
// 1. Configuration defaults
interface AppConfig {
  port?: number;
  host?: string;
  debug?: boolean;
  logLevel?: "debug" | "info" | "warn" | "error";
}

function createApp(config: AppConfig) {
  return {
    port: config.port ?? 3000,
    host: config.host ?? "localhost",
    debug: config.debug ?? false,
    logLevel: config.logLevel ?? "info",
  };
}

// 2. API response defaults
function processApiResponse(response: unknown): string {
  const data = response as { message?: string | null };
  return data?.message ?? "No message";
}

// 3. Environment variables
const config = {
  port: parseInt(process.env.PORT ?? "3000"),
  host: process.env.HOST ?? "localhost",
  nodeEnv: process.env.NODE_ENV ?? "development",
};

// 4. Form field defaults
interface FormData {
  name?: string;
  email?: string;
  age?: number;
}

function sanitizeFormData(data: FormData): Required<FormData> {
  return {
    name: data.name ?? "",
    email: data.email ?? "",
    age: data.age ?? 0,
  };
}

// 5. Cache initialization
let cache: Map<string, unknown> | null = null;

function getCache(): Map<string, unknown> {
  return (cache ??= new Map());
}

// 6. Default array elements
function getFirst<T>(arr: T[] | null | undefined, defaultValue: T): T {
  return arr?.[0] ?? defaultValue;
}

// 7. Chained defaults
function getTheme(settings?: Record<string, unknown>): string {
  return (
    settings?.["theme"] ??
    settings?.["preferences"]?.["theme"] ??
    "light"
  );
}

// 8. ??= for initialization
let initialized = false;
let connection: Connection | null = null;

function init() {
  connection ??= createConnection();
  initialized = true;
}

// 9. ?? with optional chaining in loops
const users: (User | null)[] = [];
for (const user of users) {
  const name = user?.name ?? "Unknown";
  console.log(name);
}

// 10. ?? with type narrowing
function process(value: string | null | undefined): string {
  const result = value ?? "default";
  // result is string (not null/undefined)
  return result.toUpperCase();
}
```

---

## Best Practices

1. **Use `??` over `||`** when 0, "", or false are valid values
2. **Use `??=` for lazy initialization** — only create/assign if null/undefined
3. **Combine `?.` with `??`** for safe access with defaults
4. **Remember:** `??` only triggers on `null` and `undefined`, not other falsy values
5. **Use `??` with environment variables** — they're often `undefined`
6. **Use `??` in configuration** — for setting sensible defaults
7. **Don't mix `??` and `||`** without understanding the difference
8. **Use `??=` for one-time initialization** — cache, connection, etc.
9. **Be careful with `??` and `&&`** — they have different precedence
10. **Document when `0` or `""` are valid values** — explains why `??` is used over `||`

---

## Interview Questions

### Q1: What is the difference between `??` and `||`?

**Answer:** `??` (nullish coalescing) only triggers on `null` and `undefined`. `||` (logical OR) triggers on all falsy values: `false`, `0`, `""`, `null`, `undefined`, `NaN`, `0n`. This means `"" ?? "default"` returns `""`, while `"" || "default"` returns `"default"`.

### Q2: When would you use `??` over `||`?

**Answer:** Use `??` when `0`, `""`, or `false` are valid values that shouldn't trigger the default. For example, port 0 might be valid, empty string might be a valid label, and false might be a valid boolean setting.

### Q3: What is `??=`?

**Answer:** Nullish coalescing assignment. It assigns the right-hand side only if the left-hand side is `null` or `undefined`. `x ??= "default"` is equivalent to `x = x ?? "default"`. It's useful for lazy initialization and setting defaults.

### Q4: How does `??` interact with `?.`?

**Answer:** They complement each other. `?.` provides safe access (returns `undefined` for null/undefined), and `??` provides a default value. Together: `obj?.prop ?? "default"` safely accesses a property and falls back to a default when the property is null/undefined.

### Q5: What are all the falsy values in JavaScript?

**Answer:** `false`, `0`, `-0`, `0n` (BigInt zero), `""` (empty string), `null`, `undefined`, and `NaN`. Only `null` and `undefined` trigger `??`. All falsy values trigger `||`.
