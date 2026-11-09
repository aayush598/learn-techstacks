# Return Type Annotations

> Phase 1 · Module 05 · Functions

**TL;DR** — Annotate the return type to enforce and document exactly what a function produces.

## Syntax
```ts
function fn(param: Type): ReturnType { /* ... */ }
const arrow = (param: Type): ReturnType => expression;
```

## Examples
### Basic
```ts
function isEven(n: number): boolean {
  return n % 2 === 0;
}

console.log(isEven(4)); // true
```

### Practical
```ts
type Result = { ok: true; value: number } | { ok: false; error: string };

function divide(a: number, b: number): Result {
  if (b === 0) return { ok: false, error: "divide by zero" };
  return { ok: true, value: a / b };
}

const r = divide(10, 2);
if (r.ok) console.log(r.value); // 5
```

### Advanced / edge cases
```ts
// Annotating prevents accidental widening of union returns
function status(code: number): "ok" | "error" {
  return code >= 200 && code < 300 ? "ok" : "error";
}

// ✅ void means "do not use the result"
function log(msg: string): void {
  console.log(msg);
}
```

## Key points
- Annotations verify every `return` against the declared type.
- Explicit union/literal return types prevent widening.
- `void` documents side-effect-only functions.
- `never` describes functions that never return.

## Gotchas
- `// ❌ Error:` `function f(): string { return 1; }` — `number` is not assignable to `string`.
- Missing a `return` on some code path errors under `strict` when the return type is non-`void`.
- `undefined` must be included in the return type if a function can return it.

## Best practice
- Annotate exported functions and anything with a union or literal return.
- Use `never` for functions that always throw or loop forever.
