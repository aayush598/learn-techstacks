# Callback Function Types

> Phase 1 · Module 05 · Functions

**TL;DR** — Type a callback parameter with a function signature so the callee's arguments are checked at the call site.

## Syntax
```ts
function run<T>(value: T, cb: (value: T) => void): void { /* ... */ }
```

## Examples
### Basic
```ts
function repeat(times: number, cb: (index: number) => void): void {
  for (let i = 0; i < times; i++) cb(i);
}

repeat(3, (i) => console.log(i)); // 0 1 2
```

### Practical
```ts
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
type OnDone<T> = (result: Result<T>) => void;

function load(url: string, onDone: OnDone<string>): void {
  onDone(url ? { ok: true, value: url } : { ok: false, error: new Error("bad") });
}

load("/api", (result) => {
  if (result.ok) console.log(result.value);
});
```

### Advanced / edge cases
```ts
// Callback that returns a value (e.g. a mapper)
type Mapper<T, U> = (value: T, index: number, all: T[]) => U;

function map<T, U>(items: T[], fn: Mapper<T, U>): U[] {
  return items.map(fn);
}

// ✅ a callback may ignore parameters it does not need
const ids = map([{ id: 1 }, { id: 2 }], (item) => item.id);

// Node-style error-first callback
type NodeCallback<T> = (err: Error | null, data?: T) => void;
```

## Key points
- The callback's parameters are checked by the receiving function.
- Fewer parameters than declared is allowed; each parameter is bivariant for methods but strict for functions under `strictFunctionTypes`.
- `void` callbacks may return a value that is discarded.
- Callback types can be generic, error-first, or synchronous/asynchronous.

## Gotchas
- `// ❌ Error:` `repeat(3, (i: string) => {});` — parameter type mismatch.
- `// ❌ Error:` returning a value where the callback type says `never`.
- Passing an async function where a `() => void` callback is expected silently drops the promise.

## Best practice
- Name callback types (`OnDone`, `Mapper`) for readable signatures.
- Return `void` for notification callbacks; return `Promise<void>` for async work.
