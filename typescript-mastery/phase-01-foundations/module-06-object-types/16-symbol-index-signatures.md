# Symbol Index Signatures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — `[key: symbol]: T` describes values stored under symbol keys, including `unique symbol` constants.

## Syntax
```ts
type T = { [key: symbol]: string };
```

## Examples
### Basic
```ts
const id: unique symbol = Symbol("id");

type Entity = {
  [key: symbol]: string;
};

const entity: Entity = { [id]: "u1" };

console.log(entity[id]);
```

### Practical
```ts
const metadata = Symbol("metadata");

type WithMeta = {
  name: string;
  [key: symbol]: unknown;
};

const model: WithMeta = {
  name: "User",
  [metadata]: { table: "users" },
};

console.log(model[metadata]);
```

### Advanced / edge cases
```ts
const userId = Symbol("userId");
const token = Symbol("token");

type SymbolValues = {
  [key: symbol]: number | string;
};

const values: SymbolValues = {
  [userId]: 1,
  [token]: "abc",
};

console.log(values[userId], values[token]);
```

## Key points
- Symbol index signatures were added in TypeScript 4.4.
- One signature covers every symbol key, just as a string signature covers every string key.
- `unique symbol` is required when a symbol is used as a literal computed property.
- Well-known symbols such as `Symbol.iterator` are covered by the signature.
- Symbol keys do not collide with string or number keys.

## Gotchas
- `// ❌ Error:` `const s = Symbol("s"); type T = { [s]: string };` — a non-`unique` symbol cannot be a computed property name in a type.
- A symbol index signature accepts all symbols, not just the ones you intend to use.
- Symbol-keyed properties are skipped by `Object.keys` and `JSON.stringify`.

## Best practice
- Use module-scoped `unique symbol` constants to create collision-free internal keys.
- Prefer a `unique symbol` property when you know the exact key; use a symbol index for a dynamic family of symbols.
