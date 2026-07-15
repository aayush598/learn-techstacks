# Declaration Files in TypeScript

## Table of Contents

1. [What Are .d.ts Files](#1-what-are-dts-files)
2. [Generating Declaration Files](#2-generating-declaration-files)
3. [Declaration Maps](#3-declaration-maps)
4. [Triple-Slash Directives](#4-triple-slash-directives)
5. [Ambient Module Declarations](#5-ambient-module-declarations)
6. [Global Declarations](#6-global-declarations)
7. [Library Declarations](#7-library-declarations)
8. [Bundled Declarations](#8-bundled-declarations)
9. [Best Practices](#9-best-practices)

---

## 1. What Are .d.ts Files

Declaration files (`.d.ts`) provide type information for JavaScript code without including any implementation. They are the backbone of TypeScript's type system when working with existing JavaScript libraries.

```typescript
// math.d.ts — Type declarations for a JavaScript math library
export function add(a: number, b: number): number;
export function subtract(a: number, b: number): number;
export function multiply(a: number, b: number): number;

// math.js — The actual JavaScript implementation (no types)
function add(a, b) { return a + b; }
function subtract(a, b) { return a - b; }
function multiply(a, b) { return a * b; }

// usage.ts
import { add, subtract } from './math';
add(1, 2);      // ✅ Type checked
subtract(5, 3); // ✅ Type checked
add('a', 'b');  // ❌ Compile error: Argument of type 'string' not assignable to 'number'
```

### Structure of a .d.ts File

```typescript
// declarations/global.d.ts

// 1. Module declarations
declare module 'my-library' {
  export function doSomething(value: string): number;
  export interface Config {
    debug: boolean;
    timeout: number;
  }
  export default class MyClass {
    constructor(config: Config);
    run(): Promise<void>;
  }
}

// 2. Global declarations
declare const API_URL: string;
declare function fetchData(url: string): Promise<any>;

// 3. Type declarations
declare type ID = string | number;
declare interface User {
  id: ID;
  name: string;
}

// 4. Augmentations
declare module 'express' {
  interface Request {
    userId?: string;
  }
}
```

---

## 2. Generating Declaration Files

### tsconfig.json Configuration

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "declarationDir": "./dist/types",
    "emitDeclarationOnly": false,
    "outDir": "./dist"
  }
}
```

### Generated Output

```bash
# Source structure:
src/
  index.ts
  utils.ts
  models/
    user.ts
    product.ts

# After compilation with declaration: true:
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
```

### What Gets Generated

```typescript
// src/models/user.ts
export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export class UserModel {
  private users: User[] = [];

  async findById(id: string): Promise<User | null> {
    return this.users.find(u => u.id === id) ?? null;
  }

  async create(data: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    const user: User = {
      id: crypto.randomUUID(),
      ...data,
      createdAt: new Date(),
    };
    this.users.push(user);
    return user;
  }
}

// dist/models/user.d.ts (generated)
export interface User {
    id: string;
    name: string;
    email: string;
    createdAt: Date;
}
export declare class UserModel {
    private users;
    findById(id: string): Promise<User | null>;
    create(data: Omit<User, 'id' | 'createdAt'>): Promise<User>;
}
```

### EmitDeclarationOnly

```json
{
  "compilerOptions": {
    "emitDeclarationOnly": true,
    "declaration": true,
    "declarationDir": "./dist/types"
  }
}
```

```bash
# Only .d.ts files are generated, no .js files
# Useful when bundling with webpack/rollup/esbuild
# The bundler handles JS output, TypeScript only provides types
```

---

## 3. Declaration Maps

Declaration maps (`.d.ts.map`) map declaration files back to their original TypeScript sources.

```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

### What Declaration Maps Enable

```typescript
// src/utils.ts
export function add(a: number, b: number): number {
  return a + b;
}

// dist/utils.d.ts
export declare function add(a: number, b: number): number;

// dist/utils.d.ts.map
{
  "version": 3,
  "file": "utils.js",
  "sourceRoot": "",
  "sources": ["../src/utils.ts"],
  "names": [],
  "mappings": "..."
}
```

### IDE Experience

```typescript
// consumer.ts
import { add } from 'my-library';

add(1, 2);
//  ↑
//  Hover: (method) add(a: number, b: number): number
//
//  Without declarationMap:
//    "Go to Definition" → jumps to dist/utils.d.ts
//
//  With declarationMap:
//    "Go to Definition" → jumps to src/utils.ts (original source!)
```

### Package.json for Published Libraries

```json
{
  "name": "my-library",
  "types": "./dist/types/index.d.ts",
  "typings": "./dist/types/index.d.ts",
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "exports": {
    ".": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

---

## 4. Triple-Slash Directives

Triple-slash directives are single-line comments containing XML-like tags that instruct the TypeScript compiler about dependencies.

```typescript
/// <reference path="./global.d.ts" />
/// <reference types="node" />
/// <reference lib="es2020" />
/// <reference no-default-lib="true" />

// Your code here
```

### reference path

```typescript
/// <reference path="./types/custom.d.ts" />

// Tells the compiler to include the specified file
// in the compilation process. Used for local declaration files.

// project/
//   src/
//     index.ts  (contains /// <reference path="../types/custom.d.ts" />)
//   types/
//     custom.d.ts
```

### reference types

```typescript
/// <reference types="node" />

// Includes type declarations from @types/node
// Equivalent to having "types": ["node"] in tsconfig.json

/// <reference types="jest" />
/// <reference types="react" />
```

### reference lib

```typescript
/// <reference lib="es2020" />
/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

// Includes specific TypeScript standard library declarations
// Useful when you need specific lib features without including all of them
```

### reference no-default-lib

```typescript
/// <reference no-default-lib="true" />

// Prevents the compiler from including the default lib (lib.d.ts)
// Used by custom TypeScript implementations
// Almost never needed in normal projects
```

### When to Use Each

```typescript
// ✅ Use reference path for local .d.ts files
/// <reference path="./types/global.d.ts" />

// ✅ Use reference types for @types packages
/// <reference types="node" />

// ✅ Use reference lib for specific standard library features
/// <reference lib="es2020.promise" />

// ✅ Use reference no-default-lib for custom TypeScript setups
/// <reference no-default-lib="true" />
```

---

## 5. Ambient Module Declarations

Ambient module declarations declare types for modules that don't have their own type declarations.

```typescript
// declarations.d.ts
declare module 'untyped-library' {
  export function doSomething(value: string): number;
  export interface Config {
    debug: boolean;
  }
  export default class Client {
    constructor(config: Config);
    connect(): Promise<void>;
  }
}
```

### Wildcard Module Declarations

```typescript
// For CSS modules, image imports, etc.
declare module '*.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.png' {
  const src: string;
  export default src;
}

declare module '*.svg' {
  const src: string;
  export default src;
}

declare module '*.json' {
  const value: any;
  export default value;
}
```

### Module Declarations with Imports

```typescript
// When the module you're declaring imports other modules
declare module 'my-plugin' {
  import { Express, Request, Response } from 'express';

  interface PluginOptions {
    secret: string;
  }

  export default function myPlugin(options: PluginOptions): {
    (req: Request, res: Response, next: () => void): void;
  };
}
```

### Augmenting Existing Modules

```typescript
// augmenting-express.d.ts
import 'express';

declare module 'express' {
  interface Request {
    userId?: string;
    sessionId?: string;
  }

  interface Response {
    json(data: any, statusCode?: number): Response;
  }
}

// Now TypeScript knows about userId on Request:
app.get('/user', (req, res) => {
  console.log(req.userId); // ✅ No error
});
```

---

## 6. Global Declarations

Global declarations add types to the global scope without requiring imports.

```typescript
// global.d.ts
declare const API_URL: string;
declare const VERSION: string;

declare function greet(name: string): string;

// Global types
declare type ID = string | number;
declare interface Window {
  myCustomProperty: string;
}

// Global namespace
declare namespace MyLib {
  interface Config {
    debug: boolean;
  }
  function init(config: Config): void;
}

// Using global declarations anywhere in the project:
console.log(API_URL); // ✅ No import needed
const id: ID = '123'; // ✅ Type is available globally
```

### Global Type Augmentation

```typescript
// extending-global.d.ts
// Augment the global scope
declare global {
  interface Window {
    __APP_VERSION__: string;
  }

  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test';
      DATABASE_URL: string;
      API_KEY: string;
    }
  }
}

// Usage
console.log(window.__APP_VERSION__);
console.log(process.env.NODE_ENV); // ✅ Type-safe
```

---

## 7. Library Declarations

Libraries ship their own declaration files as part of their npm package.

```typescript
// my-library/
//   package.json    → "types": "./dist/index.d.ts"
//   dist/
//     index.js
//     index.d.ts    ← Ships with the library

// index.d.ts (shipped with library)
export declare function add(a: number, b: number): number;
export declare function subtract(a: number, b: number): number;
export interface Config {
  debug?: boolean;
  timeout?: number;
}
export declare class Client {
  constructor(config?: Config);
  connect(): Promise<void>;
  disconnect(): Promise<void>;
}
```

### package.json for Libraries

```json
{
  "name": "my-library",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "typings": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.js"
    },
    "./types": {
      "types": "./dist/types.d.ts"
    }
  },
  "files": [
    "dist",
    "README.md"
  ]
}
```

---

## 8. Bundled Declarations

Sometimes you want to bundle all declaration files into a single `.d.ts` file.

```json
{
  "compilerOptions": {
    "declaration": true,
    "outFile": "./dist/index.d.ts",
    "emitDeclarationOnly": true,
    "module": "amd",
    "declarationMap": false
  }
}
```

```typescript
// With outFile, all declarations are bundled:
// dist/index.d.ts contains everything:
//   - All interfaces
//   - All type aliases
//   - All function declarations
//   - All class declarations
// Useful for libraries that want to ship a single declaration file
```

### dts-bundle-generator (Recommended Tool)

```bash
npm install --save-dev dts-bundle-generator
```

```json
{
  "scripts": {
    "build:types": "dts-bundle-generator --out-file dist/index.d.ts src/index.ts"
  }
}
```

```bash
# Generates a single bundled .d.ts file
npm run build:types
# Output: dist/index.d.ts (all types bundled)
```

---

## 9. Best Practices

```typescript
// 1. Always include declaration files in your library
{
  "types": "./dist/index.d.ts"
}

// 2. Use declarationMap for source navigation
{
  "declarationMap": true
}

// 3. Use 'export type' for type-only exports
export type { User, Product } from './models';

// 4. Don't put implementation in .d.ts files
// ❌
declare function add(a: number, b: number): number {
  return a + b; // Error: Implementation in declaration file
}

// ✅
declare function add(a: number, b: number): number;

// 5. Use wildcard module declarations for asset imports
declare module '*.css';
declare module '*.png';

// 6. Augment modules, don't replace them
// ❌ Overwriting entire module declaration
declare module 'express' {
  // This replaces ALL of express's types
}

// ✅ Augmenting specific parts
import 'express';
declare module 'express' {
  interface Request {
    userId?: string;
  }
}

// 7. Organize declarations in a types/ directory
// types/
//   global.d.ts        — Global declarations
//   custom-modules.d.ts — Module declarations
//   augmentations.d.ts  — Module augmentations

// 8. Include types directory in tsconfig
{
  "include": ["src/**/*", "types/**/*"]
}
```

---

## Interview Questions

**Q1**: What is the difference between `.d.ts` and `.ts` files?
**A**: `.d.ts` files contain only type declarations (no implementation code). They describe the shape of existing JavaScript code. `.ts` files contain both types and implementation.

**Q2**: When would you use `emitDeclarationOnly`?
**A**: When you're using a separate bundler (webpack, rollup, esbuild) for JavaScript output and only need TypeScript for type checking and declaration generation.

**Q3**: What is a declaration map and why would you use it?
**A**: A `.d.ts.map` file maps declaration files back to original TypeScript source, enabling IDEs to "Go to Definition" and jump to the actual source code instead of the generated declaration file.

**Q4**: What are wildcard module declarations and when are they useful?
**A**: Wildcard declarations like `declare module '*.css'` handle imports of file types that TypeScript doesn't natively understand. They're essential for CSS modules, image imports, and JSON imports.

**Q5**: How do you augment an existing module's types?
**A**: Import the module, then use `declare module 'module-name'` to add new members to existing interfaces. This is done in `.d.ts` files and preserves the original types while adding new ones.
