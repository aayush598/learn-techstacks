# Compiler Diagnostics

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Diagnostics are `TSxxxx`-coded errors and warnings that tell you exactly where and why type checking failed.

## Syntax
```bash
tsc --noEmit
tsc --pretty false
tsc --diagnostics
```

## Examples
### Basic
```bash
npx tsc -p tsconfig.json --noEmit
```

```text
src/index.ts:3:7 - error TS2322: Type 'string' is not assignable to type 'number'.

3 const port: number = "3000";
        ~~~~
```

### Practical
```bash
# Plain output for logs and CI annotations
npx tsc -p tsconfig.json --noEmit --pretty false

# Performance summary
npx tsc -p tsconfig.json --diagnostics

# More detailed timing breakdown
npx tsc -p tsconfig.json --extendedDiagnostics
```

```json
{
  "scripts": {
    "typecheck": "tsc -p tsconfig.json --noEmit --pretty false"
  }
}
```

### Advanced / edge cases
```ts
// Suppress a known, intentional error — prefer @ts-expect-error over @ts-ignore
// @ts-expect-error — legacy API returns any
const value: number = legacyApi();

// ❌ @ts-ignore hides real regressions and never fails when the error disappears
// @ts-ignore
const other: number = legacyApi();
```

```bash
# Stop truncating long type names in error messages
npx tsc -p tsconfig.json --noErrorTruncation
```

```bash
# Skip checking third-party declarations to cut noise and time
npx tsc -p tsconfig.json --skipLibCheck
```

## Key points
- Error codes are stable identifiers you can search in the TypeScript docs.
- `--pretty false` gives stable, parseable output for CI.
- `--diagnostics` reports files, lines, memory, and time; `--extendedDiagnostics` adds detail.
- `@ts-expect-error` fails if the next line is actually fine — it is self-cleaning.
- `--skipLibCheck` skips `.d.ts` checking, not your own source.

## Gotchas
- By default `tsc` emits JavaScript even when errors are reported; add `--noEmit` or `noEmitOnError`.
- `@ts-ignore` suppresses every error on the next line and never tells you when it is unnecessary.
- Diagnostics are compile-time only; runtime failures still need tests and runtime validation.

## Best practice
- Treat every diagnostic as an error in CI and keep `pretty` off in automation.
- Use `@ts-expect-error` with a comment explaining why the suppression exists.
