# Narrowing through callbacks

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Narrowing does not survive into callbacks that might run later, unless you capture a `const` or pass the narrowed value in.

## Syntax
```ts
if (typeof value === "string") {
  const text = value; // ✅ captured as string
  setTimeout(() => text.toUpperCase(), 0);
}
```

## Examples
### Basic
```ts
function schedule(value: string | number): void {
  if (typeof value === "string") {
    setTimeout(() => {
      console.log(value.toUpperCase()); // ✅ captured const-like narrowing
    }, 0);
  }
}
```

### Practical
```ts
function mapValue(value: string | number): string {
  if (typeof value === "number") {
    const numeric = value; // ✅ snapshot
    return [1, 2, 3].map((n) => (numeric + n).toString()).join(",");
  }
  return value.toUpperCase();
}
```

### Advanced / edge cases
```ts
function process(value: string | undefined): void {
  if (value === undefined) return;
  const safe = value; // ✅ const captures the narrowed type

  const handlers = [
    () => safe.trim(),
    () => safe.length,
    () => safe.toUpperCase(),
  ];

  handlers.forEach((fn) => fn());
}

function withCallback(value: string | number): void {
  if (typeof value === "string") {
    const fn = (): string => value.toUpperCase(); // ✅ const parameter narrows
    fn();
  }
}
```

## Key points
- Narrowing of `let`/`var` is discarded inside closures that may run later.
- `const` and narrowed parameters keep their type in callbacks.
- Capturing a snapshot (`const safe = value`) is the simplest fix.
- Passing the narrowed value as an argument also preserves it.
- Use a type guard inside the callback when no snapshot is possible.

## Gotchas
- A `let` captured by a callback can be reassigned before it runs.
- Narrowing a parameter does not narrow the outer variable it came from.
- `// ❌ Error:` `let value: string | number; if (typeof value === "string") { setTimeout(() => value.toUpperCase()); }` — `value` may have changed.

## Best practice
- Snapshot narrowed values into `const` before creating closures.
- Prefer pure callbacks that receive typed arguments.
