# Section 03: Husky & Git Hooks

## Overview

Husky manages Git hooks for the voice agent platform, ensuring that every commit and push meets quality standards before reaching the repository. Combined with lint-staged, commitlint, and type-checking, Husky provides a safety net that catches issues at the earliest possible point — before code review.

## Git Hook Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Git Hook Execution Flow                          │
│                                                              │
│  git commit                                                  │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐     ┌──────────────────────┐               │
│  │ pre-commit   │────►│ lint-staged           │               │
│  │ (Husky)      │     │                      │               │
│  │              │     │  • ESLint on *.ts    │               │
│  │              │     │  • Prettier on all   │               │
│  │              │     │  • No fix? → abort   │               │
│  └──────┬──────┘     └──────────────────────┘               │
│         │                                                     │
│         ▼                                                     │
│  ┌─────────────┐     ┌──────────────────────┐               │
│  │ commit-msg   │────►│ commitlint            │               │
│  │ (Husky)      │     │                      │               │
│  │              │     │  • Check format      │               │
│  │              │     │  • Validate scope    │               │
│  │              │     │  • Bad format→ abort │               │
│  └──────┬──────┘     └──────────────────────┘               │
│         │                                                     │
│         ▼                                                     │
│  ┌─────────────┐                                             │
│  │ Commit       │                                             │
│  │ Created ✅   │                                             │
│  └─────────────┘                                             │
│                                                              │
│  git push                                                     │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────┐     ┌──────────────────────┐               │
│  │ pre-push     │────►│ Type check + tests    │               │
│  │ (Husky)      │     │  • turbo typecheck    │               │
│  │              │     │  • turbo test         │               │
│  │              │     │  • Fail→ abort push   │               │
│  └─────────────┘     └──────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Husky Setup

```bash
# Install Husky
pnpm add -D husky --workspace-root

# Initialize Git hooks directory
pnpm exec husky init

# The init command creates:
# .husky/
# ├── pre-commit
# ├── commit-msg
# └── pre-push
```

### package.json Scripts

```jsonc
{
  "scripts": {
    "prepare": "husky",
    "postinstall": "husky"
  }
}
```

The `prepare` script automatically installs Husky hooks when developers run `pnpm install`. This ensures hooks are always active without manual setup.

## Pre-commit Hook

```bash
#!/usr/bin/env sh
# .husky/pre-commit
. "$(dirname "$0")/_/husky.sh"

# Run lint-staged on staged files
pnpm exec lint-staged

# If lint-staged fails, abort the commit
if [ $? -ne 0 ]; then
  echo "❌ Pre-commit checks failed. Fix the issues and try again."
  exit 1
fi

echo "✅ Pre-commit checks passed."
```

## Commit-msg Hook

```bash
#!/usr/bin/env sh
# .husky/commit-msg
. "$(dirname "$0")/_/husky.sh"

# Validate commit message with commitlint
pnpm exec commitlint --edit "$1"

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Invalid commit message format."
  echo "Expected format: type(scope): description"
  echo "Examples:"
  echo "  feat(api): add call recording endpoint"
  echo "  fix(voice): resolve TTS timeout issue"
  echo "  chore(deps): update zod to v3.23"
  exit 1
fi
```

## Pre-push Hook

```bash
#!/usr/bin/env sh
# .husky/pre-push
. "$(dirname "$0")/_/husky.sh"

# Run type checking on affected packages
echo "🔍 Running type check..."
pnpm exec turbo typecheck --filter="[HEAD^1]"

if [ $? -ne 0 ]; then
  echo "❌ Type check failed. Fix type errors before pushing."
  exit 1
fi

# Run tests on affected packages
echo "🧪 Running tests..."
pnpm exec turbo test --filter="[HEAD^1]" -- --run

if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Fix failing tests before pushing."
  exit 1
fi

echo "✅ Pre-push checks passed."
```

## Hook Skip Mechanisms

Sometimes developers need to bypass hooks intentionally:

