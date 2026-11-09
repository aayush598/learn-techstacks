# Build Mode

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `tsc --build` compiles a graph of referenced projects in dependency order and skips anything already up to date.

## Syntax
```bash
tsc --build
tsc -b packages/core packages/api
tsc -b --clean
```

## Examples
### Basic
```json
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

```json
// packages/api/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "rootDir": "src",
    "outDir": "dist"
  },
  "references": [{ "path": "../core" }],
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -b packages/api/tsconfig.json
```

### Practical
```json
// tsconfig.json at the repo root
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/api" },
    { "path": "./packages/web" }
  ]
}
```

```json
{
  "scripts": {
    "build": "tsc -b",
    "clean": "tsc -b --clean",
    "watch": "tsc -b --watch"
  }
}
```

### Advanced / edge cases
```bash
# Rebuild everything, ignoring up-to-date checks
npx tsc -b --force

# Show what build mode is doing and why
npx tsc -b --verbose

# Report what would build without writing anything
npx tsc -b --dry

# Remove outputs and build info for the whole graph
npx tsc -b --clean
```

```json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "tsBuildInfoFile": "./dist/.tsbuildinfo",
    "declaration": true,
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

## Key points
- Build mode requires referenced projects to set `"composite": true`.
- It topologically orders the graph so dependencies build before dependents.
- Up-to-date checks use `.tsbuildinfo`; unchanged projects are skipped.
- `--clean` deletes outputs and build info; `--force` rebuilds regardless of state.
- `--watch` works with `-b` to rebuild the whole graph on change.

## Gotchas
- Referencing a non-composite project fails with an error.
- `-b` largely ignores ad-hoc CLI compiler options; put settings in each tsconfig.
- `composite` implies `declaration` and `incremental`, so outputs include `.d.ts` and build info.

## Best practice
- Use a solution-style root config with `"files": []` and a `references` list.
- Run `tsc -b --clean && tsc -b` when outputs and caches get out of sync.
