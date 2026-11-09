# Interfaces with Optional Properties

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Mark a property with `?` when it may be absent, which makes its type `T | undefined` at read time.

## Syntax
```ts
interface User {
  name: string;
  nickname?: string;
}
```

## Examples
### Basic
```ts
interface User {
  name: string;
  nickname?: string;
}

const a: User = { name: "Ada" }; // ✅
const b: User = { name: "Ada", nickname: "A" }; // ✅

console.log(a.nickname?.toUpperCase()); // undefined
```

### Practical
```ts
interface RequestOptions {
  method?: "GET" | "POST";
  headers?: Record<string, string>;
  timeoutMs?: number;
}

function request(url: string, options: RequestOptions = {}): string {
  const method = options.method ?? "GET";
  const timeout = options.timeoutMs ?? 5_000;
  return `${method} ${url} (timeout ${timeout}ms)`;
}

console.log(request("/users")); // "GET /users (timeout 5000ms)"
```

### Advanced / edge cases
```ts
interface Profile {
  bio?: string;
}

// Optional is not the same as a required property that accepts undefined.
interface WithUndefined {
  bio: string | undefined;
}

const p1: Profile = {}; // ✅
const p2: WithUndefined = { bio: undefined }; // ✅
// ❌ Error: Property 'bio' is missing
// const p3: WithUndefined = {};

// Utility type makes every property optional.
type Draft<T> = Partial<T>;
const draft: Draft<{ title: string; body: string }> = { title: "Hi" };
```

## Key points
- `prop?: T` is equivalent to `prop: T | undefined` when reading.
- Optional properties may be omitted from object literals.
- Access optional values with `?.`, `??`, or explicit narrowing.
- `Partial<T>` makes all properties optional.
- Optional methods can also be called with `?.`.

## Gotchas
- `// ❌ Error:` under `exactOptionalPropertyTypes`: `const p: Profile = { bio: undefined };` — `undefined` is not assignable to an absent optional property.
- Optional does not mean "nullable"; `null` still requires an explicit union.
- Forgetting to narrow produces `possibly undefined` errors under `strict`.

## Best practice
- Use `?` for genuinely absent data, not as a shortcut for weak typing.
- Give optional inputs defaults with `??` at the boundary.
