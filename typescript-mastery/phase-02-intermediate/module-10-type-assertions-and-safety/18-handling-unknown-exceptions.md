# Handling Unknown Exceptions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — With `useUnknownInCatchVariables`, caught values are `unknown`; narrow them before reading properties.

## Syntax

```ts
try {
  // ...
} catch (error: unknown) {
  // narrow `error`
}
```

## Examples

### Basic

```ts
try {
  JSON.parse("{");
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message); // ✅ narrowed
  } else {
    console.error(String(error));
  }
}
```

### Practical

```ts
function toError(value: unknown): Error {
  return value instanceof Error ? value : new Error(String(value));
}

try {
  throw "boom";
} catch (error) {
  const err = toError(error);
  console.error(err.message); // "boom"
}
```

### Advanced / edge cases

```ts
type Outcome<T> =
  | { ok: true; value: T }
  | { ok: false; error: Error };

function toError(value: unknown): Error {
  return value instanceof Error ? value : new Error(String(value));
}

async function attempt<T>(task: () => Promise<T>): Promise<Outcome<T>> {
  try {
    return { ok: true, value: await task() };
  } catch (error) {
    return { ok: false, error: toError(error) };
  }
}

const result = await attempt(async () => 42);
if (result.ok) {
  console.log(result.value + 1); // 43
} else {
  console.error(result.error.message);
}
```

## Key points

- `strict` enables `useUnknownInCatchVariables`, so `catch` bindings are `unknown`.
- Narrow with `instanceof Error` before accessing `message`, `stack`, or `name`.
- Thrown values are not guaranteed to be `Error` instances.
- A `toError` helper normalizes primitives and foreign errors.
- Model fallible operations with a `Result` type to avoid exceptions leaking.

## Gotchas

- Annotating the catch binding with `Error` is not allowed.

```ts
try {
  throw new Error("x");
} catch (error: Error) {
  // ❌ Error: Catch clause variable type annotation must be 'any' or 'unknown' if specified. (TS1196)
  console.error(error.message);
}
```

- Reading `message` directly fails under strict mode.

```ts
try {
  throw new Error("x");
} catch (error) {
  console.error(error.message);
  // ❌ Error: 'error' is of type 'unknown'. (TS18046)
}
```

- `instanceof Error` fails across realms and for errors from other bundles.

## Best practice

- Normalize every caught value through one `toError` helper.
- Prefer returning `Result` from library code so callers handle failures explicitly.
