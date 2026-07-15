# TypeScript Compiler API

## Table of Contents

1. [Compiler API Overview](#1-compiler-api-overview)
2. [Program Object](#2-program-object)
3. [CompilerHost](#3-compilerhost)
4. [SourceFile and AST Nodes](#4-sourcefile-and-ast-nodes)
5. [Type Checker API](#5-type-checker-api)
6. [Creating Custom Compilers](#6-creating-custom-compilers)
7. [program.emit()](#7-programemit)
8. [Diagnostics](#8-diagnostics)
9. [Custom Transformers](#9-custom-transformers)

---

## 1. Compiler API Overview

The TypeScript Compiler API allows you to programmatically compile TypeScript code, analyze types, and transform ASTs.

```typescript
import * as ts from 'typescript';

// Core concepts:
// 1. Program — represents a compilation
// 2. CompilerHost — file system abstraction
// 3. SourceFile — parsed source file
// 4. TypeChecker — type analysis
// 5. Transformer — AST transformation

// Basic compilation
const program = ts.createProgram(['src/index.ts'], {
  target: ts.ScriptTarget.ES2020,
  module: ts.ModuleKind.ESNext,
  strict: true,
});

const diagnostics = ts.getPreEmitDiagnostics(program);
diagnostics.forEach(diagnostic => {
  if (diagnostic.file) {
    const { line, character } = ts.getLineAndCharacterOfPosition(
      diagnostic.file,
      diagnostic.start!
    );
    const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
    console.log(`${diagnostic.file.fileName} (${line + 1},${character + 1}): ${message}`);
  }
});
```

---

## 2. Program Object

The Program object represents a complete TypeScript compilation.

```typescript
import * as ts from 'typescript';

// Create a program
const program = ts.createProgram(
  ['src/index.ts', 'src/utils.ts'], // Root files
  {
    target: ts.ScriptTarget.ES2020,
    module: ts.ModuleKind.CommonJS,
    outDir: './dist',
    rootDir: './src',
    strict: true,
    declaration: true,
    sourceMap: true,
  }
);

// Program methods
const sourceFiles = program.getSourceFiles(); // All parsed files
const diagnostics = ts.getPreEmitDiagnostics(program); // Type errors
const emitResult = program.emit(); // Emit JavaScript output
const checker = program.getTypeChecker(); // Get type checker
const compilerOptions = program.getCompilerOptions(); // Get options

// Get specific source file
const indexFile = program.getSourceFile('src/index.ts');

// Get file diagnostics
const fileDiagnostics = program.getSemanticDiagnostics(indexFile);

// Check if file is part of compilation
const isSourceFile = program.isSourceFileFromLibrary(indexFile!);
const isIncluded = program.isSourceFileDefaultLibrary(indexFile!);
```

---

## 3. CompilerHost

The CompilerHost provides file system abstraction for the compiler.

```typescript
import * as ts from 'typescript';

// Default compiler host
const defaultHost = ts.createCompilerHost({
  target: ts.ScriptTarget.ES2020,
  module: ts.ModuleKind.ESNext,
});

// Custom compiler host
const customHost: ts.CompilerHost = {
  ...defaultHost,
  
  // Custom file reading
  getSourceFile(fileName, languageVersion) {
    if (fileName.includes('virtual')) {
      return ts.createSourceFile(
        fileName,
        `export const virtual = true;`,
        languageVersion
      );
    }
    return defaultHost.getSourceFile(fileName, languageVersion);
  },

  // Custom file writing
  writeFile(fileName, text) {
    console.log(`Writing: ${fileName}`);
    defaultHost.writeFile!(fileName, text);
  },

  // Custom file existence check
  fileExists(fileName) {
    if (fileName.includes('virtual')) return true;
    return defaultHost.fileExists!(fileName);
  },

  // Custom directory existence check
  directoryExists(directoryName) {
    return defaultHost.directoryExists!(directoryName);
  },

  // Custom module resolution
  resolveModuleNames(moduleNames, containingFile) {
    return moduleNames.map(moduleName => {
      const resolved = ts.resolveModuleName(
        moduleName,
        containingFile,
        {},
        customHost
      );
      return resolved.resolvedModule;
    });
  },
};
```

---

## 4. SourceFile and AST Nodes

### Parsing Source Files

```typescript
import * as ts from 'typescript';

// Parse a source file
const sourceCode = `
  function add(a: number, b: number): number {
    return a + b;
  }
  const result = add(1, 2);
`;

const sourceFile = ts.createSourceFile(
  'example.ts',
  sourceCode,
  ts.ScriptTarget.ES2020,
  true // Set parent nodes
);

// Traverse AST nodes
function visit(node: ts.Node) {
  if (ts.isFunctionDeclaration(node)) {
    console.log(`Function: ${node.name?.getText(sourceFile)}`);
  }
  
  if (ts.isVariableDeclaration(node)) {
    console.log(`Variable: ${node.name.getText(sourceFile)}`);
  }
  
  ts.forEachChild(node, visit);
}

visit(sourceFile);
```

### AST Node Types

```typescript
import * as ts from 'typescript';

// Common AST node types
const sourceFile = ts.createSourceFile(
  'example.ts',
  `
    interface User {
      name: string;
      age: number;
    }
    
    class UserService {
      private users: User[] = [];
      
      async findUser(id: string): Promise<User | null> {
        return this.users.find(u => u.name === id) ?? null;
      }
    }
    
    type ID = string | number;
    
    const PI = 3.14159;
  `,
  ts.ScriptTarget.ES2020
);

// Node type checks
function analyzeNode(node: ts.Node) {
  if (ts.isInterfaceDeclaration(node)) {
    console.log(`Interface: ${node.name.text}`);
    node.members.forEach(member => {
      if (ts.isPropertySignature(member)) {
        console.log(`  Property: ${member.name.getText(sourceFile)}`);
      }
    });
  }

  if (ts.isClassDeclaration(node)) {
    console.log(`Class: ${node.name?.text}`);
    node.members.forEach(member => {
      if (ts.isPropertyDeclaration(member)) {
        console.log(`  Property: ${member.name.getText(sourceFile)}`);
      }
      if (ts.isMethodDeclaration(member)) {
        console.log(`  Method: ${member.name.getText(sourceFile)}`);
      }
    });
  }

  if (ts.isTypeAliasDeclaration(node)) {
    console.log(`Type Alias: ${node.name.text}`);
  }

  if (ts.isVariableStatement(node)) {
    node.declarationList.forEachDeclaration(decl => {
      if (ts.isIdentifier(decl.name)) {
        console.log(`Variable: ${decl.name.text}`);
      }
    });
  }

  ts.forEachChild(node, analyzeNode);
}

analyzeNode(sourceFile);
```

---

## 5. Type Checker API

```typescript
import * as ts from 'typescript';

const program = ts.createProgram(['src/index.ts'], {
  strict: true,
  target: ts.ScriptTarget.ES2020,
});

const checker = program.getTypeChecker();
const sourceFile = program.getSourceFile('src/index.ts')!;

// Get type information
function analyzeTypes(node: ts.Node) {
  if (ts.isVariableDeclaration(node) && node.name) {
    const symbol = checker.getSymbolAtLocation(node.name);
    if (symbol) {
      const type = checker.getTypeOfSymbolAtLocation(symbol, node);
      const typeString = checker.typeToString(type);
      console.log(`${node.name.text}: ${typeString}`);
    }
  }

  if (ts.isFunctionDeclaration(node) && node.name) {
    const symbol = checker.getSymbolAtLocation(node.name);
    if (symbol) {
      const type = checker.getTypeOfSymbolAtLocation(symbol, node);
      const signatures = type.getCallSignatures();
      signatures.forEach(sig => {
        const returnType = checker.typeToString(sig.getReturnType());
        const params = sig.parameters.map(p => {
          const paramType = checker.typeToString(
            checker.getTypeOfSymbolAtLocation(p, node)
          );
          return `${p.name}: ${paramType}`;
        });
        console.log(`${node.name!.text}(${params.join(', ')}): ${returnType}`);
      });
    }
  }

  ts.forEachChild(node, analyzeTypes);
}

analyzeTypes(sourceFile);
```

---

## 6. Creating Custom Compilers

```typescript
import * as ts from 'typescript';

// Custom compiler that adds logging
function compileWithLogging(fileNames: string[], options: ts.CompilerOptions) {
  const program = ts.createProgram(fileNames, options);
  const emitResult = program.emit();

  const allDiagnostics = ts.getPreEmitDiagnostics(program).concat(emitResult.diagnostics);

  allDiagnostics.forEach(diagnostic => {
    if (diagnostic.file) {
      const { line, character } = ts.getLineAndCharacterOfPosition(
        diagnostic.file,
        diagnostic.start!
      );
      const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
      console.log(`${diagnostic.file.fileName}(${line + 1},${character + 1}): ${message}`);
    } else {
      console.log(ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'));
    }
  });

  const exitCode = emitResult.diagnostics.length > 0 ? 1 : 0;
  console.log(`Process exiting with code '${exitCode}'.`);
  process.exit(exitCode);
}

// Usage
compileWithLogging(
  ['src/index.ts'],
  {
    target: ts.ScriptTarget.ES2020,
    module: ts.ModuleKind.ESNext,
    outDir: './dist',
    strict: true,
  }
);
```

---

## 7. program.emit()

```typescript
import * as ts from 'typescript';

const program = ts.createProgram(['src/index.ts'], {
  target: ts.ScriptTarget.ES2020,
  module: ts.ModuleKind.ESNext,
  outDir: './dist',
  declaration: true,
  sourceMap: true,
});

// Basic emit
const emitResult = program.emit();

// Emit with custom transformer
const emitResult2 = program.emit(
  undefined, // Target source file (undefined = all)
  undefined, // Write callback (undefined = use host)
  undefined, // CancellationToken
  false,     // emitOnlyDtsFiles
  []         // Custom transformers
);

// Emit specific files
const sourceFile = program.getSourceFile('src/index.ts');
program.emit(
  sourceFile, // Only emit this file
  (fileName, text) => {
    console.log(`Emitting: ${fileName}`);
    ts.sys.writeFile(fileName, text);
  }
);

// Emit with custom transformers
const transformResult = program.emit(
  undefined,
  undefined,
  undefined,
  false,
  [
    // Before transformers
    (context) => (sourceFile) => {
      return ts.visitNode(sourceFile, (node) => {
        // Transform nodes
        return node;
      });
    }
  ]
);
```

---

## 8. Diagnostics

```typescript
import * as ts from 'typescript';

const program = ts.createProgram(['src/index.ts'], { strict: true });

// Pre-emit diagnostics (type errors)
const preEmitDiagnostics = ts.getPreEmitDiagnostics(program);

// Post-emit diagnostics (emit errors)
const emitResult = program.emit();
const postEmitDiagnostics = emitResult.diagnostics;

// All diagnostics
const allDiagnostics = preEmitDiagnostics.concat(postEmitDiagnostics);

// Format diagnostics
function formatDiagnostic(diagnostic: ts.Diagnostic): string {
  if (diagnostic.file) {
    const { line, character } = ts.getLineAndCharacterOfPosition(
      diagnostic.file,
      diagnostic.start!
    );
    const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
    return `${diagnostic.file.fileName}(${line + 1},${character + 1}): ${message}`;
  }
  return ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
}

// Log all errors
allDiagnostics.forEach(diagnostic => {
  console.log(formatDiagnostic(diagnostic));
});

// Check for specific error codes
const hasErrors = allDiagnostics.some(
  d => d.category === ts.DiagnosticCategory.Error
);
if (hasErrors) {
  console.error('Compilation failed!');
  process.exit(1);
}
```

---

## 9. Custom Transformers

```typescript
import * as ts from 'typescript';

// Transformer that renames variables
function renameTransformer(context: ts.TransformationContext) {
  return (sourceFile: ts.SourceFile) => {
    function visit(node: ts.Node): ts.Node {
      // Rename 'oldName' to 'newName'
      if (ts.isIdentifier(node) && node.text === 'oldName') {
        return ts.factory.createIdentifier('newName');
      }
      return ts.visitEachChild(node, visit, context);
    }
    return ts.visitNode(sourceFile, visit);
  };
}

// Transformer factory
function createRenameTransformer(
  renames: Record<string, string>
): ts.TransformerFactory<ts.SourceFile> {
  return (context: ts.TransformationContext) => {
    return (sourceFile: ts.SourceFile) => {
      function visit(node: ts.Node): ts.Node {
        if (ts.isIdentifier(node) && renames[node.text]) {
          return ts.factory.createIdentifier(renames[node.text]);
        }
        return ts.visitEachChild(node, visit, context);
      }
      return ts.visitNode(sourceFile, visit);
    };
  };
}

// Use in compilation
const program = ts.createProgram(['src/index.ts'], {
  target: ts.ScriptTarget.ES2020,
});

program.emit(
  undefined,
  undefined,
  undefined,
  false,
  [
    createRenameTransformer({
      oldFunction: 'newFunction',
      oldVariable: 'newVariable',
    })
  ]
);
```

---

## Interview Questions

**Q1**: What is the TypeScript Compiler API and when would you use it?
**A**: The Compiler API allows programmatic compilation, type analysis, and AST transformation. Use it for: custom build tools, code generators, linters, type analyzers, IDE plugins, and build system integrations.

**Q2**: What is the difference between `Program` and `CompilerHost`?
**A**: `Program` represents a complete compilation (files, options, diagnostics). `CompilerHost` is the file system abstraction that the program uses to read/write files.

**Q3**: How do you traverse an AST in TypeScript?
**A**: Use `ts.forEachChild(node, visitor)` to visit child nodes, or `ts.visitNode(node, visitor)` with a transformation context. Check node types with `ts.isFunctionDeclaration()`, `ts.isVariableDeclaration()`, etc.

**Q4**: What are transformers in the Compiler API?
**A**: Transformers are functions that modify the AST during compilation. They can rename variables, add code, remove code, or transform syntax. They run in before/after phases.

**Q5**: How do you get type information for a variable?
**A**: Use `checker.getSymbolAtLocation(node)` to get the symbol, then `checker.getTypeOfSymbolAtLocation(symbol, node)` to get the type. Use `checker.typeToString(type)` to display it.
