# Section 01: ESLint Configuration

## Overview

ESLint enforces code quality and consistency across the voice agent platform's TypeScript codebase. Using the flat config format (ESLint v9+), we define shared rules for type safety, import organization, React best practices, and Next.js conventions.

## Flat Config Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              ESLint Flat Config Hierarchy                     │
│                                                              │
│  @voice-agent/config-eslint                                  │
│  ├── base.ts              # TypeScript strict rules          │
│  ├── react.ts             # React + hooks rules              │
│  ├── next.ts              # Next.js specific rules           │
│  └── library.ts           # Library package rules            │
│                                                              │
│  Consumers:                                                  │
│  apps/web/eslint.config.js → import { nextConfig }           │
│  apps/api/eslint.config.js → import { nextConfig }           │
│  packages/ui/eslint.config.js → import { reactConfig }       │
│  packages/db/eslint.config.js → import { libraryConfig }     │
└─────────────────────────────────────────────────────────────┘
```

## Base ESLint Configuration

```typescript
// packages/config/eslint/base.ts
import type { Linter } from "eslint";
import tseslint from "typescript-eslint";
import tsparser from "@typescript-eslint/parser";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import unusedImports from "eslint-plugin-unused-imports";

export const baseConfig: Linter.Config[] = [
  // Ignore patterns
  { ignores: ["dist/**", ".next/**", "node_modules/**", "coverage/**"] },

  // TypeScript files
  ...tseslint.configs.recommended,
  ...tseslint.configs.stylistic,

  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        projectService: true,
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    plugins: {
      "simple-import-sort": simpleImportSort,
      "unused-imports": unusedImports,
    },
    rules: {
      // TypeScript strict rules
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          destructuredArrayIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-non-null-assertion": "error",
      "@typescript-eslint/prefer-nullish-coalescing": "error",
      "@typescript-eslint/prefer-optional-chain": "error",
      "@typescript-eslint/strict-boolean-expressions": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports" },
      ],

      // Import sorting
      "simple-import-sort/imports": [
        "error",
        {
          groups: [
            // Node builtins
            ["^node:"],
            // External packages
            ["^@?\\w"],
            // Internal packages (@voice-agent/)
            ["^@voice-agent/"],
            // Internal aliases (@/)
            ["^@/"],
            // Relative imports
            ["^\\.\\./", "^\\./"],
            // Side effect imports
            ["^\\u0000"],
            // Styles
            ["\\.css$", "\\.scss$"],
          ],
        },
      ],
      "simple-import-sort/exports": "error",
      "unused-imports/no-unused-imports": "error",

      // General
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "eqeqeq": ["error", "always"],
      "curly": ["error", "all"],
      "no-throw-literal": "error",
      "prefer-const": "error",
      "no-var": "error",
    },
  },
];
```

## React Configuration

```typescript
// packages/config/eslint/react.ts
import type { Linter } from "eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import { baseConfig } from "./base";

export const reactConfig: Linter.Config[] = [
  ...baseConfig,
  {
    files: ["**/*.tsx"],
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      // React
      "react/jsx-uses-react": "error",
      "react/jsx-uses-vars": "error",
      "react/self-closing-comp": "error",
      "react/jsx-boolean-value": ["error", "always"],
      "react/no-array-index-key": "warn",
      "react/jsx-no-target-blank": "error",
      "react/jsx-key": ["error", { checkFragmentShorthand: true }],
      "react/no-unstable-nested-components": "error",

      // React Hooks
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
  },
];
```

## Next.js Configuration

```typescript
// packages/config/eslint/next.ts
import type { Linter } from "eslint";
import nextPlugin from "@next/eslint-plugin-next";
import { reactConfig } from "./react";

export const nextConfig: Linter.Config[] = [
  ...reactConfig,
  {
    plugins: {
      "@next/next": nextPlugin,
    },
    rules: {
      "@next/next/no-html-link-for-pages": "error",
      "@next/next/no-img-element": "error",
      "@next/next/no-sync-scripts": "error",
      "@next/next/no-before-interactive-script-outside-document": "error",
      "@next/next/google-font-display": "error",
      "@next/next/google-font-preconnect": "error",
      "@next/next/inline-script-id": "error",
      "@next/next/no-duplicate-head": "error",
      "@next/next/no-page-custom-font": "error",
      "@next/next/no-title-in-document-head": "error",
      "@next/next/no-unwanted-polyfillio": "error",
    },
  },
];
```

## Library Package Configuration

```typescript
// packages/config/eslint/library.ts
import type { Linter } from "eslint";
import { baseConfig } from "./base";

