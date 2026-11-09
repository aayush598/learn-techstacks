# Parameter Typing

> Phase 1 · Module 05 · Functions

**TL;DR** — Every parameter needs a type (explicit or inferred); types flow from the call site into the body.

## Syntax
```ts
function fn(a: TypeA, b: TypeB): ReturnType { /* ... */ }
const arrow = (a: TypeA, b: TypeB) => { /* ... */ };
```

## Examples
### Basic
```ts
function area(width: number, height: number): number {
  return width * height;
}

console.log(area(2, 3)); // 6
```

### Practical
```ts
type User = { id: number; name: string };

function label(user: User, prefix = ""): string {
  return `${prefix}${user.name}#${user.id}`;
}

console.log(label({ id: 1, name: "Ada" }, "@")); // "@Ada#1"
```

### Advanced / edge cases
```ts
// Inline object parameter types
function distance(p: { x: number; y: number }): number {
  return Math.hypot(p.x, p.y);
}

// ✅ destructuring with annotation
function first<T>({ items }: { items: T[] }): T | undefined {
  return items[0];
}

console.log(distance({ x: 3, y: 4 })); // 5
```

## Key points
- `strict` implies `noImplicitAny`; untyped parameters become errors.
- Object parameters benefit from a named `type` or interface.
- Destructured parameters still need an annotation on the whole object.
- Parameter types are checked at every call site.

## Gotchas
- `// ❌ Error:` `function f(x) { return x; }` — parameter implicitly has type `any`.
- Widening to `object` or `any` loses useful checking.
- Excess properties in object literals are flagged, even when the type has those optional fields elsewhere.

## Best practice
- Type the parameter object, not each destructured property.
- Prefer precise types (`User`) over `any` or broad unions.
