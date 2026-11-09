# Compiling Individual TypeScript Files

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Pass file paths to `tsc` to compile just those files, remembering that this mode ignores `tsconfig.json`.

## Syntax
```bash
tsc src/index.ts
tsc src/a.ts src/b.ts --outDir dist
```

## Examples
### Basic
```bash
# Emits src/index.js next to the source
npx tsc src/index.ts
```

```ts
// src/index.ts
const greeting: string = "hello";
console.log(greeting);
```

```js
// emitted src/index.js (default target downlevels as needed)
var greeting = "hello";
console.log(greeting);
```

### Practical
```bash
# Compile several entry files into one output directory
npx tsc src/index.ts src/math.ts \
  --outDir dist \
  --target ES2022 \
  --module NodeNext \
  --strict
```

### Advanced / edge cases
```bash
# Imports are followed even when only the entry file is listed
npx tsc src/index.ts --outDir dist

# Watch an explicit file list
npx tsc src/index.ts src/math.ts --watch

# Verify that a project config is NOT being used
npx tsc src/index.ts --showConfig
```

```ts
// src/index.ts imports ./math; math.ts is compiled too
import { add } from "./math.js";
console.log(add(2, 3));
```

## Key points
- File arguments define the root files; imported files join the program automatically.
- When files are passed, `tsconfig.json` is ignored unless `-p` is also used.
- Output paths mirror the input paths unless `--outDir` is set.
- Useful for quick experiments and single-file scripts, not for whole applications.
- Defaults apply (target, module, strictness), so results differ from a configured project.

## Gotchas
- `tsc src/index.ts` does not read `include`/`exclude` or `compilerOptions` from your config.
- `.d.ts` files can be listed but produce no JavaScript output.
- Missing imports still fail the build — listing a file does not make it self-contained.

## Best practice
- Use file-level compilation only for scratch work; use a project config for anything real.
- If you must mix both, add `-p` and let `include` select the files.