export const libraryConfig: Linter.Config[] = [
  ...baseConfig,
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      // Libraries don't have side effects
      "no-console": "error",
      // Ensure proper exports
      "import/no-default-export": "error",
    },
  },
];
```

## Consumer Configuration

### Next.js App

```typescript
// apps/web/eslint.config.js
import { nextConfig } from "@voice-agent/config-eslint/next";

export default nextConfig;
```

### Library Package

```typescript
// packages/ui/eslint.config.js
import { reactConfig } from "@voice-agent/config-eslint/react";

export default reactConfig;
```

### Database Package

```typescript
// packages/db/eslint.config.js
import { libraryConfig } from "@voice-agent/config-eslint/library";

export default libraryConfig;
```

## Running ESLint

```bash
# Lint all packages
pnpm lint

# Lint specific package
pnpm --filter @voice-agent/web run lint

# Auto-fix issues
pnpm lint:fix

# Lint staged files (via lint-staged)
pnpm exec lint-staged
```

## Custom Rules

```typescript
// packages/config/eslint/custom-rules/no-direct-prisma.ts
import type { Rule } from "eslint";

export const noDirectPrisma: Rule.RuleModule = {
  meta: {
    type: "problem",
    docs: {
      description: "Forbid direct Prisma imports outside @voice-agent/db",
    },
    messages: {
      noDirectPrisma:
        "Do not import Prisma directly. Use @voice-agent/db repository methods instead.",
    },
  },
  create(context) {
    return {
      ImportDeclaration(node) {
        if (
          node.source.value === "@prisma/client" &&
          !context.filename.includes("packages/db")
        ) {
          context.report({
            node,
            messageId: "noDirectPrisma",
          });
        }
      },
    };
  },
};
```

## Design Decisions

### Flat Config vs. Legacy .eslintrc

ESLint's flat config (v9+) is declarative, composable, and TypeScript-native. Unlike the legacy cascading config system, flat config arrays are explicit and don't have surprising inheritance behavior.

### strict-boolean-expressions

This rule prevents implicit boolean coercion, which is a common source of bugs:

```typescript
// ❌ Bad — coerces empty string to false
if (agent.name) { /* ... */ }

// ✅ Good — explicit comparison
if (agent.name !== "") { /* ... */ }

// ❌ Bad — accidental null check
if (agent.calls.length) { /* ... */ }

// ✅ Good — explicit
if (agent.calls.length > 0) { /* ... */ }
```

### consistent-type-imports

Enforce `import type` syntax for type-only imports:

```typescript
// ❌ Bad
import { Agent, AgentService } from "@voice-agent/types";

// ✅ Good
import type { Agent } from "@voice-agent/types";
import { AgentService } from "@voice-agent/types";
```

This prevents type imports from being included in the JavaScript bundle.

## Integration Points

- **Pre-commit hook**: lint-staged runs ESLint on staged files
- **CI pipeline**: `pnpm lint` runs on every PR
- **VS Code**: ESLint extension shows errors inline
- **Code review**: ESLint violations are visible in PR annotations

## Production Considerations

1. **Performance**: Flat configs are faster than legacy configs. For very large projects, use ESLint's `--cache` flag to skip already-checked files
2. **Rule updates**: When adding new rules, use `"warn"` first, then escalate to `"error"` after a grace period. This prevents breaking existing PRs
3. **TypeScript integration**: ESLint with `parserOptions.projectService` uses TypeScript's language service for faster type-aware linting. Ensure `tsconfig.json` is properly configured
4. **Suppression comments**: Use `// eslint-disable-next-line` sparingly. Each suppression should have a comment explaining why
5. **CI annotations**: Use `reviewdog` or GitHub Annotations to surface ESLint errors in PR diffs, not just in build logs
