# Avoiding Unnecessary Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Most assertions can be replaced by inference, narrowing, generics, or `satisfies`, keeping the compiler's safety intact.

## Syntax

```ts
const inferred = value; // let TypeScript infer
const checked = value satisfies Type; // validate without widening
```

## Examples

### Basic

```ts
const name = "Ada"; // ✅ inferred as string
const count = 42; // ✅ inferred as number

const redundant = 42 as number; // ✅ compiles, but adds nothing
console.log(name, count, redundant);
```

### Practical

```ts
const el = document.querySelector("#app");

if (el instanceof HTMLDivElement) {
  el.innerHTML = "Ready"; // ✅ narrowed, no assertion needed
}

const value: string | number = Math.random() > 0.5 ? "x" : 1;
const text = typeof value === "string" ? value : String(value); // ✅ narrowed
console.log(text);
```

### Advanced / edge cases

```ts
type Config = {
  mode: "dark" | "light";
  retries?: number;
};

// `satisfies` validates the shape while preserving literal types.
const config = {
  mode: "dark",
  retries: 3,
} satisfies Config;

const mode: "dark" = config.mode; // ✅ literal preserved
console.log(mode);
```

## Key points

- Inference already produces precise types for literals and object literals.
- Narrowing (`typeof`, `in`, `instanceof`) proves a type at runtime.
- Generics preserve relationships that assertions would flatten.
- `satisfies` checks a value without overriding its inferred type.
- Removing an assertion restores future compile-time protection.

## Gotchas

- Redundant assertions mask later type changes.

```ts
const value = "hello" as string;
// If the source type changes, the assertion keeps compiling silently.
```

- Asserting instead of narrowing can crash on the other branch.

```ts
const value: string | number = 1;
const length = (value as string).length;
// compiles, but length is undefined at runtime
```

- `satisfies` is not a cast: it still rejects invalid values.

```ts
const bad = { mode: "auto" } satisfies Config;
// ❌ Error: Type '"auto"' is not assignable to type '"dark" | "light"'. (TS2322)
```

## Best practice

- Delete assertions that do not change the type; they only hide information.
- Reach for `satisfies` when you need validation without widening.
