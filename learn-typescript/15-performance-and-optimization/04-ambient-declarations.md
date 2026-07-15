# Ambient Declarations in TypeScript

## Table of Contents

1. [The declare Keyword](#1-the-declare-keyword)
2. [declare module](#2-declare-module)
3. [declare global](#3-declare-global)
4. [declare function](#4-declare-function)
5. [declare class](#5-declare-class)
6. [declare namespace](#6-declare-namespace)
7. [Ambient vs Module Declarations](#7-ambient-vs-module-declarations)
8. [.d.ts File Structure](#8-dts-file-structure)
9. [@types Packages](#9-types-packages)
10. [Best Practices](#10-best-practices)

---

## 1. The declare Keyword

The `declare` keyword tells TypeScript that something exists elsewhere (in JavaScript, native APIs, or external libraries) and should not be compiled to JavaScript.

```typescript
// declare tells TypeScript: "Trust me, this exists at runtime"
// It produces NO JavaScript output

// Variable declarations
declare const PI: number;
declare let counter: number;

// Function declarations
declare function greet(name: string): string;

// Class declarations
declare class MyClass {
  constructor(name: string);
  greet(): string;
  name: string;
}

// Type/Interface declarations (declare is optional here)
type ID = string | number; // No declare needed
interface User {           // No declare needed
  id: ID;
  name: string;
}
```

### Why declare Is Needed

```typescript
// Without declare — TypeScript tries to compile this to JavaScript:
const PI = 3.14159; // Compiles to: const PI = 3.14159;

// With declare — TypeScript only provides type information:
declare const PI: number; // Compiles to: nothing
// TypeScript knows PI is a number, but doesn't generate code

// This is crucial for:
// 1. Browser globals (window, document, navigator)
// 2. Node.js globals (process, __dirname, __filename)
// 3. Native APIs (fetch, setTimeout, Promise)
// 4. Third-party JavaScript libraries without types
```

---

## 2. declare module

`declare module` provides type information for JavaScript modules that don't have their own type declarations.

```typescript
// declarations.d.ts

// Basic module declaration
declare module 'my-untyped-library' {
  export function doSomething(value: string): number;
  export interface Config {
    debug: boolean;
    timeout?: number;
  }
  export default class Client {
    constructor(config: Config);
    connect(): Promise<void>;
    disconnect(): Promise<void>;
    send(data: unknown): Promise<unknown>;
  }
}
```

### Module Declaration with Dependencies

```typescript
// When the module uses types from other packages
declare module 'my-express-plugin' {
  import { Request, Response, NextFunction } from 'express';

  interface PluginOptions {
    secret: string;
    excludePaths?: string[];
  }

  export default function plugin(options: PluginOptions): 
    (req: Request, res: Response, next: NextFunction) => void;
}
```

### Wildcard Module Declarations

```typescript
// Handle any file matching a pattern
declare module '*.css' {
  const classes: Record<string, string>;
  export default classes;
}

declare module '*.module.css' {
  const classes: Record<string, string>;
  export default classes;
}

declare module '*.png' {
  const value: string;
  export default value;
}

declare module '*.svg' {
  const content: string;
  export default content;
}

declare module '*.json' {
  const value: any;
  export default value;
}

// Usage in TypeScript:
import styles from './Button.module.css';
import logo from './logo.png';

// TypeScript knows styles is Record<string, string>
// and logo is string
```

### Module Declaration Patterns

```typescript
// Pattern 1: Declare module with all exports
declare module 'my-lib' {
  export const version: string;
  export function init(config: object): void;
  export class Client {
    constructor();
    connect(): Promise<void>;
  }
}

// Pattern 2: Declare module with default export
declare module 'my-lib' {
  export default class Client {
    constructor(config: { apiKey: string });
    connect(): Promise<void>;
  }
}

// Pattern 3: Declare module with namespace
declare module 'my-lib' {
  namespace MyLib {
    interface Config {
      apiKey: string;
    }
    function init(config: Config): void;
  }
  export = MyLib;
}

// Pattern 4: Ambient module with import
declare module 'my-plugin' {
  import type { Application } from 'express';
  export default function plugin(app: Application, options?: object): void;
}
```

---

## 3. declare global

`declare global` adds type declarations to the global scope from within a module.

```typescript
// In a .d.ts file or a module with exports
export {}; // Makes this file a module

declare global {
  // Global variables
  const API_VERSION: string;
  const IS_DEVELOPMENT: boolean;

  // Global functions
  function trackEvent(eventName: string, data?: object): void;

  // Global types
  type Nullable<T> = T | null;
  type Optional<T> = T | undefined;

  // Global interfaces
  interface Window {
    __APP_CONFIG__: {
      apiUrl: string;
      version: string;
    };
    analytics: {
      track(event: string): void;
    };
  }

  // Augment Node.js types
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test';
      DATABASE_URL: string;
      API_KEY: string;
      PORT?: string;
    }
  }
}

// Now these are available globally:
console.log(API_VERSION);
trackEvent('page_view');
process.env.DATABASE_URL; // ✅ Type-safe
window.__APP_CONFIG__.apiUrl; // ✅ Type-safe
```

### When to Use declare global

```typescript
// ✅ Use declare global in module files
// utils.d.ts (module file because it has 'export')
export {};

declare global {
  interface Window {
    myApp: { version: string };
  }
}

// ❌ Don't use declare global in script files
// global.d.ts (script file — no exports)
// Just use declare directly:
declare const API_URL: string;
declare function fetchData(url: string): Promise<any>;
```

---

## 4. declare function

Declares the type signature of a function that exists in JavaScript.

```typescript
// Basic function declaration
declare function setTimeout(
  handler: TimerHandler,
  timeout?: number,
  ...arguments: any[]
): number;

// Function with overloads
declare function fetch(
  input: RequestInfo,
  init?: RequestInit
): Promise<Response>;

// Function with generic types
declare function useState<T>(
  initialValue: T | (() => T)
): [T, (newValue: T | ((prev: T) => T)) => void];

// Custom function declarations
declare function log(message: string, level?: 'info' | 'warn' | 'error'): void;
declare function formatCurrency(amount: number, currency?: string): string;
declare function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void;

// Usage:
log('Hello', 'info');
formatCurrency(100, 'USD');
const debouncedFn = debounce((x: number) => console.log(x), 300);
```

---

## 5. declare class

Declares the shape of a JavaScript class.

```typescript
// Basic class declaration
declare class EventEmitter {
  constructor();
  on(event: string, listener: (...args: any[]) => void): this;
  off(event: string, listener: (...args: any[]) => void): this;
  emit(event: string, ...args: any[]): boolean;
}

// Class with generics
declare class Collection<T> {
  constructor(items?: T[]);
  add(item: T): void;
  remove(item: T): boolean;
  find(predicate: (item: T) => boolean): T | undefined;
  filter(predicate: (item: T) => boolean): Collection<T>;
  toArray(): T[];
  get length(): number;
}

// Class with static members
declare class MathUtils {
  static PI: number;
  static E: number;
  static abs(x: number): number;
  static random(): number;
}

// Abstract class declaration
declare abstract class BaseRepository<T> {
  constructor(tableName: string);
  abstract findById(id: string): Promise<T | null>;
  abstract findAll(): Promise<T[]>;
  abstract create(data: Omit<T, 'id'>): Promise<T>;
  abstract update(id: string, data: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;
}
```

---

## 6. declare namespace

Namespaces group related type declarations under a single name.

```typescript
// Namespace for a library
declare namespace Express {
  interface Request {
    body: any;
    params: Record<string, string>;
    query: Record<string, string>;
    headers: Record<string, string | string[]>;
  }

  interface Response {
    status(code: number): Response;
    json(data: any): Response;
    send(data: any): Response;
  }

  interface NextFunction {
    (err?: any): void;
  }
}

// Namespace for constants
declare namespace HTTP_STATUS {
  const OK: 200;
  const CREATED: 201;
  const BAD_REQUEST: 400;
  const UNAUTHORIZED: 401;
  const NOT_FOUND: 404;
  const INTERNAL_SERVER_ERROR: 500;
}

// Namespace with functions
declare namespace Logger {
  function info(message: string, ...args: any[]): void;
  function warn(message: string, ...args: any[]): void;
  function error(message: string, ...args: any[]): void;
  function debug(message: string, ...args: any[]): void;
}

// Usage
HTTP_STATUS.OK; // 200
Logger.info('Server started');
```

### Namespace vs Module

```typescript
// ✅ Modern: Use ES modules
// math.ts
export function add(a: number, b: number) { return a + b; }

// ❌ Legacy: Use namespaces
// math.ts
namespace Math {
  export function add(a: number, b: number) { return a + b; }
}

// Namespaces are primarily used in declaration files (.d.ts)
// to organize type declarations
```

---

## 7. Ambient vs Module Declarations

```typescript
// AMBIENT declarations (in .d.ts files)
// - Declare types for things that exist in the global scope
// - No import/export statements in the file
// - Types are available everywhere without importing

// ambient.d.ts (script file — no module boundary)
declare const API_URL: string;
declare function log(message: string): void;

// Available anywhere without import:
console.log(API_URL);
log('hello');

// MODULE declarations (in .d.ts files)
// - Declare types for things in a specific module
// - The file acts as a module (has imports/exports or declares a module)
// - Types must be imported to use

// module.d.ts
declare module 'my-lib' {
  export function doSomething(): void;
  export interface Config {
    debug: boolean;
  }
}

// Must import to use:
import { doSomething, Config } from 'my-lib';
doSomething();
```

### Decision Guide

```
┌─────────────────────────────────────────┐
│ Do you need to declare types for...     │
├─────────────────────────────────────────┤
│                                         │
│ Browser/Node globals (window, process)  │
│ → declare global { }                    │
│                                         │
│ A JavaScript library without types      │
│ → declare module 'library-name' { }     │
│                                         │
│ Asset imports (CSS, images)             │
│ → declare module '*.css' { }            │
│                                         │
│ Your own global constants               │
│ → declare const / declare function      │
│                                         │
│ A namespace of related types            │
│ → declare namespace Name { }            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 8. .d.ts File Structure

### Recommended Structure

```typescript
// types/
//   global.d.ts         — Global declarations
//   modules.d.ts        — Module declarations
//   augmentations.d.ts  — Module augmentations

// ==========================================
// types/global.d.ts
// ==========================================

// Global constants
declare const APP_NAME: string;
declare const APP_VERSION: string;

// Global types
type ID = string | number;
type Timestamp = number;
type Nullable<T> = T | null;

// ==========================================
// types/modules.d.ts
// ==========================================

// CSS modules
declare module '*.css' {
  const classes: Record<string, string>;
  export default classes;
}

// Image imports
declare module '*.png' {
  const src: string;
  export default src;
}

// Untyped third-party libraries
declare module 'old-library' {
  export function doStuff(): void;
}

// ==========================================
// types/augmentations.d.ts
// ==========================================

// Augment Express Request
import 'express';
declare module 'express' {
  interface Request {
    userId?: string;
    sessionId?: string;
  }
}

// Augment Process Env
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
  }
}
```

---

## 9. @types Packages

`@types` packages provide TypeScript declarations for JavaScript libraries.

```bash
# Install type declarations
npm install --save-dev @types/node
npm install --save-dev @types/express
npm install --save-dev @types/jest

# Type declarations are automatically included
# when @types/package-name is installed
```

### How @types Works

```bash
# When you install:
npm install --save-dev @types/express

# TypeScript automatically finds:
node_modules/@types/express/index.d.ts

# No need for triple-slash directives or types config
```

### tsconfig.json types Configuration

```json
{
  "compilerOptions": {
    "types": ["node", "jest", "react"],
    // ↑ Only these @types packages are included
    // Others are ignored (useful for controlling global pollution)
    
    "typeRoots": ["./types", "./node_modules/@types"],
    // ↑ Where to look for type declarations
  }
}
```

### Finding and Installing Types

```bash
# Search for types
npm search @types/express

# Check if types exist for a package
npm info @types/express

# If no @types package exists, create your own:
# types/my-library.d.ts
declare module 'my-library' {
  export function doSomething(value: string): number;
}
```

### Contributing to DefinitelyTyped

```bash
# Clone DefinitelyTyped
git clone https://github.com/DefinitelyTyped/DefinitelyTyped

# Install dependencies
npm install

# Create new types
cd types/new-package
# ... write type declarations ...

# Test types
npm run test new-package
```

---

## 10. Best Practices

```typescript
// 1. Organize declarations in a types/ directory
// types/
//   global.d.ts
//   modules.d.ts
//   augmentations.d.ts

// 2. Use 'declare module' for untyped libraries
declare module 'untyped-lib' {
  export function doSomething(): void;
}

// 3. Use 'declare global' for global augmentations
export {};
declare global {
  interface Window {
    myApp: { version: string };
  }
}

// 4. Prefer @types packages over custom declarations
// ✅ npm install --save-dev @types/express
// ❌ declare module 'express' { ... }

// 5. Don't put implementation in declaration files
// ❌ declare function add(a: number, b: number) { return a + b; }
// ✅ declare function add(a: number, b: number): number;

// 6. Use wildcard declarations for asset imports
declare module '*.css';
declare module '*.png';

// 7. Keep declaration files focused and small
// One .d.ts file per concern:
//   global.d.ts — global types
//   modules.d.ts — module declarations
//   augmentations.d.ts — module augmentations

// 8. Use TypeScript's built-in types when possible
// ❌ declare type Nullable<T> = T | null; // Already in TypeScript
// ✅ Use T | null directly

// 9. Document complex declarations
declare module 'complex-library' {
  /**
   * Initializes the library with the given configuration.
   * @param config - The configuration object
   * @returns A promise that resolves when initialization is complete
   */
  export function init(config: Config): Promise<void>;
}
```

---

## Interview Questions

**Q1**: What is the difference between `declare` and a regular declaration?
**A**: `declare` tells TypeScript that a variable/function/class exists elsewhere (in JavaScript, native APIs, etc.) without generating any code. Regular declarations generate JavaScript output.

**Q2**: When would you use `declare global` vs `declare module`?
**A**: `declare global` adds types to the global scope from within a module file. `declare module` provides types for a specific JavaScript module. Use `declare global` for window/process augmentation, `declare module` for untyped libraries.

**Q3**: What are ambient module declarations and when are they needed?
**A**: Ambient module declarations (`declare module 'name'`) provide types for JavaScript modules that don't have their own type declarations. They're needed when you use a library that doesn't ship `.d.ts` files and doesn't have an `@types` package.

**Q4**: How do wildcard module declarations work?
**A**: Wildcard declarations like `declare module '*.css'` match any import ending with that extension. They're essential for CSS modules, image imports, and other non-JavaScript assets.

**Q5**: What is the difference between ambient declarations and module declarations?
**A**: Ambient declarations (in script `.d.ts` files) are available globally without importing. Module declarations (in module `.d.ts` files or files with imports/exports) require importing to use.
