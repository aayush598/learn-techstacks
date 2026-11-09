# Async Function Return Types

> Phase 1 · Module 05 · Functions

**TL;DR** — An `async` function always returns a `Promise`; annotate it as `Promise<T>`, never `T`.

## Syntax
```ts
async function fn(param: Type): Promise<ReturnType> {
  return value;
}
```

## Examples
### Basic
```ts
async function greet(name: string): Promise<string> {
  return `Hello, ${name}`;
}

greet("Ada").then(console.log); // "Hello, Ada"
```

### Practical
```ts
type User = { id: number; name: string };

async function fetchUser(id: number): Promise<User> {
  const res = await fetch(`/users/${id}`);
  if (!res.ok) throw new Error("not found");
  return (await res.json()) as User;
}

// ✅ errors reject the returned promise
fetchUser(1).catch((e: unknown) => console.error(e));
```

### Advanced / edge cases
```ts
// Async functions always wrap returned values
async function wrapped(): Promise<number> {
  return 42; // returned directly, not Promise.resolve
}

// ✅ returning a promise is flattened, not double-wrapped
async function flattened(): Promise<number> {
  return Promise.resolve(42);
}

// void async work
async function logIt(): Promise<void> {
  await Promise.resolve();
}
```

## Key points
- `async` forces the return type to be a `Promise`.
- Returning `T` inside an async function produces `Promise<T>`.
- Returning `Promise<T>` is flattened, not `Promise<Promise<T>>`.
- `Promise<void>` is the async analogue of `void`.

## Gotchas
- `// ❌ Error:` `async function f(): number { return 1; }` — async must return a promise type.
- `// ❌ Error:` `async function f(): Promise<number> { return "x"; }` — wrong resolved type.
- Forgetting `await` leaks a `Promise` into code expecting the value.

## Best practice
- Always annotate async functions with `Promise<T>` for clear contracts.
- Throw errors instead of returning sentinel values; callers use `.catch`/`try`.
