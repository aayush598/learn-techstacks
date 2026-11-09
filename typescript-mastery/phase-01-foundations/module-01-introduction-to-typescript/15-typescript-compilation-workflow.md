# TypeScript Compilation Workflow

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — The workflow is: write TypeScript, run `tsc` with a config, fix diagnostics, then execute the emitted JavaScript.

## Syntax

```ts
// npx tsc --noEmit   # type-check only
// npx tsc            # emit according to tsconfig.json
export const ready: boolean = true;
```

## Examples

### Basic

```ts
// npx tsc src/index.ts --outDir dist
export const ready: boolean = true;
```

### Practical

```ts
const tsconfig = {
  compilerOptions: {
    strict: true,
    target: "ES2022",
    module: "NodeNext",
    moduleResolution: "NodeNext",
    outDir: "dist",
    noEmitOnError: true,
  },
  include: ["src"],
} as const;
```

### Advanced / edge cases

```ts
const buildSteps = ["parse", "type-check", "transform", "emit", "run"] as const;
type BuildStep = (typeof buildSteps)[number];

function isBeforeEmit(step: BuildStep): boolean {
  return step === "parse" || step === "type-check" || step === "transform";
}
```

## Key points

- `tsc` reads `tsconfig.json` to resolve files, options, and output paths.
- `--noEmit` performs type checking without writing JavaScript.
- `--watch` recompiles when input files change.
- `--incremental` and `tsc -b` reuse previous work for faster builds.
- Source maps connect runtime stack traces back to TypeScript source.
- The emitted JavaScript is what actually runs.

## Gotchas

- By default, `tsc` emits even when type errors are present.
- Stale `dist/` output can hide missing or deleted source files.
- Path aliases must also be resolved by the runtime or bundler, not only by `tsc`.

## Best practice

- Type-check with `tsc --noEmit` and bundle separately for applications.
- Clean the output directory before release builds, and enable `noEmitOnError` when emitting.
