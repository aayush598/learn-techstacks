# Section 04: lint-staged Configuration

## Overview

lint-staged runs linters only on staged files, making pre-commit checks fast by avoiding unnecessary work. Instead of linting the entire codebase on every commit, it filters to only the files about to be committed and runs the appropriate linters on each file type.

## Configuration

```javascript
// lint-staged.config.js
/** @type {import('lint-staged').Config} */
const config = {
  // TypeScript and JavaScript files
  "*.{ts,tsx,js,jsx}": [
    "eslint --fix --max-warnings=0",
    "prettier --write",
  ],

  // Other files that need formatting
  "*.{json,md,yaml,yml,css,scss,graphql}": [
    "prettier --write",
  ],

  // Markdown files — lint only, no auto-fix for content
  "*.md": [
    "prettier --write",
  ],

  // Configuration files — no auto-fix
  "*.{config.*,*rc}": [
    "prettier --check",
  ],
};

export default config;
```

## Package-Specific Configuration

For packages with specialized linting needs, lint-staged supports per-package configuration:

```javascript
// apps/web/lint-staged.config.js
/** @type {import('lint-staged').Config} */
const config = {
  "*.{ts,tsx}": [
    "eslint --fix --max-warnings=0",
    "prettier --write",
  ],
  "*.css": [
    "stylelint --fix",
    "prettier --write",
  ],
};

export default config;
```

```javascript
// packages/db/lint-staged.config.js
/** @type {import('lint-staged').Config} */
const config = {
  "*.ts": [
    "eslint --fix --max-warnings=0",
    "prettier --write",
  ],
  "prisma/schema.prisma": [
    "prisma format",
  ],
};

export default config;
```

## Integration with Husky

```bash
#!/usr/bin/env sh
# .husky/pre-commit
. "$(dirname "$0")/_/husky.sh"

pnpm exec lint-staged
```

The `lint-staged` command automatically reads the configuration from the project root, applies it to staged files, and passes the file list to each configured linter.

## Execution Flow

```text
git add file1.ts file2.tsx file3.json

git commit
  │
  ▼
Husky pre-commit → lint-staged
  │
  ▼
lint-staged reads config:
  *.ts,*.tsx → eslint --fix + prettier --write
  *.json     → prettier --write
  │
  ▼
eslint --fix file1.ts file2.tsx
  │ Errors? → Abort commit
  │
  ▼
prettier --write file1.ts file2.tsx file3.json
  │ Changes? → Added to commit
  │
  ▼
Commit proceeds ✅
```

## Advanced Configuration

### Parallel Execution (Default)

```javascript
// Default — run linters in parallel for each file group
const config = {
  "*.ts": ["eslint --fix", "prettier --write"],
};
```

### Concurrency Control

```javascript
// Limit concurrency for resource-intensive linters
const config = {
  "*.ts": ["eslint --fix", "prettier --write"],
};

export default config;
// lint-staged runs tasks with default concurrency (half of CPU cores)
```

### File Type Filtering

```javascript
// Only lint files in src/ directories
const config = {
  "src/**/*.ts": ["eslint --fix"],
  "!src/generated/**": [],  // Skip generated files
};
```

## Error Handling

```javascript
// lint-staged.config.js with custom error handling
const config = {
  "*.{ts,tsx}": [
    // --max-warnings=0 ensures warnings also fail the commit
    "eslint --fix --max-warnings=0",
    "prettier --write",
  ],
};

// If ESLint finds any issues:
// 1. Auto-fix what it can
// 2. Report remaining issues
// 3. Abort commit with error message
// 4. Developer must fix issues and re-stage
```

## Performance Optimization

```bash
# Speed up lint-staged by caching
# ESLint caching
echo '--cache' >> .eslintrc

# Prettier caching
echo '--cache' >> .prettierrc

# lint-staged automatically only processes staged files
# Additional optimization: ignore large files
echo '--ignore-path .gitignore' >> .eslintrc
```

## Ignoring Files

```javascript
// lint-staged.config.js
const config = {
  "*.{ts,tsx}": [
    "eslint --fix --max-warnings=0",
    "prettier --write",
  ],
  // Ignore generated files
  "!src/generated/**": [],
  // Ignore test fixtures
  "!src/**/__fixtures__/**": [],
};
```

## Design Decisions

### ESLint --fix vs. manual fixes

**Decision**: Auto-fix what can be auto-fixed (import order, formatting) and fail for what can't (type errors, logic bugs).

**Rationale**: Auto-fixing reduces developer friction. Developers appreciate that `git commit` automatically formats their code. But semantic issues (unused variables, missing error handling) should stop the commit because they require human judgment.

### Why --max-warnings=0?

Warnings become noise if they're always present. By failing on warnings, we force developers to either fix the issue or explicitly disable the rule with a comment explaining why.

## Integration Points

- **Husky pre-commit**: Invokes lint-staged
- **ESLint**: Linting with auto-fix
- **Prettier**: Formatting with auto-write
- **stylelint**: CSS/SCSS linting (if applicable)
- **CI**: lint-staged is not used in CI — CI runs full lint suite

## Production Considerations

1. **Staged file limits**: If a commit contains hundreds of files, lint-staged could take long. Consider `--concurrency` limits or increasing the `--max-warnings` threshold temporarily
2. **Binary files**: lint-staged ignores binary files automatically. Ensure `.gitattributes` correctly marks binary file types
3. **Merge commits**: lint-staged may behave unexpectedly during merge conflict resolution. Husky should be configured to skip hooks during merges: `git merge --no-verify`
4. **Large monorepos**: For very large monorepos, lint-staged with per-package configurations prevents cross-package linting issues
5. **CI consistency**: lint-staged results should match CI lint results. If there's a discrepancy (e.g., different ESLint versions), fix the configuration, not the CI
