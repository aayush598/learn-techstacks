# Section 07: CI Lint Checks

## Overview

Lint checks in CI ensure that every pull request meets the project's code quality standards before merging. By running ESLint, Prettier, and type checking in CI with the same configuration as local development, we prevent quality regressions and enforce consistency across all contributions.

## CI Lint Workflow

```yaml
# .github/workflows/lint.yml
name: Lint
on:
  pull_request:
    branches: [main, staging]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: ESLint
        run: pnpm lint
        env:
          NODE_ENV: development

      - name: Prettier Check
        run: pnpm format:check

      - name: TypeScript Type Check
        run: pnpm typecheck

      - name: Comment PR on failure
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `❌ Lint/Type checks failed. Please run \`pnpm lint\` and \`pnpm typecheck\` locally to see errors.`
            })
```

## Lint Result Annotations

ESLint and TypeScript errors can be surfaced directly in the PR diff using GitHub Annotations:

```yaml
# Use reviewdog for inline annotations
- name: Run ESLint with reviewdog
  uses: reviewdog/action-eslint@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    reporter: github-pr-review
    level: error
    filter_mode: diff_context
    fail_on_error: true
```

## Quality Gate Configuration

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate
on:
  pull_request:
    branches: [main]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install
        run: pnpm install --frozen-lockfile

      # ── Lint Quality Gate ─────────────────────────────────
      - name: Lint Check
        id: lint
        run: |
          if pnpm lint -- --max-warnings=0 2>&1 | tee lint-output.txt; then
            echo "status=pass" >> $GITHUB_OUTPUT
          else
            echo "status=fail" >> $GITHUB_OUTPUT
          fi

      # ── Diff-Based Linting ────────────────────────────────
      - name: Diff-Based Lint (Changed files only)
        run: |
          CHANGED_FILES=$(git diff --name-only origin/main...HEAD -- '*.ts' '*.tsx')
          if [ -n "$CHANGED_FILES" ]; then
            pnpm exec eslint $CHANGED_FILES --max-warnings=0
          fi

      # ── Type Check ────────────────────────────────────────
      - name: Type Check
        run: pnpm typecheck

      # ── Check for TODO/FIXME without tracking issues ─────
      - name: Check TODO/FIXME
        run: |
          TODOS=$(grep -rn "FIXME\|TODO" --include="*.ts" --include="*.tsx" src/ \
            | grep -v "node_modules" | grep -v "// eslint-disable" || true)
          if [ -n "$TODOS" ]; then
            echo "⚠️  Found TODOs/FIXMEs (non-blocking):"
            echo "$TODOS"
          fi
```

## Diff-Based Linting

For large monorepos, running ESLint on only changed files is significantly faster:

```yaml
- name: Diff-Based Lint
  run: |
    # Get files changed in this PR
    CHANGED_FILES=$(git diff --name-only origin/main...HEAD \
      -- '*.ts' '*.tsx' '*.js' '*.jsx' \
      | grep -v node_modules \
      | grep -v '.generated.' \
      || true)

    if [ -z "$CHANGED_FILES" ]; then
      echo "No TypeScript/JavaScript files changed"
      exit 0
    fi

    echo "Changed files: $CHANGED_FILES"
    pnpm exec eslint $CHANGED_FILES --max-warnings=0
```

## Cache Strategy

```yaml
- name: Cache ESLint
  uses: actions/cache@v4
  with:
    path: .eslintcache
    key: eslint-${{ runner.os }}-${{ hashFiles('**/*.ts', '**/*.tsx', '**/eslint*', '**/tsconfig.json') }}
    restore-keys: |
      eslint-${{ runner.os }}-
```

## Reporting and Dashboards

```yaml
- name: Generate Lint Report
  if: always()
  run: |
    pnpm lint -- --format=json -o lint-report.json || true

- name: Upload Lint Report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: lint-report
    path: lint-report.json
```

## Custom Lint Rules for Voice Agent Platform

```typescript
// packages/config/eslint/custom-rules/no-mock-in-production.ts
import type { Rule } from "eslint";

export const noMockInProduction: Rule.RuleModule = {
  meta: {
    type: "problem",
    docs: {
      description:
        "Prevent mock providers from being used in production code",
    },
    messages: {
      noMockInProduction:
        "Mock providers should not be imported in production code. Use a real provider or mock conditionally.",
    },
  },
  create(context) {
    return {
      ImportDeclaration(node) {
        if (node.source.value.endsWith("/mock") || node.source.value.endsWith("/mock.ts")) {
          const filename = context.filename ?? "";
          if (
            filename.includes("/production/") ||
            filename.includes("/prod/")
          ) {
            context.report({
              node,
              messageId: "noMockInProduction",
            });
          }
        }
      },
    };
  },
};
```

## PR Status Checks

```yaml
# Branch protection rule configuration (requires GitHub API or UI)
# Required status checks:
#   - Lint / lint
#   - Quality Gate / quality-gate
#   - Type Check / typecheck
#   - Test (vitest)
#   - Build
```

## Design Decisions

### Why run lint in CI if pre-commit hooks already enforce it?

Pre-commit hooks can be bypassed (`git commit --no-verify`). CI lint checks provide:
1. **Safety net**: Catches bypasses and edge cases
2. **Consistency**: Different OS or Node.js versions may produce different lint results locally
3. **Orchestration**: CI runs lint in the same environment as other checks, ensuring consistency
4. **Visibility**: Lint failures are visible to the entire team in PR checks

### ESLint --max-warnings=0

Failing on warnings ensures that warnings don't accumulate. Without this, teams often end up with thousands of warnings that are permanently ignored.

## Integration Points

- **GitHub Actions**: Workflow runs on every PR
- **GitHub Branch Protection**: Required status checks block merging
- **PR Annotations**: Inline error display in PR diffs
- **Slack/Notifications**: Lint failures can be posted to team channels

## Production Considerations

1. **Performance**: Full lint suite should complete in under 5 minutes. If it's slower, use diff-based linting or split into parallel jobs
2. **False positives**: Custom lint rules should be thoroughly tested to avoid blocking legitimate code
3. **Grace period**: When introducing new strict rules, give a grace period where they're warnings before promoting to errors
4. **Brownfield projects**: For existing projects, use `--no-ignore` and `--quiet` initially, then gradually increase strictness
5. **Branch-specific rules**: Consider different strictness levels for different branches — main can be strict, feature branches can be lenient during active development
