# `extends` in Configuration

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `extends` chains configs from files or npm packages, and since TypeScript 5.0 it accepts an array for layered overrides.

## Syntax
```json
{
  "extends": "./tsconfig.base.json"
}
```

```json
{
  "extends": ["@tsconfig/strictest/tsconfig.json", "./tsconfig.local.json"]
}
```

## Examples
### Basic
```json
// tsconfig.json
{
  "extends": "./configs/tsconfig.base.json",
  "compilerOptions": {
    "outDir": "dist"
  }
}
```

```bash
npx tsc -p tsconfig.json
```

### Practical
```json
// tsconfig.json
{
  "extends": "@tsconfig/node22/tsconfig.json",
  "compilerOptions": {
    "rootDir": "src",
    "outDir": "dist",
    "declaration": true
  },
  "include": ["src/**/*.ts"]
}
```

```bash
npm install --save-dev @tsconfig/node22
```

### Advanced / edge cases
```json
// tsconfig.json — later entries win
{
  "extends": [
    "@tsconfig/strictest/tsconfig.json",
    "@tsconfig/node22/tsconfig.json",
    "./tsconfig.paths.json"
  ],
  "compilerOptions": {
    "noEmit": true
  }
}
```

```json
// Resolving a base inside node_modules without the package name
{
  "extends": "./node_modules/@tsconfig/recommended/tsconfig.json"
}
```

```json
// Circular extends is an error
{
  "extends": "./tsconfig.json"
}
```

## Key points
- `extends` accepts a relative path, an absolute path, or a package specifier.
- Package specifiers resolve like Node modules, including `exports` and `node_modules`.
- Array form (TS 5.0+) applies configs left to right; the last writer wins.
- `references` is not inherited; declare project references in each config.
- The child config may override any inherited top-level field.

## Gotchas
- A circular `extends` chain fails with a configuration error.
- Package-provided configs may pin `target`/`module` that conflict with your runtime.
- Relative `include` paths in a base are resolved from the base file's directory.

## Best practice
- Prefer published `@tsconfig/*` bases for runtime defaults, then layer a repo base for policy.
- Keep the chain short and verify the merged result with `--showConfig`.
