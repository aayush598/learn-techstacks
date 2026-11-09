# TypeScript Documentation and Handbook Navigation

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — Use the Handbook for language guides, the compiler reference for options, and release notes for version-specific behavior.

## Syntax

```ts
// https://www.typescriptlang.org/docs/handbook/
// https://www.typescriptlang.org/tsconfig
// https://devblogs.microsoft.com/typescript/
const docs = ["handbook", "reference", "release-notes"] as const;
type Docs = (typeof docs)[number];
```

## Examples

### Basic

```ts
const handbookSections = [
  "Everyday Types",
  "Narrowing",
  "Generics",
  "Type Manipulation",
] as const;

type Section = (typeof handbookSections)[number];
```

### Practical

```ts
// npx tsc --showConfig   # resolved compiler options
// npx tsc --help --all   # all compiler flags
const commands = ["--showConfig", "--help --all", "--noEmit"] as const;
```

### Advanced / edge cases

```ts
const handbookMap = {
  narrowing: "https://www.typescriptlang.org/docs/handbook/2/narrowing.html",
  generics: "https://www.typescriptlang.org/docs/handbook/2/generics.html",
  tsconfig: "https://www.typescriptlang.org/tsconfig",
} as const;

type HandbookTopic = keyof typeof handbookMap;

function docsUrl(topic: HandbookTopic): string {
  return handbookMap[topic];
}
```

## Key points

- The Handbook teaches language features with guided examples.
- The reference documents every compiler option and its interactions.
- Release notes describe new features, deprecations, and breaking changes.
- The Playground is the fastest way to test a documented example.
- Search diagnostic codes such as `TS2322` to find targeted explanations.
- Check the version selector so the docs match your compiler.

## Gotchas

- Blog posts and tutorials may describe older versions or non-strict defaults.
- Handbook examples often omit strictness assumptions; verify against your config.
- Documentation can lag newly shipped features.

## Best practice

- Prefer official documentation, and verify every example with your installed compiler.
- Link to version-specific docs in code reviews and issue reports.
