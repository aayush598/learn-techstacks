# Chapter 05: Linting, Formatting & Pre-commit Hooks

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [ESLint Configuration](sec-01-eslint-configuration.md) | Flat config, TypeScript rules, React hooks, Next.js plugin, import ordering, custom rules |
| 02 | [Prettier Configuration](sec-02-prettier-configuration.md) | Consistent formatting, print width, trailing commas, semicolons, plugins for Tailwind |
| 03 | [Husky & Git Hooks](sec-03-husky-git-hooks.md) | pre-commit (lint-staged), commit-msg (commitlint), pre-push (type check + tests) |
| 04 | [lint-staged Configuration](sec-04-lint-staged-configuration.md) | Run linters on staged files, parallel execution, auto-fix, file type filtering |
| 05 | [commitlint & Conventional Commits](sec-05-commitlint-conventional-commits.md) | Commit message format (type(scope): description), changelog generation, semantic versioning |
| 06 | [Editor Integration](sec-06-editor-integration.md) | VS Code settings, workspace recommendations, format on save, code actions on save |
| 07 | [CI Lint Checks](sec-07-ci-lint-checks.md) | Lint step in CI, quality gate, diff-based linting, reporting annotations |

---

## Key Takeaways

- ESLint flat config with TypeScript strict rules
- Prettier for consistent formatting (120 print width, trailing all)
- Husky manages pre-commit, commit-msg, pre-push hooks
- lint-staged runs linters only on changed files
- Conventional commits (feat:, fix:, chore:, docs:, refactor:)
- All lint checks must pass in CI before merge
