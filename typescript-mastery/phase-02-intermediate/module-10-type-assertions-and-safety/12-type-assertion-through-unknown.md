# Type Assertion through `unknown`

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — `value as unknown as T` is the standard escape hatch for forcing an incompatible type, and it is still completely unchecked at runtime.

## Syntax

```ts
const value = expression as unknown as Target;
```

## Examples

### Basic

```ts
const source: string = "42";
const forced = source as unknown as number;

console.log(forced); // "42"
console.log(typeof forced); // "string"
```

### Practical

```ts
// Narrow a generic helper to a concrete type at a call site.
function cast<T>(value: unknown): T {
  return value as T; // ✅ unchecked, but explicit
}

const ids = cast<number[]>([1, 2, 3]);
console.log(ids.map((id) => id * 2)); // [2, 4, 6]
```

A safe version validates before returning:

```ts
function asNumberArray(value: unknown): number[] {
  if (!Array.isArray(value) || !value.every((v) => typeof v === "number")) {
    throw new TypeError("Expected number[]");
  }
  return value;
}

console.log(asNumberArray([1, 2, 3])); // [1, 2, 3]
```

### Advanced / edge cases

```ts
type ApiResponse = { data: { id: number } };

const raw: unknown = { data: { id: 1 } };

// `unknown` is the top type, so both casts are always permitted.
const response = raw as unknown as ApiResponse;
console.log(response.data.id); // 1
```

## Key points

- `unknown` is the top type, so asserting to it always succeeds.
- Asserting from `unknown` to any type always succeeds, so no safety remains.
- The idiom is equivalent to `as any as T` but avoids leaking `any`.
- It is useful for deliberate library internals and test doubles, not for input data.
- Every `as unknown as T` should be justified by an external invariant.

## Gotchas

- The double cast silences genuine incompatibilities that direct `as` would flag.

```ts
const text = "42" as string;
const count = text as unknown as number;
console.log(count * 2); // 84 — numeric coercion hides the lie
```

- Reaching for this pattern to fix a type error usually hides a modeling mistake.
- It provides no runtime validation, so malformed input still propagates.

## Best practice

- Prefer a validated parser that returns `T` or an error instead of a blind cast.
- Confine `as unknown as` to a single documented adapter, never across feature code.
