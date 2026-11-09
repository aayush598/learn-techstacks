# Understanding TypeScript Compiler Errors

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — A compiler error is a structured diagnostic with a code, a location, and a message describing which type rule failed.

## Syntax

```ts
const port: number = 3000;
```

## Examples

### Basic

```ts
let count: number = 1;
// ❌ Error: Type 'string' is not assignable to type 'number'. (TS2322)
count = "two";
```

### Practical

```ts
type User = { name: string };
const user: User = { name: "Ada" };
// ❌ Error: Property 'age' does not exist on type 'User'. (TS2339)
console.log(user.age);
```

### Advanced / edge cases

```ts
// ✅ Fails if the expected error disappears
// @ts-expect-error
const a: number = "x";

// ❌ Hides future errors without verification
// @ts-ignore
const b: number = "x";
```

## Key points

- Errors use codes such as `TS2322`, which are searchable in the docs and issue tracker.
- The message often includes a type chain explaining the failed relation.
- The reported location may be the call site rather than the root cause.
- One bad type can produce a cascade of related diagnostics.
- `@ts-expect-error` suppresses an error but fails if the error is absent.
- `--pretty false` produces plain, machine-friendly diagnostic output.

## Gotchas

- Do not silence errors with `any`, `@ts-ignore`, or assertions before understanding them.
- Fixing a downstream error often makes several upstream errors disappear.
- Type errors do not necessarily stop JavaScript from being emitted.

## Best practice

- Fix the root cause, then re-run the compiler to clear cascaded errors.
- Use `@ts-expect-error` only in tests that intentionally verify an error.
