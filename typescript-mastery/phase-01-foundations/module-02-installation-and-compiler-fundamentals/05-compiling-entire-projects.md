# Compiling Entire Projects

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Let a `tsconfig.json` define the file set and options, then compile the whole program with one command.

## Syntax
```bash
tsc
tsc -p tsconfig.json
```

## Examples
### Basic
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
  "include": ["src/**/*.ts"]
}
```

```bash
npx tsc -p tsconfig.json
```

### Practical
```json
{
  "scripts": {
    "clean": "rm -rf dist",
    "build": "npm run clean && tsc -p tsconfig.json",
    "typecheck": "tsc -p tsconfig.json --noEmit"
  }
}
```

```bash
npm run build
find dist -name '*.js' | sort
```

### Advanced / edge cases
```json
{
  "files": ["src/index.ts"],
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "dist"
  }
}
```

```bash
# A monorepo root that only orchestrates referenced projects
npx tsc -b packages/*/tsconfig.json

# Inspect the exact file set the project compiles
npx tsc -p tsconfig.json --listFiles
```

## Key points
- A project is the set of root files from `files`/`include` plus their transitive imports.
- One config yields one consistent set of options for the whole program.
- `tsc` walks up from the working directory to find the nearest `tsconfig.json`.
- Use `--listFiles` and `--explainFiles` to understand program membership.
- Large repos should split into referenced projects and compile with build mode.

## Gotchas
- A config without `files` or `include` defaults to `**/*`, which may pull in unexpected files.
- Adding a new top-level folder can change the program silently; pin `include` explicitly.
- `outDir` is not cleaned automatically, so deleted sources leave stale output behind.

## Best practice
- Keep one `tsconfig.json` per package and a root config that references them.
- Run `--noEmit` in CI and a clean emit for release builds.
