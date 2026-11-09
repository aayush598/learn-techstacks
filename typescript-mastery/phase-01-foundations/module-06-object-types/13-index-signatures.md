# Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — An index signature describes a whole family of keys and the value type every matching key must have.

## Syntax
```ts
type T = {
  [key: string]: number;
  [index: number]: number;
  [key: symbol]: number;
};
```

## Examples
### Basic
```ts
type Scores = { [name: string]: number };

const scores: Scores = { alice: 10, bob: 20 };
scores["carol"] = 30;

console.log(scores["alice"]);
```

### Practical
```ts
type Counters = { [key: string]: number };

function increment(counters: Counters, key: string): Counters {
  counters[key] = (counters[key] ?? 0) + 1;
  return counters;
}

console.log(increment({}, "views"));
```

### Advanced / edge cases
```ts
type StringKeyed = { [key: string]: unknown };
type NumericKeyed = { [index: number]: string };

const byId: NumericKeyed = ["a", "b"];
const meta: StringKeyed = { version: 1, stable: true };

console.log(byId[0], meta["version"]);
```

## Key points
- Index signatures can use `string`, `number`, or `symbol` key types.
- Every property that matches the key kind must conform to the value type.
- A type can combine index signatures with explicitly named properties.
- Reading an index can return `undefined` at runtime if the key is absent.
- Index signatures do not enforce the presence of any particular key.

## Gotchas
- Without `noUncheckedIndexedAccess`, reading a missing key is typed as the value type even though the runtime value is `undefined`.
- `// ❌ Error:` `type Bad = { [key: string]: number; name: string };` — `name` is not a `number`.
- Index signatures are compile-time only; they do not validate or create runtime keys.

## Best practice
- Enable `noUncheckedIndexedAccess` when indexed reads are common, then handle `undefined`.
- Prefer `Record<K, V>` for a simple map and explicit properties for a fixed shape.
