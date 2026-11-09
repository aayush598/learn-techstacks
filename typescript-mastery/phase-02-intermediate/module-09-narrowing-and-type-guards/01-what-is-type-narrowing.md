# What is type narrowing?

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Type narrowing is TypeScript reducing a broad type to a more specific one inside a guarded branch, based on runtime checks.

## Syntax
```ts
function handle(value: string | number) {
  if (typeof value === "string") {
    value.toUpperCase();
  } else {
    value.toFixed(2);
  }
}
```

## Examples
### Basic
```ts
type Id = string | number;

function formatId(id: Id): string {
  if (typeof id === "number") {
    return id.toString(); // ✅ id is number
  }
  return id.toUpperCase(); // ✅ id is string
}
```

### Practical
```ts
type ApiResponse =
  | { ok: true; data: string[] }
  | { ok: false; error: string };

function render(res: ApiResponse): string {
  if (res.ok) {
    return res.data.join(", "); // ✅ narrowed to success shape
  }
  return `Error: ${res.error}`; // ✅ narrowed to failure shape
}
```

### Advanced / edge cases
```ts
function process(input: string | string[] | null): number {
  if (input === null) {
    return 0; // ✅ null removed
  }
  if (Array.isArray(input)) {
    return input.length; // ✅ string[]
  }
  return input.length; // ✅ string
}
```

## Key points
- Narrowing happens through control flow, not by reassigning types.
- Guards like `typeof`, `instanceof`, `in`, equality, and truthiness all narrow.
- The narrowed type only applies inside the branch where the check holds.
- Narrowing works with unions; it removes members that fail the check.
- User-defined guards extend narrowing to custom shapes.

## Gotchas
- Narrowing is erased at runtime; it does not add validation.
- Reassigning a variable can widen it back.
- Mutating objects after a check can invalidate the narrowed assumption.

## Best practice
- Prefer explicit guards over type assertions (`as`).
- Keep guard conditions close to where the narrowed value is used.
