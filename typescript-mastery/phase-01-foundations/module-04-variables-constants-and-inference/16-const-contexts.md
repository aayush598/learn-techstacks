# Const Contexts

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — A const context is a position where TypeScript infers literal and readonly types without an explicit `as const`.

## Syntax
```ts
const tuple = [1, "one"] as const;
function literal<const T>(value: T): T { return value; }
```

## Examples
### Basic
```ts
const tuple = [1, "one"] as const; // const context

const config = {
  mode: "dark",
} as const;

// Const type parameter creates a const context for the argument
function literal<const T>(value: T): T {
  return value;
}

const a = literal({ mode: "dark" }); // { readonly mode: "dark" }
```

### Practical
```ts
function defineRoutes<const T extends readonly string[]>(routes: T): T {
  return routes;
}

const routes = defineRoutes(["home", "about", "contact"]);
// readonly ["home", "about", "contact"]

type Route = (typeof routes)[number]; // "home" | "about" | "contact"

const route: Route = "about"; // ✅

// Without const context the literals widen
function loose<T extends readonly string[]>(routes: T): T {
  return routes;
}

const wide = loose(["home", "about"]); // string[]

console.log(routes, route, wide);
```

### Advanced / edge cases
```ts
const enumLike = <const T extends Record<string, string>>(obj: T): T => obj;

const COLORS = enumLike({
  red: "red",
  blue: "blue",
}); // { readonly red: "red"; readonly blue: "blue" }

type Color = (typeof COLORS)[keyof typeof COLORS]; // "red" | "blue"

// Nested const inference
function nested<const T>(value: T): T {
  return value;
}

const data = nested({ tags: ["a", "b"] });
// { readonly tags: readonly ["a", "b"] }

// Const context does not make runtime values immutable
const arr = nested([1, 2]);
// arr.push(3); // ❌ Error: Property 'push' does not exist on type 'readonly [1, 2]'.

const c: Color = "red";

console.log(COLORS, data, arr, c);
```

## Key points
- `as const` creates a const context for the whole expression.
- `const` type parameters create one for arguments at the call site.
- Const contexts infer `readonly` and literal types deeply.
- They are purely type-level; runtime objects are unchanged.
- Const contexts make deriving unions from data convenient.

## Gotchas
- A `const` declaration alone is not a const context for object members.
- `readonly` in an annotation is shallow unless applied recursively.
- Const type parameters require a recent TypeScript version.

## Best practice
- Prefer `const` type parameters in APIs that should preserve caller literals.
- Use `as const` locally when no generic wrapper is involved.
