# Type Alias Fundamentals

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A `type` alias gives a reusable name to any type: primitives, unions, objects, functions, tuples, and computed types.

## Syntax
```ts
type UserId = string | number;
type Point = { x: number; y: number };
```

## Examples
### Basic
```ts
type UserId = number;
type Point = { x: number; y: number };

const id: UserId = 42;
const point: Point = { x: 1, y: 2 };
```

### Practical
```ts
type Status = "idle" | "loading" | "success" | "error";

type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

function parse(input: string): Result<number> {
  const n = Number(input);
  return Number.isNaN(n)
    ? { ok: false, error: "not a number" }
    : { ok: true, value: n };
}

const result = parse("42");
if (result.ok) {
  console.log(result.value * 2); // 84
}
```

### Advanced / edge cases
```ts
type Mapper<T, U> = (value: T, index: number) => U;

type ReadonlyDeep<T> = {
  readonly [K in keyof T]: T[K] extends object ? ReadonlyDeep<T[K]> : T[K];
};

const config: ReadonlyDeep<{ port: number; db: { host: string } }> = {
  port: 5432,
  db: { host: "localhost" },
};

// ❌ Error: Cannot assign to 'host' because it is a read-only property
// config.db.host = "remote";
```

## Key points
- `type` aliases work for every type, including unions and primitives.
- Aliases are erased; they add names, not runtime objects.
- Generic aliases accept type parameters and defaults.
- Aliases can reference other aliases and computed types.
- A type alias does not create a new nominal type.

## Gotchas
- `// ❌ Error:` `type Id = string; type Id = number;` — duplicate alias names do not merge.
- Recursive aliases must eventually bottom out through a reference, array, or object.
- An alias is not a substitute for runtime validation; `type Age = number` does not stop `-1`.

## Best practice
- Use aliases for unions, tuples, function signatures, and mapped types.
- Name the concept, not the representation: `UserId` beats `NumberType`.
