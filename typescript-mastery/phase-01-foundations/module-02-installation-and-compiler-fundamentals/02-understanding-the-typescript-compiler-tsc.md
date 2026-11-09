# Understanding the TypeScript Compiler (`tsc`)

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `tsc` is the official compiler CLI: it type-checks a program and emits JavaScript, declarations, and source maps.

## Syntax
```bash
tsc [options] [file ...]
tsc --project tsconfig.json
```

## Examples
### Basic
```bash
npx tsc --version
npx tsc --help
npx tsc src/index.ts
```

### Practical
```bash
# Compile a project using its tsconfig.json
npx tsc -p tsconfig.json

# Type-check only (no files written)
npx tsc --noEmit

# Print the fully resolved configuration
npx tsc --showConfig
```

### Advanced / edge cases
```bash
# Compiler performance report
npx tsc --diagnostics

# Machine-readable build trace for chrome://tracing
npx tsc --generateTrace trace

# Explain which files entered the program and why
npx tsc --explainFiles
```

```ts
// tsc checks types but does not run this file
const port: number = Number(process.env.PORT ?? 3000);
console.log(`listening on ${port}`);
```

## Key points
- `tsc` performs **type checking** and **emit**; it is not a bundler, test runner, or runtime.
- With no file arguments it looks for `tsconfig.json` in the current directory (or a parent).
- The compiler builds a *program* from entry files plus everything they import.
- Options come from the CLI, the tsconfig file, or both — the CLI wins.
- It exits non-zero when there are errors, which makes it CI-friendly.

## Gotchas
- Passing files explicitly (`tsc src/index.ts`) bypasses `tsconfig.json`; use `-p` to force the project.
- `tsc` never executes output; run it with `node dist/index.js`.
- `--showConfig` reflects defaults too, so it is the fastest way to debug unexpected behavior.

## Best practice
- Standardize on `tsc -p tsconfig.json` (or plain `tsc`) instead of ad-hoc file lists.
- Use `--noEmit` for checks and let a bundler handle production transpilation.
