# Generic Type Aliases

> Phase 2 · Module 11 · Generics

**TL;DR** — A generic type alias names a type expression that depends on parameters, ideal for unions, tuples, and mapped shapes.

## Syntax
```ts
type Nullable<T> = T | null;
```

## Examples
### Basic
```ts
type Nullable<T> = T | null;
type List<T> = T[];

const maybeName: Nullable<string> = null;
const scores: List<number> = [1, 2, 3];
```

### Practical
```ts
interface User {
  id: string;
  name: string;
}

type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

const idle: AsyncState<User> = { status: "idle" };
const ready: AsyncState<User> = {
  status: "success",
  data: { id: "u1", name: "Ada" },
};
```

### Advanced / edge cases
```ts
type Fn<TArgs extends unknown[], TReturn> = (...args: TArgs) => TReturn;

type Handler<T> = Fn<[value: T], void>;
const logNumber: Handler<number> = (value) => console.log(value);

type Recursive<T> = { value: T; next?: Recursive<T> };
const chain: Recursive<number> = { value: 1, next: { value: 2 } };

type NonNullish<T> = T extends null | undefined ? never : T;
const defined: NonNullish<string | null> = "x";

// ❌ Error: Type 'null' is not assignable to type 'string'.
// const missing: NonNullish<string | null> = null;
```

## Key points
- Aliases accept parameters just like interfaces and functions.
- They can wrap unions, tuples, functions, conditionals, and mapped types.
- Aliases do not create a new runtime or nominal type.
- Generic aliases can be recursive.
- A generic alias can describe a function type (`type Fn<T> = (x: T) => T`).

## Gotchas
- `// ❌ Error:` aliases cannot be declaration-merged like interfaces.
- `// ❌ Error:` `type Bad<T> = T; const x: Bad = 1;` — missing type argument.
- Recursive aliases must terminate through an object, array, or tuple, not directly.

## Best practice
- Use aliases for unions, conditionals, and derived shapes; interfaces for extendable object contracts.
- Keep aliases readable by composing smaller named pieces.
