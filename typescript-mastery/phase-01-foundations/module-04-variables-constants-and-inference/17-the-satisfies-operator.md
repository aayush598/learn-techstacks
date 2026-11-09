# The `satisfies` Operator

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — `satisfies` checks that a value conforms to a type while keeping the value's own inferred type.

## Syntax
```ts
const mode = "idle" satisfies "idle" | "loading" | "done";
const config = { retries: 3 } satisfies { retries: number };
```

## Examples
### Basic
```ts
type Status = "idle" | "loading" | "done";

const currentStatus = "idle" satisfies Status; // "idle"
const declaredStatus: Status = "idle";         // Status (widened by annotation)

const config = {
  retries: 3,
} satisfies { retries: number }; // { retries: number }
```

### Practical
```ts
type Route = "home" | "about" | "contact";

const routes = {
  home: "/",
  about: "/about",
  contact: "/contact",
} satisfies Record<Route, string>;

// Keys are still known exactly
routes.home;    // string
// routes.blog; // ❌ Error: Property 'blog' does not exist on type ...

// Typos are caught at the definition
// const bad = {
//   home: "/",
//   blog: "/blog",
// } satisfies Record<Route, string>;
// ❌ Error: Object literal may only specify known properties, and 'blog' does not exist.

console.log(routes);
```

### Advanced / edge cases
```ts
type Config = {
  mode: "light" | "dark";
  retries: number;
};

const config = {
  mode: "dark",
  retries: 3,
} satisfies Config; // mode: "dark" (literal preserved)

// config.mode = "light"; // ❌ Error: Type '"light"' is not assignable to type '"dark"'.

// Compare with an annotation, which widens the property
const annotated: Config = { mode: "dark", retries: 3 };
annotated.mode = "light"; // ✅

// satisfies composes with as const
const frozen = {
  mode: "dark",
  retries: 3,
} as const satisfies Config;

// Arrays keep tuple-like precision
const tuple = ["a", "b"] satisfies string[]; // string[]

console.log(config, annotated, frozen, tuple);
```

## Key points
- Validates against a type without changing the inferred type.
- Catches excess properties and typos at the definition site.
- Preserves literal types that an annotation would widen.
- Composes with `as const` for immutable, validated data.
- Returns the original expression, so it is usable inline.

## Gotchas
- `satisfies` does not widen or narrow the value to the target type.
- It performs an assignability check, not an exact-shape check.
- Older TypeScript versions (before 4.9) do not support it.

## Best practice
- Use `satisfies` when you want validation plus precise inference.
- Reserve annotations for cases where the wider declared type is intended.
