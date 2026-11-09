# Implementation Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — The implementation signature is the single body that must satisfy every overload but is hidden from callers.

## Syntax
```ts
function fn(a: string): string;
function fn(a: number): number;
function fn(a: string | number): string | number {
  return typeof a === "string" ? a : a;
}
```

## Examples
### Basic
```ts
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  // ✅ implementation signature is not callable externally
  return typeof value === "string" ? value : value.toFixed(2);
}

console.log(format(1)); // "1.00"
```

### Practical
```ts
function make(value: string): { s: string };
function make(value: number): { n: number };
function make(value: string | number): { s: string } | { n: number } {
  return typeof value === "string" ? { s: value } : { n: value };
}

console.log(make("x")); // { s: "x" }
```

### Advanced / edge cases
```ts
// Implementation parameters may be broader than any overload
function pick(key: string): string;
function pick(key: number): number;
function pick(key: string | number | boolean): string | number {
  return typeof key === "boolean" ? String(key) : key;
}

// ✅ the implementation may accept more than the overloads expose
// ❌ Error: no overload accepts boolean
console.log(pick(true));
```

## Key points
- Exactly one implementation follows the overload signatures.
- The implementation signature must be compatible with all overloads.
- Callers cannot invoke the implementation directly when overloads exist.
- Broader parameter types in the implementation are fine; narrower are not.

## Gotchas
- `// ❌ Error:` `function f(a: string): string; function f(a: number): number; function f(a: string): string { ... }` — implementation must accept `number` too.
- An implementation signature alone (without overloads) is just the public signature.
- Return type must cover every overload's return type.

## Best practice
- Write a broad implementation signature and narrow with runtime checks.
- Keep the body's branches aligned with each overload.
