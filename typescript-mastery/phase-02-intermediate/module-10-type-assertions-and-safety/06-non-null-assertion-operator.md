# Non-Null Assertion Operator

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — The postfix `!` removes `null` and `undefined` from a type without checking the value at runtime.

## Syntax

```ts
const value = maybeNull!;
const member = object!.property;
```

## Examples

### Basic

```ts
const element = document.getElementById("app")!;
element.textContent = "Ready";
```

### Practical

```ts
type User = { name?: string };

const user: User = { name: "Ada" };

// ✅ Safe only because we know name was set.
const upper = user.name!.toUpperCase();
console.log(upper); // "ADA"
```

### Advanced / edge cases

```ts
const cache = new Map<string, number>();
cache.set("count", 1);

// The key is known to exist because we just inserted it.
const count = cache.get("count")!;
console.log(count + 1); // 2

// A cleaner contract avoids the assertion entirely.
function getOrThrow(map: Map<string, number>, key: string): number {
  const value = map.get(key);
  if (value === undefined) throw new Error(`Missing key: ${key}`);
  return value;
}
```

## Key points

- `!` is erased at compile time and emits no runtime check.
- It only removes `null` and `undefined` from the type.
- `!` binds tightly, like member access, so it applies to the preceding expression.
- It is appropriate only when an invariant outside the type system guarantees presence.
- Prefer explicit checks or throwing helpers when absence is possible.

## Gotchas

- `find` can return `undefined`; `!` hides that and delays the failure.

```ts
const found = [1, 2, 3].find((n) => n > 5)!;
console.log(found + 1); // compiles, but logs NaN at runtime
```

- Optional chaining plus `!` is easy to misread.

```ts
const el = document.querySelector("#app")!;
// The element may still be missing; the cast only silences the type error.
```

- `!` on an already-null value produces `never` and can push errors elsewhere.

## Best practice

- Use `!` only after an explicit runtime guarantee, such as a prior check or insert.
- Prefer a guard or `throw` so the failure is local and debuggable.
