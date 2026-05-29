# Section 06: Monorepo Scripts & Task Running

## Overview

A well-organized set of root-level scripts is essential for developer productivity in a monorepo. Combined with pnpm's filtering and Turborepo's task orchestration, scripts provide a uniform interface for building, testing, and deploying across all workspaces.

## Root Package Scripts

```jsonc
{
  "scripts": {
    // ── Development ────────────────────────────────────────
    "dev": "turbo dev",
    "dev:web": "turbo dev --filter=@voice-agent/web",
    "dev:api": "turbo dev --filter=@voice-agent/api",
    "dev:packages": "turbo dev --filter='./packages/*'",
    "dev:types": "turbo dev --filter=@voice-agent/types",
    "dev:db": "turbo dev --filter=@voice-agent/db",
    "dev:storybook": "turbo dev --filter=@voice-agent/ui storybook",

    // ── Build ──────────────────────────────────────────────
    "build": "turbo build",
    "build:web": "turbo build --filter=@voice-agent/web",
    "build:api": "turbo build --filter=@voice-agent/api",
    "build:packages": "turbo build --filter='./packages/*'",
    "build:affected": "turbo build --filter='[HEAD^1]'",

    // ── Quality ────────────────────────────────────────────
    "lint": "turbo lint",
    "lint:fix": "turbo lint -- --fix",
    "typecheck": "turbo typecheck",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md,yaml,yml}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md,yaml,yml}\"",

    // ── Test ───────────────────────────────────────────────
    "test": "turbo test",
    "test:unit": "turbo test -- --run",
    "test:integration": "turbo test --filter=@voice-agent/api -- --run integration",
    "test:e2e": "turbo test --filter=@voice-agent/web e2e",
    "test:coverage": "turbo test -- --coverage",
    "test:affected": "turbo test --filter='[HEAD^1]'",

    // ── Database ───────────────────────────────────────────
    "db:generate": "pnpm --filter=@voice-agent/db run db:generate",
    "db:migrate": "pnpm --filter=@voice-agent/db run db:migrate",
    "db:push": "pnpm --filter=@voice-agent/db run db:push",
    "db:seed": "pnpm --filter=@voice-agent/db run db:seed",
    "db:reset": "pnpm --filter=@voice-agent/db run db:reset",
    "db:studio": "pnpm --filter=@voice-agent/db run db:studio",

    // ── Docker ─────────────────────────────────────────────
    "docker:up": "docker compose -f docker/docker-compose.yml up -d",
    "docker:down": "docker compose -f docker/docker-compose.yml down",
    "docker:logs": "docker compose -f docker/docker-compose.yml logs -f",
    "docker:rebuild": "docker compose -f docker/docker-compose.yml up -d --build",

    // ── Clean ──────────────────────────────────────────────
    "clean": "turbo clean",
    "clean:all": "turbo clean && rm -rf node_modules && pnpm store prune",
    "reset": "turbo clean && rm -rf node_modules && pnpm install",

    // ── Dependency Management ──────────────────────────────
    "outdated": "pnpm outdated -r",
    "update": "pnpm update -r --latest",
    "audit": "pnpm audit --audit-level=high",
    "dedupe": "pnpm dedupe",
    "why": "pnpm why",

    // ── CI ─────────────────────────────────────────────────
    "ci:setup": "pnpm install --frozen-lockfile",
    "ci:validate": "pnpm install --frozen-lockfile && pnpm audit --audit-level=high",
    "ci:checks": "turbo lint typecheck test build",
    "ci:full": "pnpm ci:validate && pnpm ci:checks"
  }
}
```

## pnpm Filtering Patterns

```bash
# Basic filtering
pnpm --filter @voice-agent/web build

# Filter by directory
pnpm --filter ./packages/* test

# Filter by glob
pnpm --filter "./packages/**" lint

# Filter by git changes
pnpm --filter "[HEAD^1]" build         # Changed since last commit
pnpm --filter "[main...HEAD]" test     # Changed since branching

# Include dependencies
pnpm --filter "@voice-agent/api..." build
# ^ Build @voice-agent/api AND all its dependencies

# Include dependents
pnpm --filter "...@voice-agent/db" test
# ^ Test @voice-agent/db AND everything that depends on it

# Exclude specific packages
pnpm --filter "!@voice-agent/ui" build
```

## Common Task Patterns

### Running Commands Across All Packages

