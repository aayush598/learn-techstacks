# Preventing Accidental `any`

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — `any` disables type checking, so eliminate implicit and explicit `any` in favor of `unknown`, generics, and narrow types.

## Syntax

```ts
function handle(value: unknown): void; // safe default
function handle(value: any): void; // ❌ opts out of checking
```

## Examples

### Basic

```ts
function log(value) {
  // ❌ Error: Parameter 'value' implicitly has an 'any' type. (TS7006)
  console.log(value);
}

function safeLog(value: unknown): void {
  console.log(value); // ✅ unknown accepts every value
}
```

### Practical

```ts
// ✅ Generic preserves the relationship between input and output.
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const n = first([1, 2, 3]); // number | undefined
const s = first(["a", "b"]); // string | undefined

console.log(n, s);
```

### Advanced / edge cases

```ts
// ❌ `any` spreads through every expression it touches.
const data: any = JSON.parse('{"user":{"name":"Ada"}}');
const name: number = data.user.name;
console.log(name.toFixed(2)); // compiles, throws at runtime: name.toFixed is not a function

// ✅ `unknown` forces a check before use.
const safe: unknown = JSON.parse('{"user":{"name":"Ada"}}');
if (typeof safe === "object" && safe !== null && "user" in safe) {
  console.log(safe.user); // unknown — still requires narrowing
}
```

## Key points

- `noImplicitAny` (included in `strict`) turns accidental `any` into errors.
- `unknown` is the type-safe counterpart: it accepts values but permits no operations.
- Generics preserve type relationships that `any` erases.
- `any` propagates: one `any` can silently untype a whole expression chain.
- `JSON.parse`, untyped libraries, and `catch` are common sources of `any`.

## Gotchas

- `any` disables checks in both directions, including assignment to narrow types.

```ts
const value: any = "not a number";
const n: number = value; // ✅ no error, wrong at runtime
console.log(n.toFixed()); // throws at runtime
```

- `Array<any>` and `Record<string, any>` hide mistakes in every element access.
- `any` in a public API forces every consumer to lose safety.

## Best practice

- Enable `noImplicitAny` and lint with `@typescript-eslint/no-explicit-any`.
- Use `unknown` plus narrowing at boundaries, and generics inside reusable code.
