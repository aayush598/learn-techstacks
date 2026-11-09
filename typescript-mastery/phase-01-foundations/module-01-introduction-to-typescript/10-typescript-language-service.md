# TypeScript Language Service

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — The language service exposes the compiler's type information to editors for completion, diagnostics, rename, and navigation.

## Syntax

```ts
const name: string = "Ada";
name.toUpperCase();
```

## Examples

### Basic

```ts
// Hover, completion, and go-to-definition all use inferred types.
const values = [1, 2, 3];
const doubled = values.map((value) => value * 2); // number[]
```

### Practical

```ts
import * as ts from "typescript";

const fileName = "example.ts";
const source = "const value = 42; value.";
const host: ts.LanguageServiceHost = {
  getScriptFileNames: () => [fileName],
  getScriptVersion: () => "0",
  getScriptSnapshot: (name) =>
    name === fileName ? ts.ScriptSnapshot.fromString(source) : undefined,
  getCurrentDirectory: () => "/",
  getCompilationSettings: () => ({ strict: true }),
  getDefaultLibFileName: (options) => ts.getDefaultLibFilePath(options),
  fileExists: ts.sys.fileExists,
  readFile: ts.sys.readFile,
  readDirectory: ts.sys.readDirectory,
};

const service = ts.createLanguageService(host);
const completions = service.getCompletionsAtPosition(fileName, source.length, {});
console.log(completions?.entries.map((entry) => entry.name));
```

### Advanced / edge cases

```ts
import * as ts from "typescript";

function describe(diagnostic: ts.Diagnostic): string {
  const category = ts.DiagnosticCategory[diagnostic.category];
  const code = `TS${diagnostic.code}`;
  const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, "\n");
  const position =
    diagnostic.file && diagnostic.start !== undefined
      ? diagnostic.file.getLineAndCharacterOfPosition(diagnostic.start)
      : undefined;

  return position
    ? `${position.line + 1}:${position.character + 1} ${category} ${code}: ${message}`
    : `${category} ${code}: ${message}`;
}
```

## Key points

- The language service is the API behind editor features, not a separate type checker.
- It uses the same checker as `tsc`, so results should agree given the same version and config.
- It supports completions, hover, signatures, diagnostics, rename, and references.
- Editors usually run a `tsserver` process and communicate with it over a protocol.
- Unsaved buffers are analyzed through snapshots supplied by the editor.

## Gotchas

- Editor diagnostics can differ when the editor bundles a different TypeScript version.
- A stale `tsserver` process can show errors that a fresh compile does not.
- The service analyzes source text; it does not execute the program.

## Best practice

- Select the workspace TypeScript version in your editor so it matches CI.
- Use the language service for fast feedback, but verify releases with `tsc --noEmit`.