```bash
# Skip pre-commit and commit-msg hooks
git commit --no-verify -m "chore: wip"

# Skip pre-push hook
git push --no-verify

# Skip all hooks (environment variable)
HUSKY=0 git commit -m "chore: emergency fix"
```

The `--no-verify` flag should be used sparingly and never on the main branch. The `HUSKY=0` environment variable is useful in CI environments where hooks are already handled by the CI pipeline.

## CI Hook Validation

In CI, hooks are redundant since the CI pipeline runs the same checks. Configure Husky to skip in CI:

```bash
#!/usr/bin/env sh
# .husky/pre-commit

# Skip hooks in CI
if [ -n "$CI" ]; then
  exit 0
fi

. "$(dirname "$0")/_/husky.sh"
pnpm exec lint-staged
```

## Custom Hook for Branch Naming

```bash
#!/usr/bin/env sh
# .husky/pre-push (extended with branch naming check)
. "$(dirname "$0")/_/husky.sh"

BRANCH_NAME=$(git symbolic-ref HEAD 2>/dev/null | cut -d'/' -f3-)

# Validate branch name pattern
if [[ ! "$BRANCH_NAME" =~ ^(feature|fix|chore|docs|refactor)/[a-z0-9-]+$ ]]; then
  # Only warn for personal branches
  if [[ "$BRANCH_NAME" != "main" && "$BRANCH_NAME" != "staging" ]]; then
    echo "⚠️  Branch name does not follow convention."
    echo "Expected: type/description (e.g., feature/add-tts-support)"
    echo "Current: $BRANCH_NAME"
  fi
fi

# ... continue with type check and test hooks ...
```

## Hook Testing

```typescript
// packages/config/src/husky.test.ts
import { describe, it, expect } from "vitest";
import { execSync } from "child_process";

describe("Husky hooks", () => {
  it("pre-commit hook should exist", () => {
    const hooks = execSync("ls .husky/", { encoding: "utf-8" });
    expect(hooks).toContain("pre-commit");
  });

  it("commit-msg hook should exist", () => {
    const hooks = execSync("ls .husky/", { encoding: "utf-8" });
    expect(hooks).toContain("commit-msg");
  });

  it("pre-push hook should exist", () => {
    const hooks = execSync("ls .husky/", { encoding: "utf-8" });
    expect(hooks).toContain("pre-push");
  });

  it("hooks should be executable", () => {
    const preCommit = execSync("ls -la .husky/pre-commit", {
      encoding: "utf-8",
    });
    expect(preCommit).toMatch(/^-rwx/);
  });
});
```

## Design Decisions

### Pre-push hooks vs. CI-only checks

**Decision**: Run type checking and tests both pre-push AND in CI.

**Rationale**: Pre-push hooks catch issues before they reach the remote repository, saving time and preventing broken commits from blocking other developers. CI provides a more comprehensive check with environment isolation. The combination provides defense in depth.

### Why pre-push instead of pre-commit for type checking?

Type checking and tests take significantly longer than linting. Running them on every commit would be disruptive. Pre-push runs them once before the developer shares their changes with the team.

## Integration Points

- **lint-staged**: Called from pre-commit hook
- **commitlint**: Called from commit-msg hook
- **Turborepo**: Pre-push uses `turbo typecheck` and `turbo test`
- **CI pipeline**: Mirrors the same checks as local hooks
- **VS Code**: Editor integration with Git GUI

## Production Considerations

1. **Hook performance**: Keep pre-commit hooks fast (< 5 seconds). Move slow checks (type checking, full test suite) to pre-push
2. **Cross-platform**: Husky hooks use shell scripts. Ensure compatibility across macOS (zsh), Linux (bash), and Windows (Git Bash)
3. **Hook bypass audit**: Track `--no-verify` usage. If developers frequently bypass hooks, the hooks are too strict or the workflow is broken — investigate and adjust
4. **CI consistency**: CI should run the same checks as local hooks with the same configuration. Any discrepancy between hook and CI behavior erodes trust in the system
5. **Migration**: When migrating an existing project to hooks, communicate the change clearly. Schedule a team meeting to demonstrate the new workflow and provide a grace period for adaptation
