# Maybe Types in TypeScript

Maybe types represent values that might not exist — they are `T | null | undefined`. TypeScript's `strictNullChecks` flag makes working with maybe types explicit and safe, eliminating null reference errors at compile time.

---

## Table of Contents

1. [T | null | undefined](#t--null--undefined)
2. [Handling Maybe Types](#handling-maybe-types)
3. [Optional Chaining Patterns](#optional-chaining-patterns)
4. [Nullish Coalescing Patterns](#nullish-coalescing-patterns)
5. [Maybe Type in Functions](#maybe-type-in-functions)
6. [Maybe Type in Arrays](#maybe-type-in-arrays)
7. [Safe Unwrapping Patterns](#safe-unwrapping-patterns)
8. [Maybe Monad Pattern](#maybe-monad-pattern)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## T | null | undefined

In TypeScript with `strictNullChecks`, `null` and `undefined` are separate types. A value of type `string` can only be a string — not `null` or `undefined`.

```typescript
// With strictNullChecks enabled:
let name: string = "Alice";
// name = null;      // Compile error
// name = undefined; // Compile error

// Explicitly allow null/undefined
let maybeName: string | null | undefined = "Alice";
maybeName = null;      // OK
maybeName = undefined; // OK
maybeName = "Bob";     // OK
```

### Common maybe type patterns

```typescript
// Function that might not find a value
function findUser(id: string): User | null {
  const user = database.get(id);
  return user ?? null;
}

// Function that might not have a result
function parseConfig(input: string): Config | undefined {
  try {
    return JSON.parse(input);
  } catch {
    return undefined;
  }
}

// API response that might be null
interface ApiResponse {
  data: User | null;
  error: string | null;
}
```

### Strict null checks impact

```typescript
// Without strictNullChecks — no compile errors
function greet(name: string) {
  console.log(name.toUpperCase()); // no error even if name is null
}

// With strictNullChecks — compile error if not handled
function greet(name: string | null) {
  // console.log(name.toUpperCase()); // Error: 'name' is possibly 'null'
  if (name) {
    console.log(name.toUpperCase()); // OK — narrowed to string
  }
}
```

---

## Handling Maybe Types

### Type narrowing

```typescript
function processValue(value: string | null | undefined): string {
  if (value === null || value === undefined) {
    return "default";
  }
  // value: string (narrowed)
  return value.toUpperCase();
}
```

### Truthiness check

```typescript
function processValue(value: string | null | undefined): string {
  if (value) {
    // value: string (null and undefined are falsy)
    return value.toUpperCase();
  }
  return "default";
}
```

### Early return

```typescript
function getLength(value: string | null): number {
  if (value === null) {
    return 0;
  }
  // value: string (narrowed after early return)
  return value.length;
}
```

### Type assertion (use sparingly)

```typescript
function process(value: string | null) {
  // ⚠️ Only use when you're certain the value is not null
  const length = value!.length;
}
```

---

## Optional Chaining Patterns

Optional chaining (`?.`) safely accesses nested properties that might be null/undefined.

### Basic optional chaining

```typescript
interface User {
  name: string;
  address?: {
    street?: string;
    city?: string;
  };
}

function getCity(user: User): string | undefined {
  return user.address?.city;
  // If address is undefined, returns undefined instead of throwing
}
```

### Optional method calls

```typescript
interface Logger {
  log?: (message: string) => void;
}

function doWork(logger?: Logger) {
  logger?.log("Starting work"); // Calls log only if logger and log exist
}
```

### Optional element access

```typescript
function getFirstItem(arr: number[] | null): number | undefined {
  return arr?.[0];
}
```

### Chaining multiple levels

```typescript
interface Company {
  ceo?: {
    name?: string;
    contact?: {
      email?: string;
    };
  };
}

function getCeoEmail(company: Company): string | undefined {
  return company.ceo?.contact?.email;
  // Returns undefined if any level is null/undefined
}
```

### Optional chaining with nullish coalescing

```typescript
function getConfigValue(config: Config | null): string {
  return config?.database?.host ?? "localhost";
}
```

---

## Nullish Coalescing Patterns

The nullish coalescing operator (`??`) provides a default value only for `null` or `undefined`.

### Basic nullish coalescing

```typescript
function greet(name: string | null | undefined): string {
  return `Hello, ${name ?? "World"}`;
}

greet("Alice");  // "Hello, Alice"
greet(null);     // "Hello, World"
greet(undefined); // "Hello, World"
greet("");       // "Hello, " (empty string is NOT nullish!)
```

### vs OR operator

```typescript
const value = "" || "default";   // "default" (empty string is falsy)
const value2 = "" ?? "default";  // "" (empty string is not null/undefined)

const value3 = 0 || "default";   // "default" (0 is falsy)
const value4 = 0 ?? "default";   // 0 (0 is not null/undefined)

const value5 = false || "default"; // "default"
const value6 = false ?? "default"; // false
```

### Cascading defaults

```typescript
function getConfig(config: Partial<Config>): Config {
  return {
    host: config.host ?? "localhost",
    port: config.port ?? 3000,
    debug: config.debug ?? false,
    timeout: config.timeout ?? 5000,
  };
}
```

### Nullish coalescing assignment

```typescript
let userConfig: Partial<Config> = {};

// Set defaults
userConfig.host ??= "localhost";
userConfig.port ??= 3000;
userConfig.debug ??= false;

// Only sets if currently null/undefined
userConfig.host = "custom-host";
userConfig.host ??= "localhost"; // No change — host is already "custom-host"
```

---

## Maybe Type in Functions

### Optional parameters

```typescript
function createUser(
  name: string,
  email?: string,        // string | undefined
  age?: number           // number | undefined
) {
  return { name, email, age };
}

createUser("Alice");                    // OK
createUser("Alice", "alice@example.com"); // OK
createUser("Alice", "alice@example.com", 30); // OK
```

### Optional return types

```typescript
function findUser(id: string): User | undefined {
  const user = database.get(id);
  return user; // might be undefined
}

// Caller must handle the undefined case
const user = findUser("123");
if (user) {
  console.log(user.name);
}
```

### Function that might throw

```typescript
function parseJSON<T>(json: string): T | null {
  try {
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}

const data = parseJSON<{ name: string }>('{"name": "Alice"}');
if (data) {
  console.log(data.name);
}
```

### Higher-order functions with maybe types

```typescript
function withDefault<T>(value: T | null | undefined, defaultValue: T): T {
  return value ?? defaultValue;
}

const name = withDefault(null, "Anonymous"); // "Anonymous"
const age = withDefault(undefined, 0);      // 0
const greeting = withDefault("Hello", "Hi"); // "Hello"
```

---

## Maybe Type in Arrays

### Arrays with possible null elements

```typescript
function processItems(items: (string | null)[]): string[] {
  return items.filter((item): item is string => item !== null);
}

const result = processItems(["hello", null, "world", null]);
// ["hello", "world"]
```

### Arrays that might be null

```typescript
function getTags(post: Post): string[] {
  return post.tags ?? []; // Return empty array if tags is null/undefined
}
```

### Filtering nulls from arrays

```typescript
function filterNull<T>(arr: (T | null | undefined)[]): T[] {
  return arr.filter((item): item is T => item != null);
}

const items = [1, null, 2, undefined, 3];
const filtered = filterNull(items); // [1, 2, 3]
```

### Map with possible null results

```typescript
function parseIntSafe(values: string[]): number[] {
  return values
    .map((v) => {
      const parsed = parseInt(v);
      return isNaN(parsed) ? null : parsed;
    })
    .filter((v): v is number => v !== null);
}

const result = parseIntSafe(["1", "abc", "3", "def"]);
// [1, 3]
```

---

## Safe Unwrapping Patterns

### assertDefined

```typescript
function assertDefined<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? "Value is null or undefined");
  }
}

function processUser(user: User | null) {
  assertDefined(user, "User must exist");
  // user: User (narrowed)
  console.log(user.name);
}
```

### unwrap utility

```typescript
function unwrap<T>(value: T | null | undefined, errorMessage?: string): T {
  if (value === null || value === undefined) {
    throw new Error(errorMessage ?? "Unexpected null/undefined value");
  }
  return value;
}

const user = unwrap(findUser("123"), "User not found");
console.log(user.name);
```

### Promise unwrap

```typescript
async function fetchAndUnwrap<T>(promise: Promise<T | null>): Promise<T> {
  const result = await promise;
  if (result === null) {
    throw new Error("Unexpected null result");
  }
  return result;
}

const user = await fetchAndUnwrap(fetchUser("123"));
```

### Maybe with Result type

```typescript
type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function fromNullable<T>(value: T | null | undefined, error: string): Result<T> {
  if (value === null || value === undefined) {
    return { ok: false, error };
  }
  return { ok: true, value };
}

const result = fromNullable(findUser("123"), "User not found");
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error);
}
```

---

## Maybe Monad Pattern

The Maybe monad provides a functional way to handle nullable values.

```typescript
class Maybe<T> {
  private constructor(private value: T | null | undefined) {}

  static of<T>(value: T | null | undefined): Maybe<T> {
    return new Maybe(value);
  }

  static empty<T>(): Maybe<T> {
    return new Maybe<T>(null);
  }

  isNothing(): boolean {
    return this.value === null || this.value === undefined;
  }

  isJust(): boolean {
    return !this.isNothing();
  }

  map<U>(fn: (value: T) => U): Maybe<U> {
    if (this.isNothing()) {
      return Maybe.empty();
    }
    return Maybe.of(fn(this.value as T));
  }

  flatMap<U>(fn: (value: T) => Maybe<U>): Maybe<U> {
    if (this.isNothing()) {
      return Maybe.empty();
    }
    return fn(this.value as T);
  }

  filter(predicate: (value: T) => boolean): Maybe<T> {
    if (this.isNothing() || !predicate(this.value as T)) {
      return Maybe.empty();
    }
    return this;
  }

  getOrElse(defaultValue: T): T {
    return this.value ?? defaultValue;
  }

  orElse(fn: () => Maybe<T>): Maybe<T> {
    if (this.isNothing()) {
      return fn();
    }
    return this;
  }

  toArray(): T[] {
    return this.isNothing() ? [] : [this.value as T];
  }
}

// Usage
const result = Maybe.of(findUser("123"))
  .map((user) => user.name)
  .filter((name) => name.length > 0)
  .getOrElse("Anonymous");

const email = Maybe.of(findUser("123"))
  .flatMap((user) => Maybe.of(user.email))
  .map((email) => email.toLowerCase())
  .getOrElse("no-email@example.com");
```

### Maybe with async operations

```typescript
class AsyncMaybe<T> {
  constructor(private promise: Promise<T | null>) {}

  static of<T>(promise: Promise<T | null>): AsyncMaybe<T> {
    return new AsyncMaybe(promise);
  }

  async map<U>(fn: (value: T) => U): Promise<Maybe<U>> {
    const value = await this.promise;
    return Maybe.of(value === null ? null : fn(value));
  }

  async getOrElse(defaultValue: T): Promise<T> {
    const value = await this.promise;
    return value ?? defaultValue;
  }
}
```

---

## Best Practices

1. **Enable `strictNullChecks`** — always, for type safety
2. **Use `T | null` over `T | null | undefined`** — pick one unless you need both
3. **Use optional chaining `?.`** — for safe property access
4. **Use nullish coalescing `??`** — for default values
5. **Use type narrowing, not assertions** — `if (value !== null)` over `value!`
6. **Prefer `??` over `||`** — for default values (preserves `0`, `""`, `false`)
7. **Use `assertDefined` pattern** — for preconditions
8. **Return `null` over `undefined`** — for "not found" cases (more explicit)
9. **Use the Maybe monad** — for complex nullable chains

---

## Interview Questions

### Q1: What is a maybe type in TypeScript?

**Answer:** A maybe type is `T | null | undefined` — a type that might not have a value. TypeScript's `strictNullChecks` flag requires explicit handling of `null` and `undefined`, preventing null reference errors at compile time.

### Q2: What is the difference between `??` and `||`?

**Answer:** `??` (nullish coalescing) returns the right operand only for `null` or `undefined`. `||` (logical OR) returns the right operand for any falsy value, including `0`, `""`, and `false`. Use `??` when you want to preserve falsy values like `0` or `""`.

### Q3: How does optional chaining work?

**Answer:** Optional chaining (`?.`) short-circuits and returns `undefined` if the left operand is `null` or `undefined`. It works for property access (`obj?.prop`), method calls (`obj?.method()`), and element access (`arr?.[0]`). It prevents TypeError when accessing properties on nullable values.

### Q4: What is the Maybe monad?

**Answer:** The Maybe monad is a functional pattern for handling nullable values. It wraps a value that might be null and provides methods like `map`, `flatMap`, and `filter` to chain operations without explicit null checks. It eliminates null reference errors in a functional style.

### Q5: When should you use `null` vs `undefined`?

**Answer:** By convention: `undefined` means "not assigned" or "missing" (optional parameters, missing properties); `null` means "intentionally empty" or "no value" (cleared references, search results). TypeScript treats both the same way with `??`, but `||` treats them differently with `undefined`.

### Q6: How do you safely unwrap a maybe type?

**Answer:** Options include: (1) type narrowing with if/else, (2) optional chaining with nullish coalescing, (3) `assertDefined` helper that throws if null, (4) `unwrap` utility, (5) Maybe monad with `map`/`flatMap`, (6) Result type pattern. Choose based on whether you want to handle, propagate, or fail on null values.
