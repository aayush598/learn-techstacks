# Const Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — `as const` preserves literal types and marks objects and arrays deeply readonly.

## Syntax

```ts
const value = { key: "value" } as const;
const tuple = [1, 2, 3] as const;
```

## Examples

### Basic

```ts
const config = {
  mode: "dark",
  retries: 3,
} as const;

// config.mode has type "dark", not string.
const mode: "dark" = config.mode;
console.log(mode); // "dark"
```

### Practical

```ts
const routes = ["home", "about", "contact"] as const;

type Route = (typeof routes)[number];
// "home" | "about" | "contact"

function navigate(route: Route): void {
  console.log(`Navigating to /${route}`);
}

navigate("about"); // ✅
```

### Advanced / edge cases

```ts
type HexColor = `#${string}`;

const palette = {
  primary: "#0af",
  secondary: "#f0a",
} as const satisfies Record<string, HexColor>;

type Primary = (typeof palette)["primary"]; // "#0af"

const matrix = [
  [1, 2],
  [3, 4],
] as const;
// readonly [readonly [1, 2], readonly [3, 4]]
```

## Key points

- Object properties become `readonly` and keep their literal types.
- Array literals become `readonly` tuples with fixed length.
- Primitive literals keep their exact literal type.
- `as const` is compile-time only; it does not freeze objects at runtime.
- Combine with `typeof` to derive unions and tuple types.

## Gotchas

- Const-asserted objects reject mutation in the type system.

```ts
const settings = { theme: "dark" } as const;
settings.theme = "light";
// ❌ Error: Cannot assign to 'theme' because it is a read-only property. (TS2540)
```

- Applying `as const` directly to a `let` variable produces an immutable literal type.

```ts
let status = "ready" as const;
status = "done";
// ❌ Error: Type '"done"' is not assignable to type '"ready"'. (TS2322)
```

- `as const` does not deep-freeze: `Object.isFrozen(settings)` is still `false`.

## Best practice

- Use `as const` for configuration, route tables, and discriminated-union tags.
- Pair `as const` with `satisfies` to validate shape without widening literals.
