# Include and Exclude Patterns

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `include` selects root files by glob and `exclude` filters that set, but neither prevents imported files from being compiled.

## Syntax
```json
{
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Examples
### Basic
```json
{
  "include": ["src"]
}
```

```bash
npx tsc -p tsconfig.json --listFiles
```

### Practical
```json
{
  "include": ["src/**/*.ts", "src/**/*.tsx", "types/**/*.d.ts"],
  "exclude": ["node_modules", "dist", "coverage", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Advanced / edge cases
```json
{
  "include": ["src/**/*.ts", "scripts/**/*.ts"],
  "exclude": ["src/generated/**", "scripts/fixtures/**"]
}
```

```json
{
  "compilerOptions": {
    "outDir": "dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "bower_components", "jspm_packages"]
}
```

```ts
// src/index.ts
// Even if src/internal is excluded, this import still compiles it
import { helper } from "./internal/helper.js";
console.log(helper());
```

## Key points
- `include` patterns are relative to the config file and support `*`, `?`, and `**/`.
- Directories are expanded to supported extensions (`.ts`, `.tsx`, `.d.ts`, and `.js` if allowed).
- Default `include` is `**/*` when neither `files` nor `include` is present.
- Default excludes are `node_modules`, `bower_components`, `jspm_packages`, and `outDir`.
- `exclude` only filters `include`; entries in `files` are always included.

## Gotchas
- A file imported by an included file is compiled even if it matches `exclude`.
- `exclude` does not affect type acquisition from `node_modules` or `types`.
- Negated `!` patterns are not a supported tsconfig feature; use explicit includes instead.

## Best practice
- Use a narrow `include` (`src/**/*.ts`) instead of relying on the broad default.
- Keep tests either in `include` for type-checking or excluded from the emit build, not both.
