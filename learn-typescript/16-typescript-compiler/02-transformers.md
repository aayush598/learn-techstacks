# TypeScript Transformers

## Table of Contents

1. [What Are Transformers](#1-what-are-transformers)
2. [Compiler Transformer API](#2-compiler-transformer-api)
3. [Custom Transformers](#3-custom-transformers)
4. [AST Transformation](#4-ast-transformation)
5. [Before/After Transformers](#5-beforeafter-transformers)
6. [Transformer Factories](#6-transformer-factories)
7. [Practical Transformer Examples](#7-practical-transformer-examples)

---

## 1. What Are Transformers

Transformers modify the Abstract Syntax Tree (AST) during TypeScript compilation. They run between parsing and code generation.

```
Source Code → Parser → AST → Type Checker → Transformers → Printer → Output
                                        ↑                 ↑
                                   Type errors        Code modifications
```

### Types of Transformers

```typescript
// 1. Built-in transformers (run automatically)
// - ES3/ES5 downleveling (async/await → generator)
// - Module transformation (ESM → CommonJS)
// - Decorator transformation
// - JSX transformation

// 2. Custom transformers (user-defined)
// - Add logging
// - Rename variables
// - Remove console.log
// - Add assertions
// - Code generation
```

---

## 2. Compiler Transformer API

```typescript
import * as ts from 'typescript';

// Transformer factory: creates a transformer for a source file
type TransformerFactory<T extends ts.Node> = (
  context: ts.TransformationContext
) => (node: T) => T;

// Transformation context
interface TransformationContext {
  factory: ts.NodeFactory;
  suspendEmitHelper(name: string, args: readonly ts.Expression[], hasEffects?: boolean): void;
  readEmitHelpers(): readonly ts.EmitHelper[];
  requestEmitHelper(helper: ts.EmitHelper): void;
  setEmitResolver(resolver: ts.EmitResolver): void;
}

// Usage in compilation
const program = ts.createProgram(['src/index.ts'], {
  target: ts.ScriptTarget.ES2020,
  module: ts.ModuleKind.ESNext,
});

program.emit(
  undefined, // sourceFile
  undefined, // writeFile
  undefined, // cancellationToken
  false,     // emitOnlyDtsFiles
  [          // transformers
    // Before transformers (run first)
    myBeforeTransformer,
    // After transformers (run after before transformers)
    myAfterTransformer,
  ]
);
```

---

## 3. Custom Transformers

### Basic Transformer

```typescript
import * as ts from 'typescript';

// Simple transformer that adds a comment to every function
function addFunctionCommentTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile: ts.SourceFile) => {
    function visit(node: ts.Node): ts.Node {
      if (ts.isFunctionDeclaration(node)) {
        // Get function name
        const funcName = node.name?.getText(sourceFile) || 'anonymous';
        
        // Add JSDoc comment
        const comment = ts.factory.createSingleLineComment(
          ` Function: ${funcName}`
        );
        
        // Create new node with comment
        return ts.factory.createFunctionDeclaration(
          node.modifiers,
          node.asteriskToken,
          node.name,
          node.typeParameters,
          node.parameters,
          node.type,
          node.body
        );
      }
      
      return ts.visitEachChild(node, visit, context);
    }
    
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}
```

### Rename Variables Transformer

```typescript
import * as ts from 'typescript';

function renameTransformer(
  renames: Record<string, string>
): ts.TransformerFactory<ts.SourceFile> {
  return (context: ts.TransformationContext) => {
    return (sourceFile: ts.SourceFile) => {
      function visit(node: ts.Node): ts.Node {
        // Rename identifiers
        if (ts.isIdentifier(node) && renames[node.text]) {
          return ts.factory.createIdentifier(renames[node.text]);
        }
        
        // Rename property access
        if (ts.isPropertyAccessExpression(node)) {
          const newNode = ts.visitEachChild(node, visit, context);
          if (ts.isPropertyAccessExpression(newNode) && 
              renames[newNode.name.text]) {
            return ts.factory.createPropertyAccessExpression(
              newNode.expression,
              ts.factory.createIdentifier(renames[newNode.name.text])
            );
          }
        }
        
        return ts.visitEachChild(node, visit, context);
      }
      
      return ts.visitNode(sourceFile, visit) as ts.SourceFile;
    };
  };
}

// Usage
program.emit(undefined, undefined, undefined, false, [
  renameTransformer({
    oldName: 'newName',
    getUser: 'fetchUser',
  })
]);
```

---

## 4. AST Transformation

### Creating New Nodes

```typescript
import * as ts from 'typescript';

// Node factory methods
const factory = ts.factory;

// Create identifiers
const id = factory.createIdentifier('myVariable');

// Create string literals
const str = factory.createStringLiteral('hello');

// Create numeric literals
const num = factory.createNumericLiteral('42');

// Create function declarations
const func = factory.createFunctionDeclaration(
  undefined, // modifiers
  undefined, // asteriskToken
  'add',     // name
  undefined, // typeParameters
  [
    factory.createParameterDeclaration(
      undefined, undefined,
      'a', undefined,
      factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword),
      undefined
    ),
    factory.createParameterDeclaration(
      undefined, undefined,
      'b', undefined,
      factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword),
      undefined
    ),
  ],
  factory.createKeywordTypeNode(ts.SyntaxKind.NumberKeyword),
  factory.createBlock([
    factory.createReturnStatement(
      factory.createBinaryExpression(
        id,
        ts.SyntaxKind.PlusToken,
        factory.createIdentifier('b')
      )
    ),
  ])
);

// Create variable statements
const varStatement = factory.createVariableStatement(
  undefined,
  factory.createVariableDeclarationList(
    [
      factory.createVariableDeclaration(
        'result',
        undefined,
        undefined,
        factory.createNumericLiteral('0')
      ),
    ],
    ts.NodeFlags.Const
  )
);
```

### Traversal Patterns

```typescript
import * as ts from 'typescript';

// Depth-first traversal
function deepVisit(node: ts.Node, visitor: (node: ts.Node) => void) {
  visitor(node);
  ts.forEachChild(node, child => deepVisit(child, visitor));
}

// Conditional traversal
function findNodes(
  node: ts.Node,
  predicate: (node: ts.Node) => boolean
): ts.Node[] {
  const results: ts.Node[] = [];
  
  function visit(current: ts.Node) {
    if (predicate(current)) {
      results.push(current);
    }
    ts.forEachChild(current, visit);
  }
  
  visit(node);
  return results;
}

// Find all function declarations
const functions = findNodes(sourceFile, ts.isFunctionDeclaration);

// Find all variable declarations
const variables = findNodes(sourceFile, ts.isVariableDeclaration);
```

---

## 5. Before/After Transformers

```typescript
import * as ts from 'typescript';

// Before transformer: runs before emit
function beforeTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile) => {
    console.log('Before transformer running');
    
    function visit(node: ts.Node): ts.Node {
      // Transform before code generation
      if (ts.isStringLiteral(node) && node.text === 'DEBUG') {
        return ts.factory.createStringLiteral('PRODUCTION');
      }
      return ts.visitEachChild(node, visit, context);
    }
    
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}

// After transformer: runs after before transformers
function afterTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile) => {
    console.log('After transformer running');
    
    function visit(node: ts.Node): ts.Node {
      // Transform after before transformers
      if (ts.isNumericLiteral(node)) {
        // Double all numeric literals
        const value = parseInt(node.text) * 2;
        return ts.factory.createNumericLiteral(value.toString());
      }
      return ts.visitEachChild(node, visit, context);
    }
    
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}

// Usage
program.emit(
  undefined,
  undefined,
  undefined,
  false,
  [beforeTransformer], // Before transformers
  [afterTransformer]   // After transformers
);
```

---

## 6. Transformer Factories

```typescript
import * as ts from 'typescript';

// Factory pattern for configurable transformers
function createLogTransformer(
  logLevel: 'info' | 'warn' | 'error'
): ts.TransformerFactory<ts.SourceFile> {
  return (context: ts.TransformationContext) => {
    return (sourceFile: ts.SourceFile) => {
      function visit(node: ts.Node): ts.Node {
        if (ts.isCallExpression(node)) {
          const expression = node.expression;
          
          // Wrap console.log calls
          if (ts.isPropertyAccessExpression(expression) &&
              expression.expression.getText(sourceFile) === 'console' &&
              expression.name.text === 'log') {
            
            const logMethod = ts.factory.createPropertyAccessExpression(
              ts.factory.createIdentifier('console'),
              ts.factory.createIdentifier(logLevel)
            );
            
            return ts.factory.createCallExpression(
              logMethod,
              undefined,
              node.arguments
            );
          }
        }
        
        return ts.visitEachChild(node, visit, context);
      }
      
      return ts.visitNode(sourceFile, visit) as ts.SourceFile;
    };
  };
}

// Usage
program.emit(undefined, undefined, undefined, false, [
  createLogTransformer('warn'), // console.log → console.warn
]);
```

### Parameterized Transformers

```typescript
import * as ts from 'typescript';

function createAssertTransformer(
  asserts: Array<{
    condition: string;
    message: string;
  }>
): ts.TransformerFactory<ts.SourceFile> {
  return (context) => {
    return (sourceFile) => {
      function visit(node: ts.Node): ts.Node {
        if (ts.isIfStatement(node)) {
          const conditionText = node.expression.getText(sourceFile);
          
          const matchingAssert = asserts.find(
            a => a.condition === conditionText
          );
          
          if (matchingAssert) {
            const assertCall = ts.factory.createCallExpression(
              ts.factory.createIdentifier('console.error'),
              undefined,
              [ts.factory.createStringLiteral(matchingAssert.message)]
            );
            
            const assertStatement = ts.factory.createExpressionStatement(assertCall);
            
            return ts.factory.createIfStatement(
              node.expression,
              ts.factory.createBlock([assertStatement, node.thenStatement]),
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

## 7. Practical Transformer Examples

### Remove Console.log Transformer

```typescript
import * as ts from 'typescript';

function removeConsoleLogTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile) => {
    function visit(node: ts.Node): ts.Node {
      if (ts.isExpressionStatement(node) &&
          ts.isCallExpression(node.expression)) {
        const expression = node.expression;
        
        if (ts.isPropertyAccessExpression(expression) &&
            expression.expression.getText(sourceFile) === 'console' &&
            ['log', 'debug', 'info'].includes(expression.name.text)) {
          // Remove the statement entirely
          return undefined as any;
        }
      }
      
      return ts.visitEachChild(node, visit, context);
    }
    
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}
```

### Add Error Handling Transformer

```typescript
import * as ts as ts;

function addErrorHandlingTransformer(
  context: ts.TransformationContext
): ts.TransformerFactory<ts.SourceFile> {
  return (sourceFile) => {
    function visit(node: ts.Node): ts.Node {
      if (ts.isFunctionDeclaration(node) && node.body) {
        // Wrap function body in try-catch
        const tryStatement = ts.factory.createTryStatement(
          node.body,
          ts.factory.createCatchClause(
            ts.factory.createVariableDeclaration('error'),
            ts.factory.createBlock([
              ts.factory.createExpressionStatement(
                ts.factory.createCallExpression(
                  ts.factory.createPropertyAccessExpression(
                    ts.factory.createIdentifier('console'),
                    'error'
                  ),
                  undefined,
                  [ts.factory.createIdentifier('error')]
                )
              ),
              ts.factory.createThrowStatement(
                ts.factory.createIdentifier('error')
              ),
            ])
          ),
          undefined
        );
        
        return ts.factory.createFunctionDeclaration(
          node.modifiers,
          node.asteriskToken,
          node.name,
          node.typeParameters,
          node.parameters,
          node.type,
          ts.factory.createBlock([tryStatement])
        );
      }
      
      return ts.visitEachChild(node, visit, context);
    }
    
    return ts.visitNode(sourceFile, visit) as ts.SourceFile;
  };
}
```

### TypeScript Plugin Example

```typescript
// ts-plugin.ts
import * as ts from 'typescript';

function init(modules: { typescript: typeof ts }) {
  const ts = modules.typescript;

  function create(info: ts.server.PluginCreateInfo) {
    const proxy: ts.LanguageService = {
      ...info.languageService,
      getSemanticDiagnostics(fileName) {
        const prior = info.languageService.getSemanticDiagnostics(fileName);
        
        // Add custom diagnostics
        const sourceFile = info.languageService
          .getProgram()
          ?.getSourceFile(fileName);
        
        if (sourceFile) {
          // Find all 'any' types and warn
          function visit(node: ts.Node) {
            if (node.kind === ts.SyntaxKind.AnyKeyword) {
              prior.push({
                file: sourceFile,
                start: node.getStart(),
                length: node.getEnd() - node.getStart(),
                messageText: 'Avoid using "any" type',
                category: ts.DiagnosticCategory.Warning,
                code: 9999,
                source: 'my-plugin',
              });
            }
            ts.forEachChild(node, visit);
          }
          visit(sourceFile);
        }
        
        return prior;
      },
    };

    return proxy;
  }

  return { create };
}

export = init;
```

---

## Interview Questions

**Q1**: What are transformers in the TypeScript Compiler API?
**A**: Transformers are functions that modify the AST during compilation. They receive the AST, make modifications (rename variables, add code, remove code), and return the modified AST.

**Q2**: What is the difference between before and after transformers?
**A**: Before transformers run before code generation. After transformers run after before transformers. Before transformers can modify the AST freely; after transformers work with the already-transformed AST.

**Q3**: How do you create a custom transformer?
**A**: Create a transformer factory function that takes `TransformationContext` and returns a function that takes a `SourceFile` and returns a transformed `SourceFile`. Use `ts.visitNode` and `ts.forEachChild` for traversal.

**Q4**: What is a transformer factory and why is it needed?
**A**: A transformer factory is a function that creates a transformer for each source file. It's needed because TypeScript compiles multiple files and each needs its own transformer instance with its own context.

**Q5**: How do you traverse and modify an AST?
**A**: Use `ts.visitNode(node, visitor)` for the root, `ts.forEachChild(node, visitor)` for children, and `ts.visitEachChild(node, visitor, context)` for transformation. Check node types with `ts.isFunctionDeclaration()`, etc.
