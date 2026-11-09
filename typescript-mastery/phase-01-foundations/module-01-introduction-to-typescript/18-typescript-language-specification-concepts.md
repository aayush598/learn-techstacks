# TypeScript Language Specification Concepts

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — The specification defines the grammar, type system, assignability rules, and emit semantics that the compiler implements.

## Syntax

```ts
type Digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
const digit: Digit = 7;
```

## Examples

### Basic

```ts
// A type denotes a set of values.
type Bool = true | false;
const flag: Bool = true;
```

### Practical

```ts
// Assignability is structural: a value with more properties satisfies a smaller type.
type Named = { name: string };
type Person = { name: string; age: number };

const person: Person = { name: "Ada", age: 36 };
const named: Named = person; // ✅ Person is assignable to Named
```

### Advanced / edge cases

```ts
// Function parameter positions are checked contravariantly under strictFunctionTypes.
type Handler = (event: { type: string; x: number }) => void;
type GeneralHandler = (event: { type: string }) => void;

const general: GeneralHandler = (event) => {
  console.log(event.type);
};

const handler: Handler = general; // ✅ accepts a broader parameter
```

## Key points

- The spec defines lexical grammar, syntax, and the static type system.
- Types are best understood as sets of values; assignability is set inclusion.
- Structural typing compares members rather than nominal names.
- Declaration merging, overload resolution, and emit rules are specified behaviors.
- The compiler may implement features beyond the published specification.
- The specification can lag the current compiler release.

## Gotchas

- The Handbook is a guide, not the normative specification.
- Some specification text describes older TypeScript versions and may be outdated.
- Compiler behavior can differ by version even when the spec has not changed.

## Best practice

- Use the spec to reason about semantics and the Handbook to learn usage.
- Verify surprising behavior against the compiler version you actually run.
