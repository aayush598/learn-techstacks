# TypeScript Compiler Overview

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — `tsc` parses TypeScript, builds a program, type-checks it, and emits JavaScript plus optional declaration files.

## Syntax

```ts
// npx tsc src/index.ts --strict --outDir dist
export const version: string = "1.0.0";
```

## Examples

### Basic

```ts
// Compile one file; the output is plain JavaScript.
const message: string = "compiled";
console.log(message);
```

### Practical

```ts
const config = {
  compilerOptions: {
    strict: true,
    target: "ES2022",
    module: "NodeNext",
    moduleResolution: "NodeNext",
    outDir: "dist",
    declaration: true,
    noEmitOnError: true,
  },
  include: ["src"],
} as const;
```

### Advanced / edge cases

```ts
// Simplified compiler pipeline.
const pipeline = ["scanner", "parser", "binder", "checker", "emitter"] as const;
type Stage = (typeof pipeline)[number];

function isBeforeEmit(stage: Stage): boolean {
  return stage !== "emitter";
}
```

## Key points

- The compiler is written in TypeScript and runs on Node.js.
- It reads `tsconfig.json` to determine files, options, and output.
- The checker validates the program after binding symbols and types.
- The emitter writes JavaScript, source maps, and optionally `.d.ts` files.
- `tsc` does not bundle modules, minify output, or add polyfills.
- Incremental and project-reference builds reduce repeated work.

## Gotchas

- `tsc` can emit output even when type errors are reported.
- `tsc` is not a bundler; browser module resolution still needs a build tool.
- The emitted JavaScript may rely on features missing from older runtimes.

## Best practice

- Separate type-checking (`tsc --noEmit`) from bundling in application builds.
- Enable `noEmitOnError` when `tsc` is responsible for production output.
