# TypeScript File Extensions: `.ts`, `.tsx`, `.d.ts`, `.mts`, `.cts`

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — The extension signals both syntax and module semantics: `.ts` is standard, `.tsx` enables JSX, `.d.ts` declares types, `.mts` is ESM, and `.cts` is CommonJS.

## Syntax

```ts
// src/app.ts — the default TypeScript extension
export const appName: string = "demo";
```

## Examples

### Basic

```ts
// src/math.ts
export function sum(values: number[]): number {
  return values.reduce((a, b) => a + b, 0);
}
```

### Practical

```ts
// src/Button.tsx — JSX is enabled only in .tsx files
// const element = <button>Save</button>;
type ButtonProps = { label: string };

export function buttonProps(label: string): ButtonProps {
  return { label };
}
```

### Advanced / edge cases

```ts
// types/env.d.ts — declarations only, no runtime code
declare const BUILD_VERSION: string;

// src/config.mts — always ESM
export const mode = "esm" as const;

// src/legacy.cts — always CommonJS (commented to keep this file valid)
// const legacyMode = "cjs" as const;
// export = { legacyMode };
```

## Key points

- `.ts` — standard TypeScript with no JSX; the default for most files.
- `.tsx` — TypeScript with JSX enabled; use for React and other JSX dialects.
- `.d.ts` — declaration files that describe types without runtime code.
- `.mts` — always an ES module, emitting `.mjs`.
- `.cts` — always a CommonJS module, emitting `.cjs`.
- Under `NodeNext`, import specifiers must match emitted extensions such as `.mjs` and `.cjs`.

## Gotchas

- `.d.ts` files cannot contain executable statements or initializers that emit code.
- Angle-bracket assertions such as `<T>value` conflict with JSX in `.tsx`; use `value as T`.
- Importing `./config.ts` under `NodeNext` is wrong; import the emitted `./config.mjs`.

## Best practice

- Use `.ts` by default, `.tsx` only when the file contains JSX, and `.d.ts` for external contracts.
- Choose `.mts` or `.cts` only when a file must force a specific module system.
