# TypeScript Playground

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — The TypeScript Playground runs the compiler in the browser and shows type errors, emitted JavaScript, and inferred types.

## Syntax

```ts
// https://www.typescriptlang.org/play
const message: string = "Hello, Playground";
console.log(message);
```

## Examples

### Basic

```ts
const values = [1, 2, 3];
const total = values.reduce((sum, value) => sum + value, 0); // => 6
```

### Practical

```ts
const values = [1, 2, 3];
//    ^? const values: number[]
```

### Advanced / edge cases

```ts
// The Playground can switch target, strictness, module, and compiler version.
const options = { strict: true, target: "ES2022" } as const;
```

## Key points

- The Playground compiles entirely in the browser using the TypeScript compiler.
- It shows diagnostics, hover types, and the emitted JavaScript side by side.
- Compiler options and TypeScript versions are configurable per session.
- Shareable URLs preserve code and settings for bug reports and questions.
- Twoslash comments such as `// ^?` display inferred types inline.

## Gotchas

- The Playground is not a Node.js sandbox; filesystem and native modules are unavailable.
- Package imports are limited unless they are available through the Playground's resolution.
- Playground defaults may differ from your project's `tsconfig.json`.

## Best practice

- Reduce a problem to the smallest Playground example before asking for help.
- Share a Playground link that includes the same compiler options as your project.
