# Rest Parameters

> Phase 1 · Module 05 · Functions

**TL;DR** — `...args` collects remaining arguments into a real array, which can itself be typed.

## Syntax
```ts
function fn(...args: Type[]): ReturnType { /* ... */ }
```

## Examples
### Basic
```ts
function sum(...nums: number[]): number {
  return nums.reduce((total, n) => total + n, 0);
}

console.log(sum(1, 2, 3)); // 6
console.log(sum());        // 0
```

### Practical
```ts
function logAll(prefix: string, ...messages: string[]): void {
  for (const msg of messages) console.log(`${prefix}${msg}`);
}

logAll("> ", "a", "b");
// > a
// > b
```

### Advanced / edge cases
```ts
// A rest parameter may be omitted; it becomes []
const count = (...xs: unknown[]): number => xs.length;

// ✅ rest must be last and only one is allowed
function tag(name: string, ...labels: string[]): string {
  return [name, ...labels].join(":");
}

// Spread an existing array into a rest parameter
const sum = (...nums: number[]): number => nums.reduce((a, b) => a + b, 0);
const nums = [1, 2, 3] as const;
console.log(sum(...nums)); // 6
```

## Key points
- A rest parameter is always an array inside the body.
- It must be the last parameter and only one is permitted.
- Rest can follow required or optional parameters.
- `as const` tuples spread cleanly into rest parameters.

## Gotchas
- `// ❌ Error:` `function f(...a: number[], b: string) {}` — rest must be last.
- `// ❌ Error:` `function f(...a: number[], ...b: string[]) {}` — only one rest parameter.
- `...` in a parameter list is not the same as the spread operator at a call site.

## Best practice
- Use a tuple type for a fixed-length rest with heterogeneous element types.
- Prefer rest over `arguments`, which is untyped and unavailable in arrow functions.
