# Incremental Compilation

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `incremental` caches program state in a `.tsbuildinfo` file so subsequent compiles only re-check what changed.

## Syntax
```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "dist/.tsbuildinfo"
  }
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "incremental": true,
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json
# writes dist/.tsbuildinfo alongside output
```

### Practical
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "incremental": true,
    "tsBuildInfoFile": "node_modules/.cache/tsbuildinfo/api.tsbuildinfo",
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

```json
{
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "clean": "rm -rf dist node_modules/.cache/tsbuildinfo"
  }
}
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "tsBuildInfoFile": "./dist/.tsbuildinfo",
    "rootDir": "src",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

```bash
# Watch mode is incremental by default
npx tsc -w -p tsconfig.json

# CI: restore the cache directory between runs
# cache key should include the TypeScript version and tsconfig hash
```

```bash
# A stale cache can be deleted safely; the next build recreates it
rm -f dist/.tsbuildinfo
```

## Key points
- `incremental` stores file hashes, diagnostics, and dependency info in `.tsbuildinfo`.
- Subsequent builds re-check only changed files and their dependents.
- `--watch` implies incremental behavior even without the flag.
- `tsBuildInfoFile` lets you move the cache out of `outDir`.
- `composite` projects are always incremental.

## Gotchas
- Do not edit `.tsbuildinfo` by hand; it is compiler-managed binary-ish JSON.
- A missing or mismatched cache just triggers a full rebuild — never a wrong build.
- Caches are not portable across TypeScript versions or different compiler options.

## Best practice
- Cache `.tsbuildinfo` in CI keyed by lockfile, tsconfig, and TypeScript version.
- Keep build info out of published artifacts and out of source control.
