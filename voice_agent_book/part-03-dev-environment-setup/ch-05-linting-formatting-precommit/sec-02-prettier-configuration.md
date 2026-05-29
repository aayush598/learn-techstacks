# Section 02: Prettier Configuration

## Overview

Prettier provides consistent code formatting across the entire voice agent platform, eliminating debates about style in code reviews. By integrating with ESLint via `eslint-config-prettier`, we avoid conflicting rules and enforce a single formatting standard.

## Configuration

```javascript
// packages/config/prettier/index.js
/** @type {import("prettier").Config} */
const config = {
  // Line length
  printWidth: 100,

  // Indentation
  tabWidth: 2,
  useTabs: false,

  // Semicolons and quotes
  semi: true,
  singleQuote: false,
  quoteProps: "as-needed",

  // Trailing commas
  trailingComma: "all",

  // Whitespace
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: "always",

  // Line endings
  endOfLine: "lf",

  // Embedded language formatting
  embeddedLanguageFormatting: "auto",

  // HTML whitespace sensitivity
  htmlWhitespaceSensitivity: "css",

  // JSX
  jsxSingleQuote: false,

  // Plugins
  plugins: ["prettier-plugin-tailwindcss"],
};

module.exports = config;
```

## Package Configuration

```jsonc
{
  "name": "@voice-agent/config-prettier",
  "version": "0.0.1",
  "private": true,
  "main": "./index.js",
  "dependencies": {
    "prettier-plugin-tailwindcss": "^0.6.0"
  },
  "peerDependencies": {
    "prettier": "^3.2.0"
  }
}
```

## Root Prettier Configuration

```jsonc
// .prettierrc
"@voice-agent/config-prettier"
```

This single line references the shared config package, ensuring all workspaces use identical formatting rules.

## `.prettierignore`

```gitignore
# .prettierignore
node_modules
dist
.next
.turbo
coverage
pnpm-lock.yaml
*.md
*.svg
*.png
*.jpg
*.ico
.editorconfig

# Generated files
packages/db/prisma/migrations/**/*.sql
apps/web/src/generated/**
```

## Prettier with ESLint

ESLint and Prettier rules can conflict (e.g., both wanting to control quote styles). We resolve this with `eslint-config-prettier`:

```typescript
// packages/config/eslint/base.ts
import prettierConfig from "eslint-config-prettier";

export const baseConfig: Linter.Config[] = [
  // ... TypeScript rules ...
  // Disable ESLint rules that conflict with Prettier
  prettierConfig,
];
```

The `eslint-config-prettier` package turns off all ESLint rules that are unnecessary or might conflict with Prettier. This must be the last entry in the config array.

## Formatting Scripts

```jsonc
{
  "scripts": {
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md,yaml,yml,graphql,css}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md,yaml,yml,graphql,css}\""
  }
}
```

### Format on Save (VS Code)

```jsonc
// .vscode/settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[yaml]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Tailwind CSS Class Sorting

The `prettier-plugin-tailwindcss` plugin automatically sorts Tailwind CSS classes according to the recommended order:

```typescript
// Before formatting
<div className="px-4 py-2 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600">

// After formatting (Tailwind classes sorted)
<div className="rounded-lg bg-blue-500 px-4 py-2 font-medium text-white hover:bg-blue-600">
```

The plugin follows the Tailwind CSS class ordering convention:
1. Layout (display, position)
2. Box model (width, height, margin, padding)
3. Typography (font, text)
4. Visual (background, border, shadow)
5. Interactive (hover, focus, active)

## Prettier Configuration Decisions

### printWidth: 100 vs. 80

**Decision**: 100 characters.

**Rationale**: Modern widescreen monitors make 80 characters unnecessarily restrictive. 100 characters provides enough room for descriptive variable names in TypeScript while still fitting in a split-editor view. This is the standard for most Vercel/Next.js projects.

### trailingComma: "all" vs. "es5"

**Decision**: Trailing commas everywhere (all).

**Rationale**: Trailing commas produce cleaner git diffs — adding a new property only adds one line instead of modifying two. TypeScript and modern JavaScript engines support trailing commas in all contexts.

### semi: true vs. false

**Decision**: Always use semicolons.

**Rationale**: While ASI (Automatic Semicolon Insertion) usually works, there are edge cases where missing semicolons cause bugs. Consistent semicolons eliminate an entire class of issues.

### singleQuote: false vs. true

**Decision**: Double quotes.

**Rationale**: Double quotes are standard in JSON and JSX attributes. Using double quotes consistently avoids unnecessary escaping when working with HTML-like syntax.

## Integration Points

- **VS Code**: Format on save via Prettier extension
- **ESLint**: `eslint-config-prettier` disables conflicting rules
- **lint-staged**: Prettier runs on staged files before commit
- **CI pipeline**: `pnpm format:check` ensures formatting consistency
- **Husky**: Pre-commit hook enforces formatting

## Production Considerations

1. **Formatting speed**: Prettier is fast but on very large files (500+ lines) it can take noticeable time. Use `--cache` to skip already-formatted files
2. **Editor plugin version**: Ensure all team members use the same Prettier extension version. Different versions may format differently
3. **Ignored files**: Keep `.prettierignore` up to date. Generated files, SQL migrations, and lockfiles should never be formatted
4. **CI check**: `pnpm format:check` in CI should fail if any file is unformatted. This prevents unformatted code from being merged
5. **Migration**: When changing Prettier settings (e.g., printWidth), run a single commit that reformats the entire codebase. This prevents formatting changes from polluting functional diffs
