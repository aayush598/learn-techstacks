# Best Practices for Function Signatures

> Phase 1 · Module 05 · Functions

**TL;DR** — Make signatures small, explicit at boundaries, generic where it removes repetition, and honest about effects.

## Syntax
```ts
type Fn<T> = (input: T) => T;
function fn<T>(input: T, options?: Options): T { /* ... */ }
```

## Examples
### Basic
```ts
// ✅ explicit input and output at a public boundary
export function slugify(input: string): string {
  return input.trim().toLowerCase().replace(/\s+/g, "-");
}
```

### Practical
```ts
// ✅ options object for optional, non-positional flags
type FormatOptions = {
  locale?: string;
  currency?: string;
  compact?: boolean;
};

export function formatMoney(value: number, options: FormatOptions = {}): string {
  const { locale = "en-US", currency = "USD", compact = false } = options;
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    notation: compact ? "compact" : "standard",
  }).format(value);
}
```

### Advanced / edge cases
```ts
// ✅ generic + constraint instead of overloads when the shape is uniform
function property<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// ✅ return a discriminated union instead of throwing for expected failures
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseJson(text: string): Result<unknown> {
  try {
    return { ok: true, value: JSON.parse(text) };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}

// ✅ prefer unknown over any at the edges
function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
```

## Key points
- Annotate exported functions; infer small private helpers.
- Use an options object instead of many boolean positional parameters.
- Prefer generics over overloads when one shape covers all cases.
- Return `Result` unions for recoverable errors; throw for exceptional ones.
- Keep `any` out of public signatures; use `unknown` and narrow.

## Gotchas
- Boolean parameters (`fn(true, false)`) are unreadable at the call site.
- Too many overloads or generic parameters hurt inference and errors.
- Annotating everything adds noise where inference is already obvious.

## Best practice
- Design from the caller's perspective: name types by intent.
- Treat the signature as a contract and test each branch's return type.
