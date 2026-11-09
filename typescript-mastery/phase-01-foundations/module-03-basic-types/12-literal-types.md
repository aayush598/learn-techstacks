# Literal Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A literal type is a single exact value used as a type, forming the building blocks of precise unions.

## Syntax
```ts
type Direction = "north" | "south";
type Status = 200 | 404 | 500;
type Flag = true | false;
```

## Examples
### Basic
```ts
let direction: "north" = "north"; // ✅
// ❌ Error: Type '"east"' is not assignable to type '"north"'.
// direction = "east";

const answer: 42 = 42;
const yes: true = true;
console.log(direction, answer, yes);
```

### Practical
```ts
type Method = "GET" | "POST" | "PUT" | "DELETE";

function request(url: string, method: Method): string {
  return `${method} ${url}`;
}

console.log(request("/users", "GET")); // ✅
// ❌ Error: Argument of type '"PATCH"' is not assignable to parameter of type 'Method'.
// request("/users", "PATCH");
```

### Advanced / edge cases
```ts
// Literals combine into discriminated unions
type Result =
  | { ok: true; value: string }
  | { ok: false; error: string };

function unwrap(result: Result): string {
  return result.ok ? result.value : result.error; // ✅ narrowed by `ok`
}

// `as const` preserves literals in objects and arrays
const settings = { mode: "dark", retries: 3 } as const;
// { readonly mode: "dark"; readonly retries: 3 }

console.log(unwrap({ ok: true, value: "done" }), settings.mode);
```

## Key points
- Literal types describe exactly one value.
- They compose with unions to model finite sets.
- `const` variables infer literal types; `let` widens them.
- Discriminated unions use a shared literal field to enable narrowing.
- Literal types exist for strings, numbers, booleans, and bigints.

## Gotchas
- A widened `let` loses the literal.
  ```ts
  let x = "north"; // string, not "north"
  ```
- Object properties widen unless frozen with `as const`.
  ```ts
  const cfg = { mode: "dark" }; // mode: string
  ```
- Mutating a literal-typed value is rejected.
  ```ts
  // ❌ Error: Type '"south"' is not assignable to type '"north"'.
  // direction = "south";
  ```

## Best practice
- Use literal unions instead of magic strings for finite domains.
- Add `as const` to config objects you want to keep literal.
