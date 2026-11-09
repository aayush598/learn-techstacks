# Compiler Version Compatibility

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Pin TypeScript per project and align `target`, `lib`, and `@types` with the runtime and compiler version you actually ship.

## Syntax
```bash
npm install --save-dev --save-exact typescript@5.9.3
npx tsc --version
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "skipLibCheck": true
  }
}
```

## Examples
### Basic
```bash
npx tsc --version
node -p "require('typescript/package.json').version"
node --version
```

```json
{
  "engines": {
    "node": ">=20"
  },
  "devDependencies": {
    "typescript": "5.9.3"
  }
}
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
    "skipLibCheck": true,
    "types": ["node"]
  }
}
```

```json
{
  "devDependencies": {
    "@types/node": "^22.10.0",
    "typescript": "5.9.3"
  }
}
```

### Advanced / edge cases
```bash
# Upgrading: see which files and errors change before committing
npx tsc -p tsconfig.json --noEmit --pretty false > after.txt

# Compare against a specific older compiler
npx --package typescript@5.6.3 tsc -p tsconfig.json --noEmit
```

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true
  }
}
```

```bash
# Some options require a minimum compiler version
npx tsc -p tsconfig.json
# error TS6046: Argument for '--moduleResolution' option must be: ...
```

## Key points
- TypeScript versions are not fully interchangeable; options and defaults change between majors.
- `target` controls emitted syntax; `lib` controls which standard APIs type-check.
- `moduleResolution: "Bundler"` requires TypeScript 5.0 or newer.
- `@types/*` packages can require a minimum TypeScript version via `typesVersions`.
- Editors may bundle a different TypeScript than your project; select the workspace version.

## Gotchas
- A global or editor-bundled compiler can disagree with the pinned project version.
- Upgrading TypeScript can surface new errors with no source changes.
- `skipLibCheck` hides errors inside dependency declarations, not version mismatches in your own code.

## Best practice
- Pin TypeScript exactly, upgrade deliberately, and type-check before and after the bump.
- Keep `@types/node` aligned with the Node runtime and TypeScript version you support.
