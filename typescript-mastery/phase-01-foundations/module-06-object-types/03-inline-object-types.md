# Inline Object Types

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Write an object shape directly where it is used, without declaring a separate name.

## Syntax
```ts
function fn(value: { key: string }): { result: number } {
  return { result: value.key.length };
}
```

## Examples
### Basic
```ts
const point: { x: number; y: number } = { x: 1, y: 2 };

console.log(point.x + point.y);
```

### Practical
```ts
function area(rect: { width: number; height: number }): number {
  return rect.width * rect.height;
}

function makePoint(): { x: number; y: number } {
  return { x: 0, y: 0 };
}

console.log(area({ width: 3, height: 4 }), makePoint());
```

### Advanced / edge cases
```ts
function pickId<T extends { id: string }>(value: T): string {
  return value.id;
}

// inline index signature type
const cache: { [key: string]: { value: number; expiresAt: number } } = {};

cache["a"] = { value: 1, expiresAt: Date.now() };

console.log(pickId({ id: "u1", name: "Ada" }), cache["a"].value);
```

## Key points
- Inline types work anywhere a type is accepted: variables, parameters, returns, generics.
- They avoid polluting the module scope with one-off names.
- The same shape written twice creates two independent type literals.
- Inline types can contain optional, readonly, and index signature members.
- Generic constraints can be inline object types.

## Gotchas
- Duplicated inline shapes drift apart when only one is updated.
- `// ❌ Error:` `area({ width: 3 });` — `height` is missing.
- Long inline types make signatures hard to read; extract them when they grow.

## Best practice
- Keep inline types for small, local, single-use shapes.
- Promote a shape to a named type as soon as it appears in two signatures.
