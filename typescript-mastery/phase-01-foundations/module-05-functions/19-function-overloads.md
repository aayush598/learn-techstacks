# Function Overloads

> Phase 1 · Module 05 · Functions

**TL;DR** — Overloads declare several call shapes for one implementation, chosen by the arguments at each call.

## Syntax
```ts
function fn(a: string): string;
function fn(a: number): number;
function fn(a: string | number): string | number {
  return typeof a === "string" ? a.toUpperCase() : a * 2;
}
```

## Examples
### Basic
```ts
function toNumber(value: string): number;
function toNumber(value: number): number;
function toNumber(value: string | number): number {
  return typeof value === "string" ? Number(value) : value;
}

console.log(toNumber("42")); // 42
console.log(toNumber(7));    // 7
```

### Practical
```ts
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div = createElement("div"); // HTMLDivElement
const span = createElement("span"); // HTMLSpanElement
```

### Advanced / edge cases
```ts
// Overloads can vary arity, not only types
function pad(value: string, length: number, char: string): string;
function pad(value: string, length: number): string;
function pad(value: string, length: number, char = " "): string {
  return value.padStart(length, char);
}

console.log(pad("7", 3));     // "  7"
console.log(pad("7", 3, "0")); // "007"
```

## Key points
- Overload signatures are public; the implementation signature is not callable.
- Each overload is tried in order during resolution.
- Return types can differ per overload, giving precise results.
- One implementation must be compatible with all overloads.

## Gotchas
- `// ❌ Error:` calling with an argument set no overload accepts.
- The implementation signature is not part of the public API.
- Too many overloads become hard to reason about; prefer unions/generics when possible.

## Best practice
- Use literal overloads for DOM/event APIs where return type depends on input.
- Keep the implementation signature broad enough to cover all overloads.
