# Compiler Configuration Inheritance

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Put shared options in a base config and let package configs inherit and override them.

## Syntax
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "dist"
  }
}
```

## Examples
### Basic
```json
// tsconfig.base.json
{
  "compilerOptions": {
    "target": "ES2022",
    "strict": true,
    "skipLibCheck": true
  }
}
```

```json
// packages/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
```

### Practical
```json
// tsconfig.base.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

```json
// packages/web/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "noEmit": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"]
}
```

### Advanced / edge cases
```json
// packages/node-service/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "rootDir": "src",
    "outDir": "dist",
    "declaration": true,
    "composite": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

```bash
# Confirm the merged result for one package
npx tsc -p packages/node-service/tsconfig.json --showConfig
```

## Key points
- Child `compilerOptions` override the same keys from the base; other keys are inherited.
- `include`, `exclude`, and `files` are inherited too, but a child value replaces the base value.
- Relative paths are resolved relative to the config file that declares them.
- `extends` can point at a relative path or a package (`@tsconfig/node22`).
- Inheritance is shallow per key: objects like `paths` are replaced, not deep-merged.

## Gotchas
- If the child defines `include`, the base's `include` is ignored entirely.
- `outDir` inherited from a base resolves against the base config's directory, not the child's.
- Deeply nested bases make it hard to see the effective config; use `--showConfig`.

## Best practice
- Keep exactly one root base config for the repo and inherit from it everywhere.
- Put shared *policy* (strictness, libs) in the base and *layout* (rootDir/outDir) in packages.
