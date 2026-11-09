# Optional Parameters

> Phase 1 · Module 05 · Functions

**TL;DR** — Mark a parameter optional with `?`; it may be omitted and its type includes `undefined`.

## Syntax
```ts
function fn(required: Type, optional?: Type): ReturnType { /* ... */ }
```

## Examples
### Basic
```ts
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}`;
}

console.log(greet("Ada"));             // "Hello, Ada"
console.log(greet("Ada", "Welcome"));  // "Welcome, Ada"
```

### Practical
```ts
type Options = { retries?: number; timeout?: number };

function request(url: string, options: Options = {}): string {
  const retries = options.retries ?? 3;
  return `${url}?retries=${retries}`;
}

console.log(request("/api")); // "/api?retries=3"
```

### Advanced / edge cases
```ts
// Optional parameters must follow required ones
function build(name: string, size?: number, color?: string): string {
  return `${name}:${size ?? 1}:${color ?? "black"}`;
}

// ✅ optional is exactly `Type | undefined`
function setLabel(value?: string): string {
  return value === undefined ? "(none)" : value;
}
```

## Key points
- `x?: T` is shorthand for `x: T | undefined` and makes the argument skippable.
- Optional parameters must come after all required parameters.
- Callers may pass `undefined` explicitly to use the default branch.
- Optional properties of an object parameter are a separate concept.

## Gotchas
- `// ❌ Error:` `function f(a?: number, b: number) {}` — required parameter after optional.
- `// ❌ Error:` with `exactOptionalPropertyTypes`, `{ x: undefined }` is not assignable to `{ x?: number }`.
- A default value also makes a parameter effectively optional.

## Best practice
- Prefer a single options object for many optional arguments.
- Treat `undefined` explicitly rather than relying on truthiness.
