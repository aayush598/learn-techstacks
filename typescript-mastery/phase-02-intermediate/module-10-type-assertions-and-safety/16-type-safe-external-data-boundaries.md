# Type-Safe External Data Boundaries

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Every value crossing into your program from the network, storage, environment, or DOM is untrusted and must be validated.

## Syntax

```ts
async function fetchJson(url: string): Promise<unknown>;
```

## Examples

### Basic

```ts
async function fetchJson(url: string): Promise<unknown> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json() as Promise<unknown>; // ✅ safe widening
}

fetchJson("/api/health").then((data) => console.log(typeof data));
```

### Practical

```ts
type Env = Record<string, string | undefined>;

function requiredEnv(env: Env, key: string): string {
  const value = env[key];
  if (value === undefined || value === "") {
    throw new Error(`Missing environment variable: ${key}`);
  }
  return value;
}

const env: Env = { API_URL: "https://example.com" };
console.log(requiredEnv(env, "API_URL"));

const page = new URLSearchParams("?page=2").get("page"); // string | null
const pageNumber = page === null ? 1 : Number(page);
console.log(pageNumber); // 2
```

### Advanced / edge cases

```ts
type User = { id: number; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  const record = value as Record<string, unknown>;
  return typeof record.id === "number" && typeof record.name === "string";
}

async function loadUser(url: string): Promise<User> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data: unknown = await response.json();
  if (!isUser(data)) {
    throw new TypeError("Invalid user payload");
  }
  return data; // ✅ validated
}

loadUser("/api/user").then((user) => console.log(user.name));
```

## Key points

- Network, storage, environment, URL params, and `postMessage` are all boundaries.
- Model boundary results as `unknown` until they pass a validator.
- `fetch` does not throw on 4xx/5xx; check `response.ok`.
- URL query parameters are always `string | null`, never numbers.
- Validate once at the boundary and pass typed values through the core.

## Gotchas

- `response.json()` is typed `any`; asserting a domain type skips validation.

```ts
const user = (await fetch("/api/user").then((r) => r.json())) as User;
// ✅ compiles, but malformed payloads are now silently trusted
```

- `localStorage.getItem` can return `null`, and stored JSON may not match your type.
- Trusting `event.data` from `postMessage` exposes the app to injected shapes.

## Best practice

- Wrap boundary access in typed adapters that return `Result<T>` or throw on invalid data.
- Never export raw `any`/unvalidated data from a fetch or storage helper.
