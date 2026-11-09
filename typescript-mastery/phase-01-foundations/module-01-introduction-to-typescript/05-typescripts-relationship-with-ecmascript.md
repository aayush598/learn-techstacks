# TypeScript's Relationship with ECMAScript

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript tracks the ECMAScript standard, types standardized features, and uses `target` and `lib` to control syntax and APIs.

## Syntax

```ts
const label = (value?: string): string => value ?? "unknown"; // => "unknown"
```

## Examples

### Basic

```ts
// ECMAScript syntax is typed by TypeScript; emit depends on `target`.
const sum = (values: number[]): number =>
  values.reduce((a, b) => a + b, 0);

console.log(sum([1, 2, 3])); // => 6
```

### Practical

```ts
const compilerOptions = {
  target: "ES2017",
  lib: ["ES2017", "DOM"],
} as const;

// `target` controls emitted syntax; `lib` controls which standard APIs type-check.
```

### Advanced / edge cases

```ts
// TypeScript adds types around standard APIs; it does not replace them.
const entries = Object.entries({ a: 1, b: 2 }); // [string, number][]
const formatted = entries.map(([key, value]) => `${key}=${value}`);
console.log(formatted); // => ["a=1", "b=2"]
```

## Key points

- TypeScript implements the ECMAScript grammar and adds type annotations to it.
- New standard features are supported once they are stable enough to type.
- `target` selects the emitted JavaScript version and which downlevel transforms run.
- `lib` selects the standard library type definitions available to the checker.
- TypeScript does not ship runtime polyfills for older environments.
- Some proposals are supported early, but behavior can change before standardization.

## Gotchas

- Changing `target` changes emitted syntax, not the runtime APIs available.
- A missing `lib` entry produces errors for APIs that exist at runtime.

```ts
// With "lib": ["ES2020"], replaceAll is not typed:
// ❌ Error: Property 'replaceAll' does not exist on type 'string'. (TS2550)
const slug = "Hello World".replaceAll(" ", "-");
```

- Editor libraries and runtime Node.js versions can diverge from your `lib` settings.

## Best practice

- Set `target` to the oldest runtime you actually support, and `lib` to the APIs you actually use.
- Update `target` and `lib` deliberately when dropping runtime support.