```bash
# List all workspace packages
pnpm ls -r --depth=0 --json | jq '.[].name'

# Add a script to all packages
for pkg in apps/* packages/*; do
  if [ -f "$pkg/package.json" ]; then
    node -e "
      const pkg = require('./$pkg/package.json');
      pkg.scripts = pkg.scripts || {};
      pkg.scripts.typecheck = 'tsc --noEmit';
      require('fs').writeFileSync('./$pkg/package.json', JSON.stringify(pkg, null, 2));
    "
  fi
done

# Check package version consistency
pnpm ls -r --depth=0 --json | jq '[.[] | {name: .name, version: .version}]'
```

### Parallel vs. Sequential Execution

```bash
# Parallel execution across all packages
pnpm -r --parallel exec -- node -e "console.log(process.cwd())"

# Sequential execution (respecting dependency order)
pnpm -r exec -- node -e "console.log(process.cwd())"

# Run with concurrency limit
pnpm -r --workspace-concurrency=4 exec -- node build.js
```

## Turborepo Integration

Turborepo commands complement pnpm filtering:

```bash
# Turbo with filters
turbo build --filter=@voice-agent/web

# Run tasks in dependency order
turbo build --filter="@voice-agent/api..."

# Run tasks for changed packages
turbo build --filter="[HEAD^1]"

# Continue on error
turbo test --continue

# Dry run — show what would be executed
turbo build --dry-run

# Show dependency graph
turbo build --graph

# Profile execution
turbo build --profile=profile.json
```

## Predefined Scripts in Packages

Each package should define consistent scripts that the root scripts delegate to:

```jsonc
// packages/db/package.json
{
  "scripts": {
    "build": "tsc && prisma generate",
    "dev": "tsc --watch",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "clean": "rm -rf dist .turbo"
  }
}

// apps/web/package.json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "e2e": "playwright test",
    "clean": "rm -rf .next dist .turbo"
  }
}
```

## Custom Script Helpers

```javascript
// scripts/affected-packages.js
// Helper to get packages affected by changes
const { execSync } = require("child_process");

function getAffectedPackages(base = "main") {
  const changedFiles = execSync(`git diff --name-only ${base}...HEAD`, {
    encoding: "utf-8",
  }).trim().split("\n");

  const workspacePackages = execSync(
    "pnpm ls -r --depth=0 --json",
    { encoding: "utf-8" }
  );

  const packages = JSON.parse(workspacePackages);
  return packages.filter((pkg) => {
    const packagePath = pkg.path;
    return changedFiles.some((file) => file.startsWith(packagePath));
  });
}

const affected = getAffectedPackages();
console.log(affected.map((p) => p.name).join("\n"));
```

## Script Composition Patterns

```bash
# Chained scripts with &&
pnpm ci:setup && pnpm ci:checks

# Conditional execution
pnpm test -- --coverage || echo "Tests failed, but continuing..."

# Timeout wrapper
timeout 300 pnpm build

# Resource limits
NODE_OPTIONS="--max-old-space-size=4096" pnpm build

# Environment-specific commands
NODE_ENV=production pnpm build
```

## Design Decisions

### Root scripts vs. package-local scripts

**Decision**: Centralize orchestration in root scripts, but implement the actual logic in package-local scripts.

**Rationale**: Root scripts provide a uniform interface (`pnpm dev`), while package-local scripts allow each package to have its own implementation. This separation means:
- A new developer can run `pnpm dev` without knowing which packages exist
- Each package can change its dev server without changing the root API
- CI uses the same root scripts, ensuring local/CI parity

### pnpm exec vs. npx

Use `pnpm exec` for workspace-aware command execution. It respects the workspace's `node_modules/.bin` and PATH:

```bash
# Good — workspace-aware
pnpm exec vitest run

# Avoid — might pick global installation
npx vitest run
```

## Integration Points

- **CI/CD**: All CI jobs use root scripts (`pnpm ci:setup`, `pnpm ci:checks`)
- **Developer onboarding**: Root scripts are the single entry point
- **Pre-commit hooks**: Scripts like `lint-staged` delegate to pnpm filtering
- **Deployment**: Build and test scripts are used in the deployment pipeline

## Production Considerations

1. **Script naming conventions**: Use a consistent prefix system: `ci:`, `db:`, `docker:`, `dev:`. This makes script discovery easier
2. **Completion times**: Long-running scripts should provide feedback. Use `--concurrency` limits to prevent resource exhaustion
3. **Cross-platform**: Avoid bash-specific syntax in root scripts. Use Node.js scripts for complex logic and rely on `npm-run-all` or `concurrently` for parallel execution
4. **Error handling**: Scripts that fail should exit non-zero. The `--continue` flag in Turbo allows running all tasks despite failures, but use it intentionally
5. **CI vs. local divergence**: Keep CI scripts identical to local scripts. If CI needs extra steps, add them as CI-specific scripts that compose the base scripts
