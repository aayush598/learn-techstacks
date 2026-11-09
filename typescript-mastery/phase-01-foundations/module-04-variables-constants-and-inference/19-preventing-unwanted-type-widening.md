# Preventing Unwanted Type Widening

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Stop widening by using `const`, `as const`, literal annotations, or `const` type parameters.

## Syntax
```ts
const mode = "on";                    // literal preserved
const config = { mode: "on" } as const; // deep literals
let pinned: "on" = "on";              // annotation pins the literal
function literal<const T>(v: T): T { return v; } // const inference for arguments
```

## Examples
### Basic
```ts
// ❌ Widened
let a = "on";        // string
const b = { mode: "on" }; // { mode: string }

// ✅ Preserved
const c = "on";      // "on"
const d = { mode: "on" } as const; // { readonly mode: "on" }
```

### Practical
```ts
type Method = "GET" | "POST";

// ❌ let widens the literal
let method = "GET"; // string
// const request = (m: Method) => m;
// request(method); // ❌ Error: Type 'string' is not assignable to type 'Method'.

// ✅ const keeps the literal
const safeMethod = "GET"; // "GET"

const request = (m: Method): Method => m;
console.log(request(safeMethod));
```

### Advanced / edge cases
```ts
// ❌ Object properties widen even with const
const settings = { theme: "dark" }; // { theme: string }

// ✅ as const stops widening recursively
const exactSettings = { theme: "dark" } as const; // { readonly theme: "dark" }

// ✅ const type parameter preserves caller literals
function literal<const T>(value: T): T {
  return value;
}
const exact = literal({ theme: "dark" }); // { readonly theme: "dark" }

// ✅ satisfies validates without widening
type Theme = { theme: "light" | "dark" };
const validated = { theme: "dark" } satisfies Theme; // { theme: "dark" }

// ✅ Return annotation pins a literal return
function ready(): "ready" {
  return "ready";
}

// ❌ Mutating a literal-typed property is rejected
// exactSettings.theme = "light"; // ❌ Error: Cannot assign to 'theme' because it is a read-only property.

console.log(settings, exact, validated, ready());
```

## Key points
- `let` and mutable properties are the main sources of widening.
- `const` preserves scalar literals but not object members.
- `as const` preserves literals and adds `readonly` deeply.
- Literal annotations pin a variable to a single value.
- `const` type parameters preserve literals passed to functions.

## Gotchas
- `as const` cannot recover literals from an already-widened value.
- Readonly from `as const` can block legitimate mutation.
- Annotating with the wide type re-introduces widening: `const x: string = "on"`.

## Best practice
- Choose the narrowest tool: `const` for scalars, `as const` for structures.
- Use `satisfies` when you need validation without losing precision.
