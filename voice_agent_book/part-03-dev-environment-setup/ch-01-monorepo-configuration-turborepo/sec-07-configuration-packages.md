# Section 07: Configuration Packages

## Overview

Configuration packages centralize shared tool configurations (ESLint, TypeScript, Prettier, Tailwind) so that every workspace inherits the same base rules without duplicating config files. This approach ensures consistency, simplifies updates, and provides a single source of truth for each tool's behavior.

## Configuration Architecture

```text
packages/config/
├── eslint/
│   ├── package.json          # @voice-agent/config-eslint
│   ├── base.ts               # Base ESLint flat config
│   ├── react.ts              # React-specific rules
│   ├── next.ts               # Next.js-specific rules
│   └── library.ts            # Library package rules
├── typescript/
│   ├── package.json          # @voice-agent/config-typescript
│   ├── base.json             # Base tsconfig (strict mode)
│   ├── nextjs.json           # Next.js tsconfig extension
│   ├── library.json          # Library package tsconfig extension
│   └── node.json             # Node.js script tsconfig
├── prettier/
│   ├── package.json          # @voice-agent/config-prettier
│   └── index.js              # Prettier configuration
└── tailwind/
    ├── package.json          # @voice-agent/config-tailwind
    └── preset.ts             # Tailwind preset with design tokens
```

## ESLint Configuration Package

### Package Definition

```jsonc
{
  "name": "@voice-agent/config-eslint",
  "version": "0.0.1",
  "private": true,
  "main": "./base.ts",
  "exports": {
    ".": "./base.ts",
    "./react": "./react.ts",
    "./next": "./next.ts",
    "./library": "./library.ts"
  },
  "dependencies": {
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "eslint-plugin-react": "^7.34.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-import": "^2.29.0",
    "eslint-plugin-unused-imports": "^3.1.0",
    "eslint-plugin-simple-import-sort": "^12.0.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-tailwindcss": "^3.15.0",
    "@next/eslint-plugin-next": "^14.2.0"
  },
  "peerDependencies": {
    "eslint": "^8.57.0"
  }
}
```

### Base ESLint Configuration (Flat Config)

```typescript
// packages/config/eslint/base.ts
import type { Linter } from "eslint";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import unusedImports from "eslint-plugin-unused-imports";

export const baseConfig: Linter.Config[] = [
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: true,
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
      "simple-import-sort": simpleImportSort,
      "unused-imports": unusedImports,
    },
    rules: {
      // TypeScript strict rules
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", destructuredArrayIgnorePattern: "^_" },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/explicit-function-return-type": "off",
      "@typescript-eslint/strict-boolean-expressions": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-misused-promises": "error",

      // Import sorting
      "simple-import-sort/imports": "error",
      "simple-import-sort/exports": "error",
      "unused-imports/no-unused-imports": "error",

      // General rules
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "eqeqeq": ["error", "always"],
      "curly": ["error", "all"],
    },
  },
  { ignores: ["dist/**", ".next/**", "node_modules/**", "coverage/**"] },
  { linterOptions: { reportUnusedDisableDirectives: true } },
];
```

### React Configuration Extension

```typescript
// packages/config/eslint/react.ts
import type { Linter } from "eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import { baseConfig } from "./base";

export const reactConfig: Linter.Config[] = [
  ...baseConfig,
  {
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      "react/jsx-uses-react": "error",
      "react/jsx-uses-vars": "error",
      "react/self-closing-comp": "error",
      "react/jsx-no-target-blank": "error",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
  },
];
```

## TypeScript Configuration Package

### Package Definition

```jsonc
{
  "name": "@voice-agent/config-typescript",
  "version": "0.0.1",
  "private": true,
  "exports": {
    "./base.json": "./base.json",
    "./nextjs.json": "./nextjs.json",
    "./library.json": "./library.json",
    "./node.json": "./node.json"
  }
}
```

### Base TypeScript Configuration

```jsonc
// packages/config/typescript/base.json
{
  "compilerOptions": {
    // Strict mode
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,

    // Module resolution
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "esModuleInterop": true,

    // Output
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",

    // Additional
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "allowJs": false,
    "checkJs": false
  }
}
```

### Next.js Extension

```jsonc
// packages/config/typescript/nextjs.json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "preserve",
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"],
      "@voice-agent/*": ["../../packages/*/src"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"]
}
```

## Prettier Configuration Package

```javascript
// packages/config/prettier/index.js
/** @type {import("prettier").Config} */
const config = {
  printWidth: 100,
  tabWidth: 2,
  useTabs: false,
  semi: true,
  singleQuote: false,
  trailingComma: "all",
  bracketSpacing: true,
  arrowParens: "always",
  endOfLine: "lf",
  plugins: ["prettier-plugin-tailwindcss"],
};

module.exports = config;
```

```jsonc
{
  "name": "@voice-agent/config-prettier",
  "version": "0.0.1",
  "private": true,
  "main": "./index.js",
  "dependencies": {
    "prettier-plugin-tailwindcss": "^0.5.0"
  },
  "peerDependencies": {
    "prettier": "^3.2.0"
  }
}
```

## Consuming Configuration Packages

### App-Level ESLint Config

```typescript
// apps/web/eslint.config.js
import { nextConfig } from "@voice-agent/config-eslint/next";

export default nextConfig;
```

### App-Level tsconfig

```jsonc
// apps/api/tsconfig.json
{
  "extends": "@voice-agent/config-typescript/nextjs.json",
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@voice-agent/db": ["../../packages/db/src"]
    }
  }
}
```

### Root Prettier Config

```jsonc
// .prettierrc
"@voice-agent/config-prettier"
```

## Design Decisions

### Why config packages instead of files at the root?

1. **Versioning**: Config packages can be versioned independently. If the ESLint config adds new rules, packages can upgrade at their own pace
2. **Composability**: Each package provides multiple exports (base, react, next, library) so consumers import exactly what they need
3. **Testing**: Config packages can be tested independently — verify the ESLint config produces expected errors, or the TS config doesn't cause type errors
4. **Discoverability**: The `exports` field makes it clear what configurations are available

### Flat Config vs. Legacy ESLint Config

ESLint's flat config (v9+) is the recommended format. Benefits:
- **No cascading config files**: One export, one source of truth
- **Composable**: Configs are plain objects that can be spread, filtered, or transformed
- **TypeScript native**: Config files can be written in TypeScript directly

## Integration Points

- **Every workspace** extends these configs for consistent behavior
- **CI pipeline** uses the same configs for linting and type checking
- **Editor extensions** (VS Code ESLint, Prettier) respect the centralized configs

## Production Considerations

1. **Config updates**: When updating a config package, run `turbo lint` and `turbo typecheck` across the entire monorepo to catch regressions
2. **Lockstep versions**: Pin config package versions across workspaces — inconsistent config versions can lead to confusing lint errors
3. **Overrides**: Allow workspace-specific overrides but enforce that they must be explicit (no silent config drift)
4. **Migration strategy**: When upgrading ESLint or TypeScript major versions, update config packages first in a dedicated PR, then update consumers
