# `as` Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — The `as` operator is the modern, JSX-safe syntax for type assertions.

## Syntax

```ts
const a = value as Type;
const b = (value as Type).member;
```

## Examples

### Basic

```ts
let input: unknown = "42";
const text = input as string;

console.log(text.trim()); // "42"
```

### Practical

```ts
type Role = "admin" | "user" | "guest";

const rawRole = "admin";
const role = rawRole as Role; // ✅ narrows string to the union

function greet(who: Role): string {
  return `Hello, ${who}`;
}

console.log(greet(role)); // "Hello, admin"
```

### Advanced / edge cases

```ts
// `as` is also used for mapped-type key remapping — a different feature.
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type User = { name: string; age: number };
type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }

// Member access binds tighter than `as`, so parentheses matter.
const box = {} as { value: number };
const value = (box as { value: number }).value; // ✅
```

## Key points

- `as` works in both `.ts` and `.tsx` files, unlike angle-bracket assertions.
- The compiler still checks that the two types sufficiently overlap.
- `as` binds at a lower precedence than member access and calls.
- `as const` is a distinct const assertion, not a normal type cast.
- `as` can appear in mapped-type key remapping clauses with different semantics.

## Gotchas

- Forgetting parentheses changes what is asserted.

```ts
const obj = { value: "x" };
const bad = obj.value as number;
// ❌ Error: Conversion of type 'string' to type 'number' may be a mistake because neither type sufficiently overlaps with the other. (TS2352)
```

- Asserting a boolean to a string is rejected because the types do not overlap.

```ts
const flag = true as string;
// ❌ Error: Conversion of type 'boolean' to type 'string' may be a mistake because neither type sufficiently overlaps with the other. (TS2352)
```

- `as` does not perform conversions: `"42" as number` is a compile error, not `42`.

## Best practice

- Reach for `as` only after narrowing, generics, or validation cannot express the type.
- Prefer `satisfies` when you want checking without changing the inferred type.
