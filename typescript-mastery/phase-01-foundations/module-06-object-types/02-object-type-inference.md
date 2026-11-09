# Object Type Inference

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — TypeScript derives an object type from its literal values, widening literals unless you prevent it.

## Syntax
```ts
const value = { key: "value" };          // inferred object type
const literal = { key: "value" } as const; // readonly literal types
```

## Examples
### Basic
```ts
const user = { name: "Ada", age: 36 };
// inferred as { name: string; age: number }

// ✅ property access is fully typed
console.log(user.name.toUpperCase());
```

### Practical
```ts
function createUser(name: string, age: number) {
  return { name, age, active: true };
}

const user = createUser("Ada", 36);
// inferred as { name: string; age: number; active: boolean }

console.log(user.active);
```

### Advanced / edge cases
```ts
const config = { mode: "dark", retries: 3 } as const;
// { readonly mode: "dark"; readonly retries: 3 }

const routes = {
  home: "/",
  user: "/users/:id",
} satisfies Record<string, `/${string}`>;
// inference is preserved, but the literal is validated

console.log(config.mode, routes.home);
```

## Key points
- Literal values widen to their base type: `0` becomes `number`, `"dark"` becomes `string`.
- `as const` preserves literal types and marks every property `readonly`.
- Function return types are inferred from the returned object literal.
- `const` stops rebinding but does not make properties immutable.
- An empty object literal infers `{}`, which only excludes `null` and `undefined`.

## Gotchas
- `const point = { x: 0 }; point.x = 1;` — `point.x` is `number`, not the literal `0`.
- `const cfg = { mode: "dark" };` gives `mode: string`, which fails where `"light" | "dark"` is required.
- Destructuring copies the property type; it does not carry the parent object's identity.

## Best practice
- Rely on inference inside functions and annotate the public boundaries.
- Use `satisfies` when you want validation without widening the inferred type.
