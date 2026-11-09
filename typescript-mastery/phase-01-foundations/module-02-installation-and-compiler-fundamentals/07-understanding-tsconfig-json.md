# Understanding `tsconfig.json`

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — `tsconfig.json` is the project file that marks the project root and configures which files compile and how.

## Syntax
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
    "sourceMap": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "strict": true
  },
  "include": ["src"]
}
```

```bash
npx tsc -p tsconfig.json
```

### Practical
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "rootDir": "src",
    "outDir": "dist",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Advanced / edge cases
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"],
  "references": [{ "path": "../shared" }]
}
```

```json
{
  "compilerOptions": {},
  "files": []
}
```

## Key points
- The presence of `tsconfig.json` defines the project root and the base for relative paths.
- Top-level fields: `compilerOptions`, `files`, `include`, `exclude`, `extends`, `references`.
- Paths inside the file resolve relative to the file's own directory.
- Comments and trailing commas are allowed (JSONC), unlike strict JSON.
- Unknown options are errors, which catches typos early.

## Gotchas
- A `tsconfig.json` with no `include`/`files` compiles `**/*`, including files you did not intend.
- `exclude` does not stop an imported file from being compiled.
- `extends` changes which directory relative paths are based on; see the inheritance topics.

## Best practice
- Start strict (`"strict": true`) and add opt-in checks as the codebase matures.
- Keep one config per package; use `extends` for shared settings instead of copy-paste.
