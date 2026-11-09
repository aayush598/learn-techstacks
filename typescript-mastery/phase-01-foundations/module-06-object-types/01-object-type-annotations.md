# Object Type Annotations

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Annotate an object with a shape that lists each property name and its type.

## Syntax
```ts
const value: { key: string; other?: number } = { key: "value" };
```

## Examples
### Basic
```ts
const user: { name: string; age: number } = {
  name: "Ada",
  age: 36,
};

// ✅ every property is checked at the assignment
console.log(user.name.toUpperCase());
```

### Practical
```ts
function greet(person: { name: string; age: number }): string {
  return `${person.name} (${person.age})`;
}

// ✅ the argument must match the object shape
greet({ name: "Grace", age: 45 });
```

### Advanced / edge cases
```ts
type Point = {
  x: number;
  y: number;
};

// separators can be ; , or line breaks
const originPoint: { readonly x: number; readonly y: number } = { x: 0, y: 0 };

// nested inline annotation
const config: { server: { host: string; port: number } } = {
  server: { host: "localhost", port: 8080 },
};

console.log(originPoint.x, config.server.port);
```

## Key points
- `{ ... }` in type position describes an object's properties.
- Properties are required and mutable unless marked with `?` or `readonly`.
- Property separators can be `;`, `,`, or line breaks.
- Annotations are checked at compile time and erased at runtime.
- Object types can nest other object types inline.

## Gotchas
- `// ❌ Error:` `const u: { name: string } = {};` — `name` is missing.
- `// ❌ Error:` `const u: { name: string } = { name: 42 };` — `number` is not a `string`.
- The annotation does not validate data that arrives at runtime from JSON or network calls.

## Best practice
- Annotate values at module and function boundaries; let inference handle locals.
- Name a shape once it is reused in more than one place instead of repeating it inline.
