# Understanding TypeScript Warnings and Diagnostics

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript reports errors, warnings, suggestions, and messages as diagnostics; many "warnings" become errors only when a compiler flag is enabled.

## Syntax

```ts
type DiagnosticCategory = "error" | "warning" | "suggestion" | "message";
```

## Examples

### Basic

```ts
// tsconfig: "noUnusedLocals": true
const unused = 42;
// ❌ Error: 'unused' is declared but its value is never read. (TS6133)
```

### Practical

```ts
// tsconfig: "noImplicitReturns": true
function sign(value: number): number {
  if (value >= 0) return 1;
  // ❌ Error: Function lacks ending return statement and return type does not include 'undefined'. (TS2366)
}
```

### Advanced / edge cases

```ts
import * as ts from "typescript";

function describe(diagnostic: ts.Diagnostic): string {
  const category = ts.DiagnosticCategory[diagnostic.category];
  const code = `TS${diagnostic.code}`;
  const text = ts.flattenDiagnosticMessageText(diagnostic.messageText, "\n");
  return `${category} ${code}: ${text}`;
}
```

## Key points

- Diagnostics have a category: error, warning, suggestion, or message.
- The CLI primarily reports errors; editors also surface suggestions and refactors.
- `noUnusedLocals`, `noUnusedParameters`, and `noImplicitReturns` are opt-in checks.
- `skipLibCheck` suppresses diagnostics from declaration files, not your source.
- Diagnostic codes are stable enough to search for explanations and fixes.

## Gotchas

- `strict` does not enable unused-variable or unused-parameter checks.
- Treating every suggestion as an error can create noise; choose flags intentionally.
- `skipLibCheck` can hide real conflicts between dependency declarations.

## Best practice

- Enable unused checks in CI to catch dead code early.
- Treat compiler diagnostics as errors in automated builds and review warnings deliberately.
