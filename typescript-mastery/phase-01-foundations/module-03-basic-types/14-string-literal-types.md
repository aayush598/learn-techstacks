# String Literal Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A string literal type permits one exact string, and unions of them model enumerations cleanly.

## Syntax
```ts
type Role = "admin" | "editor" | "viewer";

let role: Role = "admin";
// role = "owner"; // ❌
```

## Examples
### Basic
```ts
const greeting: "hello" = "hello";
// ❌ Error: Type '"hi"' is not assignable to type '"hello"'.
// const wrong: "hello" = "hi";

console.log(greeting); // ✅
```

### Practical
```ts
type Theme = "light" | "dark" | "system";

function applyTheme(theme: Theme): string {
  return `theme:${theme}`;
}

console.log(applyTheme("dark")); // ✅
// ❌ Error: Argument of type '"blue"' is not assignable to parameter of type 'Theme'.
// applyTheme("blue");
```

### Advanced / edge cases
```ts
// Template literal types derive new string literals
type Variant = "sm" | "md" | "lg";
type ClassName = `btn-${Variant}`; // "btn-sm" | "btn-md" | "btn-lg"

const cls: ClassName = "btn-md"; // ✅

// String literals as discriminants
type Event =
  | { type: "click"; x: number }
  | { type: "keydown"; key: string };

function handle(e: Event): string {
  return e.type === "click" ? `click@${e.x}` : `key=${e.key}`;
}

console.log(cls, handle({ type: "keydown", key: "Enter" }));
```

## Key points
- String literal types accept only the exact string.
- Unions of string literals are the idiomatic enum alternative.
- Template literal types build literal sets from other literals.
- They drive discriminated unions and exhaustive checks.
- Runtime strings still need validation at trust boundaries.

## Gotchas
- `let` widens the literal to `string`.
  ```ts
  let role = "admin"; // string, not "admin"
  ```
- Concatenation widens to `string`.
  ```ts
  const r: "admin" = "admin";
  const label = r + "!"; // string
  ```
- Untrusted input must be validated before casting.
  ```ts
  const raw = "owner" as Role; // ✅ compiles, ❌ lies at runtime
  ```

## Best practice
- Use literal unions for finite string domains and config keys.
- Validate external strings with a type guard before assigning.
