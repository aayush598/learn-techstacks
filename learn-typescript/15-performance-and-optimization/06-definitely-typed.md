# DefinitelyTyped and @types Packages

## Table of Contents

1. [What is DefinitelyTyped](#1-what-is-definitelytyped)
2. [@types Packages](#2-types-packages)
3. [Installing Type Declarations](#3-installing-type-declarations)
4. [Contributing to DefinitelyTyped](#4-contributing-to-definitelytyped)
5. [Testing Type Declarations](#5-testing-type-declarations)
6. [Finding Correct Types](#6-finding-correct-types)
7. [Versioning of Type Declarations](#7-versioning-of-type-declarations)
8. [Fallback Types](#8-fallback-types)
9. [Best Practices](#9-best-practices)

---

## 1. What is DefinitelyTyped

DefinitelyTyped (DT) is the largest repository of TypeScript type declarations for JavaScript libraries. It hosts over 10,000 `@types` packages.

```
Repository: github.com/DefinitelyTyped/DefinitelyTyped
Website:    definitelytyped.org
npm scope:  @types/*

Structure:
DefinitelyTyped/
  types/
    express/          → @types/express
      index.d.ts
      express-tests.ts
      tsconfig.json
      tslint.json
    react/            → @types/react
      index.d.ts
      ...
    node/             → @types/node
      index.d.ts
      ...
```

### How It Works

```
npm install --save-dev @types/express

1. npm downloads @types/express from registry
2. TypeScript finds types in node_modules/@types/express/index.d.ts
3. Types are automatically available when importing 'express'
4. No need for triple-slash directives or configuration
```

---

## 2. @types Packages

### Package Structure

```bash
@types/
  package-name/
    index.d.ts        # Main type declarations
    package-name.d.ts  # Alternative naming
    tsconfig.json      # TypeScript config for this package
    tslint.json        # Linting rules for this package
    README.md          # Documentation
```

### Example: @types/express

```typescript
// node_modules/@types/express/index.d.ts (simplified)
import * as http from 'http';
import * as qs from 'qs';

declare namespace express {
  interface Request {
    body: any;
    params: Record<string, string>;
    query: qs.ParsedQs;
    headers: http.IncomingHttpHeaders;
    get(name: string): string | undefined;
  }

  interface Response {
    status(code: number): Response;
    json(data: any): Response;
    send(data: any): Response;
    redirect(url: string): void;
    setHeader(name: string, value: string): void;
  }

  interface NextFunction {
    (err?: any): void;
  }

  interface Application {
    get(path: string, handler: RequestHandler): this;
    post(path: string, handler: RequestHandler): this;
    use(handler: RequestHandler): this;
    listen(port: number, callback?: () => void): http.Server;
  }

  interface RequestHandler {
    (req: Request, res: Response, next: NextFunction): void;
  }

  function express(): Application;
}

export = express;
```

### How TypeScript Finds @types

```json
// tsconfig.json
{
  "compilerOptions": {
    "typeRoots": ["./node_modules/@types"],
    // ↑ Default location for @types packages
    
    "types": ["node", "jest", "react"],
    // ↑ Only include these specific @types packages
    // Others in node_modules/@types are ignored
  }
}
```

---

## 3. Installing Type Declarations

### Automatic Installation

```bash
# Install the library and its types (if available)
npm install express
npm install --save-dev @types/express

# Types are automatically found by TypeScript
```

### When Types Don't Exist

```bash
# Check if @types exist
npm search @types/my-library

# If not found, options:
# 1. Create your own declaration file
# 2. Use @ts-ignore
# 3. Use declare module

# Create types/my-library.d.ts
declare module 'my-library' {
  export function doSomething(value: string): number;
  export interface Config {
    debug: boolean;
  }
}
```

### Bundled Types

```bash
# Some libraries ship their own types
# No need for @types package

# Examples:
npm install lodash         # Has built-in types
npm install typescript     # Has built-in types
npm install zod            # Has built-in types
npm install axios          # Has built-in types

# Check if a library has built-in types:
ls node_modules/axios/index.d.ts
# If this file exists, no @types needed
```

---

## 4. Contributing to DefinitelyTyped

### Getting Started

```bash
# Fork the repository
git clone https://github.com/YourUsername/DefinitelyTyped.git
cd DefinitelyTyped

# Install dependencies
npm install

# Create a new package
npx dtslint --install-all

# Or manually create types/my-package/
mkdir types/my-package
```

### Creating Type Declarations

```typescript
// types/my-package/index.d.ts

// Type definitions for my-package 1.0
// Project: https://github.com/user/my-package
// Definitions by: Your Name <https://github.com/yourname>

import { EventEmitter } from 'events';

declare namespace MyPackage {
  interface Options {
    timeout?: number;
    retries?: number;
    debug?: boolean;
  }

  interface Result<T> {
    success: boolean;
    data?: T;
    error?: string;
  }

  class Client extends EventEmitter {
    constructor(options?: Options);
    connect(): Promise<void>;
    disconnect(): Promise<void>;
    send<T>(data: unknown): Promise<Result<T>>;
    on(event: 'connected', listener: () => void): this;
    on(event: 'error', listener: (err: Error) => void): this;
  }
}

declare function MyPackage(options?: MyPackage.Options): MyPackage.Client;

export = MyPackage;
```

### Testing Your Types

```typescript
// types/my-package/my-package-tests.ts

import MyPackage = require('my-package');

// Test: constructor
const client = MyPackage({ timeout: 5000 });

// Test: connect
async function test() {
  await client.connect();
  
  // Test: send
  const result = await client.send<{ id: number }>({ name: 'test' });
  
  if (result.success) {
    console.log(result.data?.id); // Should be number | undefined
  }
  
  // Test: events
  client.on('connected', () => {
    console.log('Connected!');
  });
  
  client.on('error', (err) => {
    console.error(err.message);
  });
}

// Compile check — these should error:
client.send(123); // Error: not assignable
client.on('unknown', () => {}); // Error: unknown event
```

### Submitting to DefinitelyTyped

```bash
# 1. Create your types
# 2. Test with dtslint
npx dtslint types/my-package

# 3. Run the full test suite
npm test my-package

# 4. Submit PR
git add types/my-package/
git commit -m "Add types for my-package"
git push origin main

# 5. Wait for CI and review
# Automated checks ensure:
# - Types compile correctly
# - Tests pass
# - No conflicts with existing types
```

---

## 5. Testing Type Declarations

### dtslint

```bash
# Install dtslint
npm install -g dtslint

# Run dtslint on your types
dtslint types/my-package

# dtslint checks:
# - TypeScript compilation
# - No explicit any (unless allowed)
# - Consistent formatting
# - Proper exports
```

### Type Test Files

```typescript
// types/my-package/my-package-tests.ts

// Use $ExpectType to verify type inference
const result = someFunction();
// $ExpectType string

// Use $ExpectError to verify errors
const error = someFunction(123);
// $ExpectError — should not compile

// Use $ExpectType for complex types
const data = getData();
// $ExpectType { id: number; name: string }
```

### tsd

```bash
# Alternative to dtslint — tsd
npm install --save-dev tsd

# In package.json
{
  "tsd": {
    "directory": "test-d"
  }
}
```

```typescript
// test-d/index.test-d.ts
import { expectType, expectError } from 'tsd';
import myPackage from '../';

const result = myPackage({ timeout: 1000 });

expectType<Promise<void>>(result.connect());
expectError(myPackage({ invalid: true }));
```

### Manual Testing

```typescript
// Create a test file and check compilation
// test/types-test.ts

import { add, Config } from '../src';

// Verify types compile correctly
const sum: number = add(1, 2);
const config: Config = { debug: true };

// Verify errors are caught
// @ts-expect-error — should error
const error = add('a', 'b');

// If TypeScript compiles without errors, types are correct
```

---

## 6. Finding Correct Types

### Search for Types

```bash
# Search npm for @types
npm search @types/express

# Check specific package
npm info @types/express

# Visit DefinitelyTyped
# https://definitelytyped.org
# Search: https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types
```

### Verify Quality

```bash
# Check download count
npm info @types/express --json | grep "downloads"

# Check last publish date
npm info @types/express --json | grep "time"

# Check TypeScript version compatibility
npm info @types/express --json | grep "peerDependencies"

# Check for issues
# Visit: https://github.com/DefinitelyTyped/DefinitelyTyped/issues
```

### When Types Don't Match

```bash
# Problem: @types/express@4.x but using express@4.18
# Solution: Pin the @types version
npm install --save-dev @types/express@4.17.13

# Problem: Library ships its own types but they're wrong
# Solution: Override with custom declarations
// types/express/index.d.ts
declare module 'express' {
  // Your corrected types
}
```

---

## 7. Versioning of Type Declarations

```bash
# @types version matches the library version
@types/express@4.17.13  →  express@4.17.13
@types/node@18.0.0      →  node@18.0.0

# Check compatibility
npm info @types/express --json | grep "version"
npm info express --json | grep "version"

# If versions don't match, types may be outdated
# Pin versions in package.json:
{
  "devDependencies": {
    "@types/express": "4.17.13",
    "express": "4.17.13"
  }
}
```

### Version Ranges

```json
{
  "devDependencies": {
    "@types/express": "^4.17.13",
    // ↑ Allows minor/patch updates
    // Could break if library changes
    
    "@types/node": "~18.0.0",
    // ↑ Only allows patch updates
    // Safer for production
  }
}
```

---

## 8. Fallback Types

### When No @types Package Exists

```typescript
// Option 1: Create your own declaration
// types/my-library.d.ts
declare module 'my-library' {
  export function doSomething(value: string): number;
  export interface Config {
    debug: boolean;
  }
}

// Option 2: Use declare module with minimal types
// types/my-library.d.ts
declare module 'my-library' {
  const value: any;
  export default value;
}

// Option 3: Use @ts-ignore
// @ts-ignore — No types available
import myLibrary from 'my-library';
```

### Bundled Types Fallback

```typescript
// Some libraries have types bundled
// Check if the library has .d.ts files:
ls node_modules/my-library/*.d.ts

// If yes, no @types needed
// If no, create your own or install @types
```

---

## 9. Best Practices

```bash
# 1. Always install @types for libraries without bundled types
npm install --save-dev @types/express @types/jest

# 2. Pin @types versions for production
npm install --save-dev @types/express@4.17.13

# 3. Check for bundled types first
ls node_modules/my-library/*.d.ts
# If exists, don't install @types

# 4. Create custom declarations for untyped libraries
// types/my-library.d.ts
declare module 'my-library' {
  // Your type declarations
}

# 5. Use tsconfig.json types to control @types inclusion
{
  "compilerOptions": {
    "types": ["node", "jest"],
    // Only these @types packages are included
  }
}

# 6. Test your types with dtslint or tsd
npx dtslint types/my-package

# 7. Contribute to DefinitelyTyped when you create custom types
# This helps the community

# 8. Keep @types up to date
npm outdated @types/*
```

---

## Interview Questions

**Q1**: What is DefinitelyTyped and why does it exist?
**A**: DefinitelyTyped is the largest repository of TypeScript type declarations for JavaScript libraries. It exists because many JavaScript libraries don't ship their own type declarations, so the community maintains types separately.

**Q2**: How do you install type declarations for a library?
**A**: Run `npm install --save-dev @types/library-name`. TypeScript automatically finds types in `node_modules/@types/`. If no @types package exists, create your own declaration file.

**Q3**: When should you create your own types vs using @types?
**A**: Use @types when available and well-maintained. Create your own types when: no @types package exists, the @types package is outdated, or you need more specific types for your use case.

**Q4**: How do @types packages version with their corresponding libraries?
**A**: @types version matches the library version (e.g., @types/express@4.17.13 for express@4.17.13). Pin versions in package.json to avoid compatibility issues.

**Q5**: What is the difference between bundled types and @types packages?
**A**: Bundled types are `.d.ts` files included with the library itself. @types packages are separate npm packages maintained by DefinitelyTyped. Bundled types are preferred when available.
