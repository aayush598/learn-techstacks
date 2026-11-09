# Default Generic Parameters

> Phase 2 · Module 11 · Generics

**TL;DR** — Defaults let callers omit a type argument when a sensible fallback exists, reducing ceremony without losing type safety.

## Syntax
```ts
type Box<T = string> = { value: T };
```

## Examples
### Basic
```ts
type Box<T = string> = { value: T };

const implicit: Box = { value: "hello" };  // Box<string>
const explicit: Box<number> = { value: 1 };
```

### Practical
```ts
type ApiResult<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

const success: ApiResult<number> = { ok: true, value: 1 };
const failure: ApiResult<number, string> = { ok: false, error: "nope" };
```

### Advanced / edge cases
```ts
interface Emitter<Events extends Record<string, unknown> = Record<string, unknown>> {
  emit<K extends keyof Events>(event: K, payload: Events[K]): void;
}

type LoginEvents = { login: { userId: string } };
declare const loginEmitter: Emitter<LoginEvents>;
loginEmitter.emit("login", { userId: "u1" });

// A default can reference an earlier parameter.
type Pair<A, B = A> = { first: A; second: B };
const same: Pair<number> = { first: 1, second: 2 };

// ❌ Error: Required type parameters may not follow optional type parameters.
// type Broken<A = string, B> = { first: A; second: B };
```

## Key points
- Defaults apply only when the argument is omitted and cannot be inferred.
- A default may reference parameters declared before it.
- Defaults keep simple call sites short while allowing overrides.
- Defaults do not validate explicit arguments; `Box<number>` is still allowed.
- Function, interface, class, and alias declarations all support defaults.

## Gotchas
- `// ❌ Error:` a required parameter after a defaulted one.
- Inference wins over the default when an argument supplies a candidate.
- A default like `= any` silently erases type safety.

## Best practice
- Default metadata parameters (`E = Error`) and rarely used knobs.
- Avoid defaults that make a wrong type look correct.
