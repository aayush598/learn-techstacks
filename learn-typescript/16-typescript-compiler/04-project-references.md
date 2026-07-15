# TypeScript Project References

## Table of Contents

1. [What Are Project References](#1-what-are-project-references)
2. [Composite Projects](#2-composite-projects)
3. [tsconfig References](#3-tsconfig-references)
4. [Building Referenced Projects](#4-building-referenced-projects)
5. [Incremental Builds with References](#5-incremental-builds-with-references)
6. [Monorepo with Project References](#6-monorepo-with-project-references)
7. [Build Mode](#7-build-mode)

---

## 1. What Are Project References

Project references allow you to split a TypeScript project into multiple sub-projects that can be compiled independently and in parallel.

```
Without project references:
┌─────────────────────────────────┐
│          tsc (one big project)   │
│  ┌─────────┐  ┌──────────────┐  │
│  │  core   │  │     app      │  │
│  │ 200 files│  │  1000 files  │  │
│  └─────────┘  └──────────────┘  │
│  Compile time: 30 seconds       │
└─────────────────────────────────┘

With project references:
┌─────────────────┐    ┌─────────────────┐
│  tsc (core)     │    │  tsc (app)      │
│  200 files      │    │  1000 files      │
│  Compile: 5s    │───►│  Compile: 10s    │
└─────────────────┘    └─────────────────┘
                       Total: 10s (parallel)
```

### Benefits

1. **Faster builds**: Only recompile changed projects
2. **Better encapsulation**: Each project has clear boundaries
3. **Incremental compilation**: Cache build results per project
4. **Type safety across projects**: References maintain type checking

---

## 2. Composite Projects

A composite project is one that can be referenced by other projects.

```json
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### What composite: true Enables

```json
{
  "composite": true
  // Implies:
  // "declaration": true    — Generate .d.ts files
  // "incremental": true    — Enable incremental compilation
}
```

### Composite Project Structure

```
packages/core/
  src/
    index.ts
    utils.ts
    models/
      user.ts
      product.ts
  dist/
    index.js
    index.d.ts
    index.d.ts.map
    utils.js
    utils.d.ts
    utils.d.ts.map
    models/
      user.js
      user.d.ts
      user.d.ts.map
      product.js
      product.d.ts
      product.d.ts.map
    tsconfig.tsbuildinfo
  package.json
  tsconfig.json
```

---

## 3. tsconfig References

Reference other projects in your tsconfig.

```json
// packages/app/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "references": [
    { "path": "../core" },
    { "path": "../utils" }
  ]
}
```

### Reference Syntax

```json
// Simple reference
{ "path": "../core" }

// Reference with specific config
{ "path": "../core", "prepend": true }

// Multiple references
{
  "references": [
    { "path": "../core" },
    { "path": "../utils" },
    { "path": "../models" }
  ]
}
```

### Root tsconfig.json

```json
// Root tsconfig.json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/utils" },
    { "path": "./packages/app" }
  ]
}
```

---

## 4. Building Referenced Projects

### Build All Projects

```bash
# Build all referenced projects
tsc --build
# or
tsc -b

# Build with verbose output
tsc --build --verbose

# Clean build (rebuild everything)
tsc --build --clean

# Force rebuild
tsc --build --force
```

### Build Specific Projects

```bash
# Build only the core project
tsc --build packages/core

# Build core and its dependents
tsc --build packages/core --verbose

# Build with watch mode
tsc --build --watch
```

### Build Order

```json
// packages/app/tsconfig.json
{
  "references": [
    { "path": "../core" },
    { "path": "../utils" }
  ]
}

// TypeScript builds dependencies first:
// 1. Build core (no dependencies)
// 2. Build utils (no dependencies)
// 3. Build app (depends on core and utils)
```

---

## 5. Incremental Builds with References

### How Incremental Builds Work

```bash
# First build: full compilation
tsc --build --verbose
# Output:
# Projects in this build:
#   * packages/core/tsconfig.json
#   * packages/utils/tsconfig.json
#   * packages/app/tsconfig.json
#
# Building project 'packages/core/tsconfig.json'...
# Updating output timestamps of project 'packages/core/tsconfig.json'...
# Building project 'packages/utils/tsconfig.json'...
# Updating output timestamps of project 'packages/utils/tsconfig.json'...
# Building project 'packages/app/tsconfig.json'...
# Updating output timestamps of project 'packages/app/tsconfig.json'...

# Second build (no changes): near-instant
tsc --build --verbose
# Output:
# Projects in this build:
#   * packages/core/tsconfig.json
#   * packages/utils/tsconfig.json
#   * packages/app/tsconfig.json
#
# Projects to build are up to date

# Third build (one file changed in core):
tsc --build --verbose
# Output:
# Building project 'packages/core/tsconfig.json'...
# Building project 'packages/app/tsconfig.json'...
# (utils not rebuilt — no changes)
```

### tsBuildInfoFile

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo"
  }
}
```

```bash
# tsBuildInfoFile contains:
# - File hashes
# - Semantic diagnostics
# - Affected file lists
# - Build timestamps

# This allows TypeScript to:
# 1. Skip unchanged files
# 2. Skip unchanged projects
# 3. Only rebuild what's necessary
```

---

## 6. Monorepo with Project References

### Example: Full Monorepo Setup

```json
// Root package.json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "build": "tsc --build",
    "build:watch": "tsc --build --watch",
    "clean": "tsc --build --clean"
  }
}

// Root tsconfig.json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/api" },
    { "path": "./packages/web" },
    { "path": "./packages/shared" }
  ]
}
```

### Package Setup

```json
// packages/core/package.json
{
  "name": "@myorg/core",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.js"
    }
  }
}

// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

### Inter-Package Dependencies

```json
// packages/api/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "references": [
    { "path": "../core" },
    { "path": "../shared" }
  ],
  "include": ["src/**/*"]
}

// packages/web/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "references": [
    { "path": "../core" },
    { "path": "../api" },
    { "path": "../shared" }
  ],
  "include": ["src/**/*"]
}
```

---

## 7. Build Mode

### tsc --build

```bash
# Build all projects
tsc --build

