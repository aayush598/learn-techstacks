# Fresh Object Literals

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — A freshly written object literal receives contextual typing and excess property checks; once stored in a variable it stops being fresh.

## Syntax
```ts
type Target = { key: string };
const fresh: Target = { key: "value" }; // fresh: checked
const stored = { key: "value" };        // widened: no freshness
```

## Examples
### Basic
```ts
type Mode = "light" | "dark";

function setMode(mode: Mode): void {
  console.log(mode);
}

setMode("dark"); // ✅ literal fits the union
// setMode("blue"); // ❌ Error: not assignable to Mode

setMode("light");
```

### Practical
```ts
type Config = { mode: "light" | "dark" };

const direct: Config = { mode: "dark" }; // ✅ contextually typed as "dark"

const widened = { mode: "dark" }; // { mode: string }
// const viaVariable: Config = widened; // ❌ Error: string is not "light" | "dark"

const literal = { mode: "dark" } as const; // { readonly mode: "dark" }
const viaConst: Config = literal; // ✅

console.log(direct.mode, viaConst.mode);
```

### Advanced / edge cases
```ts
type Config = { mode: "light" | "dark" };

const validated = { mode: "dark" } satisfies Config;
// validated.mode is "dark", not string

const annotated: Config = { mode: "dark" };
// annotated.mode is "light" | "dark" — the annotation wins

console.log(validated.mode, annotated.mode);

// ❌ Error: "blue" is not assignable to "light" | "dark"
const invalid = { mode: "blue" } satisfies Config;
```

## Key points
- Freshness is a property of object literals, not of variables.
- Contextual typing assigns literal types before widening.
- Storing a literal in a variable lets its properties widen to `string`, `number`, and so on.
- `as const` preserves literal types and readonly modifiers.
- `satisfies` validates a fresh literal while keeping its inferred type.

## Gotchas
- `const config = { mode: "dark" };` gives `string`, not `"dark"`.
- `// ❌ Error:` passing `{ mode: "dark" }` to a `{ mode: string }` parameter is fine, but passing a widened `{ mode: string }` to a literal union is not.
- Freshness also enables excess property checks; losing freshness also loses that protection.

## Best practice
- Use `satisfies` for configuration objects to validate without widening.
- Annotate the target when you need the declared type; use `as const` when you need literal values.
