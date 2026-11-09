# Project Root Configuration

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `rootDir` sets the root of your source tree, which fixes the output layout and rejects files that live outside it.

## Syntax
```json
{
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist"
  }
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json
# src/index.ts        -> dist/index.js
# src/utils/math.ts   -> dist/utils/math.js
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
    "sourceMap": true
  },
  "include": ["src/**/*.ts"]
}
```

```bash
# Confirm the computed common source directory
npx tsc -p tsconfig.json --showConfig
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts", "scripts/**/*.ts"]
}
```

```bash
# error TS6059: File 'scripts/build.ts' is not under 'rootDir' 'src'.
# 'rootDir' is expected to contain all source files.
```

```json
{
  "compilerOptions": {
    "rootDir": ".",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts", "scripts/**/*.ts"]
}
```

## Key points
- `rootDir` is the directory all source files must live under.
- Output structure is computed relative to `rootDir`, preserving subdirectories.
- If unset, TypeScript uses the longest common path of all input files.
- It does not select files; `files`/`include` do that.
- `rootDir` affects emitted `.js`, `.d.ts`, and source map paths.

## Gotchas
- Adding a file outside `rootDir` fails with `TS6059`; widen `rootDir` or move the file.
- An unset `rootDir` can shift the output layout when a new top-level source folder appears.
- `rootDir` must be a concrete directory, not a glob.

## Best practice
- Set `rootDir: "src"` explicitly for applications to keep `dist/` flat and predictable.
- Use `rootDirs` only for virtual merging, not as a substitute for a clean source tree.
