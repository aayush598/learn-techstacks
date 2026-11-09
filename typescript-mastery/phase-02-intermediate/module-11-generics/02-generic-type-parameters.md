# Generic Type Parameters

> Phase 2 · Module 11 · Generics

**TL;DR** — Type parameters are named placeholders declared in angle brackets and substituted with concrete types at each use site.

## Syntax
```ts
type Box<T> = { value: T };
```

## Examples
### Basic
```ts
type Box<T> = { value: T };

const count: Box<number> = { value: 3 };
const label: Box<string> = { value: "items" };
```

### Practical
```ts
type ApiResult<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function ok<T>(value: T): ApiResult<T> {
  return { ok: true, value };
}

const created = ok({ id: "u1" }); // ApiResult<{ id: string }>
```

### Advanced / edge cases
```ts
function map<T, U>(items: readonly T[], fn: (item: T) => U): U[] {
  return items.map(fn);
}

const lengths = map(["a", "bb"], (word) => word.length); // number[]

type Nested<T> = {
  value: T;
  child: { value: T };
};

const nested: Nested<boolean> = {
  value: true,
  child: { value: false },
};

function scoped<T>(value: T): T {
  return value;
}

// ❌ Error: Cannot find name 'T' — parameters are local to their declaration.
// const leaked: T = 1;
```

## Key points
- Declared in `<...>` and substituted at each use.
- Scope is limited to the function, type, interface, or class that declares them.
- Conventional names: `T`, `U`, `K`, `V`, `E`.
- Type parameters can have defaults and constraints.
- The same parameter can appear in several positions to link them.

## Gotchas
- Accessing `T` outside its declaration is a compile error.
- A parameter that appears only once usually adds ceremony, not safety.
- Shadowing an outer type parameter is legal but makes code hard to follow.

## Best practice
- Use the fewest parameters that still express the relationship.
- Use descriptive names (`TValue`, `TError`) when single letters become ambiguous.
