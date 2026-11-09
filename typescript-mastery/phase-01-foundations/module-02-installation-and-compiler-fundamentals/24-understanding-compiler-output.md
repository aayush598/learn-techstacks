# Understanding Compiler Output

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `tsc` emits JavaScript that mirrors your source structure, plus optional source maps, declarations, and build info — types are erased.

## Syntax
```bash
tsc -p tsconfig.json
tsc --listEmittedFiles
```

## Examples
### Basic
```ts
// src/index.ts
interface User {
  id: string;
  name: string;
}

const user: User = { id: "1", name: "Ada" };
console.log(user.name);
```

```js
// dist/index.js (target ES2022; types erased)
const user = { id: "1", name: "Ada" };
console.log(user.name);
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
    "sourceMap": true,
    "declaration": true
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json --listEmittedFiles
```

```text
TSFILE: /project/dist/index.js
TSFILE: /project/dist/index.js.map
TSFILE: /project/dist/index.d.ts
```

### Advanced / edge cases
```bash
# List every file in the program
npx tsc -p tsconfig.json --listFiles

# Explain why each file was included
npx tsc -p tsconfig.json --explainFiles

# Inspect the effective config that produced the output
npx tsc -p tsconfig.json --showConfig
```

```ts
// src/math.ts (target ES5)
export const add = (a: number, b: number): number => a + b;
```

```js
// dist/math.js (downleveled for ES5)
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.add = void 0;
var add = function (a, b) { return a + b; };
exports.add = add;
```

## Key points
- Types, interfaces, and annotations are erased; only runtime JavaScript remains.
- Output directory structure mirrors the source tree relative to `rootDir`.
- `sourceMap` adds `.js.map`; `declaration` adds `.d.ts`; `declarationMap` adds `.d.ts.map`.
- `target` changes emitted syntax (arrow functions, classes, optional chaining, etc.).
- `--listEmittedFiles` shows exactly what was written; `--explainFiles` shows why a file is in the program.

## Gotchas
- Output is not bundled: every source module becomes a separate output module and imports are preserved.
- `tsc` does not copy non-TypeScript assets such as JSON, CSS, or templates.
- Emitting with errors is allowed unless you set `noEmitOnError`.

## Best practice
- Treat `dist/` as a disposable artifact and rebuild it cleanly for releases.
- Inspect `--listEmittedFiles` and `--explainFiles` when output differs from expectations.
