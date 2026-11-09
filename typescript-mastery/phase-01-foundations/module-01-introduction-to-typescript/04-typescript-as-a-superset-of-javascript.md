# TypeScript as a Superset of JavaScript

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript accepts JavaScript syntax and adds types on top, so existing JavaScript can be adopted incrementally.

## Syntax

```ts
const count: number = 1;
```

## Examples

### Basic

```ts
// Plain JavaScript is valid TypeScript.
const names = ["Ada", "Grace"];
const upper = names.map((name) => name.toUpperCase()); // => ["ADA", "GRACE"]
```

### Practical

```ts
// Rename a .js file to .ts, then add annotations where inference is not enough.
function greet(name: string, punctuation = "!"): string {
  return `Hello, ${name}${punctuation}`;
}

console.log(greet("Ada")); // => "Hello, Ada!"
```

### Advanced / edge cases

```ts
// A valid JavaScript function can still fail under strict TypeScript.
// ❌ Error: Parameter 'x' implicitly has an 'any' type. (TS7006)
function double(x) {
  return x * 2;
}
```

## Key points

- Every JavaScript statement is intended to parse as TypeScript.
- TypeScript adds annotations, interfaces, generics, enums, and declaration syntax.
- TypeScript-only syntax must be compiled before a JavaScript runtime sees it.
- `allowJs` and `checkJs` let JavaScript and TypeScript coexist during migration.
- `strict` applies stronger rules, so some untyped JavaScript needs annotations.

## Gotchas

- Superset describes syntax compatibility, not that all JavaScript passes `strict`.
- TypeScript does not polyfill runtime features; it only checks and transforms syntax.
- Type-only syntax cannot be executed directly by Node.js or browsers.

## Best practice

- Migrate incrementally: enable `allowJs`, then tighten checks file by file.
- Add annotations at module boundaries first; let inference handle locals.
