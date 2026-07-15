# 03 - First Program

## Table of Contents

- [Hello World in TypeScript](#hello-world-in-typescript)
- [Compiling and Running](#compiling-and-running)
- [Understanding the Output JavaScript](#understanding-the-output-javascript)
- [Source Maps](#source-maps)
- [Strict Mode Introduction](#strict-mode-introduction)
- [Your First TypeScript Function](#your-first-typescript-function)
- [Type Annotations on Your First Program](#type-annotations-on-your-first-program)
- [Putting It All Together](#putting-it-all-together)
- [Summary](#summary)

---

## Hello World in TypeScript

Let's write the classic first program in TypeScript.

### The File

Create a file called `index.ts` inside the `src/` directory:

```typescript
// src/index.ts
const greeting: string = "Hello, World!";
console.log(greeting);
```

### Breaking It Down

Let's examine every element of this simple program:

```typescript
// 'const' declares a block-scoped constant
// 'greeting' is the variable name
// ': string' is the type annotation — tells TypeScript this is a string
// '=' assigns the value
// '"Hello, World!"' is the value (a string literal)
const greeting: string = "Hello, World!";

// 'console.log()' outputs to the terminal
// This is standard JavaScript — no TypeScript-specific syntax
console.log(greeting);
```

### Without Type Annotation

Notice that TypeScript can **infer** the type automatically:

```typescript
// With explicit type annotation
const greeting: string = "Hello, World!";

// With type inference (TypeScript figures out it's a string)
const greeting = "Hello, World!";

// Both are identical to the TypeScript compiler
```

> **Key Insight:** For simple variable declarations with immediate initialization, type annotations are often optional because TypeScript infers the type from the assigned value.

---

## Compiling and Running

### Step 1: Compile

```bash
npx tsc src/index.ts
```

This produces `src/index.js` (or `dist/index.js` depending on your tsconfig).

### Step 2: Run

```bash
node src/index.js
# or
node dist/index.js
```

Output:

```
Hello, World!
```

### The Full Workflow

```
┌──────────────────┐
│  src/index.ts     │  ← You write this
│  const greeting:  │
│  string = "Hello" │
└────────┬─────────┘
         │  npx tsc
         ▼
┌──────────────────┐
│  dist/index.js    │  ← Compiler generates this
│  const greeting = │
│  "Hello"          │
└────────┬─────────┘
         │  node dist/index.js
         ▼
┌──────────────────┐
│  Hello, World!    │  ← Output in terminal
└──────────────────┘
```

### Using npm Scripts

If you set up your `package.json`:

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

Then:

```bash
npm run build     # Compiles TypeScript
npm start         # Runs the output
```

---

## Understanding the Output JavaScript

Let's look at how TypeScript compiles to JavaScript for different targets.

### ES2020 Target (Modern)

**TypeScript input:**

```typescript
const greeting: string = "Hello, World!";
console.log(greeting);
```

**JavaScript output** (with `"target": "ES2020"`):

```javascript
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const greeting = "Hello, World!";
console.log(greeting);
```

### ES5 Target (Legacy)

**JavaScript output** (with `"target": "ES5"`):

```javascript
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var greeting = "Hello, World!";
console.log(greeting);
```

### What Changed Between Input and Output

| TypeScript Input | JavaScript Output |
|-----------------|-------------------|
| `const greeting: string` | `const greeting` (type removed) |
| `: string` annotation | Completely removed |
| `console.log(greeting)` | `console.log(greeting)` (unchanged) |

The type annotation `: string` is **completely stripped** — it has zero runtime cost.

---

## Source Maps

Source maps create a mapping between the compiled JavaScript and the original TypeScript source code. This is essential for debugging.

### Generating Source Maps

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "sourceMap": true
  }
}
```

Or via command line:

```bash
npx tsc --sourceMap
```

### What Gets Generated

After compilation:

```
dist/
├── index.js
├── index.js.map    ← Source map file
└── index.d.ts      ← Declaration file (if declaration is enabled)
```

### Source Map Format

The `.map` file is a JSON file that maps positions in the JavaScript output to positions in the TypeScript source:

```json
{
  "version": 3,
  "file": "index.js",
  "sourceRoot": "",
  "sources": ["../src/index.ts"],
  "names": [],
  "mappings": "..."
}
```

### Debugging with Source Maps

With source maps enabled, you can debug TypeScript directly in VS Code:

1. Create a `launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug TypeScript",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "sourceMaps": true
    }
  ]
}
```

2. Set breakpoints in your `.ts` files
3. Press F5 to start debugging
4. The debugger hits breakpoints in the TypeScript source, not the compiled JavaScript

> **Best Practice:** Always enable source maps in development. You can disable them in production for smaller file sizes.

---

## Strict Mode Introduction

TypeScript's strict mode is the most important configuration you'll use. It enables a collection of type-checking options that catch the most common bugs.

### Enabling Strict Mode

In `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### What Strict Mode Catches

Let's see examples of bugs that strict mode catches:

#### 1. Implicit Any (noImplicitAny)

```typescript
// Without strict mode — this compiles fine (implicit any)
function add(a, b) {
  return a + b;
}

add("hello", 42); // No error — runs silently, produces "hello42"

// With strict mode — ERROR: Parameter 'a' implicitly has an 'any' type
function add(a, b) {
  return a + b;
}
```

#### 2. Strict Null Checks

```typescript
// Without strict mode — this compiles fine
const user = null;
const name = user.name; // No error at compile time — crashes at runtime!

// With strict mode — ERROR: 'user' is possibly 'null'
const user = null;
const name = user.name; // Compile-time error
```

#### 3. No Implicit This

```typescript
// Without strict mode — 'this' is implicitly 'any'
function logName() {
  console.log(this.name); // No error
}

// With strict mode — ERROR: 'this' implicitly has type 'any'
```

#### 4. Strict Function Types

```typescript
// Without strict mode — function parameter bivariance is allowed
type Handler = (event: MouseEvent) => void;
const handler: Handler = (event: KeyboardEvent) => {}; // No error

// With strict mode — ERROR: Type mismatch detected
```

### Strict Mode Checklist

| Option | What It Does |
|--------|-------------|
| `noImplicitAny` | Error when TypeScript can't infer a type |
| `strictNullChecks` | `null` and `undefined` are separate types |
| `strictFunctionTypes` | Strict checking of function parameter types |
| `strictBindCallApply` | Strict checking of `bind`, `call`, and `apply` |
| `strictPropertyInitialization` | Class properties must be initialized |
| `noImplicitThis` | Error when `this` has implicit `any` type |
| `alwaysStrict` | Emit `"use strict"` in every file |
| `useUnknownInCatchVariables` | Catch variables typed as `unknown` instead of `any` |

> **Best Practice:** Always start new projects with `"strict": true`. It's easier to enable it from the beginning than to retrofit it later.

---

## Your First TypeScript Function

Let's write a more complete program with functions.

### A Simple Function

```typescript
// src/index.ts

// Function with type annotations on parameters and return type
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Calling the function
const message: string = greet("TypeScript");
console.log(message); // Output: Hello, TypeScript!
```

### Breaking Down the Function

```typescript
//       ↓ function keyword (same as JavaScript)
//       ↓         ↓ function name
//       ↓         ↓      ↓ parameter with type annotation
//       ↓         ↓      ↓             ↓ return type annotation
function greet(name: string): string {
//  ↑                    ↑        ↑
//  opening brace       colon    return type
  
  return `Hello, ${name}!`;
  // ↑ return type is string (matches the annotation)
}

// Calling the function
const message = greet("TypeScript");
//            ↑ return value is string (matches the annotation)
```

### Arrow Function Version

```typescript
// Arrow function with type annotations
const greet = (name: string): string => {
  return `Hello, ${name}!`;
};

// Concise body (implicit return)
const greet = (name: string): string => `Hello, ${name}!`;

// With type inference (TypeScript infers return type)
const greet = (name: string) => `Hello, ${name}!`;
```

### Multiple Parameters

```typescript
function createFullName(firstName: string, lastName: string): string {
  return `${firstName} ${lastName}`;
}

const fullName = createFullName("Anders", "Hejlsberg");
console.log(fullName); // Output: Anders Hejlsberg
```

### Default Parameters

```typescript
function greet(name: string, greeting: string = "Hello"): string {
  return `${greeting}, ${name}!`;
}

greet("Alice");            // "Hello, Alice!"
greet("Alice", "Hi");     // "Hi, Alice!"
```

### Optional Parameters

```typescript
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}!`;
}

greet("Alice");            // "Hello, Alice!"
greet("Alice", "Hi");     // "Hi, Alice!"
```

---

## Type Annotations on Your First Program

Let's expand our Hello World program to demonstrate various type annotations.

### Variables

```typescript
// String
const name: string = "TypeScript";

// Number (no distinction between int and float)
const version: number = 5.4;

// Boolean
const isAwesome: boolean = true;

// Array of strings
const features: string[] = ["Types", "Interfaces", "Generics"];

// Tuple
const coordinates: [number, number] = [10, 20];

// Object literal type
const config: { apiUrl: string; timeout: number } = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};
```

### Type Inference vs Explicit Annotation

```typescript
// TypeScript infers 'string'
const name = "TypeScript"; // type: string

// Explicit annotation (redundant here)
const name: string = "TypeScript"; // type: string

// Type inference is usually sufficient for simple declarations
// Use explicit annotations when:
// 1. The type is not obvious
// 2. You want to ensure a specific type
// 3. The variable is initialized later
```

### When to Use Explicit Annotations

```typescript
// GOOD: Annotation not needed (inferred from value)
const count = 42;
const message = "hello";
const isActive = true;

// GOOD: Annotation helps clarity
interface User {
  name: string;
  age: number;
}

const user: User = { name: "Alice", age: 30 };

// GOOD: Annotation prevents wider type
let result: string | null = null;
result = "success";

// BAD: Unnecessary annotation on simple variable
const x: number = 42; // Redundant — TypeScript knows it's a number
```

### Function with All Type Annotations

```typescript
function processUser(
  name: string,
  age: number,
  isActive: boolean
): { name: string; age: number; status: string } {
  return {
    name,
    age,
    status: isActive ? "active" : "inactive",
  };
}

const user = processUser("Alice", 30, true);
// TypeScript knows the exact shape of 'user':
// { name: string; age: number; status: string }

console.log(user.name);   // "Alice"
console.log(user.status); // "active"
```

---

## Putting It All Together

Here's a complete first program that uses everything we've learned:

```typescript
// src/index.ts

// ==========================================
// Type Annotations
// ==========================================

const appName: string = "My First TypeScript App";
const appVersion: string = "1.0.0";
const isDebug: boolean = true;

// ==========================================
// Interface (preview of future topics)
// ==========================================

interface Greeting {
  message: string;
  timestamp: Date;
}

// ==========================================
// Functions
// ==========================================

function createGreeting(name: string, language: string = "en"): Greeting {
  const greetings: Record<string, string> = {
    en: "Hello",
    es: "Hola",
    fr: "Bonjour",
    de: "Hallo",
  };

  const greeting = greetings[language] ?? "Hello";

  return {
    message: `${greeting}, ${name}!`,
    timestamp: new Date(),
  };
}

// ==========================================
// Main Program
// ==========================================

function main(): void {
  console.log(`=== ${appName} v${appVersion} ===`);
  console.log(`Debug mode: ${isDebug}`);
  console.log();

  const enGreeting = createGreeting("TypeScript");
  const esGreeting = createGreeting("TypeScript", "es");
  const frGreeting = createGreeting("TypeScript", "fr");

  console.log(enGreeting.message); // "Hello, TypeScript!"
  console.log(esGreeting.message); // "Hola, TypeScript!"
  console.log(frGreeting.message); // "Bonjour, TypeScript!"
  console.log();

  console.log(`Generated at: ${enGreeting.timestamp.toISOString()}`);
}

main();
```

### Compiling and Running

```bash
npx tsc src/index.ts
node src/index.js
```

Output:

```
=== My First TypeScript App v1.0.0 ===
Debug mode: true

Hello, TypeScript!
Hola, TypeScript!
Bonjour, TypeScript!

Generated at: 2024-01-15T12:00:00.000Z
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| **File extension** | `.ts` for TypeScript files |
| **Type annotations** | Added with `: type` syntax |
| **Compilation** | `npx tsc filename.ts` |
| **Running** | `node filename.js` (compiled output) |
| **Source maps** | Enable for debugging `.ts` files |
| **Strict mode** | Always use `"strict": true` |
| **Type inference** | TypeScript can often infer types automatically |
| **Functions** | Annotate parameters and return types |

> **Next Step:** Now that you can write and run TypeScript, let's explore the [primitive types](04-primitive-types.md) in detail.
