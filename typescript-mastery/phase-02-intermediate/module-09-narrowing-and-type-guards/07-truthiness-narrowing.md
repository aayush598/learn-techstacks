# Truthiness narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — A truthiness check removes `null`, `undefined`, `false`, `0`, `""`, and `NaN` from the type.

## Syntax
```ts
if (value) {
  // value is truthy here
}
```

## Examples
### Basic
```ts
function greet(name: string | null | undefined): string {
  if (name) {
    return `Hello, ${name}`; // ✅ string
  }
  return "Hello, stranger"; // ✅ null | undefined
}
```

### Practical
```ts
function firstItem(items: string[] | undefined): string {
  if (!items || items.length === 0) {
    return ""; // ✅ handles undefined and empty
  }
  return items[0]; // ✅ string[]
}
```

### Advanced / edge cases
```ts
type Options = { retries?: number; label?: string };

function withDefaults(options: Options): Required<Options> {
  return {
    retries: options.retries || 3, // ⚠️ 0 becomes 3
    label: options.label ?? "default", // ✅ only nullish falls back
  };
}

function hasLength(value: string | number): boolean {
  if (value) {
    return value.toString().length > 0; // ✅ excludes 0 and ""
  }
  return false;
}
```

## Key points
- Falsy values in JS: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`.
- Truthiness narrowing removes `null` and `undefined` reliably.
- It also removes `false`, `0`, and `""`, which is often unintended.
- `!value` narrows the else branch to falsy members.
- `??` handles only `null`/`undefined`, unlike `||`.

## Gotchas
- `0`, `""`, and `false` are valid values that truthiness discards.
- `// ❌ Error:` `items.length` after `if (!items)` is fine, but `items[0]` after only `if (items)` may still be `undefined` under `noUncheckedIndexedAccess`.
- Using `||` for defaults replaces `0` and `""` unexpectedly.

## Best practice
- Use `value != null` when only nullish values should be excluded.
- Use `??` instead of `||` for defaults that allow `0` or `""`.
