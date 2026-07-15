# TypeScript Compiler & Advanced Interview Questions

## 20+ Questions and Answers

---

### Q1: What is the TypeScript Compiler API and when would you use it?

**Answer**: The Compiler API provides programmatic access to TypeScript's compilation, type checking, and AST manipulation. Use it for:

- Custom build tools and bundlers
- Code generators and scaffolding tools
- Linters and static analysis tools
- IDE plugins and language extensions
- AST-based refactoring tools
- Type-level testing frameworks

```typescript
import * as ts from 'typescript';

const program = ts.createProgram(['src/index.ts'], {
  strict: true,
  target: ts.ScriptTarget.ES2020,
});

const diagnostics = ts.getPreEmitDiagnostics(program);
console.log(`Found ${diagnostics.length} errors`);
```

---

### Q2: What is the difference between `Program`, `CompilerHost`, and `TypeChecker`?

**Answer**:

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| `Program` | Represents a compilation | `getSourceFiles()`, `getTypeChecker()`, `emit()` |
| `CompilerHost` | File system abstraction | `getSourceFile()`, `writeFile()`, `fileExists()` |
| `TypeChecker` | Type analysis | `getTypeOfSymbol()`, `typeToString()`, `getDiagnostics()` |

```typescript
const program = ts.createProgram(fileNames, options);
const checker = program.getTypeChecker();
const host = ts.createCompilerHost(options);
```

---

### Q3: How do you traverse an AST in TypeScript?

**Answer**: Use `ts.forEachChild()` for depth-first traversal and `ts.visitNode()` for transformations.

```typescript
function visit(node: ts.Node) {
  if (ts.isFunctionDeclaration(node)) {
    console.log(`Function: ${node.name?.text}`);
  }
  ts.forEachChild(node, visit);
}

visit(sourceFile);
```

For transformations:

```typescript
function transform(node: ts.Node): ts.Node {
  return ts.visitNode(node, (child) => {
    if (ts.isIdentifier(child) && child.text === 'oldName') {
      return ts.factory.createIdentifier('newName');
    }
    return ts.visitEachChild(child, transform, context);
  });
}
```

---

### Q4: What are transformers and how do they work?

**Answer**: Transformers modify the AST during compilation. They receive the AST, make modifications, and return the transformed AST.

```typescript
function myTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile) => {
    function visit(node: ts.Node): ts.Node {
      if (ts.isStringLiteral(node)) {
        return ts.factory.createStringLiteral('transformed');
      }
      return ts.visitEachChild(node, visit, context);
    }
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}
```

---

### Q5: What is the difference between `tsc` and `tsc --build`?

**Answer**:

```bash
# tsc: Single project compilation
tsc                      # Compile all files
tsc --watch              # Watch mode
tsc --noEmit             # Type check only

# tsc --build: Multi-project compilation
tsc --build              # Build all referenced projects
tsc --build --watch      # Watch mode for all projects
tsc --build --clean      # Clean build outputs
tsc --build --force      # Force full rebuild
```

---

### Q6: How do project references improve build performance?

**Answer**: Project references split a monorepo into sub-projects that compile independently. Only changed projects are recompiled.

```json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/app" }
  ]
}
```

Benefits:
- Parallel compilation
- Incremental builds per project
- Dependency tracking between projects
- Reduced compile times in large codebases

---

### Q7: What is `isolatedModules` and why does it matter for transpilers?

**Answer**: `isolatedModules` ensures each file can be independently transpiled, which is required by Babel, esbuild, and SWC.

```typescript
// ❌ Error with isolatedModules
const enum Direction { Up, Down } // Can't be inlined without full compilation
export { User } from './types';    // Can't re-export types without 'type'

// ✅ Works with isolatedModules
enum Direction { Up, Down }
export type { User } from './types';
```

---

### Q8: What is the difference between `module: CommonJS` and `module: ESNext`?

**Answer**:

```typescript
// module: CommonJS
const { add } = require('./math');
module.exports = { result };

// module: ESNext
import { add } from './math';
export const result = add(1, 2);
```

ESNext is tree-shakeable. CommonJS is not. Use ESNext for bundlers, CommonJS for Node.js (legacy).

---

### Q9: How do you create a TypeScript compiler plugin?

**Answer**:

```typescript
// ts-plugin.ts
function init(modules: { typescript: typeof ts }) {
  const ts = modules.typescript;

  function create(info: ts.server.PluginCreateInfo) {
    return {
      ...info.languageService,
      getSemanticDiagnostics(fileName) {
        const prior = info.languageService.getSemanticDiagnostics(fileName);
        // Add custom diagnostics
        return prior;
      },
    };
  }

  return { create };
}

export = init;
```

