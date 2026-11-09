# Declaration-Only Compilation

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `declaration` + `emitDeclarationOnly` produces only `.d.ts` files, the public type surface consumers need.

## Syntax
```bash
tsc --declaration --emitDeclarationOnly
```

```json
{
  "compilerOptions": {
    "declaration": true,
    "emitDeclarationOnly": true
  }
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "declaration": true,
    "emitDeclarationOnly": true,
    "rootDir": "src",
    "outDir": "dist/types"
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json
# src/index.ts -> dist/types/index.d.ts (no .js)
```

### Practical
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "rootDir": "src",
    "outDir": "dist",
    "declaration": true,
    "declarationDir": "dist/types",
    "declarationMap": true,
    "emitDeclarationOnly": true
  },
  "include": ["src/**/*.ts"]
}
```

```ts
// src/index.ts
export interface User {
  id: string;
  name: string;
}

export function getUser(id: string): Promise<User> {
  return Promise.resolve({ id, name: "Ada" });
}
```

```ts
// dist/types/index.d.ts (emitted)
export interface User {
    id: string;
    name: string;
}
export declare function getUser(id: string): Promise<User>;
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "declaration": true,
    "emitDeclarationOnly": true,
    "stripInternal": true,
    "outDir": "dist/types"
  },
  "include": ["src/**/*.ts"]
}
```

```ts
// @internal members are removed from .d.ts when stripInternal is on
export class Client {
  /** @internal */
  reset(): void {}
  connect(): void {}
}
```

```bash
# Typical library pipeline: bundler emits JS, tsc emits types
npx tsc -p tsconfig.types.json
npx vite build
```

## Key points
- `emitDeclarationOnly` requires `declaration: true`; it cannot be used alone.
- Output contains `.d.ts` (and optionally `.d.ts.map`) but no `.js`.
- `declarationDir` separates types from JavaScript output.
- Only exported declarations appear in the public type surface.
- `stripInternal` removes `/** @internal */` members from declarations.

## Gotchas
- Private or unexported types referenced by exports can force unexpected type exposure.
- Declaration emit can fail with `TS4023` when an exported type cannot be named.
- `emitDeclarationOnly` and `noEmit` are mutually exclusive.

## Best practice
- Ship `.d.ts` files generated from the same source as the JavaScript.
- Publish `types` (or `exports.types`) in `package.json` pointing at the declaration entry.
