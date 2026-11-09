# Compiler Defaults

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — With no config, `tsc` uses permissive legacy defaults, so always set your important options explicitly.

## Syntax
```bash
tsc --showConfig
tsc --all
```

## Examples
### Basic
```json
{
  "compilerOptions": {
    "target": "ES5",
    "module": "CommonJS",
    "strict": false,
    "esModuleInterop": false,
    "skipLibCheck": false,
    "declaration": false,
    "sourceMap": false,
    "noEmit": false
  }
}
```

### Practical
```bash
# See the resolved defaults plus your overrides
npx tsc --showConfig
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Advanced / edge cases
```bash
# Compare defaults across versions after upgrading TypeScript
npx tsc --version
npx tsc --showConfig > before.json

# A single flag changes downstream defaults (module implies moduleResolution)
npx tsc -p tsconfig.json --module NodeNext --showConfig
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Key points
- Defaults are chosen for maximum compatibility, not safety.
- `strict` defaults to `false`; all strict-family checks are off unless enabled.
- `target` defaults to `ES5` in TypeScript 5.x, downleveling modern syntax.
- `module` defaults to `CommonJS`, with Node-style resolution.
- `outDir` is unset, so output lands next to each source file.
- `--showConfig` prints the effective configuration, defaults included.

## Gotchas
- Defaults change between major TypeScript versions; never rely on them implicitly.
- Enabling `strict` turns on a family of checks at once, which can surface many errors at once.
- `moduleResolution` is often inferred from `module`, so setting only one can surprise you.

## Best practice
- Write every behavior-critical option into `tsconfig.json` rather than depending on defaults.
- Review `--showConfig` after upgrades and commit the effective config when it matters.
