# Section 06: Editor Integration

## Overview

Consistent editor configuration ensures all developers on the voice agent platform have the same development experience — automatic formatting on save, inline linting, and recommended extensions. This section covers VS Code workspace settings, extension recommendations, and editor-agnostic tooling.

## VS Code Workspace Settings

```jsonc
// .vscode/settings.json
{
  // ── Editor Behavior ─────────────────────────────────────
  "editor.formatOnSave": true,
  "editor.formatOnPaste": false,
  "editor.formatOnType": false,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "never"
  },
  "editor.rulers": [100],
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "editor.minimap.enabled": false,
  "editor.renderWhitespace": "boundary",
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,

  // ── Files ───────────────────────────────────────────────
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.trimTrailingWhitespace": true,
  "files.exclude": {
    "**/.git": true,
    "**/.next": true,
    "**/dist": true,
    "**/node_modules": true,
    "**/.turbo": true
  },

  // ── TypeScript ──────────────────────────────────────────
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.preferences.importModuleSpecifier": "non-relative",
  "typescript.preferences.quoteStyle": "double",
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.validate.enable": true,
  "typescript.format.enable": false,

  // ── JavaScript ──────────────────────────────────────────
  "javascript.format.enable": false,
  "javascript.updateImportsOnFileMove.enabled": "always",

  // ── ESLint ──────────────────────────────────────────────
  "eslint.validate": [
    "typescript",
    "typescriptreact",
    "javascript",
    "javascriptreact"
  ],
  "eslint.format.enable": false,
  "eslint.run": "onType",
  "eslint.codeActionsOnSave.mode": "all",

  // ── Prettier ────────────────────────────────────────────
  "prettier.requireConfig": true,
  "prettier.configPath": ".prettierrc",

  // ── Tailwind CSS ────────────────────────────────────────
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ],
  "tailwindCSS.includeLanguages": {
    "typescript": "javascript",
    "typescriptreact": "javascript"
  },

  // ── Git ─────────────────────────────────────────────────
  "git.enableSmartCommit": true,
  "git.autofetch": true,
  "git.confirmSync": false,

  // ── Search ──────────────────────────────────────────────
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/.turbo": true,
    "**/coverage": true,
    "pnpm-lock.yaml": true
  },

  // ── Terminal ────────────────────────────────────────────
  "terminal.integrated.defaultProfile.linux": "bash",
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.cursorBlinking": true,

  // ── Emmet ───────────────────────────────────────────────
  "emmet.includeLanguages": {
    "typescript": "typescriptreact",
    "javascript": "javascriptreact"
  },

  // ── Workbench ───────────────────────────────────────────
  "workbench.colorTheme": "GitHub Dark Default",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.startupEditor": "none",
  "workbench.tree.indent": 20,
  "workbench.editor.enablePreview": false,
  "window.title": "${dirty}${activeEditorShort}${separator}${rootName}",
}

// .vscode/extensions.json
{
  "recommendations": [
    // Language support
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "Prisma.prisma",

    // TypeScript
    "ms-vscode.vscode-typescript-next",

    // Git
    "eamodio.gitlens",
    "mhutchie.git-graph",

    // Development
    "github.vscode-github-actions",
    "ms-azuretools.vscode-docker",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-js-profile-flame",

    // Testing
    "ZixuanChen.vitest-explorer",
    "ms-playwright.playwright",

    // Markdown
    "yzhang.markdown-all-in-one",

    // Other
    "streetsidesoftware.code-spell-checker",
    "aaron-bond.better-comments",
    "christian-kohler.path-intellisense",
    "formulahendry.auto-rename-tag",
    "mikestead.dotenv",
    "bobbyfidz.ulid"
  ],
  "unwantedRecommendations": [
    "hookyqr.beautify",
    "dbaeumer.jshint"
  ]
}
```

## Editor-Agnostic Configuration

### EditorConfig

```ini
# .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 100

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2

[*.sql]
indent_size = 2
```

EditorConfig is editor-agnostic and ensures basic formatting settings (indentation, line endings) work in any editor, even without specific extensions.

### Git Attributes

