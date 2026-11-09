# Overload Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — Overload signatures are the declaration-only lines that define the callable shapes callers see.

## Syntax
```ts
function fn(a: string): string;
function fn(a: number): number;
```

## Examples
### Basic
```ts
function len(value: string): number;
function len(value: unknown[]): number;
function len(value: string | unknown[]): number {
  return value.length;
}

console.log(len("abc")); // 3
console.log(len([1, 2])); // 2
```

### Practical
```ts
type Query = { id: number } | { name: string };

function find(query: { id: number }): string;
function find(query: { name: string }): string;
function find(query: Query): string {
  return "id" in query ? `id=${query.id}` : `name=${query.name}`;
}

console.log(find({ id: 1 }));    // "id=1"
console.log(find({ name: "a" })); // "name=a"
```

### Advanced / edge cases
```ts
// Signatures can be generic
function first<T>(items: T[]): T | undefined;
function first<T>(items: T[], fallback: T): T;
function first<T>(items: T[], fallback?: T): T | undefined {
  return items.length > 0 ? items[0] : fallback;
}

const a = first([1, 2]);        // number | undefined
const b = first([1, 2], 0);     // number
```

## Key points
- Overload signatures have no body and end with `;`.
- They must be immediately followed by the implementation signature.
- Callers only see the overload signatures, never the implementation.
- Generic overloads can specialize the result by argument type.

## Gotchas
- `// ❌ Error:` `function f(a: string): string;` with no implementation is only valid in ambient declarations.
- Overload signatures that are not assignable to the implementation produce an error.
- An overload with a `never` return makes matching calls return `never`.

## Best practice
- Order overloads from most specific to most general.
- Keep each overload minimal and non-redundant.
