# Generic Interfaces

> Phase 2 · Module 11 · Generics

**TL;DR** — A generic interface describes a family of object shapes parameterized by one or more types.

## Syntax
```ts
interface Container<T> {
  value: T;
}
```

## Examples
### Basic
```ts
interface Box<T> {
  readonly value: T;
}

const numberBox: Box<number> = { value: 1 };
const stringBox: Box<string> = { value: "one" };
```

### Practical
```ts
interface ApiResponse<T> {
  data: T;
  status: number;
}

interface Repository<T extends { id: string }> {
  findById(id: string): T | undefined;
  save(entity: T): T;
}

const response: ApiResponse<{ id: string; name: string }> = {
  data: { id: "u1", name: "Ada" },
  status: 200,
};
```

### Advanced / edge cases
```ts
interface Mapper<T> {
  map<U>(fn: (value: T) => U): Mapper<U>;
  unwrap(): T;
}

declare const numberMapper: Mapper<number>;
const stringMapper: Mapper<string> = numberMapper.map((n) => n.toString());

interface Pair<A, B = A> {
  first: A;
  second: B;
}

const same: Pair<number> = { first: 1, second: 2 };
const mixed: Pair<number, string> = { first: 1, second: "two" };

// ❌ Error: Generic type 'Box' requires 1 type argument.
// const untyped: Box = { value: 1 };
```

## Key points
- Declared as `interface Name<T>`.
- Methods can introduce their own type parameters independent of the interface's.
- Defaults reduce ceremony for common cases.
- Constraints restrict which types fit the contract.
- Interfaces can share parameters with other interfaces and classes.

## Gotchas
- A generic interface needs an argument unless every parameter has a default.
- `// ❌ Error:` `const b: Box = { value: 1 }` when `Box` has no default.
- Adding a required type parameter later is a breaking change for consumers.

## Best practice
- Give parameters defaults when a sensible one exists.
- Name parameters after the role (`TData`, `TError`) in public APIs.
