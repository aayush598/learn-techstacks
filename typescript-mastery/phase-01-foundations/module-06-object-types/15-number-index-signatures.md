# Number Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `[index: number]: T` describes values addressed by numeric keys, such as array-like collections.

## Syntax
```ts
type Numeric = { [index: number]: string };
```

## Examples
### Basic
```ts
type StringList = { [index: number]: string };

const list: StringList = ["a", "b", "c"];

console.log(list[0].toUpperCase());
```

### Practical
```ts
type Sparse<T> = { [index: number]: T };

function at<T>(values: Sparse<T>, index: number): T | undefined {
  return values[index];
}

console.log(at(["a", "b"], 1));
```

### Advanced / edge cases
```ts
type TupleLike = {
  0: string;
  1: number;
  [index: number]: string | number;
};

const pair: TupleLike = ["age", 36];

console.log(pair[0], pair[1]);
```

## Key points
- A number index signature governs numeric keys only.
- Arrays and tuples satisfy a number index signature when their element type fits.
- The signature does not add array members such as `length` or `map`.
- Numeric keys are strings at runtime, but TypeScript keeps them distinct for checking.
- Named properties can coexist if they are compatible with any overlapping signature.

## Gotchas
- Reading past the end is typed as `T` unless `noUncheckedIndexedAccess` is enabled, but the runtime value is `undefined`.
- `// ❌ Error:` `const n = list.length;` — `length` is not part of a bare number index type.
- `Object.keys` returns `string[]`, not `number[]`, even for numeric keys.

## Best practice
- Use arrays or `ReadonlyArray<T>` when you need array behavior; use a number index signature only for array-like contracts.
- Explicitly declare `length` if a numeric collection must expose it.
