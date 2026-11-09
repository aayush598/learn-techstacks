# Promise Return Types

> Phase 1 · Module 05 · Functions

**TL;DR** — Type asynchronous results as `Promise<T>` so `.then`, `await`, and error handling are checked.

## Syntax
```ts
function fn(param: Type): Promise<ReturnType> { /* ... */ }
type Async<T> = () => Promise<T>;
```

## Examples
### Basic
```ts
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

delay(100).then(() => console.log("done"));
```

### Practical
```ts
type ApiError = { code: number; message: string };

async function request<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as T;
}

// ✅ T flows through await
async function main(): Promise<void> {
  const user = await request<{ id: number }>("/me");
  console.log(user.id);
}

main();
```

### Advanced / edge cases
```ts
// Accept any thenable, not just Promise
type MaybeAsync<T> = T | Promise<T>;

async function unwrap<T>(value: MaybeAsync<T>): Promise<T> {
  return value;
}

// ✅ Awaited flattens nested promises in type positions
type Nested = Promise<Promise<number>>;
type Flat = Awaited<Nested>; // number

// Promise-returning type alias
type Task = () => Promise<string>;
```

## Key points
- `Promise<T>` models the resolved value `T`.
- A rejected promise carries `unknown` errors; narrow before use.
- `Promise<void>` has no useful resolved value.
- `Awaited<T>` recursively unwraps promise types.

## Gotchas
- `// ❌ Error:` `const x: number = request<number>("/n");` — missing `await`.
- `// ❌ Error:` `function f(): Promise<number> { return 1; }` — non-async must return a promise.
- Unhandled rejections are runtime issues; types cannot force `.catch`.

## Best practice
- Annotate exported async APIs with `Promise<T>`.
- Use `Promise<void>` for fire-and-forget async side effects.
