# TypeScript Project Structure

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — A TypeScript project separates source, build output, tests, configuration, and declarations into predictable locations.

## Syntax

```ts
// src/index.ts
export const appName: string = "demo";
```

## Examples

### Basic

```ts
// project/
// ├── src/
// │   ├── index.ts
// │   └── lib/
// ├── tests/
// ├── dist/
// ├── tsconfig.json
// └── package.json
```

### Practical

```ts
// src/lib/math.ts
export function sum(values: number[]): number {
  return values.reduce((a, b) => a + b, 0);
}

// src/index.ts imports from "./lib/math"
const total = sum([1, 2, 3]); // => 6
```

### Advanced / edge cases

```ts
const tsconfig = {
  compilerOptions: {
    rootDir: "src",
    outDir: "dist",
    strict: true,
    declaration: true,
    sourceMap: true,
  },
  include: ["src/**/*.ts"],
  exclude: ["node_modules", "dist"],
} as const;
```

## Key points

- Keep source in `src/` and generated output in `dist/` or `build/`.
- `rootDir` and `outDir` preserve a predictable output tree.
- Tests can live beside source or in a separate `tests/` directory.
- Libraries often emit `.d.ts` files alongside JavaScript.
- `dist/` is usually generated and excluded from version control.
- Shared code belongs in a workspace package rather than deep relative imports.

## Gotchas

- Importing from `dist/` creates circular build dependencies and stale types.
- Files outside `rootDir` cause output-path errors or unexpected nesting.
- An overly narrow `include` silently omits files from type checking.

## Best practice

- Keep one clear source root and one generated output root.
- Commit `tsconfig.json` and ignore generated directories and build metadata.
