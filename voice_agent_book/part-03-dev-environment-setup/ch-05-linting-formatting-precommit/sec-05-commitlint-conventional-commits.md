# Section 05: commitlint & Conventional Commits

## Overview

Conventional Commits provide a standardized format for commit messages that enables automated changelog generation, semantic versioning, and better project history readability. commitlint enforces this format at commit time, ensuring every commit message follows the convention.

## Commit Message Format

```text
type(scope): description

[optional body]

[optional footer(s)]
```

### Types

| Type | Usage | Release Impact |
|------|-------|----------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `chore` | Maintenance, tooling | PATCH |
| `docs` | Documentation changes | PATCH |
| `refactor` | Code restructuring | PATCH |
| `test` | Adding or modifying tests | PATCH |
| `style` | Formatting, linting | PATCH |
| `perf` | Performance improvement | PATCH |
| `ci` | CI/CD changes | PATCH |
| `build` | Build system changes | PATCH |
| `revert` | Revert a previous commit | PATCH |

### Scopes

Scopes indicate which part of the codebase the change affects:

```
feat(api): add call recording endpoint
fix(voice): resolve TTS timeout issue
chore(deps): update zod to v3.23
docs(web): update README with setup instructions
refactor(db): extract repository pattern
test(ai): add LLM provider mock tests
ci(actions): optimize cache strategy
```

Valid scopes for our monorepo: `web`, `api`, `ui`, `db`, `voice`, `ai`, `types`, `config`, `deps`, `docker`, `ci`, `docs`

## commitlint Configuration

```javascript
// commitlint.config.js
/** @type {import('@commitlint/types').UserConfig} */
const config = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // Type rules
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "chore",
        "docs",
        "refactor",
        "test",
        "style",
        "perf",
        "ci",
        "build",
        "revert",
      ],
    ],
    "type-case": [2, "always", "lower-case"],

    // Scope rules
    "scope-enum": [
      2,
      "always",
      [
        "web",
        "api",
        "ui",
        "db",
        "voice",
        "ai",
        "types",
        "config",
        "deps",
        "docker",
        "ci",
        "docs",
        "release",
      ],
    ],
    "scope-case": [2, "always", "lower-case"],

    // Subject rules
    "subject-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "subject-max-length": [2, "always", 100],

    // Body rules
    "body-max-line-length": [2, "always", 100],
    "body-leading-blank": [2, "always"],

    // Footer rules
    "footer-leading-blank": [2, "always"],
    "footer-max-line-length": [2, "always", 100],
  },
  helpUrl:
    "https://github.com/voice-agent-platform/voice-agent/blob/main/CONTRIBUTING.md#commit-messages",
};

module.exports = config;
```

## Package Configuration

```jsonc
{
  "scripts": {
    "commit": "cz"  // Commitizen CLI
  },
  "devDependencies": {
    "@commitlint/cli": "^19.0.0",
    "@commitlint/config-conventional": "^19.0.0",
    "commitizen": "^4.3.0",
    "cz-conventional-changelog": "^3.3.0"
  }
}
```

## Husky Integration

```bash
#!/usr/bin/env sh
# .husky/commit-msg
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

The `--edit "$1"` flag reads the commit message file and validates it against the configured rules.

## Commitizen CLI

Commitizen provides an interactive commit message builder that ensures format compliance:

```bash
# Install Commitizen
pnpm add -D commitizen cz-conventional-changelog

# Configure Commitizen
# In package.json:
"config": {
  "commitizen": {
    "path": "cz-conventional-changelog"
  }
}

# Use Commitizen to make commits
pnpm commit
```

```text
? Select the type of change: feat (new feature)
? What is the scope of this change: api
? Write a short description: add voice activity detection endpoint
? Provide a longer description: (optional)
? Are there any breaking changes: No
? Does this affect any open issues: No

Generated commit message:
feat(api): add voice activity detection endpoint
```

## Changelog Generation

Conventional Commits enable automated changelog generation:

```bash
# Install conventional-changelog
pnpm add -D conventional-changelog-cli

# Generate changelog
pnpm exec conventional-changelog -p angular -i CHANGELOG.md -s

# Generate for a specific version
pnpm exec conventional-changelog -p angular -i CHANGELOG.md -s -r 2
```

### Generated CHANGELOG.md

```markdown
# Changelog

## [1.2.0] - 2024-06-15

### Features
- **api**: add voice activity detection endpoint (abc1234)
- **voice**: implement streaming TTS (def5678)

### Bug Fixes
- **db**: resolve migration ordering issue (ghi9012)
- **ai**: handle LLM timeout gracefully (jkl3456)

### Chores
- **deps**: update zod to v3.23 (mno7890)
- **ci**: optimize Turborepo cache strategy (pqr1234)
```

## Semantic Versioning Automation

With conventional commits, semantic version bumps can be automated:

```javascript
// scripts/version.js
import { execSync } from "child_process";

const TYPES = {
  feat: "minor",
  fix: "patch",
  chore: "patch",
  refactor: "patch",
  test: "patch",
  docs: "patch",
  perf: "patch",
};

function determineBump() {
  const commits = execSync(
    'git log $(git describe --tags --abbrev=0)..HEAD --format="%s"',
    { encoding: "utf-8" }
  ).trim().split("\n");

  const types = commits.map((c) => c.split("(")[0]?.split(":")[0]);

  if (types.some((t) => t === "BREAKING CHANGE" || t?.includes("!"))) {
    return "major";
  }
  if (types.some((t) => t === "feat")) {
    return "minor";
  }
  return "patch";
}

console.log(determineBump());
```

## Valid Commit Examples

```text
# ✅ Good commits
feat(api): add pagination to call list endpoint
fix(voice): handle WebSocket disconnect during streaming
chore(deps): update eslint to v9.0
docs(web): add JSDoc to API client methods
refactor(db): extract repository pattern from services
test(ai): add unit tests for LLM provider selection
ci(actions): add stale issue management workflow
style(ui): sort Tailwind classes with plugin

# ❌ Bad commits
fixed stuff
WIP
update
asdf
Added some changes (wrong case)
feat(api):Added feature (missing space after colon)
```

## Design Decisions

### Why conventional commits?

1. **Automated changelog**: No manual CHANGELOG.md editing
2. **Semantic versioning**: Automated version bumps based on commit types
3. **Release notes**: Generate release notes from commits between tags
4. **Project history**: At a glance, you can see what types of changes went into a release
5. **PR titles**: PR titles follow the same convention for squash merges

### Enforcing via commit-msg hook vs. PR lint check

**Decision**: Both. Validate at commit time (immediate feedback) AND in CI (catches bypasses).

## Integration Points

- **Husky commit-msg**: Enforces format at commit time
- **CI**: commitlint runs in CI to validate PR titles for squash merges
- **Changelog generator**: Produces markdown from commit history
- **Semantic release**: Automated versioning and package publishing
- **Code review**: Standardized commit messages make PRs easier to review

## Production Considerations

1. **Squash merge strategy**: When using squash merges, ensure the squash commit message follows conventional commits. GitHub's default squash message uses the PR title, which should be conventional
2. **Breaking changes**: Mark breaking changes with `!` after the type/scope: `feat(api)!: remove deprecated v1 endpoints`. This triggers a major version bump
3. **Revert commits**: `git revert` produces conventional-format commit messages automatically
4. **Merge commits**: Merge commits from `git merge` don't follow conventional commits. Use rebase or squash merge instead
5. **Migration**: If migrating an existing project, don't retroactively change old commits. Start enforcing the convention from a specific date or tag forward
