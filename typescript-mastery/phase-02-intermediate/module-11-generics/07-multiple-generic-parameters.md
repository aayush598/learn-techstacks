# Multiple Generic Parameters

> Phase 2 · Module 11 · Generics

**TL;DR** — Multiple type parameters let one declaration relate several independent types, such as a value and its error, or a key and a value.

## Syntax
```ts
function pair<A, B>(first: A, second: B): [A, B] {
  return [first, second];
}
```

## Examples
### Basic
```ts
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

const success: Result<number, string> = { ok: true, value: 1 };
const failure: Result<number, string> = { ok: false, error: "failed" };
```

### Practical
```ts
type Either<T, E = Error> =
  | { right: T }
  | { left: E };

const value: Either<number> = { right: 1 };
const problem: Either<number, string> = { left: "bad input" };

function swap<A, B>(pair: readonly [A, B]): [B, A] {
  return [pair[1], pair[0]];
}

const swapped = swap([1, "one"] as const); // ["one", 1]
```

### Advanced / edge cases
```ts
function zip<A, B>(left: readonly A[], right: readonly B[]): Array<[A, B]> {
  const length = Math.min(left.length, right.length);
  return Array.from({ length }, (_, index): [A, B] => [left[index], right[index]]);
}

const zipped = zip([1, 2], ["a", "b"]); // Array<[number, string]>

// Later parameters can depend on earlier ones.
function get<T, K extends keyof T>(source: T, key: K): T[K] {
  return source[key];
}

const name = get({ id: "u1", name: "Ada" }, "name"); // string

// ❌ Error: Required type parameters may not follow optional type parameters.
// type Broken<T = string, U> = { first: T; second: U };
```

## Key points
- Parameters are positional: `Result<number, string>` is not `Result<string, number>`.
- Defaults must come after required parameters.
- Later parameters can be constrained by earlier ones (`K extends keyof T`).
- Each parameter can be inferred independently from different arguments.
- Order should follow how consumers think about the type.

## Gotchas
- Reordering parameters is a breaking change.
- `// ❌ Error:` a required parameter cannot follow a defaulted one.
- Too many parameters make call sites hard to read; group related ones.

## Best practice
- Put the primary value type first and the error or metadata type later.
- Use defaults for parameters that usually have an obvious choice.
