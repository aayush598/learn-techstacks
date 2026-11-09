# Type Erasure

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — Type annotations, interfaces, and type aliases are removed during compilation, leaving only runtime JavaScript.

## Syntax

```ts
const id: number = 1; // emits: const id = 1;
```

## Examples

### Basic

```ts
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Emitted JavaScript:
// function greet(name) { return `Hello, ${name}`; }
```

### Practical

```ts
// `import type` is erased entirely; value imports remain.
// import type { User } from "./user";
type User = { name: string };
const user: User = { name: "Ada" };
console.log(user.name); // => "Ada"
```

### Advanced / edge cases

```ts
// Enums are not erasable: they emit a runtime object.
enum Color {
  Red,
  Green,
}

// Emitted JavaScript:
// var Color;
// (function (Color) { ... })(Color || (Color = {}));
```

## Key points

- Annotations, interfaces, type aliases, and type-only imports disappear.
- Type erasure means there is no runtime reflection over TypeScript types.
- `enum`, `namespace`, decorators, and parameter properties can emit runtime code.
- The emitted JavaScript contains no type metadata to inspect or validate against.
- `import type` guarantees a type-only import is removed.

## Gotchas

- You cannot use an interface or type alias as a runtime value.

```ts
interface User { name: string }
// ❌ Error: 'User' only refers to a type, but is being used as a value here. (TS2693)
const u = User;
```

- `instanceof` cannot test a type alias or interface.
- Enums and namespaces are not erased, so they affect bundle size and runtime shape.

## Best practice

- Use `import type` for imports that are only used in type positions.
- Validate runtime data explicitly instead of expecting erased types to help.
