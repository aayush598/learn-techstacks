# Readonly Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — A `readonly` index signature prevents adding, replacing, or deleting entries through that type.

## Syntax
```ts
type T = { readonly [key: string]: number };
type R = Readonly<Record<string, number>>;
```

## Examples
### Basic
```ts
type ReadonlyScores = {
  readonly [name: string]: number;
};

const scores: ReadonlyScores = { alice: 10 };

// scores.alice = 20;  // ❌ Error: index signature only permits reading
// scores["bob"] = 30; // ❌ Error: index signature only permits reading

console.log(scores.alice);
```

### Practical
```ts
type ImmutableRecord = Readonly<Record<string, string>>;

const env: ImmutableRecord = { NODE_ENV: "production" };
// env.NODE_ENV = "test"; // ❌ Error: read-only property

console.log(env.NODE_ENV);
```

### Advanced / edge cases
```ts
type ReadonlyNumeric<T> = { readonly [index: number]: T };

function first<T>(values: ReadonlyNumeric<T>): T | undefined {
  return values[0];
}

const nums: ReadonlyNumeric<number> = [1, 2, 3];

console.log(first(nums));
```

## Key points
- `readonly` before the index signature makes every indexed access read-only.
- `Readonly<Record<K, V>>` produces the same read-only index behavior.
- The restriction applies to the annotated reference, not the underlying object.
- Nested values remain mutable unless they are also read-only.
- Read-only index signatures are compatible with mutable ones during assignment.

## Gotchas
- `readonly` is shallow; object values stored in the index can still be mutated.
- `// ❌ Error:` `scores.alice = 20;` — assignment through a readonly index is rejected.
- A readonly type can be assigned to a mutable type, so the same object may be mutated through another reference.

## Best practice
- Expose read-only index signatures from APIs that must not be modified by callers.
- Combine with `Readonly<T>` or a deep-readonly type when nested immutability matters.
