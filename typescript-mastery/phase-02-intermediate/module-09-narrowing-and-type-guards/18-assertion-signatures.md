# Assertion signatures

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Assertion signatures are the `asserts` return types that encode "this call narrows a value or a condition".

## Syntax
```ts
function assertString(value: unknown): asserts value is string;
function assertTruthy(condition: unknown): asserts condition;
```

## Examples
### Basic
```ts
function assertNumber(value: unknown): asserts value is number {
  if (typeof value !== "number" || Number.isNaN(value)) {
    throw new Error("Expected a valid number");
  }
}

function double(value: unknown): number {
  assertNumber(value);
  return value * 2; // ✅ number
}
```

### Practical
```ts
type Config = { url: string; timeout: number };

function assertConfig(value: unknown): asserts value is Config {
  const config = value as Partial<Config> | null;
  if (!config || typeof config.url !== "string" || typeof config.timeout !== "number") {
    throw new Error("Invalid config");
  }
}

function connect(value: unknown): string {
  assertConfig(value);
  return `${value.url} (${value.timeout}ms)`; // ✅ Config
}
```

### Advanced / edge cases
```ts
function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${String(value)}`);
}

type Status = "idle" | "ready";

function check(status: Status): void {
  assert(status === "ready", "Not ready");
  const ready: "ready" = status; // ✅ narrowed by asserts condition
}

function exhaustive(status: Status): string {
  switch (status) {
    case "idle":
      return "idle";
    case "ready":
      return "ready";
    default:
      return assertNever(status); // ✅ never
  }
}
```

## Key points
- Two forms: `asserts value is T` and `asserts condition`.
- `asserts condition` narrows based on the boolean expression passed in.
- Signatures can be overloaded for different inputs.
- They integrate with exhaustiveness via `assertNever`.
- Only functions and methods may declare assertion signatures.

## Gotchas
- Assertion signatures require an explicit type annotation on the function.
- The compiler trusts the assertion; a weak check produces false narrowing.
- `// ❌ Error:` `function assertString(value: unknown): asserts value is number` — asserted type must be assignable to the parameter type.

## Best practice
- Use `asserts condition` for generic preconditions.
- Use `asserts value is T` for shape validation.