# Build with options
tsc --build --verbose    # Show build progress
tsc --build --clean      # Clean build outputs
tsc --build --force      # Force full rebuild
tsc --build --watch      # Watch mode

# Build specific project
tsc --build packages/core

# Build with specific tsconfig
tsc --build --project tsconfig.build.json
```

### Build Mode vs Regular Mode

```bash
# Regular mode (tsc)
# - Compiles all files matching include/exclude
# - No dependency tracking
# - No incremental builds
# - Single project only

# Build mode (tsc --build)
# - Compiles referenced projects
# - Tracks dependencies between projects
# - Supports incremental builds
# - Parallel compilation
# - Better for monorepos
```

### CI/CD Integration

```json
// package.json
{
  "scripts": {
    "build": "tsc --build",
    "build:ci": "tsc --build --force",
    "typecheck": "tsc --build --noEmit",
    "clean": "tsc --build --clean"
  }
}
```

```yaml
# .github/workflows/build.yml
- name: Build
  run: npm run build

- name: Type Check
  run: npm run typecheck
```

---

## Interview Questions

**Q1**: What are project references and when should you use them?
**A**: Project references split a TypeScript project into sub-projects that compile independently. Use them for: monorepos, large codebases, teams working on different parts, or when build times are too long.

**Q2**: What does `composite: true` do?
**A**: It enables a project to be referenced by other projects. It implies `declaration: true` and `incremental: true`. It's required for project references to work.

**Q3**: How do you build referenced projects?
**A**: Use `tsc --build` or `tsc -b`. This compiles all referenced projects in dependency order, supporting parallel compilation and incremental builds.

**Q4**: What is the difference between `tsc` and `tsc --build`?
**A**: `tsc` compiles a single project. `tsc --build` compiles multiple referenced projects with dependency tracking, incremental builds, and parallel compilation.

**Q5**: How do project references help with monorepos?
**A**: They allow each package to be compiled independently. TypeScript tracks dependencies and only recompiles changed packages. This dramatically reduces build times in large monorepos.
