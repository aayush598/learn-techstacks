# Control-flow analysis limitations

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Control-flow analysis is conservative: it gives up at closures, loops, aliasing, and indirect mutation where it cannot prove a type.

## Syntax
```ts
if (check) {
  // analysis is only as precise as the flow it can see
}
```

## Examples
### Basic
```ts
function pick(value: string | undefined): string {
  if (value === undefined) {
    value = "fallback"; // ✅ assignment re-narrows
  }
  return value; // ✅ string
}
```

### Practical
```ts
function loop(values: (string | null)[]): string[] {
  const result: string[] = [];
  for (const value of values) {
    if (value !== null) {
      result.push(value); // ✅ per-iteration narrowing
    }
  }
  return result;
}
```

### Advanced / edge cases
```ts
function delayed(value: string | number): void {
  if (typeof value === "number") {
    queueMicrotask(() => {
      // ⚠️ value is string | number again inside the async callback
      console.log(String(value));
    });
  }
}

function viaAlias(value: { data?: string }): string {
  const data = value.data;
  if (data !== undefined) {
    value.data = undefined; // mutation invalidates the alias assumption
    return data; // ✅ local const still string
  }
  return "";
}

function tryParse(input: string): number {
  try {
    const parsed = JSON.parse(input) as unknown;
    if (typeof parsed === "number") return parsed; // ✅ narrowed
    return 0;
  } catch {
    return 0; // ✅ catch variable is unknown
  }
}
```

## Key points
- Async callbacks re-widen captured mutable variables.
- Loops re-analyze each iteration, but not across `await` boundaries.
- `catch` variables are `unknown` under `useUnknownInCatchVariables`.
- Indirect mutation through aliases defeats the analysis.
- The analyzer never assumes a function has no side effects.

## Gotchas
- `await` can invalidate a narrowing done before it.
- Function calls may mutate objects the analyzer cannot track.
- `// ❌ Error:` `try { } catch (e) { e.message }` under strict mode — `e` is `unknown`.

## Best practice
- Re-check or snapshot values after `await` and callbacks.
- Keep narrow scopes: narrow and use immediately.
