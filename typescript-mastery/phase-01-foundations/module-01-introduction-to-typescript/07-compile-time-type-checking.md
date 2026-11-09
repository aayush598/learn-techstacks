# Compile-Time Type Checking

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — `tsc` checks the entire program for type errors at compile time, before any emitted JavaScript runs.

## Syntax

```ts
// npx tsc --noEmit
const port: number = 3000;
```

## Examples

### Basic

```ts
const port: number = 3000;
// ❌ Error: Type 'string' is not assignable to type 'number'. (TS2322)
const badPort: number = "3000";
```

### Practical

```ts
type Expect<T extends true> = T;
type IsString<T> = T extends string ? true : false;

type _ = Expect<IsString<"hi">>; // ✅ compiles only if the condition is true
```

### Advanced / edge cases

```ts
// @ts-expect-error — number is not assignable to string
const bad: string = 42;
```

## Key points

- Compile-time checks cover the whole program, including imported files.
- `--noEmit` type-checks without producing JavaScript.
- The editor and `tsc` share the same checking rules but may run different versions.
- Type-level assertions can verify inferred types during development.
- `@ts-expect-error` asserts that a line must produce an error.

## Gotchas

- By default `tsc` still emits JavaScript when type errors exist.
- `noEmitOnError: true` is required if a failed build must not write output.
- Compile-time success does not guarantee runtime correctness.

## Best practice

- Run `tsc --noEmit` in CI as a dedicated type-check step.
- Enable `noEmitOnError` for production builds that use `tsc` to emit.
