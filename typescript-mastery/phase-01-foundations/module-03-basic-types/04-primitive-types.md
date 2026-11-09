# Primitive Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `string`, `number`, `boolean`, `bigint`, and `symbol` are the immutable value types you use everywhere.

## Syntax
```ts
let s: string = "text";
let n: number = 42;
let b: boolean = true;
let big: bigint = 9007199254740993n;
let sym: symbol = Symbol("id");
```

## Examples
### Basic
```ts
const name: string = "Ada";
const age: number = 36;
const active: boolean = true;
const huge: bigint = 12345678901234567890n;
const tag: symbol = Symbol("user");

console.log(name, age, active, huge, tag.toString());
```

### Practical
```ts
// Each primitive has its own operations
const price: number = 19.99;
const quantity: number = 3;
const total: number = price * quantity; // 59.97

const currency: string = "USD";
const formatted: string = `${currency} ${total.toFixed(2)}`;

const ids: bigint[] = [1n, 2n, 3n];
const sum: bigint = ids.reduce((acc, id) => acc + id, 0n);

console.log(formatted, sum); // ✅
```

### Advanced / edge cases
```ts
// Symbols are unique even with the same description
const a = Symbol("key");
const b = Symbol("key");
console.log(a === b); // false

// bigint and number do not mix in arithmetic
const big: bigint = 10n;
// ❌ Error: Operator '+' cannot be applied to types 'bigint' and 'number'.
// const mixed = big + 1;

const asNumber: number = Number(big); // explicit conversion ✅
console.log(asNumber);
```

## Key points
- Primitives are immutable; methods return new values.
- `number` is a 64-bit float; use `bigint` for arbitrary integers.
- `bigint` literals end in `n` and never mix with `number` arithmetic.
- Each `Symbol()` call produces a unique value.
- Lowercase names are the types; `String`, `Number`, `Boolean` are wrapper objects (avoid).

## Gotchas
- `Number` (capitalized) is the boxed object type, not the primitive.
  ```ts
  const x: Number = 1; // ✅ compiles, but avoid boxed types
  ```
- Mixing `bigint` and `number` throws.
  ```ts
  // ❌ Error: Operator '*' cannot be applied to types 'bigint' and 'number'.
  // const bad = 2n * 2;
  ```
- `NaN` and `Infinity` are `number` values.
  ```ts
  const bad: number = NaN; // ✅ type-wise, but check with Number.isNaN
  ```

## Best practice
- Always use lowercase primitive types (`string`, not `String`).
- Reach for `bigint` only when values exceed `Number.MAX_SAFE_INTEGER`.
