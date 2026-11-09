# Narrowing with `unknown`

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — `unknown` accepts anything but forces you to narrow before use, making it the safest input type.

## Syntax
```ts
function parse(input: unknown) {
  if (typeof input === "string") {
    // input is string
  }
}
```

## Examples
### Basic
```ts
function print(value: unknown): string {
  if (typeof value === "string") {
    return value; // ✅ string
  }
  if (typeof value === "number") {
    return value.toFixed(2); // ✅ number
  }
  return String(value);
}
```

### Practical
```ts
type User = { name: string; age: number };

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "name" in value &&
    typeof (value as Record<string, unknown>).name === "string" &&
    "age" in value &&
    typeof (value as Record<string, unknown>).age === "number"
  );
}

function greet(value: unknown): string {
  if (isUser(value)) {
    return `Hi ${value.name}, age ${value.age}`; // ✅ User
  }
  return "Hi stranger";
}
```

### Advanced / edge cases
```ts
function parseJson(text: string): unknown {
  return JSON.parse(text) as unknown;
}

function describe(data: unknown): string {
  if (Array.isArray(data)) {
    return `array of ${data.length}`; // ✅ unknown[]
  }
  if (data instanceof Date) {
    return data.toISOString(); // ✅ Date
  }
  if (typeof data === "object" && data !== null) {
    return `object with ${Object.keys(data).length} keys`; // ✅ object
  }
  return String(data);
}
```

## Key points
- `unknown` is the type-safe counterpart of `any`.
- Every operation requires a guard first.
- Narrowing `unknown` works with all standard guards.
- `Array.isArray` narrows to `unknown[]`.
- Prefer `unknown` for external input: JSON, `catch`, events.

## Gotchas
- `any` silently disables narrowing; `unknown` enforces it.
- `typeof value === "object"` still includes `null`.
- `// ❌ Error:` `unknownValue.trim()` without a `typeof` check.

## Best practice
- Use `unknown` at every trust boundary, then validate once.
- Return typed values from a validation function, not raw `unknown`.