---

### Q10: What are diagnostics and how do you interpret them?

**Answer**: Diagnostics are compiler errors and warnings.

```typescript
const diagnostics = ts.getPreEmitDiagnostics(program);

diagnostics.forEach(diagnostic => {
  if (diagnostic.file) {
    const { line, character } = ts.getLineAndCharacterOfPosition(
      diagnostic.file,
      diagnostic.start!
    );
    const message = ts.flattenDiagnosticMessageText(
      diagnostic.messageText, '\n'
    );
    console.log(`${diagnostic.file.fileName}(${line + 1},${character + 1}): ${message}`);
  }
});
```

---

### Q11: What is `composite: true` and when should you use it?

**Answer**: `composite: true` enables a project to be referenced by other projects. It implies `declaration: true` and `incremental: true`.

```json
{
  "compilerOptions": {
    "composite": true
  }
}
```

Use it when building a monorepo or multi-package project.

---

### Q12: How do you handle `any` types in a large codebase?

**Answer**:

```json
// Enable strict mode
{ "strict": true }

// Additional checks
{
  "noImplicitAny": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noFallthroughCasesInSwitch": true
}

// Gradual migration
// Step 1: Enable noImplicitAny
// Step 2: Fix errors one by one
// Step 3: Enable strictNullChecks
// Step 4: Enable full strict mode
```

---

### Q13: What is the difference between `skipLibCheck` and `skipDefaultLibCheck`?

**Answer**:

```json
// skipLibCheck: Skip checking all .d.ts files
{ "skipLibCheck": true }

// skipDefaultLibCheck: Skip checking default lib files only
// (lib.d.ts, dom.d.ts, etc.)
// Almost never used
```

`skipLibCheck: true` speeds up compilation by not type-checking declaration files.

---

### Q14: How do you use the Compiler API to generate code?

**Answer**:

```typescript
import * as ts from 'typescript';

// Create AST nodes
const factory = ts.factory;

const func = factory.createFunctionDeclaration(
  undefined,
  undefined,
  'add',
  undefined,
  [
    factory.createParameterDeclaration(undefined, undefined, 'a', undefined,
      factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword), undefined),
    factory.createParameterDeclaration(undefined, undefined, 'b', undefined,
      factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword), undefined),
  ],
  factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword),
  factory.createBlock([
    factory.createReturnStatement(
      factory.createBinaryExpression(
        factory.createIdentifier('a'),
        ts.SyntaxKind.PlusToken,
        factory.createIdentifier('b')
      )
    ),
  ])
);

// Print to string
const printer = ts.createPrinter();
const result = printer.printNode(
  ts.EmitHint.Unspecified,
  func,
  ts.createSourceFile('output.ts', '', ts.ScriptTarget.Latest)
);
console.log(result);
// Output: function add(a, b) { return a + b; }
```

---

### Q15: What is the difference between `declaration` and `declarationMap`?

**Answer**:

```json
// declaration: Generate .d.ts files
{ "declaration": true }

// declarationMap: Generate .d.ts.map files (map .d.ts to source)
{ "declarationMap": true }
```

`declarationMap` enables "Go to Definition" to jump to original TypeScript source instead of the generated declaration file.

---

### Q16: How do you handle circular dependencies in TypeScript?

**Answer**:

```typescript
// Problem: A imports B, B imports A

// Solution 1: Extract shared types
// types.ts (no imports)
export interface Shared { /* ... */ }

// A.ts
import { Shared } from './types';

// B.ts
import { Shared } from './types';

// Solution 2: Use dependency injection
// A.ts
export function createA(b: B) { /* ... */ }

// B.ts
export function createB() { /* ... */ }

// Solution 3: Dynamic imports
const module = await import('./module');
```

---

### Q17: What are the performance implications of `strict` mode?

**Answer**: `strict` mode adds compile-time checking but doesn't affect runtime performance. It:

1. Slightly increases compile time (more type checking)
2. Requires more null checks in code
3. Catches bugs that would cause runtime errors
4. Results in more reliable code

The compile-time cost is negligible compared to bug prevention benefits.

---

### Q18: How do you optimize TypeScript compilation for CI/CD?

**Answer**:

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./tsconfig.tsbuildinfo",
    "skipLibCheck": true,
    "sourceMap": false,
    "declaration": false
  }
}
```

Additional optimizations:
- Cache `.tsbuildinfo` between CI runs
- Use `tsc --build` for monorepos
- Consider esbuild/SWC for faster transpilation
- Parallelize builds

---

### Q19: What is `downlevelIteration` and when should you use it?

**Answer**:

```typescript
// downlevelIteration: true
// Enables full iteration support for ES5/ES3 targets

