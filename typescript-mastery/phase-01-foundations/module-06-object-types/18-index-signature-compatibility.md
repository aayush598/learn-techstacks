# Index Signature Compatibility

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Index signatures are compatible when the source value type is assignable to the target value type for the same key kind.

## Syntax
```ts
type Narrow = { [key: string]: string };
type Wide = { [key: string]: string | number };

const narrow: Narrow = { a: "x" };
const wide: Wide = narrow; // ✅ source value type is narrower
```

## Examples
### Basic
```ts
type Dict = { [key: string]: number };

const a: Dict = { x: 1, y: 2 };
const b: { [key: string]: number } = a; // ✅ same signature

console.log(b["x"]);
```

### Practical
```ts
type Alias = { x: number; y: number };
type Dict = { [key: string]: number };

const point: Alias = { x: 1, y: 2 };
const dict: Dict = point; // ✅ a type alias gets an implicit index signature

console.log(dict["x"]);
```

### Advanced / edge cases
```ts
type Base = { [key: string]: string | number };
type Derived = { [key: string]: string };

const derived: Derived = { a: "x" };
const base: Base = derived; // ✅ narrower string index to wider union

// const back: Derived = base; // ❌ Error: number is not assignable to string

console.log(base["a"]);
```

## Key points
- Source index values must be assignable to target index values.
- Narrower index value types are assignable to wider ones.
- Object literals and type aliases can receive an implicit index signature.
- `interface` types do not get an implicit index signature; they need one declared explicitly.
- Compatibility is checked per key kind: string, number, and symbol.

## Gotchas
- `// ❌ Error:` `interface Point { x: number } const d: { [key: string]: number } = point;` — the interface has no index signature.
- `// ❌ Error:` widening the value type in the source and narrowing it in the target fails.
- A number index signature is compatible with a string index signature when its value type is assignable.

## Best practice
- Declare an explicit index signature on an interface when it must be used as a dictionary.
- Keep index value types as wide as the values that will actually be stored.
