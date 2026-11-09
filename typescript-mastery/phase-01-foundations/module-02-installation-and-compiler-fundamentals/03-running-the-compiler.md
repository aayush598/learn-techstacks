# Running the Compiler

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Run `tsc` directly, through `npx`, or from an npm script, and always know which config and options are in effect.

## Syntax
```bash
npx tsc
npx tsc --project tsconfig.json
npm run build
```

## Examples
### Basic
```bash
# Compile using tsconfig.json in the current directory
npx tsc

# Compile a specific project config
npx tsc -p ./tsconfig.build.json
```

### Practical
```json
{
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "watch": "tsc -p tsconfig.json --watch",
    "typecheck": "tsc -p tsconfig.json --noEmit"
  }
}
```

```bash
npm run build
node dist/index.js
```

### Advanced / edge cases
```bash
# CLI flags override the config for this run only
npx tsc -p tsconfig.json --outDir build --sourceMap

# Use a different working directory without changing config
npx tsc -p packages/api/tsconfig.json

# Fail fast in CI and show machine-friendly output
npx tsc -p tsconfig.json --noEmit --pretty false
```

```bash
# Exit code tells you whether compilation succeeded
npx tsc -p tsconfig.json
echo "exit code: $?"
```

## Key points
- `tsc` with no arguments searches upward for the nearest `tsconfig.json`.
- `-p` / `--project` accepts a directory or a config file path.
- CLI options override matching `compilerOptions` values from the config.
- Exit code `0` means success; non-zero means diagnostics were reported.
- Running through npm scripts guarantees the local compiler version is used.

## Gotchas
- Running `tsc file.ts` while expecting `tsconfig.json` settings silently ignores the config.
- Relative paths on the CLI resolve from the shell's working directory, not the config location.
- `tsc` does not watch or re-run unless you pass `--watch` or use an external runner.

## Best practice
- Put every compiler invocation behind an npm script so it is discoverable and consistent.
- Use `-p` explicitly in scripts to avoid ambiguity in monorepos.
