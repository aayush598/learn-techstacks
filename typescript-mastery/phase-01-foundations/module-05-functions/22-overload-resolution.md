# Overload Resolution

> Phase 1 · Module 05 · Functions

**TL;DR** — TypeScript picks the first overload whose parameters accept the arguments, so order matters.

## Syntax
```ts
function fn(a: "a"): 1;
function fn(a: string): 2;
function fn(a: string): 1 | 2 { return a === "a" ? 1 : 2; }
```

## Examples
### Basic
```ts
function kind(value: string): "text";
function kind(value: number): "number";
function kind(value: string | number): "text" | "number" {
  return typeof value === "string" ? "text" : "number";
}

console.log(kind("x")); // "text"
console.log(kind(1));   // "number"
```

### Practical
```ts
// Specific overload must come first
function area(size: number): number;
function area(width: number, height: number): number;
function area(a: number, b?: number): number {
  return a * (b ?? a);
}

console.log(area(2));    // 4
console.log(area(2, 3)); // 6
```

### Advanced / edge cases
```ts
// First matching overload wins, even if a later one is more precise
function parse(input: string): string;
function parse(input: "yes"): boolean;
function parse(input: string): string | boolean {
  return input === "yes" ? true : input;
}

const r = parse("yes"); // string — the first overload matched

// ✅ put literal overloads first
function parseFixed(input: "yes"): boolean;
function parseFixed(input: string): string;
function parseFixed(input: string): string | boolean {
  return input === "yes" ? true : input;
}
const ok = parseFixed("yes"); // boolean
```

## Key points
- Resolution walks overloads top to bottom and returns the first match.
- Literal and narrower overloads must precede broader ones.
- Argument count and types both participate in matching.
- If none match, the call is an error at the call site.

## Gotchas
- `// ❌ Error:` calling with an argument set no overload accepts, even if the implementation would handle it.
- A broad overload first shadows all later ones.
- `// ❌ Error:` ambiguity can surface as an unhelpful "no overload matches" message.

## Best practice
- Order overloads from most specific to most general.
- Write a test for each overload's expected return type.
