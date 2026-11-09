# Files Configuration

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `files` is an explicit, non-glob list of root files that are always included in the program.

## Syntax
```json
{
  "files": ["src/index.ts", "src/globals.d.ts"]
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "strict": true,
    "outDir": "dist"
  },
  "files": ["src/index.ts"]
}
```

```bash
npx tsc -p tsconfig.json --listFiles
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
    "outDir": "dist"
  },
  "files": ["src/index.ts", "src/global.d.ts"],
  "exclude": ["node_modules", "dist"]
}
```

```ts
// src/index.ts — only the entry point is listed; imports join the program
import { start } from "./server.js";
start();
```

### Advanced / edge cases
```json
{
  "files": ["src/main.ts"],
  "include": ["src/**/*.ts"],
  "exclude": ["**/*.test.ts"]
}
```

```json
{
  "files": [],
  "references": [{ "path": "./packages/core" }]
}
```

```bash
# A listed file that does not exist is a hard error
npx tsc -p tsconfig.json
# error TS6053: File 'src/missing.ts' not found.
```

## Key points
- `files` entries are exact paths relative to the config file — no glob patterns.
- Listed files are always part of the program, regardless of `exclude`.
- `files` and `include` can be combined; the union forms the root file set.
- An empty `files: []` is a common pattern for solution-style root configs.
- Imports still pull in additional files beyond the listed roots.

## Gotchas
- Globs in `files` are treated as literal filenames and fail with `TS6053`.
- A missing listed file stops the build even if other files are fine.
- Listing only `index.ts` does not isolate it — its imports are still compiled.

## Best practice
- Use `files` for a small, stable entry set or global `.d.ts` files.
- Use `include` for everything else; reserve `files` for what must always be present.