// Without downlevelIteration:
for (const item of items) { /* ... */ }
// Error: Iterable type not found

// With downlevelIteration:
for (const item of items) { /* ... */ }
// Compiles to generator-based iteration

// Use when targeting ES5/ES3 and using:
// - for...of loops
// - Spread operator (...iterable)
// - Destructuring from iterables
```

---

### Q20: How do you create custom type guards with the Compiler API?

**Answer**:

```typescript
import * as ts from 'typescript';

function createTypeGuardTransformer(
  typeGuardName: string
): ts.TransformerFactory<ts.SourceFile> {
  return (context) => {
    return (sourceFile) => {
      function visit(node: ts.Node): ts.Node {
        if (ts.isIfStatement(node)) {
          // Transform: if (isString(value)) → if (typeof value === 'string')
          const expression = node.expression;
          if (ts.isCallExpression(expression) &&
              ts.isIdentifier(expression.expression) &&
              expression.expression.text === typeGuardName) {
            
            const arg = expression.arguments[0];
            const typeCheck = ts.factory.createBinaryExpression(
              ts.factory.createTypeOfExpression(arg),
              ts.SyntaxKind.EqualsEqualsEqualsToken,
              ts.factory.createStringLiteral('string')
            );
            
            return ts.factory.createIfStatement(
              typeCheck,
              node.thenStatement,
              node.elseStatement
            );
          }
        }
        return ts.visitEachChild(node, visit, context);
      }
      return ts.visitNode(sourceFile, visit) as ts.SourceFile;
    };
  };
}
```

---

### Q21: What is `moduleResolution` and what are the differences between options?

**Answer**:

| Option | Resolution Strategy | Use Case |
|--------|-------------------|----------|
| `Node` | Classic Node.js | Most projects |
| `Node16` | Node.js ESM/CJS | Node.js 16+ |
| `NodeNext` | Node.js latest | Node.js latest |
| `Bundler` | Webpack/esbuild-like | Bundler projects |
| `Classic` | TypeScript legacy | Rarely used |

```json
// Most common
{ "moduleResolution": "Node" }

// For Node.js with ESM
{ "moduleResolution": "NodeNext" }

// For bundler projects
{ "moduleResolution": "Bundler" }
```

---

### Q22: How do you handle path aliases in TypeScript?

**Answer**:

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@utils/*": ["./src/utils/*"],
      "@models/*": ["./src/models/*"]
    }
  }
}
```

```typescript
// Usage
import { add } from '@utils/math';
import { User } from '@models/user';
```

For bundlers, also configure path aliases in webpack/vite/rollup config.

---

### Q23: What is the difference between `type` and `interface` in TypeScript?

**Answer**:

```typescript
// Interface: extensible, declaration merging
interface User {
  name: string;
}
interface User {
  age: number; // Merges with previous declaration
}
// User = { name: string; age: number }

// Type: more powerful, no declaration merging
type User = {
  name: string;
};
// Can't declare another type User (error)

// Interface: extends other interfaces
interface Admin extends User {
  role: string;
}

// Type: intersection, unions, primitives
type ID = string | number;
type Admin = User & { role: string };
type Result<T> = { data: T } | { error: string };
```

Use interfaces for object shapes and public APIs. Use types for unions, intersections, and complex type manipulation.

---

### Q24: How do you test TypeScript types at compile time?

**Answer**:

```typescript
// Using tsd
import { expectType, expectError } from 'tsd';
import { add } from './math';

expectType<number>(add(1, 2));
expectError(add('a', 'b'));

// Using conditional types
type AssertEqual<T, U> = T extends U ? U extends T ? true : never : never;
type Test = AssertEqual<string, string>; // true

// Using @ts-expect-error
// @ts-expect-error — should not compile
const error = add('a', 'b');

// Using type-level assertions
type IsString<T> = T extends string ? true : false;
type Test1 = IsString<string>; // true
type Test2 = IsString<number>; // false
```

---

### Q25: What is `verbatimModuleSyntax` and when should you use it?

**Answer**:

```typescript
// verbatimModuleSyntax: true
// Ensures imports/exports match the output module system

// Error: Named import of type without 'type' keyword
import { User } from './types'; // Error if User is only a type
import type { User } from './types'; // OK

// Use it when:
// - You want strict module syntax
// - Building for ESM
// - Using isolatedModules
// - Preventing accidental runtime imports of types
```
