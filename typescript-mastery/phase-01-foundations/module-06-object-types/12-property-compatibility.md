# Property Compatibility

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — A property type in the source must be assignable to the property type in the target.

## Syntax
```ts
type Target = { key: string | number };
type Source = { key: string };

const source: Source = { key: "value" };
const target: Target = source; // source assignable to target
```

## Examples
### Basic
```ts
type Source = { value: number };
type Target = { value: number | string };

const source: Source = { value: 1 };
const target: Target = source; // ✅ number is assignable to number | string

console.log(target.value);
```

### Practical
```ts
type User = { name: string; nickname?: string };
type Named = { name: string };

const user: User = { name: "Ada" };
const named: Named = user; // ✅ optional property can be dropped

type WithNick = { name: string; nickname: string };
// const invalid: WithNick = named; // ❌ Error: nickname is missing

console.log(named.name);
```

### Advanced / edge cases
```ts
type ReadonlyPoint = { readonly x: number };
type MutablePoint = { x: number };

const readonlyPoint: ReadonlyPoint = { x: 1 };
const mutablePoint: MutablePoint = readonlyPoint; // ✅ readonly is ignored here
mutablePoint.x = 2; // mutates the same object

console.log(readonlyPoint.x, mutablePoint.x);
```

## Key points
- Property types are checked covariantly: narrower source types are accepted.
- Optional source properties satisfy optional target properties.
- A required target property cannot be satisfied by an optional source property.
- `readonly` does not affect assignability between object types.
- Extra source properties do not block assignment when the source is not a fresh literal.

## Gotchas
- `// ❌ Error:` `const invalid: WithNick = named;` — a required `nickname` cannot be supplied by a type that lacks it.
- `// ❌ Error:` `const p: { value: number } = { value: "x" };` — `string` is not assignable to `number`.
- `any` disables property checks, while `unknown` requires narrowing before use.

## Best practice
- Type target properties as widely as the consumer can handle, and source properties as narrowly as the producer guarantees.
- Avoid `any` in object properties; it lets incompatible values through silently.
