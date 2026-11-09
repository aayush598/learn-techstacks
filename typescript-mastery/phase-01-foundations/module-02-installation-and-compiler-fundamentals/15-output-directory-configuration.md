# Output Directory Configuration

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `outDir` redirects emitted files into one directory that mirrors the source tree relative to `rootDir`.

## Syntax
```json
{
  "compilerOptions": {
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
# src/index.ts -> dist/index.js
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
    "sourceMap": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

```json
{
  "scripts": {
    "clean": "rm -rf dist",
    "build": "npm run clean && tsc -p tsconfig.json"
  }
}
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "outDir": "dist",
    "outFile": "dist/bundle.js",
    "module": "AMD"
  },
  "include": ["src/**/*.ts"]
}
```

```bash
# outFile only works with AMD or System modules; CommonJS fails
npx tsc -p tsconfig.json
# error TS6082: Only 'amd' and 'system' modules are supported alongside '--outFile'.
```

```json
{
  "compilerOptions": {
    "outDir": "dist",
    "noEmit": true
  }
}
```

## Key points
- `outDir` receives all emitted `.js`, `.d.ts`, `.map`, and build info files (unless overridden).
- Directory structure is preserved relative to `rootDir`.
- `outDir` is excluded from `include` automatically, but keep it in `exclude` for clarity.
- `declarationDir` can separate type declarations from JavaScript.
- `outFile` is a different feature: it concatenates into one file and needs AMD/System.

## Gotchas
- `outDir` is never cleaned; stale files from deleted sources remain until you remove it.
- Setting both `outDir` and `noEmit` is legal but nothing is written.
- `outFile` is not a bundler and does not support CommonJS or ESM output.

## Best practice
- Clean `outDir` before every release build.
- Keep `dist/` in `.gitignore` and treat emitted files as build artifacts.
