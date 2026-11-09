# No-Emit Mode

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `--noEmit` type-checks the program without writing any files, which is ideal for CI and bundler-based builds.

## Syntax
```bash
tsc --noEmit
tsc -p tsconfig.json --noEmit
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "noEmit": true,
    "strict": true
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json
```

### Practical
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noEmit": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"]
}
```

```json
{
  "scripts": {
    "typecheck": "tsc -p tsconfig.json --noEmit",
    "build": "vite build"
  }
}
```

### Advanced / edge cases
```bash
# Override an emitting config for a one-off check
npx tsc -p tsconfig.json --noEmit

# CI job: fail on type errors, produce nothing
npx tsc -p tsconfig.json --noEmit --pretty false
```

```json
{
  "compilerOptions": {
    "noEmit": true,
    "declaration": true
  }
}
```

```bash
# noEmitOnError is different: it still emits when there are no errors
npx tsc -p tsconfig.json --noEmitOnError
```

## Key points
- `noEmit: true` performs full type checking and writes zero files.
- It does not skip type checking and does not speed up checking much.
- Use it when Vite, esbuild, SWC, or another tool transpiles the code.
- `noEmitOnError` only suppresses emit when diagnostics exist — the opposite intent.
- `--noEmit` on the CLI overrides an emitting tsconfig for that run.

## Gotchas
- `noEmit` combined with `emitDeclarationOnly` is contradictory and errors.
- `declaration: true` with `noEmit` is allowed but produces no `.d.ts` files.
- Type-checking still needs correct `moduleResolution`; `noEmit` does not relax resolution.

## Best practice
- Run `tsc --noEmit` in CI even if your bundler never type-checks.
- Keep a single `tsconfig.json` with `noEmit: true` for apps and a separate emit config for libraries.
