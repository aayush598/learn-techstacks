# Namespaces in TypeScript

## Table of Contents

- [Overview](#overview)
- [Namespace Syntax](#namespace-syntax)
- [Namespace Merging](#namespace-merging)
- [Namespace Augmentation](#namespace-augmentation)
- [Ambient Namespaces](#ambient-namespaces)
- [Namespaces vs Modules](#namespaces-vs-modules)
- [When Namespaces Are Still Useful](#when-namespaces-are-still-useful)
- [Declaration Files with Namespaces](#declaration-files-with-namespaces)
- [Global Namespaces](#global-namespaces)
- [Nested Namespaces](#nested-namespaces)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Namespaces (formerly called "internal modules") provide a way to organize code into logical groupings and avoid name collisions. They compile to JavaScript IIFEs (Immediately Invoked Function Expressions) that create closure-scoped objects. While modules are the standard for code organization, namespaces still have specific use cases.

```typescript
// Namespaces create a scope — code inside is NOT global
namespace Validation {
  export interface Validator {
    validate(value: string): boolean;
  }

  export class EmailValidator implements Validator {
    validate(value: string): boolean {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }
  }
}

// Usage
const validator = new Validation.EmailValidator();
validator.validate('test@example.com'); // true
```

### What Namespaces Compile To

```javascript
// The compiled JavaScript uses IIFEs and namespaces
var Validation;
(function (Validation) {
  class EmailValidator {
    validate(value) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }
  }
  Validation.EmailValidator = EmailValidator;
})(Validation || (Validation = {}));
```

---

## Namespace Syntax

### Basic Declaration

```typescript
namespace Geometry {
  export interface Point {
    x: number;
    y: number;
  }

  export interface Line {
    start: Point;
    end: Point;
  }

  export function distance(p1: Point, p2: Point): number {
    return Math.sqrt(
      Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2)
    );
  }

  export function midpoint(p1: Point, p2: Point): Point {
    return {
      x: (p1.x + p2.x) / 2,
      y: (p1.y + p2.y) / 2,
    };
  }
}

// All usage goes through the namespace
const a: Geometry.Point = { x: 0, y: 0 };
const b: Geometry.Point = { x: 3, y: 4 };
console.log(Geometry.distance(a, b)); // 5
```

### Access Modifiers in Namespaces

```typescript
namespace Banking {
  // Private by default (no export)
  function calculateInterest(principal: number, rate: number): number {
    return principal * rate;
  }

  // Public (exported)
  export interface Account {
    id: string;
    balance: number;
  }

  export class SavingsAccount implements Account {
    id: string;
    balance: number;

    constructor(id: string, initialBalance: number) {
      this.id = id;
      this.balance = initialBalance;
    }

    addInterest(rate: number): void {
      // Can access private function within the namespace
      const interest = calculateInterest(this.balance, rate);
      this.balance += interest;
    }
  }
}
```

### Namespaces Can Span Multiple Files

```typescript
// file1.ts
namespace App {
  export interface Config {
    apiUrl: string;
  }
}

// file2.ts
namespace App {
  export class ApiClient {
    constructor(private config: Config) {}
    // Config is available from file1.ts
  }
}

// file3.ts
namespace App {
  export function createApp(config: Config): ApiClient {
    return new ApiClient(config);
  }
  // Both Config and ApiClient are available
}
```

---

## Namespace Merging

TypeScript automatically merges namespaces with the same name across different declarations, even in different files.

### Basic Merging

```typescript
// types/user.ts
namespace Models {
  export interface User {
    id: number;
    name: string;
  }
}

// types/post.ts
namespace Models {
  export interface Post {
    id: number;
    title: string;
    authorId: number;
  }
}

// Both User and Post are available under Models
const user: Models.User = { id: 1, name: 'Alice' };
const post: Models.Post = { id: 1, title: 'Hello', authorId: 1 };
```

### Merging Interfaces in Namespaces

```typescript
// When merging interfaces with the same name inside a namespace,
// they are combined (declaration merging).

namespace Animals {
  export interface Dog {
    breed: string;
    bark(): void;
  }
}

namespace Animals {
  export interface Dog {
    age: number;  // adds age to the existing Dog interface
    fetch(): void;
  }
}

// Dog now has: breed, bark(), age, fetch()
const myDog: Animals.Dog = {
  breed: 'Labrador',
  age: 3,
  bark() { console.log('Woof!'); },
  fetch() { console.log('Fetching!'); },
};
```

### Namespace + Class + Enum Merging

```typescript
// A namespace can merge with a class, enum, or function

class Observable<T> {
  constructor(private value: T) {}
  getValue(): T { return this.value; }
}

// Augment the class with static members via namespace merging
namespace Observable {
  export function fromPromise<T>(promise: Promise<T>): Observable<T | undefined> {
    let value: T | undefined;
    promise.then((v) => (value = v));
    return new Observable(value);
  }
}

// Now Observable has both instance and static members
const obs = new Observable(42);
Observable.fromPromise(fetch('/api'));
```

### Merging Rules

| Combination | Allowed | Result |
|---|---|---|
| Namespace + Namespace | Yes | Merged into single namespace |
| Namespace + Class | Yes | Adds static members to class |
| Namespace + Function | Yes | Adds overloaded signatures |
| Namespace + Enum | Yes | Adds types to enum |

---

## Namespace Augmentation

Namespace augmentation adds new members to existing namespaces in other files, commonly used with declaration files.

```typescript
// declarations.d.ts
declare namespace Express {
  interface Request {
    userId?: string;
    sessionId?: string;
  }

  interface Response {
    json(data: Record<string, unknown>): void;
  }
}

// Now every Express Request in your codebase has userId and sessionId
app.get('/profile', (req, res) => {
  console.log(req.userId);    // TypeScript knows about this
  console.log(req.sessionId); // No error
});
```

### Augmenting Global Namespace

```typescript
// global.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'production' | 'test';
      DATABASE_URL: string;
      API_KEY: string;
      PORT?: string;
    }
  }
}

export {}; // must be a module

// Now process.env is fully typed
const dbUrl: string = process.env.DATABASE_URL; // string, not string | undefined
const port: string | undefined = process.env.PORT;
```

---

## Ambient Namespaces

Ambient namespaces (in `.d.ts` files) describe the shape of existing JavaScript libraries that don't have type definitions.

```typescript
// types/my-legacy-lib.d.ts
declare namespace MyLegacyLib {
  function init(config: { debug: boolean }): void;
  function fetchData(url: string, callback: (data: string) => void): void;

  interface Cache {
    get(key: string): string | undefined;
    set(key: string, value: string): void;
    clear(): void;
  }

  const cache: Cache;
}

// In your TypeScript code:
MyLegacyLib.init({ debug: true });
MyLegacyLib.fetchData('/api/users', (data) => {
  console.log(data);
});
MyLegacyLib.cache.set('key', 'value');
```

### Describing UMD Libraries

```typescript
// Many libraries use UMD (Universal Module Definition)
// which can be imported as module or used as global

// types/jquery.d.ts (simplified)
declare module 'jquery' {
  export function $(selector: string): JQuery;
  export function ajax(settings: JQueryAjaxSettings): JQueryXHR;
}

declare namespace JQuery {
  interface HTMLElement {
    html(content?: string): string;
    css(properties: Record<string, string>): JQuery;
    on(events: string, handler: () => void): JQuery;
  }
}

// Global usage (if jQuery is loaded via script tag)
const elem = $('#my-element');
elem.html('Hello').css({ color: 'red' });
```

---

## Namespaces vs Modules

### Key Differences

| Feature | Namespaces | Modules |
|---|---|---|
| Runtime behavior | IIFEs, object properties | `require()` or `import` |
| File relationship | Multiple namespaces per file | One module per file |
| Dependency management | Manual (concat, reference) | Automatic (import resolution) |
| Tree-shaking | Not possible | Possible with ESM |
| Browser support | Via bundler or script tags | Native (modern browsers) |
| Isolation | Closure scope | Module scope |
| Declaration merging | Supported | Not supported (across files) |
| Configuration | Triple-slash references | tsconfig.json paths |

### When Modules Win

```typescript
// Modules: clean, static, tree-shakable
import { User, Post } from './models';
import { formatDate } from './utils';

// Namespaces: verbose, not tree-shakable
// namespace Models {
//   // Everything must be here or use triple-slash references
// }
```

### When Namespaces Win

```typescript
// Namespace declaration merging — you can't do this with modules!

// Declaration merging lets you extend any class or interface
// without modifying the original file.

// Example: extending a third-party library's types
namespace ThirdPartyLib {
  export interface Config {
    timeout: number;
  }
}

// In another file, augment it:
namespace ThirdPartyLib {
  export interface Config {
    retries: number;  // merged!
  }
}

const config: ThirdPartyLib.Config = {
  timeout: 5000,
  retries: 3,
};
```

---

## When Namespaces Are Still Useful

### 1. Declaration Merging / Type Augmentation

```typescript
// Extend third-party types without modifying source
declare namespace AWS {
  interface S3 {
    customMethod(): void;
  }
}
```

### 2. Organizing Ambient Type Definitions

```typescript
// types/global.d.ts
declare namespace MyCompany {
  namespace Api {
    interface Response<T> {
      data: T;
      status: number;
      message: string;
    }
  }

  namespace Utils {
    function formatDate(date: Date): string;
    function parseCurrency(value: string): number;
  }
}

// Clean, organized global types without module imports
```

### 3. Libraries Without Module Support

```typescript
// For old JavaScript libraries that expose globals
declare namespace Three {
  class Scene {
    add(object: Object3D): void;
  }
  class Camera { /* ... */ }
  class WebGLRenderer { /* ... */ }
}
```

### 4. Plugin/Extension Patterns

```typescript
namespace PluginSystem {
  export interface Plugin {
    name: string;
    version: string;
    install(): void;
  }

  const plugins: Plugin[] = [];

  export function register(plugin: Plugin): void {
    plugins.push(plugin);
  }

  export function loadAll(): void {
    plugins.forEach((p) => p.install());
  }
}
```

---

## Declaration Files with Namespaces

```typescript
// types/env.d.ts

// Declare a namespace for environment variables
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
    PORT?: string;
    DATABASE_URL: string;
  }
}

// Declare global constants
declare const __DEV__: boolean;
declare const __VERSION__: string;

// Declare global types
declare type Nullable<T> = T | null;
declare type AsyncFunction<T> = () => Promise<T>;
```

### Reference Triple-Slash Directive

```typescript
// For namespaces in non-module files, use triple-slash references
/// <reference types="node" />
/// <reference path="./custom-types.d.ts" />

// These directives tell TypeScript to include the types from those files
// before compiling this file.
```

---

## Global Namespaces

```typescript
// In a non-module file (no import/export statements),
// all declarations are global

// globals.ts (no import/export)
interface User {
  id: number;
  name: string;
}

function createDefaultUser(): User {
  return { id: 0, name: 'Anonymous' };
}

// These are now available globally!
// Be careful: this pollutes the global scope
```

### Preventing Global Pollution

```typescript
// In a .ts file with import/export, everything is module-scoped
export interface User {
  id: number;
  name: string;
}

// User is NOT global — must be imported
import { User } from './types';
```

---

## Best Practices

1. **Prefer modules over namespaces** for code organization — namespaces are a legacy pattern.

2. **Use namespaces for type augmentation** — declaration merging is uniquely powerful.

3. **Use `declare namespace`** in `.d.ts` files for ambient type definitions.

4. **Avoid global namespaces** in application code — polluting the global scope causes conflicts.

5. **Use triple-slash references** only when working with legacy code that doesn't use modules.

6. **Combine namespace + class merging** to add static methods to classes from other packages.

7. **Keep namespace usage confined to `.d.ts` files** — avoid runtime namespaces in new code.

8. **Namespace merging is for types, not implementations** — prefer module patterns for runtime code.

9. **Use `declare global`** to augment global types from within module files.

10. **When refactoring, convert namespaces to modules** — it enables tree-shaking and better tooling.

---

## Interview Questions

### Q1: What is the difference between a namespace and a module?

**Answer**: A namespace creates a named scope at compile time using IIFEs — it doesn't perform any module loading. A module is a file with `import`/`export` that uses a module system (ESM or CJS) for dependency management. Namespaces support declaration merging; modules don't. Modules enable tree-shaking and static analysis.

### Q2: When would you use namespaces in 2024+?

**Answer**: Primarily for: (1) declaration merging to augment third-party types, (2) ambient type definitions in `.d.ts` files, (3) typing old JavaScript libraries that expose globals, (4) organizing global type declarations. They should NOT be used for application code organization.

### Q3: Can namespaces span multiple files?

**Answer**: Yes. TypeScript automatically merges namespace declarations with the same name across multiple files. All members are combined. This is useful for splitting large type definitions across logical files.

### Q4: What is declaration merging with namespaces?

**Answer**: When multiple namespace declarations exist with the same name, TypeScript merges their members. This works for interfaces (members are combined), classes (static members added), functions (overload signatures added), and enums (members combined). This is the primary reason to use namespaces.

### Q5: What is an ambient namespace?

**Answer**: An ambient namespace (in a `.d.ts` file using `declare namespace`) describes the shape of JavaScript code that exists at runtime but has no TypeScript types. It's used to provide type definitions for libraries written in plain JavaScript.

### Q6: Why did TypeScript introduce modules to replace namespaces?

**Answer**: Namespaces don't integrate with the standard JavaScript module systems (AMD, CommonJS, ESM), don't support tree-shaking, require manual dependency management (triple-slash references, concatenation), and can't leverage bundler optimizations. Modules are the JavaScript standard and provide static analysis capabilities.

### Q7: What do namespaces compile to in JavaScript?

**Answer**: IIFEs (Immediately Invoked Function Expressions) that create an object. The namespace name becomes a variable, and the IIFE populates it with exported members. Non-exported members remain in the IIFE's closure scope.

### Q8: Can you merge a namespace with a class?

**Answer**: Yes. When a namespace and a class have the same name in the same file, the namespace's exported members become static members of the class. This is useful for adding factory methods or utility functions related to a class.
