# Default Parameters

> Phase 1 · Module 05 · Functions

**TL;DR** — Supply `= value` after a parameter; it is used when the argument is `undefined` and its type is inferred from the default.

## Syntax
```ts
function fn(param: Type = defaultValue): ReturnType { /* ... */ }
```

## Examples
### Basic
```ts
function power(base: number, exponent = 2): number {
  return base ** exponent;
}

console.log(power(3));    // 9
console.log(power(2, 10)); // 1024
```

### Practical
```ts
type Config = { retries: number; verbose: boolean };

function connect(host: string, config: Partial<Config> = {}): Config {
  return { retries: config.retries ?? 3, verbose: config.verbose ?? false };
}

console.log(connect("db.local")); // { retries: 3, verbose: false }
```

### Advanced / edge cases
```ts
// Defaults can reference earlier parameters
function makeId(prefix: string, suffix = prefix.length): string {
  return `${prefix}-${suffix}`;
}

// ✅ default values only apply to `undefined`, not `null`
function withDefault(value: string | null = "fallback"): string {
  return value ?? "fallback";
}

console.log(withDefault(null)); // "fallback"
console.log(makeId("abc"));     // "abc-3"
```

## Key points
- Defaults make a parameter optional at the call site.
- The default's type participates in the parameter's inferred type.
- Defaults can reference previously declared parameters.
- Only `undefined` triggers the default; `null` does not.

## Gotchas
- `// ❌ Error:` `function f(a = 1, b: number) {}` is allowed syntactically, but callers must still pass `b`.
- Defaults are evaluated at call time, not definition time.
- A default of a mutable object is shared unless recreated per call.

## Best practice
- Prefer defaults over manual `??` guards for simple literals.
- Avoid mutable default objects; create them inside the body instead.
