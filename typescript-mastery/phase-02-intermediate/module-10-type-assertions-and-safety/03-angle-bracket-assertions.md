# Angle-Bracket Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — `<Type>value` is the legacy assertion syntax; it is unavailable in `.tsx` files and generally discouraged.

## Syntax

```ts
const value = <Type>expression;
```

## Examples

### Basic

```ts
const raw: unknown = "hello";
const text = <string>raw;

console.log(text.toUpperCase()); // "HELLO"
```

### Practical

```ts
function identity<T>(value: T): T {
  return value;
}

const count = <number>identity(42);
const label = <string>identity("items");

console.log(count + 1); // 43
console.log(label.length); // 5
```

### Advanced / edge cases

```ts
type Point = { x: number; y: number };

const parsePoint = (value: unknown): Point => {
  const candidate = <Point>value; // ✅ only valid in a .ts file
  return { x: candidate.x, y: candidate.y };
};

console.log(parsePoint({ x: 1, y: 2 }));
```

In a `.tsx` file the same line is parsed as JSX:

```ts
// ❌ Error: JSX element 'string' has no corresponding closing tag. (TS17008)
const text = <string>raw;
```

## Key points

- Angle brackets and `as` are equivalent assertions with different grammar.
- `.tsx` files treat `<Type>` as the start of a JSX element.
- The syntax is retained for compatibility with older TypeScript code.
- Use `as` in shared codebases that contain `.tsx` files.
- Angle-bracket assertions do not validate anything at runtime.

## Gotchas

- Copying `<T>value` into a `.tsx` component breaks the parser.

```ts
// ❌ Error: JSX element 'T' has no corresponding closing tag. (TS17008)
```

- Nesting angle-bracket assertions is hard to read: `<Foo<Bar>>value`.
- The syntax cannot express `as const`; use a const assertion instead.

## Best practice

- Standardize on `as` so code works identically in `.ts` and `.tsx`.
- Avoid mixing both assertion styles in one project.
