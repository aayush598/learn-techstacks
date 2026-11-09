# `instanceof` narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — `instanceof` narrows a union to classes by checking the prototype chain at runtime.

## Syntax
```ts
if (value instanceof Date) {
  // value is Date here
}
```

## Examples
### Basic
```ts
function format(value: Date | string): string {
  if (value instanceof Date) {
    return value.toISOString(); // ✅ Date
  }
  return value.toUpperCase(); // ✅ string
}
```

### Practical
```ts
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "HttpError";
  }
}

function handleError(error: Error): string {
  if (error instanceof HttpError) {
    return `${error.status}: ${error.message}`; // ✅ HttpError
  }
  return error.message; // ✅ Error
}
```

### Advanced / edge cases
```ts
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = "ValidationError";
  }
}

function classify(error: unknown): string {
  if (error instanceof ValidationError) {
    return `invalid ${error.field}`; // ✅ subclass check works
  }
  if (error instanceof Error) {
    return error.message; // ✅ base class
  }
  return String(error);
}
```

## Key points
- Works with classes, built-ins (`Date`, `Map`, `Set`, `RegExp`), and subclass hierarchies.
- Checks the prototype chain, so subclasses match base-class checks.
- Cannot narrow interfaces or type aliases, which have no runtime constructor.
- Requires the constructor to be in scope and to be a real value.
- Great for `Error` hierarchies and domain models.

## Gotchas
- `instanceof` fails across realms (iframes, workers, VM contexts).
- Plain object literals never match a class check.
- `// ❌ Error:` `value instanceof Shape` when `Shape` is only an interface.

## Best practice
- Use class hierarchies plus `instanceof` when behavior belongs to objects.
- Prefer discriminated unions for plain data shapes.
