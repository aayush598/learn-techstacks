# Assertion versus Annotation

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — An annotation is checked against the value, while an assertion overrides the compiler's check.

## Syntax

```ts
const annotated: Type = value; // verified
const asserted = value as Type; // trusted
```

## Examples

### Basic

```ts
const name: string = "Ada"; // ✅ string is assignable to string
const id = "42" as string; // ✅ assertion, no check on the source

console.log(name, id);
```

### Practical

```ts
type Status = "idle" | "loading" | "done";

// Annotation checks the value against the union.
const a: Status = "done"; // ✅

// Assertion claims the value belongs to the union.
const raw: string = "done";
const b = raw as Status; // ✅ compiles, but an invalid string would slip through

console.log(a, b);
```

### Advanced / edge cases

```ts
type Config = {
  mode: "dark" | "light";
  retries?: number;
};

// `satisfies` validates without widening or overriding the inferred type.
const config = {
  mode: "dark",
  retries: 3,
} satisfies Config;

const mode: "dark" = config.mode; // ✅ literal type preserved
console.log(mode);
```

## Key points

- Annotations participate in assignability checking in both directions.
- Assertions only check that source and target sufficiently overlap.
- Annotations widen literals; `satisfies` preserves the inferred literal type.
- Assertions can make an incorrect value compile; annotations cannot.
- Use annotations at API boundaries and assertions only as a last resort.

## Gotchas

- An annotation rejects a mismatched value.

```ts
const n: number = "42";
// ❌ Error: Type 'string' is not assignable to type 'number'. (TS2322)
```

- An assertion can silently accept a wrong runtime value.

```ts
const raw: unknown = 42;
const label = raw as string;
console.log(label.toUpperCase()); // compiles, fails at runtime
```

- An annotation on an object widens string literals unless you add `as const` or `satisfies`.

## Best practice

- Prefer annotations and `satisfies` so the compiler verifies as much as possible.
- Reserve assertions for cases where the type is known but not provable from the value.
