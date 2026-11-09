# Generic Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A generic interface takes type parameters so one contract can describe many element types while preserving their relationship.

## Syntax
```ts
interface Pair<T, U = T> {
  first: T;
  second: U;
}
```

## Examples
### Basic
```ts
interface Box<T> {
  value: T;
}

const numberBox: Box<number> = { value: 42 };
const stringBox: Box<string> = { value: "hello" };
```

### Practical
```ts
interface ApiResponse<T> {
  data: T;
  status: number;
}

interface Repository<T extends { id: string }> {
  find(id: string): T | undefined;
  save(entity: T): void;
}

class MemoryRepository<T extends { id: string }> implements Repository<T> {
  private readonly items = new Map<string, T>();

  find(id: string): T | undefined {
    return this.items.get(id);
  }

  save(entity: T): void {
    this.items.set(entity.id, entity);
  }
}

const response: ApiResponse<{ id: string; name: string }> = {
  data: { id: "u1", name: "Ada" },
  status: 200,
};
```

### Advanced / edge cases
```ts
interface Pair<A, B = A> {
  first: A;
  second: B;
}

const same: Pair<number> = { first: 1, second: 2 };
const mixed: Pair<number, string> = { first: 1, second: "two" };

// Generic methods keep the element type flowing.
interface Mapper<T> {
  map<U>(fn: (value: T) => U): Mapper<U>;
  get(): T;
}

declare const mapper: Mapper<number>;
const asString: Mapper<string> = mapper.map((n) => n.toString());

// ❌ Error: Property 'id' does not exist on type 'T'
// interface Bad<T> { find(id: T["id"]): void }
```

## Key points
- Type parameters are placeholders filled by the consumer.
- Defaults let callers omit parameters that have a sensible default.
- Constraints (`T extends Shape`) allow safe member access.
- Generic methods can introduce their own type parameters.
- Type arguments can be inferred from function arguments.

## Gotchas
- `// ❌ Error:` accessing members of an unconstrained `T`.
- `// ❌ Error:` `const box: Box = { value: 1 };` — a generic interface needs its argument or an inference site.
- Over-constraining `T` makes the interface hard to reuse.

## Best practice
- Constrain only the members you actually use.
- Prefer `T` for element types and descriptive names for roles (`TValue`, `TError`).
