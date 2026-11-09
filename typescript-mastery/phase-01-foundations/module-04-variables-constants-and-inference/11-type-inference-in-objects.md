# Type Inference in Objects

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Object literals infer a shape from their properties, widening values unless const-asserted.

## Syntax
```ts
const user = { id: 1, name: "ada" };        // inferred shape
const config: { mode: string } = { mode: "dark" }; // checked
const exact = { mode: "dark" } as const;    // readonly literal
```

## Examples
### Basic
```ts
const user = {
  id: 1,
  name: "ada",
  active: true,
}; // { id: number; name: string; active: boolean }

const nested = {
  meta: { version: 1 },
}; // { meta: { version: number } }
```

### Practical
```ts
type User = { id: number; name: string };

const ada: User = { id: 1, name: "ada" }; // ✅
// const bad: User = { id: 1, name: "ada", admin: true };
// ❌ Error: Object literal may only specify known properties.

const byId: Record<number, User> = {
  1: ada,
};

const partial = { id: 2 }; // { id: number }
const merged: User = { ...ada, ...partial, name: "alan" }; // ✅

console.log(byId, merged);
```

### Advanced / edge cases
```ts
const config = {
  mode: "dark",   // string, widened
  retries: 3,     // number
};

const exact = {
  mode: "dark",
  retries: 3,
} as const; // readonly { readonly mode: "dark"; readonly retries: 3 }

type Config = typeof config;
type Exact = typeof exact;

// Index signatures come from computed keys
const scores = {
  math: 95,
  art: 88,
}; // { math: number; art: number }

const dynamic: Record<string, number> = {};
dynamic["science"] = 90;

const key = "mode";
const picked = config[key]; // string

console.log(exact, scores, dynamic, picked, {} as Config, {} as Exact);
```

## Key points
- Property names become required keys in the inferred type.
- Values widen to primitives unless `as const` is used.
- Nested objects infer nested shapes recursively.
- Computed keys with a literal produce a specific property.
- Contextual annotations add excess-property checks.

## Gotchas
- `const` objects still widen properties: `{ mode: "dark" }` gives `mode: string`.
- Excess properties error only on fresh object literals, not on variables.
- Adding a property later requires it to exist in the inferred type.

## Best practice
- Use `as const` for configuration-like objects that need literal types.
- Annotate with a named type at API boundaries to catch excess properties.