```gitignore
# .gitattributes
* text=auto eol=lf
*.ts text diff=typescript
*.tsx text diff=typescript
*.js text diff=javascript
*.json text diff=json
*.md text diff=markdown
*.yml text diff=yaml
*.yaml text diff=yaml
*.prisma text
pnpm-lock.yaml binary
```

## Debugging Configuration

```jsonc
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Web (Next.js)",
      "type": "node-terminal",
      "request": "launch",
      "command": "pnpm dev:web",
      "serverReadyAction": {
        "action": "debugWithChrome",
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "webRoot": "${workspaceFolder}/apps/web"
      }
    },
    {
      "name": "Debug API (Next.js)",
      "type": "node-terminal",
      "request": "launch",
      "command": "pnpm dev:api",
      "port": 4000
    },
    {
      "name": "Debug Tests (Current File)",
      "type": "node-terminal",
      "request": "launch",
      "command": "pnpm --filter ${relativeFileDirname} test -- --run",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Debug Vitest",
      "type": "node-terminal",
      "request": "launch",
      "command": "pnpm test -- --reporter=verbose",
      "skipFiles": ["<node_internals>/**"]
    }
  ],
  "compounds": [
    {
      "name": "Full Stack",
      "configurations": ["Debug Web (Next.js)", "Debug API (Next.js)"]
    }
  ]
}
```

## Task Runner Configuration

```jsonc
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Docker Services",
      "type": "shell",
      "command": "pnpm docker:up",
      "problemMatcher": [],
      "group": "build"
    },
    {
      "label": "Run Database Migrations",
      "type": "shell",
      "command": "pnpm db:migrate",
      "problemMatcher": [],
      "dependsOn": ["Start Docker Services"]
    },
    {
      "label": "Type Check All",
      "type": "shell",
      "command": "pnpm typecheck",
      "problemMatcher": "$tsc",
      "group": "build"
    },
    {
      "label": "Lint All",
      "type": "shell",
      "command": "pnpm lint",
      "problemMatcher": "$eslint-stylish",
      "group": "build"
    }
  ]
}
```

## IntelliJ / WebStorm Configuration

```xml
<!-- .idea/inspectionProfiles/Project_Default.xml -->
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <option name="myName" value="Project Default" />
    <inspection_tool class="Eslint" enabled="true" level="ERROR" />
    <inspection_tool class="TsLint" enabled="false" level="ERROR" />
    <inspection_tool class="RequiredAttributes" enabled="true" level="ERROR">
      <scope name="Open Files" level="ERROR" />
    </inspection_tool>
  </profile>
</component>
```

## Design Decisions

### Why VS Code-specific settings (not editor-agnostic)?

VS Code is the team's agreed-upon editor. While EditorConfig provides basic cross-editor support, VS Code-specific settings unlock features like format-on-save with Prettier, ESLint auto-fix, and Tailwind CSS IntelliSense that have no editor-agnostic equivalent.

### Commit .vscode/ to version control

**Decision**: Yes, commit `.vscode/settings.json` and `.vscode/extensions.json`.

**Rationale**: Workspace settings ensure every developer gets the same editor configuration automatically. Extension recommendations prompt developers to install essential tools. This eliminates "works on my machine" issues caused by different editor configurations.

## Integration Points

- **ESLint**: Inline error display, auto-fix on save
- **Prettier**: Format on save
- **Tailwind CSS**: Class name autocompletion
- **TypeScript**: IntelliSense with path alias resolution
- **Git**: Inline blame, commit graph
- **Docker**: Container management within VS Code

## Production Considerations

1. **Settings drift**: Periodically audit that all developers have the recommended extensions installed. VS Code's extension recommendations prompt on workspace open
2. **Performance**: Some extensions (GitLens, Tailwind CSS IntelliSense) can slow down VS Code on large projects. If performance degrades, disable extensions selectively
3. **Remote development**: DevContainers (see Chapter 06) provide a fully configured development environment including all extensions. This is the most reliable way to ensure consistent editor setup
4. **Custom snippets**: Team-wide code snippets can be shared via `.vscode/project.code-snippets`. Useful for common patterns like React components, API route handlers, and Prisma queries
5. **Workspace trust**: VS Code's Workspace Trust feature should be enabled to prevent automatic execution of code in the workspace
