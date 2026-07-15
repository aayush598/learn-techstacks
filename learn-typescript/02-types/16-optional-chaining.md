# Optional Chaining in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [?. Operator](#-operator)
3. [Optional Method Calls](#optional-method-calls)
4. [Optional Element Access](#optional-element-access)
5. [Short-Circuiting Behavior](#short-circuiting-behavior)
6. [Optional Chaining with Nullish Coalescing](#optional-chaining-with-nullish-coalescing)
7. [Deep Optional Chaining](#deep-optional-chaining)
8. [Optional Chaining in Type Narrowing](#optional-chaining-in-type-narrowing)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Overview

Optional chaining (`?.`) is an ECMAScript 2020 feature that safely accesses nested properties, methods, and elements. If the value before `?.` is `null` or `undefined`, the expression short-circuits and returns `undefined`.

```typescript
// Without optional chaining
const street = user && user.address && user.address.street;

// With optional chaining
const street2 = user?.address?.street;
```

---

## ?. Operator

```typescript
// Basic property access
interface User {
  name: string;
  address?: {
    street?: string;
    city?: string;
    country?: string;
  };
}

const user: User = { name: "Alice" };

// Without optional chaining
const city1 = user.address && user.address.city; // string | undefined

// With optional chaining
const city2 = user?.address?.city; // string | undefined
const country = user?.address?.country; // string | undefined

// Safe access on potentially undefined
interface Config {
  db?: {
    connection?: {
      host: string;
      port: number;
    };
  };
}

const config: Config = {};
const host = config?.db?.connection?.host; // string | undefined
const port = config?.db?.connection?.port; // number | undefined

// Optional chaining with union types
function getLength(value: string | null | undefined): number {
  return value?.length ?? 0; // 0 if value is null/undefined
}

// Optional chaining in expressions
const result = user?.address?.city ?? "Unknown";

// Optional chaining with comparison
if (user?.address?.country === "US") {
  console.log("US user");
}

// Optional chaining in template literals
const greeting = `Hello, ${user?.name ?? "stranger"}`;
```

---

## Optional Method Calls

```typescript
// Optional method calls
interface User {
  name: string;
  greet?(): string;
  getAge?(): number;
}

const user: User = { name: "Alice" };

// Without optional chaining
const greeting1 = user.greet && user.greet();

// With optional chaining
const greeting2 = user.greet?.(); // string | undefined
const age = user.getAge?.(); // number | undefined

// Calling methods that might not exist
interface EventEmitter {
  emit?(event: string, data?: unknown): void;
  on?(event: string, handler: () => void): void;
}

function setupEvents(emitter: EventEmitter): void {
  emitter.on?.("click", () => console.log("clicked"));
  emitter.emit?.("init");
}

// Optional method on potentially undefined object
interface Service {
  process(data: string): string;
}

function callService(service: Service | null): string | undefined {
  return service?.process("data"); // undefined if service is null
}

// Optional chaining with async methods
interface API {
  fetch?(url: string): Promise<Response>;
}

async function makeRequest(api: API): Promise<Response | undefined> {
  return api?.fetch?.("/api/data"); // undefined if api or fetch is undefined
}
```

---

## Optional Element Access

```typescript
// Optional element access for arrays
const arr: (string | undefined)[] = ["a", "b", "c"];

const first = arr?.[0]; // string | undefined
const second = arr?.[1]; // string | undefined
const tenth = arr?.[9]; // undefined (out of bounds)

// Optional element access on potentially undefined array
function getFirstItem(items?: string[]): string | undefined {
  return items?.[0]; // undefined if items is undefined
}

// 2D array access
const matrix: (number | undefined)[][] = [
  [1, 2, 3],
  [4, 5, 6],
];

const cell = matrix?.[0]?.[1]; // number | undefined (row 0, col 1)

// Optional element access with computed index
function getProperty<T>(obj: T[], index: number): T | undefined {
  return obj?.[index];
}

// Optional element access on Map-like objects
interface MapLike {
  get(key: string): { value: string } | undefined;
}

function getValue(map: MapLike, key: string): string | undefined {
  return map.get(key)?.value;
}

// Optional element access in function results
function findUser(id: number): User | undefined {
  const users: User[] = [];
  return users.find((u) => u.name === `user-${id}`);
}

const user = findUser(1);
const name = user?.name; // string | undefined
```

---

## Short-Circuiting Behavior

Optional chaining short-circuits the entire expression when it encounters `null` or `undefined`.

```typescript
// Short-circuiting returns undefined
let result: string | undefined;

const obj = { a: { b: { c: "hello" } } };

result = obj?.a?.b?.c;    // "hello"
result = obj?.a?.b?.d;    // undefined (d doesn't exist)
result = obj?.a?.x?.c;    // undefined (x doesn't exist)
result = obj?.x?.b?.c;    // undefined (x doesn't exist)

// Side effects don't execute when short-circuited
let sideEffect = 0;

const obj2 = null;
const value = obj2?.a[sideEffect++]; // sideEffect is NOT incremented
console.log(sideEffect); // 0

// Short-circuiting in function calls
let called = false;

const obj3 = null;
obj3?.method(() => {
  called = true; // This never executes
});

console.log(called); // false

// Short-circuiting with method chains
interface Query {
  execute(): { result: string } | null;
}

function processQuery(query: Query | null): string | undefined {
  // If query is null, the entire chain short-circuits
  return query?.execute()?.result;
}

// Short-circuiting in assignments
let target: string | undefined;
const source = null;
target = source?.toString(); // target = undefined (no error)

// Short-circuiting with new (doesn't work — new is not chainable)
// null?.new Method(); // SyntaxError
// You can't use ?. with constructors
```

---

## Optional Chaining with Nullish Coalescing

The `?.` and `??` operators work together to provide safe defaults.

```typescript
// Basic combination
interface Config {
  database?: {
    host?: string;
    port?: number;
  };
}

const config: Config = {};

// ?. for safe access, ?? for default
const host = config?.database?.host ?? "localhost";
const port = config?.database?.port ?? 5432;

// vs || (important distinction)
const port2 = config?.database?.port || 5432; // Falls back for 0 too!
const port3 = config?.database?.port ?? 5432; // Only for null/undefined

// Real-world: API response handling
interface ApiResponse {
  data?: {
    user?: {
      name?: string;
      email?: string;
      settings?: {
        theme?: string;
      };
    };
  };
}

function processResponse(response: ApiResponse): string {
  const name = response?.data?.user?.name ?? "Anonymous";
  const email = response?.data?.user?.email ?? "no-email";
  const theme = response?.data?.user?.settings?.theme ?? "light";

  return `${name} (${email}) - ${theme}`;
}

// Chaining multiple ??
function getDisplayName(
  user?: { firstName?: string; lastName?: string } | null,
): string {
  return (
    user?.firstName ??
    user?.lastName ??
    "Unknown User"
  );
}

// ?? with function results
function getPort(): number | null {
  return null;
}

const port4 = getPort() ?? 3000; // 3000

// Nested ?? with ?.
interface Settings {
  ui?: {
    colors?: {
      primary?: string;
      secondary?: string;
    };
    fonts?: {
      heading?: string;
      body?: string;
    };
  };
}

function getTheme(settings: Settings): string {
  return settings?.ui?.colors?.primary ?? "#000";
}

function getFont(settings: Settings): string {
  return settings?.ui?.fonts?.heading ?? "Arial";
}
```

---

## Deep Optional Chaining

```typescript
// Deeply nested optional chaining
interface Company {
  ceo?: {
    name?: string;
    contact?: {
      email?: string;
      phone?: string;
    };
  };
  departments?: {
    engineering?: {
      lead?: {
        name?: string;
      };
    };
  };
}

const company: Company = {};

// Chain of ?. operators
const ceoName = company?.ceo?.name; // string | undefined
const ceoEmail = company?.ceo?.contact?.email; // string | undefined
const engLead = company?.departments?.engineering?.lead?.name; // string | undefined

// ⚠️ Deep chaining can be a code smell
// Consider flattening your data structure instead

// Alternative: use a helper function
function getNestedValue<T>(
  obj: unknown,
  path: string,
  defaultValue: T,
): T {
  const keys = path.split(".");
  let current: unknown = obj;

  for (const key of keys) {
    if (current === null || current === undefined) {
      return defaultValue;
    }
    current = (current as Record<string, unknown>)[key];
  }

  return (current as T) ?? defaultValue;
}

const name2 = getNestedValue(company, "ceo.name", "Unknown");
const email2 = getNestedValue(company, "ceo.contact.email", "no-email");

// Deep optional chaining with arrays
interface Data {
  users?: Array<{
    name?: string;
    posts?: Array<{
      title?: string;
      comments?: Array<{
        author?: string;
        text?: string;
      }>;
    }>;
  }>;
}

const data: Data = {};

const firstComment = data?.users?.[0]?.posts?.[0]?.comments?.[0]?.text;
// string | undefined
```

---

## Optional Chaining in Type Narrowing

```typescript
// Optional chaining narrows types
interface User {
  name: string;
  address?: {
    city?: string;
  };
}

function processUser(user: User): string {
  // After ?. access, the type is T | undefined
  const city = user?.address?.city;

  if (city !== undefined) {
    // city is narrowed to string
    return `City: ${city.toUpperCase()}`;
  }
  return "No city";
}

// Optional chaining with type guards
function getCityName(user: User): string {
  const city = user?.address?.city;

  // Type guard after optional chaining
  if (typeof city === "string") {
    return city.toUpperCase();
  }
  return "Unknown";
}

// Optional chaining with nullish coalescing
function getCityOrDefault(user: User): string {
  return user?.address?.city ?? "Unknown";
}

// Optional chaining in switch
function handleValue(value?: string | null): void {
  switch (value?.toUpperCase()) {
    case "HELLO":
      console.log("Greeting");
      break;
    case undefined:
      console.log("No value");
      break;
    default:
      console.log("Other");
  }
}

// Optional chaining with instanceof
function handleError(error?: Error | null): string {
  return error?.message ?? "Unknown error";
}

// Optional chaining with array methods
const users: (User | null)[] = [{ name: "Alice" }, null, { name: "Bob" }];

const names = users
  .map((u) => u?.name)
  .filter((name): name is string => name !== undefined);
// ["Alice", "Bob"]
```

---

## Best Practices

1. **Use `?.` instead of `&&` chains** — `?.` is more concise and handles null/undefined correctly
2. **Combine `?.` with `??`** for safe defaults — `?.` for access, `??` for fallback
3. **Avoid deep chaining** (3+ levels) — consider flattening your data structure
4. **Use `?.` with method calls** — `obj.method?.()` safely calls if the method exists
5. **Use `?.` with element access** — `arr?.[index]` safely accesses array elements
6. **Remember:** `?.` only short-circuits for `null` and `undefined`, not for falsy values
7. **Use `?.` in callbacks** — safely access properties in map/filter callbacks
8. **Prefer `?.` over `!`** — optional chaining is always safer than non-null assertion
9. **Use `?.` in template literals** — `${user?.name ?? "Guest"}` is clean and safe
10. **Use `?.` with `??` for function parameters** — safe access with sensible defaults

---

## Interview Questions

### Q1: What does the `?.` operator do?

**Answer:** Optional chaining (`?.`) safely accesses nested properties, methods, and elements. If the value before `?.` is `null` or `undefined`, the expression short-circuits and returns `undefined` instead of throwing an error.

### Q2: What is the difference between `?.` and `&&`?

**Answer:** `?.` specifically checks for `null` and `undefined` and handles them gracefully. `&&` checks for any falsy value (including `0`, `""`, `false`). `?.` is also more concise and handles method calls and element access, which `&&` cannot do safely.

### Q3: Can you use `?.` with function calls?

**Answer:** Yes. `obj.method?.()` calls the method only if it exists and is not null/undefined. This is useful for optional methods in interfaces.

### Q4: What does `?.` return when it short-circuits?

**Answer:** `undefined`. For example, `null?.a` returns `undefined`, and `undefined?.a?.b` also returns `undefined`.

### Q5: How does `?.` interact with `??`?

**Answer:** They complement each other. `?.` provides safe access (returns `undefined` for null/undefined), and `??` provides a default value for null/undefined. Together: `obj?.prop ?? "default"` safely accesses a property and falls back to a default.
