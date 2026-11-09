# Installing TypeScript

> Phase 1 · Module 02 · Installation and Compiler Fundamentals

**TL;DR** — Install `typescript` as a local dev dependency so every machine and CI run uses the same `tsc` version.

## Syntax
```bash
npm install --save-dev typescript
npx tsc --version
```

## Examples
### Basic
```bash
# Create a project and install the compiler locally
mkdir my-app && cd my-app
npm init -y
npm install --save-dev typescript

# Run the locally installed binary
npx tsc --version
```

### Practical
```bash
# Pin an exact version for reproducible builds
npm install --save-dev --save-exact typescript@5.9.3

# Verify what will run in CI
npx tsc --version
node -p "require('typescript/package.json').version"
```

```json
{
  "name": "my-app",
  "private": true,
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build": "tsc -p tsconfig.json"
  },
  "devDependencies": {
    "typescript": "5.9.3"
  }
}
```

### Advanced / edge cases
```bash
# Other package managers
pnpm add -D typescript
yarn add -D typescript

# Clean, lockfile-exact install (CI)
npm ci

# Inspect the resolved binary without relying on PATH
./node_modules/.bin/tsc --version

# Global installs work but are not recommended
npm install -g typescript
```

## Key points
- `typescript` is a **dev dependency**: it is erased at runtime, so production installs do not need it.
- `npx tsc` resolves `node_modules/.bin/tsc` first, which keeps versions consistent.
- The package ships the compiler, the standard library `.d.ts` files, and the `tsc`/`tsserver` binaries.
- `npm ci` installs exactly what `package-lock.json` records — use it in CI.
- Editors (VS Code, etc.) can use their own bundled TypeScript; align it with the project version.

## Gotchas
- A stale global `tsc` can silently compile with different defaults than your local one.
- Installing without `--save-dev` makes TypeScript a production dependency that is never used at runtime.
- Version ranges like `^5.9.0` drift over time; use `--save-exact` for compiler-sensitive projects.

## Best practice
- Pin TypeScript exactly and commit the lockfile.
- Add `typecheck` and `build` scripts so local runs and CI use the same command.
