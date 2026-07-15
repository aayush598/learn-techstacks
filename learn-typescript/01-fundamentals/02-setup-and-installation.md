# 02 - Setup and Installation

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installing TypeScript](#installing-typescript)
  - [Global Installation](#global-installation)
  - [Local Installation (Recommended)](#local-installation-recommended)
- [The `tsc` Command](#the-tsc-command)
- [Initializing a TypeScript Project](#initializing-a-typescript-project)
- [tsconfig.json Basics](#tsconfigjson-basics)
- [Running TypeScript Files](#running-typescript-files)
- [VS Code Setup](#vs-code-setup)
- [Extensions](#extensions)
- [ts-node](#ts-node)
- [Nodemon with ts-node](#nodemon-with-ts-node)
- [Watch Mode](#watch-mode)
- [Alternative Transpilers](#alternative-transpilers)
- [Summary](#summary)

---

## Prerequisites

Before installing TypeScript, ensure you have the following:

- **Node.js** (version 18 or later recommended)
- **npm** (comes with Node.js)
- **A code editor** (VS Code is recommended)

Verify your installations:

```bash
node --version    # Should output v18.x.x or later
npm --version     # Should output 9.x.x or later
```

---

## Installing TypeScript

### Global Installation

Installing TypeScript globally makes the `tsc` command available system-wide:

```bash
npm install -g typescript
```

Verify the installation:

```bash
tsc --version
# Output: Version 5.x.x
```

> **Note:** Global installation is useful for quick experiments but is **not recommended** for projects. Different projects may need different TypeScript versions.

### Local Installation (Recommended)

For real projects, always install TypeScript as a **dev dependency**:

```bash
# Initialize a package.json (if you don't have one)
npm init -y

# Install TypeScript as a dev dependency
npm install -D typescript
```

This adds TypeScript to your `package.json`:

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "devDependencies": {
    "typescript": "^5.4.0"
  }
}
```

To run `tsc` locally:

```bash
npx tsc --version
```

> **Best Practice:** Using `npx` or `npm scripts` ensures everyone on your team uses the same TypeScript version, avoiding "works on my machine" issues.

---

## The `tsc` Command

`tsc` is the TypeScript compiler (more accurately, transpiler). Here are essential commands:

### Basic Compilation

```bash
# Compile a single file
npx tsc myfile.ts

# Compile all .ts files in the current directory
npx tsc

# Compile using a specific tsconfig.json
npx tsc --project tsconfig.json
```

### Useful Flags

```bash
# Watch mode — recompile on file changes
npx tsc --watch

# Generate source maps
npx tsc --sourceMap

# Specify output directory
npx tsc --outDir ./dist

# Target a specific ECMAScript version
npx tsc --target ES2020

# Strict mode
npx tsc --strict

# Skip type checking (just transpile)
npx tsc --noEmit false --isolatedModules

# Show all compiler options
npx tsc --help
```

### Checking Without Emitting

```bash
# Type-check only — no output files generated
npx tsc --noEmit
```

This is useful for CI/CD pipelines where you want to check types but not produce output.

---

## Initializing a TypeScript Project

### Step 1: Create the Project

```bash
mkdir my-typescript-project
cd my-typescript-project
npm init -y
npm install -D typescript
```

### Step 2: Initialize tsconfig.json

```bash
npx tsc --init
```

This generates a `tsconfig.json` with extensive comments. The key generated file looks like:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Step 3: Create Project Structure

```
my-typescript-project/
├── src/
│   └── index.ts
├── dist/              (auto-generated output)
├── node_modules/
├── package.json
└── tsconfig.json
```

### Step 4: Add npm Scripts

Update `package.json`:

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc --watch",
    "typecheck": "tsc --noEmit"
  }
}
```

### Step 5: Write Your First File

```typescript
// src/index.ts
const message: string = "Hello, TypeScript!";
console.log(message);
```

### Step 6: Build and Run

```bash
npm run build    # Compiles TypeScript to JavaScript
npm start        # Runs the compiled JavaScript
```

---

## tsconfig.json Basics

The `tsconfig.json` file configures the TypeScript compiler. Here are the most important options:

### `compilerOptions`

```json
{
  "compilerOptions": {
    // Compilation Target
    "target": "ES2020",           // Output ECMAScript version
    
    // Module System
    "module": "commonjs",         // Module system (commonjs, esnext, nodenext)
    "moduleResolution": "node",   // How modules are resolved
    
    // Strictness
    "strict": true,               // Enable ALL strict type-checking options
    
    // Output
    "outDir": "./dist",           // Output directory for compiled files
    "rootDir": "./src",           // Root directory of source files
    "sourceMap": true,            // Generate .map files for debugging
    
    // Interoperability
    "esModuleInterop": true,      // Allow default imports from CommonJS modules
    "allowSyntheticDefaultImports": true, // Allow synthetic default imports
    
    // Type Checking
    "noUnusedLocals": true,       // Warn on unused local variables
    "noUnusedParameters": true,   // Warn on unused parameters
    "noImplicitReturns": true,    // Error if function has implicit undefined return
    
    // Performance
    "skipLibCheck": true,         // Skip type checking of declaration files
    "incremental": true,          // Enable incremental compilation
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  }
}
```

### `include` and `exclude`

```json
{
  "include": ["src/**/*"],                    // Include all files in src/
  "exclude": ["node_modules", "dist", "**/*.test.ts"]  // Exclude patterns
}
```

### The `strict` Flag

When `strict: true` is enabled, it activates ALL of the following:

```json
{
  "compilerOptions": {
    "strict": true
    // Equivalent to enabling ALL of these:
    // "noImplicitAny": true,
    // "strictNullChecks": true,
    // "strictFunctionTypes": true,
    // "strictBindCallApply": true,
    // "strictPropertyInitialization": true,
    // "noImplicitThis": true,
    // "alwaysStrict": true,
    // "useUnknownInCatchVariables": true,
    // "exactOptionalPropertyTypes": false,
    // "noImplicitOverride": false,
    // "noPropertyAccessFromIndexSignature": false,
    // "noUncheckedIndexedAccess": false,
    // "noFallthroughCasesInSwitch": false
  }
}
```

> **Best Practice:** Always use `"strict": true` in new projects. It catches the most bugs.

---

## Running TypeScript Files

### Option 1: Compile Then Run

```bash
npx tsc src/index.ts     # Generates dist/index.js
node dist/index.js        # Runs the compiled JavaScript
```

### Option 2: Using ts-node (Recommended for Development)

```bash
npx ts-node src/index.ts
# or
npx tsx src/index.ts
```

### Option 3: Using Bun

```bash
bun run src/index.ts      # Bun runs TypeScript natively
```

### Option 4: Using Deno

```bash
deno run src/index.ts     # Deno runs TypeScript natively
```

---

## VS Code Setup

### Recommended Settings

Create a `.vscode/settings.json` in your project:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### The `typescript.tsdk` Setting

The setting `"typescript.tsdk": "node_modules/typescript/lib"` tells VS Code to use the **project-local** TypeScript version instead of its built-in version. This ensures VS Code uses the same TypeScript version as your build.

---

## Extensions

### Essential Extensions

| Extension | ID | Purpose |
|-----------|-----|---------|
| **TypeScript** | Built-in | VS Code has built-in TS support |
| **ESLint** | dbaeumer.vscode-eslint | Linting for TypeScript |
| **Prettier** | esbenp.prettier-vscode | Code formatting |
| **Error Lens** | usernamehw.errorlens | Inline error display |
| **Import Cost** | wix.vscode-import-cost | Show import sizes |

### TypeScript Inspector Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Click` / `Cmd+Click` | Go to definition |
| `F12` | Go to definition |
| `Shift+F12` | Peek references |
| `Ctrl+T` / `Cmd+T` | Go to symbol in workspace |
| `Ctrl+Shift+O` / `Cmd+Shift+O` | Go to symbol in file |
| `F2` | Rename symbol |
| `Ctrl+Space` / `Cmd+Space` | Trigger suggestions |
| `Ctrl+Shift+F` | Search across project |

### Useful Snippets

Install **TypeScript Importer** or create your own snippets for common patterns:

```json
// .vscode/typescript.code-snippets
{
  "Interface": {
    "prefix": "int",
    "body": [
      "interface ${1:Name} {",
      "\t${2:key}: ${3:type};",
      "}"
    ]
  },
  "Function": {
    "prefix": "fn",
    "body": [
      "function ${1:name}(${2:params}): ${3:void} {",
      "\t${4:// body}",
      "}"
    ]
  }
}
```

---

## ts-node

[ts-node](https://typestrong.org/ts-node/) is a TypeScript execution and REPL for Node.js that allows you to run TypeScript files directly without a separate compile step.

### Installation

```bash
npm install -D ts-node
```

### Basic Usage

```bash
# Run a TypeScript file
npx ts-node src/index.ts

# Run with arguments
npx ts-node src/cli.ts --arg value

# Interactive REPL
npx ts-node
```

### Configuration

Add to `package.json`:

```json
{
  "ts-node": {
    "compilerOptions": {
      "module": "commonjs"
    },
    "transpileOnly": true,
    "esm": true
  }
}
```

Or create a `tsconfig.ts-node.json`:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "module": "commonjs"
  }
}
```

### tsx — A Modern Alternative

[tsx](https://github.com/privatenumber/tsx) is a faster alternative to ts-node that uses esbuild under the hood:

```bash
npm install -D tsx

# Run TypeScript directly
npx tsx src/index.ts

# Watch mode
npx tsx --watch src/index.ts
```

---

## Nodemon with ts-node

[Nodemon](https://nodemon.io/) automatically restarts your Node.js application when file changes are detected. Combined with ts-node, it gives you a seamless development experience.

### Installation

```bash
npm install -D nodemon ts-node
```

### Configuration

Create a `nodemon.json`:

```json
{
  "watch": ["src"],
  "ext": "ts",
  "exec": "ts-node src/index.ts"
}
```

### package.json Scripts

```json
{
  "scripts": {
    "dev": "nodemon",
    "dev:debug": "nodemon --exec 'ts-node --inspect src/index.ts'"
  }
}
```

### Usage

```bash
npm run dev
```

Now every time you save a `.ts` file, nodemon will automatically restart the application with the latest changes.

### Alternative: tsx with watch

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts"
  }
}
```

---

## Watch Mode

TypeScript has a built-in watch mode that watches for file changes and recompiles automatically.

### Basic Watch Mode

```bash
npx tsc --watch
```

Output:

```
[12:00:00] File change detected. Starting incremental compilation...
[12:00:01] src/index.ts(5,1): error TS2322: Type 'string' is not assignable to type 'number'.
[12:00:01] Found 1 error. Watching for file changes.
```

### Watch Mode with Project References

```bash
npx tsc --build --watch
```

This is useful for monorepo setups where multiple TypeScript projects depend on each other.

### Watch Mode in package.json

```json
{
  "scripts": {
    "build:watch": "tsc --watch",
    "typecheck:watch": "tsc --noEmit --watch --preserveWatchOutput"
  }
}
```

> **Tip:** Use `--preserveWatchOutput` to prevent the terminal from clearing on each compilation, making it easier to see error history.

---

## Alternative Transpilers

While `tsc` is the official compiler, there are faster alternatives for development:

### SWC

[SWC](https://swc.rs/) is a Rust-based platform that can compile TypeScript 20-70x faster than `tsc`:

```bash
npm install -D @swc/cli @swc/core
npx swc src -d dist
```

### esbuild

[esbuild](https://esbuild.github.io/) is an extremely fast bundler that handles TypeScript:

```bash
npm install -D esbuild
npx esbuild src/index.ts --outfile=dist/index.js --bundle --platform=node
```

### Vite

[Vite](https://vitejs.dev/) uses esbuild for dev and Rollup for production, with first-class TypeScript support:

```bash
npm create vite@latest my-app -- --template vanilla-ts
```

> **Note:** SWC and esbuild skip type checking — they only transpile. Use `tsc --noEmit` separately for type checking.

---

## Summary

| Step | Command |
|------|---------|
| Install locally | `npm install -D typescript` |
| Init config | `npx tsc --init` |
| Type check | `npx tsc --noEmit` |
| Build | `npx tsc` or `npm run build` |
| Run (dev) | `npx ts-node src/index.ts` |
| Watch | `npx tsc --watch` |
| Run (production) | `node dist/index.js` |
| Use project TS | `"typescript.tsdk": "node_modules/typescript/lib"` in VS Code |

> **Best Practice:** Always use local TypeScript installation, `"strict": true` in tsconfig, and VS Code with the project-local TypeScript SDK.
