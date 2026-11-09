# Understanding Compiler Arguments

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Every CLI flag maps to a `compilerOptions` key, and flags passed on the command line override the config.

## Syntax
```bash
tsc --target ES2022 --module NodeNext --strict --outDir dist
tsc --noEmit
tsc --project tsconfig.json --pretty false
```

## Examples
### Basic
```bash
npx tsc src/index.ts \
  --target ES2022 \
  --module CommonJS \
  --strict \
  --outDir dist
```

### Practical
```bash
# Boolean flags: presence = true, --flag false = false
npx tsc -p tsconfig.json --sourceMap --declaration
npx tsc -p tsconfig.json --strict false

# Check-only invocation for CI
npx tsc -p tsconfig.json --noEmit --pretty false
```

### Advanced / edge cases
```bash
# See every option the compiler supports
npx tsc --all

# Inspect the resolved config after merging CLI + tsconfig
npx tsc -p tsconfig.json --showConfig

# Performance and tracing flags
npx tsc -p tsconfig.json --extendedDiagnostics
npx tsc -p tsconfig.json --generateTrace ./trace

# Scaffolding and build-mode flags
npx tsc --init
npx tsc -b --verbose
```

## Key points
- CLI flags use camelCase: `--outDir`, `--noEmit`, `--moduleResolution`.
- Command-line values override `tsconfig.json` for that invocation only.
- `--help` lists common options; `--all` lists everything.
- Some flags only apply to specific modes, e.g. `--outFile` requires `amd`/`system`.
- `--showConfig` is the ground truth for what the compiler will actually do.

## Gotchas
- Misspelled flags fail with `TS5023: Unknown compiler option`.
- `--strict false` is valid, but `--strict=false` may not be parsed as you expect in all shells.
- Passing files alongside options disables project config loading; add `-p` if you need both.

## Best practice
- Keep persistent options in `tsconfig.json`; use CLI flags only for one-off overrides and CI checks.
- Document non-obvious flags in npm scripts rather than tribal knowledge.
