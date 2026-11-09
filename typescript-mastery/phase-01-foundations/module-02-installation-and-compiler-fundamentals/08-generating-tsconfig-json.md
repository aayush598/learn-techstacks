# Generating `tsconfig.json`

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Use `tsc --init` to scaffold a commented `tsconfig.json`, then trim it to the options you actually need.

## Syntax
```bash
tsc --init
```

## Examples
### Basic
```bash
npx tsc --init
```

```json
{
  "compilerOptions": {
    "target": "es2016",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Practical
```bash
# Scaffold, then replace the generated file with a project-specific one
npx tsc --init
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "rootDir": "src",
    "outDir": "dist",
    "sourceMap": true,
    "declaration": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

### Advanced / edge cases
```bash
# Fail instead of overwriting an existing config
npx tsc --init

# Generate into a non-default path, then point tsc at it
npx tsc --init --project ./configs/tsconfig.base.json
```

```json
{
  "scripts": {
    "init:ts": "tsc --init",
    "build": "tsc -p tsconfig.json"
  }
}
```

## Key points
- `tsc --init` creates `tsconfig.json` in the current directory (or the `--project` path).
- The generated file is heavily commented and includes many disabled options.
- Defaults in the scaffold are conservative, not necessarily right for your runtime.
- It refuses to overwrite an existing config; delete or rename first.
- The generated file is a starting point — review every option you keep.

## Gotchas
- The scaffold may target an older ECMAScript version than your runtime supports.
- Commented options in the generated file are documentation, not active configuration.
- `--init` writes a config even in a directory with no sources, so add `include` yourself.

## Best practice
- Generate once, then replace boilerplate with a minimal, explicit config.
- Commit the final config so every contributor and CI run uses identical settings.
