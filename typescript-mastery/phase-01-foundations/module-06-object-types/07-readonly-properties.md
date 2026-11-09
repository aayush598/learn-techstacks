# Readonly Properties

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `readonly` blocks reassignment of a property through that type, but it is shallow and erased at runtime.

## Syntax
```ts
type T = { readonly key: string };
type R = Readonly<T>;
type A = readonly string[];
```

## Examples
### Basic
```ts
type Point = { readonly x: number; readonly y: number };

const point: Point = { x: 1, y: 2 };

// point.x = 10; // ❌ Error: cannot assign to 'x' because it is a read-only property

console.log(point.x, point.y);
```

### Practical
```ts
type User = Readonly<{ id: string; name: string }>;

const user: User = { id: "u1", name: "Ada" };
// user.name = "Grace"; // ❌ Error: read-only property

function total(values: readonly number[]): number {
  return values.reduce((sum, n) => sum + n, 0);
}

console.log(total([1, 2, 3]));
```

### Advanced / edge cases
```ts
type ReadonlyDeep<T> = {
  readonly [K in keyof T]: T[K] extends object ? ReadonlyDeep<T[K]> : T[K];
};

type State = ReadonlyDeep<{ user: { name: string }; tags: string[] }>;

const state: State = { user: { name: "Ada" }, tags: ["admin"] };

// state.user.name = "Grace"; // ❌ Error: deeply read-only
console.log(state.user.name, state.tags.length);
```

## Key points
- `readonly` prevents assignment through the annotated type.
- `Readonly<T>` applies the modifier to every top-level property.
- `readonly T[]` and `ReadonlyArray<T>` describe arrays that cannot be mutated.
- The modifier is shallow: nested objects keep their own mutability.
- `readonly` has no runtime effect and does not freeze objects.

## Gotchas
- `Readonly<T>` does not make nested properties read-only; use a recursive mapped type.
- `Readonly<T>` allows assigning a readonly object to a mutable target, so mutation can still happen elsewhere.
- A type assertion can bypass `readonly`; it is not a security boundary.

## Best practice
- Use `readonly` on configuration, constants, and parameters you do not intend to mutate.
- Accept `readonly T[]` in functions that only read arrays so callers can pass both mutable and readonly arrays.
