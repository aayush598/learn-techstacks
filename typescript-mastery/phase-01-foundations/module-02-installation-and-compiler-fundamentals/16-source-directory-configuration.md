# Source Directory Configuration

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `rootDirs` declares several source roots that TypeScript treats as one virtual directory, useful when generated and handwritten files are split.

## Syntax
```json
{
  "compilerOptions": {
    "rootDirs": ["src", "generated"]
  }
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "rootDirs": ["src", "generated"],
    "outDir": "dist"
  },
  "include": ["src/**/*.ts", "generated/**/*.ts"]
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
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "rootDirs": ["src", "generated"],
    "outDir": "dist"
  },
  "include": ["src/**/*.ts", "generated/**/*.ts"]
}
```

```ts
// src/index.ts
// src/schema.ts does not exist, so resolution falls through to generated/schema.ts
import { schema } from "./schema.js";
console.log(schema);
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "rootDirs": ["src", "build/generated"],
    "outDir": "dist"
  },
  "include": ["src/**/*.ts", "build/generated/**/*.ts"]
}
```

```ts
// Resolves to src/i18n/en.ts when present, otherwise build/generated/i18n/en.ts
import { messages } from "./i18n/en.js";
console.log(messages);
```

```json
{
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

If generated files live under `src/`, a single `rootDir` is enough and `rootDirs` is unnecessary.

## Key points
- `rootDirs` (plural) is a list of directories merged into one virtual root for module resolution.
- `rootDir` (singular) sets the output root; the two options serve different purposes.
- Relative imports are resolved against every `rootDirs` entry in order.
- Output paths are still governed by `rootDir`/common source directory, not `rootDirs`.
- Common use: `src` plus a generated-code directory that mirrors the same layout.

## Gotchas
- `rootDirs` does not make files compile on its own; they must still be in `files`/`include`.
- It affects resolution, not emit layout, so output may not mirror the virtual tree.
- Overlapping entries can resolve the same import to different files than you expect.

## Best practice
- Keep `rootDirs` entries aligned in structure so relative imports are unambiguous.
- Prefer generating code into `src/generated` and using a single `rootDir` when possible.
